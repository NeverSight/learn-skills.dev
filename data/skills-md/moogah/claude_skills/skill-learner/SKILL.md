---
name: skill-learner
description: "Reviews conversation context to identify learnings and patterns that should be captured in skills. Use when the user asks to review the session for skill creation or updates."
---

# Skill Learner

## Overview

This skill reviews the conversation context to identify learnings worth capturing in the skills system. When invoked, it analyzes the session to find patterns, corrections, and insights that should be incorporated through skill updates or new skill creation.

## Core Principles

- **Capture only non-obvious, repeatable patterns** - Skip trivial one-off tasks
- **Extend existing skills when related; create new ones for distinct domains** - Avoid skill proliferation
- **Always review with user before implementing** - Never assume, always ask
- **Start new skills minimal and concise** - Incorporate only direct observations, grow through iteration
- **Consider appropriate hierarchy** - Local skills for repo-specific, user-level for broadly applicable

## Workflow

The skill-learning process follows four sequential steps:

1. **Review** - Analyze conversation context to identify learnings
2. **Assess** - Evaluate significance and filter out noise
3. **Determine** - Decide on action type (update/create, local/user-level)
4. **Propose** - Present findings and get user approval to implement

## Step 1: Reviewing Context for Learnings

When invoked, review the conversation context looking for these patterns:

### Explicit Corrections
User directly corrects Claude's approach or provides specific guidance:
- "Actually, do it this way instead..."
- "In this repo, we always..."
- "No, use X not Y because..."
- Corrects terminology or technical approach

### Repeated Patterns
Similar tasks or requests appear multiple times:
- Claude solves same type of problem 3+ times in session
- User makes same request with consistent requirements
- User repeatedly provides same context or explanation

### Repo-Specific Conventions
User mentions patterns specific to the codebase:
- Specific testing patterns: "Always run X before Y"
- Code style preferences beyond linters
- Deployment or build procedures
- Team-specific workflows or architectures
- Database connection patterns or schemas

### Performance Struggles Leading to Insights
Claude struggles then succeeds after receiving key information:
- Multiple approaches attempted before success
- User provides crucial missing context that unlocks solution
- Error patterns that required specific fixes
- Discovery of non-obvious dependencies or requirements

### Coverage Gaps
Tasks that don't trigger any existing skill:
- User requests help with tasks Claude handles only generically
- User mentions tools/frameworks that could benefit from specialized guidance
- Workflow sequences that would be valuable to formalize

## Step 2: Assessing Significance

Use decision-framework.md for detailed criteria. Key filters:

### Significance Threshold
- **Capture** if: Appears 2-3+ times OR user explicitly states importance
- **Filter out** if: One-off task, trivial variation, already obvious to Claude

### Non-Obvious Check
- **Capture** if: Contains information Claude wouldn't know by default
- **Filter out** if: Claude already knows this from training

### Future Applicability
- **Capture** if: Will apply to future similar tasks
- **Filter out** if: Highly specific to current unique context

### Examples of What to Filter Out
- Single typo fixes
- Standard operations Claude already handles well
- User preferences that are inconsistent or one-time
- Information that's easily discoverable from code/docs

See references/decision-framework.md for flowcharts and references/examples.md for concrete scenarios.

## Step 3: Determining Action Type

Make two key decisions about how to capture the learning:

### Decision 1: Update Existing vs Create New

**Update existing skill when:**
- Learning directly relates to an existing skill's domain
- Fills a gap or corrects information in existing skill
- Extends capabilities of existing workflow
- Examples: Adding PDF watermark to pdf skill, adding testing pattern to existing testing skill

**Create new skill when:**
- Learning represents a distinct domain or capability
- No existing skill covers this area
- Would make existing skill unfocused or too broad
- Examples: First-time repo deployment process, new database-specific patterns

**Principle:** Prefer updates to avoid skill proliferation, but don't force unrelated content together.

### Decision 2: Local vs User-Level

**Local (.claude/skills in repo) when:**
- Specific to this codebase's architecture
- References specific file paths, modules, or components in this repo
- Tied to team conventions that wouldn't apply elsewhere
- Contains repo-specific schemas, APIs, or data structures
- Examples: "repo-deployment", "project-database-queries"

