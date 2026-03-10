---
name: create-skill
description: >
  Create a new SKILL.md file following the Agent Skills open standard
  (agentskills.io). Covers frontmatter schema, section structure,
  writing effective procedures with Expected/On failure pairs,
  validation checklists, cross-referencing, and registry integration.
  Use when codifying a repeatable procedure for agents, adding a new
  capability to the skills library, converting a guide or runbook into
  agent-consumable format, or standardizing a workflow across projects
  or teams.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.1"
  domain: general
  complexity: intermediate
  language: multi
  tags: meta, skill, agentskills, standard, authoring
---

# Create a New Skill

Author a SKILL.md file that agentic systems can consume to execute a specific procedure.

## When to Use

- Codifying a repeatable procedure that agents should follow
- Adding a new capability to the skills library
- Converting a guide, runbook, or checklist into agent-consumable format
- Standardizing a workflow across projects or teams

## Inputs

- **Required**: Task the skill should accomplish
- **Required**: Domain classification — one of the 48 domains in `skills/_registry.yml`:
  `r-packages`, `jigsawr`, `containerization`, `reporting`, `compliance`, `mcp-integration`,
  `web-dev`, `git`, `general`, `citations`, `data-serialization`, `review`, `bushcraft`,
  `esoteric`, `design`, `defensive`, `project-management`, `devops`, `observability`, `mlops`,
  `workflow-visualization`, `swarm`, `morphic`, `alchemy`, `tcg`, `intellectual-property`,
  `gardening`, `shiny`, `animal-training`, `mycology`, `prospecting`, `crafting`,
  `library-science`, `travel`, `relocation`, `a2a-protocol`, `geometry`, `number-theory`,
  `stochastic-processes`, `theoretical-science`, `diffusion`, `hildegard`, `maintenance`,
  `blender`, `visualization`, `3d-printing`, `lapidary`, `versioning`
- **Required**: Complexity level (basic, intermediate, advanced)
- **Optional**: Source material (existing guide, runbook, or working example)
- **Optional**: Related skills to cross-reference

## Procedure

### Step 1: Create Directory

Each skill lives in its own directory:

```bash
mkdir -p skills/<skill-name>/
```

Naming conventions:
- Use lowercase kebab-case: `submit-to-cran`, not `SubmitToCRAN`
- Start with a verb: `create-`, `setup-`, `write-`, `deploy-`, `configure-`
- Be specific: `create-r-dockerfile` not `create-dockerfile`

**Expected:** Directory `skills/<skill-name>/` exists, and the name follows lowercase kebab-case starting with a verb.

**On failure:** If the name does not start with a verb, rename the directory. Check for naming conflicts: `ls skills/ | grep <keyword>` to ensure no existing skill has an overlapping name.

### Step 2: Write YAML Frontmatter

```yaml
---
name: skill-name-here
description: >
  One to three sentences plus key activation triggers. Must be clear
  enough for an agent to decide whether to activate this skill from
  the description alone. Max 1024 characters. Start with a verb.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob  # optional, experimental
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: general
  complexity: intermediate
  language: R | TypeScript | Python | Docker | Rust | multi
  tags: comma, separated, lowercase, tags
---
```

**Required fields**: `name`, `description`

**Optional fields**: `license`, `allowed-tools` (experimental), `metadata`, `compatibility`

**Metadata conventions**:
- `complexity`: basic (< 5 steps, no edge cases), intermediate (5-10 steps, some judgment), advanced (10+ steps, significant domain knowledge)
- `language`: primary language; use `multi` for cross-language skills
- `tags`: 3-6 tags for discovery; include the domain name

**Expected:** YAML frontmatter parses without errors, `name` matches the directory name, and `description` is under 1024 characters with clear activation triggers.

**On failure:** Validate YAML by checking for matching `---` delimiters, proper quoting of version strings (e.g., `"1.0"` not `1.0`), and correct `>` multi-line folding syntax for the description field.

