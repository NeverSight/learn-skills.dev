---
name: odoo-migrate-to-20
description: >
  Migrate a custom Odoo module (or a whole addons folder) from Odoo 14, 15, 16, 17, 18 or 19 to
  Odoo 20 and prove it installs and runs. Copies the module into a separate Odoo 20 addons tree,
  runs Odoo 20's own upgrade_code scripts safely, scans for every known 14→20 breaking change
  (manifest, Python/ORM, override signatures, renamed xmlids and fields, controllers, views, server
  QWeb t-esc, ir.access security, Owl 3 backend JS, publicWidget→Interactions, jQuery/Font
  Awesome/Bootstrap 4 removal, website builder, eCommerce, portal, tours and tests, secrets), checks
  every JS and Python import against the real Odoo 20 source, fixes the rest by hand with parallel
  per-area subagents, then loops install + headless-browser smoke tests and flow tours on a throwaway
  database until clean, and finishes with a code review.
  Use when the user says "migrate <module> to 20", "make it installable on Odoo 20", "port to v20",
  "upgrade module from 16/17/18 to 20", or invokes /odoo-migrate-to-20.
compatibility: >-
  Agent-neutral (Agent Skills format). Needs a shell with bash, python3, git and rsync; an Odoo 20
  checkout with a Python 3.12+ venv; PostgreSQL 16+. Chrome/Chromium for browser tests.
metadata:
  version: "1.1.0"
  odoo-target: "20.0"
  odoo-sources: "14.0-19.0"
---

# Migrate an Odoo module to Odoo 20

The goal is a module that **installs cleanly and works** on Odoo 20, migrated the way current Odoo
core code is written. Compiling is not enough: several 20 changes are **silent**. Server `t-esc`
renders nothing, `_sql_constraints` are dropped, `name_get` is never called, `oe_chatter`
disappears, and overrides with an old signature crash only when called. So every scan finding
counts, not only install errors.

This skill works with any coding agent that can read files and run shell commands (Claude Code,
Codex, Cursor, Antigravity, Gemini CLI, Copilot, OpenCode, …). Scripts live in the `scripts/`
folder next to this `SKILL.md`; below, `S` means that absolute path (e.g.
`S=~/.agents/skills/odoo-migrate-to-20/scripts`). Knowledge lives in `references/`: open files
there by path whenever a step names one.

## Configuration: run once per machine, and whenever something looks off

```bash
$S/doctor.sh                                   # show auto-detected settings + check prerequisites
$S/doctor.sh ODOO20_CONF=/path/odoo20.conf --write   # override anything, then save the config
```

The settings (`scripts/env.sh` documents each one):

| Setting | Meaning |
|---|---|
| `ODOO20_SERVER` | Odoo 20 community checkout (required) |
| `ODOO20_ENTERPRISE` | enterprise addons (optional) |
| `ODOO20_PYTHON` | Python ≥ 3.12 with Odoo 20 requirements (required) |
| `ODOO20_CONF` | odoo.conf holding DB credentials (optional) |
| `MIG20_DB_*` | a PostgreSQL ≥ 16 server for throwaway test databases |
| `MIG20_TARGET_ROOT` | where migrated projects go (`<root>/<project>/<module>`) |
| `MIG20_OLD_SOURCES` | older Odoo checkouts, used to look up what an API used to be (optional) |

- Everything is auto-detected when possible. The saved config is
  `~/.config/odoo-migrate-to-20/config.env`.
- If `doctor.sh` says NOT READY, show the FAIL lines to the user and help fix them before
  migrating. Typical fixes: clone Odoo 20, create the venv, pip install requirements and
  `websocket-client`, start PostgreSQL 16.
- Never guess machine paths in commands. Use the variables (`$ODOO20_SERVER`, …): source
  `$S/env.sh` in a shell to get them.

Knowledge files:

| Reference | Read when |
|---|---|
| `upgrade-code-tool.md` | always (what the automatic pass did and did wrong) |
| `lessons-learned.md` | always, before starting; append at the end |
| `manifest-and-modules.md` | manifest, depends on removed/merged modules |
| `python-orm.md`, `field-model-renames.md` | any `.py`, any renamed field |
| `controllers-http.md` | `controllers/`, `odoo.http` imports, routes |
| `views-xml-data.md` | `views/`, `data/`, actions, menus, cron, search views |
| `qweb-reports-mail.md` | server templates (website pages, reports, portal, mail) |
| `security-ir-access.md` | `security/`, groups, secrets |
| `backend-js-owl3.md` | backend code in `static/src`: field/view widgets, systray, assets |
| `website-interactions.md` | frontend code in `static/src` (publicWidget, jQuery) |
| `website-builder-snippets.md` | snippets, snippet options, themes, header templates |
| `website-sale-portal.md` | website_sale overrides, cart routes, portal home |
| `scss-bootstrap-icons.md` | Bootstrap 4 classes, Font Awesome icons, SCSS |
| `tests-and-tours.md` | `tests/`, `static/tests/`, tours; writing the smoke flow tour; reading browser test failures |

