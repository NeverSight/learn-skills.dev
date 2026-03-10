---
name: brainstorm-design
description: Transform rough ideas into validated design documents through structured dialogue before any implementation. Use when user has a vague idea needing concrete design.
tags: [writing, eng-standards, documentation]
version: 1.0.0
license: MIT
related_skills: [refine-skill-design, generate-standard-readme, bootstrap-docs]
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "brainstorming"
        repo: "obra/superpowers"
        version: "1.0.0"
        license: "MIT"
        type: "fork"
        borrowed: "Structured dialogue approach, incremental validation, HARD-GATE pattern, anti-pattern documentation"
      - name: "writing-plans"
        repo: "obra/superpowers"
        version: "1.0.0"
        license: "MIT"
        type: "integration"
        borrowed: "Bite-sized task granularity, exact file paths, complete code in plan"
      - name: "systematic-debugging"
        repo: "obra/superpowers"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Phase-based process, root cause investigation methodology"
      - name: "frontend-design"
        repo: "anthropics/skills"
        version: "1.0.0"
        license: "Apache-2.0"
        type: "reference"
        borrowed: "Production-grade quality focus, aesthetic direction emphasis"
      - name: "web-design-guidelines"
        repo: "vercel-labs/agent-skills"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Compliance checking pattern, guideline fetching approach"
      - name: "vercel-react-best-practices"
        repo: "vercel-labs/agent-skills"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Best practices encapsulation, performance optimization focus"
      - name: "skill-creator"
        repo: "anthropics/skills"
        version: "1.0.0"
        license: "Apache-2.0"
        type: "reference"
        borrowed: "Structured creation workflow, metadata requirements"
    enhancements:
      - "Unified workflow from 7 top-ranked skills"
      - "Added YAGNI and DRY principles from writing-plans"
      - "Integrated phase-based validation from systematic-debugging"
      - "Enhanced with production-grade quality standards"
      - "Added comprehensive self-check mechanism"
      - "Defined clear core objective and success criteria"
      - "Established explicit skill boundaries to avoid overlap"
triggers: [brainstorm design, design, brainstorm]
input_schema:
  type: free-form
  description: Rough idea, feature request, or problem statement from user
output_schema:
  type: document-artifact
  description: Validated design document written per [spec/artifact-contract.md](../../spec/artifact-contract.md)
  artifact_type: design
  path_pattern: docs/design-decisions/YYYY-MM-DD-{topic}.md
  lifecycle: snapshot
---

# Skill: Brainstorm Design

## Purpose

Transform rough ideas into validated, production-grade designs through systematic collaborative dialogue. Prevent premature implementation by exploring context, clarifying requirements, proposing alternatives with trade-offs, and obtaining explicit approval before any code is written.

---

## Core Objective

**Primary Goal**: Produce a validated design document that serves as the single source of truth for implementation.

**Success Criteria** (ALL must be met):

1. ✅ **Design document exists**: Written to `docs/design-decisions/YYYY-MM-DD-<topic>.md` and committed to version control
2. ✅ **User explicitly approved**: User said "approved", "looks good", "proceed", or equivalent confirmation
3. ✅ **Alternatives documented**: At least 2-3 approaches considered with trade-offs analysis
4. ✅ **YAGNI applied**: Design focuses on minimum viable solution, unnecessary features removed
5. ✅ **DRY applied**: Design references existing patterns/components rather than reinventing
6. ✅ **No code written**: Zero implementation code exists (design only)

**Acceptance Test**: Can a developer with zero project context implement this design without asking clarifying questions?

---

## Scope Boundaries

**This skill handles**:

- Rough idea → Validated design document
- Requirement clarification through dialogue
- Alternative exploration and trade-off analysis
- Design approval and documentation

**This skill does NOT handle**:

- Implementation planning (use `writing-plans` or similar)
- Code writing (use implementation skills)
- Testing strategy details (mention in design, detail in implementation plan)
- Deployment planning (out of scope)

**Handoff point**: When design is approved and documented, hand off to implementation planning or development workflow.

---

## Use Cases

- **Feature planning**: User has rough idea for new functionality; needs help refining requirements and design approach.
- **Architecture decisions**: Team needs to explore multiple technical approaches with clear trade-offs before committing.
- **Requirement clarification**: Stakeholder request is vague or incomplete; extract concrete specifications through dialogue.
- **Design validation**: Existing design draft needs review and user approval before development.
- **Best practices application**: Apply domain-specific best practices (React, Next.js, Remotion, etc.) during design phase.

