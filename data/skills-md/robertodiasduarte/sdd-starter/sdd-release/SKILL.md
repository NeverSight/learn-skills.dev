---
name: sdd-release
license: MIT
description: "Fecha uma frente de trabalho e a leva para produção com UM ponto de aprovação: verifica sozinha o que vai subir (sintaxe, testes, segredo no diff, base desatualizada), mostra uma vez o que exatamente vai para produção e se o push publica sozinho, e só depois do OK do usuário commita, integra, publica e confere. Use de dentro da pasta da frente quando o usuário disser 'release', 'publicar', 'subir para produção', 'fechar a frente' ou 'integrar'. É a outra ponta da skill sdd-new-session."
metadata:
  author: Roberto Dias Duarte
---

# Release — fechar a frente com um OK

Verificar o que vai subir, mostrar **uma vez** o que vai para produção e — só depois do OK — integrar e
publicar.

## As duas regras que governam esta skill

1. **Não pergunte o que dá para descobrir.** Investigue e decida; pergunte só o ambíguo, com
   recomendação. No fim, liste o que assumiu ("assumi X porque Y").
2. **Simples não é sem rede de proteção.** Um passo a mais custa trinta segundos; uma publicação errada
   custa o fim de semana. O que se corta é **burocracia** (changelog elaborado, versionamento novo,
   relatório longo). **Nunca** o que impede publicar algo quebrado, e nunca o momento em que o usuário vê
   e aprova o que vai subir.

## Passo 0 — Onde estou

- Rode `git rev-parse --show-toplevel` e `git branch --show-current`. Se não for um repositório git, ou se
  a branch atual **for** a principal, pare e diga: esta skill roda de dentro da pasta de uma frente (criada
  pela `sdd-new-session` ou por `git worktree add`).
- O checkout principal é o primeiro caminho de `git worktree list --porcelain`. Se existir
  `<checkout principal>/sdd/ambiente.md`, **leia e use** (branch principal, cenário, testes, deploy).

## Passo 1 — Descubra o que faltar (sem perguntar)

Só o que `sdd/ambiente.md` não disser:

```bash
git remote show origin
git log --oneline -20
git tag --list
ls .github/workflows/
```

E leia: `README.md`, `package.json` (seção `scripts`), `Makefile`, `.github/workflows/*`, `CLAUDE.md`,
`AGENTS.md`.

- **Branch principal** — a "HEAD branch" do remoto.
- **Como o código chega em produção** — a descoberta mais importante. Seja honesto:
  - **Deploy automático**: um workflow dispara em push na principal ⇒ **o push É o deploy**.
  - **Deploy manual**: há um comando de publicação (`npm run deploy`, `make deploy`, um script).
  - **Nenhum**: o repositório só guarda código ⇒ "release" = integrar na principal, sem fingir que publicou.
- **Testes** (`npm test`, `pytest`, um job de CI) e **checagem de sintaxe** para os arquivos tocados
  (`node --check`, `php -l`, `python -m py_compile`, `tsc --noEmit`).
- **Versionamento** (tags `v*`, `version` no `package.json`, `CHANGELOG.md`). Se não houver nada disso,
  não invente: projeto sem versão não ganha versão junto com a release.
- **Cenário** (o mesmo da `sdd-new-session`): commits diretos na principal ⇒ **A, Trunk-Based**
  (termina em push na principal); merges de PR ⇒ **B, GitHub Flow** (termina em PR para a principal);
  tags de versão **e** branches `release/*` ou `hotfix/*` ⇒ **C, GitFlow** (termina em PR para `develop`) —
  o mesmo critério da `sdd-new-session`. Na dúvida entre A e B, A. Se existir `develop` no remoto mas o
  critério de C não fechar, **não decida sozinha**: a última linha do bloco do OK vira
  "**Posso publicar na `<recomendada>`?** (responda `develop` ou `main` para trocar)" — continua sendo
  uma pergunta só. **O destino respondido vira o `<alvo>` da Fase 3**: `develop` ⇒ a frente segue o
  caminho do cenário C (push da branch + PR para `develop`), nunca o push direto na principal.
