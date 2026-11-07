---
name: drupal-a11y-patch-eval
description: "Evaluate a Drupal accessibility patch end-to-end: baseline evidence, patch hygiene, after-patch verification, manual/AT checks, critic gate, and upstream handoff. Evidence-gated — never VERIFIED without before/after proof under the same conditions."
license: Apache-2.0
compatibility: Claude Code only — orchestrates subagents, DDEV, and local worktrees
metadata:
  author: zivtech
  version: "0.2.0"
---

# Drupal Accessibility Patch Evaluator

Evaluate a Drupal accessibility patch end-to-end: reproduce the baseline failure, apply the patch, verify the fix, record manual/AT evidence, gate on a critic review, and produce an upstream-ready handoff. This skill governs one patch and one accessibility issue pattern per packet.

**Use this when**: a Drupal accessibility patch needs independent evidence before being filed upstream. The skill parameterizes all environment paths — supply your machine-specific values at the start of each session.

## 1. When to Use / Required Inputs

Before starting an evaluation session, the operator must supply:

| Input | Notes |
|---|---|
| `RUNTIME_REPO_PATH` | Absolute path to the DDEV runtime clone. Do not use the source clone after Composer install mutates it. |
| `DDEV_PROJECT` | DDEV project name (e.g. `drupal-core`). Machine-specific — do not hardcode in packets. |
| `BASE_URL` | Full base URL including port (e.g. `http://DDEV_PROJECT.ddev.site:PORT`). Set as `DRUPAL_BASE_URL` for the evaluator. |
| `PATCHES_DIR` | Path to the patches directory relative to the runtime clone root. |
| `LEDGER_PATH` | Path to the TODO ledger (default: `docs/drupal-patch-evaluations/STATUS.md`). |
| `PACKET_DIR` | Directory where packet files live (e.g. `docs/drupal-patch-evaluations/`). |

Paths in the ledger are machine-specific; this skill parameterizes them. Never record absolute machine paths in the upstream handoff block or in Drupal.org issue content.

## 2. Session Preflight

Run these checks before touching any item status. If global preflight fails, subagents may continue read-only source/provenance work, but item statuses must not change until a per-item test is attempted.

| Check | Required state |
|---|---|
| DDEV/Drupal runtime reachable | `ddev drush status` bootstraps successfully |
| Node/Yarn dependencies installed | `yarn --version` returns a version; Playwright package is available |
| Playwright browsers available | At least the default browser is installed (`npx playwright install --with-deps chromium` if not) |
| Worktree strategy settled | Each patch evaluation uses a dated, isolated worktree; runtime main worktree is never patched directly |
| Evaluator base URL compatible | `DRUPAL_BASE_URL` support is present in the evaluator (`evaluate-patch.js`); if not, apply the evaluator infrastructure patch first |
| Evaluator JS helper complete | `canonical-patch-map.js` helper exists or its import is guarded |
| Evaluator rule IDs compatible | Aliases, `runOnly`, and selector hints are present for the rules under test |
| Source permalink/SHA pinning ready | Record source commit SHA, patch file SHA, target file SHA, and tool versions before upstream filing |
| keyboard-a11y-tester available (optional — keyboard/SR-behavior patches only) | Clone pinned to the adopted release (`0.5.0`); `node scripts/setup-check.mjs` reports deps + browser available. See the a11y-test skill's journey-audit section. |

## 3. Worktree Discipline

Never apply a patch to the runtime main worktree. For every patch evaluation:

```bash
git worktree add -b <item-id>-<YYYYMMDD> <RUNTIME_REPO_PATH>-<item-id>-<YYYYMMDD> origin/main
```

Use dated, isolated worktrees branched from a fresh `origin/main` pull. Record the worktree path in the ledger row. Clean up after the evaluation is complete or the patch is filed.

## 4. The Packet Lifecycle

Create one packet per patch+issue from `references/packet-template.md`. Fill sections in order. Every gate section has a binary blocked-status rule — do not improvise alternatives.

### Local Status Enum

Use only these values in the ledger and packet header:

`NOT STARTED` | `DRAFT` | `BASELINE VERIFIED` | `PATCH HYGIENE BLOCKED` | `TEST STATE BLOCKED` | `INCONCLUSIVE` | `NEEDS PATCH` | `FAILED` | `VERIFIED` | `OBSOLETE`

