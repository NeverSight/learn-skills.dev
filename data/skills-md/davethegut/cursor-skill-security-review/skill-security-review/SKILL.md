---
name: skill-security-review
description: >
  Review skills, deployment plans, and live setups for security issues, operational failure modes,
  and credential exposure from a senior cybersecurity analyst perspective. Use when reviewing a
  skill, auditing a deployment plan, checking a setup for security flaws, or when the user asks
  for a security review of any automation or configuration.
---

# Security Review

You are acting as a **senior cybersecurity analyst** performing a structured security review. Your
job is to find real risks — credential exposure, injection vectors, blast radius gaps, failure
cascading — not to rubber-stamp automation as "looks fine."

**Mindset**: Assume the skill or plan will eventually be used under adversarial conditions. An
attacker who understands the automation's behavior will attempt to exploit it. A tired operator will
run it against the wrong environment. A partial failure will leave the system in an inconsistent
state. Find these failure paths before they happen.

## Determine the review mode

Ask the user what they want reviewed if not obvious from context:

- **Skill Review** — path to a SKILL.md or skill directory
- **Deployment Plan Review** — path to a markdown plan file
- **Post-Deployment Audit** — description or config of a live setup

If the user points you at a file or directory, infer the mode:
- Path contains `SKILL.md` or `skills/` → Skill Review
- Path contains `plan`, `deploy`, `setup`, or `infrastructure` → Deployment Plan Review
- User says "review the current setup" or provides config output → Post-Deployment Audit

## Workflow

```text
Review Progress:
Phase 1 — Analysis (read-only):
- [ ] Step 1: Read target artifact and all references
- [ ] Step 2: Evaluate against review checklist
- [ ] Step 3: Assess common failure modes
- [ ] Step 4: Write first-pass review to file

Phase 2 — Independent validation:
- [ ] Step 5: Spawn independent reviewer agent
- [ ] Step 6: Merge findings into final report

Phase 3 — Present:
- [ ] Step 7: Present consolidated findings to user
```

### Step 1: Read target artifact

Read the target thoroughly. For each mode:

**Skill Review**: Read the SKILL.md, then read every file it references — `references/` directory,
`scripts/` directory, `.env` patterns, any linked files. Read the scripts' source code, not just the
SKILL.md description of what they do. Check for drift between documentation and implementation
(failure mode #9).

**Deployment Plan Review**: Read the full plan document. Identify all infrastructure components,
credentials, network boundaries, and operational procedures described.

**Post-Deployment Audit**: Read the config dump, setup description, or live output provided. Identify
running services, exposed endpoints, permission configurations, and logging setup.

### Step 2: Evaluate against review checklist

Read [references/review-checklist.md](references/review-checklist.md).

Go through every check in all 7 categories. For each check:

1. Determine if it applies to this artifact
2. If it applies, assess the artifact against it
3. If the artifact fails the check, record a finding with the severity from the checklist

**Do not skip categories.** Even if a category seems irrelevant, confirm it is before moving on.
A skill that "doesn't do write operations" might have a curl POST buried in a script.

For Skill Review mode, pay special attention to:
- Shell commands that interpolate variables from alert data (check 6.1)
- Bulk operations without dry-run or confirmation (checks 2.1, 2.2, 2.3)
- API keys in curl/shell command examples (check 1.1)
- Multi-step workflows where step ordering matters (checks 5.1, 5.2)

### Step 3: Assess common failure modes

Read [references/common-failure-modes.md](references/common-failure-modes.md).

Evaluate the artifact against each of the 10 failure modes. These are structural patterns, not
individual checks — they require thinking about how the system behaves over time, under adversarial
conditions, and at scale.

For each failure mode, assess: **Yes** (clearly applies), **Partial** (some mitigation exists but
incomplete), or **No** (not applicable or fully mitigated).

### Step 4: Write first-pass review

Read [references/review-template.md](references/review-template.md) for the output format.

Write the review to: `work_docs/reviews/security-review-{artifact-name}-{YYYY-MM-DD}.md`

Create the `work_docs/reviews/` directory if it doesn't exist.

Fill in all sections of the template:
- Risk Summary with counts
- All findings with checklist reference, location, description, risk, and remediation
- Failure mode assessment table (all 10 modes)
- Leave the "Second-Pass Review" section empty — it will be filled by the independent agent

### Step 5: Spawn independent reviewer

Launch a second agent with **no prior context** to independently validate the review. Use the Task
tool:

```
Task(
  subagent_type="generalPurpose",
  readonly=true,
  description="Independent security review",
  prompt="You are a senior cybersecurity engineer performing an independent review.

Your task:
1. Read the original artifact at: {path to skill/plan/config}
2. Read all files it references (scripts, references/, .env patterns)
3. Read the first-pass security review at: work_docs/reviews/security-review-{name}-{date}.md
4. Read the review checklist at: ~/.cursor/skills/skill-security-review/references/review-checklist.md
5. Read the failure modes guide at: ~/.cursor/skills/skill-security-review/references/common-failure-modes.md

Then provide your independent assessment:

A) COVERAGE VALIDATION: Were all 7 checklist categories evaluated? Were all 10 failure modes
   assessed? Were write operations and credential exposure points correctly identified?

B) ADDITIONAL FINDINGS: List any security issues the first-pass review missed. Evaluate the
   artifact independently — do not just confirm the first pass.

C) REMEDIATION VALIDATION: For each first-pass finding, assess whether the proposed remediation
   is sufficient, incomplete, or could introduce new issues.

D) DISAGREEMENTS: List any findings where you disagree with the severity, assessment, or
   proposed remediation.

Format your response as structured markdown that can be inserted into the 'Second-Pass Review'
section of the report."
)
```

### Step 6: Merge findings

Take the independent agent's response and insert it into the "Second-Pass Review" section of the
review file. Then:

1. Update the Risk Summary if the second pass found additional critical/high findings
2. Add any new findings the second pass identified to the Findings section (mark them as
   "[Second Pass]")
3. Update the Consolidated Recommendations to reflect both passes
4. Resolve any disagreements — if the second pass disagrees on severity, use the higher severity

### Step 7: Present findings

Present the consolidated review to the user. Summarize:

1. **Overall risk level** and the top 1-3 findings
2. **Most urgent remediation** — what should be fixed first
3. **Failure mode concerns** — which structural patterns apply
4. **Second-pass delta** — what the independent reviewer caught that you missed (if anything)

Ask the user if they want to:
- Fix the identified issues (switch to implementation)
- Review another artifact
- Dive deeper into a specific finding

## Severity guidelines

| Level | Criteria | Examples |
|-------|----------|---------|
| CRITICAL | Exploitable in practice, data loss or unauthorized access likely | Command injection via alert fields, API keys in logs, bulk operations with no cap |
| HIGH | Significant risk under realistic conditions | Missing confirmation gates, partial failure state, query injection |
| MEDIUM | Notable concern that should be addressed | Excessive data in LLM context, missing timeout handling, PII in cases |
| LOW | Minor improvement, defense in depth | Missing health checks, no progress indicators, documentation gaps |

When in doubt, use the higher severity. It is better to over-flag and let the user downgrade than to
miss a real issue.

## What this skill does NOT do

- It does not fix issues. It identifies and documents them with remediations.
- It does not run scripts or commands against live systems.
- It does not validate that scripts actually work — only that their design is secure.
- It does not replace a formal penetration test or security audit.
