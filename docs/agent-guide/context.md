# WordCraft — decisões, contexto e pendências

Última atualização: 2026-10-28.

## Decisões e suas fontes

| Escolha | Motivo documentado / onde aprofundar |
|---|---|
| Engine separado das interfaces | Permite alcançar o comportamento por diferentes interfaces e manter UI substituível; [arquitetura](../architecture.md). |
| Comandos/ferramentas como contrato | Centraliza execução e comportamento entre UI e automação; [arquitetura](../architecture.md). |
| Preservação do trabalho e tratamento de entradas inválidas | Evita perda de dados; regras e exceções específicas em [AGENTS](../../AGENTS.md). |
| Layout produz uma lista de desenho | Renderização de páginas e exportação PDF usam o resultado da paginação; comportamento de digitação tem referência própria em typing-parity.md. Fonte: [arquitetura](../architecture.md) e referências do [índice](../INDEX.md). |
| Base versionada com índice e links | Permite retomada em um checkout sem histórico de conversa e evita divergência entre cópias; decisão documental desta tarefa, 2026-10-28. |

Não atribua uma justificativa histórica a uma decisão apenas por inferência do código. Quando ela não estiver registrada, marque como hipótese e investigue antes de consolidar.


## Estado e próximos passos

O estado atual permanece em [ROADMAP](../../ROADMAP.md), [gaps](../gaps.md) e [roadmap detalhado](../roadmap.md). Consulte as evidências da [avaliação de paridade](../target-app-parity.md) antes de tratar uma funcionalidade como concluída. Não replique percentuais ou listas de tarefas neste guia.

Ao retomar: leia a demanda do usuário, consulte a lacuna correspondente, confira o estado real do checkout e só então escolha os módulos. `plan/STATUS.md`, se existir, pode complementar esse percurso; não é pré-requisito nem substitui o acompanhamento versionado.

## Pendências documentais identificadas em 2026-10-28

| Pendência | Impacto | Próxima ação / critério de conclusão |
|---|---|---|
| Referências a `plan/` e regras compartilhadas fora do checkout | Uma sessão nova pode não ter esses arquivos. O checkout compartilhado de craftrules não foi encontrado nos caminhos locais consultados. | Usar as regras versionadas locais; ao precisar de uma justificativa ausente, registrar contexto não sensível no documento técnico apropriado e ligá-lo aqui. |
| Documentos de arquitetura misturam fotografias históricas e atualizações recentes | Contagens ou descrições antigas não comprovam o estado de todos os módulos. | Conferir o módulo ao alterá-lo e atualizar a seção afetada com data e evidência; não recalcular métricas sem execução autorizada. |
| Contratos detalhados variam entre módulos | O inventário fornece navegação, não especifica toda API. | Ao tocar um módulo sem contrato, documentar entradas, saídas, erros, dependências e exemplo em seu README/doc técnico; atualizar o link em funcionalidades. |

Essas são pendências da base, não novos bugs confirmados do produto. Limitações funcionais continuam em `gaps.md`. Não foi feita nova medição de desempenho, cobertura ou paridade nesta tarefa.

## Registro de decisões futuras

No documento do assunto (ou em ADR quando envolver várias áreas), registre: data; problema; alternativas consideradas; decisão e motivo; consequências; limites; evidência; links para implementação e verificações. Adicione aqui apenas a referência. Uma hipótese deve ser distinguida de uma decisão aceita.

[Voltar ao índice](../INDEX.md).

## Identidade independente — 2026-10-28

A edição local usa Creative Workshop. Consulte a [política de identidade](../branding.md) antes de integrar alterações upstream ou gerar uma distribuição. A validação de código e a reconstrução dos pacotes dependem de autorização; os binários existentes não foram atualizados.
