---
name: axiom-create-org
description: Provision a temporary Axiom organization with one unauthenticated API call, store its one-time token securely, and hand the claim URL to the user. Use when an agent needs an Axiom org and the user has none configured, or asks for a new or throwaway one.
---

# axiom-create-org

`POST https://api.axiom.co/v2/orgs/provision` creates a real Axiom organization and returns a full-access API token. The org is deleted after 24 hours unless a human opens its claim URL.

## Before provisioning

- Use an existing deployment from `~/.axiom.toml` if one fits the task.
- Provision at most one org per task. Agents can create at most 3 orgs a day.
- Tell the user the org is temporary and needs claiming to persist.

## Provision and store the token

The token and claim URL are returned **once** and can never be retrieved again. Save them before doing anything else, and never print the token, echo the raw response, or commit either value.

Run this as one command so the response only touches a private temp file:

```bash
umask 077
resp=$(mktemp)
code=$(curl -sS -o "$resp" -w '%{http_code}' -X POST https://api.axiom.co/v2/orgs/provision \
  -H 'Content-Type: application/json' -d '{"name": "<short-task-name>"}')
if [[ "$code" == 200 ]]; then
  jq -r '"\n[deployments.\(.id)]\nurl = \"https://api.axiom.co\"\ntoken = \"\(.token)\"\norg_id = \"\(.id)\"\nclaim_url = \"\(.claimUrl)\"\nexpires_at = \"\(.expiresAt)\""' \
    "$resp" >> ~/.axiom.toml && chmod 600 ~/.axiom.toml &&
    jq '{id, name, defaultEdgeDeployment, expiresAt}' "$resp" && rm -f "$resp"
else
  echo "provision failed: HTTP $code" >&2; cat "$resp" >&2; rm -f "$resp"
fi
```

- Body fields are optional; `{}` is valid. `name` defaults to `Agent Org <hex>`.
- Omit `edgeDeployment` unless the user asks for one; the default is `US East 1 (AWS)`.
- `429 Too Many Requests` means the daily limit is hit. Retry later with backoff; never loop.
- If the append to `~/.axiom.toml` fails, the response stays in `$resp`. Recover the token from it before deleting it.

## Use the org

The org id is the deployment name, so the other Axiom skills work as-is:

```bash
skills/axiom-alerting/scripts/axiom-api <org-id> GET /datasets
```

For direct calls, send `Authorization: Bearer <token>` and `X-Axiom-Org-Id: <org-id>`. Read the token from `~/.axiom.toml` into a variable; do not paste it into commands or output. The org behaves like any Axiom org: create datasets, ingest, query, and build dashboards and monitors.

## Hand off the claim URL

Claiming needs a human signed in to Axiom; there is no API for it. Try to open the claim URL in the user's browser, and print it with the deadline:

```bash
url=$(awk -F'"' -v d="[deployments.<org-id>]" '$0==d{f=1;next} /^\[/{f=0} f&&/^claim_url/{print $2}' ~/.axiom.toml)
{ open "$url" || { [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] && xdg-open "$url"; }; } >/dev/null 2>&1 && echo "opened claim URL in browser" || echo "no browser available"
awk -v d="[deployments.<org-id>]" '$0==d{f=1;next} /^\[/{f=0} f&&/^(claim_url|expires_at)/' ~/.axiom.toml
```

Always show the claim URL once in your reply too: on a remote machine the browser may open where the user cannot see it. Tell the user:

- Anyone who opens the link can take ownership. Do not share it beyond the user.
- Unclaimed, the org and all its data, dashboards, monitors, and the token are permanently deleted at `expires_at` (24 hours after provisioning).
- Claiming keeps everything the agent built, makes the org permanent on the Personal plan, and keeps the token working. The link is single-use.

## Limits until claimed

- 10 GB ingest and 1 GB-hour of query compute over the 24 hours.
- Few datasets: creating a 4th dataset failed with `dataset license limit exceeded` in testing (not documented). Put related data in one dataset.
- Monitors and notifiers can be created, but notifications are not delivered.
- Claiming lifts these to full Personal plan limits and enables notifiers.

If the token is lost, the org is unreachable over the API until a human claims it and creates a new token.

Docs: https://axiom.co/docs/console/intelligence/agent-created-orgs
