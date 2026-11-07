---
name: agent-data-cli
description: >-
  Install, authenticate, update, and troubleshoot the agent-data CLI. Use for
  agent-data command syntax, typed API requests, account inspection, notify,
  output handling, and error recovery. Other agent-data skills use this skill
  when they need shared CLI mechanics.
metadata:
  version: "0.2.2-draft"
---

# Use the agent-data CLI

Use installed command help and the selected API's current docs. Read the section needed for the task; a working connection does not need repeated setup.

## Setup and identity

```bash
agent-data --version
agent-data --help
agent-data whoami
agent-data account
```

`whoami` reports locally resolved configuration, including the service URL and credential source; it does not authenticate with the service. `account` makes an unbilled authenticated request and returns account identity, allowance, and credit information. Use these checks when setting up or diagnosing a connection. Browser, CLI, and MCP sessions may use different accounts.

Use Node.js 22.20.0 or later. If the CLI is missing, use the project's installation method or inspect the current release without a global install:

```bash
npx --yes agent-data@latest --help
```

Sign in with `agent-data auth login` when credentials are missing. Open the returned URL and approve its code; the CLI saves the sign-in and renews access automatically. `--no-wait` returns the pending login immediately; use the returned login ID with `agent-data auth login --resume LOGIN_ID` after approval.

