---
name: debug-workflow
description: "Debug GitHub Agentic Workflow runs using gh-aw CLI tools to investigate failures, analyze logs, identify MCP server issues, and troubleshoot workflow execution problems. Use when: (1) Investigating workflow run failures or unexpected behavior, (2) Analyzing workflow execution logs, (3) Debugging MCP server connectivity or tool availability issues, (4) Creating issues to document workflow problems, (5) Understanding why a successful workflow didn't produce expected results, (6) Examining firewall blocks or network issues in workflows"
---

# Workflow Debugging

Debug agentic workflow runs using `gh aw audit` and `gh aw logs` commands.

## Core Commands

### Audit a Specific Run

Investigate a single workflow run with comprehensive error detection:

```bash
gh aw audit <run-id-or-url> --parse -v
```

**Accepts:**
- Numeric run ID: `21005890162`
- GitHub Actions URL: `https://github.com/owner/repo/actions/runs/21005890162`
- Job URL: `https://github.com/owner/repo/actions/runs/21005890162/job/9876543210`
- Job URL with step: `https://github.com/owner/repo/actions/runs/21005890162/job/9876543210#step:7:1`

**What it does:**
- Downloads artifacts and logs to `.github/aw/logs/run-<id>/`
- Detects errors and warnings
- Analyzes MCP tool usage statistics
- Generates detailed Markdown report
- Extracts specific step output (if job URL with step)

**Output location:** `.github/aw/logs/run-<run-id>/`

### Download Multiple Runs

Analyze patterns across multiple workflow executions:

```bash
gh aw logs [workflow] --count <N> --parse
```

**Common options:**
- `--count 10` - Download last 10 runs
- `--start-date -1w` - Last week's runs
- `--end-date -1d` - Until yesterday
- `--engine claude` - Filter by engine (claude/codex/copilot)
- `--firewall` - Filter runs with firewall enabled
- `--safe-output create-issue` - Filter by safe output type
- `--parse` - Generate Markdown reports
- `--json` - JSON output format

**Output location:** `.github/aw/logs/` (configurable with `-o`)

## Debugging Workflow

### Step 1: Audit the Run

Start with the audit command to get a comprehensive overview:

```bash
gh aw audit <run-url> --parse -v
```

Review the generated report for:
- ✅ Success indicators
- 🟡 Warnings
- ❌ Errors
- Token usage and performance metrics
- Job status and duration
- Tool usage statistics

### Step 2: Examine Logs

Navigate to the downloaded logs:

```bash
cd .github/aw/logs/run-<id>/
```

**Key files:**
- `agent-stdio.log` - Full agent execution log (search here for errors)
- `aw_info.json` - Workflow metadata and configuration
- `workflow-logs/` - GitHub Actions job logs
- `mcp-logs/gateway.md` - MCP Gateway status and requests
- `mcp-logs/mcp-gateway.log` - Raw MCP Gateway logs
- `sandbox/firewall/logs/access.log` - Firewall access logs (if enabled)
- `safe_output.jsonl` - Agent's final output (if available)

### Step 3: Search for Common Issues

Use the quick scan script for rapid error detection:

```bash
python3 scripts/quick_scan.py .github/aw/logs/run-<id>/
```

Or search manually for specific patterns:

**MCP server failures:**
```bash
grep -E "mcp:.*failed" agent-stdio.log
```

**DNS resolution errors:**
```bash
grep "dns error.*Name does not resolve" agent-stdio.log
```

**OAuth/authentication issues:**
```bash
grep "WARN codex_rmcp_client::oauth" agent-stdio.log
```

**Tool availability errors:**
```bash
grep -i "tool.*not available\|tool.*failed" agent-stdio.log
```

**Firewall blocks:**
```bash
grep "TCP_DENIED" sandbox/firewall/logs/access.log
```

### Step 4: Check MCP Gateway

Review MCP Gateway logs to verify server connectivity:

```bash
cat mcp-logs/gateway.md
```

Look for:
- ✓ Successfully loaded servers
- 🔍 RPC request/response pairs
- ⚠️ HTTP errors (404, 500, etc.)
- ✓ Tools list responses

### Step 5: Analyze Root Cause

Consult the common errors reference for known patterns:

```bash
cat references/common_errors.md
```

This document catalogs:
- MCP server failures (DNS, OAuth, session)
- Firewall issues
- Agent execution errors
- GitHub Actions problems

### Step 6: Document Findings

Create an issue to document the problem:

```bash
gh issue create \
  --repo <owner/repo> \
  --title "<concise-issue-title>" \
  --body "<detailed-description>"
```

Include:
- Workflow run URL
- Summary of the issue
- Evidence from logs (error messages)
- Root cause analysis
- Impact assessment
- Reproduction steps
- Suggested fixes

## Common Patterns

### Silent MCP Failures

**Symptom:** Workflow shows green but agent couldn't use MCP tools

**Detection:**
```bash
gh aw audit <run-id> -v
grep -E "mcp:.*failed" .github/aw/logs/run-<id>/agent-stdio.log
```

**Causes:**
- DNS resolution failure (`host.docker.internal`)
- OAuth token issues
- MCP Gateway not reachable
- Session not found errors

**Reference:** See `references/common_errors.md` for detailed patterns

### False Success

**Symptom:** Workflow completed successfully but didn't produce expected results

**Investigation:**
1. Check for MCP server failures (tools unavailable)
2. Check for firewall blocks (network requests failed)
3. Review agent output for errors
4. Verify safe outputs were created

### Network Issues

**Detection:**
```bash
grep "TCP_DENIED\|TAG_NONE" sandbox/firewall/logs/access.log
```

**Causes:**
- Domain not in firewall allowlist
- DNS resolution through proxy failed
- Network timeout

## Tips

**Green doesn't mean success:** Always audit the logs even if the workflow shows as successful. Many failures are silent.

**Use audit first:** The audit command provides a comprehensive overview and is faster than manually downloading and examining logs.

**Check all MCP servers:** If one MCP server fails, check if others also failed—this indicates a systemic issue like DNS or networking.

**Firewall logs are crucial:** When debugging network issues, always check firewall access logs for blocked domains.

**Look for patterns:** Use the logs command to download multiple runs and identify patterns across executions.

**Reference common errors:** Before deep investigation, check `references/common_errors.md` for known patterns and solutions.

## Resources

### scripts/quick_scan.py

Rapid error detection script that scans for common issues:
- MCP server failures
- DNS resolution errors
- OAuth/keyring warnings
- Tool availability errors
- Firewall blocks
- MCP Gateway session errors

Usage:
```bash
python3 scripts/quick_scan.py <log-directory>
```

### references/common_errors.md

Comprehensive catalog of common error patterns with:
- Error signatures and patterns
- Search commands for detection
- Root cause explanations
- Impact assessments
- Known symptoms
