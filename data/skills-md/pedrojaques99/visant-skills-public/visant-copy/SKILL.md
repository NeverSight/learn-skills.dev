---
name: visant-copy
description: 'Writes and reviews public-facing Brazilian Portuguese copy in Visant''s spoken voice, in any repo, and runs copy-lint, which catches AI tics in PT and English copy. Use on "copy", "headline", "landing copy", "remove the AI feel", "texto da landing", "reescrever a dobra", "essa copy tá confusa", "tirar cara de IA", "burilar a copy".'
---

# Visant Copy

Two things live here: **how Visant copy sounds** (valid in any repo) and **how it
is operated**, which depends on where the text lives. The voice below is for
Brazilian Portuguese; **for English copy read [english.md](references/english.md)**.
The linter runs a PT and an English rule set on every input.

- **The repo uses Visant's pipeline** (`copy*.json` at the root and
  `copy:build`/`copy:check` scripts in `package.json`): the JSON is the SSoT and
  the HTML is a generated view, so never edit text directly in the `.html`. See
  "If the repo uses Visant's pipeline".
- **Any other repo** (copy inside the component, `.md`, exported CMS): the
  component is the SSoT, and the risk is echo, the same sentence in four files.

Find out which one before touching text:

```bash
ls copy*.json 2>/dev/null; grep -nE '"copy:(lint|build|check)"' package.json
```

Either way, never write Visant copy without going through the prohibitions
below.

## Rule zero: propose, never apply

**Only the tic fixes the linter points out go into the file.** A headline, lead
or sentence that passes clean stays untouched, even if you think it sounds flat.

Style improvements go as a **proposal table in the report** (key, before, after),
and the user picks row by row. Rewriting what was already good burns trust and
makes the user review the reviewer.

**The exception is an explicit request.** "Essa copy tá confusa, tem que ser na
pegada X" is a work order, not an invitation to debate: apply it, show the
before/after table, and leave **one or two ONE-line alternatives** at the end, so
a swap costs one Edit and not a new round. Returning only options when the user
already gave the direction pushes the work back to them.

## The prohibitions

Absolute. They apply to headline, body, CTA, FAQ, email, caption, alt text,
error message, meta description. No "but here it worked" exception.

1. **Dash (— or –) never.** Period, comma, colon or parentheses.
2. **Separator dot (`·`, alt+7) never.** Not in metadata lists, not in a CTA with
   a price, not in a phase label, not on the social card. In a list it becomes
   period and comma ("34 páginas. 9 etapas, 1 case inteiro"), in a label a colon
   ("Fase 1: A Estratégia"), in a CTA a preposition ("Quero o e-book por R$ 47").
