---
name: hackathon-pitchdeck
description: >-
  Construct a complete hackathon pitch deck narrative with slide content, speaker notes, and judging alignment.
---
# hackathon-pitchdeck

## Goal
Construct a complete hackathon pitch deck narrative with slide-by-slide content, speaker notes, and a persuasive storyline aligned to judging criteria.

---

## Trigger Conditions

Use this skill when:
- The demo flow is implemented and the wow factor is confirmed
- Judging evaluation axes from `hackathon-track-analyzer` are available
- A pitch deck must be constructed before the presentation phase
- The pitch duration is known (determines slide count and time allocation)
- Invoked during Phase 6; run in parallel with `hackathon-demo-video` after implementation is frozen

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `project_title` | string | Yes | Name of the project |
| `tagline` | string | Yes | One-sentence project description |
| `problem_statement` | string | Yes | The problem being solved |
| `solution_summary` | string | Yes | How the project solves the problem |
| `mvp_demo_flow` | object[] | Yes | Demo steps from `hackathon-scope-cutter` |
| `target_user` | string | Yes | Primary user segment |
| `wow_factor` | string | Yes | The single most impressive aspect |
| `evaluation_axes` | object[] | Yes | Judging criteria from `hackathon-track-analyzer` |
| `team_members` | string[] | Yes | Team member names and roles |
| `pitch_duration_minutes` | integer | No | Available pitch time (default: 3) |

---

## Outputs

| Output | Description |
|---|---|
| `slides` | Ordered slide definitions with title, content, and speaker notes |
| `opening_hook` | First 15-second attention-grabbing statement |
| `closing_call_to_action` | Final memorable statement for judges |
| `judging_alignment` | How each slide addresses a judging axis |

---

## Rules

1. Map every slide to at least one `evaluation_axis`.
2. Open with the problem, not the team or technology.
3. Lead with the `wow_factor` within the first 60 seconds.
4. Include a live demo slide referencing `mvp_demo_flow`.
5. Each slide must be completable in under 30 seconds of speaking time.
6. Do not use more than 7 words per bullet point on any slide.
7. End with a memorable `closing_call_to_action`, not a "thank you" slide.

---

## Output Format

```yaml
opening_hook: "<string>"

slides:
  - number: <number>
    title: "<slide title>"
    type: "<hook|problem|solution|demo|technology|team|vision|cta>"
    bullets:
      - "<bullet>"
    speaker_notes: "<what to say>"
    judging_axes_addressed:
      - "<axis name>"

closing_call_to_action: "<string>"

judging_alignment:
  - axis: "<axis name>"
    addressed_in_slides:
      - <slide number>
```

---

## Example

**Input:**
```yaml
project_title: "AnchorAI"
tagline: "An AI companion that remembers your emotional journey so you never have to start over."
problem_statement: "College students wait 6 weeks for counseling while anxiety compounds daily."
solution_summary: "AnchorAI uses GPT-4 with persistent memory to provide empathetic, context-aware check-ins."
wow_factor: "The AI recalls your emotional context from 3 days ago and adapts its tone in real time"
pitch_duration_minutes: 3
team_members: ["Alex (backend)", "Sam (frontend)", "Jordan (design)"]
```

**Output:**
```yaml
opening_hook: "What if you waited 6 weeks for help, and your anxiety got worse every day?"

slides:
  - number: 1
    title: "The 6-Week Wait"
    type: "problem"
    bullets:
      - "40% of students report anxiety as top concern"
      - "Average campus counseling wait: 6 weeks"
      - "Most give up before they're seen"
    speaker_notes: "Open with the stat, then pause. Let it land."
    judging_axes_addressed: ["Impact"]

  - number: 2
    title: "Meet AnchorAI"
    type: "solution"
    bullets:
      - "Always available — no waitlist"
      - "Remembers your emotional history"
      - "Adapts tone to your current state"
    speaker_notes: "One sentence, then say 'let me show you.'"
    judging_axes_addressed: ["Innovation", "Impact"]

  - number: 3
    title: "Live Demo"
    type: "demo"
    bullets: []
    speaker_notes: "Show the memory recall moment. Slow down. Let silence work."
    judging_axes_addressed: ["Technical Execution", "Innovation"]

  - number: 4
    title: "What's Next"
    type: "vision"
    bullets:
      - "Partnership with student counseling centers"
      - "Crisis escalation to human counselors"
      - "1M students underserved — this is the start"
    speaker_notes: "End with the question: what if no student ever had to wait alone again?"
    judging_axes_addressed: ["Impact"]

closing_call_to_action: "No student should have to manage anxiety alone while waiting for help that may never come."

judging_alignment:
  - axis: "Innovation"
    addressed_in_slides: [2, 3]
  - axis: "Impact"
    addressed_in_slides: [1, 2, 4]
  - axis: "Technical Execution"
    addressed_in_slides: [3]
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-pitch-strategy.md`
- `knowledge/hackathon-demo-psychology.md`
- `knowledge/hackathon-judging-criteria.md`
- `knowledge/hackathon-winning-patterns.md`

### Templates

- `templates/pitchdeck-outline.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
