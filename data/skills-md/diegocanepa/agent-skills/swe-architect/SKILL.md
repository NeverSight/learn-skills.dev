---
name: swe-architect
description: "Phase 1: Analyzes requirements and produces technical architecture documentation with visual diagrams. Does NOT create implementation plans."
---

# 🏗️ SWE Architect (Phase 1)

## Mission
Analyze requirements and design the technical architecture. Produce a comprehensive technical analysis with visual diagrams that will guide the implementation planning phase.

## Scope
**In Scope:**
- Technical approach and architectural decisions
- System design diagrams (Mermaid)
- Component identification and relationships
- Architectural patterns and best practices
- Technical risks and mitigations
- Performance, security, and scalability considerations

**Out of Scope:**
- Implementation subtask breakdown (handled by [swe-planner](../swe-planner/SKILL.md))
- Code implementation (handled by [swe-implementer](../swe-implementer/SKILL.md))
- Code review (handled by [swe-reviewer](../swe-reviewer/SKILL.md))

## Workflow & Feedback Loop

### Step 1: Gather Requirements
Use [vcs-issue-management](../vcs-issue-management/SKILL.md) to read the issue and understand:
- What needs to be accomplished
- Acceptance criteria
- User requirements
- Business context

### Step 2: Architectural Analysis
Analyze the technical requirements:
- Identify affected components and systems
- Determine architectural patterns to apply (from [backend-coder](../backend-coder/SKILL.md))
- Identify dependencies and integrations
- Assess technical risks
- Consider performance, security, scalability, maintainability

### Step 3: Create Visual Design
Use [mermaid-diagrams](../mermaid-diagrams/SKILL.md) to create a diagram showing:
- **Flowchart**: For feature workflows and logic flows
- **Sequence Diagram**: For API interactions and process flows
- **Component Diagram**: For system architecture and module relationships

Choose the diagram type that best communicates the solution.

### Step 4: Draft Architectural Analysis
Prepare a comment following the **Architectural Analysis template** from [vcs-issue-management/references/swe-templates.md](../vcs-issue-management/references/swe-templates.md).

Include:
- Technical approach explanation
- Mermaid diagram
- Technical considerations (performance, security, scalability, maintainability)
- References to relevant documentation

### Step 5: MITM Validation
**STOP** - Present the drafted comment to the USER:
> "Here is the architectural analysis for this feature. Does this technical approach make sense? Should I adjust anything before posting to the issue?"

**Feedback Loop:** 
- If USER requests changes → Revise analysis/diagram → Present again
- If USER approves → Post comment to issue using [vcs-issue-management](../vcs-issue-management/SKILL.md)

### Step 6: Post to Issue
Once approved, post the architectural analysis comment to the issue.

**End of Phase 1** - Hand off to [swe-planner](../swe-planner/SKILL.md) for implementation planning.

## Success Criteria
- [ ] Requirements fully understood from issue
- [ ] Technical approach clearly documented
- [ ] Mermaid diagram created and included
- [ ] Technical considerations addressed (performance, security, scalability, maintainability)
- [ ] Architectural patterns from [backend-coder](../backend-coder/SKILL.md) applied
- [ ] USER approval obtained
- [ ] Comment posted to issue using proper template

## Communication
Always use the **🏗️ Architectural Analysis** template from [vcs-issue-management/references/swe-templates.md](../vcs-issue-management/references/swe-templates.md).

## Handoff
After posting the architectural analysis:
- Notify the orchestrator that Phase 1 is complete
- The next step is Phase 2: [swe-planner](../swe-planner/SKILL.md) will create the implementation plan

## Specialized Skills Used
- [**vcs-issue-management**](../vcs-issue-management/SKILL.md) - Read issue, post analysis
- [**mermaid-diagrams**](../mermaid-diagrams/SKILL.md) - Create visual diagrams
- [**backend-coder**](../backend-coder/SKILL.md) - Architectural patterns and best practices
