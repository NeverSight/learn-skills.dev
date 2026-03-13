---
name: log-analyzer
description: Expert guide for analyzing application logs including log searching, pattern detection, error tracking, and debugging. Use when investigating issues, tracking errors, or understanding application behavior.
---

# Log Analyzer Skill

## Overview

This skill helps you effectively analyze application logs to diagnose issues, track errors, and understand system behavior. Covers log searching, pattern detection, structured logging, and integration with monitoring tools.

## Log Analysis Philosophy

### Principles
1. **Structure over text**: Structured logs are easier to analyze
2. **Context matters**: Include relevant metadata
3. **Levels have meaning**: Use appropriate severity levels
4. **Correlation is key**: Link related events across services

### Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| ERROR | Something failed, needs attention | Database connection failed |
| WARN | Unexpected but handled | Retry succeeded after failure |
| INFO | Normal operation milestones | User signed up |
| DEBUG | Detailed diagnostic info | Query executed in 50ms |
| TRACE | Very detailed, usually disabled | Function entered/exited |

## Structured Logging

### Winston Configuration (Node.js)

```typescript
// src/lib/logger.ts
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'my-app',
    environment: process.env.NODE_ENV,
  },
  transports: [
    // Console for development
    new winston.transports.Console({
      format: process.env.NODE_ENV === 'development'
        ? winston.format.combine(
            winston.format.colorize(),
            winston.format.simple()
          )
        : winston.format.json(),
    }),
  ],
});

// Add request context
export function createRequestLogger(requestId: string, userId?: string) {
  return logger.child({
    requestId,
    userId,
  });
}

export { logger };
```

### Pino Logger (High Performance)

```typescript
// src/lib/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development'
    ? {
        target: 'pino-pretty',
        options: {
          colorize: true,
          translateTime: 'SYS:standard',
        },
      }
    : undefined,
  base: {
    service: 'my-app',
    env: process.env.NODE_ENV,
  },
  redact: {
    paths: ['password', 'token', 'apiKey', '*.password', '*.token'],
    censor: '[REDACTED]',
  },
});

// Request-scoped logger
export function requestLogger(requestId: string, userId?: string) {
  return logger.child({ requestId, userId });
}
```

### Logging Best Practices

```typescript
// DO: Include context
logger.info('User signed up', {
  userId: user.id,
  email: user.email,
  plan: 'free',
  source: 'web',
});

// DO: Log errors with stack traces
logger.error('Payment failed', {
  error: err.message,
  stack: err.stack,
  userId: user.id,
  amount: 99.99,
  provider: 'stripe',
});

// DO: Use appropriate levels
logger.debug('Database query', {
  query: 'SELECT * FROM users WHERE id = ?',
  duration: 45,
  rows: 1,
});

// DON'T: Log sensitive data
// BAD: logger.info('Login', { password: user.password })

// DON'T: Use string concatenation
// BAD: logger.info('User ' + user.id + ' signed up')
```

## Log Searching & Filtering

### Command Line (grep, jq)

```bash
# Search JSON logs with jq
cat logs.json | jq 'select(.level == "error")'

# Search for specific user
cat logs.json | jq 'select(.userId == "usr_123")'

# Search by time range
cat logs.json | jq 'select(.timestamp >= "2024-01-15T10:00:00")'

# Count errors by type
cat logs.json | jq 'select(.level == "error") | .error.code' | sort | uniq -c

# Extract specific fields
cat logs.json | jq '{timestamp, level, message, userId}'

# Search text logs
grep -i "error" logs.txt
grep -E "error|warn" logs.txt
grep -A5 "ERROR" logs.txt  # 5 lines after match
grep -B3 "ERROR" logs.txt  # 3 lines before match
```

### Vercel Log Analysis

```bash
# View live logs
vercel logs --follow

# Filter by level
vercel logs --level error

# Search specific timeframe
vercel logs --since 2h

# Filter by deployment
vercel logs --deployment-url https://myapp-abc123.vercel.app

# Output JSON for processing
vercel logs --output json | jq 'select(.level == "error")'
```

### Supabase Log Analysis

```sql
-- Query Postgres logs
SELECT *
FROM postgres_logs
WHERE timestamp > now() - interval '1 hour'
  AND error_severity = 'ERROR'
ORDER BY timestamp DESC
LIMIT 100;

-- Query auth logs
SELECT *
FROM auth.audit_log_entries
WHERE timestamp > now() - interval '24 hours'
  AND payload->>'action' = 'login'
ORDER BY timestamp DESC;

-- Find slow queries
SELECT
  query,
  calls,
  mean_exec_time,
  total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

## Pattern Detection

### Common Error Patterns

```typescript
// Error pattern analyzer
interface ErrorPattern {
  pattern: RegExp;
  category: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  suggestion: string;
}

