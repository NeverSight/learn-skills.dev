---
name: code-validation
description: Automated code validation for diff review, change hygiene, and red flag detection. Use when reviewing git diffs, PRs, or changed files for test disabling patterns, secrets, path portability issues, security flags, and large deletions. Supports Python, TypeScript, JavaScript, HTML, and CSS.
---

# Code Validation

Validates code changes through automated scanning and LLM-guided heuristics to detect:
- Test disabling patterns (skip, only, todo)
- Secret exposure (hardcoded credentials, API keys)
- Path portability issues (user-specific paths)
- Dangerous security flags
- Large deletions
- Dependency/import changes
- Broad exception handling

## When to Use

Execute code-validation as part of QA validation protocol:
1. After Action Agent completes implementation
2. Before approving changes for merge
3. When reviewing diffs for red flags
4. During final validation phase

## Validation Workflow

### 1. Automated Scanning (Scripts)

Run scripts first for deterministic, fast checks:

**For Git Diffs (comparing branches):**
```bash
# Compare feature branch against main
python scripts/diff_analyzer.py --base main --format json

# Compare specific commit range
python scripts/diff_analyzer.py --range HEAD~5..HEAD --format json

# Save report to file
python scripts/diff_analyzer.py --base main --output validation-report.json
```

**For Static File Analysis (staged changes or specific files):**
```bash
# Scan specific files
python scripts/static_analyzer.py src/app.py src/utils.py --format json

# Scan entire directory
python scripts/static_analyzer.py ./src --format json

# Exclude patterns
python scripts/static_analyzer.py ./src --exclude node_modules .git --format json

# Save report
python scripts/static_analyzer.py ./src --output scan-report.json
```

### 2. Interpret Scan Results

Parse JSON output and evaluate findings:

**Finding Structure:**
```json
{
  "category": "test_disabling|secret_exposure|path_portability|security_flags|large_deletion|dependency_change",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "file": "path/to/file.py",
  "line": 42,
  "pattern": "regex pattern matched",
  "context": "actual line content",
  "message": "human-readable description"
}
```

**Severity Guidelines:**
- **CRITICAL**: Secrets, user-specific paths in docs - BLOCK merge immediately
- **HIGH**: Test disabling, security flags, user-specific paths in code - Require Action Agent fixes
- **MEDIUM**: Large deletions, dependency changes, broad exceptions - Review and justify
- **LOW**: Minor issues - Optional fixes

### 3. LLM Heuristic Review (Context-Dependent)

After automated scanning, apply human judgment for:

#### Test Assertion Weakening
Scripts cannot detect semantic changes. Manually review:
- Reduced assertion count without clear reason
- Replaced specific assertions with generic checks
- Removed edge case validations
- Changed from behavior validation to mock validation only

**Red Flags:**
```typescript
// Before
expect(response.data).toMatchObject({
  id: expect.any(String),
  status: 'active',
  count: expect.any(Number)
});

// After - WEAKENED
expect(response.data).toBeDefined(); // ❌ Lost specificity
```

#### Broad Try/Catch Appropriateness
Evaluate if exception handling is justified:
- Top-level error boundaries: Often acceptable
- Business logic: Usually inappropriate
- Missing error logging/reporting: Red flag
- Swallowing errors without assertions in tests: Red flag

**When Acceptable:**
```typescript
// Top-level boundary
app.use((err, req, res, next) => {
  logger.error(err);
  res.status(500).json({ error: 'Internal error' });
});
```

**Red Flag:**
```typescript
// Business logic swallowing errors
try {
  await processPayment(data);
} catch (e) {
  // ❌ Silent failure, no logging
}
```

#### Scope Creep vs Legitimate Refactoring
Assess if changes align with issue scope:
- Issue describes feature X, but changes include unrelated Y
- "While I was here" refactoring without issue reference
- Architecture changes not mentioned in acceptance criteria

**Legitimate:**
- Refactoring directly related to implementation
- Fixing bugs discovered during implementation (document in scratch notes)
- Updating tests to match new implementation

**Scope Creep:**
- Reformatting unrelated files
- Adding features not in issue
- Changing patterns/conventions beyond issue scope

#### Architecture Alignment
Verify changes match current production architecture:
- Check against ADRs referenced in `.project-context.md`
- Verify stack matches documented tech stack
- Confirm patterns follow project standards
- Ensure deprecated approaches aren't reintroduced

