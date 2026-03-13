---
name: delegation-prompt-crafter
description: Transform clarified user requests into structured delegation prompts optimized for specialist agents (cto-architect, strategic-cto-mentor, cv-ml-architect). Use after clarification is complete, before routing to specialist agents. Ensures agents receive complete context for effective work.
---

# Delegation Prompt Crafter

Creates structured, context-rich prompts for specialist agents that maximize their effectiveness and minimize back-and-forth.

## When to Use

- After clarification-protocol has resolved ambiguities
- When routing to cto-architect for design work
- When routing to strategic-cto-mentor for validation
- When routing to cv-ml-architect for ML-specific architecture
- For any handoff between agents in a workflow

## Why This Matters

Specialist agents work best with:
1. **Clear context**: Business goals, constraints, current state
2. **Specific task**: Exactly what deliverable is expected
3. **Structured requirements**: Must-haves vs nice-to-haves
4. **Quality criteria**: How to evaluate success

Without this structure, agents may:
- Ask redundant questions (wasting time)
- Solve the wrong problem (misunderstanding context)
- Over-engineer or under-engineer (missing constraints)
- Produce outputs in wrong format (unclear expectations)

## Delegation Prompt Structure

Every delegation prompt follows this format:

```markdown
## CONTEXT

### Business Goal
[What business outcome this serves]

### Current State
[Relevant existing systems, constraints, decisions]

### Key Constraints
- [Constraint 1: e.g., "Budget: < $10K/month infrastructure"]
- [Constraint 2: e.g., "Timeline: MVP in 8 weeks"]
- [Constraint 3: e.g., "Team: 3 senior engineers, Python/React expertise"]

### Background Information
[Any relevant context from clarification or previous agents]

---

## TASK

### Primary Deliverable
[Exactly what output is expected]

### Format Requirements
[Structure, sections, level of detail expected]

### Scope Boundaries
- **In scope**: [What to cover]
- **Out of scope**: [What to explicitly exclude]

---

## REQUIREMENTS

### Must-Haves
- [Critical requirement 1]
- [Critical requirement 2]

### Nice-to-Haves
- [Optional enhancement 1]
- [Optional enhancement 2]

### Quality Criteria
- [Criterion 1: e.g., "Architecture must support 10x growth"]
- [Criterion 2: e.g., "Trade-offs explicitly documented"]

### Integration Points
- [What this output feeds into: e.g., "Will be validated by strategic-cto-mentor"]
- [What depends on this: e.g., "Development team will implement from this"]

---

## ADDITIONAL CONTEXT

[Any other relevant information, links to documentation, previous decisions, etc.]
```

## Agent-Specific Templates

See the prompt-templates folder for pre-built templates:

- [architect-delegation.md](prompt-templates/architect-delegation.md) - For cto-architect design work
- [mentor-delegation.md](prompt-templates/mentor-delegation.md) - For strategic-cto-mentor validation
- [ml-architect-delegation.md](prompt-templates/ml-architect-delegation.md) - For cv-ml-architect ML work

## Crafting Guidelines

### Context Section

**Business Goal**: Be specific about outcomes, not activities
- Bad: "Build a notification system"
- Good: "Enable real-time alerts so users act on time-sensitive events, reducing missed opportunities by 50%"

**Current State**: Include what exists and what's working
- Existing architecture and tech stack
- Pain points with current solution
- Previous attempts and why they failed
- Existing integrations that must be preserved

**Constraints**: Be explicit about non-negotiables
- Budget (infrastructure and development)
- Timeline (deadlines, milestones)
- Team (size, skills, availability)
- Technical (must-use technologies, compliance)
- Political (stakeholder preferences, past decisions)

### Task Section

**Primary Deliverable**: One clear output
- Bad: "Help us with the architecture"
- Good: "Provide a system architecture design document with component diagrams, data flow, and technology recommendations"

**Format Requirements**: Specify structure
- "7-section architecture document per standard format"
- "Executive summary (2 pages max) + detailed appendix"
- "Focus on Phase 1 MVP, with notes on Phase 2 considerations"

