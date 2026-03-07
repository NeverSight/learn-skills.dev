---
name: dead-code-detector
description: Detect unused/unreachable code in polyglot codebases (Python, TypeScript, Rust). TRIGGERS - dead code, unused functions, unused imports, unreachable code.
allowed-tools: Read, Grep, Bash, Edit, Write
---

# Dead Code Detector

Find and remove unused code across Python, TypeScript, and Rust codebases.

## Tools by Language

| Language   | Tool                                                      | Detects                                       |
| ---------- | --------------------------------------------------------- | --------------------------------------------- |
| Python     | [vulture](https://github.com/jendrikseipp/vulture) v2.14+ | Unused imports, functions, classes, variables |
| TypeScript | [knip](https://knip.dev/) v5.0+                           | Unused exports, dependencies, files           |
| Rust       | `cargo clippy` + `rustc` lints                            | Unused functions, imports, dead_code warnings |

**Why these tools?**

- **vulture**: AST-based, confidence scoring (60-100%), whitelist support
- **knip**: Successor to ts-prune (maintenance mode), monorepo-aware, auto-fix
- **cargo clippy**: Built-in to Rust toolchain, zero additional deps

---

## When to Use This Skill

Use this skill when:

- Cleaning up a codebase before release
- Refactoring to reduce maintenance burden
- Investigating bundle size / compile time issues
- Onboarding to understand what code is actually used

**NOT for**: Code duplication (use `quality-tools:code-clone-assistant`)

---

## Quick Start Workflow

### Python (vulture)

```bash
# Step 1: Install
uv pip install vulture

# Step 2: Scan with 80% confidence threshold
vulture src/ --min-confidence 80

# Step 3: Generate whitelist for false positives
vulture src/ --make-whitelist > vulture_whitelist.py

# Step 4: Re-scan with whitelist
vulture src/ vulture_whitelist.py --min-confidence 80
```

### TypeScript (knip)

```bash
# Step 1: Install (project-local recommended)
bun add -d knip

# Step 2: Initialize config
bunx knip --init

# Step 3: Scan for dead code
bunx knip

# Step 4: Auto-fix (removes unused exports)
bunx knip --fix
```

### Rust (cargo clippy)

```bash
# Step 1: Scan for dead code warnings
cargo clippy -- -W dead_code -W unused_imports -W unused_variables

# Step 2: For stricter enforcement
cargo clippy -- -D dead_code  # Deny (error) instead of warn

# Step 3: Auto-fix what's possible
cargo clippy --fix --allow-dirty
```

---

## Confidence and False Positives

### Python (vulture)

| Confidence | Meaning                                     | Action                          |
| ---------- | ------------------------------------------- | ------------------------------- |
| 100%       | Guaranteed unused in analyzed files         | Safe to remove                  |
| 80-99%     | Very likely unused                          | Review before removing          |
| 60-79%     | Possibly unused (dynamic calls, frameworks) | Add to whitelist if intentional |

**Common false positives** (framework-invoked code):

- Route handlers / controller methods (invoked by web frameworks)
- Test fixtures and setup utilities (invoked by test runners)
- Public API surface exports (re-exported for consumers)
- Background job handlers (invoked by task queues / schedulers)
- Event listeners / hooks (invoked by event systems)
- Serialization callbacks (invoked during encode/decode)

### TypeScript (knip)

Knip uses TypeScript's type system for accuracy. Configure in `knip.json`:

```json
{
  "entry": ["src/index.ts"],
  "project": ["src/**/*.ts"],
  "ignore": ["**/*.test.ts"],
  "ignoreDependencies": ["@types/*"]
}
```

### Rust

Suppress false positives with attributes:

```rust
#[allow(dead_code)]  // Single item
fn intentionally_unused() {}

// Or module-wide
#![allow(dead_code)]
```

---

## Integration with CI

### Python (pyproject.toml)

```toml
[tool.vulture]
min_confidence = 80
paths = ["src"]
exclude = ["*_test.py", "conftest.py"]
```

### TypeScript (package.json)

```json
{
  "scripts": {
    "dead-code": "knip",
    "dead-code:fix": "knip --fix"
  }
}
```

### Rust (Cargo.toml)

```toml
[lints.rust]
dead_code = "warn"
unused_imports = "warn"
```

---

## Reference Documentation

For detailed information, see:

- [Python Workflow](./references/python-workflow.md) - vulture advanced usage
- [TypeScript Workflow](./references/typescript-workflow.md) - knip configuration
- [Rust Workflow](./references/rust-workflow.md) - clippy lint categories

---

## Troubleshooting

| Issue                          | Cause                         | Solution                                                       |
| ------------------------------ | ----------------------------- | -------------------------------------------------------------- |
| Reports framework-invoked code | Framework magic / callbacks   | Add to whitelist or exclusion config                           |
| Misses dynamically loaded code | Not in static entry points    | Configure entry points to include plugin/extension directories |
| Warns about test-only helpers  | Test code compiled separately | Use conditional compilation or test-specific exclusions        |
| Too many false positives       | Threshold too low             | Increase confidence threshold or configure ignore patterns     |
| Missing type-only references   | Compile-time only usage       | Most modern tools handle this; check tool version              |

---

## Multi-Perspective Validation (Critical)

**IMPORTANT**: Before removing any detected "dead code", spawn parallel subagents to validate findings from multiple perspectives. Dead code may actually be **unimplemented features** or **incomplete integrations**.

### Classification Matrix

| Finding Type          | True Dead Code                | Unimplemented Feature               | Incomplete Integration        |
| --------------------- | ----------------------------- | ----------------------------------- | ----------------------------- |
| Unused callable       | No callers, no tests, no docs | Has TODO/FIXME, referenced in specs | Partial call chain exists     |
| Unused export/public  | Not imported anywhere         | In public API, documented           | Used in sibling module        |
| Unused import/include | Typo, refactored away         | Needed for side effects             | Type-only or compile-time     |
| Unused binding        | Assigned but never read       | Placeholder for future              | Debug/instrumentation removed |

### Validation Workflow

After running detection tools, **spawn these parallel subagents**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Dead Code Findings                           │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Intent Agent    │ │ Integration     │ │ History Agent   │
│                 │ │ Agent           │ │                 │
│ - Check TODOs   │ │ - Trace call    │ │ - Git blame     │
│ - Search specs  │ │   chains        │ │ - Commit msgs   │
│ - Find issues   │ │ - Check exports │ │ - PR context    │
│ - Read ADRs     │ │ - Test coverage │ │ - Author intent │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AskUserQuestion: Confirm Classification            │
│  [ ] True dead code - safe to remove                            │
│  [ ] Unimplemented - create GitHub Issue to track               │
│  [ ] Incomplete - investigate integration gaps                  │
│  [ ] False positive - add to whitelist                          │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Prompts

**Intent Agent** (searches for planned usage):

```
Search for references to [IDENTIFIER] in:
1. TODO/FIXME/HACK comments in codebase
2. Issue tracker (open and closed issues)
3. Design documents and architecture decision records
4. README and project documentation files
Report: Was this code planned but not yet integrated?
```

**Integration Agent** (traces execution paths):

```
For [IDENTIFIER], analyze:
1. All module import/include/use statements
2. Runtime module loading mechanisms (lazy loading, plugins)
3. Framework-invoked patterns (metadata attributes, config bindings, annotations)
4. Test files that may exercise this code path
Report: Is there a partial or indirect call chain?
```

**History Agent** (investigates provenance):

```
For [IDENTIFIER], check:
1. VCS blame/annotate - who wrote it and when
2. Commit message - what was the stated intent
3. Code review / merge request context - was it part of larger feature
4. Recent commits - was calling code removed or refactored
Report: Was this intentionally orphaned or accidentally broken?
```

### Example: Validating Findings

```bash
# Step 1: Run detection tool for your language
<tool> <source-path> --confidence-threshold 80 > findings.txt

# Step 2: For each high-confidence finding, spawn validation
# (Claude Code will use Task tool with Explore agents)
```

**Sample finding**: `unused function 'calculate_metrics' (src/analytics.py:45)`

**Multi-agent investigation results**:

- Intent Agent: "Found TODO in src/dashboard.py:12 - 'integrate calculate_metrics here'"
- Integration Agent: "Function is imported in tests/test_analytics.py but test is marked skip/pending"
- History Agent: "Added in MR #234 'Add analytics foundation' - dashboard integration deferred"

**Conclusion**: NOT dead code - it's an **unimplemented feature**. Create tracking issue.

### User Confirmation Flow

After agent analysis, use `AskUserQuestion` with `multiSelect: true`:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "How should we handle these findings?",
      header: "Action",
      multiSelect: true,
      options: [
        {
          label: "Remove confirmed dead code",
          description: "Delete items verified as truly unused",
        },
        {
          label: "Create issues for unimplemented",
          description: "Track planned features in GitHub Issues",
        },
        {
          label: "Investigate incomplete integrations",
          description: "Spawn deeper analysis for partial implementations",
        },
        {
          label: "Update whitelist",
          description: "Add false positives to tool whitelist",
        },
      ],
    },
  ],
});
```

### Risk Classification

| Risk Level   | Criteria                                                | Action                      |
| ------------ | ------------------------------------------------------- | --------------------------- |
| **Low**      | 100% confidence, no references anywhere, >6 months old  | Auto-remove with VCS commit |
| **Medium**   | 80-99% confidence, some indirect references             | Validate with agents first  |
| **High**     | <80% confidence, recent code, has test coverage         | Manual review required      |
| **Critical** | Public API surface, documented, has external dependents | NEVER auto-remove           |

---

## Sources

- [vulture GitHub](https://github.com/jendrikseipp/vulture)
- [knip documentation](https://knip.dev/)
- [Effective TypeScript: Use knip](https://effectivetypescript.com/2023/07/29/knip/)
- [Rust dead_code lint](https://doc.rust-lang.org/rust-by-example/attribute/unused.html)
- [DCE-LLM research paper](https://aclanthology.org/2025.naacl-long.501.pdf) (emerging LLM-based approach)
