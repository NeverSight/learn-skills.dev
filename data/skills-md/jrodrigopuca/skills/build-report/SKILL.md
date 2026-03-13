---
name: build-report
description: Generate structured, actionable build reports from Node.js build outputs (TypeScript, ESLint, Webpack, Vite). Groups errors by pattern, prioritizes issues, and suggests documented solutions. Orchestrates three specialized sub-skills for parsing, analysis, and report generation. Supports fast path for quick builds and sampled mode for large outputs. | Genera reportes estructurados y accionables de builds Node.js (TypeScript, ESLint, Webpack, Vite). Agrupa errores por patrón, prioriza issues y sugiere soluciones documentadas. Orquesta tres sub-skills especializadas para parsing, análisis y generación de reportes.
license: MIT
metadata:
  author: jrodrigopuca
  version: "1.0"
---

# Build Report Generator

Generate structured, actionable reports from build outputs for Node.js projects.

**Version 2.0** - Refactored with sub-skill architecture for optimized context usage.

---

## Overview

Build Report transforms raw build outputs into organized, prioritized reports using a three-stage orchestration workflow:

1. **Parse** - Extract structured errors from build tool outputs
2. **Analyze** - Group by pattern, identify root causes, prioritize
3. **Generate** - Create actionable Markdown report

### Key Features

- ✅ **Multiple build tools:** TypeScript, ESLint, Webpack, Vite
- ✅ **Intelligent grouping:** By pattern, root cause, and module
- ✅ **Priority-driven:** Focus on what blocks the build first
- ✅ **Documentation links:** Points to official docs, doesn't duplicate them
- ✅ **Three workflow paths:** Fast (< 10 errors), Standard (10-100), Sampled (100+)
- ✅ **Context-optimized:** Lazy loading per step (~7.5K tokens vs 19K)

---

## Prerequisites

- Node.js project with npm/yarn/pnpm
- Build tools: TypeScript, ESLint, Webpack, Vite, or similar
- Build output (from console or CI/CD logs)

---

## Quick Start

**Typical invocation:**

```
User: "Analyze this build output and generate a report"

[User provides build output]

Orchestrator:
1. Determine workflow path (fast/standard/sampled)
2. Launch parse-build-output sub-skill
3. Launch analyze-errors sub-skill
4. Launch generate-report sub-skill
5. Present final report to user
```

---

## Workflow Orchestration

### 1. Planning Phase

**Load:** This file + `orchestration-policy.md`  
**Token budget:** ~2,000 tokens

**Assess the build output:**

```
error_count = estimate errors from output size/scan
warning_count = estimate warnings

if error_count + warning_count < 10:
  path = "fast"
elif error_count + warning_count < 100:
  path = "standard"
else:
  path = "sampled"
```

**Inform user of path selection:**

```
"Detected [N] errors in build output. Using [path] workflow for optimal analysis."
```

### 2. Execution Phase - Parse Step

**Launch:** `sub-skills/parse-build-output.md`  
**Load:** Orchestrator + parse sub-skill (~2,500 tokens)  
**Input:** Raw build output (string)  
**Output:** Parsed Errors Artifact (JSON)

**Sub-skill responsibilities:**

- Detect build tools (TypeScript, ESLint, Webpack, Vite)
- Extract structured errors with file, line, code, message
- Categorize by error type
- Handle truncation if output too large

**Wait for artifact before proceeding.**

### 3. Execution Phase - Analyze Step

**Launch:** `sub-skills/analyze-errors.md`  
**Load:** Orchestrator + analyze sub-skill + `references/error-docs-map.md` (~7,000 tokens)  
**Input:** Parsed Errors Artifact (from parse step)  
**Output:** Analyzed Errors Artifact (JSON)

**Sub-skill responsibilities:**

- Group errors by pattern/code/root cause
- Assign priorities (critical/high/medium/low)
- Identify cascading errors
- Map errors to official documentation
- Generate prioritized recommendations

**Path-specific behavior:**

- **Fast path:** Basic grouping, skip root cause analysis
- **Standard path:** Full analysis with all features
- **Sampled path:** Analyze all but detail only top 10 groups

**Wait for artifact before proceeding.**

### 4. Execution Phase - Generate Step

**Launch:** `sub-skills/generate-report.md`  
**Load:** Orchestrator + generate sub-skill + `templates/report-template.md` (~3,500 tokens)  
**Input:** Analyzed Errors Artifact (from analyze step)  
**Output:** Markdown Build Report (final deliverable)

