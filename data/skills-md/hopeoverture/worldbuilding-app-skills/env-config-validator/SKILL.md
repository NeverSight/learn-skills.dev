---
name: env-config-validator
description: Validate environment configuration files across local, staging, and production environments. Ensure required secrets, database URLs, API keys, and public variables are properly scoped and set. Use this skill when setting up environments, validating configuration, checking for missing secrets, auditing environment variables, ensuring proper scoping of public vs private vars, or troubleshooting environment issues. Trigger terms include env, environment variables, secrets, configuration, .env file, environment validation, missing variables, config check, NEXT_PUBLIC, env vars, database URL, API keys.
---

# Environment Configuration Validator

Validate `.env` files across local, staging, and production environments. Ensure all required secrets, database URLs, API keys, and public variables are properly scoped, set, and secure.

## Core Capabilities

### 1. Validate Environment Files

To validate environment configuration:

- Parse `.env`, `.env.local`, `.env.production`, etc.
- Check for required variables
- Verify variable naming conventions
- Detect security issues (exposed secrets, weak values)
- Use `scripts/validate_env.py` for automated validation

### 2. Check Variable Scoping

Ensure proper scoping of environment variables:

- **Public variables** (`NEXT_PUBLIC_*`): Accessible in browser
- **Private variables**: Server-side only
- **Database credentials**: Never exposed to client
- **API keys**: Properly scoped based on usage

### 3. Cross-Environment Validation

Compare configurations across environments:

- Identify missing variables in staging/production
- Check for environment-specific overrides
- Ensure consistency in variable names
- Validate environment-specific values (URLs, keys)

### 4. Security Auditing

Detect security vulnerabilities in environment configuration:

- Exposed secrets in public variables
- Weak or default values
- Hardcoded credentials in code
- Missing required security variables (JWT secrets, encryption keys)

## Validation Rules

### Required Variables

Ensure these categories of variables are present:

1. **Database Connection**
   - `DATABASE_URL` or equivalent
   - Connection pool settings (optional)

2. **Authentication**
   - `JWT_SECRET` or `AUTH_SECRET`
   - OAuth credentials (if using OAuth)
   - Session secrets

3. **External APIs**
   - Third-party API keys
   - Service endpoints
   - Rate limiting tokens

4. **Application Config**
   - `NODE_ENV`
   - `NEXT_PUBLIC_APP_URL` or `APP_URL`
   - Feature flags (optional)

5. **Email/Notifications** (if used)
   - SMTP credentials
   - Email service API keys

### Naming Conventions

Follow Next.js environment variable conventions:

- **Public variables**: `NEXT_PUBLIC_*` prefix
  - Example: `NEXT_PUBLIC_API_URL`
  - Accessible in browser
  - Never put secrets here

- **Private variables**: No prefix
  - Example: `DATABASE_URL`, `API_SECRET`
  - Server-side only
  - Safe for secrets

- **Naming style**: `SCREAMING_SNAKE_CASE`
  - Example: `DATABASE_URL`, `JWT_SECRET`, `STRIPE_API_KEY`

### Security Rules

1. **Never expose secrets in public variables**
   - [ERROR] `NEXT_PUBLIC_DATABASE_URL`
   - [OK] `DATABASE_URL`

2. **Database URLs must be private**
   - [ERROR] `NEXT_PUBLIC_DB_URL`
   - [OK] `DATABASE_URL`

3. **API keys scoping**
   - Client-side API keys → `NEXT_PUBLIC_*` (e.g., Google Maps)
   - Server-side API keys → No prefix (e.g., Stripe secret)

4. **No hardcoded secrets in code**
   - Use environment variables for all secrets
   - Never commit `.env.local` or `.env.production`

5. **Strong secrets**
   - JWT/session secrets: minimum 32 characters
   - Use cryptographically random values
   - No default or example values in production

## Validation Script

Use `scripts/validate_env.py` to automate validation:

```bash
# Validate current .env file
python scripts/validate_env.py

# Validate specific file
python scripts/validate_env.py --file .env.production

# Compare multiple environments
python scripts/validate_env.py --compare .env.local .env.production

# Check against required variables template
python scripts/validate_env.py --template .env.example
```

The script checks:
- Required variables are present
- Naming conventions are followed
- No secrets in public variables
- No weak or default values
- Consistent naming across environments

## Common Issues and Solutions

### Issue: Missing DATABASE_URL in Production

**Detection**: Script reports missing required variable

**Solution**:
```bash
# Add to .env.production
DATABASE_URL="postgresql://user:password@host:5432/dbname"
```

**Note**: Use different databases for dev/staging/prod

### Issue: Secret Exposed in Public Variable

**Detection**: Script finds `NEXT_PUBLIC_` prefix on secret

**Problem**:
```bash
# [ERROR] WRONG - secret exposed to browser
NEXT_PUBLIC_API_SECRET="secret123"
```

**Solution**:
```bash
# [OK] CORRECT - server-side only
API_SECRET="secret123"
```

### Issue: Weak JWT Secret

**Detection**: Script detects short or weak secret

**Problem**:
```bash
# [ERROR] WRONG - too short, predictable
JWT_SECRET="secret"
```

**Solution**:
```bash
# [OK] CORRECT - strong, random, 32+ characters
JWT_SECRET="a8f3d9c2e1b7f4a6d8c3e9b2f1a7d4c8e3b9f2a1d7c4e8b3f9a2d1c7e4b8f3a9"
```

Generate with:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### Issue: Inconsistent Variable Names Across Environments

