---
name: workflow-setup
description: Create, edit, inspect, run, schedule, pause, or delete workflows and automations.
---

# Workflow Setup

Use this skill to help users create and manage workflows and their
automations. A workflow is the reusable SOP/skill body. An automation is a
trigger attached to a workflow. The CLI represents automations as
`okou workflow trigger ...`; the user-facing conversation should usually call
them "automations" or "triggers" in plain language, not CLI objects.

Prefer workflow triggers over legacy automations unless the user explicitly asks
for the old automation system.

Run Okou CLI commands as:

```bash
okou <command>
```

The Okou binary is provided by the current agent runtime.

## User Experience Contract

Hide implementation details by default. Do not show raw commands, workflow IDs,
trigger IDs, cron expressions, JSON configs, webhook signing material, or
verification output unless the user asks for technical details, auditability, or
debugging context.

Speak in terms the user understands:

- "workflow" = the reusable instructions or SOP.
- "automation" = when and how that workflow should run automatically.
- "trigger" = the condition that starts the automation.
- "run now" = manually start the workflow once.
- "pause" / "turn back on" = disable / enable the automation while preserving
  its settings.

Default to a requirements-first conversation. Ask only for missing information
needed for the next action, and keep questions short. Prefer one question with
2-4 concrete choices over a generic template.

For built-in templates, use a draft-first setup path. If the template already
defines a clear job, save the reusable workflow before asking about connector
setup or automation details. Keep it without an automation until the user
confirms the trigger and any safety-sensitive side effects. If permission to
send, merge, edit, spend, delete, or contact people is unclear, make the draft
prepare or recommend the action and require approval instead of blocking draft
creation.

Good user-facing questions:

- "What should this workflow do each time it runs?"
- "When should it run: on a schedule, every few minutes, when an email arrives,
  when a Gmail label is applied, from a webhook, from a GitHub label, or when a
  calendar event is created?"
- "Should it only draft changes, or is it allowed to send messages / edit data /
  create issues?"
- "Do you want this paused for now, or enabled immediately after I create it?"

Avoid user-facing phrasing like:

- "Give me the cron expression."
- "Which workflow ID should I use?"
- "Should I call `okou workflow trigger add`?"
- "Send me the JSON config."

## Product Model

Follow the Automation x Workflow model:

- A workflow is a pure definition: name, description, instructions, optional
  supplementary files, and the agent that owns it.
- A workflow does not run automatically by itself.
- An automation is one trigger attached to one workflow.
- A workflow can have zero or more automations.
- Enabled cron, loop, and event automations persist beyond this conversation and
  can start future runs until disabled or removed. A `once` automation has one
  fire time.
- Editing the instructions means editing the workflow.
- Editing schedule, email matching, labels, webhook, enable/disable, or delete
  means managing the automation/trigger.

When a user says "make this automatic", "set this to run every day", "notify me
when...", or "turn this workflow into an automation", create or update a trigger
on a workflow.

When a user says "save these steps", "create a workflow", "make a reusable SOP",
"edit the instructions", or "use this template", create or edit a workflow.

## Fast Path

1. Identify whether the request is about the workflow body, an automation, or
   both.
2. If the request mentions an existing workflow by name, list workflows when
   needed to resolve the name. If ambiguous, ask the user to choose by friendly
   name/description, not by ID.
3. If creating an automation and no suitable workflow exists, offer to create
   one with Okou first, then attach the automation.
4. Collect the minimum missing requirements for the next command. A connector,
   schedule, destination, or trigger setting is not required to save a workflow
   draft when the reusable job is already clear.
5. Execute the Okou CLI command(s) in the background. For a template, create and
   verify the workflow draft before asking the next activation question.
6. Verify with `workflow view` and/or `workflow trigger list` after create or
   update operations.
7. Report the result in plain language, including what will happen next and any
   safety limits. After creating a new automation, proactively name the model it
   will use. Keep technical IDs out of the normal response.

Do not inspect connector authorization or request permissions as part of the
default setup path. If the command reports connector authorization or permission
failure, stop the blocked action and use the relevant connector doctor or
permission flow requested by the platform instructions.

## Creation Flows

### Create Workflow With Okou

Use this when the user wants a new reusable workflow, has no suitable workflow
for an automation, or chooses "Create with Okou".

Collect:

- The workflow's job: what it should do when run.
- Inputs or sources it should use.
- Output or final deliverable.
- Allowed side effects.
- Any approval gates, safety limits, or recipients.
- Whether it should be enabled automatically later, and on what trigger.

Then draft concise workflow instructions and create the workflow:

```bash
okou workflow create <name> --agent <agent-id> --display-name "<display name>" --description "<description>" --instruction "<workflow instructions>"
```

Use `--instruction-file <path>` for longer instructions. Use `--dir <path>` only
for supplementary files. Never include a root `SKILL.md` in `--dir`; the workflow
upload synthesizes it from workflow metadata and instruction.

After creation, stay in the conversation. Say that the workflow has been saved
and offer the natural next action, such as setting when it should run.

### Save Conversation As Workflow

Use this when the user wants to preserve steps from a completed conversation.

Summarize the actual steps into reusable instructions, ask the user to confirm or
adjust the name/instructions, then create a workflow under the current agent
unless they specify another agent.

Do not add a trigger unless the user explicitly asks to automate it.

### Create Automation For Existing Workflow

Use this when the user wants a workflow to run automatically.

Collect:

- Which workflow should be automated.
- The trigger type and required trigger settings.
- Whether to enable it immediately.
- Whether the workflow is allowed to send messages, modify systems, spend money,
  delete data, or contact customers.

Check existing triggers for that workflow before creating a new one. If a similar
automation already exists, ask whether to keep both, update the existing one, or
disable the old one.

After adding a new automation, read its thread model from the creation result.
If the result does not include the model, inspect the created automation or its
chat thread before responding. Proactively tell the user the friendly model name
the automation will use; include the model ID only when the user asks for
technical details. Automations use their chat thread's current model rather than
storing an independent model, so phrase this as the model the automation will
use and do not imply that the model is pinned to the automation itself.

### Template Or Uploaded Workflow

If the user starts from a built-in template, treat the selected template as
enough approval to save a reusable workflow draft when its job is clear. Infer
the name and description from the template, create it without an automation,
and verify it. Do not inspect connector authorization first.

When trigger details or destinations are missing, ask one short question only
after the draft exists. Do not add or enable an automation until the user has
confirmed its trigger and safety-sensitive side effects. For destructive or
external actions that are not yet confirmed, keep the draft in
recommend/draft-only mode with an approval gate.

For an uploaded file whose job is ambiguous, ask only the next question needed
to understand the reusable workflow body. Do not expose file packaging details
unless import fails.

## Trigger Setup

Before creating or updating an automation trigger, read
[references/trigger-setup.md](references/trigger-setup.md) for trigger-specific
requirements and command shapes.

## Management Flows

### Inspect

Use:

```bash
okou workflow list
okou workflow list --agent <agent-id>
okou workflow view <workflow-id>
okou workflow trigger list <workflow>
okou workflow trigger show <trigger-id>
```

Summarize in product language: what the workflow does, whether it has
automations, when it next runs, whether it is enabled, and what it is allowed to
do.

### Edit Workflow Instructions

When the user asks to change what the workflow does, edit the workflow
instruction:

```bash
okou workflow edit <workflow-id> --instruction-file ./instruction.md
okou workflow edit <workflow-id> --display-name "<name>" --description "<text>"
```

Ask for confirmation before making changes that broaden side effects.

### Edit Automation

When the user asks to change when or how it runs, update the trigger. Keep the
conversation inline: ask for the new schedule, interval, label, email matching,
GitHub matching, or replacement behavior, then run the update command.

Do not imply that workflow instructions changed when only the trigger changed.

### Run Now

When the user wants to test or manually run once:

```bash
okou workflow run <workflow-id>
```

Tell the user it has started in a new thread. Include the log command only when
they ask for technical details or progress debugging.

### Pause Or Resume

Use disable/enable for an automation. This preserves its settings:

```bash
okou workflow trigger disable <trigger-id>
okou workflow trigger enable <trigger-id>
```

Ask before pausing broad or business-critical automations if the impact is not
obvious.

### Delete

Only delete a workflow or trigger when the user explicitly asks and confirms the
target.

Use trigger removal when deleting one automation:

```bash
okou workflow trigger remove <trigger-id>
```

Use workflow deletion when deleting the workflow itself:

```bash
okou workflow delete <workflow-id> -y
```

Explain the effect in plain language: deleting an automation stops that one
automatic run path; deleting a workflow removes the reusable SOP and its attached
triggers.

### Copy Or Fork

Only copy/fork a workflow when the user asks to reuse it on another agent:

```bash
okou workflow copy <workflow-id> --to-agent <agent-id>
```

Tell the user the workflow has been copied to the target agent.

### Run History

If the user asks for run history, first inspect the trigger details for last run
and next run. If they need full execution logs, use the available logs/search
tooling with a known run ID or relevant workflow context. Do not claim full
history is available from `okou workflow trigger` if the CLI only returns summary
fields.

## Safety Rules

- Ask before enabling or testing workflows that send external messages, modify
  production systems, spend money, delete data, or contact customers.
- For broad triggers, say the scope plainly, e.g. "This would run for every
  incoming email. Should I narrow it down?"
- Treat webhook secrets as sensitive. Preserve the creation output, but do not
  expose full secrets in normal responses unless the user explicitly needs the
  creation-time secret.
- Disable or remove triggers only when the user explicitly approves that action.
- Do not fork/copy a workflow unless the user explicitly asks to copy, fork,
  move, or reuse an existing workflow on another agent.

## Verification

After creating or updating a workflow:

```bash
okou workflow view <workflow-id>
```

After creating, updating, enabling, disabling, or removing a trigger:

```bash
okou workflow trigger list <workflow-id>
okou workflow trigger show <trigger-id>
```

For a newly created automation, verification is incomplete until its thread
model is known. Read it from the creation result or inspect the automation or
chat thread before replying to the user.

Keep verification output internal unless the user needs technical detail.

## Final Response Defaults

Default final response:

- State the outcome in plain language.
- Name the workflow and the automation behavior.
- Mention enabled/paused status.
- For a newly created automation, proactively state the model it will use.
- Mention important safety behavior, such as "draft only, never sends".
- Tell the user the natural next action, such as applying a Gmail label or using
  the webhook URL.

Do not include workflow IDs, trigger IDs, raw commands, cron expressions, JSON,
or check lists by default.

Technical final response format, when needed:

- Workflow: name and id.
- Automation/trigger: kind, id, enabled status, and match/schedule summary.
- Checks run: list/view/trigger list/show.
- Blockers: missing user criteria, command failure, or permission denial.
