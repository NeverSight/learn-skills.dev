---
name: ui-sdk-write-code
description: Writes and edits ui-sdk code (core, the React, Vue, Svelte, Solid and web component adapters, examples, specs and scripts) the way an expert in that framework would, then checks it with the linters, the framework expert's checklist and a cold read. Use whenever you write or change code in this repo, before you call the change done.
metadata:
  internal: true
---

# Write ui-sdk code

The bar: an expert in the framework reads the file and says "this is how I'd write it", and anyone else reads it top to bottom without stopping. Readable first, then fast, never clever.

## 1. Find the twin

Every piece of code here has a twin that already does it well. Open it before you write a line, and copy its shape, names and order.

| You're writing             | Start from                                                                                                                         |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| A core component           | `packages/core/src/components/tabs/tabs.ts`, or `menu/` once it passes about 400 lines (`menu.ts`, `menu-api.ts`, `menu-parts.ts`) |
| A popup                    | `packages/core/src/components/popover/popover.ts` and its adapters, on `createPopup` in `foundation/popups/`                       |
| A React, Vue or Solid part | The same component's file in `packages/<framework>/src/`, on `createParts`                                                         |
| A Svelte part              | `packages/svelte/src/tabs/`                                                                                                        |
| A web component            | `packages/web/src/tabs.ts`, on `createParts`                                                                                       |
| An example                 | The same example in another framework: `examples/components/<name>/<framework>/`                                                   |
| A spec                     | `tests/specs/tabs*.spec.ts`                                                                                                        |

If two twins disagree, the shape is wrong in one of them. Say so instead of picking one.

Copy a twin's shape, not its comments. Older files carry more comments than the rules below allow.

## 2. Load the framework

Read the expert's knowledge file for every framework you touch: `.agents/experts/<framework>/knowledge.md`, part 1 and "Common mistakes to flag", and its `decisions.md`. It's pinned to the versions this repo installs, so trust it over memory. Write in the current idiom of that version:

- **React 19**: pure render, no `forwardRef`, `ref` as a prop, no effect where an event handler or a derived value belongs, code the React Compiler compiles without a bailout.
- **Vue 3.5**: `<script setup lang="ts">`, `v-model` on parts, `defineModel` when a component you write takes one, typed `defineProps` and `defineSlots`, no options API.
- **Svelte 5**: runes only (`$state`, `$derived`, `$props`, `$bindable`), snippets, `onclick` attributes, attachments. No `$:`, `on:`, `<slot>` or `createEventDispatcher`. Props typed with an `interface Props`. Outside `packages/svelte`, declaration tags (`{const x = $derived(...)}`) instead of `{@const}`.
- **Solid 2**: props read where they're used, never destructured; derive with memos, not effects; Solid 2 APIs only.
- **Web components**: platform first. Options reflect as attributes the way built-ins do, public events are `composed` and don't bubble (listen with `{ capture: true }`), and the user's markup stays in light DOM.

## 3. Write it

The rules in `contributing/code.md` hold everywhere. The ones that make code look generated when missed:

- **One shape.** `<Name>` root, `<Name><Part>` per slot, `render` to change the element, never `as`. Same names and the same props in every framework.
- **Names in full words** that say what a thing is. Booleans read as questions.
- **Exports listed once at the end.** Inline types. No return type annotations.
- **No comment by default.** Write one only when a reader would get the code wrong without it: a browser bug, an APG rule, a trade-off. One to three lines. Never a comment per declaration, and never one that explains the design or the data flow. Examples have none.
- **No defensive code for cases that can't happen.** Types already rule them out.
- **No helper for one caller,** and no wrapper that only renames.
- **Behavior lives in core.** An adapter that grows a listener, a focus call or an `aria-*` attribute is in the wrong layer.

## 4. Check it

Run each and check the exit code, not the output:

```sh
pnpm lint
pnpm format
pnpm typecheck
pnpm --filter <package> test
pnpm --filter examples build   # when you touched examples
pnpm test:pr                   # the specs your change reaches
```

Then run each framework's own lint rules on the files you touched: `npx eslint <files>` (`pnpm lint:idioms` runs them on the whole repo, as CI does). Fix what each one reports and run it again until all pass. Older errors are listed in `eslint-suppressions.json`; when you fix one, run `pnpm lint:idioms --prune-suppressions`.

## 5. Read it cold

Read the whole diff as the framework's expert would, using the "Review checklist" in each `knowledge.md` you loaded, and as a teammate who has never seen it:

- Would an expert in this framework write it this way? If you can name a more idiomatic version, write that one.
- Is every name clear without its comment?
- Is anything duplicated that exists elsewhere?
- Does any function do two things, or any file hold two ideas?
- Any allocation on a hot path, or a layout read after a write?

## 6. Unslop

Run `ui-sdk-unslop` on your diff. The change isn't done until it has. Before merging a change to an adapter, core, the specs, examples or framework docs, run `ui-sdk-expert-review`.
