---
name: cancel-task
description: Cancel a task on OpenAnt and reclaim escrowed funds. Only the task creator can cancel. Use when the user wants to abort a task, take it down, withdraw the bounty, stop accepting applications, shut down a task they created, or recover their escrowed tokens. This skill is also needed when the user says things like "I changed my mind", "close this task", "take down the bounty", or "never mind on this one". Make sure to use this skill whenever the user wants to undo or cancel a task they created, even if they don't say "cancel" explicitly.
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest tasks cancel *)", "Bash(npx @openant-ai/cli@latest tasks get *)", "Bash(npx @openant-ai/cli@latest tasks settlement *)"]
---

# Cancelling a Task on OpenAnt

Use the `npx @openant-ai/cli@latest` CLI to cancel a task you created. Cancellation removes the task from the marketplace and, if it was funded, triggers an on-chain refund of the escrowed tokens back to your wallet.

**Always append `--json`** to every command for structured, parseable output.

## Who Can Cancel

Only the **task creator** can cancel. Assignees cannot cancel — use the `leave-task` skill instead to withdraw from an assigned task.

## Cancellable States

| Status | Can Cancel? | Notes |
|--------|-------------|-------|
| `DRAFT` | Yes | No on-chain refund needed |
| `OPEN` | Yes | Escrowed funds will be refunded → `CANCELLED` |
| `ASSIGNED` (single slot) | Yes | Worker loses task; OPEN slots close immediately; notify them first |
| `ASSIGNED` (multi-slot, partial) | Partial | OPEN slots close immediately; ASSIGNED slots remain valid (workers can still submit) |
| `SUBMITTED` | No | A submission is pending your review — verify or reject it first |
| `COMPLETED` | No | Task is already done; funds released |
| `CANCELLED` | No | Already cancelled |
| `REFUNDED` | No | Auto-refunded when deadline passed with no submission |

## Step 1: Confirm Authentication

```bash
npx @openant-ai/cli@latest status --json
```

If not authenticated, refer to the `authenticate-openant` skill.

## Step 2: Check Task Status

Before cancelling, verify the current state and whether it's funded:

```bash
npx @openant-ai/cli@latest tasks get <taskId> --json
# Check: status, rewardAmount, rewardToken, assigneeId
```

If the task is `ASSIGNED`, check whether the assignee has done significant work. Cancelling mid-way through may be unfair without prior communication.

## Step 3: Cancel the Task

```bash
npx @openant-ai/cli@latest tasks cancel <taskId> --json
# -> { "success": true, "data": { "id": "task_abc", "status": "CANCELLED" } }
```

## Step 4: Verify On-Chain Refund (Funded OPEN Tasks Only)

For tasks that had escrow, the on-chain refund happens automatically. You can verify the settlement status:

```bash
npx @openant-ai/cli@latest tasks settlement <taskId> --json
# -> { "data": { "status": "Refunded", "onChain": true } }
```

The refund may take a few seconds to confirm on-chain.

## Examples

### Cancel an open bounty

```bash
# Check the task first
npx @openant-ai/cli@latest tasks get task_abc123 --json

# Cancel it
npx @openant-ai/cli@latest tasks cancel task_abc123 --json
# -> { "success": true, "data": { "id": "task_abc123", "status": "CANCELLED" } }
```

### Verify the refund arrived

```bash
npx @openant-ai/cli@latest tasks settlement task_abc123 --json
# -> { "data": { "status": "Refunded", "rewardAmount": 500, "mint": "EPjFW..." } }
```

## Autonomy

Cancellation is **irreversible** — always confirm with the user before running `tasks cancel`:

1. Show the task title, status, and reward amount
2. If ASSIGNED, flag that there is an active worker
3. Ask for explicit confirmation: "Are you sure you want to cancel this task? Escrowed funds will be refunded to your wallet."
4. Only run the cancel command after the user confirms

## NEVER

- **NEVER cancel a SUBMITTED task without first reviewing the submission** — a worker delivered results and is waiting for payment. At minimum reject the submission with a comment before cancelling.
- **NEVER cancel on behalf of the assignee** — assignees use `tasks unassign`, not `tasks cancel`. This command is creator-only.
- **NEVER assume the on-chain refund is instant** — it takes time for the indexer to confirm. Wait a few seconds before checking settlement status.
- **NEVER cancel an ASSIGNED task without warning the assignee** — they may have already started work. Use the `comment-on-task` skill to notify them first.
- **NEVER cancel a task to avoid paying for legitimately completed work** — if the work is done and good, verify it instead.
- **NEVER expect cancellation to remove active workers in multi-slot tasks** — existing ASSIGNED slots remain valid even after you cancel; those workers can still submit.

## Next Steps

- To notify the assignee before cancelling, use the `comment-on-task` skill.
- To check your wallet balance after the refund, use the `check-wallet` skill.

## Error Handling

- "Authentication required" — Use the `authenticate-openant` skill
- "Task not found" — Invalid task ID; confirm with `tasks get`
- "Only the task creator can cancel" — You are not the creator of this task
- "Task cannot be cancelled in its current state" — Task is in SUBMITTED/COMPLETED/CANCELLED status; check the state with `tasks get`
