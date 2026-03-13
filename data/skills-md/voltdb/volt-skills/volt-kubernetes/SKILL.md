---
name: volt-kubernetes
description: Helps deploying VoltDB cluster on Kubernetes. Use when user wants to create scripts creating clusters on Kubernetes with Volt's releases. Use when user asks to create terraform, helmfile or helm scripts. Use when user want to create configuration as code.
---

# Helper for deploying Volt's resources on Kubernetes
This skill focuses on creating cluster configuration as code using terraform, helmfile and helm.

## Tool Overview
- **Helm**: Configures kubernetes resources for a VoltDB cluster (called a release)
- **Helmfile**: Manages multiple helm releases with dependencies
- **Terraform**: Creates and manages cloud resources and high-level kubernetes resources

All tools use declarative scripts that can be version-controlled in git.
After changes are approved, re-run the specific tool to update resources.

## Quick Reference for LLM

**Key patterns to follow:**
1. **Directory structure**: Use modular, descriptive filenames (e.g., `voltdb-master.tf`, not `cluster.tf`)
1. **StateValues separation**: `base.yaml` (versions), `env.yaml.gotmpl` (env vars), `override.yaml.local` (local overrides)
1. **Create default environment for HelmFile**: Always start with a default environment.
1. **Service DNS**: `<release-name>-<service-name>.<namespace>.svc.cluster.local:<port>`
1. **Release dependencies**: Use `needs: [namespace/release-name]` in helmfile
1. **Local charts**: Use `chart: {{ .StateValues.voltsp.chart.path }}` for development
1. **VoltDB Published charts**: Use `chart: voltdb/voltdb` with `version: "{{ .StateValues.voltdb.chart.version }}"`
1. **VoltSP Published charts**: Use `chart: voltdb/volt-streaming` with `version: "{{ .StateValues.voltsp.chart.version }}"`
1. **Dangerous operations**: Comment out `initForce` and `deletePVC` by default with warnings
1. **Gitignore patterns**: `*local` in stateValues, `*.tfvars` in terraform
1. **Environment variables**: Pass from terraform to helmfile via `helmfile.tf` using `null_resource` with `local-exec`

## Important note about resource management
Terraform can execute helm with the helm-release resource, but we have found it to be unreliable.
Both terraform and helm depend on some internal state and those two are not always compatible.
That's why deployment scripts must be layered: **Terraform as cloud orchestrator, Helm as kubernetes orchestrator**.
Helmfile manages multiple helm releases and must be run from terraform.

**Resource ownership:**
- **Terraform manages**: Cloud resources (GKE/EKS/AKS), namespaces, secrets, network, infrastructure
- **Helm manages**: VoltDB/VoltSP cluster resources (pods, services, configmaps created by charts)

If some kubernetes resources are not strictly related to a cluster deployment, those can be created and managed by terraform.
For example, namespaces, config maps, pvc-s, secrets, etc.

Helm creates some kubernetes resources implicitly by setting values for the release. Those resources must be created and managed by helm.
If in doubt, always check the helm chart and clarify with a user.

## Prerequisites
Before generating deployment scripts, check that:
- **Helm v4.1.1+** is installed
- **kubectl v1.34.2+** is installed
- **Helmfile v1.2.3+** is installed
- **Terraform v1.5.7+** is installed
- **Java 17+** is installed
- **Maven 3.6+** is installed
- Valid **VoltDB Enterprise license** file is available

kubectl must be configured to connect to a cloud provider.

## Instructions
### Step 1: Understand the application details
Before any code is generated, verify with a user that there is a running integration test using testcontainers.
Such a test validates all required VoltDB components — helm values file, schema file, license, optional java code that can be packaged into a jar file.
Such a test validates all required VoltSP components — helm values file, license, optional java code that can be packaged into a jar file.
Such a test can be easily translated into a helm configuration.
If a user cannot point to such a test, please recommend creating one and quit.
**If a user selects a testcontainer test, please run it locally and verify that it passes.**

### Step 2: Script directory layout
Create the following directory structure at the root of the application:
```text
k8s/
  helmfile/
    stateValues/
      base.yaml                      # Default values (versions, paths)
      env.yaml.gotmpl                # Environment-specific values (from env vars)
      override.yaml.local.template   # Template for local overrides
    values/
      <release-name>.yaml            # Helm values for each release
    helmfile.yaml.gotmpl             # Helmfile release configuration
    README.md                        # Instructions for running helmfile
    .gitignore                       # Ignore *local files
  terraform/
    provider.tf                      # Cloud provider configuration
    variables.tf                     # Variable definitions
    terraform.tfvars.template        # Template for sensitive values
    outputs.tf                       # Output values
    gke.tf (or eks.tf, aks.tf)       # Cluster configuration
    network.tf                       # Network configuration
    namespace.tf                     # Namespace and secrets
    <resource>-<name>.tf             # Resource-specific files (e.g., voltdb-master.tf)
    build-jar.tf                     # Application build (if needed)
    helmfile.tf                      # Helmfile execution
    .gitignore                       # Ignore *.tfvars, .terraform, etc.
    README.md                        # Instructions for running terraform
```

