---
name: project-requirements
description: "Guided interview to create comprehensive project requirements documentation (requirements.md, business-rules.md, user-types.md, workflows.md) for a new SaaS project. Use before bootstrapping the SaaS Seeder Template."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Project Requirements Documentation Helper

Create comprehensive requirements documentation for a new SaaS project through a guided AI-assisted interview process.

## When to Use

Use when starting a new SaaS project from the template:

- "Help me create project requirements for [SaaS name]"
- "I need to document requirements for my SaaS"
- "Create requirements documentation for a new project"
- "Guide me through requirements gathering"

## Purpose

This skill helps developers create the required documentation files that must be placed in `docs/project-requirements/` **BEFORE** bootstrapping the SaaS Seeder Template.

## Output Files

The skill creates four core documentation files plus optional UI mockups:

```
docs/project-requirements/
├── requirements.md       # Feature requirements & specifications
├── business-rules.md     # Business logic & validation rules
├── user-types.md         # User roles and permissions
├── workflows.md          # Key user workflows
└── ui-mockups/           # Optional UI designs (images/PDFs)

**Documentation Requirement (Mandatory):**
- Define the end-user manual scope for each core feature so manuals can be built immediately after implementation.

**Planning Index Rule:** When feature plans are created later, always update `docs/plans/INDEX.md` with status, urgency, last implementation date, and last modification date.
```

## Guided Interview Process

### Phase 1: Project Overview (requirements.md foundation)

**Questions to ask:**

1. **Project Basics**
   - What is the name of your SaaS?
   - What domain/industry? (School, Restaurant, Medical, E-commerce, etc.)
   - Who are the primary users?
   - What is the main problem you're solving?
   - Target launch date?

2. **Core Features** (iterative)
   For each feature:
   - What is the feature name?
   - Brief description (1-2 sentences)
   - User stories: "As a [user type], I want to [action] so that [benefit]"
   - Acceptance criteria (specific, testable requirements)
   - Priority: High / Medium / Low

   **Example prompts:**
   - "Let's start with your top 3 most important features"
   - "What happens when a user clicks this button?"
   - "What data needs to be collected?"
   - "What validations are needed?"

3. **Non-Functional Requirements**
   - Performance expectations (concurrent users, response times)
   - Security requirements
   - Scalability needs (how many franchises, users per franchise)
   - Usability requirements (mobile, offline, languages)
   - GIS requirements (Leaflet maps, geofencing, optional tile provider API key if needed)
   - Documentation requirements (manuals, guides, release notes, FAQs)

**Output:** Generate `docs/project-requirements/requirements.md`

### Phase 2: Business Rules (business-rules.md)

**Questions to ask:**

1. **Validation Rules**
   For each entity/form:
   - What fields are required?
   - What are the validation rules? (length, format, range)
   - Are there unique constraints?
   - Cross-field validations?

2. **Calculations**
   - What formulas/algorithms are needed? (GPA, pricing, discounts, etc.)
   - Provide examples with sample inputs and outputs
   - Edge cases to handle

3. **State Machines**
   - What statuses can entities have? (e.g., student: PENDING → ACTIVE → GRADUATED)
   - What are valid transitions?
   - What triggers each transition?
   - What transitions are not allowed and why?

