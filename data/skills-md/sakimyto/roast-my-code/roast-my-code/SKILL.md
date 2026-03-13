---
name: roast-my-code
description: "Comprehensive code review in roast style. Analyzes security, architecture, complexity, TDD compliance, type safety, error handling, naming, dead code, performance, dependencies, API design, frontend quality, and git hygiene. Delivers findings as entertaining roasts with actionable fixes. Use /roast to review your codebase. Supports --level (gentle/spicy/savage/sensei)."
user-invocable: true
argument-hint: "[target-path] [--level=gentle|spicy|savage|sensei] [--diff] [--quick] [--lang=en|ja]"
allowed-tools: Read, Glob, Grep, Bash
---

# roast-my-code

Roast the target codebase with devastating accuracy and actionable fixes.

## Usage

```
/roast                              # Review cwd at spicy level
/roast src/                         # Review src/ directory
/roast --level=savage               # Maximum roast intensity
/roast src/ --level=sensei          # TDD-focused wisdom
/roast --diff                       # Review staged changes only
/roast --quick                      # Fast scan (top 3 checkers)
/roast --lang=ja                    # Force output language
```

## Levels

| Level | Tone | Best For |
|-------|------|----------|
| gentle | Friendly mentor | Juniors, OSS contributors |
| **spicy** | Sarcastic reviewer (default) | Daily use, team reviews |
| savage | Brutally honest senior | Content, self-roasts |
| sensei | TDD master (t_wada style) | TDD adoption, testing culture |

## Instructions

Follow these steps precisely. Do NOT skip any step.

### Step 1: Parse Arguments

Parse the user's input to extract:

- `TARGET_PATH`: directory or file to review (default: current working directory)
- `LEVEL`: one of gentle/spicy/savage/sensei (default: spicy)
- `OUTPUT_LANG`: detect from the user's message language (en or ja).
  If the user wrote in Japanese, set to ja. Otherwise, set to en.
  If `--lang=` is specified, use that value instead of auto-detection.
- `DIFF_MODE`: boolean (default: false). If `--diff` is present, set to true.
- `QUICK_MODE`: boolean (default: false). If `--quick` is present, set to true.

Extract `--level=`, `--lang=`, `--diff`, `--quick` from the argument string.
Everything else is treated as the target path.

**Diff mode:** When `DIFF_MODE` is true, run `git diff --cached --name-only`
via Bash to get the list of staged files. Only analyze those files instead
of the full project. If no files are staged, inform the user and exit.
Project detection (Step 2) still runs normally to determine framework context.

**Quick mode:** When `QUICK_MODE` is true, run only these 3 checkers:
Security, Architecture, TDD. Skip all other checkers. Output includes a
note that this was a quick scan.

### Step 2: Project Detection

Analyze the target to detect the project type. Run these checks:

```
Glob: TARGET_PATH/**/package.json
Glob: TARGET_PATH/**/tsconfig.json
Glob: TARGET_PATH/**/Cargo.toml
Glob: TARGET_PATH/**/go.mod
Glob: TARGET_PATH/**/requirements.txt
Glob: TARGET_PATH/**/pyproject.toml
Glob: TARGET_PATH/**/*.sln
Glob: TARGET_PATH/.git
```

Read the **root-level** `package.json` (at `TARGET_PATH/package.json`) first.
If none exists, fall back to the nearest `package.json` to TARGET_PATH.
Extract:

- `dependencies` and `devDependencies` keys
- `scripts` keys
- `engines` field

Detect frameworks by checking dependency names:

- **HTTP frameworks:** express, hono, fastify, koa, @nestjs/core
- **Frontend frameworks:** react, vue, svelte, @angular/core, next, nuxt
- **Test frameworks:** jest, vitest, mocha, @testing-library/*
- **Language:** presence of tsconfig.json = TypeScript

Store results as:

- `LANG`: typescript | javascript | rust | go | python | csharp | unknown
- `HAS_TESTS`: boolean
- `HAS_HTTP_FRAMEWORK`: boolean
- `HAS_FRONTEND_FRAMEWORK`: boolean
- `HAS_GIT`: boolean
- `HAS_PACKAGE_MANIFEST`: boolean

### Step 3: Checker Activation

Determine which checkers to run based on detection results:

| Checker | Reference File | Condition |
|---------|---------------|-----------|
| Security | `references/security.md` | Always |
| Architecture | `references/architecture.md` | Always |
| Complexity | `references/complexity.md` | Always |
| TDD | `references/tdd.md` | Always |
| Type Safety | `references/type-safety.md` | LANG = typescript OR .ts/.tsx files found |
| Error Handling | `references/error-handling.md` | Always |
| Naming | `references/naming.md` | Always |
| Dead Code | `references/dead-code.md` | Always |
| Performance | `references/performance.md` | Always |
| Dependencies | `references/dependencies.md` | HAS_PACKAGE_MANIFEST |
| API Design | `references/api-design.md` | HAS_HTTP_FRAMEWORK |
| Frontend | `references/frontend.md` | HAS_FRONTEND_FRAMEWORK |
| Git Hygiene | `references/git-hygiene.md` | HAS_GIT |

### Step 4: Execute Checks (2-Phase)

Uses a compact index for fast detection, then reads full reference files
only for categories with findings.

#### Phase 1: Quick Scan

1. **Read** `references/checks-index.md` (single file — all 162 check
   patterns in one place).

2. **Batch Grep execution** — combine patterns per category x severity:
   - For each active checker category, combine all Grep patterns at the
     same severity level using `|` (OR) into a single Grep call.
   - Example: Security Grep [critical] has 6 patterns — combine into
     1 Grep call with patterns joined by `|`.
   - This reduces ~100+ individual Greps to ~20-30 batched calls.
   - **Presence (P)**: pattern found = potential finding. Map matched
     lines back to the specific check by inspecting which sub-pattern
     matched.
   - **Absence (A)**: run a separate Grep per absence check. Zero
     results = finding.

3. **Glob checks** — run all Glob patterns from the index in parallel.

4. **Bash checks** — run Bash commands from the index in parallel where
   independent. Group related commands together.

5. **Map results** — for each match, identify the specific check name
   from the index. Record:
   - Which categories have findings (= need Phase 2 detail)
   - Which categories are clean (= Strengths, skip in Phase 2)
   - Approximate severity distribution per category

**Phase 1 rules:**

- Skip `node_modules/`, `dist/`, `build/`, `.next/`, `vendor/`,
  `target/`, `.git/` directories.
- Sample up to 20 files per category for tractability.
- For large projects, prioritize: `src/` > `lib/` > `app/` > others.

**Phase 1 target: ~20-30 Grep + 10-15 Glob/Bash calls total.**

#### Phase 2: Detailed Roast

1. **Read** `references/roast-style.md` to load the roast persona for
   the selected LEVEL.

2. **For each category WITH findings** from Phase 1:
   a. Read the category's full reference file (e.g.,
      `references/security.md`).
   b. For each finding detected in Phase 1, extract from the reference:
      - Roast line (en and ja — select based on OUTPUT_LANG)
      - Fix description
      - Exact deduction value
   c. Refine findings: verify context around matches, discard false
      positives from batch grep, deepen analysis where needed.
   d. Record each confirmed finding with:
      - `category`: checker name
      - `check`: check item name
      - `severity`: critical / error / warning / info
      - `location`: file path and line number(s)
      - `evidence`: the actual code/pattern found
      - `deduction`: point deduction value

3. **For categories with zero findings**: do NOT read the reference
   file. Add the category to Strengths in the final output.

**Important rules:**

- Only report findings backed by actual evidence found in the code.
- Do NOT invent findings for entertainment. Every roast must be
  grounded in fact.
- **Deduplication:** If the same issue appears in multiple checkers
  (e.g., CORS in Security and API Design, Error Boundaries in Error
  Handling and Frontend), count the deduction in only ONE category —
  whichever is more specific. Note the cross-reference in the other
  category without deducting.
- Per-check cap: max **3 findings** per check type count toward the
  score. Additional instances are reported but do not deduct further.
- **Parallelism:** Run Grep and Glob calls for independent checks in
  parallel where possible. Batch tool calls to minimize round-trips.

### Step 5: Calculate Scores

For each active checker category:

1. Start at **100 points**.
2. Apply deductions for each finding:
   - `critical`: **-20** points
   - `error`: **-10** points
   - `warning`: **-4** points
   - `info`: **-1** point
3. **Per-check cap:** Max **3 findings** per check type count toward the
   score. Additional instances are reported but do not deduct further points.
4. Floor at **0** (no negative scores).
5. The category score displayed in the table is always out of **100**
   (do NOT multiply by weight here).

Calculate the **Overall Score** using category weights:

- Weights: Security **1.5x**, Architecture **1.2x**,
  TDD **1.5x** in sensei mode (1.0x otherwise), all others **1.0x**.
- `overall = sum(score_i * weight_i) / sum(weight_i)`
- Weights are used ONLY in this overall calculation, not on individual
  category scores.

Determine the **Grade**:

| Grade | Score Range | Label |
|-------|-----------|-------|
| S | 90 - 100 | Immaculate |
| A | 80 - 89 | Solid |
| B | 70 - 79 | Decent |
| C | 60 - 69 | Needs Work |
| D | 40 - 59 | Rough |
| F | 0 - 39 | Dumpster Fire |

### Step 6: Generate Output

Compose the final output using the Output Format below.
Apply the roast persona from roast-style.md for the selected LEVEL.

**Rules:**

- Every finding gets a roast line AND a concrete fix.
- Group findings by category.
- Show the most critical findings first within each category.
- Keep total output under 300 lines. If more findings exist, show top 5 per
  category and note how many were omitted.
- Lines should be under 80 characters where possible for screenshot-friendliness.
- **Language:** If `OUTPUT_LANG` is ja, write all roast lines, fix descriptions,
  summary text, and section labels in Japanese. Category names in the scorecard
  table and structural elements (box-drawing, header) remain in English.
  If `OUTPUT_LANG` is en, write everything in English.

---

## Output Format

Generate output following this structure (adapt rows to active checkers):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔥 ROAST MY CODE — REPORT CARD 🔥
  Level: {LEVEL} | Target: {TARGET_PATH}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 OVERALL: {GRADE} ({SCORE}/100)

┌─────────────────────────────────────┐
│ Category          Score    Grade    │
├─────────────────────────────────────┤
│ Security          {xx}/100   {G}   │
│ Architecture      {xx}/100   {G}   │
│ Complexity        {xx}/100   {G}   │
│ TDD               {xx}/100   {G}   │
│ Type Safety       {xx}/100   {G}   │
│ Error Handling    {xx}/100   {G}   │
│ Naming            {xx}/100   {G}   │
│ Dead Code         {xx}/100   {G}   │
│ Performance       {xx}/100   {G}   │
│ Dependencies      {xx}/100   {G}   │
│ API Design        {xx}/100   {G}   │
│ Frontend          {xx}/100   {G}   │
│ Git Hygiene       {xx}/100   {G}   │
└─────────────────────────────────────┘
(Only show rows for active checkers)

━━━ 🔥 FINDINGS ━━━━━━━━━━━━━━━━━━━━━━

## {CATEGORY} ({SCORE}/100)

### 🚨 {CHECK_NAME} [{SEVERITY}]
📍 {file_path}:{line}
> {code evidence or description}

💬 "{ROAST_LINE}"

🔧 Fix: {actionable fix description}

---

(Repeat for each finding, grouped by category)

━━━ 📋 SUMMARY ━━━━━━━━━━━━━━━━━━━━━━━

🏆 Top 3 Strengths:
  1. {strength}
  2. {strength}
  3. {strength}

💀 Top 3 Priorities to Fix:
  1. {priority with file reference}
  2. {priority with file reference}
  3. {priority with file reference}

📈 Quick Wins (< 5 min each):
  - {quick fix 1}
  - {quick fix 2}
  - {quick fix 3}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Roasted with ❤️ by roast-my-code
  ⭐ github.com/sakimyto/roast-my-code
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Output Rules

1. **Scorecard table** always appears first.
2. **Findings** are grouped by category, ordered by score
   (worst category first).
3. Within each category, findings are ordered: critical > error >
   warning > info.
4. **Summary** always appears last.
5. If a category scored 100 (no findings), show it in the table
   but skip the findings section for it. Add it to Strengths.
6. The roast line MUST match the selected LEVEL's tone from
   roast-style.md.
7. Every roast MUST be paired with a Fix.
8. Use box-drawing characters for the table exactly as shown.
9. If the overall grade is S, add a congratulatory roast:
   "I came here to roast, but your code left me speechless.
   Well played."

---

## Scoring Quick Reference

| Severity | Deduction | Examples |
|----------|-----------|---------|
| critical | -20 | Hardcoded secrets, SQL injection, no tests |
| error | -10 | Empty catch, God files, `any` abuse |
| warning | -4 | console.log, TODO comments, inline styles |
| info | -1 | Missing engine field, no readonly |

| Weight | Category | Multiplier | Note |
|--------|----------|-----------|------|
| High | Security | 1.5x | Always |
| Medium | Architecture | 1.2x | Always |
| Elevated | TDD | 1.5x | sensei mode only (1.0x otherwise) |
| Normal | All others | 1.0x | |

**Note:** Weights apply ONLY to the overall weighted average, not to
individual category scores (which are always displayed out of 100).
Per-check cap: max 3 findings per check type count toward the score.

| Grade | Range | Vibe |
|-------|-------|------|
| S | 90-100 | Ship it yesterday |
| A | 80-89 | Production-ready |
| B | 70-79 | Code review approved |
| C | 60-69 | Needs another pass |
| D | 40-59 | Intern's first week? |
| F | 0-39 | Call the fire department |
