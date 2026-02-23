---
name: fix-decision-router
description: Post-documentation decision menu for fix-reporter. Routes to critical patterns, skill updates, cross-references, or discovery enablement.
allowed-tools: Read Write Edit Bash Grep AskUserQuestion
preconditions:
  - fix-reporter has created documentation
  - File path known from fix-reporter output
disable-model-invocation: true
---

# fix-decision-router Skill

**Purpose:** Present post-capture options and execute user's choice after fix-reporter creates documentation.

## Decision Menu

Present after successful documentation:

```
Solution documented

File created:
- .agents/lessons/[category]/[filename].md

What's next?
1. Continue workflow (recommended)
2. Add to Critical Patterns
3. Link related issues
4. Add to existing skill
5. Create new skill
6. View documentation
7. Enable discovery
8. Other
```

## Option Handlers

### Option 1: Continue workflow
- Return to calling skill/workflow
- Documentation complete, no further action

### Option 2: Add to Critical Patterns

**When user selects:** Pattern is non-obvious but must be followed every time.

```
1. Extract pattern from the documentation
2. Format as WRONG vs CORRECT (use template below)
3. Append to .agents/lessons/patterns/critical-patterns.md
4. Add cross-reference back to source doc
5. Confirm: "Added to Critical Patterns"
```

**Template:**
```markdown
## N. [Pattern Name] (Required)

### WRONG ([Will cause X error])
```[language]
[code showing wrong approach]
```

### CORRECT
```[language]
[code showing correct approach]
```

**Why:** [Technical explanation]
**Context:** [When this applies]
**Source:** `.agents/lessons/[category]/[filename].md`
```

### Option 3: Link related issues

```
1. Prompt: "Which doc to link? (filename or describe)"
2. Search .agents/lessons/ for matching doc
3. Add cross-reference to both docs under "## Related Issues"
4. Confirm: "Cross-reference added to both files"
```

### Option 4: Add to existing skill

```
1. Prompt: "Which skill?"
2. Find skill in plugins/*/skills/
3. Determine target: resources.md, patterns.md, or examples.md
4. Add link and brief description
5. Confirm: "Added to [skill-name] in [file]"
```

### Option 5: Create new skill

```
1. Prompt: "Skill name?"
2. Create directory: plugins/majestic-engineer/skills/[name]/
3. Create SKILL.md with basic structure
4. Add solution as first example in references/
5. Confirm: "Created [skill-name] skill"
```

### Option 6: View documentation

```
1. Read and display the created file
2. Present decision menu again
```

### Option 7: Enable discovery

Make lesson discoverable by lessons-discoverer agent:

```
1. Prompt workflow phases: [planning, debugging, review, implementation]
2. Prompt tech stacks: [rails, python, react, node, generic]
3. Prompt lesson type: [antipattern, gotcha, pattern, setup, workflow]
4. Update YAML frontmatter with:
   - workflow_phase: [selected phases]
   - tech_stack: [selected stacks]
   - lesson_type: [selected type]
   - impact: Derive from severity
   - keywords: Extract from tags + symptoms
5. Confirm: "Lesson discoverable during [phases] workflows"
```

**Impact mapping:**
- critical → blocks_work
- high → major_time_sink
- medium/low → minor_inconvenience

### Option 8: Other

Prompt for custom action and execute.

## Integration

**Invoked by:** fix-reporter (after Step 7)
**Invokes:** None (terminal options)

## Input Schema

```yaml
doc_path: string  # Path to created documentation
category: string  # Problem category from fix-reporter
```
