---
name: init-copilot-review
description: Use skill if you are creating or refining GitHub Copilot code review instruction files such as .github/copilot-instructions.md and scoped *.instructions.md for repository-specific PR reviews.
---

# Copilot Review Init

Create or refine GitHub Copilot review instruction files for a specific repository. Focus on repo-grounded `copilot-instructions.md` and scoped `*.instructions.md` files that improve pull request review quality without wasting character budget.

## Trigger boundaries

Use this skill when you need to:
- Create or revise `.github/copilot-instructions.md`
- Create, split, or tighten `.github/instructions/*.instructions.md`
- Decide root vs scoped review rules, monorepo/package scoping, `applyTo`, or `excludeAgent`
- Debug why Copilot review ignores, misroutes, or weakly follows instruction files

Do not use this skill when:
- You are reviewing a PR directly instead of authoring Copilot review instructions
- You are creating non-Copilot agent files such as `CLAUDE.md`, `AGENTS.md`, or generic review docs
- You want generic best-practice prose without grounding it in the target repository

## Start with the smallest relevant reference set

| Need | Read |
| --- | --- |
| File locations, root vs scoped format, base-branch behavior, character limits | `references/setup-and-format.md` |
| Rule-writing quality, root vs scoped content decisions, character budgeting, iteration | `references/writing-instructions.md` |
| `applyTo`, `excludeAgent`, precedence, monorepo layout, overlapping scopes | `references/scoping-and-targeting.md` |
| Ignored instructions, wrong file scope, debugging order, verification | `references/troubleshooting.md` |
| Full-stack examples after the file architecture is chosen | `references/scenarios.md` |
| Small starter patterns after repo grounding | `references/micro-library.md` |

Do not read every reference by default. Start with the minimum set that fits the task, then expand only if a real uncertainty remains.

## Workflow

### 1. Ground on the repository before drafting

Inspect the actual repository first. Quick repo scan recipe:

```bash
find . -maxdepth 3 -type f -name "*.md" | head -20       # doc landscape
ls .github/ .github/instructions/ 2>/dev/null             # existing Copilot config
cat .eslintrc* .prettierrc* biome.json 2>/dev/null | head  # enforced style rules
find . \( -name "*.test.*" \) -o \( -name "*.spec.*" \) | head -10  # test conventions
```

Gather:
- Structure: single app, multi-service, or monorepo
- Dominant languages, frameworks, and path boundaries
- Existing `.github/copilot-instructions.md`, `.github/instructions/`, `CONTRIBUTING.md`, `CLAUDE.md`, and similar repo guidance
- Linter, formatter, test, and CI configuration so you do not waste rule budget on enforced style rules
- Representative files in each scope (examine 2–3 files per scope: one typical, one complex, one boundary-case)
- Recurring review themes: look for repeated patterns in recent PRs, open issues, code comments, and CONTRIBUTING.md that point to risk areas or repeated defects

> **⚠️ Steering: Existing instruction files.** If the repository already has copilot instruction files, do NOT start from scratch. Evaluate them against the quality criteria in Step 3 (SMSA). Note gaps, redundancies, and linter-duplicated rules. Then decide: **refine in place** if the architecture is sound (most existing files just need tightening), or **recreate** only if the structure fundamentally misroutes rules. The default is to refine.

> **⚠️ Steering: Multi-stack repositories.** When a repo has two fundamentally different stacks (e.g., Go backend + Svelte frontend, Python API + React SPA), treat each stack as a separate scope from the start. Check whether the secondary stack is a bundled artifact (e.g., `ui/dist/`) or actively developed source (e.g., `ui/src/`). Only actively developed source needs its own instruction files.

**Stopping test — move on when you can answer all three:**
1. What are the 2–4 highest-risk areas where review catches real bugs?
2. Which linter/formatter rules already enforce style, so you can skip them?
3. What is the narrowest directory structure that separates review scopes?

**Done when:** All three stopping-test questions are answered with repo evidence. If you cannot answer one, you need more exploration. If all three are answered, stop — more exploration adds no value.

### 2. Choose the instruction architecture before writing prose

Start from this default shape:

```text
.github/
├── copilot-instructions.md
└── instructions/
    ├── <language>.instructions.md
    └── <domain-or-package>.instructions.md
```

Use this placement logic:

| Put it in | When |
| --- | --- |
| `.github/copilot-instructions.md` | The rule is truly universal across the repo: security fundamentals, shared error-handling philosophy, shared performance red flags, or repo-wide testing expectations |
| `.github/instructions/<language>.instructions.md` | The rule applies to one language or ecosystem and is not just a linter concern |
| `.github/instructions/<framework-or-path>.instructions.md` | The rule applies only to a framework, directory, layer, or critical path such as `api`, `auth`, `migrations`, or `components`. For frameworks with route groups (e.g. Next.js `(admin)`, `(marketing)`), scope to the parent directory rather than each group |
| Package/service-scoped `*.instructions.md` | A monorepo package or service has unique review needs not already covered by repo-wide rules. A package qualifies for its own file only when it has 2+ rules that do not apply to any other package |
| `excludeAgent` | A rule should guide code review but would confuse the coding agent, or vice versa |

