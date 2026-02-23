---
name: mem-skill
description: "Self-evolving memory and knowledge accumulation system for AI agents. Acts as a persistent 'second brain' that automatically retrieves past experiences, captures best practices, and proactively records successful solutions to a private knowledge base. Use this skill whenever starting any task, opening a new conversation, or triggering any other skill. Supports memory engines (default: built-in JSON/Markdown index; optional: QMD semantic search). Initialize with: /mem-skill init [--mem-engine=qmd]."
---

# Mem-Skill: Self-Evolving Knowledge System

## Initialization

When the user runs `/mem-skill init`, execute the following setup:

1. Determine the current workspace root directory.
2. Create the directory structure:
   ```
   <workspace>/
   ├── knowledge-base/
   │   └── _index.json
   └── experience/
       └── _index.json
   ```
3. Populate `knowledge-base/_index.json` with the starter template (see "Knowledge Base Index Format" below).
4. Populate `experience/_index.json` with the starter template (see "Experience Index Format" below).
5. Confirm to the user: "mem-skill initialized. Knowledge base and experience directories created."

### Engine Selection

When the user runs `/mem-skill init --mem-engine=qmd`, optionally with extra `--qmd-*` flags:

**Supported flags (all optional):**
| Flag | Values | Default |
|------|--------|---------|
| `--qmd-scope=<scope>` | `project`, `global` | _(ask user)_ |
| `--qmd-knowledge=<name>` | any string | _(ask user)_ |
| `--qmd-experience=<name>` | any string | _(ask user)_ |
| `--qmd-mask=<pattern>` | glob pattern | `**/*.md` |

**Examples:**
```
/mem-skill init --mem-engine=qmd
/mem-skill init --mem-engine=qmd --qmd-scope=project
/mem-skill init --mem-engine=qmd --qmd-scope=global --qmd-knowledge=my-kb --qmd-experience=my-exp
/mem-skill init --mem-engine=qmd --qmd-mask="**/*.md,**/*.txt"
```

**Init procedure:**

1. Perform all standard init steps above.
2. Check if QMD is installed: run `which qmd` or `npx @tobilu/qmd status`.
3. If QMD is **not** installed, prompt:
   > "QMD is not installed. Install it now with `npm install -g @tobilu/qmd`? (QMD requires Node.js >= 22)"
4. **Determine collection scope:**
   - If `--qmd-scope` was provided, use that value.
   - **Otherwise, you MUST ask the user** (do NOT guess or auto-choose):
     > "Where should QMD collections be stored?
     > 1. **Project** — scoped to this workspace (recommended for multi-project setups)
     > 2. **Global** — shared across all workspaces"
   - If **project**: default collection name prefix is the sanitized workspace folder name (e.g., folder `my-app` → prefix `my-app`).
   - If **global**: default collection name prefix is `mem`.
5. **Determine collection names:**
   - If `--qmd-knowledge` was provided, use that value.
   - If `--qmd-experience` was provided, use that value.
   - **For any name NOT provided via flags, you MUST ask the user** (do NOT auto-generate):
     > "What name for the knowledge collection? (default: `<prefix>-knowledge`)"
     > "What name for the experience collection? (default: `<prefix>-experience`)"
   - Accept user input or use the defaults if the user confirms.
6. **Determine file mask:**
   - If `--qmd-mask` was provided, use that value.
   - Otherwise use `**/*.md`.
7. After all values are confirmed, create the QMD collections:
   ```bash
   qmd collection add <workspace>/knowledge-base --name <knowledge-name> --mask "<mask>"
   qmd collection add <workspace>/experience --name <experience-name> --mask "<mask>"
   qmd context add qmd://<knowledge-name> "General knowledge base: reusable workflows, preferences, best practices"
   qmd context add qmd://<experience-name> "Skill-specific experience: pitfalls, parameters, solutions"
   qmd embed
   ```
8. Create a `.mem-skill.config.json` at the workspace root:
   ```json
   {
     "engine": "qmd",
     "version": "1.0.0",
     "scope": "<project|global>",
     "mask": "<mask>",
     "collections": {
       "knowledge": "<knowledge-name>",
       "experience": "<experience-name>"
     }
   }
   ```
9. Confirm: "mem-skill initialized with QMD memory engine. Collections created and embeddings generated."

**IMPORTANT:** Never silently create QMD collections without confirming scope and names with the user. If no `--qmd-*` flags were provided, every question above MUST be asked interactively.

For the **default engine** (no `--mem-engine` flag), create `.mem-skill.config.json` with:
```json
{
  "engine": "default",
  "version": "1.0.0"
}
```

