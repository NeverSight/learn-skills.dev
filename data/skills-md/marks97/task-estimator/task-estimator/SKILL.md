---
name: task-estimator
description: Estimate how long a coding task will take, using the user's own measured history instead of intuition. Use this skill whenever someone asks for an estimate, an ETA, a timeline or a deadline for a feature, bug, refactor, migration, script or investigation — "how long will this take", "give me an estimate", "how many hours is this", "can this ship today", "is this a one-day job", "how many days for the whole epic", "what should I tell the client", "estimate this ticket", "size this" — and equally when the ask is skeptical ("is that realistic", "why did that take three days"). Also use it for the machinery behind the estimates — setting up or calibrating estimation, backfilling the task ledger from past Claude Code transcripts, recording a finished task's actuals ("record this task", "log this one", "add this to the ledger"), and re-running calibration or checking whether past estimates were any good. Trigger it even when the word "estimate" never appears — a question about how much work something is, or how long something took, is this skill.
---

# Task estimator

Estimates from **your measured history**, not from the model's intuition about how hard
something looks. The model's intuition is the thing that is broken: developers using AI
tools believed they were 20% faster while measuring 19% slower (METR 2025). An estimate
that is not anchored to recorded actuals just reproduces that gap in writing.

So this skill does three things: it keeps a ledger of what tasks actually cost, it quotes
new tasks against the empirical distribution of similar past tasks, and it scores its own
past quotes so the bias is visible.

Depth on the evidence is in `references/`: `estimation-science.md` (the classical results
— EBS, reference classes, anchoring, flow metrics), `ai-era-evidence.md` (what changed once
an agent was in the loop), `measurement-model.md` (the phase taxonomy, the measured
constants, and the calibration math the scripts implement). Read them when a rule here looks
arbitrary — every rule traces to a result there. Do not re-derive the theory during an
estimate; execute the steps.

## Pick a mode

| The user is doing this | Mode |
|---|---|
| Asking how long something will take, ETA, sizing, "is this a day?" | **estimate** (default) |
| First run, no `$LEDGER` (see *Ledger layout*), "set this up", "calibrate me", "backfill" | **setup** |
| "record this task", "log this", finished a task, the CLAUDE.md hook fired | **record** — `record.mjs` |
| "re-run calibration", "how good are your estimates", "were you right", "recalibrate" | **recalibrate** — `calibrate.mjs` + `score.mjs` |

The four modes are one loop, and it only closes if every leg runs: **estimate** logs a
quote → **record** measures the actual and scores it against that quote → **recalibrate**
reports whether the quotes are any good → the next **estimate** corrects for it. Skipping
the log in estimate mode, or never running record mode, leaves the skill quoting from
history forever without ever learning whether its own quotes were right.

If `$LEDGER/calibration.json` does not exist and the user asks for an
estimate, say so and offer setup — then still give a prior-only estimate if they want one
now. Never silently estimate off an empty ledger.

## Ledger layout

`$LEDGER` resolves in this order, first hit wins:

1. `$CLAUDE_ESTIMATION_DIR` — explicit override.
2. `~/.claude/estimation` — the portable default.

The ledger lives outside the skill directory so it survives reinstalls, and
outside any per-account config dir so it is one history, not one per account.

```
$LEDGER/
  ledger/
    chats.ndjson       # one row per Claude Code conversation (mined)
    tasks.ndjson       # one row per unit of work; the reference class lives here
    estimates.ndjson   # one row per quote this skill emitted, for scoring
  calibration.json     # population priors + per-class empirical quantiles
```

Scripts (`$SKILL/scripts/`). The four primitives are pure and stdout-oriented:
`extract.mjs` (transcript JSONL → one chat row), `stitch.mjs` (chats → tasks),
`digest.mjs` (one chat → compact text for an LLM pass), `calibrate.mjs` (ledger →
calibration.json). `slice.mjs` sits between the last two: it cuts each epic's chats into
labelled sub-deliverables (`task.sub_tasks[]`) without ever splitting the epic row.

Two more close the loop, and they are the ones **record** and **recalibrate** run:
`record.mjs` (one finished session → extract → stitch → rework-merge → outcome →
score, appended to the ledger) and `score.mjs` (estimates × tasks → how good the
quotes were). Note the division of labour, because the two calibrations answer
different questions and get confused constantly:

| | Question | Reads | Writes |
|---|---|---|---|
| `calibrate.mjs` | how long do tasks *like this* take? | tasks.ndjson | calibration.json |
| `score.mjs` | were my *quotes* any good? | estimates.ndjson + tasks.ndjson | nothing |

`calibrate.mjs` is what an estimate quotes from. `score.mjs` is what tells you the
quotes are systematically low. A ledger with no `estimates.ndjson` rows can do the
first forever and never the second — which is the failure this loop exists to stop.

### estimates.ndjson — the row schema

One row per quote, written by **estimate** step 8, read by `record.mjs` and
`score.mjs`. `schema: "estimate.v1"`:

```json
{"schema":"estimate.v1",
 "estimate_id":"2026-08-31-add-oauth-provider",
 "date":"2026-08-31",
 "task":"add-oauth-provider",
 "ticket":null,
 "task_desc_hash":null,
 "features":{"type":"feature-epic","novelty":"adaptation","precedent":"saml-provider"},
 "class":{"neighbors":["example-api/TICKET-3880"],"n":1,"gate":"prior-only"},
 "quoted":{"agent_hours":{"p50":76,"lo":50,"hi":150},
           "human_rounds":{"p50":null,"lo":600,"hi":1000},
           "calendar_days":{"p50":null,"lo":28,"hi":49}},
 "source":"ledger-neighbor+bounded-adjustment"}
```

Field rules, each of which exists because breaking it makes the row unscorable:

