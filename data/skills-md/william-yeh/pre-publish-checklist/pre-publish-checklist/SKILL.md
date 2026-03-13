---
name: pre-publish-checklist
description: >
  Use when about to tag, release, or push a repo for publication. Detects repo
  type(s) from filesystem signals, runs all applicable checks (skill lint, code
  review, tests, CI), classifies findings as blocking or non-blocking, then
  hands off to publishing.
metadata:
  author: William Yeh <william.pjyeh@gmail.com>
  license: Apache-2.0
  version: 0.1.0
---

# Pre-Publish Checklist

## Arguments

- `--skip <check>` — skip a specific check by name. Can be repeated.
  Valid values: `skill-lint`, `version-sync`, `code-review`, `tests`, `ci`

## Process

### Step 1 — Detect repo types

Scan the repo root for the following signals. Collect **all** matches — a repo can be multiple types simultaneously.

| Signal (file at repo root) | Repo Type |
|---|---|
| `SKILL.md` | Agent Skill |
| `pyproject.toml` / `setup.py` / `setup.cfg` | Python program |
| `package.json` | Node.js program |
| `go.mod` | Go program |
| `Cargo.toml` | Rust program |
| `pom.xml` / `build.gradle` | Java program |
| `build.gradle.kts` / `settings.gradle.kts` | Kotlin program |
| `project.clj` / `deps.edn` / `build.clj` | Clojure program |
| `*.sln` / `*.csproj` (any at root) | C# program |
| `*.fsproj` (any at root) | F# program |
| `CMakeLists.txt` / `meson.build` / `configure.ac` | C/C++ program |

If no signals match, report "unknown repo type — cannot determine which checks to run" and stop.

### Step 2 — Run checks

Run every applicable check. Skip any whose name matches a `--skip` argument.

#### Agent Skill checks (when `SKILL.md` detected)

1. **Skill lint** (`--skip skill-lint` to skip)
   - Invoke the `William-Yeh/agent-skill-linter` skill: `/skill-lint check`
   - Linter errors → BLOCKING
   - Linter warnings only → WARNING

2. **Version sync** (`--skip version-sync` to skip)
   - Run: `git tag --list` to check if the repo has any existing git tags.
   - If no tags exist, skip this check (nothing to compare against).
   - If tags exist, get the latest tag: `git describe --tags --abbrev=0`
   - Parse the `version` field from the SKILL.md frontmatter.
   - Strip any leading `v` prefix from the git tag before comparing (e.g. `v0.1.0` → `0.1.0`).
   - Compare SKILL.md version against the latest git tag:
     - If SKILL.md version == latest tag → BLOCKING: "Version not bumped — SKILL.md `<version>` matches existing tag `<tag>`. Increment the version before publishing."
     - If SKILL.md version < latest tag → BLOCKING: "SKILL.md version `<version>` is older than existing tag `<tag>`."
     - If SKILL.md version > latest tag → PASS

#### Program source code checks (when any language build manifest detected)

3. **Code review** (`--skip code-review` to skip)
   - Invoke the `William-Yeh/common-code-reviewer` skill: `/common-code-reviewer`
   - Reviewer verdict "REQUEST CHANGES" → BLOCKING
   - Reviewer verdict "APPROVE WITH COMMENTS" → WARNING
   - Reviewer verdict "APPROVE" → pass

4. **Local tests** (`--skip tests` to skip)
   - Run the test command for each detected language:

     | Repo type | Test command |
     |---|---|
     | Python | `uv run pytest` |
     | Node.js | `npm test` |
     | Go | `go test ./...` |
     | Rust | `cargo test` |
     | Java | `./mvnw test` or `./gradlew test` |
     | Kotlin | `./gradlew test` |
     | Clojure | `lein test` or `clojure -T:build test` |
     | C# / F# | `dotnet test` |
     | C/C++ | `cmake --build . --target test` or `make test` |

   - Any test failure → BLOCKING

5. **CI status** (`--skip ci` to skip)
   - Run: `gh run list --branch $(git branch --show-current) --limit 1`
   - Latest run status is not `completed` with `success` conclusion → BLOCKING

### Step 3 — Report

Output a consolidated report:

```
## Pre-Publish Checklist

Detected types: <comma-separated list>

### <Type>
- [x] <check name>: PASSED
- [WARNING] <check name>: <reason>
- [BLOCKING] <check name>: <reason>

---

Verdict: BLOCKED — N blocking issue(s) must be resolved before publishing.

Blocking issues:
1. <description>

Warnings (non-blocking):
1. <description>
```

When all checks pass or only warnings remain, the verdict is:

```
Verdict: READY TO PUBLISH
```

### Step 4 — Handoff

- **No blocking issues**: Offer to invoke `commit-commands:commit-push-pr` to complete the publish step.
- **Blocking issues remain**: Display them clearly. Do not proceed.
