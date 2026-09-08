---
name: weekly-work-update
description: Draft an evidence-backed weekly work update from Monologue voice notes. Use when a user wants to review a week, summarize project progress and decisions, identify next steps, blockers, or owners, or prepare a status update from multiple recordings.
---

# Weekly Work Update

Turn work-related Monologue notes from a selected week into a concise, sourced draft. Keep retrieval read-only and do not send, publish, or update another system without explicit approval.

## Workflow

1. Determine the reporting interval and the user's timezone. Resolve relative dates such as "this week" or "last week" in that timezone and state the exact start and end dates. Treat weeks as Monday through Sunday unless the user specifies another convention.
2. Invoke `$monologue-notes` for all Monologue access. If setup is required, have the user run `monologue onboarding` in their own terminal; never request or accept an API token in chat.
3. Retrieve the complete note list, including pagination. Do not use
   `created-after` or `created-before` as recording-time filters; delayed uploads
   can be created outside the reporting week:

   ```bash
   monologue notes all
   ```

   Select the reporting interval locally using `recorded_at` in the user's
   timezone. If it is absent, use `created_at` as a disclosed fallback. If the
   library is too large for exhaustive retrieval, ask before applying a
   creation-time optimization and disclose the resulting coverage limit.

4. Shortlist notes from their titles, dates, and summaries. Search results are candidates, not proof of relevance. Fetch each likely source and verify its contents before using it:

   ```bash
   monologue notes get NOTE_ID
   ```

5. Exclude personal notes and unrelated personal passages in mixed notes. If work/personal scope is ambiguous, omit the material or ask a focused question rather than exposing it.
6. Extract evidence into these categories:
   - project changes and progress
   - decisions made
   - next steps
   - blockers and dependencies
   - owners and collaborators
   - unresolved questions
7. Reconcile repeated or conflicting statements chronologically. Prefer the latest explicit update while noting a material contradiction. Do not convert an idea, suggestion, or another speaker's promise into the user's commitment.
8. Draft the update using the format below. Cite every material bullet with the source note title and local date: `(Note title — YYYY-MM-DD)`.

## Output

```markdown
# Weekly work update — DATE–DATE (TIMEZONE)

## Summary
[Two to four sentences]

## Project updates
- **Project:** Change, result, and current state. (Source — date)

## Decisions
- Decision and relevant rationale. (Source — date)

## Next steps
- [ ] Action — **Owner:** Name or `unclear` — timing, if explicitly stated. (Source — date)

## Blockers
- Blocker, impact, and owner if known. (Source — date)

## Open questions
- Question that still needs resolution. (Source — date)

## Sources
- Note title — date
```

Omit empty sections. Keep the update readable rather than reproducing transcripts.

## Evidence Rules

- Attribute an owner only when the recording identifies one. Otherwise use `Owner: unclear`.
- Label tentative language as tentative. Preserve distinctions such as planned, proposed, in progress, blocked, and completed.
- Separate the user's commitments from other speakers' commitments.
- Do not infer completion merely because a task was discussed.
- Cite note title and date in the update; keep note IDs internal unless the user requests them.
- Offer alternate formats, such as a Slack-ready draft or manager update, but do not send them.
