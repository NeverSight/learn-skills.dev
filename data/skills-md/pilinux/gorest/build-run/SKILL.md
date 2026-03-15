---
name: build-run
description: Build and run the project locally to reproduce compile/runtime issues in a safe, non-production way.
license: MIT
metadata:
  mode: verify
  purpose: build-run
---

# Build and Run

## When to Use

- Confirm the codebase compiles, reproduce a runtime issue locally, or validate environment-dependent changes.

## Rules

- Do not use production credentials or external services unless the user provides safe mocks/stubs.
- Use `source setTestEnv.sh` for local env needed by tests or the app.
- Prefer reproducible, minimal commands and capture key output lines.

## Commands

- **Compile:** `go build -v ./...`
- **Format:** `go fmt ./...`
- **Vet:** `go vet -v ./...`
- **Tidy deps:** `go mod tidy`
- **Run tests that reproduce an issue:** `source setTestEnv.sh && go test -run <TestName> ./pkg/path`
- **Start example app:** `cd example2/cmd/app && go run main.go` (use with test env)

## Output

- **Result:** success or failure.
- **Key logs:** first relevant error or stack lines.
- **Minimal repro:** 1-3 commands.
- **Next steps:** which logs/files to inspect or which mocks to add.

## Examples

- "Does the project compile?" - run `go build -v ./...` and report.
- "Reproduce failing integration test X" - provide commands and first failing lines.

## Related Skills

- `test-runner`, `ci-orchestrator`, `fix-suggester`

## References

- `AGENTS.md` (build and run commands), `setTestEnv.sh`, `llms.txt`
