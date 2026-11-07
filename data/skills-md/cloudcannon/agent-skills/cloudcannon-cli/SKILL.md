---
name: cloudcannon-cli
description: >-
  Use when running the CloudCannon CLI — logging in, listing or creating sites,
  reading and writing files on a hosted site, triggering and inspecting builds,
  changing a site's build configuration, reading form submissions, or finding
  out which command and flags exist for a task.
---

# The CloudCannon CLI

`@cloudcannon/cli` has two halves. The local half reads and writes files in the working directory and needs no account. The remote half talks to the CloudCannon API, needs credentials, and acts on live sites.

## When to use

- Finding out whether a command exists for a task, and what its flags are
- Authenticating, or setting the CLI up in CI
- Listing, inspecting, or creating sites and organisations
- Reading or changing files on a hosted site, and committing those changes
- Triggering a rebuild, or reading build and sync logs
- Changing an existing site's build configuration
- Listing form submissions

## When not to use

- **Deciding what belongs in `cloudcannon.config.yml`** — that is [`cloudcannon-configuration`](../cloudcannon-configuration/SKILL.md). This skill runs `configure` and `validate`; that skill owns what their output should say.
- **Running the site locally in CloudCannon** — `cloudcannon dev` is covered end to end by [`cloudcannon-dev-server`](../cloudcannon-dev-server/SKILL.md), including the rebuild loop and the `/__api` surface.
- **Calling the CloudCannon API from code** — that is [`cloudcannon-sdk`](../cloudcannon-sdk/SKILL.md). It also owns the surface no command reaches: DAMs, backups, sync history and pulls, site scans, screenshots, provider connections, `site.copy`, `site.delete`.
- **Authoring editable regions or snippets** — [`cloudcannon-visual-editing`](../cloudcannon-visual-editing/SKILL.md) and [`cloudcannon-snippets`](../cloudcannon-snippets/SKILL.md).

## The rule that costs the most

**MUST confirm with the user before any command that writes to a hosted site.**

**Why:** the remote half is not a sandbox. `sites files commit` pushes to the site's real git repository, `sites rebuild` starts a real build, and `sites update-build-config` changes how every future build runs. None of them prompt, and none are undone by re-running the command.

The read-only remote commands — every `list`, every `get`, every `print-*` — are safe to run unprompted.

## Local and remote

| Half       | Commands                                               | Credentials | Acts on                        |
| ---------- | ------------------------------------------------------ | ----------- | ------------------------------ |
| **Local**  | `configure detect-*`, `configure generate`, `validate` | None        | Files in the working directory |
| **Local**  | `dev`                                                  | None        | A built output directory       |
| **Remote** | `orgs`, `sites`, `builds`, `inboxes`, `login`/`logout` | Required    | Live sites over the API        |

**MUST NOT** assume a command is local because it reads rather than writes. `sites files get` reads, but reads it over the API from a hosted site.

## Requirements

Node 24 or newer (the current LTS). Install globally with `npm i -g @cloudcannon/cli`, or invoke with `npx @cloudcannon/cli <command>`.

## Quick start

```sh
# What commands exist, and what flags does one take
npx @cloudcannon/cli --help
npx @cloudcannon/cli sites files commit --help

# Local: generate and check a configuration
npx @cloudcannon/cli configure generate --auto --initial-site-settings
npx @cloudcannon/cli validate

# Remote: authenticate, then read
npx @cloudcannon/cli login
npx @cloudcannon/cli sites list
```

## Contents

| File                                       | Covers                                                                      |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| **SKILL.md** (this file)                   | Routing, the local/remote split, the live-site rule                         |
| [commands.md](commands.md)                 | The full command surface, and querying `documentation.json` for exact flags |
| [authentication.md](authentication.md)     | Credential methods, their precedence, where they are stored, CI setup       |
| [editing-sessions.md](editing-sessions.md) | `sites files` — the staged-changes model, committing, discarding            |
| [troubleshooting.md](troubleshooting.md)   | Symptom → cause → fix                                                       |

## Common mistakes

| Excuse                                                   | Reality                                                                                                                                                    |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "I'll write out the flags for this command from memory." | Flags change between releases. Query `documentation.json` or run `--help`. See [commands.md](commands.md#discovering-the-exact-flags).                     |
| "Build settings can only be changed in the dashboard."   | `sites update-build-config` changes them for an existing site. See [commands.md § Changing build configuration](commands.md#changing-build-configuration). |
| "I uploaded the file, so the site has it."               | An upload lands in an editing session, not the repository. It is not live until committed. See [editing-sessions.md](editing-sessions.md).                 |
| "The command printed nothing, so it failed."             | Read commands print JSON to stdout and nothing else. An empty result is an empty array, not an error — check the exit code.                                |
| "`--site` needs the UUID."                               | It accepts a name, ID, UUID, or domain.                                                                                                                    |