- **Branch de integração** — onde esta frente entra: a principal nos cenários A e B, `develop` no C. Daqui
  em diante, `<alvo>` é ela. Comparar ou integrar uma frente do cenário C contra a principal levaria para
  produção o que ainda está em desenvolvimento.

Grave o que descobriu em `sdd/ambiente.md` do checkout principal (chaves `deploy`, `testes`, `sintaxe`,
`versionamento`), criando o arquivo no formato da `sdd-new-session` se ele não existir.

## Fase 1 — Verificar (sozinha, sem perguntar)

Tudo aqui é local e reversível. Nesta ordem, **parando na primeira falha**:

1. **O que exatamente vai subir** — inclusive o que ainda não foi commitado:
   - `git status --short --untracked-files=all` — arquivos modificados e **novos** (`??`, um por arquivo,
     nunca a pasta inteira agrupada) em relação ao último commit. **Esta
     é a lista do commit** da Fase 3, inclusive um arquivo que foi commitado e depois desfeito na pasta
     (ele some do resumo abaixo, mas precisa entrar no commit para o desfazer valer).
   - `git diff --stat $(git merge-base origin/<alvo> HEAD)` — compara a base da frente com a
     **pasta de trabalho**: cobre os commits da frente **e** as mudanças ainda não commitadas.
   - Não use só `git diff origin/<principal>...HEAD`: ele ignora o que não foi commitado, e numa frente
     sem commit mostraria um resumo vazio — o usuário aprovaria algo diferente do que sobe.
   - Arquivo que não pertence a esta frente? **Pare e mostre** — não decida sozinha o que fica de fora.
     Exceção que não é da frente e nunca entra no commit: pastas de skills não versionadas
     (`.claude/skills/…`, `.agents/skills/…`) — a `sdd-new-session` as copia para a frente funcionar.
   - Algo **staged** com versão diferente da pasta (o mesmo arquivo em `git diff --cached --name-only` e
     em `git diff --name-only`)? **Pare e mostre**: qual das duas versões sobe é decisão do usuário, e
     nenhuma das duas pode ser descartada sem ele ver.
   - **Impressão digital do que vai subir** — guarde `git rev-parse HEAD` (fixa o histórico que o push
     vai enviar), o resultado de `git diff <base> | shasum`, o de `git diff --cached | shasum` (o que já
     está staged) e o `shasum` de cada arquivo novo (`??`) — no PowerShell, `Get-FileHash` —, onde
     `<base>` é `$(git merge-base origin/<alvo> HEAD)`. É o que o OK aprova; a Fase 3 confere antes de
     commitar. Um commit reescrito depois do OK muda o `HEAD` mesmo que o conteúdo final seja igual.
2. **Sintaxe** dos arquivos tocados, com a ferramenta do Passo 1.
3. **Testes**, se existirem. Vermelho **para tudo**: aprovar um diff com teste quebrado transforma o OK em
   carimbo.
4. **Segredo vazando** — em tudo o que vai subir, não no repositório inteiro: o diff dos arquivos
   modificados **e o conteúdo inteiro de cada arquivo novo** (`??` do `git status`), que não aparece no
   `git diff` mas será commitado. Procure chave de API, token, senha, `.env` sendo versionado por engano:
   atribuições como `API_KEY=`, `SECRET=`, `PASSWORD=`, `TOKEN=` com valor literal, prefixos de chave de
   provedor e blocos `PRIVATE KEY`. **E também no histórico da frente** (`git log -p <base>..HEAD`): uma
   chave que entrou num commit e saiu no seguinte some do diff agregado, mas o push envia os dois
   commits. Achou no histórico? Pare: reescrever histórico é decisão do usuário, nunca desta skill.
   Uma chave publicada não se despublica, nem apagando o commit depois.
