---
name: ux-journey-definition
description: "Define a practical, story-first product experience before UI prototyping. Use when you need one canonical artifact that explains what users see, what they can do, and how screens transition."
---

# UX Journey Definition

## Overview

Create one canonical artifact, `experience-story.md`, that captures the product story, main journey, screen-by-screen behavior, and transition mapping. This is the upstream input for `$product-ui-prototyping`.
The artifact must also encode cognition-first decisions so flow order and interaction density reduce user burden.

## Default Output

- `ui-prototypes/<prototype-name>/experience-story.md`
- If the user specifies a different path, follow the user path.

## Workflow

### Audible Notifications (Speak Tool, Required)

- Use the `Speak` tool for key stage-boundary updates so the user does not need to watch the screen continuously.
- Hard rule: speak at both stage start and stage completion for each key stage below (no selective skipping).
- Required speak stages:
  - workflow kickoff (`prototype context acknowledged`, `next stage`),
  - product story + main journey stage (`started`, then draft completed),
  - cognitive load criteria stage (`started`, then criteria drafted),
  - screen stories + alternate/error paths stage (`started`, then draft completed),
  - transition index stage (`started`, then index completed),
  - canonical artifact write stage (`started`, then `experience-story.md` written/updated),
  - quality gate stage (`started`, then `Pass`/`Needs fixes` result),
  - handoff-ready stage for `$product-ui-prototyping` (`started`, then ready status).
- Speak trigger policy:
  - do not skip required stage-boundary speak events,
  - for completion events, speak only after milestone content is physically written,
  - do not speak for partial drafts between required stage-boundary events,
  - batch close-together milestone updates into one short message.
- Keep each spoken message short (1-2 sentences), status-first, with one clear next step.
- If the `Speak` tool fails or is unavailable, continue workflow and provide the same update in text.
- Do not speak secrets, tokens, or full sensitive payloads.

### 1) Capture Product Story

Write one short paragraph:
- who the user is,
- what they are trying to achieve,
- what success looks like.

Keep this concrete and product-facing.
- Speak completion after product story draft is physically written.

### 2) Write Main Journey (Happy Path)

Write a numbered flow from entry to success.
Each step should include:
- what the user does,
- what the system does,
- which `screen_id` is involved.

Prioritize one critical flow first before expanding.
- Speak completion after main journey draft is physically written.

### 3) Define Cognitive Load Criteria (Required)

Before writing detailed screen behavior, define a short cognition-first rubric for this product:
- learning order strategy (what comes first and why),
- connection strategy (group by semantic/stem linkage where possible),
- chunking limits (items per step/screen),
- interference controls (what confusing patterns are delayed),
- progression policy (when to unlock complexity).

Keep this practical and measurable so it can be used as a review gate.
- Speak completion after cognitive-load criteria are physically written.

### 4) Write Screen Stories

For each screen, describe behavior in plain language with stable IDs.

Required shape:
- `screen_id`
- user arrives from
- user sees
- user can do (`action_id`)
- system behavior for each action
- cognitive objective (what mental burden this screen reduces)
- cognition controls (chunking, progressive disclosure, contrast/clarity choices)
- states to prototype (`default`, `loading`, `success`, `error`, `empty` when applicable)
- Speak completion after screen stories are physically written.

### 5) Capture Alternate/Error Paths

Document only meaningful branches:
- validation failures,
- empty/no-results states,
- recoverable errors.

For each branch, state:
- trigger/condition,
- what user sees,
- recovery action and destination.
- Speak completion after alternate/error paths are physically written.

### 6) Build Transition Index

Create a single transition table that links interactions to movement.

Columns:
- `transition_id`
- `trigger`
- `from_screen`
- `to_screen`
- `expected_feedback`

Use IDs consistently across the whole document.
- Speak completion after the transition index is physically written.

### 7) Record Blocking Questions

List only blockers that can change behavior or flow.
Do not include cosmetic/open-ended discussion items.

## Canonical Artifact Template

Use this structure in `experience-story.md`:

```markdown
# Experience Story: <prototype-name>

## 1) Product Story
<one short paragraph>

## 2) Main Journey
1. ...
2. ...

## 3) Cognitive Load Criteria
- Learning order: ...
- Connection strategy: ...
- Chunking limit: ...
- Interference control: ...
- Progression policy: ...

## 4) Screen Stories

### screen_id: <screen_id>
- User arrives from: ...
- User sees:
  - ...
  - ...
- User can do:
  - `<action_id>`: ...
- System behavior:
  - when `<action_id>` -> <feedback> -> go to `<next_screen_id>`
- Cognitive objective: ...
- Cognition controls:
  - chunking: ...
  - progressive disclosure: ...
  - clarity guardrails: ...
- States to prototype: default, loading, success, error, empty

## 5) Alternate And Error Paths
- If <condition>, show <state/message>, then user can <recovery action>.

## 6) Transition Index
| transition_id | trigger | from_screen | to_screen | expected_feedback |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... |

## 7) Blocking Questions
- <question> (owner: <name>)
```

## Practical Rules

- Keep it practical and short. Avoid heavy theory.
- No `out-of-scope` section by default.
- Focus on behavior and navigation, not design tokens.
- Keep each screen section to 5-8 bullets.
- Every action must define both feedback and next destination.

## Quality Gate

- One clear happy path exists from entry to success.
- Every major trigger maps to a target screen/state.
- Screen IDs and transition IDs are consistent.
- Error and empty states include recovery actions.
- The learning sequence explicitly minimizes cognitive burden (simple -> connected -> complex).
- Early modules prioritize semantic/stem-connected content before higher-interference pattern groups.
- Each screen declares its cognitive objective and concrete burden-control mechanisms.
- The document can be directly used by `$product-ui-prototyping`.
- Speak quality-gate result after validation completes.

## Handoff To Prototyping

When visual prototyping is requested next, invoke `$product-ui-prototyping` with:
- `ui-prototypes/<prototype-name>/experience-story.md`
- product constraints from this document
- chosen platform (`web`, `ios`, `android`)

Then generate state images, flow maps, and viewer artifacts based on the transition index and screen stories.
- Speak handoff-ready completion after `experience-story.md` is written/updated.