**Detection**: Script comparison shows name mismatch

**Problem**:
```bash
# .env.local
DATABASE_URL="..."

# .env.production
DB_URL="..."  # [ERROR] Different name
```

**Solution**: Use consistent names
```bash
# Both files
DATABASE_URL="..."
```

### Issue: Missing Public API URL

**Detection**: Client-side code fails to connect to API

**Problem**: `NEXT_PUBLIC_API_URL` not set

**Solution**:
```bash
# .env.local
NEXT_PUBLIC_API_URL="http://localhost:3000"

# .env.production
NEXT_PUBLIC_API_URL="https://api.yourapp.com"
```

## Resource Files

### scripts/validate_env.py
Python script to validate environment files, check for security issues, compare across environments, and verify against templates. Provides detailed error messages and suggestions.

### references/env_best_practices.md
Comprehensive guide to environment variable management including:
- Security best practices
- Naming conventions
- Scoping rules (public vs private)
- Common patterns for different services
- Environment-specific configuration
- Secret rotation strategies

### assets/.env.example
Template showing all required environment variables for a worldbuilding application. Use as a reference for setting up new environments or auditing existing ones.

## Environment-Specific Configuration

### Development (.env.local)

```bash
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/worldbuilding_dev"

# Authentication
JWT_SECRET="dev-secret-change-in-production"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="dev-nextauth-secret"

# Public
NEXT_PUBLIC_API_URL="http://localhost:3000"
NEXT_PUBLIC_APP_NAME="Worldbuilding App (Dev)"

# External APIs (test keys)
OPENAI_API_KEY="sk-test-..."
STRIPE_SECRET_KEY="sk_test_..."
```

### Staging (.env.staging)

```bash
# Database
DATABASE_URL="postgresql://user:password@staging-db.com:5432/worldbuilding_staging"

# Authentication
JWT_SECRET="staging-secret-32-chars-minimum"
NEXTAUTH_URL="https://staging.yourapp.com"
NEXTAUTH_SECRET="staging-nextauth-secret"

# Public
NEXT_PUBLIC_API_URL="https://staging.yourapp.com"
NEXT_PUBLIC_APP_NAME="Worldbuilding App (Staging)"

# External APIs (test keys)
OPENAI_API_KEY="sk-test-..."
STRIPE_SECRET_KEY="sk_test_..."
```

### Production (.env.production)

```bash
# Database
DATABASE_URL="postgresql://user:password@prod-db.com:5432/worldbuilding_prod"

# Authentication
JWT_SECRET="production-secret-use-crypto-random-32-chars-minimum"
NEXTAUTH_URL="https://yourapp.com"
NEXTAUTH_SECRET="production-nextauth-secret"

# Public
NEXT_PUBLIC_API_URL="https://api.yourapp.com"
NEXT_PUBLIC_APP_NAME="Worldbuilding App"

# External APIs (production keys)
OPENAI_API_KEY="sk-live-..."
STRIPE_SECRET_KEY="sk_live_..."

# Monitoring
SENTRY_DSN="https://..."
```

## Best Practices

1. **Never commit secrets**
   - Add `.env.local`, `.env.production` to `.gitignore`
   - Commit `.env.example` as a template

2. **Use strong, random secrets**
   - Minimum 32 characters for JWT/session secrets
   - Use `crypto.randomBytes()` or password manager

3. **Scope variables correctly**
   - Public (`NEXT_PUBLIC_*`): Only non-sensitive, client-accessible data
   - Private (no prefix): All secrets, credentials, server-only config

4. **Consistent naming**
   - Use same variable names across all environments
   - Follow `SCREAMING_SNAKE_CASE` convention

5. **Environment-specific values**
   - Different database URLs per environment
   - Test API keys in dev/staging, production keys in prod
   - Environment-specific URLs and endpoints

6. **Document required variables**
   - Keep `.env.example` updated
   - Add comments explaining each variable
   - Document where to get values (API dashboard, etc.)

7. **Validate on deployment**
   - Run validation script in CI/CD pipeline
   - Fail deployment if required variables missing
   - Check for security issues before deploying

8. **Rotate secrets regularly**
   - Change JWT secrets periodically
   - Rotate API keys on schedule
   - Update after team member departures

9. **Use secret management tools**
   - Consider Vercel Environment Variables
   - AWS Secrets Manager, HashiCorp Vault for sensitive data
   - Never store production secrets in code or comments

10. **Test environment parity**
    - Staging should mirror production as closely as possible
    - Use same variable names, just different values
    - Test with production-like data

## Integration with Worldbuilding App

Common environment variables for worldbuilding applications:

### Database
```bash
DATABASE_URL="postgresql://..."
DATABASE_POOL_SIZE="10"  # Optional
```

### Authentication
```bash
JWT_SECRET="..."
NEXTAUTH_URL="..."
NEXTAUTH_SECRET="..."
```

### External APIs
```bash
# AI services (optional)
OPENAI_API_KEY="..."

# Maps (if using)
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY="..."

# Image hosting (if using)
CLOUDINARY_URL="..."
```

### Application
```bash
NODE_ENV="production"
NEXT_PUBLIC_APP_URL="https://..."
NEXT_PUBLIC_APP_NAME="Worldbuilding App"
```

### Email (if using)
```bash
SMTP_HOST="..."
SMTP_PORT="587"
SMTP_USER="..."
SMTP_PASSWORD="..."
```

Consult `references/env_best_practices.md` for detailed guidance and `assets/.env.example` for a complete template.
