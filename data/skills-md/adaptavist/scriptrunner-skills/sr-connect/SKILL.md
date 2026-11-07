---
name: sr-connect
description: >-
    ScriptRunner Connect (SR Connect, SRC), Adaptavist's code-first iPaaS: whether and how a
    service can be integrated, workspaces, connectors, managed APIs, event listeners, scheduled
    triggers, record storage, runtime limits, plans and hosting, and doing the work through the
    @sr-connect/cli. Use for any SRC, ScriptRunner Connect or Atlassian-integration question, and
    load references/ before running the CLI.
metadata:
    version: '1.14'
---

# ScriptRunner Connect

This file answers theory. Before touching the CLI read `references/cli-workflow.md`. Before writing a script read `references/scripting.md`, and the one file under `references/product-gotchas/` for each product the script calls, where one exists. Read `references/testing.md` only when the user asks for tests.

## Before the first CLI call

Settle which command to invoke, once per session, ahead of every other CLI step.

1. `command -v sr-connect`. A hit means the CLI is installed and on PATH: call it as `sr-connect <group> <verb>` everywhere, including in commands handed to the user. No hit: call it as `npx @sr-connect/cli <group> <verb>`, and pin the session's first call to `npx @sr-connect/cli@latest` so the cached copy is current.

    On a miss, tell the user one plain line, so it does not read as something broken: npx works and there is nothing to fix; for faster calls they can install it globally with `npm install -g @sr-connect/cli`. npx checks its cache on every call, which costs several seconds a call, 4 to 10 s in one agent's measurement. A project-local install does not put `sr-connect` on PATH, so it does not help. Under nvm a global install belongs to the active Node version, and switching versions takes `sr-connect` off PATH again. If the user installs it mid-session, run this step again so the session switches to `sr-connect`.
