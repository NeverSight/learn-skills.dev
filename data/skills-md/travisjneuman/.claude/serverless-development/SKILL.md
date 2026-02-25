---
name: serverless-development
description: >-
  AWS Lambda, Vercel Edge Functions, Cloudflare Workers, cold starts, deployment patterns, and infrastructure as code (SST, Serverless Framework). Use when building serverless applications or optimizing function-based architectures.
---

# Serverless Development

## Overview

This skill covers building applications on serverless compute platforms where infrastructure management is abstracted away. It addresses AWS Lambda (Node.js, Python, Go runtimes), Vercel Edge Functions and Serverless Functions, Cloudflare Workers, cold start optimization, serverless design patterns (fan-out, step functions, event-driven), database connection management, deployment with SAM/SST/Serverless Framework, monitoring, and cost optimization.

Use this skill when building APIs, webhooks, background processing, scheduled tasks, or any workload that benefits from auto-scaling, pay-per-use pricing, and zero infrastructure management.

---

## Core Principles

1. **Design for statelessness** - Every function invocation is independent. Never store state in global variables between invocations (though you can reuse connections). Use external state stores (databases, caches, queues) for persistence.
2. **Minimize cold starts** - Cold starts add 100ms-10s of latency on first invocation. Keep bundles small, use lightweight runtimes, and consider provisioned concurrency for latency-sensitive paths.
3. **Connection management is critical** - Serverless functions can spawn thousands of concurrent instances. Each opening its own database connection will exhaust connection pools. Use connection pooling (RDS Proxy, Prisma Data Proxy, PgBouncer).
4. **Pay-per-invocation thinking** - You pay for execution time and memory. Optimize hot paths, choose appropriate memory sizes (more memory = more CPU = potentially faster = sometimes cheaper), and batch operations where possible.
5. **Embrace the constraints** - Function timeouts, payload limits, and concurrency limits are features, not bugs. Design around them: use queues for long tasks, S3 for large payloads, and step functions for complex orchestration.

---

## Key Patterns

### Pattern 1: AWS Lambda with TypeScript

**When to use:** Backend APIs, event processing, scheduled tasks on AWS.

**Implementation:**

```typescript
// handler.ts - Lambda handler with proper typing
import {
  APIGatewayProxyEventV2,
  APIGatewayProxyResultV2,
  SQSEvent,
  ScheduledEvent,
  Context,
} from "aws-lambda";

// Reusable across invocations (connection reuse)
let dbConnection: PrismaClient | null = null;

function getDb(): PrismaClient {
  if (!dbConnection) {
    dbConnection = new PrismaClient({
      datasources: {
        db: { url: process.env.DATABASE_URL },
      },
    });
  }
  return dbConnection;
}

// API Gateway handler
export async function apiHandler(
  event: APIGatewayProxyEventV2,
  context: Context
): Promise<APIGatewayProxyResultV2> {
  // Don't wait for event loop to drain (for connection reuse)
  context.callbackWaitsForEmptyEventLoop = false;

  try {
    const method = event.requestContext.http.method;
    const path = event.rawPath;

    if (method === "GET" && path === "/api/users") {
      const db = getDb();
      const users = await db.user.findMany({ take: 50 });
      return response(200, { users });
    }

    if (method === "POST" && path === "/api/users") {
      const body = JSON.parse(event.body ?? "{}");
      const db = getDb();
      const user = await db.user.create({ data: body });
      return response(201, { user });
    }

    return response(404, { error: "Not found" });
  } catch (error) {
    console.error("Handler error:", error);
    return response(500, { error: "Internal server error" });
  }
}

// SQS event handler (batch processing)
export async function sqsHandler(event: SQSEvent): Promise<{ batchItemFailures: Array<{ itemIdentifier: string }> }> {
  const failures: string[] = [];

  for (const record of event.Records) {
    try {
      const body = JSON.parse(record.body);
      await processMessage(body);
    } catch (error) {
      console.error(`Failed to process message ${record.messageId}:`, error);
      failures.push(record.messageId);
    }
  }

  // Partial batch failure reporting (only retry failed messages)
  return {
    batchItemFailures: failures.map((id) => ({ itemIdentifier: id })),
  };
}

// Scheduled event handler (cron)
export async function cronHandler(event: ScheduledEvent): Promise<void> {
  console.log("Running scheduled task at:", event.time);
  const db = getDb();

  // Clean up expired sessions
  const deleted = await db.session.deleteMany({
    where: { expiresAt: { lt: new Date() } },
  });

  console.log(`Cleaned up ${deleted.count} expired sessions`);
}

function response(statusCode: number, body: Record<string, unknown>): APIGatewayProxyResultV2 {
  return {
    statusCode,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": process.env.ALLOWED_ORIGIN ?? "*",
    },
    body: JSON.stringify(body),
  };
}
```