4. **Business Constraints**
   - Capacity limits (e.g., max students per class)
   - Time-based rules (e.g., can't modify grades after term closes)
   - Access restrictions (e.g., teachers only see their own subjects)

**Output:** Generate `docs/project-requirements/business-rules.md`

### Phase 3: User Types (user-types.md)

**Questions to ask:**

1. **User Type Identification**
   - Beyond owner/staff, what custom user types do you need?
   - Examples: student, teacher, parent, customer, patient, waiter, chef
   - Which users are "end users" vs "franchise staff"?

2. **For Each User Type:**
   - What is their role/purpose?
   - What can they do? (capabilities)
   - What data can they access?
   - Which panel do they use? (franchise admin vs member portal)
   - Does franchise_id apply? (REQUIRED for non-super_admin)

3. **Permissions**
   - What permission codes are needed?
   - Which user types get which permissions?
   - Any special access rules?

4. **Registration Workflows**
   - How is each user type created/registered?
   - Self-registration or admin-created?
   - What information is collected?

**Output:** Generate `docs/project-requirements/user-types.md`

### Phase 4: Workflows (workflows.md)

**Questions to ask:**

1. **Key Workflows Identification**
   - What are the 3-5 most important user journeys?
   - Examples: student enrollment, grade submission, fee payment, order placement

2. **For Each Workflow:**
   - Who are the actors? (users, system, external services)
   - What triggers this workflow?
   - What are the preconditions?
   - What are the postconditions?

3. **Step-by-Step Flow**
   For each step:
   - Who does what?
   - What does the system do in response?
   - What data is collected/saved?
   - Any branching logic?

4. **Alternative Flows & Errors**
   - What can go wrong?
   - How should errors be handled?
   - What alternative paths exist?

**Output:** Generate `docs/project-requirements/workflows.md`

### Phase 5: UI Mockups (Optional)

**Questions to ask:**

1. Do you have UI mockups or wireframes?
2. If yes: Place files in `docs/project-requirements/ui-mockups/`
3. Reference them in requirements.md where relevant

## Interview Techniques

### Ask Follow-Up Questions

**When user gives vague answer:**

```
User: "I need a student management system"
AI: "Great! Let's break that down:
  - What information do you need to track about students?
  - How do students get enrolled?
  - Who can view/edit student data?
  - What reports do you need?"
```

### Use Examples

**When explaining complex concepts:**

```
AI: "For grade calculation, here's an example:
  Subject 1: Grade A (4.0), Credits 3 → 4.0 × 3 = 12
  Subject 2: Grade B (3.0), Credits 4 → 3.0 × 4 = 12
  GPA = (12 + 12) ÷ (3 + 4) = 24 ÷ 7 = 3.43

  Does this match your grading system?"
```

### Provide Templates

**Show structure to guide thinking:**

```
AI: "For each feature, let's capture:
  ✓ Feature name
  ✓ Description
  ✓ User stories
  ✓ Acceptance criteria
  ✓ Priority

  Let's start with your first feature..."
```

## Quality Standards

### Good Requirements

✅ **Specific:** "Student email must be unique within franchise" not "email must be valid"
✅ **Testable:** "GPA calculated as weighted average" with formula
✅ **Complete:** All user types, all workflows, all validations documented
✅ **Unambiguous:** Clear language, examples provided
✅ **Prioritized:** High/Medium/Low for features

### Red Flags

❌ **Too vague:** "The system should be user-friendly"
❌ **Missing details:** "User can edit data" (which data? which users?)
❌ **Assumptions:** "Obviously students can't delete grades" (document it!)
❌ **No examples:** Formula without sample calculation

## Template Usage

**Reference the template files:**

When starting the interview, tell the user:

```
I'll help you create comprehensive requirements documentation.
We have template files to guide us:
- requirements.md.template
- business-rules.md.template
- user-types.md.template
- workflows.md.template

Let's start with your project overview...
```

**Use template structure but customize content:**

- Replace example content with user's actual requirements
- Add more sections as needed
- Remove sections not applicable
- Keep examples where they help clarify

## Integration with SaaS Seeder

**After completing requirements documentation:**

1. Verify files are in `docs/project-requirements/`:

   ```
   ✓ requirements.md
   ✓ business-rules.md
   ✓ user-types.md
   ✓ workflows.md
   ```

2. Create database schema in `database/schema/core-schema.sql` based on requirements

3. Run the `saas-seeder` skill to bootstrap the template:
   ```
   "Using the saas-seeder skill, prepare this repository for [Project Name]"
   ```

## Example Interview Flow

```
AI: "Let's create your project requirements! What's your SaaS project about?"
User: "A school management system"

AI: "Great! Let's start with the basics:
  1. What's the name of your SaaS?
  2. What types of schools? (Primary, Secondary, University, All)
  3. Who will use it? (Teachers, Students, Parents, Admins)"

User: "EduTrack SaaS. For all school types. Teachers, students, parents, and school admins."

AI: "Perfect! Let's identify your core features.
  What's the #1 most important feature?"

User: "Student enrollment"

AI: "Let's detail that. When a student enrolls:
  - Who creates the enrollment? (Admin, Parent, or Self-registration)
  - What information is collected?
  - What happens after enrollment?
  - Any approval process?"

... (continue interview)

AI: "Excellent! I've created your requirements.md.
  Now let's talk about business rules.
  For student enrollment, are there any restrictions?
  - Age limits?
  - Class capacity limits?
  - Document requirements?"

... (continue for all phases)
```

## Validation Checklist

Before completing, verify:

- [ ] All four core files created
- [ ] Each feature has acceptance criteria
- [ ] User types clearly defined
- [ ] Key workflows documented step-by-step
- [ ] Validation rules specified
- [ ] Calculations have examples
- [ ] State transitions documented
- [ ] Permission codes listed
- [ ] Multi-tenant requirements considered (franchise_id filtering)

## Output Confirmation

When complete, report to user:

```
✅ Project Requirements Documentation Complete!

Created Files:
- ✓ docs/project-requirements/requirements.md
- ✓ docs/project-requirements/business-rules.md
- ✓ docs/project-requirements/user-types.md
- ✓ docs/project-requirements/workflows.md

Summary:
- Features documented: [count]
- User types defined: [list]
- Key workflows: [list]
- Business rules: [count]

Next Steps:
1. Review the documentation files
2. Create database schema in database/schema/core-schema.sql
3. Run the saas-seeder skill to bootstrap your project
4. Start development!

Ready to bootstrap? Use:
"Using the saas-seeder skill, prepare this repository for [Your Project Name]"
```

## Best Practices

**Do:**

- Ask open-ended questions first, then drill down
- Provide examples to illustrate concepts
- Summarize what you've learned before moving to next section
- Offer to add more details if user thinks of something later
- Keep documentation practical and actionable

**Don't:**

- Assume requirements without asking
- Skip validations and edge cases
- Create generic documentation (make it specific to their SaaS)
- Overwhelm with too many questions at once
- Forget to save progress incrementally

## References

- Template files in `docs/project-requirements/*.template`
- `saas-seeder` skill for bootstrapping after requirements
- `../../CLAUDE.md` - Project-specific documentation after bootstrap
- Multi-tenant patterns: All franchise-scoped data needs franchise_id

## Cross-References to SDLC Skills

### Downstream Skills (use AFTER this skill)

| Skill | Relationship |
|-------|-------------|
| `sdlc-planning` | Takes this skill's output (requirements.md, business-rules.md, user-types.md, workflows.md) as input for Feasibility Study, Vision & Scope, SRS, and other planning documents. **This is the primary next step.** |
| `sdlc-design` | Uses the SRS (produced via `sdlc-planning`) to generate System Design Document, Database Design, API Documentation, and Technical Specifications. |
| `sdlc-testing` | Uses the SRS and SDD to create test plans, test cases, and V&V documentation. |
| `sdlc-user-deploy` | Uses all prior SDLC outputs to create user manuals, deployment guides, training materials, and release notes. |
| `feature-planning` | For individual feature specs and implementation plans after project-level requirements are established. |
| `android-saas-planning` | For Android companion app planning (PRD, SDS, API Contract). Uses SRS as input. |
| `saas-seeder` | Bootstrap the SaaS template using requirements from this skill's output. |

### Complete SDLC Workflow

```
project-requirements (THIS SKILL)
    ↓ requirements.md, business-rules.md, user-types.md, workflows.md
sdlc-planning
    ↓ SRS, Vision & Scope, SDP, Feasibility Study, QA Plan, Risk Plan, SCMP
sdlc-design
    ↓ SDD, Database Design, Tech Spec, API Docs, ICD, Code Standards
sdlc-testing
    ↓ Test Plan, Test Cases, V&V Plan, Test Report, Peer Reviews
sdlc-user-deploy
    ↓ User Manual, Ops Guide, Training, Release Notes, Maintenance, README
```
