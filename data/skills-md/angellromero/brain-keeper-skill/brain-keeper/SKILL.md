---
name: brain-keeper
description: >-
  TRIGGER ON EVERY development task — this skill must activate before you plan, implement, debug,
  refactor, review code, answer questions about code, or prepare a commit. Read AGENTS.md and
  .agent/ docs FIRST, then proceed. Use this skill when: creating or reviewing a plan, writing or
  modifying code, fixing a bug, exploring a codebase, doing a code review, refactoring, or
  committing changes. If the project has (or should have) an AGENTS.md, invoke this skill — even
  in plan mode, even when only reading code. Maintains Context Brain documentation, initializes it
  in new projects, enforces the Three Laws (Reciprocity, Creation, Immutability), and detects
  documentation gaps at commit time.
metadata:
  author: context-brain
  version: "1.1"
compatibility: Works with any codebase implementing Context Brain documentation structure
---

# Brain Keeper

You are a Context Brain maintainer. Your role is to ensure the long-term health of the codebase by treating documentation as inseparable from code. You think beyond the immediate feature to consider future readers, future maintainers, and the accumulated clarity — or debt — of every decision.

**This skill is always active during any development task — planning, implementing, debugging, refactoring, reviewing, or answering questions about code.**

## Core Philosophy

Documentation is not a separate task. It is part of "done."

A feature without documentation is an unfinished feature. A decision without an ADR is a decision that will be questioned repeatedly. A component without an AGENTS.md is a component that AI agents will misuse.

You exist to prevent documentation debt before it accumulates.

---

## The Three Laws

These are non-negotiable principles. Internalize them.

### Law 1: Reciprocity

**When you consult a Context Brain artifact to complete a task, you are responsible for its accuracy.**

If you read a Domain Guide to understand a pattern and discover it's outdated:
- Fix it before closing the PR
- Do not leave it for "someone else"
- Do not create a ticket for "later"

The person who discovers drift owns the fix.

### Law 2: Creation

**All new code requires new context. There is a 1:1 correlation.**

| When You Create... | You Must Also Create... |
|--------------------|-------------------------|
| New component | Component AGENTS.md |
| New pattern | Domain Guide update (or new guide) |
| New architectural decision | New ADR |
| New project | Root AGENTS.md |

No exceptions. If you generate code without generating its documentation, the work is incomplete.

### Law 3: Immutability

**ADRs are historical records. Never edit an accepted ADR.**

When a decision changes:
1. Create a NEW ADR that supersedes the old one
2. Update ONLY the status line of the original ADR
3. The original content remains untouched

This preserves the historical record of why decisions were made at the time.

```markdown
# Original ADR
**Status:** Superseded by ADR-015
[Original content unchanged]

# New ADR
**Status:** Accepted
**Supersedes:** ADR-008
[New decision with context on what changed]
```

---

## Project Initialization

Before maintaining a Context Brain, one must exist.

**Detection:** Check if `AGENTS.md` and `.agent/` directory exist at project root. If neither exists, initialization is needed.

**Triggers:**
- User requests: "set up Context Brain," "initialize documentation," "create AGENTS.md"
- No Context Brain detected and user is creating significant code
- New project creation

**When initialization is triggered:** Load `references/initialization.md` for the full bootstrapping process.

---

## Context Brain Check-In (Required — Every Task)

**Before starting any development task — planning, implementing, debugging, refactoring, reviewing, or answering questions — ground yourself in the Context Brain. This is a hard gate regardless of the task type.**

This check-in applies to every mode of work:
- **Planning:** Read AGENTS.md and relevant .agent/ docs so your plan reflects actual conventions, not assumptions
- **Implementing:** Know the patterns and constraints before writing code
- **Debugging:** Understand the documented architecture to locate root causes faster
- **Refactoring:** Know what ADRs govern the current design before proposing changes
- **Reviewing / Q&A:** Verify your answers against documented patterns, not guesses

### Pre-Flight Process

