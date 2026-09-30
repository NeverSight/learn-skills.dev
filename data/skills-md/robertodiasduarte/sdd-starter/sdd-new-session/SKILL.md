---
name: sdd-new-session
license: MIT
description: "Abre uma frente de trabalho isolada neste repositório: cria uma git worktree fora da pasta do projeto, com uma branch nova nascida da branch de produção ATUALIZADA do remoto, prepara a pasta (dependências, arquivos locais) e abre no editor. Na primeira vez, investiga o repositório e grava o que descobriu em sdd/ambiente.md. Use quando o usuário disser 'abrir uma frente', 'nova sessão', 'nova tarefa isolada', 'criar worktree para X' ou quiser começar uma feature/correção sem misturar com outra em andamento."
metadata:
  author: Roberto Dias Duarte
---

# Nova frente de trabalho (new-session)

Um comando, uma tarefa, um diretório: `git worktree` + branch nova nascida do estado **remoto atual**
da branch de produção, pronta para abrir no editor.

## Passo 0 — Confirme que você consegue fazer isto

Rode `git remote -v`.

- **Se o comando não executa** (você está num aplicativo de chat, sem acesso ao computador do usuário),
  **pare** e diga exatamente: *"Não tenho acesso ao seu repositório — estou rodando no aplicativo,
  não na sua máquina. Para esta tarefa você precisa do Claude Code ou do Codex instalado no terminal,
  aberto na pasta do projeto."* Em seguida diga o comando de instalação atual do agente que você é e
  onde fica a documentação oficial.
- **Se executa, mas a pasta não é um repositório git** (`git rev-parse --show-toplevel` falha), diga
  isso e **pare sem criar nada** — provavelmente o terminal foi aberto na pasta errada, ou o projeto
  ainda não tem git.

⛔ Não invente uma frente assumindo como o projeto é. Uma frente criada a partir de suposição falha na
primeira vez que for usada, e o usuário não vai saber por quê. Parar aqui é melhor que entregar algo
plausível e errado.

## Regra número um: não pergunte o que dá para descobrir

Investigue e decida. Só pergunte o que for genuinamente ambíguo — e aí com a sua recomendação e o
motivo, para o usuário só confirmar. Tudo o que você assumir sozinho vai para a seção `## Suposições`
de `sdd/ambiente.md`, onde ele corrige em uma linha.

## Passo 1 — Descubra o ambiente (uma vez por repositório)

O checkout principal é o primeiro caminho de `git worktree list --porcelain` (linha `worktree …`).
Se existir `<checkout principal>/sdd/ambiente.md`, **leia e use** — não redescubra o que já está
escrito. Se não existir, investigue sem perguntar — mas, se o nome da tarefa já veio no pedido, faça
**antes** a checagem de colisão do Passo 2 (item 2): nome repetido aborta sem gravar nada, nem o
`sdd/ambiente.md`.

```bash
git remote show origin
git branch -r
git log --oneline -20
git tag --list
git worktree list
```

E leia, se existirem: `README.md`, `package.json`, `composer.json`, `requirements.txt`, `Makefile`,
`.gitignore`, `.env.example`, `.github/workflows/`, `CLAUDE.md`, `AGENTS.md`.

Extraia:

- **Branch principal** — a "HEAD branch" do `git remote show origin`. Não é "a branch em que estou agora".
- **Preparação** — `package.json` versionado com `node_modules` no `.gitignore` ⇒ `npm install` na pasta
  nova (senão ela nasce quebrada). Mesma lógica para `requirements.txt`, `composer.json`.
- **Arquivos locais fora do git** — `.env` no `.gitignore` e `.env.example` versionado ⇒ a pasta nova
  precisa de uma cópia do `.env` do checkout principal.
- **Skills do agente fora do git** — cada pasta em `.claude/skills/` ou `.agents/skills/` sem nenhum
  arquivo versionado (`git ls-files <pasta>` vazio, pasta por pasta) ⇒ precisa ser copiada para a frente;
  sem isso, a `sdd-release` não existe dentro dela.
- **Editor** — o primeiro que existir de `code`, `cursor`, `subl` (`command -v <nome>` no bash/zsh,
  `Get-Command <nome>` no PowerShell).
- **Cenário de branching**, pela evidência do repositório (critério do material "Git na Prática"):

| Cenário | Como reconhecer | Estratégia | A frente termina em |
|---|---|---|---|
| **A — entrega contínua, sem revisor** | Sem `develop`/`staging` no remoto; histórico de commits diretos na principal | Trunk-Based simplificado | merge direto na principal |
| **B — entrega via Pull Request** | Histórico com "Merge pull request #…"; `.github/workflows/`; mais de um autor | GitHub Flow | push da branch + PR |
| **C — várias versões em suporte** | Tags de versão **e** branches `release/*` ou `hotfix/*` no remoto | GitFlow | PR para `develop` (a branch nasce de `develop`) |

Escolha sempre o mais simples que serve. Empate entre A e B ⇒ **A** (acrescentar PR depois é trivial;
tirar cerimônia que virou hábito, não). C exige as **duas** evidências; repositório de uma pessoa quase
nunca é C — se você concluiu C, reveja.

Grave em `<checkout principal>/sdd/ambiente.md` (crie a pasta `sdd/` se preciso), neste formato — uma
chave por linha, para o usuário corrigir à mão:

