---
name: skill-authoring
description: Create and maintain Claude Code skills following Anthropic best practices. Use when building new skills, refactoring existing ones, or ensuring skills follow official guidelines for structure, naming, progressive disclosure, and testing.
---

# Skill Authoring

Create effective Claude Code skills that follow Anthropic's official best practices and guidelines.

## When to Use This Skill

Use this skill when:

- Creating new skills from scratch
- Refactoring existing skills for better structure
- Ensuring skills follow Anthropic guidelines
- Troubleshooting skill discovery or performance issues
- Optimizing skills for token efficiency

## Core Principles

### 1. Concise is Key

- Context window is shared - be economical with tokens
- Assume Claude is already smart - don't over-explain basics
- Challenge every piece of information: "Does this justify its token cost?"

### 2. Progressive Disclosure

Skills load in three tiers:

- **Level 1**: Metadata (name/description) - always loaded (~100 tokens/skill)
- **Level 2**: SKILL.md body - loaded when triggered (<500 lines recommended)
- **Level 3**: Reference files/scripts - loaded/executed as needed

### 3. Appropriate Freedom Levels

- **High freedom**: Text instructions for flexible, context-dependent tasks
- **Medium freedom**: Parameterized scripts with some variation
- **Low freedom**: Specific scripts for fragile, error-prone operations

## Skill Structure

### Required Files

Each skill is a directory containing a `SKILL.md` file. Multiple locations
are scanned, in order of preference:

**Project-local** (walked up from cwd to git worktree root):
- `.agents/skills/<name>/SKILL.md` — preferred cross-platform standard
- `.claude/skills/<name>/SKILL.md` — Claude-compatible
- `.opencode/skills/<name>/SKILL.md` — OpenCode-specific

**Global** (user home):
- `~/.agents/skills/<name>/SKILL.md`
- `~/.claude/skills/<name>/SKILL.md`
- `~/.config/opencode/skills/<name>/SKILL.md`

Use `.agents/skills/` for new skills — it is the emerging cross-platform
standard supported by Claude Code, OpenCode, and other agents.

```
.agents/skills/skill-name/
├── SKILL.md (required - instructions + metadata)
└── Optional bundled resources:
    ├── scripts/     - Executable code (Python/Bash/etc.)
    ├── references/  - Documentation loaded as needed
    └── assets/      - Files for output (templates, images)
```

### YAML Frontmatter Requirements

```yaml
---
name: skill-name-here          # lowercase, hyphens, max 64 chars
description: What + When       # max 1024 chars, include trigger contexts
---
```

**Critical**: Description must include both WHAT the skill does AND WHEN to use it. Include:
- Task types (create, analyze, process)
- File types (.pdf, .docx, .json)
- Keywords users might mention
- Specific trigger contexts

### Example `SKILL.md`

N.B. The following example is indented here so that triple backticks can be included within the example, but when creating / editing a `SKILL.md`, most of it should not be indented.

Note also that `SKILL.md` files do not necessarily need to provide and use helper tools; however it's included this example skill for illustrative purposes.

    ---
    name: example-skill
    description: Process example files with specific formatting. Use when users mention examples, processing, or .example files.
    ---

    # Example Skill

    Process example files following consistent patterns.

    ## When to Use This Skill

    - When processing .example files
    - When users ask about example formatting
    - When converting example formats

    ## How It Works

    1. Read the input file using the example-parser tool
    2. Apply formatting rules from references/rules.md
    3. Write output to destination

    ## Usage

    ```bash
    python scripts/process_example.py input.example output.txt
    ```

    ## How to use the example-parser tool

    ```python
    from example_parser import parse

    result = parse("data.example")
    print(result.summary)
    ```

    ## Reference Files

    - [Formatting Rules](references/rules.md)
    - [Parser Documentation](references/parser.md)

## Best Practices

### Naming Conventions

Use gerunds or gerundial nouns:

- **Gerunds** (verb + -ing): `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`
- **Gerundial nouns** (verb-derived nouns): `generation`, `authoring`, `initialization`, `management`

- ✅ `processing-pdfs`, `generating-prps`, `authoring-skills`
- ❌ `pdf-helper`, `data-utils`, `skill-creator`

### Writing Effective Descriptions

- Write in third person (not "I can help" but "Processes files")
- Include specific triggers: "Use when working with PDF files or when users mention PDFs, forms, or document extraction"
- Be specific about capabilities and contexts

### Progressive Disclosure Patterns

#### High-Level Guide with References

```
# PDF Processing

## Quick start

Extract text with pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Common Anti-Patterns to Avoid

### Over-Verbose Instructions

- ❌ Paragraphs explaining basic concepts Claude knows
- ✅ Concise examples that demonstrate patterns

### Deep Reference Nesting

- ❌ SKILL.md → file1.md → file2.md → file3.md
- ✅ SKILL.md → file1.md, file2.md, file3.md (one level deep)

### Time-Sensitive Content

- ❌ "Current best practice as of 2025"
- ✅ "Current best practice (see [UPDATES.md](references/updates.md))"

### Windows Path Usage

- ❌ `scripts\helper.py`
- ✅ `scripts/helper.py`

## Executable Scripts Best Practices

### Solve Problems, Don't Punt

Handle errors explicitly rather than letting Claude figure it out:

```python
# Good: Handle file not found

def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
```

### Provide Utility Scripts

Pre-made scripts offer advantages:

- More reliable than generated code
- Save tokens (no need to load contents)
- Ensure consistency across uses

## References

For complete official guidelines, see:
- [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Progressive Disclosure Architecture](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)
