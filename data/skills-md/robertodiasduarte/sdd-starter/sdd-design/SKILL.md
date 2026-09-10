---
name: sdd-design
description: "Elaborar a fase Design de um fluxo SDD/AgentSpec a partir do arquivo Markdown do Brainstorm, do arquivo DEFINE e de interações de clarificação técnica com o usuário. Transformar requisitos validados em arquitetura, componentes, ADRs inline, file manifest, padrões de código, fluxo de dados, integrações, estratégia de testes, tratamento de erros, configuração, segurança e observabilidade. Usar após o SDD Define by RDD, especialmente quando o usuário fornecer BRAINSTORM_*.md e DEFINE_*.md e quiser gerar um DESIGN_*.md pronto para o SDD Build by RDD."
---

# SDD Design

## Quick start

Transformar Brainstorm + DEFINE em um DESIGN técnico implementável.

1. Ler integralmente o Brainstorm e o DEFINE.
2. Ler UX Review se o usuário também o fornecer.
3. Separar requisitos autoritativos, intenção original, decisões anteriores e evidências técnicas.
4. Inspecionar contexto de código/projeto quando estiver disponível.
5. Identificar lacunas técnicas que impedem arquitetura ou File Manifest concretos.
6. Perguntar apenas o necessário, preferencialmente uma pergunta principal por interação.
7. Criar a arquitetura e documentar decisões significativas como ADRs inline.
8. Criar File Manifest completo, padrões de código, fluxo de dados, integrações e estratégia de testes.
9. Aplicar a regra condicional de LLM Prompts de [references/llm-prompts.md](references/llm-prompts.md).
10. Preencher obrigatoriamente [assets/DESIGN_TEMPLATE.md](assets/DESIGN_TEMPLATE.md).
11. Executar `python scripts/validate_design.py <DESIGN.md>` quando houver filesystem e Python.
12. Salvar ou entregar `DESIGN_{FEATURE_NAME}.md`.
13. Encerrar o documento somente com `Execute o **SDD Build by RDD**.`

Consultar [references/design-protocol.md](references/design-protocol.md) durante todo o fluxo. Consultar [references/advisor-review.md](references/advisor-review.md) somente se houver uma revisão técnica externa formal antes do Build.

## Dados necessários

### Obrigatórios

- arquivo Markdown do Brainstorm, preferencialmente `BRAINSTORM_{FEATURE_NAME}.md`;
- arquivo Markdown do Define, preferencialmente `DEFINE_{FEATURE_NAME}.md`.

Ler ambos antes de formular perguntas.

### Opcionais

- `UX_REVIEW_{FEATURE_NAME}.md`, quando existir;
- árvore de diretórios ou arquivos relevantes do projeto;
- convenções técnicas do repositório;
- documentação de APIs, schemas, filas, banco ou infraestrutura;
- comandos reais de testes, lint, typecheck, build ou smoke;
- catálogo de agentes/especialistas disponíveis;
- respostas de clarificação do usuário.

Não exigir internet. Não alegar ter inspecionado repositório, agentes, infraestrutura ou código quando esse material não estiver acessível.

## Hierarquia das fontes

Para requisitos e comportamento:
1. resposta explícita mais recente do usuário;
2. UX Review, se fornecido e se não contradizer requisitos centrais;
3. DEFINE;
4. Brainstorm.

Usar o Brainstorm para recuperar intenção, alternativas exploradas, YAGNI e contexto de decisões, mas não reabrir requisitos já fechados no DEFINE sem motivo.

Para fatos técnicos atuais:
1. arquivos/código do projeto realmente acessíveis;
2. documentação técnica fornecida pelo usuário;
3. respostas explícitas do usuário;
4. inferências claramente marcadas.

Se duas fontes relevantes entrarem em conflito, perguntar antes de consolidar a decisão.

## Procedimento

### 1. Ler os artefatos de entrada

Extrair do Brainstorm:
- problema e intenção original;
- abordagem selecionada;
- alternativas rejeitadas;
- decisões-chave;
- itens removidos/adiados por YAGNI;
- dependências e amostras;
- hipóteses e limitações.

