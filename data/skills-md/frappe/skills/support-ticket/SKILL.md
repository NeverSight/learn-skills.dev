---
name: support-ticket
description: >-
  Handle Frappe/ERPNext client support tickets: triage a reported issue/error,
  request site data via sandbox-safe System Console snippets, trace code paths,
  and fix with a safe branch/commit flow. Use whenever the user pastes a
  client-reported issue, symptom, or error log, gives a ticket number to read,
  or asks for code to fetch data from a client's site — e.g.
  "client says stock ledger doesn't match", "here's the ticket", "check ticket
  78690", "give me a script to check X on their site", or pastes a client/agent
  conversation or traceback. Also use to refresh context from the latest
  communication — "check the latest client reply", "any new reply on the ticket",
  "refresh the thread".
---

# Support ticket workflow

Works for technical and non-technical users. Anyone can run steps 1–3 to triage,
request data, and draft a client reply. Steps 4–5 (ruling out customizations and
fixing) need a developer, but a non-technical user can stop at a clear answer or a
drafted reply.

Input: either a ticket number (pull the issue + email chain) or a pasted issue
description. Also pull attachments like images and xlsx/csv files; ignore videos.

Note the ticket number somewhere visible (session/task title) before digging in,
so the thread stays easy to find.

**Iterative loop, not one-shot:** classify → ask for data → analyze → go deeper
→ rule out customizations → repeat until root cause is pinned. Expect several
data round-trips. Only then fix (step 5).

**Session rules:**
- **The client only has Desk access.** No SSH, no `bench` commands, no server
  logs, no file system. Never ask for anything not reachable via the System
  Console or Desk UI.
- **Keep it tight — each step is a one/two-line read of the output + the next
  snippet.** No summaries, no restating the problem.
- Pin the app version early; reason against *that* version's codebase — branches
  diverge. Check out or read the branch/tag matching the client's installed
  version: `git -C apps/<app> show <branch>:path/to/file.py`, or
  `git -C apps/<app> grep <term> <branch> -- '*.py'`.
- Client reply drafts: as short as possible, in very simple language, and grounded
  in the findings of the investigation. **Output the reply text and nothing else**
  — no "Here's a draft" preamble, no surrounding commentary, no trailing follow-up
  question — so it can be copied and sent verbatim.
- **Customizations are a grey area — don't endorse, implement, or assist.**
  Framework customization (Client Scripts, Custom Fields, Server Scripts, Property
  Setters) lets end users close real gaps, but it is out of scope for core support.
  Don't propose, write, or implement customizations on a client's behalf. If a
  request can only be met by customization, say so plainly and stop there — no
  scripts, no how-to.

## Reading a ticket (Frappe Helpdesk)

If tickets live in Frappe Helpdesk (`HD Ticket`), pull the ticket and its email
chain with a read-only Frappe API client such as [`frappectl`](https://pypi.org/project/frappectl/)
(or the REST API directly):

- Ticket fields: `frappectl doc get "HD Ticket" <name>`
- **Email chain + internal notes:** `frappectl doc list Communication` returns
  `[]` (permission-filtered), so don't use it. Instead:
  ```bash
  frappectl api "method/frappe.desk.form.load.get_docinfo?doctype=HD%20Ticket&name=<name>"
  ```
  `docinfo.communications` = the email thread (`content`, `sender`,
  `communication_date`); `docinfo.comments` = internal agent notes.

**Refreshing the thread:** when asked to check the latest reply or refresh
context, re-run the `get_docinfo` call and read the newest entries in
`docinfo.communications` (sort by `communication_date`) — the chain is updated
on the server, so re-fetch rather than relying on what was pulled earlier.

## 1. Classify → pick the outcome

Form your own hypothesis from the code and data — the ticket and any client/agent
thread are symptoms, not a diagnosis; don't anchor on a guessed cause. Don't fix
before data confirms it. Outcomes — the later ones are often reached only after
steps 2–4:
- **Functional / "how it works"** (setting, permission, misunderstood workflow)
  → explain using the findings; draft a client reply. No fix.
- **Confirmed code bug, patchable** → fix via steps 2–5.
- **Data inconsistency** (code is correct; client's data is in a bad state —
  orphaned/stale rows, un-delinked ledger entries, broken outstanding) → cross-check
  the code against the client's actual data to prove the record, not the logic, is
  wrong; then a targeted data repair, not a code patch. See step 5.
- **Bug, but RCA = major refactor / breaking change** → tell the user that. No fix.
- **Feature request** → tell the user it's a feature request. No fix.
- **Already fixed / stale release** → nudge the client to update the app. No fix.
  Pin their commit → tag early and compare to the latest release. Many fixes
  already live on later releases. If the fix exists on a newer tag, or the symptom
  is a sync gap an update + migrate resolves, ask them to update the required apps
  and recheck before investigating further.

## 2. Ask for data — runnable code, never prose

Give a snippet the client pastes into the **in-site System Console**
(Desk → `/app/system-console`) — a RestrictedPython sandbox, NOT `bench
console`/SSH. Follow the sandbox rules below. Label every print
(`print("outstanding:", ...)`) so returned output maps back unambiguously;
batch related questions into one snippet to minimize round-trips.

## 3. Analyze → conclude or loop

- Conclusive → give the answer, done.
- Points at code → trace the implicated code paths in the pinned version;
  hunt edge cases/bugs.
- Unclear → refine hypothesis, back to step 2.

## 4. Rule out customizations (when code says it should work)

If reasoning against the pinned version says the behaviour is correct, but the
client still sees the issue AND you cannot replicate it locally, suspect a
site-level customization before calling it a core bug or a dead end. Do this
*before* step 5 — never raise a core fix for behaviour a customization owns.
If custom apps are present, check the "Audit System Hooks" report, plus
Client/Server Scripts, Custom Fields, and Property Setters on the object in
play (doctype / report / whitelisted method).

## 5. Fix

### Code bug
- Analyze edge cases + regression impact deeply before fixing; don't patch the
  symptom. Add a regression test where warranted — one that fails without the fix.
- Reproduce and verify on a dedicated test site (e.g. `<app>-test.localhost`),
  never on the client's site.
- Write the fix following the `code-style` and `frappe-app-dev` skills.

### Branching & backports

- **Branch before editing** — never edit directly on the mainline (`develop`) or
  a release branch.
- **Fix on `develop` first, then backport** to each still-maintained release
  branch; never below the oldest maintained release.
- Wait for review before committing, and open a PR only when asked.

### Data repair (data-inconsistency outcome)
Run via the client's System Console (writes persist only with the Commit box
ticked). The script must be:
- **Safe** — guard every write with the condition that proves the row is wrong
  (e.g. source doc `docstatus == 2`, row still live) so it no-ops on good data.
