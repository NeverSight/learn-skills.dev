---
name: ing-skill-generator
description: >
  Expert skill for generating GitHub Copilot skills from ING-internal documentation repositories.
  Use this skill when asked to create a skill from any ING documentation-as-code repo,
  generate a knowledge base skill for an ING framework, convert ING tool documentation
  into a Copilot skill, or turn any docs/ folder into an expert skill file. Also trigger
  when the user mentions "skill from docs", "generate skill", "create skill from repo",
  or references ING-internal frameworks like Baker, Merak, Kingsroad, or similar.
  Includes evaluation framework, grading agents, and benchmark tools for testing generated skills.
---

# ING Skill Generator — Complete Knowledge Base

Generate production-ready GitHub Copilot skills from ING documentation repositories. This skill
transforms documentation-as-code into self-contained expert knowledge bases that senior engineers
can use in their Spring Boot / Java 21 projects.

**This skill includes:**
- Skill generation from local cloned repos
- Evaluation framework with with-skill vs baseline comparison
- Grading agents for automated assertion checking
- Benchmark aggregation and interactive review viewer
- Description optimization for better triggering

At a high level, the process goes like this:

1. User provides a path to a locally cloned ING documentation repository
2. Analyze the repo structure, identify tool name, latest version, documentation files
3. Extract and synthesize content following ING skill template (8 sections)
4. Generate the SKILL.md with proper frontmatter and verbatim code examples
5. Run test cases (with-skill vs baseline) to verify quality
6. Review results, iterate based on feedback
7. Optimize description for better triggering

Your job is to figure out where the user is in this process and help them progress. Maybe they have a freshly cloned repo and want a skill generated. Or maybe they already have a draft and want to improve it. Be flexible — if they say "just generate the skill, I don't need evals", do that instead.

---

## Communicating with the User

The ING skill generator may be used by people across a range of familiarity with coding jargon. While most users are likely senior engineers, pay attention to context cues.

Default assumptions:
- "evaluation" and "benchmark" are OK
- "JSON" and "assertion" — look for cues the user knows these before using without explanation
- ING-specific terms (Baker, Merak, Kingsroad) — explain briefly if unclear

It's OK to briefly explain terms if you're in doubt. Feel free to clarify with a short definition if unsure.

---

## 1. Process Overview

1. **Analyze the repository** — identify the tool name, latest version, documentation structure
2. **Extract content** — gather all relevant docs, configs, code examples, warnings
3. **Synthesize knowledge base** — merge, dedupe, organize into standard sections
4. **Output the skill file** — produce a valid SKILL.md with proper frontmatter

---

## Creating a Skill from Repository

This is the core workflow for generating ING skills from documentation repositories.

### Step 1: Capture Intent

Start by understanding what the user wants. Key questions:

1. **What repository?** Get the local path to the cloned repo (e.g., `/tmp/baker-docs`, `~/projects/merak-sdk`)
2. **What tool/framework?** Confirm the tool name if not obvious from the repo
3. **Any specific focus?** Sometimes users want only certain parts (e.g., "just the API, not the tutorials")
4. **Run test cases?** Suggest yes for complex repos, optional for simple ones

If the conversation already contains this info (e.g., "generate a skill from /tmp/baker"), extract it and confirm.

### Step 2: Analyze the Repository

Before writing anything, understand the documentation structure:

```bash
# Find all documentation files
find <repo-path> -name "*.md" -o -name "*.adoc" -o -name "*.rst" | head -50

# Check for docs directory
ls -la <repo-path>/docs/ 2>/dev/null || ls -la <repo-path>/

# Look for version info
cat <repo-path>/pom.xml 2>/dev/null | grep -A1 "<version>" | head -5
cat <repo-path>/package.json 2>/dev/null | grep "version"
cat <repo-path>/CHANGELOG.md 2>/dev/null | head -20
```

Identify:
- **Tool name** — from repo name, README title, or project config
- **Current version** — from pom.xml, package.json, build.gradle, or badges
- **Documentation structure** — where the main docs live, how they're organized
- **Code examples** — where sample code is located

