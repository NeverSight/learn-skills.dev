---
name: voltsp
description: Build, troubleshoot, and test VoltSP pipelines (Java DSL and YAML API), including runtime configuration/secrets interpolation and deployment via CLI or Kubernetes/Helm. Use when authoring pipeline definitions, environment configs, plugin extensions, or pipeline validation tests.
---

# VoltSP Pipeline Engineering

Use this skill as a compact execution guide, then load only the reference file needed for the current task.

Prefer official VoltSP documentation whenever details conflict with memory.

## Choose the track

1. Choose pipeline definition style:
- Java DSL: read `references/pipelines-java.md` and `references/maven-setup.md`.
- YAML API: read `references/pipelines-yaml.md`.

2. Choose runtime/deployment context:
- Local CLI: read `references/cli-bare-metal.md`.
- Kubernetes/Helm: read `references/kubernetes.md`.

3. Configure values and secrets:
- Runtime configuration model + interpolation + secure config: read `references/configuration.md`.

4. Implement pipeline logic and tests:
- For list of plugins and their APIS: read `references/plugins-catalog.md`.
- Plugin deep dives and response format: read `references/plugins.md`.
- Test strategy (unit/in-process/Testcontainers): read `references/testing.md`.
- E2E-backed pipeline implementation patterns: read `references/pipeline-kinds.md`.

## Deterministic resources

Use deterministic helpers for repetitive or fragile setup work:

- Create starter files from templates with:
  `python3 scripts/scaffold_voltsp_pipeline.py --out-dir <dir> --pipeline-name <name> --track <java|yaml|both>`.
- Validate separation of pipeline definition vs runtime config/helm values with:
  `python3 scripts/check_voltsp_yaml_layout.py --definition <pipeline.yaml> [--config <config.yaml>] [--helm-values <values.yaml>]`.

Template files used by the scaffold script:
- `assets/templates/java/Pipeline.java.tmpl`
- `assets/templates/maven/pom.xml`
- `assets/templates/yaml/pipeline-definition.yaml`
- `assets/templates/yaml/runtime-config.yaml`
- `assets/templates/helm/values.yaml`

## Output rules

- Return copy-pasteable commands and files.
- Keep environment-specific values in config, not hardcoded in pipeline logic.
- Use secure paths for secrets (`--configSecure`, Helm `configurationSecure`, or secret interpolation) instead of plain values.
