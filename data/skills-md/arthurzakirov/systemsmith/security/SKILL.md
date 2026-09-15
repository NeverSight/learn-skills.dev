---
name: security
description: Mandatory credential protection skill for all agents. Prevents reading, exposing, or leaking credentials, secrets, API keys, tokens, passwords, and auth-capable config files.
---

# Credential And Data Protection

## Core Principle

Judge sensitivity by what a file could contain, not by where it lives. If a file type can hold auth data, treat it as sensitive unless clearly proven otherwise.

## Generalization Principle

When a security lesson is learned for one kind of sensitive data, generalize the fix across the whole category rather than protecting only the exact instance that triggered the lesson.

Categories include:

- Credentials
- PII
- Customer data
- Infrastructure secrets
- Sensitive logs and error output

## Safe Exceptions

Source code that reads credentials from env vars or secret managers is not itself sensitive unless it embeds real values.

Test and development credentials tied only to dummy systems may be acceptable to inspect, but production and personal credentials remain strictly protected. When in doubt, ask.

## Proactive Reporting

If you spot a likely security problem or accidentally see sensitive credential material, warn the user immediately without repeating the secret value.

## Never Read Sensitive Files

Do not read auth-capable files such as:

- `.env` or `.env.*`
- `.npmrc`
- `.yarnrc` or `.yarnrc.yml`
- `.netrc`
- `.ssh/*`
- `.aws/credentials`
- Package-manager auth files
- Any path containing words like `secret`, `credential`, or `token`

Apply the principle beyond this list when a filename suggests it can contain secrets.

If a file passes by name but appears to contain credential-like content, stop and ask the user which parts are safe to inspect.

## Never Expose Credentials Via Output

Avoid:

- Printing env vars
- Inline credentials in command arguments
- Logs that reveal tokens, passwords, or personal data
- Debug output that dumps headers or secret-bearing configs

## Secure Error Handling

Treat error messages as a leak surface. Standard library and CLI exceptions can embed credential values.

Mitigations:

1. Strip and validate credential env vars at read time.
2. Wrap HTTP and subprocess calls so low-level exceptions do not surface raw credential-bearing values.
3. Prefer env vars over command-line arguments for secrets.
4. Treat redaction hooks as a fallback, not a primary control.

## Sensitive Business Data

Treat customer data, ticket exports, API responses, CSVs, and database query results as confidential even when they are not credentials. Do not print raw values unless the user explicitly confirms it is safe.

## LLM-Safe Logging

When scripts produce paths to sensitive files, phrase the message so a human knows to inspect it and the assistant knows not to read it.

Good pattern:

```text
/tmp/users.json — WARNING: Contains sensitive data. Only a human should review it.
```

## AI-Blind Debugging

When a script may emit sensitive diagnostic output, prefer having the human run it in a separate terminal and report back only safe summaries such as the error type.