### Step 3: Write the Title and Introduction

```markdown
# Skill Title (Imperative Verb Form)

One paragraph: what this skill accomplishes and the value it provides.
```

The title should match the `name` but in human-readable form. "Submit to CRAN" not "submit-to-cran".

**Expected:** A top-level `#` heading in imperative form followed by a concise paragraph stating what the skill accomplishes.

**On failure:** If the title reads as a noun phrase rather than a verb phrase, rewrite it. "Package Submission" becomes "Submit to CRAN."

### Step 4: Write "When to Use"

List 3-5 trigger conditions — concrete scenarios where an agent should activate this skill:

```markdown
## When to Use

- Starting a new R package from scratch
- Converting loose R scripts into a package
- Setting up a package skeleton for collaborative development
```

Write from the agent's perspective. These are the conditions the agent checks to decide activation.

> **Note**: The most important trigger conditions should also appear in the `description` frontmatter field, since that is read during the discovery phase before the full body is loaded. The `## When to Use` section provides additional detail and context.

**Expected:** 3-5 bullet points describing concrete, observable conditions under which an agent should activate this skill.

**On failure:** If triggers feel vague ("when something needs to be done"), rewrite from the agent's perspective: what observable state or user request would trigger activation?

### Step 5: Write "Inputs"

Separate required from optional. Be specific about types and defaults:

```markdown
## Inputs

- **Required**: Package name (lowercase, no special characters except `.`)
- **Required**: One-line description of the package purpose
- **Optional**: License type (default: MIT)
- **Optional**: Whether to initialize renv (default: yes)
```

**Expected:** Inputs section clearly separates required from optional parameters, each with a type hint and default value where applicable.

**On failure:** If a parameter's type is ambiguous, add a concrete example in parentheses: "Package name (lowercase, no special characters except `.`)".

### Step 6: Write "Procedure"

This is the core of the skill. Each step follows this pattern:

```markdown
### Step N: Action Title

Context sentence explaining what this step accomplishes.

\```language
concrete_code("that the agent can execute")
\```

**Expected:** What success looks like. Be specific — file created, output matches pattern, command exits 0.

**On failure:** Recovery steps. Don't just say "fix it" — provide the most common failure cause and its resolution.
```

**Writing effective steps**:
- Each step should be independently verifiable
- Include actual code, not pseudocode
- Put the most common path first, edge cases in "On failure"
- 5-10 steps is the sweet spot. Under 5 may be too vague; over 12 should be split into multiple skills.
- Reference real tools and real commands, not abstract descriptions

**Expected:** Procedure section contains 5-12 numbered steps, each with concrete code, an `**Expected:**` outcome, and an `**On failure:**` recovery action.

**On failure:** If a step lacks code, add the actual command or configuration. If Expected/On failure is missing, write it now — every step that can fail needs both.

### Step 7: Write "Validation"

A checklist the agent runs after completing the procedure:

```markdown
## Validation

- [ ] Criterion 1 (testable, binary pass/fail)
- [ ] Criterion 2
- [ ] No errors or warnings in output
```

Each item must be objectively verifiable. "Code is clean" is bad. "`devtools::check()` returns 0 errors" is good.

**Expected:** A markdown checklist (`- [ ]`) with 3-8 binary pass/fail criteria that an agent can verify programmatically or by inspection.

**On failure:** Replace subjective criteria with measurable ones. "Well-documented" becomes "All exported functions have `@param`, `@return`, and `@examples` roxygen tags."

### Step 8: Write "Common Pitfalls"

3-6 pitfalls with cause and avoidance:

```markdown
## Common Pitfalls

- **Pitfall name**: What goes wrong and how to avoid it. Be specific about the symptom and the fix.
```

Draw from real experience. The best pitfalls are ones that waste significant time and are non-obvious.

