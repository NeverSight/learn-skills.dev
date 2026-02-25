---
name: prd-creator
description: This skill should be used when creating, validating, or converting Product Requirements Documents (PRDs) to LLM-native format. Use this skill when the user asks to write a PRD, review a PRD for compliance, convert an existing PRD to machine-readable format, or ensure PRD quality for AI agent consumption. This skill is optimized for users working with agentic coding frameworks who need strict requirement specifications to prevent context poisoning, hallucination, and mesa-optimization.
license: Complete terms in LICENSE.txt
---

# PRD Creator

## Overview

Create LLM-native Product Requirements Documents that serve as machine-interpretable, safety-focused specifications for AI agent development workflows. This skill implements a hybrid Markdown+YAML format optimized for token efficiency, human readability, and strict structural compliance.

**Key Principle**: The PRD is not documentation—it is a **control surface** that prevents AI agents from going rogue. Structured requirements protect non-technical users from context poisoning, hallucination, and constraint violations.

---

## When to Use This Skill

Use this skill when the user requests:

- "Help me write a PRD for [feature]"
- "Create a requirements document for [product]"
- "Review this PRD for LLM compatibility"
- "Convert this doc to LLM-native format"
- "Validate my PRD for compliance"
- "Make this PRD safe for AI agents"

**Context indicators**: User mentions PRD, product requirements, specification, feature definition, or expresses concerns about AI agent behavior, hallucination, or code safety.

---

## Core Workflow

### Workflow Decision Tree

```
┌─────────────────────────────────┐
│ User wants PRD-related help     │
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐      ┌─────────────┐
│ New PRD │      │ Existing PRD│
└────┬────┘      └──────┬──────┘
     │                  │
     ▼                  ▼
Create from        ┌─────────┐
template           │ Convert │
(Step 1)           │   OR    │
                   │ Validate│
                   └────┬────┘
                        │
                   ┌────┴─────┐
                   ▼          ▼
              Convert     Validate
              (Step 2)    (Step 3)
                   │          │
                   └────┬─────┘
                        ▼
                   Review &
                   Iterate
                   (Step 4)
```

---

## Step 1: Creating a New PRD

### When to Use

User needs to create a PRD from scratch for a new feature or product.

### Process

1. **Understand the Feature**
   - Ask clarifying questions about the feature/product
   - Identify user personas and their goals
   - Determine technical constraints (languages, frameworks, security requirements)
   - Clarify what is explicitly OUT of scope

2. **Initialize the PRD**

Run the initialization script:
```bash
scripts/init_prd.py <output-path>
```

Example:
```bash
scripts/init_prd.py ./prds/user-authentication.md
```

The script will prompt for:
- Product/Feature name
- Owner name
- Version number (default: 1.0.0)

3. **Fill in Core Sections**

Load `assets/prd-template.md` for reference structure. Use the following order (forward-chaining principle):

**Section Order**:
1. YAML frontmatter (metadata)
2. Overview & Goals (the "why")
3. Technical Constraints (immutable rules)
4. User Personas (the actors)
5. Functional Requirements (the "what")
6. Non-Functional Requirements (quality attributes)
7. Out of Scope (boundaries)
8. Success Metrics (validation)

**Critical Safety Elements**:

In **YAML frontmatter**:
```yaml
llm_directives:
  temperature: 0.2  # Low temperature reduces hallucination
  persona: >
    You MUST NOT deviate from technical constraints or functional
    requirements without explicit approval.
```

In **Technical Constraints**:
```markdown
## 2. Technical Constraints & Environment

**CRITICAL**: These constraints are immutable.

* **Forbidden Libraries/Patterns**: pickle, eval(), exec()
```

In **Out of Scope**:
```markdown
## 6. Out of Scope (Non-Goals)

**CRITICAL**: Explicitly define what will NOT be built to prevent
scope creep and agent hallucination.

* [Feature X]
* [Feature Y]
```

4. **Assign Unique IDs**

Every requirement MUST have a machine-readable ID:

- User Stories: `LAW-31`, `LAW-32`, `LAW-33` (3-digit format)
- Acceptance Criteria: `AC-001-A`, `AC-001-B` (matches parent US)
- NFRs: `NFR-Perf-001`, `NFR-Sec-001` (category prefix)
- Personas: `Persona-Admin`, `Persona-User` (PascalCase)

Example:
```markdown
### **LAW-31**: User Registration

* **As a**: Persona-NewUser
* **I want to**: Create an account
* **So that**: I can access platform features

**Acceptance Criteria**:

* **AC-001-A**: System MUST validate email format
* **AC-001-B**: System MUST require password minimum 12 characters
* **AC-001-C**: System MUST hash passwords using bcrypt cost factor 12
```

