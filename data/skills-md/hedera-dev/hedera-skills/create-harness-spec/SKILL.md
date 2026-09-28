---
name: create-harness-spec
description: Create a hedera-harness recipe — PRD, recipe file, validators, and optional stages — by grilling an idea into a runnable feature spec. Use when the user wants to turn a Hedera feature idea into harness inputs.
---

# Create Harness Spec

Grill a Hedera feature idea into a complete **recipe** for
[hedera-harness](https://github.com/hedera-dev/hedera-harness).

Load the shared vocabulary first: read
[`../harness-spec-anatomy/SKILL.md`](../harness-spec-anatomy/SKILL.md) and its
[GLOSSARY.md](../harness-spec-anatomy/GLOSSARY.md). Use those terms exactly.

Targets **hedera-harness schemaVersion 3**.

These skills are for authoring. Recipes do not list skills — product plugins
from `hedera-skills` are discovered per run and the generator picks. Keep the
run **blind**: the PRD carries journeys and outcomes; numbered assertions live
in the **evaluate checklist**.

Works in **Claude Code** (marketplace plugin) and Cursor / other agents that
load SKILL.md. Prefer `/grilling` when that skill is installed; otherwise use
the inline protocol — Claude Code typically takes the inline path.

## Step 1: Locate the target

A recipe lives at `.harness/` inside a scaffolded app. There is no other layout.

| Situation | What to do |
|-----------|------------|
| Cwd is a scaffolded app (Scaffold HBAR or `hedera-harness init`) | Author into its `.harness/` |
| Cwd is an app without `.harness/` | `hedera-harness init` adopts the harness in place |
| No app yet | `hedera-harness init <dir>` (optionally `--template <name>`) |
| Cwd already has `.harness/spec.yaml` | Check `schemaVersion`. If absent, `1`, or `2`, rewrite to v3 (or regenerate with `init` and reapply edits). `hedera-harness migrate` is gone. |

Never treat a v1/v2 recipe as loadable. `contract:` → `eval:`, drop `skills:`,
set `schemaVersion: 3`.

Paths in the **recipe file** are relative to the project root.

## Step 2: Grill

Follow [references/grilling.md](references/grilling.md). Prefer `/grilling` if
available; otherwise use the inline protocol there.

Do **not** write files until the user confirms shared understanding.

## Step 3: Emit the recipe

Prefer copying the shipped skeleton — it is always current:

```bash
cp -r "$(npm root -g)/hedera-harness/skeletons/project-harness/." .harness/
```

Then:

1. Write `.harness/prd.md` (or one file per **increment** under
   `.harness/prds/`) from the grill. Product-facing only — keep the run **blind**.
2. Fill `.harness/spec.yaml`. Required: `schemaVersion: 3`, `name`,
   `description`, and `baseline` with a command literally named `install`.
   **Leave every default commented out.** A four-key recipe is complete.
   Omit `agent:` unless the user wants Cursor (default is Claude).
3. Write `.harness/validators/static.json` and `.harness/validators/yarn.json`
   against the feature deliverables. Do not assert on `template.json` —
   create-scaffold-hbar removes it when scaffolding.
4. Do **not** add a `skills:` list. Mention relevant Hedera services in the PRD
   so the generator can pick product skills.
5. Add SMOKE / EVALUATE / CHAIN only if the user opted in during the grill —
   see `harness-spec-anatomy` → [references/stage-strategy.md](../harness-spec-anatomy/references/stage-strategy.md).
   If `prd:` is a list and EVALUATE is on, write a matching `eval:` list.
6. Install the SMOKE host package if you just enabled it — at the **project
   root**, not only inside a workspace. Doctor imports `playwright` from next
   to `hedera-harness`, and Yarn `nmHoistingLimits: workspaces` hides
   `packages/nextjs` installs.
   - SMOKE → `yarn add -D playwright` (or npm/pnpm equivalent)
   Skip the add if the root `package.json` already lists it. Do this as part
   of emit, not as a follow-up after `doctor` fails.
   CHAIN does **not** need a project install: `@hiero-ledger/sdk` ships with
   `hedera-harness`. Only the operator env vars are host-provided.

Reconstruct bodies by hand only when the skeleton is unavailable:
`harness-spec-anatomy` → [references/spec-files.md](../harness-spec-anatomy/references/spec-files.md).

## Step 4: Completion criterion

Two checks, in order:

```bash
# 1. Does the recipe load? (authoritative — schema, defaults, baseline, network)
hedera-harness doctor .harness/spec.yaml --recipe-only

# 2. Is it coherent across files? (traceability, stage pairing, blind rule)
bash <path-to>/harness-spec-anatomy/scripts/check-spec.sh <project-root>
```

`check-spec.sh` runs `doctor` itself, so running it alone is enough when the
harness CLI is installed. If it reports that the schema was **not** validated,
that is a partial result — install or upgrade the harness and rerun.

**Done when `check-spec.sh` exits clean.**

Then hand off:

```bash
# Prefer /review-harness-spec next, then:
hedera-harness run .harness/spec.yaml --max-attempts 3
# or: yarn harness:run
```

Point at the harness README for install, agent auth, and stage host
prerequisites. `hedera-harness doctor` (without `--recipe-only`) checks those.
Do not expand CLI teaching beyond these next commands.

## Additional resources

- [references/grilling.md](references/grilling.md)
- Companion: `/review-harness-spec`
- Vocabulary: `/harness-spec-anatomy`
- Upstream: [docs/authoring-a-recipe.md](https://github.com/hedera-dev/hedera-harness/blob/dev/docs/authoring-a-recipe.md)
