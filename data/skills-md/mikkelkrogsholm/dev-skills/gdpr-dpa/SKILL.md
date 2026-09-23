---
name: gdpr-dpa
description: "Generate a GDPR-compliant Data Processing Agreement (DPA) for a project. Use when asked to create, generate, or write a DPA or data processing agreement. Autonomously scans the project to identify all sub-processors (third-party services that handle personal data), then generates a minimal Article 28-compliant DPA covering actual data flows — no compliance theater, no unnecessary boilerplate. Works with any language or framework."
---

# GDPR DPA Generator

Generate a minimal, accurate DPA by scanning the project rather than interviewing the user.

## Workflow

### Step 1: Discover Sub-processors

Scan the project for service fingerprints. Check ALL of the following (not just package.json — this must work for any language):

**Dependency files** (read whichever exist):
- Node.js: `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- Python: `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py`
- Ruby: `Gemfile`
- Go: `go.mod`
- Rust: `Cargo.toml`
- PHP: `composer.json`
- Dart/Flutter: `pubspec.yaml`

**Infrastructure and config files:**
- `docker-compose.yml`, `Dockerfile`
- `.env.example`, `.env.sample`, `.env.template`
- `coolify.yaml`, `render.yaml`, `railway.toml`, `fly.toml`
- Any `*.config.*`, `*.toml`, `*.yaml`, `*.ini`

**Source code signals:**
- Import/require statements for known SDK packages
- Direct HTTP calls to known API endpoints (`api.stripe.com`, `sentry.io`, `api.resend.com`, etc.)
- Environment variable names that reveal services (`STRIPE_SECRET_KEY`, `SENTRY_DSN`, `RESEND_API_KEY`, etc.)

Cross-reference every discovered service against `references/sub-processors.md` to get GDPR metadata.

### Step 2: Identify Personal Data Types

Scan schema files, models, and form handlers to identify what personal data is actually processed:
- User identity: name, email, username, phone
- Location: address, IP address, coordinates
- Financial: payment methods, transaction history
- Behavioral: activity logs, session data, analytics events
- Device: user agent, device ID
- Sensitive: health data, biometrics (flag these — Article 9 requires explicit consent)

### Step 3: Flag Issues

Before generating, list any issues found:
- Services detected but NOT in sub-processors.md (unknown sub-processor — user must add manually)
- Services using non-EU regions when EU region is available (flag with recommended config)
- Sensitive data (Article 9) detected without evidence of explicit consent mechanism
- Services where DPA URL could not be confirmed (mark as "verify link")
- No `.env.example` found — sub-processor list may be incomplete

### Step 4: Generate the DPA

Use `references/dpa-template.md` as the template. Fill in:
- **Annex A (Sub-processors)**: list every identified sub-processor with their role and DPA link
- **Data types section**: the personal data categories found in Step 2
- **Purpose of processing**: inferred from the project (auth, payments, error tracking, etc.)
- Leave `[YOUR COMPANY NAME]` and `[CUSTOMER COMPANY NAME]` as placeholders
- Leave `[DATE]` as a placeholder
- Add a note at the top: "Generated from project scan — review before use. Not legal advice."

Output the DPA as a Markdown document ready to save as `DPA.md` in the project root.