---

## Behavior

### Interaction Policy

- **Defaults**: Design path from project norms or `docs/design-decisions/`; present section by section
- **Choice options**: One question at a time; offer `[A][B][C]` for preferences
- **Confirm**: User must say "approved" or equivalent before handoff; no code until design approved

### HARD-GATE: No Implementation Before Approval

```
DO NOT invoke implementation skills, write code, scaffold projects,
or take implementation actions until design is presented and approved.

This applies to EVERY project regardless of perceived simplicity.
```

### Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, single-function utility, config change — all require design. "Simple" projects are where unexamined assumptions cause most wasted work. Design can be short (few sentences for simple projects), but MUST be presented and approved.

### Phase 1: Explore Context

**Announce at start:** "I'm using the brainstorm-design skill to refine this idea into a validated design."

1. **Examine project state**: Review relevant files, documentation, recent commits, existing architecture.
2. **Identify constraints**: Note technical limitations, dependencies, existing patterns, team conventions.
3. **Check for best practices**: If domain-specific (React, Next.js, etc.), note applicable best practices.
4. **Surface assumptions**: Document what is known vs. what needs clarification.

### Phase 2: Clarify Through Dialogue

**Core principle:** One question at a time, building understanding incrementally.

1. **Ask focused questions**: Understand purpose, constraints, success criteria.
2. **Prefer structured questions**: Use multiple choice when possible; open-ended when exploration needed.
3. **Build incrementally**: Each answer informs next question; avoid overwhelming with multiple questions.
4. **Validate understanding**: Summarize key points periodically to confirm alignment.

**Question patterns:**

- Purpose: "What problem does this solve?" "Who is the user?"
- Constraints: "What are the technical limitations?" "What must we preserve?"
- Success criteria: "How will we know this works?" "What defines done?"

### Phase 3: Explore Alternatives

**Core principle:** Always propose 2-3 approaches before settling.

1. **Propose 2-3 distinct approaches**: Present options with clear trade-offs.
2. **Lead with recommendation**: State your recommended option and explain reasoning.
3. **Consider constraints**: Ensure each approach addresses identified requirements and limitations.
4. **Apply YAGNI ruthlessly**: Remove unnecessary features from all designs; focus on minimum viable solution.
5. **Invite feedback**: User may prefer different approach or suggest hybrid solution.

**Trade-off framework:**

- Pros: What makes this approach strong?
- Cons: What are the downsides or risks?
- Best for: When is this the right choice?

### Phase 4: Present Design

**Core principle:** Scale to complexity, validate incrementally.

1. **Scale to complexity**:
   - Simple projects: Concise design (few sentences to 1 paragraph)
   - Medium projects: Structured sections (100-200 words each)
   - Complex projects: Detailed sections (200-300 words each)

2. **Present incrementally**: Show design in logical sections; validate each before proceeding.

3. **Cover key aspects** (adjust depth to complexity):
   - Architecture: High-level structure, component relationships
   - Components: Key modules, their responsibilities
   - Data flow: How information moves through system
   - Error handling: How failures are managed
   - Testing strategy: How correctness is verified
   - Performance considerations: Optimization approach (if relevant)
   - Security considerations: Auth, data protection (if relevant)

4. **Apply DRY principle**: Don't repeat yourself; reference existing patterns.

5. **Iterate as needed**: Revise sections based on feedback; go back to clarify when needed.

### Phase 5: Document and Transition

1. **Resolve project norms**: Check for `.ai-cortex/artifact-norms.yaml` or `docs/ARTIFACT_NORMS.md` per [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md). If found, use project path for `design`; otherwise use default `docs/design-decisions/YYYY-MM-DD-<topic>.md` from [spec/artifact-contract.md](../../spec/artifact-contract.md).

2. **Write design document**: Save to resolved path. Create directory if it does not exist.