- **Idempotent** — re-running changes nothing once fixed.
- **Minimal** — touch only the identified bad rows, never a blind bulk update.
- **Verifiable** — print before/after so the client's output confirms the change.
Have an accountant/user confirm the correct end state first. If the same bad
state could recur, the root-cause code gap is a separate code-bug fix.

## System Console sandbox rules

Runs via `safe_exec` — same sandbox as Server Scripts.

**Only printed output is visible** (`print()`); bare expressions
output nothing. prefer **Python mode** but for complex reads use **SQL mode**. Bound queries with `limit`.

**Not allowed:**
- Sequence unpacking — `a, b = x`, `for a, b in items:`, `k, v` in a
  comprehension. RestrictedPython emits a `_unpack_sequence_` guard that isn't in
  the namespace → `NameError: name '_unpack_sequence_' is not defined`. Index
  instead (`r["a"]`, `r[0]`); keep dict values as dicts, not tuples.
- `import` (any) — blocked at compile; even indirect imports fail with
  `ImportError: __import__ not found`. You CANNOT import app code
  (`from erpnext... import x`) or reach it via `frappe.get_attr` /
  `frappe.call` (not in namespace). To test a helper's logic, **replicate it
  inline** with allowed calls; don't try to invoke the real function.
- `frappe.get_installed_apps` — not in namespace (`AttributeError`). Get apps
  via SQL: `SELECT app_name FROM \`tabInstalled Application\`` (SQL mode), or
  check one with `frappe.db.exists("Module Def", {"app_name": "erpnext"})`.
- `frappe.get_single_value` — not in namespace; use
  `frappe.db.get_single_value("Doctype", "field")`.
- `frappe.get_conf` / `conf` / `get_site_config` / `local` / `cache` /
  `get_single` — not in namespace.
- `frappe.parse_json` — use `frappe.utils.parse_json` or `json.loads`.
- `.format()`/`.format_map()` — use f-strings.
- `_`-prefixed attributes (`doc.__dict__`, `obj._x`).
- Non-whitelisted `frappe.utils.X` (e.g. `get_site_path`, `get_files_path`).
- `open()`/file I/O; non-SELECT `frappe.db.sql`.

**Allowed:**
- ORM: `frappe.get_doc` (real Document), `get_all`, `get_list`,
  `get_cached_doc`, `get_last_doc`, `get_meta`, `new_doc`, `copy_doc`,
  `get_mapped_doc`.
- `frappe.db`: `get_value`, `set_value`, `get_single_value`, `get_list`,
  `get_all`, `exists`, `count`, `get_default`, `escape`, `sql` (SELECT/EXPLAIN),
  `commit`/`rollback` (writes persist only if Commit box ticked).
- `frappe.utils`: `getdate`, `get_datetime`, `nowdate`, `today`, `now`,
  `now_datetime`, `add_days`, `add_months`, `date_diff`, `get_first_day`,
  `get_last_day`, `flt`, `cint`, `cstr`, `fmt_money`, `money_in_words`,
  `parse_json`, `get_link_to_form`.
- Misc: `print`, `frappe.log`, `frappe.msgprint`, `frappe.throw`, `frappe.qb`,
  `frappe.get_system_settings`, `frappe.session`, `frappe.form_dict`,
  `json.loads/dumps`, `_dict`, builtins (`dict/list/set/tuple`,
  `len/str/int/float/round/bool`, `range/enumerate/sorted/sum/min/max`),
  comprehensions, f-strings, loops.
