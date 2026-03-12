---
name: jobs
description: Deploys and monitors TrueFoundry batch jobs, scheduled cron jobs, and one-time tasks. Uses YAML manifests with `tfy apply`. Use when deploying jobs, scheduling cron tasks, checking job run status, or viewing execution history. For listing job applications, use `applications` skill.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(tfy*) Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Jobs

Deploy, schedule, and monitor TrueFoundry job runs. Two paths:

1. **CLI** (`tfy apply`) -- Write a YAML manifest and apply it. Works everywhere.
2. **REST API** (fallback) -- When CLI unavailable, use `tfy-api.sh`.

## When to Use

- User asks "deploy a job", "create a job", "run a batch task"
- User asks "schedule a job", "run a cron job"
- User asks "show job runs", "list runs for my job"
- User asks "is my job running", "job status"
- User wants to check a specific job run
- Debugging a failed job run

## When NOT to Use

- User wants to list job *applications* -> prefer `applications` skill; ask if the user wants another valid path with `application_type: "job"`

</objective>

<context>

## Prerequisites

**Always verify before deploying:**

1. **Credentials** -- `TFY_BASE_URL` and `TFY_API_KEY` must be set (env or `.env`)
2. **Workspace** -- `TFY_WORKSPACE_FQN` required. **Never auto-pick. Ask the user if missing.**
3. **CLI** -- Check if `tfy` CLI is available: `tfy --version`. If not, install a pinned version (`pip install 'truefoundry==0.5.0'`).

For credential check commands and .env setup, see `references/prerequisites.md`.

</context>

<instructions>

### Step 1: Analyze the Job

- What does the job do? (training, batch processing, data pipeline, maintenance)
- One-time or scheduled?
- Resource requirements (CPU/GPU/memory)
- Expected duration

> **Security requirements**
> - Never request or print raw secret values in chat.
> - For sensitive env vars (tokens/passwords/keys), require `tfy-secret://...` references instead of inline values.
> - For `build_source.type: git`, use trusted repositories and prefer immutable refs (commit SHA or pinned tag) over floating branches.

### Step 2: Generate YAML Manifest

Based on the job requirements, create a YAML manifest.

> **Security:** Always confirm container image sources and git repository URLs with the user before deploying. Do not pull untrusted container images or clone unverified git repositories. Pin image tags to specific versions — avoid `:latest` in production.

#### Option A: Pre-built Image

```yaml
name: my-batch-job
type: job
image:
  type: image
  image_uri: my-registry/my-image:v1.0.0  # pin to a specific version
  command: python train.py
resources:
  cpu_request: 2
  cpu_limit: 4
  memory_request: 4000
  memory_limit: 8000
  ephemeral_storage_request: 1000
  ephemeral_storage_limit: 2000
env:
  ENVIRONMENT: production
workspace_fqn: cluster-id:workspace-name
```

#### Option B: Git Repo + Dockerfile

```yaml
name: my-batch-job
type: job
image:
  type: build
  build_source:
    type: git
    repo_url: https://github.com/user/repo
    branch_name: main
    ref: 3f2a1c9b0d7e6f5a4b3c2d1e0f9876543210abcd
  build_spec:
    type: dockerfile
    dockerfile_path: Dockerfile
    build_context_path: "."
    command: python train.py
resources:
  cpu_request: 2
  cpu_limit: 4
  memory_request: 4000
  memory_limit: 8000
env:
  ENVIRONMENT: production
workspace_fqn: cluster-id:workspace-name
```

#### Option C: Git Repo + PythonBuild (No Dockerfile)

```yaml
name: my-batch-job
type: job
image:
  type: build
  build_source:
    type: git
    repo_url: https://github.com/user/repo
    branch_name: main
    ref: 3f2a1c9b0d7e6f5a4b3c2d1e0f9876543210abcd
  build_spec:
    type: tfy-python-buildpack
    command: python train.py
    python_version: "3.11"
    python_dependencies:
      type: pip
      requirements_path: requirements.txt
resources:
  cpu_request: 2
  cpu_limit: 4
  memory_request: 4000
  memory_limit: 8000
workspace_fqn: cluster-id:workspace-name
```

