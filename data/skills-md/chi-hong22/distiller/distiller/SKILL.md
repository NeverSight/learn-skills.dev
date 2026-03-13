---
name: distiller
description: Extract reusable knowledge from AI coding sessions into structured, Obsidian-compatible documents. Use when the user wants to distill experience after completing a project, fixing bugs, refactoring code, or learning new tech. Triggers include "distill", "extract distilled knowledge", "summarize learnings", "retrospective", "what did I learn", or any request to convert session experience into reusable knowledge assets.
---

<!--
Input: AI session content (current chat, today's transcripts, or specific files)
Output: Structured knowledge document (Obsidian-compatible .md) + updated .distiller/ memory
Pos: Experience extraction engine — transforms ephemeral AI sessions into compound knowledge assets (skills/distiller/)
-->

# Distiller

Transform one-off AI coding sessions into structured, reusable knowledge assets. Instead of "use once, forget once", extract underlying logic, reusable patterns, and pitfall guides — building compound interest on development experience.

## Core Principles

1. **Extract, don't interpret** — Faithfully capture what happened. Do not invent rationale or over-generalize beyond what the content supports.
2. **Score by confidence** — Not all extractions are equal. Each extracted point gets a confidence level (high/medium/low) so the user can prioritize review.
3. **Scene-specific depth** — Generic extraction misses nuance. Each scene has tailored extraction dimensions.
4. **User retains control** — AI proposes, user confirms. Every key decision (scene, storage, create/append) requires user approval.
5. **Zero external dependencies** — Pure skill, no CLI tools required.

## Workflow

Follow these 10 steps in order:

### Step 1: Initialize Memory

Scan the project root for `.distiller/` directory. If it does not exist, create it with these files:

```
.distiller/
├── profile.json        → {}
├── history.jsonl       → (empty)
├── search-index.jsonl  → (empty)
└── index.md            → # Distilled Knowledge Index\n\n_No entries yet._
```

### Step 2: Load Preferences

Read `.distiller/profile.json`. Use stored values to pre-fill subsequent choices (preferred storage, frequent tags, etc.). If empty or first run, proceed with defaults.

### Step 2.5: Resolve Interaction Language

Before asking any user-facing question, detect the current user language from the latest user message:

- If the latest message contains Chinese characters, ask questions in Chinese.
- Otherwise, ask questions in English.

All follow-up prompts in Steps 3, 5, 6, and 9 MUST use this interaction language.

### Step 3: Ask Scope

Ask the user which content to distill, using the interaction language from Step 2.5.

Chinese prompt example:

| 选项 | 说明 |
|------|------|
| **当前对话** | 仅分析本次对话 |
| **今天全部对话** | 扫描 `agent-transcripts/` 中今天的 `.jsonl` |
| **指定文件/目录** | 由用户提供文件或目录路径 |

English prompt example:

| Option | Description |
|--------|-------------|
| **Current chat** | Analyze this conversation only |
| **Today's all chats** | Scan `agent-transcripts/` for today's `.jsonl` files |
| **Specific files/dirs** | User provides paths to code files or directories to analyze |

### Step 4: Analyze & Detect Scene

Analyze the scoped content. Auto-detect the most likely scene by scanning for signal patterns. Also detect the source language (en or zh).

**Scene routing logic** — Read the detection signals table from each `references/scene-*.md` file. Match content against signal patterns and score:

| Scene | Reference File | Trigger When |
|-------|---------------|--------------|
| Project Wrap-up | `references/scene-project-wrapup.md` | Architecture decisions, module design, deployment, lessons learned |
| Bug Retrospective | `references/scene-bug-retrospective.md` | Bug fixes, error traces, debugging sessions, root cause analysis |
| Code Refactoring | `references/scene-refactoring.md` | Code restructuring, design patterns applied, performance optimization |
| Tech Learning | `references/scene-tech-learning.md` | New framework/tool exploration, API discovery, concept learning |
| Universal | `references/scene-universal.md` | No scene scores above threshold, or mixed content |

Select the scene with the highest match score. If no scene exceeds the threshold, default to Universal.

### Step 5: Confirm Scene

Present the detected scene and confidence to the user using the interaction language from Step 2.5. Ask them to confirm or override.

### Step 6: Ask Storage Target

Ask the user where to save the output using the interaction language from Step 2.5. Pre-fill with `profile.json` preference if available:

| Option | Path |
|--------|------|
| **Obsidian vault** | User specifies vault path |
| **Project local** | `docs/distiller/` in current project root |
| **Global knowledge base** | `~/.agents/distiller/` |

### Step 7: Search Existing Docs

Run `scripts/search_distiller.py` against the chosen storage directory (or read `search-index.jsonl` directly) to find documents with related topics or tags. Present findings and suggest:

- **Create new** — if no related docs found
- **Append to existing** — if a closely related doc exists (show filename)

User confirms the choice.

### Step 8: Extract

Read the full scene template from the matched `references/scene-*.md`. Follow its extraction dimensions, prompt template, and output structure. Apply confidence scoring to each extraction point:

- **high** — Explicitly stated in source, well-supported, directly actionable
- **medium** — Reasonably inferred from context, may need verification
- **low** — Weak signal, speculative, worth noting but needs validation

Format confidence inline: `**[high]** The race condition occurs because...`

**Language rule**: Frontmatter keys and values are always in English. Document body (section headers + content) follows the detected source language (en or zh).

Use the frontmatter skeleton from `assets/distiller-frontmatter.md`. Populate all fields. For tags, consult `references/tags-taxonomy.md`.

### Step 9: User Review

Present the complete distilled document to the user using the interaction language from Step 2.5. Ask them to confirm, revise, or request re-extraction with different parameters.

### Step 10: Write & Update Memory

1. **Write the document** to the chosen storage path. Filename format: `YYYY-MM-DD-<topic-slug>.md`
2. **Update `.distiller/profile.json`** — Increment scene frequency, update preferred storage, refresh frequent tags
3. **Append to `.distiller/history.jsonl`** — One JSON line: `{"date": "...", "scene": "...", "topic": "...", "tags": [...], "output_path": "...", "scope": "...", "lang": "..."}`
4. **Append to `.distiller/search-index.jsonl`** — One JSON line: `{"file": "...", "title": "...", "keywords": [...], "timestamp": "..."}`
5. **Regenerate `.distiller/index.md`** — Rebuild the full index from `history.jsonl`, grouped by scene then date

## Output Specification

See `assets/distiller-frontmatter.md` for the complete frontmatter skeleton.

Key rules:
- All frontmatter fields and values in English (including `title`, `tags`, `aliases`)
- `tags` use hierarchical `/`-separated format (see `references/tags-taxonomy.md`)
- Base tag `distilled` always present
- Body language follows source (en or zh)
- Use `[[filename]]` wiki-links for cross-references between distilled docs
- Confidence shown inline per extraction point as `**[high]**`, `**[medium]**`, or `**[low]**`

## Resources

- `references/scene-project-wrapup.md` — Project wrap-up extraction template
- `references/scene-bug-retrospective.md` — Bug retrospective extraction template
- `references/scene-refactoring.md` — Code refactoring extraction template
- `references/scene-tech-learning.md` — Tech learning extraction template
- `references/scene-universal.md` — Universal extraction template (fallback)
- `references/tags-taxonomy.md` — Hierarchical tag taxonomy definition
- `assets/distiller-frontmatter.md` — Obsidian-compatible frontmatter skeleton template
- `scripts/search_distiller.py` — Search existing distilled documents by keyword/tag
