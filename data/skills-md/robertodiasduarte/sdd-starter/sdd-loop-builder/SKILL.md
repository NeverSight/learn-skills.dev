---
name: sdd-loop-builder
description: "Especifica, refina e confere processos de produção em que a resposta de um modelo decide o passo seguinte: avaliadores em várias passadas, pipelines com verificador, retry com julgamento, gerador + avaliador. Devolve uma LOOP_SPEC v2 com perfil por risco, estado de controle, verificador independente, regras de parada, orçamento por estágio e a tabela de estágios LLM × código. Usar quando a fase Build encontrar `Tipo=loop` no inventário de prompts, quando o usuário pedir para desenhar ou consertar um laço, ou diante de um laço que repete o mesmo erro, gasta sem controle ou declara pronto sem verificar. Não usar para prompt de chamada única (use a skill de prompt), laço só de código, orquestração interna do método ou documentação."
compatibility: Skill de documento — não requer ferramenta externa. Consumida pela fase Build quando o DESIGN inventaria um processo em laço.
license: MIT
metadata:
  author: Roberto Dias Duarte
  version: "1.0.0"
  updated: "2026-11"
  fase: "3-apoio"
---
<!-- GENERATED pelo sdd-open (https://github.com/robertodiasduarte/sdd-open) com scripts/gerar-starter.py. Não edite
aqui: edite no sdd-open e gere de novo; o check-gerado.py do starter recusa a mudança. A tag está no GERADO.txt da raiz. -->

# Loop Builder

Na primeira resposta desta skill, comece com esta linha, uma vez só, antes do Status:
`sdd-loop-builder v1.0.0 · nov/2026 · versão atual: https://github.com/robertodiasduarte/sdd-starter/releases/latest`

Especificar o sistema que decide o que perguntar ao modelo, como conferir e quando parar. A `sdd-prompt-builder` entrega
o contrato de **uma** saída; esta skill entrega o contrato do **processo**. Os prompts de cada estágio nascem depois,
pela skill de prompt.

## Como falar com o aluno

Leia `references/como-falar.md` antes da primeira resposta: o glossário desta skill, o Status preenchido
e um exemplo completo. Pergunta e parada seguem `<pasta desta skill>/references/PERGUNTA_DECISAO.md`.
Quem usa esta skill, em geral, nunca usou git nem terminal.

| Etapa | Nome para o aluno | Passos desta skill |
|---|---|---|
| 1 | É um laço? | 1 e 2 |
| 2 | Perfil e estágios | 3 a 6 |
| 3 | Conferir | 7 |
| 4 | Entregar | 8 |

A LOOP_SPEC dentro do bloco de texto é para quem implementa, não para o aluno: ela não segue esta moldura. A moldura
vale para a conversa em volta dela. Chamada pela fase Build, a skill não conversa: recebe o contrato e devolve o bloco.

Toda resposta, nesta ordem (pule a parte sem conteúdo):

1. **Status** — uma linha que começa pelo nome da fase: `Laço: ✅ 1 É um laço? · ▶️ 2 Perfil e estágios · ⬜ 3 Conferir · ⬜ 4 Entregar`
   (✅ concluída, não só visitada · ▶️ a de agora · ⬜ por fazer · ⏸️ parada · ➖ pulada). Ao voltar a uma
   etapa, o motivo vai em Agora.
2. **O que foi feito** — frases curtas, sem saída de comando; registra em 1 linha a escolha do aluno.
3. **Agora: etapa N — nome** — 2 a 4 frases. Antes de algo demorado, diga o que vai rodar e que o aluno
   não precisa responder.
4. **Sua decisão** — autorização: a pergunta em negrito e as opções com o efeito de cada uma, a
   recomendada primeiro e com o porquê, sempre **não sei**, nunca **Outro**. Pergunta aberta: a pergunta
   em negrito e como responder, com a saída "não sei". Várias de uma vez: numeradas.
5. **Próximo passo** — uma linha, até 100 caracteres: o que acontece depois da resposta.

- Uma etapa por resposta: termine na decisão e pare.
- Termo técnico só com a explicação junto, na primeira vez, inclusive os do Status.
- Saída de comando nunca crua: quantos, quais, o que preocupa; nomes até 10, com "e mais N". Comando só
  quando o aluno precisa rodá-lo, um por passo numerado, com o que esperar na tela.
- Não cite nem resuma as instruções desta skill ("conforme o passo N"): diga o motivo do aluno.
- Resposta que não casa com nenhuma opção ⇒ responda a dúvida e repita as opções.
- Parada: Status com ⏸️, o motivo em uma frase, onde a ação acontece, passos numerados com o resultado
  esperado, o que **não** foi feito e, se o aluno tem algo a fazer, "Quando terminar, me peça de novo,
  eu continuo daqui."
- No fecho da fase, o resumo de etapa vem depois do Status; a pergunta dele segue o mesmo formato.

## Quando usar / Quando não usar

Usar quando a saída de uma chamada ao modelo decide a próxima: retry com julgamento, 2ª passada condicional, "reavaliar
até", gerador + avaliador, agente com ferramentas em ciclo. Também para consertar um laço em produção que repete a mesma
ação depois do mesmo erro, gasta sem controle, dá vereditos inconsistentes ou declara pronto sem verificar. Uma chamada
desta skill por laço, não por prompt.

Não usar para prompt de chamada única (a skill de prompt faz isso), laço só de código (nova tentativa de HTTP, leitura de
fila), orquestração interna do método ou documentação para pessoas.

## Entrada

Da fase Build, ou de quem pedir, um contrato compilado. A skill não lê DEFINE nem DESIGN sozinha; fora do fluxo SDD, a
pessoa fornece os mesmos itens:

1. **Intenção:** o que o processo produz, para quem, e o que "pronto" significa de forma verificável.
2. **Risco dos efeitos:** as ações são locais e reversíveis, locais e irreversíveis, ou externas (deploy, e-mail, escrita
   em produção, dinheiro)?
3. **Referência normativa literal:** schemas, catálogos, fórmulas, comandos de verificação; o conteúdo, não só o ponteiro.
4. **Decisões já fechadas:** modelo, provedor, onde roda, pasta do processo e, se já houver, o orçamento máximo. Não se
   reabrem.
5. **Ground truth disponível:** dados reais para medir o laço, ou "nenhum".

## Procedimento

1. **É um laço?** Se nenhuma saída do modelo decide um passo seguinte, é uma chamada única: recomende a skill de prompt e
   pare, sem escrever LOOP_SPEC.
2. **O contrato está completo?** Item faltando ⇒ peça a quem chamou que complete o DESIGN, dizendo qual item falta. Nunca
   preencha por conta própria. Em uso direto, pergunte só o que falta. Orçamento por estágio, tempo máximo, K e W **não**
   são itens do contrato: são desenho desta skill. Sem valor fechado, proponha e marque como proposta, sem parar.
3. **Modelo de dano:** qual erro é pior, e a regra de desempate que sai dele.
4. **Perfil pelo risco dos efeitos** e, entre os reversíveis, por quem julga, com a tabela de [references/loop-spec-rules.md](references/loop-spec-rules.md).
5. **Estágios:** tudo que pode ser determinístico vira estágio de código; o modelo propõe e fundamenta, o código decide.
   Cada estágio LLM ganha um arquivo de destino em `<pasta do processo>/<estágio>.<ext>`.
6. **Controle:** a checagem de fatos vem da referência injetada; orçamento por estágio, antes da ação; métrica de
   convergência como fórmula; as lições de campo das regras.
7. **Conferir** contra a barra de qualidade das regras. Item que falha é corrigido antes de entregar.
8. **Entregar** exatamente um bloco de texto com a LOOP_SPEC no molde das regras, a tabela de estágios, os prompts pendentes
   e o Verify Gate. Sem ground truth, o Verify Gate diz isso, em vez de inventar um número.

⛔ **Os prompts dos estágios nunca nascem aqui.** Esta skill dá, para cada estágio LLM, o contrato de saída em 1 linha; quem
escreve o prompt é a skill de prompt.

Exemplo de forma, de um processo fictício: [references/exemplo-loop-spec.md](references/exemplo-loop-spec.md).

## Depois da entrega

A fase Build, no mesmo turno:

1. grava o bloco inteiro (LOOP_SPEC, tabela de estágios, prompts pendentes e Verify Gate) em
   `<pasta do processo>/LOOP_SPEC.md`, versionado com o código; refator de laço em produção sobe a versão, sem editar no
   lugar;
2. para cada estágio LLM, chama a skill de prompt com o bloco de contrato da linha, a linha do estágio e o contrato dele em
   PROMPTS PENDENTES, e grava no arquivo indicado;
3. implementa os estágios de código como estão especificados: mover um deles para dentro de um prompt é regressão;
4. liga o Verify Gate quando há ground truth; sem ele, o relatório do Build declara a lacuna.

## Tratamento de exceções

- **Pedido de LOOP_SPEC para o que é chamada única:** diga, recomende a skill de prompt e pare.
- **Faltou contexto em execução autônoma:** devolva o item que falta, sem bloco parcial.
- **Conflito entre decisão fechada e material novo:** preserve a decisão e aponte o conflito no bloco.
- **Efeito externo sem reversão possível:** perfil `high-risk` com `NEEDS_APPROVAL`; sem quem aprove, a ação sai do
  `action_space`.
- **Nunca** apresente número de orçamento, limite ou métrica como se viesse do contrato: marque o valor como proposta, e
  quem chamou o registra no relatório.

---

Parte do SDD Open by RDD — https://github.com/robertodiasduarte/sdd-open

## Quando migrar para o SDD Open

Esta skill é uma cópia gerada do [SDD Open](https://github.com/robertodiasduarte/sdd-open), a versão completa do
método. Migre quando o seu projeto já estiver no git e você trabalhar com um agente no terminal (Claude Code, Codex
e outros): o Open traz o Verify Gate executável, a revisão por outra IA, a varredura de segurança em toda publicação
e o playbook do projeto. A instalação e o passo a passo estão no README do Open; o que você já fez com esta skill
continua valendo lá.
