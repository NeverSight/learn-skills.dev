---
name: find-peers
description: Refresh public peers, exact stack versions, and usefulness tiers every week or two and after each shared dependency update. Study source before adopting patterns.
plain: "Every week or two, refresh public repos on the same pins and adopt a pattern only after reading its code."
diagram: |-
  refresh peers
    │ exact versions
    ▼
  tier S to F, with evidence
    │
  ask one narrow question
    │ read the files
    ▼
  adopt or reject, with why
---

# Find peers

A peer is a public repo that uses our dependency families or a relevant integration. Default discovery requires two shared families. A relevant XState runtime or integration can qualify without Alchemy. Peers can reveal breaking changes and useful patterns before documentation covers them.

Effect describes work with typed failures and required dependencies. Alchemy declares and deploys cloud resources through Effect programs. Effect 4 still counts as a shared dependency family after its stable release. Record version differences between beta, release candidate, and stable releases.

## Run

```sh
pnpm find-peers
```

The script reads exact prerelease versions and the stable Effect 4 major version from workspace `package.json` files. It searches Sourcegraph once per dependency family. It ranks repos by the number of shared families. Scoped packages that move with their parent, such as `@effect/vitest` with `effect`, count once.

A repo missing from `.brain/data/peers.json` is marked `new`. The search takes about twenty seconds. Pass `--min 1` to see repos that share only one family.

## Refresh peers, versions, and tiers

Refresh the structured rows in `.brain/data/peers.json` every week or two and after every shared dependency update (Effect, Alchemy, XState, or `@xstate/effect`). The gardener pass owns this step. Run discovery, add new peers, and revisit existing peers even when discovery finds nothing new.

Rat-stack's own pins are read from its root, infra, and core manifests at content-build time, so a bump changes the comparison without a hand-edited baseline. For every peer, resolve its default branch to a commit and read its actual manifests or lockfiles at that commit. Record all four dependency families, the checked date, and source links. Preserve exact pins; label ranges, workspace/catalog references, and missing dependencies honestly. Resolve references from the workspace catalog or lockfile where possible; never turn a range into an invented pin. Show differences beside rat-stack's pins. Expect version drift. Keep tiers unchanged unless usefulness changes.

Keep every peer in `.brain/data/peers.json`, including its first-seen date, tier, one-line evidence-based reason, versions, checked date, default branch and commit, manifest/lockfile source paths, and study links. The content build reads that one dataset, sorts by tier then repository name, and renders `.brain/resources/peers.svx`: S, A, and B in the main table; C through F in a collapsed **Also seen** list. Edit structured rows, never hand-edit rendered table rows. Never delete a peer that fell behind.

## Targeted XState discovery

Run `pnpm find-peers --min 1`, then supplement Sourcegraph with GitHub code search. Search `"@xstate/effect"` across manifests and lockfiles, and `xstate alpha filename:package.json` plus `xstate "6.0.0-alpha" filename:pnpm-lock.yaml`. GitHub's token search produces false positives: an unrelated dependency may supply the alpha version. Read the actual file before counting a match.

GitHub search under an authenticated account may include private repos. Filter `repository.isPrivate` and `repository.isFork` in the results; confirm public visibility, non-fork status and no mirror via repository metadata. Exclude rat-stack itself, vendored `.repos`/`.agent_sources` trees and historical archives. A template-derived application with its own behavior is not a mirror.

Resolve the repository's default branch to a commit, read the manifests there, and resolve ranges/catalogs with that commit's lockfile. Verify candidate versions in their manifests and lockfiles. Keep relevant integrations that use one shared dependency family as B. Keep checked repos with no relevant pattern as C. Do not claim that no public pin exists from an empty, truncated or failed search. If a completed targeted pass finds no verified public consumer for a dependency family, record its query, checked date and verified result count in structured search evidence and derive the dated page statement from it; recheck that evidence on the next refresh.

## Tier rubric

Rank tiers by usefulness to rat-stack. Stars and exact version alignment do not set the tier:

- **S:** an upstream reference for our stack, or a pattern adopted here. Link the upstream source or adoption evidence; a recommendation alone is not an adoption.
- **A:** recently active, close to our stack, and studied with a relevant source-backed finding. Verify activity on the default branch (within the last 30 days); link the study.
- **B:** relevant shared dependencies or an integration worth following, without enough study or adoption evidence for A or S.
- **C:** screened with no relevant pattern for the current work. Preserve the screening evidence; revisit when our work changes.
- **D:** no longer uses our stack, with no current relevant integration identified. State which dependencies or integration disappeared.
- **E:** stale (no default-branch activity for at least 90 days) and no current relevant pattern identified. Age alone does not demote a useful upstream or adopted reference.
- **F:** inaccessible or archived with no usable source-backed reference left. Record the access/archive evidence; record a temporary fetch failure as unknown.

C means the repo was checked and has no relevant pattern for current work. B can include a relevant repo not yet studied. D, E, and F distinguish stack mismatch, inactivity, and unusable evidence rather than pretending they are quality scores. When evidence is missing, say what is unknown and do not invent a claim. Reconsider tiers on every refresh and explain changes in the report.

Put the rubric and full ranking (peer, tier, reason, and versions) at the top of the report so Joel can give feedback after shipping. No separate approval round is required.

## Learn from the new ones

Pick at most three new peers, the ones closest to what we are building next. For each:

1. Ask DeepWiki (the `deepwiki` MCP server) one narrow question tied to current work, such as "How does this repo bind a Durable Object to an Alchemy Worker?" Treat the answer as a pointer to files.
2. Read those files at the commit that uses our versions. Adopt a pattern only after reading the code, and only when it is simpler than ours or fixes something we do wrong.
3. Record adoptions and rejections, with the reason, in `.brain/resources/same-version-repos.svx`, and link that entry from the peer's Studied column.

Stars measure attention. Verify correctness before copying a popular repo's pattern.

## Report

List the new peers, what you studied, and anything adopted. Commit the roster and notes together.
