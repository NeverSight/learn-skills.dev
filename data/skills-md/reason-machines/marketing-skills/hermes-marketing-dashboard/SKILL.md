---
name: hermes-marketing-dashboard
description: Open-source marketing operations control center for AI agent teams with CRM, outreach, content ops, and analytics powered by OpenClaw + SQLite
triggers:
  - set up hermes marketing dashboard
  - configure openclaw marketing operations
  - build ai agent marketing control center
  - integrate crm with openclaw agents
  - create marketing automation dashboard
  - deploy hermes dashboard with sqlite
  - set up marketing ops for ai teams
  - configure hermes openclaw integration
---

# Hermes Marketing Dashboard

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Hermes Dashboard is an open-source marketing operations control center designed for AI agent teams. It provides CRM, outreach sequencing, content operations, analytics, and automation workflows in a single Next.js application powered by OpenClaw integration and local SQLite storage.

## Installation

### Prerequisites

- Node.js 18+
- pnpm (required) - install with `npm install -g pnpm` or `corepack enable`
- OpenClaw CLI (optional but recommended for agent integration)

### Quick Start

```bash
git clone https://github.com/builderz-labs/marketing-dashboard.git
cd marketing-dashboard
pnpm install
pnpm env:bootstrap
pnpm dev
```

The application will start at `http://localhost:3000`.

## Configuration

### Required Environment Variables

Create a `.env.local` file:

```bash
# Authentication (required)
AUTH_USER=admin
AUTH_PASS=your-secure-password-min-10-chars
API_KEY=your-api-key-for-programmatic-access

# Cookie security (false for HTTP local, true for HTTPS production)
AUTH_COOKIE_SECURE=false

# Database (auto-created in ./state)
DATABASE_URL=./state/hermes.db
```

### OpenClaw Integration

For AI agent integration with OpenClaw:

```bash
# OpenClaw home directory
HERMES_OPENCLAW_HOME=/path/to/openclaw

# Default instance name
HERMES_DEFAULT_INSTANCE=main

# Multi-instance support (optional JSON array)
HERMES_OPENCLAW_INSTANCES='[{"name":"prod","path":"/openclaw/prod"},{"name":"dev","path":"/openclaw/dev"}]'
```

### Security Configuration

```bash
# Host access lock (default: local-only)
HERMES_HOST_LOCK=local  # or 'off' or 'host1,host2'

# Writeback protection (keep false unless explicitly needed)
HERMES_ALLOW_POLICY_WRITE=false
HERMES_ALLOW_CRON_WRITE=false
HERMES_ALLOW_WORKSPACE_WRITE=false
```

### Optional Analytics Integration

```bash
# Plausible Analytics
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=yourdomain.com
PLAUSIBLE_API_KEY=your-plausible-api-key

# Google Analytics 4
NEXT_PUBLIC_GA4_ID=G-XXXXXXXXXX
```

### 1Password Runtime Overlay (Optional)

```bash
HERMES_1PASSWORD_MODE=auto  # off|auto|required
HERMES_OP_ENV_FILE=/etc/hermes-dashboard/hermes-dashboard.op.env
```

## Key Commands

### Development

```bash
# Start development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Type checking
pnpm typecheck

# Linting
pnpm lint

# Run tests
pnpm test

# Run end-to-end tests
pnpm test:e2e
```

### Database Management

```bash
# Bootstrap environment and database
pnpm env:bootstrap

# Reset database (warning: destructive)
pnpm db:reset
```

### Template Export

```bash
# Audit template for sensitive data
./scripts/template-audit.sh

# Export clean template
./scripts/template-export.sh /path/to/output
```

## Core API Patterns

### CRM Lead Management

```typescript
// app/api/crm/leads/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getDatabase } from '@/lib/db';

export async function GET(request: NextRequest) {
  const db = getDatabase();
  
  const leads = db.prepare(`
    SELECT id, email, name, source, status, created_at
    FROM crm_leads
    WHERE status = ?
    ORDER BY created_at DESC
  `).all('active');
  
  return NextResponse.json({ leads });
}

export async function POST(request: NextRequest) {
  const db = getDatabase();
  const { email, name, source, metadata } = await request.json();
  
  const result = db.prepare(`
    INSERT INTO crm_leads (email, name, source, metadata, status)
    VALUES (?, ?, ?, ?, 'new')
  `).run(email, name, source, JSON.stringify(metadata));
  
  return NextResponse.json({ id: result.lastInsertRowid }, { status: 201 });
}
```

