---
name: hackathon-submission-prep
description: >-
  Compile and validate all hackathon submission artifacts into a complete, polished package ready for platform upload.
---
# hackathon-submission-prep

## Goal
Compile and validate all required hackathon submission artifacts into a complete, polished submission package ready for upload.

---

## Trigger Conditions

Use this skill when:
- The demo video is uploaded and the pitch deck is finalized
- Submission deadline is approaching and artifacts must be validated
- A submission platform (Devpost, Dorahacks, etc.) requires a structured description
- The team needs a checklist of what is complete versus what is still missing
- Invoked during Phase 8; submit output to the platform at least 1 hour before the deadline

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `project_title` | string | Yes | Name of the project |
| `tagline` | string | Yes | One-sentence description |
| `problem_statement` | string | Yes | The problem being solved |
| `solution_summary` | string | Yes | How the project solves it |
| `tech_stack` | string[] | Yes | Technologies used |
| `team_members` | object[] | Yes | Team member names and roles |
| `demo_url` | string | No | Live demo URL |
| `video_url` | string | No | Demo video URL |
| `repo_url` | string | Yes | Source code repository URL |
| `track` | string | Yes | Hackathon track being entered |
| `submission_platform` | string | No | Platform name (e.g., Devpost, Dorahacks) |
| `custom_fields` | object[] | No | Platform-specific required fields |

---

## Outputs

| Output | Description |
|---|---|
| `submission_description` | Full formatted project description for submission |
| `short_description` | 280-character tagline/elevator pitch |
| `artifact_checklist` | All required submission items with completion status |
| `missing_artifacts` | Items not yet provided that must be completed |
| `submission_quality_score` | 1–10 rating of submission readiness |
| `last_mile_actions` | Final actions required before submitting |

---

## Rules

1. `submission_description` must include: problem, solution, tech stack, team, and demo link.
2. `short_description` must be 280 characters or fewer.
3. `artifact_checklist` must verify: repo URL accessible, README exists, demo video linked, team listed.
4. Assign `submission_quality_score` using: completeness (40%), clarity (30%), impact framing (30%).
5. `last_mile_actions` must be ordered by priority with estimated time per action.
6. Flag any missing required field from `custom_fields` as a blocking `missing_artifact`.
7. Do not submit placeholder text; flag any `[TBD]` fields as incomplete in `missing_artifacts`.

---

## Output Format

```yaml
submission_description: |
  <Full Markdown submission text>

short_description: "<≤280 characters>"

artifact_checklist:
  - item: "<artifact name>"
    status: "<complete|incomplete|missing>"
    url_or_value: "<link or value if complete>"

missing_artifacts:
  - item: "<name>"
    blocking: <true|false>
    action_required: "<what to do>"

submission_quality_score:
  score: <1-10>
  breakdown:
    completeness: <1-10>
    clarity: <1-10>
    impact_framing: <1-10>

last_mile_actions:
  - priority: <number>
    action: "<what to do>"
    estimated_minutes: <number>
```

---

## Example

**Input:**
```yaml
project_title: "AnchorAI"
tagline: "An AI companion that remembers your emotional journey so you never have to start over."
problem_statement: "College students wait 6 weeks for counseling while anxiety compounds daily."
solution_summary: "GPT-4 with Redis-backed session memory for always-available, context-aware emotional support."
tech_stack: ["Python", "FastAPI", "React", "Redis", "OpenAI GPT-4"]
team_members:
  - name: "Alex"
    role: "Backend"
  - name: "Sam"
    role: "Frontend"
  - name: "Jordan"
    role: "Design"
repo_url: "https://github.com/team/anchorai"
track: "AI for Mental Health"
submission_platform: "Devpost"
```

**Output:**
```yaml
submission_description: |
  ## Inspiration
  40% of college students report anxiety as their top health concern, yet the average campus counseling wait is 6 weeks. Most students give up before they're seen.

  ## What It Does
  AnchorAI is a GPT-4 powered emotional support companion that remembers your history across sessions. It opens every conversation with context from your last check-in — so you never have to re-explain your situation.

  ## How We Built It
  Python FastAPI backend with OpenAI GPT-4 API. Session summaries stored in Redis and injected into the system prompt. React frontend with a clean single-page chat UI.

  ## Challenges
  Getting memory injection to stay within GPT-4 context window limits required hard-capping summaries at 150 tokens and testing multiple summarization prompts.

  ## Accomplishments
  Working live demo with genuine session memory recall. Crisis escalation card renders on distress detection.

  ## What We Learned
  The emotional framing of AI responses matters more than technical sophistication. Users notice tone before they notice features.

  ## What's Next
  Human counselor escalation. University licensing. Multi-session longitudinal mood tracking.

short_description: "AnchorAI: GPT-4 emotional support companion that remembers your mental health journey. No waitlist. No starting over. Always there. 🧠"

artifact_checklist:
  - item: "Source code repository"
    status: "complete"
    url_or_value: "https://github.com/team/anchorai"
  - item: "Demo video"
    status: "complete"
    url_or_value: "https://youtube.com/watch?v=demo"
  - item: "Live demo URL"
    status: "incomplete"
    url_or_value: ""
  - item: "README with setup instructions"
    status: "complete"
    url_or_value: "https://github.com/team/anchorai#readme"

missing_artifacts:
  - item: "Live demo URL"
    blocking: false
    action_required: "Deploy to Railway or Render; update Devpost submission with URL"

submission_quality_score:
  score: 8
  breakdown:
    completeness: 9
    clarity: 8
    impact_framing: 8

last_mile_actions:
  - priority: 1
    action: "Deploy live demo to Railway and update Devpost URL field"
    estimated_minutes: 20
  - priority: 2
    action: "Add 3 screenshots to Devpost gallery"
    estimated_minutes: 10
  - priority: 3
    action: "Confirm repo is public and README loads correctly"
    estimated_minutes: 5
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-submission-guidelines.md`
- `knowledge/hackathon-winning-patterns.md`
- `knowledge/hackathon-pitch-strategy.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
