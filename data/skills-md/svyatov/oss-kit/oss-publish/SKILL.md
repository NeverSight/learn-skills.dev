---
name: oss-publish
description: "Set up a secure release process for an open source package so no long-lived publishing token exists to steal. Covers trusted publishing with OIDC, build provenance, and approval-gated release workflows for npm, PyPI, RubyGems, crates.io, NuGet, Maven Central, Hex, pub.dev, and container images, plus the tag-published flow for Go modules and Packagist, on both GitHub Actions and GitLab CI/CD. Use for any request to publish a package or a container image, secure or harden a release process, set up trusted publishing or provenance, generate an SBOM, sign release binaries, publish checksums for release assets, or create a release workflow."
license: MIT
---

# Secure package publishing

Set up a release process where no registry token exists to steal, releases can come only from one CI workflow triggered by a tag, and a human still approves each one before it reaches the public registry. The decisions below are the same regardless of ecosystem: gather the facts, configure trusted publishing, write a hardened workflow, gate it on approval, verify provenance. The exact fields a registry's trusted publisher form asks for, and the exact YAML a workflow needs, differ by ecosystem and by forge, so that detail lives in one reference file per ecosystem, under `references/ecosystems/`: [npm](references/ecosystems/npm.md), [pypi](references/ecosystems/pypi.md), [rubygems](references/ecosystems/rubygems.md), [crates](references/ecosystems/crates.md), [go-modules](references/ecosystems/go-modules.md), [packagist](references/ecosystems/packagist.md), [nuget](references/ecosystems/nuget.md), [maven-central](references/ecosystems/maven-central.md), [hex](references/ecosystems/hex.md), [pubdev](references/ecosystems/pubdev.md), and [containers](references/ecosystems/containers.md). Each file covers both GitHub Actions and GitLab CI/CD, and each carries the same six steps, with a gap section wherever a step has no answer in that ecosystem. Read the matching file before writing any configuration or giving any settings instruction; do not carry a flow, a field name, or a workflow snippet from one ecosystem or forge to another by analogy.

Two of the eleven run on the tag-published track, where the registry reads the forge instead of taking an upload: Go modules and Packagist. There is no publish credential on that track at all, so R-PUB-01 through R-PUB-04 do not reach it and R-PUB-07 does. `STANDARD.md`'s release preamble is what assigns the track, and each of those two files states it at the top.

## How to run this skill

Half of this setup is repository files, which this skill writes directly. The other half is settings on the registry's website and on the forge that only the user can change: the trusted publisher entry, the approval environment, account-level two-factor authentication, tag protection. For that half, give click-by-click instructions with direct links resolved from the repository's own data: the package, gem, or crate name from its manifest, the owner and repository from the forge remote or the manifest's repository field, never a placeholder like "go to your package settings". Present each settings block, wait for the user to confirm it is done, then verify what can be verified from the command line before moving to the next block.

## Principles

Verify every registry and forge claim against the current documentation before writing it into a repository. A wrong trusted publishing flow is worse than a missing one: it either fails at publish time or, if papered over with a long-lived token, defeats the entire point of this skill. Where a registry and forge combination has no supported trusted publishing flow, say so plainly and give the documented fallback; do not invent a flow to fill the gap.

A registry's documentation is not proof that a command still exists. Before handing a maintainer a command to run, confirm its flags parse against the client that will run it: `<tool> help <subcommand>` where the toolchain is installed, or that subcommand's source in the client's own repository where it is not. Where neither is available, say the command is unverified rather than presenting it as checked, and do not install a language toolchain to settle it unless the maintainer agrees. This is not hypothetical. This skill shipped a hex.pm key-generation command that the Hex client had removed a release earlier, and every re-verification passed, because hex.pm's own guide still documented it: reading the vendor's documentation confirmed the vendor's error. `references/ecosystems/hex.md` carries the case.

When a registry's documentation and its client disagree, that is a defect in the registry, not a puzzle to work around. Name which two sources disagree and what you ran to establish it. Do not improvise a substitute credential path, do not extract an undocumented on-disk token, and do not pin around the version where it last worked. Offer to report it upstream, and write the issue with `oss-writing`.

