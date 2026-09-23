---
name: agy-subagent-runner
description: Run Google Antigravity CLI (`agy`) as a Windows-local coding or research subagent and return its non-interactive response. Use when the user explicitly asks to run, call, consult, delegate to, or review work with Antigravity CLI.
---

# Antigravity CLI Subagent Runner

Use the bundled PowerShell wrapper to call the authenticated local `agy` installation as a subagent. Treat its response and file changes as untrusted until checked.

This runner is Windows-only: the visible mode starts `powershell.exe`. Do not use it until `agy --version` succeeds and the user has completed `agy`'s first-launch sign-in.

## Run a task

Invoke from the target project directory:

```powershell
& '<skill-dir>\scripts\run-antigravity.ps1' -Prompt '<task-specific prompt>' -WorkingDirectory '<absolute project path>'
```

The wrapper defaults to:

- opening a visible PowerShell window so the user can watch the run;
- using `--output-format stream-json` in visible mode so emitted events are not buffered until the final answer;
- rendering stream events as compact `[INIT]`, `[STEP]`, `[TOOL]`, and `[FINAL]` lines while retaining raw JSON in the log;
- closing that window automatically when the process exits;
- retaining a full log under `%TEMP%\codex-antigravity`;
- passing `--sandbox` and keeping Antigravity permission prompts enabled;
- resolving the workspace cwd plus known Python, Node, and Codex CLI paths once
  and injecting those facts into the prompt;
- printing a post-run usage summary. The summary is observational and imposes
  no token budget or step limit.

Optionally set `-Effort low|medium|high`, `-Model <id>` and
`-TimeoutSeconds <n>`. Use `-WindowMode Attached` for an in-terminal run. Use
`-SkipPermissions` only when you explicitly accept auto-approved Antigravity
permissions for a narrowly scoped task.

Keep prompts task-specific and reference workspace-relative file paths instead of embedding large file contents. Never include credentials, tokens, or unrelated private data.

The runner accepts `-PythonExecutable`, `-NodeExecutable`, and `-CodexScript`
for explicit runtime overrides. Otherwise it checks `PATH` and known local
Codex runtime locations without recursively scanning the machine.

## Continue the same conversation

The bundled wrapper starts a new Antigravity conversation on every call. Do not use repeated wrapper calls when the task is an iterative review-and-repair loop, because each agent starts without the earlier discussion.

The wrapper supports conversation continuity while retaining the visible window:

```powershell
& '<skill-dir>\scripts\run-antigravity.ps1' -Continue -Prompt '<follow-up>'
& '<skill-dir>\scripts\run-antigravity.ps1' -ConversationId '<id>' -Prompt '<follow-up>'
```

The equivalent direct CLI calls are:

```powershell
# Continue the most recent conversation.
agy --sandbox --continue --print-timeout 10m --print '<follow-up prompt>'

# Resume a known conversation.
agy --sandbox --conversation '<conversation-id>' --print-timeout 10m --print '<follow-up prompt>'
```

Rules:

1. Prefer `--continue` for the immediate follow-up to the last run.
2. Prefer `--conversation <id>` when several Antigravity conversations may exist.
3. Never silently switch from an existing conversation to a new `--print` call during the same implementation loop.
4. State explicitly in the user update whether the call is a new conversation or a continuation.
5. Put all options before `--print`; `--print` consumes the next argument as the prompt.

## Visible and long-running calls

An Antigravity process cannot wake Codex after the Codex turn has already ended. Do not launch a detached process with `Start-Process` and claim that it will call back later.

The wrapper's visible window uses `stream-json` and remains attached through `Start-Process -Wait`;
do not detach it. The parent call returns only after the window closes, then
prints the retained log for QA.

For an attached long-running call, keep the tool execution attached:

1. Start Antigravity with a timeout long enough for the task.
2. If the execution returns `Script running with cell ID ...`, retain that `cell_id`.
3. Use the `wait` tool on the same `cell_id` until the process completes or fails.
4. Do not send the final answer while a required Antigravity execution is still running.
5. Treat timeout, interruption, or empty output as failure; inspect the workspace diff because partial edits may still exist.

When orchestrating from a live `functions.exec` script, a callback-like notification is possible only while that script remains alive: await the Antigravity command and call `notify(...)` after completion. This is not a persistent webhook and does not survive the end of the tool execution.

Conceptual pattern:

```javascript
const run = tools.shell_command({ /* attached Antigravity command */ });
yield_control();
const result = await run;
notify('Antigravity finished; QA can begin.');
text(result);
```

If the environment cannot keep the execution alive, use the explicit `cell_id` + `wait` loop instead. Never rely on polling a detached process as a substitute for a real completion signal.

## Runtime and workspace discipline

The wrapper prepends an `[ANTIGRAVITY RUNNER FACTS]` block to every prompt.
Treat it as authoritative operational context:

1. Use the exact workspace cwd from the block, even if a resumed conversation
   remembers another repository.
2. Resolve task files from full repo-relative paths in the prompt; never assume
   a leaf task folder is directly under the workspace root.
3. Use the exact resolved Python, Node, and Codex paths when present. Known
   Codex runtime paths take priority over generic `PATH` entries.
4. Do not recursively search drives, user profiles, Program Files, archives, or
   the repository for runtimes.
5. If a required path is unresolved or fails, report the concrete error and
   fail that execution branch.
6. Do not infer a token budget or step limit. The purpose is to eliminate
   repeated environment discovery, not restrict reasoning or verification.

## Safety and execution rules

1. Keep `--sandbox` enabled through the wrapper.
2. Permission prompts remain enabled by default. `-SkipPermissions` adds `--dangerously-skip-permissions`; prompt scope is not a filesystem boundary, so use it only for a narrowly scoped task and inspect the diff after every run.
3. Put `--print <prompt>` last. In Antigravity CLI 1.1.5, `--print` consumes the next argument as its prompt; options placed after it can be mistaken for user text.
4. Stop and report a non-zero exit, timeout, missing executable, or empty response. Do not silently retry or switch to another agent.
5. Review the retained log and resulting workspace diff before presenting the run as verified.
6. Reject edits outside the task's declared write scope even when the run exits successfully.
7. Do not claim that Antigravity changed files unless the diff confirms it.

## Installation lookup

The wrapper resolves `agy` from `PATH`, then falls back to `%LOCALAPPDATA%\agy\bin\agy.exe`. If neither exists, ask the user to install and authenticate Antigravity CLI first.