Odoo ships its own guideline skills in `$ODOO20_SERVER/skills/` (`odoo-guidelines`,
`odoo-web-guidelines`, `odoo-security`, `odoo-review`). Use them for house style and the final
review: through your agent's skill mechanism if they are installed, or by reading
`$ODOO20_SERVER/skills/<name>/SKILL.md` and the files it points to directly.

## Guardrails

- Never modify the source module, `$ODOO20_SERVER` or `$ODOO20_ENTERPRISE`.
  `run_upgrade_code.sh` enforces this for the automatic pass; you enforce it for manual edits.
- Only throwaway databases named `mig20_*` on the configured server. `install_test.sh` drops them.
  Never touch other databases.
- **Never comment out code, assets, data files or xpaths to make the install pass.** A feature
  that can't be migrated now is listed in `MIGRATION_20.md` under "Not migrated", with the reason.
- Never write an API, field, template id, xpath target, widget or icon name from memory. Grep
  `$ODOO20_SERVER` (and `$ODOO20_ENTERPRISE`) first; the references say where.
- Migration is not refactoring. Change what 20 requires, in the style of current core code, and
  keep the module's structure and behaviour.
- Commit after each phase in the project repo, so the user can review the diff phase by phase.
- Found a credential in the source? Remove it from the migrated copy, and tell the user to revoke
  it: it is still in the original and its history.
- Installing a missing Python library into `$ODOO20_PYTHON`, or anything outside the target
  project, changes the user's environment. Say what you install.

## Workflow

### 0. Inputs and plan

1. Run `$S/doctor.sh`. It must say READY, or the user must accept what is missing (for example,
   no enterprise).
2. Resolve the **source module path(s)** and a **project** name. Default project: the source's
   parent folder name, lower-cased.
3. If a whole addons folder is given, list its modules.
4. Read each manifest's `depends`:
   - A custom dependency must be migrated first, into the same project, bottom-up.
   - A third-party vendor module (OCA, Cybrosys, Emipro, …): ask whether an upstream 20 release
     exists before migrating it yourself.
   - A removed or merged core module: see `manifest-and-modules.md`.
5. Read `references/lessons-learned.md`.
6. **Fork check:** run `python3 $S/fork_check.py <source_module_dir>`.
   - If it prints `VERDICT: FORK`, the module is a renamed copy of an Odoo (or vendor) module that
     also exists in Odoo 20. Use the **rebase path**: after step 1, run
     `python3 $S/rebase_fork.py <UPSTREAM_20> <DEST>`. It replaces the copy with the upstream 20
     module renamed to the fork's name; model names are kept, so the schema is unchanged.
   - Then diff the fork against `<UPSTREAM_OLD>`: rename it in a scratch copy, then `diff -ru`.
     Re-apply only the meaningful custom delta and list the rest in the report.
   - Skip step 2 (upstream 20 code is already migrated), and continue with steps 3 and 5–8.
   - Report the licence the upstream code carries: `rebase_fork.py` prints a LICENSE line when it
     differs from the fork's.

### 1. Prepare

```bash
$S/prepare.sh <source_module_dir> <project> [<from_version>]   # prints DEST, FROM, BASELINE
python3 $S/scan.py <DEST> --summary                           # "before" numbers for the report
```

Then fix the manifest by hand:
- `version` becomes `20.0.x.y.z`;
- `license` present;
- `qweb` key moved into `assets`;
- `depends` fixed;
- every listed file exists.

Commit `[MIG] <module>: manifest`.

### 2. Automatic pass

```bash
$S/run_upgrade_code.sh <DEST> <FROM>
python3 $S/scan.py <DEST> --fix-tesc --summary     # mechanical t-esc/t-raw -> t-out
```

- Read every WARNING/ERROR line the first command prints, especially from ir-access
  (`security-ir-access.md` explains how to judge public access).