### Outreach Sequencing

```typescript
// lib/outreach/sequence.ts
import { getDatabase } from '@/lib/db';

export interface OutreachSequence {
  id: number;
  name: string;
  steps: OutreachStep[];
  status: 'active' | 'paused' | 'archived';
}

export interface OutreachStep {
  order: number;
  delay_hours: number;
  template_id: string;
  channel: 'email' | 'linkedin' | 'twitter';
}

export function createSequence(
  name: string,
  steps: OutreachStep[]
): number {
  const db = getDatabase();
  
  const result = db.prepare(`
    INSERT INTO outreach_sequences (name, steps, status)
    VALUES (?, ?, 'active')
  `).run(name, JSON.stringify(steps));
  
  return result.lastInsertRowid as number;
}

export function enrollInSequence(
  leadId: number,
  sequenceId: number
): void {
  const db = getDatabase();
  
  db.prepare(`
    INSERT INTO outreach_enrollments (lead_id, sequence_id, current_step, status)
    VALUES (?, ?, 0, 'active')
  `).run(leadId, sequenceId);
}

export function pauseSequence(sequenceId: number): void {
  const db = getDatabase();
  
  db.prepare(`
    UPDATE outreach_sequences
    SET status = 'paused'
    WHERE id = ?
  `).run(sequenceId);
}
```

### Content Operations

```typescript
// lib/content/calendar.ts
import { getDatabase } from '@/lib/db';

export interface ContentItem {
  id: number;
  title: string;
  type: 'blog' | 'social' | 'email' | 'video';
  status: 'draft' | 'scheduled' | 'published';
  scheduled_at?: Date;
  published_at?: Date;
  metadata: Record<string, any>;
}

export function getContentCalendar(
  startDate: Date,
  endDate: Date
): ContentItem[] {
  const db = getDatabase();
  
  const items = db.prepare(`
    SELECT id, title, type, status, scheduled_at, published_at, metadata
    FROM content_items
    WHERE scheduled_at BETWEEN ? AND ?
    ORDER BY scheduled_at ASC
  `).all(startDate.toISOString(), endDate.toISOString());
  
  return items.map(item => ({
    ...item,
    metadata: JSON.parse(item.metadata as string),
    scheduled_at: item.scheduled_at ? new Date(item.scheduled_at) : undefined,
    published_at: item.published_at ? new Date(item.published_at) : undefined,
  }));
}

export function createContentItem(item: Omit<ContentItem, 'id'>): number {
  const db = getDatabase();
  
  const result = db.prepare(`
    INSERT INTO content_items (title, type, status, scheduled_at, metadata)
    VALUES (?, ?, ?, ?, ?)
  `).run(
    item.title,
    item.type,
    item.status,
    item.scheduled_at?.toISOString(),
    JSON.stringify(item.metadata)
  );
  
  return result.lastInsertRowid as number;
}
```

### OpenClaw Agent Integration

```typescript
// lib/openclaw/agents.ts
import { readdir, readFile } from 'fs/promises';
import { join } from 'path';

export interface OpenClawAgent {
  name: string;
  description: string;
  type: 'agent' | 'squad';
  capabilities: string[];
  config: Record<string, any>;
}

export async function discoverAgents(
  openclawHome: string
): Promise<OpenClawAgent[]> {
  const agentsDir = join(openclawHome, 'agents');
  const agents: OpenClawAgent[] = [];
  
  try {
    const entries = await readdir(agentsDir, { withFileTypes: true });
    
    for (const entry of entries) {
      if (entry.isDirectory()) {
        const configPath = join(agentsDir, entry.name, 'agent.json');
        try {
          const configData = await readFile(configPath, 'utf-8');
          const config = JSON.parse(configData);
          
          agents.push({
            name: entry.name,
            description: config.description || '',
            type: config.type || 'agent',
            capabilities: config.capabilities || [],
            config,
          });
        } catch (err) {
          console.warn(`Could not load agent config for ${entry.name}`);
        }
      }
    }
  } catch (err) {
    console.error('Failed to discover agents:', err);
  }
  
  return agents;
}
```

