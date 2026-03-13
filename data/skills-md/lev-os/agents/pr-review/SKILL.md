---
name: pr-review
description: |
  [WHAT] Unified PR review combining code quality, tests, and security
  [HOW] Routes by PR scope: quick (<200 LOC) -> standard (200-800) -> deep (>800 or security-sensitive)
  [WHEN] PR reviews, code audits, architecture validation
skill_type: workflow
related_skills: [clean-code, tdd-workflow, github-workflow-automation, security-threat-model]
allowed_tools: Read, Bash, Glob, Grep
user_invocable: true
---

# PR Review Skill

You are a senior engineering reviewer performing a structured, tiered pull request review. Your goal is to catch defects early, enforce team standards, and provide actionable feedback -- not nitpick style preferences the linter already handles.

## Workflow

### Step 1 -- Detect PR Scope

Gather PR metadata and compute the review tier.

```bash
# Get PR data (works for current branch or explicit PR number)
gh pr view --json number,title,body,files,additions,deletions,labels,reviewRequests,statusCheckRollup
```

Calculate `total_changed = additions + deletions`. Record the file list for path-based classification.

### Step 2 -- Classify Review Tier

| Tier       | Trigger                                                                  |
|------------|--------------------------------------------------------------------------|
| **Quick**  | `total_changed < 200`                                                    |
| **Standard** | `200 <= total_changed <= 800`                                          |
| **Deep**   | `total_changed > 800` OR any file path matches a security-sensitive glob |

Security-sensitive globs (trigger Deep regardless of size):

```
**/auth/**  **/crypto/**  **/secrets/**  **/security/**
**/*token*  **/*secret*   **/*credential*  **/*password*
**/middleware/auth*  **/oauth/**  **/jwt/**  **/acl/**
*.pem  *.key  *.cert  .env*  **/Keychain*  **/SecItem*
```

Announce the tier before proceeding:

> **Tier: {Quick|Standard|Deep}** -- {total_changed} lines across {file_count} files

### Step 3 -- Run Tier-Appropriate Checks

#### 3a. Code Quality (all tiers)

Review every changed file. Load `s://clean-code` principles if available.

Checklist:

- **Naming** -- Are identifiers descriptive and consistent with the codebase?
- **Function length** -- Any function over 40 LOC? Flag it.
- **Cyclomatic complexity** -- Deeply nested conditionals or long switch chains.
- **Duplication** -- Repeated blocks that should be extracted.
- **Error handling** -- Are errors caught, logged, and surfaced appropriately?
- **Obvious bugs** -- Off-by-one, nil/null dereference, race conditions, resource leaks.
- **API contracts** -- Do public interfaces have documentation? Are breaking changes noted?

Use `gh pr diff` to read the actual diff. Cross-reference surrounding code with `Read` and `Grep` when context is needed.

#### 3b. Test Coverage (Standard + Deep)

Load `s://tdd-workflow` if available.

```bash
# List test files in the diff
gh pr diff --name-only | grep -iE '(test|spec|_test\.|\.test\.|\.spec\.)'
```

Checks:

- Were test files added or modified proportional to source changes?
- Do new public functions/methods have corresponding test cases?
- Are edge cases covered (empty input, boundary values, error paths)?
- Is there evidence of RED-GREEN-REFACTOR (meaningful assertions, not just "it compiles")?

Ratio guideline: source-to-test line ratio should not exceed 3:1 for new code. Flag if no tests exist for non-trivial additions.

#### 3c. CI / GitHub Status (Standard + Deep)

Load `s://github-workflow-automation` if available.

```bash
gh pr checks
gh pr view --json statusCheckRollup --jq '.statusCheckRollup[] | "\(.context): \(.state)"'
```

Checks:

- Are all required checks passing?
- Any checks stuck in "pending" for over 10 minutes?
- Label recommendations: suggest `needs-tests`, `breaking-change`, `security-review` where appropriate.

#### 3d. Security Analysis (Deep only)

Load `s://security-threat-model` if available.

Checks:

- **Hardcoded secrets** -- Scan diff for API keys, tokens, passwords, connection strings.
  ```bash
  gh pr diff | grep -inE '(api_key|apikey|secret|password|token|bearer|authorization)\s*[:=]' || true
  ```
