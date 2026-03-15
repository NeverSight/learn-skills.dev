---
name: agent-best-practices
description: Field-tested engineering principles. Apply when writing, modifying, or reviewing code. Emphasizes verification over assumption, scope discipline, root cause analysis, staying current, and automation. These principles are distilled from real project experience and hundreds of debugging sessions.
license: MIT
metadata:
  author: sceiler
  version: "1.0.0"
---

# Agent Best Practices

Field-tested principles from a decade of software development, IT consulting, and web development. These rules are distilled from real project experience, hundreds of debugging sessions, and patterns observed across 167+ chat histories with AI coding assistants.

## Core Philosophy

**Never assume. Always verify.**

Code that hasn't been tested is broken code you haven't discovered yet. A fix you haven't verified isn't a fix—it's a hypothesis.

---

## 1. Verification & Testing (CRITICAL)

### `verify-never-assume`
**Never say "fixed" without running verification.**

Don't claim something works until you've proven it. Run the build, run the tests, visually check the output.

- For code changes: run `build` and `test` commands
- For UI changes: describe what to visually verify
- For data changes: show sample output proving correctness
- If verification cannot be done locally, say so explicitly
- Ask user to confirm fix works before moving to next task

### `verify-all-environments`
**Solutions must work everywhere, not just locally.**

"Works on my machine" is not sufficient. Consider:

- Environment variables: verify they exist in ALL environments (local, CI, production)
- Build behavior: local build ≠ CI build (different env, caching, timing)
- Platform differences: Windows, macOS, and Linux behave differently
- Version differences: Node.js version on local must match deployment
- Note when something "works locally" is not sufficient verification

### `verify-test-after-changes`
**Always run tests after making changes.**

Never assume your change is safe. Run the existing test suite to catch regressions. If tests don't exist, this is a signal to write them.

### `verify-manual-check`
**Automated tests are not enough.**

Tests catch regressions, but you must also verify actual behavior matches intent. Run the code, check the output, confirm it does what was requested.

### `verify-build-succeeds`
**A passing test suite means nothing if the project doesn't build.**

Always run the build command before considering work complete. TypeScript errors, lint errors, and build failures must be resolved. Zero tolerance for lint/TypeScript errors.

---

## 2. Scope Discipline (CRITICAL)

### `scope-respect-keywords`
**"Just", "only", "simple" = minimum viable change ONLY.**

When you see these keywords, limit yourself to the EXACT request:

| Keyword | Required Response |
|---------|-------------------|
| "just", "only", "simple", "don't add" | Limit to EXACT request, no extras |
| "check", "verify", "test" | MUST execute verification and report results |
| "carefully", "thoroughly" | Extra testing, full verification |
| "again", "still", same issue repeated | Stop guessing, do root-cause analysis |

Example: User says "just add schema SEO breadcrumbs" → do NOT propose full visual breadcrumb UI components.

### `scope-no-extras`
**Do NOT add improvements, refactoring, or "nice to haves".**

If something seems like it should be done, mention it as a suggestion but don't implement unless asked.

- A bug fix doesn't need surrounding code cleaned up
- A simple feature doesn't need extra configurability
- Three similar lines of code is better than a premature abstraction
- Don't add error handling for scenarios that can't happen
- "Heading is too long and flows over" → minimal CSS fix only, not component refactor

### `scope-suggest-dont-implement`
**If you see potential improvements, mention them—don't do them.**

Your job is to complete the requested task. Additional improvements should be proposed for the user to approve, not silently implemented.

---

## 3. Root Cause Analysis (HIGH)

### `root-cause-stop-guessing`
**If the same issue appears twice, STOP making surface-level fixes.**

When a fix doesn't work:

1. Don't try another quick fix
2. Perform deep investigation
3. Trace the issue to its actual origin (state management, CSS specificity, data flow)
4. Ask for diagnostic information if needed
5. Don't guess repeatedly—investigate systematically

Real example: Mobile menu focus state persisting after close took 4 messages to fix because surface-level fixes didn't address the real problem.

### `root-cause-trace-origin`
**Find where the problem actually starts.**

Issues often manifest far from their source:

- State management bugs appear as UI glitches
- Data model issues appear as wrong calculations
- CSS specificity problems cascade to multiple components
- Import order issues cause mysterious runtime errors

### `root-cause-investigate-implausible`
**When values seem implausible, investigate the source data first.**

Don't trust outputs that don't make sense. If a dashboard shows 916 views for a day but individual blog posts show far fewer, something is wrong with the data model (cumulative vs. daily totals), not the display.

### `root-cause-data-assumptions`
**Explicitly state data model assumptions before writing aggregation code.**

Cumulative vs. incremental metrics must be explicitly clarified upfront. Verify calculations with real sample data before declaring completion.

---