### Cron Job Management

```typescript
// lib/cron/scheduler.ts
import { getDatabase } from '@/lib/db';

export interface CronJob {
  id: number;
  name: string;
  schedule: string;  // cron expression, 'every 1h', or 'at 09:00'
  agent: string;
  task: string;
  enabled: boolean;
  last_run?: Date;
}

export function createCronJob(job: Omit<CronJob, 'id'>): number {
  const db = getDatabase();
  
  const result = db.prepare(`
    INSERT INTO cron_jobs (name, schedule, agent, task, enabled)
    VALUES (?, ?, ?, ?, ?)
  `).run(job.name, job.schedule, job.agent, job.task, job.enabled ? 1 : 0);
  
  return result.lastInsertRowid as number;
}

export function getCronJobs(): CronJob[] {
  const db = getDatabase();
  
  const jobs = db.prepare(`
    SELECT id, name, schedule, agent, task, enabled, last_run
    FROM cron_jobs
    ORDER BY name ASC
  `).all();
  
  return jobs.map(job => ({
    ...job,
    enabled: Boolean(job.enabled),
    last_run: job.last_run ? new Date(job.last_run) : undefined,
  }));
}

export function updateLastRun(jobId: number): void {
  const db = getDatabase();
  
  db.prepare(`
    UPDATE cron_jobs
    SET last_run = ?
    WHERE id = ?
  `).run(new Date().toISOString(), jobId);
}
```

## Authentication Patterns

### Session-Based Auth

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const session = request.cookies.get('hermes-session');
  
  if (!session && request.nextUrl.pathname.startsWith('/api/')) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: '/api/:path*',
};
```

### API Key Auth

```typescript
// lib/auth/api-key.ts
import { NextRequest } from 'next/server';

export function validateApiKey(request: NextRequest): boolean {
  const authHeader = request.headers.get('authorization');
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return false;
  }
  
  const token = authHeader.substring(7);
  return token === process.env.API_KEY;
}

// Usage in API route
export async function GET(request: NextRequest) {
  if (!validateApiKey(request)) {
    return NextResponse.json({ error: 'Invalid API key' }, { status: 401 });
  }
  
  // Continue with request...
}
```

## Analytics Integration

### Track Events

```typescript
// lib/analytics/events.ts
import { getDatabase } from '@/lib/db';

export interface AnalyticsEvent {
  event_type: string;
  properties: Record<string, any>;
  user_id?: string;
  session_id?: string;
}

export function trackEvent(event: AnalyticsEvent): void {
  const db = getDatabase();
  
  db.prepare(`
    INSERT INTO analytics_events (event_type, properties, user_id, session_id, timestamp)
    VALUES (?, ?, ?, ?, ?)
  `).run(
    event.event_type,
    JSON.stringify(event.properties),
    event.user_id,
    event.session_id,
    new Date().toISOString()
  );
}

export function getKPIs(startDate: Date, endDate: Date) {
  const db = getDatabase();
  
  return {
    leads: db.prepare(`
      SELECT COUNT(*) as count FROM crm_leads
      WHERE created_at BETWEEN ? AND ?
    `).get(startDate.toISOString(), endDate.toISOString()),
    
    outreach_sent: db.prepare(`
      SELECT COUNT(*) as count FROM outreach_messages
      WHERE sent_at BETWEEN ? AND ?
    `).get(startDate.toISOString(), endDate.toISOString()),
    
    content_published: db.prepare(`
      SELECT COUNT(*) as count FROM content_items
      WHERE published_at BETWEEN ? AND ?
    `).get(startDate.toISOString(), endDate.toISOString()),
  };
}
```

## Component Patterns

### Dashboard Widget

```typescript
// components/dashboard/LeadsFunnel.tsx
'use client';

