---
name: pr-creation
description: Guidelines for creating high-quality Freenet pull requests. This skill should be used when creating PRs for freenet-core, freenet-stdlib, or related repositories. Emphasizes quality over speed, thorough testing, and proper review process.
license: LGPL-3.0
---

# Freenet Pull Request Quality Standards

## Core Philosophy

**Our goal is high-quality code that won't require future fixes.** Don't cut corners, be a perfectionist, don't increase tech debt. A quick fix that causes problems later wastes more time than doing it right the first time.

## Before Creating the PR

### Sync with Latest Main from GitHub

**CRITICAL:** Always ensure you're working from the latest `main` branch from GitHub, not a stale local copy:

```bash
cd ~/code/freenet/freenet-core/main
git fetch origin
git log --oneline -1 origin/main  # Check what's latest on GitHub
git pull origin main              # Update local main
git log --oneline -1              # Verify you have the latest
```

This prevents:
- Working on outdated code that's already been fixed
- Merge conflicts when the PR is ready
- Basing work on code that's already been superseded

### Create a Worktree

Never work directly in the main worktree. Create a dedicated worktree for your branch:

```bash
cd ~/code/freenet/freenet-core/main
git worktree add ../fix-<issue-number> -b fix-<issue-number>
cd ../fix-<issue-number>
```

### Verify Your Environment

```bash
# CRITICAL: Verify you're in a worktree, not the main directory
pwd  # Should be .../freenet-core/<branch-name>, NOT .../freenet-core/main
git branch --show-current  # Should be your feature branch
```

### Run Local Checks

```bash
cargo fmt
cargo clippy --all-targets --all-features
cargo test
```

Fix all warnings and errors before pushing.

### Choosing the Right Test Level

**Simulation tests (primary):** For logic errors in routing, topology, subscriptions, operations, or any behavioral change. Use the direct simulation runner (`run_simulation_direct`) in `crates/core` — it's deterministic, fast, runs in CI, and has zero external dependencies. This should be the default for validating that changes don't regress subscribe rates, GET rates, tree formation, etc.

**Docker NAT simulation:** Only for transport-layer issues that require real network namespaces — firewall hole-punching, NAT traversal, UDP behavior behind iptables rules. In-memory sockets can't reproduce these. Don't use this for testing routing logic or subscription behavior.

**Manual multi-machine testing:** For issues that require real geographic distribution, actual internet latency, or cross-architecture validation (nova/vega/technic).

## PR Title and Description

### Title Format

PR titles **must** follow Conventional Commits - CI fails non-conforming titles:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code change that neither fixes a bug nor adds a feature
- `test:` - Adding or correcting tests
- `chore:` - Maintenance tasks

### Description Requirements

**Explain WHY, not just WHAT.** Structure your PR description:

```markdown
## Problem
[What's broken? What's the user impact? Why does it matter?]

## Approach
[Why this solution over alternatives? What's the key insight?]

## Testing
[New tests added and what scenarios they validate]
[Local validation steps performed]
[E2E testing results if applicable]

## Fixes
Closes #XXXX
```

**Bad:** "Add observed_addr field to ConnectRequest"
**Good:** "The joiner can't know its public address until observed externally. Previous approach rewrote addresses at transport boundary, but that's a hack. This lets the gateway fill in the observed socket naturally since it already sees the real UDP source."

## Test Quality Standards

### CI Must Be a Reliable Safety Net

**The test harness should be growing faster than the core code.** Quick fixes without test coverage create an illusion of speed — we end up in a patch → break → patch cycle where each fix introduces new regressions. Almost every logical bug can be reproduced in a synthetic test with zero external dependencies. The work to build those tests is harder than a quick fix, but it's the only way to stop the cycle.

**Every PR that changes behavior must include tests that would have caught the problem before merge.** Not just tests that verify the fix works — tests that would have prevented the bug from shipping in the first place. If you're changing routing logic, test that routing actually makes correct decisions under realistic data conditions. If you're changing topology, test that subscribe/GET success rates don't regress. If you're changing subscription handling, test that subscription trees form and survive peer churn.

