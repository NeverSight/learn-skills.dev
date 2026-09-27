---
name: ac-django
description: Django bible for Django 6.1 with a trailing Django 5.2 LTS section and optional DRF. Fat Models doctrine with migrations, transactions, security, testing, and tooling. Use when writing Django models, views, forms, serializers, migrations, tests, or reviewing Django code. Do NOT use for project-specific Django patterns (load the project overlay skill instead).
compatibility: python3. Knowledge-only skill with no external tool requirements beyond a Django codebase.
requires:
  - ac-python
metadata:
  version: 0.1.0
  subagent_safe: true
---

# Django Bible (Django 6 · optional DRF)

**Targets:** Django **6.1** on Python **3.14** · **Previous line:** Django **5.2 LTS** (trailing section) · **API:** DRF _when you choose it_

## Version Policy

This skill documents **one** Django line: the current one. Keep it that way when
you update it.

- **Main path = the current feature release.** Today that is Django **6.1**. When
  a newer feature release lands, the main path moves to it in the same edit.
- **Unmarked prose means the first release of the current line** — Django **6.0**.
  Anything the line gained _after_ that carries a `(6.1+)` marker placed right
  after the API or feature it qualifies: `` `QuerySet.fetch_mode()` (6.1+) ``. One
  form only. Do not write "Django X.Y+ adds", "new in X.Y", "as of X.Y", or a
  `### Django X.Y note` heading — the marker is the whole convention, and it is
  only useful if it is the only one.
- **Older lines get one trailing section each, at the end of `SKILL.md`**, and
  nothing anywhere else — the reference files carry the current line only and get
  no trailing section of their own. Today that is
  `## Previous line: Django 5.2 LTS`. It carries the diff a reader on that
  version needs: what is missing, what to use instead, and what to change on
  upgrade. A version note interrupting the main path is a defect — move it down.
- **Research order when refreshing.** Release notes and official docs first
  (`docs.djangoproject.com/en/<version>/releases/<version>/` and the topic
  pages they link). Then the authors already cited under Canonical Sources. Blogs
  and newsletters last, briefly, for what the docs do not cover.
- **Rotation.** When Django releases the next line, the current trailing section
  is replaced by the line being retired, unmarked prose is re-based on the new
  line's first release, and markers below that release are dropped. Django 6.2 is
  the last release under the `A.B` scheme; feature releases after it use a
  calendar `YYYY` format, one every January. "Current line" then means the newest
  `YYYY` release, and the same rules apply unchanged.

## Canonical Sources

