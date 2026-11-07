---
name: cloudcannon-sdk
description: >-
  Use when calling the CloudCannon API from code — constructing a client,
  finding a site or organisation UUID, reading or writing files on a hosted
  site programmatically, triggering and inspecting builds, or reaching a
  CloudCannon endpoint the CLI has no command for (DAMs, backups, sync history, site
  scans, screenshots, provider connections, copying or deleting a site).
---

# The CloudCannon SDK

`@cloudcannon/sdk` is the REST API client the CloudCannon CLI is built on. It exposes a hierarchy of sub-clients over the API, plus a typed `fetch` that reaches endpoints no sub-client wraps.

Reach for it when the work is programmatic. Reach for the CLI when the work is a shell command.

## When to use

- Calling the CloudCannon API from a script, a build step, or a service
- Operating over many sites or organisations in one pass
- Reaching a surface the CLI does not expose — DAMs, backups, sync history and pulls, site scans, screenshots, provider connect/disconnect, `site.copy`, `site.delete`
- Handling API failures by type rather than by exit code
- Finding out which methods exist, and what they take

## When not to use

- **A one-off operation from a shell** — that is [`cloudcannon-cli`](../cloudcannon-cli/SKILL.md). If a command already does the job, use it; it resolves site names, prints JSON, and needs no client wiring.
- **Running the site locally in CloudCannon** — `cloudcannon dev` is covered end to end by [`cloudcannon-dev-server`](../cloudcannon-dev-server/SKILL.md). The SDK has nothing to do with it.
- **Deciding what belongs in `cloudcannon.config.yml`** — that is [`cloudcannon-configuration`](../cloudcannon-configuration/SKILL.md). The SDK reads and writes the file as bytes; it has no opinion on its contents.
- **Authoring editable regions or snippets** — [`cloudcannon-visual-editing`](../cloudcannon-visual-editing/SKILL.md) and [`cloudcannon-snippets`](../cloudcannon-snippets/SKILL.md).

## The rule that costs the most

**MUST confirm with the user before any call that writes to a hosted site.** This is the same rule the CLI carries, and the reason is the same — see [`cloudcannon-cli` § The rule that costs the most](../cloudcannon-cli/SKILL.md#the-rule-that-costs-the-most) for the canonical statement.

Two things make it easier to break here than at the command line:

- There is no command name to read as a warning. `site.delete()` is a method call with no arguments, no flag, and no confirmation prompt.
- The SDK reaches destructive endpoints the CLI has no command for at all — `site.delete()`, `site.copy()`, `disconnectSourceProvider()`, `disconnectOutputProvider()`.

The gate covers [`client.fetch`](api-surface.md#the-raw-escape-hatch) too. A `POST` through the escape hatch is a write.

## Requirements

Node 20 or newer, per the package's `engines` field — lower than the CLI's Node 24. The package is ESM (`"type": "module"`) and its default export is the client class.

```js
import CloudCannonClient from "@cloudcannon/sdk";
```

## Quick start

Sub-clients take a UUID and nothing else, so almost every task starts by finding one.

```js
import CloudCannonClient from "@cloudcannon/sdk";

// The SDK reads no credentials of its own — you supply them.
const client = new CloudCannonClient({
  userAccessKey: {
    id: process.env.CC_ACCESS_KEY_ID,
    secret: process.env.CC_ACCESS_KEY_SECRET,
  },
});

const { items: orgs } = await client.orgs();
const { items: sites } = await client.org(orgs[0].uuid).sites({ filters: { search: "my-site" } });

const site = await client.site(sites[0].uuid).get();
```

## Contents

| File                                       | Covers                                                                            |
| ------------------------------------------ | --------------------------------------------------------------------------------- |
| **SKILL.md** (this file)                   | Routing, the write gate, requirements                                             |
| [client.md](client.md)                     | Constructing the client, the config shape, and why it reads no credentials itself |
| [resources.md](resources.md)               | The sub-client hierarchy, UUID addressing, pagination, return types               |
| [api-surface.md](api-surface.md)           | Reading the authoritative method list, and the raw `client.fetch` escape hatch    |
| [editing-sessions.md](editing-sessions.md) | Writing files to a hosted site through the SDK                                    |
| [troubleshooting.md](troubleshooting.md)   | Symptom → cause → fix                                                             |

## Common mistakes

| Excuse                                                                   | Reality                                                                                                                                      |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| "I'll pass the site name to `client.site()`."                            | Sub-clients take a UUID only. Resolve it first — [resources.md § Addressing a resource](resources.md#addressing-a-resource).                 |
| "`client.sites()` will list every site I can see."                       | There is no such method. Sites are listed per organisation. See [resources.md](resources.md#finding-a-site-by-name).                         |
| "The SDK will pick up my `cloudcannon login` credentials."               | It reads nothing from disk or the environment. That chain is a CLI feature — [client.md](client.md#the-sdk-reads-no-credentials-of-its-own). |
| "I'll write out the method signatures from memory."                      | Signatures change between releases. Read them from the installed package — [api-surface.md](api-surface.md#reading-the-method-list).         |
| "`await site.getFile(path)` gives me the file contents."                 | It gives you a `Response`. Several methods do — [resources.md § What a method returns](resources.md#what-a-method-returns).                  |
| "The list came back, so that's all of them."                             | Paginated endpoints return one page. Check `total_pages` — [resources.md § Pagination](resources.md#pagination-sorting-and-filtering).       |
| "`client.fetch` is the low-level API, so the write gate is a CLI thing." | The gate is about the endpoint, not the wrapper. A `POST` through `fetch` writes to a live site exactly as a named method does.              |
