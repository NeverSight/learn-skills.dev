---
name: scribe
description: Maintain product, architecture, and implementation docs — routes input, detects gaps, and interviews for completeness
tools:
  - question
  - read
  - write
  - edit
  - glob
  - grep
---

# Scribe

Use this skill to maintain documentation across multiple documents that represent different levels of abstraction. When the user provides input, analyze it and route it to the correct document. Scribe is not a passive filing system — after recording what the user provides, it actively identifies gaps, checks cross-document consistency, and asks targeted questions to strengthen the documentation.

## Document Discovery

Before processing input, locate the documentation files:

1. Search for existing files matching `PRODUCT.md`, `ARCHITECTURE.md`, and `IMPLEMENTATION.md` (case-insensitive) in:
   - Repository root
   - `docs/` directory

2. If documents exist, use their locations. If multiple matches exist for the same type, prefer the repository root.

3. If no documents exist, use these defaults when creating new ones:
   - `PRODUCT.md` in repository root
   - `ARCHITECTURE.md` in repository root
   - `IMPLEMENTATION.md` in repository root

## Document Types

**Product** - Product-level documentation
- What we're building and why
- User-facing value propositions
- Vision and goals
- Target users and use cases
- Business justification

**Architecture** - System architecture documentation
- How the system is structured
- Components and their relationships
- Abstractions and interfaces
- Data flow and control flow
- Design decisions that are technology-agnostic

**Implementation** - Implementation documentation
- Specific technology choices
- Protocols and formats
- Libraries and frameworks
- Concrete technical details
- Configuration and deployment specifics

## Using the Question Tool

Throughout this skill, you will use the `question` tool (also known as AskUserQuestion in some contexts) to interact with the user. The question tool allows you to present multiple questions with predefined options to the user.

**Key mechanics:**
- You can present multiple questions in a single tool call (as an array of questions)
- Each question has a header, question text, and multiple options
- Each option has a label and description
- Users can select one or multiple options (if `multiple: true`)
- The tool automatically includes a "Type your own answer" option by default
- Questions are answered together as a batch, but you should make options context-aware based on information you already have

**When to provide context-aware options:**
- Reference similar features, patterns, or components already documented
- Suggest options based on answers from previous interactions in the session
- Use project-specific terminology from existing documents
- When no patterns exist (empty/minimal documents), provide general options as fallbacks

**Example invocation:**

```json
{
  "questions": [
    {
      "header": "Document classification",
      "question": "Is 'fast and reliable' a user-facing promise or a system design requirement?",
      "options": [
        {
          "label": "User-facing promise",
          "description": "Add to PRODUCT.md like other user benefits"
        },
        {
          "label": "System design requirement",
          "description": "Add to ARCHITECTURE.md with latency targets"
        },
        {
          "label": "Both",
          "description": "It's a user promise AND a technical constraint"
        }
      ]
    },
    {
      "header": "Performance target",
      "question": "Does 'fast' have a concrete target?",
      "options": [
        {
          "label": "Under 5 seconds",
          "description": "Similar to report generation target"
        },
        {
          "label": "Different target",
          "description": "Specify a different performance goal"
        },
        {
          "label": "No specific target",
          "description": "Keep it qualitative for now"
        }
      ]
    }
  ]
}
```

The tool returns the selected options as an array of labels (e.g., `["Both", "Under 5 seconds"]`).

## Execution Steps

### Step 0: Document Discovery and Reading

Before classifying input, locate and read the existing documentation files to learn project-specific vocabulary and patterns. This information will be used throughout all subsequent steps for context-aware questioning.

1. Search for existing files matching `PRODUCT.md`, `ARCHITECTURE.md`, and `IMPLEMENTATION.md` (case-insensitive) in repository root and `docs/` directory
2. Read all existing documents to extract:
   - Key terms and component names
   - Patterns in how features are described
   - Existing constraints, limits, or policies
   - Similar features that can serve as templates
