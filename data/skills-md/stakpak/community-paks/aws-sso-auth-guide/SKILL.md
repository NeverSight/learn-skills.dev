---
name: aws-sso-auth-guide
description: AWS SSO discovery, configuration, and terminal usage
license: MIT
tags:
  - aws
  - sso
  - authentication
  - iam-identity-center
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.2"
---

# AWS SSO Terminal Guide

## Discovery: Finding SSO Configuration

### Get SSO Instance & Portal URL

```bash
# From management account
aws sso-admin list-instances --profile <mgmt-profile>
# Returns: InstanceArn, IdentityStoreId (d-xxxxxxxxxx), OwnerAccountId

# Portal URL format: https://d-xxxxxxxxxx.awsapps.com/start
```

### List Accounts & Permission Sets

```bash
# List organization accounts
aws organizations list-accounts --profile <mgmt-profile>

# List permission sets
aws sso-admin list-permission-sets \
  --instance-arn <instance-arn> \
  --profile <mgmt-profile>

# Get permission set name
aws sso-admin describe-permission-set \
  --instance-arn <instance-arn> \
  --permission-set-arn <ps-arn> \
  --profile <mgmt-profile>

# Check account assignments
aws sso-admin list-account-assignments \
  --instance-arn <instance-arn> \
  --account-id <account-id> \
  --permission-set-arn <ps-arn> \
  --profile <mgmt-profile>
```

## Configuration

### Profile Structure (Recommended)

```ini
# ~/.aws/config

[profile my-profile]
sso_session = my-sso
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
region = us-east-1

[sso-session my-sso]
sso_start_url = https://d-xxxxxxxxxx.awsapps.com/start
sso_region = us-east-1
sso_registration_scopes = sso:account:access
```

**Benefits:** Token reuse across profiles, automatic refresh (CLI v2.22.0+)

### Interactive Configuration

```bash
aws configure sso
```

## Authentication

### Login Flow

```bash
# Login (PKCE auth - default in CLI v2.22.0+)
aws sso login --profile my-profile

# Login with device code (for headless/remote)
aws sso login --profile my-profile --use-device-code

# Verify
aws sts get-caller-identity --profile my-profile
```

**Token Cache:** `~/.aws/sso/cache/`

## Key Endpoints & Flow

- `oidc.{region}.amazonaws.com` - OIDC authentication
- `portal.sso.{region}.amazonaws.com` - SSO portal
- Auth flow: `RegisterClient` → `StartDeviceAuthorization` → `CreateToken`

## Troubleshooting

**Missing SSO Configuration:**

```bash
# Error: Missing sso_start_url, sso_region
# Fix: aws configure sso
```

**Expired Token:**

```bash
# Error: Token is expired
# Fix: aws sso login --profile my-profile
```

**Proxy SSL Issues:**

```bash
# Error: SSL certificate verification failed
# Fix: Set AWS_CA_BUNDLE to proxy CA certificate
export AWS_CA_BUNDLE=/path/to/proxy-ca.crt
```

**Access Denied:**

```bash
# Check permission set assignments
aws sso-admin list-account-assignments \
  --instance-arn <arn> \
  --account-id <id> \
  --permission-set-arn <ps-arn>
```

## Quick Reference

**CLI Versions:**

- v2.22.0+: PKCE auth (default), auto-refresh
- < v2.22.0: Device code auth

**Authorization Types:**

- **PKCE**: Same-device, browser required
- **Device Code**: Cross-device, browser optional
