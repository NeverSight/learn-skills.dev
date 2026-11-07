---
name: fix-php-vuln
description: "Use when the user asks to fix, patch or upgrade a PHP vulnerability (e.g. 'Please fix my PHP vulnerability'), PHP2Shell, CVE-2026-109618 or CVE-2026-109619, or to find vulnerable PHP versions in Dockerfiles, distro packages, source builds, setup-php CI, Helm/IaC or Ansible/Chef/Puppet. Read-only inventory, approval gate, regression tests, focused PRs."
license: MIT
compatibility: Needs git, a shell and read access to the target repos. Build and verification steps need Docker and access to the image registry or package mirror the repos already use.
metadata:
  author: Cognition AI
  version: "1.0.0"
---

# Fix PHP vulnerability (PHP2Shell, CVE-2026-109618 / CVE-2026-109619)

## Overview
Find and fix PHP runtimes affected by PHP2Shell: two critical (CVSS v4 9.2) unauthenticated RCEs fixed on 2026-10-21 in 8.2.35, 8.3.36, 8.4.27 and 8.5.12. PHP 8.1 and older are affected too and get no releases, only source backports. PHP says every web-serving SAPI is at risk (mod_php highest, plus FPM, php-cgi, FrankenPHP and LiteSpeed). Treat the built-in `php -S` server as exposed too, and flag it as not meant for production. Inventory read-only first. Wait for approval before editing. Patch each approved repo to a fixed vendor build, verify the built artifact, and open focused PRs. Upgrading is the only complete fix.

## What's Needed From User
- Repos or org to scan. Default: the repos the user names, or every repo the agent can reach.
- Approval of which discovered repos to patch, and of any minor/major upgrade, base-OS change or likely app-code change.
- Registry, package-mirror and CI access needed to verify targets and run builds.

## Procedure
1. Search all accessible repos read-only with the git host's code search before cloning (if there is none, which is common on GitHub Enterprise Server and self-managed GitLab, shallow-clone and `rg -n --hidden --glob '!.git'`). Look for:
   - `php:` images and other PHP base images.
   - `php*` OS packages (apt/apk/dnf), `setup-php` CI steps, and PHP source downloads/`./configure` builds.
   - Helm, Kustomize, Terraform/Packer, and Ansible/Chef/Puppet code that installs PHP.
   - `composer.json`/`composer.lock` and `*.php` as usage signals.
   - The repo's test command and code the target minor is known to break (e.g. for 8.2: undeclared/dynamic properties, `${}` interpolation, `utf8_encode`), so the gate can show upgrade risk.
2. Produce one inventory table: repo, file:line, signal, current version, channel (official image, distro package, source build, managed platform), exact/floating/digest pin, SAPI, internet exposure if discernible, test coverage (none, thin, suite), and confidence. List repos you could not search separately.
3. Mark each entry fixed, vulnerable, or unknown. For distro and managed-platform builds, check the vendor's package changelog or advisory for both CVEs. Never compare `php -v` with upstream numbers to decide this.
4. Stop. Show the table and ask which repos to patch. Ask in the same message about minor/major upgrades, base-OS changes and likely app-code changes, so they can all be approved up front. Change nothing during discovery.
5. Work through the approved repos one at a time. If your agent supports subagents, run one per repo, at most five at once. Recheck the inventory for a repo before you edit it.
6. For each repo, pick the smallest fixed target per path and confirm it exists before editing. Check against the registry or package mirror the repo's CI already uses (Artifactory, Nexus, Harbor or a cloud registry) when public hosts are blocked; if neither is reachable, mark the target unverified in the PR and let the CI build prove it.
   - Exact image tag: bump to the fixed patch in the same minor, keeping the variant (`-fpm`, `-apache`, `-alpine`, `-bookworm`, etc.).
   - Digest pin: resolve and pin the new digest.
   - Floating tag: leave the tag. Require a `--pull --no-cache` rebuild and redeploy, and record the per-platform digest you verified (index digests change when tags are re-pushed). Say if the tag's base OS has moved (e.g. bookworm → trixie).
   - Placeholder or unresolvable digest: flag it, since what is actually deployed is unknown, and ask the user to confirm the running image.
   - Distro package: upgrade from the vendor security repo and record the package release and its changelog's CVE entry. In Dockerfiles, pin the fixed release or fail the build if an older one is installed. In Ansible/Chef/Puppet, `state=present` (or equivalent) never upgrades existing hosts: use `latest` or a version pin, then restart PHP.
   - CI `setup-php`: it takes `major.minor` and installs the newest patch the runner can get, so set `major.minor` and confirm the patch in the CI log.
   - Source build: move to the fixed tarball, verify the php.net SHA-256, and keep configure flags and extensions. For 7.4/8.0/8.1, use PHP's published backport commits instead (pin the commit hash; there is no tarball checksum) or, with approval, a supported branch (step 8).
   - Helm/IaC: change the input that actually selects the artifact (image tag/digest, AMI, package pin) and regenerate lock or render outputs.