```yaml
# template.yaml - AWS SAM template
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: nodejs20.x
    Timeout: 30
    MemorySize: 256
    Environment:
      Variables:
        DATABASE_URL: !Ref DatabaseUrl
        NODE_OPTIONS: "--enable-source-maps"

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: dist/handler.apiHandler
      Events:
        Api:
          Type: HttpApi
          Properties:
            Path: /api/{proxy+}
            Method: ANY
    Metadata:
      BuildMethod: esbuild
      BuildProperties:
        Minify: true
        Target: es2022
        Sourcemap: true
        EntryPoints:
          - src/handler.ts

  QueueProcessor:
    Type: AWS::Serverless::Function
    Properties:
      Handler: dist/handler.sqsHandler
      Events:
        Queue:
          Type: SQS
          Properties:
            Queue: !GetAtt ProcessingQueue.Arn
            BatchSize: 10
            FunctionResponseTypes:
              - ReportBatchItemFailures

  ScheduledCleanup:
    Type: AWS::Serverless::Function
    Properties:
      Handler: dist/handler.cronHandler
      Events:
        Schedule:
          Type: Schedule
          Properties:
            Schedule: rate(1 hour)

  ProcessingQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DLQ.Arn
        maxReceiveCount: 3

  DLQ:
    Type: AWS::SQS::Queue
```

**Why:** AWS Lambda with SAM provides infrastructure-as-code, local testing (`sam local invoke`), and automated deployment. Connection reuse via module-level variables avoids the cold start penalty of reconnecting on every invocation. Partial batch failure reporting for SQS ensures only failed messages are retried.

---

### Pattern 2: Vercel Edge Functions

**When to use:** Low-latency API routes and middleware that need to run close to users globally.

**Implementation:**

```typescript
// app/api/geo/route.ts - Edge Function
export const runtime = "edge"; // Run on Vercel Edge Network

export async function GET(request: Request) {
  // Access geo information (available at the edge)
  const country = request.headers.get("x-vercel-ip-country") ?? "US";
  const city = request.headers.get("x-vercel-ip-city") ?? "Unknown";

  // Edge-compatible KV store
  const cachedData = await kv.get(`content:${country}`);
  if (cachedData) {
    return Response.json(cachedData);
  }

  // Lightweight processing at the edge
  const content = await getLocalizedContent(country);
  await kv.set(`content:${country}`, content, { ex: 3600 });

  return Response.json(content, {
    headers: {
      "Cache-Control": "public, s-maxage=3600, stale-while-revalidate=86400",
    },
  });
}
```

```typescript
// middleware.ts - Edge Middleware for auth, redirects, A/B testing
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export const config = {
  matcher: ["/dashboard/:path*", "/api/:path*"],
};

export function middleware(request: NextRequest) {
  // Auth check at the edge (fast, runs before serverless function)
  const token = request.cookies.get("session_token");

  if (!token && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // A/B test assignment at the edge
  const abCookie = request.cookies.get("ab-pricing");
  if (!abCookie && request.nextUrl.pathname === "/pricing") {
    const variant = Math.random() < 0.5 ? "control" : "new-layout";
    const response = NextResponse.next();
    response.cookies.set("ab-pricing", variant, { maxAge: 60 * 60 * 24 * 30 });

    // Rewrite to variant-specific page
    if (variant === "new-layout") {
      return NextResponse.rewrite(new URL("/pricing-v2", request.url));
    }
    return response;
  }

  return NextResponse.next();
}
```

**Why:** Edge Functions run in 30+ global locations with sub-millisecond cold starts (V8 isolates, not containers). They're ideal for auth checks, geo-routing, A/B testing, and API responses that benefit from proximity to users. The tradeoff: limited runtime (no Node.js APIs, no native modules, smaller memory).

---

### Pattern 3: Cold Start Optimization

**When to use:** When latency-sensitive endpoints experience unacceptable cold start times.

**Implementation:**

```typescript
// 1. Minimize bundle size with esbuild tree-shaking
// esbuild.config.mjs
import { build } from "esbuild";

await build({
  entryPoints: ["src/handler.ts"],
  bundle: true,
  minify: true,
  platform: "node",
  target: "node20",
  outdir: "dist",
  external: [
    // Don't bundle the AWS SDK (already available in Lambda)
    "@aws-sdk/*",
  ],
  // Tree-shake unused code
  treeShaking: true,
  // Source maps for debugging
  sourcemap: true,
});
```

```typescript
// 2. Lazy-load heavy dependencies
let _sharp: typeof import("sharp") | null = null;

async function getSharp() {
  if (!_sharp) {
    _sharp = await import("sharp");
  }
  return _sharp;
}

// Only load sharp when actually processing images
export async function imageHandler(event: APIGatewayProxyEventV2) {
  if (event.rawPath.includes("/resize")) {
    const sharp = await getSharp();
    // Use sharp...
  }
}
```

