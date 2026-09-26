---
name: access-control-testing
description: Use when testing whether users can access data or actions they shouldn't — IDOR/BOLA, horizontal and vertical privilege escalation, multi-tenant isolation, forced browsing, function-level authorization (BFLA), and mass assignment. The #1 cause of real-world breaches.
---

# Access Control Testing (FIND/EXPLOIT — OWASP A01)

## Overview
Verify that every object and every action enforces "is *this* caller allowed?" server-side.
Broken access control is the most common and highest-impact real-world flaw — and the easiest
to miss because the happy path works perfectly.

**Core principle:** Authentication proves *who you are*; authorization proves *what you may do*.
Test the second one on every object and every action — not just the UI-visible ones.

## Applies when / Skip when
- **Applies when:** the app has authentication, multiple users, roles, or multi-tenant data —
  any resource or action that should be restricted. (Almost every non-trivial app.)
- **Skip when:** the app is fully public/anonymous with no per-user or privileged data → N/A.
- **If N/A:** report "access-control-testing: N/A — no auth/multi-user surface" and stop. Don't
  invent access boundaries that don't exist.

## ⚠️ Authorization
Use test accounts you created on an app you own/are authorized to test. Two accounts (A and B)
plus one admin/one low-priv account is the cleanest setup.

## The test matrix (run every cell)
| | Read | Write/Update | Delete | Admin action |
|---|---|---|---|---|
| **As another user (horizontal)** | A reads B's object? | A edits B's? | A deletes B's? | — |
| **As lower privilege (vertical)** | user hits admin read? | user hits admin write? | — | user invokes admin fn? |
| **Unauthenticated** | no token → data? | no token → mutate? | — | no token → admin? |

If any cell succeeds, that's a finding.

## Method
1. **Capture a legitimate request** as user A (note every id, uuid, slug, filename).
2. **Swap the object reference** to B's resource, keep A's session → IDOR/BOLA.
3. **Swap the session** (remove token / use lower-priv token) on privileged endpoints → BFLA / vertical.
4. **Force-browse** hidden routes (`/admin`, `/api/internal`) with a normal account.
5. **Mass assignment** — add fields the UI never sends (`role`, `isAdmin`, `userId`, `price`).
6. **Check every method** — `GET` may be guarded but `PUT`/`DELETE`/`PATCH` forgotten.

See `references/access-control-tests.md` for concrete request recipes and edge cases.

## Quick reference — bug classes
| Class | Test |
|-------|------|
| IDOR / BOLA | Change an id/uuid/filename to another user's; do you get their data? |
| Horizontal privesc | Act on another *same-level* user's resources. |
| Vertical privesc | Low-priv account reaches admin function/data. |
| BFLA | Admin endpoint guarded in UI but callable directly by anyone. |
| Multi-tenant break | Tenant A reads tenant B (swap `org_id`/`tenant_id`). |
| Mass assignment | Inject privileged fields into the request body. |
| Forced browsing | Guess/enumerate unlinked privileged routes. |

## Output
Findings in the register: which account hit which endpoint/object, the exact swapped request,
what was exposed, and horizontal vs vertical. Severity is almost always High+.

## Hand-off
Confirmed on a running app → reproduce via **`active-pentest`**; chain with others in
**`vulnerability-chaining`**; fix via **`security-hardening`** (deny-by-default, server-side checks).

## Common mistakes
- Testing only as admin — you'll never see the bug. Always test as the *lower* privilege.
- Trusting that a hidden/unlinked endpoint is safe — enumerate and call it directly.
- Checking `GET` only — mutations are where damage happens.
- Assuming UUIDs are safe — they leak (in responses, logs, referrers) and are still IDOR-able.
- Forgetting predictable patterns: sequential ids, base64'd ids, guessable filenames.
