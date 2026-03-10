---
name: write-helm-chart
description: >
  Create production-ready Helm charts for Kubernetes application deployment with templating,
  values management, chart dependencies, hooks, and testing. Covers chart structure, Go
  template syntax, values.yaml design, chart repositories, versioning, and best practices
  for maintainable and reusable charts. Use when packaging a Kubernetes application for
  repeatable deployments, parameterizing manifests for multiple environments, managing
  complex multi-component applications with dependencies, or standardizing deployment
  practices with versioned rollback capability across teams.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: intermediate
  language: multi
  tags: helm, chart, go-templates, kubernetes, packaging, deployment, templating
---

# Write Helm Chart

Create production-ready Helm charts for deploying applications to Kubernetes.

## When to Use

- Need to package Kubernetes application for repeatable deployments
- Want to parameterize manifests for different environments (dev/staging/prod)
- Managing complex multi-component applications with dependencies
- Sharing reusable deployment patterns across teams or organizations
- Implementing versioned application releases with rollback capability
- Need template-based configuration management for Kubernetes resources
- Want to standardize deployment practices across projects

## Inputs

- **Required**: Kubernetes manifests for your application (deployment, service, etc.)
- **Required**: Application name and version
- **Required**: List of configurable parameters (image tag, replicas, resources, etc.)
- **Optional**: Dependencies on other Helm charts (databases, message queues)
- **Optional**: Pre/post-install hooks for migrations or setup
- **Optional**: Chart repository URL for publishing
- **Optional**: Values for different environments

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete template files, values structures, and hooks.

### Step 1: Initialize Chart Structure and Metadata

Create the Helm chart directory structure and define chart metadata.

**Install Helm:**
```bash
# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# macOS
brew install helm

# Windows (Chocolatey)
choco install kubernetes-helm

# Verify installation
helm version
```

**Create chart structure:**
```bash
# Create new chart
helm create my-app

# Chart structure created:
# my-app/
#   Chart.yaml          # Chart metadata
#   values.yaml         # Default configuration values
#   charts/             # Chart dependencies
#   templates/          # Template files
#     deployment.yaml
#     service.yaml
#     ingress.yaml
#     _helpers.tpl      # Template helpers
#     NOTES.txt         # Post-install notes
#   .helmignore         # Files to ignore

# Or create from scratch
mkdir -p my-app/{templates,charts}
cd my-app
```

**Define Chart.yaml:**
```yaml
# Chart.yaml (excerpt - see EXAMPLES.md for complete file)
apiVersion: v2
name: my-app
description: A Helm chart for deploying my-app to Kubernetes
version: 0.1.0
appVersion: "1.0.0"
maintainers:
- name: Platform Team
  email: platform@example.com
# ... (keywords, dependencies, kubeVersion - see EXAMPLES.md)
```

**Create .helmignore:**
```
# .helmignore
# Patterns to ignore when packaging chart
.git/
.gitignore
.bzr/
.bzrignore
.hg/
.hgignore
.svn/
*.swp
*.bak
*.tmp
*.orig
*~
.DS_Store
.project
.idea/
*.tmproj
.vscode/
```

**Expected:** Chart directory structure created with all required files. Chart.yaml contains complete metadata. Dependencies listed if applicable. Chart validates: `helm lint my-app`.

**On failure:**
- Check YAML syntax in Chart.yaml: `helm lint my-app`
- Verify apiVersion is v2 (v1 deprecated)
- Ensure version follows SemVer (x.y.z)
- Check dependency repository URLs are reachable
- Use `helm show chart <chart>` to inspect existing charts for examples

### Step 2: Design values.yaml Structure

Create well-organized values.yaml with sensible defaults and documentation.

**Create comprehensive values.yaml:**
```yaml
# values.yaml (excerpt - see EXAMPLES.md for complete structure)
global:
  imageRegistry: ""
image:
  registry: docker.io
  repository: mycompany/my-app
  tag: ""
replicaCount: 3
service:
  type: ClusterIP
  port: 80
resources:
  limits: {cpu: 1000m, memory: 512Mi}
  requests: {cpu: 100m, memory: 128Mi}
# ... (ingress, autoscaling, probes, persistence - see EXAMPLES.md)
```

