---
name: anti-slop-engineering
description: Prevent, detect, and repair AI coding slop and dirty engineering in repositories. Use for planning features, writing code, changing tests, reviewing pull requests, refactoring, hardening CI, debugging regressions, or auditing agent-generated changes. Enforces behavioral contracts, focused diffs, test integrity, repo conventions, security boundaries, and evidence-based completion.
author: Mamdouh Aboammar <mamdouhfces1997@gmail.com>
license: MIT
metadata:
  version: "1.0.0"
  focus: "engineering-discipline"
  repository: "https://github.com/imMamdouhaboammar/anti-slop-engineering"
---

# Anti-Slop Engineering

**Mission:** Deliver the smallest *coherent, correct, maintainable* change supported by independent evidence. Never trade contract integrity, security, or reviewability for a green CI badge. Enforce Google Site Reliability Engineering (SRE) principles: Simplicity (KISS), Single Source of Truth (DRY), Anti-Speculation (YAGNI), and Fixing Issues at Scale (Eliminating Toil). Incorporate clean-room Stop-That-Shit boundary interception, Senior Dev ladders, and high-performance Rust/Go microservices. This skill applies to human and AI-authored changes equally.

## Operating priorities

1. Explicit user requirements, repository architecture, security policy, and existing public contracts outrank aesthetic preferences.
2. Preservation of authorized existing behavior outranks making a new implementation pass its own tests.
3. Prove behavior before polishing style; fix correctness and security blockers before cosmetic issues.
4. Minimize **unnecessary** complexity, not required tests, safety checks, or clarity. A short but incorrect solution fails.
5. Do not declare a finding without file/line evidence and an impact story. Never invent tool results or test runs.
6. Never change or approve unrelated code, tests, policies, dependencies, CI, or infra merely to make the current request pass.
7. **Official boilerplate & installers over manual scaffolding:** For any greenfield project, service, framework, library, or SDK integration, agents MUST rely on the official CLI installer, starter boilerplate, or generator (e.g., `uv init`, `cargo init`, `bun create`, official SDK quickstarts). Never manually hand-roll ad-hoc scaffolding, arbitrary directory layouts, or loose config files by hand.
8. **Strict latest stable versioning:** When installing, initializing, or introducing any new dependency, library, or SDK, strictly query the registry and pin the **latest stable version**. Never guess outdated versions from training memory or rely on obsolete templates.
9. **Taste, Visual Restraint & Clean UI Microcopy:** Never clutter user interfaces with walls of text, repetitive explanations, or overcrowded navigation bars. Respect visual hierarchy, purposeful white space, and minimal, polished microcopy. Eliminate gratuitous widgets, stat pills, or icon clutter.
10. **Zero Dev-Notes Leakage in User-Facing UI:** Never render internal developer instructions, agent reminders, mock disclaimers, or architecture apologies (`"Note: In production..."`, `"Mock data displayed"`, `"TODO: Add auth"`) into user-visible DOM/JSX. Keep internal technical context strictly in code comments or project design documents.
11. **Documentation Restraint & Zero Speculative Docs:** Never generate unprompted documentation files, submission dossiers, reviewer packets, or platform guides (e.g. "Publish to OpenAI ChatGPT Plugins", fake marketplace submission dossiers, speculative deployment recipes). Never cite dead, deprecated, or hallucinated third-party submission portals (e.g. `platform.openai.com/plugins`). Keep documentation strictly factual, lean, and grounded in real, requested repository capabilities. Reject documentation file sprawl and ceremonial note callouts.
12. **The Zero-Obviousness & Direct Payload Doctrine:** Strictly eliminate trivial syntax narration, tautological docstrings, patronizing UI microcopy, ceremonial documentation truisms, and affordance narration. All documentation, code, and interfaces must adhere to the **Direct Payload Invariant**: transition directly from domain headers into technical payloads (code, tables, media, schemas) with ZERO conversational preambles ("The following table outlines..."), ZERO affordance narration ("click to play/expand/copy/scroll", "watch here without leaving the page"), ZERO mechanical hand-holding ("open your terminal", "save the file"), and ZERO bilingual title-stacking or promotional buzzword inflation. Standard UI affordances and technical payloads speak for themselves; silence and clarity outrank noise.
13. **Google Site Reliability Engineering (SRE) Discipline:** Enforce the four foundational Google SRE principles across all changes:
    - **KISS (Simplicity as a prerequisite to reliability):** Keep cyclomatic nesting <=4 levels. Functions exceeding 80 lines must be decomposed into single-responsibility units. Reject pass-through wrapper chains that add no value.
    - **DRY (Single source of truth):** Replicated invariants, duplicated validation patterns, or parallel error structures are reliability hazards. Consolidate into canonical modules.
    - **YAGNI (Anti-speculative engineering):** Zero speculative parameters (`_unused_param`, `future_kwargs`), dead branches (`if False:`), or placeholder stubs. Build for active requirements only.
    - **Fix Issues at Scale (Eliminating toil & distributed resilience):** Automate repetitive manual toil. Enforce exponential backoff with full jitter on all network retries to avoid retry storms. Never use `sleep()` as an async race band-aid. Bound concurrency and enforce idempotency on state-changing endpoints.
