---
name: codebase-readiness
description: This skill should be used to run an Agent-Ready Codebase Assessment — scoring a codebase across 8 dimensions, producing a weighted score (0-100), band rating, and improvement roadmap. Run the four assessment passes in parallel when the runtime supports subagents, and sequentially in the current agent otherwise. Supports Ruby, Python, PHP, TypeScript, JavaScript, Go, Java, Scala, and Rust.
---

# Codebase Readiness Assessment

Run an **Agent-Ready Codebase Assessment** — a scored evaluation of how well a codebase supports autonomous AI agent work, framed against the Stripe benchmark of 1,000+ AI-generated pull requests per week.

Work through the following phases sequentially.

---

## Phase 1: Codebase Reconnaissance

Execute the reconnaissance script to gather project metadata before the assessment passes. Run it directly in the current agent.

```bash
bash scripts/recon.sh
```

The script is located at `scripts/recon.sh` relative to this skill's directory.

After reviewing the output, format a **Codebase Snapshot**:

```
## Codebase Snapshot: [Project Name]

- **Primary language/framework**: [detected]
- **Language tier**: [statically-typed | dynamically-typed | gradually-typed]
  - Statically-typed: TypeScript, Go, Java, Scala, Rust, C#, Kotlin
  - Dynamically-typed: Ruby, Python (unannotated), JavaScript/Node.js, PHP
  - Gradually-typed: Python with mypy/Pydantic, TypeScript with strict:false
- **Commit count**: [X]
- **Contributors**: [X]
- **Source files**: [X]
- **Test files**: [X] (ratio: X%)
- **CI/CD**: [platform(s) found or none]
- **Agent instructions**: [AGENTS.md / CLAUDE.md / both, with canonical path and symlink status / absent]
- **Domain context**: [CONTEXT.md / CONTEXT-MAP.md / docs/DOMAIN.md / absent; ADR location and count]
- **Linting config**: [tools found or none]
- **Quality gates**: [copy the `Suggested Gate Maturity Level: Lx -- ...` line from recon output, e.g. "L0 -- no complexity, duplication, or dead-code tooling detected"]
- **README**: [present, X lines / absent]
```

**The `Quality gates` line is required.** `recon.sh` ends its `=== QUALITY GATES ===` section with `Suggested Gate Maturity Level: Lx -- <reason>`. Copy that level and reason onto the snapshot's `Quality gates` line. Then read `references/quality-gates.md` and check the suggestion against the detailed evidence above it (L0 none, L1 report-only, L2 threshold, L3 regression-aware blocking, L4 governed); change the line only when the evidence contradicts the heuristic, and say why. Do not start the assessment passes with a snapshot that lacks this line -- each pass scores only its own slice of the gate evidence and reads the level from the snapshot; if it is missing, each pass re-derives it independently and the four dimensions drift apart.

Determine `PRIMARY_LANGUAGE` and `LANGUAGE_TIER` from the snapshot. These values drive which language reference file to load.

**Supported languages:** ruby, python, php, typescript, javascript, go, java, scala, rust.

If the primary language is not in the supported list, inform the user which languages are supported. Offer to proceed with the closest supported language file if the user agrees, or assess dimensions generically without language-specific criteria.

---

## Phase 2: Run 4 Assessment Passes

### Prompt Composition

Each pass receives a composed prompt built from reference files:

1. **Read the language file** — `references/languages/{PRIMARY_LANGUAGE}.md`
2. **Read the dimension files** — each pass gets its relevant dimension files from `references/dimensions/`
3. **Read the shared gate reference** — `references/quality-gates.md` goes to the Test & CI, Code Quality, and Architecture passes (each scores a distinct slice; the credit-ownership table prevents double counting)
4. **Compose the prompt** — role preamble + codebase snapshot + dimension content + quality-gates content + language content + output instructions

Load each reference file, then include the content inline in the pass prompts. When including the language file, instruct each pass to reference only the sections relevant to its assigned dimensions.

### How to run the passes

