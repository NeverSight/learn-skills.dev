---
name: creating-flow
description: "Creates Robomotion automation flows with the @robomotion/sdk TypeScript builder. Owns the full lifecycle: requirements → plan → build → validate → deploy. Also use when the user has a plan ready and wants the flow code written."
---

# Robomotion Flow Builder

Robomotion is an RPA platform with a TypeScript SDK and a visual node editor. This skill is a thin index over the reference docs in `./docs/`. Read the relevant doc when a topic comes up — don't try to memorize it from this file.

## Hard Rules (SDK rejects violations at validate time)

The SDK enforces these. Violations throw at `robomotion validate` / `build` with descriptive messages, so the agent never silently produces broken flows:

1. **Node IDs MUST be 6-char lowercase hex** — `/^[0-9a-f]{6}$/`. `f.node()`, `.then()`, `f.edge()` reject non-hex IDs (`'begin'`, `'label'`, `'maps'`, uppercase) at registration. Generate each id at random (`openssl rand -hex 3`); never copy an example id from these docs and never write a pattern like `a1b2c3` or `aa11bb`. See `./docs/reference/id-format.md`.
2. **Subflow node ID = `subflows/<id>.ts` filename, exactly.** Both must be 6-hex. The Designer's "enter subflow" UX depends on the match.
3. **`f.addDependency(namespace, version)` is validated against the live package index.** `version` must be concrete (`'latest'` is rejected) and must exist in the package's published `versions` list. `namespace` must exist in `https://packages.robomotion.io/stable/index.json`. Run `robomotion get packages <ns>` or `robomotion describe package <ns>` to resolve real versions before calling `addDependency`. Never invent a version.
4. **Terminal nodes (`Debug`, `Log`, `Stop`, `GoTo`, `End`, `WaitGroup.Done`) have 0 outputs** — wire TO them via `f.edge()`, never `.then()` from them.
5. **Every `Core.Flow.GoTo` references a `Core.Flow.Label` id that exists in the same flow file.**
6. **A flow file is a declaration the Flow Designer can READ, not a program only Bun can run.** The Designer parses `main.ts` and each `subflows/*.ts` statically, one file at a time, draws what it understood, and **regenerates the whole file from the canvas on every save** - whatever it could not read is gone from git after the person's first save. So: the ONE import is `@robomotion/sdk`; every node is a literal `f.node()` / `.then()` / `f.edge()` written inside the `create` callback (no helper functions, no loops, no `.map()`); every prop is a literal, an array/object of literals, a scope helper over one, or a string built from **same-file** `const`s with a template, `+` or `[..].join('\n')`; no spreads (`{ ...SHARED }`), no shorthand props, no imported helpers in a `func`. A shared helper string is declared again in each file that uses it. `robomotion validate` refuses the rest with "the Flow Designer cannot read it". Full table: `./docs/reference/project-format.md`.
7. **The program is the flow; a Function node is glue code, written only where necessary, and written for a person to read.** We do write code, but only where a step needs it: a Function shapes `msg` for the next node. The work goes into nodes: **SQL lives in the SQL node** with `{{{field}}}` placeholders, never string-built in JavaScript; a rule the person would name is its own Function with `outputs: 2`; formatting is the screen's job; there is no helper library, and never one pasted into every node. The code is formatted: one statement per line, blocks on their own lines, indented, blank lines between parts. No line limit - a long Function that does one thing and reads top to bottom is fine. `robomotion validate` refuses crammed code ("several statements on one line", "a whole block on one line") and the same block opening three or more Functions. Where each urge belongs: `./docs/reference/function-nodes.md`.

## Required First Line

Every flow file (`main.ts` and every `subflows/*.ts`) starts with this exact import — copy verbatim, including helpers you don't currently use (Bun won't flag dead imports, but missing ones become runtime `ReferenceError`):

```ts
import { flow, Message, Custom, JS, Global, Flow, Credential, AI } from '@robomotion/sdk';
```

For library files swap `flow` for `library` / `subflow`. Full reference: `./docs/reference/imports.md`.

