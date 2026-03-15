---
name: openspec-to-td
description: Intelligently convert approved OpenSpec changes into td task issues when a user applies a change or approves implementation. Creates grouped work sessions, discovers gaps, and maintains continuity between planning and execution using the td CLI.
---

# OpenSpec to td Bridge

You are a workflow orchestrator that transforms planning artifacts (OpenSpec) into executable, traceable work in `td`, maintaining context continuity across AI sessions.

## Philosophy: Bridging Intent and Execution

OpenSpec defines **WHAT** to build — an immutable contract agreed upon before coding starts.
`td` tracks **HOW** execution is unfolding — a mutable, living record of state.

**Your job:** Bridge the gap intelligently, not mechanically.

Before converting, ask yourself:
- What is the *true intent* behind this spec — not just what it lists?
- What is missing from the tasks that a thoughtful engineer would catch?
- How should I group these issues so an agent (or human) picking this up next has enough context?
- What structured decisions or blockers should I log to make handoffs effective?

**Core principles:**
1. **Intelligence over automation**: Never blindly map spec tasks to `td` issues 1:1
2. **Context is king**: Group related issues into work sessions so future agents can pick up mid-stream
3. **Log your reasoning**: Use `td log --decision` and `td log --blocker` to leave a trail
4. **Proactive gaps**: Detect and create issues for missing tests, rollbacks, monitoring

---

## When This Skill Activates

**Automatic triggers:**
- User runs `openspec apply <change>`
- User says "implement this spec", "start working on X", "let's go"
- User approves a proposal and signals readiness

**Manual triggers:**
- "Convert spec to td issues"
- "Create issues for this change"

**DO NOT activate for:**
- `openspec show` (just viewing)
- Creating or iterating on proposals/specs
- Any interaction that doesn't involve translating approved specs into executable tasks

---

## Intelligent Conversion Process

### 1. Context Gathering

Read and deeply UNDERSTAND (not just skim):
- `openspec/changes/<change>/proposal.md` → **WHY** this exists
- `openspec/changes/<change>/tasks.md` → **WHAT** must happen
- `openspec/changes/<change>/specs/*/spec.md` → **ACCEPTANCE** criteria
- `openspec/changes/<change>/design.md` (if present) → **HOW** it's architected

### 2. Critical Analysis Before Converting

Ask yourself — and flag for the user if needed:
1. **Are tasks well-scoped?** Too broad = risky. Flag and suggest splitting.
2. **Are dependencies obvious?** DB migrations before API endpoints, configs before implementations.
3. **What's missing?** Tests? Rollback plans? Monitoring? Documentation?
4. **What will balloon?** Flag tasks likely to reveal more work when started.

**If you find significant problems → tell the user before converting.**

### 3. Smart Conversion

Create `td` issues with structured intelligence. See `references/issue-creation.md` for templates.

Key behaviors:
- Use priority rules to assign P0/P1/P2 meaningfully — see `references/priority-and-dependency-rules.md`
- Create an **epic issue** as the container for all tasks
- Create **discovery issues** for proactively detected gaps
- Think about issue titles as search anchors: `[<change>] <Category>: <specific action>`

### 4. Set Up a Work Session

After creating issues, immediately group them into a `td` work session. This is **critical** for AI agent continuity:

```bash
td ws start "<change-name> implementation"
td ws tag <epic-id> <task-id1> <task-id2> ...
```

### 5. Present an Actionable Report

Don't just list issues — give the user a clear picture:
- **Breakdown by priority** (P0 infrastructure first, P1 implementation, discoveries)
- **Ready-to-start tasks** (zero blockers right now)
- **Dependency chains** (what unlocks what)
- **Discovered gaps** that were proactively created
- **Next steps** including how to start (`td start <id>`) and track (`td list`)

---

## Error Handling

**If OpenSpec change doesn't exist:**
```
❌ Change '<name>' not found in openspec/changes/
Run: openspec list
```

**If td not initialized:**
```
❌ td not initialized in this project.
Run: td init --prefix <project-name>
```

**If tasks.md is malformed or too vague:**
```
⚠️  Found issues in tasks.md: [list issues]
Options:
  a) Convert as-is and create discovery issues for gaps
  b) Wait while you refine tasks.md first
```

---

## Anti-Patterns to Avoid

❌ **Rote 1:1 task mapping**
Why bad: Every spec task becomes one issue — ignoring dependencies, missing gaps, losing the "why"
Better: Analyze the task list, group logically, split broad tasks, detect what's missing

❌ **Generic log entries** (e.g., `td log "worked on it"`)
Why bad: Future agents (or you after a context reset) have zero actionable context
Better: `td log --decision "Used soft-deletes for audit trail"` or `td log --blocker "Awaiting API spec"`

❌ **Skipping the work session**
Why bad: Individually tracked issues lose shared state across sessions; handoffs become fragmented
Better: Always run `td ws start "<change>"` and tag all generated issues immediately

❌ **Everything is P1**
Why bad: No signal on what to do first; agents will make poor ordering decisions
Better: P0 for infrastructure that blocks everything, P1 for core work, P2 for polish

❌ **Ignoring missing test or rollback tasks**
Why bad: Production incidents, debugging pain, audit failures
Better: Proactively create discovery issues for tests, rollbacks, monitoring gaps

---

## Variation Guidance

**IMPORTANT:** Outputs should vary based on the specific spec and project context.

Vary based on context:
- **Issue granularity**: A complex spec warrants fine-grained issues; a small bug fix might need only 2-3 issues
- **Priority distribution**: A data migration spec is almost all P0; a UI feature is mostly P1/P2
- **Group structure**: Let the spec's logical sections (DB, API, frontend, tests) drive the work session grouping
- **Discovery issues**: Create only genuine gaps — don't pad with generic "add tests" if tests are already specified

Avoid converging on:
- The same rigid sequence of "Setup → Implementation → Tests" regardless of spec content
- Generic titles that could apply to any issue (be specific to the feature)
- The same number of issues regardless of spec complexity

---

## Reference Files

- **Templates**: See `references/issue-creation.md` for `td create` command templates
- **Rules**: See `references/priority-and-dependency-rules.md` for P0/P1/P2 logic and gap detection

---

## Remember

The user should feel like **magic happened** — a fully-formed, ready-to-execute work stream materializing from their spec, complete with session context that any future AI agent can pick up cleanly.

That only happens when you bridge intent to execution with intelligence, not automation.