**CI gap tests go in the same PR, not a follow-up issue.** The pattern of filing "add missing test" issues that never get done is how we end up with 17 bug-fix PRs in 4 days and none of them caught by CI. If the fix PR doesn't include the test that closes the gap, it is not ready to merge.

### A Bug That Made It Past CI Is Also a Bug in CI

When fixing a bug, always ask: **"Why didn't CI catch this?"**

Investigate which test layer should have caught it:
- Unit tests for logic errors
- Integration tests for component interactions
- Network simulations for distributed behavior
- E2E tests for real-world scenarios

Document the gap in your PR description. **Then close the gap.** The fix PR should include the missing test that would have caught this bug class, not just a narrow regression test for the specific symptom.

### Simulation Health Metrics (Required)

For PRs that touch routing, topology, operations, or subscription handling, the PR **must** include simulation tests that assert key health metrics. This is not optional — discovering regressions through production telemetry days later means CI failed:

| Metric | What it catches |
|--------|-----------------|
| Subscribe success rate | Topology regressions, interest TTL issues |
| GET success rate | Routing regressions |
| Subscription tree formation | Tree building/maintenance bugs |
| Interest renewal rate | TTL/renewal bugs |
| Time to first successful operation | Bootstrap/convergence issues |

These should be measured in simulation tests and asserted against thresholds. **Discovering regressions days later through production telemetry is a test infrastructure failure.**

Use the direct simulation runner (`run_simulation_direct`) for these — it supports multi-peer networks with contract operations and is deterministic.

### Don't Discover Logic Errors in Production

If a bug is a **logic error** (wrong threshold, missing data path, incorrect fallback), it should be reproducible in a unit or integration test. Don't settle for "we'll monitor it in production." Examples:

- Router prediction function requires data from 3 estimators but threshold only checks 1 → unit test with realistic data mix
- Topology change breaks subscribe routing → simulation test measuring subscribe success rate
- Interest TTL too aggressive → test that interests survive under congestion

Reserve production telemetry analysis for genuinely environment-specific issues (OOM under specific conditions, real NAT traversal, etc.), not for catching logic errors that a test should find.

### Regression Tests Must Reproduce the Bug

1. Write the test **before** the fix
2. Verify the test **fails** without your fix
3. Verify the test **passes** with your fix

This ensures the test actually catches the bug, not just the happy path.

### Make Tests General

When improving tests, make the new test as general as possible while still catching the specific problem found. A test that catches a class of bugs is better than one that only catches the exact scenario you hit.

### Search for Similar Bugs

If a pattern caused a bug, search for similar patterns elsewhere in the codebase. Fix them all, or file separate issues for each.

## Review Process

### Code Simplification (Before Reviews)

**Before running review agents**, use the `code-simplifier` agent to clean up, simplify code, and verify documentation:

```
Task tool with subagent_type="general-purpose", prompt includes agents/code-simplifier.md instructions:

"Simplify PR #<NUMBER> (branch-name) at /path/to/worktree

Modified files:
- [list modified files]"
```

**Commit any simplifications before running reviews** — reviewers should see the cleanest version of the code.

### Run PR Reviews

Once the PR is complete, code is simplified, and CI is passing, run four parallel review agents (code-first, testing, skeptical, big-picture) using the Task tool with `subagent_type="general-purpose"`. Each agent should focus on one perspective and report findings without making edits.

### Handling Review Feedback

**Take all feedback seriously.** Freenet is complex code and we need to be perfectionists. Don't cherrypick easy wins and ignore harder issues. For each point raised:
- Fix it, OR
- Explain specifically why it's not applicable (with real justification, not convenience)

**The bar for ignoring feedback is HIGH.** Only dismiss a suggestion if it would dramatically increase complexity (like doubling the size of an already large PR). If a suggestion would improve the PR and can reasonably be done, do it.

Use common sense — if a reviewer suggests building a massive test framework for a small change, that's obviously overkill. But don't dismiss feedback just because it's inconvenient or would require more work.

**Never ignore tests to make them pass.** Flaky tests are broken tests — fix the root cause, don't hide the symptom.

**Never remove existing tests or fix code.** If tests are failing, understand why and fix the underlying issue. Removing tests that catch bugs is how regressions happen.

### Waiting for CI

CI typically takes ~20 minutes. Use:

```bash
gh pr checks <PR-NUMBER> --watch
```

