---
name: go-best-practices
description: >
  Comprehensive Go (Golang) development best practices and coding style guidelines. Activate for "audit", "review", "fix", or "refactor" tasks to ensure the development workflow follows industry standards, including concurrency safety, architectural compliance (no pkg/), and senior-level review checklists.
---

# Go Best Practices

This skill guides high-level architectural decisions and deep code reviews.

## Core Mandates
1.  **Architecture:**
    *   **NO `pkg/`**: Do not create or recommend a `pkg/` directory. It is an anti-pattern.
    *   **Flat by Default**: Encourage flat package structures unless complexity demands otherwise.
    *   **Standard Layout**: Use `internal/` for private logic and `cmd/` for multiple binaries.
2.  **Code Quality**:
    *   **Check First**: Always consult `references/style_cheatsheet.md` before making style edits.
    *   **Review Checklist**: Use `references/senior_review_checklist.md` for major PRs.
    *   **Modern Go**: Prefer generic functions (`func F[T any]`) over `interface{}`.
3.  **Concurrency**:
    *   **Lifecycle**: Every goroutine must have a clear exit condition (Context, WaitGroup).
    *   **Hygiene**: Use `errgroup` for parallel tasks.

## Workflow

### 1. Audit & Analyze
1.  **Inspect Layout**: Does the project use `pkg/`? Advise moving to `internal/` or root.
2.  **Review Style**: Check against `style_cheatsheet.md`.
    *   Are errors handled explicitly?
    *   Are contexts passed first?
    *   Are mutexes copied? (Use `go vet`).

### 2. Refactor
1.  **Plan**: Identify the specific architectural change (e.g., "Extract interface for decoupling").
2.  **Execute**: Apply changes incrementally.
3.  **Verify**: run `go build ./...`, `go test ./...`, and `golangci-lint run` after every significant edit.

### 3. Review
1.  **Checklist**: Run through `senior_review_checklist.md`.
2.  **Feedback**: Provide actionable, cited feedback.

### 4. Specialized Domains
*   **Web Services**: Consult `references/http_services.md` for routing, middleware, and observability patterns.
*   **Complex Testing**: Use `references/advanced_testing.md` for fuzzing, benchmarks, and integration tests.
*   **Game Development**: Refer to `references/ebitengine_docs.md` for Ebitengine-specific patterns.
*   **Idioms**: When in doubt, check `references/go_proverbs.md`.
*   **Linting**: Refer to `references/linting.md` for tool configuration and best practices.

## References
*   `references/style_cheatsheet.md`: Condensed critical style rules.
*   `references/senior_review_checklist.md`: High-level quality criteria.
*   `references/project_layout.md`: Standard module layout guide.
*   `references/architectural_decisions.md`: Template for ADRs.
*   `references/http_services.md`: Best practices for HTTP servers.
*   `references/advanced_testing.md`: Fuzzing and benchmarking guide.
*   `references/ebitengine_docs.md`: Ebitengine reference.
*   `references/go_proverbs.md`: Core Go philosophy.
*   `references/linting.md`: Linting tools and guidelines.
