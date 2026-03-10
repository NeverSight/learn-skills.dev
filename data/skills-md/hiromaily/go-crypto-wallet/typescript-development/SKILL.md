---
name: typescript-development
description: TypeScript/JavaScript development workflow for apps/ directory. Use when modifying TypeScript code in xrpl-grpc-server or JavaScript in eth-contracts.
---

# TypeScript/JavaScript Development Workflow

Workflow for TypeScript/JavaScript code changes in `apps/` directory.

## Prerequisites

- **Use `git-workflow` Skill** for branch management, commit conventions, and PR creation.
- **Refer to `.claude/rules/typescript.md`** for detailed verification commands (SSOT).

## Applicable Directories

| App              | Language   | Runtime | Path                     | Status                     |
| ---------------- | ---------- | ------- | ------------------------ | -------------------------- |
| xrpl-grpc-server | TypeScript | **Bun** | `apps/xrpl-grpc-server/` | **Deprecated (READ-ONLY)** |
| eth-contracts    | JavaScript | Node.js | `apps/eth-contracts/`      | Active                     |

## Workflow

### 1. Make Changes

Edit TypeScript/JavaScript files following the rules in `.claude/rules/typescript.md`.

### 2. Verify (from rules/typescript.md)

```bash
# xrpl-grpc-server (Bun)
cd apps/xrpl-grpc-server && bun run lint && bun run typecheck

# eth-contracts (Node.js/npm)
cd apps/eth-contracts && npm run lint-js && npm run fmt
```

### 3. Self-Review Checklist

- [ ] No TypeScript errors
- [ ] No `any` types (unless documented reason)
- [ ] Async errors properly handled
- [ ] Auto-generated files not edited

## Command Summary

| App              | Lint              | Format           | Type Check          |
| ---------------- | ----------------- | ---------------- | ------------------- |
| xrpl-grpc-server | `bun run lint`    | `bun run format` | `bun run typecheck` |
| eth-contracts    | `npm run lint-js` | `npm run fmt`    | -                   |

## Related

- `.claude/rules/typescript.md` - TypeScript rules (SSOT)
- `git-workflow` - Branch, commit, PR workflow
- `solidity-development` - For Solidity contracts in eth-contracts
