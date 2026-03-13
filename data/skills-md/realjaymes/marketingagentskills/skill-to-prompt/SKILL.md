---
name: skill-to-prompt
description: Converts Claude skills into ChatGPT Project format (prompt instructions + 1 knowledge file as .docx). Use when user mentions "convert to ChatGPT," "ChatGPT project," "export skill," "GPT instructions," "skill to prompt," or "skill to GPT."
version: "1.1.0"
argument-hint: "[skill-name or path]"
---

# Skill to Prompt Converter

Converts a Claude skill (SKILL.md + references/) into ChatGPT Project format: one prompt instruction document (.docx, under 8,000 characters) and one knowledge file document (.docx).

## What This Produces

For each conversion:

1. **Prompt Instructions** (.docx) — The text that gets pasted into ChatGPT's "Instructions" field. Under 8,000 characters. Structured using the 9-component prompt formula.
2. **Knowledge File** (1 .docx file) — Uploaded to the ChatGPT Project as reference material. Contains all detailed workflows, templates, frameworks, examples, and reference content consolidated into a single document.

All .docx files follow standard formatting: Arial font, 10pt normal text, H1=20pt, H2=16pt, H3=14pt, H4=12pt, 1.15 line spacing.

---

## Conversion Workflow

### Step 1: Locate and Read Source Skill

If user provides a skill name (e.g., "copywriting"):
- Look in `~/.claude/skills/[skill-name]/SKILL.md`

If user provides a path, use it directly.

Read everything:
- `SKILL.md` (full content)
- All files in `references/` folder
- Note any `scripts/` or `assets/` folders (these need special handling)

### Step 2: Analyze Skill Complexity

Count total source content to understand how much compression is needed for the single knowledge file:

| Complexity | Criteria | Compression Needed |
|---|---|---|
| Simple | <300 lines in SKILL.md, no reference files | Minimal — content fits easily in one knowledge file |
| Medium | 300-500 lines or 1-2 reference files | Moderate — condense verbose sections, keep all frameworks and examples |
| Complex | 500+ lines or 3+ reference files | Heavy — prioritize frameworks, worked examples, and actionable content. Summarize repetitive sections |

**Regardless of complexity, always produce exactly 1 knowledge file.**

### Step 3: Map Content to the 9-Component Prompt Formula

Read `references/prompt-structure-guide.md` for the full mapping guide.

Extract from the Claude skill and map to ChatGPT instruction components:

| Claude Skill Section | ChatGPT Prompt Component |
|---|---|
| Frontmatter `description` | **Role** + **Task** summary |
| "When to Use" / trigger conditions | **Task** context |
| "Before Starting" / gather context steps | **Inputs/Variables** |
| Core workflow sections (numbered steps) | **Task** (condensed steps) |
| "Output Format" section | **Formatting Instructions** |
| "Examples" section | **Example Output** (1-2 max in instructions) |
| "Constraints" / "Rules" / "Never" statements | **Constraints** |
| Target audience mentions | **Audience** |
| Voice/tone guidance | **Style/Tone** |
| Purpose / outcome descriptions | **Goal** |

### Step 4: Split Content Between Instructions and Knowledge Files

Apply the priority system to stay under 8,000 characters:

**P1 — Always in the prompt instructions:**
- Role statement (who the AI is, what it specializes in)
- Task overview (primary task + condensed workflow steps)
- Goal (desired outcome)
- Critical constraints (never/always rules)
- Knowledge file references (what each file contains, when to consult it)

**P2 — Include in instructions if character budget allows:**
- 1-2 key examples (keep short, move full examples to knowledge files)
- Input variables (what the user must provide before starting)
- Output formatting specs
- Style/tone guidance

**P3 — Always in knowledge files:**
- Full detailed workflow with multi-paragraph explanations
- Complete example library
- Templates and frameworks (from SKILL.md body and references/)
- All reference material (from references/ folder)
- Edge cases and advanced scenarios
- Decision trees and detailed tables
- Script code (from scripts/ folder, documented as reference)

**Character budget:** Target 7,500 characters for the instruction text (500-char safety buffer).

### Step 5: Write Prompt Instructions

Draft the instruction text following this structure:

Every prompt instruction document must include all 9 headings below, in this exact order. No headings may be omitted or renamed.

