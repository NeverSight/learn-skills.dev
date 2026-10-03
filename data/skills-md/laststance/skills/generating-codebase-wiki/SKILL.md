---
name: generating-codebase-wiki
description: Generate a local DeepWiki-style static HTML site that explains a codebase with numbered chapters, mermaid diagrams that name real symbols, and path:line citations. Use when asked to build a DeepWiki, codebase wiki, architecture website, or visual code explainer.
---

# Generate a DeepWiki-style codebase wiki

Produce a **self-contained static HTML site** that a new engineer can browse like [DeepWiki](https://deepwiki.com/facebook/react). Match that bar: architecture first, every claim grounded in real files/symbols, diagrams whose nodes are code entities.

## Inputs

- **Repo root** (required): absolute path to a git checkout
- **Output dir** (optional): default `<repo>/wiki-site/`
- **Language**: Japanese if the repo's product UI / CLAUDE.md is Japanese; else English. Do not mix.

## Mandatory reads (this order)

1. [references/quality-bar.md](references/quality-bar.md) — what "as good as DeepWiki" means
2. [references/research-protocol.md](references/research-protocol.md) — archaeology before any HTML
3. [references/page-anatomy.md](references/page-anatomy.md) — page chrome, citations, mermaid
4. [references/cite-write.md](references/cite-write.md) — **write-time** cite recipe (one sentence → one cite; mermaid labels are citations)
5. Copy [assets/wiki.css](assets/wiki.css) and [assets/wiki.js](assets/wiki.js) into the output dir unchanged
6. Use [assets/page.template.html](assets/page.template.html) for every page
7. Before claiming done, score the site against [references/review-rubric.md](references/review-rubric.md). Fix until every gate is Pass. `verify-cites.mjs` must print `CITE_FILES_OK` with **zero** `ILLEGAL_FIRST` / `MERMAID_TOKEN_MISSING` / `MERMAID_EXTRA_ZERO_TOKEN` / `FIGURE_NO_SOURCES` / `OVERVIEW_NO_ENTITY_TABLE` / `UNUSED_CHIP` / `CITE_UNDEFINED` / `OOB` / `MISSING` / `MERMAID_HELPER_FIRST` / `SENTENCE_TOKEN_MISSING` / `SIBLING_FIRST` / `FACTORY_ON_CALLER` / `MERMAID_FACTORY_CALLER` / `OVERVIEW_TABLE_SOURCES_DUMP` / `INNER_SUBJECT` / `SLICE_PROPERTY` / `OBJECT_KEY` / `GLOSSARY_NO_DL` / `GLOSSARY_THIN_DL` / `GLOSSARY_P_CITE` / `GLOSSARY_STUB_DT` / `OVERVIEW_ENTITY_ORPHAN` / `DOTTED_CALLEE` / `GLOSSARY_UNPAIRED` / `CALL_ON_ENCLOSING`

## Workflow

Copy and check off:

```
- [ ] Step 1 Research — concept map written (do not skip)
- [ ] Step 2 Outline — numbered IA approved against scale table
- [ ] Step 3 Scaffold — css/js copied, index.html exists
- [ ] Step 4 Pages — every outlined page written from source, not README paraphrase
- [ ] Step 5 Cross-links — child links, Sources, glossary terms resolve
- [ ] Step 6 Self-review — rubric scored; any Fail fixed
```

### Step 1 — Research

Follow `research-protocol.md`. Completion criterion: a `research-notes.md` in the output dir listing subsystems, entry files, **real symbol names**, and 3+ design decisions with file:line. If you cannot name the constructor / hook / route handler, you have not researched enough.

### Step 2 — Outline

Numbered chapters like DeepWiki (`1`, `1.1`, `2`, `2.1`…). Scale:

| Src files (approx) | Pages (excl. glossary) |
| --- | --- |
| < 80 | 6–10 |
| 80–300 | 10–16 |
| 300+ | 14–22 |

Always include: **1 Overview**, at least one **architecture** chapter that maps runtime flow to files, and **Glossary**. Overview is a map, not a file dump. Child pages go deep.

Write the outline into `research-notes.md` before HTML.

### Step 3 — Scaffold

```bash
OUT="<output-dir>"
SKILL="$HOME/.cursor/skills/generating-codebase-wiki"
mkdir -p "$OUT/pages"
cp "$SKILL/assets/wiki.css" "$SKILL/assets/wiki.js" "$OUT/"
```

Relative links from `pages/*.html` to css/js are `../wiki.css` and `../wiki.js`. From `index.html` they are `./wiki.css` and `./wiki.js`.

### Step 4 — Write pages

Every page follows `page-anatomy.md`. **Draft every claim with `cite-write.md`** — do not write a paragraph and then attach a nearby range. Rules that fail reviews if broken:

- **Relevant source files** lists 8–20 files that this page actually discusses
- Opening paragraph: what / why / what this page covers (3–6 sentences)
- **Overview `index.html`:** mandatory 3-column table `サブシステム`/`Subsystem` \| `役割`/`Role` \| `主要な記号`/`Key code entities`, **≥12 rows** (Next.js Package Ecosystem Mapping), ≥2 exported identifiers per entities cell that already appear as named tokens in that page’s **prose or mermaid node labels** (not only inside the cited source span or only inside the entities `<td>`). Two-column 領域/役割 or an 8-row table is a G5 Fail
- **Leaf architecture pages** walk one named-function branch (≥3 cited steps). Query-name inventories fail G5
- ≥1 mermaid diagram per architecture page; nodes are **file paths or symbol names**, never "Module A"
- After each major section: `Sources:` with `path:start-end`
- Claims name symbols (`beginWork`, `useXxxQuery`) and cite them
- A cite is valid only if the span contains the named token (`DndContext`, `next`, `useSensors`). Never cite `package.json:1-24` or an import/type block as a stand-in. Negation still needs the token (`does not call loginWithRedirect`). Do not cite JSDoc / a sibling MAX constant as the home of the real call. A range that **starts** on `/**`, `'use server'`, `type Props`, `export interface` (when the subject is the function), `const schema`, a `//` comment, a JSX `{/*` comment, a mid-file `import` / `import type`, `try {`, `return (`, an inner `const xxx = useCallback`, or a sibling helper (`handleGitHubError`, `getDocumentFiles`) is Fail. If the sentence subject is a component/hook, the first line of the span must be that `export` (`useXxx` → that `export`, not an inner `useCallback`). A PascalCase type is not the camelCase param. After every mermaid `</figure>`, the next sibling must be `<p class="sources">`; node tokens must appear in those spans.
- A Relevant-source chip is unused unless prose, mermaid, or an inline cite names that path or a symbol defined in that file. A route string (`/help`, `/boards/new`) does not license the page/route module. A field key or imported helper does not license a different file. Sentence subjects (`Layout`, `AdminLogin`, `TARGET_PATH`, `claims.sub`) must appear inside the cited span — a JSX child or inner memo is not enough. Do not name a negated token (`getUser`) unless a cited line contains it (JSDoc above `export` does not count)
- No marketing adjectives ("robust", "seamless", "easy")
- Do not invent packages, routes, or env vars

### Step 5 — Cross-links

Every parent lists child pages. Glossary defines domain terms used on ≥2 pages. Sidebar on every page matches the outline. `index.html` is chapter 1 (Overview), not a splash.

### Step 6 — Self-review

Score `review-rubric.md`. Any Fail → fix, do not ship. Write `SELF_REVIEW.md` in the output dir with Pass/Fail per gate and 8 sample citations you verified by re-reading the file. For each, quote the token inside the span.

Run `node ~/.cursor/skills/generating-codebase-wiki/scripts/verify-cites.mjs <out> <repo-root>`. The script now fails the process on `MISSING`, `OOB`, `ILLEGAL_FIRST`, `MERMAID_TOKEN_MISSING`, `MERMAID_EXTRA_ZERO_TOKEN`, `FIGURE_NO_SOURCES`, `OVERVIEW_NO_ENTITY_TABLE`, `UNUSED_CHIP`, `CITE_UNDEFINED`, `MERMAID_HELPER_FIRST`, `SENTENCE_TOKEN_MISSING`, `SIBLING_FIRST`, `FACTORY_ON_CALLER`, `MERMAID_FACTORY_CALLER`, and `OVERVIEW_TABLE_SOURCES_DUMP`, and `INNER_SUBJECT`, `SLICE_PROPERTY`, `GLOSSARY_NO_DL`, `GLOSSARY_THIN_DL`, `GLOSSARY_P_CITE`, `GLOSSARY_STUB_DT`, `OVERVIEW_ENTITY_ORPHAN`, `DOTTED_CALLEE`, `GLOSSARY_UNPAIRED`, and `CALL_ON_ENCLOSING`. Treat every `HEADER?` line as a Fail until you prove the named token lives in that span (not JSDoc / imports). After every `path:start-end`, re-Read the file: if `end` > last line, shrink it. Follow `cite-write.md` for the rest: one sentence → one cite; mermaid labels contain **only** in-span identifiers (no English gloss such as `rebuild`); a hook “exposes save/close” range must include `handleClose` if you named close; Sources `·` extras are judged alone; a mermaid Sources extra with **zero** node tokens fails; `lodash.merge` is not licensed by `merge(` plus an out-of-range lodash import; `export const {` is illegal; `/auth/` is not `/^\/auth\//`; `owner/repo` is not `repo_owner` + `/` + `repo_name`; imported enums used only via an alias outside the span do not count; `axiosClient.post` on a `useXxx` cite must be in-span; mapping literals must not live only in JSDoc; prose `//` is not `\/`; alias `NS` is not gloss `zod`; negation still needs identifier `X` in-span; `repo_card_id` ≠ `repoCardId`; an identifier at `end+1` fails; do not hang `proxy` / a route on a helper that never writes them; `AxiosError` ≠ `isAxiosError`; mermaid Sources must not start on `buildForwardedQuery` / `getLimiter` / `consumeCaptureQuota`; do not hang `createClient` / `toPublicBoardSlug` / `useStorageHydrated` / `requireClaims` on the caller. Overview table is **≥12 rows**. Leaf pages that only chain lookups fail G5. `ErrorBoundary` ≠ `CustomErrorBoundary`. A chip is unused unless the article names that path or that file’s export (`SortableColumn.tsx` is not licensed by a drag-type in another file). Never emit `<code class="cite">undefined</code>`. A phase sentence must not name a call at `end+1`. The shortest architecture leaf itself needs a ≥4-phase in-function walk and a mermaid of those phases — Overview’s pipeline does not rescue a 3-step `OrdersPage` or a 3-node `proxy` stub. `FAILED` ≠ `JOB_FAILED` / `failWith`. `asPath` ≠ `getRequestedPath`. Do not hang `useStorageHydrated` on `useTheme`. A `boardIdSchema` line does not contain `getBoardBundle`. `export { storageApi }` does not contain `store`. Child-link captions do not license chips. A constructor / client-factory / Provider-header span may name only identifiers in that inclusive text (`createClient` through `createServerClient(` ≠ `getAll`; `axios.create({` ≠ `post`; `AxiosClientProvider` header ≠ `401`). A mermaid Sources extra whose first line is `function getLimiter` / `const consumeCaptureQuota` / `const buildForwardedQuery` is Fail even when that helper is a node label — hang it on the prose sentence only. Prose `60000` is not licensed by `60_000`. A cite whose first line declares A may not name sibling declaration B (`CUSTOMER_LOGIN_REDIRECT_PATH` ≠ `INTERNAL_LOGIN_REDIRECT_PATH`; `WARNING_EVENTS` ≠ `logSecurityEvent`). `useEffectOnMount(` / `useEffectOnAny(` / `useEffectOnUpdate(` is an illegal first line. A one-line `export const env = parsed.data` may name `env` only — `NEXT_PUBLIC_*` keys need a span that contains that exact key. When several architecture HTML files share the shortest line count, **each** needs a ≥4-phase in-function walk; sequential Provider wrapping / “then getLayout” fails G5. A one-line `export const useXxx = () => {` may name the hook only — returned `t` must be in the `return {` span. Do not name `createClient` on `getCachedClaims` / `getBoardBundle`; mermaid node `createClient` needs Sources that start on `export async function createClient`. A `<dt>`/`<dd>` key-constant cite (`defineKey`) may name only that key. Sequential `configureStore({ reducer, middleware, devTools })` labeled as four phases fails G5 on a tied-shortest leaf. An Overview Key-code-entities `<table>` plus the following `<p class="sources">` is one sentence that names every token in every entities cell — a single `_app` / `proxy.ts` span is Fail; · extras are judged alone. Write one sentence per row with one cite. A tied-shortest leaf that only awaits a gate, logs an embed `error`, `.map`s rows, and applies a `DEFAULT_*` ternary is inventory, not a 4-phase walk. A camelCase stem is not a token (`occupiedY` ≠ `occupiedYByLevel`). `FAILED` is not a substring of `VALIDATION_FAILED` / `JOB_FAILED`. An inner `const` subject (`occupiedYByLevel`) must start on that inner line, not the enclosing `export`. A “starts by X” sentence must cite a span whose first executable statements are X. A `//` comment does not license `decodeImage` (`end+1` is Fail). `export const boardSlice = createSlice({` may name `boardSlice` only. A shortest leaf that is `return (a && b && c)` numbered as four phases fails G5. Glossary must be `<dl>` / `<dt>` / `<dd>` — a stub `<dl>` plus term `<p>` is Fail; every term is a `<dt>` / `<dd>` and the cite lives in the `<dd>`. Status-class gloss (`5xx`, `4xx`) is a token; comments do not license it. Overview entities-cell identifiers must already appear in that page’s prose or mermaid labels. Do not hang `requireClaims` on `MaintenancePage`. A separately written `decodeImage` is not licensed by `UTIF.decodeImage` — name `UTIF.decodeImage` only. Use lowercase `<dt>`/`<dd>` (uppercase tags do not hide tokens). Adjacent `<dt>`+`<dd>` pairs only (no dt-stack then dd-stack). A call subject (`UTIF.decodeImage`) starts on the call line. Prose `PUT`/`GET`/`POST` and routes (`/drawing_files`) are tokens. Overview row entities must both sit in that row’s one sentence and one span. Do not hang `createFirstBoardIfNeeded` / `setGitHubTokenCookie` / `getPublicBoardBySlug` on `GET` / `PublicBoardPage`. `return {` and `(error: unknown) => {` are illegal first lines. `export const ROUTES = {` may name `ROUTES` only. A tied-shortest leaf that is interceptor `match` status arms fails G5. Overview entities must be exports, not `children` / `baseURL`.

## After a review FAIL (orchestrator — not the generator)

Do **not** patch the generated HTML. Hand-edits teach the site, not the skill, and the next generator repeats the same miss.

1. Discard the output dirs (keep only review markdown if you want a paper trail).
2. Add the reviewer’s must-fix **class** to `cite-write.md` / `page-anatomy.md` / `review-rubric.md` and, when it is mechanical, to `verify-cites.mjs`.
3. Re-run this skill from Step 1 with a **new** generator subagent (fresh research + HTML).
4. Restart independent review at **round 1**. The consecutive-PASS streak resets.

## Output contract

```
<out>/
  index.html
  wiki.css
  wiki.js
  research-notes.md
  SELF_REVIEW.md
  pages/
    1-1-....html
    ...
    glossary.html
```

Open `index.html` in a browser. Mermaid must render. Sidebar current-page highlight must work.

## Do not

- Generate Markdown-only docs and call it a wiki
- Copy README / CLAUDE.md into HTML
- Use generic diagrams (`User → API → DB`) without code entities
- Cite a path you did not open
- Skip research because the repo "looks familiar"
- Reuse or patch HTML from a previous generation after a review Fail — start from Step 1
