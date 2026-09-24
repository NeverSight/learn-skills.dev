---
name: j-prepare-release-deployment
description: Prepare release and deployment work after validated implementation, using a discovery-first workflow for versioning, lockfiles, packaging, Docker or Podman containers, CI workflows, and deployment documentation. Use when Codex must inspect release readiness, propose or apply approved release-preparation changes, update sdlc_docs/trace_workflow.md release status, or route unresolved hosting, security, runtime, or operations decisions back to requirements or architecture. Do not use to implement product stories, validate BDD scenarios, create pull requests, publish artifacts, push tags, or deploy without separate approval.
---

# Release And Deployment Preparation

## Purpose

Prepare a repository for release or deployment without pretending the target model is known. Inspect the approved product and architecture evidence, produce a visible proposal, apply only approved local preparation changes, and keep publishing or deployment actions separately approved.

## Governing Rules

- Work in English.
- Use the exact skill identifier `j-prepare-release-deployment`.
- Treat `sdlc_docs/trace_workflow.md` as the canonical workflow status file when present.
- Start after implementation validation is complete, or when the user explicitly requests release/deployment preparation.
- Inspect approved architecture, ADRs, requirements, local implementation evidence, manifests, lockfiles, CI, container files, and deployment docs before proposing changes.
- Keep release/deployment preparation discovery-first until the artifact, runtime, target environment, ownership, and safety constraints are approved.
- Use repository-approved semantic version tooling for version changes. Prefer `bump-my-version` when configured.
- Require explicit approval of the visible proposal before local writes.
- Re-read affected files and traceability immediately before writing.
- Do not introduce public hosting, authentication, secrets, environment ownership, operational monitoring, release cadence, or rollback policy that is not approved upstream.
- Do not tag, push, publish, deploy, create releases, create pull requests, modify issues, or move project items without separate explicit approval.
- Never claim a build, container check, workflow, or deployment command passed unless it was executed successfully.

## Canonical Inputs

Read the applicable project-owned artifacts when present:

```text
sdlc_docs/00_inception/project_context.md
sdlc_docs/01_requirements/product_requirements.md
sdlc_docs/02_architecture/architecture.md
sdlc_docs/02_architecture/adr/
sdlc_docs/03_implementation/
sdlc_docs/trace_workflow.md
README.md
docs/
pyproject.toml, package manifests, or equivalent
lockfiles
Dockerfile, Containerfile, docker-compose.yml, compose.yaml, or equivalent
.github/workflows/
```

Do not hardcode repository-specific release policy. Extract constraints from approved project documents and existing repository conventions.

## Traceability Ownership

The skill owns the `Release deployment` row in `sdlc_docs/trace_workflow.md`.

Allowed fields on the owned row:

```text
Status
Current activity
Evidence
Missing or blocked
Next action
```

The skill may update prior handoff fields only when the workflow explicitly defines a release handoff row. It must not modify product requirements, architecture approval, implementation status, validation status, pull request state, or unrelated increment rows.

Use these row patterns when a project template has no stronger local convention:

```markdown
| Release deployment | Initial Release | Not Started | Release and Deployment Preparation | validated implementation available | Release/deployment proposal not prepared | Run j-prepare-release-deployment |
| Release deployment | Initial Release | In Progress | Release and Deployment Preparation | release readiness inspection started | Release/deployment proposal pending | Continue j-prepare-release-deployment |
| Release deployment | Initial Release | Under Clarification | Release and Deployment Preparation | release readiness inspection | Deployment target, artifact, security, or operations decision missing | Resolve release/deployment decision |
| Release deployment | Initial Release | Pending Approval | Release and Deployment Preparation | release/deployment proposal prepared | Human approval pending | Review release/deployment proposal |
| Release deployment | Initial Release | Complete | Release and Deployment Preparation | approved release preparation and successful validation commands | None | Release/deployment preparation complete |
```

Before every traceability write:

1. copy the current trace file to a temporary location outside the repository;
2. prepare the proposed after-file;
3. validate only authorized row and field changes;
4. reject unauthorized changes and preserve the original file;
5. report changed fields and unauthorized-change count.

Use `scripts/validate_release_preparation.py` for objective checks. Do not replace a missing validator with manual confidence.

## Workflow

1. Locate the repository root.
2. Read workflow traceability and determine whether release/deployment preparation is allowed or explicitly requested.
3. Read approved requirements, architecture, ADRs, implementation validation evidence, and pull request/review evidence when present.
4. Inspect manifests, lockfiles, build commands, package metadata, container files, CI workflows, deployment docs, and release notes conventions.
5. Read `references/release-deployment-policy.md`.
6. Identify the current release model: package-only, local executable, local container, internal deployment, hosted deployment, or unknown.
7. Identify unresolved decisions that must be routed to `c-manage-product-requirements` or `d-design-product-architecture`.
8. If material decisions are missing, set `Release deployment` to `Under Clarification`, report the blockers, and stop.
9. Draft the release/deployment proposal: versioning (including semantic bump level and tooling command), lockfile policy, build checks, container work, CI workflow changes, docs, commands, trace updates, and out-of-scope remote actions.
10. Stop for explicit approval before local writes.
11. Re-read affected files and traceability after approval.
12. Apply only approved local preparation changes.
13. Run package, lockfile, container, CI-equivalent, and documentation checks that the proposal named.
14. Run `scripts/validate_release_preparation.py`.
15. Fix preparation defects that stay inside the approved proposal.
16. Set `Release deployment` to `Pending Approval` when a release plan is prepared but human acceptance remains.
17. Set `Release deployment` to `Complete` only after approved preparation and successful validation.
18. Report files changed, command results, trace fields changed, unresolved release/deployment decisions, and remote actions not performed.

## Routing Rules

- New or changed product behavior -> `c-manage-product-requirements`.
- Public hosting, authentication, data isolation, external runtime, secrets, monitoring, or operational ownership decisions -> `d-design-product-architecture` after product scope is approved.
- Missing implementation evidence -> `g-implement-repository-work`.
- Missing BDD completion evidence -> `i-validate-user-story-completion`.
- Pull request creation or review handoff -> `h-create-implementation-pull-request`.

## Completion Gates

Release/deployment preparation is complete only when:

- the release model is approved or explicitly limited to local preparation;
- version and lockfile changes are deliberate, validated, and performed through approved semantic version tooling;
- package/build commands pass or limitations are reported;
- container files and CI workflows match approved architecture constraints when present;
- deployment documentation records how to run the approved artifact safely;
- traceability is updated only through authorized fields;
- no public publishing, tag, push, release, or deployment action occurred without separate approval.

## Resources

- Read `references/release-deployment-policy.md` before proposing release work.
- Read `references/golden-example/browser-task-board/README.md` when a concrete progressive example is useful.
- Run `scripts/validate_release_preparation.py` after approved release/deployment preparation changes.


## Progressive Audit Resources

- Read `references/golden-example/README.md` only when a progressive concrete example is useful.
- Read `references/process_flowchart.md` only for human explanation or audit.