Run all four passes below. Prefer concurrent execution when the runtime can do it, and fall back to one pass at a time in the current agent when it cannot. Do not skip a pass because parallelism is unavailable, and do not require a vendor-specific tool.

- **Parallel, when supported.** Launch all four passes together and wait until every pass has returned before Phase 3. On Claude Code, send one message with four Agent tool calls (`subagent_type: general-purpose`). On Cursor, Codex, and other agents, use that runtime's subagent or parallel-task mechanism.
- **Sequential fallback.** When the runtime has no subagent or parallel-task support, run the four passes one after another in the current agent. Finish one pass, keep its scored result, then start the next.

Each pass receives the same composed prompt either way.

### Pass Prompts

---

**Pass 1: Test & CI**

Dimension files to read and include:
- `references/dimensions/test-foundation.md`
- `references/dimensions/feedback-loops.md`
- `references/quality-gates.md` (Feedback Loops slice only: actionability, reproducibility, gate tests)

Prompt:
```
You are a senior engineering consultant specializing in test infrastructure and developer feedback loops. Assess how well this codebase's testing and CI/CD setup supports autonomous AI agent work.

Codebase Snapshot:

[INSERT FULL CODEBASE SNAPSHOT]

LANGUAGE_TIER: [static | dynamic | gradual]
PRIMARY_LANGUAGE: [Ruby | Python | TypeScript | Go | etc.]

## Assessment Instructions

Use the dimension guides and language-specific criteria below to assess two dimensions: **Test Foundation** and **Feedback Loops**. Run the evidence-gathering commands from both the dimension guides and the language file to collect data. Score each dimension 0-100 following the scoring bands, then apply any score modifiers.

Reference only the Test Foundation and Feedback Loops sections from the language file.

### Dimension Guide: Test Foundation

[INSERT CONTENT OF references/dimensions/test-foundation.md]

### Dimension Guide: Feedback Loops

[INSERT CONTENT OF references/dimensions/feedback-loops.md]

### Shared Reference: Regression-Aware Quality Gates

Use the Gate Maturity Level from the snapshot. Score only the Feedback Loops slice from the credit-ownership table (actionability, reproducibility, gate tests). Do not credit tool coverage or blocking behaviour here.

[INSERT CONTENT OF references/quality-gates.md]

### Language-Specific Criteria

[INSERT CONTENT OF references/languages/{PRIMARY_LANGUAGE}.md]

Return the full scored assessment for both dimensions in the output format specified in each dimension guide. Be specific — reference actual files, counts, and statistics.
```

---

**Pass 2: Documentation**

Dimension files to read and include:
- `references/dimensions/documentation.md`

Prompt:
```
You are a senior engineering consultant specializing in developer experience and knowledge management. Assess how well this codebase's documentation enables AI agents to work autonomously without constant human clarification.

Codebase Snapshot:

[INSERT FULL CODEBASE SNAPSHOT]

LANGUAGE_TIER: [static | dynamic | gradual]
PRIMARY_LANGUAGE: [Ruby | Python | TypeScript | Go | etc.]

## Assessment Instructions

Use the dimension guide and language-specific criteria below to assess one dimension: **Documentation & Context**. Run the evidence-gathering commands to collect data. Score 0-100 following the scoring bands.

Reference only the Documentation sections from the language file.

### Dimension Guide: Documentation & Context

[INSERT CONTENT OF references/dimensions/documentation.md]

### Language-Specific Criteria

[INSERT CONTENT OF references/languages/{PRIMARY_LANGUAGE}.md]

Return the full scored assessment in the output format specified in the dimension guide. Be specific — reference actual files found. Treat the project's canonical agent instruction entrypoint as primary: AGENTS.md when CLAUDE.md is its symlink, otherwise the existing root instruction file. Assess conflicting duplicate files as a coherence risk.
```

---

**Pass 3: Code Quality**

Dimension files to read and include:
- `references/dimensions/code-clarity.md`
- `references/dimensions/consistency.md`
- `references/quality-gates.md` (Code Clarity slice: structural coverage; Consistency slice: lint-debt treatment)

