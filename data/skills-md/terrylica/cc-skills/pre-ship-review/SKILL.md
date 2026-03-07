---
name: pre-ship-review
description: "Run a structured quality review before shipping code at any checkpoint such as PRs, releases, or milestones. Use whenever the user says 'pre-ship review', 'ship check', 'quality review', 'self review', or 'ready to ship', or before any significant code submission. This skill catches integration boundary failures where AI-generated code breaks between components. Do NOT use for routine linting or formatting (those are handled by Phase 2 of ITP) or for reviewing documentation-only changes."
allowed-tools: Bash, Read, Grep, Glob
---

# Pre-Ship Review

Structured quality review before shipping code at any checkpoint: PRs, releases, milestones. Catches the failures that occur at **integration boundaries** -- where contracts, examples, constants, and tests must all agree.

> **Core thesis**: AI-generated code excels at isolated components but fails systematically at boundaries between components. This skill systematically checks those boundaries.

## When to Use This Skill

Use before any significant code shipment:

- **Pull requests** with multiple new modules that wire together
- **Releases** combining work from multiple contributors or branches
- **Milestones** where quality gates must pass before proceeding
- **Any checkpoint** where code with examples, constants across files, or interface extensions needs validation

NOT needed for: single-file cosmetic changes, documentation-only updates, dependency bumps.

---

## TodoWrite Task Templates

**MANDATORY**: Select and load the appropriate template before starting review.

### Template A: New Feature Ship

```
1. Detect changed files and scope (git diff --name-only against base branch)
2. Run Phase 1 - External tool checks (Pyright, Vulture, import-linter, deptry, Semgrep, Griffe)
3. Run Phase 2 - cc-skills orchestration (code-hardcode-audit, dead-code-detector, pr-gfm-validator)
4. Run Phase 2 conditional checks based on file types changed
5. Phase 3 - Verify every function parameter has at least one caller passing it by name
6. Phase 3 - Verify every config/example parameter maps to an actual function kwarg
7. Phase 3 - Check for architecture boundary violations (hardcoded feature lists, cross-layer coupling)
8. Phase 3 - Verify domain constants and formulas are correct (cross-reference cited sources)
9. Phase 3 - Audit test quality - do tests test what they claim (not side effects)?
10. Phase 3 - Check for implicit dependencies between new components
11. Phase 3 - Look for O(n^2) patterns where O(n) suffices
12. Phase 3 - Verify error messages give actionable guidance
13. Phase 3 - Confirm examples reflect actual behavior, not aspirational behavior
14. Compile findings report with severity and suggested fixes
```

### Template B: Bug Fix Ship

```
1. Verify the fix addresses root cause, not symptom
2. Verify the fix does not mask information flow
3. Check that new test reproduces the original bug (fails without fix)
4. Run Phase 1 - External tool checks on changed files
5. Run Phase 2 - cc-skills checks on changed files
6. Verify constants consistency if any values changed
7. Compile findings report
```

### Template C: Refactoring Ship

```
1. Verify all callers updated to match new signatures
2. Run Phase 1 - External tool checks (especially Griffe for API drift)
3. Run Phase 2 - cc-skills checks (especially dead-code-detector)
4. Verify examples/docs updated to match new parameter names
5. Verify no dead imports from removed features
6. Check for introduced cross-boundary coupling
7. Compile findings report
```

---

## Three-Phase Workflow

### Phase 1: External Tool Checks (~15s, parallelizable)

Run static analysis tools on changed files. Skip any tool that is not installed (graceful degradation).

```
Detect scope:
  git diff --name-only $(git merge-base HEAD main)...HEAD

Run in parallel:
  pyright --outputjson <changed_py_files>          # Type contracts
  vulture <changed_py_files> --min-confidence 80   # Dead code / YAGNI
  lint-imports                                      # Architecture boundaries
  deptry .                                          # Dependency hygiene
  semgrep --config .semgrep/ <changed_files>        # Custom pattern rules
  griffe check --against main <package>             # API signature drift
```

**What each tool catches:**

| Tool             | Anti-Pattern                                              | Install                     |
| ---------------- | --------------------------------------------------------- | --------------------------- |
| Pyright (strict) | Interface contracts, return types, cross-file type errors | `pip install pyright`       |
| Vulture          | Dead code, unused constants/imports (YAGNI)               | `pip install vulture`       |
| import-linter    | Architecture boundary violations, forbidden imports       | `pip install import-linter` |
| deptry           | Unused/missing/transitive dependencies                    | `pip install deptry`        |
| Semgrep          | Non-determinism, silent param absorption, banned patterns | `brew install semgrep`      |
| Griffe           | Breaking API changes, signature drift vs base branch      | `pip install griffe`        |

**Graceful degradation**: If a tool is not installed, log a warning and skip it. Never fail the entire review because one optional tool is missing.

For detailed tool procedures, see [Automated Checks Reference](./references/automated-checks.md).
For installation instructions, see [Tool Install Guide](./references/tool-install-guide.md).

### Phase 2: cc-skills Orchestration (~30s, subagent-parallelizable)

Invoke existing cc-skills that complement external tools.

**Always run:**

- **code-hardcode-audit** -- Hardcoded values, magic numbers, leaked secrets
- **dead-code-detector** -- Polyglot dead code detection (Python, TypeScript, Rust)
- **pr-gfm-validator** -- PR description link validity (if creating a PR)

**Run conditionally based on changed file types:**

| Condition                 | Skill to invoke                                     |
| ------------------------- | --------------------------------------------------- |
| Python files changed      | impl-standards (error handling, constants, logging) |
| 500+ lines changed        | code-clone-assistant (duplicate code detection)     |
| Plugin/hook files changed | plugin-validator (structure, silent failures)       |
| Markdown/docs changed     | link-validation (broken links, path policy)         |

