---
name: software-methodology-toolkit
description: "FALLBACK ONLY: Comprehensive software engineering methodology toolkit with 10 proven agents. Only use when no project-specific skill (like requirement-workflow) matches. Provides: problem-definer (Weinberg), story-mapper (Patton), spec-by-example (Adzic), domain-modeler (DDD/Evans), responsibility-modeler (CRC/Wirfs-Brock), architecture-advisor (quality attributes/Bass), tdd-coach (Beck), refactoring-guide (Fowler), legacy-surgeon (Feathers), test-strategist (Crispin). Triggers ONLY if project skills don't match."
---

# Software Methodology Toolkit

A comprehensive collection of 10 proven software engineering methodologies, each implemented as a specialized agent. This skill provides systematic guidance across the entire software development lifecycle.

## ⚠️ Priority Notice

**This is a FALLBACK skill:**
- If you're working in a project with context-specific skills (like `requirement-workflow`), those should be triggered first
- This toolkit is designed for general use when no project-specific adaptations exist
- Project skills have higher priority because they contain context-specific adaptations (Hook Points, custom outputs, etc.)
- Only use this skill explicitly if you want the vanilla methodology without project context

## Available Methodologies

### 🔍 Analyzing Phase

#### [problem-definer](agents/analyzing/problem-definer.md)
Apply Weinberg's Six Questions Framework to systematically define problems.

**Use when:**
- Requirements are unclear or contradictory
- Stakeholders disagree on what the problem is
- Solutions keep missing the mark
- Need to identify the REAL problem

**Triggers:** "define the problem", "what's the real problem", "stakeholder analysis"

---

#### [spec-by-example](agents/analyzing/spec-by-example.md)
Create living documentation through concrete examples (Gojko Adzic).

**Use when:**
- Requirements are vague
- Need executable specifications
- Building shared understanding between business and tech
- Want tests that serve as documentation

**Triggers:** "specification by example", "concrete examples", "acceptance criteria"

---

### 📋 Planning Phase

#### [story-mapper](agents/planning/story-mapper.md)
Create user story maps to visualize user journeys and prioritize releases (Jeff Patton).

**Use when:**
- Planning products or features
- Backlog lacks context
- Deciding MVP scope
- Need to see the big picture

**Triggers:** "story mapping", "user journey", "release planning", "MVP scope"

---

### 🎨 Designing Phase

#### [domain-modeler](agents/designing/domain-modeler.md)
Apply Domain-Driven Design to model complex business domains (Eric Evans).

**Use when:**
- Designing bounded contexts
- Creating aggregates and entities
- Establishing ubiquitous language
- Modeling complex business rules

**Triggers:** "DDD", "domain model", "bounded context", "aggregate design"

---

#### [responsibility-modeler](agents/designing/responsibility-modeler.md)
Design objects by their responsibilities and collaborations (Rebecca Wirfs-Brock).

**Use when:**
- Designing OO systems
- Objects have unclear responsibilities
- Running CRC sessions
- Applying GRASP principles

**Triggers:** "CRC cards", "object responsibilities", "GRASP", "collaboration design"

---

#### [architecture-advisor](agents/designing/architecture-advisor.md)
Analyze software architecture decisions using quality attributes (Bass, Clements, Kazman).

**Use when:**
- Making architectural decisions
- Evaluating technology choices
- Analyzing trade-offs
- Defining quality attribute scenarios

**Triggers:** "architecture decision", "quality attributes", "trade-off analysis", "ADR"

---

### 💻 Implementing Phase

#### [tdd-coach](agents/implementing/tdd-coach.md)
Guide Test-Driven Development practice (Kent Beck).

**Use when:**
- Implementing features from scratch
- Learning TDD
- Stuck on implementation approach
- Need test-first discipline

**Triggers:** "TDD", "test-driven", "red-green-refactor", "test first"

---

#### [refactoring-guide](agents/implementing/refactoring-guide.md)
Identify code smells and apply refactoring techniques (Martin Fowler).

**Use when:**
- Code quality needs improvement
- Before adding features to messy code
- During code reviews
- Paying down tech debt

**Triggers:** "refactor", "code smell", "improve code quality", "clean up code"

---

#### [legacy-surgeon](agents/implementing/legacy-surgeon.md)
Safely modify legacy code without tests (Michael Feathers).

**Use when:**
- Working with untested code
- Adding features to legacy systems
- Breaking dependencies for testability
- Need characterization tests

**Triggers:** "legacy code", "working effectively", "seam", "characterization test"

---

### 🧪 Testing Phase

#### [test-strategist](agents/testing/test-strategist.md)
Plan comprehensive test strategies using Agile Testing Quadrants (Lisa Crispin).

**Use when:**
- Deciding what types of tests to write
- Reviewing test coverage
- Optimizing test suites
- Planning test distribution

**Triggers:** "test strategy", "test quadrants", "test pyramid", "test coverage"

---

## How to Use

Simply mention the methodology or trigger phrase, and this skill will invoke the appropriate agent:

### Examples

```
User: "Help me define the problem for this vague requirement"
→ Invokes problem-definer agent

User: "Let's apply DDD to model this e-commerce domain"
→ Invokes domain-modeler agent

User: "I need to refactor this messy class"
→ Invokes refactoring-guide agent

User: "Plan test strategy for authentication feature"
→ Invokes test-strategist agent
```

## Methodology Workflows

These methodologies work together in common workflows:

### New Feature Workflow
1. **problem-definer** → Define the real problem
2. **story-mapper** → Map user journey
3. **spec-by-example** → Create concrete examples
4. **domain-modeler** → Model domain concepts
5. **tdd-coach** → Implement with TDD
6. **test-strategist** → Verify test coverage

### Legacy Code Workflow
1. **problem-definer** → Understand why change is needed
2. **legacy-surgeon** → Break dependencies safely
3. **refactoring-guide** → Identify and fix smells
4. **test-strategist** → Add appropriate tests

### Architecture Workflow
1. **problem-definer** → Clarify requirements
2. **domain-modeler** → Model bounded contexts
3. **architecture-advisor** → Analyze quality attributes
4. **responsibility-modeler** → Design object responsibilities

## Philosophy

All agents follow these principles:

- ❌ **Do NOT write code** - Only provide analysis and guidance
- ❌ **Do NOT make decisions** - Present options and trade-offs
- ❌ **Do NOT run commands or modify files** - Stay strictly read-only
- ✅ **Only output**: Analysis, recommendations, structured reports

## References

This toolkit is based on these seminal works:

- **Are Your Lights On?** — Weinberg & Gause (1982)
- **User Story Mapping** — Jeff Patton (2014)
- **Specification by Example** — Gojko Adzic (2011)
- **Domain-Driven Design** — Eric Evans (2003)
- **Object Design** — Rebecca Wirfs-Brock (2002)
- **Software Architecture in Practice** — Bass, Clements, Kazman (2021)
- **Test Driven Development** — Kent Beck (2003)
- **Refactoring** — Martin Fowler (2018)
- **Working Effectively with Legacy Code** — Michael Feathers (2004)
- **Agile Testing** — Lisa Crispin & Janet Gregory (2009)
