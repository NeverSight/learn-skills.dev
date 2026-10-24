---
name: fix-node-vuln
description: "Use when the user asks to fix, patch or upgrade a Node.js vulnerability (e.g. 'Please fix my Node vulnerability'), the October 21, 2026 Node.js security release, CVE-2026-111497 (Brotli RCE), or end-of-life Node 20, across Docker images, .nvmrc/.tool-versions, setup-node CI, Lambda and IaC. Read-only inventory, approval gate, regression tests, focused PRs."
license: MIT
compatibility: Needs git, a shell and read access to the target repos. Build and verification steps need Docker and access to the image registry or package mirror the repos already use.
metadata:
  author: Cognition AI
  version: "1.0.0"
---

# Fix Node.js vulnerability (October 21, 2026 security release, incl. CVE-2026-111497)

## Overview
Find and fix Node.js runtimes affected by the October 21, 2026 security release, which fixed 10 CVEs. Four are High, including the Brotli decoder out-of-bounds write RCE (CVE-2026-111497) and three TLS/DNS hostname issues (CVE-2026-105482, -105483, -106069). Fixed releases are 22.23.4, 24.22.1 and 26.12.1. Node 20 and older are end-of-life, get no fixes, and need a major upgrade. Inventory read-only first. Wait for approval before editing. Patch each approved repo, verify the built artifact, and open focused PRs.

## What's Needed From User
- Repos or org to scan. Default: the repos the user names, or every repo the agent can reach.
- Approval of which discovered repos to patch, and whether EOL major upgrades are in scope.
- Registry and CI access needed to verify targets and run builds.

## Procedure
1. Search all accessible repos read-only with the git host's code search before cloning (if there is none, which is common on GitHub Enterprise Server and self-managed GitLab, shallow-clone and `rg -n --hidden --glob '!.git'`, since version files are dotfiles). Look for:
   - `node:` and other Node base images, including multi-stage builds.
   - `.nvmrc`, `.node-version`, `.tool-versions`, Volta config, and `actions/setup-node`/CI images.
   - NodeSource or OS `nodejs` packages.
   - Serverless runtime settings (Lambda `nodejs22.x`, Cloud Functions, Azure Functions).
   - Helm/Terraform/Ansible code that installs Node.
   - `engines.node` as a signal.
   - Code that the target major is known to break (e.g. import assertions `assert {`, native addons in `binding.gyp`/`node-gyp`, removed APIs), and the repo's test command, so the gate can show upgrade risk.
2. Produce one inventory table: repo, file:line, signal, current version, channel, exact/floating/digest pin, production vs build/CI-only, internet exposure if discernible, test coverage (none, thin, suite), and confidence. List repos you could not search separately.
3. Mark each entry fixed, vulnerable, EOL, or unknown. For distro packages and managed runtimes, check the vendor's package changelog or advisory instead of comparing upstream version strings.
4. Stop. Show the table and ask which repos to patch. List likely app-code changes for major upgrades so the user can approve them up front. Change nothing during discovery.
5. Work through the approved repos one at a time. If your agent supports subagents, run one per repo, at most five at once. Recheck the inventory for a repo before you edit it.
6. For each repo, pick the smallest fixed target per path and confirm it exists before editing. Check against the registry or package mirror the repo's CI already uses (Artifactory, Nexus, Harbor or a cloud registry) when public hosts are blocked; if neither is reachable, mark the target unverified in the PR and let the CI build prove it.
   - Exact image tag: bump to the fixed patch in the same major, keeping the variant (`-alpine`, `-slim`, `-bookworm`, etc.).
   - Digest pin: resolve and pin the new digest.
   - Floating tag within a supported major: leave the tag. Require a `--pull --no-cache` rebuild and redeploy, and record the new digest. For an approved major upgrade, keep the repo's pinning style (floating stays floating, exact stays exact).
   - Record the multi-arch index digest for every new image, including exact tags, since the OS layer still moves.
   - Version files: set the fixed patch, and keep every file that names the version consistent.
   - CI `setup-node` with a floating version (`22`, `lts/*`): add `check-latest: true`, or pin the fixed patch. Otherwise the runner's cached, older Node is used.
   - Managed serverless runtimes (e.g. Lambda `nodejs22.x`): providers don't publish the exact patch, so check the provider's public base image (e.g. `public.ecr.aws/lambda/nodejs:22`) or log `process.version` from the function. With Lambda's Auto runtime-update mode, AWS updates in place and a redeploy only speeds it up; with Function update or Manual mode, a redeploy or runtime-version change is required.