3. If documents are empty or minimal, note that general options will be needed instead of context-aware ones

### Step 1: Analyze Input

Read the user's input and determine which category it falls into. Classification is based on two sources: general heuristics and project-specific signals learned from existing documents (Step 0).

**General heuristics:**

*Product signals:*
- Describes user needs or problems
- Explains value or benefits
- Discusses market or competitive positioning
- Uses language like "users can", "enables", "provides value"
- Talks about goals without specifying how

*Architecture signals:*
- Describes components or modules
- Explains how parts interact
- Defines abstractions or interfaces
- Discusses system properties without naming specific technologies
- Technology-agnostic design decisions

*Implementation signals:*
- Names specific technologies, protocols, or formats
- Describes wire formats or API specifications
- Specifies configuration details
- Uses language like "uses", "built on", "implemented with"
- Concrete technical choices

**Project-specific signals:**

Read the existing documents to learn the project's vocabulary. Extract key terms, component names, and patterns that indicate document ownership. For example:
- If the architecture document discusses "the kernel" and "agents", mentions of these terms suggest architectural content
- If the implementation document discusses "SMTP" and "IMAP", mentions of email protocols suggest implementation content
- If the product document discusses "wallets" as a user-facing feature, wallet mentions in a value context suggest product content

Use these learned signals alongside general heuristics. Project-specific vocabulary takes precedence when it provides a clear signal.

### Step 2: Classify and Deepen

If the categorization is clear, proceed to update the appropriate document.

If the input is ambiguous or spans multiple categories, do not simply ask "which document?" Instead, use the `question` tool to interview the user and decompose the input into distinct claims that can each be routed precisely:

1. Explain what makes the input ambiguous — identify the product, architecture, and/or implementation aspects you see in it.
2. Use the `question` tool to ask targeted questions that separate those aspects. Based on the context you have from existing documents (Step 0) and the user's input, provide relevant options that help clarify the intent.

**If documents have content with patterns to reference:**
   - When user mentions "fast and reliable", reference existing performance promises or design constraints:
     - "User-facing promise (add to PRODUCT.md like [similar feature])"
     - "System design requirement (add to ARCHITECTURE.md with latency targets)"
     - "Both - it's a user promise AND a technical constraint"
   - When user mentions a component name, reference similar components:
     - "[Component] is user-facing (like [similar component] in PRODUCT.md)"
     - "[Component] is an internal abstraction (add to ARCHITECTURE.md)"

**If documents are empty/minimal (no patterns to reference):**
   - Provide general options without specific references:
     - "User-facing promise (add to PRODUCT.md)"
     - "System design requirement (add to ARCHITECTURE.md)"
     - "Both - it's a user promise AND a technical constraint"

3. Route each extracted piece to its appropriate document. A single user statement may result in updates to multiple documents.

### Step 3: Update Document

Read the target document to understand its current structure and content.

Determine where in the document the new content belongs:
- Does it extend an existing section?
- Does it require a new section?
- Does it modify existing content?

Make the update, maintaining the document's existing style and structure.

After updating, assess whether the change is **significant**. A change is significant if it:
- Introduces a new concept, component, or section
- Contradicts or substantially revises existing content
- Adds a top-level capability or design decision

If the change is minor — extending an existing section with more detail, fixing wording, adding a clarification — skip Steps 4 and 5 and proceed directly to Step 6.

### Step 4: Cross-Document Consistency

*Only for significant updates.*

Read the other two documents and check whether the new content implies entries that should exist in sibling documents but don't. Common patterns to look for:

- A new architecture component with no corresponding product justification
- A new product capability with no architectural description of how it works
- An implementation detail referencing a component not described in architecture
- A product goal with no implementation approach mentioned

If gaps are found, use the `question` tool to present them as a batch of 2-4 questions. Based on the context from existing documents (Step 0) and the change just made, provide specific, relevant options.

**Example with existing patterns:**

