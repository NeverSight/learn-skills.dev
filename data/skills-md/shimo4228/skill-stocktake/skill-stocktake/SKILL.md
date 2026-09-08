---
name: skill-stocktake
description: Audit installed Claude skills for quality and surface Keep/Improve/Update/Retire/Merge verdicts. Use when the user says "audit my skills", "stocktake", "review my skills", "which skills should I retire or merge", "do a quality pass over my skills", or "/skill-stocktake". NOT for creating or improving a single skill (that is skill-creator) and NOT for whole-config GC across hooks/permissions/MCP (that is config-gc).
license: MIT
metadata:
  author: shimo4228
  version: "3.1"
  extracted: "2026-02-21"
origin: shimo4228
---

# skill-stocktake — Skill Quality Audit

Evaluate installed skills and assign each a verdict: `Keep / Improve / Update / Retire /
Merge`, plus `Out of scope` for skills this harness does not own (Phase 0). This skill
does NOT do the improving — once it has a verdict, it **hands off to skill-creator (the
improvement engine)**. That boundary is the point: stocktake is the quality gate,
skill-creator is the fixer.

> Design note (v3.1). Per-item quality/freshness and set-level existence/overlap are
> different properties. Deterministic checks are code-owned and unconditional;
> per-item judgment gets narrow, fresh contexts; set-level judgment gets a light
> description sweep with targeted deep reads. Historical verdict counts and named past
> outcomes stay in git history, not in this operational prompt: prior outcomes anchor a
> new audit toward reproducing them instead of judging the current library.

## Modes (`$ARGUMENTS`)

| Argument | Behavior |
|----------|----------|
| none / `full` | Evaluate every skill (default) |
| `changed` | Re-evaluate only skills whose `SKILL.md` mtime is newer than `results.json`'s `evaluated_at`; carry the rest forward from the ledger. Phase 0 and Phase 3 still run over the full set (structural debt, overlap, and contradiction are set properties) |

`changed` detects changes inline (no script):
```bash
find ~/.claude/skills -name SKILL.md -newermt "$(jq -r .evaluated_at ~/.claude/skills/skill-stocktake/results.json)"
```

## Phase 0 — Structural pre-pass (deterministic, code-owned)

Run BEFORE any LLM judgment. These checks never ride on per-item attention:

1. **skill-health scan** — dangling references / missing artifacts across the library
   (run its scanner per `~/.claude/skills/skill-health/SKILL.md`). Mandatory, not
   optional: this is the structural layer of Curate (ADR-0019 layering), and the v2.2
   verification showed exactly these defects slipping through judgment-owned checks.
2. **Ledger hygiene** — for every `results.json` entry: the path must exist on disk and
   the key must follow the canonical rule below. Dedup violations (same path under two
   keys → keep the canonical key, delete the duplicate). Entries whose path no longer
   exists are removed (note them in the report as retired-from-disk).
3. **Existence before judgment** — a skill that fails the existence check never reaches
   Phase 2. Do not let an LLM assign Keep to a file that is not there (this happened:
   two nonexistent paths carried Keep verdicts in the 2026-07-05 ledger).
