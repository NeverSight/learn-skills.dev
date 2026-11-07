---
name: sota-docs-workflow
description: >-
  State-of-the-art documentation and engineering-collaboration guidance (2026)
  covering documentation architecture (Diátaxis, docs-as-code, READMEs,
  runbooks, onboarding, AI-readable docs), API/reference docs and changelogs,
  and the team workflow around code: pull requests, code review conduct,
  commit discipline, branching, and releases. Use when writing or structuring
  any documentation AND when auditing docs quality, and when designing or
  auditing collaboration workflow. Not for in-product UI microcopy (use
  sota-ux-writing) or marketing/landing-page copy (use sota-copywriting).
  Trigger keywords: documentation, docs,
  README, API docs, docstring, changelog, release notes, migration guide,
  code review, pull request, PR description, commit messages, conventional
  commits, branching, semver, onboarding, runbook, AGENTS.md, llms.txt,
  spec-driven development, SDD, Spec Kit, Kiro, specification, acceptance
  criteria, steering files.
---

# SOTA Docs & Engineering Workflow

## Purpose

Expert-level rules for the artifacts around the code: documentation (structure,
reference, freshness, runbooks) and the collaboration workflow (PRs, review,
commits, releases). These are the highest-leverage, lowest-glamour practices —
review latency and doc decay quietly dominate team throughput. Rules are
imperative with rationale and good/bad examples; every rules file ends with an
audit checklist. Load only the files relevant to the task via the index below.

Boundaries: ADR practice lives in [`sota-architecture`](../sota-architecture/SKILL.md); API contract design in
[`sota-api-design`](../sota-api-design/SKILL.md); tag signing/provenance and CI supply chain in
[`sota-devsecops`](../sota-devsecops/SKILL.md). This skill references them rather than repeating them.

## BUILD mode

When creating docs or setting up workflow:

1. **Classify before writing.** Every doc is exactly one Diátaxis mode
   (tutorial / how-to / reference / explanation) and is titled accordingly;
   mixed-mode pages are the defect to design out ([`rules/01`](rules/01-documentation-architecture.md) §1).
2. **Docs live with the code**: in-repo, PR-reviewed, CI link-checked, examples
   executed. If a doc can't change in the same PR as the code, it will decay
   ([`rules/01`](rules/01-documentation-architecture.md) §2, §4).
3. **README = what / why / 5-minute quickstart / honest status**, then links
   out ([`rules/01`](rules/01-documentation-architecture.md) §3). Runbooks are alert-linked and command-exact
   ([`rules/01`](rules/01-documentation-architecture.md) §5). Ship the **documentation baseline** — README + LICENSE +
   CHANGELOG always; SECURITY/CONTRIBUTING/CODE_OF_CONDUCT once public — each with
   one canonical home, not scattered copies ([`rules/01`](rules/01-documentation-architecture.md) §8).
4. **Reference is generated** from OpenAPI/docstrings/rustdoc/godoc with
   warnings-as-errors; doc comments carry the why, contract, and failure
   modes; examples run in CI ([`rules/02`](rules/02-api-reference-changelogs.md) §1–4).
5. **Changelog from day one**: Keep a Changelog format, `Unreleased` section
   updated in the PR that makes the change, user-impact language
   ([`rules/02`](rules/02-api-reference-changelogs.md) §6).
6. **Workflow defaults**: small single-purpose PRs with what/why/how-tested
   descriptions ([`rules/03`](rules/03-code-review-pr-workflow.md) §1–2); trunk-based short-lived branches; atomic
   commits with imperative ≤72-char subjects; conventional commits only if
   automation consumes them ([`rules/04`](rules/04-commits-branches-releases.md) §1–3).
7. **Agent docs**: one short, human-curated AGENTS.md/CLAUDE.md with exact
   commands and repo-specific traps — never auto-generated bloat, never a
   restatement of ambient/global rules ([`rules/01`](rules/01-documentation-architecture.md) §7, §10). On a **new repo**,
   `.gitignore` + secret scanning and LICENSE land before the first commit
   ([`rules/01`](rules/01-documentation-architecture.md) §10).
8. **Solved failures accrue** in a symptom-keyed troubleshooting playbook,
   written in the PR that fixed them ([`rules/01`](rules/01-documentation-architecture.md) §9).
9. Before declaring done, self-review against the relevant files' **Audit
   checklists**.

## AUDIT mode

**Coverage:** every `rules/` file's Audit checklist applies in AUDIT mode. Mark one *not applicable* only with its reason in the report — never skip a file because the thing it checks for is absent, since that absence may be the finding.

When auditing docs or workflow:

1. Scope the surfaces: docs tree + README + runbooks ([`rules/01`](rules/01-documentation-architecture.md)), generated
   reference + changelog + migration guides ([`rules/02`](rules/02-api-reference-changelogs.md)), recent PRs and review
   threads ([`rules/03`](rules/03-code-review-pr-workflow.md)), git history, branches, and tags ([`rules/04`](rules/04-commits-branches-releases.md)).
2. **Audit reality, not policy.** Sample artifacts: run the quickstart on a
   clean environment, follow a runbook's commands, read 10 docstrings, read the
   last 20 merged PRs and 50 commits, diff a recent minor release for breaking
   changes. A CONTRIBUTING.md full of rules nobody follows is itself a finding.
3. Work through each loaded file's **Audit checklist**; probe the classic gaps:
   tutorial that fails partway, stale docs contradicting code, README
   quickstart requiring tribal knowledge, alert with no runbook, `default:
   Error` as the only documented failure, changelog that's a commit dump,
   2,000-line rubber-stamped PRs, force-push during review, broken commits on
   main, moved release tags, gitflow on a continuous-deploy service.

### Severity conventions