**Key principles:**
- Use descriptive, resource-specific filenames in terraform (e.g., `voltdb-master.tf`, `voltdb-replica.tf`) instead of generic names
- Separate concerns: one file per major resource or logical grouping
- Keep sensitive data in `*.tfvars` files or `*.local` for helmfile - those files will be gitignored

### Step 3: Helm values
Look at the testcontainers test and identify all Volt services that are deployed and their resources like schema, deployment file, jar files, configuration, etc.
For each identified cluster deployment, create a yaml file with the same name as the cluster.
Those yaml files must be created in root project directory under 'k8s/helmfile/values' directory.
If the directory is missing, create it.

**Key points:**
- Add inline comments to warn about dangerous operations and explain critical settings
- Comment out dangerous options like `initForce` and `deletePVC` by default
- Add warnings about data loss risks
- Include inline explanations for non-obvious settings
- Schema can be inlined into yaml file or set with `--set-file` option with a local path
- Configure topics for CDC (Change Data Capture) if needed

See `references/volt-helm-release.md` for additional details.
Always check for the newest version of the helm chart and service version that the helm chart supports.

### Step 4: Helmfile releases
Helmfile requires a strict directory structure and configuration pattern.
```
helmfile/
  stateValues/
  - base.yaml
  - env.yaml.gotmpl
  - override.yaml.local.template
  values/
  helmfile.yaml.gotmpl
  README.md
  .gitignore
```
The README.md file with instructions on how to run helmfile. Helmfile can be run from terraform which should pass environment variables to helmfile. If helmfile is run from shell `terraform output name` commnad is used to get values for required environment variables.
The `helmfile.yaml.gotmpl` file contains helmfile release configuration.
The `stateValues` directory contains *.yaml or *.yaml.gotmpl files with helmfile values.

#### StateValues Directory
Create the following files in `helmfile/stateValues/`:

**1. base.yaml** - Default values for all releases (versions, paths):
```yaml
licensePath: ~/licence.xml
voltdb:
  chart:
    version: "3.14.0"  # Helm chart version
  version: "15.1.0"    # VoltDB application version
voltsp:
  chart:
    version: "1.6.0"   # Helm chart version
  version: "1.6.0"     # VoltSP application version
  jarPath: "/path/to/voltsp.jar"  # Path to VoltSP jar file
```
Always use the latest version of the helm chart and application version.
Check the helm chart and application versions in the helm repository.
Values related to paths in this file can be overridden with local specific values in `override.yaml.local.template`.
But keep the defaults in base.yaml.

**2. env.yaml.gotmpl** - Environment-specific values (extracted from env vars):
```yaml
namespace: {{ requiredEnv "NAMESPACE" }}
docker:
  pullImageSecretName: {{ requiredEnv "DOCKER_SECRET_NAME" }}
```
Use `{{ requiredEnv "ENV_NAME" }}` to extract required environment variables.
Helmfile will fail if required env vars are not set.

**3. override.yaml.local.template** - Template for local overrides:
The `override.yaml.local.template` file contains a template for the `override.yaml.local` file, with blank values.
Do not create `override.yaml.local` file.
The `override.yaml.local` file is created by users from the template and contains local-specific values.
This `override.yaml.local` file should not be checked in as it can contain sensitive data. Make sure adding it to .gitignore.
```yaml
# Copy this file to override.yaml.local and fill in your local values
# override.yaml.local is gitignored and should contain sensitive data
licensePath: ""
voltsp:
  jarPath: ""
```

**4. .gitignore** - Ignore local override files:
```
*local
```
This prevents sensitive local configuration from being committed.

#### Environment
The helmfile.yaml.gotmpl should configure all releases using a default environment:
```yaml
environments:
  default:
    values:
    - stateValues/base.yaml
    - stateValues/env.yaml.gotmpl
    - path: stateValues/override.yaml.local
      required: false
---
repositories:
  ...

releases:
  ...
```
User can later add more environments, but this is a good starting point.

#### Docker Pull Secret
To pull images from private repositories, kubernetes requires a secret with credentials.
The helmfile could release such a secret, but it's better to create it using terraform. The secret requires user, password, email - see terraform section.
The name should be the same as the secret name in the helmfile.yaml.gotmpl file.
The secret should be created in the namespace where the cluster is deployed.