### Step 3: Map Documentation to Sections

Create a mental map of which source files feed into which output sections:

| Source Files | → Output Section |
|--------------|------------------|
| README.md, docs/overview.md, docs/intro.md | 1. Overview |
| docs/concepts.md, docs/architecture.md | 2. Core Concepts |
| docs/configuration.md, application.properties | 3. Configuration Reference |
| examples/, docs/tutorials/, docs/guides/ | 4. Code Examples |
| docs/integration.md, docs/other-tools.md | 5. Integration |
| docs/troubleshooting.md, docs/faq.md, comments in code | 6. Pitfalls & Anti-patterns |
| docs/faq.md (or generate from common questions) | 7. FAQ |
| Terminology in any doc | 8. Glossary |

### Step 4: Extract and Synthesize

Read each relevant file and extract content:

1. **Copy code verbatim** — never summarize or paraphrase code blocks
2. **Merge duplicates** — if the same concept appears in multiple places, combine into one section
3. **Capture tribal knowledge** — look for comments like "WARNING", "NOTE", "IMPORTANT", gotchas in examples
4. **Mark gaps** — if a section is sparse, include it anyway with ⚠️ marker

### Step 5: Generate the SKILL.md

Follow the exact template structure in Section 6 (Output Template). Key requirements:

- YAML frontmatter with `name` (kebab-case) and `description` (comprehensive, trigger-friendly)
- All 8 sections present, even if sparse
- Configuration tables with 4 columns: Property, Type, Default, Description
- No hyperlinks — all content inline

### Skill Writing Guide

#### Anatomy of an ING Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions (8 sections)
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for tasks
    ├── references/ - Additional docs loaded as needed
    └── assets/     - Templates, examples
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — In context when skill triggers (<500 lines ideal)
3. **Bundled resources** — As needed (read explicitly when required)

**Key patterns:**
- Keep SKILL.md under 500 lines; if approaching limit, move detail to `references/`
- Reference files clearly with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

#### Writing Patterns

Prefer imperative form in instructions.

**Defining output formats:**
```markdown
## Configuration Reference
ALWAYS use this exact table format:
| Property | Type | Default | Description |
|----------|------|---------|-------------|
```

**Examples pattern:**
```markdown
## Code Examples
**Example 1: Basic Recipe**
```java
// Verbatim code from source
Recipe recipe = new Recipe("OrderProcess")
    .withInteraction(validateOrder)
    .withSensoryEvent(orderPlaced);
```
```

#### Writing Style

Explain **why** things are important rather than heavy-handed MUSTs. Use theory of mind and make the skill general, not narrow to specific examples. Write a draft, then review with fresh eyes and improve.

### Step 6: Test Cases

After generating the skill, create 2-3 realistic test prompts. Save to `evals/evals.json`:

```json
{
  "skill_name": "baker-framework",
  "evals": [
    {
      "id": 1,
      "name": "basic-recipe-creation",
      "prompt": "Generate a skill from the Baker docs at /tmp/baker",
      "expected_output": "SKILL.md with 8 sections, proper frontmatter",
      "files": [],
      "expectations": []
    }
  ]
}
```

See `references/schemas.md` for the full schema.

---

## 2. Naming Rules

Derive the canonical name directly from the repository:

| Source | Priority |
|--------|----------|
| Repository name | Highest (e.g., `ing-bank/baker` → `baker`) |
| Top-level README title | If repo name is generic |
| Project folder name | Fallback |

**Critical rules:**
- Use exactly what the project is called — no inventing, generalizing, or renaming
- Convert to kebab-case for the skill `name` field (e.g., `Baker Framework` → `baker-framework`)
- If the repo covers multiple tools, derive each tool's name from its module/subfolder/section title

---

## 3. Versioning Strategy

When documentation contains multiple versions:

1. **Identify latest version** using:
   - Explicit version numbers (e.g., `v4.1.0` > `v3.2.0`)
   - Release dates (e.g., `2024` > `2023`)
   - Folder/file naming (e.g., `docs-v2/` > `docs-v1/`)
   - `CHANGELOG.md` or release notes

2. **Use latest version as source of truth** for all:
   - Configuration properties
   - API signatures
   - Code examples
   - Behavioral descriptions

3. **Document version changes** when relevant:
   ```
   📌 Changed in 4.0 — previous behavior was: synchronous execution only
   ```

4. **Discard deprecated content** unless it explains a still-relevant migration path

---

## 4. Content Extraction

### 4.1 What to Include

| Content Type | Handling |
|--------------|----------|
| Code snippets | Copy **verbatim** — never summarize |
| Configuration blocks | Copy **verbatim** with all properties |
| API signatures | Copy **verbatim** with types and parameters |
| Architecture diagrams (textual) | Include as ASCII or describe structure |
| Warnings / gotchas | Always include, even if brief |
| Anti-patterns | Always include with explanations |
| Tribal knowledge | Capture implicit knowledge from comments, examples |

### 4.2 What to Exclude

- Hyperlinks (all content must be inline)
- File path references to the source repo
- Installation instructions for the docs themselves
- CI/CD pipeline configs for the docs repo
- Contributor guidelines (unless relevant to framework usage)

### 4.3 Merging and Deduplication

When a concept appears in multiple files:
1. Identify all occurrences
2. Merge into one coherent section
3. Preserve all unique details from each source
4. Remove redundant explanations

---

## 5. Handling Sparse Documentation

When documentation is incomplete or ambiguous:

1. Add a clear marker:
   ```
   ⚠️ Documentation incomplete — verify with team
   ```

2. Include whatever partial information exists

3. Note specific gaps:
   ```
   ⚠️ Default value not documented — verify in source code
   ```

---

## 6. Output Template

**CRITICAL: All 8 sections MUST be present in every generated skill.** If documentation is sparse for a section, include it anyway with a ⚠️ marker noting what's missing.

The generated skill must follow this exact structure:

```markdown
---
name: [tool-name-kebab-case]
description: >
  Expert skill for [Tool Name] — an ING-internal framework for [one-line purpose].
  Use this skill when working in any ING Spring Boot / Java 21 project that integrates
  with [Tool Name]. Covers configuration, recipes, integration patterns, pitfalls,
  and verbatim code examples.
---

# [Tool Name] — Complete Knowledge Base

## Table of Contents
1. Overview
2. Core Concepts
3. Configuration Reference
4. Code Examples
5. Integration with Other ING Tools
6. Pitfalls & Anti-patterns
7. FAQ
8. Glossary

---

## 1. Overview

[What the tool does and why it exists inside ING. MUST include current version number.]

### Current Version: X.Y.Z

[Version-specific notes if any]

## 2. Core Concepts

[Mental models, architecture decisions, key abstractions. Use tables for comparisons.]

## 3. Configuration Reference

**MANDATORY: Configuration tables MUST have exactly 4 columns: Property, Type, Default, Description**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| example.property | String | `null` | Purpose of property |
| example.timeout | int | `3000` | Timeout in milliseconds ⚠️ NOT seconds |

If default is unknown, use: `⚠️ verify` as the value.

## 4. Code Examples

[Verbatim snippets from source docs, organized by use case. NEVER summarize or paraphrase code.]

```java
// Example: Basic interaction definition
@RequiresIngredient("orderId")
@FiresEvent(OrderValidated.class)
public interface ValidateOrder {
    OrderValidated apply(String orderId);
}
```

## 5. Integration with Other ING Tools

[How this tool connects to Baker / Merak SDK / Kingsroad / other ING systems]

⚠️ If no integration docs exist, write: "No documented integrations. Check with the team for internal usage patterns."

## 6. Pitfalls & Anti-patterns

[Exact warnings from docs + implicit gotchas discovered in examples]

❌ **Don't**: [Anti-pattern description]
✅ **Do**: [Correct approach]

⚠️ If no pitfalls documented, write: "No pitfalls documented. Exercise standard caution with [relevant concerns]."

## 7. FAQ

**Q: [Common question from docs or implied by content]**
A: [Answer]

⚠️ If no FAQ exists, generate 2-3 questions based on likely user needs.

## 8. Glossary

| Term | Definition |
|------|------------|
| [ING-specific term] | [Precise definition] |

⚠️ If no glossary exists, extract key terms from the documentation and define them.
```

