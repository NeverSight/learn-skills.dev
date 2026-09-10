---
name: sdd-define
description: "Conduz a fase Define de um fluxo SDD/AgentSpec a partir do arquivo Markdown gerado pelo Brainstorm e de interações de clarificação com o usuário. Extrai e estrutura problema, usuários, objetivos, métricas, escopo, restrições e contexto técnico; escreve testes de aceitação em EARS, resolve ambiguidades, calcula Clarity Score e define um Verify Gate objetivo. Use após o SDD Brainstorm by RDD para gerar um DEFINE_{FEATURE_NAME}.md pronto para o gate seguinte."
---

# SDD Define

## Quick start

Transformar um arquivo `BRAINSTORM_*.md` em um `DEFINE_{FEATURE_NAME}.md` claro, testável e pronto para o próximo gate.

1. Receber e ler o arquivo Markdown do Brainstorm.
2. Extrair somente fatos, decisões, requisitos preliminares, limites e dependências sustentados pelo Brainstorm.
3. Preencher um rascunho usando obrigatoriamente [assets/DEFINE_TEMPLATE.md](assets/DEFINE_TEMPLATE.md).
4. Marcar ambiguidades em vez de adivinhar.
5. Calcular o Clarity Score inicial.
6. Fazer perguntas de clarificação ao usuário apenas para lacunas que impedem clareza, mensuração, testes ou o Verify Gate.
7. Escrever os Acceptance Tests em EARS usando [references/EARS.md](references/EARS.md).
8. Executar a varredura de ambiguidades de [references/CLARIFY.md](references/CLARIFY.md).
9. Derivar um Verify Gate conforme [references/VERIFY_GATE.md](references/VERIFY_GATE.md).
10. Só considerar o DEFINE pronto quando os quality gates desta Skill forem atendidos.
11. Salvar ou entregar o documento final como `DEFINE_{FEATURE_NAME}.md`.
12. Encerrar o documento com exatamente um próximo passo: `Execute o **SDD Design by RDD**.`

Para o fluxo completo e as regras de interação, consultar [references/define-protocol.md](references/define-protocol.md).

## Quando usar / Quando não usar

Usar quando:
- houver um arquivo Markdown produzido pelo SDD Brainstorm by RDD;
- o usuário quiser transformar o Brainstorm em requisitos formais e verificáveis;
- ainda forem necessárias clarificações pontuais antes de Design;
- for necessário formalizar critérios de sucesso, acceptance tests, escopo e Verify Gate.

Não usar quando:
- o usuário ainda estiver explorando o problema, público ou direção da solução; nesse caso, executar primeiro o SDD Brainstorm by RDD;
- o objetivo for desenhar arquitetura, componentes ou implementação detalhada;
- o objetivo for escrever código, executar build ou release;
- não houver Brainstorm nem informação suficiente para reconstruir sua função sem inventar requisitos.

## Dados necessários

### Obrigatório
- arquivo Markdown do Brainstorm.

Aceitar preferencialmente arquivos no padrão:
`BRAINSTORM_{FEATURE_NAME}.md`

Se o arquivo não estiver presente ou legível, pedir ao usuário para enviá-lo antes de elaborar o DEFINE.

### Opcionais
- respostas de clarificação do usuário;
- amostras já citadas no Brainstorm;
- documentação ou contexto técnico fornecido pelo usuário;
- comandos reais de teste, smoke, eval ou typecheck do projeto;
- convenções de deployment, infraestrutura ou domínio técnico.

Não exigir internet. Não presumir acesso ao repositório, filesystem, CI, banco, APIs ou comandos do projeto.

## Procedimento passo a passo

### 1. Ler e classificar o Brainstorm

Ler o documento inteiro antes de perguntar qualquer coisa.

Extrair:
- Raw Input / ideia inicial;
- problema;
- usuários e beneficiários;
- abordagem selecionada;
- decisões-chave;
- requisitos sugeridos;
- critérios de sucesso;
- YAGNI / itens removidos ou adiados;
- restrições;
- dependências;
- amostras e ground truth;
- validações já feitas;
- TBDs, limitações e perguntas pendentes.

Tratar decisões validadas no Brainstorm como contexto pré-validado. Não reabrir perguntas de descoberta sem motivo concreto.

### 2. Criar o rascunho a partir do asset

Usar [assets/DEFINE_TEMPLATE.md](assets/DEFINE_TEMPLATE.md) como única fonte de verdade estrutural para o documento final.

Não reconstruir um template alternativo de memória.

Preencher somente com:
- conteúdo explicitamente presente no Brainstorm;
- respostas dadas pelo usuário nesta fase;
- inferências técnicas claramente rotuladas como hipótese, quando inevitáveis e ainda não validadas.

Quando uma informação obrigatória não puder ser determinada, marcar a ambiguidade e perguntar; nunca inventar um valor para fazer o documento parecer completo.

### 3. Estruturar os requisitos

