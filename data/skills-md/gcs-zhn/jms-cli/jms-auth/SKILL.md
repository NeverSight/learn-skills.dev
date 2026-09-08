---
name: jms-auth
description: >-
  JumpServer v4 authentication and connection tokens: dual authentication
  (REST Bearer + Django form-login jms_sessionid cookie), MFA/TOTP handling
  (mfa_required detection on both code and error fields, the challenge
  endpoint, automatic TOTP from otp_secret vs the injected otp_prompt
  callback), connection-token creation (SSH web_cli / SFTP web_sftp, KoKo
  port 2222, JMS-{id} account), HTTP retry and error classification (401 to
  AuthError, APIError with status_code). Use whenever the user reports login
  failures, MFA prompts, WebSocket rejections (missing cookie), connection
  token errors, 401/APIError, or needs code that logs in or creates tokens,
  even if they only say "cannot log in". CLI first (jms config add validates
  credentials); use JMSSession / create_connection_token for programmatic
  sessions.
compatibility: Python >= 3.10; uv environment (requests, pyotp are project dependencies)
metadata:
  author: codex
  version: "1.0"
  project: jms-cli
---

# jms-auth — Authentication & connection tokens

## When to use

Trigger on mentions of login, authentication, MFA, OTP, TOTP, one-time codes,
jms_sessionid, csrf, Bearer token, connection token, KoKo 2222, `JMS-`
accounts, 401, APIError, or `mfa_required` — even without naming the auth
module. Use cases: debugging a failed `config add` validation, rejected
exec/login handshakes, or writing library code that creates a session or a
connection token.

## Prerequisites

- This skill consumes `ServerConfig` (host/username/password/otp_secret);
  config-file reading and credential crypto belong to the `jms-config` skill:
  load the config before logging in.
- Downstream consumption of connection tokens (SSH/WS terminals, SFTP)
  belongs to the `jms-terminal` / `jms-transfer` skills. This skill only
  produces the authentication material, not terminal protocol details.

## Core facts (read first)

1. **Both authentication steps are required**: API login for the Bearer token
   (REST) + form login for the `jms_sessionid` cookie (KoKo WebSocket). An
   API-only login is rejected by KoKo.
2. **MFA detection** checks both `data.code == "mfa_required"` and
   `data.error == "mfa_required"` (field names differ across JumpServer
   versions). With `otp_secret`, the code is computed automatically via
   `pyotp.TOTP(secret).now()`; otherwise the `otp_prompt` callback is invoked
   (the CLI injects `click.prompt`; the library default of None raises
   `MFARequired` and never hijacks stdin).
3. **Connection tokens**: terminals use `protocol="ssh"`,
   `connect_method="web_cli"`; SFTP uses `protocol="ssh"`,
   `connect_method="web_sftp"` — SFTP rides on the asset's ssh protocol
   (with `sftp_enabled`); this JumpServer version rejects `protocol="sftp"`
   with `perm_account_invalid`. `account` must be the alias (e.g. `@USER`),
   not the display name.
   > The contract is defined by live-server tests
   > (`tests/test_integration.py::test_connection_token_contract`); the
   > outdated docstring in `transport/token.py` disagrees with the
   > implementation — do not follow it.
4. End-to-end request/response shapes, pagination, and error semantics are in
   `references/endpoints.md` (open it when verifying a specific endpoint).

## Workflow

### A. CLI first (user operations)

- `jms config add <alias>` prompts interactively and fully validates
  credentials (MFA included) before saving; a failed validation writes
  nothing. For login issues, prefer having the user re-run this command and
  observe the error.
- `jms exec/login/sftp` log in automatically on every invocation; use
  `jms -l DEBUG ...` to inspect requests/responses (DEBUG re-enables
  tracebacks).

### B. Library API (programmatic session)

```python
from jms import JMSSession
from jms.config import load_config

cfg = load_config()
server = cfg.get_server("prod")
sess = JMSSession(server, otp_prompt=lambda: input("MFA code: "))
sess.login()                  # dual auth + MFA orchestration
print(sess.session_id)        # jms_sessionid cookie (WS handshake)
print(sess.bearer_token)      # Bearer (REST headers)
```

Connection token:

```python
from jms.transport import create_connection_token

token = create_connection_token(
    sess, asset,
    protocol="ssh", connect_method="web_sftp",    # SFTP; terminals use ssh / web_cli
)
# token["id"] -> SSH user JMS-{id}, token["value"] -> password (KoKo port 2222)
```

`JMSSession` subclasses `RESTClient`, so `sess.api_get/api_post/api_patch/
api_delete/api_get_all` are available; HTTP 401 raises `AuthError`, other
non-2xx raises `APIError` (HTTP code in `status_code`, 0 for network
failures).

### C. Common failure troubleshooting

| Symptom | Root cause | Fix |
|---|---|---|
| KoKo rejects / WS handshake fails | Bearer only, no `jms_sessionid`, or stale cookie | run the full `login()`; confirm `session_id` is non-empty |
| `MFARequired` raised | server demands MFA, no otp_secret and no otp_prompt | configure otp_secret or inject an otp_prompt callback |
| `API login failed` | wrong credentials, or MFA challenge rejected | verify credentials; `-l DEBUG` for the response body |
| HTTP 401 | token expired/revoked | re-run `login()` |
| `invalid JSON response` | nginx error page instead of JSON | check base_url/network; `APIError.status_code` carries the HTTP code |
| SFTP "please select one of the assets" | ssh/web_cli token used for SFTP, or the asset has connect-only perms (no upload/download) | use `protocol="ssh"`, `connect_method="web_sftp"`; confirm upload/download grants |
| token creation fails `perm_account_invalid` | this version rejects `protocol="sftp"` | use `protocol="ssh"`, `connect_method="web_sftp"` |

### D. Verification

Auth logic depends on a real server; protocol behavior must not be asserted
with mocks (project testing rule). After touching auth/http/token code, run:

```bash
uv run pytest tests/test_auth.py tests/test_http.py tests/test_backend_token.py -q
```

Real-server cases are gated by `JMS_TEST_HOST`/`JMS_TEST_USERNAME`/
`JMS_TEST_PASSWORD`/`JMS_TEST_OTP` and skip automatically without them.

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

This skill covers authentication and connection tokens only; terminal and
transfer protocol details live in `jms-terminal` / `jms-transfer`, and
admin APIs (asset CRUD etc.) are out of the current project scope.
