---
name: odoo-workflow
description: >
  Mandatory pre-code gate and definition-of-done for ANY Odoo change (add field, override method,
  inherit view/xpath, OWL/JS patch, wizard, cron, controller, report, security, migration, bug fix,
  refactor, "optimize", "clean code", "stick to base"), Odoo 16-19. Also when the user pastes an
  Odoo traceback or install/upgrade error (ParseError "cannot be located in parent view", "Field
  ... does not exist", missing xmlid) or asks where an Odoo model, field, method, view or xmlid is
  defined. Run BEFORE brainstorming or planning: Odoo design questions are answered by tracing the
  real source into a Context Brief (file:line), not by open-ended Q&A or memory. Resolves the Odoo
  runtime and version, loads the matching odoo-<major> pack, and closes with install, test,
  upgrade, i18n, security and hygiene checks before commit.
---

# Odoo Workflow - trace first, then code

Procedure for every Odoo change. The expensive failures are always the same: a field or
method that does not exist, an xpath anchor that was never there, an override hooked on the
wrong method, a stored field renamed without a migration, a `sudo()` nobody can audit, a test
run that ran no tests. The fix is mechanical: **no citation, no code**.

## When this applies

- **Full path** - anything that ends in Odoo Python, XML, JS or data: new field, override,
  inherited view, OWL patch, wizard, cron, controller, report, security, migration, bug fix,
  refactor, "optimize", "clean up". A pasted traceback starts here: its innermost frame in a
  workspace module is the first citation.
- **Brief only** - questions about Odoo symbols ("where is X defined", "does `sale.order` have
  F", "which model gets this field on 19"): run Steps 0-2 and answer with the Brief, no code.
- **Fast path** - the change names no symbol outside the module being edited and adds no field,
  override, xmlid, xpath, group or `depends`: a label, help text or typo in the module's own
  code, a manifest version bump, a test-only change. The Brief is one row citing the edited
  line; skip Steps 1, 3 and 6; Step 5 still applies (i18n when a string changed). Any doubt:
  full path.
- Skip for documentation-only and git-only tasks (use `odoo-commit`).
- Brainstorming and planning skills come *after* Step 2, and only if the business intent is still
  unclear - the Context Brief is their input.

## Step 0 - Runtime, version, pack

The bundled helper `scripts/odoo_trace.py` (stdlib Python 3.8+, read-only) resolves the runtime
and answers the Python-side trace questions. Call it with the skill's base directory written out
in full every time - shell variables do not survive between tool calls. Below, `odoo_trace`
stands for `python3 <skill_dir>/scripts/odoo_trace.py`.

```bash
odoo_trace env
```

First hit wins: flags, `.claude/odoo.json`, an `odoo-bin` configuration in `.claude/launch.json`
whose addons cover the cwd (both files in the cwd or nearest parent), then the one `*.conf` whose
`addons_path` covers the cwd, searched from the parent directory upwards (each level and its
subdirectories). It prints `version` (from `odoo/release.py`), `odoo_root`, `conf`, `python`,
`dev_db`, and the addons roots in the order Odoo uses them (the first root holding a module name
wins). An `odoo_version` in `.claude/odoo.json` or a `.odoo-version` file must match `release.py`.

- Exit 2 prints `SETUP ERROR:` and the cause. Runtime not located: ask once for the core
  checkout and conf, pass them as `odoo_trace --odoo-root <core> --conf <conf> <command>` on
  every call (`roots` included), and offer to write a gitignored `.claude/odoo.json` with
  `odoo_version`, `odoo_root`, `conf`, `python`, `dev_db` (machine-local paths). Version sources
  that disagree, or several confs covering the cwd: ask which one is right. Never trace against
  custom roots alone.
- An explicit statement from the user or the project `CLAUDE.md` / `AGENTS.md` outranks the
  helper. If they disagree, stop and ask. Do not silently assume a version.
- Load the Odoo reference pack for that major: `odoo-<major>` with the skills CLI,
  `<plugin>:odoo-<major>-0` in the Claude Code plugin (for example `agent-skills:odoo-18-0`).
  Read its `references/api-highlights.md` (APIs removed or renamed in this version) and only the
  guide section the task needs (`grep -n '^## ' <guide>`, then a range). Pack missing: say so and
  continue - the real source is the authority, never memory.

## Step 1 - Trace the chain

**Python symbols: the helper.** It parses classes with `ast`, applies the version's `_name`
rules, follows `_inherit` parents (mixins such as `mail.thread`, `portal.mixin`), `_inherits`
delegation, `base` extensions and the core `BaseModel`, marks classes in files the module never
imports (`UNIMPORTED`), and prints absolute `file:line`.

| Question | Command |
|----------|---------|
| Classes defining / extending MODEL, its mixins, type, `_auto`, `_log_access` | `odoo_trace model MODEL` |
| Does FIELD exist on MODEL (own, parent, `_inherits`, magic), every definition, comodel; a dotted path is checked hop by hop | `odoo_trace field MODEL FIELD[.FIELD...]` |
| Every definition of METHOD in `super()` order (#1 runs first), `super()` calls, hooks, AMBIGUOUS pairs | `odoo_trace method MODEL METHOD --module MODULE` |
| Transitive `depends` of MODULE in load order | `odoo_trace depends MODULE` |
| Does an xmlid exist (loaded XML record or CSV row, or generated at install) | `odoo_trace xmlid module.name` |
| Files of MODULE that never load (not in `data`/`assets`, not imported) | `odoo_trace unlisted MODULE` |

The last line is the `VERDICT`. Exit 0 = found, 1 = NOT FOUND (the verdict names the closest
real symbols), 2 = setup error or answer unknown. Only exit 1 supports a NOT FOUND cell. Lists
on hub models (`sale.order`, `mail.thread`) are capped; `--all` after `model`, `method` or
`unlisted` prints them whole.

**XML, JS, controllers, uses: grep over the same roots.** `ROOTS` below means
`$(odoo_trace roots)` written out in full: command substitution splits into one argument per root
in zsh and bash, a plain `$ROOTS` string does not split in zsh. Keep the quotes around
`--include` globs. A grep that warns `No such file or directory` or exits 2 is a broken command,
never a NOT FOUND. So is a grep run while `odoo_trace env` exits 2 (an empty `$(odoo_trace
roots)` leaves `grep -r` searching only the cwd), and one over a root whose path holds a space:
it splits, and macOS grep skips the pieces silently, so grep that root separately, quoted.

```bash
# V1. Views on MODEL
grep -rlE --include='*.xml' "<field name=\"model\">MODEL</field>" ROOTS
# V2. Every view and QWeb template inheriting VIEW; -A1 also catches inherit_id split over two lines
grep -rnE -A1 --include='*.xml' "name=['\"]inherit_id['\"]|inherit_id=['\"]" ROOTS | grep -E ":[0-9]+:.*(ref|inherit_id)=['\"](MODULE\.)?VIEW['\"]|-[0-9]+-\s*ref=['\"](MODULE\.)?VIEW['\"]"
# V3. ANCHOR nodes inside one view record, absolute lines. A = the id line, B = the next </record>: grep -nE 'id="VIEW"|</record>' VIEW_FILE
awk -v a=A -v b=B 'NR>=a && NR<=b && /name="ANCHOR"/ {print FILENAME":"NR": "$0}' VIEW_FILE
# W1. OWL / QWeb client template: definition and every t-inherit (extension or primary)
grep -rnE --include='*.xml' "t-name=['\"]TEMPLATE['\"]|t-inherit=['\"]TEMPLATE['\"]" ROOTS
# W2. JS class or component: its definition (= import path) and every patch of it
grep -rnE --include='*.js' "^export (default )?(class|function|const) NAME[^A-Za-z0-9_]|patch\(\s*NAME[^A-Za-z0-9_]" ROOTS
# C1. Route (the second pattern finds a decorator split over lines), then every subclass of
#     its controller class (an `import CLASS as ALIAS` hit: run the class grep again with ALIAS)
grep -rnE --include='*.py' "@(http\.)?route\(.*['\"]URL['\"]|^\s*(route=)?\[?\s*['\"]URL['\"]" ROOTS
grep -rnE --include='*.py' "^class \w+\(([^)]*[ ,])?([A-Za-z_.]+\.)?CLASS[,)]|import.*[ ,]CLASS as " ROOTS
# S1. ACL rows and record rules on MODEL (dots as underscores)
grep -rn --include='ir.model.access.csv' "model_MODEL_UNDERSCORED," ROOTS
grep -rlE --include='*.xml' "model_MODEL_UNDERSCORED['\"]" ROOTS | grep security
# U1. Every use of NAME before renaming, removing, or changing the signature of a field or method
grep -rnwE --include='*.py' --include='*.xml' --include='*.js' --include='*.csv' --include='*.scss' "NAME" ROOTS
# T1. Tests to mirror
ls BASE_MODULE/tests/; grep -rnE "def test_.*METHOD" MODULE/tests
```

For U1 keep the hits on MODEL and list each one: views, QWeb, `@api.depends`, `related=`,
domains, record rules, cron and server-action `code`, `<function>`, button `name=`, JS
`orm.call` strings, tests, migrations. On a generic name (`name`, `state`, `partner_id`) restrict
the list to the modules `odoo_trace model MODEL` printed plus the views from V1/V2; if it is
still over 50 hits, show the count per module and ask before going on.

A grep hit counts only if its file loads (`odoo_trace unlisted MODULE` lists the files that
never do) and, in Python, sits in MODEL's own class, not another class of the same file.

Reading budget - this is where tokens go:

- Read ranges, not files: Read with offset/limit, or `awk 'NR>=A && NR<=B'` - never
  `sed -n 'A,Bp' | grep -n`, whose line numbers restart at 1 and cannot be cited. At most 120
  lines per hop.
- At most 3 hops inline. Deeper or cross-module flows go to the `odoo-code-tracer` agent with
  `odoo_version`, `pack_dir` (the loaded pack's directory), `roots` and `helper` (the helper's
  full path, plus any flags `env` needed), **if it is installed**; otherwise keep going with the
  commands above.
- Never re-read a file already cited in the Brief.

## Step 2 - Context Brief (no citation, no code)

Write the brief before any code, one row per symbol the change touches (Odoo 18 example):

| Layer | Symbol | Source (file:line) | Base behaviour | Change |
|-------|--------|--------------------|----------------|--------|
| model | `purchase.order` | `addons/purchase/models/purchase_order.py:19` | `_name`, inherits `mail.thread` | inherit |
| method+super | `button_approve` | `purchase_order.py:528`; override `purchase_stock/models/purchase_order.py:117` calls `_create_picking` | pickings exist only with `purchase_stock` | depends `purchase_stock`, call super, then X |
| path | `stock.picking` `partner_id.commercial_partner_id.vat` | `stock/models/stock_picking.py:630` -> `base/models/res_partner.py:304` -> `:247` | Many2one, Many2one, Char | related field |
| view+xpath | `purchase.purchase_order_form` | `purchase/views/purchase_views.xml:130`, anchor `partner_ref` `:185`, one node in the form | - | add field after anchor |

Layers: model / field / method+super / path / view+xpath / client / controller / security /
company / data / migration / i18n / test.

The **Source** cell holds exactly one of:

- `file:line` - the cited line itself shows the claim (definition, record, anchor node).
- `NOT FOUND` - the helper exited 1, or a clean grep over all ROOTS matched nothing on MODEL.
  Name the closest real symbol when one exists.
- `UNCERTAIN: <what is missing>` - name the file not read, the runtime-built domain, or the
  other module's view that provides the anchor. Never for a question a command above answers.
- `AMBIGUOUS: <modules>` - overrides in modules that do not depend on each other.

Any cell other than `file:line` means no code for that row: drop it, add the missing `depends`,
or ask. More than 15 rows means the task should be split; never drop a row to fit.

Rules:

- **Redefined field.** `odoo_trace field` lists every definition in load order; cite each one
  whose attributes the change relies on. Attributes not repeated keep their earlier value
  (`selection_add` extends the list), unless the newer class does not subclass the earlier one:
  then the earlier attributes are dropped and the helper prints `final class`.
- **Path** (`related=`, `@api.depends`, `depends=`, `domain=`, `domain_force`). One `field` call
  on the dotted path, one citation per hop. A missing hop, or a non-relational hop before the
  end, is NOT FOUND at that hop.
- **Depends.** A symbol defined only in a module outside `odoo_trace depends MODULE` is not
  guaranteed to be installed, even if it exists in the current database. Add the dependency or
  drop the row.
- **Override order.** Take it from `odoo_trace method ... --module MODULE`, never from memory or
  grep order: the class loaded last runs first and its `super()` reaches the earlier ones.
  Declare `depends` on every module whose override the change relies on. Pairs it marks
  AMBIGUOUS stay AMBIGUOUS.
- **Xmlids.** `odoo_trace xmlid` decides: a record in an XML or CSV file the manifest loads, or
  GENERATED at install (`model_*`, `field_*__*`, `selection__*`, `base.module_*`,
  `account.<company id>_<name>` from a chart template), each tied to the module the helper
  names. A record only in a file the manifest never loads is NOT FOUND (UNKNOWN when an init
  hook may load it). Never invent an xmlid and never report a generated one as missing. A
  missing group in a view's `groups=` does not stop the install: Odoo only logs a WARNING, and
  the node is hidden because no user belongs to a group that does not exist.
- **Magic fields.** Never assume them; `odoo_trace field` decides. `create_uid`,
  `create_date`, `write_uid`, `write_date` exist only when `_log_access` is true; it defaults to
  `_auto`, so report and SQL-view models (`_auto = False`) do not have them.
- **Xpath anchor.** The anchor must be in the base view or in an inheriting view of a module in
  `depends`; otherwise UNCERTAIN. A locator matches the first node, so state how many nodes
  carry that name in the combined views (V2 + V3).
- **Company.** If MODEL or a comodel has `company_id`, cite it and whether the model sets
  `_check_company_auto`. New relational fields to company-bound comodels get
  `check_company=True`. A new model with `company_id` gets a record rule as core writes it:
  `[('company_id', 'in', company_ids)]`, or `[('company_id', 'in', company_ids + [False])]` when
  the company is optional.
- **Schema change.** Renaming, removing or retyping a stored field, changing or removing
  selection keys, adding `required`, adding a stored compute to a populated table, or renaming
  a model needs a `migration` row: the new manifest version and the
  `migrations/<version>/pre-*.py` / `post-*.py` script (`def migrate(cr, version)`) that moves
  the data; the script runs only if its version is above the installed one and not above the
  manifest's. A stored field renamed without one loses its column and data on `-u`, silently.
  Skip only when the user confirms the module was never installed on a database that matters.
  Recipes are in the pack's migration guide.
- **sudo.** Every added `sudo()` or `with_user(SUPERUSER_ID)` gets a `security` row: which ACL
  or record rule it bypasses (S1) and the check made before it (`check_access` / `has_access`
  on 18+, an access token, or a group check). No row, no sudo.
- Reuse over invent: before adding a field, helper, or compute, look for an existing one.
- "Clean code" / "stick to base" means: follow the base implementation's pattern with the
  minimal delta, never rewriting what `super()` already does. "Optimize" about speed means:
  measure first (query count or timing on a named case), change, measure again.

## Step 3 - Minimal plan

At most 10 bullets: files to touch, files explicitly not touched, what is deferred. One module
unless the Brief proves the change belongs to two, and one commit and PR per git repository
touched. YAGNI: no config for a value that never changes, no helper used once, no abstraction
with one implementation.

## Step 4 - Implement

- Apply the pack's `Coding Conventions` and its `api-highlights.md` list for this version;
  existing stable-addon style wins over personal preference.
- Override the narrowest hook that runs when the change needs it (the hooks `odoo_trace method`
  prints), not the public method that wraps it. Call `super()` and add the smallest delta; never
  copy the base body.
- Extend with `_inherit = 'model'` (a string); a new model sets `_name` explicitly. A list
  `_inherit` without `_name` creates a new model named after the class: on 19 always (with a
  warning), on 18 once the list has two items.
- Every new XML or CSV file goes into the manifest `data` in load order (groups,
  `ir.model.access.csv`, views, menus); every new static file must match an entry of the right
  `assets` bundle. An unlisted file installs cleanly and does nothing.
- `sudo()` naming: bind any recordset obtained through `sudo()` to a name ending in `_sudo`
  (`partner_sudo = self.partner_id.sudo()`,
  `orders_sudo = self.env['sale.order'].sudo().search(domain)`). A one-shot call
  (`record.sudo().write(vals)`) needs no variable. Never return a `_sudo` recordset from a
  public method or keep it on `self`.
- No `ponytail:` or other "simplified for now" markers in Odoo code - either the code is right
  or the plan in Step 3 says what was deferred.
- New user-facing strings go through `_()` / `_t()` / `string=` / `help=` so they are extractable.

## Step 5 - Definition of done

Read `references/definition-of-done.md` before reporting done: it holds the exact commands per
version. In short:

- [ ] One throwaway database `scratch_<module>` for the whole checklist: install with the
      module's tests, a test summary counting N > 0 tests (no summary, or `of 0 tests`, is not
      a pass), no `ERROR`/`CRITICAL`, every `WARNING` about the module explained. Never `-i`/`-u`
      a named database (the conf `db_name`, staging, dev) unless the user asks.
- [ ] Upgrade tested on a copy of a database with the previous version whenever the Brief has a
      `migration` row.
- [ ] `odoo_trace unlisted <module>` reports that all files load.
- [ ] ACL rows for every new model; company rule where the Company rule applies; every `sudo()`
      has its `security` row.
- [ ] i18n regenerated whenever a string changed; shipped `.po` files keep their names.
- [ ] The project's own linter, if it has one, passes on the changed files.
- [ ] Hygiene checks pass in every git repository the change touched.
- [ ] Scratch database dropped with its filestore. Commit through `odoo-commit`
      (`[TAG] module: description`, no AI attribution), one commit and PR per repository.

## Step 6 - Hand off

Run the `odoo-code-review` agent with `odoo_version`, `pack_dir`, `roots` and `helper` if it is
installed. If not, walk the Security and Hygiene lists in `references/definition-of-done.md`
yourself before reporting done.
