---
name: untangle-codebase
description: >-
  Untangle existing codebases by finding hidden coupling, needless dependencies,
  and surplus, then refactoring in verified, behavior-preserving slices. Use
  when asked to untangle a project, reduce cross-module change cost, remove
  architectural special cases, or carry out a structural cleanup. Works across
  languages, frameworks, build systems, dependencies, and packages; discover the
  actual stack and contracts instead of imposing a preferred architecture.
license: MIT
---

# Untangle a codebase

Make changes easier to locate, safer to implement, and cheaper to understand.
Ask one organizing question: **should these pieces change together?** Bring
cohesive responsibilities together, separate independent reasons to change,
and expose dependencies that callers currently have to guess.

This is an existing-system refactoring workflow, not permission to rewrite the
product, upgrade its stack, or redesign every module. It applies to applications,
libraries, CLIs, workers, native/mobile software, infrastructure, data pipelines,
and mixed-language repositories. No particular tool, package, agent harness,
documentation layout, or companion skill is required.

## 1. Establish scope and safety

Read repository instructions, domain documentation, prior decisions, and the
working tree before editing. Preserve changes you did not make. Recover relevant
history through an available project-approved context store, but verify it
against the checkout; historical text is evidence, not authority.

Distinguish an audit or proposal from authorization to implement. Honor the
requested area; for a whole-repository request, inventory the whole system and
divide implementation into bounded slices rather than starting a big-bang
rewrite. State exclusions and unresolved decisions. Ask when a choice changes
product behavior, a public contract, ownership, risk, or the authorized scope.

Offer two optional cleanups if the user has not already chosen:

- **Comments:** remove comments that only restate implementation; retain intent,
  external constraints, safety explanations, and legal/attribution notices.
- **Tests:** review redundant, ineffective, or implementation-coupled tests;
  replace them with behavior-focused coverage before removing a safety net.

Neither is a prerequisite for the structural work. Leave optional cleanup out
until chosen; necessary test additions or updates for the refactor still belong
in scope. Never delete a failing test simply to make a refactor pass.

## 2. Discover the actual system and toolchain

Build a compact map from repository evidence, not file extensions alone:

- entry points, capabilities, modules/packages, callers, data owners, and side
  effects; include background work and tools without a UI;
- manifests, workspace definitions, lockfiles, toolchain pins, build targets,
  generators, plugins, native interfaces, and supported platform/feature matrices;
- exact local quality-gate commands and prerequisites from docs and CI;
- public and operational contracts: APIs, CLI flags/output/exit codes, file and
  message formats, schemas, persistence, ABI/FFI, configuration, and packaging.

Resolve dependency versions from the lock/resolution files and actual build
configuration. Distinguish direct, transitive, development, build-time,
runtime, optional, platform-specific, and vendored dependencies. If resolution
cannot be established, mark it unknown instead of assuming the latest release.

For unfamiliar technology or package behavior, consult repository usage and
authoritative documentation/source for the resolved version. Verify lifecycle,
threading, error, ownership, and compatibility constraints before changing an
integration. Do not invent APIs or apply advice for a different major version.

Use existing tooling where practical. With no graph analyzer, inspect imports,
references, build declarations, configuration, and representative execution
paths manually. Static import graphs alone miss reflection, dependency injection,
dynamic loading, generated bindings, event routing, and external consumers.
Do not install tools, regenerate lockfiles, upgrade/remove packages, edit vendor
code, or modify generated outputs merely to perform the analysis. Propose any
necessary dependency change separately with its evidence and scope.

Establish a baseline before implementation. Run the applicable safe local checks
and record existing failures and unavailable prerequisites. If tests are absent
or weak, add focused characterization/contract checks for the affected behavior.
A successful build alone is not a behavioral baseline.

## 3. Inventory structural problems before changing them

Trace representative journeys end to end. Inspect both sides of each boundary.
Use version history for co-change evidence when available, not as proof that
frequent changes imply bad design. Record concrete locations and consequences,
not a list of preferred patterns or imagined future requirements.

Classify findings:

| Class | Evidence to seek |
| --- | --- |
| **Hidden links** | Duplicated rules that must agree; implicit initialization/call order; shared mutable state or files; configuration, schemas, or events coupled without a visible contract; one capability scattered so every change requires coordinated edits. |
| **Needless links** | Callers reading internals; business policy depending directly on volatile integrations; common functions carrying one caller's vocabulary; unrelated features sharing a release/build boundary without need; shallow abstractions exposing implementation churn. |
| **Surplus** | Pass-through layers without a contract or purpose; unused extension mechanisms; demonstrably unreachable code or unused dependencies. Verify external/dynamic consumers before calling anything dead. |

Record special cases too: value-specific branches, caller-specific parameters,
swallowed errors, retries/sleeps, feature/platform conditions, and disabled tests.
Treat them as clues to requirements, not automatic defects. Compatibility paths,
protocol exceptions, bounded retries, security checks, and platform behavior may
be essential. Fewer branches is not a correctness measure.