7. Leave `engines.node` unchanged unless it would exclude the new version (e.g. `20.x` on a 20 → 22 upgrade, which makes `npm ci` warn `EBADENGINE`). It doesn't install anything.
8. Report Node 20 and older separately with an upgrade path to 22 or 24 LTS. Make a major upgrade only with user approval, then apply the major-upgrade checks in step 9.
9. Test for regressions before and after the change:
   - Baseline: before editing, build the current image with `--pull` and record its digest (this is the rollback target). Inside it, run `npm ci`/`pnpm install --frozen-lockfile`/`yarn install --immutable`, the build script if any, and the tests. Record results so pre-existing failures aren't blamed on the upgrade.
   - After: repeat install, build and test inside the new production image, not on the host. If that image ships without tests or dev dependencies (multi-stage, `--omit=dev`), build the test/builder stage from the same base, or mount the tests into the production image. Treat new failures and new deprecation warnings as regressions.
   - Compare runtimes: diff `node -p process.versions` (V8, OpenSSL, ICU, etc.) and the base OS between old and new images. For services that make outbound TLS calls (`https`, `fetch`, `tls.connect`), note the eMudhra CA removal and the stricter OpenSSL defaults.
   - Smoke test: start the container with the production command, request a health or main route, and check logs for crashes and warnings.
   - For major upgrades (e.g. 20 → 22), also run tests with `NODE_OPTIONS=--pending-deprecation`, rebuild native addons from source (`npm rebuild`), and list the release notes' breaking changes that apply (e.g. Node 22 removed import assertions `assert { type: 'json' }` in favor of `with`).
   - Save each step's output as a log (baseline, after, runtime diff, smoke) and attach it to the PR.
   - If the repo has no tests or only a few, say so prominently and offer (don't commit without approval) a minimal smoke or characterization test.
   - Confirm `node -v` in the built production image or runtime.
   - If a regression appears, finish the read-only checks above, then stop and report it with the failing output and the smallest fix, verified in a scratch copy. Leave the version bump uncommitted until the user decides. Don't change app code without approval.
10. Open one focused PR per repo listing each path before → after, digests, floating tags needing rebuild, blocked items, EOL items, baseline vs. after test results, runtime diffs and verification evidence. Label risk: low for a patch bump on the same base, high for major upgrades, base-OS changes or untested repos, and note thin coverage. For floating tags, give the digest as of today's date. Include a rollout plan: staging or canary first, then the previous image digest/version to roll back to. That rollback target is still vulnerable, so roll back only briefly.
11. Roll up the per-repo results into one table: repo, PR, path, before → after, production or CI-only, tests, blocked items, follow-ups. Remind the user that fixes take effect only after deploying.

## Specifications
- Discovery is read-only and ends at an explicit approval gate.
- Every target is confirmed to exist before editing.
- Each PR includes `node -v` evidence from the built production artifact. For CI-only paths, version files and managed runtimes, give the best available evidence (the resolved version from the installer or base image) and name the check the user must run after merge.
- Done means every approved deployment is either verified fixed or reported as blocked with a concrete next step.

## Advice and Pointers
- Prioritize internet-facing services that decompress Brotli (HTTP clients/servers, proxies, `zlib.createBrotliDecompress`). Also prioritize TLS clients that connect to user-supplied hosts.
- The release also updates the bundled c-ares, OpenSSL (22/24), SQLite (22), Undici, and CA certs (eMudhra removal).
- Electron apps, vendor images and appliances bundle their own Node. Flag them for vendor updates.
- CI-only Node is lower priority than production runtimes, but patch it in the same PR when it's cheap.

## Forbidden Actions
- Do not edit before the user approves a repo.
- Do not guess image tags, digests, or package versions.
- Do not do a major Node upgrade without explicit approval.
- Do not change base distribution or image flavor without saying so.
