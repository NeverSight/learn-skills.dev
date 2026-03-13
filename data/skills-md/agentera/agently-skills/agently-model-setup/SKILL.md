---
name: agently-model-setup
description: Use when the request is already narrowed to wiring a model endpoint, env vars, settings-file-based model config, or connectivity check for a model-powered feature, including local Ollama, dotenv-loaded DeepSeek or other OpenAI-compatible settings, auth, request options, and minimal verification.
---

# Agently Model Setup

Use this skill for provider wiring and transport setup before request logic is discussed.

## Native-First Rules

- use `Agently.set_settings(...)` or `agent.set_settings(...)`
- prefer dotenv-loaded environment variables for base URL, model, and auth
- keep provider setup outside business workflow logic and prompt files

## Anti-Patterns

- do not hardcode provider-specific parsing into request code
- do not mix model setup with output parsing or workflow design

## Read Next

- `references/overview.md`