14. **Clean-Room Senior Dev Ladder & SHIT Interception (Ponytail, STS, Boring Engineering):**
    - Intercept the four SHIT hazards: Scope creep (`S`), Hypothetical hardening/unread companion hashes (`H`), Intent violation (`I`), and Task thrashing (`T`).
    - Climb the Senior Dev Ladder before authoring code: (1) Does this need to exist? (2) Does it already exist in the codebase? (3) Does the stdlib/platform do it? (4) Does native runtime cover it? (5) Does an existing dependency solve it? (6) Can it be a direct expression? (7) Write only minimal, necessary, tested code.
    - **Name the Built-in:** Before writing custom parsing, validation, or UUID/cloning utilities, name the platform built-in (`crypto.randomUUID()`, `URLSearchParams`, `structuredClone()`). Hand-rolling standard primitives is a defect.
    - **Practical DRY 3-Point Barrier:** Shared utilities or abstractions are permitted only when appearing in >=2 real existing call-sites, when all call-sites require identical modifications upon change, and when the abstraction can be named without coordinating conjunctions (`and`, `or`).

## Activation / modes

Select the relevant mode and follow the same gates:

- **BUILD:** new feature or behavior change. Baseline -> contract -> RED -> GREEN -> REFACTOR -> independent review -> evidence.
- **FIX:** reproduce observed bug first, fix smallest root cause, prove regression tests hold.
- **REVIEW:** read-only diff and repository-context audit; report findings with severity, evidence, and counterfactual.
- **CLEANUP:** establish an observable behavior baseline, isolate pure refactors from feature changes, prove no drift.
- **NOTED_SLOP:** codify newly observed AI slop into a diagnostic catalog pattern, agent directive, and automated diff guard heuristic (see [CONTRIBUTING.md](CONTRIBUTING.md)).

For extensive audits, load [anti-pattern catalog](references/anti-pattern-catalog.md). For Google SRE discipline and distributed resilience patterns, load [google-sre-discipline](references/google-sre-discipline.md). For any test changes, load [test integrity policy](references/test-integrity.md). For a PR or merge request, load [PR review protocol](references/pr-review.md). For elevated permissions, sensitive code, network access, or deployment, load [security and execution boundaries](references/security-and-operations.md). For project-specific exceptions, load [judgment and exceptions](references/engineering-judgment.md). For community contributions, follow [contributor guidelines](CONTRIBUTING.md).

## The seven gates

### Gate 0: Discover; do not improvise the repo