**Sub-skill responsibilities:**

- Select appropriate report template (quick/standard/sampled)
- Populate all sections with artifact data
- Apply activation rules for optional sections
- Format with consistent style and links

**Optional sections** (see `orchestration-policy.md` for activation rules):

- Configuration Suggestions
- Code Context
- Cascading Errors Explanation

### 5. Delivery Phase

**Present final report to user.**

Offer follow-up options:

- "Want detailed analysis for a specific error group?"
- "Need help implementing the recommended fixes?"
- "Want me to check if any of these errors are auto-fixable?"

---

## Context Loading Strategy

**Core principle:** Load only what you need for the current step.

| Step      | Files Loaded                                  | Tokens  |
| --------- | --------------------------------------------- | ------- |
| Planning  | SKILL.md + orchestration-policy.md            | ~2,000  |
| Parse     | SKILL.md + parse-build-output.md              | ~2,500  |
| Analyze   | SKILL.md + analyze-errors.md + error-docs-map | ~7,000  |
| Generate  | SKILL.md + generate-report.md + template      | ~3,500  |
| **Total** | (across 3 execution steps)                    | ~13,000 |

**Compare to v1.0:** ~19,000 tokens loaded all at once.  
**Savings:** ~31% reduction in context usage.

### Files NOT Loaded During Execution

- ❌ `references/report-examples.md` (24KB) - Training examples only
- ❌ `references/nodejs-parsers.md` (19KB) - Only if custom tool detected
- ❌ `EVALUATION.md` - Analysis document, not operational

---

## Workflow Paths

### Fast Path (< 10 errors)

**Time:** 1-2 minutes  
**Output:** Quick summary report (~50-100 lines)

**Optimizations:**

- Basic error grouping (by code only)
- Skip root cause analysis
- Skip cascading error detection
- Generate summary + immediate actions only

**Use when:** User needs rapid feedback on small builds

### Standard Path (10-100 errors)

**Time:** 3-5 minutes  
**Output:** Full structured report (~200-800 lines)

**Features:**

- Complete error grouping and root cause analysis
- Cascading error detection
- Detailed recommendations
- Optional sections (config suggestions, code context)

**Use when:** Typical build failures need comprehensive analysis

### Sampled Path (100+ errors)

**Time:** 2-4 minutes (faster than standard despite more errors)  
**Output:** Sampled report (~100-300 lines)

**Optimizations:**

- Group all errors but detail only top 10
- Summary stats for remaining errors
- Focus on patterns rather than exhaustive listing
- Top 3 recommended fixes

**Use when:** Large builds with many errors need manageable insights

---

## Artifact Contracts

All artifacts follow structured schemas defined in `contracts/artifacts.md`:

1. **Parsed Errors Artifact** - Structured errors with metadata
2. **Analyzed Errors Artifact** - Grouped, prioritized, with recommendations
3. **Report Artifact** - Final Markdown report

Each sub-skill validates its input and output against these contracts.

---

## Sub-Agent Invocation Pattern

**Use the Task tool to launch sub-skills:**

```
Task(
  description: "Parse build output for [project]",
  subagent_type: "general",
  prompt: "You are a build-report sub-agent. Read the sub-skill file at build-report/sub-skills/parse-build-output.md and follow its instructions exactly.

  CONTEXT:
  - Workflow path: [fast/standard/sampled]
  - Build output: [provided by user]

  TASK:
  Parse the build output and produce a Parsed Errors Artifact according to contracts/artifacts.md.

  Return the artifact as structured JSON."
)
```

**Sequential execution:** Wait for each sub-skill to complete before launching the next.

---

## Degradation Strategy

If issues arise during execution:

| Issue                          | Action                                              |
| ------------------------------ | --------------------------------------------------- |
| Build output > 50K tokens      | Truncate to first 1000 errors, note in report       |
| Parsing fails for a tool       | Mark as "unparsed", show raw snippet                |
| Error code not in docs map     | Link to tool's main documentation                   |
| 500+ errors after parsing      | Force sampled path                                  |
| Report generation > 2000 lines | Switch to sampled mode, warn user                   |
| Unknown build tool             | Generic parse (file:line - message), note in report |

**Graceful failures:** Always produce something useful, even if not perfect.

---

## Examples

### Example 1: TypeScript Build Failed (Fast Path)

**User:** "Analyze this build output"