### Phase 3: Human Judgment Review (Claude-assisted)

These checks require understanding intent, domain correctness, and architectural fitness. Go through each one manually.

**Check 1: Architecture Boundaries**

- Does new code in a "core" layer reference names from a "plugin" or "capability" layer?
- Are there hardcoded lists of feature/plugin names? (Boundary violation)
- Would adding another instance of this feature type require modifying core code?

**Check 2: Domain Correctness**

- Are mathematical formulas correct? Cross-reference with cited papers.
- Are constants labeled correctly? (e.g., a "daily" constant should use the daily value)
- Do units and time periods match? (annual vs daily rates, quarterly vs monthly lambdas)

**Check 3: Test Quality**

- Does each test exercise the specific function it claims to test?
- Or does it test a side-effect? (Function A tests function B which internally calls A)
- Are edge cases covered? (Empty input, NaN, single element, division by zero)

**Check 4: Dependency Transparency**

- If component A requires component B to run first, is this documented?
- Are ordering requirements explicit in interfaces, not just in examples?

**Check 5: Performance**

- Any nested loops over the same data? (Potential O(n^2))
- Any expanding-window operations that could be rolling or full-sample?
- Any per-element operations that could be vectorized?

**Check 6: Error Message Quality**

- Do errors tell users what to DO, not just what went wrong?
- Do validation errors reference the specific parameter/value that failed?

**Check 7: Example Accuracy**

- Do examples demonstrate features that actually work in the code?
- Are there parameters in examples that get silently absorbed by `**kwargs` or `**_`?

For detailed check procedures, see [Judgment Checks Reference](./references/judgment-checks.md).

---

## Universal Pre-Ship Checklist

```
Phase 1 (Tools):
- [ ] Pyright strict passes on changed files (no type errors)
- [ ] Vulture finds no unused code in new files (or allowlisted)
- [ ] import-linter passes (no architecture boundary violations)
- [ ] deptry passes (no unused/missing dependencies)
- [ ] Semgrep custom rules pass (no non-determinism, no silent param absorption)
- [ ] Griffe shows no unintended API breaking changes vs base branch

Phase 2 (cc-skills):
- [ ] code-hardcode-audit passes (no magic numbers or secrets)
- [ ] dead-code-detector passes (no unused code)
- [ ] PR description links valid (pr-gfm-validator)

Phase 3 (Judgment):
- [ ] No new cross-boundary coupling introduced
- [ ] Domain constants and formulas are mathematically correct
- [ ] Tests actually test what they claim (not side effects)
- [ ] Implicit dependencies between components are documented
- [ ] No O(n^2) where O(n) suffices
- [ ] Error messages give actionable guidance
- [ ] Examples reflect actual behavior, not aspirational behavior
```

---

## Anti-Pattern Catalog

This skill is built on a taxonomy of 9 integration boundary anti-patterns. For the full catalog with examples, detection heuristics, and fix approaches, see [Anti-Pattern Catalog](./references/anti-pattern-catalog.md).

| #   | Anti-Pattern                    | Detection Method                           |
| --- | ------------------------------- | ------------------------------------------ |
| 1   | Interface contract violation    | Pyright + Griffe + manual trace            |
| 2   | Misleading examples             | Semgrep + manual config-to-code comparison |
| 3   | Architecture boundary violation | import-linter + manual review              |
| 4   | Incorrect domain constants      | Semgrep + domain expertise                 |
| 5   | Testing gaps                    | mutmut + manual test audit                 |
| 6   | Non-determinism                 | Semgrep custom rules                       |
| 7   | YAGNI                           | Vulture + dead-code-detector               |
| 8   | Hidden dependencies             | Manual dependency trace                    |
| 9   | Performance anti-patterns       | Manual complexity analysis                 |

---

## Post-Change Checklist

After modifying THIS skill:

- [ ] Anti-pattern catalog reflects real-world findings
- [ ] Tool install guide has current versions and commands
- [ ] TodoWrite templates cover the three ship types
- [ ] Universal checklist is complete and non-redundant
- [ ] All `references/` links resolve correctly
- [ ] Append changes to `references/evolution-log.md`

---

## Troubleshooting

| Issue                                           | Cause                              | Solution                                                         |
| ----------------------------------------------- | ---------------------------------- | ---------------------------------------------------------------- |
| Tool not found                                  | External tool not installed        | Install per tool-install-guide.md or skip (graceful degradation) |
| Too many Vulture false positives                | Framework entry points look unused | Create allowlist: `vulture --make-whitelist > whitelist.py`      |
| Semgrep too slow                                | Large codebase scan                | Scope to changed files only: `semgrep --include=<changed>`       |
| import-linter has no contracts                  | Project not configured             | Add `[importlinter]` section to `pyproject.toml`                 |
| Griffe reports false breaking changes           | Intentional API change             | Use `griffe check --against main --allow-breaking`               |
| Phase 3 finds nothing but reviewer finds issues | New anti-pattern category          | Add to catalog and evolution-log.md                              |
| cc-skill not triggering                         | Skill not installed in marketplace | Verify with `/plugin list`                                       |

---

## Reference Documentation

For detailed information, see:

- [Automated Checks Reference](./references/automated-checks.md) -- Phase 1 external tool procedures
- [Judgment Checks Reference](./references/judgment-checks.md) -- Phase 3 human-judgment procedures
- [Anti-Pattern Catalog](./references/anti-pattern-catalog.md) -- Full 9-category taxonomy with examples
- [Tool Install Guide](./references/tool-install-guide.md) -- Installation and setup for all external tools
- [Evolution Log](./references/evolution-log.md) -- Change history
