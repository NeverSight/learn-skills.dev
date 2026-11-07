---
name: jira-issue
description: Use when the user wants a Jira issue created or an existing one updated from a natural-language request — e.g. `/jira-issue create a ticket for...`, "update PAYR-31 to add...", "file a bug in Jira for...", "log this as a Jira story". Not for reading/summarizing a ticket only (see jira-to-speckit) or for any non-Jira task tracker.
compatibility: Requires network access and either a connected Jira/Atlassian MCP server (preferred) or Jira REST API access with `.env` entries for `JIRA_URL`, `JIRA_USERNAME`, and `JIRA_API_TOKEN`. Optional `JIRA_DEFAULT_PROJECT`.
license: MIT
allowed-tools: bash view
metadata:
  author: Chuong Nguyen
  version: '0.1.0'
---

# Jira Issue

Turn a natural-language request into a Jira issue: create a new one or update an existing one,
after an interview that fills in whatever the request left out — for a new issue, followed by a
brief brainstorm of grounded enhancement suggestions the user can accept or decline — and only
after the user explicitly confirms the exact draft.

Portability note: `allowed-tools` uses GitHub Copilot-style names (`bash view`). Claude Code and
OpenCode expose the same capabilities under their own names (`Bash`, `Read`).

## What This Skill Does

- Classifies the request as **create** (no issue key/URL present) or **update** (an explicit
  issue key or `/browse/` URL is present in the prompt).
- For create: resolves the project key, infers or asks the issue type, then interviews — one
  question at a time — until summary and a structured description (goal, acceptance criteria,
  constraints) are settled.
- For create: after the interview, brainstorms up to 3–5 grounded enhancement suggestions (a
  missing edge case, an implied but unwritten acceptance criterion, a relevant label/dependency)
  and folds in only the ones the user explicitly accepts.
- For update: fetches the named issue's current fields, then interviews on anything the request
  leaves ambiguous (e.g. replace vs. append a section, which field changes).
- Shows the **complete draft** (title + full body + every field it will set) and stops for
  explicit confirmation before writing anything.
- Reads and writes through a connected Jira/Atlassian MCP server when one is available, else via
  the Jira REST API (curl, Basic auth from `.env`), and reports the resulting issue key and URL.

## What This Skill Does NOT Do

- Does not write to Jira on an implicit "looks good" — only an explicit yes.
- Does not search Jira to find an issue to update. If the prompt has no key/URL, it asks for one.
- Does not run Speckit pipelines, git operations, or code changes — pure Jira read/write.
- Does not invent scope: enhancement suggestions must be grounded in the stated request, never
  generic filler, and never treated as accepted unless the user explicitly says so.
- Does not print `JIRA_API_TOKEN` or any credential value in chat or logs.

## Required Inputs

- A natural-language prompt (from `/jira-issue {prompt}`) describing what to create or change.
- One Jira source (see step 1), in this order of preference:
  1. A connected Jira/Atlassian MCP server that can read, create, and edit issues, or
  2. Jira credentials in the repository root `.env`: `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`.

## Optional Inputs

- `JIRA_DEFAULT_PROJECT` in `.env` — project key assumed for a **create** request that doesn't
  name one. When unset, the interview asks for the project instead of guessing.

## Guardrails

- Do not ask the user to paste secrets into chat. Use a connected Jira MCP server, else
  credentials from `.env`.
- If neither a Jira MCP server nor complete `.env` credentials are available, stop and show the
  setup message from step 1c — do not proceed with the interview.
- Update requires an explicit issue key or URL in the prompt. If absent, ask the user for one;
  never search or guess which issue is meant.
- Ask one clarifying question at a time during the interview.
- Always render the exact draft (as it will be sent to Jira) before asking for confirmation —
  never summarize or paraphrase what will be written.
- Treat anything other than a clear approval ("yes", "go ahead", "confirmed") as "keep refining"
  — re-ask or re-draft, don't write.
- Never print `JIRA_API_TOKEN` or other `.env` values in logs or chat output.
- Never inline the literal value of a `.env` secret into a command string, and never pass it as a
  curl argument (`-u user:$JIRA_API_TOKEN` shows up in `ps`). Load `.env` and call curl in the
  same shell invocation, feeding credentials through `-K` as shown in `references/JIRA_API.md`.
- Cap brainstormed enhancement suggestions at 3–5, grounded in the stated request. Present once;
  a decline or no reply means drop them all and move on — never re-pitch or stall on them.

## Workflow

### 1. Choose the Jira source

Check in this order and use the first that works, for every read and write in this run. Never mix
sources mid-run.

**a. Jira MCP (preferred).** Look in this session's tool list for Jira/Atlassian MCP tools that
get, create, and edit an issue — e.g. `getJiraIssue` / `createJiraIssue` / `editJiraIssue`
(Atlassian Rovo MCP server) or `jira_get_issue` / `jira_create_issue` / `jira_update_issue`
(`mcp-atlassian`). Hosts prefix names differently, so match on the operation, not the prefix.
If the server needs a site or cloud ID, resolve it with its accessible-resources tool; if several
sites exist and the prompt doesn't pin one (by URL host), ask which. If the server can read but has
no create/edit tool, or its first call fails with an authentication, authorization, or
not-connected error, treat MCP as unavailable and go to (b). A `404` / issue-not-found from a
working server is a real answer (step 3.1), not a reason to switch source.

