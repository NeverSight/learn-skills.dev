---
name: coolify-manager
description: Manage self-hosted infrastructure via Coolify. Use this to deploy apps, debug build failures, manage databases, and interact with the Coolify API.
---

# Coolify Infrastructure Manager

This skill allows you to manage a self-hosted Coolify instance. It handles deployment lifecycles, resource configuration, and advanced debugging.

## 🧠 Decision Tree

**Step 1: Analyze the User Request.**
Determine which of the following categories the request falls into and follow the instructions.

### A. "Fix it" / "Debug it" (Operations)
*User asks: "Why did the build fail?", "Show me logs", "Restart the service"*
1. **Check Broad Health:** Run `coolify resources list` to see if dependencies (DBs, Redis) are healthy.
   - If multiple resources are `unhealthy` or `exited`, check the host server disk space.
2. **Check Status:** Run `coolify app get <uuid>` to see if it's running or exited.
3. **Get Logs:** 
   - If build failed: `coolify app deployments logs <app_uuid>`.
   - If runtime error: `coolify app logs <uuid>`.
4. **Action:** If stuck, `coolify app restart <uuid>`.

### B. "Change it" (Configuration)
*User asks: "Update environment variables", "Change the domain", "Add a database"*
1. **Consult Reference:** Read `resources/common-workflows.md` for specific command patterns.
2. **Environment Vars:** Remember that `coolify app env sync` is safer than adding one by one if the user provides a list.

### C. "Delete it" (Destructive Operations)
*User asks: "Delete the project", "Remove this database"*
1. **Check CLI Support:** Some delete operations (like `coolify project delete`) are not supported by the CLI.
2. **Use Raw API:** Consult `resources/api-reference.md` for the curl command.
3. **Get Credentials:** Run `coolify context get <context_name> --show-sensitive` to get the base URL and token.
4. **Execute:** Make the API call with curl.

## ⚡ Best Practices

1. **Safety First:**
   - Never use `--force` on `delete` commands unless the user explicitly requested it.
   - Always verify the context (`coolify context verify`) before running destructive commands to ensure you aren't in `prod` when you think you are in `staging`.

2. **Resource Discovery:**
   - If you don't know the UUID, search by listing resources: `coolify resources list`.
   - Always prefer UUIDs over names for critical operations to avoid ambiguity.

3. **Handling CLI Gaps (Raw API):**
   - If the CLI lacks a feature, consult `resources/api-reference.md` for the raw API endpoint.
   - Get context credentials with: `coolify context get <name> --show-sensitive`
   - Use curl to call the API directly.

## 📚 Resources

| File | Purpose |
|------|---------|
| `resources/cli-reference.md` | Complete CLI command reference |
| `resources/api-reference.md` | Raw API endpoints for operations the CLI doesn't support |
| `resources/common-workflows.md` | Recipes for common tasks (env sync, domain changes, etc.) |
| `guides/container_ssh.md` | How to SSH into containers manually |

## ⚠️ Known CLI Limitations

The Coolify CLI (as of v1.4.0) does not support every API operation:

| Operation | CLI Support | Alternative |
|-----------|-------------|-------------|
| Delete project | ❌ No | Use raw API: `DELETE /api/v1/projects/{uuid}` |
| Execute command in container | ❌ No | SSH to host + `docker exec` |
| Force delete database | ❌ No | Use raw API or Web UI |

When using the raw API, always get credentials from the context:
```bash
coolify context get <context_name> --show-sensitive
```
  