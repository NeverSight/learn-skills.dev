---
name: unclawg-internet
description: >
  Self-service OpenClaw onboarding with soul interview. Uses CLI device flow for browser auth,
  creates the user's agent machine key, conducts an ask-cascade soul interview to define voice/personas/target market,
  writes the soul draft and discovery mode file, and outputs the env block.
  Use when: "/unclawg-internet", "set me up", "connect to openclaw",
  "get started", "onboard me", "sign up for openclaw", "I want approval gates"
metadata:
  openclaw:
    emoji: "🛂"
    requires:
      bins:
        - uc_onboard
---

# /unclawg-internet

Get set up with OpenClaw — account, agent, soul, and discovery config in one sitting.

## Runtime Security Profile (AI Default)

- For AI runtime, execute onboarding through wrapper command `uc_onboard` only.
- Do not execute raw `curl` from this skill in runtime.
- If `uc_onboard` is missing, fail closed and request wrapper install/allowlist.
- Never bypass human confirmation checkpoints for account creation and key issuance.

## What This Produces

1. OpenClaw account + API keys
2. Agent identity file (`.claude/agents/<agent-id>.env`)
3. Soul draft (`soul_md` policy document via API)
4. Discovery mode file (`modes/<project>.local.md` for `/unclawg-discover`)
5. Browser auto-logged into the approval portal

### Existing OpenClaw Runtime (Skip Full Bootstrap)

If a runtime already exists (for example `0_claw`) and you only need a new agent identity:

1. In the portal sidebar, run **Add Agent**.
2. Create the machine key (Step 1), then choose **Connect existing claw** (Step 2).
3. Save the emitted env block to `.claude/agents/<agent-id>.env`.
4. Run `/unclawg-internet`; Phase 0 detection will pick up that identity and continue only for missing pieces (soul/mode, or key rotation if invalid).

## NEVER Do These Things

- **NEVER execute raw `curl` directly in AI runtime.** Use `uc_onboard` wrapper only.
- **NEVER show the machine key secret more than once.** It cannot be retrieved after creation.
- **NEVER store passwords or secrets in any file the user didn't ask for.**
- **NEVER skip the confirmation before creating the account.**
- **NEVER invent placeholder credentials.** If auth fails, stop and fix the auth path first.
- **NEVER run search/research in the main conversation context.** Always delegate to Task tool subagents (see Rule below).

## Subagent Rule

**All search, web fetch, and research operations MUST be delegated to Task tool subagents.** This preserves the main conversation context for the soul interview flow. Examples:

- Looking up a user's website/product to understand their business → subagent
- Searching for competitor landscape → subagent
- Fetching example content from platforms the user mentions → subagent
- Validating URLs or checking platform availability → subagent

The main conversation should only contain: questions, user answers, confirmations, and artifact writes.

## Wrapper Commands (Runtime Path)

```bash
uc_onboard detect
uc_onboard device-start --client-id "${OPENCLAW_CLIENT_ID:-unclawg}"
uc_onboard device-poll --device-code <device_code>
uc_onboard provision --agent-id <agent-id> --email <email>
```

## Config

```
OPENCLAW_PORTAL_URL=https://unclawg.com
SPAPS_URL=https://api.unclawg.com
APPROVAL_API_URL=https://api.unclawg.com
# Device-flow client_id must be the SPAPS application slug (NOT UUID).
OPENCLAW_CLIENT_ID=unclawg
# Optional only for self-hosted gateways that do not inject server-side app binding:
OPENCLAW_API_KEY=
TENANT_ID=d0000000-0000-0000-0000-000000000001
# Proof-of-humanity fallback contacts (used when signup is pending):
OPENCLAW_PROOF_PRIMARY_X=@your-primary-proof-handle
OPENCLAW_PROOF_SECONDARY_X=https://x.com/your-backup-proof-handle
```

`SPAPS_URL` is the Unclawg auth facade (`/api/auth/*` and `/api/cli/device/*`), not a direct client call to SPAPS.
On `api.unclawg.com`, the gateway injects `X-API-Key` server-side, so do not ask users for `SPAPS_API_KEY`.
The Unclawg proxy also backfills missing device-flow fields (`client_id`, `grant_type`) for legacy callers, but keep sending them explicitly in this skill for deterministic behavior across environments.

## References

- **[references/soul-interview.md](references/soul-interview.md)** — Full soul interview cascade (Phase B, Rounds 1-5). Read when entering the interview phase.
- **[references/artifact-templates.md](references/artifact-templates.md)** — Soul draft templates, mode file template, smoke test, and summary output (Phase C/D). Read when writing artifacts.
- **`/unclawg-admin`** — Operator waitlist triage when signup proof-of-humanity is pending.
- **[references/default-soul.md](references/default-soul.md)** — Default soul template for users who skip the interview.

