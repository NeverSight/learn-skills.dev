---
name: specs-kit-adversarial-review
description: "Stress-tests a specification and its generated task set with a panel of independent models acting as hostile reviewers. Findings are cross-compared: agreement marks real defects, disagreement marks contested areas. Use after /skill:specs-kit-spec-to-tasks and before /skill:specs-kit-task-implementation."
argument-hint: "[ --spec=\"docs/specs/XXX-feature\" ] [ --models=\"a,b,c\" ] [ --force ]"
---

# Adversarial Review — Multi-Model Panel

Submits the specification, the technical plan and the generated tasks to a panel of
independent models, each instructed to break the work rather than approve it. The
individual critiques are then cross-compared: what several models find independently is
almost certainly a real defect, what they disagree about marks a genuinely contested
decision that a single reviewer would have hidden behind a confident answer.

## Why a panel

A single reviewer — however capable — is accommodating by construction and has stable
blind spots. Models trained on different data fail in different places, so:

- **Convergent findings** (found by 2+ reviewers, independently) are treated as real defects.
- **Divergent findings** (found by exactly one, or actively contradicted) are treated as
  contested areas: they are reported as open questions, not as defects.

The panel never negotiates. Each reviewer works in isolation, without seeing the others'
output; the comparison happens afterwards, in this session.

**Input**: the spec folder produced by the upstream workflow
**Output**: `docs/specs/[id]/adversarial-review/` — raw critiques, merged report, verdict

### Workflow Position

```
brainstorm → spec-check → technical-plan → spec-to-tasks → adversarial-review (this) → task-implementation
                                                                    ↑
                                                    last gate before writing code
```

## Usage

```bash
# Review a spec folder with the panel declared in specs-kit.yaml
/skill:specs-kit-adversarial-review docs/specs/001-user-auth/

# Override the declared panel for one run
/skill:specs-kit-adversarial-review --spec=docs/specs/001-user-auth/ --models="provider-a/model-x,provider-b/model-y,provider-c/model-z"

# Proceed despite blocker findings (recorded in the report)
/skill:specs-kit-adversarial-review --spec=docs/specs/001-user-auth/ --force
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--spec` | No | Spec folder (default: auto-detect from CWD) |
| `--models` | No | Comma-separated panel, overriding the declared one. Default: `adversarial_review.panel` in `specs-kit.yaml`. Models are never chosen automatically — see Phase 2 |
| `--force` | No | Do not block on BLOCKER findings; record the override in the report |
| `--rounds` | No | `1` (default) or `2`. Round 2 is rebuttal, see Phase 5 |

## Current Context

If `--spec` is omitted, infer the spec folder from the current working directory (the
nearest folder containing a dated spec-like markdown file plus a `tasks/` directory). If
no spec folder can be determined, stop and inform the user.

## Core Principles

- **Isolation before comparison**: reviewers never see each other's findings in round 1.
- **Hostile by mandate**: a reviewer that returns "looks good" has failed its job. Each
  persona is told to produce findings or to state explicitly, per section, why an attack
  it attempted does not land.
- **Falsifiable findings only**: every finding carries a concrete failure scenario. A
  finding that cannot be phrased as "given X, the implementation will do Y, which
  contradicts Z" is dropped during merge.
- **Consensus is evidence, not authority**: three models agreeing raises severity; it
  never overrides the user's decision.
- **Everything on disk, next to the spec**: raw critiques and the merged report live
  inside the spec folder so they are read together with the specification, in review and
  in future sessions.
- **Best-effort panel**: a reviewer that fails to spawn or returns unparseable output is
  recorded as missing and the panel continues, provided at least two reviewers answered.

---

## Phase 1: Discovery

**Goal**: Locate the review target and confirm the workflow position.

**Actions**:

1. Create the todo list with all phases.
2. Resolve the spec folder from `--spec` or from the current working directory.
3. Collect the review inputs:
   - `YYYY-MM-DD--feature-name.md` — the functional specification (required)
   - `technical-plan.md` — architectural decisions, if present
   - `tasks/TASK-*.md` — the generated tasks (required)
   - `tasks.md` or the dated task index, if present
   - `data-model.md`, `contracts/` — if present
   - `docs/specs/architecture.md`, `docs/specs/ontology.md` — project-level, if present

   These documents are the **entire** review surface. The panel does not read the
   codebase: no source files, no codebase graph, no tests. The question it answers is
   "does this specification hold together", not "does the code match it" — the latter is
   what `/skill:specs-kit-sync` is for, and it only has an answer once code exists.
