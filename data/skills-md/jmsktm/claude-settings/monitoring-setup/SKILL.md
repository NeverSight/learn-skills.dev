---
name: monitoring-setup
description: Expert guide for setting up monitoring dashboards, alerting, metrics collection, and observability. Use when implementing application monitoring, setting up alerts, or building dashboards.
---

# Monitoring Setup Skill

## Overview

This skill helps you implement comprehensive monitoring for applications. Covers metrics collection, dashboard creation, alerting strategies, health checks, and observability best practices.

## Monitoring Philosophy

### Four Golden Signals
1. **Latency**: Time to serve a request
2. **Traffic**: Request volume
3. **Errors**: Failed request rate
4. **Saturation**: Resource utilization

### Observability Pillars
- **Metrics**: Numeric measurements over time
- **Logs**: Discrete events with context
- **Traces**: Request flow across services

## Health Check Endpoints

### Comprehensive Health Check

```typescript
// src/app/api/health/route.ts
import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import Redis from 'ioredis';

interface HealthCheck {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  version: string;
  uptime: number;
  checks: {
    database: CheckResult;
    redis: CheckResult;
    external: CheckResult;
  };
}

interface CheckResult {
  status: 'pass' | 'fail';
  latency?: number;
  message?: string;
}

async function checkDatabase(): Promise<CheckResult> {
  const start = Date.now();
  try {
    const supabase = createClient(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );
    await supabase.from('health_check').select('1').single();
    return {
      status: 'pass',
      latency: Date.now() - start,
    };
  } catch (error) {
    return {
      status: 'fail',
      message: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

async function checkRedis(): Promise<CheckResult> {
  const start = Date.now();
  try {
    const redis = new Redis(process.env.REDIS_URL!);
    await redis.ping();
    redis.disconnect();
    return {
      status: 'pass',
      latency: Date.now() - start,
    };
  } catch (error) {
    return {
      status: 'fail',
      message: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

async function checkExternal(): Promise<CheckResult> {
  const start = Date.now();
  try {
    const response = await fetch('https://api.stripe.com/v1/health', {
      method: 'HEAD',
    });
    return {
      status: response.ok ? 'pass' : 'fail',
      latency: Date.now() - start,
    };
  } catch (error) {
    return {
      status: 'fail',
      message: 'External service unavailable',
    };
  }
}

const startTime = Date.now();

export async function GET() {
  const [database, redis, external] = await Promise.all([
    checkDatabase(),
    checkRedis(),
    checkExternal(),
  ]);

  const checks = { database, redis, external };

  const allPassed = Object.values(checks).every((c) => c.status === 'pass');
  const anyFailed = Object.values(checks).some((c) => c.status === 'fail');

  const health: HealthCheck = {
    status: allPassed ? 'healthy' : anyFailed ? 'unhealthy' : 'degraded',
    timestamp: new Date().toISOString(),
    version: process.env.VERCEL_GIT_COMMIT_SHA || 'local',
    uptime: Math.floor((Date.now() - startTime) / 1000),
    checks,
  };

  return NextResponse.json(health, {
    status: health.status === 'healthy' ? 200 : 503,
    headers: {
      'Cache-Control': 'no-store',
    },
  });
}
```

### Kubernetes-Style Probes

```typescript
// src/app/api/health/live/route.ts
// Liveness probe - is the app running?
export async function GET() {
  return new Response('OK', { status: 200 });
}

// src/app/api/health/ready/route.ts
// Readiness probe - can the app handle traffic?
export async function GET() {
  try {
    // Check critical dependencies
    await checkDatabase();
    return new Response('OK', { status: 200 });
  } catch {
    return new Response('Not Ready', { status: 503 });
  }
}
```

## Metrics Collection

### Custom Metrics with Prometheus Client

```typescript
// src/lib/metrics.ts
import { Counter, Histogram, Gauge, Registry } from 'prom-client';

export const registry = new Registry();

// HTTP request metrics
export const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [registry],
});

export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5],
  registers: [registry],
});

// Business metrics
export const activeUsers = new Gauge({
  name: 'active_users',
  help: 'Number of currently active users',
  registers: [registry],
});

export const ordersTotal = new Counter({
  name: 'orders_total',
  help: 'Total orders processed',
  labelNames: ['status', 'payment_method'],
  registers: [registry],
});

// Database metrics
export const dbQueryDuration = new Histogram({
  name: 'db_query_duration_seconds',
  help: 'Database query duration',
  labelNames: ['operation', 'table'],
  buckets: [0.001, 0.01, 0.05, 0.1, 0.5, 1],
  registers: [registry],
});
```