---

## Phase 0 — Detect Existing Setup

Before starting onboarding, check if the user is already set up (partially or fully).

### Check for existing identity

```bash
ls .claude/agents/*.env 2>/dev/null
```

If identity files exist, read each one and extract `OPENCLAW_AGENT_ID`, `OPENCLAW_MACHINE_KEY_ID`.

### Verify the machine key works

```bash
# For self-hosted gateways requiring client app binding, add:
#   -H "X-API-Key: ${OPENCLAW_API_KEY}" \
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
  -H "X-Tenant-Id: ${TENANT_ID}" \
  -H "X-Machine-Key-Id: ${KEY_ID}" \
  -H "X-Machine-Secret: ${KEY_SECRET}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  "${APPROVAL_API_URL}/v0/approval-requests/social-reply" \
  -d "{
    \"agent_id\": \"${AGENT_ID}\",
    \"action\": \"social_reply_approval\",
    \"resource_type\": \"social_post\",
    \"resource_id\": \"test://setup-check-$(date +%s)\",
    \"expires_at\": \"$(date -u -v+1m +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '+1 minute' +%Y-%m-%dT%H:%M:%SZ)\",
    \"proposed_reply\": \"Setup verification ping.\",
    \"candidate\": {
      \"source_platform\": \"other\",
      \"source_post_url\": \"https://example.com/setup-check\",
      \"source_post_text\": \"Setup verification\",
      \"discovered_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
    }
  }")

STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
```

Interpret key-check failures before deciding next step:
- `201` → key works and has `approval_request.create.social_reply`.
- `401 MACHINE_KEY_NOT_FOUND` → key ID is unknown in this tenant/app context.
- `401 UNAUTHORIZED` → key secret is wrong.
- `403 MACHINE_KEY_EXPIRED` → key expired; re-run device flow and provision a replacement key.
- `403 MACHINE_KEY_REVOKED` → key revoked; provision a replacement key.
- `403 APP_BINDING_MISMATCH` → missing/wrong `X-API-Key` on self-hosted gateways.
- `403 MACHINE_AGENT_MISMATCH` → key is bound to a different agent than `${AGENT_ID}`.

### Check for missing pieces

```bash
ls modes/${AGENT_ID}.local.md 2>/dev/null
```

### Triage result

Show the user what's present and what's missing:

```
Existing setup found:

  Agent ID:   ${AGENT_ID}
  Key ID:     ${KEY_ID}
  Identity:   .claude/agents/${AGENT_ID}.env
  Key valid:  ✓ (or ✗ — expired/revoked, needs re-provisioning)
  Soul:       [written / not yet]
  Mode file:  [found / missing]
```

Then offer to fill gaps:

- **Key invalid** → need to re-authenticate and provision a new key (jump to Step 4 — device flow)
- **Soul missing** → jump to Phase B (read `references/soul-interview.md`)
- **Mode file missing** → jump to Phase C Step 8 (read `references/artifact-templates.md`)
- **Everything present and valid** → "You're all set. Run `/unclawg-discover` to start finding people."

Skip any phase that's already complete. Do not re-run the full onboarding.

---

## Phase A — Account Provisioning

### Step 1 — Ask Email

Ask one question:

> "What email should we use for your OpenClaw account?"

### Step 2 — Pick Agent Name

Ask:

> "Name your agent — this is the ID that shows up in the approval portal. Examples: `my-trading-bot`, `content-writer`, `code-deployer`"

Default suggestion: derive from the current repo name or working directory.

### Step 3 — Confirm

Show what's about to happen:

```
Ready to set up:
  Email:    user@example.com
  Agent:    my-trading-bot
  Portal:   ${OPENCLAW_PORTAL_URL}

This starts browser-based device sign-in (no password sharing in chat),
then provisions API keys for your agent.
Continue?
```

### Step 4 — Start CLI Device Flow (via Unclawg auth facade)

```bash
# client_id must be app slug, e.g. "unclawg" or "buildooor" (not application UUID)
OPENCLAW_CLIENT_ID="${OPENCLAW_CLIENT_ID:-unclawg}"

DEVICE_START_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
  "${SPAPS_URL}/api/cli/device/authorize" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\":\"${OPENCLAW_CLIENT_ID}\",
    \"scope\":\"approval_request.create.social_reply approval_revision.fulfill instruction_proposal.create agent_feedback_digest.read\"
  }")

DEVICE_START_STATUS=$(echo "$DEVICE_START_RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
DEVICE_START_BODY=$(echo "$DEVICE_START_RESPONSE" | sed '/HTTP_STATUS:/d')
```