4. **Abort conditions**:
   - No spec file: stop, suggest `/skill:specs-kit-brainstorm`.
   - No `tasks/` directory: stop, suggest `/skill:specs-kit-spec-to-tasks`. This skill
     reviews a task set; there is nothing to attack before one exists.
   - Unresolved `[NEEDS CLARIFICATION: ...]` markers in the spec: warn and suggest
     `/skill:specs-kit-spec-check` first, then ask whether to continue. Reviewing a spec
     with known holes produces findings that restate the holes.
5. Create `docs/specs/[id]/adversarial-review/` if missing.

---

## Phase 2: Panel Assembly

**Goal**: Take the reviewer models from a declared list — never from what happens to be
available.

The panel is **always** drawn from an explicit allowlist. The model catalogue is not a
menu to pick from: it mixes free and metered models, and several providers bill per
token on every id they expose, so selecting automatically would let the skill spend money
on models the operator never chose. The catalogue is used only to check that a declared
model is spelled correctly.

**Actions**:

1. **Read the declared panel**, in this order of precedence:
   1. `--models="a,b,c"` on the invocation — an explicit, one-off panel.
   2. `adversarial_review.panel` in the project's `specs-kit.yaml`:
      ```yaml
      adversarial_review:
        panel:
          - model: <provider/model>   # persona 1 — The Adversary
          - model: <provider/model>   # persona 2 — The Operator
            thinking: high            # optional, per reviewer
          - model: <provider/model>   # persona 3 — The Executor
      ```
      Order matters: personas are assigned in list order. An entry may also be a bare
      model string when no thinking level is needed. Unknown fields are ignored, so the
      list stays forward-compatible.

      The panel is editable from `/specs-kit-config` → **Adversarial review panel**: the
      same searchable model picker the loop roles use, one slot per persona, with add,
      remove and reorder. Reordering changes which reviewer holds which critique angle.
   3. Nothing declared → **stop**. Do not fall back to a guessed panel: print the yaml
      block above and ask the operator to declare the models they are willing to pay for.
2. **Validate, do not select**. Query the catalogue once, best-effort:
   ```bash
   pi --list-models
   ```
   The output is tabular — provider in the first column, model in the second, plus a
   header row. It is a display format, not a contract: skip lines that do not parse.
   - Declared model missing from the catalogue → hard stop naming the model and the
     reviewer slot. Never substitute a different model: a substitution is a charge the
     operator did not authorise.
   - Catalogue unobtainable → warn and proceed with the declared panel as-is. A model id
     that turns out to be wrong then fails at spawn time and is recorded as an
     unavailable reviewer.
3. **Never grow the panel.** The number of reviewers is exactly what was declared, capped
   at 4. Do not add a reviewer to break a tie, to replace a failed one, or to raise
   confidence — every extra reviewer is another metered run.
4. **Warn on redundancy, do not fix it.** If two declared models share a provider, note
   in the report that their agreement is weaker evidence — same family, shared blind
   spots — but respect the declared list.
5. **Panel size rules**:
   - 3 reviewers is the target.
   - 2 reviewers is acceptable; note in the report that consensus is weaker.
   - 1 reviewer declared: stop. A one-model panel is a single opinion with extra
     ceremony — tell the user and suggest `/skill:specs-kit-task-review` instead.
6. Assign one **persona** per reviewer, in this order (persona 1 to the first model, and
   so on). The personas attack different axes so that overlap between them is meaningful:

   | # | Persona | Attacks |
   |---|---------|---------|
   | 1 | **The Adversary** | Requirements that cannot be falsified, acceptance criteria that pass trivially, implicit assumptions, scope that quietly grew or shrank between spec and tasks |
   | 2 | **The Operator** | What happens when it fails: partial writes, concurrency, retries, unavailable dependencies, migration and rollback, observability of the failure |
   | 3 | **The Executor** | Whether the task set is actually runnable: ordering, missing prerequisite tasks, hidden coupling between "independent" tasks, DoD that cannot be checked, work no task covers |
   | 4 | **The Historian** | Whether the work contradicts what the project already decided: architecture document, ontology terms, recorded decisions |

   Personas are assigned by position, so a panel of 2 uses personas 1 and 2. Persona 4
   is only worth a slot in a project that keeps architecture and ontology documents.

