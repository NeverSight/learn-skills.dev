---
name: sdd-brainstorm
license: MIT
description: "Conduz o brainstorm da Fase 0 de um fluxo SDD/AgentSpec por interação com o usuário: explora contexto, faz perguntas de descoberta uma por vez, coleta amostras, compara 2–3 abordagens, aplica YAGNI, valida incrementalmente e gera um BRAINSTORM pronto para a fase /define. Use para ideias vagas de software, automações, agentes, produtos ou features que ainda precisam de exploração antes de formalizar requisitos; também quando o usuário pedir para transformar uma conversa, problema ou notas iniciais em um brainstorm estruturado."
metadata:
  author: Roberto Dias Duarte
---

# SDD Brainstorm

## Quick start

Transformar uma ideia inicial em uma direção validada antes de formalizar requisitos.

1. Capturar a ideia original sem reescrevê-la como requisito fechado.
2. Levantar apenas o contexto de projeto realmente disponível.
3. Fazer perguntas de descoberta **uma por vez**.
4. Fazer no mínimo 3 perguntas antes de propor abordagens.
5. Perguntar obrigatoriamente por amostras, exemplos de saída, ground truth ou código relacionado.
6. Propor 2–3 abordagens distintas, com uma recomendação explícita.
7. Aplicar YAGNI ao escopo.
8. Obter confirmação do usuário sobre a abordagem.
9. Fazer no mínimo 2 checkpoints de validação incremental.
10. Só então gerar o documento BRAINSTORM.

Consultar [references/brainstorm-protocol.md](references/brainstorm-protocol.md) para a política de interação. Para o artefato final, usar obrigatoriamente o asset canônico [assets/BRAINSTORM_TEMPLATE.md](assets/BRAINSTORM_TEMPLATE.md) como molde estrutural.

## Quando usar / Quando não usar

Usar quando a ideia ainda precisa ser explorada, quando existem alternativas relevantes, quando o problema está mais claro que a solução, ou quando o usuário quer preparar a entrada para uma fase posterior de definição.

Não usar como substituto de uma especificação formal quando problema, usuários, objetivos, critérios de sucesso, restrições e escopo já estão claros. Nesses casos, recomendar seguir diretamente para a fase de definição. Não usar para implementar código, desenhar arquitetura detalhada ou executar release.

## Dados necessários

Entrada mínima:
- ideia, problema, pedido, notas ou feature a explorar.

Entradas opcionais:
- arquivos/notas do usuário;
- contexto do projeto;
- estrutura de diretórios e padrões existentes;
- amostras de entrada;
- exemplos de saída esperada;
- ground truth ou dados verificados;
- código relacionado;
- restrições técnicas, operacionais, prazo ou orçamento.

Não exigir conector externo. Não assumir acesso à internet, repositório remoto ou sistema do usuário. Se o contexto não estiver acessível, registrar a limitação em vez de inventar observações.

### Asset obrigatório de saída

O arquivo [assets/BRAINSTORM_TEMPLATE.md](assets/BRAINSTORM_TEMPLATE.md) é o molde oficial do Brainstorm produzido por esta Skill. Ele é um **asset de saída**, não material conceitual de referência. Sempre reutilizá-lo para criar o `.md` final, em vez de reconstruir o documento apenas de memória.

## Procedimento passo a passo

### 1. Classificar a entrada

Identificar o tipo predominante:
- ideia vaga;
- pedido específico;
- problema;
- feature request;
- comparação entre alternativas;
- notas/arquivo.

Ajustar o foco sem pular as etapas obrigatórias. Uma ideia vaga pede exploração; um pedido específico pede validação do entendimento; um problema pede investigação da dor antes das soluções; uma feature request deve ter sua necessidade questionada; uma comparação deve enfatizar trade-offs.

### 2. Reunir contexto

Preservar o texto original da ideia como `Raw Input`.

Separar:
- fatos fornecidos pelo usuário;
- observações verificáveis em arquivos/contexto acessível;
- inferências.

Não transformar inferência em fato. Quando houver acesso ao projeto, observar estrutura, padrões existentes, localização provável, domínios técnicos relevantes e impacto de infraestrutura. Quando não houver, marcar como `N/A`, `desconhecido` ou `não fornecido`.

### 3. Fazer descoberta conversacional

Fazer **uma única pergunta por mensagem**.

Preferir múltipla escolha quando as opções forem claras e incluir uma opção aberta quando necessário. Usar pergunta aberta quando o território ainda for desconhecido. Se a resposta vier vaga ou contraditória, perguntar um esclarecimento antes de avançar.

