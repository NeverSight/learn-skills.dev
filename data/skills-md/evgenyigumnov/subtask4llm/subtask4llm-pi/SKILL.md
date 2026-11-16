---
name: subtask4llm-pi
description: Plan and run a dependency-ordered software change through sequential, one-shot Pi workers with bounded retries and explicit dependency handoffs. Use for authorized multi-step implementation work that benefits from isolated worker contexts; avoid it for planning-only requests or small changes that one worker can complete directly.
---

# Subtask4LLM for Pi

Use the current Pi session as the planner and reviewer. The standalone runner at [scripts/run_workflow.py](scripts/run_workflow.py) launches sequential Pi workers in the target workspace.

## Workflow

1. Choose this workflow when the requested implementation has multiple concrete steps and ordered handoffs make separate worker contexts useful. Do not split a small change just to use the runner.
2. Inspect the repository and prepare a complete version 1 JSON plan with 1–10 ordered steps. Give every step a unique ID, a bounded task, nonempty acceptance criteria, and dependencies only on earlier steps. Include shared repository findings, user requirements, constraints, relevant paths, design decisions, and edge cases in the plan so workers do not need the planner's conversation.
3. Read [references/plan-format.md](references/plan-format.md), write the plan to a temporary JSON file, and validate it with `--dry-run` before execution.
4. Before starting workers, show the user the goal and ordered step titles, each with a short description and its dependencies. Then launch the workflow unless the user asks to review or change the plan first.
5. Run the runner from the target repository.

   On macOS or Linux:

   ```bash
   python3 <skill-path>/scripts/run_workflow.py <plan.json> --workspace <repository>
   ```

   On Windows PowerShell:

   ```powershell
   py -3 <skill-path>\scripts\run_workflow.py <plan.json> --workspace <repository>
   ```

   Add `--model <model-id>` only when the model ID is known and should override the configured model. Otherwise, the runner uses `PI_WORKFLOW_MODEL` when set, then Pi's configured default. Use `--timeout-seconds`, `--timeout-checkpoint-seconds`, `--retries 0|1`, `--max-summary-chars`, `--pi-bin`, or `--artifacts-dir` only when the task calls for those controls. Add `--continue-on-error` only when the user wants later steps to run after an earlier step fails; the final workflow status still reports failure if any step failed. Artifacts are optional and the runner refuses to overwrite an existing artifact destination.
6. Workers run as one-shot JSON-event Pi processes with `--mode json --no-session --no-skills`. Prompts are sent through standard input, and the runner extracts the final assistant text, which must be raw JSON matching the documented result schema. The runner streams readable summaries from every subtask and the orchestrator into one workflow-wide live log; it does not create per-attempt progress log files. It prints the log path and a ready-to-copy `tail -f` command when the run starts; use `--live-log <path>` to choose another path. The default live log is outside the workspace in the system temp directory. The log includes tool commands and short output or assistant-response summaries, so treat it as potentially sensitive. The runner checks progress every 10 minutes, stops a shell command that has produced no update for 10 minutes, and gives the first attempt a 30-minute hard limit. If it fails and a retry is available, the second attempt gets twice the configured hard limit (60 minutes by default). Timeout diagnostics include recent activity and a timeout can use the configured retry. Workers retain normal `AGENTS.md` context discovery; the runner does not disable context files. Each worker gets the shared context, the full workflow map, its assigned task and acceptance criteria, and detailed results only for its declared dependencies.
   The live log is for the user to follow. Once the runner starts, show the user its log path and `tail -f` command, then wait for the runner process to finish. Do not repeatedly poll the process, run separate `sleep`/`tail` checks, reread the live log, or send timed progress updates. Check progress again only if the user asks or troubleshooting requires it. The runner's own process supervision and log writes continue while you wait.
7. Any failed attempt, including a timeout or detected stalled command, can use at most the configured retry. The second attempt gets twice the configured hard runtime limit. By default, the runner stops after a step remains unsuccessful; with `--continue-on-error`, it runs the remaining planned steps itself. Do not improvise extra worker runs after the runner exits.
8. Review the runner's final report and the actual workspace diff. Verify the requested changes proportionately, then report changed files, checks, and unresolved risks.

## Prerequisites and permissions

Pi CLI and a provider configured for Pi must already be installed and usable before running this workflow. This skill does not install Pi, providers, or other tools automatically.

Pi worker commands can modify files with the current user's permissions. Pi CLI is not a sandbox. Use the runner only when those permissions are appropriate for the requested repository work, preserve unrelated changes, and do not grant workers unrelated external actions.

## References

- [Version 1 plan and result format, CLI controls, and examples](references/plan-format.md)
- [Standalone sequential Pi runner](scripts/run_workflow.py)