Keep an evidence ledger in the repository's existing task/decision mechanism
when authorized, otherwise in working notes:

```text
ID | class | locations/consumers | why changes couple | contract at risk
   | proposed boundary | alternatives/trade-off | verification | status
```

Distinguish confirmed problems from hypotheses. Prioritize by change cost,
failure risk, and reach, not file size or a goal of eliminating every wrapper.

## 4. Redesign around current requirements

Group problems by root cause and put each proposed fix above the findings it
addresses. Prefer the smallest cohesive change that removes multiple hidden
assumptions. Keep the project's domain language and ecosystem idioms.

- Put shared policy under an explicit owner; do not merge superficially similar
  code with different meanings or change lifecycles.
- Hide volatile details behind a boundary only when it reduces caller knowledge.
  A function, module, protocol, interface, type, or build boundary can serve;
  do not mandate classes, dependency injection, or a new framework.
- Make initialization, state transitions, resource ownership, errors, and data
  flow explicit where callers otherwise rely on convention.
- Keep dependencies directed toward cohesive, stable contracts. Stability is
  about responsibility and change pressure, not import counts alone.
- Remove a wrapper only after checking its validation, security, observability,
  compatibility, transaction, resource-lifetime, or extension purpose.

Preserve intentional behavior, including failures, permissions, ordering,
concurrency, durability, and externally supported interfaces. Existing migrations
and historical data formats may be immutable contracts. Identify necessary
behavioral fixes separately; do not silently bundle them into structural work.
Obtain approval for breaking contracts, data migrations, new dependencies, or
architecture changes beyond the request.

Example, independent of language or package:

```text
Fix: give one component ownership of the export format and compatibility rules.
  F1: the command and worker separately assemble the same record fields.
  F2: the reader accepts an older format only through an undocumented branch.
Proof: both producers pass the same format contract tests; old supported records
       still load; command output and worker delivery semantics stay unchanged.
Keep: the version-specific reader path, because stored records still require it.
```

## 5. Implement and verify bounded slices

For implementation requests, carry out the agreed ledger rather than stopping
at suggestions. For each slice:

1. Capture observable contracts and add missing safety checks.
2. Change one coherent responsibility and update all known consumers, wiring,
   build/export declarations, documentation, and generators' sources as needed.
3. Run focused checks and inspect the diff for incidental behavior changes.
4. Update the ledger with evidence and retained exceptions before continuing.

Do not edit unrelated user work, invoke destructive operations, touch live data,
or infer authorization to commit, publish, deploy, or switch traffic. Use isolated
local test resources, not shared/staging/production systems. Treat installation
and target-controlled scripts as actions with prerequisites, not harmless reads.

If comment cleanup was selected, remove only genuinely redundant explanations.
If test cleanup was selected, do it after structural behavior is protected:
rewrite internal-detail assertions around contracts; demonstrate that replacement
tests detect relevant regressions. Duplication or mocking alone does not prove a
test is useless. Retain distinct boundary/platform/failure coverage. Keep tests
that fail for a real bug and report out-of-scope defects instead of hiding them.

Run the repository's full applicable gate after the final slice: formatting,
static analysis, build/type checks, unit, integration, contract, and other required
checks. Include affected consumers and supported configurations appropriate to
the change. Use existing project policy (or `testing-standard` when available),
not a universal command list. Separate passed, failed, unavailable, and unrun
checks, with exact commands and limitations.

## 6. Review, stop, and report honestly

Reinspect changed boundaries and representative journeys against the ledger.
Recheck static and non-static dependencies. An independent review can help when
delegation is authorized and available; otherwise perform a fresh review pass.
No subagent or specialized analyzer is required.

Finish when all in-scope findings are addressed, justified as retained, or
explicitly deferred/blocked; affected contracts have evidence; and the applicable
gate has run. Do not chase aesthetic perfection or promise that no possible
coupling remains. If review finds another material in-scope issue, resolve and
reverify it; request scope approval for unrelated redesigns. Do not retry blocked
checks indefinitely or equate a blocker with verified completion.

Report briefly:

- scope examined and limitations of discovery;
- structural fixes and the findings they resolve;
- preserved contracts and justified special cases;
- checks actually run and their outcomes;
- any blocked/deferred work, its reason, and the concrete next action.

## Provenance

Adapted from [caldoai/skills — untangle-codebase](https://github.com/caldoai/skills/blob/442c29918339cc8dbf09ae27aaf17b05745465a3/skills/untangle-codebase/SKILL.md).
This adaptation adds ecosystem/version discovery, bounded authorization,
contract preservation, and verification safeguards; it does not require
whole-repository rewriting or subagents. See [LICENSE.txt](LICENSE.txt) for the
upstream MIT notice.