import { useEffect, useState } from 'react';

interface FunnelData {
  stage: string;
  count: number;
}

export function LeadsFunnel() {
  const [data, setData] = useState<FunnelData[]>([]);
  
  useEffect(() => {
    fetch('/api/crm/funnel')
      .then(res => res.json())
      .then(setData);
  }, []);
  
  return (
    <div className="funnel-widget">
      <h3>Pipeline Funnel</h3>
      {data.map(stage => (
        <div key={stage.stage} className="funnel-stage">
          <span>{stage.stage}</span>
          <span>{stage.count}</span>
        </div>
      ))}
    </div>
  );
}
```

## Troubleshooting

### Database Lock Errors

SQLite database locks can occur with concurrent writes:

```typescript
// lib/db.ts
import Database from 'better-sqlite3';

let db: Database.Database | null = null;

export function getDatabase(): Database.Database {
  if (!db) {
    db = new Database(process.env.DATABASE_URL || './state/hermes.db');
    db.pragma('journal_mode = WAL'); // Write-Ahead Logging for better concurrency
    db.pragma('busy_timeout = 5000'); // 5 second timeout
  }
  return db;
}
```

### OpenClaw Agent Discovery Fails

Ensure `HERMES_OPENCLAW_HOME` points to valid directory:

```bash
# Verify path
ls $HERMES_OPENCLAW_HOME/agents

# Check permissions
chmod -R u+r $HERMES_OPENCLAW_HOME/agents
```

### Session Cookie Not Persisting

For HTTPS deployments, ensure:

```bash
AUTH_COOKIE_SECURE=true
```

For local HTTP development:

```bash
AUTH_COOKIE_SECURE=false
```

### Host Lock Blocking Access

If you need to access from network:

```bash
# Disable (not recommended for production)
HERMES_HOST_LOCK=off

# Allow specific hosts
HERMES_HOST_LOCK=localhost,192.168.1.100,mydomain.com
```

### API Authentication Failures

Verify API key in request headers:

```bash
curl -H "Authorization: Bearer $API_KEY" http://localhost:3000/api/crm/leads
```

Check environment variable is loaded:

```typescript
// In API route
if (!process.env.API_KEY) {
  console.error('API_KEY not configured');
}
```

## Production Deployment

### Security Checklist

1. Change default credentials:
   ```bash
   AUTH_USER=your-admin-username
   AUTH_PASS=strong-password-min-10-chars
   API_KEY=cryptographically-secure-key
   ```

2. Enable HTTPS cookie security:
   ```bash
   AUTH_COOKIE_SECURE=true
   ```

3. Keep host lock enabled:
   ```bash
   HERMES_HOST_LOCK=yourdomain.com
   ```

4. Keep writeback disabled unless required:
   ```bash
   HERMES_ALLOW_POLICY_WRITE=false
   HERMES_ALLOW_CRON_WRITE=false
   HERMES_ALLOW_WORKSPACE_WRITE=false
   ```

### Build and Deploy

```bash
pnpm build
pnpm start
```

For Docker deployment:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

EXPOSE 3000
CMD ["pnpm", "start"]
```

## Common Patterns

### Multi-Instance OpenClaw Setup

```typescript
// lib/openclaw/instances.ts
export function getInstances(): Array<{name: string, path: string}> {
  const instancesEnv = process.env.HERMES_OPENCLAW_INSTANCES;
  
  if (instancesEnv) {
    return JSON.parse(instancesEnv);
  }
  
  return [{
    name: process.env.HERMES_DEFAULT_INSTANCE || 'main',
    path: process.env.HERMES_OPENCLAW_HOME || './openclaw'
  }];
}
```

### Audit Logging

```typescript
// lib/audit/logger.ts
import { getDatabase } from '@/lib/db';

export function logAuditEvent(
  action: string,
  userId: string,
  metadata: Record<string, any>
): void {
  const db = getDatabase();
  
  db.prepare(`
    INSERT INTO audit_log (action, user_id, metadata, timestamp)
    VALUES (?, ?, ?, ?)
  `).run(action, userId, JSON.stringify(metadata), new Date().toISOString());
}
```
