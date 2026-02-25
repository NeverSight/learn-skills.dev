---
name: amp-team-usage
description: Amp Team Usage
version: 1.0.0
---

# Amp Team Usage

Check concurrent users and team members on an Amp account.

## Problem

Amp CLI has no direct command for viewing team/workspace members or concurrent sessions. The web dashboard requires manual login.

## Solution

### 1. Local Concurrent Sessions

Count running Amp processes on the local machine:

```bash
ps aux | grep -E 'amp.*dist/main.js' | grep -v grep | wc -l
```

Detailed view:

```bash
ps aux | grep -E 'amp.*dist/main.js' | grep -v grep
```

### 2. Team Members via GitHub CLI

If Amp workspace is linked to a GitHub org:

```bash
# List org members
gh api orgs/YOUR_ORG/members | jq -r '.[].login'

# Full details with GraphQL
gh api graphql -f query='
{
  organization(login: "YOUR_ORG") {
    membersWithRole(first: 50) {
      totalCount
      nodes {
        login
        name
      }
    }
  }
}' | jq
```

### 3. Recent Thread Activity

Check thread activity across the account:

```bash
# Use find_thread tool with date filters
find_thread query="after:1d" limit=50
```

## What Didn't Work

- `amp --help` has no team/account commands
- `amp workspace list`, `amp team list`, `amp account` don't exist
- Direct API calls to `ampcode.com/api/team` require browser auth
- Playwright login requires interactive Google OAuth

## Quick Reference

| Method | Command |
|--------|---------|
| Local sessions | `ps aux \| grep 'amp.*main.js' \| grep -v grep \| wc -l` |
| Org members | `gh api orgs/ORG/members \| jq '.[].login'` |
| Member count | `gh api graphql -f query='{organization(login:"ORG"){membersWithRole{totalCount}}}'` |



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 8. Degeneracy

**Concepts**: redundancy, fallback, multiple strategies, robustness

### GF(3) Balanced Triad

```
amp-team-usage (○) + SDF.Ch8 (−) + [balancer] (+) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)


### Connection Pattern

Degeneracy provides fallbacks. This skill offers redundant strategies.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.