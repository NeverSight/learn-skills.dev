---
name: lead-orchestrator
description: Coordinate implementors and their review teams across repositories, track design decisions and dependencies, and prepare delivered changes for the user's merge decision. Use only when the user explicitly invokes lead-orchestrator or asks to use this skill. Review-only requests belong to review-orchestrator.
---

# Lead orchestrator

Run this workflow only when the user explicitly invokes lead-orchestrator or asks to use this skill. An ordinary request to lead or orchestrate implementation does not activate it.

Own the overall outcome while implementors own their changes and review orchestrators own their review teams. Coordinate through the current conversation. Do not assume this conversation's project is the repository being changed.

Select by the requested responsibility, not the verb "lead" or "orchestrate". A request to orchestrate a review of an existing PR/MR belongs to review-orchestrator. Use this skill when responsible for getting changes implemented and through review, including coordinating fixes and dependencies toward delivery.

## Establish the assignment

Resolve the objective, acceptance criteria, target repositories and host URLs, workspace or remote environment, base branches, existing work, and requested implementor and review models. Infer reliable context before asking for missing information. Read applicable instructions in each target repository; instructions and permissions from the coordinator's project do not automatically transfer.

Record a compact plan with workstream owners, dependencies, design questions, verification expectations, and permission boundaries. Use the smallest useful team. Reuse existing authorized work rather than starting competing implementors or review teams. Creating this skill's team is authorized when the user invokes it to orchestrate work; select child tasks or separate threads according to the user's requested execution mode and the environment's rules. Do not treat a request for delegation as authorization to create top-level threads when the environment distinguishes them.

Discover available providers, models, workspace binding, host access, and execution capabilities before launch. Honor explicit settings per implementor, review orchestrator, and reviewer instance, including phase-specific design versus coding choices. Use the review-orchestrator model precedence and `exact`, `preferred`, and `auto` policies when available. Otherwise default to the current model for omitted settings and treat named models as exact unless the user permits substitution. Explain any automatic selection briefly. Never silently change an explicit model or execution mode. A missing provider blocks only work that needs it.

Use supported workspace selection when launching work elsewhere. A repository path in a prompt does not bind a thread to that workspace. Verify the actual binding and base before authorizing edits. Independent work normally starts from the target's default branch; dependent work may require an exact unpublished parent commit. Keep repository, branch, workspace, host URL, and coordinator project separate in the record.

## Keep coordination private and useful

Give each team only its assignment, relevant decisions, dependencies, acceptance criteria, permissions, and the lead's return channel. Do not provide sibling thread IDs, links, transcripts, or a team directory unless a concrete task requires that information. Prefer a short factual dependency summary with commit or PR evidence. Use fresh context rather than inherited coordinator history where the interface permits it.

Tell every implementor and review orchestrator:

> Route coordination affecting broader work through the lead. Do not discover, read, message, or start sibling workstream threads. Ask the user directly in your own thread when input is needed; needing user input does not require the lead's intervention. Make routine decisions within your scope. Notify the lead about decisions affecting broader design, scope, dependencies or other workstreams, team blockers, and meaningful status or readiness changes. Report relevant outcomes rather than routing each conversation through the lead. Batch routine progress; do not announce every edit or wait. Never merge or enable auto-merge without the lead relaying explicit user authorization for this request.

A review orchestrator may coordinate its own specialist reviewers under review-orchestrator. Apply the sibling-workstream restriction to those reviewers too. The review team's designated posting owner must put actionable findings, implementation questions, fix requests and follow-up in code-review comments. Internal validation and deduplication remain within that team. The lead must not relay these to the implementor. An ordinary defect does not require lead involvement merely because it blocks merge. Status reports may link to findings without requesting a relay. If posting fails, report the access blocker and retain findings for posting rather than silently switching channels. Honor explicit read-only or alternate-routing instructions from the user.

Retain peer identities centrally for recovery and user visibility. Withholding them from worker briefs does not mean hiding team activity from the user.

## Preserve decisions and ownership

Maintain a durable checkpoint outside installed skills and unrelated target checkouts, using available app storage or a user-local file. Record:

- Workstream IDs, scope, target repository/workspace/base, execution handles, actual models, PR/MR URLs, phase, and last meaningful status.
- Accepted decisions, their user or evidence source, superseded proposals, unresolved questions, and dependent workstreams.
- Current implementation head, reviewed heads and coverage, verification results, blockers, host-comment ownership, and monitor registrations.
- Merge authorization, its scope and conditions, and any separate release or publication authorization.