Prompt:
```
You are a senior engineering consultant specializing in code quality and developer tooling. Assess how navigable and consistent this codebase is for AI agents — agents perform better in codebases with small, focused files and enforced conventions.

Codebase Snapshot:

[INSERT FULL CODEBASE SNAPSHOT]

LANGUAGE_TIER: [static | dynamic | gradual]
PRIMARY_LANGUAGE: [Ruby | Python | TypeScript | Go | etc.]

## Assessment Instructions

Use the dimension guides and language-specific criteria below to assess two dimensions: **Code Clarity** and **Consistency & Conventions**. Run the evidence-gathering commands from both the dimension guides and the language file to collect data. Score each dimension 0-100 following the scoring bands.

Reference only the Code Clarity and Consistency sections from the language file.

### Dimension Guide: Code Clarity

[INSERT CONTENT OF references/dimensions/code-clarity.md]

### Dimension Guide: Consistency & Conventions

[INSERT CONTENT OF references/dimensions/consistency.md]

### Shared Reference: Regression-Aware Quality Gates

Use the Gate Maturity Level from the snapshot. Code Clarity credits which structural properties (complexity, duplication, dead code) are covered and whether each is blocked at L3+. Consistency credits lint/format enforcement and how lint legacy debt is treated. Do not credit CI ergonomics or baseline governance in either dimension.

[INSERT CONTENT OF references/quality-gates.md]

### Language-Specific Criteria

[INSERT CONTENT OF references/languages/{PRIMARY_LANGUAGE}.md]

Return the full scored assessment for both dimensions in the output format specified in each dimension guide. Be specific — reference actual files and line counts.
```

---

**Pass 4: Architecture**

Dimension files to read and include:
- `references/dimensions/type-safety.md`
- `references/dimensions/architecture-clarity.md`
- `references/dimensions/change-safety.md`
- `references/quality-gates.md` (Change Safety slice only: blocking semantics and baseline governance)

Prompt:
```
You are a senior engineering consultant specializing in software architecture and developer safety systems. Assess how safely and predictably AI agents can modify this codebase — guard rails vary by language: type systems for statically-typed languages, contract/test systems for dynamically-typed ones.

Codebase Snapshot:

[INSERT FULL CODEBASE SNAPSHOT]

LANGUAGE_TIER: [static | dynamic | gradual]
PRIMARY_LANGUAGE: [Ruby | Python | TypeScript | Go | etc.]

## Assessment Instructions

Use the dimension guides and language-specific criteria below to assess three dimensions: **Type Safety**, **Architecture Clarity**, and **Change Safety**. Run the evidence-gathering commands from both the dimension guides and the language file to collect data. Score each dimension 0-100 following the scoring bands, then apply any score modifiers. Apply the language-appropriate Type Safety rubric based on LANGUAGE_TIER.

Reference only the Type Safety, Architecture, and Change Safety sections from the language file.

### Dimension Guide: Type Safety

[INSERT CONTENT OF references/dimensions/type-safety.md]

### Dimension Guide: Architecture Clarity

[INSERT CONTENT OF references/dimensions/architecture-clarity.md]

### Dimension Guide: Change Safety

[INSERT CONTENT OF references/dimensions/change-safety.md]

### Shared Reference: Regression-Aware Quality Gates

Use the Gate Maturity Level from the snapshot. Score only the Change Safety slice: whether CI blocks new or worsened structural debt (L3+) and how the baseline is governed. Do not credit tool selection or CI ergonomics here.

[INSERT CONTENT OF references/quality-gates.md]

### Language-Specific Criteria

[INSERT CONTENT OF references/languages/{PRIMARY_LANGUAGE}.md]

Return the full scored assessment for all three dimensions in the output format specified in each dimension guide. Be specific — reference actual files, line counts, and git statistics.
```

---

Wait until all four passes have returned before proceeding. A sequential run already satisfies this once the fourth pass is done.

---

## Phase 3: Score Calculation

Weights are **language-adaptive**. Select the appropriate table based on `LANGUAGE_TIER` from the Codebase Snapshot.

### Dynamically-typed languages (Ruby, Python, JavaScript, PHP)