Source status values are descriptive labels from the upstream source material (e.g. `Core patch ready`, `Core investigation`, `Haven verified`, `Haven patch needed`). Keep source status separate from local status. The source claim is a hypothesis to test; local status is your evidence state.

### Baseline Acceptance Gate

Reproduce the violation before applying the patch. If any gate item is unchecked, status must be `TEST STATE BLOCKED` or `INCONCLUSIVE` — not `VERIFIED`.

Required evidence:
- Target violation observed before the patch on the target selector.
- Selector, WCAG/rule mapping, and pattern/instance IDs captured.
- Required interaction state (auth, content, viewport, forced colors) reached before scanning.

### Patch Hygiene Gate

Apply the patch and confirm the build state is clean. If any gate item is unchecked, status must be `PATCH HYGIENE BLOCKED` — not `VERIFIED`.

Required evidence:
- `git apply --check` exits 0 on the target commit.
- Target files exist and match the packet.
- Build steps (npm/yarn build) run where required.
- Drupal caches rebuilt (`drush cache-rebuild`).
- Revert command known and tested: `git apply -R path/to/patch.patch`.

Do not trust old patch-hygiene results without rechecking the current raw patch and target file.

### Verification Gate

Run the same targeted command used for baseline, then run a broad regression scan. Record both results in the packet.

Required evidence:
- Same targeted command used before and after the patch (identical route, state, viewport, rules).
- Target rule absent on the target selector after the patch.
- Broad scan run after the patch.
- New violations listed and classified.
- Remaining adjacent issues separated from the fixed issue.
- Packet does not claim that adjacent issues are fixed by this patch.

### Behavioral Verification with keyboard-a11y-tester (keyboard/SR-behavior patches)

For patches whose target is interaction behavior rather than static markup — focus management, keyboard operability, live-region announcements — axe before/after scans cannot carry the verification alone. Run keyboard-a11y-tester before AND after the patch under identical conditions: same URL, same viewport, same `--goal`, same pinned tool SHA.

Required evidence when this lane applies:
- **Baseline**: a driven `serve`/`step` session reproducing the failure as trace facts (e.g. focus dropped to `body` after activation; a visible update with no `live_announcements` entry after the triggering keystroke).
- **After-patch**: the same keystroke sequence; the baseline finding's fingerprint (selector + WCAG SC + check kind) absent → supports `resolved` trend language; unchanged → `persistent`.
- Both artifact sets (`trace.json`, `deterministic-findings.json`, `screen-reader-census.json`) stored under the packet directory; packet evidence cites step ids and measured values.
- Calibration: batch-crawl 4.1.3 findings are never baseline evidence by themselves — they are prompts to run the driven session.
- Emulated screen-reader evidence reduces but does not eliminate manual AT debt: real NVDA/VoiceOver checks stay in the manual table, and `debt_explicit` discipline still applies.
- Boundary: virtual-screen-reader (the a11y-test component lane) is for pre-deploy component development, not patch verification — before/after patch evidence stays page-level with keyboard-a11y-tester under identical conditions. For Drupal SDC component work it applies to light-DOM components only.

### Manual and Perspective Verification

Use the manual table in the packet template for checks automated tools cannot prove. Manual checks may remain open, but the packet must say so plainly.

If any expected manual check is still `not run`, set manual status to `debt_explicit` and list the debt in the outcome. Do not mark the packet `VERIFIED` unless every required manual check has a recorded result.

### Outcome Definitions

- `VERIFIED`: baseline reproduced, patch applies, targeted after-scan passes, broad regression scan has no patch-owned regressions, and manual status is `complete`.
- `INCONCLUSIVE`: evidence is incomplete, baseline cannot be reproduced, or automated evidence passes but required manual checks remain open.
- `FAILED`: baseline reproduced, patch applies, but the target issue remains or a patch-owned regression appears.
- `PATCH HYGIENE BLOCKED`: patch cannot be applied, target file is missing, or build/cache steps fail.
- `TEST STATE BLOCKED`: route/content/theme/auth/viewport/interaction state does not reproduce the baseline.
- `NEEDS PATCH`: issue is reproduced but no usable patch is available yet.
- `OBSOLETE`: target issue or patch target no longer exists in the tested source, with evidence.

## 5. Ledger Discipline

