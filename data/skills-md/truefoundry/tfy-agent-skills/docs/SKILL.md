---
name: docs
description: Fetches TrueFoundry documentation, API reference, and deployment guides. Use when the user needs platform docs or how-to guidance.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(curl *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# TrueFoundry Documentation

Fetch up-to-date TrueFoundry documentation for features, API reference, and deployment guides.

## When to Use

Fetch up-to-date TrueFoundry documentation for features, API reference, deployment guides, or troubleshooting.

</objective>

<instructions>

## Documentation Sources

### API Reference

Full API docs:
```
https://truefoundry.com/docs/api-reference
```

Fetch a specific section:
```bash
curl -s https://truefoundry.com/docs/api-reference/applications/list-applications
```

### Deployment Guides

| Topic | URL |
|-------|-----|
| Introduction to Services | `https://truefoundry.com/docs/introduction-to-a-service` |
| Deploy First Service | `https://truefoundry.com/docs/deploy-first-service` |
| Dockerize Code | `https://truefoundry.com/docs/dockerize-code` |
| Ports and Domains | `https://truefoundry.com/docs/define-ports-and-domains` |
| Endpoint Auth | `https://truefoundry.com/docs/endpoint-authentication` |
| Resources (CPU/Memory) | `https://truefoundry.com/docs/resources-cpu-memory-storage` |
| Fractional GPUs | `https://truefoundry.com/docs/using-fractional-gpus` |
| Environment Variables | `https://truefoundry.com/docs/environment-variables-and-secrets` |
| Autoscaling | `https://truefoundry.com/docs/autoscaling-overview` |
| Liveness/Readiness Probes | `https://truefoundry.com/docs/liveness-readiness-probe` |
| Rollout Strategy | `https://truefoundry.com/docs/rollout-strategy` |
| Deploy Programmatically | `https://truefoundry.com/docs/deploy-service-programatically` |
| CI/CD Setup | `https://truefoundry.com/docs/setting-up-cicd-for-your-service` |
| Monitoring | `https://truefoundry.com/docs/monitor-your-service` |

### Job Deployment

| Topic | URL |
|-------|-----|
| Introduction to Jobs | `https://truefoundry.com/docs/introduction-to-a-job` |
| Deploy First Job | `https://truefoundry.com/docs/deploy-first-job` |

### ML & LLM

| Topic | URL |
|-------|-----|
| ML Repos | `https://truefoundry.com/docs/ml-repos` |
| LLM Deployment | `https://truefoundry.com/docs/llm-deployment` |
| LLM Tracing | `https://truefoundry.com/docs/llm-tracing` |

### Authentication

| Topic | URL |
|-------|-----|
| Generating API Keys | `https://docs.truefoundry.com/docs/generating-truefoundry-api-keys` |

## Fetching Docs

To fetch a specific docs page for the user:

```bash
curl -sL "https://truefoundry.com/docs/deploy-first-service" | head -200
```

Or use WebFetch if available in the agent.

</instructions>

<success_criteria>

## Success Criteria

- The user has received the relevant documentation content or URL for their question
- The agent has fetched and summarized the specific docs page rather than just linking to it
- The user understands the next steps based on the documentation provided
- If the docs page was unavailable, the agent has suggested alternative resources or related skills

</success_criteria>

<references>

## Composability

- **Before deploy**: Fetch deploy guides for the specific app type
- **For API usage**: Reference `references/api-endpoints.md` in _shared
- **For troubleshooting**: Fetch relevant docs page and summarize

</references>
