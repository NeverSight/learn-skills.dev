---
name: acceptance-criteria-define
description: Use when an agent is asked to define, review, or write acceptance criteria for a request or plan. Derives acceptance criteria from the current request context, confirms them with the user, and writes them into the plan file or a standalone acceptance_criteria.md file.
---

# Acceptance Criteria: Define

## Step 0: Check for Context

If no request or task description was provided as context (the skill was invoked with no arguments and nothing in the conversation describes a feature, task, or plan to evaluate):

- Output: "This skill needs a request or task description as context. Please describe the feature or task you want acceptance criteria for, or point me to a plan file."
- **STOP — do not continue.**

---

## Step 1: Identify the Plan File (if any)

Check whether the context references an implementation plan file:

- Look for a file path ending in `.md` mentioned in the request or conversation (e.g., `.agents/plans/feature-name.md`)
- Look for any `.agents/plans/*.md` file that matches the feature being discussed

**If a plan file is identified:**
- Read the entire plan file now
- Scan for an existing `## ACCEPTANCE CRITERIA` or `## Acceptance Criteria` section
- If found, extract and note the existing criteria — these are your starting point
- Also scan the `## TESTING STRATEGY`, `## VALIDATION COMMANDS`, and `## Feature Description` sections to understand the full scope

**If no plan file:**
- Proceed with the request description from conversation context only

---

## Step 2: Derive Acceptance Criteria

Based on the context (plan file, feature description, or request in conversation), derive the acceptance criteria.

**Think through each of these dimensions and produce criteria for whichever apply:**

### Functional Correctness
- What must the feature actually do? (the happy paths)
- What inputs/outputs define success?
- What specific behaviors are required vs. optional?

### Error Handling & Edge Cases
- What happens on bad input, missing data, or failures?
- What state should the system be in after an error?

### Integration & End-to-End Flow
- What connected systems must work together for the feature to be considered complete?
- What does "it works" look like from the user's perspective end-to-end?

### Validation & Test Coverage
- Which test levels are required: unit, integration, E2E?
- What automated validation commands should pass before accepting the work?
- Are there manual steps required for final verification?

### Non-Functional Requirements
- Performance: any latency, throughput, or load requirements?
- Security: any auth, data handling, or secret management requirements?
- Observability: logging, error reporting, tracing requirements?

### Not In Scope
- Explicitly list what is NOT expected — this prevents scope creep during review

**Format each criterion as a concrete, testable statement, not a vague goal.**

Good: "The `/mcp/mcp` endpoint returns HTTP 200 with a valid MCP tools list when the server is running"
Bad: "The server should work correctly"

---

## Step 3: Present Criteria to User

Output your derived criteria in a clear, readable list. Use this format:

```
## Proposed Acceptance Criteria

### Functional
- [ ] <criterion>
- [ ] <criterion>

### Error Handling
- [ ] <criterion>

### Integration / E2E
- [ ] <criterion>

### Validation
- [ ] <criterion> — verified by: `<command or test>`

### Out of Scope
- <item> — not required for this task
```

Then use **AskUserQuestion** to ask the user:

Question: "Do these acceptance criteria look right, or would you like to define them yourself?"
Options:
1. "Looks good — use these" — proceed with the proposed criteria as-is
2. "I want to add/change something" — user will provide modifications in free text
3. "Let me define them myself" — skip the proposed criteria entirely and wait for the user to write their own

---

## Step 4: Finalize the Criteria

**If user selected option 1 (use as-is):**
- Use the proposed criteria verbatim

**If user selected option 2 (add/change):**
- Read the user's modifications from their reply
- Merge them with the proposed criteria:
  - Additions: append to the relevant section
  - Changes: replace the relevant criteria
  - Removals: remove any criteria the user rejected
- Output the final merged list to the user before writing

**If user selected option 3 (define themselves):**
- Wait for the user to provide the criteria
- Do not invent or add criteria they did not provide
- Use exactly what the user wrote

---

## Step 5: Write the Criteria

### Case A: A plan file was identified

Rewrite the `## ACCEPTANCE CRITERIA` section at the bottom of the plan file.

- If the section already exists: replace its entire contents with the final criteria
- If the section does not exist: append it before `## COMPLETION CHECKLIST` if that section exists, otherwise at the very end of the file
- Use the exact heading `## ACCEPTANCE CRITERIA`
- Format each criterion as a `- [ ]` checkbox item
- Include the "Out of Scope" list as a plain bullet list (not checkboxes) under a `### Out of Scope` subsection

**Use the Edit tool to make this change — read the file first if you have not already.**

After writing, output: "Acceptance criteria written to `<plan-file-path>`."

---

### Case B: No plan file — write to `acceptance_criteria.md`

**Check if `acceptance_criteria.md` exists in `.agents/` (preferred) or the project root.**

#### If the file does NOT exist:
Create `.agents/acceptance_criteria.md` with this structure:

```markdown
# Acceptance Criteria

---

## <short title derived from the request> — <date>

### Context
<2–4 sentence summary of the request or feature this criteria applies to>

### Criteria

#### Functional
- [ ] <criterion>

#### Error Handling
- [ ] <criterion>

#### Integration / E2E
- [ ] <criterion>

#### Validation
- [ ] <criterion> — verified by: `<command>`

#### Out of Scope
- <item>
```

#### If the file ALREADY EXISTS:
Read the file first. Append a new section after the last existing section:

```markdown
---

## <short title derived from the request> — <date>

### Context
<summary>

### Criteria
...
```

Do NOT modify any existing sections.

After writing, output: "Acceptance criteria written to `.agents/acceptance_criteria.md`."

---

## Step 6: Summary

Output a brief confirmation:

```
Acceptance criteria saved.

File: <path>
Criteria: <N> items
Next step: Run /execute <plan-file> to implement, or share the criteria with the agent executing this work.
```

If this skill was invoked as part of a planning or execution flow, return control to the calling skill now.
