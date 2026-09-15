---
name: private-context-bootstrap
description: Bootstrap private, remote-backed user context onto a fresh machine for opportunity workflows without committing personal data to public repositories.
---

# Private Context Bootstrap

## Purpose

Use this skill when an agent needs private user data that must be available across machines, but must not be hardcoded into public skills, prompts, logs, or repositories.

This skill defines how to locate, clone, decrypt, validate, and materialize private local files from remote storage.

## Core Principle

Skills are public process definitions. Private data lives outside public skill folders.

## Architecture

Use three layers:

1. Public skill repository: generic skills, schemas, fake examples, scripts, and documentation. No real personal values.
2. Private remote data repository: private YAML, JSONL logs, document manifests, criteria, and optionally PDFs. Prefer file-level encryption.
3. Secret manager: bootstrap secrets and encryption keys.

Recommended default:

- Private Git repository for versioned private data.
- `age` + `sops` for encrypted YAML/JSON files.
- Git LFS or encrypted archive for PDFs if PDFs are stored in Git.
- Bitwarden Secrets Manager stores the private repo URL if needed, the `age` private key, optional access tokens, and optional bootstrap environment variables.

Do not rely on untracked local files as the only source of truth.

## Environment Variables

Support these variables:

```bash
AGENTDESK_PRIVATE_REMOTE=""
AGENTDESK_PRIVATE_HOME="$HOME/.config/AgentDesk/private"
AGENTDESK_PRIVATE_REPO="$HOME/.local/share/AgentDesk/private-repo"
AGENTDESK_PROFILE_PATH="$AGENTDESK_PRIVATE_HOME/job-applications/application-profile.yaml"
AGENTDESK_DOCUMENT_MANIFEST_PATH="$AGENTDESK_PRIVATE_HOME/job-applications/document-manifest.yaml"
AGENTDESK_FIELD_POLICY_PATH="$AGENTDESK_PRIVATE_HOME/job-applications/field-answer-policy.yaml"
AGENTDESK_APPLICATION_LOG_PATH="$AGENTDESK_PRIVATE_HOME/job-applications/application-log.jsonl"
```

If variables are absent, use the defaults above.

## Bootstrap Workflow

On a fresh machine:

1. Check whether `AGENTDESK_PRIVATE_HOME` exists.
2. Check whether required private files exist.
3. If missing, locate the remote source from `AGENTDESK_PRIVATE_REMOTE`, the configured secret manager, or the user.
4. Clone or sync the private remote source into `AGENTDESK_PRIVATE_REPO`.
5. If files are encrypted, decrypt them into `AGENTDESK_PRIVATE_HOME`.
6. If PDFs are stored remotely, download or sync them.
7. Validate all required files against schemas.
8. Verify referenced documents exist.
9. Refuse to run workflows until validation passes.

Use `scripts/bootstrap-private-context.sh` from the OpportunityOS repo when available. It coordinates clone/sync, materialization, validation, and the readiness report.

## Never Do This

- Never commit decrypted private files to a public repository.
- Never print full private profiles into terminal logs unless explicitly requested.
- Never paste secrets, personal data, or private PDFs into public files.
- Never assume files exist on a fresh machine.
- Never invent missing private values.
- Never silently overwrite private data without making a backup.

## Expected Local Layout

After bootstrap:

```text
$AGENTDESK_PRIVATE_HOME/
  shared/
    personal-profile.yaml
  job-applications/
    application-profile.yaml
    document-manifest.yaml
    field-answer-policy.yaml
    application-log.jsonl
    documents/
      resume.pdf
      degree.pdf
      transcript.pdf
      references.pdf
      supporting-bundle.pdf
```

`shared/personal-profile.yaml` must follow the `bitwarden-personal-profile` schema. Domain folders reference it instead of duplicating identity, contact, address, employment, housing, or generic form facts.

Filenames may differ. Agents must use references and manifests, not hardcoded filenames.

## Required Checks

Before any workflow uses private data:

1. Confirm profile file exists.
2. Confirm shared personal profile exists and follows the Bitwarden personal profile shape.
3. Confirm document manifest exists.
4. Confirm field policy exists.
5. Confirm referenced document paths exist if needed.
6. Validate schemas.
7. Report missing files clearly.

## Output

Return private home path, private repo path, profile file status, document manifest status, field policy status, document availability summary, validation errors, and next manual action.
