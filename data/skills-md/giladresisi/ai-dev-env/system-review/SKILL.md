---
name: system-review
description: Use when performing a meta-level analysis of plan adherence after implementation to identify process improvements and suggest CLAUDE.md updates
---

# System Review

Perform a meta-level analysis of how well the implementation followed the plan and identify process improvements.

## Purpose

**System review is NOT code review.** You're not looking for bugs in the code - you're looking for bugs in the process.

**Your job:**

- Analyze plan adherence and divergence patterns
- Identify which divergences were justified vs problematic
- Surface process improvements that prevent future issues
- Suggest updates to Layer 1 assets (CLAUDE.md, plan templates, skills)

**Philosophy:**

- Good divergence reveals plan limitations → improve planning
- Bad divergence reveals unclear requirements → improve communication
- Repeated issues reveal missing automation → create skills

## Context & Inputs

You will analyze key artifacts:

**PROGRESS.md:**
Read this to find all notes for the current feature including:
- Planning phase notes
- Execution phase notes
- Execution report (what was actually done and why)

**Generated Plan:**
Read this to understand what the agent was SUPPOSED to do.
Look up plan file location from PROGRESS.md

**Execution Report & Code Review:**
Read `.agents/execution-reports/` and `.agents/code-reviews/` for this feature if they exist — they document divergences, challenges, and issues found post-execution.

**Skills used in the session:**
Identify which `ai-dev-env:*` skills were invoked (from PROGRESS.md, session summary, or conversation context). These are the skills you will inspect and improve in Step 6.

## Analysis Workflow

### Step 0: Read PROGRESS.md

**MANDATORY FIRST STEP:**

1. Read `PROGRESS.md` to find the feature being reviewed
2. Extract the plan file location from planning phase notes
3. Read the execution report section to understand what was actually done
4. Use this context for the remaining analysis steps

### Step 1: Understand the Planned Approach

Read the generated plan (from PROGRESS.md reference) and extract:

- What features were planned?
- What architecture was specified?
- What validation steps were defined?
- What patterns were referenced?

### Step 2: Understand the Actual Implementation

Read the execution report from PROGRESS.md and extract:

- What was implemented?
- What diverged from the plan?
- What challenges were encountered?
- What was skipped and why?

### Step 3: Classify Each Divergence

For each divergence identified in the execution report, classify as:

**Good Divergence ✅** (Justified):

- Plan assumed something that didn't exist in the codebase
- Better pattern discovered during implementation
- Performance optimization needed
- Security issue discovered that required different approach

**Bad Divergence ❌** (Problematic):

- Ignored explicit constraints in plan
- Created new architecture instead of following existing patterns
- Took shortcuts that introduce tech debt
- Misunderstood requirements

### Step 4: Trace Root Causes

For each problematic divergence, identify the root cause:

- Was the plan unclear, where, why?
- Was context missing, where, why?
- Was validation missing, where, why?
- Was manual step repeated, where, why?

### Step 5: Generate Process Improvements

Based on patterns across divergences, suggest:

- **CLAUDE.md updates:** Universal patterns or anti-patterns to document
- **Plan skill updates:** Instructions that need clarification or missing steps
- **New skills:** Manual processes that should be automated
- **Validation additions:** Checks that would catch issues earlier

## Output Format

**CRITICAL: Create review in `.agents/system-reviews/` folder**

### Step 1: Determine Feature Name

Extract the feature/module name from PROGRESS.md or the execution report.
Example: "module-5-multi-format-enhancement" from execution report path

### Step 2: Create Detailed System Review

**Create file:** `.agents/system-reviews/{feature-name}.md`

**Use Write tool to create this file with the following structure:**