See [EXAMPLES.md](references/EXAMPLES.md#step-2-valuesyaml--complete-structure) for the complete values.yaml structure and values.schema.json

**Expected:** values.yaml organized logically with sections. All values documented with comments. Sensible defaults that work out-of-box. Schema validates value types. No hardcoded environment-specific values.

**On failure:**
- Validate YAML syntax: `yamllint values.yaml`
- Check schema validation: `helm lint my-app`
- Review against Helm best practices: `helm lint --strict my-app`
- Ensure all template references have corresponding values
- Test with minimal values: `helm template my-app --set image.repository=test`

### Step 3: Create Template Files with Go Templating

Write Kubernetes resource templates using Go template syntax and Helm functions.

**Create deployment template:**
```yaml
# templates/deployment.yaml (excerpt)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        # ... (see EXAMPLES.md for complete template with probes, volumes, etc.)
```

See [EXAMPLES.md](references/EXAMPLES.md#step-3-deploymentyaml--complete-template) for the complete deployment template

**Create helper template file:**
```yaml
# templates/_helpers.tpl (excerpt)
{{- define "my-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "my-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
# ... (labels, serviceAccountName, hpa.apiVersion - see EXAMPLES.md)
```

**Create conditional templates:**
```yaml
# templates/ingress.yaml (excerpt)
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "my-app.fullname" . }}
# ... (see EXAMPLES.md for complete ingress and HPA templates)
```

See [EXAMPLES.md](references/EXAMPLES.md#step-3-helperstpl--complete-helper-functions) for complete _helpers.tpl and conditional templates

**Expected:** Templates generate valid Kubernetes YAML. Conditionals work correctly (if/with). Helper functions produce expected output. Resources properly labeled and named. No hardcoded values in templates.

**On failure:**
- Test template rendering: `helm template my-app`
- Check for template syntax errors: `helm lint my-app`
- Validate Go template syntax carefully (dashes, spaces matter)
- Use `helm template --debug` for detailed error messages
- Test with different values files: `helm template my-app -f values-prod.yaml`
- Verify output is valid Kubernetes YAML: `helm template my-app | kubectl apply --dry-run=client -f -`

### Step 4: Add Hooks for Pre/Post-Install Actions

Create hooks for database migrations, setup tasks, or cleanup.

**Create pre-install hook for migrations:**
```yaml
# templates/hooks/pre-install-migration.yaml (excerpt)
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "my-app.fullname" . }}-migration
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "-5"
spec:
  template:
    spec:
      containers:
      - name: migration
        image: "{{ .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        command: ["/app/migrate"]
# ... (see EXAMPLES.md for test hook, pre-delete backup, NOTES.txt)
```

See [EXAMPLES.md](references/EXAMPLES.md#step-4-helm-hooks) for complete hook templates and NOTES.txt

**Expected:** Hooks execute in correct order (weights determine sequence). Pre-install migration completes before deployment. Test hook validates deployment. Pre-delete hook runs cleanup. NOTES.txt provides helpful post-install information.

**On failure:**
- Check hook annotations syntax exactly matches Helm spec
- Verify hook jobs have `restartPolicy: Never`
- Review hook execution: `kubectl get jobs -n <namespace>`
- Check hook logs: `kubectl logs job/<job-name> -n <namespace>`
- Ensure hook-delete-policy appropriate (before-hook-creation, hook-succeeded, hook-failed)
- Test hooks independently: `helm install --dry-run --debug my-app`

### Step 5: Test and Package Chart

Validate chart, run tests, and package for distribution.

**Lint and validate chart:**
```bash
# Basic linting
helm lint my-app

# Strict linting
helm lint --strict my-app

# Test template rendering
helm template my-app

# Test with custom values
helm template my-app -f values-prod.yaml

# Validate against Kubernetes cluster (dry-run)
helm install my-app my-app --dry-run --debug

# Check for deprecated API versions
helm install my-app my-app --dry-run | kubectl apply --dry-run=server -f -
```

**Create chart tests:**
```bash
# Run Helm tests
helm install my-app my-app -n test --create-namespace
helm test my-app -n test
kubectl logs -n test -l "helm.sh/hook=test" --tail=-1

# See EXAMPLES.md for complete test script (test-chart.sh)
```

**Package chart:**
```bash
# Update dependencies first
helm dependency update my-app

# Package chart
helm package my-app

# Creates: my-app-0.1.0.tgz

# Verify package
helm verify my-app-0.1.0.tgz

# Generate index for repository
helm repo index . --url https://charts.example.com/

# Creates: index.yaml
```

**Create different values files for environments:**
```yaml
# values-dev.yaml (excerpt)
replicaCount: 1
resources:
  limits: {cpu: 500m, memory: 256Mi}
ingress:
  hosts: [my-app-dev.example.com]

# values-prod.yaml (excerpt)
replicaCount: 5
autoscaling: {enabled: true, minReplicas: 3, maxReplicas: 10}
# ... (see EXAMPLES.md for complete env-specific values)
  tls:
  - secretName: my-app-tls
    hosts:
    - my-app.example.com
podDisruptionBudget:
  enabled: true
  minAvailable: 2
postgresql:
  enabled: true
  primary:
    persistence:
      size: 50Gi
    resources:
      limits:
        cpu: 4000m
        memory: 8Gi
```

**Test with different environments:**
```bash
# Test development values
helm install my-app-dev my-app -f values-dev.yaml --dry-run --debug

# Test production values
helm install my-app-prod my-app -f values-prod.yaml --dry-run --debug

# Install to dev namespace
helm install my-app my-app -f values-dev.yaml -n development --create-namespace

# Install to prod namespace
helm install my-app my-app -f values-prod.yaml -n production --create-namespace
```

**Expected:** Chart passes all lint checks. Template rendering produces valid Kubernetes YAML. Tests pass successfully. Chart packages without errors. Different values files work for each environment. Installation succeeds without warnings.

**On failure:**
- Review lint output for specific issues
- Check template syntax errors with `--debug` flag
- Verify all required values are set: `helm get values <release>`
- Test dependency resolution: `helm dependency list my-app`
- Validate packaged chart: `tar -tzf my-app-0.1.0.tgz`
- Check for missing files in package


### Step 6: Publish to Chart Repository

Set up chart repository and publish versioned releases.

**Options for publishing:**
```bash
# GitHub Pages
git checkout -b gh-pages && mkdir charts
cp my-app-0.1.0.tgz charts/
helm repo index charts/ --url https://username.github.io/repo/charts

# OCI registry (Helm 3.8+)
helm registry login registry.example.com -u $USER -p $PASS
helm push my-app-0.1.0.tgz oci://registry.example.com/charts

# Install from repo
helm repo add myrepo https://charts.example.com
helm install my-app myrepo/my-app -f custom-values.yaml
```

See [Extended Examples](references/EXAMPLES.md) for ChartMuseum setup, release automation, and complete README template.

**Expected:** Chart published to repository successfully. Chart discoverable via `helm search`. Installation works from repository. Versioning follows SemVer.

**On failure:**
- Verify repository URL accessible
- Check index.yaml generated: `helm repo index --help`
- For OCI registries, ensure authentication working
- Test repository addition: `helm repo add test <url>`
