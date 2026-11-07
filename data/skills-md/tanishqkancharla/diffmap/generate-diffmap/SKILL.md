---
name: generate-diffmap
description: Create and update living specs and code walkthroughs with diffmap. Use when planning work, implementing from a spec, updating a spec, or explaining code changes.
---

# Living spec

A spec is one Markdown file at `specs/<short-kebab-case-name>.md` that shows the current system, the plan, and the work done. Update it as the plan changes and work lands. For a walkthrough of an existing pull request, use its spec if it has one; otherwise write under `.diffmap/`. Check the repo's paths and symbols before writing.

**Settle scope first.** Read the relevant code before writing. When the design, scope, or phase split is unclear, check with the user before writing much: offer the options and your pick.

## Serve and share

Run from the repo root:

```sh
npx @tanishqkancharla/diffmap list                   # reuse the URL if this file is already served
npx @tanishqkancharla/diffmap serve specs/<name>.md
npx @tanishqkancharla/diffmap share specs/<name>.md  # only when asked; prints https://diffmap.dev/g/<id>
```

Leave the server running and give the user the file path and URL. Open the browser only when asked. Before sharing, commit finished work and point its references at the commit, as in [When a phase is complete](#when-a-phase-is-complete): `share` saves each referenced commit's diff into the gist, but a reference without a commit only opens the file as it was when shared. A shared gist is unlisted: anyone with the URL can read it, including every file it snapshots. A spec on a pull request is also at `https://diffmap.dev/<owner>/<repo>/pull/<n>/specs/<name>.md`, pinned to a commit.

## Shape

Write for someone who needs to understand the change quickly. Start from what changes for the person using it, such as a screen, command, API call, or error, then work back toward the implementation as far as the reader needs. A spec usually has a problem overview, a solution overview, goals and non-goals, phases, and **References**; let the content decide what each needs.

**Phases.** Keep each small enough to commit alone. Headings are plain when planned, ⏳ in progress, and ✅ done. Open each with a short **Today** and **Proposed** from the client's view, then explain it however suits the change: a new flow might want a diagram and a call stack, a refactor a call stack diff, a dependency bump a sentence or two. Match the length to the change, and say each thing once, where it belongs. A spec explains the change; it is not a task tracker. End each phase with its `changes` fence, after the walkthrough and before the next phase or section, not right after Today and Proposed; leave it empty until the phase is committed.

**Visuals.** Diagrams, call stacks, and code often explain a change better than paragraphs, so reach for one when prose gets long. Add one only when it shows the reader something they need, not to fill a slot.

The views fit one model: services receive messages, update their state, and send messages on. Each view looks between services or inside one, at every path or at one message's trace:

|                    | Every path                                       | One message                                                        |
| ------------------ | ------------------------------------------------ | ------------------------------------------------------------------ |
| Between services   | `mermaid` flowchart: who exists, who owns what   | `services`: a message crossing services, with the state it changes |
| Inside one service | Pseudocode and types: its state, payloads, logic | `callstack`: how it turns one message into a result                |

Use `services` when the parts keep state, run at the same time, or fan out; use a call stack when they are function calls that return, branch, or return early. In a `services` diagram, state is what you would find inside a service if you paused between steps; a result passed back is a reply event, not state. To explain a step, put a `>` note under its event, its update, or a service name on its own line. Mermaid sequence and state diagrams are lighter options. If a view needs more than about 7 services, collapse some and explain them separately.

- To show a change, add `diff` after `mermaid` or `services` and start each line with `-` (Today only), `+` (Proposed only), or a space (both), as in a call stack. For code, use a `diff` fence.
- Title Mermaid diagrams with `[Title]` after the language, as in `mermaid diff [Invalid records stop before storage]`. A `services` fence uses `start "caption"` before its first step as the title of the whole diagram, with a `>` line under it that summarizes the full process in a few sentences; caption each step with what happens.
- Label nodes and arrows with real names, and link existing source with `%% ref` directives.

**Call stacks.** Write rows as data flow, `result = function(inputs)`, with `return` rows where they matter. Mark rows `-` (original), `+` (change), or a space (unchanged); a diff compares the same function before and after. Nest calls with `├──` and `└──`. Link real functions with source references; an unlinked helper is pseudocode, not a promised API. Keep stacks to about a dozen rows, splitting deep flows into an overview and a stack per changed callee.

**Code.** Keep fences short and on the point the paragraph makes; elide unchanged code with `// ...`. Highlight lines with `{2-3}` after the language (or rows with `{3-4}` after `callstack`), and explain with notes at the bottom instead of long comments: `// [!note symbol] text` for a name wherever it appears, `// [!note L3-L5] text` for lines counted from the top of the fence. Call stacks take the same notes with `#`.

**Links.** Link existing source with [references](#source-references); write planned symbols as plain text.

## Prose

Follow Orwell's six rules from "Politics and the English Language" in all prose, comments, and diagram labels. Code names are not jargon.

## Example phase

This example uses illustrative files and a commit SHA, not Diffmap source paths. Its change crosses a few layers, so it uses several views; a smaller phase needs fewer.

````md
### ⏳ Phase 1: Validate request input

**Today**

The handler passes records straight to the service. A client that sends an empty name gets a success response, and the bad record surfaces later as a storage error the client never sees, so they keep sending bad input.

**Proposed**

A client that sends an empty name gets an error naming the `name` field, so they can fix the request right away. Bulk import in Phase 2 needs every saved record to be valid, so this check comes first.

From the client's side, the same empty-name request now fails at once:

```ts
const response = await client.saveRecord({ name: "" });
// before: { ok: true }
// after:  { ok: false, error: "name must not be empty" }
```

Today every record reaches storage. In the proposed flow, a valid record follows the same save path, but an invalid one returns an error before storage. The unlinked `validateInput` helper is pseudocode, not a proposed public API:

```mermaid diff [Invalid records stop before storage]
 flowchart LR
-    A[requestHandler] -->|record| B[existingService]
+    A[requestHandler] -->|record| V[validateInput]
+    V -->|valid record| B[existingService]
+    V -->|invalid record| E[Return name error]
     B -->|record| D[Storage]
     %% ref node:A [[src/request.ts#requestHandler]]
     %% ref node:B [[src/service.ts#existingService]]
```

The call stack shows how the validation result controls the return path:

```callstack
 response = requestHandler(record) [[src/request.ts#requestHandler]]
-└── return existingService(record) [[src/service.ts#existingService]]
+├── error = validateInput(record) # reject empty names
+├── if error: return error
+├── result = existingService(record) [[src/service.ts#existingService]]
+│   ├── storage.save(record)
+│   └── return { ok: true }
+└── return result
```

In code, the handler returns before the existing save:

```ts {2-3}
function requestHandler(record: RecordInput) {
  const error = validateInput(record);
  if (error) return error;
  return existingService(record);
}
// [!note validateInput] Returns an error when `name` is blank, otherwise undefined.
// [!note L3] Storage never sees an invalid record.
```

The new check:

```ts
function validateInput(record: RecordInput) {
  if (record.name.trim() === "")
    return { ok: false, error: "name must not be empty" };
  return undefined;
}
```

```changes

```
````

## When a phase is complete

Before starting the next phase:

1. Commit the code. If the phase took several commits, use `<base>..<head>` wherever these steps say SHA.
2. Put that SHA in the phase's `changes` fence at the end of the phase. It renders the phase's summary card. Under the SHA, list the files a reviewer should read, one path per line, in the order to read them: usually the client-facing entry point first, then down the layers. Leave out files that need no thought, such as lockfiles, generated code, snapshots, fixtures, and mechanical renames; the card folds them under "N other files".
3. Point every reference the phase changed at the commit: stack rows, `%% ref` directives, and prose.
4. Update diagrams, call stacks, and pseudocode to match what was built, and mark the heading ✅.
5. Commit the spec update separately; it names the code commit's SHA.
6. Restart `serve`; it checks commit references at startup.

The example phase keeps its walkthrough, with references pointing at the commit, and ends with:

````md
```callstack
 response = requestHandler(record) [[a1b2c3d:src/request.ts#L8-L20]]
-└── return existingService(record) [[src/service.ts#existingService]]
+├── error = validateInput(record) [[a1b2c3d:src/validate.ts#L1-L9]]
+├── if error: return error
+├── result = existingService(record) [[src/service.ts#existingService]]
+│   ├── storage.save(record)
+│   └── return { ok: true }
+└── return result
```

```changes
a1b2c3d
src/request.ts
src/validate.ts
```
````

## Source references

Paths are relative to the repo root.

- `[[path/to/file.ts#symbolName]]` links a TypeScript or JavaScript declaration; qualify ambiguous ones, as in `[[src/store.ts#Store.save]]`.
- `[[path]]` links a file; `[[path#L12-L30]]` a line range.
- `[[<sha>:path#L12-L30]]` links lines in a commit, or `<base>..<head>` for a phase over several commits, where `<base>` is the commit before the first. Lines are numbered after the commit, so deleted lines cannot be linked. Find them with `git show <sha> -- <path>` and `git show <sha>:<path> | nl -ba`.
- A reference without a commit opens that file's uncommitted changes, or the current file when it has none. A shared gist opens the file as it was when shared.
- In prose, references render as clickable inline code; wrap one in backticks to show the syntax.
- In Mermaid, `%% ref node:<id> [[reference]]` links a node or participant and `%% ref edge:<index> [[reference]]` an edge or message, counting from zero in declaration order. Use one directive per target, with several references when needed.

Fences: `mermaid` draws a diagram, `services` an animated diagram of services, their state, and the events between them (add `diff` after either to mark lines `-` or `+`), `callstack` stack rows, `changes` a commit or range summary (empty for uncommitted changes) with the files to review listed under it, and `html` trusted HTML you wrote. Other languages are pseudocode and types, with optional `{…}` highlights and `[!note …]` lines. `[Title]` after the language, as in ` ```callstack [Request flow] `, titles a call stack, code fence, or Mermaid diagram.

## Feedback

When diffmap gets in your way or the user has feedback on it, such as a rendering bug, a confusing error, a missing feature, or advice in this skill that did not work, open an issue on the diffmap repo. Search first, and comment on a matching issue instead of opening a duplicate:

```sh
gh issue list --repo tanishqkancharla/diffmap --search "<keywords>" --state all
gh issue create --repo tanishqkancharla/diffmap --title "<short summary>" --body "<details>"
```

Say what you did, what you expected, and what happened, with the diffmap version (`npx @tanishqkancharla/diffmap --version`) and the smallest Markdown that shows the problem. Issues are public, so leave out private code, file contents, paths, and gist links unless the user agrees. Give the user the issue URL.

## Look up the rest

- Full reference and fence syntax → [diffmap README](https://github.com/tanishqkancharla/diffmap#link-call-stacks-to-source-changes)
- Worked examples → [annotations](https://github.com/tanishqkancharla/diffmap/blob/main/fixtures/annotations.md), [diagrams](https://github.com/tanishqkancharla/diffmap/blob/main/fixtures/references.md), and [services](https://github.com/tanishqkancharla/diffmap/blob/main/fixtures/services.md) fixtures