- **Critical** — actively dangerous artifacts: runbook whose commands are wrong
  or destructive without warning; docs instructing insecure practice (secrets
  in config examples, auth bypass); moved/deleted published release tag;
  breaking change shipped in a minor/patch with no notice; merge to default
  branch with no review or required checks at all.
- **High** — reliably costs incidents or releases: page-able alerts without
  runbooks; quickstart/tutorial that fails; published docs contradicting
  current released behavior; no changelog or migration guide across breaking
  releases; review rubber-stamping (large PRs, instant LGTMs, AI volume merged
  unread); non-bisectable main (broken commits); releases built outside CI.
- **Medium** — erodes trust and throughput: mixed Diátaxis modes; undocumented
  public symbols or name-restating docstrings; unexecuted doc examples; no
  link-checking; PR descriptions missing why/how-tested; review SLA routinely
  blown; long-lived feature branches; commit-dump changelog; conventional
  commits adopted without enforcement or automation.
- **Low** — polish: missing freshness dates; vanity/stale badges; unlabeled
  nit comments; subject lines over 72 chars; missing `.git-blame-ignore-revs`
  for reformat commits; docs index drift.

### Finding format

```
[SEVERITY] <one-line title>
Where: <file:line | doc URL | PR/commit ref | branch/tag>
Rule: <rules-file §section>
Issue: <what is wrong, with observed evidence (quote the doc/PR/commit)>
Impact: <concrete consequence — who is misled, what breaks, what it costs>
Fix: <specific change; corrected text/command/process where load-bearing>
```

Order by severity; one finding per root cause; every finding cites sampled
evidence (a doc you executed, a PR you read) — no findings from vibes.

## Rules index

| File | Read this when... |
|---|---|
| [`rules/01-documentation-architecture.md`](rules/01-documentation-architecture.md) | Writing/structuring/auditing any docs: Diátaxis modes, docs-as-code CI (link checks, doc tests), README front-door, decay control (ownership, freshness, aggressive deletion), runbooks, onboarding docs, discoverability, AGENTS.md/CLAUDE.md and llms.txt, and the repo **documentation baseline** (must-have docs + community-health files: LICENSE/SECURITY/CONTRIBUTING/CODE_OF_CONDUCT, and where GitHub looks for them). |
| [`rules/02-api-reference-changelogs.md`](rules/02-api-reference-changelogs.md) | API/library reference docs: generation from source (OpenAPI/docstrings/rustdoc/godoc), docstring content (why/contract/failures), runnable examples and doctests, error documentation, versioned docs, Keep a Changelog discipline, migration guides. |
| [`rules/03-code-review-pr-workflow.md`](rules/03-code-review-pr-workflow.md) | PR and review process: PR sizing and slicing, description discipline (what/why/how-tested), review SLAs and WIP limits, reviewer/author conduct, blocking vs non-blocking comments, draft and stacked PRs, automation boundaries, reviewing AI-generated code. |
| [`rules/04-commits-branches-releases.md`](rules/04-commits-branches-releases.md) | Git history and shipping: atomic/bisectable commits, message discipline, Conventional Commits and when they pay, trunk-based vs gitflow honesty, SemVer semantics, breaking-change pipeline, tag immutability, release notes vs changelog, release automation. |
| [`rules/05-spec-driven-development.md`](rules/05-spec-driven-development.md) | Driving non-trivial/agent-built work from a living spec: the intent→plan→tasks→implement→verify loop, separating what from how, testable acceptance criteria, `[NEEDS CLARIFICATION]` markers, specs-in-repo and spec-drift control, steering/constitution vs per-feature specs, linking ADRs/OpenAPI instead of copying, and when SDD is overhead. Pairs with [`sota-testing` rules/08](../sota-testing/rules/08-bdd-spec-by-example.md) (executable acceptance). |

## Top-10 non-negotiables

1. **One Diátaxis mode per document** — tutorials teach, how-tos accomplish,
   reference informs, explanation contextualizes; titles declare which.
   ([rules/01](rules/01-documentation-architecture.md) §1)
2. **Docs are code**: in-repo, PR-reviewed, link-checked in CI; behavior
   changes update docs in the same PR. ([rules/01](rules/01-documentation-architecture.md) §2)
3. **Wrong docs are worse than none** — own every doc, date-review the
   operational ones, delete stale pages instead of archiving them. ([rules/01](rules/01-documentation-architecture.md) §4)
4. **Every page-able alert links to a command-exact, incident-tested runbook.**
   ([rules/01](rules/01-documentation-architecture.md) §5)
5. **Reference generated from source with undocumented-public-symbol as a build
   failure; doc examples compile and run in CI.** ([rules/02](rules/02-api-reference-changelogs.md) §1–3)
6. **Document failure modes**: every operation states what can fail and what
   the caller should do; error messages point toward the fix. ([rules/02](rules/02-api-reference-changelogs.md) §4)
7. **Changelog in Keep a Changelog form, written in user-impact language,
   updated in the PR — and breaking changes ship with a migration guide after a
   deprecation period.** ([rules/02](rules/02-api-reference-changelogs.md) §6–7)
8. **Small, single-purpose PRs with what/why/how-tested descriptions; first
   review response within one business day.** ([rules/03](rules/03-code-review-pr-workflow.md) §1–3)
9. **The review bar is provenance-blind**: AI-generated code gets the same
   scrutiny, and style/lint/type findings are CI's job, never a human's.
   ([rules/03](rules/03-code-review-pr-workflow.md) §6–7)
10. **Main is always green and bisectable; published tags are immutable;
    version numbers keep SemVer's promises with breaking changes announced
    before they're shipped.** ([rules/04](rules/04-commits-branches-releases.md) §1, §4–5)
