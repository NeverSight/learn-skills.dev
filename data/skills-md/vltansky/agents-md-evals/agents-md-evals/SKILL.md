---
name: agents-md-evals
description: Evaluate and optimize AGENTS.md/CLAUDE.md instruction files through A/B testing. Use when the user says "eval my agents.md", "test my claude.md", "optimize my instructions", "which rules matter", "trim my agents file", or wants to know which instructions in their global config actually change model behavior vs. are dead weight.
---

# AGENTS.md / CLAUDE.md Evaluator

Evaluate whether rules in instruction files actually change model behavior, identify non-discriminating rules (model already does this by default), and optimize the file for maximum impact per token.

## Core Concept

Most AGENTS.md/CLAUDE.md files contain rules the model already follows without being told. These waste context tokens every conversation. This skill runs controlled A/B tests — with the instruction file vs. without it — to identify which rules earn their place and which can be cut.

### The Codebase-Teaches-Patterns Effect

Well-structured codebases make most instruction rules redundant. The model explores existing code — reads `package.json`, scans existing components, follows import patterns — and matches conventions automatically. In empirical testing on a 755-line CLAUDE.md across a monorepo with 3 frontend stacks, **25 of 26 assertions passed identically** with or without the instruction file. The model discovered React patterns, shadcn/ui conventions, Recharts usage, Hebrew labels, Firestore helpers, Zod validation, and serverTimestamp — all from existing code.

The only assertion that discriminated was pure domain knowledge the codebase couldn't teach: parallel components in separate directories that must always be changed together.

This means your CLAUDE.md is probably 80-95% redundant. The eval process will reveal exactly which rules survive.

## The Evaluation Loop

1. **Read the instruction file** and categorize each rule
2. **Generate eval prompts** from commit analysis (not guessing)
3. **Run clean A/B tests** with proper file isolation
4. **Grade and benchmark** the results
5. **Identify non-discriminating rules** and recommend cuts
6. **Iterate** until the file is lean and every rule pulls its weight

---

## Step 1: Read and Categorize Rules

Read ALL instruction files in scope. For project-level evals, find every instruction file recursively:

```bash
find {project-root} -name "CLAUDE.md" -o -name "AGENTS.md" | grep -v node_modules | grep -v .git
```

For global evals, check all config directories:
```bash
ls -la ~/.claude/CLAUDE.md ~/.codex/AGENTS.md ~/.cursor/AGENTS.md 2>/dev/null
```

Categorize each rule:

| Category | Examples | Likely discriminating? |
|----------|---------|----------------------|
| **Coding style** | `type` over `interface`, early returns, no `React.FC` | Low — models default to modern patterns |
| **Response format** | Checklist style, tldr footer, separators | Low-Medium — some are model defaults |
| **Workflow** | TDD, validation steps, branch naming | High — models don't do these unprompted |
| **Decision style** | Single recommendation, epistemic separation | High — models default to option menus |
| **Safety guardrails** | No force-push, no rm -rf, no dev server | Can't A/B test safely — keep by default |
| **Identity/preferences** | Author name, email, no emojis | Keep — low cost, high consequence if wrong |
| **Domain-specific** | Parallel component parity, project-specific helpers | Keep — can't be known without instruction |

Rules in the last three categories should be kept regardless of eval results. Focus eval effort on coding style, response format, workflow, and decision style.

---

## Step 2: Generate Eval Prompts

### Commit-Derived Evals (Preferred)

The most effective eval prompts come from analyzing real project history. Generic prompts ("write a React component") test patterns the model discovers from the codebase anyway.

Spawn a subagent to analyze recent commits:

```
Analyze the last 50-100 commits in {project-root} using git log.
Look for:
1. Patterns that appear in commits but aren't obvious from code structure alone
2. Mistakes that were fixed (these reveal non-obvious conventions)
3. Multi-file changes that suggest coupling rules
4. Domain-specific patterns (naming, helpers, config)

For each pattern, write a realistic eval prompt that would test whether
the model knows about it WITHOUT being told. Save to {workspace}/evals/commit-analysis.md
```