If you just added an export service to ARCHITECTURE.md, and PRODUCT.md has no mention of exports:

> I updated ARCHITECTURE.md with the export service. I noticed some potential gaps in other documents.

Use the `question` tool with:
- Question 1: "Should PRODUCT.md describe data export as a user-facing capability?"
  - **If PRODUCT.md has similar features**: "Add export as data access capability (like reports feature)" / "Add as part of reporting feature"
  - **If PRODUCT.md is minimal**: "Yes, add as new user-facing capability" / "No, exports are internal only"
- Question 2: "How should IMPLEMENTATION.md describe export generation?"
  - **If IMPLEMENTATION.md describes other services**: "Similar to [existing service], using [library]" / "Different approach (specify details)"
  - **If IMPLEMENTATION.md is minimal**: "Specify library/technology used" / "Defer implementation details for now"

For each question the user answers, update the corresponding document before proceeding.

### Step 5: Gap Detection and Completeness

*Only for significant updates.*

Scan the updated document for weaknesses:
- Concepts referenced but not elaborated
- Sections that are thin relative to their importance
- Missing failure modes, edge cases, or constraints
- Decisions stated without rationale

Use the `question` tool to present 2-4 probing questions as a batch. Focus on non-obvious gaps — things the user might not think to document unprompted. Based on the content just added, questions already answered in this session, and patterns from existing documentation, provide specific, contextual options.

**Example with existing patterns:**

If you just added an export service to ARCHITECTURE.md:

- Question 1: "What happens when an export fails mid-generation?"
  - **If other services have retry logic**: "Automatic retry (like [existing service])" / "User must re-trigger" / "Saved as partial export for resume"
  - **If no retry patterns exist**: "Automatic retry" / "User must re-trigger" / "Partial export saved for resume"
- Question 2: "Are there size or rate limits on exports?"
  - **If similar features have limits**: "Same limits as [similar feature]" / "Different limits (specify)" / "No hard limits - best effort"
  - **If no limits documented**: "10k rows / 100MB max" / "No hard limits - best effort" / "To be determined"
- Question 3: "Who has permission to trigger exports?"
  - **If docs mention role-based access**: "Any authenticated user" / "Only admin/owner roles" / "Configurable per workspace"
  - **If auth not documented**: "Any authenticated user" / "Role-restricted (specify roles)" / "To be determined"

Update the document with any answers the user provides. If the user declines to answer, move on without pressing.

**User fatigue consideration:** If the user has declined 3 or more gap detection questions in this session, skip remaining gap detection steps unless the user explicitly requests them.

### Step 6: Report

Briefly confirm what was changed and in which document. If Steps 4 or 5 resulted in additional updates, summarize those as well:

> Updated ARCHITECTURE.md: added export service component under "Data Pipeline" section.
> Also updated PRODUCT.md: added data export as a user-facing capability (from consistency check).

## Examples

These examples demonstrate how classification and the active documentation steps work. The specific terms will vary by project.

### Classification

**Input:** "Users can export their data in multiple formats"
**Classification:** Product (describes user-facing capability)

**Input:** "The export service validates permissions before generating files"
**Classification:** Architecture (describes component responsibility and interaction)

**Input:** "Exports are generated as CSV using the fast-csv library"
**Classification:** Implementation (names specific format and library)

### Depth Elicitation (Step 2)

**Input:** "Data export is fast and reliable"
**Classification:** Ambiguous — has both product and architecture aspects.

Instead of asking "which document?", use the `question` tool to decompose. After reading existing docs (Step 0) and seeing that PRODUCT.md already mentions "reports" as a user-facing feature and ARCHITECTURE.md discusses latency targets for other services:

Use the `question` tool:
- Question 1: "Is 'fast and reliable' a promise to users or a system design requirement?"
  - Option 1: "User-facing promise (add to PRODUCT.md like other user benefits)"
  - Option 2: "System design requirement (add to ARCHITECTURE.md with latency targets)"
  - Option 3: "Both - it's a user promise AND a technical constraint"
