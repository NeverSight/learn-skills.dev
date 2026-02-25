---
name: cloudflare-service-token-setup
description: |
  Creates and manages Cloudflare Access service tokens for automated infrastructure
  verification and non-human access. Use when setting up automation, verification scripts,
  monitoring systems, or need to test services without Google OAuth. Triggers on "create
  service token", "setup automation access", "verify without OAuth", "automated monitoring",
  or "service token for testing". Works with Cloudflare Access Service Auth, .env credential
  storage, and cf-service-token.sh script for testing and management.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Edit
---

# Service Token Setup Skill

Complete workflow for creating and managing Cloudflare Access service tokens for automated infrastructure verification and non-human access.

## Quick Start

Quick service token setup:

```bash
# 1. Create service token via Cloudflare dashboard
# Go to: https://one.dash.cloudflare.com → Access → Service Auth → Create Service Token
# Name: "Infrastructure Automation"
# Duration: 1 year

# 2. Add credentials to .env
echo "CF_SERVICE_TOKEN_CLIENT_ID=your-client-id.access" >> /home/dawiddutoit/projects/network/.env
echo "CF_SERVICE_TOKEN_CLIENT_SECRET=your-client-secret" >> /home/dawiddutoit/projects/network/.env

# 3. Test service token
source /home/dawiddutoit/projects/network/.env
curl -H "CF-Access-Client-Id: ${CF_SERVICE_TOKEN_CLIENT_ID}" \
     -H "CF-Access-Client-Secret: ${CF_SERVICE_TOKEN_CLIENT_SECRET}" \
     https://jaeger.temet.ai

# 4. Use helper script for testing
/home/dawiddutoit/projects/network/scripts/cf-service-token.sh test jaeger.temet.ai
```

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Understanding Service Tokens vs OAuth
   - 3.2 Create Service Token via Dashboard
   - 3.3 Add Credentials to .env
   - 3.4 Test Service Token Access
   - 3.5 Use Helper Script for Verification
   - 3.6 Revoke or Rotate Service Token
   - 3.7 Monitor Service Token Usage
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Create service token"
- "Setup automation access"
- "Verify services without OAuth"
- "Automated monitoring"
- "Non-human access"

**Implicit Triggers:**
- Need to test services programmatically
- Setting up monitoring scripts
- CI/CD needs to verify deployments
- Want to share verification results with Claude
- Need to bypass Google OAuth for automation

**Debugging Triggers:**
- "How do I test services without browser?"
- "How to automate verification?"
- "What's the difference between service tokens and OAuth?"

## What This Skill Does

1. **Explains Tokens** - Clarifies service tokens vs Google OAuth use cases
2. **Creates Token** - Guides through Cloudflare dashboard token creation
3. **Stores Credentials** - Adds token to .env securely
4. **Tests Access** - Verifies token works for protected services
5. **Helper Script** - Shows how to use cf-service-token.sh for testing
6. **Revokes Token** - Shows how to revoke/rotate compromised tokens
7. **Monitors Usage** - Shows how to view token usage in Access logs

## Instructions

### 3.1 Understanding Service Tokens vs OAuth

**Service Tokens (Non-Human Access):**
- For automation, scripts, monitoring systems
- Bypasses Google OAuth requirement
- Works with curl, scripts, CI/CD
- Long-lived (months/years)
- No user session required

**Google OAuth (Human Access):**
- For humans accessing via web browser
- Requires Google account login
- Session-based (24 hours default)
- Multi-factor authentication support

**When to use each:**

| Use Case | Method |
|----------|--------|
| Automated health checks | Service Token |
| CI/CD deployment verification | Service Token |
| Monitoring scripts | Service Token |
| Sharing verification with Claude | Service Token |
| Human web browser access | Google OAuth |
| Interactive service use | Google OAuth |

**Key difference:** Service tokens **automatically bypass** all Cloudflare Access policies - no additional configuration needed.

### 3.2 Create Service Token via Dashboard

**Step 1: Navigate to Service Auth**

1. Go to: https://one.dash.cloudflare.com
2. Navigate to: **Access** → **Service Auth** → **Service Tokens**
3. Click: **Create Service Token**

**Step 2: Configure Token**

