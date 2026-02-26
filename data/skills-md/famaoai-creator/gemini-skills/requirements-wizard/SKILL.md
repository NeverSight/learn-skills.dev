---
name: requirements-wizard
description: Guide for creating and reviewing requirements definitions based on IPA standards. Provides best practices for business analysis, process mapping, data modeling, and review checklists.
status: implemented
category: Engineering & DevOps
last_updated: '2026-02-13'
tags:
  - analytics
  - data-engineering
  - gemini-skill
---

# Requirements Wizard (IPA-Standard)

This skill provides expert guidance for Requirement Definition (RD) phases, leveraging IPA (Information-technology Promotion Agency, Japan) best practices.

## Capabilities

### 1. Best Practice Advisory

Consult the IPA-aligned knowledge base for advice on:

- **Business Requirements**: Stakeholder mapping, objective structuring (Why/What/How).
- **Process Visualization**: Hierarchical workflow design (Business vs. System levels).
- **Data Modeling**: Conceptual ER diagrams and CRUD analysis.
- **UI/UX Design**: UI standards and screen transitions.
- **Non-Functional Requirements**: Using IPA grades and defining metrics.

### 2. Document Review

The skill uses structured checklists to audit requirements documents following the `knowledge/orchestration/knowledge-protocol.md`:

- **Hybrid Lookup**: Checks `knowledge/` (Public) AND `knowledge/confidential/` (Private).
- **Precedence**: Internal confidential policies override general IPA/FISC standards.
- **Safety**: Proprietary details found in the confidential tier must be summarized or masked when generating public reports.

## Knowledge Base Locations

- **IPA Best Practices**: `knowledge/requirements-guide/ipa_best_practices.md`
- **AI Best Practices**: `knowledge/ai-engineering/best_practices.md`
- **Review Checklists**:
  - General: `knowledge/requirements-guide/review_checklist.md`
  - AI-Specific: `knowledge/ai-engineering/review_checklist.md`

## Usage Examples

- "Review my current requirements definition in `docs/rd.md` using the IPA checklist."
- "How should I structure my business process flow according to the IPA guide?"
- "Help me define the non-functional requirements for a high-availability banking API."

## Workflow Focus

1.  **Analyze**: Understand the current context and project scope.
2.  **Refer**: Retrieve relevant best practices from the knowledge base.
3.  **Advise/Verify**: Provide specific improvements or check for gaps using the review checklist.

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