- Read root and scoped instructions (AGENTS.md, CLAUDE.md, contributing docs), task and acceptance criteria, package manifests, lockfiles, CI, and nearby implementation/tests.
- Identify language/framework versions from the actual repo, not what is newest. Identify existing helpers, types, error patterns, transaction boundaries, observability, API contracts, and test commands.
- Read relevant open issues/PRs when available to avoid duplicates or fighting in-flight changes. Do not require network access to proceed when unavailable.
- Record working tree status; do not overwrite user changes, reset, stash, or modify unrelated files without authorization.
- Run an appropriate baseline build/test if feasible; label any existing failure as baseline, not caused by this change.
- For new projects, services, components, or SDK integrations, identify the official installer, CLI generator, and canonical starter boilerplate before writing code. Do not manually assemble configurations or directory trees from memory. Never generate unprompted documentation files, submission dossiers, or speculative third-party platform guides.

### Gate 1: Establish a change contract

Before editing, note: **what changes, what must not change, business invariants, external APIs, expected failures, data impacts, security implications, rollback plan, and proof requirements.** For a task without a formal spec, derive a provisional contract from source + existing tests + user request, label uncertainties, and choose a conservative implementation.

Create a tiny scope plan: target files, candidate reuse, test points, risk areas. Identify any migration, locking/concurrency, auth, and data retention impacts explicitly. Ask for approval only for material externally visible ambiguity or destructive action; otherwise proceed conservatively and report assumption.

### Gate 2: Lock the baseline tests without freezing legitimate evolution

- Inspect existing regression tests **before implementation**. Prefer independently specified expected outcomes.
- On bug fixes, write a failing reproduction first where practical. On new behavior, write tests for the agreed contract before implementation where practical.
- Existing assertions/fixtures/snapshots are protected: if a test fails after a change, investigate implementation/regression first. Never weaken assertions, rewrite golden values, remove coverage, mark skipped/xfail, or add exclusions merely to get green.
- Existing tests *may* change when the approved behavior genuinely changes, an assertion was incorrect, or a justified test refactor is necessary. Explain **old contract -> new contract**, cite the authority, show before/after behavior, and obtain independent review on semantics.
- Do not blindly ban test edits or insist on unit tests for every I/O interaction. Select unit/integration/contract/E2E based on risk. See [test integrity](references/test-integrity.md).

### Gate 3: Implement with minimum justified complexity

- **Official tooling over manual scaffolding:** When initializing an application, module, or SDK integration, invoke the official CLI installer / starter generator rather than manually typing out build configurations (`tsconfig.json`, `package.json`, `pyproject.toml`, Dockerfiles, etc.).
- **Strict latest stable dependency pinning:** When adding new dependencies or SDKs, always query the package manager or registry to install the latest stable release (e.g. `bun add <pkg>@latest`, `uv add <pkg>`). Pin versions strictly in manifests and generate valid lockfiles; never rely on pre-cutoff memory.
- **Frontend taste & zero dev-notes leakage:**
  - Strip out all internal developer/agent annotations, reminders, or mock warnings (`"TODO: Wire backend"`, `"Note: Mock data"`, `"Agent notice:"`) from user-visible DOM/JSX.
  - Practice visual restraint: prevent crowded navbars, multi-row icon spam, or redundant controls in headers. Maintain clean visual hierarchy, balanced padding, and purposeful negative space.
  - Enforce concise microcopy: avoid walls of explanatory text, repetitive instructions for obvious user actions, and defensive disclaimers. Every string in the UI must be concise and production-grade.
