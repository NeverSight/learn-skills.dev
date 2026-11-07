---
name: skill-publisher
description: Validate, version, package, and safely publish owned Codex skills from a skill monorepo to their configured GitHub repositories. Use when preparing or releasing a skill; do not use to discover or install unrelated third-party skills.
metadata:
  version: 0.5.0
  license: MIT
  topics: [codex, skills, publishing, github-cli, release, release-safety]
---
# Skill Publisher

Prepare, package, and publish a skill from a skill-manager repository to its configured GitHub repository. Supported layouts:

- **Standalone:** `skills/<skill-id>/` → `<github.owner>/<skill-id>`.
- **Series:** `skills/<series>/<skill-id>/` → the repository and target path configured for that series.

This skill publishes skills the user owns or is authorized to maintain. It does not search for, install, or republish unrelated third-party skills.

## Operating modes

Infer the requested mode from the user's request and state it briefly:

- **Audit / check:** inspect metadata and completeness; do not change files or remote state.
- **Prepare / package:** validate and build a local artifact; do not mutate a remote repository.
- **Publish / release:** prepare the artifact, present a concrete release plan, obtain explicit confirmation for remote mutations, publish, and verify the result.

Do not turn a check or package request into a publish request.

## Non-negotiable safety rules

1. **No unconfirmed remote mutation.** Before creating a repository, pushing commits, changing visibility, opening or merging a PR, creating a tag/release, or modifying release metadata, state the exact target, visibility, branch, version, files, and operations. Obtain explicit confirmation. Treat each materially different operation as requiring fresh confirmation.
2. **No destructive Git shortcuts.** Never force-push, force-update a tag, delete/recreate a release, run `git reset --hard`, or use `git clean -fdx` to make publishing easier. Do not overwrite unrelated target-repository files.
3. **Protect local work.** Check `git status` before editing or committing. Preserve user changes. Never include unrelated staged or untracked files in a release commit. If the worktree state makes safe isolation unclear, stop and explain the blocker.
4. **Do not guess configuration.** Read `series.json` and the target skill's `SKILL.md`; resolve the target from actual configuration. If a series target is missing or the skill reference is ambiguous, report what is ready and what configuration is missing instead of inventing a repository.
5. **Never expose credentials.** Use `gh auth status` to check authentication. Do not print tokens, copy credential files, embed secrets in URLs, or ask the user to paste credentials into chat.
6. **Version immutability.** Never silently overwrite an existing version tag or GitHub Release. If the version already exists, compare the published state; report “already published” only when equivalence can be established. Otherwise stop and recommend a new version.
7. **Separate preflight from postflight.** A matching GitHub Release cannot be a prerequisite for creating that same first release. Check for collisions before publishing; verify that the release exists only after publication.
8. **Be honest about verification.** Distinguish checks actually run from checks merely recommended. Never claim a package, push, or release succeeded without inspecting the command result and verifying the remote state.

## Workflow

### 1. Resolve the skill and target

1. Find the skill-manager repository root and the requested skill folder.
2. Normalize the skill reference. Use `<skill-id>` for a standalone skill and `<series>/<skill-id>` for a series skill. If the same ID appears in multiple series, require an explicit series-qualified reference.
3. Read the skill's `SKILL.md`, `README.md`, `LICENSE`, any `agents/` metadata, and `series.json` where relevant.
4. Resolve the destination repository and in-repository path from configuration. A standalone target may be derived from `github.owner` and the skill ID only when that owner is explicitly configured. Do not assume the target repository's default branch is named `main`.

### 2. Establish intent and release version

1. Determine whether the user asked to audit, package, or publish. Do not infer permission for a remote mutation merely from a request to inspect or prepare.
2. Read `metadata.version` from the skill front matter and inspect the relevant Git tags / GitHub Releases when accessible.
3. Use Semantic Versioning:
   - **PATCH:** backward-compatible fixes, wording corrections, and internal clarifications that do not add a meaningful capability.
   - **MINOR:** additive workflow, capability, or guidance that remains compatible with the existing purpose and interface.
   - **MAJOR:** breaking changes to the skill's expected workflow, interface, metadata contract, or supported layout.
4. Do not bump a version just because a package is being rebuilt. If a bump is required but the intended release scope is ambiguous, recommend a version and ask for confirmation before changing it. Never invent a version based on assumptions about unavailable tags.
5. Keep the `SKILL.md` version as the source version of truth. Ensure the package manifest, target repository content, Git tag, and Release name all match it.

### 3. Validate the skill

Run the repository's actual validation command and treat every reported error as a blocker:

```bash
skillctl check --skill <skill-ref>
```

If the entry point is unavailable and the manager repository supports the documented fallback, use:

```bash
PYTHONPATH=src python -m skill_manager check --skill <skill-ref>
```

Do not invent substitute commands if neither is available. Report the blocker and continue only with non-destructive review that does not depend on the missing validator.

At minimum, confirm that:

- front matter is parseable YAML and includes a valid skill `name`, useful `description`, semantic `metadata.version`, `metadata.license`, and non-empty `metadata.topics`;
- the skill directory name and front-matter name agree where required by the manager;
- `README.md` explains purpose, requirements, usage, limits, and release process;
- the license file exists and matches the intended reuse terms;
- linked files and paths referenced by the skill exist;
- examples and commands match the actual manager and repository layout.

Do not “fix” a validation failure by weakening or deleting the completeness gate.

### 4. Package and inspect the artifact