For detailed engine-specific behavior, see [references/qmd-engine.md](references/qmd-engine.md) and [references/engines.md](references/engines.md).

## Manual Recording Command

When the user runs `/mem-skill recordnow`, immediately trigger the recording flow for the **current conversation** — even if Step 5 was not triggered automatically.

This is useful when:
- Multiple tasks were completed in one session and the agent forgot to ask.
- The user wants to record something that didn't trigger the satisfaction keywords.
- The user remembers later that a solution was worth saving.

**Procedure:**
1. Review the full conversation history for completed tasks.
2. For **each completed task**, summarize it into a one-line essence.
3. Evaluate: "Will this save time next time?"
4. Present all recordable items to the user as a numbered list:
   > "I found these completed tasks worth recording:
   > 1. [summary of task 1] → knowledge-base
   > 2. [summary of task 2] → knowledge-base
   > 3. [summary of skill usage] → experience
   >
   > Which ones should I record? (all / 1,2 / none)"
5. On approval, write each selected item following the same write procedure as Step 5 (including QMD post-write sync if applicable).
6. If no recordable tasks are found, respond: "I reviewed the conversation but didn't find any completed tasks worth recording. Is there something specific you'd like me to save?"

## Core Loop (Mandatory Every Turn)

Execute these steps on every conversation turn. Do not display internal cache state to the user.

### Step 0: In-Conversation Cache (Internal)

Maintain these variables silently within the conversation:
- `last_keywords` — keywords from the previous turn
- `last_topic_fingerprint` — top 3 keywords as a fingerprint
- `last_index_lastUpdated` — timestamp of last index read
- `last_matched_categories` — categories matched on last read
- `last_used_skills` — non-mem-skill skills used this turn
- `missing_experience_skills` — skills with no experience entry
- `loaded_experience_skills` — skills whose experience has been loaded this session

### Step 1: Extract Keywords (No File I/O)

- Extract 3–8 core nouns/phrases from the user's current message.
- Deduplicate and normalize casing.
- Generate `topic_fingerprint` from the top 3 keywords.

### Step 2: Detect Topic Switch (No File I/O)

A topic switch occurs when any of these conditions are met:
- Explicit transition words: "also", "switch to", "by the way", "next", "instead"
- Current keywords differ from `last_keywords` by >= 40%
- User explicitly requests a new category or topic

### Step 3: Cross-Skill Experience Read (Forced — Ignores Topic Switch)

Whenever a non-mem-skill skill is used this turn:
- If the `skill-id` is already in `loaded_experience_skills`, skip (do not re-read or re-announce).
- Otherwise:
  1. Read `experience/_index.json`.
  2. If a matching `skill-id` entry exists, load `experience/skill-<skill-id>.md`.
  3. Add the `skill-id` to `loaded_experience_skills`.
  4. Include in response: `"Loaded experience: skill-<skill-id>.md"`
  5. If no entry exists, add to `missing_experience_skills`.

**Engine-specific retrieval:**
- **Default engine**: Read `experience/_index.json` and match by `skillId`.
- **QMD engine**: Read collection names from `.mem-skill.config.json`, then run `qmd search "<skill-id>" -c <experience-collection> --json -n 5` for keyword match, or `qmd query "<skill-id> <context>" -c <experience-collection> --json -n 5` for deeper retrieval.

### Step 4: Knowledge Base Read (Only on Topic Switch)

Execute only on the first turn of the conversation or when a topic switch is detected:

**Default engine:**
1. Read `knowledge-base/_index.json`.
2. Match current keywords against all category `keywords` arrays.
3. Load every matched category file (no priority ranking — load all matches).
4. If no category matches, follow the "Dynamic Category" flow (see below).
5. If any files were loaded, include in response: `"Loaded knowledge: <file1>.md, <file2>.md"`

If no topic switch occurred, reuse `last_matched_categories` without re-reading.

**QMD engine:**
1. Read collection names from `.mem-skill.config.json`.
2. Run `qmd query "<keywords joined by space>" -c <knowledge-collection> --json -n 10 --min-score 0.3`.
3. Load top results as context.
4. Include in response: `"Retrieved knowledge via QMD: <titles>"`

### Step 5: Proactive Recording (Most Important)

**Trigger conditions:**
- The current task is clearly completed at high quality.
- The user expresses satisfaction ("great", "perfect", "that works", etc.).

