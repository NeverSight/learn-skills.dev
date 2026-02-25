---
name: spec-development
description: Research, discuss, and write specs. Use this when creating or refining specs.
version: 1.0.0
---

# spec-development

## Overview

Research and develop specs through collaborative discussion. Spec-first approach - no jumping to action. Every process gets specced before implementation.

**Announce at start:** "Using spec-development. What are we speccing?"

**When spec is ready:** Switch to `spec-execution` skill to execute it.

---

## Core Principles

### 1. User Decides, Agent Proposes

The user has decision-making authority, not the agent. The agent proposes options, provides analysis, and makes recommendations - but the user makes all decisions.

**Agent responsibilities:**
- Present options with pros/cons
- Make recommendations with rationale
- Ask for confirmation before acting

> **Tool tip:** When presenting options or asking for choices, use structured question tools when available (`AskQuestion`, `AskUserQuestion` or similar). These provide a better UX than plain text options.

**Never assume a decision on behalf of the user:**
- **Wrong:** "I'll use approach A since it's faster"
- **Right:** "Two options: A (faster) or B (safer). I recommend A because [reason]. Which do you prefer?"

**Even when confident, confirm:**
- **Wrong:** "This is clearly a bug, I'll fix it"
- **Right:** "This looks like a bug - [description]. Should I fix it?"

### 2. Discussion by Default

When user input is ambiguous, assume they want to discuss, not act.

**User says:** "the screenshot process needs work"
- **Wrong:** Start editing the screenshot process
- **Right:** "What's not working? The steps, the naming, something else?"

**User says:** "add priority to the table"
- **Wrong:** Add a Priority column with your best guess
- **Right:** "How should priority be defined?"

### 3. Define Before Use

Never use vague or undefined terms. If a concept isn't defined, define it first.

**Wrong:** "High priority = significant market presence"
**Right:** "How is priority defined? Proposal: High = 3+ sources, Medium = 2, Low = 1"

### 4. Propose, Show, Confirm

Never make changes without showing exactly what will change and getting confirmation.

**Pattern:**
1. State what you propose
2. Show the exact change (the actual text/code)
3. Ask for confirmation
4. Only then execute

### 5. One Thing at a Time

Don't bundle multiple changes or questions. Each message should address one thing.

**Wrong:** "I'll add the template, update the criteria, and fix the naming convention"
**Right:** "First, let's define the template. Here's what I propose: [show]. Does this work?"

### 6. Trace Decisions

Document why decisions were made, not just what was decided.

In specs, include rationale:
```markdown
**Priority criteria:**
- High: 3+ sources
- Medium: 2 sources
- Low: 1 source

> Rationale: Based purely on mention frequency. Simple, concrete, measurable.
```

### 7. Don't Assume, Verify

Never guess or infer. Always research and check.

- Need a command? Check the docs
- API returns data? Check the actual response, don't assume structure
- Build succeeded? Check the output, don't assume
- File exists? Verify, don't assume from context
- User says X is broken? Reproduce before fixing

### 8. Cross-Reference, Don't Duplicate

Link to existing specs instead of restating. Keep specs DRY.

**Wrong:** Copy the criteria into every research doc
**Right:** `> **Spec**: [../README.md](../README.md)`

### 9. Template Everything

If a process will repeat, create a template in the spec.

Templates should include:
- Structure with placeholders
- Example of filled-in version
- Where the template lives (which spec doc)

### 10. Log Everything (With Permission)

Log what's defined, ask about the rest.

**Log without asking:**
- What the skill explicitly requires (step completion, test results, bugs, status updates)

**Ask before logging:**
- Any action, decision, or finding not explicitly required
- Investigations, design decisions, context, side discoveries

**Pattern:**
- Do the work
- Ask: "Should I log [this finding/decision/investigation]?"
- If yes, log it; if no, move on

**Wrong:** Assume everything should be logged and document without asking
**Wrong:** Skip logging something potentially valuable without asking
**Right:** "I checked for similar issues in other files and found none. Should I log this investigation?"

---

## Process

### Step 1: Create Research File