5. **A base andou?** `git fetch origin <alvo>` e `git rev-list --count HEAD..origin/<alvo>`. **Não
   integre agora**: um `git merge` aqui criaria commit antes do OK (e recusaria a pasta com mudanças não
   commitadas). Só registre: "a base andou N commits" vai no bloco do OK, e a Fase 3 integra a base
   atualizada e **roda os testes de novo antes de qualquer push**.

Se qualquer item falhar: **pare, diga qual falhou, com arquivo e motivo, e não siga.** Não conserte sozinha
e não peça OK "mesmo assim". Nessa resposta **não mencione o bloco do OK nem a pergunta "Posso publicar"**,
nem como passo futuro: termine com o que precisa ser corrigido e "depois, rode a `sdd-release` de novo".
Quem lê a pergunta no fim da resposta entende que o OK está sendo pedido.

## Fase 2 — O único ponto de parada

Mostre **um bloco só, neste formato** (preencha; não acrescente perguntas):

```markdown
**O que sobe**
<saída do --stat da Fase 1> + arquivos novos, pelo nome

**O que muda em produção:** <uma frase, em português — "muda o cálculo do relatório mensal da tela
inicial", não "altera handler.js">

**O push publica sozinho?** <sim, o workflow X publica ao receber o push na main | não: <por quê>>

**Verificações:** sintaxe <ok|pulada: motivo> · testes <ok|pulados: motivo> · segredo <nenhum, no
diff e nos arquivos novos> · base <atualizada | andou N commits: será integrada e testada de novo antes do push>

<só se não houver revisor humano:> Antes de responder, vale pedir à IA uma revisão do próprio código:
"isso quebra algo que já funcionava, expõe alguma senha, tem erro óbvio?"

**Posso publicar?**   ← ou "Posso publicar na <alvo>?", no único caso do destino ambíguo (Passo 1)
```

- Verificação ausente dita como ausente é informação; em silêncio, é falsa segurança.
- **A única pergunta do bloco é a última linha, "Posso publicar?"** (ou "Posso publicar na `<alvo>`?", se o
  destino ficou ambíguo no Passo 1). A sugestão de revisão
  é uma frase, não uma pergunta — transformá-la em "quer que eu revise antes?" cria um segundo ponto
  de parada, e duas paradas viram carimbo.
- Se algo ficou ambíguo (qual arquivo pertence à frente), diga **dentro deste mesmo bloco**, antes da
  última linha — nunca pare duas vezes.
- **Sem o OK, termine aqui**: nada de commit, merge ou push.

## Fase 3 — Publicar (só depois do OK)

1. **A pasta ainda é a que foi aprovada?** Recalcule a impressão digital da Fase 1. Diferente ⇒ algo mudou
   depois do OK: **pare**, mostre o que mudou e peça um OK novo — nunca commite o que não foi visto.
2. **Commit com os arquivos nomeados** um a um — exatamente os da lista do `git status` da Fase 1,
   nenhum outro. **Não resete o índice** (apagaria versão staged que não está na pasta). Depois do
   `git add`, `git diff --cached --name-only` tem de ser exatamente essa lista — se aparecer outro
   arquivo staged, pare antes do commit. Depois do commit, `git status --short` vazio — exceto as pastas
   de skills não versionadas, que ficam de fora de propósito.
   Nunca `git add -A`, nunca `git add -u`: com duas frentes abertas na mesma máquina, eles arrastam o
   trabalho da outra.
3. **Base atualizada, testada de novo.** Se a base andou: `git fetch origin <alvo>`,
   `git merge origin/<alvo>` **na frente**, e rode os testes de novo. Conflito ou teste vermelho: **pare
   antes de qualquer push**, diga o que quebrou — nada foi publicado.
