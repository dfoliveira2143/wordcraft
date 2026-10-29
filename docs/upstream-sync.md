# Official upstream synchronization

Updated: 2026-10-29.

GitHub Actions checks the matching `storytold` repository daily at 12:00 UTC
(09:00 in Sao Paulo). GitHub may delay scheduled runs. The owner keeps `main`
as a personal copy of official releases and commits; local development remains
on `development`. No Codex scheduled task or running personal computer is needed.

`ARTCRAFT_SYNC_ENABLED=true` enables the existing sync and finish workflows.
The repository-scoped GitHub App prepares an immutable merge candidate. The
existing complete Linux quality gate must pass on that candidate before main
advances, with no force push or automatic conflict resolution. Changes to the
sync controller, its regression tests, or the three artcraft workflows require
review; other official upstream workflow changes are allowed.

Only merge conflicts open an intervention PR mentioning the owner. Repeated
checks of the same conflict do not post another notice. Other blockers remain
in Actions logs and are retried on a later daily run. GitHub's own account-level
Actions notification preferences are separate. Independent Dependabot PRs in
this copy are not automatically merged. Local files and development are untouched.
