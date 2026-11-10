---
name: skill-preflight
description: "Deliver a pre-flight duplicate check before creating new skills or agents. Use when the user requests a pre-flight duplicate check before creating new skills or agents."
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Creation Guard: Pre-Flight Duplicate Check

Prevent duplicate functionality by analysing existing skills, agents, and rules before creating new ones. Intercepts creation intent, searches for overlap, and recommends one of 5 actions.

## When to Use

Invoke **before** creating ANY new:
- Skill (`skills/*/SKILL.md`)
- Agent (`.claude/agents/*.md`)
- Rule (`rules/*.md`)

Trigger phrases:
- "Create a skill for..."
- "I want a new skill that..."
- "Let's add an agent for..."
- "We need a rule for..." / "add a rule that..."
- Any intent to create new automation/tooling

**Rules need this most, not least.** A duplicate skill is visible — it shows up
in the catalogue and the slash menu. A duplicate rule is invisible: both copies
load silently as system instructions, and the first sign of trouble is two
subtly different versions of the same policy competing. Rules are also
`break-the-glass` infrastructure, so an unnecessary one is a standing cost on
every session. Check for an existing rule to **amend** before writing a new one
— amendment is the usual correct outcome for rules, where PROCEED is the usual
outcome for skills.

## Process

### Step 1: Identify the Proposal

Extract from the request:
- **Name**: Proposed name (kebab-case)
- **Type**: skill | agent | rule
- **Purpose**: What it does (one sentence)
- **Key Functions**: 3-5 main capabilities
- **Keywords**: Searchable terms related to functionality

### Step 2: Search Existing Artifacts

Run these searches in parallel:

1. **Read [`skills/shared/skill-index.md`](../shared/skill-index.md)** — scan the categorised table for potential duplicates by name and purpose
2. **Keyword search** — grep skills, agents, and rules for each keyword:

```
Grep for each keyword across:
  - skills/*/SKILL.md (frontmatter + body)
  - .claude/agents/*.md (frontmatter + body)
  - rules/*.md (frontmatter + body)
```

3. **Agent scan** — read frontmatter of each agent to check purpose overlap:

```
Glob: .claude/agents/*.md
Read first 20 lines of each match
```

4. **Rule scan** — list every rule and read its Principle:

```
Glob: rules/*.md
Read the frontmatter + "## Principle" section of each candidate
```

A rule's filename often understates its reach: the policy you want may live
inside a broader rule under a different name. Check `docs/components/rules.md`
for the full table, and read the Principle rather than matching on the title —
`bibliography-routing.md` owns paper-lookup routing, which its name does not
advertise. Also check the `paths:` frontmatter: a rule that exists but is
path-scoped away from where you need it is a **scoping** fix, not a new rule.

### Step 3: Analyse Overlap

For each potentially related artifact, assess:

| Criterion | Question |
|-----------|----------|
| Functional overlap | Does it do the same thing? (0-100%) |
| Naming confusion | Could names be confused? |
| Extension potential | Could the proposal extend this instead? |
| Composition | Could existing artifacts compose to achieve this? |

### Step 4: Generate Recommendation

Based on analysis, recommend ONE of:

| Recommendation | Criteria | Action |
|----------------|----------|--------|
| **PROCEED** | <20% overlap, genuinely new capability | Create new artifact |
| **EXTEND** | 50%+ overlap with single existing artifact | Modify existing instead |
| **COMPOSE** | Multiple artifacts cover 80%+ combined | Create thin wrapper or document workflow |
| **ITERATE** | 20-50% overlap, proposal needs refinement | Refine proposal to differentiate |
| **BLOCK** | Would create problematic duplication | Do not create |

### Step 5: Present and Confirm

Display the analysis and wait for explicit user approval before proceeding.

## Output Format