7. Leave Composer `require.php` and `config.platform.php` unchanged. They don't select the deployed runtime.
8. Report PHP 8.1 and older separately, and distinguish vendor-supported builds (e.g. Ubuntu jammy's 8.1, which is fixed by a vendor package) from unsupported ones (source builds, EOL images). Give the vendor-backport or PHP-backport option, plus an upgrade path to a supported branch. Make minor/major upgrades only if the user approves.
9. Test for regressions before and after the change:
   - Baseline: before editing, build the current artifact (`--pull`, record its digest as the rollback target) and run the repo's tests (`composer test`, PHPUnit/Pest, `make test`, or the CI test command) inside it. Official `php:` images have no Composer: run the script's underlying command, or use a scratch image that only adds Composer. Record results so pre-existing failures aren't blamed on the upgrade.
   - After: rebuild and run the same tests inside the new production image, not on the host. If that image ships without tests or dev dependencies, build the test stage from the same base or mount the tests in. Treat new failures, errors and new deprecation warnings as regressions.
   - Compare runtimes: diff `php -m` and key `php -i` values (ini settings, ICU/OpenSSL/libxml versions) between old and new images, and report any extension, ini or base-OS change.
   - Smoke test: start the container as production does (FPM/Apache/CLI entrypoint), request a health or main route, and check logs for fatals and deprecations. Also check response bodies and headers: with `display_errors` on (the default when an image has no php.ini), a new deprecation is printed into the page and can break JSON responses and headers.
   - For minor/major upgrades (e.g. 8.1 → 8.2), also run `composer check-platform-reqs` in the new image (without a `composer.lock`, generate one in a scratch copy first) and a PHPCompatibility (`phpcs --runtime-set testVersion`) or Rector dry-run, and list the UPGRADING notes that apply. Prefer Rector with the target PHP set; PHPCompatibility's stable release predates 8.2. These static tools miss runtime deprecations such as dynamic properties, so they don't replace tests and the smoke test. Report extension changes made by the new image itself (e.g. 8.2+ official images dropped `ftp`).
   - Save each step's output as a log (baseline, after, runtime diff, smoke) and attach it to the PR.
   - If the repo has no tests (or only a few) or doesn't build, say so prominently, validate with a scratch copy that only adds what's missing, and offer (don't commit without approval) a minimal smoke or characterization test.
   - Confirm the artifact's version (`php -v` / `php-fpm -v`, or the image SBOM). For distro builds, also confirm the installed package release contains the fix.
   - If a regression appears, finish the read-only checks above, then stop and report it with the failing output and the smallest fix, verified in a scratch copy. Leave the version bump uncommitted until the user decides. Don't change app code without approval.
10. Open one focused PR per repo listing each path before → after, digests, floating tags needing rebuild, blocked items, EOL items, baseline vs. after test results, runtime diffs and verification evidence. Label risk: low for a patch bump on the same base, high for minor/major upgrades, base-OS changes or untested repos, and note thin coverage. Include a rollout plan: staging or canary first, then the previous image digest/package version to roll back to. That rollback target is still vulnerable, so pair it with the temporary mitigations below.
11. Roll up the per-repo results into one table: repo, PR, path, before → after, fix evidence, tests, blocked items, follow-ups. Remind the user that fixes take effect only after deploying and restarting every worker.

## Specifications
- Discovery is read-only and ends at an explicit approval gate.
- Every target is confirmed to exist and contain the fix before editing.
- Each PR includes verification against the built artifact, plus baseline vs. after test results from inside the image.
- Done means every approved deployment is either verified fixed or reported as blocked with a concrete next step.

## Advice and Pointers
- Known fixed backports (check the vendor tracker for releases not listed, e.g. Debian trixie and Ubuntu php8.5):
  - Debian bookworm `8.2.35-1~deb12u1`.
  - Ubuntu noble `8.3.6-0ubuntu0.24.04.13`.
  - Ubuntu jammy `8.1.2-1ubuntu2.28`.
- remirepo.net had no same-day update. Recommend distro packages or source builds instead.
- Temporary mitigations only reduce exposure:
  - `session.upload_progress.enabled=0`, set in php.ini or the FPM pool (not `ini_set()` or `.user.ini`), then restart every worker.
  - On 8.5, `fatal_error_backtraces=0`.
  - `post_max_size` of 8M without uploads, or 32M with uploads.
  - Proxy limits on body size, field count, multipart part count, header count and nesting depth.
  - `memory_limit=-1`, combined with a container/cgroup memory limit.
- Appliances and vendor products that embed PHP need vendor updates. Flag them; don't patch them in place.
- An unverified claim that the 8.5.12 fix is incomplete circulated on oss-security. Check the PHP advisories (GHSA-w8hw-w9fx-j79w, GHSA-6wmf-4rv5-p3rp) for updates before rollout.

## Forbidden Actions
- Do not edit before the user approves a repo.
- Do not guess image tags, digests, or package versions.
- Do not present a mitigation as a fix.
- Do not use `RLIMIT_AS` or `RLIMIT_DATA` as a mitigation. They trigger the vulnerable allocation failure.
- Do not change the SAPI, base distribution, image flavor, extensions, or build flags without saying so.