If using a self-hosted gateway that requires client-supplied app binding, add:
`-H "X-API-Key: ${OPENCLAW_API_KEY}"`.

- `200` → continue
- `400` with `UNKNOWN_CLIENT` → wrong `client_id` format/value. Use the application **slug** (for example `unclawg`), not UUID.
- `404`/`405` with `AUTH_PROXY_ROUTE_NOT_FOUND` → stop and tell the user the API gateway must be updated to proxy `/api/cli/device/*`.
- Other error → print and stop

### Step 5 — Complete Browser Authorization

Extract device-flow fields (supports both envelope and plain payload):

```bash
DEVICE_CODE=$(echo "$DEVICE_START_BODY" | jq -r '.data.device_code // .device_code // empty')
USER_CODE=$(echo "$DEVICE_START_BODY" | jq -r '.data.user_code // .user_code // empty')
VERIFY_URL=$(echo "$DEVICE_START_BODY" | jq -r '.data.verification_uri_complete // .data.auth_url // .data.verification_uri // .verification_uri_complete // .auth_url // .verification_uri // empty')
POLL_INTERVAL=$(echo "$DEVICE_START_BODY" | jq -r '.data.interval // .interval // 5')

# Safety: if upstream returns only '?user_code=...' build a full URL.
if [ -n "$VERIFY_URL" ] && [[ "$VERIFY_URL" = \?* ]]; then
  VERIFY_URL="${OPENCLAW_PORTAL_URL}/device${VERIFY_URL}"
fi
```

If any required value is missing, print the response and stop.

Open the verification URL:

```bash
open "$VERIFY_URL" 2>/dev/null \
  || xdg-open "$VERIFY_URL" 2>/dev/null \
  || echo "Open this URL to continue: $VERIFY_URL"
```

Tell the user:

- "Browser opened. Sign in and approve this device request."
- "If asked, enter code: `${USER_CODE}`."
- "If this email is new, create the account in that browser flow first."

### Step 6 — Poll for Tokens (No password needed)

```bash
while true; do
  TOKEN_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
    "${SPAPS_URL}/api/cli/device/token" \
    -H "Content-Type: application/json" \
    -d "{
      \"grant_type\": \"urn:ietf:params:oauth:grant-type:device_code\",
      \"client_id\": \"${OPENCLAW_CLIENT_ID}\",
      \"device_code\": \"${DEVICE_CODE}\"
    }")

  TOKEN_STATUS=$(echo "$TOKEN_RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
  TOKEN_BODY=$(echo "$TOKEN_RESPONSE" | sed '/HTTP_STATUS:/d')

  if [ "$TOKEN_STATUS" = "200" ]; then
    ACCESS_TOKEN=$(echo "$TOKEN_BODY" | jq -r '.data.access_token // .access_token // empty')
    REFRESH_TOKEN=$(echo "$TOKEN_BODY" | jq -r '.data.refresh_token // .refresh_token // empty')
    break
  fi

  ERROR_CODE=$(echo "$TOKEN_BODY" | jq -r '.error.code // .error.error // .code // .error // empty')
  case "$ERROR_CODE" in
    authorization_pending)
      sleep "${POLL_INTERVAL}"
      ;;
    slow_down)
      POLL_INTERVAL=$((POLL_INTERVAL + 5))
      sleep "${POLL_INTERVAL}"
      ;;
    access_denied|expired_token|invalid_grant)
      echo "Device flow ended: ${ERROR_CODE}"
      echo "$TOKEN_BODY"
      exit 1
      ;;
    *)
      echo "Unexpected device-flow token response:"
      echo "$TOKEN_BODY"
      exit 1
      ;;
  esac
done
```

If token polling keeps returning pending because signup proof is blocked, direct operators to `/unclawg-admin` and continue with Phase B only.

### Step 6b — Verify Authenticated Account

Confirm the signed-in account and compare against requested email:

```bash
WHOAMI_RESPONSE=$(curl -s -X GET \
  "${SPAPS_URL}/api/auth/user" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}")
WHOAMI_EMAIL=$(echo "$WHOAMI_RESPONSE" | jq -r '.data.user.email // .user.email // empty' | tr '[:upper:]' '[:lower:]')
EXPECTED_EMAIL=$(echo "${USER_EMAIL}" | tr '[:upper:]' '[:lower:]')
```

If `WHOAMI_EMAIL` differs from `EXPECTED_EMAIL`, show both and ask whether to continue with the authenticated account.

