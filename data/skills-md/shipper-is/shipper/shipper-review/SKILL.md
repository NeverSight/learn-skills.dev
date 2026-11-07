---
name: shipper-review
description: Orchestrate a QUIPS code review (Quality, Uptime, Intent, Performance, Security) of a PR or branch. Deterministic scripts build the risk floor and compute the verdict; tiered lane and persona subagents find issues; blockers must carry proof and survive a cross-family fact-check; a tech-lead judge writes the scorecard. Produces one report headed by a verdict and per-lane grades, posted to the PR and persisted in `<reviews>/`. Use before requesting human review on a PR, or whenever the user asks for a thorough review of changes.
---

The goal of this skill is to produce a review that is broader, more consistent, and more measurable than a single human pass, so the human reviewer only has to read one verdict, one scorecard line, and the blockers. You are the orchestrator: you do not review code yourself. You run the scripts, plan the review, launch a fresh subagent per lane or persona, collect proof, and hand the results to a judge and then to the policy script.

Before anything else, read and follow [./CONFIG.md](./CONFIG.md). It tells you where plans, spikes, bugs, reviews, and modules live in this repository (written below as `<plans>`, `<spikes>`, `<bugs>`, `<reviews>`, and `<modules>`) and which team and personal preferences apply.

The lane charters, personas, accepted evidence kinds, and the output contract every reviewer follows are in [./LANES.md](./LANES.md). This skill is repo-agnostic; repo-specific rules enter only through the host repo's own documents and the optional `review` key in `.shipper/config.json` (described in CONFIG.md).

## Hard rules

- **Findings only.** Nothing under review is edited. The only writes are scratch files in a temporary work directory, repro tests in a disposable worktree that is removed afterward, and the review artifact in `<reviews>/`. Fixes are a separate, explicit request from the user.
- **Plain code decides.** Unit splitting, the risk floor, sampling, and the verdict come from the scripts in `./scripts/`. Never compute them by hand, and never override or soften the policy script's verdict.
- **Blockers need evidence; suggestions don't.** A blocker without accepted proof becomes a suggestion. An author agent will dutifully "fix" a hallucinated blocker and make the code worse.
- **Model diversity over model size.** Heavy panels span at least two model families, and a finding is fact-checked by a different family than the one that wrote it.
- **Security fails closed.** If the Security lane crashes, times out, or skips an applicable scanner, the verdict is escalate. Only a named human from the security team can dismiss a Security finding.
- **Never merge, never approve.** A READY verdict means "ready for a human reviewer", not "merge". Team policy on human sign-off always applies.

## Model tiers

| Tier | Use it for | Pick |
|------|------------|------|
| No model | Risk floor, unit splitting, sampling, verdict | `./scripts/` |
| System 1 | Triage of every unit | The fastest model your harness offers |
| Light | Light-tier lane generalists; fact-checking suggestions | Fast models from at least two vendors |
| Heavy | Persona panels, evidence provers, fact-checking blockers and all Security findings, the judge | Frontier models from at least two vendors |

