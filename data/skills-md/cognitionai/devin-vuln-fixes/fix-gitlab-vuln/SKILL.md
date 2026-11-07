---
name: fix-gitlab-vuln
description: "Use when the user asks to fix, patch or upgrade a self-managed GitLab vulnerability (e.g. 'Please fix my GitLab vulnerability'), CVE-2026-110264 or the GitLab 19.5.1 critical patch release, across Omnibus, Docker, Helm chart and IaC deployments. Read-only inventory, approval gate, post-deploy checklist, focused PRs."
license: MIT
compatibility: Needs git, a shell and read access to the target repos. Build and verification steps need Docker and access to the image registry or package mirror the repos already use.
metadata:
  author: Cognition AI
  version: "1.0.0"
---

# Fix GitLab vulnerability (CVE-2026-110264, October 21, 2026 critical patch)

## Overview
Find and patch self-managed GitLab instances affected by CVE-2026-110264. It is a CVSS 10.0 unauthenticated RCE caused by an integer overflow in the Onigmo regex compiler, and it affects every CE/EE version from 7.0. Fixed releases: 19.5.1, 19.4.3, 19.3.6, 19.2.9, 19.1.9, 19.0.10 and 18.11.13. The same patch release fixes 2 High, 6 Medium and 4 Low issues, and it includes the October 8 fix for CVE-2026-97229 (CVSS 10.0, fixed in 19.4.2/19.3.5/19.2.8). GitLab.com and GitLab Dedicated are already patched, so this playbook covers self-managed installs only. Inventory read-only first. Wait for approval before editing. Patch the IaC that deploys GitLab, verify the running version, and open focused PRs.

## What's Needed From User
- Repos or org holding GitLab infrastructure code (Helm values, Terraform, Ansible, Compose, Packer). Default: the repos the user names, or every repo the agent can reach.
- Whether the user runs GitLab.com, GitLab Dedicated, or a self-managed instance, and the instance URL if self-managed.
- Approval of which deployments to patch, plus a maintenance window for single-node instances.

## Procedure
1. Search all accessible repos read-only with the git host's code search before cloning (if there is none, which is common on GitHub Enterprise Server and self-managed GitLab, shallow-clone and `rg -n --hidden --glob '!.git'`). Look for:
   - `gitlab/gitlab-ee` and `gitlab/gitlab-ce` images, and CNG images (`registry.gitlab.com/gitlab-org/build/cng/*`).
   - The `gitlab` Helm chart (`charts.gitlab.io`) and the GitLab Operator.
   - `gitlab-ee`/`gitlab-ce` Omnibus packages in Ansible/Chef/Puppet/cloud-init/Packer.
   - Terraform modules and AMIs that deploy GitLab.
   - Source installs (`gitlab-foss`/`gitlab` checkouts).
2. Produce one inventory table: repo, file:line, deployment type (Omnibus, Docker, Helm, Operator, source), edition, current version or chart version, exact/floating pin, node topology (single vs multi-node), and confidence. List repos you could not search separately. If the user is on GitLab.com or Dedicated, say no action is needed and stop.
3. Mark each entry fixed, vulnerable, or unknown. If the instance URL is reachable, compare with `/help` or the `/api/v4/version` result (token required). Otherwise rely on the pinned version.
4. Stop. Show the table, flag single-node instances that will have downtime, and ask which deployments to patch. Change nothing during discovery.
5. Work through the approved deployments one at a time. If your agent supports subagents, run one per repo, at most five at once. Repeat the inventory for a repo before you edit it.
6. For each repo, pick the fixed patch in the same minor and confirm it exists before editing. Check against the registry or package mirror the repo's CI already uses (Artifactory, Nexus, Harbor or a cloud registry) when public hosts are blocked; if neither is reachable, mark the target unverified in the PR and let the CI build prove it.
   - Docker: `gitlab/gitlab-ee:<ver>-ee.0` or `gitlab/gitlab-ce:<ver>-ce.0`. Resolve and pin the new digest if digest-pinned.
   - Helm/Operator: look up the chart version on https://docs.gitlab.com/charts/installation/version_mappings/ (for example, GitLab 19.5.1 is chart 10.5.1 and GitLab 18.11.13 is chart 9.11.14). If that page is unreachable, run `helm search repo gitlab/gitlab -l` against the chart repo or mirror the cluster uses. Bump the chart version, not just `global.gitlabVersion`.
   - Omnibus: pin `gitlab-ee=<ver>-ee.0` (or the CE equivalent) in the config-management code.
   - Source: check out the fixed tag and follow the source upgrade guide for the target version.
7. If the current version is more than one minor behind or on an unsupported branch, report the required upgrade-path stops (https://gitlab-com.gitlab.io/support/toolbox/upgrade-path/) instead of jumping. Do multi-stop upgrades only with user approval.
8. Add rollout notes to each PR:
   - A backup before upgrading.
   - Downtime for single-node instances, since migrations must finish before GitLab starts.
   - Zero-downtime procedure for multi-node instances.
   - Post-deploy migrations.
9. Validate what you can without production access: `helm template`/`helm lint`, `terraform validate`/`plan`, `ansible-lint`, and Compose config checks. List the post-deploy checks for the user to run:
   - `gitlab-rake gitlab:env:info` showing the fixed version.
   - `gitlab-rake gitlab:check`.
   - `gitlab-ctl status`, or pod readiness on Helm.
   - Background migrations completed.
   - Web, Git over SSH and HTTPS, and CI runners working.
10. Open one focused PR per repo listing each deployment before → after, chart/image/package versions, digests, upgrade-path notes, downtime expectations, validation results, and the post-deploy checklist.
11. Roll up the per-repo results into one table: repo, PR, deployment type, before → after, downtime, validation, blocked items, follow-ups. Remind the user that the instance stays vulnerable until the change is deployed.

## Specifications
- Discovery is read-only and ends at an explicit approval gate.
- Every target image, chart or package is confirmed to exist before editing.
- Each PR states the downtime impact and includes the post-deploy validation checklist.
- Done means every approved deployment has a PR, or has been reported as blocked with a concrete next step.

## Advice and Pointers
- Internet-reachable instances are the top priority, because the bug is exploitable without authentication.
- GitLab published two threat detections for self-managed instances: "Onigmo native worker crash" and "Org mode render error burst". Point security teams to them so they can hunt for prior exploitation.
- GitLab Runner and the GitLab Agent are versioned separately and are not listed in this advisory. Do not upgrade them as part of this fix.
- Geo secondaries and every node of a multi-node install must run the same version.

## Forbidden Actions
- Do not edit before the user approves a deployment.
- Do not guess image tags, chart versions, or package versions.
- Do not skip required upgrade-path stops or tell the user to skip migrations.
- Do not change the edition (CE↔EE) or deployment type.
- Do not run commands against a production GitLab instance.
