---
name: tech-preferences
description: Apply James's technology choices and exclusions when selecting stacks, building software, adding dependencies, reviewing architecture or considering migrations. Flag meaningful deviations early, ask before unfamiliar technology, and respect recorded decisions.
license: Apache-2.0
metadata:
  author: jamespegg
  version: "1.2.0"
---

# Tech Preferences

Use these defaults for James's personal software projects. This skill is about **what to build with**; `engineering-principles` is about how to design it, and `verifiable-trust` concerns AI verification and execution risks.

## How to apply

1. First inspect repository state, relevant `AGENTS.md` instructions and documented decisions. Existing technology is evidence, not automatically a permanent architectural decision.
2. For new work, follow the defaults below. In existing projects, **flag meaningful deviations early** and recommend alignment where useful; explain trade-offs and ask before migrating. Never make a migration incidentally.
3. If James chooses to retain a deviation, record that decision and its rationale in the appropriate repository documentation. Don't reopen it unless requested or materially new evidence warrants reconsideration.
4. Proactively suggest modern alternatives when they offer meaningful improvement or a learning opportunity, clearly distinguishing proven from experimental technology and explaining risk, operational cost and reversibility. **Ask before introducing any unfamiliar technology.** Avoid short-lived fads.
5. "Explore" means interest, **not** approval to adopt. Recorded project decisions and explicit exclusions take precedence over generic preferences. Prefer reusing existing conventions and infrastructure.

## Languages and frontend

| Classification | Guidance |
| --- | --- |
| **Prefer** | Go for new backends, CLIs and developer tools. Go standard library first; small focused libraries when useful. |
| **Go CLIs** | Use **Cobra** for maintained Go CLIs, including single-command tools. Scaffold with **`cobra-cli`** (both `init` and `add`) rather than hand-building the command structure. Add **Viper** only when configuration complexity warrants it. |
| **Prefer** | React + TypeScript + Vite for frontends, npm as package manager, ESLint and Prettier. Zustand for shared state. |
| **Accept** | Tailwind CSS; choose component, routing, query, form and validation libraries case by case. No mandated design system. |
| **Strongly avoid** | Next.js unless there is an exceptionally strong, concrete reason over React + Vite. Ask before introducing. |
| **Avoid** | Redux, Java, C#/.NET, PHP and heavyweight enterprise frameworks unless explicitly required. |
| **Scripting** | Just as task runner. Only tiny development glue in Bash; no substantial Bash scripts. Go for reusable tools. Python mainly for machine learning, not general scripting. |
| **Explore** | Microfrontends and Module Federation, not defaults. |
| **Quality** | Responsive and accessible UI, proportional to project maturity. |

## Go CLI conventions

- For **maintained CLI applications**, initialise the command structure with `cobra-cli init` in that executable's directory inside the existing Go module. Keep the generated `main.go` and `cmd/root.go` pattern; in a multi-executable monorepo this naturally becomes `cmd/<binary>/cmd/root.go` without an extra Go module. Use `cobra-cli add` when adding commands.
- Keep Cobra command files focused on flags, help, argument validation and dispatch. Put substantive application behaviour in appropriately named `internal/<capability>` packages; avoid additional framework layers.
- When adopting Cobra for an **existing CLI**, generate into an empty/disposable location first rather than overwriting code. Adapt the generated structure to preserve documented flags, positional arguments, stdin, help, signals and exit statuses. Retain idiomatic generator conventions wherever compatible; justify exceptions against real behaviour.
- Use **Viper** only for genuine multi-source configuration requirements (e.g. coordinated flags, environment variables and config files). The generator's `--viper` option is appropriate only then; a handful of flags or one environment variable do not justify it.
- Pure background services without a meaningful CLI need not use Cobra. Standard-library-only argument handling is reserved for disposable or exceptionally trivial one-off tools, **not** maintained single-command applications.

## Applications, interfaces and data

