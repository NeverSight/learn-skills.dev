---
name: code-review-infra
description: "Reviews infrastructure changes: GitHub Actions workflows, Terraform, Dockerfiles, docker-compose, IaC. Focuses on supply-chain pinning, secret handling, least-privilege permissions, action versions, and CI failure modes. Always verifies action hash pins when present."
when_to_use: "Use for reviews of infrastructure files (`.github/`, `*.tf`, `Dockerfile`, `docker-compose*`). Invoked directly with a PR URL or diff file path, or dispatched by `/code-review`. Follow all steps in order; do not shortcut based on this description."
argument-hint: "[PR URL | path to diff file] [--source=...] [--pr=<URL>] [--file=<path>]"
effort: xhigh
allowed-tools: Bash(git *) Bash(gh *) Read Grep
---

## Steps

### 1. Source and diff

Read `~/.claude/skills/code-review/references/review-shared.md` and follow its source detection and diff fetching sections. If `--source` and the corresponding identifier args were passed, use those and skip any prompting.

### 2. GitHub Actions hash verification

If the diff contains any line matching `^\+\s*uses:\s+\S+@[0-9a-f]{40}`, run the verification per the shared doc for every pinned action. Infra reviews always run this step when pins are present.

### 3. Review

Read `~/.claude/skills/code-review/references/review-checklist.md` first.

Focus on:

- **Supply-chain pinning**: third-party actions pinned to a 40-char hash, comments accurately name the corresponding tag, dependabot configured if appropriate.
- **Secret handling**: no secrets in plain text, no secrets echoed or set-output, scoped via repository secrets or OIDC, redacted in logs.
- **Least-privilege permissions**: explicit `permissions:` blocks at the job or workflow level, `GITHUB_TOKEN` scope minimised, no blanket `write-all`.
- **Action version recency**: pin against a current major; flag deprecated actions (e.g. set-output, save-state).
- **Dockerfile hygiene**: non-root user, image pinning (digest or specific tag, not `latest`), layer-cache friendliness, no secrets baked into image, multi-stage builds where appropriate.
- **IaC drift risk**: missing state backend lock, destructive operations (forced replacements, deletions), unbounded blast radius.
- **CI failure modes that block deploys**: missing fallbacks, single points of failure, flaky external dependencies, missing timeouts.

Apply the common review rules from the shared doc.

### 4. Output

Format per the output section of `~/.claude/skills/code-review/references/review-shared.md`. The linter section does not apply; do not run a linter.
