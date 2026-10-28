# WordCraft — diretrizes e padrões

Última atualização: 2026-10-28.

## Onde estão as regras

[AGENTS.md](../../AGENTS.md) é a fonte obrigatória para segurança, licenças, organização dos commits, branch e autorização de testes/push. [CLAUDE.md](../../CLAUDE.md) complementa a rotina; instruções antigas conflitantes cedem às regras locais de AGENTS.md.

| Ao alterar | Consultar |
|---|---|
| Relações entre bibliotecas e separação engine/UI | [Arquitetura](../architecture.md) e [mapa de camadas](../../xtask/src/layers.rs) |
| Nomes de pacotes, features e dependências | [Manifesto do workspace](../../Cargo.toml) e manifesto do módulo |
| Formatação e lints | Configurações do repositório e lints do manifesto; não inventar uma convenção paralela |
| Comandos e parâmetros públicos | Registro do engine e documentação de automação no [índice](../INDEX.md) |
| Recursos visuais, fontes e fixtures | Política de assets e clean-room em [AGENTS](../../AGENTS.md) |
| Novos comportamentos | Contrato do módulo, testes existentes e documento de paridade correspondente |

## Aplicação prática

Antes de criar um módulo, procure um vizinho da mesma camada e siga seus nomes e organização. Identificadores de comando são contratos compartilhados entre interfaces: confira o registro antes de nomear uma nova ação. Regras de tratamento de erros, preservação de dados e exceções de plataforma devem ser lidas no projeto, sem importar exceções de outro Craft.

Para uma mudança em abertura/salvamento, consulte a biblioteca de formato e seu contrato de round-trip. Para um comando novo, localize seu registro, a ligação de UI/CLI/automação e os testes de histórico/erros aplicáveis. Para mudanças visuais, consulte o tema e os componentes já usados pela interface.

## Documentação

Use nomes descritivos em Markdown, links relativos e uma fonte por assunto. Adote `Última atualização: AAAA-MM-DD` nos novos documentos; preserve o formato de data/histórico dos existentes ao atualizá-los. O ciclo e a matriz de atualização ficam em [maintenance.md](maintenance.md).

[Voltar ao índice](../INDEX.md).
