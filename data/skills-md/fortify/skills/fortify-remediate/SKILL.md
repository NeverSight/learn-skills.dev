---
name: fortify-remediate
description: Remediate SAST (static) and DAST (dynamic) security vulnerabilities ALREADY detected by Fortify in FoD or SSC — fix specific issues, categories, or reduce issue counts, including applying SAST Aviator fixes. For SCA / open source dependency findings (vulnerable third-party components, CVEs), use fortify-dependency-upgrade instead. NOT for discovering or reviewing new issues (use fortify-change-review for a local code-change review, or fortify-fod / fortify-ssc to scan and triage).
license: MIT
metadata:
  version: "1.1.1"
  tested-with:
    fcli: "3.23"
    fod: "26.2"
    ssc: "26.2"
---

# Fortify Remediation

Remediating Fortify findings is a 4-step process. Work through steps in order — each step has a clear entry condition and output that feeds the next.

> **Scope: SAST and DAST only.** This skill remediates static (SAST) and dynamic (DAST) findings — issues fixed by changing application source code or configuration. It does **not** cover SCA / open source dependency findings (vulnerable third-party components, CVEs), which are fixed by upgrading dependencies. If the target issues are SCA / open source, stop and use the `fortify-dependency-upgrade` skill instead.

> **Stay within the documented workflow.** Do not proactively offer side-quests or capabilities that aren't part of the step you're in — e.g., don't search for vulnerabilities in the source code, look for local files or vulnerabilities detected by non-Fortify scanners, set up CI/CD scanning, reconfigure scan settings, parse FPR files, etc. If a step in this skill calls for it, do it; if not, don't surface it as an option. Eager suggestions waste the user's attention and lead them off the remediation path.

---

## Step 0: Establish Context

Before any remediation work, confirm these three things:

**1. Platform** — Fortify on Demand (FoD) vs Software Security Center (SSC). If the user did not specify, run both session checks to determine which platform is active:

```bash
fcli fod session ls --query "expired=='No'"
fcli ssc session ls --query "expired=='No'"
```

- If only a FoD session is active → platform is FoD.
- If only an SSC session is active → platform is SSC.
- If both are active → ask the user which platform they want to use.
- If neither is active → ask the user which platform they are using and prompt them to create an fcli session with FoD or SSC.

**fcli not found:** You interact with Fortify using `fcli`. It must already be on the PATH. If it is not installed, load `references/fcli-install.md`.

**2. Target release or application version** — You need this to query issue data. If the user hasn't provided it, load:
- FoD: `references/resolving-release.md`
- SSC: `references/resolving-appversion.md`

### Step 0 → Step 1 gate

Before advancing, confirm all three items are resolved:

- [ ] Platform identified (FoD or SSC)
- [ ] Active fcli session for target platform
- [ ] Release / application version identified

Do NOT proceed to Step 1 until all three are confirmed.

### FoD ↔ SSC Field Mapping

FoD and SSC use different field names for the same concepts. Use this mapping whenever constructing queries or interpreting results:

| Concept | FoD field | SSC field |
|---------|-----------|----------|
| Issue instance ID | `instanceId` | `issueInstanceId` |
| Category name | `category` | `issueName` |
| Severity | `severityString` | `friority` |
| Scan type | `scanType` (`Static`, `Dynamic`) | `analyzer` (`SCA` = Static Code Analyzer, etc.) |
| Auditor/analysis status | `auditorStatus` | Custom tag (typically `Analysis`) |
| Suppressed | `isSuppressed` | `suppressed` |

---

## Step 1: Identify the Target Issue Set

> Load `references/issue-targeting.md` before working through this step.

Step 1 ends when you have a **confirmed, specific list of Fortify issue IDs with enough summary data to begin planning**.

**Specific request** (issue IDs or precise filter already given): Verify you have the issue details; proceed immediately.

**Category/file/component request**: Use the platform skill's issue investigation commands to filter to the matching issues. Present the full matching list to the user so they can confirm the scope before you proceed.

**General request** ("fix the top issues", no specific target): Identify a proposed batch of related issues representing the best remediation value, then present this proposal to the user for confirmation. See `references/issue-targeting.md` for how to select and group issues effectively.

