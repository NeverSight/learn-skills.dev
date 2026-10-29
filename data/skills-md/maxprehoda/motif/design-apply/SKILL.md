---
name: design-apply
description: "Updates a codebase to use the design tokens from design-ratify, in four batches ordered from safest to riskiest: exact matches, near matches, Tailwind colors to named roles, then everything else. Commits each batch separately. Use as phase 4 of design-system, after design-ratify."
---

# Design Apply

Replace values in the code that aren't tokens with the matching token. Work in four batches and commit each one separately, so if something looks wrong you can tell which batch caused it.

## Before you start

```bash
test -f DESIGN.md || echo "MISSING"
```

## Never make up a value

When a value has no matching token, stop and note it. Don't use the closest token, and don't add a new one.

Keep a list as you go. At the end of the phase, show it to the user as questions. Each value is either a gap in the system or a value that shouldn't exist, and the user decides which.

## Batch 1: exact matches

Values that already equal a token but are written out by hand, like `p-[16px]` to `p-4`. Nothing looks different. Apply these across the whole repo.

## Batch 2: near matches

Values within half a spacing step of a token, like `pb-[15px]` to `pb-4`.

Before making the changes, tell the user how many there are and the biggest single change. For example: "47 changes, the biggest is 15px to 16px."

## Batch 3: Tailwind colors to named roles

For example, `text-neutral-700` to `text-muted-foreground`.

This needs judgment, not find-and-replace. The same gray can be body text in one component and a disabled button in another, and those need different roles.

Go one component at a time: read it, decide the right role for each color, and update the whole file.

## Batch 4: everything else

Values with no obvious token. Handle each one on its own. Don't batch them.

## For each batch

```bash
git checkout -b design-apply-batch-N
# make the edits
npm run build          # or the project's own check command
git diff --stat
```

Tell the user what changed, which direction each change went (bigger or smaller, lighter or darker), and the biggest single difference. Wait for them to review before starting the next batch.

## Finish

Run the linter and report what's left, grouped by rule. It isn't installed until phase 5, so if `npm run design-lint` doesn't exist yet, run `node <design-enforce skill folder>/assets/design-lint.mjs`. For each remaining finding, say whether it's a deliberate exception or a gap in the system.