- **Repository and deployment structure:** One monorepo per side project, product or self-contained concept. Prefer distinct backend domains as small **independently deployed microservices**, even on small projects. Do not combine frontend and backend into one monolithic application. Independently deployed does *not* imply separate repositories or infrastructure stacks.
- **APIs:** gRPC + Protobuf by default, with REST/JSON gateway for browser or external clients. Buf and gRPC libraries/frameworks are welcome. Generate frontend TypeScript API clients from the REST gateway's OpenAPI contract by default. Protobuf-generated clients need not imply direct browser gRPC, but OpenAPI matches this preferred browser integration. GraphQL backed by gRPC is an area to explore only deliberately.
- **Databases:** PostgreSQL default. SQLite for genuinely small/embedded cases; MongoDB familiar and acceptable when suitable. GORM is familiar; `sqlc` is an interesting alternative to evaluate, not a mandatory default. Avoid stored procedures.
- **Communication:** Use synchronous flows for immediate consistency requirements and asynchronous flows for deliberately eventual consistency. Prefer fact/event-driven integration over command-like messaging where appropriate. Use Dapr's pub/sub, service invocation and related capabilities where helpful, without introducing needless indirection.
- **Identity:** Hosted OIDC/OAuth rather than home-grown auth. Auth0 familiar; Stytch worth exploring with permission. Keep authorisation explicit.

## Infrastructure, operations and security

- **Hosting:** Existing **Rackspace Spot Kubernetes only**. Use Kubernetes even for small projects; do not introduce a new cloud or hosting platform without approval.
- **GitOps:** Argo CD + Kustomize for first-party services; Helm for third-party applications. Avoid Terraform. Reuse current infrastructure and deployment conventions.
- **Development:** Devcontainers, Just and Docker/Compose; reproducible tooling and documented local setup.
- **CI/CD:** GitHub Actions with separate build, release and deploy/promotion workflows. Reuse existing flows. Build once, version an immutable artefact and promote the *same* artefact. Multi-stage minimal container images, pinned base images, non-root runtime, immutable image tags.
- **Configuration:** Environment variables for environment-specific settings, Kubernetes Secrets for credentials, suitable additional secrets solutions only when needed. Reviewable application policy may belong in version-controlled structured configuration; never embed secrets.
- **Telemetry:** OpenTelemetry instrumentation, structured logs, metrics, distributed traces; Grafana ecosystem with Prometheus, Loki and Tempo.
- **Resilience:** Explicit errors, reasonable timeouts, bounded retries, Kubernetes health/readiness probes, graceful shutdown and resource limits. Use Dapr where it reduces custom plumbing. Add advanced resilience patterns only when justified.
- **Security:** Secure by default even in experiments: least privilege, restricted permissions, non-root containers, validated inputs and security/dependency scanning.

## Verification, dependencies and documentation

- **TDD is the default for behavioural implementation and bug fixes.** Follow Matt Pocock's `implement` → `tdd` workflow: agree useful public testing seams, write one failing behaviour test before its implementation (red), implement only enough to pass (green), and repeat in small vertical slices. Test externally observable success, failure and recovery; use independently derived expected results, not tests that merely restate the code. Use an explicitly justified exception for non-behavioural or impractical-to-test work rather than creating low-value tests.
- Go `testing` package + Testcontainers for integration tests. Frontend Vitest + React Testing Library + Playwright.
- Enforce formatter, linter, type checks and security scanning in CI; checks should enforce real invariants.
- Use focused dependencies; embrace genuinely useful improvements rather than avoiding modern tools. Automate **minor/patch** updates; **major** upgrades require approval. Unfamiliar dependencies also require approval regardless of version.
- Maintain concise README, architecture and operations documentation, clear build/test commands and ADRs for important non-obvious decisions.

When recommending technology, clearly identify the default, material deviations, trade-offs, what needs explicit approval, and any decision worth recording. Avoid repeatedly debating settled choices.