### Scheduled Jobs (Cron)

Add a `trigger` section for scheduled execution:

```yaml
name: nightly-retrain
type: job
trigger:
  type: cron
  schedule: "0 2 * * *"  # 2 AM daily
image:
  type: image
  image_uri: my-registry/my-image:v1.0.0
  command: python train.py
resources:
  cpu_request: 2
  cpu_limit: 4
  memory_request: 4000
  memory_limit: 8000
workspace_fqn: cluster-id:workspace-name
```

Cron format: `minute hour day_of_month month day_of_week`

Common schedules:
| Schedule | Cron | Description |
|----------|------|-------------|
| Every hour | `0 * * * *` | Top of every hour |
| Daily at 2 AM | `0 2 * * *` | Nightly jobs |
| Weekly Monday | `0 9 * * 1` | Weekly Monday 9 AM |
| Monthly 1st | `0 0 1 * *` | First of month midnight |

### Manual Trigger with Retries

```yaml
name: my-job
type: job
trigger:
  type: manual
  num_retries: 3
image:
  type: image
  image_uri: my-registry/my-image:v1.0.0
  command: python job.py
resources:
  cpu_request: 2
  cpu_limit: 4
  memory_request: 4000
  memory_limit: 8000
workspace_fqn: cluster-id:workspace-name
```

### Concurrency Policies

Three options for scheduled jobs when a run overlaps:
- **Forbid** (default): Skip new run if previous still running
- **Allow**: Run in parallel
- **Replace**: Kill current, start new

### Parameterized Jobs

```python
import argparse
# In your job script, use argparse for dynamic params
parser = argparse.ArgumentParser()
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--batch-size", type=int, default=32)
args = parser.parse_args()
```

Then set command: `python train.py --epochs 50 --batch-size 64`

### GPU Jobs

```yaml
name: gpu-training-job
type: job
image:
  type: image
  image_uri: my-registry/my-image:v1.0.0
  command: python train.py
resources:
  cpu_request: 4
  cpu_limit: 8
  memory_request: 16000
  memory_limit: 32000
  devices:
    - type: nvidia_gpu
      name: A10_24GB
      count: 1
workspace_fqn: cluster-id:workspace-name
```

### Job with Volume Mounts

```yaml
name: training-job
type: job
image:
  type: image
  image_uri: my-registry/my-image:v1.0.0
  command: python train.py
resources:
  cpu_request: 2
  cpu_limit: 4
  memory_request: 4000
  memory_limit: 8000
mounts:
  - mount_path: /data
    volume_fqn: your-volume-fqn
workspace_fqn: cluster-id:workspace-name
```

### Step 3: Write and Apply Manifest

Write the manifest to `tfy-manifest.yaml`:

```bash
# Preview
tfy apply -f tfy-manifest.yaml --dry-run --show-diff

# Apply after user confirms
tfy apply -f tfy-manifest.yaml
```

### Fallback: REST API

If `tfy` CLI is not available, convert the YAML manifest to JSON and deploy via REST API. See `references/cli-fallback.md` for the conversion process.

```bash
TFY_API_SH=~/.claude/skills/truefoundry-jobs/scripts/tfy-api.sh

$TFY_API_SH PUT /api/svc/v1/apps '{
  "manifest": { ... JSON version of the YAML manifest ... },
  "workspaceId": "WORKSPACE_ID"
}'
```

### Step 4: Trigger the Job

After deployment, trigger manually via API:

```bash
TFY_API_SH=~/.claude/skills/truefoundry-jobs/scripts/tfy-api.sh
$TFY_API_SH POST /api/svc/v1/jobs/JOB_ID/runs '{}'
```

## After Deploy -- Report Status

**CRITICAL: Always report the deployment status and job details to the user.**
Do this automatically after deploy, without asking an extra verification prompt.

### Check Job Status

```text
# Preferred (MCP tool call)
tfy_applications_list(filters={"workspace_fqn": "WORKSPACE_FQN", "application_name": "JOB_NAME"})
```

If MCP tool calls are unavailable, use API fallback:

