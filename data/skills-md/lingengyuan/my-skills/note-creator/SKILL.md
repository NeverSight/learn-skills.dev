---
name: note-creator
description: Orchestrates creation of structured Obsidian notes with markdown, canvas diagrams, and table bases. Use when users ask to create notes, save knowledge, or document concepts in their Obsidian vault. Delegates to specialized format skills.
allowed-tools:
  - Read
  - Write
  - Edit
  - Skill
  - Glob
  - Bash(mkdir:*, echo:*, cat:*)
---

# note-creator (Orchestrator Skill)

## Purpose
Given a short user prompt (and optional raw context), this skill MUST:

1) Classify intent and decide a minimal artifact plan (default: md only)
2) Select a destination folder and stable naming
3) Invoke underlying format skills with runtime context
4) WRITE all generated artifacts to disk following a strict contract

This skill is an ORCHESTRATOR.
Generating content without writing files is considered a FAILURE.

---

## Dependencies
This skill MUST delegate format correctness to:

- obsidian-markdown/SKILL.md
- json-canvas/SKILL.md
- obsidian-bases/SKILL.md

---

## Inputs
- user_prompt: a short sentence or paragraph describing what to record
- optional_context_files (optional): raw markdown or text provided by the user

---

## Output Contract

**CRITICAL: Output paths are relative to CURRENT WORKING DIRECTORY (CWD)**
- The CWD when the skill is invoked is the base (e.g., `F:/Project/Obsidian/`)
- All outputs MUST be written to: `<cwd>/outputs/<folder>/<title>/`
- DO NOT write to the skill's own directory
- When computing paths, always use the current working directory as the base

All outputs MUST be written to:

outputs/<folder>/<title>/
  - note.md (required)
  - diagram.canvas (optional)
  - table.base (optional)
  - meta.json (required)

Rules:
- <folder> MUST come from rules/folders.md
- <title> MUST follow rules/naming.rules.md
- Writing files is mandatory

---

## Algorithm (Strict Execution Checklist)

### 1) Read Inputs
- Read user_prompt
- Read any optional_context_files

### 2) Classify Intent
Produce a STRICT classification JSON according to rules/classify.intent.md.
The JSON MUST include:
- title
- folder
- diagram_type
- artifact_plan (must include "md")
- tags (3–8)
- properties (category, created, modified, source)

If the request is a COMPARISON and "base" is included, the JSON MUST ALSO include:
- base_mode = "comparison"
- comparison_items: an array of items to compare (slug + display_name + optional fields)

### 3) Compute Output Paths
- CRITICAL: Get the current working directory (CWD) first
- CWD is the directory where the user invoked the skill (e.g., `F:/Project/Obsidian/`)
- Compute all paths as relative to CWD:
  - root_dir    = <cwd>/outputs/<folder>/<title>/
  - note_path   = <cwd>/outputs/<folder>/<title>/note.md
  - canvas_path = <cwd>/outputs/<folder>/<title>/diagram.canvas
  - base_path   = <cwd>/outputs/<folder>/<title>/table.base
  - meta_path   = <cwd>/outputs/<folder>/<title>/meta.json
  - compare_dir = <cwd>/outputs/<folder>/<title>/compare/   (comparison only)

- When writing files, use these full paths or ensure you're in the CWD

### 4) Generate and WRITE note.md (MANDATORY)
- Invoke obsidian-markdown skill using templates/note.md.prompt
- The invocation MUST include runtime context:
  - title
  - folder
  - tags
  - properties
  - root_dir (<cwd>/outputs/<folder>/<title>/)

- The generated markdown MUST be written to disk at:
  <cwd>/outputs/<folder>/<title>/note.md

### 5) Generate and WRITE diagram.canvas (CONDITIONAL)

