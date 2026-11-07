---
name: dscrd-auth
description: "Manage bot credentials"
metadata:
  version: 0.2.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - dscrd
    cliHelp: "dscrd auth --help"
---

# dscrd auth

Manage bot credentials

> **PREREQUISITE:** Read `../dscrd-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `dscrd generate-skills`.

| Command | Description |
|---------|-------------|
| `dscrd auth invite-url` | Generate the OAuth2 URL that invites the bot to a server |
| `dscrd auth logout` | Remove a stored profile |
| `dscrd auth rename` | Rename a stored profile |
| `dscrd auth set-token` | Store a bot token (prompted securely when --token is omitted) |
| `dscrd auth status` | List profiles and verify the active token |
| `dscrd auth switch` | Switch the active profile |
| `dscrd auth test` | Verify the active token against Discord |

## dscrd auth invite-url

Generate the OAuth2 URL that invites the bot to a server

```bash
dscrd auth invite-url [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--permissions` | — | `write` | permission preset (read\|write\|admin) or raw bit set |

## dscrd auth logout

Remove a stored profile

```bash
dscrd auth logout [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--name` | — | — | profile to remove (default: active) |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd auth rename

Rename a stored profile

```bash
dscrd auth rename <old> <new> [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--force` | — | — | overwrite the target profile if it already exists |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd auth set-token

Store a bot token (prompted securely when --token is omitted)

```bash
dscrd auth set-token [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--application-id` | — | — | application ID (for invite-url) |
| `--default-guild` | — | — | default guild ID or name |
| `--force` | — | — | overwrite the profile if it already exists |
| `--name` | — | `default` | profile name |
| `--token` | — | — | bot token (omit to be prompted) |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd auth status

List profiles and verify the active token

```bash
dscrd auth status
```

## dscrd auth switch

Switch the active profile

```bash
dscrd auth switch <name>
```

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd auth test

Verify the active token against Discord

**Discord API:** `GET /users/@me`

```bash
dscrd auth test
```