## Builder grammar

- `f.node(id, type, name, props)` — param order. Only emit non-default props (Go runtime fills defaults from pspec).
- `.then()` for sequential, `.edge()` for multi-port wiring.
- `Message(name)` for variables · `Custom(value)` for literals · `JS(expr)` for one-line JS · `Credential({vaultId, itemId})` for secrets.
- **A field takes a scope helper based on its TYPE IN THAT NODE, not its `in*`/`opt*` name — and the SAME name can differ across nodes.** Every `in*`/`out*` port takes a scope helper (`Custom('…')` / `Message()`); a bare literal there is silently dropped. For `opt*` fields, don't guess from the name — check `get_node_schema`: a field typed `object` + `variableType` (even a numeric one) takes a scope helper; a plain `number`/`boolean`/`enum` field takes a bare literal and must NOT be wrapped. **The very same property can differ by node:** `Core.Browser.OpenLink` `optTimeout` is a plain number → `optTimeout: 32`, but `Core.Browser.WaitElement` `optTimeout` is `variableType:Integer` → `optTimeout: Custom('30')`. Mismatching either way VALIDATES but FAILS TO LOAD on the robot (`flow_error: failed` / `Config parse error`, no nodes run): wrapping a plain field sends an object to a scalar; leaving a variable-backed field bare sends a scalar into a `{scope,name}` slot. Enums/booleans are always plain (`optBrowser: 'chrome'`, `optMethod: 'post'`, `optInsecure: true`); `in*` ports and value fields like `optUrl`/`optDownloadDir`/`optNofBranches` always take `Custom()`/`Message()`.
- `func` is a literal string (NOT `JS()`).
- Common runtime props also take raw values: `delayBefore: 2`, `delayAfter: 0.5`, `continueOnError: true`.
- ES5-only inside `func`: no `=>`, no template literals, no `const`/`let`, no destructuring. No `require()` / `fs` / `Buffer` / `process` (pure JS sandbox).
- Loops: `Label → ForEach → body → GoTo`. `Stop` is standalone, wired via `f.edge()` on ForEach port 1.
- **`GoTo`/`Label` are not only for loops: a long wire is a `GoTo`.** Any edge that would travel back, or across other rows to reach a shared or late-declared node (an error handler, a common "say why" responder, a rejoin after a branch), draws a diagonal over everything in between - once per branch - and the canvas becomes unreadable. Put a `Core.Flow.Label` beside the target, and end each far branch with a `Core.Flow.GoTo` sitting in its own row. A `GoTo` has no outgoing wire, so the long edge stops existing rather than being redrawn shorter. Rule of thumb: **more than about two rows of travel, make it a `GoTo`**, and name it after where it goes so the row still reads left to right. See `./docs/patterns/branches.md`.
- Library projects use `library.create(id, name, fn)` with `Begin`/`End` nodes (no `.start()`). Inline subflows use `subflow.create(name, fn)`.
- Every flow ends with `.start()`. Every flow has a `Core.Flow.Stop` node — **except an app backend**: a flow triggered by `Robomotion.Apps.Action` is a long-lived service behind a Robomotion App's screens and must never stop, so it has no `Stop` and no `End`. See the `building-app` skill.
- `Core.*` packages (`Core.Trigger`, `Core.Browser`, `Core.Programming`, `Core.CSV`, `Core.Flow`, `Core.Vault`, `Core.Net`, `Core.Excel`, …) are **embedded in the robot** — NEVER call `f.addDependency('Core.*', …)`. The Designer auto-loads them. Only call `f.addDependency(ns, ver)` for non-`Core.*` packages. When updating an existing flow, NEVER bump existing `addDependency` versions; only add missing ones.
- **Comments & canvas layout** — `Core.Flow.Comment` nodes (with an `optText` markdown string) title the flow and fence its logical phases; the visual arrangement — node `positions`, comment box colors/sizes, and Sugiyama-style layering — lives in `main.designer.ts`. Layout is cosmetic (never affects runtime) but it's what makes a flow readable. See `./docs/patterns/comments-and-layout.md`.

