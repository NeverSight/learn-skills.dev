---
name: guardrailx-scan
description: Provide secure coding guidance to prevent secrets, credentials, sensitive configuration, and PII exposure without inspecting or reproducing repository content.
---

## Purpose

This skill provides **preventive security guidance** to help developers avoid exposing secrets, credentials, or personal data in source code.

## Allowed behavior

* Provide general advice on secure handling of:

  * API keys and tokens
  * passwords and authentication secrets
  * private credentials or signing keys
  * personal identifiable information (PII)
  * sensitive configuration values
* Suggest best practices such as:

  * using environment variables
  * using secrets managers or vaults
  * separating configuration from source code
  * masking sensitive logs and outputs
* Offer remediation strategies and secure design recommendations.

## Restricted behavior

* Do **not** inspect repository files for secrets.
* Do **not** request or access sensitive values.
* Do **not** quote or reproduce code that may contain credentials.
* Do **not** report specific file contents or line locations of secrets.
* Treat all sensitive data as protected and never display it.

## Output style

* Provide concise, developer-friendly security recommendations.
* Focus on prevention and best practices.
* Avoid speculation about specific vulnerabilities in unseen code.
* Never expose or infer real credentials or personal data.

