---
name: debate-protocol
description: Generic 5-phase structured adversarial analysis protocol. Model-agnostic and domain-agnostic. Works for review, audit, research synthesis, planning, creative critique, or any task requiring multi-perspective examination. Can be used standalone or embedded by any orchestrating skill. Produces verdict with confirmed/withdrawn/disputed/merged/discovered findings.
location: managed
allowed-tools:
  - Read
  - Task
  - Write
  - Bash(mkdir *)
---

# Debate Protocol: Generic 5-Phase Adversarial Analysis

Execute this skill to run a structured adversarial analysis among domain experts and structural challengers, producing high-confidence findings through iterative challenge and synthesis.

---

## What Debate Is For

Debate is NOT brainstorming and NOT round-table discussion. Debate is **adversarial validation** — the structured attempt to disprove each finding before accepting it as real.

**The core problem debate solves:** Domain experts find what they're looking for. A security expert finds security issues. A database expert finds schema problems. Left unchallenged, findings accumulate without any filter for whether they're actually real, actually severe, or actually the root cause. Debate applies that filter.

**What debate produces that solo analysis cannot:**
- Findings that survived an attack (higher confidence than ones that weren't challenged)
- Downgraded findings where the initial severity was an assumption, not evidence
- Withdrawn findings that were patterns, not problems
- New findings that only appear when you combine two domain experts' views

### What "Debate" Means Per Task Context

The same 5-phase structure applies to every context. What changes is *what each participant is looking for* and *what counts as a valid challenge*:

**Code / Technical Review:**
- Domain experts analyze: correctness, safety, performance, maintainability
- DA challenges: "Is this finding a real bug or just a style preference? What production scenario triggers it? Has the codebase already handled it somewhere else?"
- IC checks: "If this bug exists in module A, does module B's error handling assume it can't happen?"
- Valid challenge: "This SQL injection claim assumes the ORM doesn't sanitize inputs — it does at the call site in auth_middleware.go"

**Security Audit:**
- Domain experts analyze: threat vectors, attack surface, data exposure, access controls
- DA challenges: "Is this exploitable in practice given the deployment context? Does the attacker need prior access that narrows the risk?"
- IC checks: "Does this authentication gap in the API also affect the admin panel that shares the same session store?"
- Valid challenge: "CRITICAL classification assumes external attacker access — this endpoint is only reachable from the private VPC"

**Architecture / Planning:**
- Domain experts analyze: feasibility, scalability assumptions, dependency risks, sequencing
- DA challenges: "What assumption does this plan depend on that hasn't been validated? What's the failure mode if the third-party API changes its contract?"
- IC checks: "Does the proposed event-sourcing approach in service A create a schema coupling problem with service B's projection?"
- Valid challenge: "This plan assumes linear traffic growth — if traffic spikes 10x on launch day, step 3 blocks everything"

**Research Synthesis:**
- Domain experts analyze: source credibility, evidence quality, conclusion validity
- DA challenges: "Does this conclusion follow from the cited sources, or is there a logical gap? Are the sources independent, or do they all cite the same original study?"
- IC checks: "Does finding X from the technology domain contradict finding Y from the business domain in a way neither domain's report acknowledged?"
- Valid challenge: "The cited study had n=47 and no control group — the confidence should be LOW, not STRONG"

**Creative / UX / Content:**
- Domain experts analyze: clarity, consistency, user task completion, brand alignment
- DA challenges: "Does this UX issue reflect the actual user population or just power users? Would the proposed fix create a different problem for a different segment?"
- IC checks: "Does the navigation change proposed by the UX expert break the content structure the content expert assumed?"
- Valid challenge: "The 'confusing label' finding is based on one user test — the current label tests well with users who read the tooltip"

---

## What Makes a Valid Challenge vs Invalid

**A valid challenge MUST do ONE of:**
1. **Identify a missing assumption** — "This finding assumes X. X is not true because Y."
2. **Propose an alternative explanation** — "The symptom you found has a different cause: Z. If Z is the cause, the severity changes."
3. **Surface a non-applicability scenario** — "This finding doesn't apply when condition W is true. W is true in this codebase/plan/system because..."

**An invalid challenge:**
- "I don't think this is a big deal" — no mechanism identified
- "This might not be an issue" — no reason given
- "Other systems handle this fine" — comparison without applicable context
- Restating the finding differently without attacking it

**The key test for DA:** If your challenge doesn't include a specific reason the finding is wrong, weaker than stated, or inapplicable — it's not a challenge, it's an opinion.

---

## Execution Instructions

When invoked, accept the following input (from conversation context or caller):

```yaml
debate_input:
  review_id: ""          # Unique ID for this debate session (generate UUID if not provided)
  review_scope: ""       # What is being reviewed (files, topics, description)
  domains: []            # Domains selected (from domain-registry or caller)
  intensity: "standard"  # quick | standard | thorough
  context_summary: ""    # What the conversation/task is about
```

---

## Intensity Modes

```yaml
quick:
  phases: [1, 2, 5]      # Skip challenge and synthesis
  max_rounds: 0
  budget: "reviewer_count + 5 tasks"

standard:
  phases: [1, 2, 3, 4, 5]  # All phases
  max_rounds: 3
  budget: "3 * reviewer_count + 10 tasks"

thorough:
  phases: [1, 2, 3, 4, 5]  # All phases, extended
  max_rounds: 5
  budget: "5 * reviewer_count + 10 tasks"
```

---

## Parameter Presets

```yaml
default:
  da_weight: 0.40           # Devil's Advocate finding weight
  consensus_threshold: 0.50  # Fraction needed for "confirmed"
  security_threshold: 0.67   # Higher bar for security findings

security-elevated:
  da_weight: 0.50
  consensus_threshold: 0.67
  security_threshold: 0.75
```

---

## Phase 1: Independent Investigation (Parallel)

**Rationale:** Isolation prevents anchoring bias. If experts see each other's findings first, they pattern-match and corroborate rather than independently discover. Phase 1 ensures each participant forms their view from the evidence alone — not from social agreement with the first finding published.

Spawn all participants in parallel using Task tool. Each receives the same `scope` and `context_summary` but NO communication with other participants.

### Participant Roster

| Role | Count | Source |
|------|-------|--------|
| Domain expert | One per domain in `debate_input.domains` | domain-registry Lookup Protocol — exact match, adapted match, or session-based virtual expert |
| Devil's Advocate | 1 (always) | `debate-protocol/experts/devils-advocate.md` |
| Integration Checker | 1 (always) | `debate-protocol/experts/integration-checker.md` |

Domain experts are the primary roster. DA and Integration Checker are structural roles that always accompany them.

### Task Prompt Template

```
You are a {expert_role}.

Task: {context_summary}
Scope: {scope}
Domains in scope: {domains}

## Phase 1: Independent Investigation

Analyze independently. Do NOT coordinate with other participants.

Focus areas: {focus_areas}
Standards: {standards}

## Output Format (JSON)

{
  "participant": "{role-name}",
  "findings": [
    {
      "id": "F001",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO",
      "title": "Short finding title",
      "description": "Detailed description",
      "evidence": "Specific evidence or reference",
      "recommendation": "What to do about it",
      "domains": ["{domain}"]
    }
  ],
  "phase": 1
}
```

For Devil's Advocate and Integration Checker: apply the role-specific instructions from their expert files.

---

## Phase 2: Finding Publication

**Rationale:** DA cannot challenge what it hasn't seen. Publishing all findings at once (rather than letting DA see them one-by-one) lets DA identify cross-domain patterns and spot findings that look independent but share the same root assumption. Publication is read-only — no responses yet, no anchoring on first reactions.

Collect all Phase 1 findings. As coordinator:

1. Assign unique IDs to all findings (F001, F002, ...)
2. Broadcast complete finding list to all participants
3. No responses yet — publication only

Finding inventory at this point:
```yaml
all_findings:
  - id: F001
    origin: devil-advocate
    severity: HIGH
    title: "..."
    ...
```

---

## Phase 3: Challenge Round (standard + thorough only)

**Rationale:** Domain experts are motivated to defend their findings — they found them, they believe them. DA's adversarial role exists precisely because no expert naturally looks for reasons their own finding is wrong. The challenge round is the mechanism that separates real findings (survive attack) from inflated or pattern-matched ones (fail under scrutiny). Multi-round structure catches second-order effects: a DA challenge may spawn a discovery, which then needs its own challenge.

Run challenge rounds up to `max_rounds`. Each round:

### Devil's Advocate Obligations

**MUST challenge** every CRITICAL/HIGH finding not originated by DA.
**SHOULD challenge** MEDIUM findings when pattern detected.
**Cross-domain synthesis** — DA discovers new findings from cross-domain patterns.

### Challenge Message Format

Send via Task agent communication (embed in follow-up Task prompts):

```json
{
  "type": "challenge",
  "from": "devil-advocate",
  "to": "target-reviewer",
  "finding_id": "F002",
  "challenge": "This assumes X, but what if Y?",
  "severity_challenge": "MEDIUM not HIGH because..."
}
```

### Response Types

- **defense**: Reviewer defends finding with additional evidence
- **withdrawal**: Reviewer withdraws finding (insufficient evidence)
- **corroboration**: Another reviewer confirms the finding
- **cross-challenge**: Reviewer challenges a different finding
- **discovery**: New finding discovered during debate
- **merge-proposal**: Two similar findings proposed for merging

### Challenge Loop

Repeat for up to `max_rounds` rounds:
1. Spawn DA Task agent with all current findings + challenge obligations
2. Spawn all other participants with challenges directed at them
3. Collect responses
4. Update finding states

---

## Phase 4: Synthesis (standard + thorough only)

**Rationale:** Multiple domain experts often find the same root issue from different angles (a missing input validation shows up in security, API, and testing domains independently). Without synthesis, the final report over-counts the same problem. Merging also reveals when "two issues" are actually one issue that's been inflated by being described separately — or genuinely different issues that need separate remediation.

Identify merge opportunities:
- Findings with >70% description overlap → propose merge
- Merged findings inherit highest severity
- Both origin reviewers must agree to merge

Update finding states:
- `confirmed` — defended and/or corroborated by ≥ consensus_threshold of reviewers
- `withdrawn` — reviewer withdrew after challenge
- `disputed` — challenged but not resolved
- `merged` — two findings consolidated
- `discovered` — emerged during challenge rounds

---

## Phase 5: Final Verdict

**Rationale:** Requiring all participants to submit a final position catches dissent that didn't surface during challenge rounds. A participant who was challenged and defended their finding may still have a different severity than others. Final positions reveal whether the session reached genuine consensus or just an uneasy truce. Dissent recorded here becomes the `disputed_findings` that callers can inspect.

All participants submit final positions.

### Verdict Logic

```yaml
FAIL:
  - Any CRITICAL confirmed finding
  - 3+ HIGH confirmed findings
  - Any confirmed security finding with domain security-elevated preset

CONCERNS:
  - 1-2 HIGH confirmed findings
  - Multiple MEDIUM confirmed findings
  - Any disputed CRITICAL/HIGH finding

PASS:
  - No confirmed CRITICAL/HIGH findings
  - Only confirmed MEDIUM/LOW/INFO
```

---

## Fallback Mode

If TeamCreate fails (not available in context):
- Spawn independent Task sub-agents (no debate, no cross-challenge)
- Collect findings independently
- Skip Phases 3 and 4
- Run Phase 5 synthesis directly
- Mark output with `"type": "debate-protocol-fallback"`

---

## Artifact Output

Save to `.outputs/debate/{YYYYMMDD-HHMMSS}-debate-{review_id}.md` with YAML frontmatter:

```yaml
---
skill: debate-protocol
timestamp: {ISO-8601}
artifact_type: debate
domains: [{domain1}, {domain2}]
verdict: PASS | FAIL | CONCERNS
intensity: quick | standard | thorough
review_id: "{unique id}"
context_summary: "{brief description of the task}"
---
```

Also save JSON companion: `{YYYYMMDD-HHMMSS}-debate-{review_id}.json`

**No symlinks.** To find the latest artifact:
```bash
ls -t .outputs/debate/ | head -1
```

**QMD Integration (optional):**
```bash
qmd collection add .outputs/debate/ --name "debate-artifacts" --mask "**/*.md" 2>/dev/null || true
qmd update 2>/dev/null || true
```
