---
name: work-queue-processor
description: Autonomous work loop that processes validated queue items with fresh sub-agent contexts
version: 1.0.0
---

# Work Queue Processor Skill

## When to Use

- User wants to start autonomous work processing
- Queue has validated items ready for execution
- Running in dedicated "Work Claude" instance (not Capture instance)
- User says: "process the queue", "start working on ideas", "execute queue items"

## Purpose

This skill implements **Matt Maher's autonomous work loop pattern** where a persistent orchestrator processes queue items one-by-one, spawning fresh sub-agent contexts for each item to avoid context pollution.

**Key Principles**:
1. **Autonomous**: Runs until queue empty or tokens exhausted
2. **Fresh Contexts**: Each item gets new sub-agent (no pollution)
3. **Fault Tolerant**: Handles errors gracefully, continues processing
4. **Observable**: Updates Linear and queue status in real-time

## Architecture

```
┌─────────────────────────────────────────┐
│  Work Queue Processor (Orchestrator)     │
│  - Persistent context                    │
│  - Monitors queue continuously           │
│  - Spawns sub-agents per item            │
└──────────────┬──────────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ Validated Queue Item │
    └──────────┬───────────┘
               │
               ├─ Simple? ────► Execute directly
               │
               ├─ Medium? ────► PLANNER sub-agent ───► EXECUTOR sub-agent
               │
               └─ Complex? ───► PLANNER sub-agent ───► Ask user ───► EXECUTOR sub-agent
```

## Process

### Orchestrator Loop

```pseudocode
INITIALIZE orchestrator (persistent context)

LOOP while (queue has items) AND (tokens available):
  1. Fetch next validated item (status = 'validated')
  2. If no items: sleep 5 seconds, retry
  3. If item found:
     a. Mark as 'processing'
     b. Create Linear issue if not exists
     c. Route based on complexity:
        - Simple: Execute directly
        - Medium: PLANNER → EXECUTOR
        - Complex: PLANNER → USER APPROVAL → EXECUTOR
     d. Update Linear status
     e. Mark as 'complete' or 'failed'
     f. Archive if complete
  4. Sleep 2 seconds (rate limit protection)
  5. Continue to next item

END LOOP

REPORT summary (items processed, successes, failures)
```

### Execution Routing Logic

#### Simple Complexity (Execute Directly)

```typescript
// No planning needed, execute immediately
if (item.complexity === 'simple') {
  const result = await executeSimpleTask(item);
  await markAsComplete(item.id, result);
}
```

**Examples:**
- Fix typo
- Update CSS padding
- Change button color
- Add console.log for debugging

#### Medium Complexity (Planner → Executor)

```typescript
// Spawn planner sub-agent
const plan = await spawnPlannerSubAgent(item);

// Present plan to user for approval (if needed)
if (requiresApproval(plan)) {
  const approved = await askUserForApproval(plan);
  if (!approved) {
    await markAsFailed(item.id, 'User rejected plan');
    continue;
  }
}

// Spawn executor sub-agent with plan
const result = await spawnExecutorSubAgent(item, plan);
await markAsComplete(item.id, result);
```

**Examples:**
- Add form validation
- Create new component
- Update database query
- Refactor function

#### Complex Complexity (Planner → Approval → Executor)

```typescript
// Always requires user approval for complex items
const plan = await spawnPlannerSubAgent(item);

// Present detailed plan with risks/considerations
const approved = await askUserForApproval(plan, {
  showRisks: true,
  showEstimate: true,
  requireExplicitConfirmation: true,
});

if (!approved) {
  await markAsFailed(item.id, 'User rejected complex plan');
  continue;
}

// Spawn executor with careful progress tracking
const result = await spawnExecutorSubAgent(item, plan, {
  progressUpdates: true,
  checkpoints: true,
});

await markAsComplete(item.id, result);
```

**Examples:**
- New agent creation
- Database migration
- Multi-file refactoring
- R&D tax analysis (complex calculation)

### Sub-Agent Pattern (Fresh Context)

**Matt Maher's Key Insight**: Each queue item gets a **fresh sub-agent context** to avoid pollution:

```
Orchestrator (persistent)
  ├─ Item 1 → PLANNER (fresh) → EXECUTOR (fresh) → Complete
  ├─ Item 2 → PLANNER (fresh) → EXECUTOR (fresh) → Complete
  └─ Item 3 → PLANNER (fresh) → EXECUTOR (fresh) → Complete
```

