"""GitHub Actions: prepare an immutable merge candidate, then publish only tested commits.

Only the copy checked out from the trusted default branch executes with write permissions.
Candidate/application code executes in a different workflow with a read-only token.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

REPO = os.environ.get("GITHUB_REPOSITORY", "")
OWNER, _, NAME = REPO.partition("/")
MAIN = "main"
PREFIX = "sync/upstream-"
CONTEXT = "artcraft/validated"
APP_BOT = "upstream-sync-dfoliveira2143[bot]"
PROTECTED = [".github/workflows", ".github/artcraft-sync.py", "docs/branding.md"]


def branding_problems(base, candidate):
    """Inspect Git objects as data; never execute a candidate's checker or application."""
    problems = []
    policy = git("show", f"{candidate}:docs/branding.md", check=False)
    if policy.returncode or "Creative Workshop" not in policy.stdout:
        problems.append("A política Creative Workshop ainda não está integrada à proposta.")
    paths = git("ls-tree", "-r", "--name-only", candidate).splitlines()
    for path in paths:
        if re.search(r"(?:^|/)(?:artcraft-(?:logo|mark)[^/]*|LICENSE-brand\.txt\.(?:png|svg))$", path, re.I):
            problems.append(f"Marca restrita presente: {path}")
    # New presentation text is checked even when the merge has no conflicts. Legal
    # notices, dependency provenance and historical documentation remain permitted.
    diff = git("diff", "--no-ext-diff", "--unified=0", base, candidate, "--",
               "README.md", "apps", "crates", "packaging")
    path = ""
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        value = line[1:].strip()
        if path.endswith((".attribution", "LICENSE", "NOTICE")) or "/licenses/" in path:
            continue
        if value.startswith(("//", "#", "<!--")):
            continue
        if re.search(r"copyright|©|LegalCopyright|based on|not affiliated|not an official|restricted|trademark", value, re.I):
            continue
        if re.search(r"getartcraft\.com|discord\.gg/artcraft|\bArtCraft\b", value):
            problems.append(f"Revisar identidade pública em {path}: {value[:160]}")
    return problems


def branding_gate(base, candidate, branch, url):
    problems = branding_problems(base, candidate)
    if not problems:
        return True
    status(candidate, "failure", "Identidade Creative Workshop exige revisão", url)
    pull_request(branch, "A proteção de identidade bloqueou a integração:\n\n" +
                 "\n".join("- " + p for p in problems[:40]), url)
    return False


def api(route, method="GET", body=None):
    req = Request("https://api.github.com/" + route,
                  data=json.dumps(body).encode() if body is not None else None,
                  method=method, headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
                  "Accept": "application/vnd.github+json", "Content-Type": "application/json",
                  "X-GitHub-Api-Version": "2022-11-28"})
    with urlopen(req, timeout=60) as response:
        data = response.read()
    return json.loads(data) if data else None


def git(*args, check=True):
    p = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8")
    if check and p.returncode:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip())
    return p.stdout.strip() if check else p


def status(sha, state, description, url):
    api(f"repos/{REPO}/statuses/{sha}", "POST", {
        "context": CONTEXT, "state": state, "description": description[:140], "target_url": url})


def pull_request(branch, reason, url):
    query = urlencode({"state": "open", "head": f"{OWNER}:{branch}", "base": MAIN})
    prs = api(f"repos/{REPO}/pulls?{query}")
    body = (f"@{OWNER}, a atualização oficial precisa de intervenção.\n\n{reason}\n\n"
            f"Origem: https://github.com/storytold/{NAME}\nExecução: {url}\n\n"
            "A branch principal não foi alterada. Nenhum conflito foi resolvido automaticamente. "
            "Revise esta branch e os testes antes de integrar.\n\n"
            "<!-- artcraft-upstream-sync -->")
    if prs:
        api(f"repos/{REPO}/pulls/{prs[0]['number']}", "PATCH", {"body": body})
        return prs[0]["number"]
    pr = api(f"repos/{REPO}/pulls", "POST", {
        "title": "Atualização oficial: intervenção necessária", "head": branch,
        "base": MAIN, "body": body, "maintainer_can_modify": False})
    return pr["number"]