#### Helm Repository
See `references/volt-helm-release.md` for information how to configure helm repository.
Verify whether additional repositories are required and include them in the helmfile.yaml.gotmpl file.
Example:
```yaml
repositories:
  - name: voltdb
    url: https://voltdb-kubernetes-charts.storage.googleapis.com
  # any other valid helm repository for kafka, prometheus, etc.
```

#### Releases
Helmfile can manage any number of releases with dependencies.

**Key patterns:**
- Use `needs` to define release dependencies (ensures correct deployment order)
- Use `{{ .StateValues.voltsp.chart.path }}` or `{{ .StateValues.voltdb.chart.path }}` for local charts during development
- Use `chart: voltdb/voltdb` or `chart: voltdb/volt-streams` for published charts
- Service DNS pattern: `<release-name>-cluster-client.{{ .StateValues.namespace }}.svc.cluster.local:<port>`
- Kafka DNS pattern: `<release-name>-cluster-0-kafka.{{ .StateValues.namespace }}.svc.cluster.local:9092`

**Example releases:**
Example, for the `products` application:
```yaml
releases:
  # VoltDB Products
  - name: voltdb-products
    chart: voltdb/voltdb
    version: "{{ .StateValues.voltdb.chart.version }}"
    namespace: {{ .StateValues.namespace | quote }}
    values:
      - values/voltdb-products-values.yaml
    set:
      - name: global.voltdbVersion
        value: {{ .StateValues.voltdb.version | quote }}
      - name: cluster.config.licenseXMLFile
        file: {{ .StateValues.licensePath | quote }}
      - name: cluster.config.schemas.products
        file: {{ .StateValues.voltdb.resources.products.schemaPath | quote }}
      - name: cluster.config.classes.products
        file: {{ .StateValues.voltdb.resources.products.jarPath | quote }}
      - name: cluster.clusterSpec.imagePullSecrets[0].name
        value: {{ .StateValues.docker.pullImageSecretName | quote }}

  # VoltSP Products
  - name: voltsp-products
    chart: voltdb/volt-streams
    version: "{{ .StateValues.voltsp.chart.version }}"
    namespace: {{ .StateValues.namespace | quote }}
    needs:
      - {{ .StateValues.namespace }}/voltdb-products
    values:
      - values/voltsp-products-values.yaml
    set:
      - name: streaming.licenseXMLFile
        file: {{ .StateValues.licensePath | quote }}
      - name: streaming.voltapps
        file: {{ .StateValues.voltsp.resources.products.jarPath | quote }}
      - name: imagePullSecrets[0].name
        value: {{ .StateValues.docker.pullImageSecretName | quote }}
      - name: podEnv.kafka-bootstrap-servers
        value: voltdb-products-cluster-0-kafka.{{ .StateValues.namespace }}.svc.cluster.local:9092
      - name: podEnv.voltdb-products-server
        value: voltdb-products-cluster-client.{{ .StateValues.namespace }}.svc.cluster.local:21212
```

**Important notes:**
- The `needs` field ensures releases are deployed in the correct order
- Use `namespace/release-name` format in `needs` when releases are in the same namespace
- The `podEnv` section sets environment variables used by the application
- Service DNS names follow kubernetes conventions: `<service-name>.<namespace>.svc.cluster.local:<port>`
- For local development, use `chart: {{ .StateValues.voltsp.chart.path }}` to reference local chart directories. no version is needed.
- For production, switch to published charts: `chart: voltdb/volt-streams` with `version` specified

See `references/volt-helm-release.md` for detailed helm values configuration.

#### Optional Observability release
**Propose to a user whether to include an observability release.**

As the cluster is created from scratch, the assumption is that monitoring services are not installed.
Volt uses Prometheus and Grafana for monitoring. See `references/volt-monitoring.md` for information how to enable monitoring.
Prometheus creates special kubernetes resources to correctly target and scrape metrics from pods.
By default, Prometheus is looking for pods in the same namespace.
Example of the standalone prometheus and grafana releases:
```yaml
releases:
  - name: prometheus
    chart: prometheus-community/prometheus-operator-crds
    namespace: {{ .StateValues.namespace | quote }}

  - name: monitoring
    chart: voltdb/management-console
    namespace: {{ .StateValues.namespace | quote }}
```
Mind that prometheus and grafana require additional cpu and memory resources.
Monitoring has to be released first.

### Step 5: Terraform resources
Terraform should define all cloud resources required for deployment. 