```typescript
// 3. Provisioned concurrency for critical paths
// In SAM template:
// Properties:
//   ProvisionedConcurrencyConfig:
//     ProvisionedConcurrentExecutions: 5

// 4. Keep-alive with scheduled warming (cheaper than provisioned concurrency)
// CloudWatch rule: rate(5 minutes) -> Lambda with warming event
export async function handler(event: unknown) {
  // Check if this is a warming invocation
  if ((event as Record<string, unknown>).source === "serverless-warming") {
    console.log("Warming invocation, returning early");
    return { statusCode: 200, body: "warm" };
  }

  // Normal handler logic...
}
```

**Why:** Cold starts are the primary latency concern in serverless. Smaller bundles initialize faster. Lazy loading defers heavy import costs to when they're actually needed. Provisioned concurrency eliminates cold starts entirely for critical paths (at a cost). Warming invocations keep a function instance hot without paying for provisioned concurrency.

---

### Pattern 4: Database Connection Pooling

**When to use:** Any serverless function that connects to a relational database.

**Implementation:**

```typescript
// prisma/schema.prisma - Use Prisma Accelerate or Data Proxy for serverless
datasource db {
  provider = "postgresql"
  // Direct connection for migrations
  url      = env("DATABASE_URL")
  // Pooled connection for serverless runtime
  directUrl = env("DIRECT_DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}
```

```typescript
// For AWS Lambda: Use RDS Proxy
// DATABASE_URL = "postgresql://user:pass@my-rds-proxy.proxy-xxx.region.rds.amazonaws.com:5432/mydb"

// For Vercel/Cloudflare: Use Neon serverless driver or Prisma Accelerate
import { Pool, neonConfig } from "@neondatabase/serverless";
import { PrismaNeon } from "@prisma/adapter-neon";
import { PrismaClient } from "@prisma/client";
import ws from "ws";

// Required for Node.js environments
neonConfig.webSocketConstructor = ws;

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const adapter = new PrismaNeon(pool);
const prisma = new PrismaClient({ adapter });

// Connection reuse pattern
let client: PrismaClient | null = null;

export function getClient(): PrismaClient {
  if (!client) {
    client = new PrismaClient({
      log: process.env.NODE_ENV === "development" ? ["query"] : [],
    });
  }
  return client;
}
```

**Why:** Each Lambda invocation can create a new database connection. With thousands of concurrent invocations, this exhausts the database connection limit (typically 100-500 for managed databases). Connection pooling (RDS Proxy, PgBouncer, Neon serverless, Prisma Accelerate) multiplexes many serverless connections through fewer database connections.

---

## Cost Optimization Reference

| Strategy | Savings | Tradeoff |
|---|---|---|
| Right-size memory | 20-40% | Requires benchmarking |
| ARM64 (Graviton) | 20% | Minor compatibility concerns |
| Provisioned concurrency (vs over-provisioned servers) | 50-70% vs always-on | Higher latency on scale-up |
| Reserved concurrency | Prevents runaway costs | Limits throughput |
| Batch processing (SQS batch size) | 50-80% | Higher latency |
| Tiered storage (S3 lifecycle) | 30-60% | Access latency for cold tiers |

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|---|---|---|
| Opening DB connection per invocation | Exhausts connection pool | Module-level connection reuse + RDS Proxy |
| Bundling entire `node_modules` | Massive cold start (5-10s) | Tree-shake with esbuild, external AWS SDK |
| Storing state in global variables | Lost between invocations (unreliable) | Use DynamoDB, Redis, or S3 for state |
| 15-minute timeout for API handlers | User waiting 15 minutes? | 30s for APIs, use Step Functions for long tasks |
| No concurrency limits | Runaway costs, downstream overload | Set reserved concurrency per function |
| Synchronous fan-out | Slow, timeout risk | Use SQS/SNS for fan-out, process async |
| `console.log` without structure | Unsearchable in CloudWatch | Structured JSON logging with correlation IDs |

---

## Checklist

- [ ] Bundle size minimized (esbuild tree-shaking, external AWS SDK)
- [ ] Database connections pooled (RDS Proxy, Neon, Prisma Accelerate)
- [ ] Cold start measured and acceptable for the use case
- [ ] Provisioned concurrency configured for latency-sensitive paths
- [ ] Memory size benchmarked and right-sized
- [ ] SQS partial batch failure reporting enabled
- [ ] Dead letter queues configured for async event sources
- [ ] Reserved concurrency set to prevent runaway costs
- [ ] Structured logging with request/correlation IDs
- [ ] Timeout set appropriately (30s for APIs, longer for batch)
- [ ] Environment variables for all configuration (no hardcoded values)
- [ ] ARM64/Graviton runtime selected for cost savings

---

## Related Resources

- **Skills:** `event-driven-architecture` (SQS/SNS patterns), `monitoring-observability` (Lambda tracing)
- **Skills:** `performance-engineering` (cold start impact on latency)
- **Rules:** `rules/stacks/python.md` (Python Lambda patterns)