Steering rules:
- Start minimal: most repos should begin with **1 repo-wide file plus 2–4 scoped files**
- Grow toward **5–12 total files** only when repo breadth justifies it
- Do **not** create a file just because you detected a language or framework; create it only if you have **2–3 high-signal rules** (rules that catch bugs, security issues, or architectural mistakes a linter cannot) **unique to that scope**
- Do **not** dump everything into `copilot-instructions.md`; that causes scope bleed and usually wastes the 4,000-character limit
- Monorepo package files must contain only package-unique rules, not repeated root rules

> **⚠️ Steering: Over-creation trap.** The most common mistake is creating a file for every detected technology. A repo using TypeScript + React + Prisma does NOT need three separate files if most rules are shared. Start with 1 root + 2 scoped, then add only when a new scope has 2+ unique rules that do not fit anywhere else.

**Done when:** You have a file tree with file names and the `applyTo` glob for each scoped file. Every file in the tree has a clear reason to exist.

### 3. Select rules with evidence and reuse discipline

Every rule should be **Specific, Measurable, Actionable, and Semantic** (SMSA).

**SMSA quick check for each rule:**

| Criterion | Pass | Fail |
| --- | --- | --- |
| **Specific** | "Flag any `useEffect` that directly calls a fetch function without AbortController cleanup" | "Avoid side effects in components" |
| **Measurable** | Copilot can clearly decide yes/no per diff hunk | Requires subjective judgment |
| **Actionable** | "When a Prisma `findMany` lacks a `take` or `where` clause, flag it as an unbounded query" | "Be careful with database queries" |
| **Semantic** | Catches architectural/security/logic issues beyond syntax | "Use consistent naming" (linter territory) |

Use this filter:

| Keep | Drop |
| --- | --- |
| Rules backed by repo code, configs, docs, or repeated defects | Generic best practices with no repo evidence |
| Semantic review guidance about security, architecture, data flow, error handling, performance, tests, or accessibility | Formatting, import order, spacing, quote style, or other linter territory |
| Short imperative bullets that say what to flag and why | Narrative paragraphs, hedged advice, or vague slogans like "write clean code" |
| Adapted examples using repo patterns | Copy-pasted templates or external-link references |

Reusable categories are helpful only when the repository actually needs them:
- Repo-wide candidates: security, shared error handling, shared performance risks, testing philosophy
- Scoped candidates: language idioms, framework conventions, API validation, auth/payment paths, migrations, package boundaries, test-file rules

If you use `references/scenarios.md` (consult when you need a full-stack example for an architecture you have already chosen) or `references/micro-library.md` (consult when you need a starter pattern for a specific scope after grounding), treat them as **pattern libraries to adapt — never copy verbatim**. Change variable names, error types, framework calls, and examples to match the target repo's actual code.

> **⚠️ Steering: Concept overlap ≠ duplication.** Two files may mention the same concept (e.g., error handling) as long as the rules are additive and target different contexts. A root file saying "always return structured errors" and a scoped API file saying "use ApiError with status codes" are complementary, not duplicates. Flag duplication only when the same instruction text is copy-pasted or when rules could contradict.

**Done when:** Every rule passes the SMSA check, no rule duplicates a linter, and every rule cites specific repo evidence (file, config, pattern, or convention).

### 4. Draft files with scope-safe formatting

When writing files:
- `copilot-instructions.md` is plain Markdown in `.github/` and has **no frontmatter**
- Every scoped file lives under `.github/instructions/`
- Every scoped file starts at **line 1** with YAML frontmatter:

```yaml
---
applyTo: "src/api/**/*.ts"
---
```

- `applyTo` is a **single quoted or double-quoted glob string** relative to repo root
- GitHub Copilot uses standard glob patterns including `**`, `*`, and brace expansion `{a,b}`
- Glob syntax: `*` matches within a directory, `**` matches across directories, `{ts,tsx}` matches alternatives
- When a logical domain spans multiple directories, prefer a broader wildcard like `src/**/*.ts` over listing each subdirectory
- `excludeAgent`, when used, should be either `"code-review"` or `"coding-agent"`
- File names should use `kebab-case.instructions.md`
- Highest-priority rules go first
- Keep examples short and include them only when they clarify a semantic rule

> **⚠️ Steering: Brace expansion platform validation.** While `{ts,tsx}` is standard glob syntax and works in `find` and most glob engines, always verify your patterns match the intended files with the `find` command in Step 5. If you are uncertain about Copilot's glob engine supporting a specific syntax, use a broader pattern (e.g., `**/*.ts` plus a separate file for `**/*.tsx`) as a safe fallback.

Overlapping scoped files are acceptable only when the rules are **additive** — two files may mention the same concept if the rules target different contexts. Flag duplication only when the same instruction is copy-pasted or when rules could conflict. If two matching files would disagree, narrow `applyTo` until they no longer conflict. Multiple matching scoped files are concatenated, so never rely on overlap to resolve contradictions for you.