Configure one publication gate by default. Additional gates remain valid, but they add another human action to every release. In an established release flow, preserve every configured gate, report the human actions it requires, and recommend the default path. Change those gates only after the maintainer accepts the migration.

Present other policy choices instead of guessing at them, even when the repository already contains a release workflow or a stored token. Which cooldown to use, whether to keep an existing publish step, and how much of an existing workflow to carry over are decisions the user makes.

## The shape of a release workflow

One vocabulary, across all eleven ecosystems and both forges. A maintainer who reads two of these repositories should not have to work out that `pack` and `build` are the same job, and a form field that is always the same string is one nobody has to discover. This is a convention, not a rule: no `STANDARD.md` rule scores a job name, and none should, because failing a repository over a word is a cost with no security or correctness argument behind it. Follow it in what you write; do not rename a working job in a repository that already has one unless the user asks.

| | value |
| --- | --- |
| File | `.github/workflows/release.yml`, or the release section of `.gitlab-ci.yml` |
| Workflow name | `Release` |
| Trigger | push of tags matching `v*` |
| Environment | `release` |

Job names come from a fixed set, and a job appears only where the ecosystem needs one:

| Job | When it appears |
| --- | --- |
| `test` | always |
| `build` | where the artifact can be built separately from the push |
| `publish` | always |
| `github-release` | where the release attaches assets to a forge release |

`release` names the file, the trigger, and the environment, so it does not also name a job. Where an ecosystem departs from any of this, its reference file says so in one line and gives the reason, so a difference reads as a decision rather than as drift. Two departures are structural and both are recorded where they apply: the tag-published track keeps its release job inside the `CI` workflow, because pushing the tag is the publish; and Hex has no `build` job, because `mix hex.publish` builds the tarball it uploads and accepts no prebuilt path.

## Process

### Step 1: Gather repo facts

Detect the ecosystem from what the repository ships, using the signals in the routing table at the end of this file. A repository can ship more than one publishable thing; enumerate every one, since trusted publisher entries and approval environments are configured per package, not per repository. Container images stack rather than replace: a Go module or an npm package can also ship an image, so `containers` runs alongside the manifest-detected ecosystem rather than instead of it.

Detect what the repository ships, not what it merely contains. A manifest present only for a documentation site or a development dependency is not a published package, and a Dockerfile that builds a test harness is not a published image, so neither pulls this skill in. The signal for a container image is a workflow step pushing to a registry, or an image that already exists on the forge's registry.

Collect, from the manifest and the repository, before changing anything: the package, gem, or crate name and version; the owner and repository, from the manifest's own repository or source metadata first, falling back to the git remote; repository visibility and forge plan, since approval protection is not available on every plan; whether the owner is an organization or a personal account; whether the package is already published, since an unpublished package may need a different first-release path; the existing tag format from `git tag --sort=-creatordate | head`, keeping whatever format is already in use; and any existing release workflow or pipeline, especially one referencing a stored registry token, which this skill's changes should remove.

Identify each release flow. One tag or release event can publish several packages when they version and ship together. Independently tagged packages are separate flows. Inventory every forge and registry approval each flow already requires before proposing a change.

Detect the forge the same way `oss-ci` does: look for `.github/workflows/` or `.gitlab-ci.yml`, check the git remote host, or ask directly if neither signal is present. If the user states the forge explicitly, trust that over any signal found in the repository.

Route to the matching reference file now, using the table at the end of this file. If what the repository ships matches none of the eleven rows there, say so plainly: name the ecosystem found and state that this skill has no reference file for it, rather than improvising a publishing flow for a registry nobody has read the documentation of.

### Step 2: Configure trusted publishing

Open the matched reference file and read the section for the detected forge. Every reference file states, for each forge it covers, either the exact fields the registry's trusted publisher form asks for and the exact permission or `id_tokens` block the workflow needs, or, where the combination has no supported flow, a gap section naming that plainly and giving the strongest documented fallback.