```
════════════════════════════════════════════════════════════════
CREATION GUARD ANALYSIS
════════════════════════════════════════════════════════════════

PROPOSAL:
  Type: [skill|agent]
  Name: [proposed-name]
  Purpose: [one sentence]

EXISTING ARTIFACTS ANALYSED: [count]

RELATED ARTIFACTS FOUND:

1. [artifact-name] ([type])
   Purpose: [what it does]
   Overlap: [X]% - [explanation]

2. [artifact-name] ([type])
   Purpose: [what it does]
   Overlap: [X]% - [explanation]

RECOMMENDATION: [PROCEED|EXTEND|COMPOSE|ITERATE|BLOCK]

RATIONALE:
[2-3 sentences explaining the recommendation]

SUGGESTED ACTION:
[Specific next step based on recommendation]

════════════════════════════════════════════════════════════════
```

## Recommendation Details

### PROCEED
- Artifact is genuinely new
- No significant overlap found
- Clear differentiation from existing tools
- Go ahead and create

### EXTEND
Present extension proposal:
```
Instead of creating [new-name], extend [existing-name]:

Current capabilities:
- [existing feature 1]
- [existing feature 2]

Proposed additions:
- [new feature 1]
- [new feature 2]
```

### COMPOSE
Present composition approach:
```
The proposed functionality can be achieved by combining:

1. [artifact-1] — handles [aspect]
2. [artifact-2] — handles [aspect]

Options:
A) Document this workflow (no new code)
B) Create thin orchestration skill
C) Add to existing skill's integration section
```

### ITERATE
Present refinement questions:
```
Overlap detected with [existing-artifact].

Differentiation needed:
1. [question about scope]
2. [question about use case]
3. [question about implementation]

Please clarify to proceed.
```

### BLOCK
Explain why creation should not proceed:
```
BLOCKED: Would create problematic duplication.

Existing artifact: [name]
- Already does: [capabilities]
- Your request: [same capabilities]

Alternatives:
1. Use existing: /[skill-name]
2. If missing features, extend the existing artifact
3. If different use case, explain how this differs
```

## Post-Match Action Table

When overlap IS found, use this table to decide the specific action:

| Situation | Action |
|-----------|--------|
| Nothing related found | Create new artifact |
| Same trigger + same fix as existing | Update existing (bump version, improve docs) |
| Same trigger, different root cause | Create new + add cross-links in both |
| Partial overlap (same domain, different trigger) | Add variant subsection to existing |
| Same domain, different problem | Create new + add "See also" references |
| Existing is stale or wrong | Mark deprecated + create replacement |

This complements the PROCEED/EXTEND/COMPOSE/ITERATE/BLOCK recommendation above. The recommendation decides *whether* to create; this table decides *how* to handle the relationship with existing artifacts.

## Self-Check Questions

Before creating ANY new artifact, ask:

1. Does something similar already exist?
2. Could this be added to an existing artifact?
3. Would a user know to look for this vs the existing one?
4. Am I creating this because it's needed or because it's easier than finding what exists?

## Naming Convention Enforcement

When creating a new skill, **always** name the definition file `SKILL.md` (uppercase). Never `skill.md`, `Skill.md`, or any other casing.

- The MCP server's skill discovery scans for `SKILL.md` explicitly
- Documentation generators and `system-audit` use `find -name 'SKILL.md'`
- On case-insensitive filesystems (macOS APFS), lowercase files appear to work locally but fail in case-sensitive contexts (Linux CI, Docker, MCP server pattern matching)

**Check before writing:** If the target directory already contains a `skill.md` (lowercase), rename it to `SKILL.md` first.

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Skip the check | "It's obviously new" — famous last words | Always run the analysis |
| Name-only matching | Names differ but functions overlap | Search by purpose and keywords |
| Create then merge | Merge debt accumulates fast | Check first, create once |
| Over-splitting | Two skills that always run together | Consider a single skill with phases |
| Lowercase `skill.md` | Invisible to MCP server, audit tools, and case-sensitive systems | Always use `SKILL.md` (uppercase) |

## Integration

This skill is invoked by `skill-extract` in Phase 2 to replace the old subset/partial/no-overlap check. When called from `skill-extract`, return the recommendation label (PROCEED/EXTEND/COMPOSE/ITERATE/BLOCK) so `skill-extract` can branch accordingly.
