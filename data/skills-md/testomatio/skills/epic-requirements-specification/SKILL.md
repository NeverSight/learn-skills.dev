---
name: epic-requirements-specification
description: Use to interactively define and scope a project as an Epic, asking one question at a time. Generates a Markdown file, syncs via MCP, and handles the User Story handoff upon approval.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

## Phase 1: Interactive Discovery

1. **One Question Policy:** You are strictly locked in an information-gathering state. Analyze the user's input, map it to the structure in the background, and ask exactly **one focused question at a time** to fill missing or ambiguous gaps.

2. **Absolute Tool Lock:** Do not call any MCP tracking tools, do not create Jira tickets, and do not write markdown files to the workspace during this phase.

3. **Minimal Input Handling:** If the user's input is extremely short or vague (e.g., "create blue cup"), do not assume the interview is finished. Instead, treat it as a trigger to ask your very first clarifying question about the core business context.

4. **Sequential Progress:** Wait for the user's explicit response to the current question before moving to the next topic. Do not invent business facts; use `[Assumption]` or `[Open Question]` if the user chooses to skip a point.

5. **Epic Scope:** Keep all questions at the business and capability level. Do not ask for technical implementation details, APIs, database schemas, or UI rules.

## Phase 2: Draft Review & Approval Gate

1. **Draft Presentation:** Only when all key sections are covered, or if the user explicitly asks to see the draft, output the complete Epic Specification text inside the chat window for review.

2. **The Execution Trigger:** You are legally permitted to move to Phase 3 and run automation tools **ONLY IF** the user explicitly reviews the text draft and types the exact word: **APPROVED**. If they ask for changes, update the text draft and request approval again.

## Phase 3: Post-Approval Execution

1. **File Persistence:** Once approved, write the finalized text to a Markdown file (`epic-<slug>.md` or `project-<slug>.md`) in the workspace.

2. **Next Actions Offering:** Do not automatically sync to tracking systems. Instead, report the saved file path and present a "Next Actions" section at the bottom asking the user to explicitly confirm which follow-up steps they want to trigger next.

## Output Specification

The final document generated at the end of the loop must use the following Markdown structure:

### 1. Business Context
* **Business Problem:**
* **Business Goal:**
* **Business Value:**
* **Success Criteria / KPIs:**

### 2. Scope & Stakeholders
* **Target Users / Actors:**
* **End Beneficiaries:**
* **In Scope:**
* **Out of Scope:**

### 3. Constraints & Risks
* **Dependencies:**
* **Constraints:**
* **Critical Risks:**
* **Assumptions:**
* **Open Questions:**

### 4. Analyst's Insights
Include only when there are meaningful gaps, contradictions, or risks identified during the interactive loop.

## Interaction Model

* **During Phase 1 (Discovery):** State what you have captured from the user's last message and present your **single next question**. Do not output the markdown document structure or code blocks yet.
* **During Phase 2 (Review):** Present the complete text draft inside the chat and explicitly ask the user for confirmation.
* **During Phase 3 (Execution):** Report the saved file path and present the "Next Actions" choices at the bottom. Ask: *"The Epic is saved as a file. What would you like to do next?*
    * *1. Sync this Epic to the tracking system (MCP)*
    * *2. Break down this approved Epic into the first User Story using the `write-user-story` skill*