**Done when:** Every file has correct frontmatter (or none for root), every `applyTo` glob is verified against the repo structure, and no file exceeds 3,500 characters (leaving buffer below the 4,000 hard limit).

### 5. Validate before presenting anything

Run this checklist — every item must pass:

**Character limits:**
- Each file stays under the **hard 4,000-character limit**; aim for **2,500–3,500**
- Frontmatter counts toward the limit
- Use `wc -c` for byte count or `wc -m` for true character count (matters for multi-byte content like UTF-8 emoji or CJK characters)

**Content quality:**
- No external links
- No attempts to control Copilot's comment formatting, severity labels, approvals, or merge blocking
- No rules duplicated from linter or formatter config — verify by grepping: `grep -r "rule-name" .eslintrc* biome.json golangci* 2>/dev/null`
- No contradictory rules across overlapping scopes
- Root file contains only universal rules
- Package/service files do not repeat root rules

**Glob verification:**
```bash
# Verify a glob pattern matches intended files
find . -path "./<applyTo-pattern>" -type f | head -20
```

**Deployment awareness:**
- Instruction changes must be on the **base branch** of the PR (typically `main` or `develop`) to affect review. A feature-branch-only change does NOT affect the same PR's review. Plan for a merge-to-base then re-review workflow.

**Done when:** All checklist items pass. If any fail, fix before proceeding to Step 6.

### 6. Present the result as an architecture, not just a dump

Return:
- The `.github/` file tree
- Full contents of each generated instruction file
- A 1–3 sentence per-file explanation covering:
  - Why this file exists
  - What scope it targets
  - Which repo evidence justified its rules
  - Why the rule set was kept out of other files

If repo evidence is weak or mixed, say so explicitly and keep the instruction set conservative.

**Done when:** The user can copy the file tree and contents directly into their repo with no further editing. Every file has a justification grounded in repo evidence.

## Do this, not that

| Do this | Not that |
| --- | --- |
| Use repo code and configs as the primary evidence base | Write generic rules from memory |
| Put universal semantic rules in `copilot-instructions.md` | Put framework- or path-specific rules in the root file |
| Add a scoped file only when the scope has unique review value | Generate one file for every detected tool |
| Use short, imperative, semantic bullets | Write long prose or vague quality slogans |
| Evaluate existing instruction files before overwriting them | Start from scratch when files already exist |
| Verify glob patterns with `find` before presenting | Assume glob patterns match without testing |
| Adapt scenario and template references to the repo | Copy templates verbatim |
| Split files when they near 4,000 characters | Assume trailing content will still be read |
| Make overlapping files complementary | Rely on conflicting files and hope Copilot resolves them |
| Plan for base-branch rollout and re-review | Assume feature-branch changes affect the current PR automatically |
| Treat multi-stack repos as separate scopes | Scope by technology name without checking directory structure |
| Count characters with `wc -m` for multi-byte content | Use `wc -c` and assume bytes equal characters |

## Recovery paths

If the task starts drifting, recover in this order:
1. **Too broad or too many files** → collapse to the root file plus only the highest-signal scoped files
2. **File near 4,000 characters** → remove low-priority rules, shorten examples, or split by narrower `applyTo`
3. **Unclear scoping** → inspect representative repo files and choose the narrowest glob that still matches the intended scope
4. **Conflicting rules** → make scopes non-overlapping or rewrite the rules to be additive
5. **Weak or generic Copilot comments** → rewrite rules for specificity and remove linter-level noise
6. **Instructions seem ignored** → follow `references/troubleshooting.md` in order: location → character count → frontmatter → base branch → glob match → conflicts → specificity → incremental retest → re-review
7. **Existing files are poor quality** → evaluate against SMSA, note specific gaps, refine in place rather than discarding
8. **Multi-stack repo is confusing** → treat each stack as an independent scope; do not force cross-stack rules

## Reference routing

- **`references/setup-and-format.md`** — file locations, root vs scoped formats, character limits, review modes, configuration levels, base-branch behavior, and working with existing instruction files
- **`references/writing-instructions.md`** — rule quality (SMSA criteria with pass/fail examples), section ordering, root vs scoped content decisions, character budgets, code examples, concept overlap vs duplication, and iteration workflow
- **`references/scoping-and-targeting.md`** — `applyTo` glob syntax with framework-specific patterns, `excludeAgent`, precedence, additive overlap, monorepo layout, multi-stack repos, gap analysis, and optimal file counts
- **`references/troubleshooting.md`** — ignored instructions, scope mistakes, architecture mistakes, existing-instructions evaluation, glob verification recipes, conflict diagnosis, debugging order, verification, and non-determinism
- **`references/scenarios.md`** — full-stack examples with adaptation workflow and scenario selection guide; adapt only after the file architecture is already chosen
- **`references/micro-library.md`** — small templates with adaptation warnings and consultation triggers; adapt only after repo grounding when you need a starter pattern for a specific scope
