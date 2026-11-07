---
name: slk-auth
description: "Manage Slack credentials"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk auth --help"
---

# slk auth

Manage Slack credentials

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk auth login` | Run the OAuth flow with your own Slack app credentials |
| `slk auth logout` | Remove a profile |
| `slk auth revoke` | Revoke the active token at Slack (server-side) |
| `slk auth set-token` | Store a token for a profile |
| `slk auth status` | Show configured profiles |
| `slk auth switch` | Set the active profile |
| `slk auth test` | Verify the active token and show its live identity |

## slk auth login

Run the OAuth flow with your own Slack app credentials

**Slack API:** `oauth.v2.access`

```bash
slk auth login [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--client-id` | — | — | your Slack app client ID |
| `--client-secret` | — | — | your Slack app client secret |
| `--non-interactive` | — | — | never prompt; require values via flags |
| `--port` | — | `3000` | local callback port |
| `--profile` | — | `default` | profile name |
| `--scopes` | — | — | comma-separated scopes to request (default: generated from supported commands for the chosen identity) |

**Tips:** Run the OAuth flow with your own Slack app credentials. Pass values via flags for scripts/agents, or run with missing fields in a terminal to be prompted (the client secret is entered hidden). Use --as bot to mint a bot token instead of a user token.

## slk auth logout

Remove a profile

```bash
slk auth logout <profile>
```

## slk auth revoke

Revoke the active token at Slack (server-side)

**Slack API:** `auth.revoke`

```bash
slk auth revoke
```

**Tips:** Revoke the active token at Slack. This invalidates the token server-side; it does not remove the local profile (use `auth logout` for that).

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk auth set-token

Store a token for a profile

```bash
slk auth set-token [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--non-interactive` | — | — | never prompt; require values via flags |
| `--profile` | — | `default` | profile name |
| `--token` | — | — | token (xoxp- or xoxb-, or - to read stdin) |

**Tips:** Store a single token (user xoxp- or bot xoxb-) for a profile. Pass --token for scripts/agents (use --token - to read from stdin), or run in a terminal to be prompted (token entry is hidden). A profile holds exactly one token; its scope is derived from the prefix.

## slk auth status

Show configured profiles

**Slack API:** `auth.test`

```bash
slk auth status [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--all` | — | — | verify every profile live, not just the active one |
| `--offline` | — | — | skip the live Slack check; list local info only |

**Tips:** Show configured profiles with a derived [user]/[bot] scope label. By default the active profile is verified live (auth.test); --all verifies every profile, --offline skips the network. --format json emits a structured object.

## slk auth switch

Set the active profile

```bash
slk auth switch <profile>
```

## slk auth test

Verify the active token and show its live identity

**Slack API:** `auth.test`

```bash
slk auth test
```


