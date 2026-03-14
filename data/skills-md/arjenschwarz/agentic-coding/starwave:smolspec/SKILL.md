---
name: starwave:smolspec
description: Small Spec (Smolspec) - Lightweight Specification for Minor Changes
---

# Small Spec (Smolspec) - Lightweight Specification for Minor Changes

Create a lightweight specification for small changes that don't warrant the full spec workflow. This command combines research, planning, and task creation into a streamlined process.

## Scope Assessment

**Complexity Estimation:**
- The model MUST first estimate implementation complexity before proceeding
- Estimate lines of code to be added/modified (target: <80 LOC for smolspec)
- Count affected files and components (target: 1-3 files)
- Assess if this fits micro-plan criteria: single component, minimal dependencies
- The model MUST check whether an existing smolspec or full spec already covers the requested functionality

**Initial Research:**
- The model MUST explore the codebase to identify affected areas
- Identify existing patterns that can be leveraged
- Document dependencies and integration points
- Check for related features or ongoing work
- The model MUST capture a concise summary of affected files, dependencies, and unknowns before moving forward

**Assessment Questions:**
The model MUST answer these before proceeding:
- Is this truly a small, isolated change?
- Can this be implemented incrementally without breaking existing functionality?
- Are the requirements clear enough to proceed without extensive clarification?
- Does the codebase have established patterns for this type of change?

**Escalation Criteria:**
If the change meets ANY of these criteria, the model MUST recommend using the full spec workflow instead:
- Affects multiple subsystems or architectural boundaries
- Requires breaking changes or significant API modifications
- Impacts backward compatibility
- Involves complex business logic or multiple user workflows
- Requires coordination across multiple components
- Has significant security, performance, or reliability implications
- Estimated implementation >80 lines of code or >3 files
- Requirements are ambiguous or need extensive clarification
- The user explicitly requests a full spec
- If uncertain between smolspec vs full spec, the model SHOULD default to recommending the full spec workflow

If escalation is needed, the model MUST:
1. Explain why the full spec workflow is more appropriate
2. Highlight specific complexity factors discovered during research
3. Provide the complexity metrics (LOC estimate, file count, dependencies)
4. Recommend starting with `/starwave:requirements` skill instead
5. STOP execution of smolspec workflow

## Feature Naming

- The model MUST propose a {feature_name} based on: (1) user's explicit preference, (2) current branch name if not a default branch, (3) derived from the prompt
- The model MUST allow the user to override the proposal
- Feature names should be concise and descriptive (e.g., "add-logging", "fix-validation")
- The model MUST sanitize feature names into filesystem-safe kebab-case slugs and ensure they do not collide with existing specs
- The model MUST wait for user approval of the feature name

## Lightweight Documentation

For changes that are appropriate for smolspec, the model MUST create documentation in two files:

**File Structure:**
- Create `specs/{feature_name}/smolspec.md` for requirements and design
- Create `specs/{feature_name}/tasks.md` for implementation tasks (compatible with next-task skill)
- Create `specs/{feature_name}/decision_log.md` if any decisions need to be documented

**Document Formats:**

The smolspec.md file MUST contain these sections:

```markdown
# {Feature Name}

## Overview
Brief description of what this change does and why it's needed (2-4 sentences).

## Requirements
Simple list of what needs to be accomplished using specification language:
- The system MUST {core requirement 1}
- The system SHOULD {recommended approach}
- The system MAY {optional enhancement}

Note: Use MUST for non-negotiable requirements, SHOULD for strong recommendations, MAY for optional features.

## Implementation Approach
Brief description of how this will be implemented:
- Key files to modify (with paths)
- Approach or pattern to use (reference existing similar implementations if available)
- Any important technical considerations
- Dependencies (existing code/libraries this relies on)
- Out of Scope (what will NOT be changed)

## Risks and Assumptions
Brief list of technical risks and key assumptions:
- Risk: {potential problem} | Mitigation: {how to address}
- Assumption: {what we're assuming is true}
- Prerequisite: {what must exist/work before this can be implemented}
```

