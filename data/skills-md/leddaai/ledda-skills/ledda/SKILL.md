---
name: ledda
description: Search and debug LLM traces from Ledda's observability platform. Find errors, compare traces, analyze costs and tokens.
version: 1.0.0
license: MIT
---

# Ledda Skill

Connect to Ledda's LLM observability platform to search traces, inspect errors, compare runs, and analyze costs — from any AI coding agent.

## User-Invocable Skills

### /ledda onboarding

Set up Ledda credentials for this project.

**When the user runs `/ledda onboarding`:**

1. Look for a credentials block in the user's message. The block contains ini-formatted sections like:

```
[account-42]
api_key = ldda_ak_...
account_name = Production
base_url = https://app.ledda.ai
```

2. Write the credentials to `.ledda/.credentials` in the project root. If the file already exists, ask the user if they want to overwrite or merge.

3. Add `.ledda/` to the project's `.gitignore` if not already present.

4. Confirm which accounts were configured by listing account names.

### /ledda

Search and debug LLM traces using Ledda's API.

**When the user runs `/ledda` (with or without a follow-up question):**

1. Read `.ledda/.credentials` to discover available accounts and their API keys.
   - If `.ledda/.credentials` doesn't exist, tell the user to run onboarding from the Ledda UI first (Settings > AI Agent Integration).

2. Check the documentation version:
   - Call `GET <base_url>/docs/version` (no auth needed) to get the current content hash.
   - Check if `.ledda/<hash>/` directory exists locally.
   - If not, fetch the latest docs:
     - `GET <base_url>/docs/md/reference` → save to `.ledda/<hash>/reference.md`
     - `GET <base_url>/docs/md/guide` → save to `.ledda/<hash>/guide.md`

3. Read the cached documentation files (`.ledda/<hash>/guide.md` and `.ledda/<hash>/reference.md`) to understand available API endpoints.

4. Help the user with their request using the Ledda API:
   - Use the appropriate account's API key as a Bearer token: `Authorization: Bearer <api_key>`
   - If the user doesn't specify an account and there's only one, use it
   - If there are multiple accounts, ask which one to use (or let them specify by name)
   - Follow the guide for common workflows (searching, filtering, comparing traces)

## Authentication

All Ledda API calls (except `/docs/*`) require a Bearer token:

```
Authorization: Bearer ldda_ak_your_key_here
```

Each API key is scoped to a single account. Use the key matching the account the user wants to query.

## Credentials File Format

The `.ledda/.credentials` file uses ini format. See `references/credentials-format.md` for details.
