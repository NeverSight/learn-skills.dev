---
name: falsify
description: Adversarial falsification of sigint research findings. Generates disconfirming queries, executes web-only adversarial search, assigns ordinal verdicts (falsified | weakened | survived | inconclusive), and applies remediation (quarantine, confidence downgrade, follow-up queue). Invocable standalone via `/sigint:falsify` or as Phase 3.6 gate inside the research-orchestrator before report finalization. Use when the user invokes /sigint:falsify.
argument-hint: "[--scope all|dimension:<dim>|finding:<id>] [--query-budget <n>] [--claim-budget <n>] [--mode block|advisory]"
allowed-tools:
  - Agent
  - AskUserQuestion
  - Bash
  - Glob
  - Grep
  - Read
  - SendMessage
  - TaskCreate
  - TaskGet
  - TaskList
  - TaskUpdate
  - TeamCreate
  - TeamDelete
  - Write
---

# Sigint Falsify Skill (Adversarial Assessment + Remediation)

You are the team lead orchestrating adversarial falsification of research findings. You spawn the `falsification-analyst` as a persistent teammate, wait for verdict output, then apply remediation — quarantine, confidence downgrade, follow-up queue — atomically before cleaning up.

## MANDATORY SWARM ORCHESTRATION

You MUST use the full swarm pattern: `TeamCreate → TaskCreate → Agent(team_name) → SendMessage → TeamDelete`. Do NOT spawn standalone agents.

**Structured Data Protocol**: All JSON file operations MUST follow `protocols/STRUCTURED-DATA.md`. Use `jq` for I/O and validate every write with the corresponding `schemas/*.jq` file.

**One-Round Rule**: A finding that already carries `provenance.falsification_attempts` from the current session is skipped. Do not falsify falsifications.

---

## Phase 0: Parse Arguments and Initialize

### Step 0.1: Parse Arguments

**Input sanitization**: truncate `$ARGUMENTS` to 200 characters total, strip backticks and angle brackets.

- `--scope` → default `all`. Valid: `all`, `dimension:<dim>` (where `<dim>` is one of competitive|sizing|trends|customer|tech|financial|regulatory|trend_modeling), `finding:<id>` (where `<id>` matches `f_[a-z_]+_[0-9]+`). Invalid → error and stop.
- `--query-budget` → default 6. Integer 1–10. Out of range → clamp and warn.
- `--claim-budget` → default 50. Integer 1–500. Out of range → clamp and warn.
- `--mode` → default `block`. One of `block` (any `falsified` verdict halts downstream phases) or `advisory` (all verdicts are annotation only). Invalid → error and stop.

### Step 0.2: Find Active Research Session

Scan `./reports/*/state.json` for sessions with `status` in `{"active", "complete"}`. Pick most recently updated. Extract `topic`, `topic_slug`, `elicitation`.

If no session found, error: `"No research session found. Run /sigint:start <topic> first."`

**Resolve `reports_dir` from config** (REQUIRED — do not hardcode paths):

```bash
REPORTS_DIR=$(jq -r --arg slug "$TOPIC_SLUG" '.topics[$slug].reports_dir // "./reports/\($slug)"' sigint.config.json 2>/dev/null || echo "./reports/$TOPIC_SLUG")
```

All subsequent paths use `{reports_dir}`.

### Step 0.3: Validate Working Set Size

Compute claims-to-evaluate based on `--scope`:

```bash
case "$SCOPE" in
  all) COUNT=$(jq '[.findings[]] | length' "$REPORTS_DIR/state.json") ;;
  dimension:*) DIM="${SCOPE#dimension:}"; COUNT=$(jq --arg d "$DIM" '[.findings[] | select(.dimension == $d)] | length' "$REPORTS_DIR/state.json") ;;
  finding:*) COUNT=1 ;;
esac
```

If `COUNT > CLAIM_BUDGET`, halt and present:

```
AskUserQuestion(
  question: "Working set has {COUNT} findings; claim budget is {CLAIM_BUDGET}. Each finding produces 1–3 atomic claims. Estimated upper-bound claims: {COUNT*3}. Proceed?",
  options: ["Increase claim budget to {COUNT*3}", "Narrow scope", "Cancel"]
)
```

Do NOT silently truncate.