2. `<cli> cli check-updates --agent --raw`. The document carries `updateAvailable`, `current` and `latest`, plus `command` when there is an update. Exit 1 is a registry it could not read and exit 4 is a registry publishing no release; neither blocks the work, so say so and carry on with the version in hand.
3. When `updateAvailable` is true, name both versions, link the changelog (https://cdn.jsdelivr.net/npm/@sr-connect/cli@latest/CHANGELOG.md) so the user can see what changed, and ask whether the user upgrades it or you do. Never upgrade without that answer.

The `command` field is the upgrade line derived from how this copy was installed, and it is right for npm, pnpm, bun and npx. It is wrong for two installs the CLI reads as npm, so check for them before quoting it: resolve `sr-connect` to its real path, or run `yarn global bin` and `volta which sr-connect`.

| Install                                      | Upgrade with                                                          |
| -------------------------------------------- | --------------------------------------------------------------------- |
| npm global                                   | `npm install -g @sr-connect/cli@latest`                               |
| pnpm global                                  | `pnpm add -g @sr-connect/cli@latest`                                  |
| bun global                                   | `bun add -g @sr-connect/cli@latest`                                   |
| Yarn 1 global                                | `yarn global upgrade @sr-connect/cli`                                 |
| Volta                                        | `volta install @sr-connect/cli@latest`                                |
| npx, or Yarn 2+, which has no global install | nothing to upgrade; run the next call as `npx @sr-connect/cli@latest` |

When the user runs it, hand them the one line, without `--agent` or `--raw`, and wait. When you run it, run that same line and re-run `cli check-updates` to confirm the new version answered.

The snapshots in this file, the connector table, limits, plans and package list, are dated 2026-09-12 and carry their source URL. Re-fetch the source when an answer hinges on the number.

## Is this skill current

Once per session, before the first CLI call. Compare hashes when you can, and fall back to comparing versions when you cannot. With no network, skip it: say so in one line and carry on with this copy.

1. Find the hash of the installed copy. A project lockfile wins over the home one. No lockfile with an `sr-connect` entry means no hash: go to the version check below.
    - `./skills-lock.json` at the project root, which a project install by a recent `npx skills` writes. Its `computedHash` hashes the installed files a way GitHub does not, so do not compare it. Compute the git tree sha of the installed folder instead, which needs `git`; without it, go to the version check. Set `s` to the folder this `SKILL.md` was loaded from. The config flags and the `.DS_Store` sweep keep the user's git settings and Finder's files out of the hash:

        ```bash
        s=.agents/skills/sr-connect; d=$(mktemp -d) && cp -R "$s/." "$d" && find "$d" -name .DS_Store -delete && git -C "$d" init -q && git -C "$d" -c core.excludesFile=/dev/null -c core.attributesFile=/dev/null -c core.autocrlf=false add -A -f && git -C "$d" write-tree; rm -rf "$d"
        ```

    - `./.agents/.skill-lock.json` or `~/.agents/.skill-lock.json`: read `skills["sr-connect"].skillFolderHash`, which is already the git tree sha of `skills/sr-connect` in the published repo.
2. Fetch the published sha of that folder. The endpoint is unauthenticated and lists every skill in the repo:

    ```bash
    curl -s 'https://api.github.com/repos/adaptavist/scriptrunner-skills/contents/skills?ref=main'
    ```

    Take `sha` from the entry whose `name` is `sr-connect`. A 403 means GitHub's limit of 60 unauthenticated calls an hour per address ran out: go to the version check.

3. Equal hashes: say nothing. Different hashes: tell the user this copy differs from the published skill, which usually means it is behind, and recommend updating, strongly, since the published copy holds guidance this one lacks. Offer to run the update for them, or to hand them the line to run themselves, and say that either way the new files load from their next session, not this one, so the current session carries on with this copy. Wait for their answer. Do not run it without one.

    ```bash
    npx skills@latest update sr-connect
    ```

The version check, for when there is no hash to compare. Fetch the published `SKILL.md`, which is not subject to the API limit:

```bash
curl -s 'https://raw.githubusercontent.com/adaptavist/scriptrunner-skills/main/skills/sr-connect/SKILL.md'
```

Read `metadata.version` from its frontmatter and from this file's, and compare them part by part as numbers, so `1.10` is newer than `1.9`. A newer published version means this copy is behind: tell the user as for different hashes above. The same version, or a fetch that fails: say nothing. The version moves once per release that changes the skill, so it misses a release that went out without a bump. The hash catches every change, which is why it comes first.

## What it is

ScriptRunner Connect is a general-purpose, code-first integration platform as a service. You write TypeScript scripts that run in a managed runtime, wire them to events from external apps or to a schedule, and call other apps through typed clients. Coverage is deepest for Atlassian and the business tools around it, but the platform is not limited to them. Being code-first makes it a good fit for agents: everything an integration needs is a script, a configuration record, or a CLI verb.

Terminology: the official word for an external system is app. Use it.

## Can it integrate X

Two prerequisites. If both hold, the answer is almost always yes.

1. The app is reachable from the internet. SRC is SaaS. Its outbound calls leave from one static IP per instance, EU `34.251.34.27` and US `35.163.23.171`, which a firewall can allowlist to reach an on-premise network. A reverse proxy in a DMZ is the other route. For clients who cannot open a path at all there is private cloud hosting: the SRC team runs the product in an AWS account dedicated to the client, optionally inside the client's own VPC, reaching internal services directly, optionally cut off from the internet.
2. The app has an HTTP API.

A non-HTTP protocol needs an HTTP layer in front of it, which the client sets up. SQL databases are the usual example.

Inbound traffic to SRC, meaning webhooks, arrives through a cloud gateway with no static IP; a restricted network sending webhooks needs egress to the internet. OAuth consent needs a browser that can reach both the app and SRC.

Sources: https://docs.adaptavist.com/src/latest/get-started/connect-to-services-behind-the-firewall, https://www.scriptrunnerhq.com/scriptrunner-connect/private-cloud-hosting

## The building blocks

Five constructs. An event listener receives an event from an app and invokes a script. The script imports API connections to talk to apps. An API connection substitutes base URL and auth headers, using a connector, which is an authorized account. Everything lives in a workspace. Scripts can also run manually, from a schedule, or from another script.

Glossary, docs word first, CLI group second:

| Concept                                                              | Docs                | CLI                                     |
| -------------------------------------------------------------------- | ------------------- | --------------------------------------- |
| Container for one integration                                        | workspace           | `workspace`                             |
| Authorized account for an app, owned by a user, shared through teams | connector           | `connector`, `connector-sharing`        |
| Outbound client a script imports from `./api/<path>`                 | API connection      | `api-connection`                        |
| Typed client package behind an API connection                        | Managed API         | `package` (type MANAGED_API)            |
| Inbound trigger bound to an app event type                           | event listener      | `event-listener`                        |
| Stored sample event for a manual run                                 | test event payload  | `event-listener-test-payload`           |
| Per-environment typed configuration                                  | parameters          | `environment-parameter`                 |
| CRON-driven run                                                      | scheduled trigger   | `scheduled-trigger`                     |
| FIFO processing for a listener's events                              | event queue         | `event-queue`                           |
| Editable working version of a workspace                              | HEAD                | an environment with no `release` field  |
| Immutable snapshot                                                   | release, deployment | `release create -e <env>`, one call     |
| Space an environment's config lives in, targets HEAD or a release    | environment         | `environment`; `-e` takes its ID        |
| Editing lock, shared with the web app                                | none                | `workspace-lock`                        |
| Team allowlist of outbound destinations, connectors and hostnames    | Egress Firewall     | `egress-firewall`                       |

## Capabilities

### Workspaces, HEAD, releases, environments

A workspace holds scripts, API connections, event listeners, scheduled triggers, packages, parameters and a README. It belongs to at most one team; visibility is private, meaning team admins and you, or public, meaning every team member. Language is js, ts or ts-strict. Always use ts-strict.

HEAD is the working version and is always editable. A release is a snapshot of HEAD, scripts, README and the release-level configuration of listeners, API connections and triggers, and it cannot change afterwards. Versions are semver and must increase. `release create -e <env>` cuts the release and deploys it into the environment in one call; `environment target-release` only moves an environment onto an existing release or back to HEAD. An environment targets HEAD or a single release and holds its own environment-specific configuration: the connector on each API connection, the connector and setup state on each event listener, a generic listener's URL path, each scheduled trigger's CRON and enabled state, each queue's enabled state, and parameter values. That configuration stays editable in a released environment; everything else is read-only there, and a resource created after the release is out of scope until a release containing it is deployed.

Every workspace starts with a single environment named Default on HEAD. Default is its name; the CLI addresses it by the ID `environment list` reports. Keep exactly one environment on HEAD and develop there; fix forward with a new release rather than editing an old one. Rolling back means pointing the environment at an older release or back at HEAD. Scripts read `context.environment.name`; `context.deployment` is undefined on HEAD.

Source: https://docs.adaptavist.com/src/latest/workspaces/deployments-and-environments

### Parameters

Typed, per-environment values a script reads from `context.environment.vars`, one level of folders allowed. Eleven types, from TEXT and NUMBER to LIST, MAP and FOLDER; the type cannot be changed later. A default value seeds new environments and workspace copies, but the value itself is not copied and a default is not read at runtime. A required parameter blocks saving in the web app until it has a value; the CLI does not enforce it, so a required parameter can still be unset. For that reason `ev-params.ts` declares every parameter optional, required or not, and a script checks a value is present before using it; a required one is marked `Required: yes` in its JSDoc there.

A PASSWORD never reaches the script. The code sees a placeholder and so do the logs, and the real value is substituted only into an outbound HTTP call. So a password cannot be hashed, signed or base64-encoded in code; anything needing runtime handling goes in a TEXT parameter created with `--masked`. The full type table, the content types the substitution covers and the `ev-params.ts` consequences are in `references/scripting.md`.

**Never read parameter values without the user's explicit permission.** `environment-parameter list` returns them, and TEXT, MULTILINE_TEXT and MAP parameters can hold secrets that are not typed PASSWORD, masked TEXT among them. To see what exists, clone the workspace and read `ev-params.ts`: every parameter with its description, type and requiredness, and no values. `references/cli-workflow.md` has the rule under Posture.

Source: https://docs.adaptavist.com/src/latest/workspaces/parameters

### API connections and Managed APIs

An API connection is the outbound side: a path unique in the workspace, a vendor API package, and a connector per environment. Scripts import it, `import JiraCloud from './api/jira/cloud'`. Three tiers of abstraction, highest available wins: a Managed API, the typed client mirroring the vendor API one to one as in `JiraCloud.Issue.getIssue({ issueIdOrKey })`; managed `fetch` on the connection, where base URL and auth are supplied and you write the HTTP; and raw global `fetch`, where nothing is supplied. Managed APIs exist for every connector app; there is no public per-app reference, the typings in the workspace are the reference. monday.com's Managed API is GraphQL-shaped and takes `args` and `fields`. What a product's API, Managed API and event types do that the typings do not say, deprecated methods that answer 410, fields the event types leave out, is one file per product under `references/product-gotchas/`; load a file only when a script calls that product or handles its events, as `references/scripting.md` describes under Product gotchas.

Sources: https://docs.adaptavist.com/src/latest/workspaces/api-connections, https://docs.adaptavist.com/src/latest/managed-apis, and for the GraphQL shape https://docs.adaptavist.com/src/latest/managed-apis/managed-api-for-monday.com

### Event listeners

An event listener binds an app event type to a script, optionally through a connector and an event queue. The event type, script and queue are workspace-level and captured by a release; the connector, URL path and enabled state are per environment. Creating a script from the listener gives it the right typed event. Setup is finished by a human registering a webhook in the app; the CLI returns `webhookUrl`, the callback to register, and `setupUrl`, the instructions. Most apps cannot register webhooks programmatically. A new environment needs the connector relinked and setup redone: the listener exists there and reports `disabled: false`, but its URL path is per environment and a fresh environment has none, so `event-listener get -e <env>` shows `urlPath` and `webhookUrl` as null and the listener is enabled yet unreachable. The first `event-listener update` in that environment assigns one, `--url-path` for a generic listener, a no-op update such as `--disabled false` for the rest, and the resulting `webhookUrl` differs from HEAD's, so the webhook is registered again. Most listener types need no connector at all; `event-listener get` reports `connectionRequired` for the ones that do. Still, when the team already has an authorized connector for the app, attach it: the setup instructions improve, because the app's base URL comes from the connector and the webhook deep link is built on it. When there is none, leave the listener without one; never make a connector just to give a listener one. Test event payloads run the listener with a stored sample; a new listener gets a seeded Default payload sampling its event type. The registration steps for each app, what the app can filter on its side and how its webhook is secured are one file per app under `references/event-listener-setup/`; load a file only when handing the registration to the user, as `references/cli-workflow.md` describes under Webhook handoff.

Sources: https://docs.adaptavist.com/src/latest/workspaces/event-listeners

### Generic event listener

The Generic app's HTTP_ENDPOINT listener type. It accepts any HTTP request on a URL path that is unique across the whole platform and hands the request to a script: method, path, query, headers, source IP and a body parsed by content type into `json`, `text` or `base64`. Two modes. Async is the default: the caller is answered at once with an acknowledgement carrying the invocation ID, and the script runs afterwards under the usual 15-minute limit. Sync makes the caller wait for whatever the script returns, status, headers and body, within 25 seconds; past that the caller gets 408, and a response of the wrong shape gets 422.

Its primary purpose is to receive events from apps SRC does not support out of the box: anything that can send an HTTP request can trigger a script. It also covers apps that have no webhooks of their own when something else can be made to send the event. Confluence Cloud is the standing example: it offers no webhooks, so it has no listener type, but ScriptRunner for Confluence Cloud can listen to events inside Confluence and forward them to a generic listener's URL, which gives SRC a Confluence Cloud event feed after all. Two more apps reach SRC the same way. Trello has an API that registers a webhook, so point that webhook at a generic listener. Google Calendar and Google Sheets have no connector-level events, but Google Apps Script can watch the calendar or sheet and post to a generic listener's URL.

Because the sync mode sends a response back, the listener is also a way to publish something rather than only to receive. A script that answers with JSON is a small API of your own, in front of any system the workspace can reach, with SRC handling hosting, auth headers and logging. A script that answers with HTML is a custom user interface: a status page, a form, a lookup screen, served from the workspace with no separate web host. Between those two, the same listener adds security a plain webhook lacks: check a shared secret header, allowlist `sourceIp`, or validate a signature before doing anything, since the endpoint is otherwise anonymous.

A Generic listener with no check in its script is protected only by the secrecy of its URL, and URLs leak: chat messages, browser history, proxy logs, screenshots, shared documents, notification payloads. Treat any endpoint that reads non-public data, changes state or triggers scripts as one that needs authentication. When you build such an endpoint, add the check without being asked and say in the closing summary that you did; leave it out only for a pure public sink, and say that too. The default check is a shared-secret header compared against a masked TEXT parameter, failing closed; the code is under Generic HTTP events in `references/scripting.md`. A link posted to Slack or an email must not carry the secret: link to a page that asks for it, or put a short-lived signed token in the link instead.

Source: https://docs.adaptavist.com/src/latest/workspaces/event-listeners/generic-http-events

### Scheduled triggers

Run a script on a six-field CRON, seconds first, in UTC. Minimum interval 15 minutes; tighter schedules are raised to it, and minute intervals should be multiples of 15. The CRON and enabled state are per environment; the script is shared. A trigger created after a release is inactive in a released environment until that environment is redeployed.

Source: https://docs.adaptavist.com/src/latest/workspaces/scheduled-triggers

### Event queues

Default processing is concurrent. A queue makes a listener's events FIFO, split into independent streams by up to 10 dot-path groupings from the payload, `issue.key` for example. Eviction policy: a maximum queued time in minutes and an action, process out of order or drop with an email. Queued runs see `context.queue.{id,name,groupId}` and `context.queuedAt`. Paid non-legacy plans only; `team get` reports `features.eventQueues`.

Source: https://docs.adaptavist.com/src/latest/workspaces/event-queues

### Packages

Three classes. Core packages, `@sr-connect/convert`, `record-storage` and `trigger`, and the event libraries `@sr-connect/<app>` arrive with the listeners you create. Managed API packages, `@managed-api/<service>[-v<N>]-sr-connect`, arrive with the API connections you declare. Third-party NPM packages are added by hand. All three classes are pinned at the version current when added and upgraded by hand; the one exception is `@sr-connect/runtime-types`, which tracks latest and cannot be changed. ESM imports only. Add `@types/<name>` beside a package without its own types. Packages built only for Node do not work; the runtime is a web-standards subset. The product's verified list is in `references/scripting.md`.

Source: https://docs.adaptavist.com/src/latest/workspaces/package-manager

### Record storage

A key-value store scripts use for state across invocations: get, set, delete, exists, list keys. Scopes are environment, the default, workspace, team and invocation. Options: TTL, encryption, deny-overwrite. A plain write overwrites, last writer wins; a write with deny-overwrite is an atomic create-if-absent, exactly one of several racing writers succeeds, which is what makes a lock, an idempotency guard or an append log possible. Rate-limited per team with automatic retry. Capacity is per plan; see Limits.

Source: https://docs.adaptavist.com/src/latest/scripting/record-storage

### Triggering scripts from scripts

`@sr-connect/trigger` fires another script of the same environment asynchronously with a JSON payload and returns an invocation ID. Used to fan out work and to build long-running jobs, a migration for one, as a chain of invocations each under the 15-minute limit with progress kept in record storage. Chains are capped; see Limits. A working example is the Tempo Cloud worklogs migration template, https://templates.scriptrunnerconnect.com/template/tempo-cloud-worklogs-migration?expand=true.

Source: https://docs.adaptavist.com/src/latest/scripting/triggering-scripts

### Connectors and sharing

A connector holds an app's credentials, is created outside any workspace, belongs to a user and is looked up through a team. Sharing has three levels. Use lets someone attach it in workspaces, in all teams or named ones. Edit adds renaming and re-authorizing. Own adds sharing and deleting and stays with the creator. Connectors attached to a team workspace are implicitly usable by team members. Revoking Use, narrowing team scope, or leaving the team forcibly detaches the connector from workspaces. Most connectors authorize in a browser; the CLI creates one unauthorized and returns the URL. `connector list` and `connector get` report the base URL a connector points at, the Atlassian site or self-managed host it was authorized against. That host is the best evidence of which installation a connector reaches, and it often settles whether an environment is production. Names settle nothing, since two connectors called Jira Cloud can point at a sandbox and a live site. `connector list --app-id <appId>` gives it for every connector of one app in a single call. The field is absent while a connector is unauthorized. It is absent too, authorized or not, for an app whose connector records no host: GitHub, Azure DevOps, Bitbucket Cloud, Microsoft Teams, NetSuite, Zoom and Statuspage, so an absent field says nothing about those. Jira and Confluence Cloud, the on-premise connectors, GitLab, Zendesk, ServiceNow, Salesforce, monday.com and Opsgenie record the customer's own host, and those are the ones where reading the base URL earns its keep. Slack records the app's configuration page on api.slack.com, which separates nothing from anything but is the page its event listener is registered on. Snapshot 2026-09-14, read from a Jira Cloud connector, a Slack connector and an unauthorized GitHub connector; the rest of the two lists follows from which connectors store a host at all. The `connector list` fields rechecked 2026-10-16.

How each app's connector is authorized, which methods its wizard offers and the fixed-key alternative through a Generic connector are one file per connector type under `references/connector-setup/`; load a file only when a connector has to be authorized or re-authorized, as `references/cli-workflow.md` describes under Connector setup.

The Generic connector reaches any HTTP API: base URL plus none, basic or custom headers. It does not do OAuth 2.0; for that, see the recipe in `references/scripting.md`. Its API connection exposes `fetch` only, and a Managed API can be built on it by passing `connectionId` to the `<Product>Api` class from the matching `@managed-api/*-sr-connect` package.

Sources: https://docs.adaptavist.com/src/latest/connectors, https://docs.adaptavist.com/src/latest/connectors/generic-connector

### Egress Firewall

A team-level allowlist of where scripts may send requests. A script's outbound call runs only when its destination has an approved entry, and the kinds of entry never cover each other:

- A connector entry allows the requests a script makes through that connector: the Managed API, and managed `fetch` on the API connection.
- A Fetch API destination entry allows raw global `fetch` calls to one hostname. `https://API.Example.com:8443/v2` is stored as `api.example.com`, subdomains are separate entries, and wildcards are refused. So are `localhost` and private, loopback and link-local addresses such as `10.0.0.1` or `192.168.1.1`, which scripts cannot reach whatever the list says; a hostname that resolves to one is accepted and still fails at run time.

Allowing a Generic connector for `https://api.example.com` does not allow `fetch('https://api.example.com/...')`, and allowing the hostname does not allow the connector.

An entry is either approved or waiting for approval. It is approved on the spot only when the person adding it has the Admin or Super Admin role in the team, the request did not opt out of auto-approval, and the team's connections allowance has room. Otherwise it is recorded as a request and the team admins are emailed. A full allowance is not an error: the entry is created and waits. The allowance is the plan's connector count, `connections` on `team get`, where `max` is null for an unlimited plan. Approved entries use it, including an approved connector entry no API connection uses any more (`usedByApiConnection: false`), which keeps its place until it is removed; waiting entries do not, and neither do the two public ScriptRunner Connect API hosts, `api.scriptrunnerconnect.com` and `api.us.scriptrunnerconnect.com`, which still need an entry like any other destination but are marked `exemptFromLimit: true` in `egress-firewall list`.

Once an entry exists, one thing changes it: the connector changing tenant. Re-authorizing a connector against a different Atlassian site, Slack or Bitbucket workspace, NetSuite account, self-managed GitLab host or Microsoft tenant, or `connector update` moving a Generic base URL to another host or port, sends every approved entry for that connector back to waiting, in every team it is allowed in, and emails each team's admins; the connector is blocked until an admin approves it again. Apps that store no tenant (GitHub, GitLab.com, Google Sheets, Calendar and Drive, Zoom, Trello, Statuspage, AWS, JSM Cloud Assets, Microsoft and Azure DevOps on the shared app) do the same on every re-authorization of an already authorized connector. The same tenant, a renewed credential, a header edit or a path change on the same host change nothing, and the first authorization of a new connector never does. A team whose `connections.used` on `team get` exceeds `max` cannot approve the entry again until it removes something or upgrades, so never re-authorize or re-point an approved connector in such a team without the user's say-so. Otherwise a waiting entry stays waiting when an admin adds it again with auto-approval, and when an API connection attaches the connector again. Adding one again is safe: both kinds answer with the stored entry, unchanged. Approving, rejecting and removing happen in the web app only, under Team Settings, Egress Firewall. Deleting a connector removes its entry and frees its place in the allowance; a Fetch API destination can only be removed there. Making room approves nothing: an entry that was waiting for room still waits, now for an admin to approve it.

Attaching a connector to an API connection puts it on the allowlist in the same call, approved when the rules above allow it, and `api-connection create` and `update` report `egressFirewall.state` for the connector attached: approved, waiting, not listed, or no firewall on the deployment. A waiting entry also says what stands between it and approval for the caller, on every write and in the list: the allowance is full, in which case nobody can approve it until room is made; the caller is not a team admin; the call asked for approval; or nothing, and the caller can approve it themselves in the web app. `egress-firewall check-api-connections` reads the same for every API connection in one environment at once. A connector cannot be added on its own until an API connection in the team uses it.

A blocked call fails the run with error code 11007. The messages, as the runtime writes them:

```text
Request blocked by the team's Egress Firewall.
google.com is not on the allowed destinations list. A team admin can allow it under Team Settings → Egress Firewall. - ScriptRunner Connect Error code: 11007
```

```text
Request blocked by the team's Egress Firewall.
The "Jira Cloud" connector is not on the allowed connectors list. A team admin can allow it under Team Settings → Egress Firewall. - ScriptRunner Connect Error code: 11007
```

A different error means something else. Error code 10001 is the runtime failing a connection, and it is checked before the firewall. `Connection not allowed for URL` means a hostname that does not resolve or an address scripts cannot reach, and is fixed in the URL or DNS, never in the allowlist. The other 10001 messages name the cause. One saying the service that makes the call ran out of memory, or that the response is too large to return to the script, means a response too big to bring back: fetch in smaller pages or use the vendor's export. One saying the call timed out means the remote host took too long to send the full response. `Error while performing HTTP call (Fetch API)` is what is left, a connector call that never received a response among it, and its text does not say whether the firewall is involved, so run `egress-firewall check-api-connections` in that workspace and environment. `APPROVED` there means look at the vendor, the connector's base URL or the connection; any other state is an entry to fix, since it would block the call as well. Only 11007 with "Request blocked by the team's Egress Firewall" is the firewall's own answer.

A deployment says whether it has a firewall. A private cloud instance can run without one; there `egress-firewall list` is refused with `EGRESS_FIREWALL_DISABLED`, nothing is filtered, and nothing here applies. A deployment that predates the feature answers the same read with `Path not found`, exit 4, and filters nothing either. Assume the firewall is on until one of those answers says otherwise. How the agent asks about approval, adds entries and stops for a human is under Egress Firewall in `references/cli-workflow.md`.

### Teams

Three roles. A Member sees workspaces shared with them, usage and the member list. An Admin also opens every team workspace, invites, edits roles below super admin, changes sharing settings and moves a workspace between teams they admin. A Super Admin also edits every role, the plan and billing, and can delete the team. One person edits a workspace at a time; others get a read-only copy and can take edit control. The CLI's workspace lock is that same control.

Source: https://docs.adaptavist.com/src/latest/collaborate-with-teams

### Observability

Invocation logs are kept six months, per team. Each row has a status, one of Finished, Running, Denied, Timed out, Aborted, Function Error, Malformed Payload Error and Runtime Error; a trigger type, one of Manual, Manual Event Listener, External, Chained and Scheduled; and the console and HTTP log counts. Console logs cap at 1,000 lines per invocation; a line too large is stored separately. HTTP logs record every outbound call with headers and bodies truncated over 1 KB. Audit logs record every user action, six months. Replay re-runs an event-triggered invocation with an editable payload (not manual or scheduled runs, 4 MB cap). Script failure notifications email on uncaught errors, per user, per workspace and environment.

Source: https://docs.adaptavist.com/src/latest/observability

### Security

AWS, in EU Ireland or US Oregon, chosen at signup; no data is stored outside the chosen region. Credentials encrypted with AWS KMS AES-256-GCM, TLS 1.2 in transit. Scripts run in fresh V8 isolates; enhanced isolation gives a tenant its own compute, at the price of more cold starts. ISO 27001, SOC 2 Type 2, GDPR, CREST-tested, Bugcrowd bounty. The in-app AI features use OpenAI models, with no training on your code.

Source: https://docs.adaptavist.com/src/latest/security

### Templates

A template is a published workspace: connections, triggers and code for one use case. Most are examples. The Sync and Migration categories hold ready-made integrations worth starting from when the use case matches. Procedure: `template list` gives IDs and preview URLs; for a sync or migration ask also read the public library at https://templates.scriptrunnerconnect.com/ where `sitemap.xml` lists every template and `/template/<slug>?expand=true` renders the full README and source. Create from one with `workspace create --source-template-id`; the language is inherited, so upgrade it to ts-strict afterwards.

Source: https://docs.adaptavist.com/src/latest/templates

### REST API and the CLI

Basic auth with the account email and an API key created under the user menu, API Keys; the key is shown once. Base URLs are `https://api.scriptrunnerconnect.com` for EU and `https://api.us.scriptrunnerconnect.com` for US. The CLI `@sr-connect/cli` is the client for it and covers workspaces, environments, parameters, scripts, listeners, payloads, queues, API connections, connectors, sharing, packages, releases, locks, logs, replay and abort.

Source: https://docs.adaptavist.com/src/latest/rest-api

### AI assistant

The web app has a built-in assistant. When working from outside, use your own capabilities and ignore it.

### Plans and hosting

| Plan       | Connectors | Executions per month    | Event queues | Hosting                           |
| ---------- | ---------- | ----------------------- | ------------ | --------------------------------- |
| Free       | 4          | 5,000                   | no           | shared AWS, EU or US              |
| Basic      | 4          | unlimited (500,000 cap) | yes          | shared AWS                        |
| Advanced   | 8          | unlimited               | yes          | shared AWS                        |
| Pro        | unlimited  | unlimited               | yes          | shared AWS                        |
| Enterprise | unlimited  | unlimited               | yes          | private AWS account, optional VPC |

A plan belongs to a team and its limits are shared by every workspace in the team. The Connectors column is the team's connections allowance, which approved Egress Firewall entries count against; see Egress Firewall. SSO is a paid add-on below Enterprise. Free plan support is community only.

Source: https://www.scriptrunnerhq.com/atlassian-apps/jira/scriptrunner-connect-pricing

## Limits

Source: https://docs.adaptavist.com/src/latest/limits-and-quotas and the pages above.

| Limit                                                                       | Value                                                            |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Async invocation duration                                                   | 15 min                                                           |
| Sync HTTP invocation duration                                               | 25 s                                                             |
| Memory per invocation                                                       | 400 MB; paid plans can request an 800 MB variant through support |
| Event payload                                                               | 6 MB                                                             |
| Replay payload                                                              | 4 MB                                                             |
| Chained invocations                                                         | 200                                                              |
| Console lines per invocation                                                | 1,000                                                            |
| HTTP log body kept                                                          | 1 KB, then truncated                                             |
| Scheduled trigger interval                                                  | 15 min minimum                                                   |
| Queue groupings per listener                                                | 10                                                               |
| Log retention (audit, invocation, HTTP)                                     | 6 months                                                         |
| Record storage                                                              | Free 100 MB, Basic 1 GB, Advanced 5 GB, Pro 10 GB                |
| Per workspace: API connections, listeners, payloads, triggers, environments | 1,000 each                                                       |
| Deployments per workspace                                                   | 10,000                                                           |
| Workspaces, connectors per account                                          | 1,000 each                                                       |
| Script invocations (team)                                                   | Free 1/s, paid 100/s                                             |
| External API calls (team)                                                   | Free 5/s, paid 100/s                                             |
| Record storage calls (team)                                                 | Free 1/s, paid up to 50/s depending on plan; shared by every workspace and invocation |
| Trigger script calls (team)                                                 | Free 1/s, paid 10/s                                              |
| REST API calls (user)                                                       | Free 5/s, paid 20/s; shared by all of the user's API keys and agents |

## Runtime in one paragraph

Not Node. A custom V8 runtime on a web-standards subset, ES2020 in syntax and standard library alike, ESM only: `fetch` with fully buffered bodies, `Request`/`Response`/`Headers`/`URL`/`FormData`/`Blob`, `TextEncoder`/`TextDecoder`, `btoa`/`atob`, timers, `console`, `crypto.getRandomValues` and `crypto.subtle` for keys, sign and verify only. Every outbound call needs an approved Egress Firewall entry for its connector or, for raw `fetch`, its hostname. No `Buffer`, no `process.env`, no `node:*`, no WebSocket, no streams, no `subtle.digest`, and no library method or option newer than ES2020 until a probe proves it, `Intl.DateTimeFormat`'s `timeStyle` being the known casualty. `@sr-connect/convert` replaces Buffer conversions; `jose-browser-runtime` signs JWTs. Full table and the coding rules in `references/scripting.md`.

Source: https://docs.adaptavist.com/src/latest/scripting/runtime

## Connectors, snapshot 2026-09-15

Source: https://docs.adaptavist.com/src/latest/connectors and the web application's authorization wizards. Every connector has a Managed API. The live catalogue with IDs is `app list`; query it rather than trusting this table when building. The NPM names of each app's events library and Managed API package are in `references/scripting.md`; they cannot be derived from the app name in this table. The Auth column is the wizard's own method; the per-app steps are under `references/connector-setup/`.

| Connector                                 | Auth                                                        | Event listeners                        |
| ----------------------------------------- | ----------------------------------------------------------- | -------------------------------------- |
| AWS                                       | IAM role with a generated trust policy, or access key       | no                                     |
| Azure DevOps                              | OAuth 2.0, platform's Azure app or own                      | yes                                    |
| Bitbucket Cloud                           | OAuth 2.0, own OAuth client                                 | yes                                    |
| Bitbucket On-Premise                      | OAuth 2.0, own incoming application link                    | yes                                    |
| Confluence Cloud                          | OAuth 2.0, platform's app or own                            | no, bridge through a generic listener  |
| Confluence On-Premise                     | Application link with a generated key pair                  | yes                                    |
| GitHub                                    | OAuth 2.0, platform's GitHub app                            | yes                                    |
| GitLab                                    | OAuth 2.0, platform's app on gitlab.com or own              | yes                                    |
| Google Calendar                           | Google sign-in, platform's app                              | no, bridge from Google Apps Script     |
| Google Drive                              | Google sign-in, platform's app; platform-created files only | no                                     |
| Google Sheets                             | Google sign-in, platform's app                              | no, bridge from Google Apps Script     |
| Jira Cloud                                | OAuth 2.0, platform's app or own                            | yes                                    |
| Jira On-Premise                           | Application link with a generated key pair                  | yes                                    |
| Jira Service Management Cloud             | OAuth 2.0, platform's app or own                            | yes, through Jira Cloud webhooks       |
| Jira Service Management Cloud Assets      | Email and API token                                         | no                                     |
| Jira Service Management On-Premise        | shares Jira On-Premise                                      | yes                                    |
| Jira Service Management On-Premise Assets | shares Jira On-Premise                                      | no                                     |
| Microsoft                                 | OAuth 2.0, platform's Azure app (Teams only) or own         | yes                                    |
| monday.com                                | OAuth 2.0, platform's app installed by an admin             | yes                                    |
| NetSuite                                  | Client credentials with a generated certificate             | yes                                    |
| Opsgenie                                  | API key                                                     | yes                                    |
| Salesforce                                | OAuth 2.0, own Connected App                                | yes                                    |
| ServiceNow                                | OAuth 2.0, own OAuth API endpoint                           | yes                                    |
| Slack                                     | App ID, signing secret, bot token                           | yes                                    |
| Statuspage                                | API key                                                     | yes                                    |
| Tempo Cloud                               | OAuth 2.0, own application in Tempo                         | no                                     |
| Tempo Planner On-Premise                  | shares Jira On-Premise                                      | no                                     |
| Tempo Timesheets On-Premise               | shares Jira On-Premise                                      | no                                     |
| Trello                                    | API key and token from own Power-Up                         | no, register a webhook through its API |
| Zendesk                                   | OAuth 2.0, own OAuth client                                 | yes                                    |
| Zoom                                      | OAuth 2.0, own General app                                  | yes                                    |
| Generic                                   | none, basic, headers                                        | yes, generic HTTP events               |

Sample test payloads exist for most listener apps. Zoom, Azure DevOps, Microsoft, NetSuite, Salesforce and ServiceNow have none; write those payloads from what the app documents.

## Which kind of ask

| Ask                                           | First move                                                                                                                                                                  | Load                                               | CLI needed |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ---------- |
| Can SRC do X, how does X work                 | Answer from this file. If an existing workspace is named, read its setup first                                                                                              | `cli-workflow.md` only if reading a workspace      | sometimes  |
| Something fails, look at it                   | Ask for team, workspace, time span. Read invocation logs, then console and HTTP logs, then the script                                                                       | `cli-workflow.md`, then `scripting.md` and `product-gotchas/<app>.md` for the fix | yes        |
| Build or change an integration                | Gather requirements, probe connectors and environment, take the lock, clone                                                                                                 | `cli-workflow.md`, `scripting.md`, `product-gotchas/<app>.md` per product the scripts call | yes        |
| One-off job                                   | The short recipe in `cli-workflow.md`; ask whether it recurs, delete after if not                                                                                           | `cli-workflow.md`, `scripting.md`                  | yes        |
| Register a webhook, or events never arrive    | Read the listener and its connector, then load the one app file; see Webhook handoff in `cli-workflow.md`                                                                   | `cli-workflow.md`, `event-listener-setup/<app>.md` | yes        |
| Authorize a connector, or one stopped working | `connector list` and `connector get` first; load the one connector file only when a new or expired connector has to be authorized; see Connector setup in `cli-workflow.md` | `cli-workflow.md`, `connector-setup/<type>.md`     | yes        |
| A run fails with error code 11007             | The Egress Firewall blocked a destination. `egress-firewall check-api-connections` maps a connector name to its ID, `egress-firewall list` shows a host; see Egress Firewall in `cli-workflow.md` | `cli-workflow.md`                                  | yes        |
| A run fails with error code 10001             | `Connection not allowed for URL`: not the Egress Firewall, the hostname does not resolve or its address is private; check the URL and DNS and add no entry. Out of memory or too large: smaller pages. `Error while performing HTTP call (Fetch API)` on a connector call: `egress-firewall check-api-connections` first, see Egress Firewall | `scripting.md`, `cli-workflow.md`                  | sometimes  |
| Tests                                         | Only when asked                                                                                                                                                             | `testing.md`                                       | yes        |

When there is no bespoke connector, use the Generic connector for fixed-key auth. For OAuth, set the flow up in the workspace instead; the recipe is in `references/scripting.md`. When there is a bespoke connector but the user refuses every method its wizard offers, the app's file under `references/connector-setup/` names the fixed-key alternative through a Generic connector, where the vendor has one.

## Sending feedback

When the `agenticFeedback` switch is on, the work leaves notes for the ScriptRunner Connect team. What goes in them, when to post and the verb that sends them are under Feedback in `references/cli-workflow.md`. When the switch is off, the user has said no: no notes, no nudge to enable it, and no word about feedback in the summary.

## Asking questions

Front-load them. Before the first change, gather everything the work will turn on: which apps and which environments, what counts as production, whether a non-production instance of each app exists and, when none does, whether the user would get one (`references/dev-instances.md` says how quickly), whether you may probe and whether a probe may mutate, whether you may run a simulation loop with test payloads, whether you may auto-approve the Egress Firewall entries the work adds, which package upgrades are wanted, how the result will be tested end to end. One round of questions up front is cheaper for the user than a question every ten minutes, and it is what lets you go away, build in the simulation loop for as long as the user allowed, and come back once with something to test. Waiting is different from building: any one wait on the user, for an event they fire or an approval they give, stops at 30 minutes, as `references/cli-workflow.md` says under Posture.

VERY IMPORTANT: a request for a plan does not skip that round. A plan for an integration written without knowing which environments exist, what counts as production, or whether you may probe is a guess dressed as a plan. Whatever mechanism your harness has for putting questions to the user, plan mode included, use it for these questions before writing the plan. The plan depends on what the workspace and the target apps hold, so probing belongs before the plan and not after it, but only once the user has consented to probing. No consent means no probe: write the plan from the reads the CLI allows and what the user told you, and mark each place a probe would have settled.

Front-loading is not a licence to assume. When the work raises a question the answers did not cover, or a probe shows something that contradicts what you were told, stop and ask. A wrong assumption in an integration costs a round of debugging against a live system; a question costs a minute. Probe when probing would answer it; ask when only the user can. Never skip either to keep momentum.

An obvious match is still a guess. When the ask names a resource loosely, "the Jira connector", a script by half its name, and the lookup turns up exactly one plausible candidate, do not write to it on that basis. Name what you matched, by ID as well as name, say what you are about to do to it, and wait for the user. Reads need none of this, so probe first and bring the candidate to the question rather than asking which one they meant.

The single match is the trap, not the safeguard. A sandbox connector and a live one share a name more often than not, a script name repeats across workspaces, and the one candidate in view can be the only one because the scope was wrong. Where the ask is exact, an ID, or a name with nothing else close to it, go ahead.
