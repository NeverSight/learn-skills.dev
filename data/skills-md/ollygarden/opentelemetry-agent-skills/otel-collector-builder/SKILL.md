---
name: otel-collector-builder
description: Build custom OpenTelemetry Collector distributions with OCB (OpenTelemetry Collector Builder). Use when authoring or debugging a builder manifest (builder.yaml), choosing component and provider versions, building a collector that bundles a custom or out-of-distribution component, setting up CI or Docker builds of a distribution, or troubleshooting OCB build failures. Triggers on "ocb", "collector builder", "custom collector distribution", "builder manifest", "builder-config", and version-mismatch errors from OCB builds.
---

# OpenTelemetry Collector Builder (OCB)

OCB generates and compiles a custom Collector binary from a YAML manifest that lists exactly the components to include. Source of truth: [cmd/builder](https://github.com/open-telemetry/opentelemetry-collector/tree/main/cmd/builder) in opentelemetry-collector.

Use OCB when the stock `otelcol`/`otelcol-contrib` distributions don't fit: you need a component that ships in no distribution, a private/local component, or a slimmer binary with only the components you run.

This skill covers building the distribution. For configuring individual components, see `otel-collector`; for writing a new component, see the component-authoring guidance; for generating test traffic against the built binary, see `otel-telemetrygen`.

## Workflow

1. **Install OCB** at the version matching your target Collector version (see [Install](#install)).
2. **Write the manifest** — `dist:` block plus component lists. Start from the [minimal manifest](#minimal-manifest); full key reference in [references/manifest.md](references/manifest.md).
3. **Align versions.** All core components share one `v0.x.0` version, contrib components use the same `v0.x.0`, and confmap providers use the paired stable `v1.y.0`. Getting this wrong is the #1 build failure — see [Version alignment](#version-alignment).
4. **Build** with `ocb --config=builder.yaml` (binary is named `builder` when installed via `go install`). CI, Docker, multi-arch, and local-component workflows are in [references/workflows.md](references/workflows.md).
5. **Verify**: run `./dist/<name> validate --config=<collector-config>.yaml`, then start it and send test data (`otel-telemetrygen` skill). If the build fails, see [references/troubleshooting.md](references/troubleshooting.md).

## Install

Pick the OCB version equal to the Collector core version you're targeting.

```bash
# Release binary (named ocb): https://github.com/open-telemetry/opentelemetry-collector-releases/releases?q=cmd/builder
# Go install (binary is named `builder`, not `ocb`):
go install go.opentelemetry.io/collector/cmd/builder@v0.160.0
```

The commands below use `ocb`, the release-archive binary name. If you install with
`go install`, invoke the same commands as `builder ...` instead.

`ocb init` (experimental) scaffolds a new distribution repo — manifest, Makefile, sample config, README — in `--path` (default `.`).

## Minimal manifest

```yaml
# builder.yaml
dist:
  name: otelcol-custom
  description: Custom OpenTelemetry Collector distribution
  output_path: ./dist
  version: 1.0.0

receivers:
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.160.0

processors:
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.160.0

exporters:
  - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.160.0
  - gomod: go.opentelemetry.io/collector/exporter/debugexporter v0.160.0

providers:
  - gomod: go.opentelemetry.io/collector/confmap/provider/fileprovider v1.66.0
  - gomod: go.opentelemetry.io/collector/confmap/provider/envprovider v1.66.0
```

**`providers:` semantics.** Omitting the key entirely keeps OCB's built-in default set (env, file, http, https, yaml at the paired stable version). But setting `providers:` at all **replaces** that set. The generated Collector defaults `conf_resolver.default_uri_scheme` to `env`, so an explicit list without `envprovider` fails configuration validation unless you set another included provider as the default. Either omit the key, or include `envprovider` plus every scheme the collector's config will use.

Contrib components use the same list syntax:

```yaml
processors:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/tailsamplingprocessor v0.160.0
```

## Version alignment

Two version streams exist and must be paired:

| Stream | Modules | Example |
|--------|---------|---------|
| `v0.x.0` | OCB itself, all core components (`go.opentelemetry.io/collector/...`), all contrib components | `v0.160.0` |
| `v1.y.0` (stable) | confmap providers (`confmap/provider/...`), other 1.x modules (pdata, etc.) | `v1.66.0` |

Rules:

- Use the **same `v0.x.0`** for every core and contrib component, matched to the OCB version.
- The paired provider version for a given release is authoritative in that release's embedded default manifest: `https://github.com/open-telemetry/opentelemetry-collector/blob/cmd/builder/v0.160.0/cmd/builder/internal/config/default.yaml` — check it rather than guessing (for `v0.160.0` it is `v1.66.0`).
- Versions require the `v` prefix (`v0.160.0`, not `0.160.0`).
- `--skip-strict-versioning` defaults to `true`, so mismatches surface as Go module resolution errors, not friendly OCB errors. Align versions up front instead of debugging `go mod tidy` output.

## Build commands and flags

```bash
ocb --config=builder.yaml                                  # full build: generate + go mod tidy + compile
ocb --config=builder.yaml --skip-compilation               # generate sources only (two-stage CI)
ocb --config=builder.yaml --skip-generate --skip-get-modules  # compile pre-generated sources untouched
```

| Flag | Default | Purpose |
|------|---------|---------|
| `--config` | embedded default manifest | Manifest path. With no `--config`, OCB builds `otelcorecol`, a minimal test-only distribution. |
| `--skip-generate` | `false` | Don't regenerate Go sources |
| `--skip-compilation` | `false` | Generate sources, don't compile |
| `--skip-get-modules` | `false` | Don't run `go mod tidy`/downloads. Since v0.154.0 also leaves `go.mod` unregenerated. |
| `--skip-strict-versioning` | `true` | Set to `false` to make OCB verify resolved versions against the manifest |
| `--ldflags` / `--gcflags` | — | Extra `go build` flags |
| `--verbose` | `false` | Log the underlying Go commands |

Generated output in `output_path`: `main.go`, `components.go`, `main_others.go`, `main_windows.go`, `go.mod`, `go.sum`, and the compiled binary named `dist.name`. By default binaries are stripped (`-s -w`); set `dist.debug_compilation: true` for Delve-friendly builds.

## Reference files

- [references/manifest.md](references/manifest.md) — every manifest key: `dist:` fields, component spec (`gomod`/`import`/`name`/`path`), providers, `replaces`, `excludes`, `conf_resolver`, `telemetry`
- [references/workflows.md](references/workflows.md) — local component development, CI two-stage builds, Docker and multi-arch builds, relationship to `opentelemetry-collector-releases`
- [references/troubleshooting.md](references/troubleshooting.md) — version mismatches, module conflicts, CGO, missing providers, runtime failures
