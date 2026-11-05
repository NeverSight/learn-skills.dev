---
name: cicd-security
description: CI/CD pipeline security hunting — GitHub Actions workflow injection, secret exfiltration, self-hosted runner poisoning, dependency confusion, OIDC token theft, and supply chain attacks. Covers sisakulint scanning, manual workflow analysis, and chaining CI/CD bugs into critical findings. Use when a target has public repos, GitHub Actions, CircleCI, Jenkins, or GitLab CI.
---

# CI/CD SECURITY — Pipeline Attack Surface

## Overview

> CI/CD pipelines are high-value targets — a single workflow injection can give you code execution on the build server, read ALL org secrets, and push backdoored releases to production.

This skill hunts CI/CD vulnerabilities in public repositories: script injection
through GitHub Actions contexts, `pull_request_target` misuse, secret
exfiltration paths, self-hosted runner poisoning, OIDC token abuse, dependency
confusion, and unpinned actions. Workflow `scan-workflows` runs the automated
scan; the runbooks cover manual analysis of each bug class.

## Quick Reference

### Quick kill checklist

```
[ ] Run cicd_scanner.sh <owner/repo> — catch low-hanging workflow lint issues
[ ] Check for script injection: ${{ github.event.*.body/title/name }}
[ ] Find secrets referenced in env: — test if they leak in logs
[ ] Check pull_request_target with checkout of untrusted code
[ ] Look for self-hosted runners on public repos
[ ] Search for OIDC token requests without audience restriction
[ ] Check for unpinned actions (uses: owner/action@main)
[ ] Look for workflow_dispatch with no input validation
[ ] Find artifact downloads without integrity checks
[ ] Search for GITHUB_TOKEN with write permission used insecurely
```

### Injectable contexts (always check these)

```
github.event.pull_request.title
github.event.pull_request.body
github.event.pull_request.head.ref        ← branch names
github.event.issue.title
github.event.issue.body
github.event.comment.body
github.event.review.body
github.event.review_comment.body
github.event.discussion.title
github.event.discussion.body
github.head_ref                            ← alias for branch name
github.event.inputs.*                      ← workflow_dispatch inputs
```

### Bug class table

| Bug | Trigger | Severity | CVSS Range |
|-----|---------|----------|-----------|
| Workflow injection via PR title | `${{ github.event.pull_request.title }}` in `run:` | Critical | 9.0–10.0 |
| `pull_request_target` + checkout | Accepts PRs from forks | Critical | 9.0–10.0 |
| Self-hosted runner on public repo | `runs-on: self-hosted` + public repo | High | 7.5–9.0 |
| OIDC trust too broad | Any-branch/any-repo claim | High | 7.5–8.5 |
| Secret in log | `echo ${{ secrets.X }}` | Medium | 5.5–7.0 |
| Unpinned action | `@main` / `@v1` tag | Low–Medium | 3.0–5.5 |
| Artifact poisoning | Unsigned artifact download + exec | Medium | 5.5–7.0 |
| `GITHUB_TOKEN` write abuse | Push to protected branch | Medium | 5.5–7.0 |
| Dependency confusion | Internal pkg not on public registry | High | 7.5–9.0 |
| `workflow_dispatch` injection | Unvalidated inputs in `run:` | Medium–High | 6.0–8.0 |

## Workflow Selection

| Situation | Workflow |
|---|---|
| Scan a public repo/org's workflows | `scan-workflows` |
| Local checkout available — static injection scan | `scripts/workflow_inject_scan.py` |
| Look for hardcoded secrets in CI configs | `scripts/cicd_secret_scan.py` |
| Deep dive on a found pattern | matching runbook (injection / pull-request-target / secrets / runners) |

## Available Workflows

### scan-workflows
Scans GitHub Actions workflows for a repo or org via sisakulint (remote scan),
then runs the local static injection and secret scans on any local checkout.

```
bash .claude/skills/cicd-security/scripts/cicd_scanner.sh "${REPO:?Set REPO (owner/repo)}" \
  --output-dir $OUTDIR/cicd
```

Outputs: `$OUTDIR/cicd/scan_results.txt`, `$OUTDIR/cicd/summary.txt`. Safety tier: passive (reads public workflow files only).

## Evidence Required

| Artifact | File |
|---|---|
| Workflow file with the vulnerable pattern | `$OUTDIR/cicd/scan_results.txt` |
| Proof of injectable context (grep line) | `$OUTDIR/cicd/evidence/` |
| PoC payload used (PR title / issue title) | `evidence/<finding>/poc.sh` |
| Public repo + workflow path + line number | in finding report |

## References

- Workflow injection deep dive: `runbooks/workflow-injection.md`
- `pull_request_target` misuse: `runbooks/pull-request-target.md`
- Secret exfil patterns: `runbooks/secret-exfiltration.md`
- Self-hosted runner poisoning: `runbooks/runner-poisoning.md`
- Scope notes: most programs scope public repos only; opening a real PR to trigger a workflow requires explicit program permission
- Redaction policy: scan output stays local-only under `$OUTDIR`; redact any
  secret values surfaced by scans before committing evidence.
