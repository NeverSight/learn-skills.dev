---
name: infrahub-auditing-repo
description: >-
  Audits an Infrahub repository against best practices and rules, producing a structured compliance report.
  TRIGGER when: reviewing repo for compliance, onboarding to existing project, pre-deployment validation, catching issues.
  DO NOT TRIGGER when: creating schemas, writing checks/generators, querying live data, populating objects, planning an Infrahub version upgrade (use infrahub-planning-upgrades).
context: fork
argument-hint: "[focus-area]"
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Repo Auditor

## Overview

Comprehensive audit of an Infrahub repository against
all rules and best practices from the infrahub-skills
plugin. Produces a structured report covering schemas,
objects, checks, generators, transforms, menus,
`.infrahub.yml` configuration, and deployment readiness.

**The audit is read-only.** The one file it writes is
its own report, `AUDIT_REPORT.md`. Nothing else in the
working tree or the index is touched, and no
destructive git command is run against them, including
to undo the audit's own side effect. An audit is most
useful on a tree that holds uncommitted work, which is
exactly the tree where a write cannot be undone.

[rules/audit-is-read-only.md](./rules/audit-is-read-only.md)
holds the canonical lists: which git commands are
forbidden and which read another revision without
touching the tree. Read it, and Phase 0 of the
procedure, before Phase 1. The `Bash` tool is granted
for read-only inspection, not for changing state;
`Write` is granted for the report file only.

## Project Context

Project structure:
!`find . -maxdepth 2 -type f \( -name "*.yml" -o -name "*.yaml" -o -name "*.py" -o -name "*.gql" -o -name "*.j2" \) 2>/dev/null | head -40`

Infrahub config:
!`cat .infrahub.yml 2>/dev/null || echo "No .infrahub.yml found"`

## When to Use

- Before deploying a repository to Infrahub
- When onboarding to an existing Infrahub project
- After significant refactoring to catch regressions
- As a periodic quality gate in development workflows
- When troubleshooting schema loading, object sync,
  or pipeline failures

## How It Works

When invoked, the auditor:

1. **Discovers** the project structure
   (`.infrahub.yml`, schemas, objects, checks,
   generators, transforms, menus)
2. **Validates** each component against the rules
   defined in the infrahub-skills plugin
3. **Cross-references** between components (e.g.,
   query names match between Python files and
   `.infrahub.yml`)
4. **Generates** a markdown report with findings organized by severity

The phased procedure that ties these steps together
lives in [audit-procedure.md](./audit-procedure.md) —
read that file when running an audit. It opens with
Phase 0, the read-only constraint every other phase
runs under, then defines the nine phases (project
structure → schema → objects → Python components →
cross-references → registration → best practices →
deployment → YAGNI / cost-to-fix) and the per-finding
severity levels used in the final report.

Before emitting the first finding, read
[rules/audit-cites-all-reference-sites.md](./rules/audit-cites-all-reference-sites.md)
and
[rules/audit-verifies-proposed-syntax.md](./rules/audit-verifies-proposed-syntax.md).
A finding states how it was verified, or says in
`verified_against` that it could not be — never by
lowering its severity, which belongs to the rule. It
enumerates every reference site it wants changed, and it
resolves any filter, field or config key it proposes
against the version under audit rather than against the
published docs. Both apply to every phase, and both add
a field to the finding shape.

When Phase 7 reaches `.infrahub.yml`, read
[rules/practices-watch-dependencies.md](./rules/practices-watch-dependencies.md)
before judging a `watch` block: a missing key, an
incomplete list, and an entry naming an untracked file
each fail silently, and the key has to be confirmed
against the version under audit before it is proposed.

## Audit Categories

