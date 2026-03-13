---
name: blogwatcher-cli
description: Use when managing or interacting with favorite blogs via the BlogWatcher CLI—adding/removing blogs, scanning for new posts, listing articles, marking read/unread, or modifying related CLI behavior, scanning, storage, and tests.
---

# BlogWatcher CLI

## Quick Orientation
- Use the Cobra entry point in `cmd/blogwatcher/main.go` and `internal/cli/`.
- Route business logic through `internal/controller` and persistence through `internal/storage`.
- Use scanning pipeline packages in `internal/scanner`, `internal/rss`, and `internal/scraper`.
- Remember the default SQLite path is `~/.blogwatcher/blogwatcher.db` and is created on demand.

## Run Commands
- Run locally with `go run ./cmd/blogwatcher ...`.
- Build with `go build ./cmd/blogwatcher`.

## Change Workflow
1. Add or adjust CLI commands in `internal/cli/commands.go` (Cobra options, arguments, output formatting).
2. Put non-trivial logic in `internal/controller` so the CLI stays thin and testable.
3. Update storage or schema in `internal/storage/database.go` and adjust model conversion in `internal/model` if needed.
4. Modify scanning behavior in `internal/scanner` and its helpers (`internal/rss`, `internal/scraper`).
5. Update or add tests under `internal/` or `cmd/` for every feature change or addition.

## Test Guidance
- Run tests with `go test ./...`.
- If you add a feature, add tests and any necessary dummy data.
- Keep tests focused on CLI behavior, controller logic, and scraper/RSS parsing outcomes.

## Output Conventions
- Preserve user-friendly CLI output with colors and clear errors.
- When listing posts available for reading, always include the link to each post in the output.
- Keep error handling consistent with existing exceptions (`BlogNotFoundError`, `BlogAlreadyExistsError`, `ArticleNotFoundError`).

### Example (posts available for reading)
```text
Unread articles (2):

  [12] [new] Understanding Click Contexts
       Blog: Real Python
       URL: https://realpython.com/click-context/
       Published: 2025-11-02

  [13] [new] Async IO in Practice
       Blog: Test & Code
       URL: https://testandcode.com/async-io-in-practice/
```