Run the package command only after validation passes:

```bash
skillctl package --skill <skill-ref>
```

Packaging must run its validation gate again. Inspect the resulting archive rather than trusting the exit code alone:

- verify the artifact exists, can be opened, and contains the expected skill files;
- inspect `MANIFEST.json` and verify the skill ID, version, license, topics, and entrypoint;
- check that no unrelated project files, `.git/`, virtual environments, caches, credentials, `.env` files, private keys, or accidental local artifacts were included;
- verify referenced supporting files are included and paths are portable;
- preserve deterministic packaging; do not modify archive contents after validation without rebuilding and rechecking it.

If the command does not reveal the output path clearly, inspect its help or output. Do not guess an artifact filename.

### 5. Preflight the GitHub target

For a publish request:

1. Check authentication with `gh auth status`; do not disclose authentication details.
2. Inspect the target repository, if it exists, using GitHub CLI or another available read-only mechanism. Record its canonical owner/name, visibility, URL, default branch, description, topics, README, license, and branch-protection constraints when available.
3. Query the actual default branch; never hard-code `main`.
4. Check whether `v<version>` (or the repository's documented tag convention) already exists as a Git tag or Release. Resolve collisions before preparing a push.
5. Distinguish metadata that must exist **before** a release (repository description, topics, README, license, correct skill files) from metadata that is verified **after** the release (tag, Release page, notes, and attached package asset).
6. If the target repository does not exist, propose the repository name, description, topics, target path, and visibility. Use private visibility by default unless the user explicitly requests public visibility; obtain explicit confirmation before creating it.
7. If the series target is not configured, stop remote publishing. The package may still be reported as ready.

### 6. Present the release plan and obtain confirmation

Before the first remote mutation, summarize:

- source skill and current / proposed version;
- validation and package results;
- exact target repository URL and visibility;
- target path and actual default branch;
- files that will be added, updated, or removed (normally no removals unless explicitly listed);
- planned commit / branch / PR strategy;
- tag and Release name, notes source, and package asset to attach;
- any repository metadata changes.

Ask the user to confirm this concrete plan. Do not rely on a vague earlier instruction if the destination, visibility, version, or affected files have since changed.

### 7. Stage changes safely

1. Re-check the target's latest remote state after confirmation and before writing.
2. Prefer an isolated clone, worktree, or dedicated publish checkout. Confirm its origin and current branch before use.
3. Fetch the target's actual default branch. Preserve existing files and repository-specific workflows. Copy only the validated skill files into the configured target path; never copy the manager repository wholesale.
4. Inspect the diff and status. Confirm that unrelated changes are absent from the proposed commit. Do not delete repository files simply because they are absent from the source skill folder.
5. Commit only the exact intended skill files. If the repository requires a branch or pull request, follow that policy and do not bypass protection. Direct push to the default branch is permitted only when the user explicitly approved that method and repository policy allows it.
6. Never force-push or discard concurrent target changes. If the remote has advanced, fetch and reconcile safely; stop if a conflict cannot be resolved without guessing.

### 8. Create the GitHub Release

Only after the target content has been pushed or the required PR has been merged:

1. Confirm the intended target commit contains the validated skill files.
2. Ensure the target version tag and Release do not already point to different content.
3. Generate concise, factual release notes from the actual diff or supplied changelog. Do not claim tests or features that were not verified.
4. Create the Release using `v<version>` unless the target repository documents another convention.
5. Attach the validated deterministic ZIP produced by the package step when the artifact is available and the release plan includes it. Do not rename an unrelated file and pass it as the package.
6. Do not overwrite an existing Release or tag. If a conflict appears between preflight and creation, stop and report it.

### 9. Verify and report

After publishing, independently verify the remote result where tools permit:

- the target repository and published path are correct;
- the intended commit is present on the expected branch;
- the tag and Release name match the skill version;
- the Release URL and release notes are available;
- the expected package asset is attached and downloadable, if one was planned;
- repository description, topics, README, and license are accurate;
- no unrelated files or secrets were published.

Return a concise report listing the source skill, version, target URL, commit/branch, Release URL, artifact path, checks passed, checks not run, and any residual issues. For package-only mode, provide the local artifact path and explicitly state that nothing was published.

## Failure handling and recovery

- **Validation failure:** stop packaging and publishing; list the failing checks and the smallest safe fixes.
- **Package failure:** retain source files, inspect the error, and rebuild only after fixing the cause.
- **Authentication or permission failure:** stop; report the missing permission category without exposing secrets.
- **Missing series destination:** report that local validation/package may be complete but publishing is blocked by configuration.
- **Dirty worktree or unrelated staged files:** preserve the state; isolate the release in a separate worktree or ask the user to resolve it.
- **Remote changed during release:** fetch again, inspect differences, and do not overwrite concurrent work.
- **Version already released:** compare tag, commit, source version, and assets. If equivalence is proven, report the existing release; otherwise require a new version rather than rewriting history.
- **Partial publication:** report exactly which steps succeeded. Resume from the first incomplete step after rechecking remote state; do not blindly repeat repository creation, push, tag, or Release creation.

## Final constraints

- Never claim an operation succeeded without evidence from its result and, for remote publication, a read-back check.
- Never turn inferred recommendations into facts. Label unavailable checks as **not verified**.
- Keep user-facing output focused on decision points, actual changes, verification, and blockers; do not dump credentials, excessive command logs, or irrelevant repository contents.