- **`estimate_id`** is the join key `record.mjs --estimate-id` takes. Default it to
  `<date>-<task>`. Once a task is recorded against it, the id is written back onto
  the **task row** as `estimate_id`, so the link is never re-guessed.
- **`task`** is a slug, and it must be one `record.mjs` can find later: the ticket
  key, the branch name, or the phrase the classifier will summarise the work as.
  Matching runs `estimate_id → ticket → task_desc_hash → task_id slug → summary →
  epic-slice slug → sub-deliverable slug`, first hit wins. **A quote that matched an
  epic slice is scored against that slice's hours, not the epic's** — scoring "the
  webhook part" against a 76-hour integration would report a 60× miss on a quote that
  was never about the integration. `score.mjs` names the slice in `sub_task` when it
  does this.
- **`quoted`** carries the **three axes the ledger measures — `agent_hours`,
  `human_rounds`, `calendar_days` — and no others.** A band quoted in weeks is
  stored in days. Quote something on every axis you can: an axis with no band is
  silently unscorable, which is how an estimator ends up with a coverage number
  built from one axis.
- **`lo`/`hi` are the band you actually committed to** (the P50→P85 span, or the
  regime-split range). `score.mjs` scores coverage at 80% nominal against them.
- **`p50` may be null**, and then `score.mjs` uses the band's **log** midpoint
  (`sqrt(lo*hi)`) and flags every ratio derived from it — so a derived centre is
  never mistaken for something you said.
- **`task_desc_hash`** — sha256 of the anchor-stripped description. Optional but
  preferred when there is no ticket: it keeps prose out of the ledger while still
  matching later.

Legacy rows (the pre-schema hand-written shape: `agent_h_p50`, `agent_h_band`,
`rounds_band`, `calendar_weeks_band`) are normalised on read and still score. Write
new rows in the canonical shape.

**Not every real string is a real join signal.** `stitch.mjs` denies generic branches
(`main` is on every chat that ever pushed) and, for the same reason, unattested ticket keys:
a dated report filename pasted into a review round yielded `REPORT-2026` and welded 46 chats
and 79 agent-hours into one "task". A key only becomes a stitch edge if it is below the
load-bearing fan-out, or its prefix appears in a feature branch, or its namespace is *live* —
several sibling keys that also turn up **apart** from it, since co-pasted fragments always
travel together and real tickets do not. The rules and their evidence are in the comments on
`isPlausibleTicketKey` (extract.mjs) and `eligibleTicketKeys` (stitch.mjs).

Three drivers run a whole corpus and are **resumable** — re-running one continues, it never
restarts: `backfill.mjs` (walk a transcripts root → chats.ndjson + tasks.ndjson),
`classify.mjs` (haiku → classifications.ndjson, merged into tasks.ndjson),
`audit.mjs` (stratified sonnet re-judgement → audit.ndjson + per-field agreement).

## Mode: estimate

**The order below is mandatory.** Each step exists to stop a specific failure. Do not
reorder, do not skip ahead to "well, this looks like about a day".

### 1. Strip the anchors — before any reasoning

Read the task description. Before you think about duration at all, remove from
consideration: stated deadlines, target dates, story points, "should be quick / small /
huge / trivial", the user's own guess, a client's promised date, a ticket estimate field.

An irrelevant number in the prompt shifts estimates by **4–5×**, and the effect survives
being told to ignore it and survives coming from an obviously unqualified source. You
cannot un-see an anchor, so handle it explicitly: if the ask contained one, say
**"noting you said ~X — the number below is history-derived and was computed before
reading it"** and never let it move the quantile.

### 2. Readiness gate — refuse to estimate unready work

Do not produce an estimate if either is true:

- **No testable acceptance criteria.** Nobody can say what "done" is, in a way a test or a
  concrete observation could settle.
- **No converged implementation strategy.** Two or more materially different approaches are
  still live, and the choice changes the work by more than one bucket.

These are exactly the tasks that explode: the distribution is bimodal — ~78% of "easy"
tasks land near their class median, and the other ~22% overrun by more than 180%, and the
overrunners are overwhelmingly the ones that failed this gate.

Output instead:

> **Not estimable yet — recommend a timeboxed spike.**
> Missing: `<the specific criterion or the unresolved fork>`.
> Timebox: `<1 bucket on the ladder>`, and the deliverable of the spike is the missing
> thing, not the feature.
> Re-run the estimate after the spike; it will be a different (and much tighter) class.

Recommending a spike is a real answer. Producing a number for an unspecified task is not.

### 3. Extract features

Follow `prompts/estimate-features.md`. It is a checklist with the actual commands to run —
do the searches, do not guess the answers. It yields:

`repos[]`, `task_type` (bugfix|feature|refactor|migration|infra|investigation|script),
`greenfield|brownfield`, `precedent_in_repo` (did we ship this shape here before — find it
or state none), `self_verifiable` (tests|typecheck-only|human-eyes|prod-only),
`blast_radius` (grep-counted files likely touched), `external_deps[]` (third-party
approvals, other humans, deploys), `parallelizable` (across files/repos).

Precedent and self-verifiability do the most work of any features in the set. Spend the
searches on them.

Then place the task in the **speedup quadrant**, because the agent discount is not a
scalar:

| | Simple | Complex |
|---|---|---|
| **Greenfield** | +30–40% | +10–15% |
| **Brownfield** | +15–20% | 0–10%, sometimes negative |

Most work in a mature repo is bottom-right, where the discount is near zero and can invert.
Record the quadrant; step 6 uses it.

### 4. Retrieve the reference class

From `$LEDGER/ledger/tasks.ndjson`, in this order:

1. **k = 1–3 nearest neighbours** on the feature vector. Small k on purpose — larger k
   regresses to the mean and destroys what made analogy work.
