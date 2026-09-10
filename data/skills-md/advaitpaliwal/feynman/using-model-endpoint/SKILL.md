---
name: using-model-endpoint
description: Call a configured Feynman model endpoint and interpret its response. Use when a task needs inference from a registered endpoint, remote model API, local model service, or custom connector-backed predictor.
---

# Using Model Endpoint

Use this skill after a model endpoint is already configured or explicitly chosen.

Workflow:

1. Confirm endpoint identity, auth status, input schema, output schema, model version, and rate/size limits.
2. Build a minimal request with explicit inputs and no hidden context.
3. Save request metadata, response, latency, status, and parsing code as artifacts without exposing secrets.
4. Validate response shape and handle model errors as evidence, not as missing work to hide.
5. Interpret predictions separately from source-backed facts.

When the endpoint is not configured, switch to `managed-model-endpoints` or `compute-env-setup` instead of pretending inference ran.
