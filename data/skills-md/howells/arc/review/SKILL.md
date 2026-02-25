---
name: review
description: |
  Run expert review on a plan with parallel reviewer agents. Presents findings as Socratic questions.
  Use when asked to "review the plan", "get feedback on the design", "check this approach",
  or before implementation to validate architectural decisions.

  Optional argument: reviewer name (e.g., `/arc:review daniel-product-engineer` to use a specific reviewer)
license: MIT
metadata:
  author: howells
website:
  order: 5
  desc: Get expert eyes
  summary: Get feedback from specialized reviewers—security, performance, architecture, and more. Runs automatically during ideate, or on-demand for any code.
  what: |
    Review spins up specialized agents based on what it's looking at—a new auth flow gets security and architecture reviewers, a database change gets the data engineer. Each agent reviews independently, then their feedback is consolidated into a prioritized list of concrete items: things to fix, questions to answer, risks to consider.
  why: |
    No single perspective catches everything. Review gives you a panel of experts without the scheduling overhead. It runs automatically at the end of /arc:ideate, but you can also invoke it on an entire app, a specific file, or a plan you're unsure about.
  decisions:
    - Runs during ideate automatically. You don't have to remember to ask for review.
    - Agent selection is dynamic. It picks reviewers based on what the code touches.
    - Output is prioritized and concrete. Not vague concerns—specific items you can act on.
  agents:
    - security-engineer
    - performance-engineer
    - architecture-engineer
    - data-engineer
    - senior-engineer
    - simplicity-engineer
    - designer
  workflow:
    position: spine
    after: ideate
---

<tool_restrictions>
# MANDATORY Tool Restrictions

## BANNED TOOLS — calling these is a skill violation:
- **`EnterPlanMode`** — BANNED. Do NOT call this tool. This skill has its own structured process. Execute the steps below directly.
- **`ExitPlanMode`** — BANNED. You are never in plan mode.
</tool_restrictions>

<required_reading>
**Read these reference files NOW:**
1. ${CLAUDE_PLUGIN_ROOT}/references/review-patterns.md
2. ${CLAUDE_PLUGIN_ROOT}/disciplines/dispatching-parallel-agents.md
3. ${CLAUDE_PLUGIN_ROOT}/disciplines/receiving-code-review.md
</required_reading>

<rules_context>
**Check for project coding rules:**

**Use Glob tool:** `.ruler/*.md`

**Determine rules source:**
- **If `.ruler/` exists:** Read rules from `.ruler/`
- **If `.ruler/` doesn't exist:** Read rules from `${CLAUDE_PLUGIN_ROOT}/rules/`

**Pass relevant core rules to each reviewer:**

| Reviewer | Rules to Pass |
|----------|--------------|
| daniel-product-engineer | react.md, typescript.md, code-style.md |
| lee-nextjs-engineer | nextjs.md, api.md |
| senior-engineer | code-style.md, typescript.md, react.md |
| architecture-engineer | stack.md, turborepo.md |
| simplicity-engineer | code-style.md |
| security-engineer | security.md, api.md, env.md |
| data-engineer | database.md, testing.md, api.md |
| senior-engineer | cloudflare-workers.md (if wrangler.toml exists) |
| accessibility-engineer | (interface rules only — already in agent prompt) |
| designer | design.md, colors.md, spacing.md, typography.md |
</rules_context>

<progress_context>
**Use Read tool:** `docs/progress.md` (first 50 lines)

Check for context on what led to the plan being reviewed.
</progress_context>

<process>
## Phase 0: Check for Specific Reviewer

**If argument provided** (e.g., `daniel-product-engineer`):
- Look for `${CLAUDE_PLUGIN_ROOT}/agents/review/{argument}.md`
- If found → use only this reviewer, skip Phase 2 detection
- If not found → list available reviewers from `${CLAUDE_PLUGIN_ROOT}/agents/review/` and ask user to pick

**Available reviewers:**
- `daniel-product-engineer` — Type safety, UI completeness, React patterns
- `lee-nextjs-engineer` — Next.js App Router, server-first architecture
- `senior-engineer` — Asymmetric strictness, review discipline
- `architecture-engineer` — System design, component boundaries
- `simplicity-engineer` — YAGNI, minimalism
- `performance-engineer` — Bottlenecks, scalability
- `security-engineer` — Vulnerabilities, OWASP
- `data-engineer` — Migrations, transactions
- `designer` — Visual design quality, UX fundamentals, AI slop detection
- `codex-reviewer` — Independent second opinion via OpenAI Codex CLI (different AI model)
- `gemini-reviewer` — Independent second opinion via Google Gemini CLI (different AI model)