### 4. Generate Validation Report

Combine automated findings with heuristic review:

```
## Code Validation Results for [ISSUE-ID]

### Automated Scan Summary
- Files Changed: X
- Total Findings: Y
- CRITICAL: Z findings
- HIGH: A findings
- MEDIUM: B findings

### Critical Findings (BLOCK)
[List CRITICAL severity findings with file:line references]

### High Priority Findings (FIX REQUIRED)
[List HIGH severity findings]

### Heuristic Review
- Test Assertion Quality: [PASS/FAIL with specifics]
- Exception Handling: [PASS/WARN/FAIL with examples]
- Scope Alignment: [PASS/WARN/FAIL with details]
- Architecture Compliance: [PASS/FAIL with ADR references]

### Recommendation
[APPROVED | CHANGES REQUIRED | BLOCKED]

### Action Items
[Specific fixes needed with file:line references]
```

## Script Output Format

Both scripts output JSON with this structure:

```json
{
  "commit_range": "main..HEAD",
  "files_scanned": 42,
  "files_changed": 15,
  "total_findings": 8,
  "findings_by_severity": {
    "CRITICAL": 1,
    "HIGH": 3,
    "MEDIUM": 4,
    "LOW": 0
  },
  "findings": [
    {
      "category": "secret_exposure",
      "severity": "CRITICAL",
      "file": "src/config.py",
      "line": 12,
      "pattern": "...",
      "context": "API_KEY = 'sk_live_abc123...'",
      "message": "Potential hardcoded secret"
    }
  ],
  "summary": {
    "test_disabling": 2,
    "secret_exposure": 1,
    "path_portability": 3,
    "security_flags": 1,
    "dependency_changes": 1,
    "large_deletions": 0
  }
}
```

## Red Flag Categories

### Test Disabling (HIGH)
Patterns indicating tests were disabled rather than fixed:
- `.skip()`, `.only()`, `.todo()`
- `xit()`, `xdescribe()`, `fit()`, `fdescribe()`
- `@pytest.skip`, `@unittest.skip`

**Action**: Require Action Agent to fix tests or justify with comment

### Secret Exposure (CRITICAL)
Hardcoded credentials or API keys:
- API keys, tokens, passwords
- AWS credentials
- GitHub tokens
- Stripe keys

**Action**: BLOCK merge, require environment variables

### Path Portability (CRITICAL in docs, HIGH in code)
User-specific paths that won't work for other developers:
- `/Users/username/`
- `/home/username/`
- `C:\Users\username\`
- `~/Desktop`, `~/Documents`

**Action**: BLOCK if in documentation, require repo-relative paths

### Security Flags (HIGH)
Commands that weaken security:
- `--no-verify`, `--insecure`, `-k`
- `chmod 777`
- `StrictHostKeyChecking no`
- `--allow-root`

**Action**: Require justification comment or removal

### Large Deletions (MEDIUM)
Files with >100 lines removed:
- May indicate legitimate refactoring
- Could hide removed validation logic
- Might remove important error handling

**Action**: Manual review to verify deletions are intentional

### Dependency Changes (MEDIUM)
New imports or package additions:
- Track new dependencies for security review
- Verify necessity for issue scope
- Check for unnecessary additions

**Action**: Verify in package.json/requirements.txt, run security audit

## Integration with QA Protocol

Execute code-validation at **Step 3: Change Review (Diff)** in QA workflow:

1. Switch to feature branch
2. **Run code-validation scripts**
3. **Interpret automated findings**
4. **Apply LLM heuristics**
5. Continue with Claude Code Review (MCP)
6. Proceed with remaining QA steps

If CRITICAL or multiple HIGH findings:
- BLOCK validation
- Report to Traycer with specific file:line references
- Delegate to Action Agent for fixes
- Re-run validation after fixes

## Resources

- **Scripts**:
  - `scripts/diff_analyzer.py` - Analyzes git diffs for red flags
  - `scripts/static_analyzer.py` - Scans files without git context

## Notes

- Scripts are deterministic and fast; use them first
- LLM heuristics handle context-dependent evaluation
- Always provide file:line references in reports
- CRITICAL findings must block merge
- Document justified exceptions in code comments