- **Name:** `Infrastructure Automation` (or descriptive name)
- **Duration:** 1 year (or as needed)
- **Recommended:** Use descriptive names like "CI/CD Pipeline" or "Health Monitoring"

**Step 3: Save Credentials**

After creation, Cloudflare shows:
- **Client ID:** `8f0eb3c52a7236fc952d9b11cd67b960.access`
- **Client Secret:** `63b34062dbca3405521196952ba4d155...` (long hex string)

⚠️ **IMPORTANT:** Client secret is shown **only once**. Copy it immediately.

**Step 4: Copy Credentials**

Copy both values - you'll add them to .env in the next step.

### 3.3 Add Credentials to .env

Add service token credentials to project .env file:

```bash
# Navigate to project directory
cd /home/dawiddutoit/projects/network

# Add credentials to .env
cat >> .env << 'EOF'

# Cloudflare Access Service Token (for automation)
CF_SERVICE_TOKEN_CLIENT_ID="your-client-id.access"
CF_SERVICE_TOKEN_CLIENT_SECRET="your-client-secret-here"
EOF
```

**Replace values** with actual credentials from dashboard.

**Verify credentials added:**

```bash
grep CF_SERVICE_TOKEN /home/dawiddutoit/projects/network/.env
```

Expected output:
```
CF_SERVICE_TOKEN_CLIENT_ID="8f0eb3c52a7236fc952d9b11cd67b960.access"
CF_SERVICE_TOKEN_CLIENT_SECRET="63b34062dbca3405521196952ba4d155de00f59e52d0fa23d0a7f3de66696c6c"
```

**Security note:** .env is already in .gitignore, so credentials won't be committed.

### 3.4 Test Service Token Access

**Test with curl directly:**

```bash
# Load environment variables
source /home/dawiddutoit/projects/network/.env

# Test single service
curl -I \
  -H "CF-Access-Client-Id: ${CF_SERVICE_TOKEN_CLIENT_ID}" \
  -H "CF-Access-Client-Secret: ${CF_SERVICE_TOKEN_CLIENT_SECRET}" \
  https://jaeger.temet.ai
```

**Expected result:**
```
HTTP/2 200
server: Caddy
...
```

**Test multiple services:**

```bash
source /home/dawiddutoit/projects/network/.env

for service in pihole jaeger langfuse ha sprinkler code webhook; do
  echo "Testing ${service}.temet.ai..."
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "CF-Access-Client-Id: ${CF_SERVICE_TOKEN_CLIENT_ID}" \
    -H "CF-Access-Client-Secret: ${CF_SERVICE_TOKEN_CLIENT_SECRET}" \
    "https://${service}.temet.ai")

  echo "  Status: HTTP $status"
  echo
done
```

**Success indicators:**
- HTTP 200: Service accessible and working
- HTTP 502: Service token working but backend down
- HTTP 403: Service token invalid or expired

### 3.5 Use Helper Script for Verification

The project includes a helper script for easier testing:

**Test single service:**

```bash
/home/dawiddutoit/projects/network/scripts/cf-service-token.sh test jaeger.temet.ai
```

Expected output:
```
Testing jaeger.temet.ai...
✓ Service token accepted (HTTP 200)
```

**Test with full response:**

```bash
/home/dawiddutoit/projects/network/scripts/cf-service-token.sh test jaeger.temet.ai --verbose
```

Shows complete HTTP response and headers.

**List all service tokens:**

```bash
/home/dawiddutoit/projects/network/scripts/cf-service-token.sh list
```

Shows all service tokens configured in your Cloudflare account.

**Test all configured services:**

```bash
for domain in pihole jaeger langfuse ha sprinkler code webhook; do
  /home/dawiddutoit/projects/network/scripts/cf-service-token.sh test ${domain}.temet.ai
done
```

### 3.6 Revoke or Rotate Service Token

**When to revoke:**
- Token compromised or exposed
- Token no longer needed
- Regular security rotation (annually recommended)

**Revoke via Dashboard:**

1. Go to: https://one.dash.cloudflare.com
2. Navigate to: **Access** → **Service Auth** → **Service Tokens**
3. Find token by name: "Infrastructure Automation"
4. Click trash icon → **Delete**
5. Confirm deletion

**Revoke via Script:**