### Designing Good Assertions

Each eval needs 3-6 assertions. Mix automated (grep-able) and manual:

- **Automated**: `"check": "companyCollection"` — regex against output
- **Manual**: "Mentions or checks the parallel component" — requires reading context

A discriminating assertion:
1. **Passes** when the instruction file is loaded
2. **Fails** when the instruction file is absent
3. Cannot be explained by the codebase alone

If an assertion passes in both conditions, the rule it tests is dead weight.

Save prompts to `{workspace}/evals/evals.json`. Present to the user before running.

---

## Step 3: Run Clean A/B Tests

**This is the most error-prone step.** Claude Code auto-loads CLAUDE.md/AGENTS.md into every conversation, including subagents. A contaminated baseline produces false results — you'll think rules are "non-discriminating" when really both runs had them.

### Clean Baseline Protocol

This protocol was refined through 3 failed attempts. Follow it exactly.

**Phase 1: Discover all instruction and memory files**

```bash
# Find ALL instruction files in the project (monorepos have them in packages)
find {project-root} -name "CLAUDE.md" -o -name "AGENTS.md" \
  | grep -v node_modules | grep -v .git | sort
```

Also check user-level config and memory files — these are auto-loaded too:
```bash
ls -la ~/.claude/CLAUDE.md ~/.codex/AGENTS.md ~/.cursor/AGENTS.md 2>/dev/null
ls -d ~/.claude/projects/*/memory/ 2>/dev/null
```

**Phase 2: Move ALL files to /tmp/ (not rename, not .bak)**

Renaming to `.bak` in the same directory is weak — the model might still discover it. Move to `/tmp/` with directory structure preserved. Include memory files — there is no CLI flag to disable memory loading.

```bash
BACKUP_DIR="/tmp/{project-name}-md-backup-$(date +%s)"
mkdir -p "$BACKUP_DIR"

# For each instruction file found in Phase 1:
for f in {list of files}; do
  REL_PATH="${f#{project-root}/}"
  mkdir -p "$BACKUP_DIR/$(dirname $REL_PATH)"
  mv "$f" "$BACKUP_DIR/$REL_PATH"
done

# User-level files: ASK before touching. These are outside the project.
# "I found global instruction files and memory dirs that will contaminate baselines.
#  OK to temporarily rename them? I'll restore immediately after."
# Only proceed with explicit user consent:
for f in ~/.claude/CLAUDE.md ~/.codex/AGENTS.md ~/.cursor/AGENTS.md; do
  [ -f "$f" ] && mv "$f" "${f}.bak"
done
find ~/.claude/projects -type d -name "memory" -exec sh -c 'mv "$1" "${1}_bak"' _ {} \; 2>/dev/null
# If the user declines, note that baselines may be partially contaminated by global rules.
```

**Phase 3: Verify removal**

```bash
# Must return zero results:
find {project-root} -name "CLAUDE.md" -o -name "AGENTS.md" \
  | grep -v node_modules | grep -v .git | wc -l
```

If ANY files remain, do not proceed.

**Phase 4: Spawn all clean baseline agents**

Launch all baseline agents NOW. They start in a world with zero instruction files.

**Phase 5: WAIT for ALL baseline agents to complete**

DO NOT restore files until every single baseline agent has finished and you have saved its timing data. This is critical — restoring early creates a race condition where agents that haven't fully initialized yet may pick up the restored files.

**Phase 6: Restore all files (ALWAYS — even if baselines errored)**

Restoration is non-negotiable. If agents fail, time out, or you hit any error — restore FIRST, debug second. Leaving user config renamed breaks all future Claude sessions.

