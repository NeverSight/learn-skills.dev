---
name: jinko-sdk-setup
description: Authenticate and configure access to a Jinkō project via the jinko-sdk. Use this skill whenever the user wants to connect to Jinkō, install the SDK, set up credentials or a .env file, verify API access, fail-fast check that a JINKO_API_KEY and JINKO_PROJECT_ID work, or debug ConfigurationError, AuthenticationError, or AuthorizationError from the SDK. Do not use this skill for creating models, vpops, protocols, output sets, or trials.
compatibility: Requires Python 3.11+ and network access. The validation script diagnoses missing or outdated SDK installations, credentials, and optional python-dotenv support.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Jinkō SDK Setup

Use this skill for SDK setup and credential checks only. Keep the user focused on proving that Python can authenticate against Jinkō and read one project item list before moving to model, vpop, protocol, output-set, or trial workflows.

BE CAREFUL: the right package is `jinko-sdk` that export a `jinko` module. `jinko` is a different package unrelated to the Jinko SDK.

## Workflow

> **SDK VERSION PREREQUISITE:** Run the check below. It ships with the SDK and
> verifies the installed SDK against every neighboring SDK-dependent skill
> before API access.

Run the deterministic check and follow its success or error message:

```bash
python -m jinko.cli.check_jinko_connection
```

The script:

- Loads `.env` when `python-dotenv` is installed.
- Redacts sensitive values when showing configuration.
- Requires both `JINKO_API_KEY` and `JINKO_PROJECT_ID`.
- Constructs `JinkoClient()` from environment variables.
- Calls `client.auth_check()` to prove authentication.
- Calls `client.search(limit=1, show_table=False, show_table_hint=False)` to prove minimal read-only project-item access.
- Prints minimal output on success.

Use `--show-config` only when debugging local setup; it prints presence and redacted values, never the full API key.

## After Validation

Once the connection check passes, prefer `client.search(...)` for project exploration because it gives the user an immediate view across project items.

Use a minimal example like:

```python
from jinko import JinkoClient

client = JinkoClient()
client.search(limit=20, columns="compact")
```

Use `search()` when the user wants to:

- browse what exists in the configured project
- find an item by name or free text
- orient themselves before choosing a model, protocol, vpop, or trial workflow

The setup script uses a one-item, non-rendered `search()` only as its project-read check after authentication. Use a larger interactive `search()` only for exploration after validation succeeds.

## Troubleshooting

Run the check again and act on its deterministic diagnostic. Do not replace it with ad hoc checks or ask the user to share secrets.
