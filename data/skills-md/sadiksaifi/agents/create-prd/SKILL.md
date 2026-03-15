---
name: create-prd
description: >-
  Generates a product requirements document through interactive planning.
  Supports iterative discussion or ingestion of prepared material. Outputs
  to a local file or GitHub issue. Use when creating a PRD, writing a
  feature spec, planning a feature, or when the user says "create PRD,"
  "write PRD," "feature spec," or "/create-prd."
compatibility: gh CLI (authenticated) required for GitHub issue output
---

<HARD-GATE>
Do NOT generate a PRD until you genuinely understand the feature. A premature PRD full of vague bullets wastes more time than no PRD at all. Complete Steps 1–3 first.
</HARD-GATE>

## Anti-Pattern: "Premature PRD"

Jumping straight to document generation produces generic, placeholder-heavy output. Even a "simple" feature has unstated assumptions about users, scope, and success criteria. The exploration steps exist to surface those assumptions — skip them and the PRD will need a full rewrite.

## Process

### 1. Understand the request

Read the user's feature request. If unclear, ask for a one-sentence description of what the feature does and who it's for.

### 2. Choose exploration path

Ask the user:

> How would you like to explore this feature?
>
> **(A) Discuss interactively** — I'll ask questions one at a time to build understanding
> **(B) Provide prepared material** — share docs, notes, or context you already have

#### Path A: Discuss interactively

- One question per message — build on previous answers
- Focus on: target users, desired behavior, scope boundaries, success criteria, constraints
- Prefer multiple-choice questions; open-ended when choices aren't obvious
- Continue until the user signals readiness or you have enough to draft

#### Path B: Prepared material

- Read everything provided (docs, notes, prior art, screenshots)
- Only ask follow-ups if genuine gaps exist — don't re-ask what's already answered
- Summarize your understanding in 3–5 bullets
- Ask: **"Continue with this understanding, or discuss further?"**
  - If "discuss further" → switch to Path A

### 3. Confirm readiness

<HARD-GATE>
Summarize key decisions, scope boundaries, and non-goals. Ask the user to confirm before generating. Do NOT proceed to Step 4 without explicit approval.
</HARD-GATE>

### 4. Generate PRD

Load the [PRD template](references/prd-template.md) and fill every section with specifics from the exploration.

**Writing guidelines:**
- Explicit and unambiguous — write for junior developers and AI agents
- Number all requirements (FR-1, FR-2, …)
- Acceptance criteria must be verifiable, not vague (good: "Button displays 'Save' text"; bad: "Button looks good")
- No placeholders — if a section genuinely doesn't apply, write "N/A" with a brief reason
- Reference the user's own language and examples from the exploration

### 5. Approve and deliver

<HARD-GATE>
Present the full PRD for review. The user must approve content AND choose an output format before delivery. Do NOT publish without explicit approval.
</HARD-GATE>

Ask:

> **Approve this PRD?** Deliver as:
>
> **(A) GitHub issue** — creates an issue for tracking
> **(B) Local file** — saves to `prds/`
>
> Or request edits.

#### Option A: GitHub issue

```bash
gh issue create --title "PRD: [Feature Name]" --body "$PRD_CONTENT"
```

Print the issue URL. Mention `/prd-to-issues` for decomposing the PRD into implementation issues.

#### Option B: Local file

Save to `prds/[feature-name].md`. Print the file path.