Full grammar: `./docs/sdk-grammar.md`. Architecture: `./docs/architecture.md`.

## Diagnostic map

Map an error symptom to the doc that fixes it. When `validate_flow` fails, look up the symptom here before reading the full failure trace.

| Symptom | Likely cause | Fix |
|---|---|---|
| `[SDK] Invalid node ID '<x>' in f.node('<x>', …)` | Semantic / non-hex ID | `./docs/reference/id-format.md` — pick 6-hex |
| `[SDK] Invalid subflow filename '<x>.ts'` | Subflow filename non-hex | Rename file + update parent SubFlow node ID to match |
| `version must be concrete; 'latest' and empty are not allowed` | `f.addDependency(ns, 'latest')` | `robomotion describe package <ns>` → pin a real version |
| `package '<ns>' not found in repository` | Hallucinated namespace | `robomotion get packages <kw>` → use the real namespace |
| `version '<v>' is not published for <ns>` | Wrong version pinned | Pick from `available_versions` returned by validator |
| `Cannot chain from node (outputs=0)` | `.then()` after `Debug`/`Log`/`Stop`/`GoTo`/`End` | Wire TO terminals via `f.edge()`, never FROM them |
| `the Flow Designer cannot read it` (an import, a spread, a helper, a value "not a const declared in this file") | The file is a program, not a declaration (hard rule 6) | Inline: one `@robomotion/sdk` import, nodes written in the callback, same-file `const`s, no spreads. `./docs/reference/project-format.md` |
| `several statements on one line` / `a whole block on one line` / `the same block opens N Function nodes` | Code not written for a person, or a helper library pasted into the steps (hard rule 7) | Format it (one statement per line, blocks on their own lines); SQL into the SQL node with `{{{field}}}`; one Function per rule; formatting on the screen. `./docs/reference/function-nodes.md` |
| `Invalid input port 0. Node has 0 input(s)` on a Label | Wired into `Core.Flow.Label` (Label has 0 inputs in some pspecs) | Use `Core.Flow.GoTo` with `optNodes.ids: [<labelId>]` to jump to the Label |
| `Vault has to be selected` at runtime | Missing `optCredentials` on `Core.Vault.GetItem` | `./docs/patterns/credentials.md` |
| `Property 'optCredentials' requires vault credentials but has empty/placeholder values` | An OPTIONAL credential prop (e.g. `Core.Excel.Open` for password-protected files) set with `_`/blank placeholders | Omit `optCredentials` entirely unless you have a real vault reference — `./docs/patterns/credentials.md` |
| `inSelectorType` invalid value `'xpath'` (allowed: `xpath:position`, `css`) | Wrote `inSelectorType: 'xpath'` — not a valid enum value | For XPath just OMIT `inSelectorType` (it's the default); the XPath enum literal is `xpath:position`, never `xpath`. CSS ⇒ `inSelectorType: 'css'`. `./docs/patterns/browser.md` |
| `inLabel` property not found on GoTo | Wrong property | `optNodes: { ids: [...], type: 'goto', all: false }` |
| `Core.Programming.If` not found | Node doesn't exist | `Core.Programming.Function` with `outputs: 2` (`./docs/patterns/conditions.md`) |
| Wrong node name (e.g. `Core.CSV.Read`, `Browser.Click`) | Common naming mistake | `./docs/reference/node-naming.md` |
| `inPath: Custom('$Home$/file')` literal not resolved | System variables only resolve in Function nodes | `global.get('$Home$') + '/file'` (`./docs/reference/system-variables.md`) |
| Flow VALIDATES but FAILS TO LOAD on robot (`flow_error: failed` / `Config parse error`, no nodes run) | An `opt*` value shape mismatches its per-node type: a plain `number`/`bool`/`enum` field wrapped in `Custom()`, OR a `variableType`/object field left as a bare literal | Check `get_node_schema` per node. Enums/bools are plain (`optBrowser: 'chrome'`). Numeric fields depend on the node: `OpenLink.optTimeout: 32` (plain `number`) vs `WaitElement.optTimeout: Custom('30')` (`variableType:Integer`). `in*` ports + `optUrl`/`optDownloadDir`/`optNofBranches` always take `Custom()`/`Message()`. |
| Any CSV / Excel / Sheets / SQLite / Pandas / Airtable / DOMParser / DataTable node in scope | Custom data shape is wrong (e.g. `{header: [...]}`, rows as arrays) | **MANDATORY** read `./docs/patterns/data-tables.md` — the format is `{columns: [...], rows: [{key: value}]}` with row keys matching column names |
| Write produces empty cells / `ErrFilePath` / "table not recognized" | `header` instead of `columns`, or rows are arrays not objects | `./docs/patterns/data-tables.md` — the property is `columns`, never `header`; rows are objects keyed by column name, never positional arrays |

Drift-prone reminders before every `Write` / `Edit` of flow code:

- Never output TypeScript as chat text — always use `Write` / `Edit`. Plans and explanations stay in chat.
- Hex IDs from the start. Cross-references (`optNodes.ids`, `Catch.optNodes.ids`, subflow filenames) must use the same hex.
- For browser flows: explore the live page first (`Skill(exploring-browser)` or `mcp__browser__*` after `ToolSearch` warmup). Don't guess selectors. **`Core.Browser.*` element nodes (`ClickElement`/`TypeText`/`GetValue`/`SetValue`/`WaitElement`/`Select`) default `inSelector` to XPath — translate CSS handles you find (`#email`, `input[type="email"]`) to XPath (`//input[@id='email']`) and omit `inSelectorType`; use a CSS string ONLY with `inSelectorType: 'css'` (plain literal — `inSelectorType` is an enum, so NEVER `Custom('css')`). A CSS string with the default engine fails at runtime with "element not found". Never write `inSelectorType: 'xpath'` (invalid; the value is `xpath:position`). Also: enum/dropdown opts (`optBrowser`, `optProxy`, `optProxyAuth`, `optClickType`) take a PLAIN string/boolean — NEVER `Custom()`; wrapping an enum in `Custom()` emits a `{name,scope}` object and the robot rejects the node at load with `Config parse error` (flow never starts). `Custom()`/`Message()` are only for variable value fields (selectors/URLs/text/paths). See `./docs/patterns/browser.md`.**
- For any flow that READS or WRITES tabular data (CSV / Excel / Google Sheets / Excel 365 / SQLite / Airtable / Pandas / DataTable / DOMParser) — read `./docs/patterns/data-tables.md` BEFORE adding the node, both for the Function that builds the table AND for the reader/writer node. That doc names the exact node and shows its properties (e.g. write CSV = `Core.CSV.WriteCSV` with `inFilePath` + `inTable`; write Sheets = `Robomotion.GoogleSheets.SetRange`; etc.) and the `{columns: [...], rows: [{key: value}]}` format (never `{header: ...}`, never rows-as-arrays). **Do NOT `unified_search` / `search` for data-output nodes — search returns TEMPLATES, not nodes, and looping on it wastes the turn. The node names are in data-tables.md; once you know the node, use `get_node_schema` for its exact properties.** When a search returns templates instead of the node you need, stop searching and read the relevant pattern doc.
- For any `Robomotion.ChatAssistant` flow in **conversational** mode — read `./docs/patterns/conversational-chat.md` BEFORE writing it. One user message is one `ChatIn → ChatOut` run and **`ChatOut` is the only thing that unlocks the composer**, so a branch that ends anywhere else (an error, a missing `ChatOut`) freezes the chat until the page is reloaded — the most common bug in these flows, and it looks like a product fault rather than a flow fault. That doc also carries the streaming wiring (Callback In `stream_delta` → `Streaming Text`, and **no `Text` node repeating the answer**) and the attachments wiring (`GetAttachments`, because `msg.payload.files` is names and versions, never files on disk).
- Validate BEFORE save — `save_flow` only compiles, it does NOT pspec-validate.

## Pattern reference

Read these docs before writing the corresponding code:

| Pattern | Doc |
|---|---|
| Loops (Label → ForEach → body → GoTo) | `./docs/patterns/loops.md` |
| Conditions (Function with `outputs: N`) | `./docs/patterns/conditions.md` |
| Credentials (vault + categories) | `./docs/patterns/credentials.md` |
| Browser automation (incl. proxy) | `./docs/patterns/browser.md` |
| Exception handling (Catch, continueOnError) | `./docs/patterns/exceptions.md` |
| Branches & parallel (ForkBranch, WaitGroup) | `./docs/patterns/branches.md` |
| Subflows (Begin/End, multi-output) | `./docs/patterns/subflows.md` |
| Data tables (CSV / Excel / Sheets / SQLite / Pandas / Airtable / DOMParser / DataTable) — **MANDATORY** before writing any code that produces or consumes `msg.table` | `./docs/patterns/data-tables.md` |
| Captcha solving | `./docs/patterns/captcha.md` |
| Migrating a legacy `Robomotion.Assistant` flow → `Robomotion.ChatAssistant` | `./docs/patterns/assistant-migration.md` |
| Conversational Chat Assistant (turn contract, Stop, streaming, attachments) — **MANDATORY** before writing any conversational-mode chat flow | `./docs/patterns/conversational-chat.md` |
| Comments, grouping & Sugiyama layout (title box, colored phase headers + description text, box sizing, `main.designer.ts`) | `./docs/patterns/comments-and-layout.md` |

References:

| Topic | Doc |
|---|---|
| Imports (every scope helper + example) | `./docs/reference/imports.md` |
| Node ID format (the hex rule) | `./docs/reference/id-format.md` |
| The project format both the Designer and the CLI can read and save (hard rule 6) | `./docs/reference/project-format.md` |
| Function nodes: glue code written only where necessary, formatted for a person; where each urge belongs (hard rule 7) | `./docs/reference/function-nodes.md` |
| System variables (`$Home$`, `$TempDir$`) | `./docs/reference/system-variables.md` |
| Node naming (wrong → correct) | `./docs/reference/node-naming.md` |
| Credential categories (field layouts) | `./docs/reference/credential-categories.md` |

For schemas, examples, and package docs, use the `robomotion` CLI (it's already on `PATH`, call it by bare name):

| Need | Command |
|---|---|
| Cross-source fuzzy/semantic search | `robomotion search <query>` |
| Find packages | `robomotion get packages [query]` |
| Find nodes | `robomotion get nodes [query] [--in <ns>]` |
| Find templates | `robomotion get templates [query] [--category <name>] [--tag <name>]` |
| Full node schema + docs + example | `robomotion describe node <type>[,<type>...]` |
| Package info (incl. published versions) | `robomotion describe package <namespace>` |
| Template source | `robomotion describe template <slug>` |
| Package docs (llms.txt) | `robomotion docs <namespace> [--grep <pattern>]` |
| List vaults / vault items | `robomotion get vaults` · `robomotion get vault-items <vault-id>` |
| List robots | `robomotion get robots` |

> **Public templates repo:** [`github.com/robomotionio/robomotion-templates`](https://github.com/robomotionio/robomotion-templates) is the canonical source. Prefer cloning/forking a matching template over building from scratch.

## Workflow

Full step-by-step: **`./docs/workflow.md`**. Outline:

0a. **The project.** A flow is a folder: `main.ts` at its root, a git checkout of the flow's own repository, signed in. When there is none yet, make it, in the folder the person wants it under:

    robomotion create flow "<short human name>"

   It makes the folder (a slug of the name, or `--dir <path>`), signs it in when it is not (a code and a link the person approves in their browser; run it in the background, it waits for the approval; `--workspace <host>` when they named one), creates the flow on the server and checks it out there. Then `cd` into it. An existing checkout (a `git clone` from the flow's Home card) needs nothing; if `robomotion auth whoami` says not logged in, `robomotion auth login --workspace <host>` in it.
0. **Gather requirements** (interactive only) — credentials (commit to a vault-item pick, don't quiz the user; **never ask for the secret itself** — `vault_picker`, or ask them to add it to Vault first: `./docs/patterns/credentials.md`), URLs, files, iteration, error handling.
1. **Discover** — `robomotion search`, `robomotion get nodes`, `robomotion docs <namespace>` (MANDATORY for every non-`Core.*` package).
2. **Plan** — output plan as chat text, then `AskUserQuestion(["Build it", "Modify plan"])`.
3. **Write** — read 1-2 relevant `./docs/patterns/*.md`, verify property names with `robomotion describe node`, then `Write` `main.ts` (and any `subflows/<id>.ts`). For browser flows: explore live first.
4. **Validate** — call `validate_flow` MCP tool. Pspec-checks AND dependency-checks. MUST run BEFORE save.
5. **Save** — `save_flow` if registered (Designer / pi); else `git add -A && git commit -m "..." && git push` from inside the flow dir (the checkout `robomotion create flow` made pushes with no setup). **This is the terminal step.** Stop here and report success — do NOT chain into running the flow. Running is a separate user request handled by the `running-flow` skill.

If invoked in **direct mode** ("Write main.ts for X", "Generate a flow that does Y"), skip 0-2 and jump to 3.

**Browser caveat:** if code changed after the initial exploration (different selectors, new actions), re-verify selectors against the live page before saving. Selectors are owned by Step 3, not a post-save step. **And close the exploration browser the moment exploring ends** - whichever tool opened it (robomotion-browser-mcp, a Playwright MCP) - before writing the flow; never leave it open while the flow is built or run. The robot opens its own.

## Canonical example (simple chain)

For loop / conditional / subflow / catch examples, see the corresponding pattern docs — they have richer working snippets.

```typescript
import { flow, Message, Custom } from '@robomotion/sdk';

flow.create('main', 'Simple Flow', (f) => {
  f.node('42ec21', 'Core.Trigger.Inject', 'Start', {})
    .then('7dbafc', 'Core.Programming.Function', 'Setup', {
      func: `msg.url = 'https://example.com'; return msg;`
    })
    .then('a06926', 'Core.Browser.Open', 'Open Browser', {
      outBrowserId: Message('browser_id')
    })
    .then('8e1c4b', 'Core.Browser.OpenLink', 'Navigate', {
      inBrowserId: Message('browser_id'),
      inUrl: Message('url'),
      outPageId: Message('page_id')
    })
    .then('d52f73', 'Core.Browser.Close', 'Close', {
      inBrowserId: Message('browser_id')
    })
    .then('b9a841', 'Core.Flow.Stop', 'Stop', {});
}).start();
```

## CLI & MCP

- `robomotion` — self-sufficient CLI. Builds, validates, runs, searches, inspects. `robomotion help` for the full verb list.
- `robomotion-browser-mcp` — MCP server for interactive browser exploration (used by `exploring-browser` and `mcp__browser__*` tools).

The `robomotion` CLI shells out to `robomotion-sdk-mcp` internally for search-backed commands and calls `api.robomotion.io` directly for run/stop/vault/robot operations. No additional MCP servers required.

## Regression suite

This skill ships with an automated eval suite at `./evals/` — Tier A pinpoint regressions (handcrafted fixtures, one rule each) plus Tier B integration tests (live `main.ts` from the public `robomotion-templates` repo). Run `bun run skills/creating-flow/evals/run-evals.ts` from the agent-skills root before committing edits to this SKILL.md or the `./docs/` files. See `./evals/README.md` for adding new cases and the assertion grammar.

## Related skills

- `validating-flow` — schema validation
- `testing-flow` — behavioral tests
- `running-flow` — execute on robot
- `searching-packages` — find packages, nodes, templates
- `exploring-browser` — interactive browser automation
- `reversing-network` — convert a browser flow to HTTP after capturing traffic