### Metrics Endpoint

```typescript
// src/app/api/metrics/route.ts
import { NextResponse } from 'next/server';
import { registry } from '@/lib/metrics';

export async function GET(request: Request) {
  // Optional: Basic auth protection
  const authHeader = request.headers.get('authorization');
  if (authHeader !== `Bearer ${process.env.METRICS_TOKEN}`) {
    return new Response('Unauthorized', { status: 401 });
  }

  const metrics = await registry.metrics();

  return new Response(metrics, {
    headers: {
      'Content-Type': registry.contentType,
    },
  });
}
```

### Middleware for Request Metrics

```typescript
// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { httpRequestsTotal, httpRequestDuration } from '@/lib/metrics';

export async function middleware(request: NextRequest) {
  const start = Date.now();

  const response = NextResponse.next();

  // Record metrics after response
  const route = request.nextUrl.pathname;
  const method = request.method;
  const status = response.status.toString();

  httpRequestsTotal.inc({ method, route, status });
  httpRequestDuration.observe(
    { method, route },
    (Date.now() - start) / 1000
  );

  return response;
}
```

## Alerting Configuration

### Alert Rules (Prometheus/Grafana)

```yaml
# alerts.yml
groups:
  - name: application
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
          > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          description: Error rate is {{ $value | humanizePercentage }} over the last 5 minutes

      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
          description: 95th percentile latency is {{ $value | humanizeDuration }}

      # Service down
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: Service is down
          description: "{{ $labels.instance }} has been down for more than 1 minute"

      # Database connection pool exhausted
      - alert: DatabaseConnectionsHigh
        expr: pg_stat_activity_count > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: Database connection pool nearly exhausted
          description: "{{ $value }} connections in use"

  - name: infrastructure
    rules:
      # High CPU
      - alert: HighCPU
        expr: node_cpu_seconds_total{mode="idle"} < 20
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: High CPU usage

      # Low disk space
      - alert: LowDiskSpace
        expr: |
          (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: Low disk space
          description: Only {{ $value | humanizePercentage }} disk space remaining
```

### Vercel/Uptime Monitoring

```typescript
// scripts/uptime-check.ts
// Run via cron or external monitoring service

const ENDPOINTS = [
  { name: 'Health', url: 'https://myapp.com/api/health' },
  { name: 'Homepage', url: 'https://myapp.com' },
  { name: 'API', url: 'https://myapp.com/api/status' },
];

const WEBHOOK_URL = process.env.SLACK_WEBHOOK_URL;

async function checkEndpoint(endpoint: typeof ENDPOINTS[0]) {
  const start = Date.now();
  try {
    const response = await fetch(endpoint.url, {
      method: 'GET',
      signal: AbortSignal.timeout(10000),
    });

    return {
      name: endpoint.name,
      url: endpoint.url,
      status: response.status,
      latency: Date.now() - start,
      healthy: response.ok,
    };
  } catch (error) {
    return {
      name: endpoint.name,
      url: endpoint.url,
      status: 0,
      latency: Date.now() - start,
      healthy: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

async function notifySlack(message: string) {
  if (!WEBHOOK_URL) return;

  await fetch(WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: message }),
  });
}

async function runChecks() {
  const results = await Promise.all(ENDPOINTS.map(checkEndpoint));

  const unhealthy = results.filter((r) => !r.healthy);

  if (unhealthy.length > 0) {
    const message = `🚨 *Uptime Alert*\n${unhealthy
      .map((r) => `• ${r.name}: ${r.error || `Status ${r.status}`}`)
      .join('\n')}`;

    await notifySlack(message);
  }

  console.log(JSON.stringify(results, null, 2));
}

runChecks();
```

## Dashboard Configuration

### Grafana Dashboard JSON

