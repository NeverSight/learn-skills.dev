---
name: use-approved-secrets
description: Discover, use, and record Bitwarden-backed credentials through the local secretary broker and its Telegram approval channel. Use whenever a Code Agent needs to search or list available API keys, tokens, passwords, usernames, credentials, or secret environment variables; must run a command with an approved secret without revealing its value; or has just obtained a credential that should be stored in the vault instead of a file.
---
# Use Approved Secrets

## Prerequisite

This skill describes how to drive the `approved-secret` command. Installing the
skill does not install that command. If it is missing, stop and tell the user to
run:

```sh
curl -fsSL https://raw.githubusercontent.com/broven/secretary/main/install.sh | sh
```

If you are running it for them, add `SECRETARY_SKIP_SKILL=1` — the default path
opens an interactive picker you have no terminal to answer — and see the
"code agent" section of the repository README for how to place this file
yourself.

Then the user points it at their broker: `auth set-url <their broker URL>` and
`auth import` (the token comes from `client add` on the broker host). Those two
steps are theirs — never ask for, accept, or echo the token.

Credentials live in a Bitwarden/Vaultwarden vault. The `approved-secret` command talks
to the secretary broker, which is the only thing that ever holds plaintext. You can:

- **read** the safe catalog (`list`) and run one command with secrets injected (`exec`);
- **write** to the vault (`create` / `update` / `remove`), each write approved by the
Owner from Telegram;
- **ask** the Owner for a credential you must not see (`ask-owner`).

You never see a credential value. Reads inject into a child process's environment;
writes take values from stdin or from the Owner directly.

## Reading

### 1. Find the item

```bash
approved-secret list github
approved-secret list github --json
```

Each item shows `name`, `fields`, `description` and `created_at`. `**description` is
the item's stated purpose** (it is the vault's notes field) — use it to decide whether
an item is the one you want. `created_at` tells you whether an item is one you just
made or one that predates you.

### 2. Run the command

Prepare the real command first, pick explicit env names, then run `exec` once. Write a
truthful `--reason` (≥10 characters): it appears verbatim on the approval card and is
the Owner's main basis for deciding.

```bash
# One item
approved-secret exec --reason "check which account the CI token belongs to" \
  --item "GitHub Automation" password=GITHUB_TOKEN \
  -- gh api user

# Several items, one approval, one command
approved-secret exec --reason "nightly sync between GitHub and OpenAI usage data" \
  --item "GitHub Automation" password=GITHUB_TOKEN \
  --item "OpenAI Prod"       password=OPENAI_KEY \
  -- ./scripts/sync
```

Every env name must be unique across all `--item` groups; each field may be bound once;
up to 10 items per approval. A previously approved request may be reused silently with no
Telegram prompt at all; `exec` says which happened when it succeeds, so read that line
before telling the user anything about approvals.

### When exec comes back "尚未批准"

`exec` waits about 100 seconds and then gives up **on the wait, not on the request**
(exit code 75). The approval card is still live in the Owner's chat, and the broker will
keep re-sending it for roughly 25 minutes. Nothing was granted and nothing ran.

Do this, in order:

1. Tell the user, in one line, that a card is waiting for them — name the item.
2. Re-run **the same command** after about 60 seconds. Approval mints the authorization,
 so a re-run after approval is an ordinary fast path and returns in under a second.
3. At most three re-runs. Then stop, say the card is still unanswered, and wait for the
 user.

Never submit a *second* request instead of re-running: re-sending the card is the
broker's job, and a duplicate request just puts two cards in front of the Owner.

Report the command result or the approval failure. **Never report a credential value.**

### What one approval covers

The Owner picks 1 hour, 8 hours, or 7 days. The authorization is stored per
**(caller, client, repository, item, field)** and matched by containment:

- Requesting a **subset** of what was approved reuses it silently.
- **Renaming the env variable does not re-trigger approval** — it is a local alias.
- **Rotating the value does not revoke it** — the item's identity is its id.
- Adding an item or field that was never approved does re-trigger approval.
- The command is **not** part of the authorization. The first time a given command runs
against a given set of items, the Owner gets a non-blocking notification carrying the
full argv and a revoke button. Execution is not delayed by it.

### Inline shell

Inline code (`sh -c`, `bash -lc`, `python -c`, …) is allowed and passed through verbatim.
It is approved **every single time** and never writes a reusable authorization, because
the whole code string is what the Owner is being asked to judge. Prefer it over a
throwaway script file when you need a pipeline — the inline string is visible on the
card, a script file's contents are not.

## Writing

Three verbs. **Every write needs the Owner's approval and never creates a read
authorization** — after writing, using the credential still goes through `exec`.

Values never appear in argv. A field's value comes from exactly one of:

- `@stdin` — you already have the value; pass it as a JSON object on standard input.
- `@owner` — the value must not enter your context; the Owner types it into a one-time
web form. **Only `create` may use `@owner`.**

### ask-owner — you need a credential you must not see

Use this the moment you need a credential you do not have. It writes **nothing** and
reveals nothing: it prints a one-time link and exits. Running it is always safe, so
**do not ask permission first, and do not hand the command to the user to run.**

```bash
approved-secret ask-owner --item "Linear API" \
  --description "Linear Personal API Key，直接调 GraphQL API 用" \
  --how-to-get "Linear → Settings → Security & access → Personal API keys → New key" \
  --field api_key \
  --reason "要直接调 Linear GraphQL API，vault 里没有可用的 key"
```

Fields are bare names — no `=@owner`. **Pick the item name and description yourself**;
they are yours to decide, and a name you regret costs one `update --rename` later. Ask
the user only when you genuinely cannot tell what the credential is *for* — not to have
a name approved.