```markdown
# Ambiente deste repositório

> Gerado pelas skills sdd-new-session/sdd-release. Está errado? Corrija a linha — as skills leem daqui.

- branch_principal: main
- cenario: A (Trunk-Based) — evidência: <o que você viu, ex.: "20 últimos commits diretos na main, sem develop no remoto">
- pasta_das_frentes: ../<nome-do-repo>-frentes
- editor: code
- preparacao: npm install
- arquivos_locais: .env
- deploy: <preencha só se descobriu; senão "a descobrir pelo sdd-release">
- testes: <comando, se descobriu>
- sintaxe: <comando, se descobriu>
- versionamento: nenhum

## Suposições

- assumi <X> porque <Y>
```

Não commite esse arquivo: ele é do usuário, que decide se versiona.

## Passo 2 — Crie a frente

Receba o nome da tarefa em linguagem natural e, na ordem:

1. **Slug**: minúsculas, hífens, sem acento (ex.: "Relatório mensal" → `relatorio-mensal`).
2. **Aborte se a branch ou a pasta já existirem** (`git show-ref --verify refs/heads/<slug>`,
   `git ls-remote --heads origin <slug>`, e a pasta `<pasta_das_frentes>/<slug>`). Não invente outro
   nome: peça outro ao usuário. Nada pode ter sido criado antes desta checagem.
3. `git fetch origin <branch-base>` e
   `git worktree add <pasta_das_frentes>/<slug> -b <slug> origin/<branch-base>` — a partir do estado
   **remoto**, não do local, que pode estar atrasado. `<branch-base>` é a principal (A, B) ou `develop` (C).
   Cenário C sem `origin/develop` (`git ls-remote --heads origin develop` vazio)? Pare antes de criar
   qualquer coisa e diga: o critério aponta GitFlow, mas não há `develop` de onde a frente possa nascer.
4. Na pasta nova: rode a preparação, se houver.
5. **Copie para a frente o que o git não leva**: os arquivos locais (`.env`) e **cada pasta de skill não
   versionada**, sempre a partir do checkout principal (caminhos absolutos, entre aspas):
   `mkdir -p "<frente>/.claude/skills" && cp -R "<checkout principal>/.claude/skills/<skill>" "<frente>/.claude/skills/"`,
   idem `.agents/skills/`.
   Confira que `<frente>/.claude/skills/sdd-release` (ou `.agents/skills/sdd-release`) existe quando existe
   no checkout principal — sem ela, a frente não consegue ser fechada. O Claude Code pede aprovação para
   escrever em `.claude/`: se a cópia for negada, **não pare** — termine a frente e, na resposta, entregue
   o comando de cópia pronto e a alternativa de instalar as skills uma vez para todos os projetos
   (`npx skills add robertodiasduarte/sdd-starter -a <motor> -g -y`).
6. Abra no editor (`code <pasta>`). **Sem editor, não aborte**: a frente já está pronta; mostre o caminho
   para abrir à mão.

A pasta fica **fora** do repositório (`../<repo>-frentes/<slug>`): dentro dele, a worktree apareceria
como arquivo não rastreado e sujaria o `git status` de todas as outras frentes.

**O que esta skill NÃO faz:** não commita, não faz push, não apaga, não integra. Só cria. Tudo o que
destrói ou publica é entregue como comando — ou fica para a skill `sdd-release`.

## Passo 3 — Responda

Nesta ordem:

1. **Cenário** (A, B ou C) com a evidência — o que você viu, não "parece ser".
2. **Caminho** da pasta e **nome da branch**.
3. **Como encerrar** esta frente, pronto para copiar: no fim, use a skill `sdd-release` de dentro da
   pasta nova; ou, à mão, o comando de integração do cenário seguido de
   `git worktree remove <pasta>` e `git branch -d <slug>`.
4. **Suposições** que você fez (se houver) e onde corrigi-las (`sdd/ambiente.md`).
5. No cenário A, trabalhando sozinho com IA: lembre de pedir uma revisão do código à IA antes de
   integrar — não há segundo humano olhando.
6. **Última linha, destacada:**
   `⚠️ Continue na janela nova. Esta sessão do agente continua presa à pasta onde foi aberta — nenhum
   cd muda isso. Build, commit e push rodam lá dentro.`

## Por que cada regra existe (não apague sem ler)

- **A branch nasce de `origin/<branch-base>` atualizada** (a principal; `develop` no cenário C) — nascer da branch atual herda trabalho pela
  metade de outra tarefa, e a frente nova "já vem com código estranho".
- **A mesma branch não abre em duas worktrees** — o Git recusa. Por isso não se volta para a principal
  dentro da pasta da frente: integra-se pelo caminho do cenário e atualiza-se no checkout principal.
- **Se outra frente for integrada antes desta**, esta nasceu de um ponto que já não existe. Antes de
  integrar: `git fetch origin` + `git merge origin/<branch-base>` + **rodar os testes de novo** — é aí que
  o conflito entre as duas aparece. (A `sdd-release` faz isso.)
- **Worktree e branch órfãs se acumulam** — depois de integrar, `git worktree remove` **e**
  `git branch -d`. O `-d` minúsculo é proteção: só apaga o que já foi integrado.
- **A sessão do agente não migra** — abrir a pasta nova abre outra janela, mas a sessão onde a skill
  rodou fica ancorada no diretório de origem. Sem o aviso final, a frente inteira acaba sendo feita no
  lugar errado e isso só aparece na hora do commit.

---

Parte do SDD Starter by RDD — https://github.com/robertodiasduarte/sdd-starter