Credentials resolve from `--api-key`, then `AGENT_DATA_API_KEY`, then selected browser sign-in, then the legacy key in `~/.agent-data/config.json`. API keys remain available through [account settings](https://agent-data.motie.dev/settings/account). A failed selected sign-in does not fall back to a stored key; inspect `agent-data auth status` and sign in again when required.

The service URL resolves from `--base-url`, then `AGENT_DATA_BASE_URL`, then the release default. Preserve the selected service URL and `--auth-dir` through login and subsequent commands.

## Install and update

In CLI 0.13.0 and later, `init` signs in, installs the CLI globally, and uses Vercel's skills installer to install the five skills from [agent-data/skills](https://github.com/agent-data/skills). Select the actual host:

```bash
npx --yes agent-data@latest init --codex
```

Targets are `--codex`, `--claude-code`, `--open-claw`, `--hermes`, and `--nano-claw`. Multiple target flags install for those agents. The first four use global skill scope. NanoClaw uses project scope at `--nano-claw-path <repo>` with the Claude Code skill layout. `--yes` skips setup confirmations but still requires browser approval when signing in.

For an earlier CLI release, or to install skills without running CLI setup:

```bash
npx skills add agent-data/skills --global --agent codex
```

Select all five skills so their cross-references resolve. Omit `--global` for a project installation; run it from that project. Use Vercel's agent names `openclaw` and `hermes-agent` for direct installation to OpenClaw and Hermes.

Update the CLI through its npm installation method. Refresh skills separately through Vercel's standard commands:

```bash
npx skills update agent-data-cli agent-data-search agent-data-build agent-data-extend agent-data-monitor --global
```

This refreshes the five global skills from their tracked source. Upgrading the CLI alone does not update skills. In Vercel skills 1.7.4, `check` is an alias for `update` and can change installed files.

For project skills, repeat `skills add` from that project with the original explicit agent target. For NanoClaw:

```bash
npx skills add agent-data/skills --agent claude-code --skill agent-data-cli agent-data-search agent-data-build agent-data-extend agent-data-monitor --yes
```

Restart the coding agent after installation or refresh so it reloads the instructions.

For an old standalone `agent-data` skill, inspect its installation with `npx skills list --global`, remove that skill with `npx skills remove agent-data --global --agent codex`, then install `agent-data/skills`. Substitute the actual agent and scope. Older copied files do not gain update tracking automatically. If the legacy copy is outside the installer's recognized directories, remove that specific copy through its original installation method.

## Discover commands and inspect API docs

```bash
agent-data search --help
agent-data list --help
agent-data docs LISTING_ID
agent-data call --help
```

`search` finds APIs by query; `list` browses the catalog without semantic ranking. Replace `LISTING_ID` with an observed identifier. Workflow-specific skills provide guidance on choosing and qualifying a data source.

Docs expose routes under `api.routes`, including slugs, methods, paths, parameter locations, and examples. Read machine input schemas and contract warnings when present. Some response schemas use descriptive shorthand rather than complete JSON Schema; validate against what the contract states.

For build, extension, or account operations beyond these instructions, inspect the installed CLI's help and current operation contract before acting. A command name or historical example does not establish current support.

## Construct a call

Start with the selected route's current example. Simple inputs may use `--NAME VALUE`; the CLI places documented parameters in their declared locations. Preserve strings that resemble numbers and inspect unknown-parameter warnings.

Use `--input-json` when the published machine contract supports it and typed values, nested bodies, or conflicting parameter names require explicit locations. Its envelope has optional `path`, `query`, and `header` objects. A body uses `body.contentType` and `body.value`. Supply only needed locations and values; omission and explicit JSON `null` differ.

For example, the Hacker News newest feed uses a path parameter. Read its current docs before reuse:

```bash
agent-data docs c96b10fb-7db3-4761-8b45-be46c4825d78
agent-data call c96b10fb-7db3-4761-8b45-be46c4825d78 feeds-by-feed \
  --input-json '{"path":{"feed":"newest"}}'
```

`--method` disambiguates routes when necessary. `call --dry-run` displays the resolved request without executing the data route, but still fetches docs over the network; it does not validate returned data.

For direct HTTP or application code, use the published URL, authentication, method, and serialization contract. Do not derive URLs from handles or assume MCP inputs accept the CLI envelope.

## Inspect account information or send a notification

`agent-data account` inspects identity, allowance, and credits. It does not authorize changing billing or account policy.

For an authorized report notification, save and check the report first, then preview it:

```bash
agent-data notify --subject "Daily report" --dry-run < report.md
```

Remove `--dry-run` to send the checked report when sending is within the user's request. `--body` can supply Markdown directly and takes precedence over stdin. This release requires a nonempty body, accepts at most 32,768 UTF-8 bytes after trimming, and requires a subject of at most 200 characters without line breaks. Preserve the full report if a shorter email or link is needed.

`notify` authenticates and sends to the account's email address; it has no arbitrary-recipient option and is unbilled. A successful response supplies `sent`, `to`, `subject`, and `message_id`; it indicates provider acceptance, not confirmed inbox delivery. There is no public idempotency-key option. Retain the workflow's report/run identity and returned message ID, check prior send state before sending again, and do not blindly retry an ambiguous timeout: the first attempt may have sent.

The CLI does not schedule recurring runs. Scheduling, durable workflow state, and duplicate-notification handling belong to the calling workflow and its execution environment.

## Capture output and recover from errors

Search and docs produce JSON. Successful calls pass through the upstream body, which may be JSON or text; help/setup are not JSON APIs, and build events may stream. Capture stdout, stderr, and exit status before parsing. CLI errors use stderr and a nonzero status; a warning accompanying successful output is different from a failed request.

For large results, retain the complete output artifact and inspect selected fields. Keep source/retrieval metadata needed by the task. Pagination, caching, freshness, and rate limits are API-specific; consult the selected contract and responses.

- Correct invalid inputs using the contract rather than retrying the same invalid request.
- Resolve authentication, access, or allowance errors before repeating the affected request; report the dependency without changing account policy.
- For retryable reads, follow returned retry timing and keep retries proportionate to the task. If the same failure persists without changed prerequisites or new evidence, report it and preserve successful partial results.
- After a timeout or display failure, inspect retained output and request IDs before repeating work. Calls may incur another charge; mutations need their own recovery semantics.

An empty result and a transport failure are different outcomes. Preserve their actual error codes, messages, validation details, and request identifiers.