Extrair do DEFINE:
- Problem Statement;
- Target Users;
- Goals e prioridades;
- Success Criteria;
- Acceptance Tests;
- Out of Scope;
- Constraints;
- Technical Context;
- Assumptions;
- Verify Gate;
- flag `LLM Prompts`.

Extrair do UX Review, se houver:
- MUSTs de UX/CX;
- fluxos;
- estados;
- restrições de interação;
- recomendações que afetem arquitetura ou implementação.

Não duplicar conteúdo textual dos artefatos no DESIGN. Converter apenas o que afeta decisões técnicas.

### 2. Verificar prontidão da entrada

Antes de desenhar, confirmar:
- DEFINE está suficientemente fechado para orientar implementação;
- requisitos críticos não têm contradições;
- `LLM Prompts` é literalmente `true` ou `false`;
- o Verify Gate existe ou há um sinal objetivo de conclusão;
- Out of Scope está explícito.

Se algum desses pontos bloquear arquitetura, perguntar ao usuário. Não “corrigir” silenciosamente o DEFINE.

### 3. Inspecionar o contexto técnico disponível

Quando houver projeto/código acessível:
- identificar linguagem/framework;
- observar estrutura de diretórios;
- localizar módulos semelhantes;
- observar convenções de configuração;
- localizar testes existentes;
- identificar integrações e abstrações reutilizáveis;
- identificar padrões de logging/observabilidade;
- identificar catálogo de agentes, se existir.

Quando não houver:
- não inventar paths, bibliotecas ou agentes;
- perguntar por stack e estrutura mínima necessárias para um File Manifest concreto;
- permitir projeto greenfield apenas após o usuário confirmar stack/base técnica.

### 4. Detectar decisões técnicas bloqueantes

Listar internamente as decisões necessárias para:
- fronteiras de componentes;
- persistência e modelo de dados;
- contratos de integração;
- execução síncrona/assíncrona;
- idempotência e retries;
- autenticação/autorização;
- configuração;
- observabilidade;
- estratégia de testes;
- arquivos a criar/modificar;
- runtime LLM, quando aplicável.

Não perguntar sobre escolhas que já estejam resolvidas pelas fontes ou pelos padrões existentes do projeto.

Preferir uma pergunta principal por mensagem. Quando alternativas forem claras, apresentar 2–4 opções, recomendar uma com justificativa e permitir alternativa aberta.

### 5. Criar Architecture Overview

Produzir um diagrama ASCII legível que represente:
- entradas;
- componentes;
- armazenamento;
- integrações externas;
- saídas;
- direção principal do fluxo.

O diagrama deve ser coerente com Components e Data Flow.

Não adicionar componente sem função definida.

### 6. Definir Components

Para cada componente, registrar:
- nome;
- responsabilidade;
- tecnologia/padrão;
- entradas;
- saídas;
- dependências.

Favorecer componentes coesos e fronteiras simples.

Evitar nova abstração quando uma estrutura existente atende ao requisito.

### 7. Documentar Key Decisions como ADRs inline

Para cada decisão significativa, registrar:
- Status;
- Date;
- Context;
- Choice;
- Rationale;
- Alternatives Rejected;
- Consequences.

Registrar decisões que mudam arquitetura, custo de manutenção, contratos, dados, deployment, segurança ou testabilidade.

Não criar ADR para detalhe trivial.

Quando a escolha vier diretamente do DEFINE, preservar a decisão e explicar apenas seu impacto técnico; não fingir que alternativas foram reavaliadas nesta fase.

### 8. Criar File Manifest

Listar todos os arquivos que o Build deverá criar, modificar ou excluir.

Cada linha deve conter:
- número;
- caminho;
- ação;
- propósito;
- owner/agent;
- dependências.

Regras:
- usar caminhos reais do projeto quando disponíveis;
- não inventar caminhos fingindo que foram observados;
- em greenfield, usar caminhos coerentes com a stack confirmada;
- incluir arquivos de teste;
- incluir configurações, migrations, schemas e prompts quando fazem parte da implementação;
- evitar dependência circular;
- numerar dependências pelo índice do manifest.

