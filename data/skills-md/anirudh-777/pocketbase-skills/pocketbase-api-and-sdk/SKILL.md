---
name: pocketbase-api-and-sdk
description: Use when you specifically need detailed PocketBase REST/SDK integration guidance for advanced query, pagination, and error handling patterns
---

# PocketBase API and SDK (Advanced)

## Overview
Use this only for deeper integration patterns. Default to `pocketbase-agent-orchestrator` for common operational tasks.

## Focus
- REST and SDK CRUD patterns
- Filtering, sorting, pagination, and relation expansion
- Error classification and retry boundaries

## Minimal Workflow
1. Choose execution context (client/server/worker).
2. Define request/response contract and query constraints.
3. Implement bounded reads and validated writes.
4. Verify auth + schema implications.

## References
- [rest-cheatsheet.md](references/rest-cheatsheet.md)
- [js-sdk-patterns.md](references/js-sdk-patterns.md)
- [filter-examples.md](references/filter-examples.md)
- [nextjs-app-router.md](references/nextjs-app-router.md)
- [node-express.md](references/node-express.md)
- [react-native-expo.md](references/react-native-expo.md)
