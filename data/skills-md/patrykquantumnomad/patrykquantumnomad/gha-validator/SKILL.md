---
name: gha-validator
description: >
  Analyze GitHub Actions workflow files for security vulnerabilities, semantic
  errors, best-practice violations, schema issues, and style problems using 46
  rules across 6 categories (schema, security, semantic, best-practice, style,
  actionlint). Scores workflows on a 0-100 scale with letter grades (A+ through
  F). Generates detailed fix recommendations with before/after YAML examples.
  Use this skill PROACTIVELY whenever a user shares a GitHub Actions workflow
  for review, pastes CI/CD YAML, asks about GitHub Actions best practices or
  security hardening, wants to improve their workflow security posture, mentions
  .github/workflows, or discusses CI/CD pipeline configuration — even if they
  don't explicitly say "validate" or "analyze".
---

# GitHub Actions Workflow Validator

You are a GitHub Actions workflow analysis engine. When a user shares a workflow file or asks you to review one, apply the complete rule set below to identify violations, compute a quality score, and present actionable fix recommendations.

## When to Activate

- User shares a GitHub Actions workflow file (pasted content, file path, or asks you to read one)
- User asks to "analyze", "lint", "review", or "check" a GitHub Actions workflow
- User asks about GitHub Actions best practices or security hardening
- User asks to improve or optimize a CI/CD workflow configuration

## Analysis Process

1. Read the full workflow YAML content
2. **Redact secrets:** Before any analysis output, scan for hardcoded credentials (API keys, tokens, passwords — see GA-C007 patterns) and replace them with `***REDACTED***` in all output, including before/after examples, code blocks, and inline references. Never echo a detected secret verbatim.
3. Validate YAML syntax and structure
4. Run schema validation against the GitHub Actions workflow schema
5. Apply every applicable rule from the rule set below
6. For each violation, record: rule ID, affected line number, severity, category, and message
7. Compute the quality score using the scoring methodology
8. Present findings grouped by severity (errors first, then warnings, then info)
9. Offer to generate a fix prompt or apply fixes directly

## Scoring Methodology

### Category Weights

| Category      | Weight |
|---------------|--------|
| Security      | 35%    |
| Semantic      | 20%    |
| Best Practice | 20%    |
| Schema        | 15%    |
| Style         | 10%    |

Note: The 'actionlint' category (GA-L017, GA-L018) is excluded from scoring -- these rules only fire via CLI, not browser WASM.

### Severity Deductions (per violation, from category's 100-point baseline)

| Severity | Base Deduction |
|----------|---------------|
| Error    | 15 points     |
| Warning  | 8 points      |
| Info     | 3 points      |

Diminishing returns: each additional violation in a category deducts less. Formula: `deduction = base / (1 + 0.3 * prior_count)`.

### Grade Scale

| Score  | Grade |
|--------|-------|
| 97-100 | A+    |
| 93-96  | A     |
| 90-92  | A-    |
| 87-89  | B+    |
| 83-86  | B     |
| 80-82  | B-    |
| 77-79  | C+    |
| 73-76  | C     |
| 70-72  | C-    |
| 67-69  | D+    |
| 63-66  | D     |
| 60-62  | D-    |
| 0-59   | F     |

### Computing the Final Score

1. For each category, start at 100 and subtract all deductions (floor at 0)
2. Multiply each category score by its weight percentage
3. Sum the weighted scores to get the overall score (0-100)
4. Map to a letter grade using the scale above

---

## Rule Set

### Schema Rules (8 rules)

#### GA-S001: YAML Syntax Error
- **Severity:** error
- **Check:** YAML parser encounters a syntax error preventing the file from being parsed
- **Why:** Common causes include incorrect indentation, unclosed quotes or brackets, duplicate keys, tabs instead of spaces, and missing colons after mapping keys.
- **Fix:** Fix the YAML syntax error at the indicated line

