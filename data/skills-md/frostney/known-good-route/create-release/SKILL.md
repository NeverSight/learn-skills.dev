---
name: create-release
description: >-
  Prepares or publishes a release using the repository's established
  versioning and publication workflow. Use when asked to cut, prepare, or
  publish a release, when the user runs /create-release, or when
  milestone-rush hands off a milestone.
license: Unlicense OR MIT
compatibility: >-
  Requires git, Python 3.11 or newer, the GitHub CLI (gh) authenticated to the
  target repository, the internal `delivery-wait` skill, and network access.
  Supports the project's changelog tooling or a hand-maintained changelog.
metadata:
  agents-role: entry-point
  agents-text: Prepare or publish a release through the repository's release workflow.
---

# Create release

Prepare a release whose tag contains its changelog, then publish through exactly
one evidence-backed path when publication is authorized.

## Authorization

- **Prepare**: determine the version, update changelog/version declarations,
  validate, and open the release PR. Requests to prepare, bump, or generate
  notes authorize only this stage.
- **Publish**: after the PR merges, create or trigger the tag/release through the
  repository's established publisher. Requests to cut, tag, publish, or run
  `/create-release` authorize this stage too.
- A `/milestone-rush` caller supplies publication authority at its verified
  milestone boundary. Reuse its settled release plan and version; no separate
  user command is required. `/deliver` integration delivery is not this trigger.
- When standalone authorization is ambiguous, perform Prepare only.

## Invariants

- The changelog and version bump land before the tag, through a squash-merged PR.
- Use the repository's configured tools and current documentation. Regenerate
  generated changelogs rather than hand-editing them.
- Run the declared release-relevant gate and report only observed results.
- Never amend, force-push, force-update a tag, skip hooks, or publish through
  more than one path.

## Prepare

1. Require a clean working tree, then resolve the authorized stage, remote
   default branch, changelog/version tooling, last release, remote tags,
   workflows, and release documentation.
2. Stop if there are no releasable commits.
3. Use a settled explicit version, or compute it under the project's
   deterministic version policy. When neither settles it, recommend a version
   from the unreleased conventional commits and ask for that choice.
4. Create a release branch from the fresh remote base.
5. Generate the changelog section and update every authoritative version
   declaration using project tooling. Do not invent a manifest bump when the
   project derives its version from tags.
6. Run the release-relevant gate, commit `chore(release): <version>`, and open a
   draft release PR through `/create-pr` with the changelog section and observed
   validation. Prepare-only requests end here.

## Publish

1. Under publication authority, converge the release PR through
   `/address-feedback automatic-merge`, then use `delivery-wait` to verify its
   squash merge and integrated revision. Reuse an already verified merge; never
   tag the open PR branch.
2. Refresh the merged base, then re-read the actual workflow YAML and release
   documentation. Identify separate owners for tag creation, GitHub release
   creation, artifact signing, and registry publishing.
3. Select exactly one route, so no tag or release is created twice:
   - workflow owns tag and release: trigger or monitor it only;
   - agent owns tag, workflow owns release: push the verified tag once, then
     monitor;
   - workflow owns tag, agent owns release: verify its tag, then create one
     GitHub release;
   - agent owns both: only when no workflow owns either action, push the verified
     tag once and create one release.
4. Stop when ownership is ambiguous or documentation and workflow disagree.
5. Execute only the selected route and verify the final tag target, release,
   workflow result, artifacts, and registry state that the route owns. Use the
   helper's `wait workflow-terminal`, `wait tag-target`, and
   `wait release-assets` operations for those GitHub transitions; do not
   monitor unchanged state through model turns.

Lead with the release outcome, PR/release URL, selected publisher, and current
evidence. Never describe an unobserved state as complete.
