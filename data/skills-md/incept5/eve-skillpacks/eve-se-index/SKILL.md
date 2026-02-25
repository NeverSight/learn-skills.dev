---
name: eve-se-index
description: Load this first. Routes to the right Eve SE skill for developing, deploying, and debugging Eve-compatible apps.
triggers:
  - eve se
  - eve skills
  - eve help
  - how do i deploy with eve
  - eve getting started
---

# Eve SE Index (Load First)

Use this skill as the entry point for Eve SE. It routes to the correct skill for the task.

## Scope

Eve SE is for app developers using Eve to deploy and run their apps. It does not cover operating the Eve platform itself.

## Quick Routing

| Need | Load this skill |
| --- | --- |
| **Full onboarding (new or existing user)** | **`eve-bootstrap`** |
| Understand Eve CLI primitives | `eve-cli-primitives` |
| Set up a new project from the starter | `eve-new-project-setup` |
| Connect an existing repo to Eve (already authed) | `eve-project-bootstrap` |
| Implement a plan via Eve jobs | `eve-plan-implementation` |
| Edit the manifest | `eve-manifest-authoring` |
| Configure auth + secrets | `eve-auth-and-secrets` |
| Local docker-compose dev loop | `eve-local-dev-loop` |
| Deploy to staging + debug | `eve-deploy-debugging` |
| Pipelines + workflows | `eve-pipelines-workflows` |
| Troubleshoot failures | `eve-troubleshooting` |
| Keep repo aligned with platform | `eve-repo-upkeep` |
| Web UI testing with agent-browser | `eve-web-ui-testing-agent-browser` |
| Design an agent-native app | `eve-agent-native-design` (eve-design pack) |

## Default Workflow (Local -> Staging)

1. Run locally with Docker Compose: `eve-local-dev-loop`.
2. Ensure manifest matches runtime: `eve-manifest-authoring`.
3. Set secrets and auth: `eve-auth-and-secrets`.
4. Deploy to staging and debug: `eve-deploy-debugging`.

## What This Pack Does NOT Cover

- Running Eve Horizon itself (k8s, docker, infra)
- Platform operator workflows (`./bin/eh`, cluster secrets)

If you need platform operations, load the private `eve-dev` pack instead.