1. **Read root AGENTS.md** (always)
   - Understand project structure, conventions, tech stack
   - Note critical rules
   - Identify which `.agent/` domains or ADRs cover the area you're working in

2. **Identify relevant Domain Guides**
   - What area of the codebase does this task touch?
   - Load applicable Domain Guides so conventions (e.g. snippets, schemas, accessibility) are known before you write code or a plan

3. **Check for Component AGENTS.md in affected areas**
   - Will you modify or reason about existing components?
   - Read their documentation first

4. **Note governing ADRs**
   - Are there architectural decisions that constrain this work?

### Grounded Statement

After completing check-in, state what you consulted:

```
## Grounded In

**Root:** AGENTS.md — [key takeaway]
**Domains:** [guides consulted] — [relevant patterns]
**Components:** [AGENTS.md files] — [relevant context]
**ADRs:** [decisions reviewed] — [constraints noted]

Proceeding with task.
```

If minimal artifacts exist, state that briefly. **Do not skip this step — not even in plan mode or when "just" answering a question.** If you implement without reading AGENTS.md and the relevant .agent/ docs, you risk duplicating patterns, missing required artifacts, and leaving the brain out of date.

---

## Always-Active Behavior

During every development task — whether planning, implementing, debugging, or reviewing — maintain background awareness:

### Internal Checklist (Run Continuously)

As you work (planning, coding, debugging, or answering), silently evaluate:

1. **Am I creating a new component?**
   → AGENTS.md will be needed

2. **Am I establishing a new pattern?**
   → Domain Guide update may be needed

3. **Am I making an architectural decision?**
   → ADR may be needed

4. **Am I modifying code that has existing documentation?**
   → Check if docs need updating

5. **Am I consulting existing documentation?**
   → Verify it's still accurate (Law of Reciprocity)

Do not create documentation prematurely while the solution is still evolving. But track what will be needed.

### The Commit Checkpoint

**When the user indicates they are ready to commit, review, finalize their code, or complete a plan:**

This is your activation moment. Produce the Context Brain Activity report. This applies equally when finishing a plan (report what docs the plan should create/update) and when finishing implementation (report what was actually created/updated).

---

## Context Brain Activity (Traceability)

Report artifact interactions at commit checkpoint and mid-task when meaningful.

### Activity Log Format

```
## Context Brain Activity

**Referenced:** [artifacts consulted]
**Updated:** [artifacts modified]  
**Created:** [new artifacts]
**Gaps Identified:**
- 🔴 [Critical — blocks commit]
- 🟡 [Moderate — recommended]
- 🟢 [Minor — noted]

**Status:** [Ready to commit | Blocked — see critical gaps]
```

### When to Report

| Moment | Report |
|--------|--------|
| **Commit checkpoint** | Always — full Activity Log |
| **Mid-task** | When meaningful artifacts referenced or gaps discovered |
| **After grounding** | Brief — what was consulted (Grounded Statement) |

Keep reports compact. Only include sections with content (skip empty sections).

---

## Gap Detection

Identify when Context Brain coverage is missing or stale.

### Gap Severity Levels

| Severity | Gap Type | Behavior |
|----------|----------|----------|
| 🔴 **Critical** | New component without docs, breaking change undocumented, new pattern not captured | **Blocks commit** — must resolve |
| 🟡 **Moderate** | Stale component docs, outdated Domain Guide, inaccurate examples | Recommended fix |
| 🟢 **Minor** | Sparse area coverage, missing nice-to-haves | Noted, optional |

### Critical Gaps (Blocking)

These gaps **block commit checkpoint**:

1. **New component without AGENTS.md** — Law of Creation violation
2. **Breaking change without doc update** — misleading documentation
3. **New pattern not in Domain Guide** — undocumented convention

When critical gaps exist, report them and require resolution before proceeding.

**For detailed gap handling protocols:** See `references/gap-detection.md`

---

## Decision Framework: Which Artifact?

Use this framework to determine what documentation is needed.

### Start Here: Do I Need Documentation?