---

## 7. Frontmatter Requirements

### 7.1 Name Field

- Kebab-case, lowercase
- Derived from repo/project name
- Example: `baker-framework`, `merak-sdk`, `kingsroad-cli`

### 7.2 Description Field

The description is the **primary trigger mechanism**. Make it comprehensive:

1. Start with what the skill is for
2. Include the framework's purpose
3. List specific contexts when to use
4. Mention related keywords that should trigger

**Good example:**
```yaml
description: >
  Expert skill for Baker — an ING-internal framework for orchestrating microservice-based
  process flows using a declarative recipe DSL. Use this skill when working in any ING
  Spring Boot / Java 21 project that integrates with Baker. Covers configuration, recipes,
  interactions, event handling, error strategies, testing, and verbatim code examples.
```

---

## 8. Target Audience

The generated skill targets:

- **Senior engineers at ING** working in Spring Boot / Java 21 projects on Kubernetes
- They know general software engineering
- They do **not** know ING-internal framework internals
- They need practical, actionable guidance

Write accordingly:
- Explain ING-specific concepts
- Don't explain basic Java/Spring concepts
- Include complete, working examples
- Highlight common mistakes

---

## 9. Quality Checklist

Before finalizing a generated skill, verify:

**Structural Requirements (MANDATORY):**
- [ ] YAML frontmatter present with `---` delimiters
- [ ] `name` field is kebab-case, derived from repo/project
- [ ] `description` field includes purpose and trigger keywords
- [ ] All 8 sections present (Overview through Glossary)
- [ ] Table of Contents matches section headings

**Content Requirements:**
- [ ] Latest version identified and stated in Overview
- [ ] All code snippets copied verbatim (no summarization)
- [ ] Configuration table has 4 columns: Property, Type, Default, Description
- [ ] No hyperlinks or external URLs anywhere
- [ ] Sparse sections marked with ⚠️ (not omitted)
- [ ] Version changes marked with 📌
- [ ] Content is self-contained and usable in isolation

**Common Mistakes to Avoid:**
- ❌ Omitting sections because docs are sparse (always include with ⚠️)
- ❌ Missing "Default" column in config tables
- ❌ Summarizing code instead of copying verbatim
- ❌ Using non-kebab-case names (e.g., "Baker_Framework" instead of "baker-framework")
- ❌ Including hyperlinks (convert to inline content)

---

## 10. Example Workflow

When asked to generate a skill from a repo:

1. **Read the repo structure**
   ```bash
   find <repo-path> -name "*.md" -o -name "*.adoc" | head -50
   ls <repo-path>/docs/ 2>/dev/null || ls <repo-path>/
   ```

2. **Identify the tool name and version**
   - Check README.md, pom.xml, build.gradle, package.json
   - Look for version badges, changelog, releases

3. **Map documentation to output sections**
   - Overview/Introduction → Section 1
   - Concepts/Architecture → Section 2
   - Configuration/Properties → Section 3
   - Examples/Tutorials → Section 4
   - Integration guides → Section 5
   - Troubleshooting/Warnings → Section 6
   - FAQ (if exists) → Section 7
   - Glossary/Terms → Section 8

4. **Extract and synthesize**
   - Read each relevant file
   - Copy code blocks verbatim
   - Merge duplicate explanations
   - Note gaps with ⚠️ markers

5. **Generate the SKILL.md**
   - Use exact template structure
   - Validate frontmatter YAML
   - Ensure no broken references

6. **Save to appropriate location**
   - Default: `.github/skills/[tool-name]/SKILL.md`

---

