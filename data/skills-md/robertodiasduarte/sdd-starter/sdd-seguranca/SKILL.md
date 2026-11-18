---
name: sdd-seguranca
description: "Segurança do app feito com IA, do SDD Open, a partir de um catálogo de 22 falhas comuns (tabela sem RLS, chave secreta no código, registro de outra pessoa pelo id, CORS aberto, HTML do usuário sem escapar, cabeçalhos ausentes, instrução escondida em documento, agente com poder demais e outras), cada uma com a regra que previne, o teste de aceitação, a decisão de design e a conferência à mão. Quatro modos: Define (o sdd-define chama; propõe testes de aceitação em EARS, um item por vez, e responde N.A. em uma linha sem login, rota pública, dado de terceiros, upload, banco nem IA paga), checklist antes de publicar, app publicado e incidente (chave vazou, tabela ficou aberta, cliente reclamou). Use quando o sdd-define chegar ao passo de segurança, quando o usuário pedir para conferir a segurança antes de publicar, quando disser /sdd-seguranca, ou quando algo já vazou."
compatibility: "Funciona em qualquer agente, inclusive na web sem terminal: cada item tem a conferência à mão. No SDD Open, um script lê o mesmo catálogo e varre o repositório a cada publicação."
license: MIT
metadata:
  author: Roberto Dias Duarte
  version: "1.0.2"
  updated: "2026-11"
  fase: "Seg"