**SCA / open source out of scope**: This skill targets only SAST (`scanType=='Static'` / SSC `analyzer=='SCA'`) and DAST (`scanType=='Dynamic'`) issues. Exclude SCA / open source findings (FoD `scanType=='OpenSource'`, SSC `analyzer=='Open Source'`) from the target set. If the user's request is about open source dependencies, vulnerable components, or CVEs, stop here and direct them to the `fortify-dependency-upgrade` skill.

Keep the target set to related issues that can be addressed in a single pass. Mixing unrelated issue types or too many categories in one batch leads to unfocused, harder-to-review changes. See `references/issue-targeting.md` for how to group by type and category.

**Audit status and false positive awareness**: The `fcli fod/ssc issue list` commands exclude suppressed/hidden issues by default, so known false positives marked as suppressed are already filtered out. However, unaudited issues (FoD: `auditorStatus == 'Pending Review'`; SSC: no `Analysis` custom tag set) may include false positives. When selecting issues for a general request, prefer issues that have been audited and confirmed as true positives. For unaudited issues, factor the false-positive risk into your planning — flag uncertain issues to the user rather than planning fixes that may be unnecessary.

### Step 1 → Step 2 gate

Before advancing, verify:

- [ ] You have a specific, enumerated list of issue IDs (not just a filter expression)
- [ ] Each issue has enough summary data (category, severity, file/location) to begin planning
- [ ] The user has confirmed the scope
- [ ] For general requests: the user has approved your proposed batch
- [ ] Any issues flagged as uncertain false positives have been called out to the user

Do NOT proceed to Step 2 until the user has confirmed the target issue set.

---

## Step 2: Plan the Fix

Load `references/sast-dast-fix-planning.md` and follow it to completion. It owns the full planning workflow — all retrieval, analysis, and fix formulation steps — as well as the Step 2 completion gate.

Return here for Step 3 when the reference file signals that planning is complete.

---

## Step 3: Present and Confirm the Plan

Always present the full remediation plan to the user before making any changes. Include:

1. **Target issue list** — IDs, categories, severities, file/URL locations
2. **Proposed changes** — for each: what file or config changes, what specifically changes, and the security rationale (e.g., "parameterize query to prevent injection" rather than "Fortify said to fix this")
3. **Risk notes** — anything that may change behavior, break API contracts, require config updates, or affect downstream callers
4. **Unit tests** — any new or updated tests you propose to add
5. **Out of scope** — explicitly name any issues in the target set you're deferring and why (e.g., insufficient context, requires architectural change, appears to be a false positive needing review)

If you're uncertain about a fix, say so explicitly rather than guessing. It is better to flag ambiguity than to implement an incorrect fix.

**Wait for explicit user confirmation before proceeding to implementation.** Do NOT begin Step 4 until the user has reviewed and approved the plan.

---

## Step 4: Implement and Verify

Load `references/sast-dast-implementation.md` and follow it to completion. It owns the full implementation workflow and completion gate.

### Completion Summary

After the reference file signals Step 4 complete, return here and provide:

- What was changed (files, change types, issue categories resolved)
- Any issues from the original target list that were **not** fixed, with a brief explanation
- A note for the user to re-run Fortify to confirm resolution (do not block on this)

---

## Reference Files

| File | When to load |
|------|--------------|
| `references/fcli-install.md` | Full fcli installation and upgrade procedures |
| `references/fcli-query-output.md` | Detailed SpEL query syntax, null-safety patterns, output formats, `--store` variable chaining, server-side filtering, date utility functions |
| `references/resolving-release.md` | When the user has not specified a release in FoD to target or when you need to confirm the correct release/version based on an ambiguous name. |
| `references/resolving-appversion.md` | When the user has not specified an application version in SSC to target or when you need to confirm the correct release/version based on an ambiguous name. |
| `references/issue-targeting.md` | How to select and group issues; "bang for buck" heuristics; how to handle general vs specific requests; Fortify taxonomy guide; SAST vs DAST mixing rules |
| `references/sast-dast-fix-planning.md` | SAST and DAST fix planning (Step 2); retrieving Aviator AI guidance (FoD); reading and interpreting SAST traces; codebase analysis patterns; unit test guidance |
| `references/sast-dast-implementation.md` | SAST and DAST implementation (Step 4); apply-build-test loop; code comment guidelines; completion gate |
