---
name: secrets-safety
description: >-
  Protect credentials and other secrets while coding, debugging, configuring
  infrastructure, or reviewing logs and files. Use whenever work touches API
  keys, tokens, passwords, private keys, environment files, secret stores, or a
  suspected exposure. Prefer metadata and write-only/reference mechanisms over
  retrieving secret values.
---

# Secrets safety

Treat credential values as sensitive even in development environments. Avoid
retrieving, echoing, logging, copying, or committing resolved secret values.
Use the platform's reference mechanism or a secure input channel instead.

## Safe handling

- Inspect secret names and metadata only when sufficient; do not print the
  backing values to learn what they contain.
- Do not read environment files or credential stores to display values. Do not
  paste secrets into source, docs, prompts, command arguments, issue comments,
  logs, or commits.
- When one service needs another service's credential, use the provider's
  secret reference/identity mechanism rather than reading and copying the
  resolved value.
- For write operations, prefer stdin, a secret manager, or a scoped reference;
  avoid shell history and process arguments that may expose values.
- Redact logs and diagnostic output before sharing them. Check output files and
  staged diffs for accidental credentials before publishing.

## If a secret may have been exposed

1. Do not repeat or copy the value into another location.
2. Tell the user what kind of material may have been exposed and where, without
   reproducing the credential.
3. Recommend revocation/rotation and assess the exposure window and affected
   systems.
4. Remove the value from active files and reachable surfaces when authorized;
   do not rewrite shared history or perform destructive cleanup without
   authorization.
5. Verify remediation using names, status, or fingerprints that do not reveal
   the secret itself.

## Before completing a task

- No credential value appears in tool output, logs, diffs, or response text.
- No literal secret was written to configuration, examples, scripts, or docs.
- Any diagnostics shared with the user are redacted.
- Rotation or cleanup that remains is clearly identified rather than claimed
  complete.
