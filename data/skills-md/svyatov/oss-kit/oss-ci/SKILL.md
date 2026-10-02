---
name: oss-ci
description: "Set up continuous integration for an open source project on GitHub Actions or GitLab CI/CD. Use when the user asks to set up CI, create workflows or pipelines, add automated testing, building, or linting on push and pull requests, deploy a docs or other static site to GitHub Pages or GitLab Pages, or review existing CI configuration. Also use when the user mentions automating tests, running checks on PRs, or a build matrix, even without saying CI. Covers what runs. Security posture of those workflows belongs to oss-harden, and publishing belongs to oss-publish."
license: MIT
---

# Continuous integration setup

Decide what runs on push and on every change request, then write it in the syntax the project's forge understands. The decisions in this file are forge-independent: detect the ecosystem, decide what needs to run, choose a matrix, decide caching. The syntax that expresses those decisions is not, so it lives in [references/github-actions.md](references/github-actions.md) for GitHub Actions and [references/gitlab.md](references/gitlab.md) for GitLab CI/CD. Read the matching reference file before writing any configuration; do not write one forge's syntax by translating the other's keywords, because the two have different shapes for triggers, matrices, and caching. What differs by ecosystem rather than by forge, the setup action or image, the cache directory and its key, and the test command, lives in `references/ecosystems/`, one file per ecosystem, routed from Step 2.

## Scope

The CI rules belong here: R-CI-01 triggers, R-CI-02 project commands, R-CI-03 version matrix, R-CI-04 cache keying, R-CI-05 timeouts and cancellation, and R-CI-06 test suite.

When `oss-audit-report.md` exists at the repository root, read the group addressed to this skill and work from that. Each failing rule there carries the audit's evidence and that rule's `Check:` text verbatim, so reading `STANDARD.md` as well adds nothing. Where the file is absent, work from the request as usual.

This skill owns what runs: which checks execute, on which triggers, across which versions, with what caching. It shares the workflow and pipeline files it writes with two other skills, and the boundary between them is the rule area, not a description of files.

The SEC rules, security posture of the same files such as pinned action SHAs, minimal permissions, dependency updaters, branch protection, and pinned images, belong to oss-harden. The REL rules, publishing a built artifact to a registry with trusted publishing, provenance, and an approval gate, belong to oss-publish. Do not add a `permissions:` block, pin a SHA, configure branch protection, or write a publish job while working from this skill; note that the project needs it and hand the work to the owning skill. A GitHub Pages deploy is the single exception, and it covers only the two blocks [references/github-actions.md](references/github-actions.md) already emits: top-level `contents: read`, and `pages: write` plus `id-token: write` on the deploying job. Those grants are how the deployment authenticates, so a workflow written without them cannot run at all, and stripping them to honour the ban ships a green pipeline that deploys nothing. Every other permissions question still goes to `oss-harden`.

`oss-writing` is not one of those hand-offs. It owns no rule area and takes no work over, so nothing here is handed to it. Read it before writing a branch name, a commit message, a change request title or description, or an issue, which is all of what this skill leaves behind on the forge.

Deploying a built static site to the forge's own Pages hosting is also something that runs on a push, so it stays here rather than with oss-publish, which owns registry releases. No rule requires it: a project publishes a site because it has one, so it is written only where the repository builds a site and the user asks for the deployment.

## Principles

Verify everything before adding a step, a secret, or a config value: read the actual repository rather than guessing at its shape. Ask when something is uncertain instead of inventing a plausible answer.

Call the project's own automation instead of writing shell logic inside the pipeline. A step that runs `npm test` instead of `jest --coverage --ci` keeps the pipeline and a contributor's laptop running the same command, which is what R-CI-02 checks for. When no such automation exists, ask whether to add it to the project or fall back to inline commands.

Present policy choices instead of guessing at them, even when the repository already contains tests, a Dockerfile, or a pipeline. What runs on a change request, what triggers a release build, and how deployment happens are decisions the user makes; code only tells you what is possible, not what is wanted.

## Two ways in

The request decides which one runs. Read it before starting the process below.

To set up CI, or to extend what a project already has, run Steps 1 to 8 in order.

To review CI without changing it, run Steps 1 and 2, then stop and report. Read the existing workflow or pipeline against each R-CI rule's `Check:` line and against the reference file for its forge. Report every check that fails, anchored at the file and line it fails at, and name what would fix it. Change no file unless the user asks for the fix after reading the report.

## Process

### Step 1: Detect the forge

Look for an existing `.github/workflows/` directory or `.gitlab-ci.yml` file, check the git remote for a github.com or gitlab host, or ask directly if neither signal is present. This decides which reference file governs Steps 6 and 7. If the user states the forge explicitly, trust that over any signal found in the repository.

### Step 2: Analyze the repository

Identify the language and runtime from source files and the package manifest, and note the version range the project claims to support; the matrix in Step 4 has to cover all of it, including the oldest and newest supported version, per R-CI-03.

Detect every ecosystem the repository has a signal for, not only the one it ships. A manifest that exists only for development still gets installed in CI, so a Go tool with a documentation `package.json` needs a Node toolchain, cache, and test command as much as it needs the Go ones. Read the file below for each ecosystem found, and read no others.

