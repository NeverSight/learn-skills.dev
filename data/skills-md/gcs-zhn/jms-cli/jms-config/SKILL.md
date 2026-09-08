---
name: jms-config
description: >-
  Manage jms-cli JumpServer server configuration: config.yaml (schema v1.0)
  read/write, platformdirs config paths, AES-256-GCM credential encryption
  (enc:v1:), the `jms config add/list/remove/set-default` commands, and the
  load_config/add_server/remove_server/set_default_server library API. Use
  whenever the user needs to add or inspect a server alias, fix config errors
  (Config not found, missing host/username/password, decryption failure),
  hand-edit or generate config.yaml, understand or handle encrypted
  credentials, or resolve --config and JMS_CONFIG path behavior, even if they
  do not say "config". CLI first; use the library API for programmatic access.
compatibility: Python >= 3.10; uv environment (PyYAML, cryptography are project dependencies)
metadata:
  author: codex
  version: "1.0"
  project: jms-cli
---

# jms-config — Configuration & credential management

## When to use

Trigger on mentions of config, server configuration, config.yaml, adding or
removing a server, config paths, encrypted credentials, `enc:v1:`, `--config`,
`JMS_CONFIG`, `ConfigError`, or platformdirs — even when the user does not say
"config" explicitly. Use cases: registering a new server alias, listing
configured servers, pointing a command at a non-default config path,
hand-writing or repairing config.yaml, and explaining or converting encrypted
credentials.

## Prerequisites

- This skill covers config-file read/write and credential crypto only.
  `jms config add` validates credentials over the network before saving; the
  login/MFA orchestration is described by the `jms-auth` skill. Load
  `jms-auth` when debugging login failures.
- Config paths come from the project's built-in platformdirs usage. Do not
  guess `~/.config` or `./config.yaml` locations.

## Core facts (read first)

- The config file is YAML, named `config.yaml`, resolved via
  `platformdirs.user_config_dir("jms")`: macOS
  `~/Library/Application Support/jms/config.yaml`, Linux
  `~/.config/jms/config.yaml`. The CLI does **not** auto-discover
  `./config.yaml`.
- Every command has a hidden `--config <path>` option for an explicit path;
  the `JMS_CONFIG` environment variable is read only by the `jms mcp` entry
  point, never by CLI commands.
- Credential fields are stored as AES-256-GCM ciphertext (prefix `enc:v1:`);
  on read, plaintext is also accepted (`is_encrypted()` decides), but saving
  always encrypts and forces file mode 0600.
- Schema v1.0 below; PBKDF2/ciphertext details are in
  `references/credential-crypto.md` (open it when you need to encrypt/decrypt
  manually or migrate machines).

### config.yaml schema (v1.0)

```yaml
version: 1.0                # compatibility field
default: prod               # default server alias; the first one added becomes default
servers:
  prod:
    host: jump.example.com  # IP/domain, or a full http(s):// URL
    username: alice
    password: enc:v1:...    # AES-GCM ciphertext; plaintext also accepted
    otp_secret: enc:v1:...  # optional; empty by default, interactive MFA then
```

Constraints: `servers` must be a non-empty mapping; `host`/`username`/
`password` are required (missing raises `ConfigError`); `otp_secret` is
optional; `base_url` derives from host — kept as-is when a scheme is present,
otherwise `https://` is prepended and trailing slashes removed.

## Workflow

### A. CLI first (operations)

1. Inspect: `jms config list` (default server marked `*`, total shown).
2. Add/update: `jms config add <alias>` — prompts for host/username/password/
   otp_secret, runs a full login validation (MFA included) before saving;
   `--set-default` also makes it the default. The first server added becomes
   the default automatically.
3. Remove: `jms config remove <alias>` (`-y` skips confirmation).
4. Change default: `jms config set-default <alias>`.
5. Non-default path: append the hidden `--config <path>` to any command.

### B. Library API (programmatic)

Public API (`jms.config`):

| Function | Purpose |
|---|---|
| `load_config(config_path=None)` | Load and validate, returning `AppConfig` (credentials decrypted) |
| `save_config(cfg, config_path=None)` | Save with encryption, 0600 from the first write |
| `add_server(name, host, username, password, otp_secret="", set_default=False, config_path=None)` | Add/update a server, return the saved path |
| `remove_server(name, config_path=None)` / `set_default_server(name, config_path=None)` | Remove / set default |
| `config_dir()` / `config_file_path()` | platformdirs-resolved paths |

Example (generate a temp config without interactive prompts):

```python
from jms.config import add_server, load_config

path = add_server(
    "prod", "jump.example.com", "alice", "S3cret!pass",
    otp_secret="JBSWY3DPEHPK3PXP",
    config_path="/tmp/jms-eval/config.yaml",
)
cfg = load_config("/tmp/jms-eval/config.yaml")
print(cfg.get_server("prod").base_url)  # https://jump.example.com
```

### C. Validate after hand-editing

config.yaml is a structured artifact of this skill — never "eyeball" it. After
editing or generating, run:

```bash
uv run python3 skills/jms-config/scripts/validate_config.py <path>
```

Exit code 0 before delivering. The script checks YAML parseability, a
non-empty `servers` mapping, and required `host`/`username`/`password`; a
plaintext password is reported as a note (accepted on read, encrypted on
save).

### D. Common errors and fixes

| Error | Cause | Fix |
|---|---|---|
| `Config not found at <path>` | no file at the resolved path | `jms config add <alias>`, or pass `--config` |
| `Config must be a YAML mapping` / `Config file is empty` | corrupted/empty file | rewrite to the schema and run the validator |
| `Server 'X' missing 'host'/'username'/'password'` | missing field | add the field and re-run the validator |
| `credential decryption failed` | `enc:v1:` ciphertext mismatches (host, username) | re-encrypt with the same (host, username) |
| `Server 'X' not found` | unknown alias | `jms config list` for available aliases |

## Verification

- Structural check: run `scripts/validate_config.py <path>` (non-zero exit
  means invalid).
- Regression: after touching config/crypto code, run
  `uv run pytest tests/test_config.py tests/test_crypto.py -q`.

## Scope & Boundaries

> - Capabilities, commands, subcommands, flags, parameters, environment
>   variables, endpoints, and file paths **not mentioned in this skill are not
>   part of this skill**. Do not guess or extrapolate them from related tools,
>   documentation memory, or pattern-matching across similar CLIs.
> - If the user asks for functionality outside this skill, stop and ask — do
>   not invent it.
> - The consuming agent is not responsible for completing or improving the
>   skill. Discovering missing functionality is a signal to **ask the user**,
>   not to fill the gap silently.
> - If the skill's instructions appear wrong, contradictory, outdated, or
>   produce errors when executed, stop and consult the user before proceeding.
>   Do not "fix" the skill on the fly, substitute an alternative command, or
>   retry with guessed parameters.
> - Modifying or extending the skill itself requires explicit user permission
>   and should be routed back through `skill-creator`.

This skill covers the configuration domain only: login validation belongs to
`jms-auth`, and transfer-session config-path usage belongs to the CLI part of
`jms-transfer`. Do not extend beyond that here.