**Recording procedure:**
1. **Summarize**: Distill the solution into a one-line essence.
2. **Evaluate value**: "Will this save time next time?"
3. **Ask permission**: Always say something like:
   > "We solved [problem description]. I'd like to record this experience so I can reference it next time. Is that okay?"
4. **Write on approval**:
   - **Skill experience** (if a non-mem-skill skill was used and the skill has no entry or has new techniques): Write to `experience/skill-<skill-id>.md` and update `experience/_index.json`.
   - **General knowledge** (if it's a reusable workflow, preference, or solution): Write to `knowledge-base/<category>.md` and update `knowledge-base/_index.json`.

**QMD engine post-write:**
After writing any `.md` file, run:
```bash
qmd update
qmd embed
```

**Forced rule — always ask when experience is missing:**
If a non-mem-skill skill was used this turn and that skill has no entry in `experience/_index.json`, you **must** ask at task completion:
> "We used <skill-name> this time, but there's no experience record yet. Can I record this session's approach for future reference?"

**If Step 5 was not triggered** (e.g., multi-task sessions where satisfaction signals were missed), the user can run `/mem-skill recordnow` at any time to manually trigger recording. See "Manual Recording Command" above.

## Index Formats

### Knowledge Base Index Format

`knowledge-base/_index.json`:
```json
{
  "lastUpdated": "YYYY-MM-DD",
  "version": "1.0.0",
  "totalEntries": 0,
  "categories": [
    {
      "id": "category-id",
      "name": "Category Name",
      "keywords": ["keyword1", "keyword2"],
      "file": "category-id.md",
      "count": 0
    }
  ]
}
```

### Experience Index Format

`experience/_index.json`:
```json
{
  "lastUpdated": "YYYY-MM-DD",
  "version": "1.0.0",
  "skills": [
    {
      "skillId": "skill-id",
      "file": "skill-<skill-id>.md",
      "keywords": ["keyword1", "keyword2"],
      "count": 0
    }
  ]
}
```

## Entry Formats

### Knowledge Base Entry

```markdown
## [Short Title]
**Date:** YYYY-MM-DD
**Context:** One-line description of the use case
**Best Practice:**
- Key point 1
- Key point 2 — parameter notes and tuning guidance
**Keywords:** keyword1, keyword2, keyword3
```

### Experience Entry

```markdown
## [Problem/Technique Title]
**Date:** YYYY-MM-DD
**Skill:** <skill-id>
**Context:** One-line description of the issue
**Solution:**
- Concrete step 1
- Concrete step 2
**Key Files/Paths:**
- /path/to/relevant/file
**Keywords:** keyword1, keyword2, keyword3
```

## Dynamic Category (Knowledge Base Only)

When user keywords do not match any existing category:
1. Suggest creating a new category.
2. Ask the user for a category name and keywords.
3. Create a new `<category-id>.md` file and update `knowledge-base/_index.json`.

## Recording Criteria

**Core question: Will this save the user time next time?**

### Knowledge Base — Should Record:
- Reusable workflows and decision steps (cross-domain procedures)
- High-cost mistakes and their correction paths
- Critical parameters, settings, or prerequisites
- User preferences and style rules (tone, format, design)
- Multi-attempt solutions (include failure reasons and success conditions)
- Reusable templates, checklists, and output formats
- External dependencies or resource locations

### Knowledge Base — Should NOT Record:
- Single Q&A with no reusable process
- Pure conceptual explanations without concrete steps
- Context-free, non-reusable conclusions

### Experience — Should Record:
- Pitfalls and their fixes when using a specific skill (include error messages)
- Critical parameters or configurations that affect outcomes
- Reusable templates, prompts, or workflows for that skill
- Dependency or asset paths (fonts, images, project entry points)
- Steps requiring a specific order or technique to succeed

### Experience — Should NOT Record:
- Pure theory or conceptual explanations (those belong in knowledge-base)
- Conclusions without reproducible steps
- One-off, non-reusable operations

## Storage Paths

- Knowledge index: `knowledge-base/_index.json`
- Knowledge content: `knowledge-base/<category-id>.md`
- Experience index: `experience/_index.json`
- Experience content: `experience/skill-<skill-id>.md`
- Config: `.mem-skill.config.json`

## QMD Upgrade Suggestion

When the knowledge base exceeds 50 entries, proactively suggest upgrading to QMD:
> "Your knowledge base has grown to [N] entries. For faster semantic search, consider upgrading to QMD: run `/mem-skill init --mem-engine=qmd`."

For full QMD engine details, see [references/qmd-engine.md](references/qmd-engine.md).
For the engine abstraction and adding new engines, see [references/engines.md](references/engines.md).
