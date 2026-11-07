---
name: write-prd
description: Product requirements decision capture and GitHub issue creation. Use only when a human explicitly invokes `$write-prd`; never select this skill automatically from feature, planning, PRD, or issue-creation task similarity. When explicitly invoked, define or finalize a PRD, turn a feature idea into a decision-complete GitHub issue, and resolve applicable product, technical, operational, rollout, observability, support, documentation, and testing decisions.
---

# Write PRD

## Goal

Turn a feature request into a complete PRD-backed GitHub issue. Do not invent material defaults. Every applicable functional and operational decision must be answered by the user, explicitly marked not applicable by the user, or directly determined by an authoritative repository contract before creating the issue.

## Required References

Read these files before asking PRD questions or writing the issue:

- `references/question-ledger.md` for the required decision ledger.
- `references/issue-template.md` for the fallback GitHub issue shape.

## Operating Rules

- Follow all active system, developer, repository, and scoped instructions.
- Read the target repository's authoritative docs, contracts, contribution guidance, issue templates, and metadata conventions for the affected area before finalizing decisions.
- Resolve the GitHub target from an explicit repository or issue URL, otherwise from the current Git remote. Ask the user before filing when no unique target can be established.
- Determine whether a feature flag applies from an explicit user decision or repository contract. Allow the user to mark feature flags not applicable with a stated reason unless a repository contract requires one.
- When a feature flag applies, require its complete contract before finalizing or filing the issue. Treat it only as a rollout control, never as a substitute for authorization, tenancy, billing, budget, resource state, or other safety enforcement.
- Do not invent a flag key, rollout percentage, cohort, timing, or removal threshold.
- Use `gh` for GitHub issue operations when possible.
- Inspect the target repository's labels before filing. Apply `PRD` when that label already exists or when the repository contract or user requires it. Do not create labels. If `PRD` is absent and not required, file without it.
- Follow repository-required issue metadata. Do not add unrelated labels, assignees, milestones, project fields, issue types, or other metadata without an explicit user request or repository requirement. If required metadata cannot be applied, report the conflict and do not file.
- Ask questions in small batches. Prefer grouped, concrete questions that close decision-ledger rows.
- Do not close a ledger row with an inferred default, common practice, or agent preference. A row closes only through an explicit user answer, explicit user-approved `not applicable`, or an authoritative contract that directly determines the answer.
- If a repository contract determines a row, cite the path or command evidence in the ledger and ask the user only when product intent remains open.
- If the user asks to skip a category, record it as explicitly out of scope or not applicable with the user's stated reason.
- Do not create the GitHub issue while any applicable ledger row remains open.

## Question Presentation

- In every mode, including T3 Code Build mode, present decision questions with concrete choices when meaningful alternatives exist. Offer a small set of distinct options and briefly explain each option's effect or tradeoff. Allow a custom answer; use free text when the decision requires an exact name, value, or detail that choices cannot capture.
- Use a structured question tool when it is available and permitted in the active mode. In Build or Default mode, prefer `request_user_input_async` when available. Use `request_user_input` only when the active tool instructions permit it; do not switch to Plan Mode just to ask questions.
- If no permitted question tool is available, or the tool rejects the active mode, ask in chat with numbered questions and lettered choices. Keep custom answers possible in this fallback too.
- Follow the selected tool's schema and batch limits. A recommendation explains a candidate choice; it does not decide the ledger row. A preselected option, missing response, or elapsed wait is not a user answer.
- With an asynchronous question tool, continue only independent investigation while the answer is pending. Keep dependent ledger rows open and resume collection when the user replies; do not submit duplicate questions while the same request is pending.

## Workflow

1. Ground the request.
   - Identify the feature idea, affected product or domain, likely repository contracts, and issue target.
   - Read applicable docs, schemas, interfaces, existing issues, nearby code, and issue templates needed to avoid asking discoverable questions.
   - Determine feature-flag applicability and initialize a visible decision ledger using `references/question-ledger.md`.

2. Collect decisions.
   - Ask only questions that materially close open ledger rows, following Question Presentation in the active mode.
   - Keep asking until every applicable row is answered, explicitly not applicable, or contract-determined.
   - After each user answer, update the ledger. If applicable rows remain open, perform any needed read-only investigation and ask the next small batch of questions in the same turn; do not wait for a separate request to continue.
   - Reconcile contradictions immediately and track evidence, open questions, and user answers separately. Partial or ambiguous answers leave the affected decisions open and require follow-up questions, not inferred defaults.
   - While applicable rows remain open, do not end with only a progress summary, draft, or final plan, ask whether to continue, or request a mode switch to continue collecting decisions. Pair progress summaries with the next questions using the available question mechanism.
   - Honor an explicit user request to pause or stop. If a real access blocker prevents progress, explain what is missing and how it can be resolved, but continue investigating and asking independent questions before ending for that blocker.

3. Handle Plan Mode.
   - Plan Mode does not stop decision collection: continue read-only investigation and questions under step 2. Perform no GitHub write or other mutation prohibited by the active mode.
   - Prefer `request_user_input` when available and permitted in Plan Mode, following Question Presentation for choices and fallbacks. Waiting for a user answer is part of the collection loop; after the answer arrives, resume the loop automatically.
   - Only when every applicable ledger row is closed, return a final plan containing the exact issue title, body, target, metadata to apply, and later `gh` action, following the active mode's required output format.
   - When later running outside Plan Mode from a complete prior plan, create the issue without asking for another confirmation.

4. Write the PRD issue.
   - Follow the target repository's issue style and template when present; otherwise use `references/issue-template.md`.
   - Include functional and operational decisions without adding unsupported choices.
   - When a feature flag applies, include its complete contract and observable default, enabled, disabled, evaluation-failure, targeting, rollback, and lifecycle behavior.
   - Keep the issue implementation-ready with concrete scope, acceptance criteria, test scenarios, and explicit out-of-scope boundaries.

5. File the issue.
   - Outside Plan Mode, inspect available labels and required metadata, then create the issue when the ledger is complete.
   - Add `--label "PRD"` only when the label exists or is explicitly required. Add other metadata only when explicitly requested or required by the repository.
   - Use a temporary body file or another safe quoting approach for multiline Markdown.
   - Report the created issue URL, title, target repository, applied metadata, and any follow-up risk.

## Useful Commands

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
gh issue list --repo "$OWNER_REPO" --search "$SEARCH_TERMS" --state open
gh label list --repo "$OWNER_REPO" --search "PRD"
gh issue create --repo "$OWNER_REPO" --title "$TITLE" --body-file "$BODY_FILE"
gh issue create --repo "$OWNER_REPO" --title "$TITLE" --body-file "$BODY_FILE" --label "PRD"
```

Use quoted shell variables and file paths in commands.