def notify_error(reason, url):
    # Also covers infrastructure/API failures before a candidate could be created.
    issues = api(f"repos/{REPO}/issues?state=open&creator={APP_BOT}&per_page=100")
    title = "Sincronização oficial: falha de infraestrutura"
    body = f"@{OWNER}\n\n{reason}\n\nExecução: {url}\n\nNenhum histórico foi sobrescrito."
    old = next((i for i in issues if i["title"] == title and "pull_request" not in i), None)
    if old:
        api(f"repos/{REPO}/issues/{old['number']}", "PATCH", {"body": body})
    else:
        api(f"repos/{REPO}/issues", "POST", {"title": title, "body": body})


def ancestor(a, b):
    p = git("merge-base", "--is-ancestor", a, b, check=False)
    if p.returncode not in (0, 1):
        raise RuntimeError(p.stderr)
    return p.returncode == 0


def prepare(url):
    meta = api(f"repos/storytold/{NAME}")
    upstream_branch = meta["default_branch"]
    git("fetch", "--no-tags", "origin", f"refs/heads/{MAIN}")
    base = git("rev-parse", "FETCH_HEAD")
    git("fetch", "--no-tags", f"https://github.com/storytold/{NAME}.git", f"refs/heads/{upstream_branch}")
    upstream = git("rev-parse", "FETCH_HEAD")
    if ancestor(upstream, base):
        print("A origem oficial já está integrada.")
        return
    common = git("merge-base", base, upstream)
    if git("diff", "--name-only", common, upstream, "--", *PROTECTED):
        # Do not publish unreviewed workflows even on a candidate/conflict branch:
        # an App push can trigger newly introduced workflows immediately.
        notify_error("A origem alterou workflows ou o controlador. Revisão manual necessária antes de publicar uma proposta.", url)
        return
    branch = f"{PREFIX}{upstream[:12]}-{base[:12]}"
    previous = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    if previous:
        # Reuse the exact candidate; never replace a branch or discard human edits.
        sha = previous.split()[0]
        git("fetch", "--no-tags", "origin", f"refs/heads/{branch}")
        parents = git("show", "-s", "--format=%P", sha).split()
        if parents != [base, upstream]:
            pull_request(branch, "A proposta existente contém conflito ou alterações posteriores; preservada para revisão.", url)
            return
    else:
        git("checkout", "--detach", base)
        git("config", "user.name", "github-actions[bot]")
        git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
        merge = git("-c", "core.hooksPath=/dev/null", "-c", "merge.renormalize=false",
                    "-c", "rerere.enabled=false", "merge", "--no-ff", "--no-edit", upstream,
                    "-m", f"Merge storytold/{NAME}@{upstream}\n\nArtcraft-Base: {base}", check=False)
        if merge.returncode:
            conflicts = git("diff", "--name-only", "--diff-filter=U")
            git("merge", "--abort", check=False)
            if not conflicts:
                raise RuntimeError("Não foi possível preparar a integração: " + merge.stderr)
            git("push", "origin", f"{upstream}:refs/heads/{branch}")
            pull_request(branch, "Conflitos detectados:\n```text\n" + conflicts + "\n```", url)
            return
        sha = git("rev-parse", "HEAD")
        git("push", "origin", f"{sha}:refs/heads/{branch}")
    # Test code and workflow must not be allowed to change the trusted integration machinery.
    # Any change to this policy is an intentional owner operation, not an upstream merge side effect.
    changed = git("diff", "--name-only", base, sha, "--", *PROTECTED)
    if changed:
        status(sha, "failure", "A proposta altera a configuração de sincronização", url)
        pull_request(branch, "A proposta altera a configuração de sincronização; revise antes de autorizar.", url)
        return
    if not branding_gate(base, sha, branch, url):
        return
    status(sha, "pending", "Verificações Linux da proposta em execução", url)
    api(f"repos/{REPO}/actions/workflows/artcraft-check.yml/dispatches", "POST", {"ref": branch})
    print(f"Proposta {branch} enviada para verificações explícitas, sem aprovação manual.")