Resolve tiers from what your subagent tool accepts, unless the user names models or the merged config sets `models.<your agent>.shipper-review` (see CONFIG.md). Record a **family** string for every reviewer (the vendor, such as `claude`, `gpt`, `gemini`, `grok`, or `composer`; Cursor's dedicated subagents are `cursor-bugbot` and `cursor-security-review`). If your harness offers only one family, say so in the coverage notes. The policy script then escalates any blocker it cannot confirm independently, rather than sending it to the author.

## Step 1: Identify the target

The user points you at a PR, a branch, or local changes. Defaults: if a PR exists for the current branch, review the PR. Otherwise review branch changes against the merge-base with the default branch (committed, staged, and unstaged). Use `uncommitted changes` only when the user says so. Check out the target locally, and create a work directory outside the repository (`mktemp -d`); it is written below as `<work>`.

## Step 2: Context pack

1. Run the risk floor (requires Bun):

   ```bash
   bun <this skill's directory>/scripts/risk-floor.ts --repo <repo> --base <base> --out <work>/floor.json
   ```

   Use `--uncommitted` instead of `--base` for local changes. The output splits the diff into units (directories, with tests joined to the source they cover), and gives each unit a light or heavy floor per lane from path rules (auth, billing, migrations, infra, dependency manifests, secrets, plus any repo rules). It also flags deterministically sampled low-risk units for heavy review, lists files that usually change with each unit but are missing from the diff, and reports the size budget. If Bun or the script is unavailable, continue the review, but the verdict is ESCALATE with the reason "policy engine unavailable".
2. If `budget.exceeded` is true, stop before launching lanes. Report ESCALATE because the diff is too large to review without truncating it, and suggest splitting the PR. Continue only if the user explicitly asks for a full review anyway.
3. Write `<work>/context.md` for every subagent to read. It contains the target and the exact diff command; the units table from `floor.json` (files, floor per lane, matched rules, sampled, co-change partners); and the intent sources. Intent sources are the linked ticket (when you can fetch it), the Shipper plan, spike, or bug file this change came from (matched by `branch`, `pr_number`, or `pr_url` frontmatter in `<plans>/`, `<spikes>/`, `<bugs>/`), its acceptance criteria and phase Completion Notes, and the PR description. Also include required CI check status (`gh pr checks`), the repo's rule documents, and whether read-only production access is detectable.

## Step 3: Triage and review plan

Launch one System 1 subagent with `context.md` and the diff. For every unit and lane it returns an impact (low or high), a blast radius, and its confidence. A lane is planned heavy for a unit when the floor says heavy, triage says high impact, or triage confidence is low. Triage can raise a unit above its floor but never lower it below; the policy script checks this. Append the final plan (unit × lane → tier) to `context.md`.

## Step 4: Lane review (parallel)

All reviewers are read-only, so launch them concurrently. Every prompt is self-contained (the subagent cannot see this conversation). It holds the absolute repository path, the diff target, the path to `context.md`, the units it covers, and the relevant section of [./LANES.md](./LANES.md) with the output contract.

- **Light tier:** one generalist per lane, covering every unit planned light for that lane, and carrying all of that lane's persona checklists.
- **Heavy tier:** one subagent per persona, covering the units planned heavy for that lane, with personas alternating across model families so each lane's panel spans at least two.
- **Kick-ups:** when a light reviewer lists a unit in `kickUp`, launch that lane's heavy panel for the unit and update the plan.
- **Self-consistency:** for units planned heavy on Security, run one extra Security generalist from a family that is not on the panel. The judge compares its blockers with the panel's.
- **Cursor only:** also launch exactly one `bugbot` subagent (description "Bugbot") as a member of the Uptime lane, and one `security-review` subagent (description "Security Review") as a member of the Security lane. Use this prompt shape, without computing the diff for them and without `Base Branch` unless the base is not the repo default:

  ```text
  Full Repository Path: <absolute repository path>
  Diff: <"branch changes" or "uncommitted changes">
  Custom Instructions: <only when the user gave specific review instructions>
  ```

  Map their findings into the lane's format yourself (persona `Bugbot` or `Security Review`, with their family string).

If a reviewer fails or returns malformed output, retry it once with the same prompt. If it fails again, record its lane as failed for the units it owned. Do not drop those units from coverage silently.

## Step 5: Evidence

Every proposed blocker needs proof of a kind its lane accepts (see LANES.md). For each proposed blocker without it, launch a heavy-tier prover subagent that tries to produce that proof, or reports that it could not:

- **Sandbox proof** (repro tests, benchmarks, bundle diffs, cross-tenant probes against local fixtures): work only in a disposable worktree at the reviewed state, created with `git worktree add --detach <work>/sandbox <head>` (for uncommitted targets, use the commit from `git stash create` and copy untracked files in). Never commit or push from it, and remove it with `git worktree remove --force` when done. Record the command and its output as the evidence `ref`.
- **Read-only proof** (query plans, production queries, contract traces, scanner output, secret matches): follow the production-data rules in LANES.md.

## Step 6: Verify

Fact-check every finding with a reviewer from a different family than the one that wrote it. Group findings by author family so each verifier batch can pick a family outside it. Use the heavy tier for blockers and every Security finding, and the light tier for other suggestions. The verifier receives the diff and, for each finding, its location, summary, and evidence. It does not get the original reviewer's reasoning. It may read the cited files and anything they call or are called by. For each finding it returns `upheld` or `deleted` with a one-line reason. It can delete findings but never add them. Keep deleted findings in the record, marked deleted.

## Step 7: Judge

Launch one heavy-tier "tech lead" subagent with the verified findings, `floor.json`, the review plan, each lane's coverage and status, self-consistency results, and the evidence. It:

- merges findings that share a root cause, keeping the strongest evidence and listing every persona that raised it;
- settles persona disagreements. Following an existing norm never blocks; adding a new instance of a deprecated pattern always does. Architect `deprecation-proposal` findings go to rule proposals, not the PR;
- assigns final severity and sets `blocker` only where the lane's "blocks when" rule applies;
- gives findings stable ids by lane (`Q1`, `U1`, `I1`, `P1`, `S1`, ...);
- writes `<work>/scorecard.json` in this shape (the full types are in `./scripts/policy.ts`):

  ```json
  {
    "commit": "abc1234",
    "lanes": {
      "quality": { "status": "completed", "coverage": [{ "unit": "src/auth", "tier": "heavy" }] },
      "security": { "status": "completed", "coverage": [], "scannersSkipped": [] }
    },
    "findings": [
      {
        "id": "U1", "lane": "uptime", "persona": "Contract Keeper", "severity": "high", "blocker": true,
        "location": "src/api/orders.ts:42", "summary": "…", "authorFamily": "claude",
        "evidence": { "kind": "contract-trace", "ref": "web/checkout.ts:88 still sends `qty`" },
        "verification": { "result": "upheld", "verifierFamily": "gpt" }, "status": "open"
      }
    ],
    "selfConsistency": [{ "unit": "src/auth", "lane": "security", "agreed": true }],
    "budgetExceeded": false
  }
  ```

  All five lanes must be present; a lane that did not run is `skipped` with a `reason`, or `failed`;
- writes the report Overview: 2–4 plain-language sentences that both technical and non-technical team members can follow. It covers what the change does, what if anything is worrying, and what should happen next. No jargon, no file paths.

## Step 8: Policy

```bash
bun <this skill's directory>/scripts/policy.ts --floor <work>/floor.json --scorecard <work>/scorecard.json --repo <repo>
```

The script returns the verdict (`ready`, `fix`, or `escalate`), the reasons for it, a grade per lane (pass, suggest, block, failed, skipped), the confirmed blockers, demoted blockers with the reason each was demoted, the two header lines, and the frontmatter values. Exit code 2 means the scorecard is malformed: send the errors back to the judge once, and if it is still invalid, the verdict is ESCALATE. Repo thresholds (extra floor rules, ignored paths, sample rate, size budget, accepted evidence kinds) live under `review` in `.shipper/config.json`; the defaults are in `./scripts/config.ts`.

## Step 9: Report

The report always opens with this header. The first two lines are the policy script's `header`, copied verbatim; the third is the judge's Overview:

```text
Verdict: <READY FOR HUMAN REVIEW | SEND BACK TO AUTHOR | ESCALATE TO A HUMAN>
QUIPS: Quality <grade> · Uptime <grade> · Intent <grade> · Performance <grade> · Security <grade>
Overview: <2–4 plain-language sentences>
```

Then, in order:

- **Why this verdict:** the policy script's reasons.
- **Blockers:** `ID | Lane | Persona | Location (file:line) | Finding | Evidence`. Each is written so an author agent can act on it directly.
- **Suggestions:** `ID | Severity | Lane | Persona | Location | Finding`, sorted by severity, including demoted blockers with the reason. These go to the author agent or become follow-up tickets; they never block.
- **Intent trace:** each acceptance criterion marked Met, Partial, or Unmet, with locations.
- **Coverage notes:** the review plan (units per tier, sampled units, kick-ups), lanes skipped or failed, scanners run and skipped, how many findings verifiers deleted, model families used, and claims that could not be verified.
- **Rule proposals:** Architect deprecation proposals and repeated findings (see below).
- **Footer:** `Automated review by shipper-review (QUIPS), not a human reviewer. A human still approves and merges.`

Deliver the report in chat. When the target is a PR, post it as a single PR comment (`gh pr comment`) that starts with the same header. On re-review, edit that comment rather than stacking new ones.

## Step 10: Persist the review artifact

Every review leaves one markdown file in `<reviews>/` (create the folder if needed; it is committed to the repository). Name it after the target, in kebab-case: `pr-<number>-<short-title>.md` for a PR, `<branch-name-kebab>.md` otherwise. There is one file per target; a re-review updates it.

```yaml
---
type: review
repo: owner/name
pr_url: https://github.com/owner/name/pull/123
pr_number: 123
branch: shipper/add-auth
base_branch: main
commit: abc1234
source: <plans>/done/add-auth.md
verdict: fix
quality: pass
uptime: block
intent: suggest
performance: pass
security: pass
reviewed_at: "2026-07-29T23:20:00-04:00"
---
```

- `repo`: `owner/name` from the origin remote, or the repository directory name if there is no remote.
- `pr_url`, `pr_number`: only when the target is a PR.
- `branch`, `base_branch`, `commit`: the reviewed branch, what it was diffed against, and the short sha of the reviewed HEAD.
- `source`: the repo-relative path of the plan, spike, or bug file found in Step 2. Omit it if nothing matched; never guess.
- `verdict` and the five lane keys: copied from the policy script's `frontmatter`.
- `reviewed_at`: a quoted ISO 8601 timestamp.

The body is the full Step 9 report, followed by a `## Scorecard data` section containing `scorecard.json` and the policy result as fenced JSON blocks. Every finding, its persona, tier, verifier outcome, and later status is kept, so the team can measure which personas' findings get fixed and which get dismissed. Commit the artifact (for example, `Add shipper review for PR #123`). If the working tree has changes that are not yours, commit only the review file.

## Re-review mode

When the user says findings were addressed, review the delta, not the whole PR again:

1. Re-run the risk floor at the new head. Rerun the lanes whose findings the fix commits touch, plus Uptime always (fixes introduce bugs), plus Security whenever the delta touches a unit with a heavy Security floor or a Security finding is still open. Re-verify new findings.
2. Update each prior finding's `status`: `fixed`, `dismissed`, `disputed` (the author disagrees with evidence), or `open`. A Security finding counts as dismissed only when `dismissedBy` names the human from the security team who dismissed it.
3. Carry the coverage of untouched units forward from the prior scorecard, have the judge merge the new findings, and run the policy script on the complete updated scorecard.
4. Update the PR comment and the artifact in place: refresh `commit`, `verdict`, the lane keys, `reviewed_at`, the header, and the scorecard data, then commit. Do not create a second file for the same target.

## Encode repeated findings

If the same class of finding appears across multiple reviews of a repo, the review is compensating for a missing rule. Propose encoding it where the repo keeps its rules: a lint rule, an agent-docs entry, an architecture note marking the pattern deprecated (which makes future instances a Quality blocker), or a `review.riskFloor` entry in `.shipper/config.json`. List these proposals at the end of the report; creating them is the user's call.

## How this fits the Shipper framework

- **shipper-ship** should run this skill after opening the PR and before requesting human review. The report becomes part of the PR's evidence, and the artifact in `<reviews>/` links back to the plan, spike, or bug file that produced the change.
- **shipper-loop / shipper-build** may treat a READY verdict as a completion gate for a plan's final phase. A FIX verdict's blockers are the author agent's next task; an ESCALATE verdict goes to a human.
