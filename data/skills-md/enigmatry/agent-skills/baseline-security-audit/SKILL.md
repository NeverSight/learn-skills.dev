---
name: baseline-security-audit
description: Ensures baseline security practices are followed in the project. Use this when asked to perform a security audit on the codebase. Automatically creates Jira stories for each security finding.
---

# Baseline Security Audit Skill

## Overview

This skill performs a comprehensive baseline security audit of the codebase by analyzing common security vulnerabilities and misconfigurations. For each security finding, it can automatically create Jira stories for tracking and remediation.

## What This Skill Does

This skill performs the following security checks (each with detailed guidance in the references folder):

1. **Secrets Management** - Scans for hardcoded secrets, credentials, and API keys
   - *See: references/secrets.md*

2. **Package Security** - Checks for insecure dependencies and outdated packages with known vulnerabilities
   - *See: references/packages.md*

3. **SQL Injection** - Identifies potential SQL injection vulnerabilities in database queries
   - *See: references/sql_injection.md*

4. **Exception Handling** - Reviews error handling patterns to prevent information disclosure
   - *See: references/exception_handling.md*

5. **Logging Security** - Validates logging practices and checks for sensitive data in logs
   - *See: references/logging.md*

6. **Sensitive Data in Logs** - Identifies logging of passwords, tokens, and other sensitive information
   - *See: references/sensitive_data_logging.md*

7. **Sensitive Query Strings** - Checks for sensitive data exposure in URL query parameters
   - *See: references/sensitive_query_strings.md*

8. **IDOR (Insecure Direct Object References)** - Analyzes authorization checks for object access
   - *See: references/idor.md*

9. **Output Encoding** - Validates proper encoding to prevent XSS attacks
   - *See: references/output_encoding.md*

10. **Input Validation** - Ensures all user input is validated server-side and client-side
    - *See: references/input_validation.md*

11. **Code Minification** - Verifies production builds are minified and source maps are secured
    - *See: references/code_minification.md*

12. **Environment Credentials** - Ensures different credentials per environment (dev/test/staging/prod)
    - *See: references/environment_credentials.md*

13. **Data Minimization** - Identifies unnecessary storage of sensitive/personal data (GDPR compliance)
    - *See: references/data_minimization.md*

14. **Data Storage Minimization** - Reviews database entities for minimal sensitive data storage
    - *See: references/data_storage_minimization.md*

15. **Cookie and Storage Security** - Validates secure cookie configuration and localStorage usage
    - *See: references/cookie_storage_security.md*

16. **Cryptography Security** - Ensures strong cryptographic algorithms for hashing and encryption
    - *See: references/cryptography_security.md*

17. **Security Headers** - Checks proper configuration of CSP, HSTS, X-Frame-Options, and other security headers
    - *See: references/security_headers.md*

18. **Version Info Headers** - Prevents disclosure of platform/version information in HTTP headers
    - *See: references/version_info_headers.md*

19. **HTTP Verb Whitelisting** - Ensures only necessary HTTP verbs are allowed, blocks unused methods
    - *See: references/http_verb_whitelisting.md*

20. **SSL/TLS Configuration** - Validates SSL/TLS protocol versions and cipher suites using SSL Labs analysis
    - *See: references/ssl_tls_configuration.md*
    - **Note**: Requires production URL. Ask the user for the URL at the start of the audit and store it as `PRODUCTION_URL` for this check.

Each check provides:
- Specific patterns to search for
- RED FLAGS to identify
- Prioritized findings (High/Medium/Low)
- Remediation guidance
- Code examples

## How to Use

Invoke this skill by asking for a security audit:
- "Perform a baseline security audit"
- "Check the codebase for security issues"
- "Run security checks on this project"

## Execution Flow

### Step 0 — Select Checks to Run (ask once, at the very start)

Before doing anything else, present the full list of available checks and ask the user which ones to run:

> "Which security checks would you like to run?
>
> | # | Check |
> |---|-------|
> | 1 | Secrets Management |
> | 2 | Package Security |
> | 3 | SQL Injection |
> | 4 | Exception Handling |
> | 5 | Logging Security |
> | 6 | Sensitive Data in Logs |
> | 7 | Sensitive Query Strings |
> | 8 | IDOR (Insecure Direct Object References) |
> | 9 | Output Encoding |
> | 10 | Input Validation |
> | 11 | Code Minification |
> | 12 | Environment Credentials |
> | 13 | Data Minimization |
> | 14 | Data Storage Minimization |
> | 15 | Cookie and Storage Security |
> | 16 | Cryptography Security |
> | 17 | Security Headers |
> | 18 | Version Info Headers |
> | 19 | HTTP Verb Whitelisting |
> | 20 | SSL/TLS Configuration |
>
> Reply with **`all`** to run all checks, or provide a comma-separated list of numbers (e.g. `1, 3, 5`) to run a specific subset."

Store the selected check numbers as `SELECTED_CHECKS`. Only run, report on, and create Jira stories for the selected checks.
Do **not** ask again during the audit.

## Jira Integration

### Step 1 — Collect the Jira Project Code (ask once, at the very start)

After confirming the selected checks, ask the user exactly once:

> "What is the Jira project code where security stories should be created? (e.g. `SEC`, `PROJ`)"

Store the answer as `JIRA_PROJECT_CODE` and reuse it for all subsequent story creation calls.
Do **not** ask again during the audit.

### Step 2 — Severity Normalization

Reference files use two different severity scales. Normalize all findings to a single Jira priority:

| Finding Severity (in reference output)     | Jira Priority |
|--------------------------------------------|---------------|
| 🔴 Critical / Critical                     | `Highest`     |
| 🟡 High / High / High Priority             | `High`        |
| 🟢 Medium / Medium / Medium Priority       | `Medium`      |
| 🔵 Low / Low / Low Priority                | `Low`         |

When a reference file uses `✅ SECURE / ⚠️ PARTIALLY SECURE / ❌ INSECURE` status markers,
map them as: `⚠️ PARTIALLY SECURE` → `Medium`, `❌ INSECURE` → `High`.

### Step 3 — Create a Jira Story for Each Finding

After completing **each individual check**, create one Jira story per finding using the
`create_issue` tool with the following fields:

| Field         | Value                                                                                  |
|---------------|----------------------------------------------------------------------------------------|
| `project`     | `JIRA_PROJECT_CODE` (collected above)                                                  |
| `issuetype`   | `Story`                                                                                |
| `summary`     | `[Security Audit] <Check Name>: <short finding title>`                                 |
| `description` | Finding location (file + line number), description of the issue, remediation steps     |
| `labels`      | `BaselineSecurity`                                                                     |
| `priority`    | Mapped from the normalization table above                                              |

**Example summary:** `[Security Audit] Secrets Management: Hardcoded API key in appsettings.json`

After each `create_issue` call succeeds, echo the created story key inline in the audit output,
for example: *(→ created [PROJ-42](https://enigmatry.atlassian.net/browse/PROJ-42))*

### Step 4 — Final Summary Table

After all selected checks are complete, output a consolidated table of all created stories:

| Story Key | Check | Summary | Priority |
|-----------|-------|---------|----------|
| PROJ-42   | Secrets Management | Hardcoded API key in appsettings.json | High |
| ...       | ...   | ...     | ...      |

If no findings were produced for a check, skip story creation for that check silently.