---

## Phase 3: Critique Prompt Construction

**Goal**: Build one prompt per reviewer, self-contained, hostile and explicit about the
artefact it must leave behind.

Each reviewer runs as a fresh subprocess with no session and no memory of this
conversation, so the prompt must carry everything it needs. The prompt is written in
**sections with headings** — objective, review surface, rules, output contract — the same
delegation shape used elsewhere in this project: a reviewer told in one paragraph what to
do and how to answer routinely gets the answer format wrong, and an unparseable critique
is a lost reviewer.

Two things carry the reviewer: the **system prompt** fixes the role, the **user prompt**
fixes the work.

**System prompt** — you do not write this one. `run-panel.sh` carries it and fills in the
persona per reviewer, so that the "JSON only" contract is identical across the panel and
cannot drift between reviewers. It reads:

```
You are a hostile specification reviewer, acting as <persona name>: <persona mandate>.
Your job is to find defects, not to approve — approval is worthless here. You are
autonomous: read the documents you are pointed at with the tools you have, and judge
them. You do not write files, you do not modify anything, you do not ask for
confirmation. Your entire deliverable is one JSON object, emitted as the last thing you
say, matching exactly the schema in the task. No prose before it, no prose after it, no
markdown fences around it.
```

**User prompt skeleton** (per reviewer):

```
# Objective

Review the specification and task breakdown at <spec folder> BEFORE any code is written,
as <persona name>, and report every defect you can substantiate.

# Review surface

Read these files, and only these:

- <spec folder>/YYYY-MM-DD--feature-name.md — the functional specification
- <spec folder>/technical-plan.md — architectural decisions
- <spec folder>/tasks/TASK-*.md — the generated tasks (N files, all of them)
- <spec folder>/data-model.md, <spec folder>/contracts/ — when present
- docs/specs/architecture.md, docs/specs/ontology.md — project-level, when present

No code exists yet for this work. Do not read source files, tests or the codebase graph:
the question is "does this specification hold together", not "does the code match it".

# Rules

- Every finding must be falsifiable: state a concrete scenario (given X, the
  implementation will do Y, which contradicts Z). A finding you cannot phrase this way
  must be dropped.
- Do not invent requirements the specification never claimed. Judge the work against
  what it says it does.
- Do not report style, wording or formatting.
- Report any task that no agent can complete: an acceptance criterion or a Definition of Done
  item that needs an account, a credential in a vault, a signature, a purchase, physical or
  console access, or a human decision. Such a task is a BLOCKER — the implementation cannot
  satisfy it, the review is right to reject it every time, and the retries spend the whole task
  allowance before the run stops on it. The operator half belongs to the "Preconditions
  (operator)" section of the tasks document; only the part an agent can do stays a task.
- If you conclude a section is sound, say which specific attack you tried on it and why
  it did not land — record it under attacks_that_did_not_land, do not simply omit it.
- Severity: BLOCKER (implementation would produce wrong or unsafe behaviour, or a task
  cannot be executed as written) | MAJOR (real defect, discovered late it costs rework)
  | MINOR (worth fixing, does not endanger the implementation).

# Acceptance criteria

- [ ] Every file in the review surface has been read, tasks included
- [ ] Every task has been checked for work only a person could perform
- [ ] Every finding carries a concrete failure scenario
- [ ] The answer is a single JSON object, nothing else

# Output contract

Answer with this JSON object and nothing else — no preamble, no trailing commentary, no
code fences:

{
  "findings": [
    {
      "severity": "BLOCKER|MAJOR|MINOR",
      "target": "<file or task id the finding is about>",
      "claim": "<one sentence: what is wrong>",
      "scenario": "<concrete failure scenario>",
      "suggested_fix": "<one sentence>"
    }
  ],
  "attacks_that_did_not_land": [
    { "target": "<file or task id>", "attack": "<what you tried>", "why_not": "<why the work holds>" }
  ],
  "confidence": "high|medium|low"
}

The deliverable is the JSON, not an explanation of it. You are autonomous: read, judge,
emit.
```

