---
name: find-skills
description: Find, evaluate, compare, adapt, or recommend Agent Skills for Codex or compatible coding agents. Use this skill whenever the user wants to find a skill, compare skill repositories, install a skill, inspect whether an existing skill fits a workflow, modify an existing skill, or decide whether a custom skill should be created instead of installing a generic one.
metadata:
  short-description: Find, evaluate, and recommend agent skills
---

# Find Skills

## Purpose

This skill helps an agent discover, evaluate, compare, recommend, install, adapt, or reject Agent Skills.

The goal is not merely to find something with matching keywords. The goal is to help the user choose the best path for their actual workflow:

1. Use an already installed local skill.
2. Install an existing official or community skill.
3. Combine multiple skills.
4. Modify an existing skill.
5. Create a new custom skill.
6. Skip skill installation and complete the task directly.

Stay generic unless the user provides a specific domain, project, paper, repository, or workflow.

## When to Use

Use this skill when the user asks to:

- Find a skill.
- Search for GitHub skills.
- Find official, curated, popular, or high-star open-source skills.
- Compare skills or skill repositories.
- Recommend a skill for a concrete workflow.
- Find skills for local Codex installation.
- Generate installation commands for skills.
- Check whether a skill is suitable for a task.
- Improve, rewrite, or replace an existing skill.
- Decide whether a custom skill should be created from the user's workflow.

Example user requests:

- "Find a skill for reading papers."
- "Find GitHub skills with many stars."
- "Find official image skills."
- "Find a PPT skill I can install locally."
- "Compare these skill repositories."
- "Which skill should I use for this task?"
- "This skill does not fit my workflow; help me modify it."
- "I will provide a workflow document. Find or create a skill for it."

## General Rules

1. Understand the user's actual task before searching.
2. Prefer local installed skills first when they already solve the task.
3. Prefer official sources first, then curated repositories, then well-maintained community repositories.
4. Rank by workflow fit first, then trustworthiness, installability, maintenance, popularity, and documentation quality.
5. Do not recommend a repository only because it has many stars.
6. Distinguish official, curated, community-maintained, awesome-list, and reference-only resources.
7. Include repository links for recommended external skills.
8. Include installation or adaptation instructions for every recommended external skill.
9. When star counts, download/install counts, activity, APIs, install commands, or repository contents may have changed, verify current sources before relying on them.
10. For every externally recommended GitHub or catalog skill, include both GitHub stars and download/install count when available. If either metric cannot be found, write `not found` or `not listed` explicitly instead of omitting it.
11. Do not instruct the user to run unknown install scripts blindly.
12. Prefer manual inspection and safe installation over `curl | bash` style commands.
13. If search results are not a good fit, say so clearly and recommend modification or custom-skill creation.

## Workflow

### Step 0: Check Local Context First

Before searching the web or external catalogs, inspect what the current session already knows:

1. Available skills listed in the active context.
2. Any skill file path explicitly provided by the user.
3. Existing local skill directories if they are relevant and accessible.
4. The user's current project rules such as `AGENTS.md`.

If a local skill already fits the task, recommend it before external options.

If a local skill is close but flawed, recommend modifying it instead of installing another generic skill.

### Step 1: Identify the User's Real Skill Need

Infer the category from the user's request and restate the practical workflow in one sentence.

Common categories:

- `official`: official skill catalogs or curated skills.
- `slides`: slide decks, PowerPoint, presentation creation/editing.
- `image`: image generation, image editing, visual assets.
- `research`: paper search, paper reading, literature review, citation workflows.
- `writing`: academic writing, technical writing, reports, documentation.
- `coding`: coding, debugging, testing, refactoring, code review.
- `data`: spreadsheets, charts, notebooks, statistics, data analysis.
- `design`: UI, UX, frontend, Figma, visual design.
- `automation`: GitHub, Notion, browser, email, calendar, files, workflow automation.
- `meta`: skill directories, awesome lists, skill discovery tools.
- `custom`: generating or modifying a skill from the user's workflow.

