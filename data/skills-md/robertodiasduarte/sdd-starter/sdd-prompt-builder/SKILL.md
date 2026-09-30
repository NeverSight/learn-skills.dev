---
name: sdd-prompt-builder
license: MIT
description: "Gera, refina e otimiza prompts de produção para LLMs com contrato de saída explícito, critérios de completude, tratamento de contexto ausente e verificação concisa. Usar quando o usuário pedir para criar ou melhorar prompts destinados a runtime, ou quando um fluxo SDD design/build criar ou alterar system prompts, passes de pipeline, classificadores, sintetizadores, prompts em edge/worker/runtime, arquivos **/prompts/**, system prompts inline ou templates em _shared. Não usar para documentação humana, prompts internos de orquestração SDD, emails, notificações ou copy transacional de UI."
metadata:
  author: Roberto Dias Duarte
---

# Prompt Builder

Produzir um único prompt operacional pronto para uso em runtime. Priorizar o menor prompt que preserve clareza, controle de saída, recuperabilidade e fidelidade ao contexto fornecido.

## Quick start

1. Identificar a tarefa real e o artefato que o modelo-alvo deve produzir.
2. Ler [references/prompt-building-rules.md](references/prompt-building-rules.md) e aplicar somente as seções justificadas pela tarefa.
3. Se a chamada vier de SDD, ler também [references/sdd-integration.md](references/sdd-integration.md) antes de gerar qualquer prompt.
4. Usar [references/output-template.md](references/output-template.md) como esqueleto flexível; omitir seções vazias ou desnecessárias.
5. Retornar somente um TXT BLOCK contendo o prompt final. Não envolver o resultado em código TypeScript, constante exportada ou arquivo de destino.

## Quando usar / Quando não usar

Os gatilhos positivos estão definidos no frontmatter e devem ser a fonte de descoberta da skill.

Após a skill ser acionada:
- Não aplicar a documentação narrativa, READMEs, BRAINSTORM/DEFINE/DESIGN ou outros textos destinados a humanos.
- Não aplicar a prompts internos dos agentes de orquestração do próprio fluxo SDD.
- Não aplicar a emails, notificações ou copy transacional de UI.
- No `/build`, se houver drift detectado sem inventário de LLM Prompts registrado, interromper a geração direta e exigir atualização do DESIGN conforme [references/sdd-integration.md](references/sdd-integration.md).

## Dados necessários

Para uso manual, receber:
- objetivo do prompt;
- contexto ou material de referência, quando houver;
- contrato de saída desejado ou informações suficientes para inferi-lo;
- decisões já fechadas que não devem ser reabertas, quando houver.

Para uso via SDD, receber o contrato compilado descrito em [references/sdd-integration.md](references/sdd-integration.md). Não ler DEFINE, DESIGN ou BUILD_REPORT por conta própria quando o caller já for responsável por compilar o contexto.

## Procedimento passo a passo

1. Identificar o objetivo real, o consumidor da saída e o nível de autonomia esperado.
2. Definir primeiro o contrato exato de saída: tipo, estrutura, conteúdo obrigatório, limites e fallback permitido.
3. Converter cautelas e restrições em regras operacionais curtas, sem repetições.
4. Incluir `<formulas>` sempre que houver cálculo, métrica, indicador, razão ou score; declarar operandos e operações explicitamente.
5. Definir comportamento para contexto ausente, ambíguo ou não verificável. Nunca inventar dados.
6. Incluir verificação interna curta quando estrutura, transformação, extração ou criticidade justificarem.
7. Incluir contrato de completude para lotes, slots, listas, inventários ou seções obrigatórias.
8. Incluir recuperação de resultado vazio quando entradas parciais, ruidosas ou falhas de extração forem plausíveis.
9. Isolar schemas, templates, políticas, exemplos e material canônico em `<reference_material>` em vez de espalhar regras.
10. Remover texto decorativo, redundante ou não operacional.
11. Validar o prompt contra o checklist de qualidade abaixo.
12. Emitir um único TXT BLOCK com o prompt pronto.

## Validações e checklist de qualidade

Antes de responder, verificar internamente:
- O objetivo está claro e operacional.
- O contrato de saída é explícito.
- O comportamento para dados ausentes está definido quando necessário.
- Nenhuma regra importante aparece duplicada em seções diferentes.
- `<formulas>` existe sempre que a tarefa depende de cálculo.
- Seções opcionais aparecem somente quando agregam confiabilidade ou controle.
- Material de referência está isolado das instruções operacionais.
- O prompt não contém rótulos como `Reasoning Effort`, `Verbosity` ou `Mode`, salvo pedido explícito do usuário.
- A resposta final contém exatamente um TXT BLOCK e nenhum artefato concorrente.

Se qualquer item falhar, corrigir antes de emitir a resposta.

## Tratamento de exceções

- Se faltar contexto em execução autônoma, usar o fallback aprovado e registrar indisponibilidade no próprio formato previsto; não pedir esclarecimento.
- Se a tarefa permitir interação e faltar informação essencial sem fallback seguro, pedir somente o mínimo necessário.
- Se houver conflito entre decisões já fechadas e material novo, preservar as decisões fechadas e sinalizar o conflito no nível permitido pelo contrato.
- Se um prompt SDD estiver sendo alterado sem inventário válido, não improvisar o contrato; seguir o fluxo de drift em [references/sdd-integration.md](references/sdd-integration.md).
- Nunca estimar números ou completar fatos ausentes como se fossem dados fornecidos.

## Examples

Pedido simples:
`Crie um system prompt que classifique tickets em billing, bug ou feature e devolva JSON válido.`

Resultado esperado:
- Estrutura enxuta, normalmente `<goal>`, `<output_contract>`, `<workflow_rules>` e `<verification>`.
- Sem seções decorativas.

Pedido com cálculo:
`Crie um prompt que calcule margem bruta por período a partir de receita e custo.`

Resultado esperado:
- Incluir `<formulas>` com `margem bruta = (receita - custo) ÷ receita`.
- Definir fallback para receita ausente ou zero.

---

Parte do SDD Open by RDD — https://github.com/robertodiasduarte/sdd-open