Store decisions as concise contracts and examples, not transcripts. Distinguish user-approved behavior, implementor proposals, prototype limitations, and missing agreed functionality. A prototype omission does not reopen an accepted requirement. Share relevant decisions with affected owners and confirm receipt for material handoffs.

Let teams settle local details and ask the user directly about choices that change agreed behavior, public contracts, scope, dependencies, or a user's stated tradeoff. Have them report resulting decisions to the lead when they affect broader coordination; the lead coordinates consequences without becoming a mandatory approval channel. Reconcile conflicting answers or superseded requirements before clearing dependent work. Do not turn an unanswered design question into an assumed acceptance criterion.

Assign one writer per branch or overlapping change area. Prefer separate supported workspaces for concurrent edits and verification. Dependent design can proceed against a named provisional base while coding remains held. State exactly what releases each hold; design agreement, implementation clearance, dependency merge, and release approval are separate events.

## Implement and review

Write each brief for its assignment. Include relevant accepted decisions, scope and acceptance criteria, target workspace and exact base or review head, dependencies and holds, model settings, permissions, and the lead's reporting channel. Pass accessible contracts and evidence rather than assuming workers can read the original conversation or local configuration paths. Include the coordination boundaries above without sharing sibling identities. Apply pr-implementor-babysitter when available for author follow-up, subject to the assignment's permission boundaries.

Once a PR/MR is reviewable, explicitly invoke `$review-orchestrator` in the review team's brief. Pass the actual request URL, target workspace, relevant accepted design, exact candidate head, model choices, review terms, and the lead's reporting channel. Resolve that skill's installed instructions and configuration rather than copying its roster or scorecard into this skill. If unavailable, report the limitation and arrange a supported review alternative with the user; do not claim that workflow ran.

Keep review assessment independent. Provide requirements and source evidence without priming reviewers to agree with an implementor's conclusions. Let the review orchestrator own specialist selection, deduplication, posting, and follow-up under its skill. Let implementors own fixes and ordinary replies. The lead resolves cross-team conflicts and design implications; it does not duplicate their host comments or monitors.

Reviewers report concerns against exact commits. After pushes or rebases, route relevant changes back through the review orchestrator and mark old assessments stale until it confirms coverage of the new head. Batch pushes into useful review rounds rather than restarting every reviewer per commit. A final readiness claim needs all required scopes accounted for at the current head, including integration effects between workstreams. Passing CI or agreement among reviewers alone is insufficient.

When review and fixes stop converging, summarize the disputed evidence and tradeoff for the user instead of spawning more opinions indefinitely. Honor user budgets or round limits and preserve blockers when a limit is reached. Cancel superseded work through the supported lifecycle; do not leave competing assignments active.

## Prepare the user's decision

Default to awaiting the user's own review and explicit merge permission. Neither reviewer approval, a readiness score, green checks, nor "continue" authorizes merging. Do not merge, approve on the user's behalf, enable auto-merge, or permit another team to do so under this default.

The user may grant a specific exception or standing permission. Record the exact request, reviewed head or scope, and conditions. Permission for one request does not transfer to another. A substantial behavior or design change after the user's review requires renewed human review unless their authorization explicitly covers it. Refresh host state and checks immediately before any authorized merge. Publishing packages, releases, or deployments requires its own authorization; merge permission does not imply it.

Present a compact readiness report with the PR/MR links and heads, delivered behavior, remaining design decisions, review coverage and unresolved disagreements, verification limits, host blockers, and a recommendation. Separate technical readiness from human review and merge permission. When ready, ask for the user's review or merge decision on that concrete result. Continue authorized fixes and review follow-up while permission remains pending.

Post concise status and progress reports in the lead's conversation when overall progress changes substantially or something important arises, including a blocker, a dependency becoming ready, or work waiting for the user. Summarize what changed, current workstream status, blockers or pending input, and what happens next. When waiting for the user, identify the needed decision or action and link to the team thread or review discussion where it belongs; do not move the conversation to the lead unnecessarily. Batch related events and skip repeated unchanged reports. Continue independent work while a team waits.

Use supported event monitoring for work that must wait, with a named owner and coverage. Do not report active monitoring until registration succeeds. Follow the environment's wait and handback rules; if monitoring is unavailable, state what event needs a new invocation. On recovery, reconcile the checkpoint with actual executions, heads, host discussions, and decisions before launching anything again. Stop obsolete monitoring when the work ends.