- It must end with `OK: core and enterprise untouched`.

Commit `[MIG] <module>: upgrade_code + t-out`.

### 3. Scan

```bash
python3 $S/scan.py <DEST>            # grouped by severity/area, with file:line
python3 $S/scan.py <DEST> --json     # for subagents
python3 $S/scan.py <DEST> --icons    # fa-* names to map
```

Areas: `manifest python renames controllers views qweb security backend-js website-js website
website-sale assets scss tests`.

Beyond regexes, the scanner:
- imports every third-party library with `$ODOO20_PYTHON`;
- **really imports every `odoo.*` import** on Odoo 20 (moved helpers, renamed enterprise classes).
  An import inside `try/except ImportError` that fails on 20 is reported SILENT: the except branch
  would always run;
- **resolves every JS import** (`@addon/...`, relative, `@odoo/owl`) to a file in Odoo 20 and
  checks each named import is exported. A missing file breaks the whole asset bundle;
- validates tours against Odoo 20's strict tour schema: step keys, `run` helpers, selectors, and
  steps that relied on the pre-18 implicit click;
- compares every override of a core method with its Odoo 20 signature;
- checks every external xmlid the module references against Odoo 20;
- looks for secrets.

### 4. Manual pass

**4a. Global renames first**, done by you and not by subagents, because they cross Python, XML and
JS:
- the `renames` area;
- `groups_id` → `group_ids`;
- `res.groups` `category_id` → `privilege_id` + a privilege record;
- stock/sale field renames;
- `xmlid-missing` findings.

Check each field or xmlid in Odoo 20 before renaming. Commit.

**4b. Areas.** Do small areas inline.

If your agent can start sub-agents (for example Claude Code's Agent tool, Codex or Cursor
background agents), delegate the areas with substantial rewrites (typically backend JS and website)
to one sub-agent per area, started together so they run in parallel. Otherwise, work through the
areas yourself in the order A, B, C, D, re-reading the area's references before each one. The
table and the rules below apply either way.

| Agent | Areas | Owns files | References |
|---|---|---|---|
| A | python, controllers | `*.py` | python-orm, controllers-http, field-model-renames, security-ir-access |
| B | views, qweb (backend), security, reports, mail | backend views, actions, menus, data, security, report and mail XML | views-xml-data, qweb-reports-mail, security-ir-access |
| C | backend-js, assets, scss (backend) | backend `static/src/**`, manifest `web.assets_backend` | backend-js-owl3, scss-bootstrap-icons, upgrade-code-tool |
| D | website-js, website, website-sale, scss (frontend) | frontend `static/src/**` **and** the website/portal/shop QWeb templates they bind to | website-interactions, website-builder-snippets, website-sale-portal, qweb-reports-mail, scss-bootstrap-icons |

- Split `static/src` by bundle: `web.assets_frontend` and website bundles go to D, the rest to C.
- Website templates go to D with their JS, because selectors and markup must change together.
- The `tests` area (tours, `tests/`) is yours, **after** A–D: tour selectors must match the final
  migrated markup. Follow `tests-and-tours.md`.

Each subagent prompt contains:
- the module path;
- its exact file list;
- its findings (from `--json`, filtered to its areas);
- the absolute paths of the reference files to read in full first;
- the values of `$ODOO20_SERVER` / `$ODOO20_ENTERPRISE`;
- the source module path, for the intended behaviour;
- the renames done in 4a;
- these rules:
  - confirm every API, template id, xpath target, widget and icon in the Odoo 20 source with grep
    before writing;
  - copy the shape of the closest core example named in the reference;
  - edit only your files;
  - never comment code out;
  - keep behaviour identical;
  - do not run Odoo;
  - do not commit;
  - end with a list of: files changed, what was rewritten, the contracts relied on (routes, RPC
    methods, selectors), and anything uncertain or not migrated, each with a reason.

While subagents are editing, don't run git commands that touch the working tree (stash, checkout,
reset).

When they return:
1. Resolve cross-area items. Examples: a class that an interaction selects on, a route type that JS
   calls, a field that JS reads.
2. Re-run `scan.py`. Target: **0 BLOCKER, 0 SILENT**. Every remaining RUNTIME or WARN is either
   fixed or justified in the report.
3. Commit per area.

### 5. Install loop

```bash
$S/install_test.sh $MIG20_TARGET_ROOT/<project> <module>
```

