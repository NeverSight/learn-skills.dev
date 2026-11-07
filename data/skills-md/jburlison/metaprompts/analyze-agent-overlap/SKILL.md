---
name: analyze-agent-overlap
description: Analyzes existing agents, skills, prompts, and instructions to identify overlaps, redundancies, and conflicts. Works with GitHub Copilot, Claude Code, Codex, OpenCode, and other providers. Use before creating new customization files to avoid duplication, when consolidating agents, or when troubleshooting conflicting behaviors.
---

# Analyze Agent Overlap

Detects redundancy, overlap, and potential conflicts between AI coding assistant customization files.

## Provider Folder Reference

This skill works across multiple AI coding assistant providers:

| Provider | Base Folder |
|----------|-------------|
| GitHub Copilot | `.github/` |
| Claude Code | `.claude/` |
| Codex | `.codex/` |
| OpenCode | `.config/opencode/` |

**Throughout this document, `<provider>/` represents your chosen provider's base folder.**

## When to Use

- Before creating a new agent, skill, prompt, or instruction
- When you suspect two agents are doing similar things
- To audit and consolidate your customization files
- When agent behaviors seem to conflict

## Analysis Process

### Step 1: Inventory Existing Items

Scan these locations (replace `<provider>/` with actual folder):
- `<provider>/agents/*.md` - All agent definitions (including `.subagent.agent.md`)
- `<provider>/skills/*/SKILL.md` - All skill definitions
- `<provider>/prompts/*.prompt.md` - All prompt templates
- `<provider>/instructions/*.instructions.md` - All instruction files

For each item, extract:
- **Name**: The identifier
- **Purpose**: What problem it solves (from description)
- **Domain**: What areas/topics it covers
- **Triggers**: Keywords or scenarios that activate it
- **User-Invokable**: Whether it's a user-facing agent or sub-agent

### Step 2: Compare Against Proposed Item

When analyzing a proposed new item, compare:

**Direct Overlap Indicators:**
- Same or very similar name
- Same primary purpose statement
- Identical target domain
- Overlapping trigger keywords (>50% match)

**Partial Overlap Indicators:**
- Related but distinct purposes
- Some shared expertise areas
- Similar but different trigger scenarios
- Complementary functionality

**No Overlap Indicators:**
- Different domains entirely
- Non-overlapping use cases
- Distinct trigger keywords

### Step 3: Detect Conflicts

Look for these conflict types:

**Behavioral Conflicts:**
- Two agents giving contradictory guidance for same scenario
- Instructions that override each other for same file patterns
- Skills that produce incompatible outputs

**Scope Conflicts:**
- Multiple agents claiming the same use cases
- Overlapping `applyTo` patterns in instructions
- Ambiguous routing between similar agents

**Naming Conflicts:**
- Names too similar causing confusion
- Same name in different contexts

## Overlap Severity Levels

### 🔴 Critical (Do Not Proceed)
- Exact duplicate of existing item
- Direct contradiction with existing guidance
- Name collision
- >80% purpose overlap

### 🟡 Warning (Needs Discussion)
- Significant overlap (50-80% shared purpose)
- Potential user confusion about which to use
- Overlapping triggers with different behaviors
- Partial scope conflict

### 🟢 Low Risk (Proceed with Awareness)
- Minor overlap (<50% shared concerns)
- Complementary purposes
- Clear differentiation possible
- Different trigger contexts

## Resolution Strategies

When overlap is detected, consider:

### Merge
Combine into single, more comprehensive item.
- Best when: Items serve nearly identical purpose
- Action: Create unified item, deprecate duplicates

### Extend
Add new functionality to existing item.
- Best when: New need is subset of existing item's scope
- Action: Modify existing item, don't create new

### Differentiate
Clarify boundaries between items.
- Best when: Items serve related but distinct needs
- Action: Update descriptions to make distinctions clear

### Reference
Have one item delegate to another.
- Best when: Items have hierarchical relationship
- Action: Add handoff or reference in description

### Supersede
Replace older item with improved version.
- Best when: New item is strictly better
- Action: Create new, mark old as deprecated

## Output Format

```markdown
## Overlap Analysis: [Proposed Item Name]

### Summary
**Proposed Type:** [Agent|Skill|Prompt|Instruction]
**Proposed Purpose:** [Brief description]
**Overlap Level:** None | Low | Medium | High | Critical
**Recommendation:** Proceed | Modify | Merge | Reconsider

### Comparison Matrix

| Existing Item | Type | Overlap | Shared Concerns |
|---------------|------|---------|-----------------|
| [name] | [type] | [level] | [what overlaps] |

### Detailed Findings

#### High/Critical Overlap Items
[For each significant overlap:]

**[Existing Item Name]**
- Type: [type]
- Purpose: [their purpose]
- Overlap Areas: [specific shared concerns]
- Key Distinction: [how proposed differs]
- Resolution: [recommended action]

#### Potential Conflicts
[List any behavioral or scope conflicts]

#### Complementary Items
[Items that could work well alongside proposed]

### Recommendations

1. [Primary recommendation with rationale]
2. [Secondary options if applicable]

### Questions to Resolve
- [Clarifying questions that would help decision]
```

## Example Analysis

**Proposed:** `database-helper` agent for SQL query assistance

**Findings:**
- `dx12-terrain-engine-dev` - No overlap (different domain)
- `agent-builder` - No overlap (different domain)

**Result:** ✅ Proceed - no conflicts detected

---

**Proposed:** `code-reviewer` agent for code review

**Findings:**
- Existing `dx12-terrain-engine-dev` mentions code quality
- Partial overlap in "review code" scenarios

**Result:** ⚠️ Warning - clarify scope boundaries
- Recommendation: `code-reviewer` for general review, `dx12-terrain-engine-dev` for DX12-specific review only
