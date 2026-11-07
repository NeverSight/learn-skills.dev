---
name: meeting-notes-action-plan
description: "Paste messy meeting notes, get back the decisions made, owners and deadlines, open questions, and a follow-up email ready to send. Use when the user asks for \"Meeting Notes → Action Plan\" or provides paste your meeting notes."
metadata:
  author: "skillvize"
  version: "v1.0"
  source: "https://www.skillvize.com/skills/productivity-meeting-notes"
---

# Meeting Notes → Action Plan

Paste messy meeting notes, get back the decisions made, owners and deadlines, open questions, and a follow-up email ready to send.

`{{input}}` in the steps below is the user's input (Paste your meeting notes).

## Steps

### 1. Extract the decisions

From the notes ({{input}}), list every decision actually made — not discussed, made. One line each.

### 2. Assign the actions

List every action item with an owner and deadline. If either is missing, flag it as unassigned rather than guessing.

### 3. Surface the unresolved

List open questions raised but not settled, and who needs to weigh in on each.

### 4. Draft the follow-up

Write a short follow-up email — decisions, action items with owners, open questions — skimmable in 30 seconds.

## Example

**Paste your meeting notes:** Q3 planning sync — discussed launch timing, Sarah owns design, pricing page still open, EU rollout needs legal...

**Output:**

```
ACTION PLAN

DECISIONS MADE
• Launch moves to Sept 15

ACTION ITEMS
• Sarah — final designs by Aug 20
• Marco — pricing page copy by Aug 25

UNRESOLVED
• EU rollout timing — needs legal input

FOLLOW-UP EMAIL: drafted and ready to paste.
```