## 11. Running and Evaluating Test Cases

After generating a skill, run test cases to verify quality. Put results in `<skill-name>-workspace/` as a sibling to the skill directory.

### Step 1: Spawn all runs (with-skill AND baseline) in parallel

For each test case, spawn two subagents in the same turn — one with the skill, one without:

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>/SKILL.md
- Task: <eval prompt - e.g., "Generate a skill from the Baker docs at /tmp/baker">
- Input files: <path to cloned repo>
- Save outputs to: <workspace>/iteration-<N>/eval-<name>/with_skill/outputs/
- Outputs to save: The generated SKILL.md file

IMPORTANT: First read the skill, then follow its instructions.
```

**Baseline run (no skill):**
```
Execute this task (no skill guidance - baseline):
- Task: <same eval prompt>
- Input files: <same repo path>
- Save outputs to: <workspace>/iteration-<N>/eval-<name>/without_skill/outputs/
- Outputs to save: The generated SKILL.md file
```

Write an `eval_metadata.json` for each test case:

```json
{
  "eval_id": 1,
  "eval_name": "baker-repo-full",
  "prompt": "Generate a skill from the Baker docs at /tmp/baker",
  "assertions": [
    "Output is a valid SKILL.md file with YAML frontmatter",
    "Contains all 8 required sections",
    "Code examples are verbatim from source"
  ]
}
```

### Step 2: Draft assertions while runs are in progress

Good assertions for ING skill generation:

**Structural:**
- "Output has YAML frontmatter with --- delimiters"
- "Frontmatter contains 'name' field in kebab-case"
- "Contains all 8 sections: Overview through Glossary"
- "Configuration table has 4 columns: Property, Type, Default, Description"

**Content:**
- "Version number X.Y.Z is mentioned in Overview"
- "Code examples are verbatim (not summarized)"
- "No hyperlinks or external URLs"
- "Sparse sections marked with ⚠️"

**Version handling:**
- "Uses only latest version content"
- "Deprecated content excluded"
- "Version changes marked with 📌"

### Step 3: Capture timing data as runs complete

When each subagent completes, save timing to `timing.json`:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

### Step 4: Grade, aggregate, and launch viewer

1. **Grade each run** — spawn a grader subagent that reads `agents/grader.md` and evaluates assertions. Save to `grading.json`:

```json
{
  "with_skill": {
    "assertions": [
      {"text": "Has YAML frontmatter", "passed": true, "evidence": "File starts with ---"},
      {"text": "All 8 sections present", "passed": true, "evidence": "Found sections 1-8"}
    ],
    "pass_rate": 1.0
  },
  "without_skill": {
    "assertions": [
      {"text": "Has YAML frontmatter", "passed": false, "evidence": "No --- delimiters found"},
      {"text": "All 8 sections present", "passed": false, "evidence": "Missing FAQ, Glossary"}
    ],
    "pass_rate": 0.17
  },
  "winner": "with_skill",
  "notes": "Skill enforces ING template structure"
}
```

2. **Aggregate into benchmark:**
```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

3. **Launch the viewer:**
```bash
python eval-viewer/generate_review.py <workspace>/iteration-N \
  --skill-name "ing-skill-generator" \
  --benchmark <workspace>/iteration-N/benchmark.json
```

For iteration 2+, add `--previous-workspace <workspace>/iteration-<N-1>`.

For headless environments, use `--static <output.html>` instead.

### Step 5: Read feedback and improve