- If "canvas" is present in artifact_plan:

  - Select ONE canvas layout template based on diagram_type
    and content intent:

    - If diagram_type == "sequence":
        - If the note intent is documentation, explanation,
          sharing, usage instructions, or public-facing content:
            -> use templates/canvas.sequence.compact.md
        - Otherwise (internal notes, debugging, design reasoning):
            -> use templates/canvas.sequence.detailed.md

    - If diagram_type == "flowchart":
        -> use templates/canvas.flowchart.md

    - If diagram_type == "artifact":
        -> use templates/canvas.artifact.md

    - If diagram_type == "architecture":
        -> use templates/canvas.architecture.md

    - If diagram_type == "none":
        -> DO NOT generate diagram.canvas
           (remove "canvas" from artifact_plan)

  - Invoke json-canvas skill using templates/canvas.prompt

  - The invocation MUST include runtime context:
    - title
    - folder
    - diagram_type
    - artifact_plan
    - root_dir (<cwd>/outputs/<folder>/<title>/)
    - canvas_template
      (the FULL CONTENT of the selected templates/canvas.*.md)

  - The generated canvas MUST be written to disk at:
    <cwd>/outputs/<folder>/<title>/diagram.canvas


### 6) Generate and WRITE table.base (CONDITIONAL)

- If "base" is present in artifact_plan:

  #### 6.1 Comparison Base Mode (PREFERRED for comparisons)
  - If base_mode == "comparison" AND comparison_items is present and non-empty:
  - IMPORTANT:
  - If base_mode == "comparison" BUT comparison_items is missing or empty,
    this is a classification error.
  - In this case, DO NOT fall back to generic base generation.
  - The execution MUST either:
    - FAIL explicitly; OR
    - Remove "base" from artifact_plan and continue with md-only output.

    1) CREATE compare_dir:
       <cwd>/outputs/<folder>/<title>/compare/

    2) For EACH item in comparison_items:
       - Generate ONE markdown file:
         <cwd>/outputs/<folder>/<title>/compare/<slug>.md

       - Use templates/compare.item.md as a strict template.
       - Fill frontmatter fields so Base can render columns:
         - item_type: "skill"
         - name
         - 输入
         - 输出
         - 定位
         - 产物
         - 边界
         - tags (include "对比")
         - source/created/modified (from properties)

       - IMPORTANT:
         - These compare/*.md files are the "rows" of the Base.
         - Do NOT put compare rows into note.md only; they MUST exist as files.

    3) Invoke obsidian-bases skill using templates/base.comparison.prompt
       The invocation MUST include runtime context:
       - title
       - folder
       - root_dir (<cwd>/outputs/<folder>/<title>/)
       - compare_dir (<cwd>/outputs/<folder>/<title>/compare/)
       - properties (category/created/modified/source)

    4) The generated base MUST be written to disk at:
       <cwd>/outputs/<folder>/<title>/table.base

  #### 6.2 Generic Base Mode (fallback)
  - Else IF base_mode is NOT "comparison":
    - Invoke obsidian-bases skill using templates/base.prompt
    - The invocation MUST include runtime context:
      - title
      - folder
      - artifact_plan
      - root_dir (<cwd>/outputs/<folder>/<title>/)

    - The generated base MUST be written to disk at:
      <cwd>/outputs/<folder>/<title>/table.base


### 7) Generate and WRITE meta.json (MANDATORY)
- Generate meta.json according to rules/output.contract.md
- Include comparison metadata when applicable:
  - base_mode
  - compare_dir
  - comparison_items
- Write meta.json to:
  <cwd>/outputs/<folder>/<title>/meta.json

### 8) Execution Summary
- Output a short summary listing generated files and their final paths

---

## File Writing Rules (CRITICAL)
- Every generated artifact MUST be written to disk.
- Outputting content only in the conversation is NOT allowed.
- Missing file writes invalidate the execution.
- Always write files relative to the current working directory, not the skill directory

---

## Hard Constraints

### General
- artifact_plan MUST include "md"
- folder MUST be from rules/folders.md
- tags count MUST be 3–8 and include at least one domain tag

### note.md
Must include:
- YAML frontmatter (tags, category, created, modified)
- Summary section
- ≥3 structured sections
- Examples (code blocks when applicable)
- ≥5 Caveats / Notes

### diagram.canvas (if generated)
- Text nodes MUST use "type":"text" and the "text" field
- MUST NOT use "label" for text nodes
- ≥6 nodes, ≥5 edges
- Must include: user request, intent classification, and persistence to root_dir

### table.base (if generated)
- For comparison mode:
  - MUST scope sources to compare_dir ONLY
  - MUST include only markdown files
  - MUST prefer frontmatter columns from compare/*.md
- For generic mode:
  - MUST scope sources to root_dir only
  - MUST exclude non-markdown files

---

## Examples
See examples/ directory:
- e2e-docker.md
- e2e-arch.md
- e2e-table.md