## 4. Regression Prevention (HIGH)

### `regression-consider-side-effects`
**Before any change, consider what else might be affected.**

Changes cascade. Before editing:

- CSS/styling changes: check all components using same classes/variables/tokens
- Shared utilities: check all consumers
- Data model changes: trace through all usages
- API changes: verify all callers

Real examples of regressions:
- Styling fixes caused OG images to break
- Title formatting fixes caused rendering issues
- Heading colors changed after an unrelated fix

### `regression-run-full-suite`
**Run the full test suite, not just tests for the changed code.**

Your change might break something unrelated. The test suite exists to catch this.

### `regression-mention-verification-areas`
**Explicitly mention what areas might need manual verification after changes.**

When completing a task, list the areas that could be affected and should be checked.

---

## 5. Clarification Over Assumption (HIGH)

### `clarify-ask-before-acting`
**When request is ambiguous, ASK before acting.**

Good clarifying questions:

- "Do you want X or Y approach?"
- "Should I also include Z or just focus on X?"
- "I want to confirm: you're asking for [specific interpretation], correct?"

Real example: Biography tone—user wanted "blend of personal and professional" but agent assumed "personal" only.

### `clarify-especially-for`
**Always clarify for: design decisions, scope boundaries, and user preferences.**

Never assume:

- Design direction (visual UI vs. schema-only)
- Tone and style (professional vs. casual)
- Scope boundaries (fix this one thing vs. fix related issues too)
- Technology preferences (which library, which approach)
- User's background, timeline, or personal preferences

---

## 6. Staying Current (HIGH)

### `current-update-dependencies`
**Reject "never change a running system" mentality.**

Keeping dependencies updated provides:

- Security patches
- Performance improvements
- Access to new capabilities
- Better developer tooling

Outdated dependencies accumulate technical debt that compounds over time. Automate minor/patch updates; reserve major versions for manual review.

### `current-check-versions`
**Always check versions before implementing features.**

Framework APIs change between versions:

- Check `package.json` for installed versions
- Confirm which router/paradigm is being used (App Router vs Pages Router)
- App Router: No direct `<head>`, use `generateMetadata` instead
- Reference documentation for the specific version
- When in doubt about approach, ask which pattern the user prefers

### `current-leverage-framework-updates`
**Framework and tooling updates often yield significant wins without code changes.**

Real example: Upgrading Next.js 15 → 16 yielded 24-second build time reduction (82s → 58s) without code changes. Infrastructure improvements are leverage.

---

## 7. Simplicity & Performance (MEDIUM)

### `simple-content-over-flash`
**Focus on content over flashy features.**

Minimal, clean design eliminates distractions. Readers should concentrate on substance rather than visual embellishment.

### `simple-measure-everything`
**"What gets measured gets improved."**

Use performance monitoring tools:

- Lighthouse / PageSpeed Insights
- Framework-specific analytics (Vercel Speed Insights)
- Build time tracking across deployments

Track changes systematically to identify what delivers real impact versus marginal gains.

### `simple-hardware-over-clever-code`
**Slow machines are a tax you pay every day.**

Sometimes throwing money at the problem (faster CI machines, better hardware) is the correct and cheapest solution long-term. Don't over-optimize code when infrastructure upgrades solve the problem.

### `simple-infrastructure-first`
**"Almost all meaningful build time improvements came from upgrading software and using faster hardware, not from changing application code."**

Try framework upgrades, tooling updates, and hardware improvements before complex code optimization.

---

## 8. Quality Over Quantity (MEDIUM)

### `quality-fewer-high-value`
**Fewer, thoroughly researched, high-value outputs surpass frequent low-quality ones.**

Each piece of work should genuinely serve its purpose. Don't rush to produce more; focus on producing better.

### `quality-accessible`
**Accessibility is mandatory, not optional.**

Follow WCAG guidelines to ensure usability across all ability levels and devices.

### `quality-syntactically-valid`
**Every code suggestion must be syntactically valid and complete.**

- Don't suggest partial code without surrounding context
- Test edge cases, not just the happy path
- Trace through logic mentally before proposing changes
- When suggesting regex/logic changes, mentally trace through the exact pattern

---

## 9. Workflow & Automation (MEDIUM)

### `workflow-branch-always`
**Never commit directly to main.**

Create a new branch BEFORE writing ANY code. Use descriptive names: `feature/add-search`, `fix/header-alignment`, `refactor/api-utils`. Committing directly to main is forbidden unless explicitly permitted.

### `workflow-test-before-commit`
**Run tests BEFORE every commit.**

NEVER assume code works. Prove it. Run unit tests, then commit.

### `workflow-commit-incrementally`
**Commit after EACH completed task, not in batches.**

Small, atomic commits create clean git history and make reverting easier. Make a local commit immediately after completing each todo item.