2. If the tight class has **n < 5**, widen to the whole `task_type` class and say you
   widened.
3. If still thin, fall back to the population priors in `calibration.json` and say the
   estimate is prior-based.

**Check `field_reliability` before you lean on a field, and say what you find.** Every field
in it is either `reliable: true` or `reliable: false` with a measured agreement rate — there
is no unmeasured field. As of the 2026-09-01 audit `task_type` is the one that fails
(0.38 raw / 0.43 admissible, n=58 stride), so **widening to the `task_type` class is the
weakest move in this list and must be stated as such**: prefer the k=1–3 neighbours, and
when you do widen, say the class label itself agreed with a stronger judge only ~4 times in
10. It agrees 0.51 on well-stitched rows, so the fault is largely the 26% of rows that are
over-merged rather than the label.

Always record which class you landed in and its `n`. Report the **variance across the
neighbours**, not just the centre: 1h/1h/9h and 3h/3h/4h centre in the same place and mean
completely different things.

**When the ask is a slice of a bigger piece of work, use the `epic-slice` class instead.**
`calibration.json` carries `reference_classes["epic-slice"]` (with its own `by_task_type`),
built by `slice.mjs` from the sub-deliverables of every task with ≥6 chats. Reach for it
when the question is "how long is the webhook part of the payments integration" rather than
"how long is the payments integration" — a slice inherits an epic's already-loaded context, its
branch and its conventions, so it is **not** the same animal as a standalone task of the
same `task_type`. Say which of the two classes you quoted; they answer different questions
and the epic row remains the unit of record for both.

**With no usable class at all**, size the human-rounds axis from the constant-hazard model
rather than from feel: an agent's 80%-reliability horizon is ~30 minutes of
human-equivalent work, so `human_rounds ≈ ceil(human_equivalent_minutes / 30)`. Sanity band:
real sessions run **3.3–5.4 interventions**. A prior-only quote landing outside that band
needs a reason.

### 5. Compute empirical quantiles — never a fit, never a mean

Sort the class's actuals and take the quantiles **directly off the observed values**, in
log space. Do not fit a lognormal (or anything else) and read quantiles off the curve: the
fit systematically understates the tail, which is the only part of the distribution anyone
is actually asking about. Do not quote a mean; on a fat-tailed class the mean is neither
the typical case nor the risk.

**Check your own bias before quoting.** Run `node $SKILL/scripts/score.mjs` and read the
per-axis line: it is the only evidence about *this estimator* rather than about the tasks.

- If it prints **TOO EARLY TO CALL** (fewer than 5 scored pairs), quote the class straight
  and say the estimator itself is unvalidated. Do **not** apply a correction derived from
  one or two points — a single ratio is an observation, not a bias.
- Once it reports a geometric mean ratio over n ≥ 5, prefer **EBS ratio resampling**: draw
  whole historical estimate/actual ratios with replacement (100+ draws) and divide the
  class centre by each draw. Same principle — whole observed values, resampled, never
  averaged. Note this in `source` on the logged row so the provenance survives.

**Sample gates. State which one you are at, every time:**

| n in class | You may quote |
|---|---|
| < 5 | Nothing from the class. Prior-only, and say so explicitly. |
| 5–9 | **P50 only**, with a warning that there is no usable upper bound yet. |
| 10–19 | **P85**. |
| ≥ 20 | **P95** allowed. |

Below **n ≈ 20** the class quantile is also **shrunk toward the population prior** by
`w = n/(n+κ)` — a personal P85 at n=11 spans 0.31–2.26× of the truth, so it is worth
something as an adjustment and nothing on its own. `calibrate.mjs` emits the shrunk value;
use it, do not recompute the raw quantile and quote that instead.

15 fresh points beat 150 stale ones. `calibrate.mjs` already applies a 90-day half-life —
do not re-weight by hand.

### 6. Inside-view adjustment — at most one bucket

The log ladder: **≈15m · 1h · 3h · 1d · 3d · 1w+**.

You may move the class result by **at most one bucket**, and only while naming the
specific evidence: "the identical Prisma migration shipped twice this month, both under
2h". Unnamed intuition ("this feels simpler") buys **zero** adjustment. Two buckets is not
an adjustment, it is a different class — go back to step 4.

Then apply the **quadrant discount** from step 3 — and **widen the interval when you do,
never narrow it.** Speedup and variance move together: the quadrants with the biggest
expected gains also have the widest spread. "The agent will handle it" is a reason for a
wider band, not a tighter one.

Budget the **failure branch longer than the success branch**. Failed trajectories run
**18–82% longer** than successful ones; failure is expensive and late, not cheap and early.

Default to the class **P85**. Dropping to P50 requires naming the mitigation that removed
the tail: spec frozen, harness exists, no external dependency, precedent in this repo.

### 7. Output — the SLE, three axes, never a single number

```
**85% of your similar tasks finished in ≤ X agent-hours, ≤ Y human rounds, Z calendar days**
(class: <description>, n=<N>, neighbors: <task ids>)
```

Then, in this order:

- **P50 line** — "half finished in ≤ …", so the typical case is visible next to the limit.
- **Regime call** — the distribution is bimodal, not a spread around a centre. Say which
  mode you think this is in and why: *agent-nails-it* (precedent exists, tests verify,
  narrow blast radius) or *integration-thrash* (verification is human-eyes or prod-only,
  no precedent, external surface). Where both are live, give both with rough weights. A
  single blended number sits in the trough between the modes and describes almost nothing.
- **Blow-up risk flags**, each named, only the ones that apply: vague spec ·
  human-eyes-only verification · wide blast radius · external waits · no precedent in repo.
  Name the flag and the specific thing that triggered it.
