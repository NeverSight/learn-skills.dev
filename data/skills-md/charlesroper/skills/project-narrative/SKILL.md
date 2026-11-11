---
name: project-narrative
description: Write and maintain NARRATIVE.md, the evidence-linked story of a project for humans and agents. Use when a project starts, a story-changing event occurs (release, incident, pivot, architecture decision), someone onboards or the user asks to write or refresh the narrative.
license: MIT
metadata:
  author: Charles Roper
  version: "1.0"
---

# Project Narrative

A narrative records the history of a project: why it exists, what happened, what changed, what failed and what comes next. Keep it separate from the README, changelog and ADRs, and link to them.

One document serves two readers. People read from the top for orientation. Agents go to the status, invariants and evidence links.

## Outcomes

- A newcomer can explain the project after five minutes.
- An agent can answer "why is this like this?" without reading the whole repository.
- Decisions, failures and reversals remain available after the people who made them leave.
- Every claim is traceable to evidence.
- The narrative reads as a series of short blog posts.

## Procedure

1. **Gather evidence.** Read the existing narrative, README, changelog, ADRs, recent commits and open issues. Completion: you can name the last three turning points and the current next action.
2. **Apply the story-changing test.** Completion: a clear yes or no. If no, stop.
3. **Write the post.** Treat the entry as a short blog post of roughly 150 to 600 words. Open with the moment, problem or question that started it. Explain what happened, what it replaced and what was learned. Show an artefact, quote, screenshot or number. Close with the consequence or the open question. Link evidence. Completion: it reads as a post a colleague would choose to read.
4. **Update the status and open questions.** Refresh the agent brief at the same time. Completion: no stale date or resolved question remains.
5. **Compress the summary.** Re-read the summary and the main story. Completion: the summary still fits five sentences and the main story still fits one screen.
6. **Verify.** Run the checks below. Completion: every check passes.

If the narrative update belongs with a significant commit, include it in that commit. Otherwise make a separate documentation commit. Add corrections forward; leave pushed history intact.

## The story-changing test

A change is story-changing when it alters one of these:

- Behaviour, scope or audience.
- Architecture or a core dependency.
- Direction, through a decision or a reversal.
- Expectations, through a failure, cost or abandoned path.
- The public surface, through a release, launch, migration or incident.
- Understanding, through an onboarding gap.

Mechanical work stays out: typos, formatting, dependency bumps and refactors with no behaviour change. Test: would a newcomer need this to understand the project? If no, skip it.

Agents update automatically when the test passes. Write only about work that passes the test.

## File contract

Default to one file: `NARRATIVE.md` at the repository root.

When it exists, extend it. Replacing it discards history.

Split only when one of these is true:

- The file passes roughly 1,000 lines or 40KB.
- The project contains multiple distinct products or teams.
- The timeline spans several eras and no longer reads as one story.
- The user explicitly asks for dated entries.

When splitting, keep a `docs/narrative/README.md` index and one file per era or product, for example `docs/narrative/2026-01-origins.md`. Move material, keep links working and leave a pointer in `NARRATIVE.md`.

## Required shape

Use these sections in this order. Rename them only when the project's language demands it.

1. **Summary**: title, one-line description and the reason the project exists. Five sentences maximum.
2. **Status and agent brief**: absolute date, current state, next action, invariants that must not break and links to deeper sources. Link to `AGENTS.md` or `CLAUDE.md` instead of repeating them.
3. **Why**: the problem, the audience and the constraints that shaped the work.
4. **How we got here**: dated blog-post entries in chronological order.
5. **Turning points**: decisions, failures, reversals and what changed because of them.
6. **How it works**: the architecture and mechanics, in prose.
7. **How it was made and tested**: the process, tools, people, checks and what the checks do not prove. Treat this as part of the story.
8. **Open questions**: what is unknown, undecided or risky.
9. **Sources**: links to commits, issues, ADRs, releases, documents and artefacts.

## Style

Apply the repository's style guide. When the repository has no style guide, use plain technical prose: active voice, one idea per sentence, concrete nouns and verbs.

