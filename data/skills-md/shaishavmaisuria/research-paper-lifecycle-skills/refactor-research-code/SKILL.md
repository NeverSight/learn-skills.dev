---
name: refactor-research-code
description: Clean research code for public release while preserving reported results. Uses release_audit.py to separate safe mechanical cleanup from ask-first behavior risks and identity leaks. Use for release-ready repos, dead experiment branches, config extraction, documented entrypoints, and double-blind code cleanup.
---

# Refactor Research Code

Take a research repo from "works on my machine" to **a clean, documented,
re-runnable public release — without changing a single number the paper
reports.** Research code accretes dead experiment branches, hardcoded paths,
magic hyperparameters, an undocumented "run this file, then that one" ritual,
and identifying breadcrumbs. This skill removes that cruft and gives the repo a
sensible layout, but it treats *result preservation* as the prime directive: it
classifies every proposed change as **safe** (mechanical, behavior-preserving)
or **ask-first** (could move the numbers), and it never touches an ask-first
item without the author's explicit say-so.

It is **not** generic refactoring (no perf rewrites, no "modernize the API," no
restructuring for its own sake). The only goal is *release readiness with
identical behavior*. When a "cleanup" would change what the code computes, the
right move is to flag it and ask — not to make the repo prettier at the cost of
the paper's claims.

## When to use

- "Clean up / refactor my research code for release." / "It's a mess — get it
  publishable."
- "Remove the dead experiment branches and commented-out code."
- "Separate config from code." / "These hyperparameters are hardcoded
  everywhere."
- "Make my runs deterministic / re-runnable." / "Document the entrypoint."
- "Give the repo a clear layout." / "Strip my identity for double-blind."
- Before `test-research-code` (which adds tests/seeds/env) and
  `prepare-artifacts` (which packages and hosts for a badge) — this is the
  *structural cleanup* that comes first.

## What this is NOT (route elsewhere)

| You want… | Use instead |
|---|---|
| Add smoke tests, pin seeds, capture the environment | [`test-research-code`](../test-research-code/SKILL.md) |
| Package + archival DOI/SWHID + badge taxonomy + appendix | [`prepare-artifacts`](../prepare-artifacts/SKILL.md) |
| Deep double-blind sweep of the *paper* + reversible de-anon | [`anonymize-paper`](../anonymize-paper/SKILL.md) |
| Confirm the produced numbers match the paper's tables | [`verify-results`](../verify-results/SKILL.md) |
| Reorganize the *paper's* sections/argument | [`refactor-structure`](../refactor-structure/SKILL.md) |

This skill *flags* seeding/env gaps and identity leaks and *hands them off*; it
does the structural cleanup itself.

## Inputs

1. The **research-code directory** (the repo, or a subfolder holding the
   experiment scripts). This skill reads local files only; it does not clone.
2. Whether review is **double-blind / single-blind / not blind** (drives the
   identity scan), and any **identifying terms** to scan for (author names,
   institution, internal codenames).
3. Optionally `.paper-memory/profile.yml` (contribution type — a `system` or
   `dataset` paper is judged harder on code quality, leaning toward a Reusable
   release).
4. Optionally the **target venue's artifact track**, if the cleanup is in
   service of one — but badge rules are fetched live by `prepare-artifacts`, not
   here.

## Prime directive: preserve exact numerical behavior

Every action this skill takes falls in one of three buckets. Treat the boundary
between them as sacred.