**Expected:** 3-6 pitfalls, each with a bold name, a description of what goes wrong, and how to avoid it.

**On failure:** If pitfalls feel generic ("be careful with X"), make them specific: name the symptom, the cause, and the fix. Draw from actual failure scenarios encountered during development or testing.

### Step 9: Write "Related Skills"

Cross-reference 2-5 skills that are commonly used before, after, or alongside this one:

```markdown
## Related Skills

- `prerequisite-skill` - must be done before this skill
- `follow-up-skill` - commonly done after this skill
- `alternative-skill` - alternative approach to the same goal
```

Use the skill `name` field (kebab-case), not the title.

**Expected:** 2-5 related skills listed with kebab-case IDs and brief descriptions of the relationship (prerequisite, follow-up, alternative).

**On failure:** Verify each referenced skill exists: `ls skills/<skill-name>/SKILL.md`. Remove any references to skills that have been renamed or removed.

### Step 10: Add to Registry

Edit `skills/_registry.yml` and add the new skill under the appropriate domain:

```yaml
- id: skill-name-here
  path: skill-name-here/SKILL.md
  complexity: intermediate
  language: multi
  description: One-line description matching the frontmatter
```

Update the `total_skills` count at the top of the registry.

**Expected:** New entry appears in `skills/_registry.yml` under the correct domain, and `total_skills` count matches the actual number of skill directories on disk.

**On failure:** Count skills on disk with `find skills -name SKILL.md | wc -l` and compare against `total_skills` in the registry. Verify the `id` field matches the directory name exactly.

### Step 11: Add Citations (Optional)

If the skill is based on established methodologies, research papers, software packages, or standards, add citation subfiles to the `references/` directory:

```bash
mkdir -p skills/<skill-name>/references/
```

Create two files:

- **`references/CITATIONS.bib`** — Machine-readable BibTeX (source of truth)
- **`references/CITATIONS.md`** — Human-readable rendered references for GitHub browsing

```bibtex
% references/CITATIONS.bib
@article{author2024title,
  author  = {Author, First and Other, Second},
  title   = {Paper Title},
  journal = {Journal Name},
  year    = {2024},
  doi     = {10.xxxx/xxxxx}
}
```

```markdown
<!-- references/CITATIONS.md -->
# Citations

References underpinning the **skill-name** skill.

1. Author, F., & Other, S. (2024). *Paper Title*. Journal Name. https://doi.org/10.xxxx/xxxxx
```

Citations are optional — add them when provenance tracking matters (academic methods, published standards, regulatory frameworks).

**Expected:** Both files exist and `.bib` parses as valid BibTeX.

**On failure:** Validate BibTeX syntax with `bibtool -d references/CITATIONS.bib` or an online validator.

### Step 12: Validate Skill

Run local validation checks before committing:

```bash
# Check line count (must be ≤500)
lines=$(wc -l < skills/<skill-name>/SKILL.md)
[ "$lines" -le 500 ] && echo "OK ($lines lines)" || echo "FAIL: $lines lines > 500"

# Check required frontmatter fields
head -20 skills/<skill-name>/SKILL.md | grep -q '^name:' && echo "name: OK"
head -20 skills/<skill-name>/SKILL.md | grep -q '^description:' && echo "description: OK"
```

**Expected:** Line count ≤500, all required fields present.

**On failure:** If over 500 lines, apply progressive disclosure — extract large code blocks (>15 lines) to `references/EXAMPLES.md`:

```bash
mkdir -p skills/<skill-name>/references/
```

Move extended code examples, full configuration files, and multi-variant examples to `references/EXAMPLES.md`. Add cross-reference in SKILL.md: `See [EXAMPLES.md](references/EXAMPLES.md) for complete configuration examples.` Keep brief inline snippets (3-10 lines) in the main SKILL.md. The CI workflow at `.github/workflows/validate-skills.yml` enforces these limits on all PRs.

### Step 13: Create Slash Command Symlinks

