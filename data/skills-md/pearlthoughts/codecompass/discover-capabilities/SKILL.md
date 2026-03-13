---
name: "discover-capabilities"
description: "Use this at session start to discover what CodeCompass can do. Read .ai/capabilities.json for module map (5 domains, 21+ modules) instead of manual Grep/Glob. Apply when: (1) planning tasks, (2) user asks 'What can CodeCompass do?', (3) before implementing features"
categories: ["meta", "discovery", "navigation"]
tags: ["capabilities", "modules", "architecture", "discovery"]
version: "1.0.0"
---

# Discover CodeCompass Capabilities

## Purpose

This meta-skill teaches how to efficiently discover what CodeCompass can do without manual exploration or rediscovery.

## When to Use

- ✅ Session start (understand available capabilities)
- ✅ User asks: "What can CodeCompass do?"
- ✅ Before implementing features (check if exists)
- ✅ Exploring unfamiliar parts of codebase
- ✅ Planning complex workflows (know available tools)

## Discovery Layers

### Layer 1: Quick Reference (CLAUDE.md)
**Purpose**: Project overview and entry point
**Location**: `/CLAUDE.md`
**Token cost**: ~2,000 tokens
**Content**: Tech stack, infrastructure, basic commands

**Read for**:
- Project background
- Technology choices
- Infrastructure setup
- Quick commands

### Layer 2: Structured Discovery (capabilities.json) ⭐
**Purpose**: Complete module and capability map
**Location**: `.ai/capabilities.json`
**Token cost**: ~2,500 tokens
**Content**: All domains, modules, relationships, entry points

**Read for**:
- What domains exist
- What modules are available
- What each module can do
- How modules relate to each other
- When to use which module

### Layer 3: Skills Index (this directory)
**Purpose**: How-to workflows and perspectives
**Location**: `.claude/skills/`
**Token cost**: ~700 tokens (metadata scan)
**Content**: Workflows, roles, patterns

**Read for**:
- How to accomplish complex tasks
- What workflows exist
- Which skill to apply

### Layer 4: Semantic Search (Weaviate)
**Purpose**: Implementation-level discovery
**Location**: Weaviate database
**Token cost**: Variable (query results)
**Content**: Actual code, indexed semantically

**Use for**:
- Finding specific implementations
- Similar code patterns
- Deep code understanding

### Layer 5: Source Code
**Purpose**: Implementation details
**Location**: `src/modules/`
**Token cost**: Variable (file reading)

**Read for**:
- Exact implementation
- Edge cases
- Internal logic

## Discovery Workflow

### Quick Discovery (5 seconds)

```bash
# 1. Read capabilities.json structure
cat .ai/capabilities.json | jq '.domains | keys'
# Returns: ["code_analysis", "semantic_search", "requirements_extraction", "vault_integration", "system_operations"]

# 2. Check specific domain
cat .ai/capabilities.json | jq '.domains.code_analysis'
# Returns: modules, capabilities, entry_points, when_to_use
```

### Structured Discovery (Recommended)

**Step 1: Read capabilities.json**
```json
{
  "domains": {
    "code_analysis": {
      "modules": ["ast-analyzer", "yii2-analyzer", ...],
      "capabilities": ["parse_php_ast", "extract_yii2_controllers", ...],
      "entry_points": {...}
    }
  }
}
```

**Step 2: Identify relevant domain**
- User wants: "Analyze Yii2 project" → `code_analysis` domain
- User wants: "Search for payment logic" → `semantic_search` domain
- User wants: "Extract requirements" → `requirements_extraction` domain

**Step 3: Check module capabilities**
```json
{
  "code_analysis": {
    "modules": ["yii2-analyzer"],
    "capabilities": ["extract_yii2_controllers", "extract_yii2_models"],
    "entry_points": {
      "cli": "codecompass analyze:yii2 <path>"
    }
  }
}
```

**Step 4: Load relevant skill**
- For Yii2 analysis → Load `analyze-yii2-project.md` skill
- For requirements → Load `extract-requirements.md` skill

### Semantic Discovery (Deep Dive)

When capabilities.json shows a module exists but you need implementation details:

**Use Weaviate semantic search**:
```bash
pnpm run cli -- search:semantic "how does Yii2 controller extraction work"
```

**Returns**:
- Relevant source files
- Similar code patterns
- Implementation examples

## Example Flows