- **External calendar waits, listed separately.** App review, a platform approval, someone
  else's deploy window, a human decision. This is **dead time, not work** — never fold it
  into agent-hours; it is why calendar days and agent-hours are separate axes.
- **The review tail is part of calendar days.** If done means merged, the estimate does not
  stop at "code written" — that is the part that got faster. Review time is up 441% and
  agent-authored PRs wait **5.3× longer** for pickup. Include the wait for a reviewer
  explicitly whenever the task ends in a PR someone else must merge.
- **"Split this"** whenever the estimate exceeds the class P85. Right-sizing beats
  budgeting more. Propose the actual split into ≤1-bucket pieces, do not just advise it.

Never emit a single number. A point estimate on a fat-tailed class is a category error,
and it is the format that makes people commit to dates they then miss.

### 8. Log the quote — not optional, and not later

**An estimate that was never logged can never be scored.** This is the step that makes
the skill improve instead of repeating itself, and it is the one that gets skipped
because the user already has their answer. Do it in the same turn you quote.

Append **one `estimate.v1` row** to `$LEDGER/ledger/estimates.ndjson` — schema and
field rules are in *Ledger layout*; the three axes and a `task` slug `record.mjs` can
find again are the load-bearing parts:

```bash
LEDGER=${CLAUDE_ESTIMATION_DIR:-~/.claude/estimation}
cat >> $LEDGER/ledger/estimates.ndjson <<'EOF'
{"schema":"estimate.v1","estimate_id":"2026-09-01-csv-export","date":"2026-09-01","task":"TICKET-1234","ticket":"TICKET-1234","features":{"task_type":"feature","greenfield":false,"precedent_in_repo":"example-api/TICKET-1180","self_verifiable":"tests","blast_radius":9},"class":{"neighbors":["example-api/TICKET-1180","example-api/TICKET-1204"],"n":7,"gate":"p50-only"},"quoted":{"agent_hours":{"p50":3,"lo":1.5,"hi":9},"human_rounds":{"p50":12,"lo":6,"hi":30},"calendar_days":{"p50":1,"lo":1,"hi":4}},"source":"class-p50+one-bucket-precedent-adjustment"}
EOF
```

Then close the estimate by telling the user the loop is armed, in one line: *"logged as
`2026-09-01-csv-export` — run record mode when it lands and it scores itself."*

Two rules about the numbers in that row:

- **Log what you told the user, not a hedged version.** A band quietly widened in the
  ledger manufactures coverage the estimator never earned.
- **Never edit a logged row once work has started.** A quote revised with knowledge of
  the outcome is not a quote. Log a second row and let both score.

Store the **hash**, not the text — the ledger stays free of task prose, and `record` mode
matches on it later to score ratio (actual/quoted) and interval coverage.

### Doctrine — state this when the shape of the estimate is questioned

> **duration ≈ rounds × (per-round agent time + per-round human wait)**
>
> **Human round count is the dominant predictor (r ≈ 0.83 on measured data). First-turn
> duration predicts nothing (r ≈ 0.0).**

So a task that one-shots in 40 minutes and a task that takes eight rounds of "not quite,
try again" are not comparable, however similar the diff looks. Estimate the rounds; the
minutes follow. And the per-round human wait is the user's own latency — it is in the
recorded actuals already, do not model it separately.

Two corollaries worth saying out loud when they apply:

- **A long first turn is a good sign, not a bad one.** It predicts *fewer* rounds —
  front-loaded framing pays for itself. Never quote a task as slow because it started slow.
- **Waiting for permission prompts is the largest recoverable loss.** Approval gaps are 52%
  of long intra-task pauses, median 32 minutes each. If the user's setup asks for approval
  per tool call, that — not model speed — is what is costing them the afternoon.

Estimate **rounds and steps, never lines**. Assistant steps correlate with duration at
r ≈ 0.86 and human rounds at r ≈ 0.82; LOC manages only 0.53. A diff-size estimate is a
worse predictor than the thing it feels more concrete than.

**Never accept self-reported speedups as calibration input.** "That took me 20 minutes" is
not data; it is the perception gap talking. Only mined actuals go in the ledger.

## Mode: setup

### 1. Structure

Check `$LEDGER` (resolution order in *Ledger layout*). Create `ledger/`, empty `chats.ndjson` / `tasks.ndjson` /
`estimates.ndjson`, and a placeholder `calibration.json`. Do not overwrite anything that
exists — if the ledger already has rows, you are in **recalibrate**, not setup.

### 2. Consent — before touching any transcript

**Stop and ask with AskUserQuestion.** Do not read a single transcript before an answer.
Explain exactly this:

- It reads Claude Code conversation JSONL under `~/.claude*/projects/` (both accounts) from
  this machine only.
- Nothing leaves the machine except the classification calls, which go to the Anthropic API
  as `claude -p` — the same place the user's normal sessions already go.
- What gets stored: task shape and durations. Not the conversation text.
- It is reversible: `rm -rf ~/.claude/estimation`.

Offer to scope it: all projects, one project, or the last N months.

### 3. Backfill — deterministic pass

One command over the whole transcripts root — it walks every project dir, extracts each
`.jsonl` **sequentially** (never parallel: these files run to 140 MB and this is a live
box), and stitches globally at the end:

```bash
nice -n 19 ionice -c3 node --max-old-space-size=2048 $SKILL/scripts/backfill.mjs \
  --root ~/.claude/projects
```

It skips transcripts under 5 KB as noise (consent probes, sessions that never got past the
banner) and counts them; it skips any chat whose file **and sidecar directory** are both
unchanged since the last run. Interrupt it and re-run — chats are appended as they are
extracted.

Scratch and its progress log go in `/tmp/claude/task-estimator-backfill/`, never in a repo
and never in the ledger.