Most of those forms ask for a workflow filename and an environment name, which are what Steps 3 and 4 produce. Do not wait for them and do not go looking for them: the reference file states both, so every field is resolvable now. Give the user the settings URL with all of them filled in, as this step's own message rather than as an item in a later summary, and carry on to Step 3 without waiting.

What blocks is the tag, not the workflow. Nothing this skill writes can publish until a version tag is pushed, so that is where the confirmation belongs: do not push the first tag, and do not report the setup done, until the user confirms the trusted publisher, or the fallback credential, is in place. Say so in the same message as the form, so the user knows what is being waited on and when. A "done" answered to a three-item wrap-up is not that confirmation.

### Step 3: Write a hardened release workflow

Trigger the workflow on a version tag, matching the format found in Step 1. Before building, compare the tag's version with the manifest version and fail on any mismatch. Isolate the publish job: it installs no dependencies beyond a publishing client that the project has already provenance-checked and version-locked, uses no dependency cache, and calls no third-party action beyond what the reference file names, because anything running in a job that can authenticate to the registry can publish the package. Build and verify the exact publishable artifact in a separate job, then hand it to the publish job as a workflow artifact when the registry client accepts a prebuilt artifact. Three ecosystems cannot be split that way and each reference says why: `cargo publish` accepts a manifest rather than a `.crate` path, `mix hex.publish` builds the tarball it uploads, and a container image has no digest to attest until the push completes. Where the split is impossible, the reference names what bounds the collapse instead of pretending it away. Ask before overwriting an existing release workflow, and carry over any extras the project relies on, such as changelog generation or forge release notes, into a job that has neither the publish credential nor `id-token: write`.

### Step 4: Gate on manual approval with two-factor authentication

Choose the last enforced publication gate that covers the complete release flow. A registry gate qualifies only when the CI identity cannot approve its own staged artifact. It must also approve every package in the flow with one human action. npm staged publishing meets both conditions for a flow containing one package.

Where a registry gate qualifies, use it as the default. Keep any forge environment binding that forms part of the publisher identity, but configure no required reviewer there. Where no registry gate qualifies, pin the publish job to a GitHub environment with required reviewers. On GitLab, use a protected environment with one blocking manual job. Set `when: manual` and `allow_failure: false`, and restrict deployment permission to at least one person who is not an automation account.

Check feature availability before writing the workflow. The ecosystem reference names the plan each gate needs. Do not simulate a missing native gate with an unverified third-party approval action. If the forge plan provides no native gate and the registry has no qualifying gate, report R-PUB-04 as unmet.

Additional gates still satisfy R-PUB-04. If a release flow already has more than one, report each human action and suggest the one-gate default. Do not remove or weaken an established gate until the maintainer accepts that change.

### Step 5: Verify provenance after the first release

Once the first tag-triggered release runs, verify the exact published artifact against the repository and workflow identity using the registry record or forge attestation named by the reference file. Record a registry limitation as a gap when it cannot serve verifiable provenance. Do not claim that OIDC authentication alone proves which artifact was built, and do not claim provenance exists from a successful publish alone.

### Step 6: Describe and sign what the release ships (R-PUB-05, R-PUB-06)

Only for a release that attaches a built asset. A source archive the forge generates is not one, and a project that publishes to a registry and attaches nothing else goes straight to Step 7. Where there is a built asset, add two steps to the build job, before the artifact is handed on: generate a software bill of materials in SPDX or CycloneDX, whichever the ecosystem's tooling already produces, and attach it to the release beside the asset it describes; then either sign each asset or write a manifest of their hashes and sign that. Prefer the forge's own attestation where it covers the exact asset, since it needs no key for the maintainer to hold, publish, or lose. On GitHub that action is `actions/attest`; `actions/attest-build-provenance` is a wrapper over it that upstream keeps for workflows already using it, and its own README sends a new workflow to `actions/attest`, so do not write the wrapper into one. If it does not, say which key verifies the signature and where a downloader finds it, because a signature nobody can trace to a published key verifies nothing. Do not generate an SBOM for the repository's source tree and attach it to a binary release; it describes a different thing and reads as though the rule were met.

