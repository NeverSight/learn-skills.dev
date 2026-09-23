---
name: blindspot
description: Read-only reconnaissance pass over an unfamiliar codebase, system, or feature area to surface hidden risks before any code is written. Use when starting work in unfamiliar territory, before a risky change, or when the user says "blindspot pass", "what am I missing", or "scan for risks".
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Blindspot Pass

Find the unknowns in a system BEFORE touching it. Reconnaissance only.

<HARD-RULE>Read-only. Do not edit, create, or delete any project file. No fixes, however tempting.</HARD-RULE>

Tip for the user (mention once at the start): running this pass in plan mode or
a read-only permission mode makes the rule enforced by the harness, not just
promised by the model.

## Process

1. **Identify the target.** Use the argument or infer the directory/system/feature
   from conversation. If no target is discernible, ask for one — don't guess.
2. **Name the domain, derive its dangerous paths.** Before scanning, state in
   one line what kind of system the target is, and list the 2–3 failure classes
   that domain actually bleeds from. The generic list below is a backend-shaped
   floor, not a ceiling — a native UI app bleeds from accessibility gaps,
   lifecycle/identity bugs, and state-restoration loss; a data pipeline from
   loss, duplication, and ordering; a CLI from argument edge cases and exit
   codes. Findings should come from the derived list first.
3. **Explore.** Use the agent's file-search/read tools (Glob/Grep/Read,
   `rg`/`find`/`cat`, or equivalent) and git log for churn hotspots to understand
   the target. Look for the domain-derived risks from step 2, plus:
   - Hidden coupling: modules that import each other's internals, shared mutable
     state, implicit ordering dependencies
   - Unowned edge cases: error paths that swallow exceptions, TODO/FIXME/HACK
     comments, empty catch blocks
   - Stale assumptions: config or constants that encode outdated facts, comments
     contradicting code, dead feature flags
   - Missing tests around dangerous paths: money, auth, deletion, migrations,
     concurrency — anything irreversible with no test coverage
   - Churn hotspots: files with many recent fixes
     (`git log --oneline --no-merges -- <path>`, ignoring generated files:
     lockfiles, `*.pbxproj`, build outputs — their churn is noise)
3. **Report up to 7 findings, ranked by risk** (highest first). If fewer
   than 5 real risks are found, say so instead of padding.

## Output format (per finding)

```
### N. <one-line risk statement>  [risk: high|medium|low]
Why it matters: <1-2 sentences, concrete failure scenario>
Investigate: `<ready-to-paste follow-up prompt the user can run next>`
```

End with a one-line recommendation of which finding to chase first.