Se agentes especializados não forem conhecidos, usar `(general)` e registrar `Agent Discovery: Not available`.

### 9. Definir Code Patterns

Fornecer snippets curtos e copy-paste ready somente para padrões-chave que reduzam ambiguidade no Build.

Priorizar:
- assinatura/interface central;
- schema/model relevante;
- padrão de erro;
- configuração;
- contrato de integração.

Usar a linguagem real da stack confirmada.

Não escrever a implementação inteira no DESIGN.

### 10. Aplicar regra de LLM Prompts

Consultar [references/llm-prompts.md](references/llm-prompts.md).

Se `LLM Prompts: false`:
- fazer rechecagem defensiva sobre Brainstorm + DEFINE + UX Review + escopo do Design;
- se não houver sinais, não criar seção `## LLM Prompts`;
- se houver sinais conflitantes, perguntar antes de continuar.

Se `LLM Prompts: true`:
- criar `## LLM Prompts` entre Code Patterns e Data Flow;
- inventariar todo prompt/runtime LLM planejado;
- classificar cada item como `one-shot` ou `loop`;
- definir contrato por prompt;
- cruzar o inventário com File Manifest e serviços que chamam LLM;
- não gerar o prompt final nesta fase.

### 11. Descrever Data Flow

Representar a sequência operacional ponta a ponta.

Para cada passo relevante, deixar claro:
- entrada;
- transformação;
- persistência;
- chamada externa;
- estado/falha;
- saída.

Cobrir também o principal caminho de erro quando isso afeta arquitetura.

### 12. Definir Integration Points

Para cada integração externa, registrar:
- sistema;
- tipo;
- autenticação;
- direção;
- timeout/retry relevante;
- comportamento de falha.

Não inventar credenciais, endpoints ou limites.

Se não houver integrações, usar `None`.

### 13. Planejar Testing Strategy

Mapear requisitos e riscos para testes:
- unit;
- integration;
- E2E;
- smoke/eval/typecheck quando derivado do DEFINE.

Não inventar ferramenta se o projeto não a usa ou o usuário não a confirmou.

Preservar alinhamento com Acceptance Tests e Verify Gate do DEFINE.

### 14. Definir Error Handling

Cobrir ao menos:
- entrada inválida;
- dependência externa indisponível;
- timeout;
- falha de persistência quando aplicável;
- conflito/idempotência quando aplicável;
- erro de LLM quando aplicável.

Registrar retry apenas quando seguro e compatível com idempotência.

### 15. Definir Configuration, Security e Observability

Configuration:
- externalizar tunables;
- evitar segredo em código;
- marcar origem de valores sensíveis.

Security:
- autenticação/autorização;
- validação de entrada;
- segredos;
- PII/dados sensíveis;
- least privilege;
- riscos específicos da feature.

Observability:
- logs;
- métricas;
- tracing quando aplicável;
- sinais ligados a Success Criteria e Verify Gate quando possível.

### 16. Validar consistência cruzada

Confirmar:
- todos os componentes aparecem no diagrama ou têm justificativa;
- File Manifest implementa todos os componentes relevantes;
- dependências do manifest são acíclicas;
- testes cobrem riscos e Acceptance Tests;
- integrações têm tratamento de erro;
- configurações citadas existem no manifest quando precisarem de arquivo;
- segurança e observabilidade não contradizem constraints;
- LLM Prompt Inventory está completo quando `true`;
- Out of Scope não aparece acidentalmente no plano.

### 17. Preencher o asset canônico

Usar [assets/DESIGN_TEMPLATE.md](assets/DESIGN_TEMPLATE.md) como única fonte estrutural do documento final.

Preservar os títulos e a ordem das seções obrigatórias.

Adicionar `## LLM Prompts` somente na condição definida.

Remover placeholders. Não deixar `TBD`, `{placeholder}` ou `[NEEDS CLARIFICATION]` em um DESIGN marcado `Ready for Build`.

