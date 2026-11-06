---
name: restraint
description: Ships the smallest thing that does the job and deletes what nobody asked for.
---

# Restraint

This skill cuts a change down to the ask. It removes extra interface, options and code and treats "remove" as delete.

## Build the ask

An element, option or code path the user did not ask for is a finding unless the ask needs it to work. Work that has not shipped carries no backwards compatibility. A cut the user has not approved is a proposal, not an edit.

Label wording belongs to `copy`. Reusing an existing part belongs to `reuse`.

## Nothing beside the ask

Add no sections, badges, counts, captions, footers, icons inside buttons, sounds or decorative effects the user did not request. A count badge on every row is `restraint-no-unrequested-ui`.

## No feedback the screen already gives

Do not add a toast or a dialog for an action whose result is already on screen. That is `restraint-no-redundant-feedback`.

## The smallest build that works

Use the native element before a custom one, one app before a monorepo and a fixed value before a setting. A custom video player where `<video controls>` works is `restraint-smallest-build`. A preference nobody will change is `restraint-no-needless-setting`.

## No defensive code before release

Keep no legacy branch and no compatibility shim in unshipped work. That is `restraint-no-legacy`. Do not add a fallback for a value that is always set. That is `restraint-no-fallbacks`.

## Remove means delete

When the user says remove, delete the code and its styles, variables, routes and menu entries. "Deferred for review" is `restraint-delete-dont-defer`. A removed package that leaves its variables in `theme.css` is `restraint-remove-the-trail`.

Asked for a cleanup, list unused files, exports, styles, dependencies and leftover prototypes. Delete them once approved.

## Comments state constraints or go

Delete comments that narrate the code. Keep one only when it states a constraint the code cannot show. A narrating comment is `restraint-no-narrating-comments`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `restraint-no-unrequested-ui` | A count badge on every row | No badge |
| `restraint-no-redundant-feedback` | A toast after a move the user can see | No toast |
| `restraint-smallest-build` | A custom video player | `<video controls>` |
| `restraint-no-needless-setting` | A preference for a gap nobody changes | A fixed `--gap` |
| `restraint-no-legacy` | A legacy branch kept "for safety" | Deleted |
| `restraint-no-fallbacks` | `value ?? defaultValue` for a value that is always set | `value` |
| `restraint-delete-dont-defer` | "Deferred for your review" | Deleted, or one question |
| `restraint-remove-the-trail` | A removed package's variables left in `theme.css` | The variables removed with it |
| `restraint-no-narrating-comments` | `// Render the header` | No comment |

## Reporting

**Severity.** `HIGH` is a feature, setting or code path nobody asked for, or a "removed" item that still exists. `MEDIUM` is a fallback, a legacy branch or a leftover variable. `LOW` is a narrating comment.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Never `Approve` a file you did not read. Mark every check you could not run as `Not verified`.