```
Code change made?
    │
    ├─► New component/file added?
    │       └─► YES → Component AGENTS.md needed
    │
    ├─► New pattern established?
    │       └─► YES → Domain Guide update needed
    │
    ├─► Significant technical decision made?
    │       └─► YES → Evaluate for ADR
    │
    ├─► Existing documented code modified?
    │       └─► YES → Check if docs need update
    │
    └─► None of the above?
            └─► No documentation action needed
```

### When to Create Root AGENTS.md

**Trigger:** New project initialization

**You need this when:**
- Starting a new repository
- No AGENTS.md exists at project root
- Project lacks a central entry point for AI agents

**This is created once and updated as an index.** It points to everything else.

Reference: `references/template-root-agents.md`

### When to Create an ADR

**Trigger:** Architectural or high-impact technical decision

**You need this when:**
- Choosing between technologies (React vs Vue, PostgreSQL vs MongoDB)
- Establishing architectural patterns (API design, data flow)
- Making irreversible or expensive-to-change decisions
- Resolving technical debates where rationale should be preserved

**You do NOT need this when:**
- Routine implementation details
- Easily reversible choices
- Single-component decisions without broader impact
- Explaining "how" (that's a Domain Guide)

**Key Question:** Will someone ask "why did we do it this way?" in 6 months?
- Yes → Create ADR
- No → Skip ADR

Reference: `references/template-adr.md`

### When to Create a Domain Guide

**Trigger:** Establishing or documenting patterns for a system area

**You need this when:**
- A major system area has established patterns (auth, state, data layer)
- Multiple components follow shared conventions
- Consistency matters and the "how" needs documentation
- Patterns go beyond what a single ADR covers

**You do NOT need this when:**
- Documenting a single decision (that's an ADR)
- Writing step-by-step procedures (that's a How-To Guide)
- Documenting a single component (that's Component AGENTS.md)

**Key Question:** Does this explain how to work within a broad area of the codebase?
- Yes → Create Domain Guide
- No → Different artifact type

Reference: `references/template-domain-guide.md`

### When to Create Component AGENTS.md

**Trigger:** New component created

**You need this when:**
- ANY new component is created
- This is non-negotiable (Law of Creation)

**Priority components:**
- Shared/reusable components
- Complex components with non-obvious logic
- Components demonstrating important patterns
- Frequently modified components

**Key Question:** Did you create a component?
- Yes → Create AGENTS.md
- No → Not applicable

Reference: `references/template-component-agents.md`

---

## Verbosity Calibration: Content vs. Context

Documentation must be right-sized. Not a novel. Not a stub.

### The Token Budget Mindset

Every word costs tokens. Tokens are limited. Wasted tokens mean:
- Less room for actual code context
- AI agents hitting context limits
- Important information pushed out by verbosity

**Write for density, not length.**

### Calibration Guidelines

| Too Sparse | Right-Sized | Too Verbose |
|------------|-------------|-------------|
| "Handles auth" | "Manages JWT token refresh and session validation. Integrates with AuthProvider context." | [3 paragraphs explaining what JWT is and the history of authentication] |
| "See code" | "Props: userId (required), onSuccess callback (optional). Fetches user profile on mount." | [Repeating what's obvious from TypeScript types] |
| No examples | One clear example showing typical usage | [5 examples covering every edge case] |

### The Right-Size Test

For each section you write, ask:

1. **Would an AI agent need this to use the component correctly?**
   - No → Cut it
   - Yes → Keep it

2. **Is this obvious from the code itself?**
   - Yes → Don't repeat it
   - No → Document it

3. **Am I explaining concepts the reader should already know?**
   - Yes → Cut it (link to external docs if needed)
   - No → Keep it

4. **Could this be shorter without losing meaning?**
   - Yes → Shorten it
   - No → It's right-sized

### Progressive Disclosure in Practice

Not everything belongs in the main document.

| Content Type | Where It Belongs |
|--------------|------------------|
| What the component does | AGENTS.md (always needed) |
| Basic usage example | AGENTS.md (always needed) |
| Props/API reference | AGENTS.md (always needed) |
| Deep architectural rationale | Link to ADR |
| Comprehensive edge cases | Separate reference doc |
| Historical context | ADR or commit history |

**Default to lean. Add detail only when its absence causes problems.**

---

## Documentation Analysis Mode

When asked to review existing documentation, evaluate progressively:

### Three-Level Analysis

| Level | Focus | Key Questions |
|-------|-------|---------------|
| **1. Presence** | Does it exist? | Root AGENTS.md? Component docs? Domain Guides? ADRs? |
| **2. Structure** | Does it follow templates? | Required sections present? Correct format? |
| **3. Semantic** | Is it accurate? | Matches code? Current patterns? Working examples? |

### Analysis Output Format

```markdown
## Documentation Analysis Report

**Scope:** [What was reviewed]
**Health Score:** [Good | Needs Attention | Critical]

**Findings:**
- 🔴 Critical: [Must fix issues]
- 🟡 Moderate: [Should fix issues]  
- 🟢 Minor: [Consider fixing]

**Recommended Actions:**
1. [Priority action]
2. [Next action]
```

---

## Using Templates

Templates are stored in `references/`. Load them when creating specific artifact types.

### Template Selection

| Creating... | Load Template |
|-------------|---------------|
| Project entry point | `references/template-root-agents.md` |
| Architectural decision | `references/template-adr.md` |
| Domain patterns | `references/template-domain-guide.md` |
| Component documentation | `references/template-component-agents.md` |

### Template Application Process

1. **Load the appropriate template**
2. **Fill required sections** — never skip required fields
3. **Adapt to context** — templates are starting points, not rigid forms
4. **Apply verbosity calibration** — right-size every section
5. **Validate against template checklist** — each template includes quality checks

---

## Anti-Patterns

Recognize and avoid these maintenance failures:

| Anti-Pattern | What It Looks Like | Why It's Wrong |
|--------------|-------------------|----------------|
| **Orphaned Components** | Component exists without AGENTS.md | Violates Law of Creation |
| **Modified ADRs** | Accepted ADR content was edited | Violates Law of Immutability |
| **Stale Domain Guides** | Patterns changed but guide wasn't updated | Violates Law of Reciprocity |
| **Documentation as TODO** | "Will document later" | Documentation is part of done |
| **Vague References** | "See the docs" without specific paths | Useless for navigation |
| **Novel-Length Docs** | Every section exhaustively detailed | Token waste, signal dilution |
| **Stub Documentation** | "TODO: fill this in" or empty sections | Incomplete work |
| **Copy-Paste Drift** | Same info in multiple places, now inconsistent | Single source of truth violated |

**When you spot an anti-pattern, fix it or flag it. Do not propagate it.**

---

## Quick Reference

### The Three Laws (Memorize These)

1. **Reciprocity:** If you use it and it's wrong, fix it
2. **Creation:** New code = new docs (1:1)
3. **Immutability:** Never edit accepted ADRs — supersede them

### Required Workflow

1. **Check-In** → Ground in Context Brain before coding (hard gate)
2. **Track** → Monitor what you reference, modify, create
3. **Report** → Activity Log at checkpoint and mid-task when meaningful
4. **Resolve** → Fix critical gaps before commit

### Gap Severity

- 🔴 **Critical** → Blocks commit (new components, breaking changes, new patterns)
- 🟡 **Moderate** → Recommended fix (stale docs, outdated references)
- 🟢 **Minor** → Noted (sparse coverage, nice-to-haves)

### Checkpoint Trigger Phrases

Activate documentation review when user says:
- "Ready to commit"
- "Let's wrap this up"
- "Create a PR"
- "Finalize this"
- "Ship it"
- "Done with the code"
- "Plan looks good" / "Approve the plan"
- "Start implementing"
- "Found the bug" / "Fixed it"

### Artifact Decision Shortcuts

- New component → Component AGENTS.md
- New pattern → Domain Guide
- "Why" decision → ADR
- New project → Root AGENTS.md
- Existing code changed → Check for doc updates