Organizar o conteúdo em:
- Problem Statement;
- Target Users;
- Goals com prioridades MUST / SHOULD / COULD;
- Success Criteria mensuráveis;
- Acceptance Tests;
- Out of Scope;
- Constraints;
- Technical Context;
- Assumptions.

Evitar duplicação. Quando Brainstorm e resposta posterior entrarem em conflito, a resposta mais recente do usuário prevalece e a mudança deve ser registrada em `Clarifications`.

### 4. Escrever Success Criteria mensuráveis

Todo critério de sucesso que represente qualidade, volume, tempo, custo, disponibilidade, precisão ou taxa deve conter um alvo observável.

Não usar adjetivos vagos como:
- rápido;
- escalável;
- confiável;
- fácil;
- grande volume;
- alta precisão.

Transformar em métrica apenas quando o número estiver sustentado pelo Brainstorm ou confirmado pelo usuário.

Se faltar o número, perguntar. Não inventar.

### 5. Escrever Acceptance Tests em EARS

Ler [references/EARS.md](references/EARS.md).

Cada acceptance test:
- deve expressar um comportamento observável;
- deve usar um padrão EARS reconhecido;
- deve manter as palavras-âncora EARS em inglês: `When`, `While`, `If`, `then`, `Where`, `shall`;
- deve ter um único comportamento principal.

Quando houver gatilho indesejado plausível, incluir pelo menos um teste `If ... then ... shall ...`.

Para bugfix, incluir pelo menos um requisito de não regressão com `shall continue to`.

Não finalizar enquanto existir acceptance test vago ou não testável.

### 6. Calcular o Clarity Score

Pontuar de 0 a 3:
- Problem;
- Users;
- Goals;
- Success;
- Scope.

Escala:
- 0 = ausente;
- 1 = vago ou incompleto;
- 2 = claro, mas faltam detalhes;
- 3 = cristalino e acionável.

Somar para um máximo de 15.

O mínimo para marcar o DEFINE como pronto é **12/15**.

Não inflar a pontuação para passar no gate.

### 7. Clarificar sem adivinhar

Ler [references/CLARIFY.md](references/CLARIFY.md).

Fazer uma varredura das nove categorias:
1. Scope;
2. Data model;
3. UX flow;
4. NFRs;
5. Integrations;
6. Edge cases;
7. Constraints;
8. Terminology;
9. Done signal.

Classificar cada categoria como `Clear`, `Partial` ou `Missing`.

Para `Partial` e `Missing` que afetem o DEFINE, criar internamente uma pergunta objetiva.

Preferir **uma pergunta principal por interação**. Se o contexto exigir agrupamento, nunca ultrapassar 5 perguntas na mesma rodada.

Quando houver alternativas claras:
- usar múltipla escolha;
- apresentar 2–4 opções;
- colocar a recomendada primeiro;
- permitir resposta aberta quando necessário.

Após cada resposta:
- substituir a ambiguidade no corpo do DEFINE;
- registrar a decisão em `## Clarifications`;
- recalcular as partes afetadas do Clarity Score.

### 8. Detectar uso de LLM Prompts

Definir `LLM Prompts` como `true` ou `false`.

Marcar `true` quando houver sinal forte de runtime prompts ou combinação suficiente de sinais fracos, como:
- provedor/modelo de LLM explícito;
- system prompt, user prompt, RAG, embeddings, classifier, synthesizer;
- chatbot, agente, resposta automática ou gerador de relatório com LLM;
- caminhos ou componentes dedicados a prompts.

Marcar `false` quando não houver sinal relevante.

Se houver apenas um sinal fraco isolado e a intenção estiver ambígua, perguntar ao usuário.

Registrar a justificativa em Notes.

### 9. Definir o Verify Gate

Ler [references/VERIFY_GATE.md](references/VERIFY_GATE.md).

O DEFINE precisa conter exatamente um bloco `verify_gate` com:
- `kind`;
- `cmd`;
- `pass_when`;
- `threshold`;
- `manual_fallback`.

Kinds aceitos:
- `test`;
- `smoke`;
- `eval`;
- `typecheck`;
- `manual-ux`.

Derivar o tipo a partir da natureza dos Acceptance Tests.

Não inventar um comando do projeto.

Se o comando real não puder ser inferido com segurança do material fornecido:
- perguntar qual comando verifica o comportamento; ou
- pedir ao usuário para escolher entre opções plausíveis de gate;
- usar `manual-ux` somente quando a aceitação for genuinamente humana/visual, não como atalho para ausência de comando.

Sem Verify Gate válido, o DEFINE não está pronto.

### 10. Resolver Open Questions

`## Open Questions` não deve esconder ambiguidade bloqueante.

Antes de concluir:
- resolver tudo que afete escopo, comportamento, critério de sucesso, acceptance tests ou Verify Gate;
- permitir apenas questões realmente não bloqueantes para Design;
- se não houver nenhuma, usar `None - ready for Design.`

### 11. Validar o documento

Executar, quando houver filesystem e Python disponível:

`python scripts/validate_define.py <caminho-do-DEFINE.md>`

