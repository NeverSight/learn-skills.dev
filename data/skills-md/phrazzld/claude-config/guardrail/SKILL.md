---
name: guardrail
description: |
  Generate custom lint rules from architectural patterns.
  ESLint local plugins (JS/TS) or ast-grep YAML rules (Python/Go/Rust/any).
  Invoke when: codifying an import boundary, enforcing API conventions,
  blocking deprecated patterns, or any "always/never" constraint.
effort: high
argument-hint: '"description of pattern to enforce" [--engine eslint|ast-grep]'
---

# /guardrail

Generate custom lint rules that enforce architectural decisions at edit time.

## Philosophy

Lint rules are the highest-leverage codification target. They're cheaper than hooks
(no custom Python), more durable than CLAUDE.md (automated, not advisory), and work
in CI too (not just Claude Code). A lint rule catches violations the moment code is
written — and `fast-feedback.py` surfaces the error immediately so Claude self-corrects.

## When to Use

- Import boundaries ("all DB access through repository layer")
- API conventions ("routes must start with /api/v1")
- Deprecated pattern blocking ("no direct fetch, use apiClient")
- Auth enforcement ("handlers must call requireAuth")
- Naming conventions that go beyond basic linting

## Workflow

### Phase 1: Accept Pattern

Parse the input. It can be:
- **Natural language:** "all database queries must go through the repository layer"
- **Code example:** "this import is wrong: `import { db } from './db'`"
- **Discovery mode:** scan codebase for architectural invariants (when invoked by `/tune-repo`)

Clarify the constraint:
- What EXACTLY should be flagged? (imports, function calls, patterns)
- What's the fix? (alternative import, wrapper function)
- Are there exceptions? (test files, migrations, the repository itself)

### Phase 2: Choose Engine

| Criterion | ESLint | ast-grep |
|-----------|--------|----------|
| Language | JS/TS only | Any (Python, Go, Rust, etc.) |
| Fixable | Yes (auto-fix) | Yes (rewrite) |
| Testing | RuleTester built-in | YAML snapshot tests |
| Config | Flat config plugin | sgconfig.yml |
| Speed | Fast | Very fast |

Default: ESLint for JS/TS projects, ast-grep for everything else.
If `--engine` is specified, use that.

### Phase 3: Generate Rule

Read the reference docs for the chosen engine:
- ESLint: `references/eslint-rule-anatomy.md`
- ast-grep: `references/ast-grep-rule-anatomy.md`

Read the appropriate template:
- ESLint: `templates/eslint-rule.js` + `templates/eslint-rule-test.js`
- ast-grep: `templates/ast-grep-rule.yml`

Generate:
1. Rule implementation with clear error message and fix suggestion
2. Rule metadata (docs URL, fixable, schema)
3. Test cases (valid AND invalid examples from the actual codebase)

### Phase 4: Test

**ESLint:**
```bash
# Run RuleTester
node guardrails/rules/<rule-name>.test.js
# Or if project uses a test runner:
npx vitest run guardrails/rules/<rule-name>.test.js
```

**ast-grep:**
```bash
sg scan --config guardrails/sgconfig.yml --test
```

Also verify against the real codebase:
```bash
# ESLint: run rule on entire project, expect 0 or known violations
npx eslint --no-warn-ignored --rule 'guardrails/<rule-name>: error' .
# ast-grep: scan project
sg scan --config guardrails/sgconfig.yml
```

### Phase 5: Install

Create the `guardrails/` directory structure if it doesn't exist:

```
guardrails/
  README.md              # Catalog of all custom rules
  index.js               # ESLint local plugin barrel (JS/TS projects)
  sgconfig.yml           # ast-grep config (if non-JS rules exist)
  rules/
    <rule-name>.js       # ESLint rule implementation
    <rule-name>.test.js  # ESLint RuleTester
    <rule-name>.yml      # ast-grep rule
```

**ESLint integration** (flat config, zero npm dependencies):

```javascript
// guardrails/index.js
import noDirectDbImport from "./rules/no-direct-db-import.js";

export default {
  rules: {
    "no-direct-db-import": noDirectDbImport,
  },
};
```

```javascript
// eslint.config.js — add to existing config
import guardrails from "./guardrails/index.js";

export default [
  // ... existing config
  {
    plugins: { guardrails },
    rules: {
      "guardrails/no-direct-db-import": "error",
    },
  },
];
```

**ast-grep integration:**

```yaml
# guardrails/sgconfig.yml
ruleDirs:
  - rules
```

### Phase 6: Document

Update `guardrails/README.md` with:

```markdown
## <rule-name>

**Engine:** ESLint | ast-grep
**Pattern:** <what it enforces>
**Rationale:** <why — link ADR if exists>
**Auto-fix:** yes | no
**Exceptions:** <files/patterns excluded>
```

## Output

```
GUARDRAIL CREATED:
- Rule: guardrails/rules/<name>.<ext>
- Test: guardrails/rules/<name>.test.<ext>
- Engine: ESLint | ast-grep
- Violations found: N (in current codebase)
- Auto-fixable: yes | no
- Config updated: eslint.config.js | guardrails/sgconfig.yml
```

## Anti-Patterns

- Rules that fire on >20% of files (too broad, probably wrong constraint)
- Rules without tests (defeats the purpose)
- Rules without clear error messages (Claude can't self-correct from "error")
- Duplicating built-in ESLint/Ruff rules (check first)
- Over-specific rules that match one file (use CLAUDE.md instead)

## Integration

| Consumed by | How |
|-------------|-----|
| `fast-feedback.py` | Runs `eslint <file>` and `sg scan <file>` on every edit |
| `/codify-learning` | Routes "lint rule" target here |
| `/done` | Routes "lint rule" target here |
| `/tune-repo` | Discovers patterns, recommends `/guardrail` invocations |
| `/check-quality` | Audits `guardrails/` completeness |
| CI (GitHub Actions) | Standard `eslint .` or `sg scan` in workflow |
