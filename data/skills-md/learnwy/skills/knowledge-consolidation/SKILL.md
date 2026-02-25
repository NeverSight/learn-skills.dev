---
name: knowledge-consolidation
description: "Consolidate and persist knowledge from AI conversations into structured documents. Use when user asks to summarize, consolidate, save knowledge, document insights, or preserve learnings. Triggers on: '总结一下', '记录下来', 'save this knowledge', 'document this', 'we figured it out', 'that was hard to solve'. Saves to .trae/knowledges/, .claude/knowledges/, or .cursor/knowledges/ based on AI IDE."
---

# Knowledge Consolidation

Persist valuable knowledge from AI conversations into structured documents.

## Workflow

```
1. DETECT AI IDE → Check for .trae/, .claude/, .cursor/
2. IDENTIFY CANDIDATES → Scan for knowledge worth preserving
3. CLASSIFY TYPE → Select appropriate knowledge type
4. GENERATE PATH → Run get-knowledge-path.sh
5. WRITE DOCUMENT → Use template format
```

## Step 1: Detect AI IDE

| Indicator            | AI Type       | Storage Path            |
| -------------------- | ------------- | ----------------------- |
| `.trae/` dir         | trae          | `.trae/knowledges/`     |
| `.claude/` dir       | claude-code   | `.claude/knowledges/`   |
| `.cursor/` dir       | cursor        | `.cursor/knowledges/`   |

## Step 2: Knowledge Types

| Type           | When to Use                              |
| -------------- | ---------------------------------------- |
| `debug`        | Bug fixes, crash analysis, error resolution |
| `architecture` | System design, module structure          |
| `pattern`      | Reusable code patterns, best practices   |
| `config`       | Build settings, environment setup        |
| `api`          | API design, integration details          |
| `workflow`     | Development processes                    |
| `lesson`       | Post-mortems, retrospectives             |

## Step 3: Generate Path

```bash
{skill_root}/scripts/get-knowledge-path.sh -r <project_root> -a <ai_type> -t <type> -n <filename>
```

Output: `{project_root}/{ai_path}/knowledges/{YYYYMMDD}_{seq}_{type}_{filename}.md`

## Step 4: Write Document

Use [template](assets/knowledge.md.template):

```markdown
# {Title}

> **Type:** {type}
> **Date:** {YYYY-MM-DD}
> **Context:** {Brief context}

## Summary

{2-3 sentence summary}

## Background

{Situation/problem/context}

## Details

{Technical content, code snippets, analysis}

## Key Takeaways

{Bullet points of actionable insights}
```

## Resources

| Resource                        | Purpose                |
| ------------------------------- | ---------------------- |
| `scripts/get-knowledge-path.sh` | Generate file path     |
| `references/knowledge-types.md` | Type selection guide   |
| `assets/knowledge.md.template`  | Document template      |