### Step 7: Verify before reporting done

Read each R-PUB rule's `Check:` line in `STANDARD.md` against the workflow, the registry configuration, and the released artifact as they now stand, and fix what fails. Start the list again after each fix, because moving a step between jobs changes which rule the credential split satisfies. Report done only when every cited rule passes, and report a rule the platform makes unreachable as unmet with the reason rather than as passed.

## Scope

The PUB rules belong here: R-PUB-01 publishing in CI tied to a release tag, R-PUB-02 trusted publishing, R-PUB-03 build provenance, R-PUB-04 human approval, R-PUB-05 artifact inventory, R-PUB-06 signed assets, and R-PUB-07 tag-published registry updates.

When `oss-audit-report.md` exists at the repository root, read the group addressed to this skill and work from that. Each failing rule there carries the audit's evidence and that rule's `Check:` text verbatim, so reading `STANDARD.md` as well adds nothing. Where the file is absent, work from the request as usual.

This skill owns publishing: trusted publishing, build provenance, the human approval gate on the release workflow, and what a release attaches alongside a built asset. It writes into the same workflow and pipeline files as two other skills, and the boundary between them is the rule area, not a description of files. `oss-ci` decides what runs on push and on every change request, including the test job this skill's publish job depends on; it does not decide how the publish job authenticates or who approves it. `oss-harden` owns the security posture of the same files: pinning third-party actions to a commit SHA, minimal workflow permissions, dependency updates, branch protection, and signed tags; it does not decide when a job runs or how a package is published. Do not pin an action to a SHA, add an unrelated `permissions:` scope, or configure branch protection from this skill; note that the project needs it and hand the work to `oss-harden`.

That hand-off assumes `oss-harden` still has a turn coming. Check whether it does. Where it has already run on this repository, handing off means the pins never happen, and this skill has just added unpinned `uses:` lines to the one workflow that authenticates to a registry. In that case pin what this skill added, to the same standard `oss-harden` uses, and say in the report that you did and why. The boundary exists so two skills do not fight over one line, not so a line ends up unpinned.

`oss-writing` is not one of those hand-offs. It owns no rule area and takes no work over, so nothing here is handed to it. Read it before writing a branch name, a commit message, a change request title or description, or an issue, which is all of what this skill leaves behind on the forge.

## Routing table

The signals below come from `skills/oss-audit/ecosystems.json`, which is the canonical copy. Where this table and that file disagree, the roster wins.

| Ecosystem | Signal | Track | Reference file |
| --- | --- | --- | --- |
| npm | `package.json` | registry push | [references/ecosystems/npm.md](references/ecosystems/npm.md) |
| PyPI | `pyproject.toml`, `setup.py`, or `setup.cfg` | registry push | [references/ecosystems/pypi.md](references/ecosystems/pypi.md) |
| RubyGems | `*.gemspec` or `Gemfile` | registry push | [references/ecosystems/rubygems.md](references/ecosystems/rubygems.md) |
| crates.io | `Cargo.toml` | registry push | [references/ecosystems/crates.md](references/ecosystems/crates.md) |
| Go modules | `go.mod` | tag published | [references/ecosystems/go-modules.md](references/ecosystems/go-modules.md) |
| Packagist | `composer.json` | tag published | [references/ecosystems/packagist.md](references/ecosystems/packagist.md) |
| NuGet | `*.csproj`, `*.fsproj`, or `*.vbproj` | registry push | [references/ecosystems/nuget.md](references/ecosystems/nuget.md) |
| Maven Central | `pom.xml`, `build.gradle`, or `build.gradle.kts` | registry push | [references/ecosystems/maven-central.md](references/ecosystems/maven-central.md) |
| Hex | `mix.exs` | registry push | [references/ecosystems/hex.md](references/ecosystems/hex.md) |
| pub.dev | `pubspec.yaml` | registry push | [references/ecosystems/pubdev.md](references/ecosystems/pubdev.md) |
| Container images | a workflow pushing to a registry, or an existing image on the forge's registry | registry push | [references/ecosystems/containers.md](references/ecosystems/containers.md) |