Cobrir, no mínimo:
1. propósito/problema central;
2. usuário ou beneficiário;
3. restrições, limites ou contexto relevante;
4. sinal de sucesso, quando ainda não estiver claro.

Fazer **no mínimo 3 perguntas de descoberta antes de propor abordagens**. Não contar a pergunta de amostras como uma das 3.

Após cada resposta, registrar internamente:
- pergunta;
- resposta;
- impacto na solução.

### 4. Coletar amostras

Perguntar, em uma única interação, se há:
- arquivos de entrada;
- exemplos de saída esperada;
- ground truth/dados verificados;
- código ou padrão relacionado;
- nenhuma amostra disponível.

Se houver amostras, analisá-las apenas com as ferramentas disponíveis e registrar como elas influenciam a solução. Se não houver, seguir normalmente sem penalizar o usuário.

### 5. Propor 2–3 abordagens

Somente depois do gate de descoberta.

Apresentar primeiro a abordagem recomendada e justificar a recomendação. Para cada abordagem, informar:
- nome;
- descrição;
- vantagens;
- desvantagens/trade-offs.

As abordagens devem ser substantivamente diferentes, não apenas variações cosméticas. Comparar complexidade, risco, esforço, flexibilidade e aderência ao problema quando relevante.

Pedir que o usuário confirme uma abordagem. Se ele rejeitar todas, revisar o entendimento e voltar ao ponto necessário.

### 6. Aplicar YAGNI

Revisar componentes e features propostos perguntando:
- isto é necessário para o MVP?
- isto resolve o problema central agora?

Remover ou adiar itens que falhem nesses testes. Documentar o que foi removido/adiado e por quê. Se nenhum item puder ser removido de forma responsável, registrar que a revisão YAGNI foi executada e que nenhum corte adicional foi identificado; nunca inventar um corte só para preencher a seção.

### 7. Validar incrementalmente

Depois que houver uma direção escolhida, apresentar a solução em blocos curtos e verificáveis, idealmente com 200–300 palavras quando o conteúdo justificar.

Realizar no mínimo 2 checkpoints, por exemplo:
- checkpoint 1: conceito, limites e componentes;
- checkpoint 2: fluxo de dados, falhas, dependências e comportamento esperado.

Em cada checkpoint:
1. apresentar a seção;
2. pedir feedback/confirmar entendimento;
3. ajustar se necessário;
4. só então seguir.

Se o usuário corrigir um entendimento anterior, voltar e atualizar decisões dependentes.

### 8. Gerar o BRAINSTORM

Gerar o artefato somente quando:
- 3+ perguntas de descoberta tiverem sido respondidas;
- a pergunta de amostras tiver sido feita;
- 2+ abordagens tiverem sido exploradas;
- YAGNI tiver sido aplicado;
- uma abordagem tiver sido confirmada;
- 2+ checkpoints tiverem sido concluídos.

Usar obrigatoriamente [assets/BRAINSTORM_TEMPLATE.md](assets/BRAINSTORM_TEMPLATE.md) como **fonte de verdade do documento final**.

Ao gerar o arquivo:
1. copiar/usar o asset como molde;
2. substituir todos os placeholders `{...}` com dados sustentados pela conversa;
3. remover apenas seções explicitamente opcionais que não se apliquem, como `Approach C`;
4. preservar a ordem e os títulos das seções canônicas;
5. não criar uma estrutura alternativa de Brainstorm quando o asset estiver disponível;
6. registrar lacunas não resolvidas como `TBD`, `N/A`, limitação ou dependência conhecida, no local apropriado do template.

O nome preferencial do arquivo final é `BRAINSTORM_{FEATURE_NAME}.md`, com `{FEATURE_NAME}` em formato legível e estável para o projeto.

**Onde salvar.** Grave em `sdd/` na raiz do projeto — pasta visível, igual em qualquer agente. Se o projeto já tiver `.claude/sdd/`, continue nela. Os documentos das cinco fases ficam lado a lado, sem subpastas.

Se houver filesystem de projeto gravável, salvar como `sdd/BRAINSTORM_{FEATURE_NAME}.md` (ou `.claude/sdd/BRAINSTORM_{FEATURE_NAME}.md` quando essa pasta já existir), sem sobrescrever silenciosamente um arquivo existente.

Se não houver filesystem acessível, entregar o Markdown completo em chat e indicar o nome sugerido do arquivo.

