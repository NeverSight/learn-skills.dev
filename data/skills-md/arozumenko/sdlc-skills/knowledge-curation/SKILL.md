---
name: knowledge-curation
description: Use when promoting a hard-won fact from per-role memory into the shared, committed `.agents/knowledge/` layer, auditing that layer for stale or unindexed notes, or retiring a fact that stopped being true. Also use at the end of a substantial session or mission to sweep memory for anything cross-role worth committing. Not for per-role notes or daily logs (that is the `memory` skill), and not for mission state (that belongs on the work board).
license: Apache-2.0
metadata:
  version: "1.0.0"
---

# Knowledge curation

Two layers, one rule each:

| Layer | Scope | Tracked |
|---|---|---|
| `.agents/memory/<role>/` | one role's working notes + daily log | **project's choice**, never reviewed — `git check-ignore` says whether it stays on this machine |
| `.agents/knowledge/` | distilled facts every role can use | **yes** — committed and reviewed |

This skill owns the **second** layer and the path between them. The `memory` skill owns the first.

**Why the second layer exists.** Per-role memory is unreviewed and role-scoped, so a fact one role paid
for is invisible to every other role — and, where memory is gitignored, to the same role on another machine. Teams routinely
rediscover, at great cost, something a teammate already diagnosed correctly weeks earlier. The
memory was not missing and not wrong; it was unreachable. Promotion is the fix.

## Admission tests — all four must hold

1. **Cross-role** — useful to two or more roles, or architecture-level.
2. **Verified** — confirmed against the running system; the note says how, with a date.
3. **Durable** — still true after the current mission ends.
4. **Costly to rediscover** — if it is obvious from reading the code, it belongs in the code.

Fail any one → leave it in `.agents/memory/<role>/`.

> **An unverified claim here is worse than silence.** It is committed, so it is trusted. If you
> cannot state how you verified it, either verify it now or do not write it.

Keep the bar high. A thin layer that is fully trusted beats a thick one that is not.

## Layout

```
.agents/knowledge/
├── README.md            ← charter: the tests above + an index of start-here notes
├── architecture/        system shape, service boundaries, seams
├── services/            per-service invariants and surprising contracts
├── frontend/            client state, lifecycle, enforced UI rules
├── integrations/        external systems this repo depends on
├── environment/         local setup and the dev loop
├── practices/           how we work: verification, migration hazards, review focus
├── testing/             suites and harness behaviour
└── security/            credential, auth and egress invariants
```

Adapt the folders to the project — the point is that a new fact has an **obvious home**. Every
folder carries a `README.md` stating what belongs in it *and what does not*, plus an index of its
notes. Read that before adding.

Empty folders are fine: a named home makes it likelier a hard-won fact gets written down at all.
Add a folder only when a third note would live in it.

## Operations

### Promote a fact

1. Apply the four tests.
2. Pick the folder; read its `README.md`.
3. Write `<folder>/<kebab-case-claim>.md`:

```yaml
---
name: <the claim, as a sentence>
description: <one line; what a reader GAINS, not what the note is "about">
type: reference | feedback | project
applies_to: [role, role, ...]
verified: YYYY-MM-DD
---
```

4. Body: the fact → **why it matters / what it costs to get wrong** → a
   `## How this was verified` section naming the method and date. One fact per note, `##` sections
   so it can be anchor-linked.
5. Add it to the folder's index, and to the charter's start-here list if it is that important.
6. **Leave the detailed working copy in the role directory.** Promotion distils; it does not move.

### Sweep at the end of a session or mission

Ask of each candidate: *would another role have needed this today?* Look for learnings that cost
real debugging time, corrections to a previously-held belief, and anything where the tests passed
but reality did not.

Do not sweep mission narrative, per-role preferences, or anything unverified.

### Audit the layer

```bash
python3 <skills>/knowledge-curation/scripts/vault.py lint .agents/knowledge --strict
```

Checks frontmatter, link and anchor resolution (by filename *or* alias), duplicate aliases,
index/disk drift both ways, and notes overdue re-verification. Exit 1 on errors, so it works in CI.

After any large refactor, also grep the layer for references to things that no longer exist — notes
describing deleted code are the most common failure of a shared layer, and the most damaging: they
mislead every role at once.

### Retire or correct a fact

- **Still valuable as a lesson?** Keep it, retitle around the transferable part, and say plainly at
  the top what changed and when.
- **Otherwise delete it.** Prefer deleting to hedging — version control keeps the history.
- Either way, update the folder index and any note linking to it.

Never leave a half-true note. If only the paths moved, correct the paths and say so.

## Bootstrapping the layer

If `.agents/knowledge/` does not exist yet, create the charter and the folder scaffolding with a
`README.md` each, then seed it from what the team already knows — typically the highest-value
entries scattered across `.agents/memory/<role>/`. Scout does this at onboarding; anyone can do it
later.

## Checks before committing

- Frontmatter complete (`name`, `description`, `type`, `applies_to`, `verified`).
- Every relative link resolves; the note appears in its folder index.
- Every claim has a stated verification method — no "should", no "presumably".
- Nothing secret: no tokens, credentials, or customer data.


## Tooling — `scripts/vault.py`

Stdlib-only, Python 3.9+. **Optional**: authoring stays file-tool based, so everything works
without it. Use it for the two jobs prompts do badly — finding the right note among many, and
checking structure deterministically.

```bash
V=<skills>/knowledge-curation/scripts/vault.py

# recall without reading every file
python3 $V query .agents/knowledge --role qa-engineer
python3 $V query .agents/knowledge --tag area/          # whole axis, prefix match
python3 $V query .agents/memory/<role> --layer memory --text "ripgrep"
python3 $V query .agents/knowledge --stale-days 180     # overdue re-verification

# peek at one note (frontmatter + sections + first paragraph)
python3 $V show .agents/knowledge "cold build"          # resolves by ALIAS too

# graph traversal — what links here, what shares tags
python3 $V links .agents/knowledge runtime-architecture-after-m10

# structural checks (CI-friendly: exit 1 on errors)
python3 $V lint .agents/knowledge --strict
```

`lint` catches what is tedious by hand: missing/invalid frontmatter, `name` not matching the
filename, wikilinks that resolve by neither filename nor alias, `[[note#Anchor]]` pointing at a
heading that does not exist, duplicate aliases (which make a link ambiguous), index/disk drift in
both directions, and notes overdue re-verification.

Resolve links **the way Obsidian does — filename OR alias**. A checker that only matches filenames
reports false dead links; that mistake has already been made here once.

## Obsidian Bases

`templates/bases/*.base` are ready-made Obsidian dashboards — copy into the vault root and open
in Obsidian: knowledge by area, notes overdue re-verification, live traps (`type/gotcha` minus
`status/fixed`), and curated memory. They make the layer browsable by a human without any plugin.

## Related

- `memory` — per-role notes and daily logs; the layer below this one.
- Mission state belongs on the work board, not in either memory layer.