5. **Write Atomic, Testable Criteria**

Each acceptance criterion = one test case.

**Bad** (too vague):
```markdown
* **AC-001-A**: The login should work and be secure
```

**Good** (testable, specific):
```markdown
* **AC-001-A**: System MUST authenticate user with valid email and password
* **AC-001-B**: System MUST return 401 Unauthorized for invalid credentials
* **AC-001-C**: System MUST use constant-time comparison to prevent timing attacks
```

6. **Validate**

Run validation before considering the PRD complete:
```bash
scripts/validate_prd.py <path-to-prd.md>
```

Address all errors. Review warnings.

---

## Step 2: Converting an Existing PRD

### When to Use

User has an existing PRD (any format) that needs to be converted to LLM-native format.

### Process

1. **Analyze the Existing PRD**

Run the conversion assistant:
```bash
scripts/convert_prd.py <path-to-existing-prd.md>
```

The tool provides:
- Structure analysis (what sections exist)
- Pattern detection (user stories, acceptance criteria)
- ID format check
- Actionable recommendations

2. **Load Context for LLM Conversion**

Use an LLM agent to perform the conversion:

**Prompt Template**:
```
Load the following files into context:
1. [Path to existing PRD]
2. assets/prd-template.md
3. references/validation-rules.md

Task: Convert the existing PRD to LLM-native format following the
template structure. Ensure:
- YAML frontmatter with llm_directives
- Forward-chaining section order (constraints before requirements)
- Unique IDs for all user stories (US-XXX)
- Unique IDs for all acceptance criteria (AC-XXX-Y)
- Technical Constraints section with security requirements
- Out of Scope section with explicitly excluded features

Validate output against validation-rules.md before returning.
```

3. **Review LLM Output**

Manually review the converted PRD for:
- ✅ All original requirements preserved
- ✅ IDs assigned correctly
- ✅ Technical constraints captured
- ✅ Out of Scope section populated
- ✅ Acceptance criteria are atomic and testable

4. **Validate**

```bash
scripts/validate_prd.py <converted-prd.md>
```

Address all errors before use.

---

## Step 3: Validating an Existing PRD

### When to Use

User has a PRD and wants to verify it meets LLM-native compliance standards.

### Process

1. **Run Validation Script**

```bash
scripts/validate_prd.py <path-to-prd.md>
```

2. **Review Output**

The validator checks:

**Errors (MUST fix)**:
- ❌ Missing or invalid YAML frontmatter
- ❌ Missing required sections
- ❌ Sections out of order (violates forward-chaining)
- ❌ Duplicate user story IDs
- ❌ Duplicate acceptance criteria IDs
- ❌ Invalid ID formats

**Warnings (SHOULD review)**:
- ⚠️ User story ID not in 3-digit format (US-1 instead of LAW-31)
- ⚠️ AC ID doesn't match parent US (AC-042-A under LAW-31)
- ⚠️ Reference to non-existent ID
- ⚠️ Status not in recommended enum

3. **Fix Issues**

Address errors in order of priority:
1. YAML frontmatter issues (breaks machine parsing)
2. Missing required sections (incomplete specification)
3. Section ordering (affects LLM reasoning)
4. ID format and duplication (breaks traceability)

4. **Re-validate**

Run validation again until all errors are resolved:
```bash
scripts/validate_prd.py <path-to-prd.md> && echo "✅ PRD is compliant"
```

---

## Step 4: Reviewing and Iterating

### When to Use

After creating, converting, or validating a PRD, review for safety and completeness.

### Safety Review Checklist

Reference `references/safety-principles.md` for detailed guidance.

**YAML Frontmatter**:
- [ ] `status: approved` (only approved PRDs for autonomous agents)
- [ ] `llm_directives.temperature: 0.2` or lower (reduces hallucination)
- [ ] `llm_directives.persona` includes "MUST NOT deviate without approval"

**Technical Constraints** (Section 2):
- [ ] Section exists and appears BEFORE Functional Requirements
- [ ] Includes `**CRITICAL**` keyword
- [ ] Lists programming languages with versions
- [ ] Specifies frameworks and style guides
- [ ] Defines security requirements explicitly
- [ ] **Includes "Forbidden Libraries/Patterns"** (negative constraints)

**Functional Requirements** (Section 4):
- [ ] All user stories have unique US-XXX IDs (3 digits)
- [ ] All acceptance criteria have unique AC-XXX-Y IDs
- [ ] Each AC is atomic (one test case per criterion)
- [ ] Each AC uses MUST/SHOULD/MAY keywords (RFC 2119)

