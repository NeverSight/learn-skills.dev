---
name: deep-read
description: Comprehensive codebase reading engine. Systematically reads actual source code line by line through a 6-phase protocol — scoping, structural mapping, execution tracing, deep reading, pattern synthesis, and structured reporting. Source code is the source of truth. Use when needing to truly understand how code works, not just what documentation claims.
disable-model-invocation: true
argument-hint: "<codebase area, module, flow, or question to understand>"
---

# Deep Read — Codebase Reading Engine

Systematic source-code-first analysis protocol. Reads implementations, not just interfaces. Every finding cites `file:line`.

**Core principle:** Source code is the source of truth. Documentation lies, comments rot, function names mislead. Read the actual code.

## Protocol

Process every `/deep-read` invocation through these 6 phases in strict order. Never skip a phase. Gate each phase: do not advance until the gate condition is met.

---

### Phase 1: SCOPE — Define the Reading Target

Narrow the target to a tractable area before reading anything.

1. Parse `$ARGUMENTS` as the reading target (module, flow, question, or path)
2. Read CLAUDE.md and MEMORY.md for project context — but treat these as **hints, not truth**
3. Run initial discovery to estimate scope:
   - `Glob` for relevant file patterns (`**/*.ts`, `**/*.py`, etc.)
   - `Grep` for key terms from the target description
   - Count matching files
4. If scope exceeds 50 source files:
   - Use `AskUserQuestion` to narrow: which subsystem, which flow, which layer?
   - Suggest specific narrowing options based on directory structure
5. If the target is a **question** (e.g., "how are commissions calculated?"):
   - Translate to concrete search terms
   - Grep for domain terms to locate relevant modules
6. If the target is a **path** (e.g., `src/services/billing/`):
   - List all files in the path
   - Identify entry points (exported functions, route handlers, main files)

**Output:** A scope definition listing:
- Target description (1-2 sentences)
- File list (< 50 source files)
- Identified entry points
- Out-of-scope areas (explicitly noted)

**Gate:** Scope is defined and contains < 50 source files. Entry points identified. Proceed.

---

### Phase 2: MAP — Build Structural Overview

Understand the shape of the code before reading it deeply.

1. **Directory structure** — map the relevant directories:
   - Use `Glob` to list files by type and directory
   - Note the organizational pattern (by feature, by layer, by domain)
2. **Tech stack** — identify from configs (not from docs):
   - Read `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`, or equivalent
   - Note frameworks, key dependencies, build tools
3. **Entry points** — verify by reading actual files (not just file names):
   - Read route definitions, main files, exported modules
   - Read the first 50 lines of each candidate entry point
   - Confirm which files are actual entry points vs. helpers
4. **Dependency graph** — map internal imports within the scope:
   - Grep for import/require statements within scoped files
   - Build a mental model: what calls what, what depends on what
   - Identify the **core files** (most imported by others)
5. **Configuration and constants** — read files that define behavior:
   - Config files, environment schemas, constants, enums, types
   - These shape behavior as much as code does

**Launch parallel Explore agents** for steps 2-4 if the scope has 20+ files.

**Output:** Structural map including:
- Directory layout with annotations
- Tech stack (from configs, not docs)
- Entry points (verified by reading)
- Dependency flow diagram (text-based)
- Core files ranked by centrality

**Gate:** Entry points verified by reading actual files. Dependency flow mapped. Proceed.

---

### Phase 3: TRACE — Follow Execution Paths

Start from entry points and trace through the code. Read every file in the path.

1. **Select the primary execution path** based on the reading target:
   - For a flow (e.g., "payment processing"): start at the user-facing entry point
   - For a module: start at its public API / exports
   - For a question: start at the code most likely to contain the answer
2. **Trace forward** from the entry point:
   - Read the entry point file **in full** with the Read tool
   - For every function call, class instantiation, or module import encountered:
     - Grep to locate the implementation (not just the type signature)
     - Read the implementation file in full
   - Continue until reaching terminal operations (DB queries, API calls, file I/O, return values)
