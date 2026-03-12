---
name: argocd-cli-guide
description: Use when managing, inspecting, syncing, or troubleshooting Kubernetes applications via the argocd CLI, including checking app health, running diffs, syncing deployments, viewing logs, or switching between ArgoCD server contexts
---

# ArgoCD CLI Guide

You are an expert Kubernetes operator. Use these command patterns when interacting with the `argocd` CLI.

## 0. Context Management (MUST READ FIRST)

**CRITICAL RULE:** When working with multiple ArgoCD servers, you MUST switch context before running any command. Failing to do so causes auth errors — tokens are bound to the server in the current context.

```bash
# List all configured contexts (shows current context with *)
argocd context

# Switch context before operating on a different server
argocd context <SERVER_ADDRESS>

# Or use per-command flags (no context switch needed)
argocd app get <APP> --argocd-context <SERVER_ADDRESS>
argocd app get <APP> --server <SERVER_ADDRESS>
```

**Multi-server pattern:**
```bash
argocd context argocd.example.com
argocd app sync argocd/my-app
argocd context argocd.other.com
argocd app sync argocd/other-app
```

**Login:**
```bash
argocd login <SERVER_ADDRESS> --grpc-web --sso
```

Per-server settings like `grpc-web` can be persisted in `~/.config/argocd/config` so you don't need to pass flags every time. See [references/argocd-config.md](references/argocd-config.md) for config details.

## 1. Information Retrieval

When asked to check an application's status, **always start here**.

```bash
# High-level status (health + sync)
argocd app get <APP_NAME>

# JSON output for scripting
argocd app get <APP_NAME> -o json

# Show parameters and last operation details
argocd app get <APP_NAME> --show-params --show-operation

# Get a specific resource's live manifest
argocd app get-resource <APP_NAME> --kind <KIND> --resource-name <NAME> -o json

# List all applications
argocd app list
```

**Application Logs:**
```bash
# All pods in the app
argocd app logs <APP_NAME>

# Stream logs in real-time
argocd app logs <APP_NAME> -f

# Last N lines
argocd app logs <APP_NAME> --tail 100

# Filter by resource kind/name/namespace
argocd app logs <APP_NAME> --kind Deployment --name <RESOURCE_NAME>
```

## 2. Safe Inspection (Diffing)

**CRITICAL GUARDRAIL:** ALWAYS run a diff before performing a manual sync to understand what will change.

```bash
argocd app diff <APP_NAME>
```

If the diff shows unexpected massive deletions, STOP and ask the user for confirmation.

**Reading diffs:** If the diff only shows image tag changes, this is typically from CI/CD auto-updates and is safe to sync.

## 3. Sync & Deployment

```bash
# Standard sync
argocd app sync <APP_NAME>

# Async sync (don't wait for completion — good for batch)
argocd app sync <APP_NAME> --async

# Dry-run (preview without applying)
argocd app sync <APP_NAME> --dry-run

# Sync specific resource only (GROUP:KIND:NAME format)
argocd app sync <APP_NAME> --resource :Service:my-service
argocd app sync <APP_NAME> --resource argoproj.io:Rollout:my-rollout
# With namespace
argocd app sync <APP_NAME> --resource argoproj.io:Rollout:my-namespace/my-rollout

# Force sync with prune (USE WITH CAUTION — only when user explicitly asks)
argocd app sync <APP_NAME> --prune --force
```

## 4. Rollback & History

```bash
# View deployment history
argocd app history <APP_NAME>

# Rollback to a specific revision
argocd app rollback <APP_NAME> <HISTORY_ID>
```

## 5. Resource Actions (Rollouts, Restarts)

```bash
# List available actions for an app
argocd app actions list <APP_NAME>

# Promote a Rollout (e.g., canary → full)
argocd app actions run <APP_NAME> promote-full --kind Rollout --resource-name <NAME>

# Restart a Deployment
argocd app actions run <APP_NAME> restart --kind Deployment --resource-name <NAME>
```

**Argo Rollouts workflow:** When an app uses Argo Rollouts, `sync` triggers a canary deployment (partial traffic). You MUST run `promote-full` after sync to complete the full rollout. Typical flow:
1. `argocd app diff <APP>` — check what changed
2. `argocd app sync <APP>` — triggers canary
3. Verify canary is healthy
4. `argocd app actions run <APP> promote-full --kind Rollout --resource-name <NAME>` — full rollout

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Unauthenticated` / `token expired` | Auth token expired | `argocd relogin` or `argocd login <SERVER> --grpc-web --sso` |
| Perpetual diff on HPA | Metrics field ordering | Ensure HPA metrics order: memory first, cpu second (matches K8s API server return order) |
| Diff shows only image tag changes | CI/CD auto-updated image | Expected behavior, safe to sync |

## Best Practices

1. **Context First:** MUST `argocd context <server>` before operating on a different server.
2. **Read Before Write:** Always `app get` + `app diff` before any `app sync` or `app rollback`.
3. **GitOps Awareness:** ArgoCD reconciles from Git. Manual `kubectl` changes will be overwritten on next sync. Prefer Git commits + ArgoCD sync.
4. **Async for Batch:** Use `--async` when syncing multiple apps to avoid blocking.
5. **Targeted Sync:** Use `--resource` to sync only the changed resource instead of the entire app.
6. **Rollout Awareness:** After syncing an app with Argo Rollouts, remember to `promote-full` to complete the rollout.