**Subagent sidecars are mined too, and they are where the delegated work is.** Next to
`<chat_id>.jsonl` the harness writes `<chat_id>/subagents/agent-*.jsonl` plus a
`.meta.json` naming each agent's type. `extract.mjs` runs the **same** extraction core over
each one and folds the result into the parent chat's `subagents` object —
`loc_added`/`loc_removed`, `files_edited`, `repos`, `active_min`, `sidecar_count` and a
`per_type` breakdown. This is not an optional refinement: a `Task`/`Agent` tool_result in
this Claude Code era carries no `toolStats`, so a chat that delegated everything reads as
zero LOC without it, and the parent does not even persist every spawn (one 104-spawn sprint
kept two). Two rules hold absolutely:

- **Nothing folds into the parent's own fields.** A subagent's minutes run *inside* its
  parent's wall clock, so adding them would count time that was spent once, twice. The
  chat's `loc_added`, `files_edited` and `agent_active_min` never move.
- **Nothing is counted twice inside `subagents` either.** Where the parent *did* report
  `toolStats` for a spawn and a sidecar for that same `toolUseId` exists, the sidecar
  measurement **replaces** the reported one — it is the primary record. Spawns with no
  sidecar keep their reported numbers. Depth-2 agents (spawned by another subagent, so no
  `tool_use` block exists in the parent at all) are added, which is why `subagents.count`
  can exceed the number of spawn blocks.

Sidecars are never emitted as chats of their own.

**Every chat also gets a `repo_share`** — `{repo: fraction}`, summing to exactly 1,
splitting its minutes across repos in proportion to the files edited there (parent edits
plus subagent edits). Chats that edited nothing attribute wholly to their cwd repo, or to
the workspace when the cwd is a multi-repo root. `stitch.mjs` rolls this into
`agent_hours_by_repo` / `subagent_hours_by_repo` on the task row. **Use those for any
per-repo or per-area question.** Summing `agent_hours` over `repos` instead counts every
multi-repo chat once per repo — on this corpus that inflated an area roll-up ~25x.

**Probe sessions get a `noise` flag** — `"permtest"` (a permission probe: `echo
PERMTEST_OK`, "testing perms here") or `"qa-probe"` (a session run out of a `/tmp` scratch
tree). Detection is ratio-based, not keyword-based, because real chats discuss permission
probes at length; a chat is a probe only when probing is essentially all it did. The rows
stay in the ledger and `calibrate.mjs` drops them from the quantiles.

### 4. Backfill — semantic pass

One classification per chat: `digest.mjs` → haiku. **Before running, count the chats,
estimate the token spend, print it, and ask to proceed.** A backfill over a year of
transcripts is not free and the user gets to see the number first — `--estimate-only`
prints exactly that and does nothing else.

```bash
node $SKILL/scripts/classify.mjs --estimate-only      # count + token/cost/wall estimate
node $SKILL/scripts/classify.mjs --concurrency 3      # then, once they agree
```

`classify.mjs` drives this call per chat, with `MAX_THINKING_TOKENS=0` (measured: 6.5 s and
$0.007 per call against 44 s and $0.025 with thinking, no loss against the prompt's rules —
the audit stage is what keeps that honest):

```bash
node $SKILL/scripts/digest.mjs --chat <chat-id> \
  | claude -p --model claude-haiku-4-5 \
      --output-format json \
      --system-prompt "$(cat $SKILL/prompts/classify-chat.md)" \
      --tools "" --safe-mode --no-session-persistence \
  | jq -r '.result'
```

Every flag is load-bearing:

- `--tools ""` — no tool loop. It is a classifier, it reads text and returns JSON.
- `--safe-mode` — no CLAUDE.md, skills, hooks, MCP servers. Keeps the classifier
  uncontaminated by project instructions and keeps the prompt prefix stable, so the batch
  gets prompt-cache hits. Auth still works normally (unlike `--bare`).
- `--no-session-persistence` — **critical.** Without it every classification writes a new
  JSONL into `~/.claude*/projects/`, which the next backfill would mine as a chat. The
  ledger would start eating its own tail.