4. **Integrar pelo cenário, sempre a partir da frente:**
   - A (Trunk-Based, `<alvo>` = principal): `git push origin HEAD:<principal>`. O push sai **da frente**, que contém exatamente
     o que foi aprovado mais a base remota — nunca do checkout principal, onde um commit local que ninguém
     aprovou iria junto. Recusado porque a base andou (`non-fast-forward`/`fetch first`)? Volte ao
     item 3 (nunca force). Recusado por outro motivo (permissão, branch protegida)? Pare e mostre o erro.
   - B (GitHub Flow): `git push -u origin <branch-da-frente>` e abra o PR para a principal — **e pare aí**.
     A integração é o merge do PR, depois da revisão.
   - C (GitFlow): `git push -u origin <branch-da-frente>` e abra o PR para `develop` — **e pare aí**. A
     frente não vai direto para a principal.
5. **Deploy manual, se houver, só a partir da principal já integrada e atualizada** — nunca da branch da
   frente não publicada. O deploy roda numa árvore **idêntica ao que foi publicado**: no cenário A, a
   própria frente logo depois do push aceito — confira `git status --porcelain` vazio e
   `git rev-parse HEAD` igual a `git rev-parse origin/<principal>` (após `git fetch`); se não bater,
   pare. Nunca do checkout principal, que pode ter mudança local ou commit que ninguém aprovou. Nos
   cenários B e C, entregue o comando de deploy para rodar **depois que o PR for integrado**; não o
   execute antes. (Com deploy automático, o próprio push na principal já publica.)
6. **Confirme que funcionou.** Não diga "publicado" porque o comando não deu erro. Há CI? Veja o resultado
   do workflow. Há URL? Veja se responde. Não há como confirmar? Diga isso: "publicado, sem verificação
   automática disponível" é honesto; "✅ tudo certo" sem ter olhado, não é.
7. **Checkout principal e limpeza**, entregues como comandos (de dentro da worktree ela não consegue se
   remover): no checkout principal, `git pull --ff-only` — se recusar, a principal local tem commits que
   não foram publicados, e isso é dito, não resolvido por você; depois `git worktree remove "<pasta>"` (com aspas: o caminho pode ter espaço) e
   `git branch -d <branch>` (o `-d` minúsculo só apaga o que já foi integrado). Nos cenários B e C, a
   limpeza vem depois do merge do PR.

Resposta final em três linhas: o que subiu, onde está, o que falta.

## O que NÃO entra nesta skill (e por quê)

- **Changelog elaborado** — se o projeto já tem `CHANGELOG.md`, uma linha. Se não tem, não crie.
- **Versionamento novo** — projeto que não versiona hoje não começa a versionar aqui.
- **Relatório final longo** — três linhas.
- **Nunca `--force`**, em nenhuma hipótese. Push recusado significa que a base andou: busque e integre,
  nunca force por cima do trabalho de outra pessoa (ou do seu de ontem).
- **Nunca um segundo ponto de parada** — duas paradas viram carimbo: a pessoa para de ler.

## Por que cada regra existe

- **O OK vem antes do push**: com deploy automático, depois do push não há "antes" para onde voltar.
- **O `git add` nomeia arquivos**: com duas frentes abertas, o `-A` publica a que nem terminou.
- **A base é conferida antes e integrada depois do OK**: se outra frente entrou primeiro, os testes
  passaram contra um estado que já não existe — mas integrar antes do OK criaria um commit que ninguém
  aprovou. Por isso: medir na Fase 1, integrar e testar de novo na Fase 3, antes do push.
- **O push sai da frente, não do checkout principal**: lá pode haver commit local que não passou pelo OK.
- **O resumo cobre o não commitado**: o commit acontece depois do OK, então o que se aprova tem de incluir
  o que ainda está só na pasta.
- **A skill roda de dentro da frente** e não consegue remover a própria worktree no fim — a limpeza é do
  checkout principal.

---

Parte do SDD Starter by RDD — https://github.com/robertodiasduarte/sdd-starter
