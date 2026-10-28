# WordCraft — visão geral

Última atualização: 2026-10-28.

Processamento de texto com estilos, tabelas, paginação, revisão e formatos de escritório.

O escopo e o estágio do produto são descritos no [README](../../README.md) e no [ROADMAP](../../ROADMAP.md); limitações são acompanhadas em [gaps.md](../gaps.md).

## Tecnologias e estrutura

Workspace Rust/Cargo, interface egui/eframe e distribuição desktop e WebAssembly. Versões, features e dependências exatas: [Cargo.toml](../../Cargo.toml) e [Cargo.lock](../../Cargo.lock). A organização de camadas está em [architecture.md](../architecture.md).

| Pasta | Onde começar |
|---|---|
| [apps/](../../apps/) | Entradas desktop, CLI e web; cada aplicativo tem seu manifesto. |
| [crates/](../../crates/) | Bibliotecas por responsabilidade; veja o mapa de funcionalidades. |
| [xtask/](../../xtask/) | Ferramentas de desenvolvimento e verificações; consultar antes de executar. |
| [docs/](../../docs/) | Referências técnicas, guias e acompanhamento de paridade. |
| [packaging/](../../packaging/) | Receitas e recursos de distribuição por plataforma. |
| [assets/](../../assets/) | Recursos do produto; atribuição e licenças seguem AGENTS.md. |
| [.github/workflows/](../../.github/workflows/) | Automação de CI e publicação; não equivale a autorização de execução. |

## Localização rápida

- Fluxos e bibliotecas: [funcionalidades](features.md).
- Execução, diagnóstico e entrega: [operação](operations.md).
- Motivações, limites e próxima tarefa: [contexto](context.md).

[Voltar ao índice](../INDEX.md).