4. **Ownership before judgment** — the same skill-health run reports `external`: skills
   whose directory is a symlink out of the skills root (a package manager's tree, a
   sibling checkout). **These do not get an Improve/Update verdict.** Record them as
   `Out of scope` with the owner and real path in the reason, and route any real defect
   **upstream** (issue / PR). A verdict here is not actionable — an edit lands in
   someone else's tree, never reaches git, and disappears on their next upgrade.
   Live miss on 2026-07-25: `hunk-review` drew an Improve for a stale flag table and the
   fix was written into `/opt/homebrew/Cellar/hunk/0.17.1/…`; it was reverted and filed
   as [modem-dev/hunk#595](https://github.com/modem-dev/hunk/issues/595). The check is
   fully structural (`is_symlink()`), so it belongs in code, never in per-item attention.

## Phase 1 — Inventory

Enumerate skill definition files with Glob (no script needed):

- `~/.claude/skills/*/SKILL.md`
- if cwd has `.claude/skills/`, also `{cwd}/.claude/skills/*/SKILL.md` (project skills)

**Canonical ledger keys**: one key per skill directory name, matching the path on disk
(ADR-0047). A rule or skill referencing a name in prose does NOT make it a skill.

**Usage evidence** (parent-owned; batch agents never see it). Step 0 — run the script and
transcribe the numbers; do not re-derive them by hand:

```bash
uv run --project ~/.claude/skills/skill-stocktake python -m scripts.usage_stats --days 14
```

JSON out, exit 0 always: `counts` (per skill — `deliberate` / `slash` / `invoke` /
`last_used`, ordered by deliberate use), `window_label`, `measurable`, and `excluded`
(how many rows each correction removed). The four corrections that decide whether the
number means anything — the event-type split, the two sandbox exclusions, and the
real-span label — live in the script's docstring together with their measured effect on
the real log. **Do not re-implement them as a jq one-liner here** (ADR-0052): the
`verify-bootstrap` case is why — 2 apparent uses, 0 after correction.

Two readings the script hands you but cannot make for you:

- `measurable: false` → render usage as `—` (unmeasured). **Never render it as 0** —
  unmeasured and unused are different facts.
- `span_shorter_than_window: true` → label the column with `window_label` (the log's real
  span), not the nominal `14d`.

**Reference-URL evidence** (parent-owned for the same reason, plus one of its own: Phase 2
runs batch agents *in parallel*, and `fetch named URLs` inside each of them is a burst
against the same hosts — the shape `rules/common/debugging.md` forbids). Check every URL
the library names once, serially, here:

```bash
set -o pipefail   # without it a producer crash reads as "0 dead links, all healthy"
uv run --project ~/.claude/skills/skill-health python -m scripts.scan_refs --external-urls |
  uv run --project ~/.claude/skills/skill-health python -m scripts.url_liveness --urls-from -
```

Extraction is `scan_refs`'s job, not a `grep`: it skips fenced code blocks and template
slots, so the audit does not fetch its own example URLs. (`--offline` on `url_liveness`
is the dry run — it reports every URL `skip` without touching the network.)

Verdicts are `live` / `dead` / `blocked` / `skip`. **`blocked` is not `dead`** — a 403 is
bot policy, not absence; reporting it as dead sends the next reader chasing a link that
is fine. `skip`, `offline_suspected: true`, `halted: true`, and a non-null `source_error` all
mean *unchecked*, not *fine* — and `input_lines: 0` means nothing was ever checked, which
is not the same as a clean corpus. If the run halted on a rate limit, say so in the report and do **not** re-run the
remainder in this session.

State the scan result up front: which paths were scanned, how many skills found, and
whether usage is measurable.

## Phase 2 — Per-item scrutiny (parallel small batches, fresh contexts)

Split the target set into batches of **10–12 files** and launch **one subagent per batch in parallel**. Small batches are
the point: per-item attention dilutes as a context fills. Do NOT pass prior verdicts or
the ledger to batch agents (anchoring); do NOT pass usage data (parent-owned dimension).

Each batch agent applies, per skill:

**Stage 1 — binary screen.** Explicit Yes/No per item; surface only the No answers
(these six questions are the canonical set — `skill-creator` §4 reuses them for its
creation-time draft gate by reference, not by copy):

- [ ] Actionability: concrete steps/commands/examples you can act on?
- [ ] Scope fit: name, trigger (description), and body aligned — not too broad or narrow?
- [ ] Within-batch uniqueness: no content overlap with other skills in this batch?
  (a documented orchestrator/sub-skill split is NOT overlap; cross-batch overlap is
  Phase 3's job, not this agent's — the same goes for contradictions with skills outside
  this batch)
- [ ] Currency: **unconditionally verify** every artifact the skill names — `ls` each
  referenced path (`~/.claude/agents/<name>.md`, hooks, bundled scripts) and run
  `--help` / version checks for named CLI flags. "Verify if it looks stale" is banned
  phrasing: the condition is what dilutes. Deterministically checkable claims get
  deterministic checks, every time. **Do not fetch URLs** — the parent checked them once
  in Phase 1 and hands you the verdicts; parallel batch agents each fetching is a burst.
- [ ] Hygiene: is the body free of bloat — trivial prohibition lists, repeated emphasis,
  and step-by-step recitals that could fold into a principle (skill-creator §3 の書き方)?
  Do NOT fold greppable detection terms, self-enforcing prohibitions, or numeric
  thresholds — abstraction destroys their function (ADR-0058 rejected uniform
  shortening for exactly this). Bodies grow after creation; this question is the
  standing check the creation-time gate cannot repeat.
- [ ] Description audit: is the description free of standing instruction text — NOT-for
  routing, "Use PROACTIVELY"-style fire directives, mentions of other skills — beyond
  stating what the skill is for and when to reach for it? A listed description resides
  in the system prompt every session as an unaudited instruction layer (RFC-0018).
  Quote each instruction sentence found (semantic judgment, not regex); do NOT judge
  its effectiveness — the parent joins quotes with invoke stats at synthesis.

**Stocktake-only existence pass (every item, including Keep-bound skills).** This is
separate from the canonical six-question quality screen above, which `skill-creator`
reuses. Answer both questions explicitly:

- [ ] Standalone value: if this file disappeared, would the library lose a user job that
  is not already covered by an installed skill, rule, runtime substrate, or cheap
  on-demand generation?
- [ ] Cost asymmetry: does the skill's independent trigger and reusable judgment justify
  its selection, drift, and maintenance cost?

A No answer makes the skill a non-Keep candidate and must be pressure-tested. Do not
shield a skill from this pass merely because it is current, well written, recently used,
or part of a documented layer.

**Stage 2 — verdict pressure-test (non-Keep candidates only).** Generate 1–3
skill-specific atomic yes/no questions that try to **refute the draft verdict** before
finalizing it. Answer each with one line of evidence (file read, path check, WebSearch).
A refuted defect → fall back toward Keep. A confirmed defect → the No answers become
the concrete improvement list handed to skill-creator (Improve/Update) or the removal
rationale (Retire).

Evaluation is **holistic judgment, not a numeric rubric** — binary answers are evidence
feeding the verdict, never aggregated into a score (a satisfaction ratio changes no
decision and dilutes a single dominant No). Batch agents return structured verdicts
with self-contained reasons. Every skill gets the fixed existence pass; only non-Keep
candidates get the dynamic pressure-test questions.

## Phase 3 — Overlap and contradiction probe (one dedicated agent, set-level)

Duplication **and contradiction** are set properties; they get a specialist, not a side
effect. A per-item batch cannot see either — each agent reads only its own 10 files and
finds nothing wrong with any of them individually. One agent, whole library:

1. Read **name + description (+ heading structure)** of every target file — light pass.
2. Propose candidate clusters greedily (false positives are fine at this stage).
3. For each candidate cluster, read the bodies side by side and judge:
   - `ABSORBABLE_OVERLAP` — two skills serve the same user intent, trigger, and job;
     maintaining both adds selection/drift cost; the source has named unique residue
     that can move into a named Merge target
   - `FULLY_ABSORBED` — another asset already covers the whole user job and the source
     has no unique residue to move; name the covering asset and use Retire, not Merge
   - `CONTRADICTION` — two skills that can both load give **opposite instructions for the
     same situation**, or a sub-skill's content violates the canon it defers to. Quote
     both sides. See the contradiction checks below.
   - `DOCUMENTED_LAYERING` — orchestrator→sub-skill, rule→skill, declared defer; quote
     the defer line and name each file's independently triggerable responsibility
   - `ADJACENT_BUT_DISTINCT` — near domain, different job; name one concrete independent
     user request that each member handles
4. One extra pass over `~/.claude/rules/` and MEMORY.md: is a rule re-stating a skill
   (or vice versa) beyond a declared pointer? Flag promotion residue (a skill whose
   content a rule has fully absorbed) as Retire/Merge candidates.

### Contradiction checks (a declared boundary is a claim, not evidence)

`DOCUMENTED_LAYERING` certifies "not duplicated". It does **not** certify "not
contradictory", and a quoted defer line is the start of the check, not the end. For every
cluster labelled `DOCUMENTED_LAYERING`, run all three:

- **Does the subordinate file comply with the canon it defers to?** Read the canonical
  file's rules and look for the subordinate stating a *different* rule for the same
  decision — especially **defaults** ("if the user gives no X, use Y"), which contradict
  quietly because they only fire in the unspecified case.
- **Is the defer bidirectional?** A one-directional defer (canon claims the subordinate,
  subordinate says nothing) means the subordinate **loads alone without its correction**
  whenever its own description wins the trigger. A broad description on a subordinate
  file turns a latent contradiction into an active one.
- **Do the two files presuppose the same author / project model?** Imported skills
  (`origin` = an external repo) carry their author's premises. A conflict of premises
  reads as a normal-looking instruction and survives every per-file check.

`ABSORBABLE_OVERLAP` produces Merge verdicts because named residue must move into the
target. `FULLY_ABSORBED` produces Retire because the target already covers the whole job
and there is nothing to move. `CONTRADICTION` produces Improve (add the missing defer,
delete the conflicting rule, narrow the trigger) or, when the premises themselves clash
and the subordinate never fires on its own, Retire-and-absorb — name what must move
before deletion.

## Phase 4 — Synthesis (parent)

Merge Phase 2 verdicts, Phase 3 overlap / contradiction verdicts, and parent-owned usage data:

- **Content owns the verdict; usage is reference evidence only.** Render the 14-day
  deliberate-use count and last-used date, but never make usage a prerequisite, veto,
  threshold, or automatic candidate trigger. Recent use does not immunize invalid
  content; zero use does not condemn valid content.
- **Retire content-first.** A skill can be Retire regardless of usage when (a) its
  workflow or underlying premise is obsolete, (b) another asset actually absorbs its
  user job and no standalone residue remains, or (c) it is too thin, non-actionable, or
  cheaply regenerated for its selection/drift/maintenance cost. State which route the
  evidence supports and what covers the need instead.
- **Treat cadence only as a clue.** A zero in 14 days may prompt a trigger/cadence
  explanation, but it never creates a candidate or verdict. A unique seasonal skill may
  remain Keep. Conversely, a recently used skill whose content is fully replaced may be
  Retire.
- **Separate existence from freshness.** A stale version pin, retired CLI flag, or dead
  pointer that is locally fixable is Update, not Retire. It becomes Retire only when the
  verified evidence shows the workflow/premise itself is no longer worth preserving.
- **Charge aggregate cost through the existence pass.** Holding a skill adds selection,
  drift, and maintenance cost. Do not protect a merely adequate skill because it has no
  individual defect; ask whether its independent trigger and reusable judgment still
  justify a separate file. This is judgment, never a quota.
- **Description-audit quotes join usage here.** An instruction sentence whose aim
  (self-firing, misfire routing) the deliberate-use record does not support is a
  removal candidate: fold it into the body or an existing rule. A supported trigger
  surface is left alone (do not strip descriptions that demonstrably fire).
- Conflicts (e.g. batch says Keep, probe says Merge) are resolved by the parent reading
  the cited evidence, not by vote.

| Verdict | Meaning |
|---------|---------|
| Keep | Useful, current, unique value |
| Improve | Worth keeping, but specific improvements needed |
| Update | Referenced technology/artifact is outdated (verified, with evidence) |
| Retire | Obsolete, cost-asymmetric, or `FULLY_ABSORBED` with no residue to move |
| Merge into [X] | `ABSORBABLE_OVERLAP` with named unique residue; name the target and residue to move |
| Retire-and-absorb | A `CONTRADICTION` whose premises clash and whose subordinate never fires on its own; name what must move into the canon before deletion |

Evaluation is **origin-blind**: the same checklist applies to every skill.

Render a table: `Skill | 14d | last used | Verdict | Reason`, where the count is
**deliberate use only** (`slash + invoke`). If the log is younger than 14 days, replace
`14d` with its real span.

## Phase 5 — Consolidation

**Confirm one by one** (config-gc's confirm-each design): walk the non-Keep candidates
sequentially — for each, show the evidence first, then ask `[y/n/skip]`. Never batch the
approval. The user can stop at any point; `skip` records the verdict in the ledger
unactioned.

- **Retire / Merge**: per file, present (1) the specific defect found, (2) what covers
  the same need instead, (3) the impact of removal (dependent skills, rule pointers,
  MEMORY references) → ask `[y/n/skip]`. **Act only after the user confirms that file.**
- **Improve / Update**: **offer** per skill — "Hand `<skill>` to skill-creator?
  `[y/n/skip]`" — and on approval invoke `skill-creator` with the target skill and the
  No-answer list. Stocktake never does the improvement work itself.
- **Update the ledger**: Read `results.json` → merge this run's verdicts → Write it back
  (`evaluated_at` = real UTC from `date -u +%Y-%m-%dT%H:%M:%SZ`). In `changed` mode,
  preserve the prior verdicts of skills you did not re-evaluate.
- If MEMORY.md exceeds 100 lines, propose compression.

## Reason quality (required)

Every `reason` must be **self-contained** — decision-enabling on its own. "unchanged"
alone is banned; always restate the evidence. For non-Keep verdicts, the reason cites
the **No answers from the binary screen / pressure-test** (question + one-line evidence).

- **Retire**: state the defect + the replacement. Bad: `"Superseded"` / Good:
  `"disable-model-invocation: true already set; continuous-learning-v2 covers the same
  patterns plus confidence scoring. No unique content remains."`
- **Merge**: name the target + what to integrate. Bad: `"Overlaps with X"` / Good:
  `"42-line thin content; Step 4 of chatlog-to-article already covers this workflow.
  Integrate the 'article angle' tip there as a note."`
- **Improve**: which section, what change. Bad: `"Too long"` / Good: `"276 lines;
  'Framework Comparison' (L80–140) duplicates ai-era-architecture-principles. Delete it
  to reach ~150 lines."`
- **Keep** (mtime-only change in `changed` mode): restate the original rationale.

## results.json (lean ledger)

```json
{
  "evaluated_at": "2026-06-24T11:09:00Z",
  "skills": {
    "<skill-name>": {
      "path": "~/.claude/skills/<name>/SKILL.md",
      "verdict": "Keep",
      "reason": "...",
      "mtime": "2026-01-15T08:30:00Z"
    }
  }
}
```

A ledger for verdict history and the last-audit timestamp only. Update it inline with
Read/Write, not a script. Global skills only (project skills are read fresh from cwd,
not cached here). Phase 0's hygiene rules (canonical keys, existing paths) are part of
every write.

## Related

- `skill-creator` — the improvement engine; hand off Improve/Update work to it.
- `skill-health` — the deterministic structural layer; Phase 0 runs its scanner as a
  mandatory pre-pass (enumerate-then-decide: code enumerates debt, judgment decides).
- `config-gc` — GC over skill *existence* and the whole of ~/.claude; stocktake judges
  skill *quality*.
- `rules-stocktake` — the same audit for `~/.claude/rules/` (residency cost instead of
  usage).
- `agent-stocktake` — the third sibling, for `~/.claude/agents/` (hybrid cost model:
  description = residency, body = invocation).
- `generation-audit` — on a model-generation change, collects runtime-layer evidence
  (conflict / redundancy / drift) and hands the skills slice to Phase 4 synthesis as
  external evidence (read, never require).
- `harness-boundary` — design-time lens (layer / portability / obsolescence) for proposed
  mechanisms; applied to an installed skill, its Delete / Move are Phase 4 evidence only.
- `repo-asset-stocktake` — the same stocktake pattern for a project repo's non-code
  assets.
- `llm-as-judge` — the generic judge design canon (binary screen → pressure-test →
  holistic named verdict, no aggregation); Phase 2 is its library-scale implementation.
- `harness-sync` — use it to sync this skill to its public repo.
- Usage measurement: `~/.claude/hooks/log-skill-usage.sh` →
  `~/.claude/metrics/skill-usage.jsonl` (a measurement layer independent of stocktake).

## References

The two-stage binary-question design (screen → verdict pressure-test, holistic verdict,
no score aggregation) follows the checklist-decomposition evaluation line: BinEval
"Ask, Don't Judge" ([arXiv:2606.27226](https://arxiv.org/abs/2606.27226)), CheckEval
(arXiv:2403.18771), TICK (arXiv:2410.03608). Scores are deliberately not adopted:
BinEval's own limitations show over-decomposition degrades correlation on holistic
quality dimensions, and a satisfaction ratio would dilute a single dominant No.

The v3.1 hybrid architecture separates deterministic verification, narrow per-item
scrutiny, and set-level existence/overlap judgment. The split preserves attention for
each property without carrying prior verdict outcomes into the next audit.