const errorPatterns: ErrorPattern[] = [
  {
    pattern: /ECONNREFUSED|connection refused/i,
    category: 'connectivity',
    severity: 'critical',
    suggestion: 'Check if the target service is running and accessible',
  },
  {
    pattern: /timeout|ETIMEDOUT/i,
    category: 'timeout',
    severity: 'high',
    suggestion: 'Increase timeout or check for slow operations',
  },
  {
    pattern: /out of memory|heap|OOM/i,
    category: 'memory',
    severity: 'critical',
    suggestion: 'Increase memory allocation or fix memory leak',
  },
  {
    pattern: /rate.?limit|429|too many requests/i,
    category: 'rate-limiting',
    severity: 'medium',
    suggestion: 'Implement backoff strategy or increase rate limits',
  },
  {
    pattern: /unauthorized|401|invalid.?token/i,
    category: 'auth',
    severity: 'medium',
    suggestion: 'Check authentication credentials or token expiry',
  },
  {
    pattern: /not.?found|404/i,
    category: 'not-found',
    severity: 'low',
    suggestion: 'Verify resource exists or check URL',
  },
];

function categorizeError(message: string): ErrorPattern | null {
  for (const pattern of errorPatterns) {
    if (pattern.pattern.test(message)) {
      return pattern;
    }
  }
  return null;
}
```

### Log Aggregation Script

```typescript
// scripts/analyze-logs.ts
import * as readline from 'readline';
import * as fs from 'fs';

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  error?: {
    message: string;
    code?: string;
  };
  [key: string]: any;
}

interface LogSummary {
  totalEntries: number;
  byLevel: Record<string, number>;
  errorMessages: Record<string, number>;
  timeRange: {
    start: string;
    end: string;
  };
}

async function analyzeLogs(filePath: string): Promise<LogSummary> {
  const summary: LogSummary = {
    totalEntries: 0,
    byLevel: {},
    errorMessages: {},
    timeRange: { start: '', end: '' },
  };

  const fileStream = fs.createReadStream(filePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    try {
      const entry: LogEntry = JSON.parse(line);
      summary.totalEntries++;

      // Count by level
      summary.byLevel[entry.level] = (summary.byLevel[entry.level] || 0) + 1;

      // Track error messages
      if (entry.level === 'error' && entry.error?.message) {
        const msg = entry.error.message.substring(0, 100);
        summary.errorMessages[msg] = (summary.errorMessages[msg] || 0) + 1;
      }

      // Track time range
      if (!summary.timeRange.start || entry.timestamp < summary.timeRange.start) {
        summary.timeRange.start = entry.timestamp;
      }
      if (!summary.timeRange.end || entry.timestamp > summary.timeRange.end) {
        summary.timeRange.end = entry.timestamp;
      }
    } catch {
      // Skip non-JSON lines
    }
  }

  return summary;
}

// Usage
analyzeLogs('logs.json').then(console.log);
```

## Request Tracing

### Request ID Middleware

```typescript
// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { v4 as uuidv4 } from 'uuid';

export function middleware(request: NextRequest) {
  const requestId = request.headers.get('x-request-id') || uuidv4();

  const response = NextResponse.next();
  response.headers.set('x-request-id', requestId);

  return response;
}
```

### Tracing Context

```typescript
// src/lib/tracing.ts
import { AsyncLocalStorage } from 'async_hooks';

interface TraceContext {
  requestId: string;
  userId?: string;
  startTime: number;
}

const asyncLocalStorage = new AsyncLocalStorage<TraceContext>();

export function withTrace<T>(
  context: TraceContext,
  fn: () => T | Promise<T>
): T | Promise<T> {
  return asyncLocalStorage.run(context, fn);
}

export function getTrace(): TraceContext | undefined {
  return asyncLocalStorage.getStore();
}

// Usage in logger
export function log(level: string, message: string, data?: object) {
  const trace = getTrace();
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level,
    message,
    requestId: trace?.requestId,
    userId: trace?.userId,
    duration: trace ? Date.now() - trace.startTime : undefined,
    ...data,
  }));
}
```

## Error Tracking Integration

### Sentry Integration

```typescript
// src/lib/sentry.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1, // 10% of transactions
  beforeSend(event, hint) {
    // Filter out specific errors
    const error = hint.originalException;
    if (error instanceof Error && error.message.includes('Network')) {
      return null;
    }
    return event;
  },
});