### `workflow-pr-when-done`
**Create a Pull Request when work is complete.**

After pushing, automatically create a PR. PRs enable review, discussion, and CI verification before merging.

### `workflow-automate-repetitive`
**Automate tedious routine tasks.**

If you do something manually more than a few times, it should be scripted or automated:

- Dependency updates (daily for minor/patch, weekly for actions)
- Build and deployment
- Testing workflows
- Monitoring and alerting

Reduced friction encourages regular maintenance.

---

## 10. Backward Compatibility (MEDIUM)

### `compat-preserve-links`
**Preserve existing canonical links.**

When restructuring URLs or identifiers:

- Maintain backward compatibility for existing links
- Set up redirects for changed paths
- Never break bookmarks or external references (SEO impact)

### `compat-plan-for-duplicates`
**Never assume uniqueness of metadata.**

When generating identifiers from content (slugs, IDs):

- Plan for duplicate values upfront
- Use guaranteed-unique properties (database IDs) as fallbacks
- Automate collision detection
- First occurrence: clean slug; subsequent: append unique suffix

---

## 11. Security Awareness (MEDIUM)

### `security-no-secrets-in-code`
**Never commit secrets or credentials.**

API keys, passwords, tokens—none of these belong in code. Use environment variables or secret management systems.

### `security-validate-input`
**Validate all external input.**

Never trust data from users, APIs, files, or environment variables. Validate before using.

### `security-block-at-edge`
**Implement defensive rules at infrastructure level, not just application level.**

Block malicious requests (probing for PHP vulnerabilities, DDoS) at the edge/firewall before they reach your application. Zero-trust for unexpected protocols—if your app is Next.js, any `.php` request is automatically suspicious.

---

## 12. AI Collaboration Principles (MEDIUM)

### `ai-claude-md-is-essential`
**Create a project-specific instruction file (CLAUDE.md) that the agent reads at every session.**

Include:
- Workflow rules (with strong imperative language at the beginning)
- Build commands
- Architecture overview
- Coding patterns

This consistency creates predictable output.

### `ai-outcome-over-specification`
**Describe what needs to happen, not every implementation detail.**

Your role becomes strategic direction-setting, not micro-management. AI amplifies whatever level of understanding you bring to the table.

### `ai-you-remain-architect`
**Architecture choices need human input.**

When multiple valid approaches exist, the agent proposes solutions but needs steering toward your preferred direction. You provide the strategic decisions.

### `ai-leverage-external-knowledge`
**Connect to live documentation sources rather than relying on potentially outdated training data.**

Use MCP servers for current platform information. Domain-specific knowledge (like optimization patterns from real codebases) compounds results better than generic advice.

### `ai-embrace-iteration`
**Complex features take multiple commits to perfect.**

AI maintains context, remembers previous attempts, and builds progressively. Tests enable confident iteration by creating a growing safety net.

---

## Quick Reference Checklist

Before completing any task:

- [ ] Did I understand the exact scope? (watch for "just", "only", "simple")
- [ ] Did I verify the fix actually works? (build, test, visual check)
- [ ] Could this change affect anything else? (regressions)
- [ ] Am I using the correct API for this framework version?
- [ ] Do environment variables exist everywhere they're needed?
- [ ] If this is a repeated issue, did I do root-cause analysis?
- [ ] Did I ask clarifying questions for ambiguous requests?
- [ ] Is my data logic correct? (cumulative vs. incremental, sample verification)

---

## Keyword Response Guide

| User Says | Your Response |
|-----------|---------------|
| "just", "only", "simple", "don't add/change" | Minimum viable change ONLY |
| "check", "verify", "test", "double-check" | MUST execute verification and report results |
| "carefully", "thoroughly", "be careful" | Extra testing, full verification before completion |
| "again", "still", same issue repeated | Stop guessing, do root-cause analysis |
| "try again" | Previous approach failed, need different strategy |

---

## Summary

These principles are distilled from real experience—not theory:

1. **Verify everything** - Never assume code works
2. **Respect scope** - Do what's asked, nothing more
3. **Find root causes** - Don't apply surface fixes repeatedly
4. **Prevent regressions** - Consider side effects before changes
5. **Clarify ambiguity** - Ask before assuming
6. **Stay current** - Update dependencies, leverage frameworks
7. **Keep it simple** - Measure, optimize infrastructure first
8. **Prioritize quality** - Fewer, better outputs
9. **Automate workflows** - Branch, test, commit, PR
10. **Maintain compatibility** - Preserve existing links
11. **Think security** - Validate input, block at edge
12. **Collaborate effectively** - Use CLAUDE.md, describe outcomes, remain the architect

These aren't theoretical guidelines—they're lessons learned from hundreds of debugging sessions, regressions, and fixes that didn't actually fix anything until properly verified.