- **Anti-logorrhea in code & interfaces:** Avoid writing unnecessary boilerplate, sprawling repetitive wrappers, or comments that merely narrate obvious syntax. Never bloat code or copy just to feel comprehensive.
- **Zero-obviousness & anti-truism:** Reject code comments that narrate obvious syntax (`// return response`, `// increment i`, `// check if null`), tautological docstrings that merely restate symbol names, patronizing UI microcopy under obvious inputs (`"Please enter your email"` under an Email field), and documentation padded with trivial prerequisite truisms ("requires internet and keyboard"). High engineering discipline favors silence over noise.
- Modify the existing abstraction whenever it fits; do not add parallel services, helpers, frameworks, compatibility layers, or configurable interfaces without a current need.
- Keep business logic separate from transport and presentation when supported by the architecture; avoid both god objects and needless micro-files.
- Use existing dependencies and repo conventions. New dependency requires clear functionality, maintenance, license, security, and bundle/runtime case.
- Maintain error semantics, resource cleanup, cancellation, idempotency, state isolation, data validation, correct authorization, transactions, and backwards compatibility where required.
- Avoid broad formatting/restructuring in functional PRs; remove incidental scaffolding that adds no value. Do not delete working behavior to make the diff smaller.

### Gate 4: Verify beyond green tests

- Run targeted tests and impacted full-suite checks supported by repo; report commands and outcomes verbatim or as reproducible summaries.
- Inspect changed tests against the baseline; manually verify independently expected outcomes. Test the old failure, the new behavior, negative paths, and nearby regressions.
- Exercise boundary tests relevant to change: contract/integration, concurrency, migrations, browser flow, performance, security and accessibility where applicable. Prefer real integration evidence over test doubles at critical seams.
- Treat test coverage, lint, snapshot updates, and static-scan results as *signals*, never proof. Use mutation tests for fragile business rules when available.
- If tools/environment prevent verification, say **NOT VERIFIED**; list exact blockers and do not claim completion.

### Gate 5: Audit the diff as a skeptical reviewer

Run `git diff --check` and inspect `git diff --stat`, changed files, changed assertions, added dependencies, config, and documentation. Triage can be executed via high-performance native Rust/Go microservices or portable Python scripts:

```bash
# Native Rust Engine (SHIT Boundary Interceptor & Senior Dev Ladder):
bunx anti-slop-engineering rust triage
bunx anti-slop-engineering rust shit-check --diff patch.diff

# Go High-Throughput SRE Engine (KISS nesting, DRY token window, Toil & Error Budget):
bunx anti-slop-engineering toil audit
bunx anti-slop-engineering toil stream

# Zero-dependency Python Core Fallback:
python scripts/diff_guard.py --base HEAD --json
python scripts/sre_guard.py --base HEAD --strict --json
```

Replace `origin/main` with your actual target branch; if unavailable, compare with a known commit using `--base HEAD`. If new files are untracked, stage only intended files *when authorized*, then re-run; the tool warns that untracked contents are excluded. **Regex flags (including trivial comment narration, patronizing UI copy, speculative docs, dev notes, and SRE scale hazards) are candidates for investigation, not confirmed defects.** The tool neither runs tests nor performs SAST.

Ask explicitly: Could a smaller design do the same thing (KISS)? Did I create two sources of truth (DRY)? Are all parameters and options actively used (YAGNI)? Will retries trigger thundering herds or retry storms under scale (SCALE)? Did I silently expand scope?

### Gate 6: Evidence and release decision

Use [PR review protocol](references/pr-review.md) and the report template at [RUN_REPORT_TEMPLATE](assets/RUN_REPORT_TEMPLATE.md).

- **BLOCK:** demonstrated critical regression; authorization/security/privacy failure; disabled or falsified tests without approved change contract; broken build; destructive migration without safety plan.
- **REWORK:** meaningful duplication, needless architecture, unjustified new dependency, test-only-for-implementation, unexplained contract drift, unreviewable mixed changes.
- **REVIEW:** large coherent changes, cosmetic smells, static heuristics, deliberate test updates or exceptions requiring context.
- **PASS:** requirements met with observable evidence; no unresolved BLOCK or REWORK, risks and exceptions documented. PASS is not a warranty.