- Django docs index: <https://docs.djangoproject.com/en/6.1/>
- Django 6.1 release notes: <https://docs.djangoproject.com/en/6.1/releases/6.1/>
- Django 6.0 release notes — what unmarked content in this skill assumes: <https://docs.djangoproject.com/en/6.0/releases/6.0/>
- Django docs — fetch modes: <https://docs.djangoproject.com/en/6.1/topics/db/fetch-modes/>
- Django docs — migrating email to mailers: <https://docs.djangoproject.com/en/6.1/topics/email/#migrating-email-to-mailers>
- Adam Johnson — `django-upgrade`: <https://adamj.eu/tech/2021/09/16/introducing-django-upgrade/>
- Adam Johnson — `django-linear-migrations`: <https://adamj.eu/tech/2020/12/10/introducing-django-linear-migrations/>
- Adam Johnson — Test for pending migrations: <https://adamj.eu/tech/2024/06/23/django-test-pending-migrations/>
- Adam Johnson — Model field choices that can change without a migration: <https://adamj.eu/tech/2025/05/03/django-choices-change-without-migration/>
- Haki Benita — "How to Get Foreign Keys Horribly Wrong": <https://hakibenita.com/django-foreign-keys>
- Haki Benita — Reliable Django Signals (django-tasks-db production pattern): <https://hakibenita.com/django-reliable-signals>
- James Bennett — Fat Model / "no service layer" (default) + followup on breaking up god-methods: <https://www.b-list.org/weblog/2020/mar/16/no-service/> · <https://www.b-list.org/weblog/2020/mar/23/still-no-service/>
- James Bennett — "Litestar is worth a look" (reaffirms no-service-layer specifically for Django, while allowing it for less-opinionated frameworks): <https://www.b-list.org/weblog/2025/aug/06/litestar/>
- DabApps — model encapsulation (never write a field / `save()` from outside): <https://www.dabapps.com/insights/django-models-and-encapsulation/>
- HackSoft Django Styleguide — the service-layer / `selectors.py` camp (one option, not this skill's default): <https://github.com/HackSoftware/Django-Styleguide>
- DRF docs: <https://www.django-rest-framework.org/>
- Factory Boy best practices: <https://github.com/camilamaia/factory-boy-best-practices>

## Reference Files (load as needed)

| File | Covers | When to load |
| --- | --- | --- |
| [`references/models-and-schema.md`](references/models-and-schema.md) | Models, fields, constraints, QuerySets, managers, ORM performance | Model changes, query optimization, schema design |
| [`references/transactions-and-migrations.md`](references/transactions-and-migrations.md) | Transactions, locking, idempotency, migration safety, FK index ops | Multi-step writes, migrations, schema changes |
| [`references/views-and-templates.md`](references/views-and-templates.md) | Views, forms, templates, partials, HTMX, file uploads, i18n, middleware, management commands, connection pooling, reference snippets | View/template work, form handling, HTMX, uploads |
| [`references/background-and-infra.md`](references/background-and-infra.md) | Background tasks, security, settings, observability, caching, async | Tasks, deployment, logging, caching, async views |
| [`references/admin-and-drf.md`](references/admin-and-drf.md) | Django Admin, DRF serializers, viewsets, permissions, pagination, versioning | Admin customization, API endpoints |
| [`references/testing-and-tooling.md`](references/testing-and-tooling.md) | Testing bible, Factory Boy, tooling, DX enforcement | Writing tests, CI setup, linting |
| [`references/antipatterns.md`](references/antipatterns.md) | django-antipatterns.com tips, patterns | Code review, avoiding common mistakes |
| [`references/troubleshooting.md`](references/troubleshooting.md) | Common Django errors and fixes | Diagnosing migration, N+1, on_commit issues |

## Dependencies

Requires `ac-python` (declared via the `requires:` frontmatter field). This skill layers Django-specific rules on top of ac-python's generic Python guidelines — see "Overrides When Loaded Alongside ac-python" below.

When used alongside lifecycle skills, provides Django best practices context for Django projects using the worktree workflow.

## Overrides When Loaded Alongside ac-python

When both ac-django and ac-python are loaded, the following Django-specific rules take precedence over the generic Python guidelines:

| Topic | ac-python (generic) | ac-django (wins) |
| --- | --- | --- |
| Test base class | Plain pytest classes (`class TestFoo:`) | `django.test.TestCase` (or `TransactionTestCase` when needed) |
| Parametrization | `pytest.mark.parametrize` | `unittest_parametrize` |
| Test data factories | `build_...()` plain functions | Factory Boy with `DjangoModelFactory`, traits, `build()` / `create()` |
| Shared setup | pytest fixtures | `setUpTestData()` (class-level, faster for DB-backed tests) |
| Time mocking | any (`freezegun`, `time_machine`, etc.) | `time_machine` (house default) |

All other ac-python guidelines (style, typing, OOP, imports, ruff config) apply unchanged in Django projects.

## Trigger QA (Release Gate)

Before shipping skill changes, validate activation behavior with sample prompts:

- Should trigger:
  - "Add a Django model field and migration."
  - "Review this DRF serializer and queryset for performance issues."
  - "Fix this Django transaction/on_commit bug."
- Should NOT trigger:
  - "Set up git worktrees for a ticket."
  - "Implement project delivery workflow and create an MR."
  - "Create a Notion research summary."

If behavior under-triggers or over-triggers, tighten `description` cues before release.

## Example: Adding a new model field

User says: "Add a postal_code field to the Address model"

1. Load [`references/models-and-schema.md`](references/models-and-schema.md) for field types and constraints
2. Load [`references/transactions-and-migrations.md`](references/transactions-and-migrations.md) for migration safety
3. Add field to model with appropriate validators, constraints, and `db_index` if queried
4. Create migration, verify with `makemigrations --check`
5. Add factory trait for the new field in tests

## Prime Directives

### Django docs first (always)

- Use Django the way Django documents it.
- Prefer built-ins over dependencies unless Django has a clear documented gap.

### Fat Model is the default (not the only answer)

Fat models win for small and medium models — the default, not a dogma.

- Default home for business rules and invariants:
  - model instance methods (single-object behavior — Django's "row-level" home)
  - QuerySet/Manager methods (collection behavior — Django's "table-level" home)
- This matches the Django docs and James Bennett's "no service layer" position: the models, with their managers/querysets, _are_ the API other code talks to.
- No `services.py` for domain logic **by default**.

Fat models stop being good once a model turns into a **god object**. A fat model is a model with rich, cohesive behavior over _its own_ data; a god object is one model that has accreted unrelated concerns and orchestration until no one can read it end to end. See "When a fat model becomes a god object" below for the signals and the escalation ladder — the escapes are _not_ a reflex service layer.

### Locality of behavior (anti-octopus)

- Co-locate behavior with:
  - the data (models/querysets)
  - the UI (partials inside the template that uses them)

### Coordination vs business logic

Allowed at boundaries (views/forms/serializers):

- sequencing calls
- selecting aggregate root objects
- transaction bracketing when spanning multiple domain calls

Not allowed at boundaries:

- invariants
- workflow rules
- state transitions that define correctness

## Deprecation Watch (flagged in 6.1, removal in the next major)

Avoid writing new code against these:

- Flat `EMAIL_*` settings (`EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, etc.) are deprecated in favor of a `MAILERS` dict setting (mirrors `DATABASES`/`CACHES`); new code should not add to the flat settings.
- `mail.get_connection()`, and the `connection` / `fail_silently` / `auth_user` / `auth_password` arguments to the mail helpers — pass `using=` with a `MAILERS` alias instead.
- `QuerySet.select_related()` called with no arguments, and `ModelAdmin.list_select_related = True` — always pass explicit field names.
- `QuerySet.values_list(flat=True)` without an explicit field name.
- `Model.from_db()` implementations that do not accept the `fetch_mode` keyword argument.
- `None` as the right-hand side of an exact lookup on a `JSONField`, meaning the JSON scalar `null` — query with `JSONNull()` instead. Querying only: storing `None` still writes SQL `NULL` and is unaffected, as are key and index lookups.
- Double-dot template lookups (`{{ book..title }}`), which resolve to a lookup of the empty string.
- `django.db.transaction.savepoint()` — use `savepoint_create()`.
- The default HMAC algorithm for `salted_hmac()`/`base64_hmac()` flips from `sha1` to `sha256` — don't hardcode `sha1` expectations.

Django's 6.1 notes name Django 7.0 as the removal release. Django's release page
states that 6.2 is the last release under the `A.B` scheme and that feature
releases after it use a `YYYY` format. Upstream does not spell out how "7.0" maps
onto that scheme.

## Project Layout & Boundaries

### Domain-first apps

- Split apps by domain capability, not by technical layer.
- Each app should be readable end-to-end.

### Public vs internal vs admin

- Separate public API/HTML surfaces from internal/admin surfaces.
- Prefer separate modules over one giant `views.py`.

### "core/" discipline

- **Allowed:** request-id middleware, logging helpers, settings checks, small shared base mixins
- **Forbidden:** hiding domain behavior "because it's shared"

### Naming

- Use business language.
- Prefer verb methods: `approve()`, `reject()`, `settle()`, `cancel()`.

## Team Style Conventions (ask once, remember)

Some style choices are equally valid — the "right" answer depends on the team. When you encounter one of these for the first time in a project, **ask the user** for their team's preference and save it to the project's `MEMORY.md` (auto-memory) so it persists across sessions.

| Topic | Option A | Option B | What to ask |
| --- | --- | --- | --- |
| Attribute/relation checks | **LBYL:** `hasattr()`, `isinstance()`, `getattr(obj, attr, default)` | **EAFP:** `try/except AttributeError` | "Does your team prefer LBYL (hasattr/getattr) or EAFP (try/except) for optional attribute and reverse-relation checks?" |
| Queryset existence checks | `if qs.exists():` then `qs.first()` | `obj = qs.first(); if obj:` | "Single query (`first()` + None check) or explicit `exists()` + `first()`?" |
| Null handling in serializers | Explicit `allow_null=True` on every nullable field | Rely on model field `null=True` inference | "Explicit `allow_null` on serializer fields, or infer from model?" |

**Rules:**

- Only ask on the **first occurrence** in a project — never re-ask if already saved.
- If a project overlay skill already documents the preference, treat that as the answer — don't ask again.
- Save the answer as a `project` type memory with a descriptive title (e.g., "Django team convention: LBYL for attribute checks").

## Fat Model Doctrine (where logic lives)

### Placement table (strict)

| Concern | Home | Notes |
| --- | --- | --- |
| invariants, transitions, domain calculations | model methods | "tell, don't ask" |
| collection logic | QuerySet methods | chainable |
| graph loading | QuerySet methods | `for_api()`, `for_list()`, `with_*()` |
| request validation | forms / DRF serializers | boundary validation |
| authorization | views / DRF permissions | check early |
| rendering | templates / serializers | no DB access |

### Encapsulate mutation

Expose domain methods that: validate state → perform mutation → persist changes → schedule side effects safely (after commit).

Encapsulation rule that keeps fat models honest (DabApps): **never write to a model field or call `save()`/`create()`/bulk ops directly from outside the model** — go through a model method or manager method. View/template code may _read_ any field, but state changes always go through one of those methods. This is what makes "fat model" mean "the model owns its invariants", not "the model has lots of code".

### When a fat model becomes a god object

Fat models are good for small/medium models. The rule does not scale to a model that has swallowed unrelated concerns. Treat the following as **god-object signals** — when two or more fire on one model, stop adding to it and climb the escalation ladder below:

- **Size:** model class body over ~200 LOC, or more than ~15-20 public methods.
- **Mixed domains:** methods on one model touch concerns that aren't that model's own data (e.g. `Order` with billing-provider calls _and_ shipping-label generation _and_ loyalty-points math).
- **Orchestration in `save()`:** `save()` (or a single method) drives a multi-step workflow across several other models / sends notifications / calls external APIs — the "cancelling a billing agreement updates a half-dozen other things in one method" smell.
- **Method count by responsibility:** clusters of methods that obviously belong to different responsibilities (a `User` that is also auth, also profile, also billing, also feature-flagging).
- **Tests scream:** unit-testing one method forces you to set up half the schema, or a single test module for one model grows unmanageable.

A long model that is still entirely about _its own_ data and reads cleanly is **not** a god object — don't refactor for LOC alone. The trigger is mixed concerns / orchestration, not size by itself.

### Escalation ladder (climb only as far as a signal forces you)

Each rung has a **WHEN**. Take the lowest rung that fixes the signal — do not skip to a service layer.

- **(a) QuerySet / Manager methods.** _WHEN:_ the logic is collection- or table-level (filtering, aggregation, bulk state changes, alternate constructors like `Account.objects.create_trial()`). This is the first place table-level logic goes — Django's own guidance. Most "the model is getting fat" pressure is really table-level logic that belongs here, not on the instance.

- **(b) Cohesive model mixins or a bounded-context model split.** _WHEN:_ the signals are _mixed domains_ / _method-count-by-responsibility_ on a single model — the model is doing several cohesive jobs.
  - First reach: extract each cohesive cluster into an **abstract model mixin** (`BillingMixin`, `AuditMixin`) so each concern is its own readable unit while the table stays one row. Mixins must be genuinely cohesive — a mixin that is just "the rest of the methods" is the god object with extra files.
  - Bigger reach: if the concerns are really _separate aggregates_, **split the model** (and often the app) along the bounded context — e.g. pull `Subscription`/`Invoice` out of a god `Account`. Splitting apps by domain capability is the real scaling move; see "Domain-first apps" above.

- **(c) Stateless processor functions (module-level), or a dedicated processor class.** _WHEN:_ the work **orchestrates several models** and has no natural single aggregate root to own it — the cross-aggregate / `save()`-doing-orchestration signals. This is the "broke the over-complex method up" answer (Bennett's followup), not a relocation of the mess.
  - Default form: **stateless module-level functions** in the app (e.g. `app/operations.py` / `app/processors.py`) that take the participating objects as arguments, do the sequencing inside one `transaction.atomic()`, and schedule side effects via `on_commit`. Functions over classes when there is no state to hold (Luke Plant).
  - Reach for a **dedicated processor/handler class** only when there genuinely is multi-step state to carry across the orchestration (a builder, a multi-phase import). Name it for the operation (`OrderCheckoutProcessor`), keep it stateless-by-default, and keep the invariants on the models it drives — the processor sequences, the models still own correctness.
  - This rung is _coordination_, not a domain service layer: it calls model/manager methods, it does not re-implement the business rules that live on them.

- **(d) Service layer — last resort, external-API orchestration only.** _WHEN:_ the orchestration is dominated by **talking to the outside world** (Stripe, AWS, a third-party API) and the sequencing/error-handling/retry of those calls is the actual complexity. Then a `services.py` _scoped to that external integration_ is fine.
  - Constraint: `services.py` holds **no DB business logic / no invariants** — those still live on the models. The service orchestrates external calls and hands results to model/manager methods.
  - This is deliberately the top of the ladder: a general "all business logic goes in `services.py`" layer (the HackSoft / enterprise pattern) is a real, defensible style, but it is **not** this skill's default — it trades the model-as-API for a parallel layer, and for most apps the rungs above cover the need. Adopt a project-wide service layer only as an explicit, documented team decision, not as a default reflex when one model got fat.

**Companion reads (`selectors.py`).** Independently of the write-side ladder, complex cross-model **read** operations (reporting/dashboards) that don't belong on any one QuerySet can live in `selectors.py` returning typed DTOs. Selectors are read-only; they never mutate.

### Sources for this doctrine

- Django docs — Managers: row-level → Model methods, table-level → Manager/QuerySet methods: <https://docs.djangoproject.com/en/6.1/topics/db/managers/#adding-extra-manager-methods>
- James Bennett — "Against service layers in Django" + followup ("More on service layers"): <https://www.b-list.org/weblog/2020/mar/16/no-service/> · <https://www.b-list.org/weblog/2020/mar/23/still-no-service/>
- James Bennett — "Litestar is worth a look" (reaffirms the no-service-layer position specifically for Django): <https://www.b-list.org/weblog/2025/aug/06/litestar/>
- DabApps — "Django models, encapsulation and data integrity" (never write a field / `save()` from outside): <https://www.dabapps.com/insights/django-models-and-encapsulation/>
- Luke Plant — "Django Views — The Right Way" (functions over classes, anti-over-abstraction): <https://spookylukey.github.io/django-views-the-right-way/>
- HackSoft Django Styleguide — the service-layer / `selectors.py` camp (the rung-(d) style, presented as one option not the default): <https://github.com/HackSoftware/Django-Styleguide>
- Carlton Gibson / Vinta — "beyond the Fat Models vs. service-layer binary" (module-level functions as the middle ground): <https://www.vintasoftware.com/lessons-learned/djangoservicelayersbeyondfatmodelsvsenterprisepatterns>

## Review Checklists

### Domain rules / Fat Model

- [ ] business rules live on models/querysets (the default home)
- [ ] boundaries only orchestrate
- [ ] no field writes / `save()` / bulk ops from outside model + manager methods
- [ ] no god-object: a fat model touching mixed domains, or a `save()`/method driving multi-model orchestration, has climbed the escalation ladder (queryset → mixin/split → processor function/class → service for external APIs only) rather than just growing

### ORM performance

- [ ] no N+1
- [ ] queryset shaped for serializer/template needs
- [ ] constraints/indexes reviewed

### Transactions and side effects

- [ ] multi-step write flows wrapped in `atomic()`
- [ ] side effects scheduled via `on_commit`

### Migrations

- [ ] linear migrations enforced (one leaf per app — `django-linear-migrations` or manual review)
- [ ] `makemigrations --check` passes
- [ ] migration safe/reviewable
- [ ] comments-as-code (per ac-python): no signature-echo docstring, no inline comment restating the RunPython body — a data migration's intent is its function name, not a 6-line docstring

### Tasks

- [ ] idempotent
- [ ] enqueued after commit

### Security

- [ ] authz checked early
- [ ] CSRF preserved
- [ ] CSP configured correctly

### Architectural Health (Module-Level)

Apply to **full files** touched by the diff, not just changed lines:

- [ ] Fat Model is the default: business logic on models/querysets, not in views/commands/CLI
- [ ] views and management commands only orchestrate — no invariants, no workflow rules
- [ ] no god-module (single file mixing unrelated concerns) and no god-object (single model that has accreted unrelated concerns / multi-model orchestration)
- [ ] multi-model orchestration sits in a stateless processor function / class (or on an aggregate-root method), not crammed onto one model's `save()`
- [ ] no complexity rule suppressions (`C901`, `PLR09xx`) in `pyproject.toml` beyond the `python-boilerplate` baseline
- [ ] `services.py` (if present) is scoped to external API orchestration (Stripe, AWS) and holds no DB business logic — a project-wide service layer is a documented team decision, not the default

### Testing

- [ ] traits used for nullable/optional data
- [ ] tests explicit about preconditions

## Enforcement via prek

The testing conventions above that are deterministically checkable ship as prek
hooks in this repo (`.pre-commit-hooks.yaml` + `ac-django/rules/`). The AST-shaped
checks are [ast-grep](https://ast-grep.github.io) YAML rules; the
`pyproject.toml` surface (which ast-grep cannot parse — no TOML language) is a
tiny standalone Python hook. A consuming repo references them by URL and rev:

```yaml
- repo: https://github.com/souliane/skills
  rev: <commit-sha>
  hooks:
    - id: ac-django-no-pytest-django-db
    - id: ac-django-testcase-no-pytest-parametrize
    - id: ac-django-no-complexity-suppressions
    - id: ac-django-no-pyproject-complexity
```

| Hook id | Engine | Fails on |
| --- | --- | --- |
| `ac-django-no-pytest-django-db` | ast-grep | any `pytest.mark.django_db` use — the `@pytest.mark.django_db` decorator **and** a module-level `pytestmark = pytest.mark.django_db` (or list). Use `django.test.TestCase`. |
| `ac-django-testcase-no-pytest-parametrize` | ast-grep | `@pytest.mark.parametrize` on a method **inside a `TestCase` subclass** (pytest silently ignores it there) — use `unittest_parametrize`. Module-level pytest-style functions are not flagged. |
| `ac-django-no-complexity-suppressions` | ast-grep | a `# noqa: C901`/`PLR09xx` comment in source/tests |
| `ac-django-no-pyproject-complexity` | standalone | a `C901`/`PLR09xx` entry in a `pyproject.toml` ruff `lint.ignore` / `lint.extend-ignore` / `lint.per-file-ignores` list |

**ast-grep is pinned to `0.44.1`.** The wrapper (`ac-django/rules/astgrep_scan.py`)
resolves it hermetically via `uvx --from ast-grep-cli==0.44.1 ast-grep` when `uv`
is on PATH (no system install needed), falling back to a system `ast-grep`.

**They fail-closed, grandfathered INLINE.** With nothing grandfathered every
violation fails (a fresh consumer gets full enforcement immediately). There is
**no baseline file and no count cap** — existing violations are grandfathered in
place:

- **ast-grep rules** — add ast-grep's native opt-out comment on the line above
  the violation: `# ast-grep-ignore[<rule-id>]` (e.g.
  `# ast-grep-ignore[ac-django-no-pytest-django-db]`). It silences only that one
  rule on that one node; every new (un-ignored) occurrence still fails.
- **`ac-django-no-pyproject-complexity`** — list each existing entry inline in
  the consuming repo's hook `args` as `--grandfather <code>@<location>` (e.g.
  `--grandfather C901@lint.per-file-ignores.scripts/**/*.py`). Any new entry not
  on the list fails; the list only shrinks as the code improves.

This keeps the ratchet's "tighten-only" property without a data file: the
grandfather record lives where the violation lives (an inline comment, or the
consumer's own `.pre-commit-config.yaml`), so it can never drift out of sync with
the tree.

**Review-only conventions (deliberately not hard-gated).** Factory Boy usage
and `setUpTestData()` for shared setup are house conventions, but a hook on them
is too noisy — there are many legitimate non-factory `create()` calls and
per-test `setUp()` needs. These stay review checklist items, not blocking hooks.

## Previous line: Django 5.2 LTS

Django 5.2 is the LTS, in extended support until April 2028, so it is still what
a lot of production code runs. Everything above targets Django 6. This section is
the diff.

### What Django 6 has that 5.2 does not

| Capability | Django 6 | On 5.2 instead |
| --- | --- | --- |
| Template partials | Native `{% partialdef %}` / `{% partial %}` | `django-template-partials` |
| Background tasks | Native `django.tasks` (`@task`, `.enqueue()`) | Celery / Huey / RQ |
| CSP | Native CSP middleware + `SECURE_CSP` | `django-csp` |
| Fetch modes (6.1+) | `QuerySet.fetch_mode()` | Explicit `select_related()` / `prefetch_related()` |
| DB-level `on_delete` (6.1+) | `DB_CASCADE` / `DB_SET_NULL` / `DB_SET_DEFAULT` | Python-level `on_delete` only |
| Multiple mailers (6.1+) | `MAILERS` | Flat `EMAIL_*` settings |

### Upgrading

- Run `django-upgrade` before any manual refactor.
- Leave explicit upgrade TODOs where a shim is in use:
  - `# TODO(Django6): switch @shared_task -> @task and .delay() -> .enqueue()`
  - `# TODO(Django6): remove {% load partials %} (partials become native)`
  - `# TODO(Django6): replace django-csp with built-in CSP middleware`
- Django 5.2 is the last line supporting Python 3.10 and 3.11; Django 6.x needs
  Python 3.12+.
