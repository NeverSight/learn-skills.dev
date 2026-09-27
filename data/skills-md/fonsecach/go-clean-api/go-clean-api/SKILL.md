---
name: go-clean-api
description: 'Validates and reproduces a Go HTTP API whose dependencies point inward: cmd wires, domain owns entities and ports, application owns use cases, infrastructure owns adapters, delivery owns chi. Use when the user says "go-clean-api", "review the layers", "where does this code go", "add an endpoint", "scaffold a Go API", "OpenAPI", or "add telemetry". Do NOT use for line-level Go style (go-coding-standards), REST resource shape (go-api-design), CLIs and libraries (go-project-layout), or feature planning (tlc-spec-lean).'
license: MIT
metadata:
  author: github.com/fonsecach
  version: '1.0.0'
---

# Go Clean API

Dependencies point inward. The binary only wires. A handler that imports a driver has already lost the architecture, no matter how clean the SQL is.

```
cmd  →  delivery  →  application  →  domain  ←  infrastructure
wire     HTTP          rules         ports         adapters
```

Two moves. **Validate** an existing tree and report what breaks the arrow. **Reproduce** by writing the next file in the package the map already names. Line-level style stays in `go-coding-standards`. This skill decides where the code lives.

## Why this shape

The failure mode is a "service" package that slowly learns HTTP, SQL, and config because every new file had nowhere obvious to go. Naming the four inner packages up front removes that choice. `domain` can be tested without a database. `infrastructure` can be swapped with a decorator without editing the handler. `cmd` is the only file that is allowed to know both.

`go-project-layout` calls the same idea `service/`, `store/`, and `handler/` directly under `internal/`. Do not rename this map to match it. Here the application layer is `application/usecase`, the port lives in `domain/repository`, and HTTP lives in `delivery`. Config loaded from the environment is a struct, not a functional option. There is no `GetDB()` singleton: construction is visible in `cmd`.

A use case that only forwards one repository call is not a layer. It is a file with nothing of its own to change. Reads that validate input and call one port stay on the handler.

## Critical rules

These hold even if no reference file is read.

1. `domain` imports the standard library and pure value types (time, uuid). An import of chi, pgx, `net/http`, config, application, infrastructure, or delivery is a blocker.
2. `application` imports `domain` only. Same blocker list as rule 1.
3. `infrastructure` implements a `domain` port. It does not import `application` or `delivery`.
4. Business data crosses into `delivery` through a `domain` port or a use case. The HTTP layer may import `infrastructure/security` (JWT, hasher) and `infrastructure/observability` (counters, trace-aware logs); `cmd` still constructs them. It must not import a repository package, `pgx`, or `database/sql`. A sentinel the handler compares with `errors.Is` is declared in `domain`, or in the use case when it is an application rule.
5. `cmd` is the only composition root. No DI framework, no `init()` wiring, no package-level connection getter. `os.Exit` appears only in `main`. `run` returns `error`.
6. Create a use case when there is a rule, a decision, or more than one port. Otherwise the handler calls the port.
7. Behavior wrapped around an existing port (fallback, cache, metrics) is a decorator in `infrastructure`, composed in `cmd`. A cancelled `context` is the caller giving up: do not fall back and do not write a side effect.
8. A change to path, body, status, or auth updates `docs/openapi.yaml` in the same change. The spec is embedded and served; it is the contract.
9. Telemetry is optional. A down collector does not stop startup. Span and metric labels use the chi route template, never the raw path.
10. Do not add `pkg/`, `src/`, `util`, `common`, `helpers`, or `models`.

Module paths, Scalar, and the OpenTelemetry wiring live in [libraries.md](references/libraries.md). Read it before adding a route's docs, before adding telemetry, and before choosing modules for a new service.

## Map

```text
cmd/<bin>/main.go
config/
internal/domain/entity/
internal/domain/repository/
internal/application/dto/
internal/application/usecase/<context>/
internal/infrastructure/database/          # pool, reference cache
internal/infrastructure/database/repository/
internal/infrastructure/security/
internal/infrastructure/external/<provider>/
internal/infrastructure/observability/
internal/delivery/http/                    # router + RouterDeps
internal/delivery/http/handler/
internal/delivery/http/middleware/
docs/openapi.yaml
docs/docs.go                               # go:embed
migrations/
```

