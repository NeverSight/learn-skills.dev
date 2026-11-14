---
name: interrogate
description: "Adversaries try to break a change or design, and only findings proven by a run survive."
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Interrogate

Adversaries try to break a change or a design. A finding survives only when a run proves it. Report the findings. Do not apply fixes.

## Frame

The scope is what the user names. Otherwise it is the branch diff from its merge base with the base branch, through the working tree. From the user's message, the commits, and the PR description, restate in your own words what you think the user's goals are and what problem they are trying to solve. This restatement is the intent. Ask the user when the intent is unclear.

## Fan out

By default there are two adversaries, on two model families. Start each subagent with a fresh context window.

- **Adversary A** is a subagent on your own model. Set its effort one step below your own. If you do not know your effort, do not set it.
- **Adversary B** runs on a different model family, through that family's CLI, with its prompt on stdin. If you are a Claude model, run `codex exec -s workspace-write -C <worktree> -o <output-file> -`. Otherwise, run `claude -p --permission-mode auto` in its worktree, and send its output to a file. The CLI uses its own configured model. If the CLI is missing or fails, run Adversary B as a second subagent on your own model, and say in the output that the review has one model family.
- If the user names more models, add one adversary for each, labeled Adversary C, D, and so on.

Give each adversary its own git worktree, so no two adversaries write to the same file. Copy the scope's uncommitted changes into each worktree. Start all adversaries at the same time, in the background. Give each adversary the scope, the intent, the path of its worktree, and this brief:

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your own worktree. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That covers style, naming, structure, and risks that need a future change to matter. No findings is a valid result.

If an adversary produces no output, go on with the others and note the dropout.

## Verify

Verify each finding by rerunning its command in that adversary's worktree. Keep a finding when the output shows the failure and the failure breaks the intent. Drop the rest. Merge findings that share a root cause.

Adversaries find different failures, so the verdict keeps every verified finding, not one adversary's list. Then remove the adversary worktrees.

## Output

- **Intent**: the restatement.
- **Findings**: for each verified finding, the command, its output, how it breaks the intent, and the adversaries that found it. Say "no verified findings" when none survive.
- **Dropped**: for each adversary, the count of dropped findings and why.