#### Questions to ask
**Ask a user the following questions:**
- which cloud provider to use
- what is the project name
- what is the project namespace
- what type of nodes the k8s will use
- whether to use a single node pool or to use multiple node pools for better transparency and isolation
- what is region and zone for deployment
- how nodes are visible to each other, should there be a specific security rules
- how nodes are accessible from the outside
- what is the name of the docker pull secret (default `dockerio-registry`) – user should provide additional email, user, password – those should be saved in terraform.tfvars file
Answer to those questions will drive values in variables.tf file.

#### Files and directories
Terraform resources are created in the root project directory under the 'k8s/terraform' directory.

**Required files:**

**1. .gitignore** - Ignore sensitive and generated files:
```
*.tfvars
.terraform
terraform.plan
terraform.tfstate
terraform.tfstate.backup
.terraform.lock.hcl
```

**2. README.md** - Instructions for running terraform with prerequisites and steps

**3. variables.tf** - Variable definitions with defaults:
```terraform
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "voltdb"
}

variable "docker_username" {
  description = "Docker registry username"
  type        = string
  sensitive   = true
}

variable "docker_password" {
  description = "Docker registry password"
  type        = string
  sensitive   = true
}

variable "docker_email" {
  description = "Docker registry email"
  type        = string
  sensitive   = true
}
```

**4. terraform.tfvars.template** - Template for sensitive values:
```terraform
# Copy this file to terraform.tfvars and fill in your values
project_id       = ""
docker_username  = ""
docker_password  = ""
docker_email     = ""
```

**5. outputs.tf** - Export values for helmfile and verification:
```terraform
output "namespace" {
  value = kubernetes_namespace.voltdb.metadata[0].name
}

output "docker_secret_name" {
  value = kubernetes_secret.dockerio_registry.metadata[0].name
}

output "cluster_endpoint" {
  value = google_container_cluster.primary.endpoint
  sensitive = true
}
```

**6. provider.tf** - Cloud provider and kubernetes configuration

**7. gke.tf (or eks.tf, aks.tf)** - Cluster configuration with node pools

**8. network.tf** - Network, VPC, firewall rules configuration

**9. namespace.tf** - Namespace and global secrets (docker pull secret)

**10. Resource-specific files** - Use descriptive names:
- `voltdb-products.tf` - VoltDB master cluster resources not controlled by helmfile or helm
- `build-jar.tf` - Application build resources (if needed)

**11. helmfile.tf** - Helmfile execution with environment variables:
```terraform
resource "null_resource" "helmfile_apply" {
  provisioner "local-exec" {
    command = "helmfile apply"
    working_dir = "${path.module}/../helmfile"
    environment = {
      NAMESPACE          = kubernetes_namespace.voltdb.metadata[0].name
      DOCKER_SECRET_NAME = kubernetes_secret.dockerio_registry.metadata[0].name
    }
  }

  depends_on = [
    kubernetes_namespace.voltdb,
    kubernetes_secret.dockerio_registry
  ]
}
```

**Key principles:**
- Use modular, resource-specific filenames instead of generic names
- One file per major resource type or logical grouping
- Keep sensitive values in terraform.tfvars (gitignored)
- Export values needed by helmfile via outputs.tf
- Pass environment variables to helmfile via helmfile.tf

#### Docker Pull Secret
In namespace.tf create a secret, with a default name `dockerio-registry`. Make sure variables contains placeholders for email, user and password that can be overridden in terraform.tfvars file.
User can choose different name for the secret. The secret name should be added to a output.tf file.
The downstream helmfile config should use the same secret name.

**Example in namespace.tf:**
```terraform
resource "kubernetes_secret" "dockerio_registry" {
  metadata {
    name      = "dockerio-registry"
    namespace = kubernetes_namespace.voltdb.metadata[0].name
  }

  type = "kubernetes.io/dockerconfigjson"

  data = {
    ".dockerconfigjson" = jsonencode({
      auths = {
        "https://index.docker.io/v1/" = {
          username = var.docker_username
          password = var.docker_password
          email    = var.docker_email
          auth     = base64encode("${var.docker_username}:${var.docker_password}")
        }
      }
    })
  }

  depends_on = [kubernetes_namespace.voltdb]
}
```

**Important:** The secret must be created after the namespace and before helmfile execution.

### Step 6: Verify the deployment
For the first time run `terraform init` command. Then run `terraform apply` command.
Verify that the deployment is working as expected.
Wait for specific pod to be ready - `kubectl wait --for=condition=ready pod -l release=<release_name> -n ${namespace} --timeout=300s;` or call `kubectl get pods -n <namespace>` and check that all pods are running without any errors. 

#### Troubleshooting
If expected pods are missing, crashing or have exited with error, check pods logs or deployment events with `kubectl describe` command.
Once event or logs are checked, propose a correction to the helmfile release configuration or to the terraform resources.
Re-run `terraform apply` command and check that all pods are running without any errors.
