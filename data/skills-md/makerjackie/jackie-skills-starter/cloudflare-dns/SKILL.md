---
name: cloudflare-dns
description: Configure and troubleshoot Cloudflare DNS records and Pages custom-domain bindings. Use when a user asks to add/edit/delete DNS records, map a custom domain to Cloudflare Pages/Workers, verify propagation, or fix domain validation errors. On first use, prompt for API token setup with DNS edit permissions before making changes.
---

# Cloudflare DNS

## Quick Start

1. Clarify target:
   - domain/host (`skills.01mvp.com`)
   - record type (`A`/`AAAA`/`CNAME`/`TXT`)
   - target value
   - proxied on/off
2. Run an auth precheck before any write action.
3. Execute idempotent change (query existing record first, then create/update).
4. Verify with DNS lookup + HTTP check + (if needed) Pages domain status.

## First-Use Auth Gate (Required)

Before first DNS write, check token:

```bash
zsh -lic 'echo ${CLOUDFLARE_API_TOKEN:+SET}'
```

If empty, stop and prompt user to configure token first.

Use this prompt style:

- 我先帮你配置，但需要你先提供 Cloudflare API Token（不是 wrangler OAuth）。
- Token 最少权限：
  - `Zone -> DNS -> Edit`
  - `Zone -> Zone -> Read`
  - 如果要查 Pages 域名状态，再加：`Account -> Cloudflare Pages -> Edit`
- Zone Resources 只选目标域名（最小权限原则）。
- 配置完成后执行：

```bash
export CLOUDFLARE_API_TOKEN='YOUR_TOKEN'
```

Optional persistent setup:

```bash
echo "export CLOUDFLARE_API_TOKEN='YOUR_TOKEN'" >> ~/.zshrc
source ~/.zshrc
```

## Standard Execution Pattern

### 1) Read current DNS record

```bash
python - <<'PY'
import json, os, urllib.request

token = os.environ['CLOUDFLARE_API_TOKEN']
zone_id = '<ZONE_ID>'
name = 'skills.01mvp.com'
url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={name}'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
print(json.dumps(json.load(urllib.request.urlopen(req)), ensure_ascii=False, indent=2))
PY
```

### 2) Create/Update record

- If record not found: create.
- If record exists but value/proxy mismatch: update.
- If already correct: report "no-op".

### 3) Pages custom domain binding (if required)

- Ensure domain is added to the Pages project.
- If not added, create binding first, then ensure DNS points to `<project>.pages.dev`.

### 4) Verification

```bash
dig +short CNAME skills.01mvp.com
dig +short skills.01mvp.com
curl -I https://skills.01mvp.com
```

For Pages validation, also check domain status via Pages API/wrangler.

## Safety Rules

- Always query before write (no blind overwrite).
- Prefer least-privilege token scope.
- Never print full token in output.
- Report exact record changed: name, type, content, proxied, timestamp.
- If API returns auth error, explicitly tell user missing scope instead of retrying blindly.
