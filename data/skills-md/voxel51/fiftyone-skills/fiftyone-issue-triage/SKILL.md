---
name: fiftyone-issue-triage
description: Triages FiftyOne GitHub issues by categorizing as fixed, won't fix, not reproducible, or still valid. Use when reviewing GitHub issues, triaging bugs, or closing stale issues in the voxel51/fiftyone repository.
---

# FiftyOne Issue Triage

## Categories

| Category | When to Use |
|----------|-------------|
| **Already Fixed** | Resolved in recent commits/releases |
| **Won't Fix** | By design, out of scope, or external behavior (browser, OS, third-party) |
| **Not Reproducible** | Cannot reproduce with provided info |
| **No Longer Relevant** | Outdated version, deprecated feature, or stale (6+ months) |
| **Still Valid** | Confirmed bug or valid feature request needing work |

## Workflow

### 1. Fetch Issue
```bash
gh issue view {number} --repo voxel51/fiftyone --json title,body,author,state,labels,comments
```

### 2. Analyze
- Extract: issue type, version, reproduction steps, error message
- Search related: `gh issue list --repo voxel51/fiftyone --state all --search "keyword"`
- Check git history: `git log --oneline --grep="keyword"`

### 3. Assess Responsibility
- External behavior (browser, OS, third-party)? → Won't Fix
- User workflow/configuration issue? → Won't Fix (with workaround)
- FiftyOne code/behavior issue? → Continue assessment

### 4. Assess Value
Before proposing fixes, ask: "Is a fix worth the effort?"
- How many users affected?
- Is workaround simple?
- Would fix add complexity or hurt performance?

### 5. Check Documentation
```bash
grep -r "keyword" docs/source/ --include="*.rst"
```

### 6. Categorize and Respond

## Quick Reference

| Category | Key Indicator | Action |
|----------|---------------|--------|
| Already Fixed | Found in git log | Point to PR, suggest upgrade |
| Won't Fix | External/by design | Explain, provide workaround |
| Not Reproducible | Can't reproduce | Request more info |
| No Longer Relevant | Old/stale/deprecated | Explain, suggest new issue |
| Still Valid | Confirmed, no fix | Document root cause, propose fix |

## Response Tone

Always start with thanks, be friendly, then explain. Keep responses simple (no internal code details).

## If User Willing to Contribute

- **Contribution guide:** https://docs.voxel51.com/contribute/index.html
- **Discord:** https://discord.com/invite/fiftyone-community (#github-contribution channel)
- Point to relevant code files for the fix