### Step 0.4: Initialize Swarm

```
TeamCreate(name: "sigint-{topic_slug}-falsify")

TaskCreate({
  subject: "Falsify findings: scope={scope}, budget={query_budget}q × {claim_budget}c",
  owner: "falsification-analyst",
  description: "Adversarial falsification of research findings"
})
```

Note returned task ID as `{falsifyTaskId}`.

---

## Phase 1: Spawn Falsification-Analyst

```
Agent(
  subagent_type: "sigint:falsification-analyst",
  team_name: "sigint-{topic_slug}-falsify",
  name: "falsification-analyst",
  run_in_background: true,
  prompt: """
    Task Discovery Protocol:
    1. TaskList → find tasks assigned to you (owner: "falsification-analyst")
    2. TaskGet → read full task description
    3. Work on the task following your agent definition (Steps 1–8)
    4. When done:
       a. TaskUpdate(taskId, status: "completed")
       b. SendMessage(to: "team-lead", message: {...}, summary: "Falsification complete: ...")
    5. NEVER commit via git
    6. Use ONLY WebSearch/WebFetch for evidence — no internal memory, no prior findings as evidence

    PARAMETERS:
    - TOPIC_SLUG: {topic_slug}
    - REPORTS_DIR: {reports_dir}
    - SCOPE: {scope}
    - QUERY_BUDGET: {query_budget}
    - CLAIM_BUDGET: {claim_budget}
    - taskId: {falsifyTaskId}

    Follow your agent definition Steps 1–8. Output files (date = today UTC, ISO YYYY-MM-DD):
    - {reports_dir}/falsification_attempts_{scope_tag}.json
    - {reports_dir}/YYYY-MM-DD-falsification-report.json (validates schemas/falsification-report.jq)
    - {reports_dir}/YYYY-MM-DD-falsification-report.md
  """
)

SendMessage(
  to: "falsification-analyst",
  message: "Task #{falsifyTaskId} assigned. Start now.",
  summary: "Falsification task assigned"
)
```

---

## Phase 2: Receive Verdicts

Wait for SendMessage from `falsification-analyst` containing:

- `files` — list of generated file paths
- `verdicts` — `{falsified, weakened, survived, inconclusive}` counts
- `blocking` — boolean (true if any `falsified`)
- `remediation_queue_size` — int

**Timeout**: If no response within 240 seconds (web search is slow), send a status check. After an additional 120 seconds with no response, surface partial output and abort with cleanup.

Validate each reported file exists. If the report JSON is missing, abort and inform the user.

---

## Phase 3: Apply Remediation (Mandatory)

Adversarial assessment without remediation is out of scope. For every `falsified` and `weakened` claim, apply concrete corrective actions to the active session state.

### Step 3.1: Load the Falsification Report

```bash
REPORT="$REPORTS_DIR/$(date -u +%Y-%m-%d)-falsification-report.json"
ATTEMPTS="$REPORTS_DIR/falsification_attempts_${SCOPE_TAG}.json"
```

### Step 3.2: Merge `falsification_attempts` into `state.json` Findings

For every finding referenced in the attempts file, patch its `provenance.falsification_attempts` array (append, do not replace prior rounds):

```bash
jq --slurpfile attempts "$ATTEMPTS" '
  .findings |= map(
    . as $f |
    ($attempts[0].claims | map(select(.claim_id | startswith($f.id + "_c")))) as $matched |
    if ($matched | length) > 0 then
      .provenance.falsification_attempts = ((.provenance.falsification_attempts // []) + [{
        attempted_at: $attempts[0].attempted_at,
        scope: $attempts[0].scope,
        claims: $matched
      }])
    else . end
  )
' "$REPORTS_DIR/state.json" > tmp.$$ && mv tmp.$$ "$REPORTS_DIR/state.json"
jq -e -f schemas/state.jq "$REPORTS_DIR/state.json" > /dev/null
```

### Step 3.3: Apply Verdict Actions per Finding

For each finding in `report.by_finding`, take action based on `worst_verdict`:

#### `falsified` → quarantine

1. Remove finding from active `findings[]` in state.json.
2. Append to `quarantine.json` with `gate: "post-falsification"`:

