---
name: sdd-iniciar-repo
license: MIT
description: "Põe no git e num GitHub privado um projeto que ainda não usa git, sem levar junto dado de cliente: confere a pasta (fora de iCloud/OneDrive/Dropbox/Google Drive), lista o que entraria no git sinalizando senha (.env), certificado A1 (.pfx), planilha e arquivo grande, propõe o .gitignore, oferece o alarme de commit da sdd-higiene-dado antes do primeiro commit e só commita e publica com o OK explícito de cada etapa. Fala com quem nunca usou git: uma etapa por vez, com o que foi feito, o que vem agora e as opções de cada decisão. Retoma de onde parou (git sem commit, commit sem GitHub, envio que falhou). Use quando o usuário disser 'pôr no git', 'criar o repositório', 'subir para o GitHub', 'este projeto não tem git', ou quando a sdd-new-session ou a sdd-checar-ambiente disserem que o projeto ainda não usa git. Não limpa histórico que já vazou, não faz login no GitHub pelo usuário e não automatiza outro host (GitLab etc.), só entrega os comandos."
metadata:
  author: Roberto Dias Duarte
  version: "1.1.0"
  updated: "2026-10"
---

# Iniciar repositório (iniciar-repo)

Na primeira resposta desta skill, comece com esta linha, uma vez só:
`sdd-iniciar-repo v1.1.0 · out/2026 · versão atual: https://github.com/robertodiasduarte/sdd-starter/releases/latest`

Um projeto que ainda não usa git sai daqui com a primeira versão salva e um repositório **privado** no
GitHub, sem levar planilha de cliente, `.env` ou certificado junto. Quatro decisões do aluno no caminho:
a lista do que fica de fora (`.gitignore`), o alarme, a primeira versão salva (commit) e a publicação.
Sem um "sim" à pergunta daquela etapa, a etapa não acontece — silêncio, "ok" a outra pergunta ou pedido
antigo não são OK.

## Como falar com o aluno

Quem usa esta skill, em geral, nunca usou git. Cada resposta é uma etapa explicada, não um relatório
técnico.

**As 5 etapas, sempre com estes nomes:**

| Etapa | Nome para o aluno | Passos desta skill |
|---|---|---|
| 1 | Conferir o que há na pasta | Passos 1 e 2 (só lê) |
| 2 | Separar o que não pode sair do computador e ligar o git | Passo 3 |
| 3 | Instalar o alarme contra dado de cliente | Passo 4 |
| 4 | Salvar a primeira versão | Passo 5 |
| 5 | Guardar uma cópia privada no GitHub | Passo 6 |

**Toda resposta tem estas partes, nesta ordem** (pule a que não tiver conteúdo):

1. **Status** — uma linha: `✅ 1 Conferir · ▶️ 2 Separar · ⬜ 3 Alarme · ⬜ 4 Primeira versão · ⬜ 5 GitHub`
   (✅ feita, ▶️ a de agora, ⬜ por fazer, ⏸️ parada, ➖ pulada).
2. **O que foi feito** — em frases curtas, o resultado da etapa anterior, sem saída de comando.
3. **Agora: etapa N — nome** — o que esta etapa faz e por que ela existe, em 2 a 4 frases, como para
   alguém que nunca viu um terminal. Se for alterar algo, diga **em passos numerados** o que vai fazer e o
   que **não** vai acontecer ainda (nada vai para a internet, nenhum arquivo seu é apagado etc.).
4. **Sua decisão** — a pergunta em negrito e as opções, cada uma com o que acontece se for escolhida:

   > **Posso gravar a lista e ligar o git nesta pasta?**
   > - **sim** — gravo a lista, ligo o git e passo para a etapa 3 (alarme).
   > - **não** — paro aqui; nada é criado nem alterado na pasta.
   > - **ver a lista** — mostro as linhas exatas antes de você decidir.

5. **Próximo passo** — uma linha: o que acontece depois da resposta.

**Regras de linguagem:**