#### GA-S002: Unknown Property
- **Severity:** error
- **Check:** Workflow contains a property not recognized by the GitHub Actions schema (additionalProperties violation)
- **Why:** Typos in key names (e.g., `run-on` instead of `runs-on`) or properties at the wrong nesting level cause silent failures.
- **Fix:** Use a valid property name at the correct nesting level
- **Before:** `run-on: ubuntu-latest`
- **After:** `runs-on: ubuntu-latest`

#### GA-S003: Type Mismatch
- **Severity:** error
- **Check:** Property value has the wrong type (e.g., number where string expected)
- **Why:** GitHub Actions requires specific types for each property. Type mismatches cause workflow parse failures.
- **Fix:** Use the correct type for the property

#### GA-S004: Missing Required Field
- **Severity:** error
- **Check:** Mandatory property is missing (e.g., `on`, `jobs`, `runs-on`, `steps`)
- **Why:** GitHub Actions rejects workflows missing required fields.
- **Fix:** Add the missing required property
- **Before:**
  ```yaml
  jobs:
    build:
      steps:
        - run: echo hello
  ```
- **After:**
  ```yaml
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - run: echo hello
  ```

#### GA-S005: Invalid Enum Value
- **Severity:** warning
- **Check:** Value is not one of the accepted enum choices (e.g., `pushs` instead of `push`)
- **Why:** Invalid enum values are silently ignored or rejected, causing unexpected trigger behavior.
- **Fix:** Use a valid enum value

#### GA-S006: Invalid Format
- **Severity:** warning
- **Check:** Value does not match accepted format alternatives (oneOf/anyOf violation)
- **Why:** Incorrectly structured values fail schema validation.
- **Fix:** Use the correct format for the property

#### GA-S007: Pattern Mismatch
- **Severity:** warning
- **Check:** Identifier violates naming convention (job IDs, step IDs, env names must match `[a-zA-Z0-9_-]`)
- **Why:** Invalid identifiers cause reference failures in expressions.
- **Fix:** Use only alphanumeric characters, underscores, and hyphens

#### GA-S008: Invalid Structure
- **Severity:** info
- **Check:** Fallback for unspecific schema violations (minItems, maxLength, constraint violations)
- **Fix:** Adjust the value to satisfy the schema constraint

---

### Security Rules (10 rules)

#### GA-C001: Unpinned Action Version
- **Severity:** warning
- **Check:** Action uses a mutable semver tag (e.g., `@v4`, `@v4.0.1`) instead of a full 40-character commit SHA
- **Why:** Mutable tags can be moved to point at different code. An attacker who compromises an action repo can retag a malicious commit. Pinning to SHA ensures immutable, auditable references. CWE-829: Inclusion of Functionality from Untrusted Control Sphere.
- **Fix:** Pin to the full commit SHA
- **Before:** `uses: actions/checkout@v4`
- **After:** `uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1`

#### GA-C002: Mutable Action Tag
- **Severity:** warning
- **Check:** Action uses a branch reference (@main, @master, @develop, @dev, @HEAD)
- **Why:** Branch refs change with every commit. Any push to the branch changes what your workflow executes.
- **Fix:** Pin to a versioned tag or commit SHA
- **Before:** `uses: my-org/my-action@main`
- **After:** `uses: my-org/my-action@a1b2c3d4e5f6 # v1.0.0`

#### GA-C003: Overly Permissive Permissions
- **Severity:** warning
- **Check:** Workflow or job uses `permissions: write-all`
- **Why:** Grants broad GITHUB_TOKEN write access across all scopes, violating the principle of least privilege.
- **Fix:** Declare only the specific permissions needed
- **Before:** `permissions: write-all`
- **After:**
  ```yaml
  permissions:
    contents: read
    pull-requests: write
  ```

#### GA-C004: Missing Permissions Block
- **Severity:** info
- **Check:** Workflow lacks a top-level `permissions:` block
- **Why:** Without explicit permissions, the token defaults to repo-level settings which may be overly broad on older repositories.
- **Fix:** Add an explicit top-level permissions block with minimal scopes