3. **Document the path** as a chain with `file:line` citations:
   ```
   Request enters at routes/payments.ts:42 (POST /api/payments)
     -> calls PaymentService.processPayment() at services/payment.ts:87
       -> validates input via PaymentSchema at schemas/payment.ts:15
       -> calls StripeClient.charge() at clients/stripe.ts:34
         -> constructs request at clients/stripe.ts:45-62
       -> stores result via PaymentRepository.save() at repos/payment.ts:28
     -> returns PaymentResponse at routes/payments.ts:58
   ```
4. **Trace secondary paths** if the reading target involves multiple flows:
   - Error paths, edge cases, fallback logic
   - Event handlers, webhooks, background jobs triggered by the primary path
5. **Note every branch point** — conditions, switches, feature flags:
   - What determines which path is taken?
   - Read the condition logic, don't just note "there's a conditional here"

**Output:** Complete execution trace(s) with `file:line` citations for every step.

**Gate:** At least 1 complete path traced from entry to terminal. Every file in the path has been Read in full. Proceed.

---

### Phase 4: DEEP READ — Line-by-Line Analysis of Critical Files

This is the core phase. Read critical files thoroughly, understanding every line of business logic.

1. **Identify critical files** from Phase 3 — files that contain:
   - Business logic (calculations, rules, transformations)
   - State management (mutations, transactions, side effects)
   - Security logic (auth, validation, access control)
   - Data transformations (mapping, filtering, aggregation)
   - Error handling (catch blocks, error boundaries, recovery logic)
2. **Read each critical file in full** with the Read tool:
   - Do NOT skim — read the entire file
   - For files > 500 lines: read in sections, but read ALL sections
   - Launch parallel Read calls for independent files
3. **For each critical file, document:**
   - **Purpose:** What this file actually does (based on code, not comments)
   - **Key functions:** Each function's logic, with citations:
     ```
     calculateCommission(sale: Sale): number  [billing/commission.ts:45-78]
       - Base rate: 5% of sale.amount (line 52)
       - Bonus tier: if sale.amount > 10000, rate += 2% (line 56)
       - Cap: commission capped at 5000 (line 62)
       - Proration: multiplied by daysInPeriod/30 (line 67)
       - Returns: rounded to 2 decimal places (line 74)
     ```
   - **Formulas and conditions:** Write out the actual math and logic, not summaries
   - **State changes:** What gets mutated, what side effects occur
   - **Edge cases handled:** Null checks, bounds, error recovery
   - **Edge cases NOT handled:** Missing validation, unchecked assumptions
4. **Cross-reference between files:**
   - When file A calls file B, verify that A's expectations match B's implementation
   - Note any mismatches between interface contracts and implementations
   - Check that error handling in callers matches errors thrown by callees

**Output:** Detailed analysis of each critical file with:
- Function-level logic documentation with `file:line` citations
- Formulas written out explicitly
- Conditions and branch logic documented
- State changes and side effects listed

**Gate:** Every critical file (identified in step 1) has been Read in full. Logic documented with formulas, conditions, and citations. Proceed.

---

### Phase 5: CONNECT — Synthesize Understanding

Step back and reason about the system as a whole. Use sequential-thinking MCP for structured analysis.

1. **Start a sequential-thinking chain** with all evidence from Phases 1-4:
   ```javascript
   mcp__sequential-thinking__sequentialthinking({
     thought: "Synthesizing understanding of <target>. Evidence from phases: ...",
     thoughtNumber: 1,
     totalThoughts: 8,
     nextThoughtNeeded: true
   })
   ```
2. **Identify patterns** across the codebase (minimum 3):
   - Architectural patterns (layering, dependency injection, event-driven, etc.)
   - Coding conventions (error handling style, naming patterns, data flow patterns)
   - Implicit rules (invariants maintained by convention, not enforced by code)
   - Anti-patterns or technical debt
3. **Map data flows** end to end:
   - How does data enter the system?
   - What transformations does it undergo? (with `file:line` citations)
   - Where does it end up? (DB, API response, file, event)
4. **Identify risks and assumptions:**
   - What assumptions does the code make that aren't validated?
   - What would break if those assumptions were violated?
   - Are there race conditions, consistency gaps, or security concerns?
5. **Answer the original question** if the reading target was a question:
   - Provide the answer with full evidence chain
   - Cite every source

Use **branching** in sequential-thinking to explore alternative interpretations of ambiguous code.