Ask a clarification question only if the request cannot be answered usefully without more information. Otherwise, make a reasonable assumption and proceed.

### Step 2: Search in the Right Order

Search sources in this order:

1. Local installed skills and user-provided skill files.
2. Official skill catalogs and documentation.
3. Official sample skills from the agent provider.
4. Curated skill repositories.
5. Large community skill collections.
6. Individual focused skill repositories.
7. Related awesome lists or reference repositories.

For GitHub or web searches, adapt query patterns like:

```text
agent skills <category> SKILL.md
codex skills <category>
openai skills <category>
claude code skills <category>
gemini cli skills <category>
awesome agent skills <category>
site:github.com <category> skill SKILL.md
```

### Step 2.1: Expand Beyond Literal Keywords

Do not rely only on the user's exact words or on a single `npx skills find` query. Before concluding that few skills exist, generate a small search set from different angles:

1. `Literal query`: the user's original wording.
2. `Task synonyms`: alternate names for the same job, including nouns, verbs, and domain terms.
3. `Workflow stages`: upstream and downstream phases that may appear in broader skills.
4. `Inputs and outputs`: file types, artifacts, APIs, or deliverables the skill may handle.
5. `Tool and platform terms`: agent names, package managers, and common directory conventions.
6. `Quality and review terms`: audit, reviewer, validator, checker, polish, critique, benchmark, submission, or deploy.
7. `Repository structure terms`: `SKILL.md`, `skills/`, `.claude/skills`, `.codex/skills`, `references/`, `scripts/`, and `assets/`.
8. `Marketplace and index terms`: skills.sh, skilld, SkillsAuth, SkillMD, GitHub topics, awesome lists, and curated catalogs.

For complex workflows, search by lifecycle rather than only by label. For example, a request for "full paper writing" should also search for `manuscript lifecycle`, `academic pipeline`, `research to publication`, `literature review`, `submission`, `revision`, `review response`, `claim evidence`, and `IMRAD`, not only `paper writing`.

Use at least three meaningfully different query families when the first search returns too few or too narrow results.

### Step 3: Evaluate Candidates

Evaluate every candidate with these criteria:

| Criterion | What to Check |
|---|---|
| Workflow fit | Does it solve the user's actual workflow, not just match keywords? |
| Relevance | Does it directly match the requested task? |
| Official status | Is it official, curated, experimental, community-maintained, or reference-only? |
| Popularity | GitHub stars, forks, skills.sh installs, npm/download counts when relevant, mentions, adoption, or ecosystem visibility. |
| Metrics freshness | Whether stars and download/install counts were verified from current sources; mark unavailable metrics explicitly. |
| Activity | Recent commits, releases, issues, and maintenance status. |
| Installability | Clear local installation path or compatible skill structure. |
| Structure | Does it contain `SKILL.md`, scripts, examples, assets, or docs? |
| Scope | Single focused skill, multi-skill pack, awesome list, or workflow reference. |
| Quality | Clear instructions, examples, guardrails, and limitations. |
| Risk | Unclear license, unsafe scripts, abandoned repo, exaggerated claims, or credentials required. |

Do not recommend a candidate until you have inspected enough of its actual contents to understand whether it fits.

### Step 4: Classify Each Result

Classify each result as one of:

- `Official`: Maintained by the provider or clearly part of official documentation.
- `Curated`: Officially curated or listed in a recognized catalog.
- `Community`: Maintained by an individual or organization outside the official provider.
- `Awesome list`: A directory of resources rather than a directly installable skill.
- `Reference only`: Useful for ideas or adaptation, but not directly installable.
- `Local existing`: Already installed or provided by the user.
- `Needs modification`: Close to the user's need but should be edited before use.

### Step 5: Make a Decision

After evaluation, choose one of these paths:

1. `Use existing local skill`: The local skill already fits.
2. `Install existing skill`: A candidate is directly suitable and trustworthy enough.
3. `Combine skills`: Multiple focused skills together cover the workflow better than one generic skill.
4. `Modify existing skill`: A local or external skill is close but needs edits.
5. `Create custom skill`: No existing skill captures the workflow well.
6. `Do task directly`: A skill would add overhead and the task can be completed now.

Explain the decision briefly. If recommending a custom skill, describe what the custom skill should contain.

### Step 6: Rank Results

Rank candidates by:

1. Fit to the user's workflow.
2. Trustworthiness.
3. Installability.
4. Maintenance/activity.
5. Popularity.
6. Documentation quality.
7. Ease of adaptation.

If the user explicitly asks for high-star projects, include popularity prominently, but still explain why a lower-star official or focused skill may be better.

### Step 7: Provide Links and Install or Adaptation Method

For every recommended external skill or repository, include:

- Name.
- Repository or catalog link.
- Official/community classification.
- What it is suitable for.
- Installation or adaptation method.
- GitHub stars and download/install count for external GitHub or catalog results.
- Notes, limitations, or safety checks.

Use this table format when helpful:

```markdown
| Rank | Skill / Repository | Type | Link | Stars | Downloads / Installs | Best For | Method | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | ... | Official / Community | https://github.com/... | 1.2k / not found | 10k installs / not listed | ... | `npx skills add ...` or skill-installer helper | ... |
```

## Installation Methods

Choose the safest applicable installation method.

### Method A: Use the Skill Installer Skill

Use this when the user asks you to install a curated skill or a GitHub-hosted skill.

The `skill-installer` skill provides helper scripts. When using those scripts, request network escalation because they fetch from GitHub.

Common helper forms:

```bash
python scripts/list-skills.py
python scripts/list-skills.py --format json
python scripts/list-skills.py --path skills/.experimental
python scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill>
python scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>
```

After installation, tell the user:

```text
Restart Codex to pick up new skills.
```

### Method B: Skills CLI

Use this when the candidate is published in a Skills CLI compatible format and the install command is known.

```bash
npx skills add <package-or-repository>
npx skills add https://github.com/<owner>/<repo> --skill <skill-name>
```

If the command requires network access in a sandbox, request escalation.

### Method C: Manual Git Clone into Skills Directory

Use this when the repository itself is a skill folder or a skill pack.

```bash
mkdir -p "$CODEX_HOME/skills"
git clone <repo-url> "$CODEX_HOME/skills/<skill-or-pack-name>"
```

Then restart Codex.

### Method D: Copy a Specific Skill Folder from a Multi-Skill Repository

Use this when the repository contains many skills and only one is needed.

```bash
git clone <repo-url> /tmp/skills-repo
mkdir -p "$CODEX_HOME/skills/<skill-name>"
cp -R /tmp/skills-repo/<path-to-specific-skill>/* "$CODEX_HOME/skills/<skill-name>/"
```

Then restart Codex.

### Method E: Single `SKILL.md` File Installation

Use this when the skill is provided as one file.

```bash
mkdir -p "$CODEX_HOME/skills/<skill-name>"
cp SKILL.md "$CODEX_HOME/skills/<skill-name>/SKILL.md"
```

Then restart Codex.

### Method F: Reference-Only Adaptation

Use this when the repository is not directly installable as a skill but contains useful workflow instructions.

```bash
mkdir -p "$CODEX_HOME/skills/<new-skill-name>"
# Create a new SKILL.md based on the reference workflow.
```

Explain clearly that this is an adaptation, not a direct install.

## Response Format

Unless the user requests another format, answer using this structure:

```markdown
## Conclusion

Give the top recommendation first and state whether the best path is use, install, combine, modify, create, or do directly.

## Recommendation

Briefly explain why this path fits the user's actual workflow.

## Candidate Comparison

Provide a ranked table. Each external row must include link, type, GitHub stars, download/install count, fit, method, and limitation. For local-only skills, use `local` or `not applicable` for metrics.

## Installation or Modification Details

Provide commands or edit plan for each recommended path.

## Example Usage Prompts

Give 1-3 prompts showing how to use the installed or modified skill.

## Notes and Risks

Mention official/community status, star/download count volatility, compatibility, and security checks.
```

## Required Content in Final Answer

For each recommended external skill, include:

1. Skill or repository name.
2. Repository or catalog link.
3. Official/community classification.
4. GitHub stars, if available; otherwise state `not found`.
5. Download/install count, if available; otherwise state `not listed`.
6. Main use case.
7. Installation or adaptation method.
8. Caveat or limitation, if any.

For each recommendation to modify or create a skill, include:

1. Existing skill path or proposed skill name.
2. Why external candidates are insufficient.
3. Proposed workflow sections.
4. What user input is needed before editing, if any.

## Search Query Examples

Use or adapt these queries depending on the user's request. Treat them as starting points, then expand with synonyms, lifecycle stages, input/output artifacts, and adjacent workflow terms.

### Official Skills

```text
OpenAI skills catalog Codex skill
OpenAI Codex skills SKILL.md
official agent skills catalog
```

### Popular Skill Repositories

```text
awesome agent skills GitHub
awesome codex skills GitHub
agent skills SKILL.md GitHub stars
```

### Slides and Presentations

```text
codex slides skill pptx SKILL.md
agent skill PowerPoint pptx
presentation skill Codex GitHub
deck generation SKILL.md
slides authoring agent skill
pptx python-pptx skill
keynote presentation workflow skill
```

### Image Skills

```text
codex image generation skill SKILL.md
agent skill image editing GitHub
imagegen skill Codex
```

### Research and Paper Reading

```text
research skills Codex GitHub
paper reading skill SKILL.md
literature review agent skill GitHub
academic research skills agent
```

### Writing and Documentation

```text
paper writing skill Codex
academic writing skill SKILL.md
technical writing agent skill
research paper writing skills GitHub
manuscript lifecycle agent skill
academic pipeline SKILL.md
research to publication skill
literature review submission revision response skill
claim evidence reviewer writing skill
```

### Coding and Review

```text
code review skill Codex GitHub
TDD skill Codex SKILL.md
refactoring skill agent GitHub
```

## Security Guidance

When recommending community repositories:

- Tell the user to inspect files before running scripts.
- Avoid `curl | bash` unless it is from a trusted official source.
- Prefer cloning the repository and copying only the needed skill folder.
- Check whether the skill asks for credentials, tokens, or external service access.
- Check the license before reuse in commercial or academic contexts.
- Do not run install scripts automatically unless the user explicitly asks and the command is understood.

## Compatibility Guidance

If a skill is written for another agent ecosystem, explain one of the following:

- It can likely be adapted because it uses a standard `SKILL.md` structure.
- It is useful as a reference but may need manual conversion.
- It is not suitable for Codex without modification.

When adapting a skill, preserve:

- Name and description metadata, unless the user wants to replace an existing skill.
- Activation conditions.
- Step-by-step workflow.
- Tool or dependency requirements.
- Safety warnings.
- Examples.

## Final Checklist

Before responding, check:

- Did I inspect local skills or user-provided skill files first?
- Did I search current sources if popularity, stars, download/install counts, or repository status matters?
- Did I distinguish official from community repositories?
- Did I avoid overclaiming compatibility?
- Did I include repository links?
- Did I include GitHub stars and download/install counts for every recommended external GitHub or catalog skill, or explicitly mark missing metrics?
- Did I include an install or adaptation method for every recommended external skill?
- Did I include example usage prompts when useful?
- Did I mention safety checks for third-party repositories?
- Did I explicitly say when custom skill creation or modification is better than installing a generic skill?
