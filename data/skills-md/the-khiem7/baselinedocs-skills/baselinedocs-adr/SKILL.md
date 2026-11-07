---
name: baselinedocs-adr
description: Draft an Architectural Decision Record in the AWS Prescriptive Guidance format from one closed decision in a baseline pack's hallucination document, written as a standalone file under docs/adr/. Use explicitly when the user wants a closed decision from a doc pack turned into an ADR for the repository or for promotion to a production repository.
version: "3.3.0"
---

# Baseline Docs ADR

Turn one closed decision in a pack into a standalone ADR. The pack is read and never written. The only files touched are the new ADR and the ADR directory's `README.md` index.

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

Read `<core-dir>/references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Inputs

Determine or confirm:

- the pack root, or the initiative index path, and the identifier of the decision entry
- the ADR directory: `docs/adr/` at the repository root, or `adr/` or `docs/decisions/` when the repository already uses one

## Workflow

1. Resolve the entry. Read that entry's section and its row in the `## Entry index`. Read nothing else from the pack.
2. Refuse and say why when the entry is an open question, or when its index status says it was retired, reversed, or superseded. An ADR would record a decision that no longer holds. Continue only when the user names the entry again and says to go on.
3. Check the decision is architecturally significant: structure, non-functional requirements, dependencies, interfaces, or construction techniques. Routine implementation detail gets no ADR; say so and stop.
4. Read `references/template.md` and `references/process.md` in full.
5. Take the next free number in the ADR directory, four digits. The file is `NNNN-short-kebab-title.md`. Never reuse a number and never overwrite an existing file.
6. Write the ADR with the template's headings in the template's order, mapping the entry as below.
7. Add the ADR to `README.md` in the ADR directory: number, title, status, newest first. Create the file when it is missing.
8. Report, then stop.

| Entry part | ADR section |
|---|---|
| Decided | Decision, stated as "We will ..." |
| Why | Context, and Consequences/Positive where it names a benefit |
| Rejected alternatives | Context, one bullet each with the reason it lost |
| What breaks if ignored | Consequences/Negative |
| a checkable rule, if the entry states one | Compliance; otherwise keep the heading with one line saying none was identified |

Notes carry the author from `git config user.name`, version `0.1`, and the changelog line `0.1: Initial proposed version`. Date is today.

## Rules

- Write the ADR so it reads with nothing beside it. No path into the pack, no entry identifier, no reference to a chat or an email. The ADR is the file that leaves the working repository for production, where a pointer into the pack resolves to nothing.
- Set the status to `Proposed`, always. Never write `Accepted`; acceptance is the team's decision and the agent wants to finish the job.
- Carry what the entry says and add nothing. Do not invent an alternative or a consequence the entry lacks; write "None recorded." in that spot and report the gap.
- Never edit an existing ADR. A changed decision is a new ADR.

## Output

- the ADR path and its status
- which entry parts went into which sections, and any section left as "None recorded."
- that the pack does not record this ADR; `baselinedocs-save` is what writes it there
- that acceptance is the team's step

## Non-Goals

- not a pack write; `baselinedocs-save` records that an ADR exists
- not a review or acceptance of an ADR
- not a read of the whole pack; `baselinedocs-onboard` and `baselinedocs-load` do that
- does not decide which decisions deserve an ADR beyond the significance check in step 3