**Out of Scope** (Section 6):
- [ ] Section exists and is populated (not empty)
- [ ] Lists explicitly excluded features
- [ ] Includes `**CRITICAL**` keyword
- [ ] Mentions "prevent hallucination" in section header

**Validation**:
- [ ] `validate_prd.py` passes with zero errors
- [ ] All warnings reviewed and addressed if necessary

### Quality Checklist

**Granularity**:
- [ ] Each user story represents ONE capability
- [ ] Each acceptance criterion is testable by ONE test case
- [ ] No compound requirements ("X and Y" or "X or Y")

**Traceability**:
- [ ] All IDs are unique
- [ ] AC numbering matches parent US (AC-001-X under LAW-31)
- [ ] Cross-references point to valid IDs

**Completeness**:
- [ ] All personas referenced in user stories are defined in Section 3
- [ ] All technical constraints are specific (not "use secure hashing" but "use bcrypt cost factor 12")
- [ ] All NFRs include measurable thresholds ("< 250ms" not "fast")

---

## Advanced Usage

### Integration with Traycer Enforcement Framework

For users working with custom agentic coding frameworks (like traycer-enforcement-framework):

1. **Store PRD in Project Root**

```
/project-root/
  ├── PRD.md          # LLM-native PRD
  ├── src/
  └── tests/
```

2. **Configure Agent Context**

Ensure agents load the PRD at the beginning of each session:

```python
# Agent initialization
context = load_prd("./PRD.md")
agent.set_constraints(context.technical_constraints)
agent.set_personas(context.user_personas)
agent.set_requirements(context.functional_requirements)
```

3. **Enforce Validation Gates**

Add validation as a pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit

scripts/validate_prd.py PRD.md || {
  echo "❌ PRD validation failed. Fix errors before committing."
  exit 1
}
```

4. **Use for RAG Context**

When agents need implementation guidance:

```python
# Query: "How to implement US-042?"
# RAG retrieves:
#   - US-042 chunk
#   - All AC-042-X chunks
#   - Referenced Technical Constraints
#   - Related Persona definitions

# Agent receives complete, coherent context
```

### LLM Directives for Different Scenarios

Customize the `llm_directives` block based on use case:

**Strict Production Code**:
```yaml
llm_directives:
  model: "gpt-4-turbo"
  temperature: 0.1  # Very low for deterministic output
  persona: >
    You are a senior engineer generating production code. You MUST NOT
    deviate from technical constraints. All code MUST be tested. Reject
    any request to implement Out of Scope features.
```

**Exploratory Prototyping**:
```yaml
llm_directives:
  model: "gpt-4-turbo"
  temperature: 0.5  # Higher for creative solutions
  persona: >
    You are building a prototype. Follow technical constraints but
    propose alternative approaches when beneficial. Flag any Out of
    Scope features for discussion.
```

**Test Generation**:
```yaml
llm_directives:
  model: "gpt-4-turbo"
  temperature: 0.2
  persona: >
    You are a QA engineer generating comprehensive test cases. For each
    acceptance criterion (AC-XXX-Y), generate positive, negative, and
    edge case tests. Ensure 100% coverage of all ACs.