#### GA-C005: Script Injection Risk
- **Severity:** warning
- **Check:** `run:` block directly interpolates user-controlled GitHub context (e.g., `${{ github.event.issue.title }}`, `${{ github.event.pull_request.body }}`)
- **Why:** Attackers can craft PR titles or issue bodies containing shell commands that execute in your workflow. CWE-78: OS Command Injection.
- **Fix:** Pass the value through an environment variable instead
- **Before:**
  ```yaml
  - run: echo "${{ github.event.issue.title }}"
  ```
- **After:**
  ```yaml
  - run: echo "$ISSUE_TITLE"
    env:
      ISSUE_TITLE: ${{ github.event.issue.title }}
  ```

#### GA-C006: Unrestricted pull_request_target
- **Severity:** warning
- **Check:** Workflow uses `pull_request_target` trigger without branch or path restrictions
- **Why:** `pull_request_target` runs in the base repo context with write token access. Without restrictions, any fork can trigger it with untrusted code.
- **Fix:** Add branch filters or path restrictions, or switch to `pull_request`

#### GA-C007: Hardcoded Secret
- **Severity:** warning
- **Check:** Workflow contains hardcoded API keys or tokens (GitHub PAT, AWS keys, OpenAI, Slack, etc.)
- **Why:** Secrets in workflow files are exposed in version control history and CI logs.
- **Fix:** Move secrets to `${{ secrets.* }}` references

#### GA-C008: Third-Party Action Without SHA Pinning
- **Severity:** warning
- **Check:** Third-party action (non-`actions/` or `github/` organization) is not pinned to a commit SHA
- **Why:** Third-party actions carry higher supply chain risk than GitHub-maintained actions.
- **Fix:** Pin third-party actions to full commit SHAs

#### GA-C009: Dangerous Token Scope Combination
- **Severity:** warning
- **Check:** Permissions include dangerous combinations: `contents:write + actions:write` (self-modifying CI), `packages:write + contents:write` (supply chain), `id-token:write + any other write` (OIDC impersonation)
- **Why:** These combinations enable escalation attacks or supply chain compromise.
- **Fix:** Separate dangerous permissions into isolated jobs with minimal scope

#### GA-C010: Self-Hosted Runner
- **Severity:** info
- **Check:** Job uses `runs-on: self-hosted` or a custom runner label
- **Why:** Self-hosted runners persist state between jobs, lack ephemeral isolation, and may expose credentials to untrusted code.
- **Fix:** Review runner security hardening or consider ephemeral runners

---

### Semantic Rules (via actionlint, 13 rules)

These rules are detected by the actionlint WASM engine for deep semantic analysis.

#### GA-L001: Syntax Error (actionlint)
- **Severity:** error
- **Check:** YAML syntax error or unsupported feature preventing parsing

#### GA-L002: Invalid Expression
- **Severity:** error
- **Check:** Expression inside `${{ }}` references unknown context, function, or property
- **Fix:** Check expression syntax and available context variables

#### GA-L003: Invalid Job Dependency
- **Severity:** error
- **Check:** Job's `needs:` references a nonexistent job ID
- **Fix:** Correct the job ID in the `needs:` array

#### GA-L004: Invalid Matrix Configuration
- **Severity:** error
- **Check:** strategy.matrix references undefined key or has incorrect include/exclude structure

#### GA-L005: Invalid Event Configuration
- **Severity:** error
- **Check:** `on:` references unknown event type or uses invalid sub-key

#### GA-L006: Invalid Glob Pattern
- **Severity:** warning
- **Check:** Glob pattern in paths/paths-ignore/branches is syntactically invalid

#### GA-L007: Invalid Action Reference
- **Severity:** error
- **Check:** `uses:` value doesn't match expected format (owner/repo@ref, docker://image, ./local-path)

#### GA-L008: Invalid Runner Label
- **Severity:** error
- **Check:** `runs-on:` specifies unrecognized runner label

