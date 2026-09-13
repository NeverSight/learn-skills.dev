---
name: start-cloud
description: >
  The CloudWeaver entry point — invoke it whenever the user types
  `/start-cloud` or asks to install, deploy or provision a ready-made
  application on the Locaweb Cloud ("subir o Hermes Agent", "instalar na
  Locaweb Cloud", "criar uma VM com...", "quero instalar uma receita"). It
  loads the CloudWeaver persona, runs the pre-flight check, presents the
  recipe catalog, collects configuration one question at a time, then
  orchestrates cloud-weaver-repo-setup through to the final report.
---

# `/start-cloud` — CloudWeaver installation flow

This skill is the single entry point for installing a recipe. It does not
provision anything by itself — it **orchestrates** the other cloud-weaver
skills in order and keeps the user informed in plain language between steps.

Follow the steps below in order. Do not skip a step, and do not run two steps
in parallel.

---

## Step 0 — Load the persona

Use the Skill tool to invoke `cloud-weaver-playbook` and adopt it for the rest
of the session: the CloudWeaver persona, the PT-BR output rule, the
`[CloudWeaver]` message tag and the standing security rules.

If the playbook is already loaded in this session, skip this step.

---

## Step 1 — Pre-flight check

**Mandatory. Never skip it, even when the user already said exactly what they
want to install.**

Use the Skill tool to invoke `cloud-weaver-pre-flight-check` and follow its
instructions. Handle the flags it prints:

| Flag | Action |
|------|--------|
| `NEEDS_COMPUTER_SETUP` | Invoke `cloud-weaver-computer-setup`, then re-run the check |
| `NEEDS_GITHUB_AUTH` | Ask the user to run `gh auth login` in their OS terminal, then resume |
| `NEEDS_LOCAWEB_CREDENTIALS` | Ask the user to export `LOCAWEB_API_KEY` and `LOCAWEB_API_SECRET` in their OS terminal and start a new session. **Never accept the values in the conversation.** |
| `NEEDS_TELEGRAM_BOT_TOKEN` | Ask the user to export `TELEGRAM_BOT_TOKEN` in their OS terminal and start a new session. **Never accept the value in the conversation.** To find the token of an existing bot: open [@BotFather](https://t.me/BotFather) on Telegram → `/mybots` → select the bot → **API Token**. |
| `PREFLIGHT_FAILED` | Explain each reason in plain language, give the remediation, and **stop** |
| No flags | The environment is ready — continue |

Adapt the greeting: if nothing needed setup, go straight to Step 2. If setup
was needed, give a short friendly status update as each item resolves.

---

## Step 2 — Present the recipe catalog

Present the catalog as a **numbered list** so the user can reply with the number
or the name. **Only recipes marked available may be selected** — show unavailable
ones so the user knows they are coming, but never offer them as a choice.

```
Qual receita você quer instalar?

1. WAHA — Agente de WhatsApp (WAHA) + PostgreSQL
2. Hermes Agent — Agente Telegram + LLM (Nous Research)

🔜 Em breve: Coolify, Jitsi Meet
```

Ask which recipe they want. Rules:

- Accept the number (1, 2) or the name (waha, hermes-agent). Map to the recipe
  ID internally: `1` → `waha`, `2` → `hermes-agent`.
- If the user picks an unavailable recipe, say plainly it is not ready yet and
  offer the available ones.
- More than one recipe may be selected. Handle them one at a time,
  sequentially — never interleave.

---

## Step 3 — Collect configuration, one question at a time

### 3.0 — Session file (resume support)

Before asking the first question, check for an existing session file:

```bash
SESSION_FILE="$HOME/.cloud-weaver-${recipe_id}-session.json"
test -f "$SESSION_FILE" && cat "$SESSION_FILE"
```

If found, show the saved values and ask: continuar de onde parou, ou começar do zero?
- **Continuar:** skip already-answered questions.
- **Começar do zero:** `rm "$SESSION_FILE"` and proceed normally.

After each answer, persist to session file (no secrets — only config values):

```bash
python3 -c "
import json, os, datetime
f = os.path.expanduser('$SESSION_FILE')
data = {'recipe': '$recipe_id', 'saved_at': datetime.datetime.utcnow().isoformat() + 'Z', 'params': <collected_params_dict>}
open(f, 'w').write(json.dumps(data, indent=2, ensure_ascii=False))
os.chmod(f, 0o600)
"
```

---

### 3.1 — Questions per recipe

Ask **exactly one question per message**, validate before moving on.

#### All recipes

1. **Nome do repositório GitHub** — o participante escolhe (ex: `meu-hermes`).
   Validate: `^[a-zA-Z0-9_][a-zA-Z0-9._-]*$`. Explain it will become the GitHub repo name.

2. **Zona Locaweb Cloud** — ZP01 (São Paulo, padrão) ou ZP02.
   Default: ZP01.

3. **Plano da VM** — micro / small (padrão) / medium / large.
   Show brief info: small = 2 vCPU / 4 GB RAM.

#### hermes-agent only

4. **ID do Telegram do usuário permitido** — número inteiro positivo (ex: 123456789).
   Explain: only this user can send commands to the bot. Validate > 0.

#### waha only

No additional questions — WAHA API key and Postgres password are generated
automatically by `cloud-weaver-repo-setup`.

---

## Step 4 — Present plan and get confirmation

Show a summary:

- **Repositório GitHub:** `<github-username>/<repo-name>` (privado)
- **VM na Locaweb Cloud:** plano `<plan>`, zona `<zone>`, disco 20 GB
- **Receita:** `<recipe>` — imagem pré-construída `ghcr.io/fagnerlopes/cw-<recipe>:latest`
- **Pipeline:** GitHub Actions — infra (~4 min) + deploy Kamal (~1 min)
- **Secrets que serão configurados:** liste apenas os NOMES, nunca valores

State plainly that this creates billable resources on their Locaweb Cloud account.
Ask for an explicit **yes** and wait for it.

---

## Step 5 — Setup and deploy

Use the Skill tool to invoke `cloud-weaver-repo-setup` and follow it through to
completion. Pass the configuration collected in Step 3:

- `RECIPE` — recipe ID (`hermes-agent` or `waha`)
- `REPO_NAME` — chosen repository name
- `ZONE` — chosen zone
- `WEB_PLAN` — chosen plan
- `TELEGRAM_USER_ID` — Telegram user ID (hermes-agent only)

Display only STEP: progress bullets during execution:
- ⏳ for in-progress steps
- ✅ for completed steps

On failure: show complete output for diagnosis. Do not retry without understanding the error.

---

## Step 6 — (Handled by repo-setup)

The GitHub Actions pipeline handles both provisioning and deployment.
`cloud-weaver-repo-setup` monitors via `gh run watch` (its Step 7).
No separate monitoring step needed in v2.

---

## Step 7 — Final report

Present in PT-BR:

- **URL de acesso:** `https://<public-ip>.nip.io` — destacar visivelmente
- **Repositório GitHub:** link `https://github.com/<user>/<repo-name>`
- **Credenciais geradas:** read from `~/.cloud-weaver-<repo-name>-report.json`,
  show once, then delete the file:
  ```bash
  cat "$HOME/.cloud-weaver-${REPO_NAME}-report.json"
  rm -f "$HOME/.cloud-weaver-${REPO_NAME}-report.json"
  ```
  - **hermes-agent:** the URL opens a web terminal protected by basic auth —
    show `ttyd_user` / `ttyd_password` and tell the user to save them now, since
    they are not recoverable afterwards. On first access the terminal opens the
    Hermes setup wizard; after that it opens the Hermes CLI.
  - **waha:** show `postgres_password` and `waha_api_key`.
- **Próximos passos:**
  - Para atualizar o deploy: `git push` ao branch `main` do repositório ativa o pipeline
  - Para reprovisionar manualmente: `gh workflow run deploy.yml --repo <user>/<repo-name>`
  - Para ver logs: `gh run list --repo <user>/<repo-name>`
  - Acesso SSH: `ssh -i ~/.ssh/cw-<repo-name> root@<public-ip>`
  - Para remover os recursos e parar a cobrança: diga "quero fazer o teardown" em uma nova sessão

Delete the session file after the report:
```bash
rm -f "$HOME/.cloud-weaver-${recipe_id}-session.json"
```

Celebrate the milestone, then invite the user to start a new session.

---

## Rules

- Every message starts with `[CloudWeaver]`.
- All output to the user in PT-BR; code comments in English.
- One question at a time — never batch questions.
- Secrets never appear in the conversation, logs or commits.
- Validate every repo name against `[a-zA-Z0-9_][a-zA-Z0-9._-]*` before it reaches a command line.
- "Locaweb Cloud" everywhere — never "CloudStack".