```markdown
# System Review: [Feature Name]

**Generated:** [Current date/time]

## Meta Information
- Plan reviewed: [path to plan file]
- Execution report: `.agents/execution-reports/{feature-name}.md`
- Executor: [team-based/sequential/etc]
- Date: [current date]

## Overall Alignment Score: X/10

**Scoring rationale:**
- [breakdown of scoring]

[Summary paragraph explaining overall alignment]

## Divergence Analysis

### Divergence 1: [Title]
```yaml
divergence: [what changed]
planned: [what plan specified]
actual: [what was implemented]
reason: [agent's stated reason from report]
classification: good ✅ | bad ❌ | environmental ⚠️
justified: yes/no
root_cause: [unclear plan | missing context | etc]
impact: [describe impact]
```

**Assessment:** [detailed analysis of this divergence]

[Repeat for each divergence]

## Pattern Compliance

- ✅/❌ Followed codebase architecture (details)
- ✅/❌ Used documented patterns (from CLAUDE.md) (details)
- ✅/❌ Applied testing patterns correctly (details)
- ✅/❌ Met validation requirements (details)

**Exemplary/Concerning:** [highlight notable observations]

## System Improvement Actions

### Update CLAUDE.md:

- [x]/[ ] Document [pattern X] discovered during implementation:
  ```markdown
  [Actual suggested text to add]
  ```

- [x]/[ ] Add anti-pattern warning for [Y]:
  ```markdown
  [Actual suggested text to add]
  ```

### Update [skill-name] skill:

- [ ] Add [specific instruction]:
  ```markdown
  [Actual suggested text to add]
  ```

### Create New Skill:

- [ ] `[skill-name]` for [manual process]
  - [Description of skill purpose]

## Key Learnings

### What worked well:

1. **[Category]:** [specific observation]
2. **[Category]:** [specific observation]

### What needs improvement:

1. **[Category]:** [specific gap identified]
2. **[Category]:** [specific gap identified]

### For next implementation:

1. **[Action]:** [concrete improvement to try]
2. **[Action]:** [concrete improvement to try]

## Process Quality Assessment

**Planning Phase:** ✅/⚠️/❌ [Rating]
- [observations and details]

**Execution Phase:** ✅/⚠️/❌ [Rating]
- [observations and details]

**Validation Phase:** ✅/⚠️/❌ [Rating]
- [observations and details]

**Documentation:** ✅/⚠️/❌ [Rating]
- [observations and details]

## Recommended CLAUDE.md Additions

Based on patterns discovered during this implementation, add these sections:

### 1. [Pattern Category]
```markdown
[Complete markdown text to add to CLAUDE.md]
```

### 2. [Pattern Category]
```markdown
[Complete markdown text to add to CLAUDE.md]
```

---

## Conclusion

**Overall Assessment:** [comprehensive summary]

**Process Improvements Identified:**
- [improvement 1] ✅/[ ] (status)
- [improvement 2] ✅/[ ] (status)

**Recommended Actions:**
1. [action with priority]
2. [action with priority]

**Ready for Next Module:** Yes/No - [reasoning]
```

### Step 3: Update PROGRESS.md

**Use Edit tool to add/update in PROGRESS.md under the current feature:**

```markdown
### Reports Generated

**Execution Report:** `.agents/execution-reports/{feature-name}.md`
- [Brief summary of execution report]

**System Review:** `.agents/system-reviews/{feature-name}.md`
- Alignment score: X/10
- Divergence analysis (X identified: Y justified, Z problematic)
- Process improvements and CLAUDE.md updates [completed/recommended]
- Key learnings and recommendations for next implementation
```

**Do NOT include the full review content in PROGRESS.md - only the reference.**

## Step 6: Auto-Update Used Skills via Worktree + PR

After completing the system review document (Steps 1–5 and Output Format), inspect and update the SKILL.md files for every skill that was invoked in this session. Changes go through a worktree + pull request — never directly into `~/.claude/`.

### 6.1 Identify Skills Used

Scan the following sources to build the list of invoked skills:
- PROGRESS.md "Reports Generated" or "Skill Improvements Applied" sections
- The session summary or conversation context — look for `ai-dev-env:*` skill invocations
- The system review document you just wrote — the "Skills invoked" line in Meta Information

**Skills to look for (any that were used):**
`execute`, `acceptance-criteria-validate`, `acceptance-criteria-define`, `code-review`, `code-review-fix`, `plan-feature`, `execution-report`, `system-review`

### 6.2 Locate the ai-dev-env Source Repo

The canonical source repo is at `~/projects/ai-dev-env`. Verify it exists:
```bash
ls ~/projects/ai-dev-env/skills/
```

If it doesn't exist, the repo may need to be cloned first. The remote is visible in the cached copy:
```bash
cd ~/.claude/plugins/cache/ai-dev-env-marketplace/ai-dev-env/1.0.0 && git remote -v
```

**Never edit files under `~/.claude/plugins/` directly** — that is an installed cache. Changes there are not tracked in the source repo and will be overwritten on next plugin update.

### 6.3 Create a Worktree

Use the `ai-dev-env:create-worktree` skill with `origin/main` as the base branch so the worktree starts from the remote state, not any local divergence:

```
/create-worktree improve-skills-from-<feature-name> origin/main
```

Replace `<feature-name>` with the slug of the feature just reviewed (e.g., `extractive-summarization`).

The working directory for subsequent steps will be `../ai-dev-env-skill-improvements`.

### 6.4 Identify Skill-Specific Improvements

For each skill, review the divergence analysis, code review findings, and challenges from this session and ask: **"What instruction was missing from this skill that would have prevented this issue?"**

Apply improvements in these priority tiers:

**Tier 1 — Missing mandatory step:** A process step that should have been enforced but wasn't. Add it explicitly with MANDATORY language.

**Tier 2 — Ambiguous instruction:** An instruction that led to two valid interpretations, one of which caused a problem. Clarify it.

**Tier 3 — Missing context:** The skill lacked awareness of project conventions it needed. Update the instruction to be more flexible or explicit.

**Do NOT apply:**
- Improvements specific to this one project that wouldn't generalize
- Changes that make a skill more rigid when current flexibility is intentional
- Rewrites of sections that worked correctly

### 6.5 Apply Changes in the Worktree

For each improvement identified:
1. Read the target SKILL.md in the worktree fully before editing
2. Use the **Edit tool** to apply targeted changes — never rewrite the whole file
3. Keep each change focused: one issue → one edit

### 6.6 Verify, Commit, Push, and Open PR

```bash
cd ~/projects/ai-dev-env-skill-improvements
git diff --stat   # verify only intended lines changed

git add skills/<skill-name>/SKILL.md ...
git commit -m "improve <skills>: <one-line summary of what changed and why>"

git push -u origin improve-skills-from-<feature-name>

gh pr create --title "Improve skills from <feature-name> session learnings" --body "..."
```

In the PR body, list each skill changed, what was changed, and the session evidence that motivated it.

### 6.7 Document in PROGRESS.md

After the PR is open, add a "Skill Improvements Applied" section to PROGRESS.md:

```markdown
### Skill Improvements Applied

**PR:** <GitHub PR URL>
**Branch:** `improve-skills-from-<feature-name>`

| Skill | Change | Reason |
|-------|--------|--------|
| `execute` | ... | ... |
```

---

## Important

- **Be specific:** Don't say "plan was unclear" - say "plan didn't specify which auth pattern to use"
- **Focus on patterns:** One-off issues aren't actionable. Look for repeated problems.
- **Action-oriented:** Every finding should have a concrete asset update suggestion
- **Suggest improvements:** Don't just analyze - actually suggest the text to add to CLAUDE.md or skills
- **For skill edits:** Always work in a worktree of `~/projects/ai-dev-env`, never in `~/.claude/plugins/`