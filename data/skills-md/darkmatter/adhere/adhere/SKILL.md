---
name: adhere
description: Gather a repository's non-deterministic coding conventions into adhere rules (Markdown files with a description and code that must, or must never, be written, judged by Jev), configure adhere, run it, and calibrate thresholds. Use when setting up adhere in a repo, when the user asks to turn conventions, AGENTS.md guidance, ADRs, or review feedback into lint rules a normal linter cannot express, or when tuning adhere findings.
---

# Gather adhere rules from a repo

adhere is a linter for rules a normal linter cannot check. Each rule is one
sentence in RFC 2119's words plus code that must be written and code that must
never be; Jev judges every source file against it and returns a probability. Your job is to find the conventions a repo already
has, write the ones that need judgment as rule files, and tune until the
report is trustworthy.

## 1. Survey where conventions live

Read, in this order, and note every "we always" or "never" statement:

- `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md` convention sections.
- `docs/`, ADRs, design notes, `CONTEXT.md`.
- Lint and type configuration (`oxlint`, `eslint`, `biome`, `tsconfig`). These
  tell you what is already enforced deterministically, so you can exclude it.
- Recent review feedback: `gh pr list --state merged --limit 20`, then
  `gh pr view <n> --comments` on a few. Repeated review comments are unwritten
  rules.
- The code. Find the module others copy from: the canonical service, the
  canonical error type, the canonical test. Those files are your references.

## 2. Keep only what needs judgment

For each candidate ask: could a regex, an import check, or the type checker
flag every violation? If yes, it belongs in the existing linter, not adhere.
Drop it or file it as a lint request.

Keep rules about intent, shape, and placement:

- "Sequential effectful steps use `Effect.gen`, not nested `flatMap`."
- "A call over the network carries a timeout and a retry schedule."
- "Business logic depends on a config service, not on `Config.*` reads."
- "Domain errors are `Schema.TaggedError` classes, not thrown `Error`."

Skip rules a preset already covers. Run `adhere lint --help` and read
`presets/effect/` in the adhere repo before writing Effect rules; extend with
`presets: ["effect"]` and add only what is specific to this repo.

## 3. Write each rule as a file

Default location `.adhere/<topic>/<slug>.md`, next to the config and the
cache. Use `docs/adhere/<topic>/<slug>.md` with `rules: "./docs/adhere"` in the
config only when the user wants rules kept with the repo's docs; rules read
that way apply project-wide, and nested `.adhere/` directories are not read.
The path without `.md` is the rule id.

````md
---
description: One sentence saying what code must be, then what it must never be.
threshold: 0.8
---

Optional prose for readers on GitHub. adhere ignores it.

## Must

```ts
// Correct code lifted from this repo, trimmed to the pattern.
```

## Never

```ts
// Optional: the incorrect form this rule catches, as it appeared in the repo.
```
````

Rules for the rule:

- `description` is one sentence, specific, in the same words as the headings:
  what code must be, and what it must never be. Jev reads the description
  with the code, and "must" in both is one demand; vague words ("properly",
  "correctly") give it nothing to judge.
- A heading names the code under it only when it is the word alone: `## Never`,
  not `## Never do this`. The next heading at its level or higher ends it.
- The `must` block is real code from the repo, not invented, and only correct
  code: Jev compares files to it, so incorrect code there teaches the wrong
  thing. Incorrect code goes under `## Never`, which Jev reads as what a
  violation looks like. Add one whenever violations have a recognizable
  shape, ideally one found in the repo's history: over the effect preset, a
  `never` block raised how well Jev told violations from compliant code under
  every wording tried. A rule with no single correct form can be only a
  `never` block.
- A convention that is a guideline rather than a requirement says "should" in
  its description and puts its code under `## Should` and `## Should not`. A
  rule is one or the other; it cannot mix the two.
- One pattern per file. Two patterns in one `must` block blur the probability.
- Jev reads code without its comments, except comments that say `@adhere`. A
  rule about comments, such as doc comments on exports, needs
  `includeComments: true` in the config.
- Rules skip tests: `.test.ts` and `.spec.ts` files, and files under `test/`,
  `tests/`, `__tests__/`, or `fixtures/`. A rule about tests says `tests: only`
  in its front matter, and one that holds in tests as well `tests: include`.
- A nit, or a rule that tends to flag code wrongly, says `level: warning` in
  its front matter: its findings show in amber and do not fail CI.
- `threshold` is optional. Start without it; set it in step 5 if needed.

## 4. Configure

Put the config at `.adhere/config.ts`. `adhere.config.ts` and
`.adhere.config.ts` also load; keep one. A config is optional when `.adhere/`
exists or a preset is passed on the command line. `adhere init` scaffolds it
with `defineConfig`, adds `@drkmttr/adhere` as a dev dependency, and writes
`.adhere/tsconfig.json` so the editor resolves its types; the native binary
supplies the import either way:

```ts
import { defineConfig } from "@drkmttr/adhere";

export default defineConfig({
  presets: ["effect"],
  threshold: 0.75,
  exclude: ["**/generated/**"],
});
```

To quiet a preset rule that does not suit the repo, override it rather than
copy it: `overrides: { "alchemy/providers/idempotent-delete": "warning" }`, or
`"off"`, or `{ threshold: 0.9 }`. The id is the one the report shows.

`exclude` lists globs, from the working directory, of files no rule judges.
Exclude generated and vendored code the skipped directories do not already
cover, since findings there are noise no one will fix.

Commit `.adhere/cache/` with the code, so the team and CI reuse its judgments
instead of paying for them again. Uncached files need a TypeSafe AI API
key: one saved by `adhere login`, or `TYPESAFE_API_KEY`, which takes
precedence; in this org it comes from SOPS via `just shell`.

## 5. Run and calibrate

```sh
adhere validate              # decodes the config and rules; reports their wording, rules a linter could check, and contradictions
adhere lint                  # or: adhere lint --preset effect
adhere lint --threshold 0.9  # re-reads the cache, sends nothing
```

Then, per rule, read the findings and decide:

- Many hits at 0.80 to 0.90, mostly not violations: the description is too
  broad. Narrow it (say what is out of scope) or raise that rule's
  `threshold`. Prefer narrowing; a threshold hides, a sentence explains.
- Hits on code that follows the pattern through a different API: the `must`
  block is too specific. Use the repo's most general correct example.
- Zero hits: plant a deliberate violation in a scratch file, run, confirm the
  rule fires, remove the file. A rule that cannot fire is not a rule.
- Hits at 0.9 and above: read them first. They are usually real.

To verify and fix the findings themselves, one at a time, use the adhere-fix
skill, which `adhere skill fix` prints.

Threshold changes never re-judge; only edited rules do (per rule) and edited
files do (per file). Iterate on wording freely, it costs one request per file
per changed rule.

## 6. Report

Give the user: the rule ids written and where, the config path, the finding
count at the chosen threshold and at 0.9, and the rules you dropped as
deterministic with where they belong instead.