In dynamic languages, tests are the type system. Test Foundation carries more weight; Type Safety reflects contracts and interface clarity, not a type checker.

| Dimension                 | Weight | Agent Score | Weighted |
|---------------------------|--------|-------------|----------|
| Test Foundation           | 25%    | XX/100      | XX       |
| Documentation & Context   | 15%    | XX/100      | XX       |
| Code Clarity              | 15%    | XX/100      | XX       |
| Architecture Clarity      | 15%    | XX/100      | XX       |
| Feedback Loops            | 10%    | XX/100      | XX       |
| Type Safety*              | 10%    | XX/100      | XX       |
| Consistency & Conventions | 5%     | XX/100      | XX       |
| Change Safety             | 5%     | XX/100      | XX       |

*Type Safety for dynamic languages = contracts (dry-rb, Pydantic), ActiveRecord/Eloquent validations, Form Requests, PHPStan/Larastan, Result pattern consistency. NOT penalized for absence of a compiled type checker.

### Statically-typed languages (TypeScript, Go, Java, Scala, Rust)

| Dimension                 | Weight | Agent Score | Weighted |
|---------------------------|--------|-------------|----------|
| Type Safety               | 20%    | XX/100      | XX       |
| Test Foundation           | 15%    | XX/100      | XX       |
| Documentation & Context   | 15%    | XX/100      | XX       |
| Code Clarity              | 15%    | XX/100      | XX       |
| Architecture Clarity      | 15%    | XX/100      | XX       |
| Feedback Loops            | 10%    | XX/100      | XX       |
| Consistency & Conventions | 5%     | XX/100      | XX       |
| Change Safety             | 5%     | XX/100      | XX       |

**Overall Score** = sum of (agent score × weight)

**Score Bands:**
- **85-100**: Agent-Ready — codebase supports autonomous agent work
- **70-84**: Agent-Assisted — agents work well with human oversight
- **50-69**: Agent-Supervised — agents need heavy review before merging
- **30-49**: Agent-Caution — foundational improvements needed first
- **0-29**: Not Agent-Ready — significant investment required before agent work

---

## Phase 4: Report Assembly

Read the report template from `assets/report-template.md`. Fill in the template using the pass results and the weight table matching the codebase's `LANGUAGE_TIER` from Phase 3.

Include the Codebase Snapshot in the report exactly as it was given to the passes, `Quality gates` line included, and repeat that line verbatim in the `Quality Gate Maturity` section. The snapshot and the section must never disagree.

**Important:** Use the exact weights from the appropriate Phase 3 table (dynamic vs. static). Do not use hardcoded weights — they differ by language tier.

Output the completed report.

---

## Phase 5: Offer to Save Report

After presenting the report, ask:

> "Would you like me to save this assessment as `AGENT_READY_ASSESSMENT.md` in the project root? It can serve as a baseline for tracking improvements over time and is useful for sharing with your team."

If the user confirms, write the full report to `AGENT_READY_ASSESSMENT.md` in the current directory.

---

## Phase 6: CI Integration Recommendation

After saving (or if the user declines), if the Gate Maturity Level is L0-L2, mention that the **agent-ready** plugin's `quality-gates` mode installs a regression-aware gate (report / check / baseline commands, merge-base-aware CI, reviewed baseline, and tests) using the project's native tools:

> Your quality gates scored [Lx]. Run `agent-ready` in **quality-gates** mode to install a gate that blocks new or worsened complexity, duplication, and dead code without forcing a cleanup of legacy debt first.

Then mention:

> **For continuous tracking:** Consider adding [`btar`](https://github.com/jaredmcfarland/btar) to your CI pipeline. It provides fast, deterministic measurement of your verification infrastructure (type errors, lint violations, test coverage) and can gate PRs when scores regress. This assessment gives a strategic baseline; btar gives daily CI enforcement of the most critical metrics.
>
> ```bash
> npm install -g btar
> btar analyze .          # Quick score: types + lint + coverage
> btar context generate agents-md  # Auto-generates AGENTS.md with your build/test commands
> ```