```bash
# Only after ALL baselines are done (or failed):
for f in $(find "$BACKUP_DIR" -type f); do
  REL_PATH="${f#$BACKUP_DIR/}"
  mv "$f" "{project-root}/$REL_PATH"
done

# Restore user-level files (if they were renamed with user consent):
for f in ~/.claude/CLAUDE.md.bak ~/.codex/AGENTS.md.bak ~/.cursor/AGENTS.md.bak; do
  [ -f "$f" ] && mv "$f" "${f%.bak}"
done

# Restore memory dirs:
find ~/.claude/projects -type d -name "memory_bak" -exec sh -c 'mv "$1" "${1%_bak}"' _ {} \; 2>/dev/null
```

**Phase 7: Git checkout**

Baseline agents may have modified project files during their runs:
```bash
cd {project-root} && git checkout .
```

### With-Skill Runs

For with-skill runs, all instruction files are on disk (auto-loaded). Additionally have the agent read the root file explicitly:

```
You are being evaluated. Read the file {path-to-instruction-file} first,
then follow ALL instructions in it exactly.

Your task: {eval prompt}

Save outputs to {workspace}/iteration-{N}/{eval-name}/with_skill/outputs/
```

### Spawning Strategy

Launch ALL runs — all with-skill and all clean-baseline agents — but in two batches:

1. **Batch 1**: All clean baselines (files are moved to /tmp/)
2. Wait for all baselines to complete, restore files, git checkout
3. **Batch 2**: All with-skill runs (files are back on disk)

Within each batch, launch all agents in a single turn for parallelism.

Each agent should save:
- Output files to `outputs/`
- Full response text to `outputs/response.md`

Capture `total_tokens` and `duration_ms` from each task notification into `timing.json`.

---

## Step 4: Grade and Benchmark

After all runs complete:

### Grade Each Run

For each output, evaluate assertions. Prefer scripted checks over eyeballing:

```bash
# Automated assertion check example
grep -cP 'companyCollection' outputs/response.md
```

Save results to `grading.json` in each run directory. The eval viewer expects this exact schema:

```json
{
  "eval_id": 6,
  "eval_name": "descriptive-name",
  "config": "with_skill",
  "expectations": [
    { "text": "Assertion description", "passed": true, "evidence": "How you verified" }
  ]
}
```

The `expectations` array MUST use fields `text`, `passed`, and `evidence` — not `name`/`met`/`details`.

### Build the Benchmark

Create `benchmark.json`. The eval viewer expects this exact schema:

```json
{
  "metadata": { "skill_name": "agents-md", ... },
  "runs": [
    {
      "eval_id": 6,
      "eval_name": "descriptive-name",
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.833,
        "passed": 5,
        "failed": 1,
        "total": 6,
        "time_seconds": 162.5,
        "tokens": 76318,
        "tool_calls": 0,
        "errors": 0
      },
      "expectations": [
        { "text": "...", "passed": true, "evidence": "..." }
      ]
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": { "mean": 0.793, "stddev": 0.124, "min": 0.667, "max": 1.0 },
      "time_seconds": { "mean": 169.5, "stddev": 31.5, ... },
      "tokens": { "mean": 69800, "stddev": 12502, ... }
    },
    "without_skill": { ... },
    "delta": { "pass_rate": "+0.067", "time_seconds": "-13.9", "tokens": "+13460" }
  }
}
```

**Critical**: `configuration` must be `"with_skill"` or `"without_skill"` — the viewer keys on these exact strings. Put each with_skill entry before its without_skill counterpart.

Aggregate with the bundled script:
```bash
python {this-skill-path}/scripts/aggregate_benchmark.py {workspace}/iteration-N --skill-name agents-md
```

### Key Metrics

For each assertion, classify it:

- **Non-discriminating**: Passes in BOTH configs (rule is dead weight — the codebase teaches it)
- **Discriminating**: Passes with-skill only (rule earns its place)
- **Inversely discriminating**: Fails with-skill, passes baseline (rule may be hurting)
- **Always failing**: Fails in both (rule isn't followed, or assertion is wrong)

---

## Step 5: Analyze and Recommend

### Expect Most Rules to be Non-Discriminating

Due to the codebase-teaches-patterns effect, most project-specific rules will be non-discriminating. The model reads existing files and matches conventions. This is the expected result, not a test failure. Common non-discriminating patterns:

- Tech stack choices (React vs Angular) — model reads `package.json`
- Library preferences (Recharts, shadcn/ui) — model reads existing imports
- Helper functions (companyCollection, serverTimestamp) — model reads existing code
- Language/locale (Hebrew, RTL) — model reads existing translations
- Path aliases, naming conventions — model reads `tsconfig.json` and existing files

### What Actually Discriminates

Rules that discriminate tend to be:
- **Coupling knowledge**: "When you change X, also change Y" (parallel component parity)
- **Non-obvious workflow**: "Run this specific validation before finishing"
- **Decision style**: Single recommendation vs. option menus
- **Epistemic style**: Separate known/inferred/uncertain
- **Non-standard patterns**: Internal packages wrapping public APIs, generated code, unconventional directory meanings — things that look standard but aren't

### The Keep Test

For each surviving rule, apply this filter — it must pass at least ONE criterion:

| Criterion | Question |
|-----------|----------|
| **Specificity** | Does it describe a project-unique decision? |
| **Behavior change** | Would the agent do something different without it? |
| **Surprise** | Would it surprise a competent dev joining the project? |
| **Pain** | Did it come from a real mistake or recurring PR feedback? |
| **Frequency** | Does it apply to nearly every task AND cost few tokens? |
| **No feedback loop** | Can't be enforced by tests, types, linters, or CI? |

If a rule fails all six AND is non-discriminating in A/B tests, it's dead weight.

### Safety/Identity/Domain Rules: Keep Regardless

Don't delete based on A/B tests:
- Safety guardrails (too dangerous to test without)
- Identity/preferences (too cheap to worry about — author name, email)
- Domain context the codebase structure can't teach

### Token Budget Analysis

Calculate: how many tokens does the instruction file add per conversation vs. behavioral improvement? A 755-line file that produces +3.8% improvement is a poor trade. A 50-line file with the same improvement is excellent.

### After Trimming: Restructure for Progressive Disclosure

Once you know which rules survive, restructure the file:
- **Root AGENTS.md should be a compact map** (<100 lines) — pointers to deeper docs, not a monolith
- **Extract domain content to `docs/`** — detailed conventions, architecture notes, testing patterns
- **Use nested AGENTS.md for scoped rules** — `packages/api/AGENTS.md` for API-only conventions
- **Delete slop** — identity prompts ("you are an expert"), vague advice ("follow best practices"), things agents already know ("use meaningful names"), empty sections
- **Prefer feedback loops over prose** — a lint rule or CI check is more reliable than an AGENTS.md bullet

---

## Step 6: Launch the Viewer

```bash
python {this-skill-path}/eval-viewer/generate_review.py \
  {workspace}/iteration-N \
  --skill-name "agents-md" \
  --benchmark {workspace}/iteration-N/benchmark.json \
  --static /tmp/agents-md-eval-review.html
```

### Fix Viewer Labels

The viewer defaults to "with skill"/"without skill" labels. For agents.md evals, post-process the HTML to show "with agents.md"/"without agents.md":

```python
html = open("/tmp/agents-md-eval-review.html").read()

LABEL_MAP = '{"with_skill": "with agents.md", "without_skill": "without agents.md"}[config] || config.replace(/_/g, " ");'

html = html.replace(
    'badge.textContent = config.replace(/_/g, " ");',
    'badge.textContent = ' + LABEL_MAP
)

# Also fix benchmark table labels (labelA, labelB, configLabel)
for var in ['labelA', 'labelB', 'configLabel']:
    orig = f'const {var} = config'
    if var == 'labelA':
        orig = 'const labelA = configA.replace(/_/g, " ").replace(/\\b\\w/g, c => c.toUpperCase());'
        repl = 'const labelA = configA === "with_skill" ? "With agents.md" : configA === "without_skill" ? "Without agents.md" : configA.replace(/_/g, " ").replace(/\\b\\w/g, c => c.toUpperCase());'
        html = html.replace(orig, repl)
    elif var == 'labelB':
        orig = 'const labelB = configB.replace(/_/g, " ").replace(/\\b\\w/g, c => c.toUpperCase());'
        repl = 'const labelB = configB === "with_skill" ? "With agents.md" : configB === "without_skill" ? "Without agents.md" : configB.replace(/_/g, " ").replace(/\\b\\w/g, c => c.toUpperCase());'
        html = html.replace(orig, repl)
    elif var == 'configLabel':
        orig = 'const configLabel = config.replace(/_/g, " ").replace(/\\b\\w/g, c => c.toUpperCase());'
        repl = 'const configLabel = config === "with_skill" ? "With agents.md" : config === "without_skill" ? "Without agents.md" : config.replace(/_/g, " ").replace(/\\b\\w/g, c => c.toUpperCase());'
        html = html.replace(orig, repl)

open("/tmp/agents-md-eval-review.html", "w").write(html)
```

For iteration 2+, pass `--previous-workspace` to show diffs.

---

## Step 7: Apply Changes and Re-test

After the user reviews:

1. **Delete non-discriminating rules** from the instruction file
2. **Strengthen discriminating rules** (add "why", make more concise)
3. **Re-run evals** into `iteration-{N+1}/` to verify:
   - Discriminating rules still pass
   - No regressions from deletions
   - Token count is lower

Keep iterating until:
- Every remaining rule is discriminating or untestable-but-necessary
- The user is satisfied with the file
- Pass rate is stable

---

## Workspace Layout

```
{workspace}/
├── evals/
│   ├── evals.json          (initial eval prompts)
│   ├── evals-v2.json       (commit-derived prompts)
│   └── commit-analysis.md  (git log findings)
├── iteration-1/
│   ├── {eval-name}/
│   │   ├── eval_metadata.json
│   │   ├── with_skill/
│   │   │   ├── outputs/
│   │   │   ├── timing.json
│   │   │   └── grading.json
│   │   └── clean_baseline/
│   │       ├── outputs/
│   │       ├── timing.json
│   │       └── grading.json
│   ├── benchmark.json
│   └── benchmark.md
├── iteration-2/
│   └── ...
└── evals.json
```

---

## Common Pitfalls (from real eval sessions)

1. **Contaminated baselines**: The #1 failure mode. Claude Code auto-loads CLAUDE.md for ALL conversations including subagents. Simply telling an agent "don't read CLAUDE.md" does nothing — the file must be physically absent.

2. **Restoring files too early**: Spawning agents then immediately restoring creates a race condition. Wait for ALL agents to finish.

3. **Missing nested instruction files**: Monorepos have package-level CLAUDE.md files (e.g., `packages/functions/CLAUDE.md`). Move ALL of them, not just the root one.

4. **Generic eval prompts**: "Write a React component" tests patterns the model discovers from `package.json` anyway. Use commit-derived prompts that target non-obvious domain knowledge.

5. **Wrong benchmark schema**: The eval viewer expects a specific JSON structure with `runs[]` array and `run_summary` with `mean`/`stddev`. Custom schemas produce empty viewers.

6. **Expecting high deltas**: Due to the codebase-teaches-patterns effect, +3-10% is a realistic delta for a well-structured codebase. +30%+ deltas suggest contaminated baselines.

---

## References

All bundled within this skill — no external dependencies:

- **Eval viewer**: `eval-viewer/generate_review.py` — generates the HTML review viewer
- **Aggregation**: `scripts/aggregate_benchmark.py` — aggregates grading into benchmark.json
- **Grader agent**: `agents/grader.md` — prompt for grading subagent
- **Analyzer agent**: `agents/analyzer.md` — prompt for analysis subagent
- **Schemas**: `references/schemas.md` — JSON schemas for evals, grading, benchmark
- **Eval categories**: `references/eval-categories.md` — rule categories, empirical findings, commit-derived eval guide
