---
name: hackathon-event-parser
description: >-
  Parse a hackathon event URL to extract tracks, judging criteria, timeline, and sponsor tools for autonomous pipeline execution.
---
# hackathon-event-parser

## Goal
Parse a hackathon event URL to extract structured information — tracks, judging criteria, timeline, and sponsor tools — required to trigger the full devkit workflow pipeline autonomously.

This is the **autonomous pipeline entry point**. When a URL is provided, this skill replaces manual track description input for all downstream skills.

---

## Trigger Conditions

Use this skill when:
- A hackathon event URL is available (Devpost, DoraHacks, Hackathon.com, MLH, or any event page)
- The team wants to run the devkit pipeline autonomously from a single input
- Track descriptions, judging criteria, or sponsor briefs must be extracted without manual copying
- Multiple tracks exist on an event page and the best-fit track must be identified
- This is always the **first skill invoked** in an autonomous pipeline; its output feeds `hackathon-track-analyzer`

---

## Inputs

```yaml
event_url: "<hackathon event URL>"           # required
preferred_track: "<track name or hint>"      # optional — if known, used to prioritize extraction
team_size: <number>                          # optional — used to filter feasibility signals
team_skills:                                 # optional — used to flag relevant sponsor tools
  - "<skill>"
extract_mode: "full | tracks_only | criteria_only"  # optional, default: full
```

---

## Outputs

```yaml
event_metadata:
  name: "<event name>"
  organizer: "<organizer name>"
  url: "<canonical event URL>"
  submission_platform: "<Devpost | DoraHacks | Hackathon.com | other>"
  start_datetime: "<ISO 8601 or 'unknown'>"
  end_datetime: "<ISO 8601 or 'unknown'>"
  duration_hours: <number or null>
  location: "<in-person | virtual | hybrid>"
  registration_deadline: "<ISO 8601 or 'unknown'>"
  submission_deadline: "<ISO 8601 or 'unknown'>"

tracks:
  - id: "<track-id>"
    name: "<track name>"
    description: "<raw track description>"
    sponsor: "<sponsor name or null>"
    prize: "<prize description or null>"
    required_tools:
      - "<tool or API name>"
    eligibility_constraints:
      - "<constraint>"
    feasibility_signal: "<high | medium | low>"  # based on team_skills if provided

judging_criteria:
  - track_id: "<track-id or 'global'>"
    axes:
      - axis: "<criterion name>"
        weight: "<high | medium | low | percentage if stated>"
        description: "<what judges evaluate>"
    rubric_source: "<verbatim | inferred | not_published>"

sponsor_tools:
  - sponsor: "<sponsor name>"
    tools:
      - name: "<tool or API>"
        use_case: "<what it enables>"
        bonus_prize: <true | false>
        docs_url: "<URL or null>"

timeline:
  - event: "<event name>"
    datetime: "<ISO 8601 or relative>"
    notes: "<optional context>"

recommended_track:
  track_id: "<id>"
  track_name: "<name>"
  rationale: "<why this track is recommended given team size/skills>"

extraction_confidence: "<high | medium | low>"
extraction_warnings:
  - "<any ambiguity, missing data, or access issues>"

next_skill: "hackathon-track-analyzer"
```

---

## Rules

1. Extract all content directly from the event page without inference where possible.
2. If the judging rubric is not published, set `rubric_source: "not_published"` and infer typical criteria — mark inferred axes with `[INFERRED]`.
3. If the URL is inaccessible (auth wall, 404, dynamic content), set `extraction_confidence: "low"` and populate fields from available fragments; list all gaps in `extraction_warnings`.
4. Never fabricate dates, prizes, or sponsor names. Use `"unknown"` or `null` for missing values.
5. If multiple tracks exist, extract all tracks and recommend one based on team signals if provided.
6. Normalize duration to hours. If only start/end dates are given, compute `duration_hours`.
7. Flag any required tool or API that conflicts with `team_skills` as a constraint.
8. `next_skill` must always be set to `hackathon-track-analyzer` to enforce pipeline continuity.

---

## Output Format