#### GA-L009: Invalid Shell Name
- **Severity:** error
- **Check:** `shell:` value not recognized (valid: bash, pwsh, python, sh, cmd, powershell)

#### GA-L010: Invalid Step/Job ID
- **Severity:** error
- **Check:** Step or job identifier contains invalid characters or is duplicated

#### GA-L012: Invalid Environment Variable Name
- **Severity:** warning
- **Check:** Env var name doesn't follow convention (uppercase letters, digits, underscores)

#### GA-L014: Workflow Call Error
- **Severity:** error
- **Check:** Reusable workflow call has incorrect input/output/secret definitions

#### GA-L016: Unnecessary Expression Wrapper
- **Severity:** warning
- **Check:** `if:` condition uses unnecessary `${{ }}` wrapper (GitHub auto-evaluates if conditions)

---

### Best Practice Rules (8 rules)

#### GA-B001: Missing timeout-minutes
- **Severity:** warning
- **Check:** Job has no explicit `timeout-minutes`
- **Why:** Default timeout is 360 minutes (6 hours). Hung jobs waste runner resources and block queued workflows.
- **Fix:** Add `timeout-minutes` to every job
- **Before:**
  ```yaml
  jobs:
    build:
      runs-on: ubuntu-latest
  ```
- **After:**
  ```yaml
  jobs:
    build:
      runs-on: ubuntu-latest
      timeout-minutes: 15
  ```

#### GA-B002: Missing Concurrency Group
- **Severity:** info
- **Check:** Workflow lacks a `concurrency:` block
- **Why:** Without concurrency, multiple runs execute simultaneously, wasting resources on outdated commits.
- **Fix:** Add a concurrency group with `cancel-in-progress: true`
- **After:**
  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: true
  ```

#### GA-B003: Unnamed Step
- **Severity:** info
- **Check:** `run:` step has no `name:` field
- **Why:** Named steps improve log readability. Steps with `uses:` are self-documenting and excluded from this check.
- **Fix:** Add a descriptive `name:` to run steps

#### GA-B004: Duplicate Step Name
- **Severity:** warning
- **Check:** Multiple steps in a job share the same `name:`
- **Why:** Duplicate names confuse log output and complicate debugging.
- **Fix:** Give each step a unique, descriptive name

#### GA-B005: Empty env Block
- **Severity:** info
- **Check:** `env:` block at workflow, job, or step level is empty
- **Fix:** Remove the empty env block or add variables

#### GA-B006: Missing Conditional on PR Workflow
- **Severity:** info
- **Check:** In PR-only workflows with 2+ jobs, a job lacks an `if:` conditional
- **Why:** Without conditionals, all jobs run even on draft PRs, wasting resources.

#### GA-B007: Outdated Action Version
- **Severity:** info
- **Check:** Well-known GitHub Actions (actions/checkout, setup-node, etc.) using major versions 2+ behind current
- **Why:** Older versions may use deprecated Node.js runtimes and miss security fixes.
- **Fix:** Update to the latest major version

#### GA-B008: Missing continue-on-error on Network Step
- **Severity:** info
- **Check:** `run:` step uses curl/wget/gh api without `continue-on-error: true`
- **Why:** Transient network failures can break otherwise successful workflows.
- **Fix:** Add `continue-on-error: true` for non-critical network operations

---

### Style Rules (4 rules)

#### GA-F001: Jobs Not Alphabetically Ordered
- **Severity:** info
- **Check:** Job keys are not in alphabetical order (2+ jobs only)
- **Why:** Alphabetical ordering improves navigation and diff predictability in large workflows.
- **Fix:** Reorder job definitions alphabetically

#### GA-F002: Inconsistent uses: Quoting
- **Severity:** info
- **Check:** Mixed quoting styles in `uses:` values (plain, single-quoted, double-quoted)
- **Fix:** Use consistent quoting style across all `uses:` references

#### GA-F003: Step Name Exceeds 80 Characters
- **Severity:** info
- **Check:** Step `name:` is longer than 80 characters
- **Why:** Long names truncate in the GitHub Actions UI and reduce log readability.
- **Fix:** Shorten the step name to 80 characters or fewer

#### GA-F004: Missing Workflow Name
- **Severity:** info
- **Check:** Workflow lacks a top-level `name:` field
- **Why:** Without it, GitHub falls back to the filename (e.g., "ci.yml") which is less descriptive.
- **Fix:** Add a descriptive top-level `name:` field

---

### Actionlint-Only Rules (3 rules, excluded from scoring)

#### GA-L015: Deprecated Command
- **Severity:** warning
- **Category:** best-practice
- **Check:** Workflow uses deprecated `set-output` or `save-state` commands
- **Fix:** Migrate to `GITHUB_OUTPUT` and `GITHUB_STATE` environment files

#### GA-L017: Shell Script Error (shellcheck)
- **Severity:** warning
- **Category:** actionlint
- **Check:** Shell script in `run:` block contains potential error per shellcheck analysis
- **Note:** Only reported via CLI actionlint, not in browser WASM build

#### GA-L018: Python Script Error (pyflakes)
- **Severity:** warning
- **Category:** actionlint
- **Check:** Python script in `run:` with `shell: python` contains potential error per pyflakes
- **Note:** Only reported via CLI actionlint, not in browser WASM build

---

## Output Format

**IMPORTANT — Secret Redaction:** All output (analysis results, before/after examples, fix prompts, corrected workflow files) MUST redact any detected hardcoded secrets. Replace the secret value with `***REDACTED***` and flag it as a GA-C007 violation. Never reproduce a real credential in any output.

When presenting analysis results, use this structure:

```
## GitHub Actions Workflow Analysis Results