## Phase 1: Find the Plan

**Check if plan file path provided as argument:**
- If yes → read that file and proceed to Phase 2
- If no → search for plans

**Search strategy:**

1. **Check conversation context first** — Look for Claude Code plan mode output
   - Look back through recent conversation messages
   - Search for plan structure markers:
     - "# Plan" or "## Plan" headings
     - "Implementation Steps" sections
     - Task lists with implementation details
     - Step-by-step procedures
   - If found → extract the plan content and proceed to Phase 2

2. **Search docs/plans/ folder** — Look for plan files

   **Use Glob tool:** `docs/plans/*.md`

   - Sort results by modification time (newest first)
   - Show all plan files (design, implementation, etc.)

3. **Present options if multiple found:**
   - List up to 5 most recent plans
   - Show: filename, modification date, brief preview
   - Ask user: "Which plan should I review?"

4. **If no plans found:**
   - "I couldn't find any plans in the conversation or in `docs/plans/`.
   - Can you point me to a plan file, or paste the plan you'd like me to review?"

**Once plan located:**
- Store the plan content
- Note the source (conversation, file path, or user-provided)
- Proceed to Phase 2

## Phase 2: Detect Project Type

**Skip if specific reviewer provided in Phase 0.**

**Detect project type for reviewer selection:**

**Use Grep tool on `package.json`:**
- Pattern: `"next"` → nextjs
- Pattern: `"react"` → react

**Use Glob tool:**
- `requirements.txt`, `pyproject.toml` → python

**Select reviewers based on project type:**

**TypeScript/React:**
- ${CLAUDE_PLUGIN_ROOT}/agents/review/daniel-product-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/senior-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/simplicity-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/architecture-engineer.md

**Next.js:**
- ${CLAUDE_PLUGIN_ROOT}/agents/review/lee-nextjs-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/daniel-product-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/senior-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/simplicity-engineer.md

**Python:**
- ${CLAUDE_PLUGIN_ROOT}/agents/review/senior-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/performance-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/architecture-engineer.md

**General/Unknown:**
- ${CLAUDE_PLUGIN_ROOT}/agents/review/senior-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/architecture-engineer.md
- ${CLAUDE_PLUGIN_ROOT}/agents/review/simplicity-engineer.md

**Conditional addition (all UI project types):**
- If plan involves UI components, forms, or user-facing features → add `${CLAUDE_PLUGIN_ROOT}/agents/review/accessibility-engineer.md`
- If plan involves UI components, pages, or visual design → add `${CLAUDE_PLUGIN_ROOT}/agents/review/designer.md`

## Phase 2.5: Team Mode Check

<team_mode_check>
**Skip if specific reviewer was provided in Phase 0** (single reviewer, no team needed).

**Check if agent teams are available** by attempting to detect team support in the current environment.

**If teams are available**, offer the user a choice:

```
Execution mode:
1. Team mode — Reviewers challenge each other's findings before you see them (higher quality, 3-5x token cost)
2. Standard mode — Independent reviewers, findings consolidated by skill (faster, lower cost)
```

Use AskUserQuestion with:
- **"Team mode"** — Reviewers cross-review and debate findings. Questions that survive peer scrutiny are stronger. Best when reviewing complex or high-stakes plans.
- **"Standard mode (Recommended)"** — Independent reviewers run in parallel. Faster and cheaper. Good default for most reviews.

**If teams are NOT available**, proceed silently with standard mode. Do not mention teams to the user.

**If team mode selected**, read the team reference:
```
${CLAUDE_PLUGIN_ROOT}/references/agent-teams.md
```
</team_mode_check>

## Phase 3: Run Expert Review

**If specific reviewer from Phase 0:** Spawn single reviewer agent.

**If team mode selected:** Run team review (see Team Execution below).

**Otherwise:** Spawn 3 reviewer agents in parallel:

```
Task [reviewer-1] model: sonnet: "Review this plan for [specialty concerns].
Plan:
[plan content]

Focus on: [specific area based on reviewer type]"

Task [reviewer-2] model: sonnet: "Review this plan for [specialty concerns]..."

Task [reviewer-3] model: sonnet: "Review this plan for [specialty concerns]..."
```