**Output:** Synthesis including:
- 3+ patterns identified with evidence (`file:line`)
- End-to-end data flow map
- Risk assessment
- Answer to the original question (if applicable)

**Gate:** At least 5 reasoning steps completed. At least 3 patterns identified with `file:line` evidence. Proceed.

---

### Phase 6: REPORT — Structured Deliverable

Produce the final report. Every claim must cite `file:line`.

```markdown
## Deep Read Report: <target>

### Scope
- **Target:** <what was analyzed>
- **Files analyzed:** <count> files, <count> read in full
- **Entry points:** <list with file:line>

### Architecture Overview
<structural summary from Phase 2 — directory layout, tech stack, dependency flow>

### Execution Flow
<traced paths from Phase 3 — entry to terminal with file:line citations>

### Critical Logic
<detailed function-level analysis from Phase 4>

For each critical area:
- **What it does:** <plain language description>
- **How it works:** <formulas, conditions, logic with file:line>
- **State changes:** <what gets mutated>
- **Edge cases:** <handled and unhandled>

### Patterns & Conventions
<synthesized patterns from Phase 5>
1. <pattern> — evidence: <file:line>
2. <pattern> — evidence: <file:line>
3. <pattern> — evidence: <file:line>

### Data Flow
<end-to-end data flow map from Phase 5>

### Risks & Assumptions
<risk assessment from Phase 5>

### Key Findings
<concise bullet list of the most important discoveries>
- <finding> — <file:line>

### Answer
<if the reading target was a question, answer it here with full evidence>
```

**Gate:** All sections populated. Every finding cites `file:line`. Report complete.

---

## Tool Usage by Phase

| Phase | Primary Tools | When to Use Agents |
|-------|--------------|-------------------|
| 1. SCOPE | Read, Glob, Grep, AskUserQuestion | -- |
| 2. MAP | Glob, Grep, Read (configs, entry points) | Explore agents (parallel) for 20+ file codebases |
| 3. TRACE | Read (full files), Grep (cross-refs) | Explore agent for locating implementations |
| 4. DEEP READ | Read (full files, parallel) | -- |
| 5. CONNECT | sequential-thinking MCP | deep-analysis skill for complex reasoning |
| 6. REPORT | Structured output | -- |

## Anti-Patterns — What This Skill Prevents

| Bad Habit | What `/deep-read` Does Instead |
|-----------|-------------------------------|
| Read README/CLAUDE.md and call it done | Phase 1 treats docs as hints; Phases 3-4 read source |
| Skim file headers and imports only | Phase 4 requires line-by-line reading with citations |
| Summarize without evidence | Every claim must cite `file:line` |
| Stop at the first abstraction layer | Phase 3 traces full call chains to leaf functions |
| Rely on function names to infer behavior | Phase 4 reads implementations, documents actual logic |
| Produce vague "this seems to do X" | Phase 4 requires concrete formulas and conditions |
| Read types/interfaces instead of implementations | Phase 3 Greps for implementations, not just signatures |
| Skip error paths and edge cases | Phase 3 traces secondary paths; Phase 4 documents edge cases |

## Scope Examples

```
/deep-read payment processing flow from checkout to settlement
/deep-read src/services/billing/
/deep-read how are sales commissions calculated and distributed?
/deep-read the authentication and authorization system
/deep-read data pipeline from ingestion to reporting dashboard
/deep-read how does the caching layer work and when does it invalidate?
```

## When to Use `/deep-read` vs Other Tools

| Situation | Use |
|-----------|-----|
| Understand how existing code works | `/deep-read` |
| Quick "what does this function do?" | Read tool directly |
| Bug, crash, error, unexpected behavior | `/investigate` |
| Architecture decision or trade-off | `/deep-analysis` |
| Build a new feature | `/execute` |
| Understand code, then reason about it | `/deep-read` then `/deep-analysis` |
| Understand code, then redesign it | `/deep-read` then `/deep-analysis` then `/execute` |
| Onboard to an unfamiliar codebase | `/deep-read` |
| Code review with full context | `/deep-read` then code-quality agent |

## References

See [references/reading-strategies.md](references/reading-strategies.md) for codebase-type-specific reading strategies and context management approaches.
