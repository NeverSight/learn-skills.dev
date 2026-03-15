---
name: workflows
description: Builds and deploys data processing and ML training pipelines using TrueFoundry Workflows (built on Flyte). Use when creating DAGs, orchestrating multi-step tasks, scheduling ETL pipelines, or running ML training workflows.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(tfy*) Bash(python*) Bash(pip*) Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# TrueFoundry Workflows

Create, configure, and deploy workflows on TrueFoundry. Workflows are built on [Flyte](https://flyte.org/), an open-source orchestration platform, and use Python decorators (`@task`, `@workflow`) to define structured sequences of tasks as directed acyclic graphs (DAGs).

Workflow **definition** uses Python SDK (`@task`/`@workflow` decorators). Workflow **deployment** uses `tfy deploy workflow` CLI command. Alternative: `tfy apply` with a YAML manifest. REST API fallback when CLI unavailable.

## When to Use

- User wants to create a data processing or ML training pipeline
- User says "create a workflow", "deploy a workflow", "run a pipeline"
- User wants to schedule recurring batch operations (cron workflows)
- User wants to orchestrate multi-step tasks: ETL, feature engineering, model training, batch inference
- User asks about Flyte tasks, map tasks, conditional tasks, or Spark tasks on TrueFoundry

## When NOT to Use

- User wants to deploy a web service or API -> prefer `deploy` skill; ask if the user wants another valid path
- User wants to deploy a one-off job (not a multi-step pipeline) -> prefer `deploy` skill; ask if the user wants another valid path with job type
- User wants to check running applications -> prefer `applications` skill; ask if the user wants another valid path
- User wants to monitor job runs -> prefer `jobs` skill; ask if the user wants another valid path
- User wants to serve an ML model behind an endpoint -> prefer `llm-deploy` or `deploy`; ask which path they want

</objective>

<context>

## Prerequisites

**Always verify before creating a workflow:**

1. **Credentials** — `TFY_BASE_URL` and `TFY_API_KEY` must be set (env or `.env`)
2. **Workspace** — `TFY_WORKSPACE_FQN` required. **Never auto-pick. Ask the user if missing.**
3. **SDK** — Install the TrueFoundry SDK with workflow extras (required for defining tasks/workflows):
   ```bash
   pip install "truefoundry[workflow]"
   ```
4. **CLI login** — Authenticate the CLI (required for deployment):
   ```bash
   tfy login --host "$TFY_BASE_URL"
   ```
5. **Python** — Python 3.9+ required for workflow definition code
6. **Cluster setup** — The Flyte data plane must be installed on the target cluster. The control plane ships with TrueFoundry (no additional setup). If the user gets errors about Flyte not being available, they need to contact their platform admin to install the data plane components.

For credential check commands and .env setup, see `references/prerequisites.md`.

### CLI Detection

```bash
tfy --version
```

| CLI Output | Status | Action |
|-----------|--------|--------|
| `tfy version X.Y.Z` (>= 0.5.0) | Current | Use `tfy apply` for deployment as documented below. |
| `tfy version X.Y.Z` (0.3.x-0.4.x) | Outdated | Upgrade: install a pinned version (e.g. `pip install 'truefoundry==0.5.0'`). Core `tfy apply` should still work. |
| Command not found | Not installed | Install: `pip install 'truefoundry==0.5.0' && tfy login --host "$TFY_BASE_URL"` |
| CLI unavailable (no pip/Python) | Fallback | Use REST API via `tfy-api.sh`. See `references/cli-fallback.md`. |

## Core Concepts

- **Task** -- The smallest unit of execution. A Python function decorated with `@task`. Each task runs in its own container with configurable resources and dependencies.
- **Workflow** -- A composition of tasks arranged as a DAG using the `@workflow` decorator. Defines execution order and data flow between tasks.
- **Task Config** -- Specifies the container image, Python version, pip packages, and compute resources for each task.
- **Execution Config** -- Controls scheduling (cron), launch plans, and runtime parameters.

**Critical rule:** The workflow function must contain **only task calls and control flow**. Do not put business logic directly in the workflow function -- all computation must live inside `@task` functions.

</context>

<instructions>

## Basic Workflow Example

```python
from truefoundry.workflow import (
    PythonTaskConfig,
    TaskPythonBuild,
    conditional,
    task,
    workflow,
)
from truefoundry.deploy import Resources

# Define task configuration
cpu_task_config = PythonTaskConfig(
    image=TaskPythonBuild(
        python_version="3.9",
        pip_packages=["truefoundry[workflow]"],
    ),
    resources=Resources(cpu_request=0.5, memory_request=500),
)

@task(task_config=cpu_task_config)
def fetch_data(source: str) -> dict:
    """Fetch and return raw data."""
    data = {"records": 1000, "source": source}
    return data

@task(task_config=cpu_task_config)
def process_data(raw_data: dict) -> dict:
    """Clean and transform the data."""
    processed = {
        "records": raw_data["records"],
        "source": raw_data["source"],
        "status": "processed",
    }
    return processed

@task(task_config=cpu_task_config)
def train_model(data: dict) -> str:
    """Train a model on processed data."""
    return f"model_trained_on_{data['records']}_records"

@workflow
def ml_pipeline(source: str = "default") -> str:
    """End-to-end ML pipeline."""
    raw = fetch_data(source=source)
    processed = process_data(raw_data=raw)
    result = train_model(data=processed)
    return result
```

**Note:** Workflows REQUIRE the Python SDK for definition -- this is the exception to the CLI-first approach. Only the deploy step uses CLI.

## Task Configuration

### PythonTaskConfig

Every task needs a `PythonTaskConfig` that defines its execution environment:

```python
from truefoundry.workflow import PythonTaskConfig, TaskPythonBuild
from truefoundry.deploy import Resources

# CPU task
cpu_task_config = PythonTaskConfig(
    image=TaskPythonBuild(
        python_version="3.9",
        pip_packages=[
            "truefoundry[workflow]",
            "pandas==2.1.0",
            "numpy",
        ],
        # Or use a requirements file:
        # requirements_path="requirements.txt",
    ),
    resources=Resources(
        cpu_request=0.5,
        memory_request=500,
    ),
)

# GPU task (for training or inference steps)
gpu_task_config = PythonTaskConfig(
    image=TaskPythonBuild(
        python_version="3.9",
        pip_packages=[
            "truefoundry[workflow]",
            "torch",
            "transformers",
        ],
    ),
    resources=Resources(
        cpu_request=2.0,
        cpu_limit=4.0,
        memory_request=8192,
        memory_limit=16384,
        devices=[
            GPUDevice(name="T4", count=1),
        ],
    ),
)
```

**Key points:**
- `truefoundry[workflow]` must always be in `pip_packages` (or in the requirements file)
- `pip_packages` takes a list of pip-installable package specifiers
- `requirements_path` can point to a requirements file instead of inline packages
- Resource `memory_request` and `memory_limit` are in MB
- Different tasks can have different configs (e.g., lightweight preprocessing vs GPU-heavy training)

### Container Tasks

For tasks that need a pre-built Docker image instead of a Python build:

```python
from truefoundry.workflow import task, ContainerTask

container_task = ContainerTask(
    name="my-container-task",
    image="my-registry/my-image:latest",
    command=["python", "run.py"],
    resources=Resources(
        cpu_request=1.0,
        memory_request=2048,
    ),
)
```

Use container tasks when:
- You need a custom base image with system-level dependencies
- The task runs non-Python code
- You have a pre-built image with all dependencies baked in

> **Security:** Verify container image sources before using them in workflow tasks. Pin image tags to specific versions — do not use `:latest`. For `pip_packages`, pin package versions to avoid supply-chain risks from unvetted upstream changes.

## Cron Workflows (Scheduling)

Schedule workflows to run at fixed intervals using cron syntax. The schedule is always in **UTC timezone**.

```python
from truefoundry.workflow import workflow, ExecutionConfig

@workflow(
    execution_configs=[
        ExecutionConfig(schedule="0 6 * * *"),  # Every day at 6:00 AM UTC
    ]
)
def daily_etl_pipeline() -> str:
    raw = fetch_data(source="production_db")
    processed = process_data(raw_data=raw)
    return processed["status"]
```

### Common Cron Patterns

| Schedule | Cron Expression | Description |
|----------|----------------|-------------|
| Every 10 minutes | `*/10 * * * *` | Frequent data sync |
| Every hour | `0 * * * *` | Hourly aggregation |
| Daily at midnight UTC | `0 0 * * *` | Nightly batch jobs |
| Daily at 6 AM UTC | `0 6 * * *` | Morning data refresh |
| Every Monday at 9 AM UTC | `0 9 * * 1` | Weekly reports |
| First of month at midnight | `0 0 1 * *` | Monthly processing |

**Cron format:** `minute hour day-of-month month day-of-week`

## Advanced Patterns

For map tasks (parallel execution), conditional tasks (branching logic), and Spark tasks (large-scale data processing), see [references/workflow-advanced-patterns.md](references/workflow-advanced-patterns.md).

## Deploying Workflows

After the user writes their workflow code (Python file with `@task` and `@workflow` decorators), deploy using `tfy deploy workflow`.

### Approach A: Via `tfy deploy workflow` (CLI -- Primary)

```bash
tfy deploy workflow \
  --name my-ml-pipeline \
  --file workflow.py \
  --workspace_fqn "$TFY_WORKSPACE_FQN"
```

**Important:** After deployment, the workflow must be triggered manually. The TrueFoundry UI shows a yellow banner indicating the workflow is deployed but not yet running. The user can trigger it from the dashboard or via a launch plan.

### Approach B: Via `tfy apply` (YAML Manifest -- Alternative)

**1. Generate the workflow deployment manifest:**

```yaml
# workflow-manifest.yaml
name: my-ml-pipeline
type: workflow
workflow_file: workflow.py
workspace_fqn: "YOUR_WORKSPACE_FQN"
```

**2. Preview:**

```bash
tfy apply -f workflow-manifest.yaml --dry-run --show-diff
```

**3. Apply:**

```bash
tfy apply -f workflow-manifest.yaml
```

### Approach C: Via Python SDK

```python
from truefoundry.workflow import WorkflowDeployment

deployment = WorkflowDeployment(
    name="my-ml-pipeline",
    workflow_file="workflow.py",
    workspace_fqn="your-workspace-fqn",
)
deployment.deploy()
```

### Deployment Checklist

Before deploying, confirm with the user:

- [ ] **Workflow name** -- a descriptive name for the workflow
- [ ] **Workspace** -- `TFY_WORKSPACE_FQN` is set (never auto-pick)
- [ ] **Task configs** -- each task has appropriate resources, Python version, and packages
- [ ] **Pip packages** -- `truefoundry[workflow]` is included in every task's packages
- [ ] **Schedule** -- if cron, confirm the cron expression and timezone (always UTC)
- [ ] **Workflow file** -- path to the Python file containing `@workflow` and `@task` definitions

**Post-deploy:** Remind the user that the workflow must be triggered manually after deployment. The TrueFoundry dashboard shows a yellow banner for newly deployed workflows that have not been triggered yet.

## Monitoring Workflow Runs

After deployment, monitor runs through:

1. **TrueFoundry Dashboard** -- Navigate to Workflows in the dashboard to see run history, task status, logs, and DAG visualization.
2. **Applications skill** -- Use the `applications` skill to list workflow applications:
   ```
   tfy_applications_list(filters={"application_type": "workflow"})
   ```
3. **Jobs skill** -- Use the `jobs` skill to inspect individual workflow run details and status.

### Run States

| State | Meaning |
|-------|---------|
| QUEUED | Run is waiting to be scheduled |
| RUNNING | Tasks are actively executing |
| SUCCEEDED | All tasks completed successfully |
| FAILED | One or more tasks failed |
| TIMED_OUT | Run exceeded its timeout |
| ABORTED | Run was manually cancelled |

</instructions>

<success_criteria>

- The user has a workflow file with properly decorated @task and @workflow functions
- The agent has confirmed that all @task functions include truefoundry[workflow] in their pip_packages
- The workflow was successfully deployed to the specified workspace using `tfy deploy workflow` (or `tfy apply` as alternative)
- The user can monitor workflow runs via the dashboard or `applications` skill
- The agent has set up a cron schedule if the user requested recurring execution

</success_criteria>

<references>

## Composability

- **Check credentials first**: Use `status` skill to verify TrueFoundry connection
- **Find workspace**: Use `workspaces` skill to list available workspaces
- **List workflows**: Use `applications` skill with `application_type: "workflow"`
- **Monitor runs**: Use `jobs` skill to check run status and history
- **View logs**: Use `logs` skill to inspect task-level logs
- **Manage secrets**: Use `secrets` skill to set up secret groups for workflow tasks that need API keys or credentials

</references>

<troubleshooting>

## Error Handling

### CLI Errors

```
tfy: command not found
Install the TrueFoundry CLI:
  pip install 'truefoundry==0.5.0'
  tfy login --host "$TFY_BASE_URL"
```

```
Manifest validation failed.
Check:
- YAML syntax is valid
- Required fields: name, type, workflow_file, workspace_fqn
- Workflow file path is correct and accessible
```

### SDK Not Installed
```
The truefoundry[workflow] package is required for defining tasks and workflows:
  pip install "truefoundry[workflow]"
```

### TFY_WORKSPACE_FQN Not Set
```
TFY_WORKSPACE_FQN is required. Get it from:
- TrueFoundry dashboard -> Workspaces
- Or use the `workspaces` skill to list available workspaces
Do not auto-pick a workspace.
```

### Flyte Data Plane Not Available
```
Flyte data plane is not installed on this cluster.
The control plane ships with TrueFoundry, but the data plane must be installed
on each cluster separately. Contact your platform admin to set up the Flyte
data plane components on the target cluster.
```

### Business Logic in Workflow Function
```
Error: Workflow function contains non-task code.
The @workflow function must only contain task calls and control flow.
Move all computation into @task-decorated functions.

Bad:
  @workflow
  def my_wf():
      data = pd.read_csv("file.csv")  # NOT allowed in workflow function
      return process(data)

Good:
  @workflow
  def my_wf():
      data = load_data()              # Call a @task instead
      return process(data)
```

### Missing truefoundry[workflow] in Task Packages
```
Each task's PythonTaskConfig must include "truefoundry[workflow]" in pip_packages.
Without it, the task container cannot communicate with the Flyte backend.

Fix: Add "truefoundry[workflow]" to the pip_packages list in every PythonTaskConfig.
```

### Task Resource Errors
```
Task failed due to resource limits (OOMKilled or CPU throttled).
Increase memory_limit or cpu_limit in the task's Resources config.
Check the task logs in the TrueFoundry dashboard for details.
```

### Cron Schedule Not Triggering
```
Cron schedules use UTC timezone. Verify your cron expression accounts for
UTC offset from your local timezone.
Use https://crontab.guru to validate your cron expression.
```

### REST API Fallback Errors

```
401 Unauthorized — Check TFY_API_KEY is valid
404 Not Found — Check TFY_BASE_URL and API endpoint path
422 Validation Error — Check manifest fields match expected schema
```

</troubleshooting>