| Signal in the repository | Read |
|---|---|
| `package.json` | [references/ecosystems/npm.md](references/ecosystems/npm.md) |
| `pyproject.toml`, `setup.py`, `setup.cfg` | [references/ecosystems/pypi.md](references/ecosystems/pypi.md) |
| a `.gemspec`, `Gemfile` | [references/ecosystems/rubygems.md](references/ecosystems/rubygems.md) |
| `Cargo.toml` | [references/ecosystems/crates.md](references/ecosystems/crates.md) |
| `go.mod` | [references/ecosystems/go-modules.md](references/ecosystems/go-modules.md) |
| `composer.json` | [references/ecosystems/packagist.md](references/ecosystems/packagist.md) |
| a `.csproj`, `.fsproj`, or `.vbproj` | [references/ecosystems/nuget.md](references/ecosystems/nuget.md) |
| `pom.xml`, `build.gradle`, `build.gradle.kts` | [references/ecosystems/maven-central.md](references/ecosystems/maven-central.md) |
| `mix.exs` | [references/ecosystems/hex.md](references/ecosystems/hex.md) |
| `pubspec.yaml` | [references/ecosystems/pubdev.md](references/ecosystems/pubdev.md) |
| a workflow or pipeline pushing an image to a registry, or an existing image on the forge's registry | [references/ecosystems/containers.md](references/ecosystems/containers.md) |

A lockfile with no manifest beside it is the same signal, and the roster names those too. `skills/oss-audit/ecosystems.json` is the canonical list; where this table and that file disagree, the file wins.

Find every applicable lint, test, typecheck, and build command the project already defines, whether that is package manager scripts, a Makefile, a Rakefile, or a tool like tox or just, and read them closely enough to know their arguments and side effects. Do not invent a missing class of check: a documentation repository may have no build, and a small script may have no linter. Where the repository ships executable code and defines no test suite at all, that is an R-CI-06 gap rather than a class of check this project does without, so raise it and ask whether to add a suite instead of writing CI that runs nothing. If the repository has a CONTRIBUTING guide, its commands and the project automation must agree; resolve any conflict before copying either into CI.

Read any existing CI configuration before changing it, so you know whether to extend it or replace it.

Identify every lockfile the project commits. The roster records which lockfiles each ecosystem's tooling produces, and whether it produces one at all; the ecosystem file names the download directory an install command can safely reuse and the file that keys it. Do not assume an installed dependency directory is a cache.

Find `.env.example` and search the source for required environment variables, so a step needing a secret is identified before generation rather than after a failed run.

### Step 3: Present findings and ask

Summarize what Step 2 found, then ask about the choices code alone cannot answer: what should run on a pull or merge request, what should trigger a release build, and whether existing CI should be extended or replaced. Ask only what applies to this project; a project with no Dockerfile gets no question about a registry.

Where Step 2 found a build that produces a static site, ask whether it should also deploy, and to where. A site can be built as a check and never published, so treat a static build as a question rather than as consent to deploy one.

### Step 4: Choose the matrix

Build the version matrix from the supported release lines identified in Step 2, not from a single pinned version. The ecosystem file read there says where the support claim lives in that ecosystem's manifest and which setup action or image installs the version. Include every maintained major or minor release line the project claims to support. A project with no stated support range gets a single-version pipeline instead of an invented matrix; do not manufacture support claims the manifest does not make. If a range is continuous and includes release lines the project does not intend to support, fix the declared range rather than silently testing a subset.

### Step 5: Decide caching

Cache only package-manager download data or another directory the tool's official documentation says is safe to reuse. Where the forge ships a first-party mechanism that caches the detected package manager's data and keys on the lockfile, prefer it; the ecosystem file names it, what it actually caches, and what it keys on by default, which is not always the lockfile. Otherwise key an explicit cache on the lockfile plus every compatibility boundary that changes its contents, such as the operating system, architecture, runtime, and package manager. A fallback key is optional and must not cross one of those boundaries. A project with no lockfile or no reusable download cache gets no cache step.

### Step 6: Write the configuration

Open the reference file for the forge chosen in Step 1 and follow its syntax exactly. Open only that one. The other forge's file has no syntax this run can use, and reading it costs the run its context for nothing.

Each reference file covers triggering on push to the default branch and on every change request (R-CI-01), a timeout on every job with cancellation of superseded runs on the same branch (R-CI-05), and the cache decisions from Step 5 (R-CI-04). Each also carries a Pages deployment section, used only when Step 3 established that the project wants one. Neither file covers permissions, SHA pinning, or publishing; those stay out of the file you write here.

Order jobs and steps so a fast check fails before a slow one starts: lint before test, test before build. This holds on either forge.

### Step 7: Validate before presenting

Confirm the configuration is syntactically valid with the forge's own validator where one is available, and confirm that every command it calls exists and succeeds locally in the same order. For GitLab, use CI Lint with included configuration expanded. For GitHub, inspect the workflow in the Actions editor or push it on a branch when the user has authorized that external change; a generic YAML parser cannot validate GitHub expressions or workflow semantics. List any secrets the pipeline needs, with the command to add each one, without running that command. The forge's CLI need not be installed here, because the command is printed for the repository owner to run on their own machine. Confirm the matrix matches every supported release line and that every job carries a timeout and participates in cancellation of superseded runs when safe.

### Step 8: Present the result

Before presenting, read each R-CI rule's `Check:` line in `skills/oss-audit/STANDARD.md` (from the plugin root, like the roster in Step 2) against the configuration as it now stands, and fix what fails. The file is long: read only its R-CI section. Start the list again after each fix, and do not report done while any cited rule still fails. On GitHub there is no local validator, so this reference-plus-checklist pass is the validator, and the loop terminates when every cited rule passes rather than when the file looks finished.

Then show the generated file, a short summary of what was detected and decided, the list of secrets to configure, and anything left for the user to set at the repository or project level, such as branch protection or environment approvers, naming the skill that owns it rather than attempting it here.