### Responding to Reviews

1. **Fix all issues** found during review before requesting re-review
2. **Respond to inline comments inline** — Don't just fix silently
3. **If you disagree**, explain your reasoning rather than ignoring the comment
4. **After fixing**, leave brief replies like "Fixed" or "Addressed in [commit SHA]"
5. **Re-request review only after substantial changes** — Don't re-ping reviewers for minor tweaks

## PR Scope

### Keep PRs Focused

- One logical change per PR
- If a fix reveals other issues, file separate issues rather than scope-creeping
- If the PR grows too large, consider splitting it (but avoid complex stacked PRs)

### Wiring Completeness

When a PR adds or modifies enum dispatch (operation types, outcome handling, event routing), the test must exhaustively verify all variants produce the expected result. Common gaps: `outcome()` returning `Irrelevant` for some operation types, match arms with `_ => {}` catch-alls that silently discard new variants, commented-out enum arms.

### Resource Invariant Assertions

For any PR that touches data structures which accumulate entries (HashMaps, Vecs, channels, caches), include assertions that sizes stay bounded after sustained operation. Every insert path must have a corresponding cleanup path that runs on both success and failure/timeout. If the cleanup path isn't obvious, document it in a code comment.

### Don't Cut Corners

- Don't weaken tests to make them pass
- Don't add `#[ignore]` - fix the test or don't merge
- Don't leave `TODO` comments for things you could fix now
- Don't skip edge cases because "they probably won't happen"

## Attribution

End all GitHub content (PR descriptions, comments, issues) with:

```
[AI-assisted - Claude]
```

## Bug-Prevention Patterns (Feb 2025 fix review)

These 5 patterns caused ALL 25 bugs in releases 0.1.147–0.1.150. When your PR introduces or modifies code matching these patterns, apply the corresponding rule:

| Pattern | Rule | Audit |
|---------|------|-------|
| `biased;` select | Per-iteration caps on high-throughput arms, document cancellation safety | `grep "biased;" crates/core/src/` |
| `GlobalExecutor::spawn` | Register JoinHandle with monitor; use `send()` not `try_send()` for critical paths; no catch-all `_ =>` in metrics | `grep "GlobalExecutor::spawn" crates/core/src/` |
| Connection removal / cleanup | Clean ALL related maps; filter peer lists to live connections; GC exemptions must have TTL | `grep "prune_connection\|drop_connection\|retain(" crates/core/src/` |
| Retry / backoff | Jitter ±20%; sleep interruptible via `select!`; zero-connection re-bootstrap; retry critical control msgs | `grep "tokio::time::sleep" crates/core/src/` |
| Deployment | Declare exit codes to service manager; gate auto-update on release; test security against app needs; remove unused deps | `cargo machete` |

Full rules: `.claude/rules/code-style.md`, `.claude/rules/ring.md`, `.claude/rules/transport.md`, `.claude/rules/deployment.md`

## Checklist Before Merging

- [ ] PR title follows Conventional Commits format
- [ ] PR description explains WHY, not just WHAT
- [ ] All local checks pass (fmt, clippy, test)
- [ ] E2E tested if applicable (network/contract changes)
- [ ] Regression test added that fails without fix
- [ ] Answered "why didn't CI catch this?" and documented gap
- [ ] **CI gap closed** — added the missing test that would have caught this bug class before merge (not just a narrow symptom test)
- [ ] **Simulation health tested** if PR touches routing/topology/operations/subscriptions — key metrics (subscribe rate, GET rate, tree formation) asserted in simulation tests
- [ ] **Bug-prevention patterns checked** — if PR touches select!/spawn/cleanup/backoff/deployment, verify compliance with the 5 rules above
- [ ] CI passing
- [ ] **PR review completed** (code-first, testing, skeptical, big-picture review agents)
- [ ] All review feedback addressed (fixed or explained why not applicable)
- [ ] All human review feedback addressed
- [ ] Responses posted to review comments

## After PR Merges

Clean up your worktree to free disk space (each worktree has its own target/ directory):

```bash
cd ~/code/freenet/freenet-core/main
git worktree remove ../fix-<issue-number>
git branch -d fix-<issue-number>  # Delete local branch
```