- **SAFE — apply freely (with the author's nod):** add a README / LICENSE /
  `.gitignore`; move files into a `src/`/package layout (then fix imports);
  delete pure junk (`__pycache__`, `*.pyc`, `.DS_Store`, editor swap files);
  document the existing entrypoint; reformat *whitespace/comments only*. These
  cannot change what the code computes.
- **ASK-FIRST — never touch without explicit confirmation:** delete a code path
  (a backup file, a commented-out block, an `if False:` branch — it may be a
  toggled experiment or silently shadow the live version); extract a hardcoded
  hyperparameter or path into config (the value must be preserved *exactly*);
  change anything touching **seeding, RNG, thread/worker count, dtype/precision,
  or evaluation order** (these *define* the numbers). For each, present the
  finding, the proposed change, and *why it might change results*, then wait.
- **IDENTITY — scrub before any blind upload:** emails, home paths, author
  names, `.git` history. Surface them here; hand the deep sweep to
  `anonymize-paper`.

If you cannot tell whether a change is safe, it is **ask-first** by default. A
prettier repo that reports different numbers is a failure, not a success.

## Process

This follows plan → confirm → apply-safe → ask-on-risk, with the plan grounded
in an **external, measurable signal** — the static audit, not the model's sense
that the repo "looks clean." Name assumptions, show competing readings, and
keep the author in control.

1. **Read memory first.** Read `.paper-memory/lessons.md` (and `profile.yml` if
   present) so you skip what the author already fixed and lead with their
   `recurring` habits (e.g. "you tend to ship `.git` and hardcoded `/home`
   paths"). See
   [`paper-memory-convention.md`](../paper-profile/references/paper-memory-convention.md).

2. **Confirm scope and blind level.** Ask whether review is double-blind and
   what the release is *for* (a public GitHub release, a blind-review supplement,
   an artifact track). Don't anonymize a single-blind/non-blind release — it
   mangles a fine repo. Get the identifying terms to scan for if blind.

3. **Run the static release-refactor audit (deterministic).** Do not hand-grep:

   ```
   python3 scripts/release_audit.py <code-dir> \
       --blind <none|single|double> --names "Jane Doe,Example University"
   # machine-readable:
   python3 scripts/release_audit.py <code-dir> --blind double --json
   ```

   It walks the repo (read-only, no execution, no network, no writes) and emits
   findings tagged by **category** (dead-code, config, entrypoint, layout,
   determinism, identity, hygiene) and, critically, by **risk**: `SAFE`,
   `ASK-FIRST` (behavior-risk), or `IDENTITY`. Flags: `--strict` (any finding
   fails), `--max-files N`, `--max-bytes N` (in-tree blob threshold). Exit
   codes: **0** no ask-first/identity findings, **1** ask-first or identity
   findings present, **2** usage error. This is the signal the plan is built on
   (an external check, not self-judgment); the audit maps *opportunities* — it does not prove
   the repo reproduces.

4. **Present a refactor plan the author approves BEFORE any edit.** Group the
   findings into the three buckets, ordered SAFE → ASK-FIRST → IDENTITY. For
   each ask-first item, state the change *and the result-risk* ("deleting this
   `if False:` block is safe **only if** it is unreachable in every config —
   confirm?"). The author approves or vetoes per item. Categories and the safe
   refactor recipes are in
   [references/release-refactor-catalog.md](references/release-refactor-catalog.md).

5. **Apply SAFE refactors** (with the author's go-ahead), in this order — each
   maps to an audit category:
   - **Layout** — add README (entrypoint, the exact reproduce command per
     result, deps, the directory map), LICENSE, `.gitignore`; move a flat dump
     of scripts into a `src/`/package layout and fix the imports.
   - **Entrypoint** — document (or wire) one obvious command that runs the
     pipeline end to end (`make reproduce` / `run.sh` / `python -m pkg`).
   - **Hygiene** — remove `__pycache__`, `*.pyc`, `.DS_Store`, editor swaps from
     the release copy; move large in-tree data/model blobs to a download
     script / archival host (this last one is *ask-first* — confirm the blob
     isn't needed at runtime).

6. **Walk ASK-FIRST items one at a time, never in bulk.** For each approved
   change: make the *minimal* edit, then **verify behavior is preserved by an
   external check** — re-run the pipeline (or the smoke test) and diff the
   output, not by eyeballing the diff. Behavior preservation is confirmed by
   re-running, which is `test-research-code` / `verify-results` territory; this
   skill **flags and coordinates**, and stops to ask when a change is genuinely
   risky. Escalation is a feature. In particular:
   - **dead-code** — only after confirming nothing imports/reaches it.
   - **config** — extract the literal into config/CLI with the **identical
     value**; a typo here silently changes results.
   - **determinism** — set/record seeds and pin order *in coordination with the
     author*, then re-run to re-confirm the paper's numbers. Adding a seed
     **changes** an unseeded run — this is the highest-risk edit. Hand the
     seed/env mechanics to `test-research-code`.

7. **Handle IDENTITY leaks for blind review.** Surface emails, home paths, names,
   and `.git` history; hand the *deep* sweep (commit history, notebook metadata,
   self-citation phrasing, anonymized mirror) to `anonymize-paper`. Never expose
   the author through the repo on a blind upload.

8. **Re-run the audit until SAFE-clean, with an explicit stop condition.** Loop
   audit → fix → audit until no SAFE/layout/hygiene findings remain and every
   ask-first item is *resolved or consciously deferred* — not open-endedly. Hard
   cap ~3 passes; if the audit still flags the same ask-first item, that is a
   judgment call to escalate, not to keep editing.

9. **Write the refactor plan + change log** to
   `paper-workspace/submission/refactor-research-code-plan.md` and append a line
   to `paper-workspace/INDEX.md`. Lead with what was
   done (safe), then the ask-first decisions (applied / vetoed / deferred, each
   with the result-risk noted), then the identity handoff. Cite each item's
   audit finding.

## Output

- A **refactor plan** (SAFE / ASK-FIRST / IDENTITY buckets, each finding with
  `category` + `risk` + `file[:line]`) plus a **change log** of what was applied,
  vetoed, or deferred — written to `paper-workspace/submission/`.
- The **edited repo files** (only with per-item approval): README / LICENSE /
  `.gitignore`, a `src/`/package layout, a documented entrypoint, junk removed,
  and any ask-first edits the author confirmed.
- A clear handoff list: seeds/env/tests → `test-research-code`; packaging/DOI/
  badge → `prepare-artifacts`; deep anonymization → `anonymize-paper`;
  number-vs-paper check → `verify-results`.

## Adapt to your discipline

The audit reads a directory, not a discipline, so the layout/dead-code/identity
checks apply broadly. For non-Python stacks, the determinism and config
patterns differ (R `set.seed`, Julia `Random.seed!`, a `renv.lock`/`Manifest.toml`
for the env) — the script already knows several; extend the pattern tables in
`scripts/release_audit.py` for your language. The result-preservation contract is
universal: clean the repo, keep the numbers.

## Guardrails

- **Preserve exact numerical behavior — this is the whole point.** Never apply an
  ask-first change (delete code, extract a constant, touch seeding/threading/
  dtype/order) without explicit author approval, and verify preservation by
  *re-running*, never by reading the diff (self-reflection validates its own
  mistakes — the verification must be external).
- **When unsure whether a change is safe, it is ask-first.** A prettier repo that
  reports different numbers is a failure.
- **Run nothing destructive and nothing untrusted.** `release_audit.py` is
  static, read-only, no network. Re-running the pipeline to verify behavior is
  the author's call and may need a sandbox/GPU.
- **Anonymization-aware:** for blind review, never expose identity through the
  repo or `.git` history; hand the deep sweep to `anonymize-paper`.
- **Stay in your lane.** Don't add tests/seeds/env (that's `test-research-code`),
  mint a DOI or package an artifact (that's `prepare-artifacts`), or claim the
  results reproduce (that's `verify-results`, and "reproduce" is never bit-exact
  and never this skill's call).
- **Copilot, not pilot:** it plans, asks, and edits on approval; it never submits,
  deposits, or pushes on the author's behalf.
- `references/` files stay one level deep; keep this file under 500 lines.

## Memory

Uses the shared `.paper-memory/` convention (full spec:
[`paper-memory-convention.md`](../paper-profile/references/paper-memory-convention.md)).

- **At start:** read `lessons.md` to skip already-fixed cleanups and lead with
  `recurring` release habits (e.g. "you ship hardcoded `/home/<you>` paths every
  repo"); read `profile.yml` for the contribution type.
- **At end:** append one dated entry per recurring habit, in the canonical
  format, via `reflect-and-improve`'s `reflect_log.py`:
  ```
  python3 ../reflect-and-improve/scripts/reflect_log.py append \
      --memory .paper-memory --skill refactor-research-code --scope recurring \
      --issue "hyperparameters hardcoded across scripts, no config file" \
      --rec "extract to config.yaml/CLI with identical values every release"
  ```
- Create `.paper-memory/` on demand and offer to add it to `.gitignore`;
  local-only, never uploaded, never copied into this repo.