When the user reviews results, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-1-with_skill", "feedback": "missing version number in overview"},
    {"run_id": "eval-2-with_skill", "feedback": ""}
  ]
}
```

Empty feedback = user is satisfied. Focus improvements on cases with complaints.

---

## 12. Improving the Skill

After running test cases and collecting feedback:

### How to improve ING skill generation

1. **Check structural compliance** — If outputs are missing sections or using wrong formats, strengthen the template instructions with explicit requirements.

2. **Check content extraction** — If code examples are summarized instead of verbatim, add more emphasis on copying exactly. If warnings/pitfalls are missed, add instructions to scan for keywords like "WARNING", "NOTE", "⚠️".

3. **Check version handling** — If old content leaks in, add clearer instructions to identify and exclude deprecated versions.

4. **Look at transcripts** — Read how the subagent processed the docs. If it's doing redundant work or missing files, adjust the workflow instructions.

5. **Look for repeated work** — If all test runs independently wrote similar helper scripts or took the same approach, consider bundling that script in the skill's `scripts/` directory.

### The iteration loop

1. Apply improvements to `SKILL.md`
2. Rerun all test cases into `iteration-<N+1>/`
3. Launch viewer with `--previous-workspace` pointing to previous iteration
4. Collect feedback, improve, repeat

Keep going until:
- User is happy
- All feedback is empty
- Pass rates are consistently high

---

## 13. Advanced: Blind Comparison

For situations where you want a more rigorous comparison between two versions of a skill (e.g., "is the new version actually better?"), there's a blind comparison system.

### How it works

1. Give two outputs to an independent agent **without telling it which is which**
2. Let it judge quality based purely on the outputs
3. Analyze why the winner won

Read `agents/comparator.md` and `agents/analyzer.md` for the details.

### When to use

- Comparing a new skill version against the previous version
- Deciding between two different approaches to the same problem
- When quantitative metrics (pass rates) are similar but you sense a quality difference

This is optional and requires subagents. The human review loop is usually sufficient.

---

## 14. Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether Claude invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger (8-10) and should-not-trigger (8-10).

The queries must be **realistic** — the kind of thing a real Claude Code user would actually type. Include:
- File paths and personal context
- Different lengths and styles (formal, casual, typos)
- Edge cases, not clear-cut examples

**Bad examples:**
```
"Format this data"
"Extract text from PDF"
"Create a skill"
```

**Good examples:**
```
"ok so I just cloned the merak-sdk repo to /tmp/merak and my tech lead wants me to turn the docs into something our team can use in their IDE. can you help?"

"I have the Baker framework documentation at ~/projects/ing-bank/baker/docs. Need to create a Copilot skill that covers all the recipe patterns and error handling strategies."

"we're using kingsroad-cli internally and the docs are scattered across like 5 different markdown files. can you consolidate them into a skill?"
```

**For should-trigger queries**, think about coverage:
- Different phrasings of the same intent (formal, casual)
- Cases where the user doesn't explicitly say "skill" but clearly needs one
- Mentions of ING frameworks (Baker, Merak, Kingsroad)
- References to documentation repos, docs/ folders

**For should-not-trigger queries**, the most valuable are near-misses:
- Using the frameworks (not creating skills for them)
- "How do I configure Baker retry policies?" — needs Baker skill, not skill generator
- General Spring Boot/Java questions
- Other types of skill creation (not ING-specific)

The key: don't make should-not-trigger queries obviously irrelevant. "Write a fibonacci function" is too easy — it doesn't test anything. Negative cases should be genuinely tricky.

### Step 2: Review with user

Present the eval set for review using the HTML template:

1. Read the template from `assets/eval_review.html`
2. Replace placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` → the JSON array
   - `__SKILL_NAME_PLACEHOLDER__` → skill name
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → current description
3. Write to temp file and open: `open /tmp/eval_review_ing-skill-generator.html`
4. User edits queries, toggles should-trigger, then clicks "Export Eval Set"
5. File downloads to `~/Downloads/eval_set.json`

This step matters — bad eval queries lead to bad descriptions.

### Step 3: Run the optimization loop

Tell the user: "This will take some time — I'll run in the background and check periodically."