3. **Document structure** (include YAML front-matter, see below):

   ```markdown
   ---
   artifact_type: design
   created_by: brainstorm-design
   lifecycle: snapshot
   created_at: YYYY-MM-DD
   ---
   
   # [Feature Name] Design
   
   **Date:** YYYY-MM-DD
   **Status:** Approved
   **Approved by:** [User name or "User"]
   
   ## Goal
   [One sentence describing what this builds]
   
   ## Architecture
   [2-3 sentences about approach]
   
   ## Components
   [Key modules and responsibilities]
   
   ## Data Flow
   [How information moves]
   
   ## Error Handling
   [How failures are managed]
   
   ## Testing Strategy
   [How correctness is verified]
   
   ## Trade-offs Considered
   [Alternatives explored and why this approach chosen]
   
   ## Acceptance Criteria
   - [ ] [Specific, measurable criterion 1]
   - [ ] [Specific, measurable criterion 2]
   - [ ] [Specific, measurable criterion 3]
   ```

4. **Commit to version control**: Preserve validated design as project artifact.

5. **Verify completion**: Check all success criteria met:
   - ✅ Design document exists and committed
   - ✅ User explicitly approved
   - ✅ Alternatives documented with trade-offs
   - ✅ YAGNI applied (unnecessary features removed)
   - ✅ DRY applied (references existing patterns)
   - ✅ No code written

6. **Announce completion and handoff**:

   ```
   "Design complete and approved. Saved to docs/design-decisions/YYYY-MM-DD-<topic>.md.
   
   Next steps:
   - For detailed implementation plan: Use writing-plans or similar skill
   - For immediate implementation: Proceed with development workflow
   - For review: Share design document with team
   
   Ready to proceed?"
   ```

---

## Input & Output

### Input

- **Rough idea**: User's initial concept, feature request, or problem statement.
- **Project context**: Existing codebase, documentation, constraints (discovered during exploration).
- **User responses**: Answers to clarifying questions, feedback on proposals, design approval.

### Output

- **Design document**: Validated design specification covering architecture, components, data flow, error handling, testing.
- **Documentation artifact**: Markdown file committed to version control at agreed location.
- **Implementation readiness**: Clear handoff point where design is approved and ready for development.
- **Trade-off analysis**: Documented alternatives considered and reasoning for chosen approach.

---

## Restrictions

### Hard Boundaries

- **No premature implementation**: Do NOT write code, scaffold projects, or invoke implementation tools until design is approved.
- **No assumption of simplicity**: Every project goes through this process, regardless of perceived simplicity. "Simple" projects can have short designs, but must still be presented and approved.
- **One question at a time**: Do not overwhelm user with multiple questions in a single message.
- **YAGNI ruthlessly**: Remove unnecessary features and complexity from all designs; focus on minimum viable solution.
- **DRY principle**: Don't repeat yourself; reference existing patterns and components.
- **Validate incrementally**: Do not present entire design at once; get approval section by section for complex projects.
- **No guessing**: If you don't understand something, ask for clarification rather than assuming.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Implementation planning**: Creating detailed task lists, file paths, exact code → Use `writing-plans` or similar
- **Code writing**: Writing actual implementation code → Use implementation/development skills
- **Code review**: Reviewing existing code for quality → Use `review-code` or similar
- **Debugging**: Investigating bugs or test failures → Use `systematic-debugging` or similar
- **Testing**: Writing test cases or test plans → Mention in design, detail in implementation phase
- **Deployment**: Planning deployment strategy → Out of scope for design phase

**When to stop and hand off**:

- User says "approved", "looks good", "proceed" → Design complete, hand off to implementation
- User asks "how do we implement this?" → Design complete, hand off to `writing-plans` or implementation
- User asks "can you write the code?" → Design complete, hand off to development workflow

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Design document exists**: Written to `docs/design-decisions/YYYY-MM-DD-<topic>.md` and committed
- [ ] **User explicitly approved**: User said "approved", "looks good", "proceed", or equivalent
- [ ] **Alternatives documented**: At least 2-3 approaches with trade-offs in design document
- [ ] **YAGNI applied**: Design focuses on minimum viable solution, unnecessary features removed
- [ ] **DRY applied**: Design references existing patterns/components rather than reinventing
- [ ] **No code written**: Zero implementation code exists (design only)

### Process Quality Checks

- [ ] **Context explored**: Did I examine project state, constraints, and existing patterns before asking questions?
- [ ] **Questions focused**: Did I ask one question at a time, building understanding incrementally?
- [ ] **Alternatives presented**: Did I propose 2-3 distinct approaches with clear trade-offs and recommendation?
- [ ] **Design validated**: Did I present design in appropriately-sized sections and get user approval?
- [ ] **Trade-offs documented**: Did I document alternatives considered and reasoning for chosen approach?
- [ ] **No premature code**: Did I avoid writing any implementation code before design approval?
- [ ] **No guessing**: Did I ask for clarification when information was missing rather than assuming?