**Scope Boundaries**: Prevent scope creep
- Explicitly state what's NOT included
- Call out decisions already made
- Identify what other agents will handle

### Requirements Section

**Must-Haves vs Nice-to-Haves**: Force prioritization
- Must-haves are blocking—solution fails without them
- Nice-to-haves are enhancements—can be deferred

**Quality Criteria**: Measurable success
- "Latency < 200ms at p95"
- "Support 100K concurrent users"
- "Cost < $5K/month at launch scale"

**Integration Points**: Connect the workflow
- What happens after this agent finishes?
- Who consumes this output?
- What format do downstream consumers need?

## Common Mistakes to Avoid

### 1. The Information Dump
**Bad**: Copying entire conversation history into delegation
**Good**: Distill to relevant context only

### 2. The Vague Task
**Bad**: "Design a good system"
**Good**: "Design a notification system architecture that supports 100K users, uses our existing PostgreSQL database, and costs < $2K/month"

### 3. The Missing Constraints
**Bad**: Letting agent assume unlimited budget/time
**Good**: Explicitly stating constraints, even if flexible

### 4. The Forgotten Handoff
**Bad**: No mention of what happens next
**Good**: "This design will be validated by strategic-cto-mentor before implementation begins"

## Output Examples

### Example 1: Architecture Delegation

```markdown
## CONTEXT

### Business Goal
Enable customers to receive real-time notifications for order status changes, reducing support tickets about "where's my order" by 60%.

### Current State
- Monolithic Node.js backend, PostgreSQL database
- Notifications currently sent via email batch (hourly)
- 50K active users, expecting 200K in 12 months
- Mobile app (React Native) and web app (React)

### Key Constraints
- Budget: < $3K/month additional infrastructure
- Timeline: MVP in 6 weeks, full rollout in 10 weeks
- Team: 2 backend engineers, 1 mobile engineer
- Must integrate with existing authentication system

### Background Information
User research shows 73% of support tickets are order status questions. Push notifications tested well in user interviews.

---

## TASK

### Primary Deliverable
System architecture design for real-time notification system

### Format Requirements
Standard 7-section architecture document:
1. Executive Summary
2. System Architecture (with diagrams)
3. Technology Stack Justification
4. Implementation Roadmap
5. Risk Assessment
6. Code Examples (WebSocket integration)
7. Deployment Strategy

### Scope Boundaries
- **In scope**: Backend notification service, mobile push integration, delivery tracking
- **Out of scope**: Email notifications (keep existing), SMS notifications (Phase 2)

---

## REQUIREMENTS

### Must-Haves
- Real-time delivery (< 5 second latency)
- Support for 200K users with 20% daily active
- Push notifications on iOS and Android
- Fallback to email if push fails

### Nice-to-Haves
- Notification preferences per user
- Read receipts / delivery confirmation
- Rich notifications with images

### Quality Criteria
- p95 latency < 5 seconds from event to notification
- 99.9% delivery success rate
- Infrastructure cost < $3K/month at 200K users

### Integration Points
- Will be validated by strategic-cto-mentor before implementation
- Development team will implement from this architecture
- Must integrate with existing user service for preferences

---

## ADDITIONAL CONTEXT

Previous attempt at WebSockets failed due to connection management complexity. Team prefers managed solutions where possible. AWS is our cloud provider.
```

## Validation Checklist

Before sending delegation prompt, verify:

- [ ] Business goal is outcome-focused, not activity-focused
- [ ] All critical constraints are explicitly stated
- [ ] Task is specific with clear deliverable
- [ ] Format requirements are defined
- [ ] Scope boundaries prevent scope creep
- [ ] Must-haves are truly must-haves (not nice-to-haves in disguise)
- [ ] Quality criteria are measurable
- [ ] Integration points explain the workflow context
- [ ] No vague terms or buzzwords remain

## References

- [Architect Delegation Template](prompt-templates/architect-delegation.md)
- [Mentor Delegation Template](prompt-templates/mentor-delegation.md)
- [ML Architect Delegation Template](prompt-templates/ml-architect-delegation.md)