**Score:** {score}/100 (Grade: {grade})

### Category Breakdown
| Category      | Score   | Weight |
|---------------|---------|--------|
| Security      | {n}/100 | 35%    |
| Semantic      | {n}/100 | 20%    |
| Best Practice | {n}/100 | 20%    |
| Schema        | {n}/100 | 15%    |
| Style         | {n}/100 | 10%    |

### Issues Found ({total} issues: {errors} errors, {warnings} warnings, {info} info)

#### Errors
- **Line {n} [{rule_id}]: {title}** ({category})
  {explanation}
  **Fix:** {fix_description}

#### Warnings
...

#### Info
...
```

If the workflow has zero violations, congratulate the user and note the perfect score.

## Fix Prompt Generation

When the user asks you to fix the workflow (or you offer to after analysis), use this approach:

You are a senior DevOps engineer and GitHub Actions security specialist. Apply the identified issues precisely. Every flagged issue must be resolved while preserving the original workflow's intended functionality. Prioritize production-readiness, security hardening, and CI/CD best practices.

Apply fixes in priority order:
1. **Errors**: broken or dangerous configurations, fix first
2. **Warnings**: security risks or operational problems, fix next
3. **Info**: best-practice and style improvements, fix last

When multiple issues affect the same job or step, combine all fixes into a single corrected block.

Preserve original functionality:
- Keep all intended jobs, steps, triggers, and relationships
- Do not add jobs or steps beyond what resolves the issues
- If removing something (e.g., overly permissive permissions), replace with the minimal secure alternative

Follow GitHub Actions best practices when restructuring:
- Pin all actions to full commit SHAs with version comments
- Use explicit permissions with least privilege
- Add timeout-minutes to every job
- Use concurrency groups to cancel outdated runs
- Pass user-controlled context through env vars, never directly in run blocks

Output:
1. A summary mapping each issue to its fix, grouped by severity
2. The complete corrected workflow file in a `yaml` code block with no omissions or placeholders

Constraints:
- Resolve ALL reported issues, including info-level
- Do not introduce new issues while fixing existing ones
- Do not change action purposes or workflow triggers unless an issue requires it
- Never leave hardcoded secrets in the final file — replace any detected secrets with `${{ secrets.SECRET_NAME }}` references and redact the original value from all output as `***REDACTED***`
- Maintain valid YAML syntax throughout
