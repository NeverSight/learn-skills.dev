---
name: search
description: >
  Find an app on the App Store / Google Play and start tracking it in AppFollow, then hand structured
  app references to the feedback-analysis and aso-analysis skills. Read-only search + dedupe works on any
  plan; the add step degrades gracefully when the plan does not allow writes. Trigger on "find app X",
  "track our app", "add <app> to AppFollow".
---

# search — find + track apps

Read `using-appfollow` first (session opening, write ritual, error codes).

## Inputs

- `query`: app name (free-text search keywords).
- `store`: `as` (App Store), `gp` (Google Play), `ms`, `am` (Amazon).
- `country` (default `us`), `collection` (name; created if new), `locale`.

## Flow

0. **Session:** `whoami` (see `using-appfollow`).
1. **Normalize input.** Search takes free-text keywords only — the ASO search endpoints do not accept
   a store URL or an `ext_id`. Trim the query to the app name (strip any pasted URL down to the app
   name/title before searching).
2. **Search (read-only, any plan).** Call `aso_search_results` (optionally `aso_search_suggestions`,
   5 cr). Present numbered candidates. Auto-pick only a single exact-title match; otherwise the user
   picks.
3. **Resolve collection.** `list_collections`. If the target collection is new, run
   `add_collection_preview` → user approval → `add_collection`.
4. **Dedupe (read-only).** `list_apps`; if the app is already tracked, record it under
   `skipped_existing` and skip the add.
5. **Add (write — may be plan-gated).** `add_app_preview` → **explicit user approval** → `add_app`
   with identical args. Valid stores: `as`, `gp`, `ms`, `am`.
6. **Verify.** `list_apps` again; confirm the app now appears; capture its `apps_id`.
7. **Emit** the JSON block (below).

## Read-only degrade path (plan-gated writes)

`add_app` and `add_collection` require an **Advanced API / Custom** plan, and those routes carry **no
feature gate** — so a plan block does **not** arrive as `FEATURE_DISABLED`. It can surface as
`AUTH_REQUIRED`, `VALIDATION_ERROR`, or `UPSTREAM_ERROR`. Therefore:

- Always complete search + dedupe (read-only — works on any plan).
- Attempt the `add_*` confirm.
- On **any** error code from the add, **do not** assert a specific code. Report the candidate refs you
  found, state plainly that the add could not be completed (likely a plan limitation), and list the
  found refs under `not_added` so the report skills can still target them (they may already be tracked).

## Output (fenced JSON)

```json
{
  "added": [{"store": "as", "ext_id": "389801252", "apps_id": 12345, "collection": "Core apps", "locale": "en-US", "title": "Example App"}],
  "skipped_existing": [],
  "not_added": [],
  "collection_created": null,
  "credits_spent_estimate": 2
}
```
