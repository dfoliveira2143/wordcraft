# WordCraft — funcionalidades e módulos

Última atualização: 2026-10-28.

## Fluxo principal

| Etapa | Entradas | Responsabilidade e dependências | Saídas |
|---|---|---|---|
| Abrir e editar | DOCX, formatos de texto e comandos de edição | [doc](../../crates/doc/), [docx](../../crates/docx/), [docbin](../../crates/docbin/), [formats](../../crates/formats/), [engine](../../crates/engine/) | Documento com histórias, seções e histórico |
| Avaliar e produzir saída | Estado editado e parâmetros de saída | [fonts](../../crates/fonts/), [layout](../../crates/layout/), [render](../../crates/render/), [pdf](../../crates/pdf/), [proof](../../crates/proof/) | Páginas diagramadas, PDF e documento salvo |
| Acesso pelo usuário ou agente | Gestos, argumentos CLI ou chamadas estruturadas | [apps](../../apps/), [engine](../../crates/engine/) e interfaces descritas abaixo | Estado atualizado, resposta ou erro; comportamento detalhado nos contratos |

A tabela mostra o caminho conceitual, não uma garantia de suporte a todos os formatos. APIs, estruturas, unidades, efeitos colaterais e limites ficam na [arquitetura](../architecture.md), nos documentos de assunto e nos módulos indicados.

## Contratos e exemplos de uso

- [typing-parity.md](../typing-parity.md)
- [layout-parity.md](../layout-parity.md)
- [recovery.md](../recovery.md)
- [spelling-dictionaries.md](../spelling-dictionaries.md)
- [zotero.md](../zotero.md)
- [control-protocol.md](../control-protocol.md)
- [mcp.md](../mcp.md)

## Inventário de bibliotecas

Responsabilidades resumidas a partir dos manifestos e comentários de módulo do checkout. As dependências listadas são as internas diretas declaradas em `dependencies` (incluindo condicionais); não incluem dependências de teste/build nem expansão de features. O manifesto de cada linha é a fonte exata.

| Módulo / manifesto | Responsabilidade declarada | Dependências internas diretas |
|---|---|---|
| [control-key](../../crates/control-key/Cargo.toml) | WordCraft control-port key file: where it lives and how to read it (shared by the app and the MCP bridge) | Nenhuma declarada nesta categoria |
| [doc](../../crates/doc/Cargo.toml) | WordCraft document model: stories, paragraphs, runs, tables, sections, styles, numbering, fields, notes, comments, revisions; edit primitives | `wordcraft-geom` |
| [docbin](../../crates/docbin/Cargo.toml) | WordCraft reader for the Word 97-2003 binary file format (.doc, [MS-DOC]) | `wordcraft-doc`, `wordcraft-geom` |
| [docx](../../crates/docx/Cargo.toml) | WordCraft DOCX (OOXML WordprocessingML) reader and writer | `wordcraft-doc`, `wordcraft-geom` |
| [engine](../../crates/engine/Cargo.toml) | WordCraft engine: session, selection, undo, the command registry (every action is a command), Word's command catalog, file I/O dispatch | `wordcraft-doc`, `wordcraft-docbin`, `wordcraft-docx`, `wordcraft-fonts`, `wordcraft-formats`, `wordcraft-geom`, `wordcraft-layout`, `wordcraft-pdf`, `wordcraft-proof`, `wordcraft-render` |
| [fonts](../../crates/fonts/Cargo.toml) | WordCraft fonts: font database (bundled OFL + system), metrics, glyph outlines, shaping | Nenhuma declarada nesta categoria |
| [formats](../../crates/formats/Cargo.toml) | WordCraft import/export: plain text, Markdown, HTML, RTF, OpenDocument Text and LaTeX | `wordcraft-doc`, `wordcraft-geom` |
| [geom](../../crates/geom/Cargo.toml) | WordCraft geometry and units: points, twips, EMU, inches, centimetres; rectangles; measurement parsing | Nenhuma declarada nesta categoria |
| [layout](../../crates/layout/Cargo.toml) | WordCraft layout: shaping, line breaking, tabs, lists, tables, pagination, headers/footers, hit testing | `wordcraft-doc`, `wordcraft-fonts`, `wordcraft-geom`, `wordcraft-metafile`, `wordcraft-proof` |
| [mcp](../../crates/mcp/Cargo.toml) | WordCraft MCP server: every command as a tool, headless or bridged to the running app | `wordcraft-control-key`, `wordcraft-doc`, `wordcraft-engine`, `wordcraft-render` |
| [metafile](../../crates/metafile/Cargo.toml) | WordCraft metafiles: parses Windows WMF and EMF records into a neutral vector model (paths and bitmaps) | Nenhuma declarada nesta categoria |
| [pdf](../../crates/pdf/Cargo.toml) | WordCraft PDF export (craft-pdf / Krilla): embedded font subsets with selectable text, links, outline, tagging | `wordcraft-doc`, `wordcraft-fonts`, `wordcraft-geom`, `wordcraft-layout`, `wordcraft-metafile` |
| [proof](../../crates/proof/Cargo.toml) | WordCraft proofing per language: spelling, suggestions, grammar checks and hyphenation for English (public-domain word list) and Polish (installed Hunspell dictionary, TeX patterns) | Nenhuma declarada nesta categoria |
| [render](../../crates/render/Cargo.toml) | WordCraft rasteriser: pages and thumbnails from the layout display list (vello_cpu), PNG/JPEG export | `wordcraft-doc`, `wordcraft-fonts`, `wordcraft-geom`, `wordcraft-layout`, `wordcraft-metafile` |
| [ui-egui](../../crates/ui-egui/Cargo.toml) | WordCraft egui front end (Word-style ribbon UI); swappable: nothing below depends on it | `wordcraft-doc`, `wordcraft-engine`, `wordcraft-fonts`, `wordcraft-geom`, `wordcraft-layout`, `wordcraft-render`, `wordcraft-zotero` |
| [zotero](../../crates/zotero/Cargo.toml) | WordCraft Zotero integration: Zotero's word-processor wire protocol, answered against an engine Session | `wordcraft-doc`, `wordcraft-engine`, `wordcraft-formats` |

Ao mudar uma entrada, saída ou dependência, atualize primeiro o contrato do módulo e depois esta navegação. [Voltar ao índice](../INDEX.md).