Create symlinks so Claude Code discovers the skill as a `/slash-command`:

```bash
# Project-level (available in this project)
ln -s ../../skills/<skill-name> .claude/skills/<skill-name>

# Global (available in all projects)
ln -s /mnt/d/dev/p/agent-almanac/skills/<skill-name> ~/.claude/skills/<skill-name>
```

**Expected:** `ls -la .claude/skills/<skill-name>/SKILL.md` resolves to the skill file.

**On failure:** Verify the relative path is correct. From `.claude/skills/`, the path `../../skills/<skill-name>` should reach the skill directory. Use `readlink -f` to debug symlink resolution. Claude Code expects a flat structure at `.claude/skills/<name>/SKILL.md`.

## Validation

- [ ] SKILL.md exists at `skills/<skill-name>/SKILL.md`
- [ ] YAML frontmatter parses without errors
- [ ] `name` field matches directory name
- [ ] `description` is under 1024 characters
- [ ] All required sections present: When to Use, Inputs, Procedure, Validation, Common Pitfalls, Related Skills
- [ ] Every procedure step has concrete code and Expected/On failure pairs
- [ ] Related Skills reference valid skill names
- [ ] Skill is listed in `_registry.yml` with correct path
- [ ] `total_skills` count in registry is updated
- [ ] SKILL.md is ≤500 lines (extract to `references/EXAMPLES.md` if over)
- [ ] Citations added to `references/CITATIONS.bib` + `CITATIONS.md` if skill is based on published methods
- [ ] Symlink exists at `.claude/skills/<skill-name>` pointing to skill directory
- [ ] Global symlink exists at `~/.claude/skills/<skill-name>` (if globally available)

## Common Pitfalls

- **Vague procedures**: "Configure the system appropriately" is useless to an agent. Provide exact commands, file paths, and configuration values.
- **Missing On failure**: Every step that can fail needs recovery guidance. Agents can't improvise — they need the fallback spelled out.
- **Overly broad scope**: A skill that tries to cover "Set up entire development environment" should be 3-5 focused skills instead. One skill = one procedure.
- **Untestable validation**: "Code quality is good" can't be verified. "Linter passes with 0 warnings" can.
- **Stale cross-references**: When renaming or removing skills, grep for the old name in all Related Skills sections.
- **Description too long**: The description field is what agents read to decide activation. Keep it under 1024 characters and front-load the key information.
- **Avoid `git mv` on NTFS-mounted paths (WSL)**: On `/mnt/` paths, `git mv` for directories can create broken permissions (`d?????????`). Use `mkdir -p` + copy files + `git rm` the old path instead. See the [environment guide](../../guides/setting-up-your-environment.md) troubleshooting section.

## Examples

A well-structured skill follows this quality checklist:
1. An agent can decide whether to use it from the description alone
2. The procedure can be followed mechanically without ambiguity
3. Every step has a verifiable outcome
4. Failure modes have concrete recovery paths
5. The skill can be composed with related skills

Size reference from this library:
- Basic skills: ~80-120 lines (e.g., `write-vignette`, `configure-git-repository`)
- Intermediate skills: ~120-180 lines (e.g., `write-testthat-tests`, `manage-renv-dependencies`)
- Advanced skills: ~180-250 lines (e.g., `submit-to-cran`, `setup-gxp-r-project`)
- Skills with extended examples: SKILL.md ≤500 lines + `references/EXAMPLES.md` for large configs

## Related Skills

- `evolve-skill` - evolve and refine skills created with this procedure
- `create-agent` - parallel procedure for creating agent definitions
- `create-team` - parallel procedure for creating team compositions
- `write-claude-md` - CLAUDE.md can reference skills for project-specific workflows
- `configure-git-repository` - skills should be version-controlled
- `commit-changes` - commit the new skill and its symlinks
- `security-audit-codebase` - review skills for accidentally included secrets or credentials