**Pointing beats inlining**: the reviewer has read tools, so name the files rather than
pasting them. Give the full task list by path — never abbreviate it to "the tasks in
`tasks/`", a reviewer that does not know a task exists cannot find the gap it leaves.
Inline a document only when it lives outside the folder the reviewer can reach.

---

## Phase 4: Panel Execution

**Goal**: Run every reviewer in isolation and persist the raw output.

**Actions**:

The panel is spawned by `scripts/run-panel.sh`, next to this file. The flags that make a
critique trustworthy — the declared model with no substitute, read-only tools, no shared
session — live in the script rather than in a code block to be retyped, so they cannot be
dropped by accident: a reviewer spawned without `--no-session` is no longer independent,
and nothing downstream would notice.

The script resolves nothing. Models come from Phase 2 already validated, prompts from
Phase 3 already written; it spawns, captures, extracts and reports status.

**Actions**:

1. Write each reviewer's user prompt from Phase 3 to its own file under the output
   directory, e.g. `prompt--<provider>-<model>.md`. A critique prompt is long and full of
   quotes, braces and newlines; a file avoids every quoting hazard of passing it inline.
2. Run the panel:

   ```bash
   skills/specs-kit-adversarial-review/scripts/run-panel.sh \
     --outdir "docs/specs/[id]/adversarial-review" \
     --reviewer "<model 1>|The Adversary|<prompt file 1>" \
     --reviewer "<model 2>|The Operator|<prompt file 2>" \
     --reviewer "<model 3>|The Executor|<prompt file 3>"
   ```

   | Argument | Meaning |
   |----------|---------|
   | `--outdir` | where transcripts and critiques land; created if missing |
   | `--reviewer "model\|persona\|prompt-file[\|thinking]"` | one per reviewer, repeatable, 2 to 4. `persona` is the name **and** its mandate, taken from the Phase 2 table (`The Operator: what happens when it fails — partial writes, concurrency, ...`), since it is what the script drops into the system prompt. The optional fourth field overrides the default `high` thinking level |
   | `--prefix` | file prefix, `raw` by default — Phase 5 passes `rebuttal` |
   | `--sequential` | run one reviewer at a time instead of all at once |
   | `--timeout` | per-reviewer seconds, when `timeout(1)` is available |

   Reviewers run **in parallel** by default. They are independent by construction —
   separate processes, no shared session, nothing from one run entering another — so
   there is nothing to serialise. The cost is the same either way: the same runs, closer
   together. Pass `--sequential` when two reviewers share a provider and the rate limit
   makes the parallel run flakier than the wait it saves.
3. Read the status lines the script prints — one per reviewer, tab-separated:
   `model`, `persona`, `ok | unparseable | unavailable`, detail. They are the input to
   the panel health table in Phase 7; the detail column carries the reason a reviewer is
   missing, which belongs in the report verbatim.
4. Each usable reviewer leaves `<prefix>--<provider>-<model>.json` — model, persona,
   timestamp, exit status and the critique under `answer` — beside the full transcript
   `<prefix>--<provider>-<model>.txt`. The transcript stays even when parsing succeeds,
   and especially when it fails: it is the evidence behind the merged report.
5. **Failure handling** is the script's, and is best-effort by design: a reviewer that
   exits non-zero but still answered is kept, one that produced no JSON is recorded as
   `unparseable`, one that died is `unavailable`. The panel continues either way.
   Exit code `1` means fewer than 2 usable reviewers: **stop before the merge** and report
   why. A merge over one critique cannot distinguish consensus from opinion. Exit code `2`
   is a caller error — malformed arguments, missing `pi` — and is a bug in this phase, not
   a failed panel.

---

## Phase 5: Rebuttal Round (optional, `--rounds=2`)

**Goal**: Let each reviewer answer the findings it did not raise.

Only worth running when round 1 produced findings the reviewers disagree about.

**Actions**:

1. Build, per reviewer, the list of findings raised by the *others*.
2. Write one prompt file per reviewer asking only: *for each of these findings, does it
   hold? Answer AGREE, DISAGREE or UNSURE with one sentence of reasoning. You did not
   raise these; say plainly if you now think they are right.* The output contract is again
   JSON only — an object with a `verdicts` array, one entry per finding id.