```json
{
  "title": "Application Overview",
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total[5m])) by (route)",
          "legendFormat": "{{ route }}"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "thresholds": {
            "steps": [
              { "value": 0, "color": "green" },
              { "value": 1, "color": "yellow" },
              { "value": 5, "color": "red" }
            ]
          }
        }
      }
    },
    {
      "title": "Response Time (p95)",
      "type": "gauge",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "s",
          "thresholds": {
            "steps": [
              { "value": 0, "color": "green" },
              { "value": 0.5, "color": "yellow" },
              { "value": 2, "color": "red" }
            ]
          }
        }
      }
    },
    {
      "title": "Active Users",
      "type": "stat",
      "targets": [
        {
          "expr": "active_users"
        }
      ]
    }
  ]
}
```

### Vercel Analytics Integration

```typescript
// src/app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

## Status Page

### Simple Status Page

```typescript
// src/app/status/page.tsx
import { Suspense } from 'react';

interface ServiceStatus {
  name: string;
  status: 'operational' | 'degraded' | 'outage';
  lastChecked: string;
}

async function getStatus(): Promise<ServiceStatus[]> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_APP_URL}/api/health`,
    { next: { revalidate: 60 } }
  );

  if (!response.ok) {
    return [
      { name: 'API', status: 'outage', lastChecked: new Date().toISOString() },
    ];
  }

  const health = await response.json();

  return [
    {
      name: 'API',
      status: health.status === 'healthy' ? 'operational' : 'degraded',
      lastChecked: health.timestamp,
    },
    {
      name: 'Database',
      status: health.checks.database.status === 'pass' ? 'operational' : 'outage',
      lastChecked: health.timestamp,
    },
    {
      name: 'Cache',
      status: health.checks.redis.status === 'pass' ? 'operational' : 'degraded',
      lastChecked: health.timestamp,
    },
  ];
}

function StatusBadge({ status }: { status: ServiceStatus['status'] }) {
  const colors = {
    operational: 'bg-green-500',
    degraded: 'bg-yellow-500',
    outage: 'bg-red-500',
  };

  return (
    <span className={`inline-block w-3 h-3 rounded-full ${colors[status]}`} />
  );
}

export default async function StatusPage() {
  const services = await getStatus();
  const allOperational = services.every((s) => s.status === 'operational');

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-8">System Status</h1>

      <div className={`p-4 rounded-lg mb-8 ${
        allOperational ? 'bg-green-100' : 'bg-yellow-100'
      }`}>
        <p className="font-medium">
          {allOperational
            ? 'All systems operational'
            : 'Some systems experiencing issues'}
        </p>
      </div>

      <div className="space-y-4">
        {services.map((service) => (
          <div
            key={service.name}
            className="flex items-center justify-between p-4 border rounded"
          >
            <div className="flex items-center gap-3">
              <StatusBadge status={service.status} />
              <span className="font-medium">{service.name}</span>
            </div>
            <span className="text-sm text-gray-500 capitalize">
              {service.status}
            </span>
          </div>
        ))}
      </div>

      <p className="mt-8 text-sm text-gray-500">
        Last updated: {new Date().toLocaleString()}
      </p>
    </div>
  );
}
```

## Monitoring Checklist

### Application Monitoring
- [ ] Health check endpoint
- [ ] Request latency metrics
- [ ] Error rate tracking
- [ ] Active user count
- [ ] Business metrics (orders, signups, etc.)

### Infrastructure Monitoring
- [ ] CPU/Memory utilization
- [ ] Disk space
- [ ] Network I/O
- [ ] Database connections
- [ ] Cache hit rate

### Alerting
- [ ] Error rate thresholds
- [ ] Latency thresholds
- [ ] Uptime monitoring
- [ ] Resource alerts
- [ ] On-call rotation configured

### Dashboards
- [ ] Overview dashboard
- [ ] API performance
- [ ] Database metrics
- [ ] Business KPIs
- [ ] Status page (public)

## When to Use This Skill

Invoke this skill when:
- Setting up monitoring for a new project
- Creating health check endpoints
- Implementing metrics collection
- Configuring alerting rules
- Building monitoring dashboards
- Setting up status pages
- Debugging performance issues
- Planning capacity