---
<!-- GENERATED pelo sdd-open (https://github.com/robertodiasduarte/sdd-open) com scripts/gerar-starter.py. Não edite
aqui: edite no sdd-open e gere de novo; o check-gerado.py do starter recusa a mudança. A tag está no GERADO.txt da raiz. -->

# sdd-seguranca — segurança do app, da ideia à publicação

Na primeira resposta desta skill, comece com esta linha, uma vez só, antes do Status:
`sdd-seguranca v1.0.2 · nov/2026 · versão atual: https://github.com/robertodiasduarte/sdd-starter/releases/latest`

A IA constrói o caminho feliz e esquece a tranca. Esta skill lembra a tranca na fase em que ela custa menos:
pergunta no Define, decide no Design, previne no Build e confere antes de publicar. A fonte de tudo é
`references/CATALOGO_SEGURANCA.md`: cada item tem a **frase** que previne, o **at** que vira teste, o
**evitar** que vira decisão, o **padrao** da varredura e o **confira** à mão.

## Como falar com o aluno

Leia `references/como-falar.md` antes da primeira resposta: o glossário desta skill, o Status preenchido
e um exemplo completo. Pergunta e parada seguem `<pasta desta skill>/references/PERGUNTA_DECISAO.md`.
Quem usa esta skill, em geral, nunca usou git nem terminal.

| Etapa | Nome para o aluno | Modo Define (os outros modos têm passos numerados próprios) |
|---|---|---|
| 1 | Gatilhos | o que o DEFINE tem de arriscado |
| 2 | Itens da stack | as fichas que valem para a stack e os gatilhos |
| 3 | Suas decisões | um item por vez: aplicar, recusar ou adiar |
| 4 | Gravar | testes novos, registro e a linha `Segurança` |

Toda resposta, nesta ordem (pule a parte sem conteúdo):

1. **Status** — uma linha que começa pelo nome da fase: `Segurança: ✅ 1 Gatilhos · ✅ 2 Itens da stack · ▶️ 3 Suas decisões · ⬜ 4 Gravar`
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

## Entrada

- `/sdd-seguranca sdd/features/DEFINE_{FEATURE}.md` — modo **Define** (o passo 12 do `sdd-define` chama assim).
- `/sdd-seguranca checklist` — modo **checklist antes de publicar**.
- `/sdd-seguranca app <URL publicada>` — modo **app publicado**.
- "vazou a chave", "a tabela ficou aberta", "um cliente viu o dado de outro" — modo **incidente**: vá direto
  para `references/INCIDENTE.md`, passo 1, sem perguntar mais nada antes de fechar a porta.

**A stack.** Pela pasta do projeto (`package.json`, `supabase/`, `vercel.json`) ou, sem acesso a ela, pergunte
em que o app é feito e anote. Item com
`stack: todas` sempre vale; os outros, só com a stack deles. Nunca proponha item de Supabase a quem não usa Supabase.

## Processo

### Modo Define

1. **Gatilhos.** Leia o DEFINE inteiro e, se existir, o `## Perfil de risco` do BRAINSTORM da feature. Os
   gatilhos são os do campo `gatilho` das fichas: `login` (contas, senha, sessão), `rota-publica` (página ou API
   que qualquer um alcança), `dado-de-terceiros` (dado de cliente, funcionário ou outra pessoa), `upload`
   (arquivo enviado), `ia` (chamada a modelo, agente, conteúdo externo lido pela IA), `banco` (tabelas, funções
   do banco). A triagem é **pelo sentido**, não só pela palavra; em dúvida, não é N.A. **Nenhum gatilho** ⇒
   responda em uma linha `✅ segurança: N.A. — <motivo>`, grave a linha do passo 4 e pare: sem perguntas.
2. **Itens da stack.** Fichas cuja stack vale e cujo `gatilho` cruza os achados (`sempre` sozinho não conta:
   esses itens ficam com a varredura e com o `AGENTS.md`), fora da fase `bancada`. Ordem: gravidade (`alta`
   antes de `media` antes de `baixa`), depois o id. Item que o DEFINE já atende (um AT que prova o mesmo lado
   negativo) sai da lista e é citado em 1 linha. Até **5 por rodada**; acima disso, diga quantos sobram e
   faça outra rodada depois das decisões.
3. **Suas decisões.** Uma pergunta por item, no formato do exemplo de `references/como-falar.md`:
   `[D2 · muda o produto]`, opções **aplicar** (recomendado), **recusar** (com motivo), **adiar**, **não sei**.
   Antes da pergunta, diga em 2 a 3 frases o risco no app desta pessoa (não o texto genérico da ficha) e o
   teste que entra se aplicado. Nunca "aplicar todos".
4. **Gravar.**
   - **aplicado** ⇒ o `at` da ficha, adaptado aos nomes do DEFINE, vira AT novo (próximo id) em EARS, com o
     lado negativo; o teste dele entra no `cmd` do Verify Gate existente (nunca um 2º bloco).
   - **recusado** e **adiado** ⇒ uma linha cada em `## Clarifications`, numa sessão `### Segurança`:
     `- [x] (segurança) Snn <falha> — recusado: <motivo>` ou `— adiado: <motivo>`. O Build copia essas
     linhas para o BUILD_REPORT; a publicação as mostra no bloco do OK.
   - A linha da tabela do `## Technical Context`, sempre esta:
     `| **Segurança** | <a> aplicados (Snn, …) · <r> recusados (Snn, …) · <d> adiados (Snn, …) | <data> |`, ou
     `| **Segurança** | N.A. — <motivo> | <data> |`. A linha é registro, não trava: o Verify Gate não a lê.

### Modo checklist antes de publicar

1. Leia o catálogo, filtre pela stack e pela fase (sem
   `bancada`) e ponha primeiro os itens com `agents: sim`.
2. Item a item, a pessoa confere à mão (ou pede à IA que mostre onde, no código, a regra é cumprida) e marca:
   **cumprido**, **não cumprido** (com o que falta) ou **não se aplica** (com o motivo). O que não der para
   conferir é pergunta, nunca ✅.
3. Grave a lista marcada em `sdd/reports/evidence/{FEATURE}/CHECKLIST_SEGURANCA.md` (sem terminal, entregue o
   texto para a pessoa guardar junto da versão publicada).

### Modo app publicado

Itens que só se conferem com o app no ar (S13 cabeçalhos, S14 CORS, S15 código e erro vazando, S08 cadastro
aberto, S07 limites): para cada um, o "confira" da ficha em passos numerados, um por vez, com o que a pessoa deve
ver na tela. A skill não acessa a URL por conta própria: quem confere é a pessoa, no navegador dela.

### Modo incidente

Siga `references/INCIDENTE.md` à letra: **fechar a porta** antes de qualquer outra coisa, depois preservar a
evidência, dimensionar, corrigir a causa, comunicar e registrar.

## Regras que não se negociam

- **Só o catálogo.** A skill propõe e confere itens do catálogo; não inventa falha nem regra fora dele.
- **Uma decisão por item**: aplicar · recusar (com motivo) · adiar. Nunca "aplicar todos".
- **Sem gatilho, N.A. em uma linha**, sem perguntas.
- **Chave real nunca se dispensa.** Achou uma chave verdadeira no código ou no histórico: é incidente (passo 1
  de `references/INCIDENTE.md`), não aviso.
- **A skill recomenda; quem constrói decide e responde.**

## Quality Gate

```text
[ ] Stack descoberta (script ou pergunta) e dita em 1 linha
[ ] Modo Define: gatilhos com o trecho do DEFINE, ou N.A. em 1 linha sem perguntas
[ ] Até 5 itens por rodada, em ordem de gravidade, um por pergunta, com aplicar · recusar · adiar · não sei
[ ] Aplicados viram AT em EARS com lado negativo e entram no cmd do Verify Gate existente
[ ] Recusados e adiados com motivo em ### Segurança; linha Segurança no Technical Context
[ ] Checklist: cada item marcado (cumprido · não cumprido · não se aplica), nunca ✅ sem conferência
[ ] Incidente: porta fechada antes de qualquer outra coisa
[ ] Resposta fechada com o resumo de etapa (`<pasta desta skill>/references/RESUMO_ETAPA.md`)
```

## Por que cada regra existe

- **Só o catálogo** — o mesmo item vira regra no `AGENTS.md`, teste no Define, decisão no Design e aviso na
  publicação; um item inventado aqui não teria as outras três metades.
- **Uma decisão por item** — "aplicar todos" põe no DEFINE testes que ninguém leu e que custam uma semana de
  build para fazer passar.
- **Sem gatilho, N.A. em uma linha** — pergunta de segurança num script local sem login ensina a pessoa a
  pular a próxima, que pode ser a de verdade.
- **Até 5 por rodada, do mais grave** — dez perguntas seguidas viram "sim, sim, sim" sem leitura.
- **Chave real nunca se dispensa** — a chave já vazou no momento em que foi salva; tirar o aviso não a troca.
- **A pessoa confere o app publicado no navegador dela** — a skill não abre a URL sozinha: o que se confere é
  o que qualquer visitante vê, e a prova fica com quem vai responder por ela.

## Encerramento (obrigatório)

Feche com o **resumo de etapa** (`<pasta desta skill>/references/RESUMO_ETAPA.md`); no modo Define, quem fecha é o
`sdd-define`, que segue para o próximo passo dele.

**Próximo passo:** modo Define, de volta ao `sdd-define`; checklist e app publicado, `/sdd-release`; incidente,
o passo de registro.

---

Parte do SDD Open by RDD — https://github.com/robertodiasduarte/sdd-open

## Quando migrar para o SDD Open

Esta skill é uma cópia gerada do [SDD Open](https://github.com/robertodiasduarte/sdd-open), a versão completa do
método. Migre quando o seu projeto já estiver no git e você trabalhar com um agente no terminal (Claude Code, Codex
e outros): o Open traz o Verify Gate executável, a revisão por outra IA, a varredura de segurança em toda publicação
e o playbook do projeto. A instalação e o passo a passo estão no README do Open; o que você já fez com esta skill
continua valendo lá.