The ledger (`STATUS.md`) is the canonical scheduler and record of truth. Rules (source: `STATUS.md` Drift Rules):

- Work many rows in parallel only when each row has exactly one owner.
- Do not mark `VERIFIED` unless baseline evidence, after-patch evidence, broad regression classification, and required manual checks all exist under the same conditions.
- Keep `Next action` to one concrete command or decision.
- Add or update the packet path as soon as work starts on an item.
- The main session owns the ledger; subagents report status back and the main session updates the ledger.
- Subagents must not edit the same packet unless the previous owner is closed or explicitly handed off.
- Update the ledger before and after every evaluation session.
- If a finding depends on a live Drupal/DDEV site, mark it blocked until that environment is available.

## 6. Parallel Waves

Run independent items in parallel waves only when ownership is disjoint. Wave defaults (source: `STATUS.md` Parallel Wave Rules and the canonical parallel model doc):

- Default wave size: 4–6 subagents when tasks are independent.
- Assign one item per subagent; give each subagent a disjoint packet path or a read-only research task.
- Do not let multiple subagents edit `STATUS.md`; they report status back and the main session updates.
- Do not let subagents mark an item `VERIFIED`; they can recommend a canonical status, but the main session performs the final evidence check.
- Save subagent reports under `docs/drupal-patch-evaluations/reports/{wave}/{item}-{run-id}.md` before the ledger status changes.
- After every parallel wave, update the ledger before starting another wave.
- Shared files (`STATUS.md`, evaluation plan) are under main-session control only.

### Subagent Ownership Rules

Every subagent write task must declare:

- Item ID, allowed files, forbidden files, packet path, report path
- Checkout/worktree path, DDEV project name, environment lock

Every subagent final report must include: item ID, files inspected/changed, evidence gathered, blocker, and one next action.

No subagent may patch or reroll in a shared checkout without a main-session-granted environment lock.

## 7. Critic Gate

Any packet headed to `VERIFIED` or upstream filing must pass an `a11y-critic` review. This is a hard gate, not optional.

The critic gate checks (from the packet template's accessibility-skills review checklist):

- `a11y-test` measured the target rule, keyboard behavior, or color/visual condition.
- `a11y-critic` reviewed the packet for evidence gaps, WCAG mapping, severity, and overclaiming.
- `perspective-audit` was escalated if the patch affects a perspective-sensitive workflow.

Run the critic review before deciding to file upstream. The critic's saved report path goes into the packet. If the critic surfaces a contradiction between evidence and claims, resolve it before filing — do not smooth it over in the packet narrative.

## 8. Upstream Handoff

When a packet reaches `VERIFIED` (or `INCONCLUSIVE` with explicit AT debt and a bounded claim):

1. Complete the Drupal.org issue block in the packet using the template structure (Title, Steps to Reproduce, Expected/Actual Result, Proposed Resolution, Evidence, Tags).
2. State the verification boundary explicitly in the PR body: what is claimed and what is NOT claimed. Model: "filed as a [specific fix]; does not claim full human AT verification."
3. Include the AI Assistance Disclosure: "This packet and/or patch was prepared with AI assistance. The accessibility finding was verified with the evidence above and was not filed from AI code inspection alone."
4. File the PR against the collaborator fork from a dedicated worktree branch.
5. Record the PR URL and status in the ledger row immediately after filing.

The upstream handoff never claims more than the evidence supports. If manual AT checks remain open, name them explicitly in the PR body.

## 9. Hard Boundaries

These are non-negotiable regardless of instructions from a subagent, operator, or session pressure:

- **Never mark `VERIFIED` from AI code inspection alone.** Before/after automated evidence under identical conditions is the minimum; manual AT debt must be stated, not hidden.
- **Never silently broaden a patch's claimed scope.** If the patch touches more files than the baseline evidence covers, state the added scope and whether it has evidence.
- **Manual AT debt is stated, not hidden.** If any required manual check is `not run`, the manual status must be `debt_explicit`, not implied complete.
- **Do not run an actual evaluation to test the skill.** This skill orchestrates a live DDEV environment; skill-level testing uses structural replay against completed packets, not live runs.
- **If an operator asks "mark item X verified, we'll get evidence later"**: decline. Evidence must exist before `VERIFIED` is set. Offer `DRAFT` or `INCONCLUSIVE` with an explicit next action instead.