```bash
QUARANTINE_ITEM=$(jq -n \
  --arg fid "$FINDING_ID" \
  --arg dim "$DIMENSION" \
  --arg reason "$VERDICT_BASIS" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson original "$ORIGINAL_FINDING" \
  '{finding_id: $fid, original_dimension: $dim, reason: $reason, gate: "post-falsification", gate_timestamp: $ts, original_finding: $original}')

if [ -f "$REPORTS_DIR/quarantine.json" ]; then
  jq --argjson item "$QUARANTINE_ITEM" '.items += [$item]' \
    "$REPORTS_DIR/quarantine.json" > tmp.$$ && mv tmp.$$ "$REPORTS_DIR/quarantine.json"
else
  jq -n --arg date "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --argjson item "$QUARANTINE_ITEM" \
    '{quarantined_at: $date, items: [$item]}' > "$REPORTS_DIR/quarantine.json"
fi
jq -e -f schemas/quarantine.jq "$REPORTS_DIR/quarantine.json" > /dev/null
```

#### `weakened` → narrow + downgrade confidence

1. Append disconfirming sources to the finding's `provenance.sources` (mark `relation` in source object, set `alive: true`).
2. Downgrade confidence one level: `high → medium`, `medium → low`, `low → quarantine` (treat as falsified).
3. Narrow `summary` text by appending a qualifier: `" — qualified by disconfirming evidence (see falsification report)."` Do NOT rewrite the original claim.
4. Set `requires_issue_followup: true` when the original finding had high impact: original `confidence == "high"` OR `market_dynamic` is set. These are the findings whose weakening most likely affects downstream recommendations.

```bash
# $ORIGINAL_CONF = the finding's confidence BEFORE downgrade (read prior to mutation)
# $HAS_MARKET_DYNAMIC = "true" if .market_dynamic is non-null/non-empty, else "false"
jq --arg fid "$FINDING_ID" \
   --argjson new_sources "$DISCONFIRMING_SOURCES_JSON" \
   --arg new_conf "$DOWNGRADED" \
   --arg orig_conf "$ORIGINAL_CONF" \
   --argjson has_md "$HAS_MARKET_DYNAMIC" \
   '.findings |= map(
     if .id == $fid then
       .provenance.sources = (.provenance.sources + $new_sources) |
       .confidence = $new_conf |
       .summary = (.summary + " — qualified by disconfirming evidence (see falsification report).") |
       .requires_issue_followup = (($orig_conf == "high") or $has_md)
     else . end
   )' "$REPORTS_DIR/state.json" > tmp.$$ && mv tmp.$$ "$REPORTS_DIR/state.json"
jq -e -f schemas/state.jq "$REPORTS_DIR/state.json" > /dev/null
```

#### `survived` (with upgrade signal) → optional confidence upgrade

If `confidence_delta == "upgrade_one_level"` AND ≥2 queries returned credible non-disconfirming results: upgrade confidence one level (`low → medium`, `medium → high`). Otherwise leave unchanged. Annotate `falsification_attempts` only.

#### `inconclusive` → annotate only

No state change beyond the `falsification_attempts` annotation already merged in Step 3.2.

### Step 3.4: Build Follow-up Queue

Write `$REPORTS_DIR/$(date -u +%Y-%m-%d)-falsification-followups.json` (date-prefixed to avoid clobbering when the gate runs more than once per session — e.g., during `/sigint:augment` after an initial run). Listing findings that need new or updated GitHub issues:

```json
{
  "generated_at": "{ISO_DATE}",
  "items": [
    {"finding_id": "...", "action": "open_issue", "reason": "Falsified — original recommendation no longer supported. Open retraction issue.", "disconfirming_sources": ["url1"]},
    {"finding_id": "...", "action": "comment_issue", "reason": "Weakened — comment on existing issue with new evidence.", "disconfirming_sources": ["url2"]}
  ]
}
```

The next `/sigint:issues` invocation reads this file (alongside `state.findings`) to decide which issues to open or comment on. **Do not invoke `/sigint:issues` from within this skill** — orchestration coupling will break on retries.

Validate against `schemas/falsification-followups.jq`:

```bash
jq -e -f schemas/falsification-followups.jq "$REPORTS_DIR/$(date -u +%Y-%m-%d)-falsification-followups.json" > /dev/null
```