### 18. Executar lint determinístico

Quando houver filesystem e Python:

`python scripts/validate_design.py <caminho-do-DESIGN.md>`

Corrigir todas as falhas estruturais antes de entregar a versão final.

O script valida estrutura e consistência básica; não substitui revisão arquitetural.

### 19. Salvar e entregar

Nome padrão:
`DESIGN_{FEATURE_NAME}.md`

**Onde salvar.** Grave em `sdd/` na raiz do projeto — pasta visível, igual em qualquer agente. Se o projeto já tiver `.claude/sdd/`, continue nela. Os documentos das cinco fases ficam lado a lado, sem subpastas.

Se houver filesystem do projeto:
- salvar como `sdd/DESIGN_{FEATURE_NAME}.md` (ou `.claude/sdd/DESIGN_{FEATURE_NAME}.md` quando essa pasta já existir);
- não sobrescrever silenciosamente arquivo existente.

Se não houver:
- entregar o `.md` para download quando a plataforma permitir.

### 20. Encerrar com o handoff padrão

A última seção deve ser exatamente:

```markdown
## Next Step

Execute o **SDD Build by RDD**.
```

Não acrescentar slash command, caminho, upload, GPT/Skill ou ação paralela depois desse texto.

## Quality gate

Antes de marcar `Ready for Build`:

- [ ] Brainstorm lido integralmente.
- [ ] DEFINE lido integralmente.
- [ ] UX Review incorporado quando fornecido.
- [ ] Requisitos autoritativos preservados.
- [ ] Contexto técnico observado ou explicitamente confirmado.
- [ ] Architecture Overview claro.
- [ ] Components coerentes com o diagrama.
- [ ] Decisões significativas documentadas com racional.
- [ ] Alternatives Rejected e Consequences registradas nas decisões relevantes.
- [ ] File Manifest completo, com testes/configuração quando aplicável.
- [ ] Paths não foram falsamente apresentados como observados.
- [ ] Dependências do File Manifest não são circulares.
- [ ] Code Patterns são copy-paste ready e compatíveis com a stack.
- [ ] LLM Prompts segue a regra condicional.
- [ ] Data Flow é coerente com arquitetura.
- [ ] Integration Points têm comportamento de falha.
- [ ] Testing Strategy cobre requisitos e riscos.
- [ ] Error Handling cobre falhas relevantes.
- [ ] Configuration não contém segredos hardcoded.
- [ ] Security Considerations são específicas.
- [ ] Observability define sinais úteis.
- [ ] Não há item Out of Scope planejado para implementação.
- [ ] Não há placeholder, TBD ou clarificação bloqueante.
- [ ] `scripts/validate_design.py` passa quando executável.
- [ ] Documento final se chama `DESIGN_{FEATURE_NAME}.md`.
- [ ] Next Step contém somente `Execute o **SDD Build by RDD**.`

## Tratamento de exceções

- Brainstorm ausente: pedir o arquivo; não reconstruir silenciosamente.
- DEFINE ausente: pedir o arquivo; não elaborar Design final apenas do Brainstorm.
- DEFINE contradiz Brainstorm: seguir DEFINE para requisitos e registrar a divergência apenas se afetar uma decisão técnica.
- UX Review contradiz DEFINE: perguntar qual direção prevalece quando o conflito for material.
- `LLM Prompts` ausente/ambíguo: perguntar; não escolher por conta própria.
- Sem contexto de código: pedir stack/estrutura necessária; não fingir inspeção.
- File Manifest não pode ser concretizado: manter status de rascunho e clarificar.
- Biblioteca/serviço não confirmado: apresentar alternativas e perguntar se a escolha for bloqueante.
- Usuário quiser encerrar com pendência bloqueante: entregar `Draft`/`Needs Clarification`, sem afirmar `Ready for Build`.
- Revisão externa formal: aplicar [references/advisor-review.md](references/advisor-review.md) e registrar cada nota como APPLIED ou REBUTTED.
