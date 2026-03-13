---
name: golangci-lint-strict
description: Use this skill to install and use the upstream powerman/golangci-lint-strict config for an exact golangci-lint version by fetching the versioned config file unchanged.
metadata:
  short-description: Exact-version setup of powerman/golangci-lint-strict without local edits.
---

# golangci-lint-strict

Expert guidance for setting up `powerman/golangci-lint-strict` in Go projects with exact version pinning and no config modifications.

## Why strict mode
- It provides a strong baseline for new Go projects by enabling a broad set of linters and rules curated for practical use.
- It helps catch correctness, API, error-handling, and maintainability issues early in local development and CI.
- Using the upstream config unchanged reduces local drift and makes lint behavior easier to reproduce across developers and agents.
- Pinning the upstream version to the installed `golangci-lint` version avoids silent incompatibilities caused by config schema changes.

## When to trigger
- The user asks for a strict `golangci-lint` configuration.
- The user mentions `powerman/golangci-lint-strict`.
- The task is to install or pin a versioned `.golangci.yml` from upstream without customizing it.

## Core rules
- Use the upstream repository `powerman/golangci-lint-strict` as the source of truth.
- Fetch the exact versioned file from `VERSION/.golangci.yml` and keep it unchanged.
- Do not merge, rewrite, or "adapt" the strict config. If customization is needed, place overrides in a separate file or get explicit approval.
- Prefer an exact config version matching the installed `golangci-lint` version. If no exact upstream version exists, stop and ask which supported version to use.
- Prefer immutable upstream refs (commit SHA) for reproducible fetches. The bundled installer defaults to the snapshot commit in [references/versions-snapshot.md](references/versions-snapshot.md).
- Use the standard config filename `.golangci.yml` unless the user explicitly asks for another path.
- Always ask before overwriting any existing config file (especially `.golangci.yml`).
- Never overwrite automatically, even if the user asked for the standard filename; confirm first, then replace only after approval.
- Verify the downloaded file header includes the expected upstream version marker (the generated strict config contains an `Origin` comment).

## Workflow
1. **Determine target version**
   - Use the user-provided `golangci-lint` version if given.
   - Otherwise detect it locally (`golangci-lint version`) and extract the semantic version.
   - Cross-check against the known upstream version directories (see [references/versions-snapshot.md](references/versions-snapshot.md)).
2. **Choose destination path**
   - Default to the standard filename `.golangci.yml`.
   - If `.golangci.yml` (or the chosen destination file) already exists, stop and ask before replacing it.
3. **Fetch exact config unchanged**
   - Prefer the helper script in [assets/install-strict-config.sh](assets/install-strict-config.sh); it uses an immutable upstream snapshot commit by default and verifies the `Origin` header line.
   - If you intentionally need a newer upstream state, re-check upstream first and only then use `UPSTREAM_REF=main` explicitly.
   - Or use a direct raw URL download from an immutable commit SHA.
4. **Verify**
   - Confirm the `# Origin:` header line references the expected version.
   - Do not edit the file after download.
5. **Overwrite flow (only after explicit confirmation)**
   - Back up the existing file (for example, `mv .golangci.yml .golangci.yml.bak`).
   - Re-run the installer to write the new `.golangci.yml`.
   - State clearly that the previous config was backed up and the new file was installed unchanged.
6. **Wire usage**
   - If installed as `.golangci.yml`, `golangci-lint run` will use it automatically.
   - If the user requested a non-default path, run `golangci-lint run -c <path>`.

## Installation procedure (agent execution)
1. **Detect or confirm `golangci-lint` version**
   - Prefer the user's requested version.
   - Otherwise run `golangci-lint version` and extract the semantic version.
2. **Check existing config**
   - If destination `.golangci.yml` exists, stop and ask for overwrite approval.
3. **Install strict config**
   - Use the bundled installer from the activated skill directory:
   - `bash "<skill-dir>/assets/install-strict-config.sh" <VERSION> .golangci.yml`
4. **If overwrite was approved**
   - Back up the old config first (for example, `mv .golangci.yml .golangci.yml.bak`).
   - Re-run the installer command.
5. **Verify + run**
   - Confirm the `# Origin:` header line matches `<VERSION>`.
   - Run `golangci-lint run ./...`

## Commands (default examples)
- Install exact version using the standard config filename (agent resolves the activated skill directory path):
  - `bash "<skill-dir>/assets/install-strict-config.sh" 2.10.1 .golangci.yml`
- Run lint (auto-detects `.golangci.yml`):
  - `golangci-lint run ./...`
- After explicit overwrite approval (example backup + replace):
  - `mv .golangci.yml .golangci.yml.bak`
  - `bash "<skill-dir>/assets/install-strict-config.sh" 2.10.1 .golangci.yml`

## Output expectations
- Provide the exact fetch command/script invocation and the selected upstream version.
- Explicitly state that the config was installed as `.golangci.yml` (or note the custom path if the user requested one).
- If an existing config was detected, explicitly note that you paused for overwrite confirmation before replacing it.
- Call out when the requested version is unavailable upstream and list supported alternatives instead of improvising.

## References
- Upstream version snapshot and URL patterns: [references/versions-snapshot.md](references/versions-snapshot.md)
- Latest local reference copy (snapshot, not auto-updating): [references/latest-2.10.1.golangci.yml](references/latest-2.10.1.golangci.yml)