- Question 2: "Does 'fast' have a concrete target?"
  - Option 1: "Yes - under 5 seconds (similar to report generation target)"
  - Option 2: "Yes - but different target (specify)"
  - Option 3: "No specific target yet"

If the user selects "Both" and "under 5 seconds", this produces two updates:
- **PRODUCT.md:** Data export completes in under 5 seconds for typical datasets (up to 10k rows).
- **ARCHITECTURE.md:** The export pipeline must meet a 5-second latency target for datasets up to 10k rows.

### Cross-Document Consistency (Step 4)

**Scenario:** User adds "The notification service delivers messages through email, SMS, and push" to ARCHITECTURE.md.

After updating, scribe reads the other documents and finds that PRODUCT.md has no mention of notifications as a user-facing feature, but does mention "alerts" in a different context. IMPLEMENTATION.md describes other third-party integrations using specific provider names.

Use the `question` tool:
- Question 1: "Should PRODUCT.md describe notifications as a user-facing capability?"
  - Option 1: "Yes - add as new notifications feature (users receive updates via email/SMS/push)"
  - Option 2: "Yes - integrate with existing 'alerts' feature (notifications are how alerts are delivered)"
  - Option 3: "No - notifications are internal only, not user-facing"
- Question 2: "Should IMPLEMENTATION.md specify the notification providers?"
  - Option 1: "Yes - using [provider] (similar to how we document other integrations)"
  - Option 2: "Yes - but different providers (specify which)"
  - Option 3: "Not yet - still evaluating options"

### Gap Detection (Step 5)

**Scenario:** User adds a new "Authentication" section to ARCHITECTURE.md describing token-based auth with refresh tokens.

After updating, scribe scans the section and identifies gaps. From reading ARCHITECTURE.md (Step 0), scribe notices other sections mention security constraints and timeout values. IMPLEMENTATION.md describes storage mechanisms for other sensitive data.

Use the `question` tool:
- Question 1: "What happens when a refresh token is revoked?"
  - Option 1: "User signed out immediately (like session invalidation elsewhere in the system)"
  - Option 2: "User signed out at next request (deferred enforcement)"
  - Option 3: "Configurable per deployment"
- Question 2: "Is there a maximum session duration?"
  - Option 1: "Yes - 30 days (similar to other timeout values in the docs)"
  - Option 2: "Yes - but different duration (specify)"
  - Option 3: "No hard limit - refresh tokens last indefinitely until revoked"
- Question 3: "How are tokens stored on the client side?"
  - Option 1: "Same as [other sensitive data] - in secure storage"
  - Option 2: "Different approach (specify storage mechanism)"
  - Option 3: "Client implementation decision - not specified in architecture"

## Error Handling

### Document does not exist

If the target document does not exist, use the `question` tool to ask the user if they want to create it, with context about what type of document it is:

Question: "The [DOCUMENT].md file does not exist. Should I create it?"
Options:
- "Yes, create [DOCUMENT].md (will contain [brief description based on document type])"
- "No, use a different document instead"

### Content conflicts

If the new content contradicts existing content, use the `question` tool to flag it with specific options:

Question: "This conflicts with existing content in [DOCUMENT].md: '[existing content]'. How should I resolve this?"
Options based on the nature of the conflict:
- "Replace old content with new (new information supersedes old)"
- "Keep both with clarification (they represent different aspects/contexts)"
- "Merge the two (combine into comprehensive description)"

### Unclear scope

If the input is too broad or vague to place in a specific document, use the `question` tool to narrow it down:

Question: "I'm not sure where '[user input]' belongs. Can you help me place it?"
Options based on what aspects you can detect:
- "PRODUCT.md ([specific user-facing aspect you detected])"
- "ARCHITECTURE.md ([specific structural aspect you detected])"
- "IMPLEMENTATION.md ([specific technical aspect you detected])"
- "Multiple documents (it spans several concerns)"
