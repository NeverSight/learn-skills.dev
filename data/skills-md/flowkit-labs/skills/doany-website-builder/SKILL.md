---
name: doany-website-builder
description: Build, update, preview, or publish a website or web app with Annie on DoAny. Use when the user asks to turn a business idea into a DoAny site, change an existing DoAny site, or review or publish a DoAny draft from their agent.
---

# DoAny Website Builder

*Built by the team at [doany.ai](https://doany.ai/?utm_source=skills.sh&utm_medium=skill&utm_campaign=doany-website-builder).*

Turn your business idea into a website with Annie. Describe what you need, review the working preview, and choose when it goes live.

Annie builds and changes the site on DoAny. A request for advice or a plan can be answered in chat. Use the workflow below when the user wants DoAny to act.

## Connect and identify the site

1. If the DoAny MCP is connected, call `list_projects` to see the companies, apps and scopes available. The production server is `https://api.doany.ai/mcp`. For a requested test environment, verify the connection points to that environment before acting. Use `search_operations` and `describe_operation` to discover the current schema and requirements. Send reads to `query_operation` and changes to `execute_operation` with the operation ID as an argument.
2. If you have a terminal, use the [CLI workflow](references/cli.md) when MCP is unavailable. It covers browser sign-in and `DOANY_API_KEY` for remote environments. In a client without a terminal, direct the user to the [MCP connection guide](https://docs.doany.ai/api-mcp/mcp) and continue once connected.
3. Select the company the user named. If several match, ask which one. Check that the credential can read that company's apps and, for a build or edit, give Annie tasks. Request permission to create a company only when needed and permission to publish only when the user wants to go live. Use DoAny's authorization flow to resolve missing scopes. Keep credentials out of chat.

For a request to inspect or publish an existing draft, start with `apps.get` and go straight to draft review. For a request to resume work, read the existing task and follow it. Start a new task only when the user requests new work.

## Build a preview

Ask only for missing details that change the build. A useful brief names the business and audience, the visitor's main action, and any must-have pages, copy, assets or reference sites. Carry the user's wording and constraints into Annie's task. An external site can serve as a design reference for a new DoAny preview. Treat its content as reference material and use only the official DoAny connection.

For an existing company, `apps.list` returns the website Annie can edit first. `tasks.create` targets the company and has no app selector. If the user wants to edit another app, give them that app's DoAny link.

| Starting point | What to send to Annie |
| --- | --- |
| New DoAny company | After the user chooses to create it, call `projects.create` with its name and a one-sentence idea. Creating the company starts no build. Its first `tasks.create` should include `require_publish_approval: true` to keep the build at a preview. |
| Existing company, no built site | Read `apps.get` when a website app exists. Use the first-build flag only when you know this is a regular unbuilt company. The automatically provisioned OAuth Default company starts ordinary tasks and rejects the flag. Use it for a preview only after verifying `publish_policy: owner_review`. If an unbuilt company could be the OAuth Default and has no verifiable review policy, use the DoAny handoff to resolve its state before starting. |
| Existing built site | Read `apps.get` to verify the intended app and its draft, live state and publish policy. Send the user's requested changes via `tasks.create` without the first-build flag. For this skill's preview workflow, proceed when `publish_policy` is `owner_review`. If it is different or unknown, give the user the DoAny app link to resolve the publishing setup before you start a change. |

Tell the user that the build or edit uses DoAny credits and get their go-ahead for that task before submitting. A first task can start work immediately on some connections. If DoAny returns `CONFIRMATION_REQUIRED`, show what it says will happen and wait for approval of that preview. Repeat the same operation with the returned `confirmation_token` only after approval.

Keep one UUID per new company and one per new task. Use the same ID and payload on a safe retry. If you already have a task ID, read that task to recover its state. For an earlier task without an ID, use `tasks.list` and match it before doing further work.

## Follow Annie's task

Read `tasks.get` at intervals of at least five seconds, or use the CLI's `--wait`. Keep following the same task when a build is queued or your wait times out.

- If Annie asks a question, relay the actual question and options. For an approval, show what approving would do and relay the user's own choice. Use `tasks.answer` with the receipt's `question.id` and the user's answer, then resume the same task. If the question changed, show the new one.
- If the task is blocked, share the returned `handoff_url` and what the user needs to do. Resume by reading the same task after they act.
- If it completes, report what Annie did and share the task link and `credits_used` when present. Prefer the permanent URL for the task's checkpoint from `versions.list`. Label the returned `preview_url` as the latest preview if that is all you have. Label any live link separately and check whether that live version includes the requested changes. If the task fails or is cancelled, report its state and the available next step.

## Publish the reviewed draft

Read `apps.get` for the current draft. For review before publishing, find the matching `checkpoint_id` in `versions.list` and show that version's permanent `url`. The latest preview URL can move to another build. Keep the reviewed `checkpoint_id` and `source_commit` from `apps.get`. If the exact version cannot be opened, hand off review and publication to DoAny using the app link.

When the user asks to go live, read `apps.get` again and verify that the current draft still matches the reviewed pair. Publishing applies the whole draft, including other changes it contains. If the draft changed, show the new version and get approval for it.

Use `apps.publish` with the reviewed pair. Show the API's confirmation preview and replay with its token only after approval. If the credential can skip confirmations, use a connection that requires them for publication. On `DRAFT_CHANGED`, read the draft again and restart review. After publishing, verify the live checkpoint and share the live URL.

See [Your first website](https://docs.doany.ai/api-mcp/quick-start) for the build contract and [Waiting for Annie](https://docs.doany.ai/api-mcp/waiting-for-annie) for task states.