### create — a new item, or a new field on an existing item

```bash
# New item. --description is REQUIRED and is what tells a future agent what this is.
USERNAME_VALUE="ops@acme.com" PASSWORD_VALUE="$TOKEN" \
  jq -n '{username: env.USERNAME_VALUE, password: env.PASSWORD_VALUE}' | \
  approved-secret create --item "Acme Prod" \
    --description "Acme 生产环境部署账号，CI 用" \
    --field username=@stdin --field password=@stdin \
    --reason "刚注册完 Acme 账号，把凭据存进 vault"

# New field on an item that already exists — omit --description.
FIELD_VALUE="$KEY" jq -n '{api_key: env.FIELD_VALUE}' | \
  approved-secret create --item "Acme Prod" --field api_key=@stdin \
    --reason "Acme 新开了 API key，和账号存在一起"

# You must not see the value: the Owner fills it in.
USERNAME_VALUE="ops@acme.com" jq -n '{username: env.USERNAME_VALUE}' | \
  approved-secret create --item "Acme Prod" \
    --description "Acme 生产环境部署账号，CI 用" \
    --field username=@stdin --field password=@owner \
    --reason "注册完账号，密码由本人设置"
```

`--how-to-get 用户引导和告知用户如何获得 or 创建对应凭据，有对应站点的 url 就告知用户。知道来源时就填写，不知道`

`时则完全不要使用这个参数。`

`**--description` is the intent switch.** With it you are creating a new item, and a
name that is already taken is an **error**. Without it you are adding fields to an item
that must already exist.

**If create reports the name is taken**, do not guess. Run `approved-secret list "<name>"`
and read its `description` and `created_at`:

- created seconds ago with your description → your previous attempt already succeeded;
carry on.
- something else entirely → pick a different item name, or add your fields to it
deliberately (drop `--description`).

Same for "already has field X": that means the field is there — use `update` to change
its value, or accept that a retry already landed.

### update — change a field's value, the item name, or the description

```bash
FIELD_VALUE="$NEW" jq -n '{password: env.FIELD_VALUE}' | \
  approved-secret update --item "Acme Prod" --field password=@stdin \
    --reason "Acme 生产 token 已轮换，同步 vault 里的旧值"

approved-secret update --item "Acme Prod" --rename "Acme Production" \
  --reason "统一命名，和其它条目对齐"

approved-secret update --item "Acme Prod" --description "Acme 生产部署账号，仅 CI 使用" \
  --reason "补一句用途，避免以后认错条目"
```

One `update` changes **one kind of thing** — field values, or the name, or the
description, or the how-to-get. Not two at once. Updating the how-to-get is worth doing
whenever you notice the acquisition path has changed (a console redesign, a moved menu).

If the vault already holds the value you are asking for, the command succeeds as
"unchanged" and the Owner is not disturbed. That is what makes a retry safe.

`update` cannot use `@owner`. If the Owner must supply a new value without you seeing
it, they do it in their vault client, or you `remove` the field and `create` it again.

### remove — soft-delete an item, or delete a field

```bash
approved-secret remove --item "Acme Prod" --reason "服务已下线，条目不再需要"
approved-secret remove --item "Acme Prod" --field api_key --reason "这个 key 已作废撤销"
```

- `how_to_get` cannot be removed. Correct it with `update --how-to-get` instead — a
stale acquisition path is still better than none.
- Removing an **item** puts it in the vault's trash — recoverable.
- Removing a **field** is **irreversible**: the vault keeps no history for fields.
- Either way, existing authorizations for what was removed are revoked. Restoring an
item from the trash does **not** bring them back.

### The Owner-entry link

A `create` with any `@owner` field does **not** block. It prints a one-time link and
exits without writing anything:

```
需要 Owner 本人填写以下字段：password
录入链接（一次性，2030-01-01T00:10:00.000Z 前有效）：
https://broker.example/entry/…
尚未写入 vault。请把链接交给本人，填完后再继续。
```

Treat that link as **credential-equivalent**: whoever holds it can complete that one
write. Show it to the user once. Do not write it to a file, do not repeat it, do not put
it in a commit message or an issue. Then **stop and wait** — the user will tell you when
they have filled it in. Confirm with `approved-secret list "<item>"` before continuing.

## Safety Rules

- **Never put a secret value in argv**, a URL, a file, logs, chat, or source code. The
CLI refuses `--field NAME=<value>` for exactly this reason.
- Never print or inspect secret-bearing environment variables with `env`, `printenv`,
`echo`, debug dumps, or `set -x`.
- Never call `bw`, `rbw`, `fnox`, or Bitwarden APIs directly for an interactive secret
request.
- Do not bind secrets to control names such as `PATH`, `HOME`, `SECRETARY_*`, `BW_*`,
or `MISE_*`; the runner rejects them.
- Do not background the broker or poll its internal APIs. One foreground command owns
start, waiting, timeout, and cancellation.
- Use `--json` only to parse catalog metadata; catalog output never contains values.
- **Denied** means stop for good: fail closed, never resend, report which item was
refused, and find another way. **尚未批准** (exit 75) is not a denial — follow the
re-run procedure above. If a command reports it cannot confirm the result, re-running
is the correct move, not a risk: it may already be approved.
- **Never weaken, pad, or genericise `--reason`.** If you cannot state a specific
purpose, you should not be asking.
- After a network failure on a write, **do not blindly retry**. Run
`approved-secret list "<item>"` first: the write may already have landed.
- If a credential you need is absent, do not stop and describe what is missing — run
`ask-owner` and give the user the link. Naming the item is your call, not theirs.

Token setup is a human-only bootstrap action. If the command reports that no token is
configured, ask the user to run `approved-secret auth import`; never request or accept
the token in chat.