### Example 1: "Can CodeCompass analyze database schemas?"

**Step 1**: Check capabilities.json
```bash
cat .ai/capabilities.json | jq '.domains.code_analysis.modules[]' | grep database
# Returns: "database-analyzer"
```

✅ **Answer**: Yes, via `database-analyzer` module

**Step 2**: Check entry points
```bash
cat .ai/capabilities.json | jq '.domains.code_analysis.entry_points'
```

**Step 3**: Check if skill exists
```bash
ls .claude/skills/ | grep database
# If exists, load that skill for workflow
# If not, use capabilities.json guidance directly
```

### Example 2: "How do I search code semantically?"

**Step 1**: Check capabilities.json
```bash
cat .ai/capabilities.json | jq '.domains.semantic_search'
```

Returns: modules, capabilities, dependencies

**Step 2**: Load semantic-search skill
```bash
cat .claude/skills/semantic-search.md
```

Follow the workflow in the skill

### Example 3: "What modules handle authentication?"

**Step 1**: Semantic search in Weaviate
```bash
pnpm run cli -- search:semantic "authentication and authorization modules"
```

**Step 2**: Verify in capabilities.json
```bash
cat .ai/capabilities.json | jq '.module_relationships'
```

## Discovery Decision Tree

```
┌─────────────────────────────────────┐
│ USER REQUEST                        │
└─────────────────────────────────────┘
              ↓
        ┌─────────┐
        │ What?   │ "What can CodeCompass do?"
        └─────────┘
              ↓
    Read: .ai/capabilities.json
              ↓
        ┌─────────┐
        │ How?    │ "How do I use X?"
        └─────────┘
              ↓
    Load: .claude/skills/<relevant>.md
              ↓
        ┌─────────┐
        │ Where?  │ "Where is X implemented?"
        └─────────┘
              ↓
    Search: Weaviate semantic search
              ↓
        ┌─────────┐
        │ Details │ "How does X work internally?"
        └─────────┘
              ↓
    Read: src/modules/<module>/<file>
```

## Avoid Rediscovery Pattern

### ❌ Old Pattern (Inefficient)
1. User asks: "Can CodeCompass do X?"
2. Claude explores with Grep: 1,000+ tokens
3. Claude reads multiple files: 5,000+ tokens
4. Claude builds mental model: slow, error-prone
5. **Total**: 6,000+ tokens, slow, may miss things

### ✅ New Pattern (Efficient)
1. User asks: "Can CodeCompass do X?"
2. Claude reads capabilities.json: 2,500 tokens (cached)
3. Claude checks domain → module → capability
4. Claude loads skill if complex workflow needed
5. **Total**: 2,500-4,000 tokens, instant, accurate

## Module Relationship Understanding

capabilities.json includes `module_relationships`:

```json
{
  "indexing": {
    "depends_on": ["vectorizer", "weaviate"],
    "used_by": ["search", "vault"],
    "provides": "embedding_generation_pipeline"
  }
}
```

**Use this to**:
- Understand module dependencies
- Trace data flow
- Plan refactoring
- Debug integration issues

## Common Workflows Reference

capabilities.json includes `common_workflows`:

```json
{
  "analyze_legacy_yii2": [
    "1. Verify infrastructure: codecompass health",
    "2. Analyze project: codecompass analyze:yii2 <path>",
    ...
  ]
}
```

**Use as**:
- Quick reference for common tasks
- Starting point for complex workflows
- Checklist for multi-step processes

## Maintenance Notes

**This skill references**:
- `.ai/capabilities.json` - Keep this file updated when modules change
- `.claude/skills/` - Skills directory for workflows
- `CLAUDE.md` - Project entry point

**Update triggers**:
- New module added → Update capabilities.json
- Module removed → Update capabilities.json
- New workflow discovered → Consider creating new skill

## Related Skills

- `analyze-yii2-project.md` - Framework-specific workflow after discovering Yii2 modules
- `semantic-search.md` - How to search capabilities after discovery
- `extract-requirements.md` - What to do after discovering requirements modules

## Related Modules

From `.ai/capabilities.json`:
- All 5 domains: code_analysis, semantic_search, requirements_extraction, vault_integration, system_operations
- All 21+ modules documented in capabilities.json

---

**Remember**: capabilities.json is the single source of truth for "WHAT exists". Skills teach "HOW to use it".
