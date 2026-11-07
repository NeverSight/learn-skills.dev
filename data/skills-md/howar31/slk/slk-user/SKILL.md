---
name: slk-user
description: "List and inspect users"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk user --help"
---

# slk user

List and inspect users

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk user by-email` | Look up a user by email address |
| `slk user channels` | List channels a user belongs to |
| `slk user delete-photo` | Delete the current user's profile photo |
| `slk user info` | Show one user's profile |
| `slk user list` | List workspace users |
| `slk user presence` | Get a user's presence status |
| `slk user profile` | Show a user's profile fields |
| `slk user set-photo` | Upload a profile photo |
| `slk user set-presence` | Set the token owner's presence (auto or away) |
| `slk user set-profile` | Update a profile field or set raw profile JSON |

## slk user by-email

Look up a user by email address

**Slack API:** `users.lookupByEmail`

```bash
slk user by-email [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--email` | ✓ | — | email address to look up |

## slk user channels

List channels a user belongs to

**Slack API:** `users.conversations`

```bash
slk user channels [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--types` | — | — | conversation types filter (e.g. public_channel,private_channel,mpim,im) |
| `--user` | — | — | user ID (defaults to the token owner when empty) |

## slk user delete-photo

Delete the current user's profile photo

**Slack API:** `users.deletePhoto`

```bash
slk user delete-photo
```

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk user info

Show one user's profile

**Slack API:** `users.info`

```bash
slk user info [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--user` | ✓ | — | user ID |

## slk user list

List workspace users

**Slack API:** `users.list`

```bash
slk user list [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--cursor` | — | — | initial pagination cursor |
| `--include-bots` | — | — | include bot users (default false) |
| `--include-deactivated` | — | — | include deactivated users (default false) |
| `--limit` | — | `0` | max users to return (0 = no client-side cap) |

**Tips:** List workspace users.

## slk user presence

Get a user's presence status

**Slack API:** `users.getPresence`

```bash
slk user presence [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--user` | — | — | user ID (defaults to the token owner when empty) |

## slk user profile

Show a user's profile fields

**Slack API:** `users.profile.get`

```bash
slk user profile [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--include-locale` | — | — | include locale in response |
| `--user` | — | — | user ID (defaults to current user when empty) |

## slk user set-photo

Upload a profile photo

**Slack API:** `users.setPhoto`

```bash
slk user set-photo [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--file` | ✓ | — | path to image file |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk user set-presence

Set the token owner's presence (auto or away)

**Slack API:** `users.setPresence`

```bash
slk user set-presence [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--presence` | ✓ | — | presence value: auto or away |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk user set-profile

Update a profile field or set raw profile JSON

**Slack API:** `users.profile.set`

```bash
slk user set-profile [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--name` | — | — | profile field name (used with --value) |
| `--profile` | — | — | raw JSON profile object (overrides --name/--value) |
| `--value` | — | — | profile field value (used with --name) |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


