---
name: hackathon-risk-analyzer
description: >-
  Detect technical and demo risks that may cause a hackathon project to fail, and generate severity-ranked mitigations.
---
# hackathon-risk-analyzer

## Goal
Identify and rank technical, integration, and demo risks that could cause the project to fail during development or live judging, and produce actionable mitigation strategies for each risk before implementation begins.

---

## Trigger Conditions

Use this skill when:
- MVP scope is locked and the tech stack is confirmed
- The team is about to begin implementation and risk exposure is unknown
- External APIs, datasets, GPU resources, or network dependencies are involved
- A deployment environment is being used for the first time by the team
- Invoked during Phase 4 (Project Planning), after `hackathon-scope-cutter` and before the first `hackathon-code-implementer` call; re-invoke if scope or tech stack changes

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `project_title` | string | Yes | Name of the project |
| `tech_stack` | string[] | Yes | Technologies in use |
| `mvp_features` | object[] | Yes | MVP features from `hackathon-scope-cutter` |
| `external_dependencies` | string[] | Yes | External APIs, services, datasets, or hardware required |
| `hackathon_duration_hours` | integer | Yes | Total hours remaining |
| `team_skills` | string[] | No | Team's proficiency areas (used to flag skill gaps) |
| `demo_environment` | string | No | Where the demo runs (e.g., local, Vercel, Render, browser) |

---

## Outputs

| Output | Description |
|---|---|
| `risks` | Full list of identified risks with severity, category, and mitigation |
| `critical_risks` | Subset of risks rated `critical` that must be resolved before coding |
| `risk_summary` | Aggregate risk score and overall project risk level |
| `pre_build_actions` | Actions to take immediately before starting implementation |
| `recommended_skills` | Suggested next skills to invoke |

---

## Rules

1. Classify every risk into one of: `api`, `data`, `infra`, `skill-gap`, `demo`, `time`.
2. Assign severity using: `critical` (blocks demo), `high` (likely to cause delay), `medium` (manageable), `low` (acceptable).
3. Every `critical` or `high` risk must have a concrete mitigation strategy and a fallback plan.
4. Flag any external dependency without a free tier or offline fallback as `critical`.
5. Flag any feature requiring GPU, specialized hardware, or proprietary datasets as `high` or `critical`.
6. `pre_build_actions` must address all `critical` risks before coding begins.
7. Do not invent risks; base all risks on `tech_stack`, `external_dependencies`, and `mvp_features`.

---

## Output Format

```yaml
risks:
  - id: "R-<number>"
    title: "<short risk title>"
    category: "<api|data|infra|skill-gap|demo|time>"
    severity: "<critical|high|medium|low>"
    description: "<what can go wrong>"
    probability: "<high|medium|low>"
    impact: "<what breaks if this occurs>"
    mitigation: "<how to prevent or reduce>"
    fallback: "<what to do if it happens anyway>"

critical_risks:
  - id: "R-<number>"
    title: "<title>"
    blocking_feature: "<which MVP feature this blocks>"

risk_summary:
  total_risks: <number>
  critical: <number>
  high: <number>
  medium: <number>
  low: <number>
  overall_level: "<red|amber|green>"
  assessment: "<one-sentence summary>"

pre_build_actions:
  - priority: <number>
    action: "<what to do>"
    risk_addressed: "R-<number>"
    estimated_minutes: <number>

recommended_skills:
  - "<skill-name>"
```

---

## Example

**Input:**
```yaml
project_title: "AnchorAI"
tech_stack: ["Python", "FastAPI", "React", "Groq API", "Supabase"]
mvp_features:
  - feature: "GPT-4 emotional check-in conversation"
    fake_ok: false
  - feature: "Session memory"
    fake_ok: false
  - feature: "Crisis escalation (mocked)"
    fake_ok: true
external_dependencies:
  - "Groq API (LLM inference)"
  - "Supabase (database)"
hackathon_duration_hours: 24
team_skills: ["Python", "FastAPI", "React"]
demo_environment: "local + Vercel frontend"
```

**Output:**
```yaml
risks:
  - id: "R-01"
    title: "Groq API rate limit hit during live demo"
    category: "api"
    severity: "critical"
    description: "Free tier Groq API has rate limits that can be exhausted under rapid demo usage"
    probability: "medium"
    impact: "Core chat feature fails live during judging"
    mitigation: "Use a dedicated API key with higher rate limits; implement exponential backoff"
    fallback: "Pre-record the memory recall exchange; play as screen capture if API fails"

  - id: "R-02"
    title: "Supabase cold start delays first DB query"
    category: "infra"
    severity: "high"
    description: "Supabase free tier instances sleep after inactivity; first query can take 3–10 seconds"
    probability: "high"
    impact: "Demo appears broken for first 10 seconds; undermines confidence"
    mitigation: "Warm up Supabase with a ping request at demo start; add a visible loading indicator"
    fallback: "Fall back to in-memory dict for demo session if Supabase is unresponsive"

  - id: "R-03"
    title: "Team unfamiliar with Supabase client library"
    category: "skill-gap"
    severity: "medium"
    description: "Team lists Python/FastAPI skills but not Supabase; integration may take longer than estimated"
    probability: "medium"
    impact: "Session memory feature delayed by 2–4 hours"
    mitigation: "Assign Supabase integration to most experienced backend developer; use official Supabase Python SDK examples"
    fallback: "Replace Supabase with Redis for demo; migrate after hackathon"

  - id: "R-04"
    title: "Context window overflow with long session summaries"
    category: "api"
    severity: "medium"
    description: "Injecting long memory summaries into the system prompt may exceed model context limits"
    probability: "medium"
    impact: "API returns error; chat feature breaks mid-demo"
    mitigation: "Hard-cap session summary at 150 tokens before injection"
    fallback: "Truncate summary silently; log warning"

critical_risks:
  - id: "R-01"
    title: "Groq API rate limit hit during live demo"
    blocking_feature: "GPT-4 emotional check-in conversation"

risk_summary:
  total_risks: 4
  critical: 1
  high: 1
  medium: 2
  low: 0
  overall_level: "amber"
  assessment: "Project is buildable but requires API key upgrade and Supabase warm-up strategy before demo."

pre_build_actions:
  - priority: 1
    action: "Upgrade Groq API key to a plan with higher rate limits and test with 10 rapid requests"
    risk_addressed: "R-01"
    estimated_minutes: 15
  - priority: 2
    action: "Add a /health endpoint that warms Supabase on backend startup; test cold-start behavior"
    risk_addressed: "R-02"
    estimated_minutes: 20
  - priority: 3
    action: "Run Supabase Python SDK quickstart tutorial to confirm team can read/write successfully"
    risk_addressed: "R-03"
    estimated_minutes: 30

recommended_skills:
  - "hackathon-repo-bootstrap"
  - "hackathon-code-implementer"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-common-failures.md`
- `knowledge/hackathon-reference-architecture.md`
- `knowledge/hackathon-tools.md`
- `knowledge/hackathon-mvp-strategy.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
- `playbooks/24h-hackathon-playbook.md`
- `playbooks/36h-hackathon-playbook.md`
- `playbooks/48h-hackathon-playbook.md`
