---
name: gateway-conformance-runner
description: Use this skill when you need to run the Gateway API conformance test suite for the multiway project. It handles building and deploying the gateway controller to a shared DigitalOcean cluster, running the official conformance tests in an isolated namespace, and analyzing the results. Use this skill whenever the user mentions conformance tests, test suite, or wants to verify Gateway API compliance.
hooks:
  pre: .claude/skills/gateway-conformance-runner/cluster-up.sh
  post: .claude/skills/gateway-conformance-runner/cluster-down.sh
---

You are responsible for running the Gateway API conformance test suite for the multiway project and reporting the results.

# Cluster and Namespace Model

The conformance suite runs on a **shared, long-lived** DigitalOcean cluster called `mw-conformance`. Each test run gets its own **isolated namespace** so that multiple agents or branches can run conformance tests in parallel without conflicting.

## Automatic Lifecycle via Hooks

- **Startup Hook** (`cluster-up.sh`): Runs before the skill starts. Verifies the shared cluster is accessible (creating it automatically if it doesn't exist) and creates a fresh namespace derived from the current git branch (e.g., branch `robbie/multi-1101` creates namespace `multi-1101`).
- **Shutdown Hook** (`cluster-down.sh`): Runs after the skill completes. Deletes the namespace and all its resources. By default the shared cluster is preserved; use `--destroy-cluster` to also tear it down and clean up kubeconfig.

## Namespace Naming

The namespace defaults to the last path component of the current git branch, lowercased. For example:
- Branch `robbie/multi-1101` → namespace `multi-1101`
- Branch `feature/my-test` → namespace `my-test`
- Branch `main` → namespace `main`

You can override the namespace with `--namespace` or the `CONFORMANCE_NAMESPACE` environment variable.

You can also run the hook scripts manually:

```bash
# Set up namespace for current branch
.claude/skills/gateway-conformance-runner/cluster-up.sh

# Use a specific namespace (e.g., for a Linear ticket)
.claude/skills/gateway-conformance-runner/cluster-up.sh --namespace multi-1101

# Tear down the namespace when done
.claude/skills/gateway-conformance-runner/cluster-down.sh

# Tear down a specific namespace
.claude/skills/gateway-conformance-runner/cluster-down.sh --namespace multi-1101

# Tear down namespace AND destroy the cluster (saves DigitalOcean costs)
.claude/skills/gateway-conformance-runner/cluster-down.sh --destroy-cluster
```

# Running Conformance Tests

Use the automated script located at `.claude/skills/gateway-conformance-runner/run-conformance.sh` to run the conformance tests.

**Note**: The namespace must exist before running this script. If using the skill hooks, the namespace is created automatically. If running manually, use `cluster-up.sh` first.

## Basic Usage

```bash
.claude/skills/gateway-conformance-runner/run-conformance.sh
```

## Script Options

| Option | Description |
|--------|-------------|
| `--skip-build` | Skip Rust compilation and Docker image building (use when images already exist) |
| `--skip-deploy` | Skip gateway controller deployment (use when controller is already running) |
| `--cluster-name NAME` | Specify cluster name (default: `mw-conformance`) |
| `--namespace NAME` | Kubernetes namespace for deployment (default: `multiway-system`) |
| `--dry-run` | Print commands without executing them |
| `--help` | Show help message |

## What the Script Does

The script automates the conformance testing workflow:

1. **Prerequisites Check**: Verifies Docker and kubectl are available, cluster is accessible
2. **Environment Verification**: Checks that `GATEWAY_CONFORMANCE_SUITE` and `DOCKER_REGISTRY` environment variables are set
3. **Build & Push**: Compiles the Rust project, builds Docker images, and pushes them to the container registry
4. **Deploy**: Cleans up any existing deployments in the namespace, installs Gateway API CRDs, deploys the gateway controller, and waits for pods to be ready
5. **Test Execution**: Runs the conformance tests from the local Gateway API repository

## Prerequisites

Before running the skill, ensure:

1. **Docker** is installed and running
2. **kubectl** is installed
3. **doctl** (DigitalOcean CLI) is installed and authenticated
4. **Gateway API repository** is cloned locally
5. **`mw-conformance` cluster** on DigitalOcean — created automatically by `cluster-up.sh` if it doesn't exist
6. **`GATEWAY_CONFORMANCE_SUITE`** environment variable is set in `.envrc.local`:
   ```bash
   export GATEWAY_CONFORMANCE_SUITE=/path/to/gateway-api
   ```
7. **`DOCKER_REGISTRY`** environment variable is set in `.envrc.local`:
   ```bash
   export DOCKER_REGISTRY=ghcr.io/myorg
   ```

## Example Commands

```bash
# Full test run (build, deploy, test) in default namespace
.claude/skills/gateway-conformance-runner/run-conformance.sh

# Run in a specific namespace (e.g., for a Linear ticket)
.claude/skills/gateway-conformance-runner/run-conformance.sh --namespace multi-1101

# Quick re-test (skip build, images already exist)
.claude/skills/gateway-conformance-runner/run-conformance.sh --skip-build --namespace multi-1101

# Just run tests (controller already deployed)
.claude/skills/gateway-conformance-runner/run-conformance.sh --skip-build --skip-deploy --namespace multi-1101

# Preview what would be executed
.claude/skills/gateway-conformance-runner/run-conformance.sh --dry-run
```

# Reporting Results

When reporting test results to the user:

- Provide a summary of tests passed vs failed
- List any specific test cases that failed with their error messages
- Include relevant log excerpts for debugging
- Do not attempt to debug or fix the errors; only report them

Your job is to run the conformance tests and report the results. Do not debug error messages or suggest fixes.

# Error Handling & Troubleshooting

If the script fails, consider these areas:

1. **Cluster Access**: The `mw-conformance` cluster is created automatically by `cluster-up.sh` if it doesn't exist. If auto-creation fails, check DigitalOcean authentication (`doctl auth init`).
2. **Build Pipeline**: Build Docker images for the gateway controller and ensure they're properly pushed to the container registry
3. **Deployment**: Deploy the gateway controller and all necessary CRDs following the project's established patterns
4. **Test Execution**: Run the official Gateway API conformance test suite with appropriate configuration
5. **Results Analysis**: Retrieve and interpret test logs, identifying failures and their root causes

When encountering issues:
- If `GATEWAY_CONFORMANCE_SUITE` is not set, guide the user to configure it in `.envrc.local`
- If `DOCKER_REGISTRY` is not set, guide the user to configure it in `.envrc.local`
- If kubectl context is wrong, run `doctl kubernetes cluster kubeconfig save mw-conformance`
- If the shared cluster doesn't exist, `cluster-up.sh` creates it automatically. If auto-creation fails, check DigitalOcean auth.
- If image push fails, verify registry authentication (e.g., `docker login ghcr.io`)
- If tests fail, analyze logs for specific failure points but do not suggest fixes
- If deployment fails, check resource definitions and cluster state

**Best Practices**:

1. Always verify kubectl context before running tests to avoid running against production clusters
2. Use namespace isolation to avoid state pollution between test runs
3. Verify all prerequisites (Docker, doctl, kubectl, Go) are installed and functioning
4. Verify that the Rust project will compile before building Docker images: `cargo check`
5. Check that the gateway controller is fully deployed before running tests
6. The shutdown hook will delete the namespace automatically; if running manually, use `cluster-down.sh`

**Available Docker Build Commands**:
The project provides several cargo make tasks for building Docker images:
- `cargo make docker-build-all` - Build both control plane and data plane for current platform
- `cargo make docker-build-controlplane` - Build only control plane
- `cargo make docker-build-dataplane` - Build only data plane
- `cargo make docker-build-all-cross` - Build for both amd64 and arm64 (multi-platform)
- `cargo make docker-build-all-push` - Build and push multi-platform images (requires DOCKER_REGISTRY env var)

**Namespace Lifecycle Commands**:
- `cluster-up.sh` - Verify cluster access (auto-create if needed) and create namespace
- `cluster-down.sh` - Delete namespace (cluster is preserved)
- `cluster-down.sh --destroy-cluster` - Delete namespace AND destroy the DigitalOcean cluster + clean up kubeconfig
- `cluster-up.sh --namespace <name>` - Create a specific namespace
- `cluster-down.sh --namespace <name>` - Delete a specific namespace
