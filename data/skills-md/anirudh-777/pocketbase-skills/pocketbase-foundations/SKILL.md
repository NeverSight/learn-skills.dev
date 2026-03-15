---
name: pocketbase-foundations
description: Use when you specifically need PocketBase setup, environment bootstrap, and initial security baseline details beyond the orchestrator quick actions
---

# PocketBase Foundations (Advanced)

## Overview
Use this only for deep setup and rollout details. Default to `pocketbase-agent-orchestrator` for normal tasks.

## Focus
- Environment setup (local/staging/production)
- Admin bootstrap and secure secret handling
- Baseline network/security checks before feature work

## Minimal Workflow
1. Confirm runtime mode and persistence strategy.
2. Verify required env values (`PB_URL`, admin/service credentials).
3. Validate health endpoint and admin authentication.
4. Hand off to modeling/auth/api skills as needed.

## References
- [setup-checklist.md](references/setup-checklist.md)
- [env-template.md](references/env-template.md)
