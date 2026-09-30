---
name: otel-go
description: OpenTelemetry in Go — SDK setup, API surface, breaking changes, contrib instrumentation libraries (otelhttp, otelgrpc, otelmongo), compile-time zero-code instrumentation (otelc), and performance tuning. Use when adding, reviewing, or configuring OpenTelemetry in a Go service. Triggers on "setup otel in go", "go telemetry", "go tracing", "otelconf go", "otelhttp", "otelgrpc", "TracerProvider go", "MeterProvider go", "otelc", "compile-time instrumentation go", "zero-code go instrumentation", "go build instrumentation", or any Go-related OTel question.
---

# OpenTelemetry in Go

Entry point for OpenTelemetry mechanics in Go services. Load a reference below based on the
task; each reference is self-contained.

## References

| File | Use when |
|---|---|
| [`references/declarative-setup.md`](references/declarative-setup.md) | Configuring the SDK via `otelconf` and YAML: providers, propagators, shutdown, env-var substitution. |
| [`references/api.md`](references/api.md) | Looking up import paths, global API access, tracer/meter/logger usage, attributes, propagation, log bridges (zap, slog). |
| [`references/instrumentation-libraries.md`](references/instrumentation-libraries.md) | Picking or wiring contrib libraries (otelhttp, otelgrpc, database, AWS, message queues, propagators, resource detectors), and writing manual instrumentation that follows semconv. |
| [`references/performance.md`](references/performance.md) | Tuning sampling, batch processor, metric reader, exporter compression/retry, attribute allocation, log `Enabled()` short-circuiting, graceful shutdown. |
| [`references/breaking-changes.md`](references/breaking-changes.md) | Auditing existing code for deprecated calls, renamed semantic conventions, and removed APIs across recent SDK / contrib releases. |
| [`references/compile-time-instrumentation.md`](references/compile-time-instrumentation.md) | Zero-code, compile-time instrumentation with `otelc`: usage modes (`otelc go build`, tool dependency, toolexec drop-in), subcommands, supported libraries, rule sources/precedence, and pinning via `otel.instrumentation.go`. |

For upgrade reviews, always finish with a safe local verification path (`go mod tidy -diff`,
`go build ./...`, and `go test ./...`). Test exporter URL or retry changes against a disposable
local receiver, never a deployment endpoint.

## Module versioning — read before adding dependencies

opentelemetry-go is split into **independently versioned module groups**. They do NOT
share one version number. Assuming they do is the most common cause of broken builds
and version churn:

| Module group | Example modules | Version line |
|---|---|---|
| Stable signals (traces, metrics) | `go.opentelemetry.io/otel`, `otel/sdk`, `otel/trace`, `otel/metric`, OTLP trace/metric exporters | **v1.x** (e.g. v1.46.0) |
| Logs | `otel/log`, `otel/sdk/log`, `otel/exporters/otlp/otlplog/otlploghttp` | **v0.x** (separate, lower line) |
| Contrib instrumentation | `contrib/instrumentation/net/http/otelhttp`, `.../otelgrpc` | **v0.x** (separate line, e.g. v0.71.0) |
| Contrib log bridges | `contrib/bridges/otelslog`, `otelzap`, `otellogrus`, `otellogr` | **v0.x** |

**The trap:** pinning every module to the core version (e.g. `go get go.opentelemetry.io/otel/log@v1.46.0`)
fails — log and bridge modules have no v1.x tag. Hand-picking and re-guessing each `@vX`
is the churn to avoid.

**Do this instead** — add each module with `@latest` and let Go resolve a compatible set:

```bash
go get go.opentelemetry.io/otel@latest go.opentelemetry.io/otel/sdk@latest
# logs (separate v0.x line — do NOT force the core version):
go get go.opentelemetry.io/otel/log@latest go.opentelemetry.io/otel/sdk/log@latest \
       go.opentelemetry.io/otel/exporters/otlp/otlplog/otlploghttp@latest
# contrib (instrumentation and bridges each resolve to their own v0.x line):
go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@latest \
       go.opentelemetry.io/contrib/bridges/otelslog@latest
go mod tidy && go build ./...
```

If exact versions are required, fetch each module group's tag from its own source
(see below) — never infer one group's version from another's.

## Sources of Truth

For YAML schema details, fetch the upstream sources listed in the `otel-declarative-config` skill.
For Go-specific facts:

| Fact | Fetch |
|---|---|
| Latest `go.opentelemetry.io/otel` core release | `gh api repos/open-telemetry/opentelemetry-go/releases/latest -q '.tag_name'` |
| Latest `go.opentelemetry.io/contrib` release | `gh api repos/open-telemetry/opentelemetry-go-contrib/releases/latest -q '.tag_name'` |
| Latest `otelconf` module tag | `gh api repos/open-telemetry/opentelemetry-go-contrib/git/matching-refs/tags/otelconf -q '.[-1].ref'` |
| Latest Go semconv package | Search the selected core release's CHANGELOG for `Add the go.opentelemetry.io/otel/semconv/`; do not infer package availability from the upstream semantic-conventions release. |
| `otel-go` CHANGELOG | `WebFetch https://raw.githubusercontent.com/open-telemetry/opentelemetry-go/main/CHANGELOG.md` |
| `otel-go-contrib` CHANGELOG | `WebFetch https://raw.githubusercontent.com/open-telemetry/opentelemetry-go-contrib/main/CHANGELOG.md` |

## Cross-References

- Schema-level facts: `otel-declarative-config` skill (language-agnostic YAML schema sources).
- SDK version selection across languages: `otel-sdk-versions` skill.
- Semantic conventions lookup: `otel-semantic-conventions` skill.
