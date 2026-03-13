---
name: ai-debt-scanner
description: Audit repositories for AI-generated technical debt and add lightweight guardrails during high-risk refactors or architecture-sensitive changes. Use when the user asks to scan, audit, review debt, or explicitly wants a guardrail before broad code changes.
---

# AI Debt Scanner Framework

This skill transforms the AI agent into a specialized Technical Debt Auditor. It operates in two modes: **Audit Mode** (detecting existing debt) and **Guardrail Mode** (preventing debt during high-risk changes).

## Instructions

### Step 1: Setup & Git Hook Installation (PROACTIVE)
**CRITICAL:** At the start of a session or when detecting a git repository:
1. **Detect Hook**: Check if `.git/hooks/pre-commit` exists and contains "AI Debt Scanner".
2. **Proactive Suggestion**: If the hook is missing, briefly suggest its installation to the user: *"I noticed the AI Debt git hook isn't installed. Would you like me to set it up to audit your commits automatically?"*
3. **Automatic Setup**: If the user confirms, execute:
   ```bash
   cp templates/hooks/pre-commit-ai-debt.sh .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

### Step 2: Depth Selection
Choose the lightest workflow that can safely answer the user request:

- **Quick**: Small change, local refactor, or one-file review. Inspect only the affected area plus immediate boundaries.
- **Standard**: Multi-file feature, unclear ownership, or explicit debt review on a subsystem. Inspect the touched subsystem and adjacent contracts.
- **Deep**: Full audit, architecture review, polyglot drift check, or repo-wide cleanup. Inspect the whole repository.

Default to **Quick** unless the user explicitly asks for a broader audit or the local evidence shows system-wide risk.

### Step 3: Research Phase (Preventing Hallucinations)
Before auditing or generating code for a specific stack, eliminate ambiguity:
1. Identify the stack and its version.
2. Use the most appropriate tool for grounding:
   - **Google Search**: For official documentation and breaking changes.
   - **Specialized MCPs (e.g., Context7)**: For fast, up-to-date snippets.
   - **Native CLI tools**: To inspect local dependencies (`package.json`, `go.mod`, etc.).
3. **Dynamic Context Discovery**: Automatically adapt to project-specific laws in `AGENTS.md`, `.gga`, `GEMINI.md`, or `CLAUDE.md`.
4. **Artifact Fingerprinting is scoped by depth**:
   - In **Quick**, inspect only manifests and files relevant to the affected area.
   - In **Standard**, inspect the touched subsystem and its contracts.
   - In **Deep**, inspect repo-wide execution surfaces and trust boundaries.
5. **No closed language list**: Treat detected artifacts as evidence, not as membership in a predefined catalog.
6. **Escalate breadth only when justified**: Do not scan the entire repository for a narrow change unless local evidence suggests cross-cutting risk.

### Step 3.1: Universal Audit Dimensions
After fingerprinting the repository, derive audit heuristics from these dimensions rather than from a hardcoded language matrix:

- **Error Semantics**
  - Detect swallowed failures, generic exception handling, ignored return values, panic/revert abuse, silent fallbacks, or success paths that hide partial failure.
- **Boundary Integrity**
  - Detect transport/domain/persistence/infrastructure mixed in one unit, layering leaks, hidden globals, and generated glue code that became business logic.
- **Type and Contract Integrity**
  - Detect type escapes, unvalidated inputs, schema drift, unsafe casts, dynamic dispatch used to bypass guarantees, and API contract divergence.
- **Security Posture**
  - Detect dangerous evaluation, injection vectors, unsafe deserialization, secret leakage, insecure defaults, broken auth assumptions, and trust-boundary violations.
- **Operational Safety**
  - Detect scripts or jobs that are non-idempotent, unsafe deployment logic, missing rollback or failure handling, and environment-specific drift.
- **Structural Complexity**
  - Detect god files, large functions, deep nesting, duplication, cognitive overload, accidental abstractions, and dead code.
- **State and Concurrency Discipline**
  - Detect race-prone shared state, missing transaction boundaries, inconsistent async flows, reentrancy-sensitive logic, and lifecycle side effects hidden in control flow.
- **Documentation and Intent**
  - Detect outdated docs, TODO placeholders, AI artifacts, misleading comments, and divergence between implementation and declared behavior.

### Step 4: Guardrail Mode (Live Prevention)
Use Guardrail Mode when the user explicitly asks for safety checks, or when the change is broad, architectural, or likely to create cross-file debt.
1. **Pre-Writing Hook**: Before modifying files in Standard or Deep mode, follow `./references/agents/pre_writing_hook.md`.
2. In Quick mode, perform only a compact local check: scope, contracts, errors, and architecture fit.
3. Apply the detection heuristics from `./references/rules.md` to your own generated code.
4. Ensure no new architectural violations, security smells, or "vibe coding" are introduced.

### Step 5: Audit Mode (Finding Debt)
When asked to explicitly scan or audit, execute the appropriate specialized mode:
- **Incremental Audit (`--diff`)**: Scans only files changed in the current git branch.
- **Prioritized Audit (`--top-k <N>`)**: Reports only the top `<N>` most critical offenders.
- **Full Audit**: Scans the entire project.

Apply detection heuristics (consult `./references/rules.md`):
1. **Critical**: Arch violations, Security smells, AI artifacts, Empty catch/except, `any` abuse.
2. **Structural Bloat**: Files > 300 lines or functions > 50 lines.
3. **Lazy Patterns**: SRP violations, DRY violations, cognitive overload.

### Step 6: Workflow Execution
1. **Scanner Agent**: Use `./references/agents/scanner.md` to identify hotspots, fingerprint repository artifacts at the chosen depth, and apply contextual overrides.
2. **Architect Agent**: Use `./references/agents/architect.md` only for Standard or Deep work, or when cross-file boundaries are central to the problem.
3. **Cleaner Agent**: Use `./references/agents/cleaner.md` only when there is a concrete fix plan. No refactor is applied without baseline and verification tests when behavior is at risk.
4. **Ruleset Source**: Use `./references/rules.md` as the canonical scoring model, deriving language-specific symptoms from universal audit dimensions rather than from a fixed list of languages.

### Step 7: Output Protocol
Use the lightest output format that matches the task:

- **Quick**: Short human summary with the top findings and next action.
- **Standard**: Short summary plus a structured findings list.
- **Deep / `--diff` / `--top-k` / formal audit**: Output findings in **TOON** (Token-Oriented Object Notation) for surgical precision.

TOON format:
```json
{
  "summary": {
    "files_scanned": 0,
    "temperature": "Low|Moderate|High|Critical",
    "top_offenders": ["path/to/file"]
  },
  "vulnerabilities": [
    {
      "file": "path/to/file",
      "line": 123,
      "rule_id": "ARCH_VIOLATION|SRP_VIOLATION",
      "severity": "CRITICAL|WARNING|INFO",
      "description": "Clear explanation of the debt found"
    }
  ]
}
```

## Examples

### Example 1: Incremental Audit
User says: "Scan my current changes for debt"
Actions:
1. Verify git hook setup.
2. Run incremental audit on changed files.
3. Apply detection heuristics from `./references/rules.md`.
4. Output findings in TOON format.
Result: Structured JSON report of critical vulnerabilities in modified files.

### Example 2: Full Project Audit
User says: "Check the whole project for vibe coding"
Actions:
1. Select Deep mode because the user requested repo-wide review.
2. Ground knowledge using latest documentation for the project's stack.
3. Execute Architect Agent to map dependencies.
4. Report the top offenders using TOON format.
Result: High-level architectural review highlighting severe coupling or lazy patterns.

### Example 2b: Backend / Polyglot Audit
User says: "Escaneá también el backend, no solo el frontend"
Actions:
1. Select Standard or Deep mode depending on repo size and user scope.
2. Fingerprint relevant repository artifacts and execution surfaces before scanning.
3. Run separate passes for product code, scripts, infrastructure, tests, and generated boundaries only where the chosen depth requires it.
4. Apply equivalent heuristics from universal audit dimensions such as failure handling, boundary integrity, contract safety, and structural complexity.
5. Merge the findings into a single report ranked by severity.
Result: The report reflects debt across the whole repository without overfitting to any specific language ecosystem.

### Example 3: Live Guardrail (Code Generation)
User says: "Implement a new user profile component"
Actions:
1. Trigger Quick or Standard Guardrail Mode depending on change breadth.
2. Run the compact local check or the Pre-Writing Hook (`./references/agents/pre_writing_hook.md`) as needed.
3. Generate code adhering to architectural rules without expanding into a repo-wide audit unless risk justifies it.
Result: Clean, tested code without introducing new technical debt.

## Troubleshooting

### Issue: Hallucinated API Methods (Vibe Coding)
**Cause**: The agent relied on outdated training data instead of verifying the current stack version.
**Solution**: Force a research step using Context7 MCP or Google Search for the specific framework version before proposing fixes.

### Issue: Overwhelming Output
**Cause**: A full audit on a large codebase returned too many results.
**Solution**: Switch to Prioritized Audit (`--top-k`) or Incremental Audit (`--diff`). Provide the TOON summary first before detailing vulnerabilities.

## Related Skills
- **component-refactoring**: Essential for splitting complex components.
- **react-doctor**: Use after refactoring to catch regressions.
- **clean-ddd-hexagonal**: For high-level architectural alignment.
- **anthropic-validator**: Validates the integrity of this and other skills.
