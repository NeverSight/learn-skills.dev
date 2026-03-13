---
name: modal-sandbox
description: >-
  Use this skill for Modal Sandbox lifecycle and interactive isolated
  execution. Trigger when the user needs to run untrusted or user-supplied code
  in a sandbox, keep a long-lived controller process alive, stream stdout from
  `exec()` calls, reattach to an existing sandbox, upload files at runtime,
  expose a tunneled HTTP or TCP service, or checkpoint and restore sandbox
  state. Do not use it for regular `@app.function` deployments, LLM serving, or
  training workflows.
license: MIT
---

# Modal Sandbox

## Quick Start

1. Verify prerequisites before doing any work.

```bash
modal --version
python -c "import modal,sys; print(modal.__version__); print(sys.executable)"
```

- Do not assume the default `python` or `python3` interpreter can import `modal` just because the `modal` CLI exists.
- Use the interpreter from the active Modal environment, project venv, or the environment behind the installed CLI.
- Do not look for a `modal sandbox` subcommand. Use `modal shell <sandbox_id>` for direct access and `modal container ...` only for generic container inspection.
- Wrap sandbox creation in `with modal.enable_output():` when you want local image-build and provisioning logs.
- Set `verbose=True` on `Sandbox.create(...)` when you want sandbox operation logs to show up in Modal logs and local output.

2. Create an App before creating a sandbox from outside Modal.

```python
import modal

app = modal.App.lookup("my-sandbox-app", create_if_missing=True)
sandbox = modal.Sandbox.create("sh", "-lc", "sleep 300", app=app)
```

3. Choose the workflow that matches the task before writing code.

- One-shot command execution and output capture: use `Sandbox.exec(...)`.
- A conversational or stateful controller loop: keep one long-lived sandbox alive.
- HTTP or TCP service exposure: use tunnels.
- Restore or persistence flows: use Volumes, CloudBucketMounts, or snapshots.

## Choose the Workflow

- Use one-shot `Sandbox.exec(...)` for isolated commands and output capture when the sandbox does not need to preserve conversational state across requests. Read [references/lifecycle-and-exec.md](references/lifecycle-and-exec.md).
- Use a long-lived controller loop when the sandbox must keep state across requests or support repeated `stdin` and `stdout` interaction. Read [references/example-patterns.md](references/example-patterns.md).
- Use tunnels when the sandbox must expose HTTP or TCP services and the client needs a public or restricted URL. Read [references/networking-and-tunnels.md](references/networking-and-tunnels.md).
- Use Volumes or CloudBucketMounts for persisted or shared files, and use snapshots only for explicit restore flows. Read [references/files-and-persistence.md](references/files-and-persistence.md) and [references/snapshots.md](references/snapshots.md).
- Reattach to a live sandbox with `Sandbox.from_id(...)` or `Sandbox.from_name(...)` instead of creating duplicates.

## Default Rules

- Create and control sandboxes through the Python SDK. Use `modal.App.lookup(..., create_if_missing=True)` before `modal.Sandbox.create(...)` when provisioning from local code.
- Set lifecycle limits deliberately. Treat the default sandbox lifetime as 5 minutes, raise `timeout` up to 24 hours when needed, and set `idle_timeout` when inactivity should shut the sandbox down.
- Reattach with `Sandbox.from_id(...)` or `Sandbox.from_name(...)` instead of creating duplicates. Name sandboxes only when you truly need a singleton on a deployed app.
- Use `Sandbox.exec(...)` as the default execution primitive. Read `stdout` and `stderr` from the returned `ContainerProcess`, use `bufsize=1` for line-oriented loops, and set `pty=True` only for commands that genuinely need a TTY.
- Keep one long-lived controller process when the task needs conversational state or repeated back-and-forth over `stdin` and `stdout`.
- Open only the ports the task actually needs. Poll `sandbox.tunnels()` for readiness, and use `block_network=True`, `cidr_allowlist=[...]`, or `create_connect_token()` when the service should be restricted.
- Bake static inputs into the image at build time, and use Volumes or CloudBucketMounts for files that must outlive one sandbox or be shared across runs.
- Prefer filesystem or directory snapshots for restore flows. Use memory snapshots only when in-memory process state matters enough to justify their current limitations.
- Use `detach()` when the sandbox should keep running after the client disconnects, and `terminate()` when the sandbox should stop immediately.
- Keep this skill focused on sandbox lifecycle and isolated execution. Do not use it for ordinary stateless `@app.function` deployments or generic Modal app hosting.
- If the task is really about fine-tuning or post-training, stop and use `modal-finetuning`.
- If the task is really about vLLM or SGLang model serving, stop and use `modal-llm-serving`.
- If the task is really about detached batch orchestration or `@modal.batched`, stop and use `modal-batch-processing`.

## Validate

- Run `npx skills add . --list` after editing the package metadata or skill descriptions.
- Keep `evals/evals.json` and `evals/trigger-evals.json` aligned with the actual workflow boundary of the skill.
- Run [scripts/smoke_test.py](scripts/smoke_test.py) with a Python interpreter that can import `modal` when changing lifecycle, `exec(...)`, or file-IO guidance.

## References

- Read [references/lifecycle-and-exec.md](references/lifecycle-and-exec.md) for lifecycle, reattachment, and command-execution details.
- Read [references/networking-and-tunnels.md](references/networking-and-tunnels.md) for tunnels, network controls, and service exposure.
- Read [references/files-and-persistence.md](references/files-and-persistence.md) for build-time uploads, runtime file IO, Volumes, and persistence tradeoffs.
- Read [references/snapshots.md](references/snapshots.md) for snapshot selection, limitations, and restore patterns.
- Read [references/example-patterns.md](references/example-patterns.md) for distilled sandbox workflow templates.
- Read [references/troubleshooting.md](references/troubleshooting.md) for common failure modes and recovery paths.
