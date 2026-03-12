---
name: software-requirements
description: >-
  Write professional software requirements documents (SRS, PRD, BRD, FRD, User
  Stories, Use Cases). Use when a user asks to write requirements, create an SRS
  or PRD, turn a feature description into user stories, generate acceptance
  criteria, review an existing requirements document, or convert an informal idea
  into structured requirements. Also trigger when the user mentions "acceptance
  criteria", "functional requirements", "non-functional requirements", or
  "requirements traceability matrix".
---

# Software Requirements Analysis

Write professional, comprehensive, and unambiguous software requirements documents
that development teams can build from, QA teams can test against, and stakeholders
can approve with confidence.

## Input Handling

Determine the input type and respond accordingly:

1. **Informal description** -- User describes what they want to build in plain
   language (e.g., "I need a login page with password reset"). Expand this into
   structured requirements by following the discovery and writing phases.

2. **Existing document to review** -- User provides an existing requirements
   document for critique. Skip discovery, proceed to Requirements Review Mode.

3. **"Write me an X" request** -- User explicitly asks for a specific document
   type (e.g., "Write me an SRS for my payment system"). Skip discovery if the
   scope is clear; proceed to document type selection and writing.

4. **Feature request for user stories** -- User wants user stories + acceptance
   criteria for a specific feature or sprint. Use the User Story template from
   the document types guide.

## Discovery Phase (Phase 1)

Before writing any requirement, you MUST gather context using these 7 questions.
If the user has already provided some information, acknowledge what you know and
ask only about what's missing. Do not skip this phase.

Ask the user to clarify:

1. **System/Product**: What is being built? What is explicitly IN scope and OUT
   of scope?
2. **Stakeholders**: Who are the end users, admins, operators, external systems,
   regulators?
3. **Problem**: What specific problem does this solve? Why does it need to exist?
4. **Constraints**: Technology stack, budget, timeline, regulatory requirements
   (GDPR, HIPAA, PCI-DSS, SOX, ADA), existing systems to integrate with, legacy
   dependencies?
5. **Document Type**: What kind of document do they need? (If unsure, recommend
   based on their context.)
6. **Delivery Format**: .docx, markdown, wiki, JIRA stories, Confluence page?
7. **Existing Materials**: Do they have wireframes, user research, competitive
   analysis, or existing documents to reference?

Explicitly surface every assumption and list them in the final document.

## Document Type Selection (Phase 2)

Read [references/document-types.md](references/document-types.md) before this
phase.

Based on the discovery phase, recommend the appropriate document type using the
decision heuristic. The reference file contains:
- Selection table (SRS, PRD, BRD, FRD, User Stories, Use Cases)
- Quick decision logic
- All 6 document templates

## Requirements Writing (Phase 3)

Read [references/requirement-writing-rules.md](references/requirement-writing-rules.md)
before this phase.

Write requirements using:

- **Language rules**: All requirements shall use "shall" (mandatory), "should"
  (recommended), or "may" (optional). Use active voice. Never combine behaviors
  with "and" or "or" in a single requirement. Specify exact quantities (e.g.,
  "within 2 seconds", not "quickly").
- **Requirement ID format**: Use hierarchical IDs like FR-AUTH-001, NFR-PERF-001,
  DR-001, IR-API-001
- **Required fields per requirement**: ID, Description, Rationale, Priority
  (Must/Should/Could/Won't), Source, Acceptance Criteria, Dependencies, Notes
- **Avoid banned words**: "should generally", "as appropriate", "etc.", "and/or",
  "user-friendly", "fast", "efficient", "robust", "seamless", "intuitive",
  "various", "some", "relevant", "adequate", "reasonable", "timely", "properly",
  "correctly", "easy", "simple", "normal"

Replace every instance of a banned word with a specific, measurable statement.

Input handling rules:
- For every INPUT: specify type, format, valid range, required vs optional,
  default value, max length
- For every OUTPUT: specify format, destination, timing, error format
- For every OPERATION: specify what happens on failure, timeout, invalid data,
  concurrent access, cancellation

Expand informal descriptions by at least 3x the original size. For example, a
one-sentence feature description should produce 20+ requirements covering
functionality, security, performance, accessibility, and compliance.

## Mandatory Coverage Areas (Phase 3 Continued)

For EVERY document, ensure ALL of these categories are addressed:

A) **Functional Requirements (FR)**: Core features, business rules, data
   validation, error handling, state transitions, batch processing, notifications

B) **Non-Functional Requirements (NFR)**: ALWAYS include ALL of these:
   - Performance: page load times, API response times, throughput, query latency
   - Scalability: max concurrent users, max data volume, growth rate
   - Security: authentication, authorization (RBAC/ABAC), encryption, audit
     logging, session management, CSRF/XSS/SQLi protection
   - Reliability: uptime target, MTTR, MTBF, failover strategy, disaster recovery
   - Accessibility: WCAG level (2.1 AA minimum), keyboard navigation, screen
     reader, color contrast
   - Usability: learnability, error recovery, user satisfaction benchmarks
   - Maintainability: logging standards, monitoring, deployment, code quality
   - Portability: browsers + versions, operating systems, devices, offline
   - Compliance: GDPR, HIPAA, PCI-DSS, SOX, ADA, COPPA, CCPA, industry regulations
   - Internationalization: languages, locales, RTL support, Unicode handling