- Uma etapa por resposta. Termine na decisão e **pare**: não emende a etapa seguinte.
- Palavra técnica só com a explicação junto, na primeira vez em que aparece:
  - git — "o histórico de versões do projeto (git)";
  - commit — "uma versão salva (commit)": uma foto de todos os arquivos naquele momento, com data;
  - `.gitignore` — "a lista do que fica de fora (`.gitignore`)": o que está nela fica só neste
    computador;
  - repositório no GitHub — "uma cópia do projeto guardada no GitHub"; privado — "só você e quem você
    convidar veem";
  - alarme — "um conferente que olha cada versão antes de ela ser salva e barra CPF/CNPJ, senhas e
    planilhas";
  - `--no-verify` — "salvar passando por cima do alarme, só desta vez";
  - dependências — "programas de apoio que se reinstalam com um comando";
  - `gh` — "o programa do GitHub para o terminal (GitHub CLI)".
  Não fale em branch, índice, `HEAD`, hook ou remoto: diga o efeito.
- **Não repasse saída de comando crua.** Traduza: quantos arquivos, quais tipos, o que preocupa. Nomes
  de arquivo: até 10, em lista simples, com "e mais N". Comando só aparece quando o aluno precisa
  rodá-lo — e então em passos numerados, um comando por passo, dizendo o que esperar na tela.