**User-level (~/.claude/skills) when:**
- Generally applicable engineering best practices
- Language/framework patterns (React, Python, testing strategies)
- Tool usage patterns (git workflows, docker commands)
- Cross-project workflow improvements
- Examples: "code-formatting-preferences", "testing-best-practices"

**When uncertain:** Start user-level. It's easier to migrate to local later if needed.

## Step 4: Proposing Changes to User

After reviewing the context and identifying learnings, present findings to the user for approval.

### Proposal Format

Summarize what was found and propose specific actions:

```
I reviewed the conversation and identified [number] learnings worth capturing:

1. [Learning description] - This seems worth capturing because [reason]
   → Suggest: [updating skill-name / creating new skill-name]
   → Key additions:
     - [Point 1]
     - [Point 2]

2. [Learning description] - This seems worth capturing because [reason]
   → Suggest: [updating skill-name / creating new skill-name]
   → Key additions:
     - [Point 1]
     - [Point 2]

Which of these would you like me to implement?
```

### If No Learnings Found

If the review doesn't reveal significant learnings worth capturing:

```
I reviewed the conversation but didn't find patterns that meet the criteria for skill creation or updates:
- [Brief explanation of what was reviewed and why nothing qualified]

The session covered [summary], which [already handled well by existing skills / too specific to generalize / etc.].
```

## Step 5: Implementing the Change

Once approved, execute the skill change promptly and efficiently.

### For New Skills

1. **Initialize structure:**
   ```bash
   ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <~/.claude/skills OR .claude/skills>
   ```

2. **Write minimal SKILL.md:**
   - Complete frontmatter with clear description (include "Use when..." triggers)
   - Brief overview (1-2 sentences of what and why)
   - Core workflow or pattern (the actual learning captured)
   - One concrete example showing usage
   - **Avoid:** Extensive background, multiple variations, comprehensive edge cases

3. **Example minimal skill structure:**
   ```markdown
   ---
   name: repo-deployment
   description: Deployment workflow for repository-name. Use when deploying changes to staging or production environments.
   ---

   # Deployment Workflow

   ## Overview
   Standard deployment process for this repository.

   ## Workflow
   1. Run tests: `npm test`
   2. Build: `npm run build`
   3. Deploy to staging: `./deploy.sh staging`
   4. Verify on staging URL
   5. Deploy to production: `./deploy.sh production`

   ## Example
   User: "Deploy my changes to production"
   → Follow steps 1-5, confirming at step 4 before step 5
   ```

4. **Clean up template files:**
   - Delete unused scripts/example.py
   - Delete unused references/api_reference.md
   - Delete assets/ directory if not needed

5. **Validate:**

   **Important**: Activate the virtual environment first (required for PyYAML dependency):
   ```bash
   source ~/.claude/skills/skill-creator/.venv/bin/activate
   ~/.claude/skills/skill-creator/scripts/quick_validate.py <path-to-skill>
   ```

   **Note**: Only run `package_skill.py` if the user explicitly requests a .skill file for distribution.

### For Updating Existing Skills

1. **Read the current skill:**
   - Use Read tool to examine current SKILL.md
   - Identify appropriate section to extend
   - Match existing style and structure

2. **Make minimal additions:**
   - Add new information to relevant section
   - Include concrete example if helpful
   - Keep additions concise and focused
   - Don't restructure unless necessary

3. **Validate:**
   - Activate virtual environment: `source ~/.claude/skills/skill-creator/.venv/bin/activate`
   - Run quick_validate.py to ensure still valid
   - Only run package_skill.py if user explicitly requests a .skill file for distribution

### Growth Through Iteration

New skills should start minimal and grow based on real usage:
- v1: Core pattern + one example
- v2: Add variations discovered in actual use
- v3: Add error handling for issues encountered
- v4: Add references/ directory if content grows large

Don't try to anticipate everything upfront - let skills evolve naturally.

## References

- **decision-framework.md** - Detailed flowcharts and decision trees for assessing significance, choosing update vs create, local vs user-level, and timing strategies
- **examples.md** - 15-20 concrete scenarios with "Should Capture" / "Should Not Capture" judgments showing the framework in action