```
## Role

You are [expertise extracted from skill description and intro].
You specialize in [specific domain/capabilities].

## Task

Your primary task is to [main objective from the skill].

Follow this workflow:
1. [Condensed step from skill workflow]
2. [Condensed step]
3. [Condensed step]
...

## Goal

[Desired outcome extracted from the skill's purpose/output sections]

## Audience

[Target audience. If the skill does not specify an audience, write: "General users seeking [skill domain] assistance. Adjust complexity based on the user's apparent experience level."]

## Style/Tone

[Voice/tone rules extracted from the skill. If the skill does not specify tone, write: "Professional and clear. Match the register of the target audience. Avoid jargon unless the audience expects it."]

Always include these writing rules regardless of skill-specific tone:
- Avoid dashes unless absolutely necessary. Prefer commas, periods, or conjunctions to keep the tone natural.
- Use en dashes (with spaces, e.g. word – word) or em dashes (without spaces, e.g. word—word) only when unavoidable, ideally no more than once per complete piece of output.

## Constraints

- [Never/always rule]
- [Character/word limits]
- [Format restrictions]
- [Quality standards]

## Inputs/Placeholders

Before starting, ask the user for:
1. [Required input from the skill's context-gathering steps]
2. [Required input]

## Example Output

[1-2 short examples showing expected output structure. Keep brief.]

## Formatting Instructions

[Output structure and formatting rules from the skill]
```

After the 9 required sections, always append a Knowledge Files section:

```
## Knowledge Files

This project includes 1 knowledge file. Consult it as needed:

1. **[SkillName]_Reference_Guide.docx** — [What it contains and when to reference it]
```

After drafting, count characters. If over 7,500:
- Cut examples to bare minimum (but keep the Example Output heading with at least a brief example)
- Compress workflow steps further
- Shorten Audience and Style/Tone content (but never remove the headings)

If over 8,000 after compression: shorten section content further, but all 9 headings must remain. Move detailed explanations to the knowledge file and replace with concise summaries under each heading.

### Step 6: Organize Knowledge File Content

Always produce exactly **1 knowledge file** named `[SkillName]_Reference_Guide.docx`.

Consolidate all P3 content into this single document, organized with clear heading hierarchy:

`[SkillName]_Reference_Guide.docx` containing:
- Full detailed workflow with complete explanations
- All examples and worked examples
- Templates and frameworks (from SKILL.md body and references/ folder)
- All reference material (from references/ folder)
- Guidelines, best practices, and edge cases
- Decision trees and detailed tables
- Script documentation (from scripts/ folder, noted as non-executable reference)

**Organization within the single file:**
- Use H1 for major sections (Workflows, Templates, Examples, Reference Material)
- Use H2-H3 for subsections within each major section
- Use page breaks between major sections for readability
- For complex skills with heavy reference content, prioritize frameworks, worked examples, and actionable content over verbose explanations

### Step 7: Generate JSON Data

Structure all content as a JSON object matching the docx-generator input format.

The JSON structure:

```json
{
  "skillName": "Skill Display Name",
  "originalSkillName": "skill-name",
  "version": "1.0.0",
  "outputDir": "~/Downloads/",
  "instructionDoc": {
    "filename": "SkillName_Prompt_Instructions.docx",
    "title": "Skill Name — ChatGPT Project Instructions",
    "characterCount": 7234,
    "sections": [
      { "type": "heading", "level": 1, "text": "Section Title" },
      { "type": "paragraph", "text": "Regular paragraph text." },
      { "type": "bold-paragraph", "label": "Label:", "text": "Text after label" },
      { "type": "bullet", "text": "Bullet point", "level": 0 },
      { "type": "numbered", "text": "Numbered item", "number": 1 },
      { "type": "table", "headers": ["H1","H2"], "rows": [["a","b"]], "columnPcts": [30,70] },
      { "type": "divider" },
      { "type": "spacer", "size": 200 },
      { "type": "meta", "text": "Metadata or footnote text" }
    ]
  },
  "knowledgeFiles": [
    {
      "filename": "SkillName_Reference_Guide.docx",
      "title": "Skill Name Reference Guide",
      "sections": [...]
    }
  ]
}
```

Write this JSON to a temporary file in the current directory: `[skill-name]-conversion.json`

### Step 8: Generate .docx Files

Run the generator:

```bash
NODE_PATH=~/Documents/node_modules node ~/.claude/skills/skill-to-prompt/references/docx-generator.js [skill-name]-conversion.json
```

This produces all .docx files in the `~/Downloads/` folder.

**If the docx package is not available**, install it first:

```bash
cd ~/Documents && npm install docx && cd -
```

**Fallback:** If .docx generation fails entirely, output the content as formatted markdown that the user can paste into Google Docs or Word. Apply the same heading hierarchy and section structure.

### Step 9: Validate and Present Results

Check and report:

- [ ] Instruction character count (must be under 8,000)
- [ ] All .docx files generated successfully
- [ ] Knowledge files contain complete referenced content
- [ ] Cross-references between instructions and knowledge files are clear

Present to the user:

```
Conversion complete: [skill-name] → ChatGPT Project

Output saved to ~/Downloads/

Prompt Instructions:
  [SkillName]_Prompt_Instructions.docx (X,XXX characters)

Knowledge File:
  [SkillName]_Reference_Guide.docx — [brief description]

Setup in ChatGPT:
  1. Create a new Project in ChatGPT
  2. Paste the instruction text from the Instructions .docx into the project's Instructions field
  3. Upload the knowledge file to the project
  4. Test with a sample prompt
```

After presenting, clean up the temporary JSON file:

```bash
rm [skill-name]-conversion.json
```

---

## Conversion Rules

### What Transfers Directly
- Role and purpose definitions
- Workflow steps (condensed)
- Constraints and rules
- Output format specifications
- Examples and templates
- Reference content

### What Requires Rewriting
- **Claude tool references** (Read, Grep, Glob, Bash, Edit, Write) → Rewrite as natural language instructions. Example: "Read the user's file" becomes "Ask the user to paste or upload the content."
- **Dynamic commands** (`!command` syntax) → Not available in ChatGPT. Document as manual steps.
- **File system operations** → Replace with "ask the user to provide" patterns.
- **Progressive disclosure** (loading references on demand) → All content must be in knowledge files upfront.

### What Does Not Transfer
- **Scripts** (scripts/ folder) → Document the script's purpose in the knowledge file. Include the code as reference if useful, but note it cannot execute in ChatGPT.
- **Assets** (assets/ folder) → Note in the output: "These assets must be manually transferred if needed."
- **Cross-skill references** → Flag as dependencies: "This skill references [other-skill]. Consider converting that skill separately."
- **MCP server integrations** → Not available in ChatGPT Projects.
- **Frontmatter fields** (version, argument-hint, context, agent, allowed-tools) → These are Claude-specific metadata. Do not include in ChatGPT instructions.

---

## Output Naming Convention

```
[SkillName]_Prompt_Instructions.docx
[SkillName]_Reference_Guide.docx
```

Where `[SkillName]` is the skill name in Title Case with spaces replaced by underscores.

Examples:
- `copywriting` → `Copywriting_Prompt_Instructions.docx`
- `digital-product-video-ads` → `Digital_Product_Video_Ads_Prompt_Instructions.docx`
- `page-cro` → `Page_CRO_Prompt_Instructions.docx`

---

## Document Formatting Standards

All .docx output follows these standards:

| Element | Setting |
|---------|---------|
| Font | Arial |
| Font color | Black (default) for all text and headings |
| Normal text | 10pt |
| Heading 1 | 20pt |
| Heading 2 | 16pt |
| Heading 3 | 14pt |
| Heading 4 | 12pt |
| Line spacing | 1.15 |

Additional rules:
- Headings are styled by size only. No extra bold on headings.
- All text and headings must be default black. No additional colors on any text or headings.
- Add space after each paragraph.
- Tables use alternating row shading for readability.
- When generating .docx, explicitly set Arial font, heading sizes, black color (no theme colors), and 1.15 line spacing on every element. Never rely on Word default styles.

---

## References

- `references/prompt-structure-guide.md` — 9-component prompt formula, character budget allocation, compression techniques
- `references/docx-generator.js` — Node.js script for generating .docx files from JSON data
- `references/AI Prompting Techniques.pdf` — Source material for the prompt structure framework

## Related Skills

- `agent-skill-builder` — The reverse direction: converts ChatGPT Projects into Claude skills
- `skill-creator` — Guide for creating new Claude skills from scratch