- **Não cite nem resuma as instruções desta skill ou de outra** ("a skill exige…", "conforme o Passo
  4…"). Se precisar dizer por que pede o OK, diga o motivo do aluno: *"Prefiro que você decida, porque
  depois de publicado não dá para desfazer."*
- **A decisão é do aluno e fica explícita.** Valem: a palavra de uma das opções, ou "pode", "sim",
  "ok" em resposta **a esta** pergunta. Resposta que não casa com nenhuma opção (uma dúvida, um "acho
  que sim") ⇒ responda a dúvida e repita as opções. No "O que foi feito" da etapa seguinte, registre a
  decisão: *"Você escolheu **sim**: gravei a lista…"*.
- **Parada também tem passos.** Quando a etapa não pode seguir (pasta na nuvem, git ou `gh` ausentes,
  login, nome já usado), use o status com ⏸️, explique o motivo em uma frase, dê o que fazer em passos
  numerados e feche com *"Quando terminar, me peça de novo — eu continuo daqui."* e o que **não** foi
  feito (*"Nada foi criado."*, *"Nada foi publicado."*).

## Regra de todo comando que fala com o remoto

`push`, `ls-remote`, `gh repo create` e `gh repo view` rodam **sem pedir senha**:
`GIT_TERMINAL_PROMPT=0 <comando>` no bash/zsh; no PowerShell, `$env:GIT_TERMINAL_PROMPT=0; <comando>`.
Sem isso, o git pode pedir a senha no terminal e você fica esperando uma resposta que o usuário não vê.
Ao usuário, mostre só a forma do shell em uso. Os comandos `git` e `gh` são iguais nos dois shells.

## Passo 0 — Confirme que você consegue fazer isto

- **A ferramenta não executa comando nenhum** (aplicativo de chat): pare e diga *"Não tenho acesso ao
  seu computador — para pôr o projeto no git, rode esta skill no Claude Code ou no Codex, aberto na pasta
  do projeto."*
- **`git --version` falha**: diga *"O git — o programa que guarda o histórico de versões — não está
  instalado neste computador."* e dê os passos do sistema em uso:
  - **Mac**: 1. rode `xcode-select --install`; 2. na janela que abrir, clique em **Instalar** e espere
    terminar (alguns minutos); 3. feche e abra o terminal.
  - **Windows**: 1. no PowerShell, rode `winget install --id Git.Git -e` (sem `winget`: baixe em
    https://git-scm.com/downloads e instale com as opções que vierem marcadas); 2. feche e abra o
    terminal.
  - **Linux**: o gerenciador de pacotes da distribuição (`sudo apt install git`, por exemplo).

  Pare: *"Nada foi criado. Quando terminar, me peça de novo — eu continuo daqui."*
- **Os scripts desta skill precisam de bash.** No macOS e no Linux já existe. No Windows, o Git for
  Windows traz o Git Bash: com `bash` fora do PATH no PowerShell, rode
  `& "$env:ProgramFiles\Git\bin\bash.exe" "<pasta desta skill>\scripts\inventario.sh"`. Sem nenhum bash,
  faça o inventário à mão (Passo 2, PowerShell) e siga sem o alarme da higiene (Passo 4).

`<pasta desta skill>` é a pasta que contém este `SKILL.md` (`.claude/skills/sdd-iniciar-repo/` ou
`.agents/skills/sdd-iniciar-repo/`, no projeto ou na pasta global do agente).

## Passo 1 — Onde o projeto está (retomável)

Descubra, sem perguntar:

| Situação | Como reconhecer | Siga para |
|---|---|---|
| Ainda sem git | `git rev-parse --show-toplevel` falha | Passo 2 |
| Dentro de um repositório maior | `--show-toplevel` é outra pasta, acima desta | o inventário diz qual; **pare** |
| Git sem nenhum commit | `git rev-parse --verify -q HEAD` falha | Passo 2 (o `git init` já foi feito: pule-o no Passo 3) |
| Commit sem remoto | há `HEAD` e `git remote` vazio | Passo 2 (inventário, inclusive o do histórico) e depois Passo 6 |
| Remoto sem a branch | `origin` existe e `GIT_TERMINAL_PROMPT=0 git ls-remote --heads origin <branch atual>` vem vazio | Passo 2 e depois Passo 6, item 7 (publicação que ficou pela metade — só se o `origin` passar na conferência de lá) |
| Pronto | `origin` existe e tem a branch atual | diga *"Este projeto já está no git e no GitHub — peça a frente."* e pare |

`<branch atual>` é `git branch --show-current`.

Numa retomada, o status já começa com as etapas feitas marcadas ✅ (ou ➖, se foram puladas), e o
"O que foi feito" diz em uma frase o que você encontrou pronto.

## Passo 2 — Inventário (só lê) e identidade

1. Rode `bash "<pasta desta skill>/scripts/inventario.sh"` de dentro da pasta do projeto e leia a saída.
   Ao aluno, traduza (veja **Como falar com o aluno**): quantos arquivos entrariam, se apareceu algo
   sensível e o quê, e o que a lista do que fica de fora vai cobrir — por grupo (*"senhas e
   certificados"*, *"programas de apoio reinstaláveis"*, *"arquivos do sistema"*, *"planilhas"*), não
   linha a linha. As linhas exatas, só se o aluno escolher **ver a lista**.
   - Saída **2**: é uma pré-condição (pasta sincronizada pela nuvem, pasta pessoal, repositório numa
     subpasta ou acima, git ausente). A mensagem já diz o que fazer: transforme em passos numerados e
     **pare**, com *"Nada foi criado."*
   - Saída **1**: o inventário não conseguiu listar os arquivos. Não siga com um inventário pela metade:
     diga o que aconteceu e pare, *"Nada foi criado."*
   - Saída **0**: siga. O inventário lista o que entraria no git (respeitando um `.gitignore` que já
     exista), sinaliza senhas e certificados, planilhas, arquivos acima de 50 MB, dependências e — se já
     há commits — o que **já passou pelo histórico**, e termina com a proposta de `.gitignore`.
2. **Sem bash (PowerShell)**, as mesmas pré-condições e o mesmo inventário à mão, parando na primeira
   que falhar:
   - o caminho tem `OneDrive`, `Dropbox`, `Google Drive`, `My Drive`, `Meu Drive` ou `iCloudDrive` ⇒ mover
     o projeto para fora da nuvem;
   - a pasta é a pessoal (`$env:USERPROFILE`) ⇒ abrir o terminal na pasta do projeto;
   - `git rev-parse --show-toplevel` responde **outra** pasta ⇒ esta está dentro de um repositório maior:
     abrir lá;
   - sem git aqui, mas `Get-ChildItem -Recurse -Depth 2 -Force -Filter .git -ErrorAction SilentlyContinue`
     acha `.git` numa subpasta (fora de `node_modules`) ⇒ o projeto é aquela subpasta: abrir lá;
   - **com commits** (`git rev-parse --verify -q HEAD` responde), o histórico:
     `(git log --all --name-only --format= -z) -split [char]0 | Where-Object { $_ } | Sort-Object -Unique | Select-String -Pattern '(^|/)\.env|\.(pfx|p12|pem|key|xlsx|xls|csv|ods)$'`
     (o `-z` e o `-split [char]0` evitam que o git ponha entre aspas o nome com acento ou aspas, o que
     esconderia a extensão) — o que aparecer conta como o bloco *Já passaram pelo histórico* (item 4).

   ```powershell
   (Get-Location).Path
   Get-ChildItem -Recurse -Force -File -ErrorAction SilentlyContinue |
     Where-Object { $_.FullName -notmatch '\\(\.git|node_modules|\.venv|venv)\\' } |
     Where-Object { $_.Name -match '^\.env' -or $_.Extension -match '^\.(pfx|p12|pem|key|xlsx|xls|csv|ods)$' -or $_.Length -gt 50MB } |
     Select-Object FullName, @{n='MB';e={[math]::Round($_.Length/1MB)}}
   ```
   e monte a proposta de `.gitignore` com as mesmas linhas-base do `inventario.sh` (senhas e
   certificados, dependências, arquivos do sistema; planilhas e cada arquivo grande, se apareceram).
3. **Identidade do git**: `git config user.name` e `git config user.email`. Vazio ⇒ explique que cada
   versão salva leva o nome e o e-mail de quem salvou, e dê os passos: 1.
   `git config --global user.name "Seu Nome"`; 2. `git config --global user.email "voce@exemplo.com"`
   (iguais nos dois shells; o e-mail de preferência é o mesmo da conta do GitHub). Pare: a primeira
   versão falharia sem isso.
4. **Achado no histórico** (bloco 🔴 *Já passaram pelo histórico*): senha ou certificado ali ⇒ **não
   publique**. Diga que publicar leva o histórico inteiro, inclusive o que foi apagado depois; que limpar
   histórico não é feito por esta skill; e que a medida que protege é trocar a senha ou revogar o
   certificado. Pare com *"Nada foi publicado."* Só planilha no histórico ⇒ cite os nomes e pergunte
   **"Essas planilhas têm dado de cliente?"** com as opções **não têm** (sigo) e **têm** (paro: este
   histórico não deve ser publicado) — e siga só com **não têm**.

## Passo 3 — `.gitignore` e `git init` (etapa 2, 1ª decisão)

O "O que foi feito" é o resultado do inventário. O "Agora" explica que, antes de ligar o git, você
grava a lista do que fica de fora, por grupos, e que o que está nela fica só neste computador. Achou
planilha ou arquivo grande? Diga que a proposta já os deixa de fora e que, se algum precisar entrar
(uma planilha fictícia de exemplo, por exemplo), o aluno diz o nome. Pergunte:

**"Posso gravar a lista do que fica de fora e ligar o git nesta pasta?"**
- **sim** — gravo a lista e ligo o git; nada é salvo no histórico nem enviado ainda;
- **não** — paro; nada é criado nem alterado;
- **ver a lista** — mostro as linhas exatas e pergunto de novo.

- Sem um sim: pare, *"Nada foi criado."*
- Com o sim: acrescente as linhas ao `.gitignore` (crie se não existir; nunca apague linha que já
  estava). Sem `.git`: `git init -b main`. Git antigo, que não conhece `-b` ⇒ `git init` e
  `git symbolic-ref HEAD refs/heads/main`.

## Passo 4 — Alarme de commit, antes do 1º commit (etapa 3, 2ª decisão)

A primeira versão salva é a de maior risco: ela leva a pasta inteira. Antes dela:

- **A skill `sdd-higiene-dado` existe** na mesma pasta de skills desta: siga o procedimento dela por
  inteiro — `verificar`, explicar, a pergunta dela e `instalar` só com o sim. Se ela recusar por outro
  alarme existente, siga o que ela disser. **As respostas ao aluno seguem o formato desta skill** (status,
  o que foi feito, etapa 3, sua decisão, próximo passo), com a pergunta dela e estas opções:

  **"Posso instalar o alarme neste projeto?"**
  - **sim** — instalo; ele passa a conferir cada versão salva, nesta pasta e nas frentes;
  - **não** — sigo sem alarme para a etapa 4; a conferência da primeira versão fica só por minha conta.

  Explique o alarme pelo efeito: o que ele barra, que fica só neste computador (não vai para o GitHub),
  que dá para salvar passando por cima dele depois de conferir, e como tirá-lo. Caminho do arquivo e
  comando de desinstalar só se o aluno perguntar.
- **Não existe**: diga em uma frase o que ela faz (barra a versão com CPF/CNPJ válido, `.env`,
  certificado ou planilha nova), que se instala com
  `npx skills add robertodiasduarte/sdd-starter -a <claude-code ou codex> -g -y`, e pergunte
  **"Quer seguir sem o alarme?"** com **sim** (sigo para a etapa 4) e **não** (paro para você instalar;
  depois me peça de novo). Sem um sim, pare: *"Nada foi commitado."*

## Passo 5 — Primeiro commit (etapa 4, 3ª decisão)

Pule este passo se já existe `HEAD` (o commit já foi feito).

1. `git rm -r -q --cached --ignore-unmatch .` — sem commit nenhum, isto só esvazia a lista do que vai
   entrar (o índice); **nenhum arquivo do disco é apagado**. Tira o que foi preparado antes do
   `.gitignore` existir.
2. `git add -A`
3. **Confira pelo efeito, não pela proposta**: `git ls-files -ci --exclude-standard` tem de vir
   **vazio**, e o inventário rodado de novo (agora ele lê o que foi preparado) não pode ter os blocos
   🔴 *Senhas e certificados*, ⚠️ *Planilhas* nem ⚠️ *Arquivos grandes* — a não ser a planilha que o
   usuário disse, no 1º OK, ser fictícia e precisar ir (citada pelo nome). Se tiver, o `.gitignore` não
   cobriu aquele arquivo (uma linha `!` antiga, um nome fora do padrão): `git reset -q`, mostre o arquivo,
   proponha a linha que falta e volte ao 1º OK. Sem bash, use `git status --short` e procure os mesmos
   nomes à mão.
4. Com o alarme instalado, rode-o antes de perguntar: `bash .git/hooks/pre-commit` (só lê o que foi
   preparado; não salva nada). Achou CPF/CNPJ? Mostre arquivo e linha (o número vem mascarado) e
   pergunte, antes da pergunta do item 5:

   **"Esses CPFs/CNPJs são fictícios ou autorizados?"**
   - **são fictícios ou autorizados** — salvo a primeira versão passando por cima do alarme, só desta
     vez; ele continua instalado para as próximas;
   - **são de cliente** — paro para você trocar por dados fictícios; nada é salvo;
   - **não sei** — paro; confira os arquivos e me peça de novo.
5. Mostre a contagem e o que entra, **por tipo** (código, testes, documentação, configuração) com até 10
   nomes de exemplo em lista simples — nunca a saída de `git status`. Pergunte:

   **"Posso salvar a primeira versão do projeto com estes N arquivos?"**
   - **sim** — salvo a versão neste computador; nada vai para a internet ainda;
   - **não** — desfaço a preparação; a pasta fica como estava, com o git ligado;
   - **ver todos** — mostro a lista completa e pergunto de novo.

6. Com o sim: `git commit -m "Primeiro commit"` (com `--no-verify` só se o aluno escolheu **são
   fictícios ou autorizados** no item 4, e só neste commit). Sem o sim: `git reset -q` (desfaz só a
   preparação) e *"Nada foi commitado."*

Se o alarme recusar o commit, siga a `sdd-higiene-dado`: mostre o que ele achou e proponha a correção.
**Nunca rode `git commit --no-verify` por conta própria** — só quando a pessoa escolher, para aquele
commit, que conferiu e quer gravar.

## Passo 6 — Publicar no GitHub, privado (etapa 5, 4ª decisão)

1. `gh --version` falha ⇒ o programa do GitHub para o terminal não está instalado. Passos:
   1. instale — Mac: baixe o instalador em https://cli.github.com; Windows: `winget install --id GitHub.cli -e`
      no PowerShell (ou o instalador do mesmo site);
   2. feche e abra o terminal;
   3. rode `gh auth login` e responda: **GitHub.com** → **HTTPS** → **Yes** → **Login with a web
      browser**; copie o código que aparecer e cole na página que abrir no navegador.

   Pare: *"Nada foi publicado. Quando terminar, me peça de novo — eu continuo daqui."*
2. `gh auth status` sem conta logada ⇒ o passo 3 acima, explicando que o login é no navegador e é a
   única etapa que você não faz pelo aluno. Pare: *"Nada foi publicado."*
3. **Dono e nome**: dono = `gh api user --jq .login` (ou a organização que o usuário disser); nome = o
   nome da pasta, com espaço e acento trocados por hífen. Mostre `<dono>/<nome>` e deixe o usuário trocar.
4. **O nome está livre?** `GIT_TERMINAL_PROMPT=0 gh repo view <dono>/<nome> --json name`:
   - responde com o nome ⇒ **já existe**: pare e peça outro nome. Nunca envie para um repositório
     existente, nem para "aproveitar";
   - `Could not resolve to a Repository` ⇒ livre, siga;
   - qualquer outro erro ⇒ rede ou login: diga o que aconteceu em uma frase, *"Nada foi publicado."*,
     pare.
5. O "Agora" explica que o GitHub guarda uma cópia do projeto fora do computador, que **privado**
   significa que só o aluno e quem ele convidar veem, e que depois de enviado não dá para "desenviar".
   Pergunte, com as palavras exatas:

   **"Posso criar o repositório PRIVADO `<dono>/<nome>` no GitHub e enviar o primeiro commit?"**
   - **sim** — crio o repositório privado e envio a versão salva;
   - **não** — paro; a versão fica só neste computador, e dá para publicar depois pedindo de novo;
   - **outro nome** — diga o nome e eu confiro se está livre.

6. Com o sim:
   - bash/zsh: `GIT_TERMINAL_PROMPT=0 gh repo create <dono>/<nome> --private --source=. --remote=origin --push`
   - PowerShell: `$env:GIT_TERMINAL_PROMPT=0; gh repo create <dono>/<nome> --private --source=. --remote=origin --push`

   `--private` é fixo: não troque por `--public` nem se o usuário pedir nesta skill — repositório
   público é uma decisão para tomar no site do GitHub, depois de conferir o conteúdo.
7. **Envio que ficou pela metade** (há `origin`, mas `ls-remote` sem a branch — o `gh repo create`
   criou e não enviou, ou é a retomada do Passo 1). Não crie de novo, e só envie se o `origin` passar
   nas quatro conferências:
   - é do GitHub e `gh repo view <dono>/<nome do origin> --json visibility --jq .visibility` responde
     `PRIVATE`;
   - o envio vai para o mesmo lugar que a consulta: `git remote get-url --push --all origin` devolve uma
     linha só, igual a `git remote get-url origin` (um `pushurl` ou `pushInsteadOf` pode desviar o envio
     para outro repositório);
   - está **vazio**: `GIT_TERMINAL_PROMPT=0 git ls-remote origin` termina sem erro e não lista **nada**
     (nem branch, nem tag);
   - a pergunta do item 5, com `<dono>/<nome do origin>`, recebeu um sim.

   Falhou alguma ⇒ pare: *"O projeto já aponta para um repositório que eu não criei vazio e privado —
   nada foi publicado."* e mostre `git remote -v`. Passou ⇒ `gh auth setup-git` e
   `GIT_TERMINAL_PROMPT=0 git push -u origin <branch atual>` (PowerShell:
   `$env:GIT_TERMINAL_PROMPT=0; git push -u origin <branch atual>`).

**Outro host (GitLab, Bitbucket, servidor da empresa)**: não automatize. Entregue, em passos, para o
usuário rodar depois de criar o repositório vazio e **privado** lá:
`git remote add origin <url>` e `GIT_TERMINAL_PROMPT=0 git push -u origin main`
(PowerShell: `$env:GIT_TERMINAL_PROMPT=0; git push -u origin main`). *"Nada foi publicado por mim."*

## Passo 7 — Feche

- Se existir a skill `sdd-checar-ambiente` na mesma pasta de skills, rode
  `bash "<pasta das skills>/sdd-checar-ambiente/scripts/checar.sh" --frente` e leia a saída; ao aluno,
  só o que ela significa.
- A última resposta é um resumo, com o status todo ✅ (ou ➖ na etapa pulada):
  - **o que foi feito**, uma linha por etapa: o que ficou de fora; se o alarme está instalado; a versão
    salva, com o número de arquivos; o endereço `https://github.com/<dono>/<nome>`, **privado**;
  - **o que mudou na prática**: o projeto agora tem histórico — dá para voltar a uma versão anterior — e
    uma cópia guardada no GitHub;
  - **próximo passo**: se esta skill foi chamada pela `sdd-new-session`, volte para ela e abra a frente.
    Senão: *"Pronto — agora é só pedir a frente."*

## O que esta skill NÃO faz

- Não limpa histórico que já tem senha, certificado ou planilha (é da pessoa; a `sdd-higiene-dado`
  explica o que protege).
- Não faz login no GitHub, não cria token, não pede senha.
- Não cria repositório público, nem automatiza outro host além do GitHub.
- Não lê planilha nem `.env` por dentro: sinaliza pelo nome.
- Não move o projeto para fora da pasta sincronizada: diz o que fazer.
- Não instala o alarme sem o procedimento e a pergunta da `sdd-higiene-dado`.

## Por que cada regra existe (não apague sem ler)

- **Uma etapa por resposta, com status e opções** — quem nunca usou git não sabe onde está nem o que
  cada "sim" autoriza. Um "pode" a uma pergunta sem opções vira autorização para algo que a pessoa não
  entendeu; com as opções escritas, cada sim tem escopo, e o status mostra quanto falta.
- **Sem citar as instruções** — "a skill exige…" é ruído para o aluno e faz a pausa parecer burocracia;
  o motivo que importa para ele é o efeito (publicado não se desfaz).
- **Pasta sincronizada para tudo** — iCloud, OneDrive, Dropbox e Google Drive sincronizam arquivo por
  arquivo; o `.git` são milhares de arquivos que mudam juntos, e a sincronização cria cópias em conflito
  ou perde parte deles. No Mac, com Mesa e Documentos no iCloud, o caminho não denuncia: o inventário
  olha o atalho que o iCloud cria.
- **Inventário antes de qualquer `git add`** — um `git add .` numa pasta de módulo de Finanças leva a
  planilha com CPF de cliente e o `.pfx` do escritório; depois de publicado, apagar não desfaz cópias.
- **O inventário roda também na retomada** — quem já fez commits por conta própria pode ter um `.env` no
  histórico; o alarme só olha o que está indo no commit atual, não o passado.
- **`git rm --cached` antes do 1º commit** — o `.gitignore` não tira o que já foi preparado com
  `git add`; sem esvaziar o índice, o arquivo ignorado entra mesmo assim.
- **Alarme antes do 1º commit, depois do `git init`** — o alarme mora dentro de `.git/`; antes do
  `init` não há onde instalá-lo, e depois do 1º commit ele chega tarde.
- **CPF/CNPJ perguntado antes do commit, com opções** — o alarme barra pelo dígito, não sabe se o dado é
  fictício; só o aluno sabe. Por isso `--no-verify` só com a opção escolhida, e só naquele commit.
- **`gh repo view` antes de criar** — o nome pode já existir (outro projeto seu, ou da organização);
  enviar para ele mistura dois projetos. Pelo mesmo motivo, a retomada só envia para um `origin` vazio e
  privado: um `origin` que alguém configurou antes pode ser público.
- **Conferir pelo efeito depois do `git add`** — o `.gitignore` proposto pode não valer: uma linha `!`
  antiga o desfaz, e nome em maiúsculas escapa do padrão em minúsculas. O que decide é o que de fato foi
  preparado para o commit.
- **`--private` fixo** — o público desta skill guarda dado de cliente; tornar público é uma decisão que
  se toma olhando o conteúdo, não no fim de um assistente.
- **Retomável** — sem `gh`, sem login ou sem rede, o aluno para no meio; pedir de novo tem de continuar
  de onde parou, não recomeçar nem duplicar.

---

Parte do SDD Starter by RDD — https://github.com/robertodiasduarte/sdd-starter