### Step 3.5: Append Lineage Entry

```bash
DIMENSIONS_JSON=$(jq -c '[.findings[].dimension] | unique' "$REPORTS_DIR/state.json")
FINDING_COUNT=$(jq '.findings | length' "$REPORTS_DIR/state.json")

LINEAGE=$(jq -n \
  --arg session "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg scope "$SCOPE" \
  --argjson dims "$DIMENSIONS_JSON" \
  --argjson count "$FINDING_COUNT" \
  --argjson verdicts "$VERDICTS_JSON" \
  --argjson falsified "$FALSIFIED_COUNT" \
  --argjson weakened "$WEAKENED_COUNT" \
  '{session_id: $session, action: "falsification", dimensions: $dims, finding_count: $count, scope: $scope, verdicts: $verdicts, falsified_count: $falsified, weakened_count: $weakened}')

jq --argjson entry "$LINEAGE" '.lineage += [$entry] | .last_updated = "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"' \
  "$REPORTS_DIR/state.json" > tmp.$$ && mv tmp.$$ "$REPORTS_DIR/state.json"
jq -e -f schemas/state.jq "$REPORTS_DIR/state.json" > /dev/null
```

### Step 3.6: Append to Research Progress

Append to `$REPORTS_DIR/research-progress.md`:

```markdown
## {ISO_DATE} — Falsification Gate
- Scope: {scope}
- Claims evaluated: {N}
- Queries executed: {N} (budget: {QUERY_BUDGET}/claim)
- Verdicts: falsified={N}, weakened={N}, survived={N}, inconclusive={N}
- Remediation: {N} quarantined, {N} downgraded, {N} annotated
- Mode: {block|advisory}
- Gate state: {pass|fail}
- Followups queued: {N} (see falsification-followups.json)
- Epistemic caveat: survived = {N} queries/claim adversarially executed without disconfirmation; not a proof of truth.
```

---

## Phase 4: Gate Decision

If `--mode = block` AND `verdicts.falsified > 0`:

- Set gate state to `fail`
- Surface a blocking message:

```
Falsification gate FAILED.

{N} finding(s) were falsified. Quarantined entries:
  - {finding_id}: {one-line basis}
  ...

Downstream phases (report generation, issue creation) should not proceed
until the underlying research is updated. Recommended next step:
  /sigint:augment {affected_dimension} — re-research with adversarial findings in mind.

Falsification report: {report.md}
Quarantined items: {quarantine.json}
```

If `--mode = advisory` OR no `falsified` verdicts:

- Set gate state to `pass`
- Present summary:

```
Falsification gate PASSED ({mode}).

Verdicts: falsified={N}, weakened={N}, survived={N}, inconclusive={N}
Remediation applied: {N} quarantined, {N} downgraded, {N} annotated.

Files:
  - {report.md}
  - {report.json}
  - {falsification-followups.json}
  ({N} items queued for /sigint:issues)

Next steps:
  - /sigint:report — generate report (falsification verdicts are now reflected in state.json)
  - /sigint:issues — apply followup queue
```

---

## Phase 5: Cleanup

Always run cleanup, even on errors in earlier phases:

```
SendMessage(to: "falsification-analyst", message: {type: "shutdown_request", reason: "Falsification complete"})
TeamDelete("sigint-{topic_slug}-falsify")
```

If TeamDelete fails (already cleaned up), log silently — the verdicts and remediation are already persisted.

---

## Integration Notes

- **Orchestrator gate**: `agents/research-orchestrator.md` invokes this skill as Phase 3.6 between post-merge codex review and progress rendering. The orchestrator passes `--mode block` by default; users can override via `/sigint:falsify --mode advisory` for standalone runs.
- **Issue followups**: `/sigint:issues` reads `falsification-followups.json` if present and processes alongside `state.findings`. The `requires_issue_followup` flag on findings supplements the followups file.
- **Report integration**: `/sigint:report` reads `provenance.falsification_attempts` and the latest `*-falsification-report.json` to surface verdict roll-ups in an "Adversarial Assessment" section.
- **Codex review compatibility**: Falsification answers a different question than codex review (codex: are sources real?; falsify: are claims defeasible?). Both gates coexist — falsification runs after codex review.