The tasks.md file MUST follow the standard task format to be compatible with the next-task skill:
- Numbered checkbox list with maximum two levels of hierarchy
- May optionally group tasks into 1-2 phases if helpful for organization
- Total task count SHOULD be 4-10 tasks (small changes shouldn't need more)
- Each task must reference the smolspec.md file
- Tasks build incrementally on previous steps

**Task Description Guidelines:**
- Tasks MUST describe WHAT outcome is needed, not HOW to implement
- Tasks SHOULD be verifiable with clear success criteria
- Tasks MUST avoid prescriptive implementation details
- Bad example: "Add validateEmail() function to utils.go"
- Good example: "Email validation prevents invalid addresses from being submitted"
- Each task SHOULD include verification steps (testing distributed throughout, not consolidated at end)

**Documentation Constraints:**
- Keep smolspec.md concise (typically under 100 lines total)
- Requirements MUST use specification language (MUST/SHOULD/MAY)
- Implementation approach MUST reference specific file paths and existing patterns
- Risks and Assumptions section MUST identify at least one risk or assumption
- Tasks MUST be outcome-focused and verifiable
- Testing MUST be distributed across tasks, not consolidated into final task
- All tasks MUST involve writing, modifying, or testing code (no deployment, user acceptance testing, etc.)

## Workflow Process

**1. Research Phase:**
- Conduct initial research to understand the codebase and change scope
- Identify affected files and components
- Check for existing patterns to follow
- Assess complexity and determine if full spec is needed
- Share the research summary (scope, risks, references) with the user before planning

**2. Planning Phase (if not escalated):**
- Propose feature name and get approval
- Create initial smolspec.md with all required sections (Overview, Requirements, Implementation Approach, Risks and Assumptions)
- Ask clarifying questions if needed (use AskUserQuestion tool)
- Keep documentation minimal but complete
- Ensure smolspec is self-contained (assume fresh AI session will execute without conversation history)
- Use the design-critic skill to review the smolspec.md document
- Incorporate the design-critic's feedback and recommendations into the smolspec.md
- Update the document based on valid critiques before presenting to user
- Capture any noteworthy decisions or trade-offs identified during critique inside `specs/{feature_name}/decision_log.md`

**3. Self-Review Phase:**
Before presenting to user, the model MUST verify:
- [ ] Requirements use specification language (MUST/SHOULD/MAY) and are testable
- [ ] Implementation approach references specific files with paths
- [ ] Implementation approach references existing patterns or similar code
- [ ] At least one risk or assumption is documented with mitigation/validation plan
- [ ] Dependencies and prerequisites are clearly stated
- [ ] Out of scope items are explicitly listed
- [ ] No vague language (e.g., "robust", "user-friendly" without specifics)
- [ ] All sections are complete and self-contained
- [ ] Document is concise (<100 lines) but complete
- [ ] Red flags checked: scope creep, wrong technology, missing prerequisites

**4. Review Phase:**
- Present the smolspec document to the user (after design-critic review, incorporation, and self-review)
- Ask "Does this smolspec look good?"
- Make modifications based on user feedback
- Repeat until explicit approval is received

**5. Task Creation:**
- Once smolspec.md is approved, create the tasks.md file
- The model MUST use the rune skill to:
  - Create the task file at specs/{feature_name}/tasks.md with a reference to smolspec.md
  - Add tasks using batch operations, including `blocked_by` dependencies where tasks build on previous steps
- Task structure should follow the standard format compatible with next-task skill
- Keep it simple: 4-10 total tasks, optionally organized into 1-2 phases
- Each task MUST be outcome-focused (WHAT needs to be achieved, not HOW)
- Each task MUST be verifiable with clear success criteria
- Testing MUST be distributed throughout tasks (e.g., Task 2 implements, Task 3 verifies)
- After creating tasks.md, perform self-review:
  - [ ] Tasks describe outcomes, not implementation steps
  - [ ] Each task has verification/success criteria
  - [ ] Testing is distributed, not consolidated at end
  - [ ] All tasks involve code changes (no deployment/UAT tasks)
  - [ ] Tasks build incrementally without gaps
  - [ ] No orphaned or hanging code
- Ask "Do these tasks look good?"
- Make modifications if needed and repeat until explicit approval

## Additional Constraints

**Workflow Execution:**
- The model SHOULD complete the entire workflow in a single conversation flow (don't split into separate skills)
- The model MUST NOT implement the feature as part of this workflow - only create the specification
- The model MAY ask targeted questions but should minimize back-and-forth compared to full spec workflow
- The model SHOULD suggest using full spec workflow if the change grows in scope during planning

**Documentation Quality:**
- All documents MUST be self-contained (assume fresh AI session without conversation history)
- The model SHOULD leverage existing patterns and conventions found in the codebase
- The model SHOULD link to relevant files, specs, or commits referenced during research to minimize rework
- The model MUST include specific file paths, not generic references
- The model SHOULD document any assumptions or uncertainties in the Risks and Assumptions section
- If decision_log.md exists for this feature, follow the decisions documented there

**Task Quality:**
- The model MUST ensure all tasks are coding-focused (no deployment, UAT, or non-code tasks)
- Tasks MUST be outcome-focused (describe WHAT, not HOW)
- Testing MUST be distributed throughout task phases
- Each task MUST be verifiable with clear success criteria
- Tasks MUST build incrementally without gaps or orphaned code

**Self-Containment Requirements:**
The smolspec MUST be executable by a fresh AI session with only:
- The smolspec.md document
- The tasks.md document
- Access to the existing codebase
- No conversation history or external context

## Success Criteria

The smolspec workflow is complete when:
- A clear, concise smolspec.md file exists with all required sections:
  - Overview (2-4 sentences)
  - Requirements (using MUST/SHOULD/MAY specification language)
  - Implementation Approach (with specific file paths and existing pattern references)
  - Risks and Assumptions (at least one documented)
- A tasks.md file exists with:
  - 4-10 total outcome-focused tasks
  - Optionally organized into 1-2 phases
  - Distributed testing (not consolidated at end)
  - All tasks are code-focused and verifiable
- User has explicitly approved both the smolspec and tasks
- Tasks have been created in the rune system and are compatible with next-task skill
- All documentation is self-contained and executable by fresh AI session
- Self-review checklists have been completed for both smolspec and tasks
- Documentation is minimal but complete (smolspec typically <100 lines)
