---
name: skills-best-practices
description: Opinionated best practices for building Agent Skills - SKILL.md structure, frontmatter, description writing, progressive disclosure, testing, distribution. Use when creating or reviewing a skill, or debugging why one will not trigger.
metadata:
  version: "0.9.1"
  categories: "agents, knowledge"
  topics: "agent-skills, skill-authoring, prompt-design, spec, best-practices"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/skills-best-practices
    emoji: "📐"
---

# Skills Best Practices

Opinionated guide to building Agent Skills for any agent - distilled from the [Agent Skills open standard](https://agentskills.io), Anthropic's official guidance, and production experience, with deviations from the official line marked where they occur. Skills are folders (often just a single file) containing instructions, scripts, and resources that teach an agent how to handle specific tasks.

## Quick Start

A minimal skill is a directory with a `SKILL.md` file:

```
my-skill/
├── SKILL.md          # Required - instructions with YAML frontmatter
├── references/       # Optional - detailed docs loaded on demand
├── scripts/          # Optional - executable code
└── assets/           # Optional - templates, fonts, icons
```

Minimal `SKILL.md`:

```yaml
---
name: my-skill-name
description: What it does. Use when [specific triggers].
---

# My Skill Name

[Instructions here]
```

Only `name` and `description` are required in frontmatter.

## Core Design Principles

### Single File vs. references/ (Most Important)

**Default to a single SKILL.md.** One file can be pasted to a person, gisted, embedded in a CLI binary, and printed by a `<tool> skill` subcommand - a directory cannot. Split into `references/` only when **both** hold:

1. **Conditional loading**: a meaningful chunk of content is needed by only a subset of invocations (e.g. a tracked-changes doc most DOCX tasks never touch). If every invocation reads everything anyway, splitting adds Read round-trips and costs shareability while saving nothing.
2. **Size pressure**: the body exceeds the recommended budget below.

**Distribution is a veto.** If the skill must travel as one file - shipped inside a CLI, printed by a command, shared by paste - stay single-file regardless of size and condense instead. Condensing means cutting redundancy, filler, and over-explanation while preserving every load-bearing instruction; losing substance to hit a line count is the failure mode, not the fix. See the single-file CLI-embedded pattern under [Patterns](#patterns).

**Size guidance** (opinionated thresholds drawn from experience, not enforced spec limits) - measure with `wc -c SKILL.md`. Chars track token cost closely (~4 chars per token); line counts are not a metric - identical content varies 2x in lines by formatting style:

| Tier | Chars | Beyond it |
|------|-------|-----------|
| Recommended | 25k | Condense carefully; split only if the conditional-loading test passes |
| Hard ceiling | 50k | Must condense or split |

> Official Anthropic guidance says to split at 500 lines. That advice assumes registry-installed skills with rarely-needed subtopics, and measures size in a unit that formatting distorts - this skill deliberately deviates on both.

When a skill does split, information loads in three levels:

| Level | When Loaded | Token Cost | Content |
|-------|------------|------------|---------|
| **1: Metadata** | Always (startup) | ~`chars / 4 + 25` - see [Length](#length) | `name` + `description` from frontmatter |
| **2: Instructions** | When skill triggers | <5k tokens (recommended) | SKILL.md body |
| **3: Resources** | As needed | Effectively unlimited | Bundled files, scripts |

Reference detail files from SKILL.md so they load only when the task requires them:

```markdown
## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md)
- **API reference**: See [reference.md](reference.md)
```

### Composability

Skills work alongside other skills. Don't assume yours is the only one loaded.

### Portability

Skills work across Claude.ai, Claude Code, API, and Agent SDK without modification (if dependencies are available).

## Writing the Description (Critical)

The description is the **single most important field** - it determines when your skill activates. Claude uses it to decide relevance from potentially 100+ available skills.

### Rules

- Write in **third person** ("Processes files..." - first or second person breaks discovery)
- Include **WHAT** it does + **WHEN** to use it
- No XML angle brackets; see [Length](#length) for the size target
- Be slightly "pushy" - Claude tends to **undertrigger** rather than overtrigger
- Include specific trigger phrases users would naturally say, plus file types where relevant
- Write natural prose, not keyword dumps - matching is semantic, so a long "Triggers on X, Y, Z..." list adds little over a clear sentence
- If the skill depends on an MCP server, name it ("...via MCP. Requires Linear MCP server connected.")

### Length

**Target 250 characters. The spec's 1024 is a ceiling, not a budget.** The description is the
only part of a skill that costs tokens on every turn of every session, whether or not the skill
ever fires. Past ~250 chars you are diluting the trigger, not sharpening it: descriptions are
dispatch signals, not summaries.

Compressing an over-long description, in the order that usually pays:

- **Cut stack enumerations restated in prose.** Listing the stack once is enough; restating it as
  "covers the frontend ... and the backend ..." is pure padding
- **Cut selling points.** "Includes exhaustive API tables" describes the body, not when to fire
- **Collapse trigger lists.** One clear clause beats three quoted phrases plus four "when" clauses -
  matching is semantic, so near-duplicate triggers add nothing
- **Keep exclusions and disambiguations.** "Not for session state", "not the LanceDB product" run
  30-40 chars and are the only thing preventing wrong-skill dispatch

### Good vs Bad

```yaml
# GOOD - specific, actionable, includes triggers
description: Extract text and tables from PDF files, fill forms, merge
  documents. Use when working with PDF files or when the user mentions
  PDFs, forms, or document extraction.

# BAD - too vague
description: Helps with documents.

# BAD - missing triggers
description: Creates sophisticated multi-page documentation systems.
```

### Negative Triggers

When a skill overtriggers, add boundaries directly in the description:

```yaml
description: Advanced data analysis for CSV files. Use for statistical
  modeling, regression, clustering. Do NOT use for simple data
  exploration (use data-viz skill instead).
```

### Manually-Invoked Skills

`disable-model-invocation: true` stops a skill from auto-triggering - its description shows only in the `/` menu, so trigger phrases do nothing for it, and it is skipped for subagent preload and scheduled tasks too.

**Don't reach for it by default.** Users ask for a workflow in prose ("polish this before committing") far more often than they type `/name`, and the flag turns those requests into a hand-rolled, degraded version of the skill. Reserve it for genuinely destructive one-shots. When it is set, write a plain one-line summary and skip the trigger-tuning.

## Frontmatter Reference

### Required Fields

| Field | Rules |
|-------|-------|
| `name` | Kebab-case, max 64 chars, lowercase + numbers + hyphens only. No "claude" or "anthropic" |
| `description` | Non-empty, max 1024 chars, no XML tags. WHAT + WHEN |

The agentskills.io standard and the Claude API require both fields. Claude Code is more lenient: `name` falls back to the directory name, and `description` falls back to the first markdown paragraph. Write both anyway for portability.

The spec also defines optional `license`, `compatibility`, and `metadata` fields. `compatibility` is capped at 500 characters and states environment requirements (intended product, system packages, network access).

### Optional Fields (Claude Code)

| Field | Purpose |
|-------|---------|
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` |
| `when_to_use` | Extra trigger context, appended to `description` in the skill listing |
| `arguments` | Named positional arguments for `$name` substitution (space-separated string or list) |
| `disable-model-invocation` | `true` = only user can invoke; also blocks subagent preload and scheduled tasks. Rarely worth it - see [Manually-Invoked Skills](#manually-invoked-skills) |
| `user-invocable` | `false` = hidden from `/` menu (background knowledge) |
| `allowed-tools` | Pre-approves tools (no permission prompt) for the current turn; space-separated, e.g. `Read Grep Glob`. In the spec allowlist but tagged **(Experimental)** |
| `disallowed-tools` | Removes tools from Claude's pool while the skill is active; clears on your next message |
| `model` | Override model for this skill; accepts `inherit`. Lasts the current turn only |
| `effort` | Override effort level: `low`, `medium`, `high`, `xhigh`, `max` |
| `context` | `fork` = run in isolated subagent |
| `agent` | Subagent type when `context: fork` (e.g. `Explore`, `Plan`) |
| `background` | `false` opts a forked skill out of background execution (v2.1.218+) |
| `shell` | `bash` (default) or `powershell` |
| `hooks` | Hooks scoped to this skill's lifecycle |
| `paths` | Glob patterns limiting when skill activates |

> **Publishing caveat:** every field above except `allowed-tools` is Claude Code-specific. They work in Claude Code at runtime, but the **official `agentskills validate` spec validator rejects them** - it allows only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`, with no relax flag. If your repo or CI runs that validator (most ClawHub-publishing repos do), a skill using these fields fails validation unless you strip them from the copy you validate/publish. The ClawHub registry itself tends to tolerate extra top-level fields on publish, but the reference validator in your pipeline will not. See [Validate Against the Spec](#validate-against-the-spec).

### Naming Conventions

The `name` (and its folder) must: be 1-64 chars; use only lowercase letters, numbers, and hyphens; not start or end with a hyphen; not contain consecutive hyphens (`--`); and match the parent directory name. Anthropic surfaces also reject the reserved words `claude` and `anthropic`.

Prefer **gerund form** for clarity:

- `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`
- Also acceptable: `pdf-processing`, `process-pdfs`
- Avoid: `helper`, `utils`, `tools`, `documents`

## Claude Code Specifics

Official docs cover most Claude Code skill behavior: the [skills docs](https://code.claude.com/docs/en/skills) (invocation control, argument substitution, discovery and priority, tool permissions, `skillOverrides`, context budget), the [commands reference](https://code.claude.com/docs/en/commands#all-commands) for the current bundled-skills roster (it churns every few releases - never hardcode it), and the [settings reference](https://code.claude.com/docs/en/settings#available-settings). Below is only what those docs miss or what bites in practice.

### Dynamic-Injection Footgun

Claude Code preprocesses SKILL.md at load: an exclamation mark immediately touching a backticked command executes that command before Claude sees the content ([dynamic context injection](https://code.claude.com/docs/en/skills#inject-dynamic-context)). The preprocessor is **not markdown-aware**:

- A literal example executes at load even inside a code fence or inline code span, and a failing placeholder command errors the whole skill at load
- The inline form fires only at line start or after whitespace; a prefix defuses it (`KEY=` before the `!` leaves it literal)
- A fence opened with `!` right after the backticks is the multi-line form and is equally live
- `references/` files are read with the Read tool and never preprocessed - the only safe home for live examples. In a SKILL.md, break the `!`-to-backtick adjacency instead (wrap the `!` in its own code span, as this section does)
- `"disableSkillShellExecution": true` in settings disables execution for user/project/plugin skills
- **In a skill you publish, prefer prose over an `!` block.** Dynamic injection is host-specific: on
  other surfaces the block arrives as literal text, and it drags `allowed-tools` along purely to
  suppress its own permission prompts. Instructing the agent to run the command costs one tool call
  and works everywhere

### Undocumented Behavior

- `display-name`, `default-enabled`, and `fallback` frontmatter keys exist but are absent from the official frontmatter table
- Frontmatter keys parse case-insensitively - kebab-case, snake_case, and camelCase resolve to the same field; boolean fields also accept `yes`/`no`/`on`/`off`/`1`/`0` (v2.1.218+)

### Behavior That Bites

- `context: fork` skills run **in the background by default** since v2.1.218 (`background: false` opts out); backgrounded forks get a narrower tool set and their edits bypass checkpoints, so `/rewind` cannot undo them. `Explore`/`Plan` forks skip CLAUDE.md and git status; since v2.1.198 `Explore` inherits the session model
- Skills stack: `/skill-a /skill-b args` in one message loads up to six skills (v2.1.199+)
- `permissions.additionalDirectories` does **not** load skills from those directories - only the `--add-dir` flag and `/add-dir` command do
- The `allowed-tools` grant lasts the current turn - it clears when the user sends their next message, not when the skill "finishes"
- The `/command` name comes from the skill's **directory**; frontmatter `name` is only a display label (plugin skills excepted). Nested skills are invocable by qualified name, e.g. `/apps/web:deploy`
- Invoked skill content stays in context all session and is not re-read - write standing instructions, not one-time steps. After auto-compaction, each skill's most recent invocation is re-attached with its first 5,000 tokens from a shared 25,000-token budget filled most-recent-first; re-invoke to restore full content
- Skill descriptions load at startup within a listing budget of **1% of the context window**; least-used descriptions drop first (names always kept), each entry capped at 1,536 chars. Diagnose with `/doctor`; tune via `skillListingBudgetFraction`, `skillListingMaxDescChars`, or `SLASH_COMMAND_TOOL_CHAR_BUDGET`

## Structuring Instructions

### Be Concise

The agent is smart. Only add context it doesn't already have - a skill that explains what a PDF is,
or lists four libraries before picking one, spends tokens telling the agent things it knows:

```markdown
# BAD:  "PDF files are a common format containing text and images. To extract
#        text you need a library. There are many available..."
# GOOD: "Use pdfplumber for text extraction."
```

### Avoid Too Many Options

Give one default with an escape hatch, not a menu:

```markdown
# BAD:  "Use pypdf, or pdfplumber, or PyMuPDF, or pdf2image..."
# GOOD: "Use pdfplumber. For scanned PDFs needing OCR, use pdf2image with pytesseract."
```

### Set Degrees of Freedom

- **High freedom** (text guidelines): Multiple approaches valid, context-dependent
- **Medium freedom** (pseudocode/templates): Preferred pattern exists, some variation OK
- **Low freedom** (exact scripts): Operations are fragile, consistency critical

### Recommended SKILL.md Structure

```markdown
# Skill Name

## Quick start
[Minimal working example]

## Workflow Decision Tree
[Route to the right approach based on task type]

## Detailed Instructions
[Step-by-step for each workflow]

## Examples
[Concrete input/output pairs]

## Troubleshooting
[Common errors and fixes]
```

### Reference Files

Keep references **one level deep** from SKILL.md. "Depth" means the reference *chain* (a file linking to a file linking to a file), not filesystem nesting - a `references/` subdirectory is fine. In a chain, Claude may preview files with partial reads (`head`) and miss content.

```markdown
# BAD: Too deep
SKILL.md -> advanced.md -> details.md -> actual info

# GOOD: One level
SKILL.md -> advanced.md (contains the info directly)
SKILL.md -> reference.md (contains the info directly)
```

For reference files >100 lines, include a **table of contents** at the top. Watch file *size* too: a single reference of many hundreds of lines defeats progressive disclosure even at one level deep, because Claude loads the whole file for any subtopic. Split large references by subtopic so each task pulls only what it needs.

## Patterns

### Common Workflow Shapes

Name the shape explicitly in the body rather than assuming the agent infers it:

- **Sequential**: numbered steps, each naming the exact command to run
- **Decision tree**: route on task type up front ("Creating new content? -> Creation workflow")
- **Feedback loop**: validate, fix, re-validate - and state that the loop exits only on a pass
- **Checklist**: for long tasks, have the agent copy a checklist and tick items as it goes

### Single-File Skill Embedded in a CLI

For skills documenting a CLI tool: keep SKILL.md as one file next to the CLI source, compile it into the binary (`go:embed`, Rust `include_str!`, or equivalent), and add a `<tool> skill` subcommand that prints it. The printed guide always matches the installed version, and one command fetches the whole doc - playwright-cli, browser-use (`browser-use skill show`), and agent-browser (`agent-browser skills get core`) all converge on this shape. Never split such a skill into references/; condense carefully instead.

### Working with MCP and Subagents

MCP provides tool access; skills provide the workflow knowledge for using those tools well. Reference MCP tools by qualified name (`BigQuery:bigquery_schema`, `GitHub:create_issue`). Skills are portable expertise; subagents are isolated execution - in Claude Code, `context: fork` frontmatter runs a skill inside a subagent.

### Developing Skills with Claude (A/B Loop)

Build skills with two Claude instances: **Claude A** helps design and refine (it knows the format and what agents need); **Claude B** is a fresh instance with the skill loaded, tested on real tasks. Notice what context you repeatedly supply during normal work, have A capture it as a skill, test with B, bring B's specific failures back to A ("it forgot to filter test accounts"), and repeat. Iterate on observed behavior, not assumptions. For output-style skills, input/output example pairs communicate the desired style better than any description.

## Scripts

When your skill includes executable code:

- **Solve, don't punt**: Handle errors explicitly instead of letting them fail
- **Justify constants**: No magic numbers - document why each value was chosen
- **Prefer execution over loading**: Scripts run without entering context; only output consumes tokens
- **Clarify intent**: "Run `analyze.py`" (execute) vs "See `analyze.py`" (read as reference)
- **List dependencies** in SKILL.md and verify availability

## Testing

### Build Evaluations First

Create evaluations **before** writing extensive instructions - this proves the skill solves a real problem. Run Claude on representative tasks *without* the skill and document the failures; build ~3 scenarios that test those gaps; measure a baseline; then write the minimum instructions needed to pass. Iterate against the baseline.

### Triggering Tests

```
Should trigger:
- "Help me set up a new project in [Service]"
- "I need to create a project" (paraphrased)

Should NOT trigger:
- "What's the weather?" (unrelated)
- "Write Python code" (too generic)
```

### Functional Tests

Test normal operations, edge cases, and out-of-scope requests. Run the same request 3-5 times to check consistency.

### Debug Triggering

Ask Claude: "When would you use the [skill-name] skill?" - it quotes the description back. Adjust based on what's missing.

### Validate Against the Spec

Run the official Agent Skills validator before publishing:

```bash
uvx --from skills-ref agentskills validate path/to/skill
```

Exit 0 means valid. It checks `SKILL.md` format and enforces the spec's strict frontmatter allowlist (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`). Most registries (e.g. ClawHub) and CI gates run this, so validating locally catches failures early. If you rely on Claude Code-only frontmatter (see the publishing caveat under [Frontmatter Reference](#frontmatter-reference)), strip those fields from the copy you validate.

## Pre-Publish Checklist

Calibrate to scope: for a project-local or single-user skill, skip the triggering-accuracy and distribution-hygiene items.

- [ ] Folder and `name` kebab-case and matching; file is exactly `SKILL.md`
- [ ] Description: third person, WHAT + WHEN, specific triggers, under 1024 chars, no angle brackets
- [ ] Single file unless conditionally-loaded content justifies references/; within size budget (`wc -c`)
- [ ] Critical instructions at the top; working examples, not pseudocode; consistent terminology
- [ ] If split: references linked from SKILL.md, one level deep, TOC for files over 100 lines
- [ ] Scripts: explicit error handling, no unexplained constants, dependencies listed, execute-vs-read intent clear
- [ ] Triggering tested: fires on direct and paraphrased requests, silent on unrelated and similar-but-distinct ones
- [ ] Functional: normal and edge cases pass, output consistent across 3-5 runs, tested on more than one model
- [ ] No time-sensitive info, Windows-style paths, or deprecated APIs
- [ ] Spec validator exits 0 (command above)
- [ ] After upload: monitor under/over-triggering in real conversations, iterate the description, bump version on every change

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skill never loads | Description too vague | Add specific triggers and key terms |
| Skill loads for wrong tasks | Description too broad | Add negative triggers, be more specific |
| Instructions not followed | Too verbose or buried | Put critical instructions at top, use headers |
| Slow/degraded responses | SKILL.md too large | Condense first; split to references/ only if content is conditionally loaded (see Single File vs. references/) |
| "Could not find SKILL.md" | Wrong filename | Must be exactly `SKILL.md` (case-sensitive) |
| "Invalid skill name" | Spaces or capitals | Use kebab-case: `my-skill-name` |
| Whole skill silently skipped at load | Description exceeds 1024 chars | Trim it - the loader rejects the file, not just the description |
| Frontmatter fails to parse | An unquoted `description` is a plain YAML scalar, so any colon-space (`Triggers: `, `Use when: `) or straight `"quotes"` inside it breaks parsing | Rewrite the colon as ` - `, or quote the whole value |
| A doc example runs a shell command | A `!` directly touching a backticked command executes on load, even inside a code fence | Move the example to `references/` or break the `!`-backtick adjacency (see [Dynamic-Injection Footgun](#dynamic-injection-footgun)) |

## Distribution

| Surface | How to Deploy |
|---------|--------------|
| Claude.ai | Settings > Features > Upload zip |
| Claude Code (personal) | `~/.claude/skills/<name>/SKILL.md` |
| Claude Code (project) | `.claude/skills/<name>/SKILL.md` |
| Claude Code (plugin) | `<plugin>/skills/<name>/SKILL.md` |
| API | Upload via the Skill Management API, use via the Messages API |
| Enterprise | Managed settings (org-wide) |

Skills don't sync across surfaces - deploy separately to each.

### Using Skills with the API

Custom skills are uploaded through the Skill Management API; `anthropic`-type skills are pre-built by Anthropic. Both are used identically - pass them in the Messages API `container` parameter, each as `{type, skill_id, version}` where `type` is `anthropic` or `custom`. Up to 8 Skills per request, 30 MB max upload (all files combined), and all files must share a common root directory. Requires the code execution tool and the beta headers `code-execution-2025-08-25` and `skills-2025-10-02` (plus `files-api-2025-04-14` for file upload/download).

**Network access differs by surface.** The API code execution environment has **no network access and no runtime package installation** - bundle dependencies or use pre-installed packages. On claude.ai, by contrast, Skills **can** install packages from npm and PyPI and pull from GitHub.

Also: a `pause_turn` stop reason signals a long-running Skill operation; reuse containers across turns via `container.id`; generated files come back via the Files API; changing the Skills list breaks prompt caching; Skills are not ZDR-eligible.

## Security

- Only use skills from **trusted sources**
- No XML angle brackets in frontmatter (injection risk)
- Audit all bundled scripts and resources before using third-party skills
- Be cautious of skills that fetch from external URLs
- Documenting the dynamic-injection syntax is itself a hazard - the loader executes examples at load, even inside code fences. See the [Dynamic-Injection Footgun](#dynamic-injection-footgun) before writing any

## Additional References

- [ClawHub publishing](references/clawhub-publishing.md) - source-mined moderation quirks: reason codes and fixes, LLM-review survival tactics, constraints absent from ClawHub's docs

## Official Resources

- [Agent Skills Spec](https://agentskills.io/specification)
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills)
- [API Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)
- [Engineering Blog: Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [Complete Guide PDF](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