Every spec development starts with a research file. This captures the discussion, decisions, and rationale that lead to the spec.

**Actions:**
1. Propose a location for the spec folder (naming convention: `[year]-[month]-[day]-[work-name]`)
2. Get user confirmation on location
3. Create `research.md` before any discussion or investigation

**This is blocking** - do not proceed until research file exists.

**Research file template:** [assets/research-template.md](assets/research-template.md)

### Step 2: Research & Discuss

Investigate and discuss until the spec can be written with no ambiguity.

**Activities:**
- Understand scope - what is this spec for? What processes does it cover?
- Work from concrete examples - start with a real case, then generalize
- Define all terms - every term used must have a clear definition
- Ask clarifying questions:
  - "How is [term] defined?"
  - "What's the inclusion/exclusion criteria?"
  - "Should this be a template?"
  - "Where does this get documented?"
  - "Is there an existing spec this should reference?"

**Update research file immediately** after each:
- **Finding** - something you learned
- **Decision** - a decision made by the user
- **Answer** - a question that got resolved

**Rules:**
- Never batch updates - update immediately after each finding
- Only log decisions after user has made them (agent proposes, user decides)
- Strike through answered questions, add answer reference

### Step 3: Confirm Research Complete

Before writing the spec, explicitly confirm with the user:

> "I believe research is complete. We have:
> - [summary of key decisions]
> - [summary of defined terms]
> - [any open questions resolved]
>
> Ready to write the spec?"

**Do not proceed to spec writing without user confirmation.**

**The user decides when research is complete.** The agent may propose that research seems sufficient, but only the user can confirm readiness to proceed.

### Step 4: Write the Spec

Create `spec.md` in the same folder as research.

**Spec template:** [assets/spec-template.md](assets/spec-template.md)

**Required sections:**
- Header (Status, Created, Research link)
- Overview (what + current/target state)
- Scope (In Scope / Out of Scope)
- Steps (with Action, Files, Changes, Verification per step)
- Verification Checklist (overall checks after all steps)
- Execution Plan (mode + rationale)

**Optional sections** (add as needed):
- Context/Background - domain-specific info
- Testing Plan - manual/automated testing
- Rollback Plan - if changes are risky

### Step 5: Confirm Spec Complete

After all sections are written, ask the user to approve the spec as final:

> "The spec is drafted. All sections complete. Is this spec approved and ready for execution?"

**The user decides when the spec is ready.** Do not consider the spec final or begin execution until the user explicitly approves it.

---

## Execution Plan Requirement

Every spec must include an execution plan. Before finalizing, propose the execution mode and get user confirmation:

> "For execution, I recommend [Direct/Subagents] because [reason]. Does this work?"

If Subagents, also propose: sequential steps, parallel steps, max concurrent.

**Recommendation guidelines:**
- Default: Direct (especially for coding)
- Subagents only when: many similar items (5+), detailed unambiguous steps, items are independent

**The user decides.** Agent provides recommendation with rationale; user confirms or chooses differently.

---

## When to Switch to Execution

After the spec is approved, switch to the `spec-execution` skill to execute it.

| Situation | Action |
|-----------|--------|
| Spec approved and ready | Switch to `spec-execution` |
| User wants to start executing | Switch to `spec-execution` |
| Gap found during execution | Return here to fill the gap, then back to execution |

---

## Anti-Patterns

**Don't do these:**

| Anti-Pattern | Instead |
|--------------|---------|
| Jump to editing when user mentions a file | Ask what they want to change |
| Use undefined terms ("market presence") | Define terms first |
| Bundle multiple changes | One change at a time |
| Assume file contents | Read the file |
| Guess at commands | Check documentation |
| Say "I'll do X, Y, and Z" | "First, let's address X. [details]. OK?" |
| Start writing spec without research file | Create research file first |
| Write spec before user confirms research complete | Confirm research complete first |

---

## Checklist

Before taking any action:
- [ ] Have I created a research file?
- [ ] Have I defined all terms I'm using?
- [ ] Have I confirmed with user before proceeding to next step?
- [ ] Am I doing one thing, not multiple things?
- [ ] Have I updated the research file with this finding/decision?
