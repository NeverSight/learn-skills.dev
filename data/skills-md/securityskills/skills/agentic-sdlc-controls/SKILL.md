---
name: agentic-sdlc-controls
description: Review a development pipeline where AI coding agents write, commit and deploy — permission boundaries, approval gates on irreversible actions, credential scope, and what must never be delegated. Use when agents have write access to a repository or an environment.
phase: harden
---

# Agentic SDLC Controls

An agent in your pipeline acts with your credentials, at machine speed, without getting tired of a repetitive task. That is the point of it, and it is also the threat model. Review the boundary, not the agent's intentions.

Applies to any coding agent with write access — Claude Code, Codex, Cursor, OpenCode, or a CI job that calls a model. Nothing here depends on which one.

## 1. Establish What the Agent Can Actually Reach

Inventory before opinion. For each agent or automation:

- **Identity**: whose credentials does it run as? A named service identity, or a human's personal token?
- **Repositories**: read, write, or admin? Can it push to a default branch, or only open a PR?
- **Environments**: can it reach staging? production? a customer's data?
- **Secrets**: which values are in its environment at runtime, and which of those does its task actually require?
- **Network**: can it make arbitrary outbound calls, or is egress restricted?

Write this down as a table. The common finding is not a subtle misconfiguration — it is that nobody had the list.

## 2. Separate Reversible from Irreversible

Classify every action the agent can take:

| Class | Examples | Control |
|---|---|---|
| Reversible, contained | edit a file, run tests, open a PR | let it run |
| Reversible, visible | push a branch, comment on an issue | let it run, log it |
| Slow to reverse | merge to main, publish a package, migrate a schema | human approval gate |
| Irreversible | delete data, rotate production credentials, send external mail, spend money | never delegated |

The line to defend is the third row. Reversibility is the property that matters, not how risky the action sounds.

## 3. Enforce Gates in the Runtime, Not the Prompt

An instruction not to do something is a preference. A control the agent cannot bypass is a boundary.

- Prefer mechanisms the agent executes inside: pre-action hooks, permission allow/deny lists, managed settings a local config cannot override
- Verify the gate holds when the agent is run non-interactively — many approval prompts silently pass in CI
- Check the deny path is tested. An untested gate is a gate nobody knows is open
- Confirm an agent cannot edit the file that constrains it

Ask directly: if the agent were to attempt the worst action in its scope, what stops it, and has anyone watched that work?

## 4. Scope Credentials to the Task and the Blast Radius

- One identity per agent purpose; no shared human tokens
- Short-lived credentials over long-lived keys; expiry measured in the length of a task
- Environment-tiered autonomy: broad in a sandbox, narrow in staging, minimal in production
- Read-only by default where the task allows it — many review and triage agents never need write
- Isolate execution so a compromised or confused agent cannot reach beyond its workspace

## 5. Treat Agent Input as Untrusted

The agent reads issues, PR descriptions, dependency READMEs, web pages and tool output. Any of those can carry instructions.

- Content fetched during a task must not be able to escalate what the task may do
- Check whether the agent's tool results feed back into privileged actions without a gate
- Test with a benign injected instruction in a source the agent reads, and observe whether it acts on it

## 6. Make the Trail Reconstructable

For any change an agent produced, an auditor or an incident responder needs to answer: what was asked, what was produced, who approved it, and against which configuration.

- Prompts, plans and specs version-controlled alongside the diff
- Agent configuration (permissions, hooks, model, skill set) captured at the time of the change, not read from HEAD afterwards
- Approvals recorded as events, not as a person's memory of clicking a button

If this is thin, pair with the `ai-change-evidence` skill, which covers turning it into audit evidence.

## Scope and Rules of Engagement

Review only pipelines you own or are authorized in writing to assess. Testing a gate means attempting an action the control should stop — do that in a sandbox or a scheduled window, with the owner's agreement, never against production on your own initiative. Injection testing uses inert markers; do not plant anything that would cause harm if the control fails.

## Output

Report per finding: what the agent can reach, which control is missing or unenforced, the concrete sequence that would exercise it, and the smallest change that closes it. Separate "an agent can do this today" from "this would be better practice". Name the owner for each gap; a control with no owner is not a control.
