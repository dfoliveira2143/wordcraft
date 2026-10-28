# WordCraft — manutenção da base

Última atualização: 2026-10-28.

## Antes de cada tarefa

1. Leia [AGENTS](../../AGENTS.md), o [índice](../INDEX.md) e o contexto do assunto afetado.
2. Confira branch, alterações locais e commits recentes. Não assuma que o estado é o da sessão anterior.
3. Consulte a arquitetura, o contrato do módulo e as pendências relevantes antes de implementar. O pedido atual do usuário define a tarefa.
4. Se encontrar informação vencida, corrija quando houver evidência; caso contrário, registre a lacuna com impacto, fonte e próxima ação em [contexto](context.md) ou na fonte funcional correspondente.

## Ao concluir ou interromper

Atualize a documentação junto da unidade de trabalho. Não deixe conhecimento necessário apenas no chat, em `plan/` ou em `log/` ignorados. Registre o que mudou, por quê, como reproduzir, verificações realizadas e pendências. Em trabalho incompleto, registre o ponto exato de retomada, arquivos envolvidos e próximo passo verificável; não declare concluído o que não foi verificado.

| Mudança | Documento que deve receber o detalhe |
|---|---|
| Propósito, tecnologias ou entrada do projeto | README / arquitetura; ajustar o link de visão geral |
| Módulo, fluxo ou contrato | README do módulo ou referência técnica; atualizar funcionalidades |
| Convenção de contribuição | AGENTS ou guia canônico de contribuição; padrões apenas aponta para ele |
| Comando operacional, requisito ou diagnóstico | Guia de desenvolvimento/publicação existente; ajustar operação |
| Decisão ou restrição | Documento técnico/ADR; link em contexto |
| Limitação funcional ou marco | gaps, paridade e roadmap, conforme regras locais |
| Lacuna da própria documentação | contexto, com critério de resolução |
| Novo documento ou caminho alterado | índice central e todos os links afetados |

## Fonte única e datas

- Antes de criar um arquivo, procure se o assunto já tem uma fonte. Amplie essa fonte e use links nos demais lugares.
- Atualize a data de cada documento realmente modificado. Uma data nova não significa que o restante do projeto foi revalidado.
- Separe fatos observados, decisões aceitas, hipóteses e trabalho planejado.
- Exemplos devem declarar diretório de execução, shell, pré-requisitos, entradas e saídas. Não inclua segredos nem caminhos pessoais obrigatórios.
- Arquivos gerados ou consumidos por build/testes seguem seu fluxo próprio e não são cobertos automaticamente pela exceção documental.

## Revisão de conclusão

Revise o diff, confira links relativos e coerência entre instruções e execute `git diff --check`. Siga [AGENTS.md](../../AGENTS.md) para a exceção documental, autorização de testes e critérios de commit. Relate explicitamente o que não foi executado. Não avance datas ou indicadores de documentos alheios à alteração.

Esta rotina é uma obrigação das sessões futuras ao executar tarefas; não cria uma automação periódica nem garante revisão fora dessas sessões.

[Voltar ao índice](../INDEX.md).