```yaml
event_metadata:
  name: "<string>"
  organizer: "<string>"
  url: "<string>"
  submission_platform: "<string>"
  start_datetime: "<ISO 8601 or 'unknown'>"
  end_datetime: "<ISO 8601 or 'unknown'>"
  duration_hours: <number or null>
  location: "<in-person | virtual | hybrid>"
  registration_deadline: "<ISO 8601 or 'unknown'>"
  submission_deadline: "<ISO 8601 or 'unknown'>"

tracks:
  - id: "<string>"
    name: "<string>"
    description: "<string>"
    sponsor: "<string or null>"
    prize: "<string or null>"
    required_tools:
      - "<string>"
    eligibility_constraints:
      - "<string>"
    feasibility_signal: "<high | medium | low>"

judging_criteria:
  - track_id: "<string>"
    axes:
      - axis: "<string>"
        weight: "<high | medium | low | percentage>"
        description: "<string>"
    rubric_source: "<verbatim | inferred | not_published>"

sponsor_tools:
  - sponsor: "<string>"
    tools:
      - name: "<string>"
        use_case: "<string>"
        bonus_prize: <boolean>
        docs_url: "<string or null>"

timeline:
  - event: "<string>"
    datetime: "<string>"
    notes: "<string>"

recommended_track:
  track_id: "<string>"
  track_name: "<string>"
  rationale: "<string>"

extraction_confidence: "<high | medium | low>"
extraction_warnings:
  - "<string>"

next_skill: "hackathon-track-analyzer"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-tools.md`
- `knowledge/hackathon-judging-criteria.md`
- `knowledge/hackathon-winning-patterns.md`
- `knowledge/hackathon-submission-guidelines.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
- `playbooks/24h-hackathon-playbook.md`
- `playbooks/36h-hackathon-playbook.md`
- `playbooks/48h-hackathon-playbook.md`

**Input:**
```yaml
event_url: "https://globalaihealth.devpost.com"
team_size: 3
team_skills: ["Python", "FastAPI", "React", "OpenAI API"]
extract_mode: "full"
```

**Output:**
```yaml
event_metadata:
  name: "Global AI Health Hackathon 2025"
  organizer: "HealthTech Alliance"
  url: "https://globalaihealth.devpost.com"
  submission_platform: "Devpost"
  start_datetime: "2025-09-12T09:00:00-05:00"
  end_datetime: "2025-09-14T17:00:00-05:00"
  duration_hours: 56
  location: "virtual"
  registration_deadline: "2025-09-11T23:59:00-05:00"
  submission_deadline: "2025-09-14T15:00:00-05:00"

tracks:
  - id: "track-mental-health"
    name: "AI for Mental Health"
    description: "Build AI-powered tools that improve mental health outcomes for young adults aged 18–30."
    sponsor: "OpenAI"
    prize: "$5,000 + OpenAI API credits"
    required_tools:
      - "OpenAI API"
    eligibility_constraints:
      - "Must use OpenAI API"
      - "Solution must target ages 18–30"
    feasibility_signal: "high"

  - id: "track-diagnostics"
    name: "AI Diagnostics"
    description: "Use AI to assist clinicians in early disease detection using medical imaging."
    sponsor: "Nvidia"
    prize: "$7,500 + Nvidia GPU credits"
    required_tools:
      - "Nvidia NIM"
      - "Medical imaging dataset"
    eligibility_constraints:
      - "Must use a publicly available medical dataset"
      - "Model must not make clinical claims"
    feasibility_signal: "low"

judging_criteria:
  - track_id: "track-mental-health"
    axes:
      - axis: "Innovation"
        weight: "30%"
        description: "Novel application of AI to mental health — beyond basic chatbots"
      - axis: "Impact"
        weight: "30%"
        description: "Potential to reach underserved users; measurable outcomes"
      - axis: "Technical Execution"
        weight: "20%"
        description: "Working demo; appropriate use of OpenAI API; code quality"
      - axis: "Presentation"
        weight: "20%"
        description: "Clarity of pitch; demo quality; storytelling"
    rubric_source: "verbatim"

  - track_id: "track-diagnostics"
    axes:
      - axis: "Clinical Validity"
        weight: "high"
        description: "[INFERRED] Accuracy and safety of diagnostic suggestions"
      - axis: "Technical Execution"
        weight: "high"
        description: "[INFERRED] Model performance; dataset usage; implementation quality"
    rubric_source: "inferred"

sponsor_tools:
  - sponsor: "OpenAI"
    tools:
      - name: "GPT-4o API"
        use_case: "Conversational AI, text generation, classification"
        bonus_prize: true
        docs_url: "https://platform.openai.com/docs"
  - sponsor: "Nvidia"
    tools:
      - name: "Nvidia NIM"
        use_case: "GPU-accelerated model inference for medical imaging models"
        bonus_prize: true
        docs_url: "https://developer.nvidia.com/nim"

timeline:
  - event: "Registration closes"
    datetime: "2025-09-11T23:59:00-05:00"
    notes: "Teams must register before hacking begins"
  - event: "Hackathon start"
    datetime: "2025-09-12T09:00:00-05:00"
    notes: "Opening keynote; tracks announced"
  - event: "Midpoint check-in"
    datetime: "2025-09-13T12:00:00-05:00"
    notes: "Optional mentor sessions available"
  - event: "Submissions close"
    datetime: "2025-09-14T15:00:00-05:00"
    notes: "Devpost submission must be complete; late submissions not accepted"
  - event: "Judging"
    datetime: "2025-09-14T16:00:00-05:00"
    notes: "3-minute pitch + 2-minute Q&A per team"

recommended_track:
  track_id: "track-mental-health"
  track_name: "AI for Mental Health"
  rationale: "Team has Python, FastAPI, React, and OpenAI API skills — all required tools are covered. Feasibility signal is high vs. low for diagnostics (which requires medical imaging expertise). Prize is competitive and judging rubric is fully published."

extraction_confidence: "high"
extraction_warnings:
  - "Judging rubric for track-diagnostics was not published; criteria are inferred from track description"
  - "Midpoint check-in schedule may change — verify on event Discord"

next_skill: "hackathon-track-analyzer"
```