### Acceptance Test

**Can a developer with zero project context implement this design without asking clarifying questions?**

If NO: Design is incomplete. Return to Phase 2 (Clarify) or Phase 4 (Present Design).

If YES: Design is complete. Proceed to handoff.

---

## Examples

### Example 1: Simple Feature - User Authentication

**User**: "I need to add login to my web app"

**Agent announces**: "I'm using the brainstorm-design skill to refine this idea into a validated design."

**Agent explores context**:

- Checks existing codebase (finds Express.js backend, React frontend)
- Notes no existing auth system
- Identifies database (PostgreSQL)

**Agent asks clarifying questions** (one at a time):

1. "What authentication method do you prefer? (A) Email/password, (B) OAuth (Google/GitHub), (C) Both"
2. "Do you need: (A) Basic login/logout only, (B) Password reset, (C) Email verification, (D) All of the above"
3. "For session management: (A) JWT tokens, (B) Server-side sessions, (C) No preference"

**Agent proposes approaches**:

- **Option A (Recommended)**: Passport.js with local strategy + JWT. Pros: Well-tested, flexible, good docs. Cons: More setup than alternatives. Best for: Production apps needing flexibility.
- **Option B**: NextAuth.js. Pros: Simpler setup, built-in OAuth. Cons: Requires Next.js migration or separate auth service. Best for: Next.js projects.
- **Option C**: Custom implementation. Pros: Full control. Cons: Security risk, more maintenance. Best for: Unique requirements not covered by libraries.

**Agent presents design** (section by section, applying YAGNI):

1. Architecture: Passport.js middleware, JWT tokens, bcrypt for passwords
2. Components: Auth middleware, User model, Token service
3. Data flow: Client → POST /auth/login → Passport → JWT → Client stores token → Authenticated requests include token
4. Database: Users table with email, password_hash, created_at (YAGNI: no roles, no profiles yet)
5. API endpoints: POST /auth/register, POST /auth/login, GET /auth/me (YAGNI: no password reset yet)
6. Frontend: Auth context, protected routes, token storage in httpOnly cookies
7. Error handling: Rate limiting (5 attempts/15min), input validation, secure password requirements (min 8 chars)
8. Testing: Unit tests for auth logic, integration tests for endpoints

**Agent documents**: Writes to `docs/design-decisions/2026-03-02-user-authentication.md` with trade-offs section and commits.

### Example 2: Complex Feature - Real-time Collaboration

**User**: "Add real-time collaboration like Google Docs"

**Agent announces**: "I'm using the brainstorm-design skill to refine this idea into a validated design."

**Agent explores context**:

- Examines existing document editor (CodeMirror-based)
- Notes current architecture (REST API, no WebSocket infrastructure)
- Identifies scale requirements (asks: "How many concurrent users per document?")

**Agent asks clarifying questions**:

1. "What collaboration features are essential? (A) Cursor positions only, (B) Live editing, (C) Comments/annotations, (D) All of the above"
2. "Expected concurrent users per document: (A) 2-5, (B) 5-20, (C) 20+, (D) Unknown"
3. "Conflict resolution preference: (A) Last-write-wins, (B) Operational Transform, (C) CRDT, (D) No preference"

**Agent proposes approaches**:

- **Option A**: Yjs (CRDT) + WebSocket. Pros: Proven, handles conflicts well, offline support. Cons: Learning curve, larger bundle (200KB). Best for: 5+ users, offline support needed.
- **Option B (Recommended for 2-5 users)**: ShareDB (OT). Pros: Simpler than CRDT, good for small teams, smaller bundle (50KB). Cons: Doesn't scale as well. Best for: Small teams, simpler requirements.
- **Option C**: Custom WebSocket + simple locking. Pros: Lightweight (10KB). Cons: Poor UX with conflicts, hard to get right. Best for: Very simple use cases, single editor at a time.

**Agent presents design** (detailed sections, applying DRY):

