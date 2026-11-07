---
name: bug-report-triage
description: "Turns a vague bug report into clear repro steps, a likely root-cause area, a severity call, and the info you still need — ready to drop into a ticket. Use when the user asks for \"Bug Report Triage\" or provides paste the bug report or user complaint."
metadata:
  author: "skillvize"
  version: "v1.0"
  source: "https://www.skillvize.com/skills/tech-bug-triage"
---

# Bug Report Triage

Turns a vague bug report into clear repro steps, a likely root-cause area, a severity call, and the info you still need — ready to drop into a ticket.

`{{input}}` in the steps below is the user's input (Paste the bug report or user complaint).

## Steps

### 1. Reconstruct repro steps

From {{input}}, write the most likely step-by-step sequence that reproduces the issue, marking any guesses clearly.

### 2. Identify the likely area

Based on the symptoms, name the part of the system most likely responsible and why.

### 3. Assess severity

Rate it low/medium/high/critical based on impact and frequency. Justify in one sentence.

### 4. List info needed to confirm

Write 2-4 specific questions or data points that would confirm the cause — to ask the reporter or check in logs.

## Example

**Paste the bug report or user complaint:** App crashes sometimes when I try to upload a photo from my phone, happened twice today

**Output:**

```
BUG TRIAGE

REPRO STEPS (best guess)
1. Open the app on mobile
2. Go to upload
3. Select a photo from the camera roll
4. Confirm upload

LIKELY AREA
Mobile photo-upload pipeline — possibly large file size or HEIC handling, since "sometimes" suggests a file-specific edge case.

SEVERITY
High — crashes risk data loss and it happened twice in one day.

INFO TO REQUEST
• Device/OS version • Photo size and format • Every photo or specific ones?
```