```bash
TFY_API_SH=~/.claude/skills/truefoundry-jobs/scripts/tfy-api.sh

# Get job application details
$TFY_API_SH GET '/api/svc/v1/apps?workspaceFqn=WORKSPACE_FQN&applicationName=JOB_NAME'
```

### Report to User

**Always present this summary after deployment:**

```
Job deployed successfully!

Job: {job-name}
Workspace: {workspace-fqn}
Status: Suspended (deployed, ready to trigger)
Schedule: {cron expression if scheduled, or "Manual trigger"}

To trigger the job:
  - Dashboard: Click "Run Job" on the job page
  - API: POST /api/svc/v1/jobs/{JOB_ID}/runs

To monitor runs:
  - Use the job monitoring commands below
  - Or check the TrueFoundry dashboard
```

**For scheduled jobs**, also show when the next run will execute.
**For manually triggered jobs**, remind the user how to trigger them.

### .tfyignore

Create a `.tfyignore` file (follows `.gitignore` syntax) to exclude files from the Docker build:
```
.git/
__pycache__/
*.pyc
.env
data/
```

## List Job Runs

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### Via Tool Call

```
tfy_jobs_list_runs(job_id="job-id")
tfy_jobs_list_runs(job_id="job-id", job_run_name="run-name")  # get specific run
tfy_jobs_list_runs(job_id="job-id", filters={"sort_by": "createdAt"})
```

### Via Direct API

```bash
# Set the path to tfy-api.sh for your agent (example for Claude Code):
TFY_API_SH=~/.claude/skills/truefoundry-jobs/scripts/tfy-api.sh

# List runs for a job
$TFY_API_SH GET /api/svc/v1/jobs/JOB_ID/runs

# Get specific run
$TFY_API_SH GET /api/svc/v1/jobs/JOB_ID/runs/RUN_NAME

# With filters
$TFY_API_SH GET '/api/svc/v1/jobs/JOB_ID/runs?sortBy=createdAt&searchPrefix=my-run'
```

### Filter Parameters

| Parameter | API Key | Description |
|-----------|---------|-------------|
| `search_prefix` | `searchPrefix` | Filter runs by name prefix |
| `sort_by` | `sortBy` | Sort field (e.g. `createdAt`) |
| `triggered_by` | `triggeredBy` | Filter by who triggered |

### Presenting Job Runs

```
Job Runs for data-pipeline:
| Run Name       | Status    | Started            | Duration |
|----------------|-----------|--------------------|---------|
| run-20260210-1 | SUCCEEDED | 2026-02-10 09:00   | 5m 32s  |
| run-20260210-2 | FAILED    | 2026-02-10 10:00   | 1m 05s  |
| run-20260210-3 | RUNNING   | 2026-02-10 11:00   | --       |
```

</instructions>

<success_criteria>

## Success Criteria

- The job has been deployed to the target workspace and the user can see it in the TrueFoundry dashboard
- The user has been provided the job ID and knows how to trigger runs (manually or via cron schedule)
- The agent has reported the deployment status including job name, workspace, and trigger type
- Deployment status is verified automatically immediately after apply/deploy (no extra prompt)
- Job logs are accessible for monitoring via the `logs` skill or the dashboard
- For scheduled jobs, the cron expression is confirmed and the user knows when the next run will execute

</success_criteria>

<references>

## Composability

- **Schedule jobs**: Use cron trigger for automated scheduling
- **Monitor runs**: Use the job runs monitoring sections below
- **Find job first**: Use `applications` skill with `application_type: "job"` to get job app ID
- **Check logs**: Use `logs` skill with `job_run_name` to see run output

</references>

<troubleshooting>

## Error Handling

### Job Not Found
```
Job ID not found. Use applications skill to list jobs:
tfy_applications_list(filters={"application_type": "job"})
```

### No Runs Found
```
No runs found for this job. The job may not have been triggered yet.
```

### CLI Errors
- `tfy: command not found` -- Install with `pip install 'truefoundry==0.5.0'`
- `tfy apply` validation errors -- Check YAML syntax, ensure required fields (name, type, image, resources, workspace_fqn) are present

</troubleshooting>
</output>