**Input:**

```
$ npm run build
> tsc

src/auth/login.ts:23:15 - error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
src/utils/validate.ts:12:8 - error TS2304: Cannot find name 'User'.

Found 2 errors in 2 files.
```

**Orchestrator Actions:**

1. **Planning:** Detect 2 errors → fast path
2. **Parse:** Extract 2 TypeScript errors
3. **Analyze:** Basic grouping, map to docs
4. **Generate:** Quick summary report

**Output:** Markdown report showing:

- Status: 🔴 FAILED
- 2 critical errors grouped by type
- Immediate actions (1. Add User import, 2. Fix type conversion)
- Links to TypeScript docs

### Example 2: Large Build (Sampled Path)

**User:** "Generate build report from this CI log"

**Input:** [500+ errors from multiple tools]

**Orchestrator Actions:**

1. **Planning:** Detect 500+ errors → sampled path
2. **Parse:** Extract first 200, collect stats on rest
3. **Analyze:** Group all, detail top 10 patterns
4. **Generate:** Sampled report with pattern focus

**Output:** Markdown report showing:

- Top 10 error patterns (detailed)
- Summary of remaining 40+ patterns
- Distribution by module
- Top 3 recommended fixes

---

## Resources

**Official Documentation** (primary source for solutions):

- [TypeScript Error Reference](https://www.typescriptlang.org/docs/handbook/error-reference.html)
- [ESLint Rules](https://eslint.org/docs/latest/rules/)
- [Webpack Errors](https://webpack.js.org/configuration/stats/#errors-and-warnings)
- [Vite Troubleshooting](https://vitejs.dev/guide/troubleshooting.html)

**Skill Internal References:**

- `orchestration-policy.md` - Workflow rules, activation criteria, degradation strategy
- `contracts/artifacts.md` - Structured artifact schemas
- `templates/report-template.md` - Report format and structure
- `references/error-docs-map.md` - Error code → documentation URL mapping
- `references/nodejs-parsers.md` - Advanced parsing strategies (rarely needed)
- `references/report-examples.md` - Training examples (not loaded during execution)

**Sub-Skills:**

- `sub-skills/parse-build-output.md` - Tool detection and error extraction
- `sub-skills/analyze-errors.md` - Grouping, prioritization, root cause analysis
- `sub-skills/generate-report.md` - Markdown report generation

---

## Version History

See `CHANGELOG.md` for detailed version history.

- **v2.0.0** (2024-03-09): Sub-skill architecture with context optimization
- **v1.0.0** (2024-02-10): Initial monolithic implementation

---

## Philosophy

1. **Link to docs, don't duplicate:** We point to official documentation rather than explaining solutions inline.
2. **Context-aware loading:** Load only what's needed for each step to minimize token usage.
3. **Priority-driven:** Focus on what blocks the build first.
4. **Actionable always:** Every report includes clear next steps.
5. **Graceful degradation:** Always produce something useful, even with incomplete data.

---

## When to Use This Skill

✅ **Use when:**

- Analyzing build failures with many errors
- Need to triage and prioritize fixes
- Want grouped, pattern-based insights
- CI/CD builds need human-readable reports
- Multiple build tools in output

❌ **Don't use when:**

- Single obvious error (user can see it directly)
- Need to actually fix the errors (this skill reports, doesn't fix)
- Output is not from Node.js build tools

---

## Invocation Triggers

The skill auto-loads when:

- User says "analyze this build output"
- User says "generate build report"
- User says "why did my build fail"
- User provides large multi-line output that looks like build errors

---

## Output

The final deliverable is a **Markdown Build Report** containing:

- ✅ Executive summary with impact and top issues
- ✅ Grouped errors with patterns and root causes
- ✅ Priority-sorted recommendations
- ✅ Documentation links for each error type
- ✅ Useful commands for next steps
- ⚠️ Optional: Configuration suggestions (when applicable)
- ⚠️ Optional: Code context (when helpful)
- ⚠️ Optional: Cascading error explanations (when detected)

---

## Notes for LLM

- **You are the orchestrator** - Coordinate sub-skills, don't do their work
- **Follow the path** - Fast/standard/sampled affects how sub-skills behave
- **Pass artifacts** - Each sub-skill produces JSON consumed by next
- **Apply activation rules** - Check `orchestration-policy.md` for optional sections
- **Degrade gracefully** - Partial results better than failure
- **Stay lightweight** - Load only step-specific files