```bash
python -m scripts.run_loop \
  --eval-set <workspace>/trigger-eval.json \
  --skill-path <skill-path> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your system prompt so triggering tests match what the user experiences.

The script:
- Splits eval set into 60% train / 40% held-out test
- Evaluates current description (3 runs per query for reliability)
- Proposes improvements based on failures
- Re-evaluates each new description on both train and test
- Selects best by **test score** (not train) to avoid overfitting

### How skill triggering works

Understanding this helps design better eval queries:

- Skills appear in Claude's `available_skills` list with name + description
- Claude decides whether to consult a skill based on that description
- **Important:** Claude only consults skills for tasks it can't easily handle on its own

This means:
- Simple queries like "read this file" may not trigger skills even if description matches
- Complex, multi-step, or specialized queries reliably trigger when description matches
- Your eval queries should be substantive enough that Claude would benefit from consulting a skill

### Step 4: Apply results

Take `best_description` from the JSON output and update SKILL.md frontmatter. Show the user before/after and report scores.

### Package and Present

If you have access to the `present_files` tool, package the skill:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

This creates a `.skill` file the user can install.

---

## 15. Claude.ai-Specific Instructions

In Claude.ai, the core workflow is the same (analyze repo → generate skill → test → review → improve), but some mechanics change because Claude.ai doesn't have subagents.

**Running test cases**: No subagents means no parallel execution. For each test case:
1. Read the skill's SKILL.md
2. Follow its instructions to accomplish the test prompt yourself
3. Do them one at a time

This is less rigorous than independent subagents (you wrote the skill and you're running it), but it's a useful sanity check — the human review step compensates.

**Reviewing results**: If you can't open a browser (no display), skip the browser reviewer. Instead, present results directly in the conversation:
- Show the prompt and output for each test case
- If output is a file, save it and tell the user where to download
- Ask for feedback inline: "How does this look? Anything you'd change?"

**Benchmarking**: Skip quantitative benchmarking — it relies on baseline comparisons which aren't meaningful without subagents. Focus on qualitative feedback.

**The iteration loop**: Same as before — improve the skill, rerun test cases, ask for feedback — just without the browser reviewer.

**Description optimization**: Requires `claude -p` CLI which is only in Claude Code. Skip it on Claude.ai.

**Blind comparison**: Requires subagents. Skip it.

**Packaging**: `package_skill.py` works anywhere with Python. User can download the resulting `.skill` file.

**Updating an existing skill**: The user might want to update, not create. In this case:
- **Preserve the original name** — use unchanged
- **Copy to writeable location before editing** — installed paths may be read-only
- **Stage in `/tmp/` first** if packaging manually

---

## 16. Cowork-Specific Instructions

If you're in Cowork:

- **Subagents work** — the main workflow (spawn tests in parallel, run baselines, grade) all works. If timeouts are severe, run tests in series.

- **No browser/display** — use `--static <output_path>` to write standalone HTML instead of starting a server. Then proffer a link for the user to open.

- **IMPORTANT: Generate the eval viewer BEFORE evaluating yourself.** Use `generate_review.py` (not custom HTML). Get results in front of the human ASAP!

- **Feedback via download** — since there's no running server, "Submit All Reviews" downloads `feedback.json`. Read it from Downloads (may need to request access).

- **Packaging works** — `package_skill.py` just needs Python and filesystem.

- **Description optimization** — `run_loop.py` / `run_eval.py` should work fine since they use `claude -p` subprocess, not browser. Save this until the skill is fully finished and user agrees it's good.

- **Updating existing skills** — follow the update guidance in Claude.ai section above.

---

## 17. Reference Files

The following files support evaluation and improvement:

**agents/**
- `grader.md` — How to evaluate assertions against outputs
- `comparator.md` — Blind A/B comparison between versions
- `analyzer.md` — Analyze why one version beat another

**references/**
- `schemas.md` — JSON structures for evals.json, grading.json, benchmark.json

**scripts/**
- `aggregate_benchmark.py` — Combine grading results into benchmark stats
- `generate_report.py` — Create summary reports
- `improve_description.py` — Generate improved descriptions
- `run_eval.py` — Run trigger evaluation
- `run_loop.py` — Full optimization loop
- `quick_validate.py` — Fast validation checks

**eval-viewer/**
- `generate_review.py` — Generate interactive review page
- `viewer.html` — Template for review interface