- Fix each reported problem **at its root**. For a missing field or xmlid, find the 20 name; for an
  xpath or RNG error, read the 20 parent arch or the schema in `odoo/addons/base/rng/`.
- Re-run until `RESULT: CLEAN`, then also clear the module's own WARNINGs.
- Stop after about 8 rounds without progress, and report what blocks.
- If the module has `tests/`: run `install_test.sh … --tests` and fix the failures. QUnit tests
  can't run in 20: list them as "to rewrite in Hoot".
- Re-run a single failing test fast with `--tags /<module>:<Class>.<test_method>`.
- A failed browser test prints the failing tour step and the paths of the PNG screenshots taken at
  that moment. **Open the screenshots** before guessing: they usually show the cause (an error
  dialog, the wrong page, an element under a modal).
- For every new kind of break you had to fix by hand, add a `scan.py` rule or check and a line in
  `lessons-learned.md`.

### 6. Smoke test in a browser

```bash
eval "$(python3 $S/smoke_test.py <module> --routes '/extra,/routes' --out <tmpdir>)"
$S/install_test.sh $MIG20_TARGET_ROOT/<project> <module>,$SMOKE_MODULE --tests --extra-addons $SMOKE_ADDONS
```

This runs Odoo's clickbot over the module's apps, opens every other module menu action (and its
"new" form), and every website menu or page URL as public and admin. Any browser console error
fails the run.

- Check the log for `Open "…" in browser`. Odoo **skips** browser tests without Chrome or
  `websocket-client`, and `install_test.sh` reports that as a problem.
- Pages that need a record (detail pages) aren't reached automatically. Pass them with `--routes`
  when demo data exists, or list them for the user to check by hand.
- **Control run.** When a failure looks unrelated to the module's own code (the clickbot timing out
  on a core flow, a rebased fork), run the same smoke test on the upstream or core module alone:
  `smoke_test.py <upstream_module>`, then `install_test.sh <empty dir> <upstream_module>,$SMOKE_MODULE --tests --extra-addons …`.
  A failure that reproduces there is not a migration defect; record it in the report as such.
- **Flow tour.** The clickbot proves pages load, not that the migrated code works. When the module
  has backend JS, frontend JS or a website flow, write one short tour of its main flow. Examples:
  create and save the main record; submit the website form; add to cart.
  - Follow "Flow tour for the smoke test" in `tests-and-tours.md`, and take every selector from the
    migrated templates.
  - Pass it with `--tour-js <file> --tour '<name>@<start url>'` (append `:public` for website
    visitors). Odoo 20 starts test tours on that URL, not on the tour's registered `url`.
  - It stays in the throwaway smoke module. Offer it to the user as a permanent test in the
    module's `static/tests/tours/`.
- Flows a tour can't reach (external services, cron, mail gateways): exercise them with
  `odoo-bin shell` on a `--keep` database, then drop that database.

### 7. Review

Review `git -C $MIG20_TARGET_ROOT/<project> diff <BASELINE>..HEAD -- <module>`:
- with Odoo's `odoo-review` skill (installed, or read from `$ODOO20_SERVER/skills/odoo-review/SKILL.md`);
- otherwise with its checklist: correctness, security (`sudo`, public routes, ACLs), and matching
  core style.

Fix blocking findings, then re-run step 5.

### 8. Report and verify

1. Write `$MIG20_TARGET_ROOT/<project>/MIGRATION_20.md`:
   - source path and version, baseline commit, commit list;
   - scan summary before and after;
   - what `upgrade_code` changed, and what was done by hand, per area;
   - decisions: ACL/public access, icon mapping, removed dependencies, installed libraries;
   - **Not migrated / follow-ups**, each with a reason;
   - **Manual checks** for the user;
   - **Data migration notes**: renamed stored fields of the module's own models need a
     `migrations/20.0.x.y.z/pre-migrate.py` for existing databases (code migration only covers
     code).
2. Prove the source is untouched: `diff <(bash -c "source $S/env.sh; mig20_sha1_tree <source>") $MIG20_TARGET_ROOT/<project>/.migration/<module>.source.sha1`.
3. Prove core is untouched: `git -C $ODOO20_SERVER status --porcelain` is empty (when it's a git
   checkout).
4. Prove no test databases are left: `psql <conn> -l | grep mig20_` is empty.
5. Tell the user how to try it:
   - add `$MIG20_TARGET_ROOT/<project>` to their Odoo 20 `addons_path`;
   - pip install any new external dependencies;
   - which pages or menus to click.
