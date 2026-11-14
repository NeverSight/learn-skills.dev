---
name: council
description: Gather independent opinions from a council of models when the user, guidance, or another skill asks for a council on a question, decision, plan, design, document, or code. The request can set members, goal, and criteria; otherwise an independent designer agent designs the council, starting from Astra, Sol 6.1, Opus 5.5, and Fable 5.2. An explicit merge council request belongs to merge-council.
---

# Council

Use independent opinions from several models to help answer the request. You coordinate and synthesize in the current thread. You do not design a council for your own question or work: a separate designer does, so the lineup and criteria do not favor your preferred answer.

## Design the council

The request may set any of these. A user, global guidance, or a calling skill such as `hill-climb` can make the request.

- **Goal:** the question to decide or the output to produce.
- **Criteria and constraints:** what makes an answer useful, and limits it must respect.
- **Members:** a model and effort for each, and optionally a lens, such as security, user experience, or maintainability.
- **Rounds:** one by default.

Use the fields the request sets as given. When the request names the lineup, frame the remaining fields from the request without a designer.

When the request leaves the lineup open, start one designer before the members: Fable 5.2 at high effort, read-only, with no further delegation. If it is unavailable, use Astra. Send it the request in the requester's words, the context and artifacts, the fields already set, the default lineup below, and the models the host can reach. Do not send your preferred answer. Ask it to return:

- The goal, criteria, and constraints.
- Each member's model, effort, and optional lens. Start from the default lineup and change it only for a reason the question gives. Include at least two providers when they are available. A lens adds focus to the full shared brief; it does not replace it.
- The number of rounds.
- Any question about the requester's goal or intent that no source answers and whose answer would change the design. The designer settles the lineup, lenses, and other internal choices itself.

Relay the designer's questions to the user and wait for answers. Then use its design unchanged, except for unavailable members as Convene describes. If no designer can run, use the default lineup and say so. State the design in one line when you launch.

## Frame the question

Give every member the same question, relevant context or artifact, constraints, and criteria for a useful answer. Preserve the user's uncertainty; omit your preferred answer. For changing artifacts, identify the version reviewed, such as commit SHAs and any uncommitted diff.

Council members advise read-only. A council request alone does not authorize implementation, publication, or merging.

## Convene

Default lineup, which the designer starts from:

| Member | Model | Effort |
| --- | --- | --- |
| Astra | `gpt-6-astra` | high |
| Sol 6.1 | `gpt-6.1-sol` | high |
| Opus 5.5 | `claude-opus-5-5` | high |
| Fable 5.2 | `claude-fable-5-2` | high |

In T3 Code, resolve targets with `orchestrator_capabilities`, then use `delegate_task` for each member. Search for an omitted model before declaring it unavailable. Map effort through the model's advertised `target.options`. These defaults use two models from each of two providers; more providers are not required.

Elsewhere, use the host's subagent tools only when they can reach the requested models and effort.

Never silently substitute a model. If a member the requester named is unavailable, ask whether to change the lineup or proceed with fewer members. If the designer chose the member, replace it with a comparable model from an available provider, such as Astra for Fable 5.2 or Sol 6.1 for Opus 5.5, or drop it, and report the change. A council needs at least two members. If a member fails after launch, retain the completed opinions and label the council incomplete.

Launch the members in parallel with separate contexts and no access to each other's responses. Each brief includes:

- The shared question, context, constraints, and criteria, plus the member's lens if it has one.
- Read-only responsibility, permitted sources, and any relevant instruction files.
- A request for a recommendation, a score from 0 to 10 for confidence that it is right, supporting evidence or reasoning, the strongest objection or alternative, and material uncertainties. A calling skill may replace the score with its own, such as a judge's vote or scorecard.
- A direction to do the work themselves without further delegation.

Follow the host's completion mechanism and collect every member's response before synthesis. Check each response against the evidence as it arrives, and change nothing a running member still reviews. Do not wait for a member the requester marks non-blocking; synthesize without it and name it as pending in the answer and the report. One round is the default. Run another only when the user requests it or a specific unresolved question warrants it within the authorized task.

## Synthesize

Check consequential claims against available evidence. Weigh reasoning rather than counting votes; keep material dissent visible.

Return a concise answer with:

- The recommendation and its rationale.
- Each member's position, attributed to the model that actually ran.
- Useful agreement, disagreements, and uncertainties that affect the decision.
- The next action, including any decision the user must make.

Report missing members or unverified model settings beside the conclusion. Council advice remains tied to the question and artifacts supplied. Continue any separately authorized work under its existing constraints.

## Report

Write a report for every council run, including runs a calling skill convenes, and link it in your answer. Use the path the requester gives, otherwise `${TMPDIR:-/tmp}/council/<UTC timestamp>-<subject-slug>/report.md`, a temporary location like the run directories of `merge-council` and `hill-climb`. A requester who needs a lasting record names a path. Invoking the skill authorizes this one file.

The report contains:

- The question, criteria, and reviewed version of any artifact.
- The design: who set it (requester or designer), and each member's model as it actually ran, effort, and lens.
- One table per round, with one row per member: position, score, and strongest objection. Mark a missing or late member.
- The outcome: the recommendation or the calling skill's verdict, material dissent, and the next action.

When a calling skill keeps its own record, such as a ledger, link it instead of copying its detail. Write summaries only: no transcripts, credentials, or full source.