### Team Execution (Agent Teams mode)

Only if user opted into team mode in Phase 2.5.

Create team `arc-review-[plan-slug]` with the 3 selected reviewers as teammates.

**Round 1 — Initial Review:**

Each reviewer performs their standard analysis independently (same prompts as standard mode).

```
Create team: arc-review-[plan-slug]
Teammates: [reviewer-1], [reviewer-2], [reviewer-3]

Each teammate reviews the plan through their domain lens.
Same prompts and focus areas as standard mode.
```

**Round 2 — Cross-Review:**

Each reviewer reads the others' findings and responds:
- **"My analysis supports this"** — Confirms another reviewer's concern with additional evidence
- **"My analysis addresses that"** — Points out that their recommendation already handles the concern
- **"I disagree because"** — Challenges a finding with code-level evidence or domain reasoning

**Resolution rules (from agent-teams reference):**
- Code-level evidence wins over principle-based reasoning
- Domain authority wins within domain
- Every challenge must include explicit rationale

**Round 2 output:** Pre-debated findings where each concern has either been confirmed by peers, refined through challenge, or dropped with stated rationale.

**Wait for team to complete.**

**If team creation fails**, fall back silently to standard parallel dispatch above.

## Phase 4: Consolidate and Present

<team_consolidation>
**If team mode was used**, consolidation is simpler:

- Findings already survived peer scrutiny — false positives were caught and removed during debate
- Conflicting recommendations already resolved with rationale from both sides
- Socratic questions derived from team-debated findings carry more weight: "Two reviewers independently flagged this — what if we..."
- Focus on transforming debated findings into questions (skip deduplication and conflict resolution)
</team_consolidation>

**Transform findings into Socratic questions:**

See `${CLAUDE_PLUGIN_ROOT}/references/review-patterns.md` for approach.

Instead of presenting critiques:
- Turn findings into exploratory questions
- "What if we..." not "You should..."
- Collaborative spirit, not adversarial

**Example transformations:**
- Reviewer: "This is overengineered"
  → "We have three layers here. What if we started with one?"
- Reviewer: "Missing error handling"
  → "What happens if the API call fails? Should we handle that now or later?"
- Reviewer: "Security concern"
  → "This stores the token in localStorage. Is that acceptable for this use case?"

**Present questions one at a time:**
- Wait for user response
- If user wants to keep something, they probably have context
- Track decisions as you go

## Phase 5: Apply Decisions

For each decision:
- Note what was changed
- Note what was kept and why

If plan came from a file:
- Update the file with changes
- Commit: `git commit -m "docs: update <plan> based on review"`

## Phase 6: Summary and Next Steps

```markdown
## Review Summary

**Reviewed:** [plan name/source]
**Reviewers:** [list]

### Changes Made
- [Change 1]
- [Change 2]

### Kept As-Is
- [Decision 1]: [reason]

### Open Questions
- [Any unresolved items]
```

**Show remaining arc:**
```
/arc:ideate     → Design doc (on main) ✓
     ↓
/arc:review     → Review ✓ YOU ARE HERE
     ↓
/arc:implement  → Plan + Execute task-by-task
```

**Offer next steps based on what was reviewed:**

If reviewed a **design doc**:
- "Ready to implement?" → `/arc:implement` (which will create the plan internally)
- "Done for now" → end

If reviewed an **implementation plan**:
- "Ready to implement?" → `/arc:implement`
- "Done for now" → end

## Phase 7: Cleanup

**Kill orphaned subagent processes:**

After spawning reviewer agents, some may not exit cleanly. Run cleanup:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/cleanup-orphaned-agents.sh
```

</process>

<arc_log>
**After completing this skill, append to the activity log.**
See: `${CLAUDE_PLUGIN_ROOT}/references/arc-log.md`

Entry: `/arc:review — [Plan name] reviewed`
</arc_log>

<success_criteria>
Review is complete when:
- [ ] Plan located (conversation, file, or user-provided)
- [ ] Project type detected and reviewers selected
- [ ] Parallel expert review completed (3 agents)
- [ ] All findings presented as Socratic questions
- [ ] User made decisions on each finding
- [ ] Plan updated (if from file)
- [ ] Summary presented
- [ ] Remaining arc shown (based on plan type)
- [ ] User chose next step (detail/implement or done)
- [ ] Progress journal updated
- [ ] Orphaned agents cleaned up
</success_criteria>
