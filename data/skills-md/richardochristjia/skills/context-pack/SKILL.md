---
name: context-pack
description: Writes one small digest of a change — the diff, the files it touches, the API contracts and the test entry points — so review agents read that instead of re-exploring the repository. Use before a review, or when several agents would otherwise re-read the same files.
---

# Context pack

Eight cold-start agents re-reading the same seven files cost 39.5M cache-read tokens in a traced run — 94% of that run's price. The pack replaces the re-reading with one shared page.

## Input

- The repo and the base ref (the same base the review uses).
- The plan folder, if there is one: `.plans/<task>/plan.md`.

## Build it

1. **The diff**, complete for the changed lines:

   ```sh
   git diff "$BASE"...HEAD
   ```

   Drop lockfiles, generated output and vendored directories. If the diff alone is over the budget, split it by file group and say which group is where.

2. **The files it touches**, one line each: path, what the file is, and its role in the change. No file bodies.

3. **The API contracts** the change crosses: endpoint, method, request shape, response shape, and where the shape is declared (the type or interface file, with a line number).

4. **The test entry points**: the test files that cover the changed source files, and the command that runs them.

5. **The plan's acceptance criteria**, verbatim, one per line, with any criterion marked `manual:` flagged as outside automated verification.

6. **What not to re-derive**: the facts a reviewer would otherwise spend turns rediscovering — which field decides the behaviour, which component owns the call, what the previous behaviour was, and the known-broken things that are not part of this change.

## Write it

Write `.plans/<task>/context-pack.md`:

```markdown
# Context pack

BASE: origin/master
CHANGED: 7 files, +283/-32

## What this change does
<two or three lines>

## Files
- `components/button/StartClassButton.vue` — start button; emits `started` on a successful start
- ...

## API contracts
- `POST /api/program-batch/start/{batchCode}` → 204; success is what emits `started`
  declared in `types/program-batch-student.d.ts:41`

## Test entry points
- `components/button/StartClassButton.test.ts` — `npx vitest run components/button/StartClassButton.test.ts`
- `pages/classes/_components/ClassesCard.test.ts` — `npx vitest run pages/classes/_components/ClassesCard.test.ts`

## Acceptance criteria
1. ...
2. manual: the list stops reporting NOT ATTEMPTED after a start (needs a real backend)

## Do not re-derive
- `batchStatus === "NOT ATTEMPTED"` is the signal; `courseStatus` is not.
- The modal's query key is built once at setup, so it does not follow a changed prop.

## Diff
```diff
<the diff>
```
```

## Rules

- **Budget: 3,000 tokens** (about 2,200 words). If it does not fit, cut prose before cutting the diff, and cut the diff by file group before dropping anything.
- Every claim carries a `file:line` anchor, so a reviewer can open exactly one place.
- No file bodies. If a reviewer needs more, they open that file — the pack's job is to say where, not to replace the file.
- The pack states the diff, the change's intent and the criteria. It does not argue that the change is correct; that is the reviewer's job.
- Write it once per change. If the branch moves, rewrite it rather than patching it.

Report one line: `Context pack: <path> (<n> words)`.