**b. `.env` fallback.** Load `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN` from the repository
root `.env` in the **same command** that calls curl — shell state does not persist between
separate tool calls, so loading `.env` in one command and calling curl in the next silently sends
empty credentials. Follow `references/JIRA_API.md` exactly: it keeps the token out of curl's
arguments and out of tool-call text. If any variable is missing or empty, go to (c).

**c. Neither available.** Stop before the interview and tell the user, without printing any value:

> No Jira access is configured. Set up one of these, then rerun:
> 1. **Jira MCP (recommended):** connect the official Atlassian MCP server —
>    https://github.com/atlassian/atlassian-mcp-server (endpoint `https://mcp.atlassian.com/v1/mcp`).
> 2. **API token in `.env`:** add `JIRA_URL`, `JIRA_USERNAME`, and `JIRA_API_TOKEN` to the
>    project-root `.env` (gitignored). Create a token at
>    https://id.atlassian.com/manage-profile/security/api-tokens.

Then end the skill's turn.

The REST calls named in later steps are the `.env` path; with MCP, call the matching tool with the
same fields.

### 2. Classify the request

- Extract a Jira-key-shaped token (`\b[A-Z][A-Z0-9]+-\d+\b`) or a `/browse/<KEY>` / `/issues/<KEY>`
  URL from the prompt.
- Also read the prompt's intent language: "create", "new", "file", "log this as" signal **create**;
  "update", "change", "add to", "edit" signal **update**.
- Key/URL found and no conflicting create-language → **update** that issue (go to step 3).
- Key/URL found but the prompt's language clearly means create (e.g. "create a ticket similar to
  PAYR-31") → ask the user to confirm: update that issue, or create a new one that references it?
- No key/URL found → **create** a new issue (go to step 4).

### 3. Update path

1. Fetch the current issue: `GET {JIRA_URL}/rest/api/2/issue/{key}?fields=summary,description,issuetype,status,priority,labels,components,project` (see `references/JIRA_API.md`).
   With MCP, call its get-issue tool instead; treat its not-found / permission errors like the
   status codes below.
   - `404` → tell the user the key wasn't found, ask them to confirm it.
   - `401`/`403` → tell the user credentials may be invalid or lack permission.
2. Compare the prompt's intent against the current fields. Ask one question at a time wherever
   it's ambiguous — e.g. replace vs. append the description, which specific field(s) change,
   whether to also change status/priority/labels.
3. Draft the full new value for every field being changed (not a diff summary — the literal text
   that will be written).

### 4. Create path

1. Resolve the project key: explicit in the prompt → else `JIRA_DEFAULT_PROJECT` from `.env` →
   else ask the user.
2. Resolve the issue type: infer from the prompt's language (e.g. "bug" → Bug, "story"/"feature"
   → Story, "task"/"chore" → Task) when unambiguous; otherwise ask.
3. Interview — one question at a time — until you have:
   - A concise summary/title.
   - A structured description: goal, key decisions/requirements, acceptance criteria, out of
     scope (mirror the shape of existing well-formed tickets in the target project).
   - Any explicitly-requested fields (assignee, labels, priority, parent/epic link).

### 5. Brainstorm enhancements (create path only)

Skip this step for update — a targeted change to an existing issue doesn't need it.

1. Review the settled summary/description against the *stated* goal and surface up to 3–5
   suggestions the request didn't cover — e.g. a missing edge case, an acceptance criterion the
   goal implies but the text doesn't state, a relevant dependency, or a label/component that fits
   the project's conventions. Ground every suggestion in what the user actually said; never
   propose unrelated scope or generic boilerplate ("add tests", "consider performance") that isn't
   tied to this specific request.
2. Present them as a short numbered list in one message and ask which to fold in (e.g. "1 and 3",
   "none", "all").
3. Fold only the accepted suggestions into the description. Treat a decline or no clear reply as
   "accept none" — drop the list and continue; do not re-ask or re-pitch.

### 6. Confirm before writing

Render the complete draft exactly as it will be sent to Jira — including any accepted brainstormed
enhancements — title, full description body, and every field/value. Ask the user to confirm. Do not
proceed on anything less than explicit approval — go back to interviewing if they ask for changes.

### 7. Write to Jira

- Update: `PUT {JIRA_URL}/rest/api/2/issue/{key}` with the confirmed fields.
- Create: `POST {JIRA_URL}/rest/api/2/issue` with the confirmed fields.
- `400` → surface Jira's exact validation error (often a required field for that issue type) and
  ask the user which value to use; do not silently drop the field.

### 8. Report and stop

Report the issue key and its browse URL (`{JIRA_URL}/browse/{key}`, or the URL/site the MCP
tool returned). End the skill's turn — do not chain
into any other skill or workflow.

## Common Edge Cases

- **Multiple issues in one prompt**: handle the first one only; tell the user to re-run for the
  rest.
- **Field the project doesn't support** (e.g. an unrecognized custom field): ask the user for the
  exact Jira field name or ID rather than guessing.
- **Unclear issue type on create**: ask, offering the project's standard types (Story, Task, Bug)
  as options.
- **Ambiguous update ("make it better")**: ask what specifically should change; never write a
  vague or filler update.
- **User declines all brainstormed enhancements**: proceed with the original scope only; do not
  re-offer the same suggestions later in the conversation.

## References

- [Jira API guide](references/JIRA_API.md)