### 8.1. Finalizar sem criar um segundo fluxo de descoberta

Antes do handoff, consolidar no próprio BRAINSTORM quaisquer lacunas ainda conhecidas. O fechamento não deve abrir uma nova frente de trabalho, por exemplo:

- "a principal informação a obter paralelamente...";
- "antes da próxima fase, colete...";
- "Ready for: `/define ...`".

A fase seguinte deve receber o Brainstorm como artefato de entrada. Se alguma informação ficou indisponível durante a exploração, registrá-la como `TBD`, limitação ou dependência no Markdown, sem substituir o `Next Step` definido abaixo.

### 9. Preparar o handoff

A seção `Suggested Requirements for /define` deve conter somente o que foi sustentado pela conversa:
- problem statement draft;
- target users;
- critérios de sucesso mensuráveis quando disponíveis;
- restrições;
- out of scope.

Não fabricar métricas. Quando um critério de sucesso ainda não puder ser quantificado, marcá-lo como ponto a definir em vez de inventar um número.

Ao concluir, o `Next Step` deve conter **somente** esta instrução:

`Execute o **SDD Define by RDD**.`

Não encerrar com comandos como `Ready for: /define ...`.
Não sugerir, no fechamento, coleta paralela de amostras, ground truth, código ou outras informações. Essas necessidades devem ser tratadas durante a própria fase de Brainstorm e registradas no documento quando permanecerem como lacunas conhecidas.

## Validações e checklist de qualidade

Antes de declarar o brainstorm concluído, verificar:

- [ ] Raw Input preservado.
- [ ] Contexto separa fatos de inferências.
- [ ] Pelo menos 3 perguntas de descoberta foram respondidas.
- [ ] As perguntas foram feitas uma por vez.
- [ ] A pergunta de amostras foi feita.
- [ ] Foram exploradas pelo menos 2 abordagens realmente distintas.
- [ ] Existe uma abordagem recomendada com justificativa.
- [ ] O usuário confirmou a abordagem selecionada.
- [ ] YAGNI foi aplicado e o resultado foi registrado.
- [ ] Foram concluídos pelo menos 2 checkpoints de validação.
- [ ] Decisões importantes e alternativas rejeitadas foram registradas.
- [ ] O handoff para Define contém somente requisitos sustentados pela conversa.
- [ ] O `Next Step` contém somente: `Execute o **SDD Define by RDD**.`
- [ ] O fechamento não contém `Ready for: /define ...` nem recomenda coleta paralela de informações.
- [ ] Nenhuma incerteza foi convertida silenciosamente em fato.
- [ ] O documento final foi gerado a partir de [assets/BRAINSTORM_TEMPLATE.md](assets/BRAINSTORM_TEMPLATE.md), sem alterar silenciosamente sua estrutura canônica.

## Tratamento de exceções

- **Usuário quer pular perguntas:** explicar de forma breve que o brainstorm ainda pode continuar, mas não concluir o handoff enquanto os gates mínimos não forem atendidos.
- **Usuário já traz requisitos completos:** oferecer seguir diretamente para definição em vez de prolongar artificialmente o brainstorm.
- **Respostas contraditórias:** perguntar uma clarificação, uma por vez, e atualizar decisões afetadas.
- **Sem amostras:** registrar `None available`/`N/A` e continuar.
- **Sem acesso ao projeto:** não alegar que estrutura, commits ou padrões foram inspecionados.
- **Usuário muda a direção após escolher uma abordagem:** reabrir comparação/YAGNI e repetir os checkpoints impactados.
- **Nenhum corte YAGNI responsável:** registrar revisão sem cortes; não fabricar exclusões.

## Examples

**Entrada vaga**
`Quero automatizar o processamento de notas fiscais, mas ainda não sei como.`

Começar pela descoberta do problema e do resultado desejado. Não apresentar arquitetura na primeira resposta.

**Feature request**
`Quero adicionar um chatbot ao portal do cliente.`

Questionar primeiro a necessidade, público e resultado esperado; depois comparar alternativas, incluindo a possibilidade de uma solução mais simples que um chatbot completo.

**Notas com contexto**
`Tenho estas notas de reunião e alguns exemplos de entrada/saída. Faça o brainstorm.`

Ler o material disponível, preservar fatos, conduzir as perguntas faltantes uma por vez e usar as amostras como grounding antes de propor abordagens.

---

Parte do SDD Open by RDD — https://github.com/robertodiasduarte/sdd-open