**Why this matters:**
- ✅ No context pollution (previous item doesn't affect next)
- ✅ Consistent execution quality
- ✅ Clean error isolation
- ✅ Predictable token usage

**Implementation (Claude Code Task tool)**:

```typescript
// Spawn PLANNER sub-agent
const plannerResult = await spawnSubAgent({
  type: 'Plan',
  prompt: `Plan implementation for: ${item.title}\n\nDescription: ${item.description}`,
  context: {
    queueItemId: item.id,
    complexity: item.complexity,
    assignedAgent: item.assigned_agent,
  },
});

// Spawn EXECUTOR sub-agent
const executorResult = await spawnSubAgent({
  type: 'general-purpose',
  prompt: `Execute the following plan:\n\n${plannerResult.plan}\n\nOriginal request: ${item.description}`,
  context: {
    queueItemId: item.id,
    plan: plannerResult.plan,
  },
});
```

## Linear Integration

### Issue Creation

When processing starts, ensure Linear issue exists:

```typescript
import { createIssue, updateIssue } from '@/lib/linear/api-client';
import { buildIssueFromQueue, mapQueueStatusToLinearState } from '@/lib/linear/graphql-queries';
import { updateLinearMetadata } from '@/lib/queue/work-queue-manager';

// Check if Linear issue already created by PM
if (!item.linear_issue_id) {
  // Create issue
  const issue = await createIssue(buildIssueFromQueue(
    serverConfig.linear.teamId,
    serverConfig.linear.projectId,
    {
      queueId: item.id,
      title: item.title,
      description: item.description,
      priority: item.priority || 'P2',
      complexity: item.complexity || 'medium',
      queueItemType: item.queue_item_type,
      assignedAgent: item.assigned_agent,
    }
  ));

  // Update queue with Linear metadata
  await updateLinearMetadata(item.id, {
    issue_id: issue.id,
    issue_identifier: issue.identifier,
    issue_url: issue.url,
  });
}
```

### Status Updates

Update Linear as queue item progresses:

```typescript
// When starting processing
await updateIssue(item.linear_issue_id, {
  stateId: await getStateIdByType('started'),
});

// When complete
await updateIssue(item.linear_issue_id, {
  stateId: await getStateIdByType('completed'),
});

// When failed
await updateIssue(item.linear_issue_id, {
  stateId: await getStateIdByType('canceled'),
});
await addComment(item.linear_issue_id, `Execution failed: ${errorMessage}`);
```

## Archive & Metadata

### Screenshots

Capture before/after screenshots:

```typescript
// Before execution
const screenshotBefore = await captureScreenshot();

// After execution
const screenshotAfter = await captureScreenshot();

// Store paths
const screenshots = [
  `.queue/screenshots/${item.id}/before.png`,
  `.queue/screenshots/${item.id}/after.png`,
];

await markAsComplete(item.id, {
  screenshots,
  execution_log: executionLog,
  token_usage: estimatedTokens,
  execution_time_seconds: Math.floor((Date.now() - startTime) / 1000),
});
```

### Execution Log

Detailed log of all actions taken:

```typescript
const executionLog = [
  `[${timestamp}] Started processing queue item ${item.id}`,
  `[${timestamp}] Complexity: ${item.complexity}`,
  `[${timestamp}] Assigned agent: ${item.assigned_agent}`,
  `[${timestamp}] Spawned PLANNER sub-agent`,
  `[${timestamp}] Plan approved by user`,
  `[${timestamp}] Spawned EXECUTOR sub-agent`,
  `[${timestamp}] Execution complete`,
  `[${timestamp}] Updated Linear issue ${item.linear_issue_identifier}`,
].join('\n');
```

### Archival

After successful completion:

```typescript
import { archiveQueueItem } from '@/lib/queue/work-queue-manager';

// Archive completed item
await archiveQueueItem(item.id);

// Item moved to 'archived' status with timestamp
// Remains in database for audit trail
```

## Configuration

### Environment Variables

```bash
# Required
LINEAR_API_KEY=lin_api_...
LINEAR_TEAM_ID=UNI
LINEAR_PROJECT_ID=project-id-optional

# Queue processing
QUEUE_BATCH_SIZE=10              # Max items per session
QUEUE_POLL_INTERVAL_MS=5000      # How often to check for new items
QUEUE_MAX_RETRIES=3              # Max retries on failure
QUEUE_TIMEOUT_HOURS=2            # Mark as failed after N hours
```

### Rate Limiting

**Linear API**: 4-second delay between calls (follows Gemini pattern)

```typescript
async function withLinearRateLimit<T>(fn: () => Promise<T>): Promise<T> {
  const result = await fn();
  await sleep(4000); // 4 second delay
  return result;
}
```

**Token Budget**: Stop if < 10,000 PTS remaining

```typescript
if (estimatedRemainingTokens < 10000) {
  console.warn('Low token budget, stopping work loop');
  break;
}
```

## Workflow Commands

### `/process-queue`
Process all validated items once.

**Usage**:
```
/process-queue
```

**Output**:
```
⚙️ Work Queue Processor Started

Processing validated items...

✅ Completed: Fix copy icon overlap (UNI-42)
   - Complexity: simple
   - Execution time: 3 minutes
   - Files changed: 1
   - Linear: https://linear.app/unite-hub/issue/UNI-42

⚙️ Processing: Add R&D analysis (UNI-43)
   - Spawned PLANNER sub-agent...
   - Plan approved
   - Spawned EXECUTOR sub-agent...
   - Routing to rnd-tax-specialist...

✅ Completed: Add R&D analysis (UNI-43)
   - Complexity: complex
   - Execution time: 12 minutes
   - Analysis: 45 transactions reviewed
   - Potential refund: $127,500
   - Linear: https://linear.app/unite-hub/issue/UNI-43

📊 Session Complete
- Processed: 2 items
- Succeeded: 2 items
- Failed: 0 items
- Total time: 15 minutes
- Tokens used: ~15,000 PTS
```

### `/process-queue --continuous`
Run until queue empty.

**Usage**:
```
/process-queue --continuous
```

Processes items non-stop until:
- Queue is empty
- Token budget exhausted
- User stops manually
- Error threshold exceeded (3 consecutive failures)

### `/process-queue --limit 5`
Process maximum 5 items.

**Usage**:
```
/process-queue --limit 5
```

### `/pause-queue`
Stop processing after current item.

**Usage**:
```
/pause-queue
```

Sets flag to stop loop gracefully.

### `/queue-status`
Show current processing status.

**Usage**:
```
/queue-status
```

**Output**:
```
📊 Queue Status

Currently processing:
- Item: Fix navigation spacing (UNI-44)
- Progress: 45% (EXECUTOR phase)
- Time elapsed: 4 minutes

Queue ahead:
- 3 validated items waiting
- Estimated time: ~20 minutes

Recently completed:
- Fix copy icon overlap (UNI-42) - 3 mins ago ✅
- Add R&D analysis (UNI-43) - 15 mins ago ✅

Session stats:
- Items processed: 2
- Success rate: 100%
- Avg execution time: 7.5 minutes
```

## Error Handling

### Execution Failures

```typescript
try {
  const result = await executeQueueItem(item);
  await markAsComplete(item.id, result);
} catch (error) {
  console.error(`Execution failed for item ${item.id}:`, error);

  // Mark as failed with error message
  await markAsFailed(item.id, error.message);

  // Update Linear
  await updateIssue(item.linear_issue_id, {
    stateId: await getStateIdByType('canceled'),
  });
  await addComment(
    item.linear_issue_id,
    `Execution failed: ${error.message}\n\nThe item has been marked as failed in the queue.`
  );

  // Continue to next item (don't stop entire loop)
  continue;
}
```

### Linear API Failures

Graceful degradation:

```typescript
try {
  await updateIssue(item.linear_issue_id, updates);
} catch (error) {
  console.warn('Linear update failed, continuing anyway:', error);
  // Don't fail entire execution just because Linear failed
}
```

### Stuck Item Timeout

Safety mechanism (runs periodically):

```typescript
import { timeoutStuckItems } from '@/lib/queue/work-queue-manager';

// Mark items stuck in 'processing' for > 2 hours as failed
const timedOut = await timeoutStuckItems(2);
console.log(`Timed out ${timedOut} stuck items`);
```

### Token Exhaustion

```typescript
if (estimatedRemainingTokens < MIN_TOKEN_THRESHOLD) {
  console.warn('Token budget low, stopping gracefully');

  // Save state
  await saveProcessorState({
    lastProcessedId: item.id,
    itemsProcessed: count,
    timestamp: new Date().toISOString(),
  });

  // Notify user
  return {
    status: 'paused',
    reason: 'token_budget_low',
    itemsProcessed: count,
    message: 'Work loop paused due to low token budget. Restart to continue.',
  };
}
```

## Performance Targets

| Metric | Target |
|--------|--------|
| Simple item execution | < 5 minutes |
| Medium item execution | < 15 minutes |
| Complex item execution | < 30 minutes |
| Queue throughput | 10-25 items per 90 minutes |
| Success rate | > 95% |
| Token usage per item | 50-500 PTS |

## Security Considerations

- ✅ Uses service role for queue operations
- ✅ Sub-agents run in sandboxed contexts
- ✅ No modification of user files without validation
- ✅ All execution logged for audit trail
- ✅ Linear API key secured in environment

**Prohibited Actions** (never executed, even if in queue):
- Deleting production data
- Modifying Xero data (read-only)
- Submitting ATO filings
- Committing secrets to git
- Force-pushing to main branch

## Testing Checklist

- [ ] Can fetch validated queue items
- [ ] Processes items sequentially
- [ ] Creates Linear issues if missing
- [ ] Updates Linear status correctly
- [ ] Spawns sub-agents with fresh contexts
- [ ] Executes simple items directly
- [ ] Plans medium items before execution
- [ ] Requires approval for complex items
- [ ] Captures screenshots before/after
- [ ] Logs execution details
- [ ] Marks items as complete
- [ ] Archives completed items
- [ ] Handles errors gracefully
- [ ] Continues on failure (doesn't stop loop)
- [ ] Respects token budget
- [ ] Stops when queue empty

## Example Processing Sessions

### Session 1: Simple Bug Fix

```
/process-queue

⚙️ Processing: Fix copy icon overlap (UNI-42)
- Complexity: simple
- Executing directly (no planning needed)...

📝 Changes made:
- Updated: app/components/DescriptionPanel.tsx
- Fixed: z-index issue causing overlap
- Added: proper spacing for icon

✅ Complete! (3 minutes)
📦 Archived queue item
🔗 Linear: https://linear.app/unite-hub/issue/UNI-42
```

### Session 2: Medium Feature (with Planning)

```
/process-queue

⚙️ Processing: Add dark mode toggle (UNI-43)
- Complexity: medium
- Spawning PLANNER sub-agent...

📋 Plan created:
1. Add theme context provider
2. Create toggle component
3. Update existing components for theme support
4. Test in both modes

✓ Plan looks good, spawning EXECUTOR...

⚙️ Executing plan...
- Created: lib/theme/ThemeContext.tsx
- Created: components/ThemeToggle.tsx
- Updated: 8 components for theme support
- Tested: Light and dark modes

✅ Complete! (12 minutes)
📦 Archived queue item
🔗 Linear: https://linear.app/unite-hub/issue/UNI-43
```

### Session 3: Complex Analysis (with Approval)

```
/process-queue

⚙️ Processing: Analyze R&D transactions FY2023-24 (UNI-44)
- Complexity: complex
- Assigned agent: rnd-tax-specialist
- Spawning PLANNER sub-agent...

📋 Plan created:
1. Fetch all Xero transactions for FY2023-24
2. Apply Division 355 four-element test
3. Calculate eligible expenditure
4. Estimate tax offset (43.5%)
5. Generate compliance report

⚠️ This is a complex analysis. Proceed? [Yes/No]

User: Yes

✓ Approved, spawning EXECUTOR (rnd-tax-specialist)...

⚙️ Analyzing transactions...
- Fetched: 1,247 transactions
- Analyzed: 387 potential R&D activities
- Eligible: 127 transactions ($293,000)
- Tax offset: $127,455 (43.5%)

📊 Generated report with:
- Detailed transaction breakdown
- Legislative compliance notes
- Recommendations for registration

✅ Complete! (18 minutes)
📦 Archived queue item
🔗 Linear: https://linear.app/unite-hub/issue/UNI-44
```

## Integration Points

### Upstream
- **work_queue table**: Reads items with status = 'validated'
- **Senior PM agent**: Items flow from validation

### Downstream
- **Linear**: Updates issue status, adds comments
- **work_queue table**: Marks complete/failed, archives
- **Domain agents**: Routes to specialists (rnd, xero, etc.)

### Parallel
- **Capture skill**: Can capture new ideas while work loop runs
- **Senior PM**: Can validate new items while work loop executes

## Notes

- Designed to run in dedicated "Work Claude" instance
- Complements "Capture Claude" instance for two-Claude pattern
- Follows Matt Maher's proven pattern (25+ changes in 90 minutes)
- Each item gets fresh sub-agent context (no pollution)
- Autonomous until queue empty or tokens exhausted
- Observable via Linear for team visibility
- Fault-tolerant: Continues on individual item failures
- Archives maintain full audit trail