`internal/` is what stops the outside world from importing the service. Package name equals the directory: short, lower case, no stutter (`auth.LoginUseCase`, not `auth.AuthLoginUseCase`).

## Modes

- **Validate** (default). Run `scripts/check_layers.py` on the module root, then write the report at the bottom. Severity: blocker (arrow broken or a rule in the wrong package), important (contract, test, degradation), note (name, file size).
- **Reproduce.** New service or new feature. Write the files. Do not stop at a tree diagram.
- **Repair.** The smallest diff that restores the arrow. Do not reshuffle packages that already match the map.

## Where a feature goes

1. New concept → `internal/domain/entity`. Named fields. An invariant with no I/O is a method or a function in that package.
2. Persistence for that aggregate → an interface in `internal/domain/repository`. Every method takes `context.Context` and returns `error`.
3. SQL → `internal/infrastructure/database/repository`, constructor `NewX(pool)`. An infrastructure error the HTTP layer must distinguish becomes a domain sentinel.
4. A rule → `internal/application/usecase/<context>/<action>.go` with `New` and `Execute`. A DTO in `application/dto` when the shape is not the entity.
5. HTTP → one handler method, one route, only the middleware that route needs.
6. Contract → `docs/openapi.yaml`, and the embed already points at it.
7. Tests sit beside the package. Use case: fake the port. Repository: a real database. Handler: a fake port. Do not mock the driver inside the repository.

The port in `domain/repository` may have several methods; it is the persistence of one aggregate. A use case that needs one or two of them declares that small interface beside itself (`Hasher`, `TokenIssuer`). The concrete value from `cmd` still satisfies both. Do not add a method nobody calls, and do not invent an interface for a single implementation that has no second consumer.

## SOLID on this map

| Principle | What it means here |
| --- | --- |
| S | One reason to change: entity, port, use case, handler, repository, middleware. |
| O | New behavior around a port is a decorator. The primary adapter stays put. |
| L | The decorator honors the port: same signature, same domain errors. |
| I | The wide port is the aggregate. The narrow interface sits next to the consumer that needs a slice. |
| D | Use case and handler receive interfaces. Postgres, Argon2, and JWT are constructed in `cmd`. |

## Patterns worth copying

| Need | Shape |
| --- | --- |
| Required dependency (app DB, JWT secret length) | Fail startup. |
| Optional dependency (telemetry, secondary DB, external provider) | Warn and continue. Health reports the degraded part. |
| Small static lookup | Load once at startup under `sync.RWMutex`. A failed load degrades the routes that need it. |
| Quota | Atomic `INSERT ... ON CONFLICT DO UPDATE` in the database. Cache the plan with a short TTL; do not cache a read error. |
| Work that must not delay the response | After the handler writes, a goroutine with `context.WithoutCancel`. Log the failure. |
| External fallback | Decorator on the same port. A disabled client returns the inner repository with no wrapper. Normalize into the entity and mark the source. |
| HTTP edge | chi. Order: request id, recover, per-IP rate limit, auth, authorization, quota, async tracker, handler. Timeouts on `http.Server`. |
| Config | Struct from the environment, validated in `Load`. Convert env integers to `time.Duration` before they leave config. Never log a secret. |

`RouterDeps` carries handlers, the ports middleware needs, and the limiters. The router does not construct a repository.

## Wiring

```go
func main() {
    if err := run(); err != nil {
        slog.Error("fatal", "error", err)
        os.Exit(1)
    }
}

func run() error {
    cfg, err := config.Load()
    if err != nil {
        return err
    }
    // pools and clients; defer Close
    // concrete repos; decorator outside the primary
    // use cases with ports
    // handlers with a use case or a port
    // router with RouterDeps
    // ListenAndServe until ErrServerClosed; Shutdown on signal
    return nil
}
```

## Docs and telemetry