```bash
# List tokens to get ID
/home/dawiddutoit/projects/network/scripts/cf-service-token.sh list

# Delete by ID
/home/dawiddutoit/projects/network/scripts/cf-service-token.sh delete <token-id>
```

**After revocation:**

1. Remove credentials from .env:
```bash
nano /home/dawiddutoit/projects/network/.env
# Delete CF_SERVICE_TOKEN_CLIENT_ID and CF_SERVICE_TOKEN_CLIENT_SECRET lines
```

2. If rotating (not removing), create new token and update .env with new credentials.

**Token rotation workflow:**

```bash
# 1. Create new token via dashboard
# 2. Add new credentials to .env (with new_ prefix temporarily)
echo "CF_SERVICE_TOKEN_CLIENT_ID_NEW=new-client-id.access" >> .env
echo "CF_SERVICE_TOKEN_CLIENT_SECRET_NEW=new-secret" >> .env

# 3. Test new token works
source .env
curl -H "CF-Access-Client-Id: ${CF_SERVICE_TOKEN_CLIENT_ID_NEW}" \
     -H "CF-Access-Client-Secret: ${CF_SERVICE_TOKEN_CLIENT_SECRET_NEW}" \
     https://jaeger.temet.ai

# 4. If working, replace old with new in .env
nano .env  # Remove old credentials, rename new_ to remove suffix

# 5. Revoke old token via dashboard
```

### 3.7 Monitor Service Token Usage

View service token access logs:

**Via Cloudflare Dashboard:**

1. Go to: https://one.dash.cloudflare.com
2. Navigate to: **Logs** → **Access**
3. Filter by: **Authentication method** → **Service token**
4. View:
   - Timestamp of access
   - Service accessed
   - Token name used
   - Source IP
   - Success/failure

**Log retention:** 30 days (free plan) to 6 months (enterprise)

**Monitoring for suspicious activity:**
- Unexpected IPs accessing services
- High frequency of requests (potential abuse)
- 403 errors (token may be expired/revoked)

**Alerts setup** (optional):

Set up Cloudflare Notifications:
1. Go to: Account → Notifications
2. Create alert for: Access events
3. Trigger: Service token authentication failures

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Service token architecture, security best practices, API details |
| `scripts/test-service-token.sh` | Automated testing script for all services |
| `examples/examples.md` | Example use cases, monitoring scripts, CI/CD integration |

## Expected Outcomes

**Success:**
- Service token created in Cloudflare dashboard
- Credentials stored securely in .env
- Token bypasses OAuth for protected services
- HTTP 200 responses for accessible services
- Helper script works for verification
- Can share verification results with Claude

**Partial Success:**
- Token created but not tested (complete step 3.4)
- Some services return 502 (backend issue, not auth issue)

**Failure Indicators:**
- HTTP 403 responses (token invalid or not configured)
- Token not found in dashboard
- Credentials not in .env
- Helper script fails with "missing credentials"

## Requirements

- Cloudflare Zero Trust account with Access configured
- Admin access to Cloudflare dashboard
- .env file with write permissions
- curl installed for testing
- Existing Cloudflare Access applications configured

## Red Flags to Avoid

- [ ] Do not treat service tokens like passwords (they are powerful credentials)
- [ ] Do not share service tokens publicly or commit to git
- [ ] Do not create unlimited tokens (1-2 per use case is sufficient)
- [ ] Do not skip saving client secret immediately (shown only once)
- [ ] Do not use service tokens for human browser access (use OAuth)
- [ ] Do not forget to revoke tokens when no longer needed
- [ ] Do not ignore 403 errors (indicates auth failure, not backend issue)

## Notes

- Service tokens **automatically bypass** Cloudflare Access policies (no policy configuration needed)
- Token duration options: 1 day, 1 week, 1 month, 6 months, 1 year, no expiry
- Recommended duration: 1 year with annual rotation
- Service tokens work for all Access-protected applications automatically
- No limit on number of service tokens per account
- Revoked tokens fail immediately (no grace period)
- Service tokens don't support MFA (they bypass all human authentication)
- Use separate tokens for different systems (easier to revoke if compromised)
- Monitor Access logs regularly for unusual service token activity
- cf-service-token.sh script location: `scripts/cf-service-token.sh`
