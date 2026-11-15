---
name: ui-sdk-unslop
description: Removes generated-looking code from a ui-sdk diff or files, like comments that restate the code, filler JSDoc, defensive checks for impossible cases, one-caller helpers and vague names, without changing behavior. Use as the last step of any change, or when asked to clean up, trim comments or remove slop.
metadata:
  internal: true
---

# Unslop

Scope is the diff (`git diff` against the base) unless you're given files. Behavior never changes: the same tests pass before and after, and nothing public is renamed.

## What goes

Each pattern, with what replaces it.

**A comment that says what the next line does.** Delete it. If the line isn't clear without it, rename something.

```ts
// Close the popup when Escape is pressed.
if (event.key === "Escape") close()
```

**A comment on every declaration.** Most constants, fields and functions need none: the name and the type say what they are. Delete each one that doesn't stop a reader from getting the code wrong.

**A comment that explains the design.** What a value holds, where it's kept, which attribute it lands on, who reads it. The code says that. Keep the one fact it can't show, in a line, or delete the comment.

```ts
// Before
// The site's color scheme, shown on <html> as `data-color-scheme`, which the
// stylesheet's colors follow. It's kept under "theme", the key the site used
// before, so readers keep what they chose.
const colorScheme = createColorScheme({
  storage: createLocalStorage("theme"),
  global: true,
})

// After
// "theme" is the key the site used before, so readers keep their choice.
const colorScheme = createColorScheme({
  storage: createLocalStorage("theme"),
  global: true,
})
```

**A comment longer than three lines.** Cut it to the reason. An explanation that needs more goes in the docs page, a test title or `contributing/`. `pnpm lint` flags it (`comment-length`).

**A comment that narrates history or the task.** "Now we", "Updated to", "Fixed the bug where", "As requested". Delete it. Git holds the history.

**A section banner.** `// ---- Helpers ----`, `// State`. Delete it. Split the file if it needs signposts.

**JSDoc that repeats the name.** `/** The value. */ value`. Say what the reader can't see: the default, the unit, when it's called, what happens on change. `pnpm lint` catches field docs that only repeat the name; write the rest the same way.

**A hedge or a sales word in a comment or a doc.** "Robust", "seamless", "comprehensive", "simply", "just", "easily", "ensure", "leverage", "utilize", "note that", "it's important to". Cut the word; if nothing is left, cut the comment.

**A defensive check the types already rule out.** `if (!items) return` on `items: Item[]`, `?? []` on a value that's never undefined, `try` around code that can't throw. Delete it. Narrow `unknown` at a boundary instead.

**A cast or `!` with no reason.** Make the type right, or say why in a comment.

**A one-caller helper, or a wrapper that only renames.** Inline it, unless its name explains something the call can't.

**A name that says nothing.** `data`, `result`, `item2`, `handleClick2`, `temp`, `flag`, `isValid2`. Name what it is: `highlightedItem`, `isOpen`, `onTriggerPress`.

**An option nobody passes,** a parameter with one value, a config object for one setting. Delete it.

**Logs, probes and commented-out code.** Delete them.

**In examples, any comment at all.** Only tool directives stay (`svelte-ignore`, `eslint-disable`, `@__PURE__`).

## What stays

- A comment that says why, in three lines at most: a browser bug and the browser, an APG rule, a trade-off, a link to the spec or test that pins the behavior.
- The word "primitive", and parentheses that hold code names, like "the trigger (`MenuTrigger`)".
- JSDoc on every public field and export. Make it say more; don't delete it.

## Steps

1. List what you'll change, by file, before touching anything.
2. Make the changes.
3. Run `pnpm lint`, `pnpm format`, `pnpm typecheck` and the unit tests for the packages you touched. Check exit codes.
4. Delete each comment left in the diff and reread the code. If it still reads right, leave it deleted.
5. Read the diff once more. Revert any change that doesn't make the code easier to read.
6. If one pattern showed up in three or more files, propose a lint rule for it in `scripts/check-code.mjs` or `scripts/check-comments.mjs`.
