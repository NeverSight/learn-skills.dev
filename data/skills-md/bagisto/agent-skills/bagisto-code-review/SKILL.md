---
name: bagisto-code-review
description: Use when reviewing Bagisto code changes or a pull request for correctness, convention compliance or quality, or when asked whether a change is ready to merge. Trigger phrases include "review", "code review", "PR review", "is this correct", "conventions", "violations", "code quality", "ready to merge".
requires: bagisto-coding-standards
license: MIT
---

# Code Review

What to look for in a Bagisto change, ordered so the findings that matter arrive
first. Pint and the test suites already decide the mechanical questions — spend
the review on what they cannot see.

## What the tools already cover

Do not spend review effort on these; run them instead.

| Checked by | Covers |
|---|---|
| `vendor/bin/pint --test` | Formatting, spacing, import order, trailing commas |
| `vendor/bin/pest` | Behaviour the suite asserts |
| `php artisan bagisto:translations:check` | A key missing from any of the 22 locales |
| Playwright | The browser layer |

If a review comment could have been an exit code, the fix is to run the tool,
not to write the comment.

## Blocking

A change should not merge with any of these outstanding.

**Correctness**

- A query inside a loop, or an N+1 from a missing eager load. The cost is
  invisible on seeded data and appears on a real catalogue.
- An unbounded `->get()` on a table that grows — products, orders, customers.
  Paginate or chunk.
- A repository method that touches seller- or customer-owned rows without
  scoping to the owner.
- A raw fragment (`whereRaw`, `selectRaw`, `DB::raw`, `orderByRaw`) built by
  interpolating a request value.

**Security**

Owned by the **`bagisto-coding-standards`** skill — load it when the diff touches
authorization, rendered output, input, uploads, raw SQL, secrets or payments,
and work its checklist rather than a remembered list. The two that account for
most real findings:

- A storefront query selecting by an id from the request without scoping to the
  authenticated customer.
- A DataGrid closure interpolating a value into an HTML attribute without
  `e()` — tags are stripped for you, quotes are not.

**Architecture**

- `DB::` or model queries outside a repository. The one sanctioned exception is
  a DataGrid's `prepareQueryBuilder()`.
- A new model without its Contract, Model, Proxy and Repository.
- A package registered in `bootstrap/providers.php` but not `config/concord.php`,
  or the reverse.
- Core files edited to serve an extension. Marketplace and B2B Suite both forbid
  core edits outright — the change belongs in a bound subclass, a
  `view_render_event` listener, or a Concord model swap.
- A user-facing string not passed through `trans()`.

## Worth raising, not blocking

- **Duplication on the third occurrence.** Twice is a coincidence; three times
  is a helper.
- **A method whose body needs a comment to follow.** The codebase forbids
  comments inside method bodies, so this is a signal to extract a named method,
  not to add prose.
- **A docblock or member order violation in a file the change touches.** A
  pre-existing violation in a touched file is the author's to fix.
- **A test that asserts a count or a list position.** Both drift as the shared
  database grows; assert on the named record instead.
- **An event fired on the single-record path but not the mass-action path**, or
  the reverse.

## How to review

1. **Read the tests first.** They state what the author believes the change
   does. A change with no test for the bug it fixes is the first question.
2. **Ask what breaks it.** For each claim, look for the input that falsifies it —
   an empty collection, a second locale, a guest, a channel that is not the
   default.
3. **Check the reverse.** A regression test that passes with the fix reverted
   guards nothing. Where the fix is subtle, ask the author to show it failing.
4. **Follow one path end to end** — request, form request, controller,
   repository, model, view — rather than reading the diff hunk by hunk. Most
   real defects sit in the seam between two files that each look fine.
5. **Confirm the gates ran**, and which were skipped.

## Writing the finding

State the defect, then the input that triggers it, then the fix. A finding
without a concrete failure is a preference, and should be marked as one.

> `CategoryRepository::saveMediaAltText()` writes to
> `translateOrNew($locale)` where `$locale` can be the literal `all` — the
> category create form posts `locale=all`. On MySQL that silently creates a row
> with an empty `name` and `slug`; on PostgreSQL it violates NOT NULL. Expand
> the sentinel to every locale before writing.

Separate what you verified from what you suspect. "This is an N+1" and "this
might be an N+1, I did not check the relation" are different claims, and
conflating them costs the author more time than saying so.

**REQUIRED SUB-SKILL:** Use bagisto-change-verification before calling any change done.
