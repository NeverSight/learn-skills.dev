---
name: otel-python
description: OpenTelemetry in Python — SDK setup, declarative config, zero-code instrumentation (opentelemetry-instrument, opentelemetry-distro), contrib auto-instrumentation, manual API, performance tuning, breaking changes. Use when configuring or troubleshooting OpenTelemetry in a Python service. Triggers on "setup otel in python", "python telemetry", "python tracing", "opentelemetry-instrument", "opentelemetry-distro", "TracerProvider python", "MeterProvider python", "FastAPI/Flask/Django otel", "python logging bridge".
---

# OpenTelemetry in Python

Entry point for OpenTelemetry mechanics in Python services. Load a reference below based on
the task; each reference is self-contained.

## References

| File | Use when |
|---|---|
| [`references/declarative-setup.md`](references/declarative-setup.md) | Configuring the SDK via declarative YAML (`opentelemetry-configuration` / `opentelemetry.configuration`): `load_config_file`, `configure_sdk`, `file_format`, env substitution, `OTEL_CONFIG_FILE` and programmatic activation. |
| [`references/api.md`](references/api.md) | Import paths, global API access, tracer/meter/logger usage, attributes, propagation, the Python logging bridge (`LoggingHandler`). |
| [`references/instrumentation-libraries.md`](references/instrumentation-libraries.md) | Zero-code (`opentelemetry-distro`, `opentelemetry-bootstrap`, `opentelemetry-instrument`), the contrib catalog, and manual instrumentation following semconv. |
| [`references/performance.md`](references/performance.md) | Tuning sampling, batch span processor, periodic metric reader, views, asyncio context, exporters, graceful shutdown. |
| [`references/breaking-changes.md`](references/breaking-changes.md) | Auditing existing code for deprecated/renamed APIs and semconv changes across recent SDK/contrib releases. |

## Sources of Truth

For YAML schema details, fetch the upstream sources listed in the `otel-declarative-config` skill.
For Python-specific facts:

| Fact | Fetch |
|---|---|
| Latest `opentelemetry-sdk` / `opentelemetry-api` | `WebFetch https://pypi.org/pypi/opentelemetry-sdk/json` (`.info.version`) |
| Latest `opentelemetry-configuration` | `WebFetch https://pypi.org/pypi/opentelemetry-configuration/json` |
| Latest `opentelemetry-distro` | `WebFetch https://pypi.org/pypi/opentelemetry-distro/json` |
| Latest `opentelemetry-instrumentation-<pkg>` (contrib) | `WebFetch https://pypi.org/pypi/opentelemetry-instrumentation-<pkg>/json` |
| Latest OTLP exporter | `WebFetch https://pypi.org/pypi/opentelemetry-exporter-otlp/json` |
| Declarative config support (released 1.44.0 overview) | `WebFetch https://raw.githubusercontent.com/open-telemetry/opentelemetry-python/v1.44.0/opentelemetry-configuration/README.rst` |
| Declarative config vendored schema (released 1.44.0) | `WebFetch https://raw.githubusercontent.com/open-telemetry/opentelemetry-python/v1.44.0/opentelemetry-configuration/src/opentelemetry/configuration/schema.json` |
| SDK CHANGELOG through 1.44.0 | `WebFetch https://raw.githubusercontent.com/open-telemetry/opentelemetry-python/v1.44.0/CHANGELOG.md` |
| Contrib CHANGELOG through 0.65b0 | `WebFetch https://raw.githubusercontent.com/open-telemetry/opentelemetry-python-contrib/v0.65b0/CHANGELOG.md` |
| Python getting-started docs | `WebFetch https://opentelemetry.io/docs/languages/python/getting-started/` |

## Cross-References

- Schema-level facts: `otel-declarative-config` skill (language-agnostic YAML schema sources).
- SDK version selection across languages: `otel-sdk-versions` skill.
- Semantic conventions lookup: `otel-semantic-conventions` skill.
