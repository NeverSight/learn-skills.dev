---
name: cheap-model-testing
description: When working on any application that integrates with LLMs or pay-per-usage APIs, always use the cheapest available model during development and testing. Remind to upgrade to a production model before deployment.
---

# Cheap Model for Testing / Expensive Model for Production

## Core Rule

When writing, editing, or reviewing code that calls an LLM or any pay-per-usage API (OpenAI, Anthropic, Google AI, Cohere, Mistral, Replicate, AWS Bedrock, Azure OpenAI, etc.), **always default to the cheapest available model** for development and testing purposes.

## What To Do

### During development and testing

- **Always choose the cheapest model** available for the provider being used.
- Common cheap model choices (use the latest available version):
  - **OpenAI**: `gpt-4o-mini` (or `gpt-3.5-turbo` if mini is unavailable)
  - **Anthropic**: `claude-haiku-4-5-20251001` (or the latest Haiku variant)
  - **Google AI / Vertex**: `gemini-2.0-flash` (or the latest Flash variant)
  - **Mistral**: `mistral-small-latest`
  - **Cohere**: `command-r` (not command-r-plus)
  - **AWS Bedrock / Azure OpenAI**: whichever is the cheapest equivalent of the above
- If the user has already specified a model and it is NOT the cheapest, **proactively suggest switching** to the cheapest one for testing and explain why (cost savings during development).
- If a config file, environment variable, or constant defines the model, set it to the cheap option and leave a code comment like:
  ```
  # TODO: Switch to production model before deploying (e.g., claude-sonnet-4-5-20250514)
  ```

### When deploying or finalizing for production

- **Before changing any model to a more expensive/capable one**, always ask the user:
  > "This code is using [cheap model] for testing. Are you ready to switch to a production-grade model for deployment? If so, which model would you prefer?"
- **Never silently upgrade** to an expensive model. Always get explicit confirmation.
- Suggest sensible production model options for the provider in use (e.g., `claude-sonnet-4-5-20250514`, `gpt-4o`, `gemini-2.0-pro`).

## How To Detect Deployment Context

Consider the task to be "deployment" or "production-ready" when the user says things like:
- "deploy", "ship it", "push to production", "release", "go live"
- "finalize", "production-ready", "ready for launch"
- "switch to the real model", "use the good model now"
- Creating a PR described as production/release-ready

In any of these cases, **stop and ask before changing the model**.

## Summary

| Phase        | Model Choice        | Action                                      |
|-------------|--------------------|--------------------------------------------|
| Development  | Cheapest available  | Set automatically, add TODO comment         |
| Testing      | Cheapest available  | Keep cheap model, remind user in output     |
| Deployment   | User's choice       | **Ask user before switching**, suggest options |