// Capture with context
export function captureError(error: Error, context?: Record<string, any>) {
  Sentry.withScope((scope) => {
    if (context) {
      scope.setExtras(context);
    }
    Sentry.captureException(error);
  });
}

// Usage
try {
  await riskyOperation();
} catch (error) {
  captureError(error, {
    userId: user.id,
    action: 'payment',
    amount: 99.99,
  });
  throw error;
}
```

### Custom Error Boundary Logging

```typescript
// src/components/error-boundary.tsx
'use client';

import { useEffect } from 'react';
import * as Sentry from '@sentry/nextjs';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log to error tracking
    Sentry.captureException(error);

    // Log to console with context
    console.error('Client Error:', {
      message: error.message,
      digest: error.digest,
      stack: error.stack,
      url: window.location.href,
      userAgent: navigator.userAgent,
    });
  }, [error]);

  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

## Log Analysis Queries

### Common Investigation Queries

```bash
# Find all errors for a specific user
jq 'select(.userId == "usr_123" and .level == "error")' logs.json

# Find errors in the last hour
jq --arg time "$(date -d '1 hour ago' -Iseconds)" \
  'select(.timestamp > $time and .level == "error")' logs.json

# Group errors by message
jq -s 'group_by(.error.message) |
  map({message: .[0].error.message, count: length}) |
  sort_by(-.count)' logs.json

# Find slow requests (>1 second)
jq 'select(.duration > 1000)' logs.json

# Trace a specific request
jq 'select(.requestId == "req_abc123")' logs.json | sort_by(.timestamp)

# Find patterns in error messages
jq -r 'select(.level == "error") | .error.message' logs.json | \
  sort | uniq -c | sort -rn | head -20
```

### SQL-Style Log Analysis

```sql
-- Using tools like clickhouse or DuckDB for log analysis

-- Error rate by hour
SELECT
  date_trunc('hour', timestamp) as hour,
  count(*) FILTER (WHERE level = 'error') as errors,
  count(*) as total,
  round(100.0 * count(*) FILTER (WHERE level = 'error') / count(*), 2) as error_rate
FROM logs
WHERE timestamp > now() - interval '24 hours'
GROUP BY 1
ORDER BY 1;

-- Top error messages
SELECT
  error_message,
  count(*) as occurrences,
  min(timestamp) as first_seen,
  max(timestamp) as last_seen
FROM logs
WHERE level = 'error'
  AND timestamp > now() - interval '24 hours'
GROUP BY error_message
ORDER BY occurrences DESC
LIMIT 10;

-- Slowest endpoints
SELECT
  path,
  count(*) as requests,
  avg(duration) as avg_duration,
  max(duration) as max_duration,
  percentile_cont(0.95) WITHIN GROUP (ORDER BY duration) as p95
FROM logs
WHERE timestamp > now() - interval '1 hour'
GROUP BY path
ORDER BY avg_duration DESC
LIMIT 10;
```

## Log Retention & Cleanup

### Log Rotation Configuration

```bash
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload myapp
    endscript
}
```

### Automated Log Cleanup

```typescript
// scripts/cleanup-logs.ts
import * as fs from 'fs';
import * as path from 'path';

const LOG_DIR = '/var/log/myapp';
const RETENTION_DAYS = 30;

function cleanupOldLogs() {
  const now = Date.now();
  const maxAge = RETENTION_DAYS * 24 * 60 * 60 * 1000;

  const files = fs.readdirSync(LOG_DIR);

  for (const file of files) {
    const filePath = path.join(LOG_DIR, file);
    const stats = fs.statSync(filePath);

    if (now - stats.mtime.getTime() > maxAge) {
      fs.unlinkSync(filePath);
      console.log(`Deleted: ${file}`);
    }
  }
}

cleanupOldLogs();
```

## Debugging Checklist

### When Investigating Issues
- [ ] Identify the time window
- [ ] Find related request IDs
- [ ] Check for error spikes
- [ ] Look at affected users/endpoints
- [ ] Check for pattern changes
- [ ] Review recent deployments

### Log Quality Check
- [ ] Structured JSON format
- [ ] Appropriate log levels
- [ ] Request IDs included
- [ ] Sensitive data redacted
- [ ] Stack traces for errors
- [ ] Relevant context included

## When to Use This Skill

Invoke this skill when:
- Investigating production issues
- Setting up logging infrastructure
- Debugging application errors
- Analyzing performance issues
- Creating log analysis scripts
- Setting up error tracking
- Implementing request tracing
- Cleaning up log data