3. Run the same script with the same models and personas and `--prefix rebuttal`, which
   persists `rebuttal--<provider>-<model>.json` beside its transcript.
4. A finding that survives rebuttal with 2+ AGREE is promoted to convergent even if only
   one reviewer raised it originally. A finding with 2+ DISAGREE is demoted to a
   contested area.

---

## Phase 6: Merge & Consensus

**Goal**: Turn N independent critiques into one ranked, deduplicated verdict.

**Actions**:

1. **Normalise** every finding to `(target, claim, scenario, severity, source model)`.
2. **Cluster** semantically equivalent findings across reviewers — same target and same
   underlying defect, regardless of wording. When clustering, keep the sharpest scenario
   and record every model that raised it.
3. **Classify** each cluster:

   | Class | Condition | Meaning |
   |-------|-----------|---------|
   | **Convergent** | raised independently by 2+ reviewers | treated as a real defect |
   | **Contested** | raised by 1, and contradicted by another reviewer or by an `attacks_that_did_not_land` entry on the same target | a genuine open decision, surfaced as a question |
   | **Singleton** | raised by 1, uncontradicted | a real finding from one angle; kept, at its stated severity |

4. **Severity resolution**: a convergent cluster takes the highest severity any reviewer
   assigned it. A singleton keeps its own.
5. **Drop** findings without a concrete scenario, findings about style, and findings that
   demand requirements the specification never claimed.
6. **Rank**: convergent BLOCKER → singleton BLOCKER → convergent MAJOR → the rest.

---

## Phase 7: Report

**Goal**: Write the merged report next to the specification.

Write `docs/specs/[id]/adversarial-review/YYYY-MM-DD--adversarial-review.md`:

```markdown
# Adversarial Review — <feature name>

Date: YYYY-MM-DD
Panel: <model> (The Adversary), <model> (The Operator), <model> (The Executor)
Rounds: 1 | 2
Reviewed: <spec file>, technical-plan.md, N task files

## Verdict

**BLOCKED** — 2 blocker, 5 major, 3 minor
<or> **PASSED WITH FINDINGS** — 0 blocker, 4 major
<or> **PASSED** — no blocker or major findings
<or> **OVERRIDDEN** — 2 blocker, proceeding on --force

## Convergent findings (agreement between reviewers)

### F1 — BLOCKER — TASK-004
Raised by: <model A>, <model C>
**Claim**: ...
**Scenario**: ...
**Suggested fix**: ...
Status: OPEN

## Singleton findings

### F7 — MAJOR — spec §Functional Requirements
Raised by: <model B>
...
Status: OPEN

## Contested areas (reviewers disagree)

### C1 — TASK-002, retry semantics
<model A> considers it a defect; <model B> explicitly judged it sound.
**Open question**: ...
Status: OPEN

## Panel health

| Reviewer | Persona | Status | Findings | Confidence |
|----------|---------|--------|----------|------------|
| <model>  | The Adversary | ok | 6 | high |
| <model>  | The Operator  | unavailable (timeout) | — | — |

## Coverage

| Input | Reviewed |
|-------|----------|
| Specification | yes |
| Technical plan | yes |
| Tasks | 12/12 |
| Contracts | n/a |
```

Every finding is written with `Status: OPEN`. The report is not only the panel's verdict, it
is the worklist that follows it: the remediation skills write back into this file as they
close findings, so a later reader sees both what was found and what was done. Nothing else
in the report is ever rewritten — claims, scenarios and panel health are evidence.

Then print a short `[specs-kit]`-prefixed summary to the user: verdict, counts, report
path.

---

## Phase 8: Gate

**Goal**: Stop the workflow when the panel found something that must not reach code.

**Rules**:

1. **BLOCKER findings present, no `--force`**: the run ends BLOCKED. Do not proceed to
   implementation and do not offer to. Tell the user, per blocker, which skill resolves
   it:
   - ambiguity or gap in the specification → `/skill:specs-kit-spec-check`, which reads
     this report, queues the open findings ahead of its own questions, and writes each
     resolution back here as `RESOLVED` or `REJECTED`
   - the specification is wrong about what the feature should do → re-run
     `/skill:specs-kit-brainstorm` on the affected area
   - architectural defect → `/skill:specs-kit-technical-plan`
   - defect in the task set → re-run `/skill:specs-kit-spec-to-tasks`, or edit the
     affected `tasks/TASK-*.md` directly when the fix is contained to one or two tasks
     (a missing dependency, an acceptance criterion that cannot be checked)
2. **`--force`**: the verdict becomes OVERRIDDEN. The blockers stay in the report, with
   the override and its date recorded. The gate is advisory to the user, never silent.
3. **MAJOR only**: the run passes with findings. Present them and let the user decide.
4. **Clean**: report and proceed.
5. **Idempotent**: re-running produces a new dated report; earlier reports are never
   overwritten, so the history of what the panel said is preserved alongside the spec.
6. **The remediation loop**: BLOCKED → fix → re-review. The panel judged a specification
   that no longer exists once the fixes land, so its verdict does not carry over: only a new
   run can clear the gate. On a re-run, read the previous report's statuses before merging —
   a finding closed as `REJECTED` that the panel raises again is worth flagging as such in
   the new report, since the user already ruled on it once.

   ```
   adversarial-review (BLOCKED)
     → spec-check          closes the findings that target the specification
     → spec-to-tasks       closes the findings that target the task set
     → technical-plan      closes the architectural ones
   adversarial-review (re-run, operator's decision)
   ```

   No remediation skill ever re-runs the panel by itself: another round is another set of
   metered runs, and that is the operator's call.

---

## Error Handling

### No panel declared
```
[specs-kit] No review panel declared. Adversarial review never picks models on its own:
several providers bill per token on every model they expose.
Declare the models you want to spend on in specs-kit.yaml:

  adversarial_review:
    panel:
      - model: <provider/model>   # The Adversary
      - model: <provider/model>   # The Operator
      - model: <provider/model>   # The Executor

or pass them for one run with --models="a,b,c".
```

### Declared model not in the catalogue
```
[specs-kit] Reviewer 2 (The Operator) declares model <model>, which the agent CLI does not know.
Fix the id in specs-kit.yaml. No substitute is chosen: that would bill a model you did not declare.
```

### Model catalogue unavailable
```
[specs-kit] Model catalogue unavailable: the declared panel cannot be validated up front.
Proceeding with the declared models; a wrong id will surface as a failed reviewer.
```

### Panel too small
```
[specs-kit] Only one usable reviewer (<model>). A single-model panel is one opinion, not a panel.
Use /skill:specs-kit-task-review for a single-reviewer pass, or declare a second provider in specs-kit.yaml.
```

### Reviewer failed
```
[specs-kit] Reviewer <model> (The Operator) failed: timeout after Ns. Continuing with 2 reviewers.
Consensus for this run is weaker: findings on failure and recovery are likely under-covered.
```

### No tasks found
```
[specs-kit] No tasks/ directory in <spec folder>. Adversarial review runs on a generated task set.
Run /skill:specs-kit-spec-to-tasks first.
```

---

## Todo Management

```
[ ] Phase 1: Discovery
[ ] Phase 2: Panel Assembly
[ ] Phase 3: Critique Prompt Construction
[ ] Phase 4: Panel Execution (0/3 reviewers)
[ ] Phase 5: Rebuttal Round (optional)
[ ] Phase 6: Merge & Consensus
[ ] Phase 7: Report
[ ] Phase 8: Gate
```

---

## Notes

- The panel reviews **documents, not code**. It runs before implementation; for reviewing
  an implemented task use `/skill:specs-kit-task-review`.
- Reviewer cost scales with the panel size and the amount of inlined material. Three
  reviewers over a large spec is the expensive step of the workflow — it is meant to be,
  since it replaces rework discovered after implementation. The panel is declared, never
  inferred, precisely so that cost is a decision the operator made once and can see in
  `specs-kit.yaml`.
- A panel entry may name a free or locally hosted model. Mixing a metered model with
  cheaper ones is a legitimate configuration: what matters for consensus is that the
  reviewers come from different families, not what they cost.
- The report is an artefact of the specification, not of the session: it is written
  inside the spec folder and is expected to be read alongside the spec.