- `--output-format json` returns an envelope; the model's text is `.result`, and it may
  still arrive fenced. Strip ``` fences before parsing. Optionally harden with
  `--json-schema` using the Schema block from the prompt file.

Merge the returned fields into the task row, plus `classified_at` and `classifier_model`.
A task has several chats, so merging has rules:

- **Labels come from the main chat** — the classification that called itself `main`,
  tie-broken by agent-active minutes. Labels do not vote: averaging a bugfix and a refactor
  produces neither.
- **`outcome` is decided by the artifact, not by the classifier.** A task with `commits > 0`
  or a non-empty `prs` is `shipped`, full stop — those fields come from git and `gh` output,
  not from a model reading a truncated digest, and they are exactly the standard *done means
  merged* sets. The classifier keeps only the two verdicts an artifact cannot express:
  `shipped-then-reverted` and `abandoned` (in both, the commit exists *and* something else
  happened). `outcome_source` records `deterministic` or `classifier` and
  `classifier_outcome` keeps the original, so an audit can still score the model.
  This exists because the classifier ran **2.3:1 too pessimistic** — a sonnet audit moved 62
  rows `unknown → shipped` against 27 the other way, all of it the "prefer unknown over a
  guess" rule firing on a digest that simply did not show the commit line.
- **`external_waits` and `user_touchpoint_kinds` are unioned over every chat.** They are a
  quantity and a set, not labels — a wait that happened in chat 3 is still dead time the
  task paid for.
- **Epics stay merged, and keep their detail.** A multi-chat task is one row (splitting it
  is exactly the under-merging that makes a ledger flatter itself), with every chat's own
  labels preserved in a `sub_deliverables[]` array. A single chat that reports several units
  of work contributes several entries too.

**Batch and resume.** Process in batches, write after each, and skip any task that already
has `classified_at`. An interrupted backfill must be resumable by re-running the same
command, not by starting over.

### 5. Audit — is the classifier trustworthy?

Take a **stratified 1-in-5 sample**, oversampling: the biggest tasks, rows with low
`stitch_confidence`, and rows where haiku contradicts the deterministic signals (says
`shipped` with no commit; says `abandoned` with a merged PR).

Re-judge each with sonnet and `prompts/audit-task.md`. `audit.mjs` does the stratification
(the three strata in full, the remainder on a deterministic 1-in-`rate` stride, so a re-run
audits the same rows), feeds the judge the task record plus its chats' digests, and prints
the per-field agreement:

```bash
node $SKILL/scripts/audit.mjs --plan-only     # what would be sampled, and why
node $SKILL/scripts/audit.mjs --rate 5
```

Report the **per-field agreement rate**. If any field agrees **< 80%**, flag that field:
say the prompt needs revision, and mark the field unreliable in `calibration.json` rather
than quietly using it in the feature vector. A classifier nobody checked is not evidence.

Two things to read carefully in that table:

- The rate is reported on the **stride stratum only**. The other three strata are
  deliberately the hardest rows, so their agreement is not a population rate.
- `outcome` is scored on the value the ledger actually holds, which for a row with an
  artifact is the deterministic one. That is the right number for "can I trust this field",
  but it is **not** a measurement of the classifier — `classifier_outcome` is what to score
  the model against.

An auditor correction only counts if the auditor was **entitled to make it**. Three kinds are
inadmissible and `calibrate.mjs` discounts all three from the adjusted rate — which is the
rate `reliable` is decided on, since an inadmissible correction must not be able to condemn
a field. When they are both the majority of the disagreements and at least two in number,
the field is reported `unmeasured` rather than unreliable: that is a defect in
`prompts/audit-task.md`, not in the data, so fix the prompt and re-audit before believing
either number.

- **`off_spec_corrections`** — a value outside the field's own enum. A "correction" in a
  different vocabulary is a different question answered.
- **`corrections_contradicting_deterministic_fields`** — `outcome → unknown` on a row whose
  `commits`/`prs` came out of git. The judge sees at most six truncated digests; the record
  is the census and the digest is a sample, so "I did not see the commit" is not a finding.
- **`self_contradicting_corrections`** — a `false` whose correction repeats the value already
  in the record. It asserts a disagreement and then fails to name one.

**Read the stitch verdict beside the label rates, because it explains most of what is left
of them.** `field_reliability.stitch` reports the verdict distribution and
`over_merged_share`, and every field also carries `agreement_on_well_stitched_rows` — the
same rate over the rows the auditor called `correct`. Measured here: `task_type` agrees
**0.51 on stitch-`correct` rows and 0.00 on the 26% called `over-merged`**. Zero across
fifteen rows is not a coin flip; it is the signature of a question with no answer, because
an over-merged row holds two or more units of work and therefore has no single true
`task_type`. That conditioning is a diagnostic and deliberately does **not** move
`reliable` — the ledger really does hold the bad label on those rows. It tells you what to
fix: the stitch, not the prompt.

### 6. Slice the epics

```bash
node $SKILL/scripts/slice.mjs --min-chats 6        # add --dry-run --json to look first
```

A task with dozens of chats is the right **unit of record** and the wrong unit to quote:
nobody is asked "how long is a 76-hour integration", they are asked "how long is the webhook
part". Splitting the epic into separate task rows is exactly the under-merging that makes a
ledger flatter itself, so the row never moves. Instead `slice.mjs` writes a *view* onto it —
`task.sub_tasks[]` — grouping its chats by **shared PR** first, then by **classifier label
overlap AND time adjacency** (both halves required: the same slug three weeks later is a
regression, not the same slice).

A slice whose member chats all reported **no unit of work** is flagged `no_work` and dropped
from the `epic-slice` quantiles, exactly as a `no_work` task row is dropped from the task
quantiles and for the same reason — it sits at the bottom of every class and answers a
different question. It stays in `sub_tasks`; only the statistics ignore it, and
`excluded_no_work_slices` reports the count.

**Every chat lands in exactly one slice**, so the slices' hours and rounds sum back to the
epic's own. That invariant is what makes a slice quotable rather than an impression. Run
this after `classify.mjs` (it reads `sub_deliverables`) and before `calibrate.mjs`, which
turns the slices into the `epic-slice` reference class.

### 7. Calibrate

```bash
node $SKILL/scripts/calibrate.mjs --ledger $LEDGER/ledger --out $LEDGER/calibration.json
```

**Two kinds of row are excluded from every quantile:** `noise` (permission probes, scratch
QA sessions) and `no_work: true` (the classifier found no unit of work — pure Q&A, a status
check, a session that only read). Both stay in `tasks.ndjson`; only the statistics ignore
them, and `calibration.json` reports the counts in `excluded` so the exclusion is never
invisible.

The `no_work` exclusion reverses an earlier call, on evidence. The old reasoning — "a
question that took two hours of reading cost two hours" — is true about the *hours* and
wrong about the *class*. These rows are 127 of 426 in this ledger, they cluster at the
bottom of every class, and a reference class only forecasts if its members are the same
KIND of thing. Leaving them in answered "how long does a bugfix take" with a distribution
that is 30% "how long does answering a question take". Ask about a question and you get a
question's number; ask about a bugfix and you should not.

Consequence for anything reading `calibration.json`: **`n_tasks` is the quotable count, not
the ledger size.** `n_tasks_in_ledger` is the ledger size.

Then print: per-class `n`, the population priors, which classes are already past the n≥10
gate, and how many rows were excluded. That tells the user which questions the ledger can
actually answer yet.

### 8. Offer the CLAUDE.md hook

Show `templates/claude-md-snippet.md`, show the exact diff, **ask**, and only then append
it to the user's global CLAUDE.md between its `<!-- task-estimator:start -->` markers. If
the markers are already present, replace the block instead of appending a second copy.
Never edit a CLAUDE.md without showing the diff first.

## Mode: record

Runs at the end of a substantive task, either because the user said "record this task" or
because the CLAUDE.md snippet fired.

**Run `record.mjs`. Do not hand-assemble a task row.** Every rule below is already in it,
and the two that are easy to get wrong by hand — rework merging and outcome sourcing — are
exactly the two that make a ledger flatter itself:

```bash
SKILL=.claude/skills/task-estimator
# the session you are in right now:
nice -n 19 ionice -c3 node --max-old-space-size=2048 $SKILL/scripts/record.mjs \
  --session <session-uuid> --project <transcript-dir-name>