Consumir a saída do script como lint estrutural. O script não substitui julgamento semântico.

Corrigir falhas antes de declarar o documento pronto.

### 12. Gerar e salvar o DEFINE

Nome preferencial:
`DEFINE_{FEATURE_NAME}.md`

**Onde salvar.** Grave em `sdd/` na raiz do projeto — pasta visível, igual em qualquer agente. Se o projeto já tiver `.claude/sdd/`, continue nela. Os documentos das cinco fases ficam lado a lado, sem subpastas.

Se houver filesystem gravável, salvar como `sdd/DEFINE_{FEATURE_NAME}.md` (ou `.claude/sdd/DEFINE_{FEATURE_NAME}.md` quando essa pasta já existir).

Se não houver filesystem, entregar o Markdown completo como arquivo `.md` para download quando a plataforma permitir.

Não declarar `Ready for Design` se:
- Clarity Score < 12/15;
- houver ambiguidade bloqueante;
- Acceptance Tests falharem nas regras EARS;
- Success Criteria relevantes não forem mensuráveis;
- Verify Gate estiver ausente ou incompleto.

### 13. Encerrar com o handoff padrão

A seção final do documento deve ser exatamente:

```markdown
## Next Step

Execute o **SDD Design by RDD**.
```

Não acrescentar comandos slash, caminhos, instruções de upload, referência a GPT/Skill ou ações paralelas depois desse texto.

## Validações e checklist de qualidade

Antes de considerar o DEFINE concluído:

- [ ] O Brainstorm foi lido integralmente.
- [ ] Decisões pré-validadas do Brainstorm foram preservadas.
- [ ] O documento usa `assets/DEFINE_TEMPLATE.md`.
- [ ] Problem Statement é específico.
- [ ] Há pelo menos um Target User com pain point.
- [ ] Goals estão priorizados.
- [ ] Success Criteria relevantes são mensuráveis.
- [ ] Acceptance Tests usam EARS.
- [ ] Existe teste If/Then para gatilho indesejado plausível.
- [ ] Bugfix, quando aplicável, contém `shall continue to`.
- [ ] As nove categorias de clarificação foram varridas.
- [ ] Não existem ambiguidades bloqueantes não resolvidas.
- [ ] Clarity Score é >= 12/15.
- [ ] Out of Scope é explícito.
- [ ] Constraints estão separadas de assumptions.
- [ ] Technical Context inclui `LLM Prompts: true` ou `false` com justificativa.
- [ ] Existe exatamente um Verify Gate válido.
- [ ] O Verify Gate não contém comando inventado.
- [ ] Open Questions não contém questão bloqueante.
- [ ] O lint `scripts/validate_define.py`, quando executável, passa.
- [ ] O arquivo final se chama `DEFINE_{FEATURE_NAME}.md`.
- [ ] `Next Step` contém somente `Execute o **SDD Design by RDD**.`

## Tratamento de exceções

- **Brainstorm ausente:** solicitar o arquivo Markdown; não reconstruir silenciosamente um Brainstorm.
- **Brainstorm incompleto:** extrair o que existe e clarificar apenas os gaps necessários.
- **Brainstorm contraditório:** perguntar qual decisão prevalece antes de formalizar o requisito.
- **Usuário altera uma decisão do Brainstorm:** aceitar a decisão mais recente, atualizar as seções dependentes e registrar em `Clarifications`.
- **Clarity Score < 12:** continuar a clarificação; não marcar como pronto.
- **Métrica sem número:** perguntar pelo alvo; não fabricar número.
- **Comando de Verify Gate desconhecido:** perguntar; não inventar comandos de projeto.
- **Sem acesso ao código/repositório:** não alegar que caminhos, testes ou infraestrutura foram inspecionados.
- **Usuário quer encerrar com pendências bloqueantes:** gerar apenas um rascunho com status `Needs Clarification`, sem o handoff final de conclusão.
- **Feature sem interface:** UX flow pode ser `N/A` quando isso for sustentado pelo escopo; não criar UI artificialmente.
- **Feature puramente UX:** `manual-ux` é permitido, com checklist humano objetivo.

## Examples

### Entrada esperada

Arquivo:
`BRAINSTORM_CONCILIACAO_BANCARIA.md`

A Skill deve:
1. extrair o problema, usuários, abordagem selecionada, YAGNI e requisitos sugeridos;
2. montar o rascunho do DEFINE;
3. identificar lacunas como métricas, tratamento de divergências, formatos suportados e gate verificável;
4. perguntar apenas o necessário;
5. gerar `DEFINE_CONCILIACAO_BANCARIA.md`.

### Pergunta de clarificação

Se o Brainstorm disser apenas "o processamento deve ser rápido", não converter isso em um número arbitrário.

Perguntar, por exemplo:
`Qual tempo máximo deve ser aceito para processar um par extrato + razão: (a) até 30s [recomendado], (b) até 60s, (c) até 2 min, (d) outro?`

### Handoff final

```markdown
## Next Step

Execute o **SDD Design by RDD**.
```