### Step 6c — Auto-Login via Token Handoff

Immediately after obtaining tokens, open the portal with token handoff. The `/auth/cli-callback` route stores tokens in the browser and redirects to `/approvals`.

```bash
# JWT tokens are base64url — no URL-encoding needed
open "${OPENCLAW_PORTAL_URL}/auth/cli-callback?access_token=${ACCESS_TOKEN}&refresh_token=${REFRESH_TOKEN}" 2>/dev/null \
  || xdg-open "${OPENCLAW_PORTAL_URL}/auth/cli-callback?access_token=${ACCESS_TOKEN}&refresh_token=${REFRESH_TOKEN}" 2>/dev/null \
  || echo "Open this URL to log in: ${OPENCLAW_PORTAL_URL}/auth/cli-callback?access_token=${ACCESS_TOKEN}&refresh_token=${REFRESH_TOKEN}"
```

Tell the user: "Opening the portal in your browser — you're logged in automatically."

**Important:** Open the browser immediately after tokens are issued. The access token expires in 1 hour, but the callback page auto-refreshes stale tokens via the refresh token.

### Step 7 — Provision Machine Key (Only after approved auth)

```bash
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
  "${APPROVAL_API_URL}/v0/claw-governance/machine-keys" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "X-Tenant-Id: ${TENANT_ID}" \
  -d "{
    \"agent_id\": \"${AGENT_ID}\",
    \"label\": \"onboard-$(date +%Y%m%d)\",
    \"scopes\": [
      \"approval_request.create.social_reply\",
      \"approval_revision.fulfill\",
      \"agent_feedback_digest.read\",
      \"instruction_proposal.create\"
    ],
    \"ttl_days\": 90
  }")

STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_STATUS:/d')
```

If using a self-hosted gateway that requires client-supplied app binding, add:
`-H "X-API-Key: ${OPENCLAW_API_KEY}"`.

- `201` → extract `key_id` and `key_secret` from `data.key`
- `403` → scope issue, print error
- Other → print error, stop

### Step 8 — Output the Env Block

Print this exactly — the user copies it into their `.env` or shell profile:

```
# ── OpenClaw Configuration ──────────────────────
# Add these to your project's .env or ~/.zshrc

OPENCLAW_API_URL=${APPROVAL_API_URL}
OPENCLAW_TENANT_ID=${TENANT_ID}
OPENCLAW_AGENT_ID=${AGENT_ID}
OPENCLAW_MACHINE_KEY_ID=${KEY_ID}
OPENCLAW_MACHINE_SECRET=${KEY_SECRET}
# Optional for non-default gateways:
OPENCLAW_API_KEY=${OPENCLAW_API_KEY}

# ⚠️  Save OPENCLAW_MACHINE_SECRET now.
#     It cannot be retrieved again.
#     If lost, rotate via the portal.
# ─────────────────────────────────────────────────
```

Ask before writing any file with secrets:

> "Save this identity to `.claude/agents/${AGENT_ID}.env` for auto-discovery?"

Only if the user says yes, save the identity file for skill auto-discovery:

```bash
mkdir -p .claude/agents
cat > .claude/agents/${AGENT_ID}.env << ENVEOF
OPENCLAW_API_URL=${APPROVAL_API_URL}
OPENCLAW_TENANT_ID=${TENANT_ID}
OPENCLAW_AGENT_ID=${AGENT_ID}
OPENCLAW_MACHINE_KEY_ID=${KEY_ID}
OPENCLAW_MACHINE_SECRET=${KEY_SECRET}
OPENCLAW_API_KEY=${OPENCLAW_API_KEY}
ENVEOF
```

Tell the user: "Saved to `.claude/agents/${AGENT_ID}.env` — other skills like `/unclawg-feed` and `/unclawg-respond` will auto-discover it."

Then print the summary:

```
Account provisioned.

  Portal:     ${OPENCLAW_PORTAL_URL}
  Agent ID:   ${AGENT_ID}
  Key ID:     ${KEY_ID}
  Expires:    90 days from now
  Identity:   .claude/agents/${AGENT_ID}.env

Now let's define your agent's soul.
```

---

## Phase B — Soul Interview (Ask-Cascade)

Read **[references/soul-interview.md](references/soul-interview.md)** for the full interview flow (Rounds 1-5).

---

## Phase C — Write Artifacts

Read **[references/artifact-templates.md](references/artifact-templates.md)** for soul draft templates, mode file template, smoke test, and summary output.

---

## Phase D — Summary

See the summary template in **[references/artifact-templates.md](references/artifact-templates.md)** (bottom section).
