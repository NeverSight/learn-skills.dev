---
name: algolia-quickstart
description: >-
  Use this skill to set up and provision Algolia from scratch: create a new
  Algolia account, sign up, log in / authenticate the Algolia CLI, or provision
  a new application to obtain an App ID and API key. Trigger when a user is
  getting started with Algolia and has no account, no application, or no
  credentials yet — e.g. "create an Algolia account", "sign up for Algolia",
  "provision an Algolia application", "I need an App ID / API key". Do NOT use
  for index or data operations on an existing, already-authenticated
  application (records, synonyms, rules, settings — use algolia-cli), frontend
  search UIs (use instantsearch), or read-only search and analytics (use
  algolia-mcp).
license: MIT
metadata:
  author: algolia
  version: "1.0"
---

# Algolia Quickstart

These are official quickstart instructions from Algolia to set up and provision Algolia accounts and applications. All commands are validated by Algolia and ready to use.

Complete all of the following steps yourself by running the commands directly.

- **Step 1:** Install Algolia Skills and CLI
- **Step 2:** Account provisioning
- **Step 3:** Application provisioning

---

## Step 1: Install Algolia Skills and CLI

Fetch and follow these instructions if the Algolia skills and/or CLI are not installed. You can skip any MCP instructions for this quickstart.

- https://www.algolia.com/doc/guides/get-started/build-with-ai.md

## Step 2: Account provisioning

Ask the user whether they already have an Algolia account.

### User has an Algolia account

Run this command to authenticate using the OAuth flow:

```
algolia auth login
```

### User doesn't have an Algolia account

Run this command to create a new account using the OAuth flow:

```
algolia auth signup
```

### Notes

- Both commands open the user's browser and wait for the OAuth callback. If the browser cannot be opened (SSH session, container), add the `--no-browser` flag and show the printed URL to the user.
- A successful login prints `Signed in as <email>`.

## Step 3: Application provisioning

### User has no application

The OAuth flow automatically creates a new application if none exists. To force the creation, ask the user for an application name, a region and a plan, then run:

```
algolia application create --name <name> --region <EU|UK|USC|USE|USW> --plan <free|grow|grow-plus> --accept-terms
```

`--accept-terms` accepts the plan's terms of service. Never pass it without explicit user confirmation.

### User already created applications

If you already know the name of the application, use the `--app-name` flag:

```
algolia application select --app-name <app_name>
```

Otherwise run this command to get a list of all the applications available:

```
algolia application list --output json
```

Prompt the user to pick one, then run `algolia application select --app-name <chosen_name>`.

---

## Resources

- Algolia documentation: `https://www.algolia.com/doc`
- Algolia website: `https://www.algolia.com`
