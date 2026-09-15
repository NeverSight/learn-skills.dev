---
name: gmail-opportunity-progress
description: Monitor Gmail for job or opportunity application updates, classify messages such as confirmations, rejections, interview invites, assessments, and follow-ups, then update a tracker or Notion opportunity database without coupling to the application execution skill.
---

# Gmail Opportunity Progress

## Purpose

Use this skill when application progress should be inferred from email and written back to an opportunity tracker.

This skill replaces brittle keyword-only Gmail filtering with a two-stage workflow:

1. Use deterministic Gmail queries to reduce the inbox to likely opportunity messages.
2. Use message content, sender, subject, thread context, and tracker rows to classify the real application event.

Do not invoke or modify `job-application-operator` from this skill. This skill tracks outcomes after applications have been submitted or when companies send next-step instructions.

## Tool Boundary

Use Gmail MCP/API tools for:

- searching recent messages and threads
- reading subject, sender, recipients, date, labels, snippets, and body
- finding related thread messages

Use Notion MCP/API or another tracker API for:

- matching messages to existing opportunity rows
- updating `Status`
- appending concise progress notes
- storing next action and relevant deadlines if the schema supports them

Do not use browser automation to read Gmail or edit Notion when MCP/API access exists.

## Candidate Email Search

Start with bounded Gmail searches. Prefer recent windows unless the user asks for a historical import.

Useful first-pass query terms:

```text
(application OR applied OR Bewerbung OR candidate OR interview OR assessment OR challenge OR rejection OR leider OR unfortunately OR congratulations OR next step OR schedule OR calendly OR confirmation)
```

Useful exclusions:

```text
-github -newsletter -promotion -unsubscribe
```

If the mailbox has labels such as `JOBS` or `JOBS/<status>`, use them as hints, not ground truth. Older label names may reflect previous workflows and should not override message content.

## Classification

Classify each relevant message into one of these event types:

- `submission_confirmation`: confirms the application was received
- `rejection`: rejects the candidate or says the company will not proceed
- `interview_invite`: asks the candidate to book or choose interview time slots
- `interview_scheduled`: confirms a booked interview time
- `interview_followup`: discusses next interview steps, rescheduling, or post-interview feedback
- `assessment_received`: sends an online assessment, take-home, coding challenge, work sample, or timed test
- `assessment_reminder`: reminds about an unsubmitted assessment or deadline
- `assessment_submitted`: confirms assessment submission or receipt
- `company_question`: asks for missing information, documents, availability, work authorization, salary expectations, or clarification
- `non_actionable`: marketing, job alerts, newsletters, generic career-site emails, unrelated recruiter outreach, or duplicate noise

When uncertain, prefer `company_question` or leave status unchanged and report the ambiguity.

## Status Mapping

Map email events to tracker status:

- `submission_confirmation` -> `Waiting for response`
- `rejection` -> `Rejected`
- `interview_invite` -> `Interview invite`
- `interview_scheduled` -> `Interview scheduled`
- `interview_followup` after a completed meeting -> `Interview completed` or `Waiting for response`, depending on the content
- `assessment_received` -> `Assessment received`
- `assessment_reminder` -> keep `Assessment received` or `Assessment in progress`
- `assessment_submitted` -> `Assessment submitted`
- `company_question` -> `Human blocked`
- `non_actionable` -> no status change

Do not collapse all positive responses into `Interviewing`; use the finer-grained statuses so the next action is visible.

## Matching Messages To Rows

Match in this order:

1. Exact company name in sender domain, subject, or body.
2. Exact role title in subject or body.
3. Application portal domain from the row URL.
4. Thread history containing earlier application confirmation.
5. Recruiter/company email domain plus a single plausible active row.

If multiple rows match, do not update automatically. Return the candidate matches and the reason for ambiguity.

## Writeback Rules

For each updated row, write:

- `Status`: mapped status from the email event
- `Rationale` or progress notes field: short note with message date, sender/company, event type, and next action
- Deadline field, if present: assessment due date or scheduling deadline

Do not paste full email bodies into the tracker. Summarize only the operational fact needed for the pipeline.

## Review Output

Return a concise report:

- messages scanned
- relevant messages found
- rows updated
- skipped ambiguous matches
- next human actions
- deadlines found

For destructive or irreversible actions, ask before acting. Status updates based on clear email evidence are safe to perform directly.
