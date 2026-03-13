---
name: design-document
description: Create comprehensive design documents that establish shared vision for eLearning projects. Use when moving from discovery to design, creating course architecture, defining instructional approach, or building detailed design specifications.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
model: claude-opus-4-5-20251101
user-invocable: true
---

# Design Document Creator

Create comprehensive design documents that establish shared vision between your ID team and clients on what is being created and why.

## What This Skill Does

The design document bridges discovery and development by capturing:

- **Shared Vision** - What we're building and why
- **Instructional Strategy** - How we'll achieve the learning goals
- **Content Architecture** - Structure and flow of the course
- **Visual Direction** - Look and feel
- **Assessment Strategy** - How we'll measure success
- **Technical Requirements** - Platform, tools, standards

## When to Use This Skill

Use after discovery is complete and before storyboarding begins:

```
Discovery → Needs Analysis → Design Brief → [DESIGN DOCUMENT] → Storyboard → Development
```

## How to Use This Skill

### Option 1: Full Guided Process
Say: "Help me create a design document for [project]" or invoke `/design-document`

I'll interview you through each section:
1. Discovery recap
2. Instructional approach
3. Content architecture
4. Visual direction
5. Characters/scenarios (if applicable)
6. Assessment strategy
7. Technical requirements

### Option 2: Build from Discovery Documents
Say: "Create a design document based on this needs analysis" and share or reference:
- Needs analysis
- Design brief
- Learner personas
- Action map

### Option 3: Specific Sections
If you need help with just one part:
- "Help me define the instructional approach"
- "Create a content architecture for this course"
- "Develop characters for my scenario-based training"
- "Design the assessment strategy"

---

## Interview Process

### Phase 1: Discovery Recap
- What's the business goal?
- Who is the target audience?
- What are the priority behaviors from your action map?
- Link to existing discovery documents?

### Phase 2: Instructional Approach
- What type of learning experience fits this content?
  - Scenario-based / Branching
  - Linear / Sequential
  - Microlearning / Chunked
  - Exploratory / Self-directed
  - Blended / Multi-modal
- Why is this approach right for your audience and goals?
- What instructional methods will you use?

See [instructional-approaches.md](instructional-approaches.md) for detailed options.

### Phase 3: Content Architecture
- How many modules/lessons?
- What's the logical flow?
- How long is each section?
- What are the learning objectives for each?

### Phase 4: Visual Direction
- What's the overall tone? (Professional, casual, playful, serious)
- Brand guidelines to follow?
- Color palette and typography?
- Illustration style?
- Photography style?

### Phase 5: Characters & Scenarios (if applicable)
- Will you use characters?
- Who are they? (Names, roles, personalities)
- What scenarios will drive the learning?
- Are characters recurring or one-time?

### Phase 6: Assessment Strategy
- What types of assessments?
  - Knowledge checks
  - Scenario-based assessments
  - Skill demonstrations
  - Cumulative final
- What's the passing score?
- How many attempts?
- How does this connect to the learning objectives?

### Phase 7: Technical Requirements
- Authoring tool (Rise/Storyline)?
- SCORM version?
- LMS requirements?
- Accessibility standard?
- Mobile requirements?
- Audio/video needs?

---

## Output: Design Document Structure

The comprehensive design document includes:

```markdown
# Course Design Document

## 1. Executive Summary
- Project overview
- Shared vision statement
- Key stakeholders

## 2. Audience Profile
- Target learner description
- Learner persona summaries
- Key characteristics and constraints

## 3. Learning Objectives
- Terminal objectives (course-level)
- Enabling objectives (module-level)
- Alignment to business goal

## 4. Instructional Strategy
- Overall approach and rationale
- Instructional methods
- Practice and application activities
- Feedback strategy

## 5. Content Architecture
- Course structure diagram
- Module breakdown with objectives and duration
- Content outline
- Prerequisite relationships

## 6. Visual Design Direction
- Design principles
- Color palette
- Typography
- Imagery style
- UI/UX guidelines

## 7. Characters & Scenarios
- Character profiles
- Character usage guidelines
- Key scenarios overview

## 8. Assessment Strategy
- Assessment types and purposes
- Question specifications
- Scoring and feedback
- Completion requirements

## 9. Technical Specifications
- Authoring tool and version
- Output format and SCORM version
- LMS requirements
- Accessibility compliance
- Browser and device support
- Audio/video specifications

## 10. Project Information
- Timeline and milestones
- Review process
- Stakeholder sign-off

## Appendices
- Detailed content outline
- Asset requirements list
- Glossary of terms
```

---

## Tips for Better Design Documents

### Make It Usable
- Design documents should guide development, not just document decisions
- Include enough detail to prevent rework
- Make it skimmable with clear headings

### Create Shared Vision
- Use language stakeholders understand
- Include visuals and examples
- Reference specific scenarios and situations

### Stay Aligned
- Connect every section back to the business goal
- Ensure objectives trace to assessments
- Keep the learner persona visible in decisions

### Plan for Change
- Note assumptions that might change
- Flag areas needing SME validation
- Include version control

---

## Related Commands & Skills

- `/objectives` - Generate learning objectives
- `/learner-persona` - Create audience profiles
- `discovery-workshop` - Process discovery outputs
- `/bloom-verbs` - Reference for objective writing

---

## Getting Started

Ready to create a design document? Tell me:

1. **What project is this for?**
2. **Do you have discovery documents to reference?** (needs analysis, design brief, personas)
3. **What authoring tool will you use?** (Rise, Storyline, both)

Or share your needs analysis and design brief, and I'll help build the design document from there.
