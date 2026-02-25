---
name: helm-best-practices
description: Expert guidance for authoring and maintaining Helm charts following standardized conventions, global registry support, templating best practices, and Kubernetes deployment patterns.
license: Apache-2.0
tags:
  - helm
  - kubernetes
  - devops
  - deployment
  - charts
---

# Helm Chart Style Guide

This skill provides standardized conventions for authoring and maintaining Helm charts, with a focus on:

- Global registry override using `.Values.global.image.registry`
- Clear, minimal templating
- Consistent `image:` blocks for all containers

## When to Use

Activate this skill when:

- Creating new Helm charts
- Reviewing or modifying existing Helm charts
- Configuring image registries for air-gapped environments
- Setting up multi-chart deployments with Helmfile

## Image Configuration Best Practices

All charts **must** support the top-level configuration for global image settings.

```yaml
global:
  image:
    registry: registry.mycompany.com
```

This enables centralized control of image sources across all dependencies and microservices.

### Consistent Image Blocks

All charts should follow a consistent `image:` block for every containerized application.

Fields should be templated for `registry`, `repository`, `tag`, `pullPolicy`, and `pullSecrets` for all containers.

Every chart **must** define all image values with reasonable defaults in `values.yaml`:

```yaml
prometheus:
  image:
    registry: docker.io
    repository: prom/prometheus
    tag: v2.52.0
    pullPolicy: IfNotPresent
```

### Templating Pattern for Registry Override

Use a registry value at the top of the template. This pattern ensures ability to use internal registries (e.g., `registry.mycompany.com`) for air-gapped environments or mirrored image sources:

```gotmpl
{{- $registry := .Values.prometheus.image.registry | default .Values.global.image.registry | default "docker.io" -}}
image:
  registry: {{ $registry }}
  repository: {{ .Values.prometheus.image.repository }}
  tag: {{ .Values.prometheus.image.tag }}
  pullPolicy: {{ .Values.prometheus.image.pullPolicy }}
```

## Templating Conventions

Template **only when necessary**. Keep templates readable and manageable by avoiding over-templating.

**Template:**

- Labels
- Annotations
- Resource requests and limits for CPU and memory for each container
- Service port numbers and names

**Avoid Templating:**

- Most values already present in `values.yaml` unless dynamically constructed

## Linting & Validation

- Run `helm lint` before commits
- Use `helm template` for rendering checks
- Ensure `values.yaml` and `Chart.yaml` are fully in sync with templated expectations

## Automated Chart Testing with ct

