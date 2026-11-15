---
name: antislop-forms
description: "Form, validation, and UX-state rules: empty/loading/error/offline states, keyboard-focus, recovery, and edge cases. Map to antislop-master section G (P4). Use when building or auditing any form, list, or interactive flow."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-forms

> Form and UX-state rules for anti-ai-slop. Map to **G-1 … G-11** (P4, quality/UX slop) in `antislop-master`.
>
> This is the part people skip when they talk about "AI slop" as a color problem. A beautiful interface with no states is unfinished — and that's a bigger tell than any gradient.

---

## The state contract

**Every data-driven view needs five states.** Not one gray placeholder — five deliberate designs:

| State | When | Must show |
|-------|------|-----------|
| Loading | content is fetching | a skeleton/spinner that matches layout, not a blank flash (G-4) |
| Empty | there is no data | a helpful message + a next action (G-3) |
| Error | a call failed | what happened + a real retry path (G-5) |
| Offline | connection lost | a clear disconnected banner + local cache note (G-7) |
| Success | an action worked | confirmation of what happened next (G-6) |

If a view only has the happy path, it's **not** finished. (G-11 speaks to this: polish ahead of function is the deep tell.)

## Forms

- **Validation on every field** with inline, field-level errors — not one banner at the top. (G-6)
- **Validate on blur and submit**, and **recover** the user's input on error.
- **Success confirmation** after submit (a toast, an inline success, a redirect), never silent.
- **A delete / destructive action needs a real confirm.** (G-8)
- **Disabled buttons must not be the only feedback** — explain *why* it's disabled.

## Interaction honesty

- **A button or link that does nothing is P4.** Remove it or wire it. (G-1)
- **Dead links / nav items pointing nowhere** are findings. (G-2)
- **Every interactive element** reachable by keyboard, with a visible focus state. (G-9, G-10)

## Edge cases

- **Zero results** for a search/filter → a designed "no matches" state. (G-8)
- **Empty list** → designed empty state, not a blank panel. (G-3)
- **Very long content** doesn't break the layout (overflow). (K-1)

---

## Audit checklist

- [ ] Each data view has loading / empty / error / success. (G-3–G-6)
- [ ] Offline state handled where data matters. (G-7)
- [ ] Fields validate with inline, recoverable errors. (G-6)
- [ ] No button or link that does nothing. (G-1, G-2)
- [ ] Full keyboard reach + visible focus. (G-9, G-10)

Findings cite the code from `antislop-master` plus one honest reason.