In the **Editorial Pipeline**, `project-narrative` serves as Stage 1 drafting. Refer to sibling skills as the single sources of truth:

- **Prose discipline and tropes:** Follow `on-writing-well` for core Zinsser mechanics (humanity, clarity, unity, clutter removal) and trope elimination (no stock phrases, no false drama, no empty framing).
- **British English and house style:** Follow `guardian-style-guide` as the Stage 2 Sub-Editor Gate for UK orthography (`-ise` endings, no Oxford comma), dates, numbers and spaced en-dashes (` – `).

## Writing rules

- Write each entry as a post that stands on its own.
- Open with the scene, problem or question that started the work.
- Use concrete detail: names, numbers, quotes, screenshots, commands and artefacts.
- Use the writer's own voice. First person is welcome when the writer did the work.
- Use the length the post needs. Cut repetition and keep detail.
- Tell the story as if speaking to a colleague.
- Date every entry absolutely. Relative time becomes wrong.
- Give each entry one event. Split an entry with two headlines.
- Attach an evidence link to every factual claim. Mark recollection and inference when evidence is absent.
- Record failures and reversals. They explain the most and are the easiest to omit.
- Attribute intent to evidence. Write "we did not know" when that is true.
- Keep open questions open. Put hindsight in a later entry.
- Correct the record by appending a dated note.
- Keep the summary to five sentences.
- Use the repository's existing terms and style.

## Verify

- A newcomer can explain the project after five minutes.
- An agent can answer "why is this like this?" from the narrative and its links.
- Every claim is linked or marked as recollection or inference.
- Status shows an absolute date.
- At least one failure, reversal or abandoned path is recorded when one exists.
- No secret, credential, personal data or customer data appears.
- Each section links to README, changelog or ADR content instead of repeating it.
- The summary fits five sentences.
- The prose follows the repository style and carries no trope in place of an explanation.

## Public and private

Determine visibility before writing:

- Run `gh repo view --json visibility,isPrivate` when `gh` is available and the repository has a remote.
- When visibility is unknown, assume private and ask the user.
- A repository with no remote is private by default.

Private narrative: write for a future colleague who lacks your context. Still exclude secrets and personal data.

Public narrative: write for outsiders. Exclude secrets, credentials, customer data, personal data, internal URLs and hostnames, unannounced plans, pricing, contracts and security weaknesses.

Private to public transition: run a review before the repository becomes public. Read the entire narrative and search for each category above. Flag anything uncertain and stop until the user decides. Editing the narrative does not remove material from git history. Review history separately, rotate any exposed secret and record the outcome.

## Failure modes

- **Changelog clone**: dated one-liners that record a commit but not a story. Instead, write a full post for the change, or leave it out.
- **Status report**: terse bullets where a scene and an explanation belong. Instead, write the scene and the explanation in prose.
- **Marketing page**: claims without evidence or failure. Instead, link evidence and name the cost.
- **Hero arc**: a tidy story that hides the dead ends. Instead, record the abandoned paths.
- **Fake certainty**: hindsight presented as intent. Instead, mark what was unknown at the time.
- **Orphan claim**: a fact with no link and no marker. Instead, link it or label it.
- **Stale status**: a current state older than the last story-changing event. Instead, update it in the same commit.
- **Duplicate docs**: one explanation maintained in three places. Instead, keep one home and link to it.

## Template

```markdown
# Project Name

One sentence on what this is and why it exists.

## Status and agent brief

31 October 2026. State. Next action. Invariants. [Sources](link)

## Why

Problem, audience, constraints.

## How we got here

### 31 October 2026: Entry title

Open with the moment or problem. Describe what happened, what it
replaced and what was learned. Include a quote, number, screenshot or
code excerpt. Close with the consequence or the open question.
[Evidence](link)

## Turning points

- Date: decision, failure or reversal, and its consequence. [Evidence](link)

## How it works

The architecture and mechanics, in prose. Link to deeper docs.

## How it was made and tested

The process, tools, people and checks. Say what the checks prove and
what they do not prove.

## Open questions

- Question. Owner or next step.

## Sources

- [Document](link)
- [Commit](link)
```