Both are part of reproducing this service, not a later project.

- **Docs.** `docs/openapi.yaml` is the source of truth. `docs/docs.go` embeds it. `GET /docs` serves Scalar. `GET /docs/openapi.yaml` serves the spec. Details and the HTML shell: [libraries.md](references/libraries.md).
- **Telemetry.** OpenTelemetry over OTLP/gRPC, `otelchi` for HTTP, `slog` JSON with `trace_id` and `span_id`, runtime and pool metrics. Disabled means zero providers. Setup failure is warn-and-continue. Backends stay outside the process. Collector, Prometheus, Loki, Tempo, and the Grafana dashboard come from the sibling skill `go-clean-observability`.

## Validation report

```markdown
# Architecture — <module or package>
## Verdict
<one sentence>
## Findings
- [blocker|important|note] `path:line` — what breaks the arrow, and the smallest move.
## Next step
<the file to write, in the package the map names>
```

When nothing breaks, say the arrow holds and which rule was checked (domain imports, wiring only in `cmd`, sentinel outside infrastructure, OpenAPI still matches the route).

## Scripts

Resolve `<skill-dir>` as the directory containing this `SKILL.md`.

| When | Command |
| --- | --- |
| Validate, and before calling Reproduce done | `python3 <skill-dir>/scripts/check_layers.py <module-root>` |

A non-zero exit means the arrow is broken. Fix the import the script names, or record it as a blocker in the report if the task is review-only. Skip the script only when no code-execution tool exists; then read the imports yourself and say once that you are on the degraded path.

The script scans non-test `.go` files. It does not judge use-case granularity, OpenAPI drift, or telemetry. Those stay in the report.

## Output behavior

Lead with the verdict or the files written. Cite `path:line` for every finding. Talk to the user in their language. Keep identifiers and package names in English. Do not reshuffle a tree that already matches the map.

## Examples

### Example 1: A handler imports the concrete repository

User says: "Does `company_handler.go` respect the layers? It imports infrastructure for `ErrReceitaUnavailable`."

Actions:

1. Run `check_layers.py` on the module.
2. Report a blocker: the handler depends on the adapter package so it can see a sentinel.
3. Name the move: declare the sentinel in `domain`, return it from the adapter and the decorator, compare it in the handler. Leave the read on the handler if it only validates the CNPJ and calls one port.

Result: A report. The repository is not edited unless the user asked for the repair.

### Example 2: Add a read endpoint

User says: "Add `GET /api/v1/companies/{cnpj}/certificates` from a `certificates` table."

Actions:

1. Entity, port, SQL adapter, handler method, route with the same middleware family as the neighboring company read.
2. No use case: the operation validates the CNPJ and reads one port.
3. Update `docs/openapi.yaml` in the same change.
4. Handler test with a fake port. Repository test against a real database when one is available.

Result: Files in the packages the map names. `check_layers.py` exits 0 on the new files.

### Example 3: Scaffold a service

User says: "New Go API, chi, Postgres, JWT. One use case: create an order."

Actions:

1. Lay down the map, `config.Load`, and a thin `main` / `run`.
2. `CreateOrder` takes a small store interface declared beside the use case. The Postgres adapter implements it. `cmd` connects them.
3. Embed an OpenAPI file and serve Scalar. Call `SetupOTel` so a missing collector does not abort startup.
4. Test the use case with a fake. Run `check_layers.py`.

Result: A module a second feature can extend without choosing new package names.

## Troubleshooting

### `check_layers.py` flags `delivery` → `infrastructure`

Cause: The handler imports a concrete repository, a pgx type, or an infrastructure sentinel.
Solution: Move the sentinel to `domain`. Depend on the port. Re-run the script.

### The route works and the spec does not mention it

Cause: The contract and the router diverged.
Solution: Update `docs/openapi.yaml` in the same change. The embed picks it up on the next build. Do not describe the route only in a comment.

### The process refuses to start because the collector is down

Cause: Telemetry was treated as a required dependency.
Solution: `SetupOTel` returns a no-op shutdown and a warning. The server still listens. Health may report telemetry as degraded.
