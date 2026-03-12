---
name: pg-boss
description: Implement reliable PostgreSQL-based job queues with PG Boss. Use when implementing background jobs, scheduled tasks, cron-like functionality, task rollover, or email notifications in Node.js/TypeScript projects.
---

# PG Boss Job Queue

PG Boss is a PostgreSQL-based job queue for Node.js. It stores jobs in the database, providing persistence and reliability.

## Quick Setup

```typescript
import { PgBoss } from 'pg-boss';

const boss = new PgBoss({
  connectionString: process.env.DATABASE_URL,
  schema: 'pgboss',
  monitorIntervalSeconds: 30,
});

await boss.start();
```

## Common Patterns

### 1. Scheduled Jobs (Cron-like)

```typescript
// v12: queue must exist before schedule/work
await boss.createQueue('my-job', {
  retryLimit: 3,
  retryDelay: 60,
  expireInSeconds: 600,
  deleteAfterSeconds: 7 * 24 * 60 * 60,
});

// Schedule job to run every minute
await boss.schedule('my-job', '* * * * *', {}, {
  tz: 'UTC',
  singletonKey: 'my-job-schedule',  // Prevents duplicates on restart
});

// Register handler
await boss.work('my-job', { pollingIntervalSeconds: 10 }, async (jobs) => {
  for (const job of jobs) {
    // Process job
  }
});
```

### 2. Queuing Jobs

```typescript
// Queue a single job
await boss.send('process-user', { userId: '123' });

// Queue with options
await boss.send('send-email', { to: 'user@example.com' }, {
  retryLimit: 5,
  expireInSeconds: 300,
});
```

### 3. Batch Processing with Concurrency

```typescript
await boss.work(
  'batch-job',
  { batchSize: 10 },  // Process 10 jobs at once
  async (jobs) => {
    await Promise.all(jobs.map(job => processJob(job)));
  }
);
```

## Reliability Patterns

### Singleton Pattern (Prevent Duplicates)

```typescript
// Use getPgBoss() singleton instead of creating new instances
let boss: PgBoss | null = null;

export async function getPgBoss(): Promise<PgBoss> {
  if (boss) return boss;
  
  boss = new PgBoss({ connectionString: process.env.DATABASE_URL });
  await boss.start();
  return boss;
}
```

### Watchdog for Auto-Recovery

PG Boss can stop unexpectedly (connection drops, crashes). Add a watchdog:

```typescript
let boss: PgBoss | null = null;
let watchdogInterval: NodeJS.Timeout | null = null;

// Listen for unexpected stops
boss.on('stopped', () => {
  console.error('[PG Boss] Stopped unexpectedly');
  boss = null;
  // Watchdog will attempt recovery
});

// Watchdog checks every 60s
watchdogInterval = setInterval(async () => {
  if (!boss && workerRegistrationFn) {
    console.log('[PG Boss] Attempting recovery...');
    await workerRegistrationFn();
  }
}, 60000);
```

### Health Check Integration

Make health check fail when PG Boss is dead (triggers container restart):

```typescript
app.get('/health', (c) => {
  const pgBossRunning = boss !== null;
  
  if (!pgBossRunning) {
    return c.json({ status: 'degraded', pgBossRunning: false }, 503);
  }
  
  return c.json({ status: 'ok', pgBossRunning: true });
});
```

## Debugging

### Check PG Boss State in Database

```sql
-- Check scheduled jobs
SELECT name, cron FROM pgboss.schedule;

-- Check recent jobs
SELECT name, state, created_on, completed_on 
FROM pgboss.job 
ORDER BY created_on DESC 
LIMIT 20;

-- Check job queue size
SELECT name, COUNT(*) 
FROM pgboss.job 
WHERE state = 'created' 
GROUP BY name;
```

### Via Node.js

```javascript
const boss = await getPgBoss();

// Get queue size
const pending = await boss.getQueueSize('my-job');

// Get job by ID
const job = await boss.getJobById(jobId);
```

### Railway-Specific Debugging

```bash
# Check environment variables
railway variables --service api

# Get public DATABASE_URL for direct access
railway variables --service Postgres | grep DATABASE_PUBLIC_URL

# Query database directly
DATABASE_URL="postgresql://..." node -e "
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL, ssl: { rejectUnauthorized: false } });
// Run queries
"
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Jobs not running | PG Boss not started | Check health endpoint, verify DATABASE_URL |
| Duplicate jobs | Missing `singletonKey` | Add singletonKey to `schedule()` call |
| Queue not found | `schedule()` called before `createQueue()` | Call `boss.createQueue(name)` first |
| Jobs stuck in 'created' | No worker registered | Call `boss.work()` for the queue |
| Connection errors | Database URL wrong/expired | Check DATABASE_URL, SSL settings |
| Jobs not persisting | Wrong schema | Verify `schema: 'pgboss'` option |
| Worker over-polling | Wrong option name | Use `pollingIntervalSeconds` (not `newJobCheckIntervalSeconds`) |
| Next.js build fails (`stream/net/tls`) | instrumentation bundles server-only deps | Use `/* webpackIgnore: true */` on instrumentation dynamic imports |

## Best Practices

1. **Always use singletonKey** for scheduled jobs to prevent duplicates on restart
2. **Create queues explicitly** in PG Boss v10+: `await boss.createQueue('my-job')`
3. **Handle the 'stopped' event** to detect unexpected shutdowns
4. **Use a watchdog** to auto-recover from crashes (clear old interval before starting a new one)
5. **Return 503 in health check** when PG Boss is dead (triggers container restart)
6. **Log job errors** but don't swallow them - let PG Boss retry
7. **Use separate workers** for different job types (rollover, email, etc.)
8. **Graceful shutdown**: call `boss.stop({ graceful: true, timeout: 30000 })` on SIGTERM/SIGINT
9. **Next.js instrumentation**: load server-only job modules with `import(/* webpackIgnore: true */ ...)`

## File Structure Example

```
apps/api/src/
├── lib/
│   └── pgboss.ts          # Singleton, getPgBoss(), stopPgBoss()
├── workers/
│   ├── index.ts           # registerAllWorkers()
│   ├── rollover/
│   │   ├── index.ts       # registerRolloverWorkers()
│   │   ├── timezone-check.ts
│   │   └── batch-processor.ts
│   └── email/
│       ├── index.ts       # registerEmailWorkers()
│       └── send-email.ts
└── index.ts               # Calls registerAllWorkers() on startup
```

## Timezone-Aware Scheduling

For jobs that need to run at specific local times (like midnight rollover):

```typescript
import { toZonedTime } from 'date-fns-tz';

// Check if it's midnight in a timezone
const zonedNow = toZonedTime(new Date(), userTimezone);
const hour = zonedNow.getHours();
const minute = zonedNow.getMinutes();

// 10-minute window for reliability
const isMidnightWindow = hour === 0 && minute <= 10;
```

## Idempotency

Use a log table to prevent duplicate processing:

```typescript
// Check if already processed
const existing = await db.query.logs.findFirst({
  where: and(
    eq(logs.timezone, timezone),
    eq(logs.date, targetDate)
  ),
});

if (existing) return; // Already processed

// Process and log
await processJobs();
await db.insert(logs).values({ timezone, date: targetDate, status: 'completed' });
```