```

---

## Reference Files

For detailed information, load these files into context as needed:

### references/prd-framework.md

Comprehensive framework documentation including:
- Format analysis (Markdown vs JSON)
- Forward-chaining principle explanation
- Section hierarchy rationale
- RAG integration patterns
- Production workflow examples

**Load when**: Need deep understanding of why the framework works this way, or designing custom workflows.

### references/safety-principles.md

Detailed explanation of how LLM-native PRDs prevent agent misbehavior:
- Context poisoning prevention
- Hallucination mitigation
- Mesa-optimization safeguards
- Constraint violation protection

**Load when**: User expresses concerns about AI safety, agent control, or non-coder protection.

### references/validation-rules.md

Complete validation rule reference:
- YAML frontmatter requirements
- Section ordering rules
- ID format specifications
- Acceptance criteria best practices

**Load when**: Debugging validation errors or authoring custom validation logic.

---

## Assets

### assets/prd-template.md

Blank template ready to copy and fill in. Use as starting point for new PRDs or reference for structure.

### assets/prd-schema.json

JSON Schema for teams requiring pure JSON format or programmatic validation. Can be used with JSON Schema validators in CI/CD pipelines.

### assets/example-prd.md

Complete, realistic example PRD for a user authentication system. Demonstrates:
- Proper ID formatting
- Atomic acceptance criteria
- Technical constraints with security requirements
- Out of Scope section
- Complete cross-reference index

**Load when**: User needs concrete example to understand format or best practices.

---

## Common Patterns

### Pattern 1: "AI as Junior PM"

**Scenario**: PM needs first draft of PRD quickly.

**Workflow**:
1. PM provides context (user research, business goals)
2. PM provides template: `assets/prd-template.md`
3. LLM generates 70-80% complete draft
4. PM refines and validates
5. Validate with `scripts/validate_prd.py`

### Pattern 2: Incremental Feature Addition

**Scenario**: Adding new user stories to existing PRD.

**Workflow**:
1. Identify next available US-XXX ID
2. Write user story following format
3. Add atomic acceptance criteria (AC-XXX-Y)
4. Update Appendix A cross-reference index
5. Validate to ensure no duplicate IDs

### Pattern 3: PRD Review Before Agent Use

**Scenario**: User finished draft, wants to ensure it's safe for agents.

**Workflow**:
1. Run `scripts/validate_prd.py <prd.md>`
2. Fix all errors
3. Load `references/safety-principles.md`
4. Review against Safety Review Checklist (Step 4)
5. Update `status: approved` in YAML frontmatter
6. Commit to version control

### Pattern 4: Converting Legacy Documentation

**Scenario**: User has old requirements doc (Word, Google Docs, etc.).

**Workflow**:
1. Export to plain text or markdown
2. Run `scripts/convert_prd.py <old-doc.md>`
3. Review recommendations
4. Use LLM agent with template to convert
5. Manual review for accuracy
6. Validate with `scripts/validate_prd.py`
7. Iterate until compliant

---

## Troubleshooting

### Error: "Missing required metadata field: X"

**Cause**: YAML frontmatter missing required field.

**Fix**: Add to frontmatter:
```yaml
version: 1.0.0
owner: your-name
status: draft
last_updated: 2025-01-15
```

### Error: "Section order violation: 'Functional Requirements' should come after 'Technical Constraints'"

**Cause**: Sections out of forward-chaining order.

**Fix**: Reorder sections to match Step 1 section order. Technical Constraints MUST come before Functional Requirements.

### Warning: "AC-042-A appears under LAW-31 but ID suggests it belongs to US-042"

**Cause**: Acceptance criterion under wrong user story.

**Fix**: Move AC-042-X criteria under their matching US-042 parent, or renumber if intentional.

### Error: "Duplicate user story ID: LAW-35"

**Cause**: Same US-XXX ID used twice in document.

**Fix**: Find duplicate IDs and renumber one of them. Update all references.

### Agent Hallucinating Features

**Cause**: Out of Scope section missing or too vague.

**Fix**: Add explicit Out of Scope section with `**CRITICAL**` keyword. List exact features that should NOT be built.

### Agent Violating Technical Constraints

**Cause**: Constraints not explicit enough or placed after requirements.

**Fix**:
1. Move Technical Constraints to Section 2 (before requirements)
2. Add `**CRITICAL**` and `**MUST**` keywords
3. List forbidden patterns explicitly
4. Lower `temperature` in llm_directives to 0.1

---

## Best Practices

1. **Validate Early and Often**: Run `validate_prd.py` after every major edit
2. **Use Low Temperature**: Set `temperature: 0.2` or lower for production code generation
3. **Be Explicit**: "Use bcrypt cost factor 12" not "use secure hashing"
4. **Define Negatives**: Out of Scope section prevents hallucination
5. **Atomic Criteria**: One AC = one test case, always
6. **Version Control**: Commit PRD changes with descriptive messages
7. **Status Discipline**: Only set `status: approved` after thorough review
8. **ID Consistency**: Use 3-digit format (LAW-31) not variable digits (US-1)

---

## Quick Reference

**Create new PRD**:
```bash
scripts/init_prd.py ./prds/my-feature.md
# Edit the file
scripts/validate_prd.py ./prds/my-feature.md
```

**Convert existing PRD**:
```bash
scripts/convert_prd.py ./old-prd.md
# Review recommendations
# Use LLM to convert with template
scripts/validate_prd.py ./new-prd.md
```

**Validate PRD**:
```bash
scripts/validate_prd.py ./PRD.md
```

**Key ID Formats**:
- User Stories: `LAW-31`, `US-042`, `US-150`
- Acceptance Criteria: `AC-001-A`, `AC-042-B`
- NFRs: `NFR-Perf-001`, `NFR-Sec-002`
- Personas: `Persona-Admin`, `Persona-User`

**Safety Keywords**:
- `**CRITICAL**` in Technical Constraints and Out of Scope headers
- `MUST` / `SHOULD` / `MAY` in acceptance criteria (RFC 2119)
- `temperature: 0.2` or lower in llm_directives
