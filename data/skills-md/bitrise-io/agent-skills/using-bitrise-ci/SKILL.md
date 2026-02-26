---
name: using-bitrise-ci
description: |
    Works with Bitrise CI. **ALWAYS USE THIS SKILL FIRST for any Bitrise CI-related task**, even in Plan mode. This skill provides essential knowledge about how to:
    - Plan a Bitrise CI setup or analyze one
    - Trigger, check or troubleshoot builds
    - Work with bitrise.yml files:
      - Design pipelines, workflows, step bundles or step configurations
      - Fix duplication or optimize workflow structure
      - Validate or explain Bitrise configurations
    - Manage workspaces, projects, apps, groups, or roles
    - Work with Bitrise CLI, API, or MCP tools

---

# Using Bitrise CI

## Contents
- Tools (Authentication, MCP, API, CLI)
- Core concepts
- Creating projects
- Working with bitrise.yml (Structure, Components)
- Troubleshooting builds

## Automated access

### Authentication

An access token is required to interact with Bitrise in automated ways (API, MCP etc.). Users can create a [personal](https://docs.bitrise.io/en/bitrise-platform/accounts/personal-access-tokens.html) or [workspace](https://docs.bitrise.io/en/bitrise-platform/workspaces/workspace-api-token.html#creating-a-workspace-api-token) access token. It should be stored securely.

### MCP server

The Bitrise MCP server is available online at https://github.com/bitrise-io/bitrise-mcp, or it can be run locally. It requires authentication with a token using the `Authorization: Bearer {token}` header. **When the MCP server is available, prefer it to the API or other tools.**

### API

The Bitrise REST API allows managing various Bitrise resources. The detailed reference is available [here](https://docs.bitrise.io/en/bitrise-ci/api/api-reference.html). The API requires authentication with a PAT with the `Authorization: {PAT}` header (without `Bearer`).

### CLI

Bitrise CLI is useful when working on a local environment. It doesn't interact with Bitrise resources, but helps with editing and validating `bitrise.yml`, and allows running workflows locally. It supports Mac and Linux.

To install, use `brew install bitrise` or check the [Releases page](https://github.com/bitrise-io/bitrise/releases) for other options.

Local runs expect `bitrise.yml` at the root of the working directory, with an optional `.bitrise.secrets.yml` containing sensitive inputs.

Common commands:

```bash
# Output the list of available commands
bitrise help

# Start local workflow editor UI
bitrise :workflow-editor

# Validate bitrise.yml
bitrise validate -c {config_path}

# List available workflows
bitrise workflows

# Run a workflow locally
bitrise run {workflow_id}
```

## Core concepts

**Workspaces** are the top-level units of organizing projects and their members.

A **project** is a container for the DevOps process. Projects can contain CI configuration (also called *apps* by some tools) to run builds based on a git repository.

**Steps** are individual build tasks that can have inputs and outputs to allow configuration and interacting with other steps. Steps can be found in the [Step Library](https://bitrise.io/integrations).

**Step bundles** are reusable collections of steps that can be included in multiple workflows to reduce duplication. 

**Workflows** are sequences of steps executed in order on a runner machine. Triggering a workflow starts a **build**, which produces a log, and optionally downloadable files (**artifacts**) and/or test results.

Builds run on a virtual machine for a **stack** (a combination of specific versions of an OS and additional software tools), on the specified **machine type** that describes the hardware resources requested. Available machine types depend on the selected stack. Use the `bitrise:list_available_stacks` tool or the `/available-stacks` API endpoint to get the options.

**Pipelines** allow creating complex processes from workflows with dependencies, parallel or sequential execution, sharding and sharing files.

**Environment variables** (envs for short) are configuration variables that can be defined on various levels and are passed to components as inputs. See [this page](https://docs.bitrise.io/en/bitrise-ci/references/available-environment-variables.html) for built-in envs available during builds.

**Secrets** are envs with protected values: they are stored encrypted, and are redacted in build logs.

These components are configured via the `bitrise.yml` file stored in the git repository or the Bitrise website.

## Creating projects

### Prerequisites

The source needs to be available as a git repository online. Repository access can be configured via [service users](https://docs.bitrise.io/en/bitrise-platform/integrations/the-service-credential-user.html) or a GitHub App. The user needs to connect with a provider via the UI first.

### Workflow

Make sure to surface any errors that occur during the process, don't leave the user with the impression that everything went OK, as critical functionality might be broken.

Use the following checklist:

- [ ] Determine the source repository
- [ ] Determine the workspace to add the project
- [ ] Select a default branch and verify that it exists in the remote repository.
- [ ] Register the app
- [ ] If the repository is private, register SSH keys
- [ ] Finish the app setup
- [ ] Update bitrise.yml. Verify that it is valid first.

**Register the app** using the `bitrise:register_app` tool or the `/apps/register` API endpoint. Unless instructed otherwise, create the project as private.

**Registering SSH keys** can be done via the `bitrise:register_ssh_key` tool or the `/apps/{app-slug}/register-ssh-key` API endpoint. Use the `app_slug` received from the previous step.

**Finish the app setup** with the `bitrise:finish_bitrise_app` tool or the `/apps/{app-slug}/finish` API endpoint. Specify a project type (default is `other`) and a stack to run builds on.

**Updating bitrise.yml**: Upload the contents of bitrise.yml if it is stored on Bitrise (This is the default for newly created apps, `/apps/{app-slug}/bitrise.yml/config` API request can be used to check for existing apps). Otherwise this step can be skipped as bitrise.yml is version controlled in the source repo.

Detailed documentation is available [here](https://docs.bitrise.io/en/bitrise-ci/api/adding-and-managing-apps.html).

### Adding a project interactively from CLI

If the user prefers so, the [bitrise-add-new-project](https://docs.bitrise.io/en/bitrise-ci/bitrise-cli/adding-a-new-project-from-a-cli.html) tool can be used. This requires a Bitrise account and a checked out git repository.

## Working with bitrise.yml

By default, bitrise.yml is stored on Bitrise servers and not read from the source repository. It is possible to switch to storing it in the repository, allowing version control, reviews etc. This can be done via the `/apps/{app-slug}/bitrise.yml/config` API endpoint.

### Best Practices

- Always plan first: design the high-level process via workflows, then break them down into steps.
- Use clear, descriptive names for pipelines, workflows, step bundles and other resources.
- Use Secret env vars for API keys, tokens, passwords, certificate passphrases. Use regular env vars for app names, bundle IDs, version numbers, feature flags.
- Store secrets in Bitrise web UI for cloud builds
- NEVER commit `.bitrise.secrets.yml`.

### Structure

See [Schemastore](https://github.com/SchemaStore/schemastore/blob/master/src/schemas/json/bitrise.json) for the JSON schema or [this page](https://docs.bitrise.io/en/bitrise-ci/references/configuration-yaml-reference.html) a complete reference.

- `format_version` is a required field describing the configuration schema version (use `"25"` for latest features)
- `default_step_lib_source` is also required, it describes where steps should be loaded from unless specified otherwise. Use https://github.com/bitrise-io/bitrise-steplib.git as value.
- `step_bundles`, `workflows` and `pipelines` list the entities described above (formatted as a map with ID as key)
- `app` can be used to define app-level envs:
  ```yaml
  app:
    envs:
      - PROJECT_NAME: MyApp
      - BUNDLE_ID: com.example.myapp
      - VERSION: 1.0.0
  ```
- `meta` block is required for running builds on Bitrise:
  ```yaml
  meta:
    bitrise.io:
      stack: linux-docker-android-22.04
  ```

### Building Workflows

Workflows contain a list of steps with optional configuration and conditions.

- The most common sequence is `get sources` -> `build` -> `test` -> `publish or deploy`.
- To get the sources from a repository, start a workflow with the `activate-ssh-key` and `git-clone` steps.
- Test results are automatically reported from certain built-in steps. For other tools, the `custom-test-results-export` is needed to convert the results, and `deploy-to-bitrise-io` to upload them to Bitrise for reporting. Details [here](https://docs.bitrise.io/en/bitrise-ci/testing/deploying-and-viewing-test-results.html).
- Dependencies can be cached between builds for better performance. Popular package managers have dedicated caching steps, others require manual configuration. Details [here](https://docs.bitrise.io/en/bitrise-ci/dependencies-and-caching/dependencies-and-caching-overview.html).

Example:
```yaml
format_version: "25"
meta:
  bitrise.io:
    stack: linux-docker-android-22.04
workflows:
  ci:
    steps:
    - activate-ssh-key@4:
        run_if: '{{getenv "SSH_RSA_PRIVATE_KEY" | ne ""}}'
    - git-clone@8: {}
    - restore-cache@2:
        inputs:
        - key: cache-key-{{ .Branch }}
    - android-unit-test@1:
        inputs:
        - project_location: $PROJECT_LOCATION
        - variant: $VARIANT
    - android-build-for-ui-testing@0:
        inputs:
        - variant: $VARIANT
        - module: $MODULE
    - virtual-device-testing-for-android@1:
        inputs:
        - test_type: instrumentation
    - android-lint@0:
        inputs:
        - variant: "$VARIANT"
    - android-build@1:
        inputs:
        - project_location: "$PROJECT_LOCATION"
        - module: "$MODULE"
        - variant: "$VARIANT"
    - deploy-to-bitrise-io@2: {}
    - slack@3:
        inputs:
        - channel: "#build-notifications"
        - webhook_url: "$SLACK_WEBHOOK"
    - save-cache@1:
        inputs:
        - key: cache-key-{{ .Branch }}
    triggers:
      push:
      - branch: '*'
      pull_request:
      - target_branch: 'main'
      - comment: 
          regex: '.*trigger (b|B)itrise.*'
```

#### Using steps

- Prefer official steps to other sources. When no dedicated step is available for an action, use `script`:
  ```yaml
  - script@1:
      title: Print build info
      inputs:
      - content: |
          echo "Building branch: $BITRISE_GIT_BRANCH"
  ```
- Use the `bitrise:step_search` tool or the `/search-steps` endpoint to find steps.
- When specifying steps, lock to the major version (e.g. `git-clone@8`), this guards against breaking changes but allows bug fixes. Use the step search tools to verify.
- Use the `bitrise:step_inputs` tool or the `/step-inputs` endpoint to get data about the step inputs.

#### Conditional Step Execution

Use `run_if` to control Step execution based on conditions:

```yaml
- slack@3:
    run_if: .IsBuildFailed
    inputs:
      - webhook_url: $SLACK_WEBHOOK_URL
      - text: "Build failed on ${BITRISE_GIT_BRANCH}"
```

Available expressions: `.IsBuildFailed`, `.IsCI`, `.IsPR`, `{{getenv "VAR" | ne ""}}`

#### Step bundles

When the same sequence of steps appears in multiple workflows, extract them into a step bundle to optimize the workflows. Step bundles can be referenced with the `bundle::` prefix, and can be configured with inputs/outputs like steps. It is possible to nest step bundles.

Example:

```yaml
step_bundles:
  install_deps:    
    inputs:
    - cache_key: "npm-cache-{{ checksum "package-lock.json" }}"
    - npm_command: install
    steps:    
    - restore-cache@2:
        inputs:
        - key: $cache_key
    - npm@1:
        inputs: 
        - command: $npm_command
workflows:
  ci:
    steps:
    - git-clone@8: {}
    - bundle::install_deps:        
        inputs:
        - cache_key: "npm-cache"
    - deploy-to-bitrise-io@2: {} 
```

**ALWAYS prefer step bundles to the obsolete `before_run` or `after_run` constructs when creating new workflows, leave them in existing ones.**

### Building pipelines

Design multi-workflow processes with dependencies, parallelism, sharding and artifact sharing. See [pipelines.md](pipelines.md) for full details.

**ALWAYS prefer using explicit dependencies with `depends_on` when creating new pipelines. Use stages only when editing an existing pipeline that already contains them.**

### Triggers

Workflows and pipelines can specify conditions for events from the source repository that should start builds.

[Triggers](https://docs.bitrise.io/en/bitrise-ci/run-and-analyze-builds/build-triggers/yaml-syntax-for-build-triggers.html) can be set on each pipeline or workflow. Multiple triggers can be added, and each can specify multiple conditions. All pipelines/workflows that have a matching trigger item will be started.

Examples:
```yaml
workflows:
  workflow-tests:
    triggers:
      push:
      # Exact match
      - branch: "release" 
pipelines:
  pipeline-build:
    workflows: {}
    triggers:
      push: 
      # Using a wildcard
      - branch: "*"
      # Multiple conditions
      - branch: release
        changed_files: path/to/library-a/.*
      tag:
      # Regex
      - name:
          regex: '^\d\.\d\.\d$'
```

#### Legacy format

The top-level `trigger_map` tag contains an ordered list of items. For an incoming event, the **first** matching item will start a build with the specified pipeline/workflow.
**ALWAYS prefer the new format when creating a new bitrise.yml file, only use `trigger_map` when already present.**

### Modular YAML

On enterprise plans, it is possible to split `bitrise.yml` into multiple files to reflect organizational or code structure, and to reduce conflicts. See details [here](https://docs.bitrise.io/en/bitrise-ci/configure-builds/configuration-yaml/modular-yaml-configuration.html).

Example:

```yaml
format_version: "25"
include:
  - _workflows/shared.yml
  - _workflows/ios.yml
  - _workflows/android.yml
```

### Verifying results

Use this workflow:

1. Validate the YML file(s). For large files, use the CLI if installed, or the API by streaming the file into cURL.
  - `bitrise validate -c bitrise.yml`
  - `bitrise:validate_bitrise_yml` MCP tool
  - `/validate-bitrise-yml` API endpoint
2. If validation fails:
   - Review error messages carefully
   - Fix the issues
   - Run validation again
3. **Only proceed when validation passes**
4. Test locally if possible: `bitrise run {workflow_id}`

## Troubleshooting builds

1. Check the build logs.
2. Identify failing steps (there can be multiple) and find errors in their output.
3. Determine whether the failure was because of a problem with the configuration (invalid stack, incorrect order etc.) or the source (tests, linting etc.)
4. If it's a configuration issue: don't remove failing steps. Verify that the right step is used and fix its configuration. Ask clarifying questions if necessary. In general, do not edit or remove unrelated parts of the configuration.

## Useful Links

- Bitrise documentation: https://docs.bitrise.io/
- Step Library: https://github.com/bitrise-steplib Each step is a repository here.
- Bitrise CLI (GitHub): https://github.com/bitrise-io/bitrise
- bitrise.yml Reference: https://docs.bitrise.io/en/bitrise-ci/references/configuration-yaml-reference.html
- Stacks documentation: https://bitrise.io/stacks
