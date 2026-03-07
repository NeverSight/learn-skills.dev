---
name: show-env-status
description: "Show mise environment status — tools, env vars, tasks, release readiness. TRIGGERS - mise status, mise env, repo status, environment check."
allowed-tools: Bash
argument-hint: ""
model: haiku
---

# /mise:show-env-status

Show a comprehensive overview of the current repo's mise environment.

## Output Sections

Run these commands and present the results in a formatted summary:

### 1. mise Version

```bash
mise --version
```

### 2. Installed Tools

```bash
mise ls --current 2>/dev/null
```

### 3. Environment Variables (Non-Sensitive)

```bash
# Show env vars, filtering out secrets
mise env 2>/dev/null | grep -v -i "TOKEN\|KEY\|SECRET\|PASSWORD\|CREDENTIAL" | sort
```

### 4. Available Tasks (Grouped)

```bash
mise tasks ls 2>/dev/null
```

Group the output by colon-namespace prefix (e.g., `release:`, `test:`, `cache:`).

### 5. Release Readiness

Check if the repo has release tasks configured:

```bash
# Check for release:full task
mise tasks ls 2>/dev/null | grep -q "release:full" && echo "✓ Release tasks configured" || echo "✗ No release tasks — run /mise:run-full-release to scaffold"

# Check for .releaserc.yml
ls .releaserc.yml .releaserc.json .releaserc 2>/dev/null && echo "✓ semantic-release configured" || echo "✗ No semantic-release config"

# Check GH_ACCOUNT
echo "GH_ACCOUNT: ${GH_ACCOUNT:-not set}"
```

### 6. Configuration Files

```bash
# Show which mise config files are active
ls .mise.toml mise.toml .mise/tasks/ 2>/dev/null
```

## Example Output Format

```
═══════════════════════════════════════════
  mise Environment Status: cc-skills
═══════════════════════════════════════════

Tools: node 25.0.0, bun 1.3.0, python 3.13
Account: terrylica

Tasks (32 total):
  release: full, dry, status, preflight, version, sync, verify, clean, hooks
  dev: lint, format, test

Release: ✓ Configured (release:full + .releaserc.yml)
Config: .mise.toml (42 lines)
═══════════════════════════════════════════
```