Use the [chart-testing](https://github.com/helm/chart-testing) tool (`ct`) to automate linting, installation, and upgrade checks for charts.

### Installing ct

Install `ct` (chart-testing) locally:

```sh
brew install helm/chart-testing/ct
# or via Docker:
# docker pull quay.io/helmpack/chart-testing
```

### Using ct

```sh
ct lint --config charts/your-chart/ct.yaml
ct install --config charts/your-chart/ct.yaml
```

Typical workflow:

- Lint all charts: `ct lint --all`
- Install and test charts: `ct install --all`
- Test only changed charts: `ct lint --charts charts/your-chart`

### Best Practices

- Always run `ct lint` and `ct install` before submitting a PR
- Ensure `ct.yaml` is up to date with chart locations and test settings
- Integrate `ct` into CI pipelines for automated validation
- Address all errors and warnings before merging

## Helmfile Multi-Chart Management

[Helmfile](https://github.com/helmfile/helmfile) enables declarative management of multiple Helm charts and environments.

### Installing Helmfile

```sh
brew install helmfile
# or via Docker:
# docker run --rm -v $PWD:/apps -w /apps ghcr.io/helmfile/helmfile:latest helmfile --help
```

### Using Helmfile

- Define releases and environments in `helmfile.yaml` or `helmfile.d/*.yaml`
- Use `values:` blocks to layer configuration and support overrides per environment
- Run `helmfile lint` to validate all releases and values
- Apply changes with `helmfile apply` (dry-run with `--dry-run` first)
- Sync state with `helmfile sync` to ensure all releases match the desired state

### Helmfile Best Practices

- Keep environment-specific values in separate files (e.g., `values-prod.yaml`, `values-dev.yaml`)
- Use `secrets:` for sensitive values, leveraging [helm-secrets](https://github.com/jkroepke/helm-secrets) if needed
- Prefer referencing charts by version for reproducibility
- Use `helmfile diff` before applying changes to preview impact
- Document all environments and overrides clearly
- Validate with `helmfile lint` and test deployments in CI where possible

## Naming Conventions

Chart names must be lower case letters and numbers. Words may be separated with dashes (-).

Neither uppercase letters nor underscores can be used in chart names. Dots should not be used in chart names.

YAML files should be indented using two spaces (and never tabs).

## CRDs

When working with Custom Resource Definitions (CRDs):

- There is a declaration of a CRD (YAML file with `kind: CustomResourceDefinition`)
- There are resources that use the CRD (resources with the CRD's `apiVersion` and `kind`)

For a CRD, the declaration must be registered before any resources of that CRD's kind(s) can be used.

With Helm 3, use the special `crds` directory in your chart to hold your CRDs. These CRDs are not templated, but will be installed by default when running `helm install`. If the CRD already exists, it will be skipped with a warning. Use `--skip-crds` flag to skip CRD installation.

**Note:** There is no support for upgrading or deleting CRDs using Helm.

## Standard Labels

The following labels are recommended for Helm charts:

| Name | Status | Description |
| ------ | -------- | ------------- |
| `app.kubernetes.io/name` | REC | App name, usually `{{ template "name" . }}` |
| `helm.sh/chart` | REC | Chart name and version: `{{ .Chart.Name }}-{{ .Chart.Version \| replace "+" "_" }}` |
| `app.kubernetes.io/managed-by` | REC | Always set to `{{ .Release.Service }}` |
| `app.kubernetes.io/instance` | REC | Set to `{{ .Release.Name }}` |
| `app.kubernetes.io/version` | OPT | App version: `{{ .Chart.AppVersion }}` |
| `app.kubernetes.io/component` | OPT | Component role, e.g., `frontend` |
| `app.kubernetes.io/part-of` | OPT | Top-level application when multiple charts work together |

An item of metadata should be a label if:

- It is used by Kubernetes to identify this resource
- It is useful for operators to query the system

If an item of metadata is not used for querying, it should be set as an annotation instead.

## Images

A container image should use a fixed tag or the SHA of the image. Never use `latest`, `head`, `canary`, or other "floating" tags.

## Pods

All PodTemplate sections should specify a selector:

```yaml
selector:
  matchLabels:
    app.kubernetes.io/name: MyName
template:
  metadata:
    labels:
      app.kubernetes.io/name: MyName
```

This makes the relationship between the set and the pod explicit and prevents breaking changes when labels change.

## RBAC Configuration

RBAC and ServiceAccount configuration should happen under separate keys:

```yaml
rbac:
  # Specifies whether RBAC resources should be created
  create: true

serviceAccount:
  # Specifies whether a ServiceAccount should be created
  create: true
  # The name of the ServiceAccount to use
  # If not set and create is true, a name is generated using the fullname template
  name:
```

For complex charts with multiple ServiceAccounts:

```yaml
someComponent:
  serviceAccount:
    create: true
    name:
anotherComponent:
  serviceAccount:
    create: true
    name:
```

`rbac.create` should default to `true`. Users who wish to manage RBAC access controls themselves can set this to `false`.

### ServiceAccount Helper Template

```yaml
{{/*
Create the name of the service account to use
*/}}
{{- define "mychart.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "mychart.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}
```

## Templates Directory Structure

The `templates/` directory should be structured as follows:

- Template files should have the extension `.yaml` if they produce YAML output
- The extension `.tpl` may be used for template files that produce no formatted content
- Template file names should use dashed notation (`my-example-configmap.yaml`), not camelcase
- Each resource definition should be in its own template file
- Template file names should reflect the resource kind (e.g., `foo-pod.yaml`, `bar-svc.yaml`)

### Defined Template Names

All defined template names should be namespaced to avoid collisions with subcharts:

**Correct:**

```yaml
{{- define "nginx.fullname" }}
{{/* ... */}}
{{ end -}}
```

**Incorrect:**

```yaml
{{- define "fullname" -}}
{{/* ... */}}
{{ end -}}
```

### Formatting Templates

Templates should be indented using two spaces (never tabs).

Template directives should have whitespace after the opening braces and before the closing braces:

**Correct:**

```text
{{ .foo }}
{{ print "foo" }}
{{- print "bar" -}}
```

**Incorrect:**

```text
{{.foo}}
{{print "foo"}}
{{-print "bar"-}}
```

## Checklist for Chart Review

### Structure

- [ ] Chart name is lowercase with dashes
- [ ] YAML files use 2-space indentation
- [ ] Templates use `.yaml` extension (or `.tpl` for helpers)
- [ ] Each resource is in its own template file

### Image Configuration

- [ ] Supports `global.image.registry` override
- [ ] Uses fixed tags or SHAs, not floating tags
- [ ] All image fields are configurable in `values.yaml`

### Labels & Selectors

- [ ] Includes recommended standard labels
- [ ] PodTemplate sections have proper selectors

### RBAC

- [ ] RBAC and ServiceAccount are separate config sections
- [ ] `rbac.create` defaults to `true`
- [ ] ServiceAccount helper template is properly namespaced

### Validation

- [ ] Passes `helm lint`
- [ ] Passes `ct lint`
- [ ] `values.yaml` and `Chart.yaml` are in sync
