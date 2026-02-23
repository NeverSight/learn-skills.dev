---
name: fix-reporter
description: Capture solved problems as categorized documentation with YAML frontmatter for fast lookup
allowed-tools: Read Write Bash Grep
preconditions:
  - Problem has been solved (not in-progress)
  - Solution has been verified working
disable-model-invocation: true
---

# fix-reporter Skill

**Purpose:** Document solved problems to build searchable institutional knowledge.

**Organization:** Single-file per problem in `.agents/lessons/[category]/[filename].md` with YAML frontmatter. Files with `workflow_phase` fields are discoverable by lessons-discoverer agent.

## 7-Step Capture Process

### Step 1: Detect Confirmation

**Auto-invoke triggers:**
- "that worked", "it's fixed", "working now", "problem solved", "that did it"

**Manual:** `/report-fix` command

**Document when:**
- Multiple investigation attempts needed
- Tricky debugging that took time
- Non-obvious solution
- Future sessions would benefit

**Skip for:** Simple typos, obvious syntax errors, trivial fixes

### Step 2: Gather Context

Extract from conversation:

| Field | Source |
|-------|--------|
| Module name | Which project module had the problem |
| Symptom | Observable error/behavior (exact messages) |
| Investigation attempts | What didn't work and why |
| Root cause | Technical explanation |
| Solution | Code/config changes that fixed it |
| Prevention | How to avoid in future |

**If critical context missing:** Ask user and WAIT before Step 3.

### Step 3: Check Existing Docs

```bash
# Search for similar issues
grep -r "exact error phrase" .agents/lessons/
ls .agents/lessons/[category]/
```

**If similar found:** Present options:
1. Create new doc with cross-reference (recommended)
2. Update existing doc (only if same root cause)
3. Other

**If not found:** Proceed to Step 4.

### Step 4: Generate Filename

Format: `[sanitized-symptom]-[module]-[YYYYMMDD].md`

**Rules:**
- Lowercase, hyphens for spaces
- Remove special characters
- Truncate < 80 chars

**Examples:**
- `missing-import-auth-module-20251110.md`
- `n-plus-one-user-queries-UserService-20251110.md`

### Step 5: Validate YAML Schema

Validate against `schema.yaml` and `references/yaml-schema.md`.

**Required fields:**
- module, date, problem_type, component
- symptoms (array 1-5), root_cause
- resolution_type, severity

**BLOCK if validation fails** - show errors, request corrections.

### Step 6: Create Documentation

```bash
CATEGORY="[mapped from problem_type]"
mkdir -p .agents/lessons/${CATEGORY}
```

Populate `assets/resolution-template.md` with:
- Context from Step 2
- Validated YAML from Step 5

**Optional discovery fields:** Add `workflow_phase`, `tech_stack`, `lesson_type`, `impact`, `keywords` if lesson should auto-surface.

### Step 7: Cross-Reference

**If similar issues from Step 3:**
- Add "Related Issues" links to both docs

**If 3+ similar issues exist:**
- Consider adding to `.agents/lessons/patterns/common-solutions.md`

**If severity=critical + non-obvious solution:**
- Note in output: "Consider adding to Critical Patterns"

## Output

After capture, invoke `fix-decision-router` skill with:

```yaml
doc_path: .agents/lessons/[category]/[filename].md
category: [problem_type category]
```

## Category Mapping

| problem_type | Directory |
|--------------|-----------|
| build_error | build-errors/ |
| test_failure | test-failures/ |
| runtime_error | runtime-errors/ |
| performance_issue | performance-issues/ |
| database_issue | database-issues/ |
| security_issue | security-issues/ |
| ui_bug | ui-bugs/ |
| integration_issue | integration-issues/ |
| logic_error | logic-errors/ |
| developer_experience | developer-experience/ |
| workflow_issue | workflow-issues/ |
| best_practice | best-practices/ |
| documentation_gap | documentation-gaps/ |

## Success Criteria

- [ ] YAML frontmatter validated
- [ ] File created in `.agents/lessons/[category]/`
- [ ] Enum values match schema exactly
- [ ] Code examples included
- [ ] Cross-references added if related issues found
- [ ] fix-decision-router invoked

## Error Handling

| Error | Action |
|-------|--------|
| Missing context | Ask user, WAIT |
| YAML validation fail | Show errors, BLOCK until valid |
| Similar issue ambiguity | Present options, let user choose |

## Quality Guidelines

**Include:**
- Exact error messages (copy-paste)
- File:line references
- Observable symptoms
- Failed attempts documented
- Technical "why" explanation
- Code examples (before/after)
- Prevention guidance

**Avoid:**
- Vague descriptions
- Missing technical details
- No context (version, file)
- Code dumps without explanation
