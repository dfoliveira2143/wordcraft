# WordCraft — operação

Última atualização: 2026-10-28.

## Preparação

Execute os comandos na raiz deste projeto, em PowerShell. Pré-requisitos e opções de plataforma ficam no [README](../../README.md); versões declaradas ficam no [Cargo.toml](../../Cargo.toml). Para desktop/web, a documentação atual requer Rust 1.95 ou posterior. Consulte também a configuração local de Cargo antes de definir caminhos de fontes ou de compilação.

```powershell
git status --short
git branch --show-current
git log -5 --oneline
```

A política de branch, preservação de alterações alheias e commits é a de [AGENTS.md](../../AGENTS.md). Os comandos de execução abaixo podem compilar dependências e demorar. Quando usados para testar ou validar código, explique necessidade e alcance e aguarde a confirmação exigida por AGENTS.md. Estão documentados aqui; não foram executados na criação desta base.

## Executar

```powershell
cargo run --release -p wordcraft -- --sample
```

Para operações headless e controle da janela, use os contratos próprios do projeto; portas, autenticação e formato de parâmetros variam entre os Craft:

- [mcp.md](../mcp.md)
- [control-protocol.md](../control-protocol.md)

## Testar e verificar código — após confirmação

Exemplo limitado ao engine; escolha outro pacote conforme a alteração e combine previamente o alcance:

```powershell
cargo test -p wordcraft-engine --lib
```

Esse exemplo não substitui os requisitos de conclusão. As verificações completas, condicionais e exceções estão em [AGENTS.md](../../AGENTS.md) e nas referências abaixo. CI completo pode compilar muitos pacotes, exemplos e alvos WASM; não o execute apenas para se orientar.



## Depurar

1. Reproduza com entrada sintética mínima e registre plataforma, comando, resultado esperado e observado.
2. Separe falha do engine de falha da UI usando a interface headless documentada. Para falha visual, use o canal próprio ou snapshot disponível e leia a imagem resultante.
3. Consulte os locais de logs e opções de diagnóstico do README e das referências operacionais; não copie dados pessoais, tokens ou bibliotecas do usuário para os documentos.
4. Registre a causa e o resultado das verificações autorizadas, incluindo testes não executados e dependências ausentes.

## Entregar e publicar

Revise o diff e os arquivos selecionados antes do commit. Para documentação passiva, aplique a exceção de validação de [AGENTS.md](../../AGENTS.md):

```powershell
git diff --check
git diff --cached --check
```

Push e release são ações distintas: siga a autorização e o destino definidos em AGENTS.md. Não trate receitas antigas de publicação como autorização. Quando o usuário solicitar push, confira remoto e commits de saída antes de enviar `development` para `origin/development`.

Receitas de empacotamento e publicação:

- [releasing.md](../releasing.md)
- [Packaging](../../packaging/)
- [Workflows](../../.github/workflows/)

[Voltar ao índice](../INDEX.md).
