---
name: eve-pipelines-workflows
description: Define and run Eve pipelines and workflows via manifest and CLI. Use when wiring build, release, deploy flows or invoking workflow jobs.
---

# Eve Pipelines and Workflows

Use these patterns to automate build and deploy actions and invoke workflow jobs.

## Pipelines (v2 steps)

- Define pipelines under `pipelines` in `.eve/manifest.yaml`.
- Steps can be `action`, `script`, or `agent`.
- Use `depends_on` to control ordering.
- Built-in actions include `build`, `release`, `deploy`, `run`, `job`, `create-pr`.
- Run manually:
  - `eve pipeline list`
  - `eve pipeline show <project> <name>`
  - `eve pipeline run <name> --ref <sha> --env <env> --repo-dir ./my-app`
- Trigger blocks exist in the manifest; GitHub and Slack webhooks can create pipeline runs.

### Built-in Actions

#### `build` action

Build actions create BuildSpec and BuildRun records that are tracked and observable:

- Creates BuildSpec (defines what to build) and BuildRun (execution record) in the database
- Outputs include `build_id` and `image_digests` map (service name to SHA256 digest)
- These outputs automatically flow to dependent steps (release uses build_id)
- Inspect builds independently: `eve build show`, `eve build diagnose`, `eve build runs`, `eve build logs`

### Agent steps

Use `agent` steps when a pipeline stage should run an AI agent job:

```yaml
pipelines:
  remediation:
    steps:
      - name: analyze
        agent:
          prompt: "Analyze the failure and propose a fix"
```

#### Canonical pipeline flow

Every deploy pipeline should follow this pattern:

```yaml
pipelines:
  deploy:
    steps:
      - name: build
        action:
          type: build
          # Creates BuildSpec + BuildRun, outputs build_id + image_digests
      - name: release
        depends_on: [build]
        action:
          type: release
          # References build_id, derives digests from BuildArtifacts
      - name: deploy
        depends_on: [release]
        action:
          type: deploy
          env_name: staging
          # Uses digest-based image refs for immutable deploys
```

#### Promotion workflow

Build once in test, then promote the same build artifacts to staging/production:

- The build step creates a BuildRun with artifacts (image digests)
- Releases carry the build_id forward, ensuring identical images across environments
- This pattern guarantees you deploy exactly what you tested

Track pipeline execution:

```bash
eve job list --phase active
eve job follow <job-id>
eve job result <job-id>
```

### Pipeline Logs & Streaming

Monitor pipeline runs in real time:

```bash
# Snapshot logs for a run
eve pipeline logs <pipeline> <run-id>

# Real-time SSE streaming
eve pipeline logs <pipeline> <run-id> --follow

# Stream specific step
eve pipeline logs <pipeline> <run-id> --follow --step <name>
```

Failed steps include failure hints and link to build diagnostics when applicable.

## Environment Deploy as Pipeline Alias

When an environment has a `pipeline` configured in the manifest, `eve env deploy <env> --ref <sha>` automatically triggers that pipeline instead of doing a direct deploy.

### Basic usage

```bash
# Triggers the configured pipeline for test environment
eve env deploy test --ref 0123456789abcdef0123456789abcdef01234567

# Pass inputs to the pipeline
eve env deploy staging --ref 0123456789abcdef0123456789abcdef01234567 --inputs '{"release_id":"rel_xxx"}'

# Bypass pipeline and do direct deploy
eve env deploy staging --ref 0123456789abcdef0123456789abcdef01234567 --direct
```

### Promotion flow example

```bash
# 1. Build and deploy to test environment
eve env deploy test --ref 0123456789abcdef0123456789abcdef01234567

# 2. Get release info from the test build
eve release resolve v1.2.3
# Output: rel_xxx

# 3. Promote to staging using the release_id
eve env deploy staging --ref 0123456789abcdef0123456789abcdef01234567 --inputs '{"release_id":"rel_xxx"}'
```

### Key behaviors

- If `environments.<env>.pipeline` is set, `eve env deploy <env>` triggers that pipeline
- Use `--direct` flag to bypass the pipeline and perform a direct deploy
- Use `--inputs '{"key":"value"}'` to pass inputs to the pipeline run
- Default inputs can be configured via `environments.<env>.pipeline_inputs` in the manifest
- The `--ref` flag specifies which git SHA to deploy (40-character SHA or ref resolved via `--repo-dir`)
- Environment variables and secrets are interpolated as usual

This pattern enables promotion workflows where you build once in a lower environment and promote the same artifact through higher environments.

## Workflows

- Define workflows under `workflows` in the manifest.
- `db_access` is honored when present (`read_only`, `read_write`).
- Invoke manually:
  - `eve workflow list`
  - `eve workflow show <project> <name>`
  - `eve workflow run <project> <name> --input '{"k":"v"}'` (fire-and-forget)
  - `eve workflow invoke <project> <name> --input '{"k":"v"}'` (wait for result)
  - `eve workflow logs <job-id>`
- Invocation creates a job; track it with normal job commands.

### Workflow Hints

Control gating, timeouts, and harness preferences via `hints`:

```yaml
workflows:
  remediate:
    hints:
      gates: ["remediate:proj_abc123:staging"]
```