Before proposing merge, report: intent, changed files, exact test evidence, baseline test delta, remaining uncertainty, findings, and decision. Do not merge, deploy, or alter protected settings without permission and applicable controls.

## Non-negotiable anti-cheating rules

- Do not change a test's expected output to match the observed buggy output unless the new output is explicitly authorized by product contract.
- Do not delete, skip, xfail, downgrade, mock away, or suppress a failing test to conceal a failure.
- Do not use fake logs, fabricated benchmarks, imagined browser screenshots, test results, or invented source references.
- Do not weaken lint/type/security/branch protection/CI policies simply to achieve success.
- Do not modify lockfiles, dependencies, formatting, codegen, database schemas, or test fixtures as collateral damage.
- Do not replace a targeted fix with a full rewrite without evidence and scope approval.
- Do not manually scaffold project skeletons or hand-stitch configuration files when official language, framework, or SDK installers and boilerplates are available.
- Do not pin outdated, deprecated, or guessed dependency versions from model training memory; always resolve and enforce the latest stable version from the official registry.
- Do not render developer notes, agent reminders, mock disclaimers, or architectural apologies into user-facing JSX/HTML views.
- Do not overcrowd headers, navbars, or dashboards with uncurated icons, redundant buttons, or gratuitous widgets that lack visual hierarchy.
- Do not bloat UI copy with walls of explanatory text, defensive disclaimers, or verbose narration of obvious UI controls.
- Do not write trivial syntax-narration comments (e.g. `// return result`, `// increment counter`, `// check null`) or tautological docstrings that merely restate symbol names.
- Do not add patronizing UI microcopy or obvious instructional labels underneath self-evident controls (e.g. `"Please enter your email"`, `"Click here to submit"`).
- Do not pad documentation, READMEs, or setup guides with obvious truisms, trivial prerequisite lists, or tautological summaries.
- Do not violate the Direct Payload Invariant: never write affordance narration (explaining how to click, expand, play, scroll, or copy standard controls), conversational preambles ("The following section discusses..."), bilingual title-stacking (e.g. `Term · الترجمة`), buzzword inflation (calling screencasts "Live Interactive Demos"), or mechanical hand-holding in documentation and code.
- Do not generate speculative submission dossiers (e.g., `docs/*SUBMISSION*.md`, `docs/*DOSSIER*.md`) or invent publishing guides for unrequested third-party platforms.
- Do not cite dead, deprecated, or hallucinated platform URLs (e.g., `platform.openai.com/plugins`).
- Do not sprawl the repository with ceremonial markdown files or pad READMEs with marketing filler, fake prompt examples, or repetitive note callouts.
- Do not use arbitrary `sleep()` or hardcoded delay loops as a synchronization band-aid for async races or flaky tests.
- Do not retry failing network operations without exponential backoff and randomized full jitter.
- Do not spawn unbounded parallel tasks, workers, or promises without explicit concurrency limiters or backpressure signals.
- Do not swallow errors silently with empty `except: pass` or `catch {}` blocks without structured logging or metric counters.
- Do not introduce speculative parameters (`_unused_param`, `future_kwargs`), dead feature toggles (`if False:`), or unreferenced extension points.
- Do not duplicate domain invariants, validation rules, or error models across multiple modules; maintain a single authoritative source of truth.
- Do not over-restrict legitimate design: duplication in readable tests can be preferable to an unreadable abstraction, and a larger implementation can be necessary for correct safety boundaries.

## Deliverable contract

For each implementation/review, produce a concise report in this order: **Outcome; Scope; Behavior preserved/changed; Verification (commands + results); Findings with exact file/line; Test modifications with rationale; Risks/limitations; Merge recommendation.** If available, distinguish baseline failures from new failures. Use `NOT RUN` and `UNKNOWN` literally when applicable.

The [catalog](references/anti-pattern-catalog.md) is diagnostic, not an instruction to create work where there is no evidence of a problem.