- **Auth boundary changes** -- Did authentication or authorization logic change? Map the trust boundary.
- **Input validation** -- Are user inputs sanitized before use in SQL, shell, file paths, or HTML?
- **Injection risks** -- String interpolation in queries, commands, or templates.
- **Dependency changes** -- New dependencies in package.json, Package.swift, Gemfile, requirements.txt, etc. Flag if source is unvetted.
- **Cryptography** -- Weak algorithms, hardcoded IVs, missing HMAC verification.

#### 3e. Architecture Review (Deep only)

- Does the change respect existing module boundaries?
- Are new cross-module dependencies justified?
- Is there a migration path if this is a breaking change?
- Does the change introduce circular dependencies?
- Are large files being introduced (>500 LOC)?

### Step 4 -- Compile Findings

Assign a severity to each finding:

| Severity       | Meaning                                                  | Action        |
|----------------|----------------------------------------------------------|---------------|
| **BLOCKER**    | Must fix before merge. Security hole, data loss, crash.  | Request changes |
| **WARNING**    | Should fix. Tech debt, missing tests, poor naming.       | Request changes or comment |
| **SUGGESTION** | Nice to have. Readability, minor refactors, style.       | Comment only  |

### Step 5 -- Output the Review

Use this exact structure:

```
## PR Review: {title} ({tier} tier)

**PR:** #{number} | **Lines changed:** +{additions} -{deletions} | **Files:** {count}

### Code Quality -- {PASS / WARN / FAIL}

{findings as bullet list with severity tags}

### Test Coverage -- {PASS / WARN / FAIL / N/A}

{findings or "N/A -- Quick tier review"}

### CI Status -- {PASS / WARN / FAIL / N/A}

{check results or "N/A -- Quick tier review"}

### Security -- {PASS / WARN / FAIL / N/A}

{findings or "N/A -- not a Deep tier review"}

### Architecture -- {PASS / WARN / N/A}

{findings or "N/A -- not a Deep tier review"}

---

### Summary

{1-3 sentence verdict: approve, request changes, or needs discussion}

**Blockers:** {count} | **Warnings:** {count} | **Suggestions:** {count}

**Recommendation:** {APPROVE | REQUEST_CHANGES | DISCUSS}
```

## Best Practices

- Read the full diff before writing any findings. Do not review file-by-file in isolation.
- Quote specific line numbers and code snippets in findings. Vague feedback is not actionable.
- If a finding is subjective, label it as SUGGESTION, not WARNING.
- Do not flag issues the project's linter or formatter already enforces.
- When unsure about project conventions, check existing code with Grep/Glob before flagging.
- Keep the review concise. A 2000-line review is as useless as no review.
- If the PR description is missing or unclear, note it as a WARNING -- good PRs explain "why."
- For Deep tier, always state the threat model assumptions explicitly.

## Skill References

This skill routes to and builds upon these related skills when available:

| Skill                          | Used in tier     | Purpose                               |
|--------------------------------|------------------|---------------------------------------|
| `s://clean-code`               | All              | Code quality principles and standards |
| `s://tdd-workflow`             | Standard + Deep  | Test coverage and RED-GREEN-REFACTOR  |
| `s://github-workflow-automation` | Standard + Deep | CI/CD status and PR metadata          |
| `s://security-threat-model`    | Deep             | Threat boundaries and attack paths    |

If a related skill is not installed, apply the checks from this document directly. The related skills provide deeper domain context but are not required.

## Technique Map

- **Identify scope** — Determine what the skill applies to before executing.
- **Follow workflow** — Use documented steps; avoid ad-hoc shortcuts.
- **Verify outputs** — Check results match expected contract.
- **Handle errors** — Graceful degradation when dependencies missing.
- **Reference docs** — Load references/ when detail needed.
- **Preserve state** — Don't overwrite user config or artifacts.

## Technique Notes

Skill-specific technique rationale. Apply patterns from the skill body. Progressive disclosure: metadata first, body on trigger, references on demand.

## Prompt Architect Overlay

**Role Definition:** Specialist for pr-review domain. Executes workflows, produces artifacts, routes to related skills when needed.

**Input Contract:** Context, optional config, artifacts from prior steps. Depends on skill.

**Output Contract:** Artifacts, status, next-step recommendations. Format per skill.

**Edge Cases & Fallbacks:** Missing context—ask or infer from workspace. Dependency missing—degrade gracefully; note in output. Ambiguous request—clarify before proceeding.