def finish(event, url):
    run = event["workflow_run"]
    branch, sha = run["head_branch"], run["head_sha"]
    if not re.fullmatch(r"sync/upstream-[0-9a-f]{12}-[0-9a-f]{12}", branch or ""):
        return
    if run["event"] != "workflow_dispatch" or run["head_repository"]["full_name"] != REPO:
        return
    if run["actor"]["login"] not in (OWNER, APP_BOT):
        return
    workflow = api(f"repos/{REPO}/actions/workflows/artcraft-check.yml")
    if run["workflow_id"] != workflow["id"]:
        raise RuntimeError("Workflow de verificação inesperado")
    if run["conclusion"] != "success":
        status(sha, "failure", "As verificações falharam ou foram interrompidas", run["html_url"])
        pull_request(branch, f"Resultado das verificações: **{run['conclusion']}**.", run["html_url"])
        return
    # Fetch by branch, verify immutable head, then verify the exact tested merge's parents.
    git("fetch", "--no-tags", "origin", f"refs/heads/{MAIN}")
    base = git("rev-parse", "FETCH_HEAD")
    git("fetch", "--no-tags", "origin", f"refs/heads/{branch}")
    if ancestor(sha, base):
        print("Esta proposta já foi integrada.")
        return
    if git("rev-parse", "FETCH_HEAD") != sha:
        pull_request(branch, "A proposta foi alterada depois dos testes; é necessária nova validação.", url)
        return
    parents = git("show", "-s", "--format=%P", sha).split()
    if len(parents) != 2 or parents[0] != base:
        pull_request(branch, "A main mudou desde a preparação; a combinação atual ainda não foi testada.", url)
        return
    if branch != f"{PREFIX}{parents[1][:12]}-{base[:12]}":
        raise RuntimeError("Metadados da proposta não correspondem aos pais do merge")
    if git("diff", "--name-only", base, sha, "--", *PROTECTED):
        raise RuntimeError("A proposta altera workflows ou o controlador confiável")
    # The recorded run succeeded. Require every actual job to have succeeded (optional jobs
    # may be skipped) and require the mandatory gate to be present and green.
    jobs = []
    page = 1
    while True:
        part = api(f"repos/{REPO}/actions/runs/{run['id']}/attempts/{run['run_attempt']}/jobs?per_page=100&page={page}")["jobs"]
        jobs += part
        if len(part) < 100:
            break
        page += 1
    if not any(j["name"] == "gate" and j["conclusion"] == "success" for j in jobs):
        raise RuntimeError("O teste obrigatório gate não terminou com sucesso")
    if any(j["conclusion"] not in ("success", "skipped") for j in jobs):
        raise RuntimeError("Há verificações sem sucesso")
    if not branding_gate(base, sha, branch, url):
        return
    status(sha, "success", "Todos os testes configurados passaram no commit exato", run["html_url"])
    # Normal, non-force push. GitHub branch protection enforces required statuses, including
    # any the owner adds later. A concurrent main update causes a non-fast-forward rejection.
    pushed = git("push", "origin", f"{sha}:refs/heads/{MAIN}", check=False)
    if pushed.returncode:
        pull_request(branch, "Publicação bloqueada por proteção de branch, concorrência ou permissão:\n```text\n" + pushed.stderr[-3000:] + "\n```", url)
        return
    query = urlencode({"state": "open", "head": f"{OWNER}:{branch}", "base": MAIN})
    for pr in api(f"repos/{REPO}/pulls?{query}"):
        # GitHub usually marks this PR merged automatically after the push; never delete it.
        api(f"repos/{REPO}/issues/{pr['number']}/comments", "POST", {
            "body": f"Integrado após todas as verificações: {run['html_url']}"})
    print(f"Integrado {sha}, preservando os dois históricos.")


def main():
    if not REPO or OWNER != "dfoliveira2143":
        raise RuntimeError("Este workflow está restrito à conta autorizada")
    url = f"https://github.com/{REPO}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
    try:
        if os.environ.get("ARTCRAFT_VERIFY_APP") == "true":
            repository = api(f"repos/{REPO}")
            if repository["full_name"] != REPO:
                raise RuntimeError("Unexpected token repository")
            print("App authentication verified; no branches or commits modified.")
            return
        event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
        if os.environ["GITHUB_EVENT_NAME"] == "workflow_run":
            finish(event, url)
        else:
            prepare(url)
    except Exception as error:
        message = f"{type(error).__name__}: {error}"
        print(message, file=sys.stderr)
        try:
            notify_error(message, url)
        except Exception as notification_error:
            print(f"Falha ao registrar aviso: {notification_error}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
