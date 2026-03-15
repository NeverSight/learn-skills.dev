---
name: hackathon-demo-video
description: >-
  Produce a structured script and time-coded shot list for a hackathon demo video that showcases the core value within a strict time limit.
---
# hackathon-demo-video

## Goal
Produce a structured script and shot list for a hackathon demo video that showcases the project's core value within a strict time limit.

---

## Trigger Conditions

Use this skill when:
- The MVP demo flow is implemented and stable
- A demo video must be recorded for submission or as a live-demo fallback
- The wow moment timing and placement in the video need to be optimized
- The recording environment must be checked and locked before recording begins
- Invoked during Phase 6; run in parallel with `hackathon-pitchdeck` after code freeze

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `project_title` | string | Yes | Name of the project |
| `tagline` | string | Yes | One-sentence description |
| `mvp_demo_flow` | object[] | Yes | Demo steps from `hackathon-scope-cutter` |
| `wow_factor` | string | Yes | The single most impressive moment |
| `video_duration_seconds` | integer | Yes | Target video length in seconds |
| `demo_environment` | string | No | Where the demo runs (e.g., web browser, mobile, CLI) |
| `voiceover` | boolean | No | Whether the video includes voiceover (default: true) |

---

## Outputs

| Output | Description |
|---|---|
| `script` | Time-coded narration script |
| `shot_list` | What is shown on screen at each moment |
| `wow_moment_timestamp` | When in the video the wow factor hits |
| `recording_checklist` | Pre-recording setup and validation steps |
| `fallback_plan` | What to do if live demo fails during recording |

---

## Rules

1. The first 5 seconds must state the problem or hook — no introductions.
2. `wow_factor` must appear before the 60% mark of `video_duration_seconds`.
3. Every `mvp_demo_flow` step must map to at least one shot.
4. Narration sentences must be under 15 words each.
5. Reserve the final 10% of video time for a summary and call-to-action.
6. `recording_checklist` must include at least: notifications off, test data ready, screen resolution set.
7. `fallback_plan` must be a static slide or pre-recorded segment, never "we'll skip this part."

---

## Output Format

```yaml
wow_moment_timestamp: <seconds>

script:
  - timestamp_start: <seconds>
    timestamp_end: <seconds>
    narration: "<spoken words>"

shot_list:
  - timestamp_start: <seconds>
    timestamp_end: <seconds>
    screen_content: "<what is visible>"
    action: "<what the presenter does>"

recording_checklist:
  - "<item>"

fallback_plan:
  trigger: "<condition>"
  action: "<what to do>"
```

---

## Example

**Input:**
```yaml
project_title: "AnchorAI"
tagline: "An AI companion that remembers your emotional journey."
wow_factor: "AI recalls emotional context from 3 days ago and adapts tone in real time"
video_duration_seconds: 120
demo_environment: "web browser"
voiceover: true
mvp_demo_flow:
  - step: 1
    action: "User types 'I'm overwhelmed today'"
    outcome: "AI responds empathetically"
  - step: 2
    action: "User mentions recurring work stress"
    outcome: "AI references last week's conversation"
  - step: 3
    action: "User expresses hopelessness"
    outcome: "Crisis resource card appears"
```

**Output:**
```yaml
wow_moment_timestamp: 45

script:
  - timestamp_start: 0
    timestamp_end: 8
    narration: "40% of college students live with anxiety. Most wait 6 weeks for help."
  - timestamp_start: 8
    timestamp_end: 15
    narration: "AnchorAI is always available — and it remembers you."
  - timestamp_start: 15
    timestamp_end: 45
    narration: "Watch what happens when a student checks in after a hard week."
  - timestamp_start: 45
    timestamp_end: 70
    narration: "AnchorAI recalls last week's conversation — without being told."
  - timestamp_start: 70
    timestamp_end: 95
    narration: "When a student signals distress, AnchorAI responds with care and resources."
  - timestamp_start: 95
    timestamp_end: 120
    narration: "No waitlist. No starting over. AnchorAI — always there."

shot_list:
  - timestamp_start: 0
    timestamp_end: 8
    screen_content: "Stat card: '40% of students report anxiety. Average wait: 6 weeks.'"
    action: "Hold on stat card"
  - timestamp_start: 15
    timestamp_end: 45
    screen_content: "Chat interface — user types message"
    action: "Type 'I'm feeling overwhelmed again this week'"
  - timestamp_start: 45
    timestamp_end: 70
    screen_content: "AI response references 'last week's exam stress you mentioned'"
    action: "Scroll to highlight the memory reference in the AI response"
  - timestamp_start: 70
    timestamp_end: 95
    screen_content: "User types hopelessness message; crisis card slides in below response"
    action: "Type message; pause on crisis card appearing"

recording_checklist:
  - "Notifications disabled on OS and browser"
  - "Demo account pre-loaded with 1 prior session in Redis"
  - "Screen resolution set to 1920×1080; browser zoom 125%"
  - "Test data: prior session summary contains 'exam stress' phrase"
  - "Run full demo flow once before recording"

fallback_plan:
  trigger: "OpenAI API fails to respond during recording"
  action: "Use pre-recorded screen capture of the memory recall exchange as an overlay segment"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-demo-psychology.md`
- `knowledge/hackathon-demo-patterns.md`
- `knowledge/hackathon-pitch-strategy.md`

### Templates

- `templates/demo-script-template.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
