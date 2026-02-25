---
name: cloudflare-access-add-user
description: |
  Adds new users to Cloudflare Access authentication by updating ACCESS_ALLOWED_EMAIL in .env
  and syncing policies to all protected services. Use when you need to grant access to a new
  user, add someone to the network, share service access, or update allowed emails. Triggers
  on "add user to access", "grant access to [email]", "add [email] to cloudflare", "share
  access with", "allow [email] to authenticate", or "update access users". Works with .env,
  update-access-emails.sh, and Cloudflare Access policies for pihole, jaeger, langfuse,
  sprinkler, ha, and temet.ai services.
allowed-tools:
  - Read
  - Edit
  - Bash
  - Grep
---

# Add Access User Skill

Grant users access to Cloudflare Access protected services by updating authentication policies.

## Quick Start

To add a new user:
```
Add user@example.com to Cloudflare Access
```

The skill will:
1. Add the email to ACCESS_ALLOWED_EMAIL in .env
2. Update the update-access-emails.sh script with new email list
3. Run the script to sync policies to Cloudflare
4. Verify policies updated for all 6 protected services
5. Provide test instructions for the new user

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Add [email] to Cloudflare Access"
- "Grant access to [email]"
- "Allow [email] to authenticate"
- "Share service access with [email]"
- "Update access users"

**Implicit Triggers:**
- User mentions sharing network access with family/colleagues
- User wants to grant remote access to services
- User asks about multi-user authentication

**Debugging Triggers:**
- "User [email] can't log in"
- "Access denied for [email]"
- "How do I add another user?"

## What This Skill Does

1. **Validates Email** - Ensures valid email format
2. **Checks Duplicates** - Prevents adding existing users
3. **Updates .env** - Adds email to ACCESS_ALLOWED_EMAIL
4. **Updates Script** - Modifies update-access-emails.sh with new email list
5. **Syncs Policies** - Runs script to update Cloudflare Access policies
6. **Verifies** - Confirms all 6 services updated successfully
7. **Provides Test Steps** - Instructions for new user to verify access

## Instructions

### 3.1 Gather Email Address

Ask user for the email address(es) to add. Accept:
- Single email: `user@example.com`
- Multiple emails: `user1@example.com, user2@example.com`

### 3.2 Validate Email Format

```python
import re
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))
```

### 3.3 Read Current Configuration

Read current ACCESS_ALLOWED_EMAIL from .env:

```bash
grep -E "^ACCESS_ALLOWED_EMAIL" /home/dawiddutoit/projects/network/.env
```

Current format: `ACCESS_ALLOWED_EMAIL="email1,email2,email3"`

### 3.4 Check for Duplicates

Before adding, verify email is not already in the list.

### 3.5 Update .env File

Edit `/home/dawiddutoit/projects/network/.env`:

**Before:**
```
ACCESS_ALLOWED_EMAIL="dawiddutoit@temet.ai,fifthchildd@gmail.com"
```

**After (adding dawidddutoit@gmail.com):**
```
ACCESS_ALLOWED_EMAIL="dawiddutoit@temet.ai,fifthchildd@gmail.com,dawidddutoit@gmail.com"
```

### 3.6 Update update-access-emails.sh Script

The script at `/home/dawiddutoit/projects/network/scripts/update-access-emails.sh` has hardcoded email addresses in the policy JSON. Update the `include` array to match all emails:

**Location in script (around line 48-52):**
```json
"include": [
    {"email": {"email": "dawiddutoit@temet.ai"}},
    {"email": {"email": "fifthchildd@gmail.com"}},
    {"email": {"email": "dawidddutoit@gmail.com"}},
    {"email": {"email": "NEW_EMAIL_HERE"}}
]
```

### 3.7 Run Update Script

```bash
cd /home/dawiddutoit/projects/network && ./scripts/update-access-emails.sh
```

**Expected output:**
```
Updating policies for all services to include all three emails...

Processing app: 56de3246-c9ed-4877-8af1-dc360ac49584
  Updating policy: <policy-id>
  [checkmark] Policy updated successfully

Processing app: 9f1e8109-3f3f-456e-94f5-093bfc9e1c1e
  ...
  [checkmark] Policy updated successfully

All policies updated!
```

### 3.8 Verify Policies Updated

All 6 protected services should show success:
- Services Dashboard (temet.ai)
- Home Assistant (ha.temet.ai)
- Sprinkler System (sprinkler.temet.ai)
- Langfuse Monitoring (langfuse.temet.ai)
- Jaeger Tracing (jaeger.temet.ai)
- Pi-hole Admin (pihole.temet.ai)

### 3.9 Provide Test Instructions

Give the new user these steps:

```
ACCESS GRANTED FOR: [email]

To test your access:
1. Open an incognito/private browser window
2. Navigate to: https://pihole.temet.ai
3. Click "Google" to authenticate
4. Sign in with your Google account: [email]
5. After successful authentication, you should see Pi-hole admin

All accessible services:
- https://pihole.temet.ai (Pi-hole DNS admin)
- https://jaeger.temet.ai (Jaeger tracing)
- https://langfuse.temet.ai (Langfuse monitoring)
- https://sprinkler.temet.ai (Sprinkler system)
- https://ha.temet.ai (Home Assistant)
- https://temet.ai (Services dashboard)
```

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Technical details, API structure, troubleshooting |
| `examples/examples.md` | Common scenarios and edge cases |

## Expected Outcomes

**Success:**
- Email added to ACCESS_ALLOWED_EMAIL in .env
- Script updated with new email in include array
- All 6 Cloudflare Access policies updated
- New user can authenticate via Google OAuth

**Partial Success:**
- .env updated but script needs manual sync
- Some policies failed (rare - API rate limiting)

**Failure Indicators:**
- "Policy update failed" in script output
- Email validation error
- Duplicate email detected
- API token expired or missing permissions

## Requirements

**Environment:**
- Valid `.env` with CLOUDFLARE_ACCESS_API_TOKEN
- CLOUDFLARE_ACCOUNT_ID set correctly
- Network connectivity to Cloudflare API

**For non-workspace Gmail accounts:**
If adding personal Gmail (not @temet.ai), Google OAuth consent screen must be set to "External":
1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Change User Type from "Internal" to "External"
3. Save changes

**Tools needed:**
- Read (check current .env)
- Edit (update .env and script)
- Bash (run update script)
- Grep (check for duplicates)

## Red Flags to Avoid

- [ ] Do not add invalid email format
- [ ] Do not add duplicate emails (check first)
- [ ] Do not forget to update BOTH .env AND the script
- [ ] Do not skip running update-access-emails.sh after editing
- [ ] Do not skip verification of all 6 services
- [ ] Do not assume non-workspace emails will work without OAuth consent change
- [ ] Do not modify the bypass policy for webhook.temet.ai
- [ ] Do not run cf-access-setup.sh (that's for initial setup, not adding users)

## Notes

- The script has hardcoded app IDs for the 6 protected services
- Webhook (webhook.temet.ai) has bypass policy and is NOT affected
- Session duration is 24 hours - users must re-authenticate daily
- Access logs available at: https://one.dash.cloudflare.com -> Logs -> Access
- Google OAuth requires the email to match exactly (case-insensitive)
- Multiple emails are comma-separated with no spaces after commas