1. Architecture: Yjs for CRDT, y-websocket for sync, y-codemirror for editor binding (DRY: reuse existing CodeMirror)
2. Infrastructure: WebSocket server (separate from REST API), Redis for presence (DRY: reuse existing Redis)
3. Components: Sync server, Presence service, Document store, Editor binding
4. Data model: Document state in Yjs format, periodic snapshots to PostgreSQL (every 5 min or 100 changes)
5. Data flow: Editor change → Yjs update → WebSocket → Server → Broadcast → Other clients → Apply update
6. Conflict resolution: Automatic via CRDT, no user intervention needed
7. Presence: Cursor positions, user colors (from existing user profiles), active user list
8. Performance: Lazy loading for large documents (>1MB), compression for network traffic (gzip), debounce snapshots
9. Error handling: Reconnection logic (exponential backoff), offline queue (max 1000 ops), sync conflict UI (rare, show merge dialog)
10. Testing: Multi-client simulation (2, 5, 10 users), network partition scenarios, data consistency checks, load testing (100 concurrent docs)

**Agent documents**: Writes to `docs/design-decisions/2026-03-02-realtime-collaboration.md` with architecture diagrams, trade-offs analysis, and commits.

### Example 3: Edge Case - "Too Simple" Project

**User**: "Just need a function to format phone numbers"

**Agent announces**: "I'm using the brainstorm-design skill to refine this idea into a validated design."

**Agent explores context**:

- Checks if utility functions directory exists (finds `src/utils/`)
- Notes existing validation patterns in codebase (uses Zod for validation)

**Agent asks clarifying questions**:

1. "Which phone number formats? (A) US only, (B) International, (C) Specific countries"
2. "Input format: (A) Any string, (B) Already validated numbers, (C) User input from form"
3. "Output format: (A) Display format (e.g., (555) 123-4567), (B) Storage format (e.g., +15551234567), (C) Both"

**Agent proposes approaches**:

- **Option A (Recommended)**: libphonenumber-js library. Pros: Handles international, well-tested, maintained. Cons: 100KB bundle size. Best for: International support needed.
- **Option B**: Simple regex for US only. Pros: Tiny (1KB), no dependencies. Cons: Breaks with international numbers, maintenance burden. Best for: US-only apps, bundle size critical.

**Agent presents design** (concise, applying YAGNI and DRY):

"Utility function using libphonenumber-js: accepts string input, validates format, returns formatted string or error. Handles US and international numbers. DRY: integrates with existing Zod validation patterns. YAGNI: no custom formatting rules, no phone number database, just format and validate. Includes unit tests for valid/invalid inputs and edge cases (empty string, partial numbers, invalid country codes, null/undefined)."

**Agent documents**: Writes brief design to `docs/design-decisions/2026-03-02-phone-formatter.md` with trade-offs (libphonenumber-js vs regex) and commits.

### Example 4: Edge Case - Blocked by Missing Information

**User**: "Build a payment system"

**Agent announces**: "I'm using the brainstorm-design skill to refine this idea into a validated design."

**Agent explores context**:

- Checks existing codebase (finds e-commerce app)
- Notes no existing payment integration

**Agent asks clarifying questions**:

1. "Which payment providers? (A) Stripe, (B) PayPal, (C) Both, (D) Other"

**User**: "Stripe"

1. "What payment methods? (A) Credit cards only, (B) Credit cards + ACH, (C) All Stripe methods"

**User**: "Not sure, what do you recommend?"

**Agent stops and asks for clarification**:

"I need to understand your requirements better before proposing approaches. Key questions:

- Who are your customers? (B2B or B2C)
- What's your average transaction size?
- Do you need recurring payments (subscriptions)?
- Any specific compliance requirements (PCI, GDPR)?

Without this information, I can't recommend the right payment methods or architecture. Should we discuss these requirements first?"

**Agent does NOT guess or proceed with assumptions.**

---

## Appendix: Output contract

This skill produces a **document-artifact** (design). Each output document MUST conform to:

| Element | Requirement |
| :--- | :--- |
| **Path** | `docs/design-decisions/YYYY-MM-DD-<topic>.md` per [spec/artifact-contract.md](../../spec/artifact-contract.md) |
| **artifact_type** | `design` |
| **created_by** | `brainstorm-design` |
| **Required sections** | Context/Problem, Alternatives (2–3 with trade-offs), Recommended approach, Components/architecture, Data flow, YAGNI/DRY notes |
| **User approval** | Design is complete only when user said "approved", "looks good", "proceed", or equivalent |