3. **"Não é X, é Y" never.** Not split in two sentences ("Não é uma lista. É uma
   cascata."). Not the sentence that defines by negation ("Não é slogan.").
4. **"É sobre X" never.** It asserts nothing. Swap it for the verb of what the
   thing does.
5. **"Não é apenas X, é X e Y" never.** Nor "mais que apenas", "menos X e mais
   Y", "não se trata de".
6. **Negation dangling at the end never.** "Feito pra ler, não pra arquivar."
   Delete the tail and the sentence gets stronger.
7. **Emoji never. Semicolon never.** (`©`, `®`, `™` are trademarks and stay.)
8. **Guru openings never.** "Imagine que", "E se eu te dissesse", "Prepare-se
   pra", "Chegou a hora de". Start with the fact or the scene.
9. **Cliché urgency never.** "Últimas vagas", "corre que acaba", "por tempo
   limitado". Scarcity must be countable: say the number ("este lote tem 30
   vagas", "a cota sobe a cada compra").
10. **Credibility seal at most once per page.** "real", "de verdade", "na
    prática", "de fato", "genuíno", "autêntico". One passes. With two, the reader
    counts and posts a screenshot ("trajetória real, projeto real, técnica real,
    processo real"). An adjective does not prove; numbers and scenes do.
    `Sete anos de projeto real` → `Sete anos entregando marca`.

**The rule that solves 3 to 6: cut the negative half.** The sentence that remains
is almost always the right one. If the contrast really is the argument, show the
**consequence** instead of negating: instead of "não é falta de talento, é falta
de ordem", write "Talento você já tem. O que falta é ordem."

## The linter

Running it before delivering copy is mandatory. Plain node, no dependencies, runs
in any repo:

```bash
L=~/.claude/skills/visant-copy/scripts/copy-lint.mjs
node $L copy.json                       # copy JSON
node $L hero.tsx page.tsx og.tsx        # components, passed TOGETHER
node $L README.md docs/landing.md       # markdown or plain text
npm run copy:lint                       # if the repo uses Visant's pipeline
```

What it accepts, exactly:

| input | how it reads | where it reports |
|---|---|---|
| `.json` (any structure, must be valid JSON) | every string value, at any depth | the dotted key (`hero.title`) |
| code (`.js .jsx .ts .tsx .mjs .cjs .vue .svelte .astro`) | line by line, comments masked | `L<n>` |
| any other text (`.md`, `.html`, `.txt`) | line by line, no masking | `L<n>` |

- **Files or folders**, one or many. A folder is walked for the types above,
  skipping `node_modules`, `.git`, `.next`, `dist`, `build`, `out`, `coverage`
  and dot-folders.
- Invalid JSON or a missing path stops with a one-line error and exit 1.
- Emoji runs on every file. Semicolon and pipe separator run **only on
  `.json`** (in `.md` the pipe is a table, in code `;` is syntax).
- Flags: `--quiet` (exit code only, for CI), `--include-comments` (lint code
  comments too), `--self-test` (every PT and EN rule fires, clean sentences pass).
- **Ids are English**, `pt-`/`en-` when language-specific (`pt-not-x-but-y`,
  `en-hype`), bare for punctuation (`em-dash`, `bullet-separator`, `semicolon`).
  Old PT ids (`travessao`, `bolinha`) still work in config. EN hype needs a
  marketing object: "Unlock account" passes, "unlock your potential" fails.

Exit 1 with the key, the excerpt and the fix. Two warnings come **outside the
exit code**, because good copy cannot fail on a detail:

- **length per line type** (headline 60, CTA 28, lead 180, body 280, SEO title
  60, meta description 160), inferred from the key suffix, so `.json` only; it
  flags the headline that breaks into three lines on mobile;
- **echo**, when the same sentence lives in two of the files passed in the same
  call. That is why you **pass the files together**, never one at a time.

In code files **comments are not linted** on purpose: a JSDoc is not copy.

### Repetition budget is per PIECE, and the file is not always the piece

`credibility-seal` (limit 1, PT and EN words share it) counts per piece: in JSON
the first key segment (`onboarding.*`), in a component the file. Money (`R$ 47`)
is not a seal; the rest is semantic, so confirm at `file:line`. [Why](references/cases.md).

## The voice

Pattern taken from Visant's e-book landing. In order of importance:

1. **Spoken Brazilian, medium dose.** "pra", "a gente", "tá". No "cê", "mano",
   "tá ligado". Short imperative: "Lê e julga", "Observa uma coisa".
2. **Short sentence after short sentence.** Average 12 words. **A verbless
   fragment is a device**, always as a punch after the long sentence: "…e a marca
   se comporta de outro jeito três meses depois. Toda vez."
3. **Scene instead of adjective.** Never "inconsistência de marca". Write what is
   seen: "Um post fala uma coisa, o atendimento fala outra, o site parece de
   outra empresa."
4. **Blame starts with the author.** Confess before charging: "A gente começava
   pelo logo também. Perdeu semanas assim, até inverter a ordem." Accusing the
   reader directly ("você começa pelo logo porque é a parte divertida") only
   after the confession, if at all.
5. **Raw numbers, not rounded to impress.** `R$450k`, `160+ lives`,
   `34 páginas`, `7 dias`.
6. **Admit limits.** "Se algo não funcionou pra gente, tá escrito que não
   funcionou." It is what most separates the voice from AI text.
7. **Humor by mocking the market**, dry and unsignposted: "Sem aula de 40 horas
   ensinando a centralizar retângulo." It targets the practice, never the person.
8. **Mild swearing, at most one per page**, and only where the argument hurts:
   "porcaria", "cagada". Never in the CTA or the main headline.
9. **Objections in the reader's voice.** The FAQ is what the person thinks, in
   their words: "Já faço branding há anos. Vou ver algo novo?". The answer opens
   by answering ("Serve.", "É."), never with "Ótima pergunta".

Line-by-line detail, vocabulary, anglicisms, money, CTA, and the before/after
table: [references/voice.md](references/voice.md). Read it before writing a new
piece or rewriting a whole section.

### The fold names the TASK, not the state

Applies to the H1, the `<title>` and the social card, and it is the most
expensive mistake because it passes every linter.

State copy describes the reader's world and leaves them to work out what they
gain: "Você tem centenas de mockups parados no disco." It is correct, real pain,
and asks for nothing. Task copy names the verb the person came to do: "Ache o
mockup certo sem abrir um PSD."

The test is one question: **which verb would the reader type into Google?** If
the headline lacks that verb, it talks about the state. And beware the wrong
task: before writing, check which step really hurts (example in
[references/cases.md](references/cases.md)).

When the pain needs to show (and sometimes it does), it goes in the **next
section**, opening the mechanism. On the fold you have 5 seconds, and spending
all five describing the problem is wasting your turn.

## Brand glossary (Visant's own copy only)

In client copy, the glossary is the client brand's, not this one.

| term | what it is | where it is used |
|---|---|---|
| **Visionário®** | lifetime plan, one-time payment | tier, CTA, FAQ, plans subtitle |
| **Visantista** | monthly subscriber, and the community's demonym | monthly plan, community |
| **Visantismo** | the movement and the landing's brand | logo, nav, footer |
| **Visant** | the agency / company | body copy, authorship |
| ~~Fundador~~ | **retired.** It was a loose synonym for Visionário and created two brands for the same plan | do not use |

## If the repo uses Visant's pipeline (`copy.json`)

**Copy lives in the JSON. HTML and Markdown are generated views.** Editing text
in the `.html` is always wrong: the next build overwrites it and the check breaks
the deploy. Flow: edit the JSON, `npm run copy:lint`, `npm run copy:build`,
commit json + html + md together (`copy:check` in the gate catches drift). SEO
(`meta.title`, `meta.description`, `meta.og_*`) lives in the JSON too, injected
via `data-copy-attr="content"`.

Full mechanics (new key, new page, `data-copy-attr`, `\n` becoming `<br>`, orphan
key error, setting it up in a new repo): [references/pipeline.md](references/pipeline.md).

## When there is no `copy.json` (any other repo)

Outside that pipeline, **the component is the SSoT**. Do not set up a
`copy.json` in the middle of a text task: the user asked for copy, not a new
architecture.

The risk changes shape. There is no build to sync views, so the same sentence
exists copied in three or four places, and changing only the `<h1>` leaves the
rest selling last month's promise. **After changing the headline, hunt the
echoes** (social card and `<title>` are the ones most often left behind):

```bash
rg -n "trecho da frase antiga" src   # and repeat with 4 or 5 words from the middle
```

Where they hide, in order of being forgotten:

| place | typical file |
|---|---|
| `<h1>` and lead | `components/**/hero.tsx` |
| link card | `app/**/opengraph-image.tsx`, and the `alt` exported there |
| `<title>` and description | `app/**/page.tsx` (and the `twitter`/`openGraph` of the same object) |
| screenshot `alt` and `figcaption` | the same hero |
| section that repeats the argument | `components/**/` in the same folder |

Close with `npx tsc --noEmit` in TS repos: a lost comma in JSX breaks the build.
The `<title>` is the only one that changes voice: it answers search, so it
carries the noun people search for ("mockups"), while the `<h1>` carries the verb.

## Work order on "review/write the copy"

1. Read the page's whole JSON (or the whole component) before touching any key.
   Including comments: they hold the WHY of the current line, and copy that
   contradicts the decision documented there is rework.
2. Run `copy-lint` to get the map of tics.
3. **Apply only the tic fixes**, and the rewrite the user asked for with a
   direction. Everything else becomes a proposal in a table.
4. Check every number against the source of truth (server-side price, client
   count, member count). The skill does not store those values on purpose: they
   age. When in doubt, ask before publishing.
5. **Hunt the echo** of the old sentence (`rg`, or the linter's echo warning with
   the files passed together) and update the social card, `<title>`, description
   and `alt`.
6. If you touched a code comment, update what it explains: a comment defending
   the old copy lies to the next dev.
7. Run `copy-lint` again. With Visant's pipeline, also `copy:build` and
   `copy:check`. In a React/TS repo, `tsc --noEmit`.
8. Report the before/after of the changed lines. The user approves text by
   reading text, never by reading a summary of the text.