# or, when the transcript is simply the newest one in that project:
node $SKILL/scripts/record.mjs --latest --project -path-to-your-project
```

Useful flags: `--dry-run` (print the row, write nothing — **always do this first**),
`--outcome <shipped|shipped-then-reverted|abandoned|superseded|unknown>`, `--in-progress`
(the work is still open; outcome stays `unknown`, sourced honestly), `--estimate-id <id>`
to force the quote it scores against, `--ticket <KEY>` to supply a rework join key the
transcript never named, `--json`, `--no-calibrate`.

What it does, and why each step is not yours to improvise:

1. **Extract + stitch, structurally.** A **resumed** session is the same task continuing,
   not a new one — stitch follows parent edges (first `sessionId` inside a file ≠ its
   filename) and never groups on elapsed time. Do not hand-split a long task by clock. The
   chat is upserted, so re-recording the same session is idempotent: the existing task row
   is *replaced*, never duplicated.
2. **Rework is charged to the original row.** If a task row exists with the same PR or
   ticket and this work lands **within 14 days**, the rows merge and the merged row keeps
   the **original `task_id`**, with the merge recorded in `rework_merges[]`. Costs are
   re-derived from the chats, so files stay a set union and a sha both rows recorded counts
   once. Filing follow-up work as a fresh task is the single most common way a history
   silently reports itself as accurate.
3. **`done` means accepted or merged.** An agent saying "done" overstates completion by
   roughly **7×**. A commit or PR on the row sets `outcome: shipped` with
   `outcome_source: "deterministic"`, and `--outcome` cannot override it — only
   `shipped-then-reverted` and `abandoned` survive an artifact, because those are the two
   verdicts an artifact cannot express. No artifact and no answer is `unknown`, never an
   optimistic default.
4. **Ask only for what cannot be mined**, and ask at most a couple of things:
   - outcome, if there is no merged PR to read it from (`--outcome`);
   - external waits — what was dead time, and roughly how long.
   Everything else (rounds, spans, files touched, repos) comes from the transcript. Do not
   ask the user how long it took; that is exactly the self-report the ledger exists to
   replace.
5. **Scoring is automatic when a quote matches** (`estimate_id` → ticket →
   `task_desc_hash` → slug → summary → sub-deliverable). It writes the ratio and the
   inside-band verdict per axis onto the estimate row, and stamps `estimate_id` onto the
   task row so the link is never re-guessed. **If it reports "no quote matches", say so to
   the user** — that is the loop being open, not a detail. Either the estimate was never
   logged (fix step 8 of estimate mode) or the slug does not match; `--estimate-id` links
   it by hand.
6. **Epics are re-sliced and `calibrate.mjs` re-runs automatically.** One completed task is
   one more point in the class, and the next estimate should already reflect it. Recording a
   chat onto an existing epic also changes that epic's `sub_tasks`, so the slicing is redone
   in the same write — a stale slice list would feed the `epic-slice` class hours that no
   longer match the ledger.

Then read the one-paragraph summary back to the user, including what was **not** measured
(no repo detected, no commits, outcome sourced from them rather than an artifact). Finish
with `score.mjs` whenever a quote was scored, so the quote and its verdict land together.

## Mode: recalibrate

Re-run `stitch.mjs`, then `slice.mjs`, then `calibrate.mjs` over the whole ledger, then
**run `score.mjs`** — it computes every number below and refuses to compute the ones the
ledger has not earned:

```bash
node $SKILL/scripts/slice.mjs --min-chats 6      # refresh the epic sub_deliverables first
node $SKILL/scripts/calibrate.mjs --ledger $LEDGER/ledger --out $LEDGER/calibration.json
node $SKILL/scripts/score.mjs                    # add --json for the machine-readable form
```

Report from its output:

- **Interval coverage** — of the quotes that have actuals, what fraction landed inside the
  quoted P80 band? It should be ~80%. Below that the quotes are too tight; well above, too
  loose. `score.mjs` prints the **binomial acceptance band at the current n** beside it;
  quote that band and never call a miss without it. At n=1 the band is 0–100%.
- **Signed bias** — the median of log(actual / quoted P50), so over- and under-estimation
  do not cancel, reported alongside the **geometric** mean ratio. Never average ratios
  linearly: 4× and 0.25× are the same error in opposite directions, and their arithmetic
  mean (2.1×) invents a bias that is not there.
- **WIS-lite decomposition** at n ≥ 5 — the 80% interval score split into sharpness +
  over-prediction + under-prediction. Read the *shares*: dominated by sharpness means the
  bands are too wide, dominated by under-prediction means the quotes are too low. Below
  n = 5 it is withheld, and "withheld" is the honest report — do not substitute a number.
- **Quotes still awaiting actuals** — every one is a task that finished without record mode
  running. Name them; that is the loop leaking.
- **Per-class n**, and which classes cleared the 5 / 10 / 20 gates since last time.
- Anything that moved: a class that just became quotable, a class whose coverage collapsed.

Recency (90-day half-life) is already inside `calibrate.mjs`. Do not apply a second decay
on top of it.

## Process hygiene — how to run these scripts on a live box

This corpus is hundreds of megabytes of transcripts on a machine that is also serving the
user's own sessions. Every rule here was paid for.

- **NEVER wait on a process with `pgrep`, `pkill -0`, `ps | grep` or any loop built on
  them.** `pgrep -f node`, `pgrep -f backfill` and friends **match the checking process
  itself** — the shell running the check, the subshell, the grep — so the loop observes a
  match forever and never exits. **Two agents deadlocked on exactly this against this
  corpus.** There is no safe flag combination; do not reach for `pgrep -v $$` either.
  - To wait for something you started: run it in the foreground, or capture its **PID** and
    wait on that PID specifically (`wait <pid>` for a child; `kill -0 <pid>` for a one-shot
    liveness check that is *not* in a loop).
  - To coordinate between separate runs: use a **PID file**. `record.mjs` writes
    `$LEDGER/ledger/.record.lock` containing its own pid, refuses **immediately** if a live
    holder exists (it never polls), and takes the lock over when the recorded pid is gone.
    `--force-lock` overrides. A killed run therefore never wedges the ledger, and nothing
    ever scans the process table.
  - A **single, non-looping** `ps` snapshot to answer "is a backfill running right now" is
    fine. It is the loop that kills you, not the tool.
- **`nice -n 19 ionice -c3` on anything that walks the corpus** (`backfill.mjs`,
  `classify.mjs`, `audit.mjs`, `record.mjs` on a large transcript). The user is working on
  this box.
- **Bound the heap: `node --max-old-space-size=2048`.** Individual transcripts reach 140 MB;
  an unbounded run will happily take the machine with it.
- **Never parallelise the extract pass.** Files are processed sequentially, one big
  transcript at a time, on purpose.
- **Scratch goes in `/tmp/claude/task-estimator*/`**, never in a repo and never in the
  ledger. Back the ledger up there before any run that rewrites it.
- **Ledger writes are atomic** (temp file + rename) so a concurrent reader never sees a
  half-written NDJSON. Keep it that way — use `writeNdjsonAtomic` from `lib.mjs`.

## Why these rules

Short version. Sources and full treatment in `references/`.

- **METR RCT 2025** (16 expert devs, 246 real tasks in repos they maintain) — **19% slower**
  with AI while believing they were **20% faster**; a **39-point perception gap that does not
  self-correct with experience**, and it was *largest* for experts in large mature repos —
  exactly the conditions here. This is why self-reports are banned as calibration input and
  why the ledger is mined rather than asked for.
- **Done inflation ~7×** — agent-declared completion overstates real completion on a
  maintainer-review basis, hiding ~26 minutes of remediation per "pass". Done means merged or
  accepted. Nothing else counts.
- **Rounds, not minutes** — measured r ≈ 0.83 between human round count and total duration
  (0.82 in the 651-session corpus; assistant steps score higher still at **0.86**), against
  **r ≈ 0.0** for first-turn duration and only **0.53** for LOC. Per-round agent work is
  stable at ~9s/step and a median turn near 45s; **all the variance lives in the round
  count**.
- **78 / 22 bimodality** — 78% of *high*-complexity tasks finished under 25% of expected
  effort, while 22% of *low*-complexity tasks blew past **180%**, driven by validation and
  integration rather than coding. The joint distribution is bimodal, so a single central
  number sits in the trough. The readiness gate is the cheapest filter on which mode a task
  is in: the blowups correlate with absent or untestable acceptance criteria.
- **Anchoring (Løhre & Jørgensen)** — an irrelevant number moves estimates **4–5×**, survives
  explicit instructions to ignore it, and survives an obviously unqualified source. Hence
  anchor-stripping happens before any reasoning, not as a caveat afterwards. Same-person
  re-estimates of an identical task deviate **71%**, so no remembered estimate is ever data.
- **Reference-class forecasting (Kahneman/Lovallo/Flyvbjerg)** — outside view first, then a
  bounded one-bucket inside-view shift. Software's class base rate is a **73% mean overrun
  with an 18% tail averaging +447%**: fat-tailed, so P85 by default and P95 whenever an
  external dependency is in play.
- **Evidence-Based Scheduling (Spolsky)** — resample whole estimate/actual ratios; never
  average velocity, because averaging deletes exactly the tail draws that produce the
  overruns. Rework is charged back to the original item — filing it separately is how a
  history silently reports itself as accurate.
- **Sample-size gates (Vacanti)** — 5 for a median, ~11 before the observed range means
  anything, 10–20 before publishing an upper limit; 15 fresh points beat 150 stale ones. A
  personal P85 at n=11 spans **0.31–2.26×** the truth, which is why everything below n≈20 is
  shrunk toward the population prior.
- **Empirical quantiles, not fits** — a fitted lognormal lands at **×0.72 of the true median
  and ×1.72 at p95**, while raw empirical quantiles scored leave-one-out coverage of
  **49.9 / 79.8 / 89.9** against nominal 50 / 80 / 90 — essentially exact. Sort the actuals
  and read the quantile off the data, in log space.
- **Only 35% of tasks land within 2× of the median.** At that dispersion a point estimate is
  indefensible; the interval is the answer.
- **The constraint moved downstream** — task throughput +33.7% alongside review time +441%,
  pickup +156%, churn +861%, and **38% of agentic PR failures are "never reviewed"**. An
  estimate that stops at "code written" measures the part that got faster. And with coding
  only ~30–40% of a developer's calendar time, any claimed end-to-end gain above ~40% is a
  measurement error, not a result.