C) **Interface Requirements (IR)**: User interfaces, API endpoints with schemas,
   hardware interfaces, third-party integrations

D) **Data Requirements (DR)**: Data models, retention policies, migration
   strategy, backup procedures, privacy classification, data quality rules

## Validation Phase (Phase 4)

Read [references/validation-checklist.md](references/validation-checklist.md)
before this phase.

Run the validation checklist against every requirement:

- [ ] AMBIGUITY SCAN: Search for banned words and replace with specific,
      measurable statements
- [ ] TESTABILITY CHECK: Can you write a pass/fail test for each requirement?
- [ ] COMPLETENESS CHECK: What about null/empty inputs, network failures,
      timeouts, disk full, malformed data, concurrent access, API unavailability,
      permission errors, session expiration?
- [ ] CONTRADICTION CHECK: Are any two requirements impossible to satisfy
      simultaneously?
- [ ] INTERFACE CHECK: Are all external interfaces completely specified?
- [ ] NFR CHECK: Are ALL non-functional categories addressed?
- [ ] PRIORITY CHECK: Is every requirement prioritized (Must/Should/Could/Won't)?
- [ ] GLOSSARY CHECK: Are all domain-specific terms defined?
- [ ] ASSUMPTIONS CHECK: Are all assumptions explicitly listed?
- [ ] SCOPE CHECK: Are out-of-scope items explicitly listed?
- [ ] TRACEABILITY CHECK: Does every requirement trace to a business objective?
- [ ] OPEN QUESTIONS: Are unresolved items captured with owners and target
      resolution dates?

Fix all issues before proceeding to delivery.

## Delivery Phase (Phase 5)

Structure the deliverable with:

1. **Main requirements document** -- Using the template from Phase 2 with all
   requirements, structured by category, with IDs, priorities, acceptance
   criteria, and cross-references

2. **Numbered Assumptions list** -- All implicit assumptions surfaced in discovery
   and planning, with risk assessment for each

3. **Open Questions log** -- Unresolved items with columns: ID, Question, Owner,
   Target Date, Status

4. **Appendices**:
   - Requirements Traceability Matrix (Requirement ID → Business Objective →
     Test Case ID)
   - Glossary of all domain-specific terms
   - Change Log (Version, Date, Author, Changes)

5. **Version block**: v0.1 Draft → v1.0 Approved as document matures

## Requirements Review Mode

When a user provides an existing requirements document for review:

1. **Read the entire document** before commenting
2. **Check each requirement** against the 7 Quality Principles (see references)
3. **Flag issues** with exact references:
   - **AMBIGUITY**: Quote the vague phrase → provide specific replacement text
   - **MISSING**: Identify the gap → suggest requirement text to fill it
   - **CONTRADICTION**: Cite both conflicting requirement IDs → recommend resolution
   - **UNTESTABLE**: Explain why → provide testable rewrite
   - **INCOMPLETE**: Identify missing error cases, edge cases, NFR categories
4. **Rate each issue**:
   - Critical: Blocks development
   - Major: Causes rework
   - Minor: Polish
5. **Summarize**: Issue count by severity, top 5 priority fixes, overall quality
   score (1-10)
6. **Rewrite the worst requirements** completely in your response

## Output Rules

- Requirements are WHAT, not HOW. Say "The system shall authenticate users" not
  "Use OAuth 2.0 with JWT" (unless technology is a genuine constraint).
- When expanding informal descriptions, produce at MINIMUM 3x the number of
  requirements the user described.
- ALWAYS include "What's Missing / Needs Stakeholder Input" section at the end.
- ALWAYS include a numbered Assumptions list.
- ALWAYS include an Open Questions log with owners and target dates.
- Version the document (v0.1 Draft → v1.0 Approved) and maintain a change log.
- Cross-reference related requirements by ID throughout.
- For formal documents: generate with table of contents, headers, page numbers,
  and requirement tables.
- For agile artifacts: format for direct import to JIRA/Linear/Shortcut.

## Guidelines

- Do not skip discovery. Do not assume. Surface every assumption explicitly.
- Never use banned words. Replace them with specific, measurable statements.
- Cross-reference related requirements by ID. For example: "See FR-AUTH-001 for
  session management requirements."
- When rewriting informal descriptions, surface hidden assumptions — list them
  and ask about each one.
- Break compound requirements into atomic single-behavior statements.
- Always add security, accessibility, and compliance requirements based on the
  domain, even if the user didn't explicitly ask.
- For very large documents (>100 requirements), divide into logical sections and
  provide a consolidated summary.
- When uncertain about user intent, state the assumption explicitly rather than
  making a silent judgment.