| Priority | Category | What It Checks |
| -------- | -------- | -------------- |
| CRITICAL | Conduct | The audit writes nothing but its report, and every finding discloses the evidence behind it; constrains the auditor, not the repo |
| CRITICAL | Project Structure | `.infrahub.yml` exists, paths valid |
| CRITICAL | Schema Validation | Naming, relationships, deprecated fields |
| CRITICAL | Object Validation | YAML structure, value types, refs |
| CRITICAL | Python Components | Class inheritance, required methods |
| HIGH | Cross-References | Query names match, target groups |
| HIGH | Relationships | Bidirectional IDs, cardinality |
| HIGH | Registration | All files registered, no orphans |
| MEDIUM | Best Practices | human_friendly_id, display_label, `watch` deps |
| MEDIUM–LOW | YAGNI / Cost-to-Fix | Python doing what schema, GraphQL, Jinja2, or built-in IPAM/VLAN can do; denormalized data; un-extracted duplicate shapes; a whole domain hand-rolled when the marketplace ships it. Severity tracks the cost-to-fix ladder: steps 1–3 MEDIUM, steps 4–7 LOW |
| MEDIUM | Deployment | Git status, bootstrap placement |
| LOW | Patterns & Style | Code organization, naming |

## Running the Audit

Tell Claude: **"Audit this Infrahub repo"** or **"Run the Infrahub repo auditor"**

The auditor will scan the current working directory,
walk the phases defined in
[audit-procedure.md](./audit-procedure.md), and
produce the report described below.

## Report Format

The report is written to `AUDIT_REPORT.md` in the project root with this structure:

```markdown
# Infrahub Repository Audit Report

## Summary

- Total findings: N
- Critical: N | High: N | Medium: N | Low: N | Info: N
- Working tree at audit time: clean | N uncommitted files
- Tree modified by this audit: no | yes, listing paths
  (the report file itself does not count)

## Project Structure

...

## Schema Audit

...

## Object Data Audit

...

## Checks Audit

...

## Generators Audit

...

## Transforms Audit

...

## Menus Audit

...

## Cross-Reference Integrity

...

## Deployment Readiness

...

## YAGNI / Cost-to-Fix Findings

Findings sorted by `ladder_step` ascending (cheapest
fix first), then by file path. Each entry names the
rule, the ladder step, the file:line, and the
suggested replacement (schema feature, GraphQL query,
Jinja2 template, `Builtin*`/`Ipam*` inheritance, or
inverse relationship declaration).

A finding also renders the evidence it carries: a
**Sites** line listing every reference the fix must
touch, a **Verified against** line naming what the
proposed syntax was resolved against, and, on a
generic-extraction finding, a **Feasibility** verdict.

...
```

## Audit Rules Reference

The auditor checks rules from all skills:

- **[../infrahub-managing-schemas/](../infrahub-managing-schemas/)** -- Naming,
  relationships, attributes, hierarchy, display,
  extensions, uniqueness, migration
- **[../infrahub-managing-objects/](../infrahub-managing-objects/)** -- Format,
  values, children, ranges, organization
- **[../infrahub-managing-checks/](../infrahub-managing-checks/)** --
  Architecture, Python class, API, registration
- **[../infrahub-managing-generators/](../infrahub-managing-generators/)** --
  Architecture, Python class, tracking, API
- **[../infrahub-managing-transforms/](../infrahub-managing-transforms/)** --
  Types, Python/Jinja2, hybrid, artifacts, API
- **[../infrahub-managing-menus/](../infrahub-managing-menus/)** -- Format,
  item properties, hierarchy, icons
- **[../infrahub-common/](../infrahub-common/)** -- Git integration,
  caching, `.infrahub.yml` reference, GraphQL
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap (e.g. deleting nodes)

## Rules and Procedure

- [audit-procedure.md](./audit-procedure.md) — the
  Phase 0 constraint and nine-phase walkthrough
  that drive every audit run
- [rules/](./rules/) — detailed audit rule
  definitions referenced from the phases
- [examples.md](./examples.md) — sample audit
  reports and finding patterns
