---
name: railway-storage
description: Configure and use Railway's S3-compatible storage buckets. Use when implementing file uploads with Railway storage, setting up S3 clients for Railway, or troubleshooting Railway bucket access issues.
---

# Railway S3-Compatible Storage

Railway provides S3-compatible storage buckets that work with standard AWS SDK. However, there are critical differences from AWS S3.

## Critical: Private Buckets Only

**Railway buckets are private by default and do not support public buckets.** The `ACL: "public-read"` setting is ignored.

To serve files publicly:
1. **Proxy endpoint** (recommended) - API route that fetches from S3 and serves to client
2. **Presigned URLs** - Generate time-limited signed URLs for direct access

## Environment Variables

Railway auto-injects these when you link a storage bucket to your service. Use these exact names:

```bash
AWS_ENDPOINT_URL=https://storage.railway.app
AWS_DEFAULT_REGION=auto
AWS_S3_BUCKET_NAME=your-bucket-name
AWS_ACCESS_KEY_ID=tid_xxx
AWS_SECRET_ACCESS_KEY=tsec_xxx
```

**Important:** Railway uses `AWS_*` prefixed names by default. Do NOT use `S3_*` prefixes as they won't match Railway's injected variables.

## S3 Client Setup

Use lazy initialization to avoid build-time errors (env vars unavailable during Docker builds):

```typescript
import { S3Client, PutObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";

let s3Client: S3Client | null = null;

function getS3Client(): S3Client {
  if (!s3Client) {
    s3Client = new S3Client({
      endpoint: process.env.AWS_ENDPOINT_URL,
      region: process.env.AWS_DEFAULT_REGION ?? "auto",
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
      },
      forcePathStyle: true, // Required for Railway
    });
  }
  return s3Client;
}
```

**Key points:**
- `forcePathStyle: true` is required
- Never access `process.env` at module level
- Region is typically `"auto"`

## Upload Implementation

```typescript
export async function uploadToS3(key: string, body: Buffer, contentType: string): Promise<string> {
  const client = getS3Client();
  const bucket = process.env.S3_BUCKET_NAME!;

  await client.send(new PutObjectCommand({
    Bucket: bucket,
    Key: key,
    Body: body,
    ContentType: contentType,
    // Note: ACL is ignored - Railway buckets are always private
  }));

  // Return proxy URL (not direct S3 URL)
  return `/uploads/${key}`;
}
```

## Proxy Endpoint Pattern

Create an API route to serve files from S3:

```typescript
// src/app/api/uploads/[...path]/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  const key = path.join("/");

  const result = await getS3Object(key);
  if (!result) {
    return NextResponse.json({ error: "File not found" }, { status: 404 });
  }

  return new NextResponse(result.body, {
    headers: {
      "Content-Type": result.contentType,
      "Content-Length": result.contentLength.toString(),
      "Cache-Control": "public, max-age=31536000, immutable",
    },
  });
}
```

Helper to read from S3:

```typescript
export async function getS3Object(key: string) {
  const client = getS3Client();
  const response = await client.send(
    new GetObjectCommand({ Bucket: process.env.AWS_S3_BUCKET_NAME!, Key: key })
  );
  if (!response.Body) return null;

  return {
    body: response.Body.transformToWebStream(),
    contentType: response.ContentType || "application/octet-stream",
    contentLength: response.ContentLength || 0,
  };
}
```

## Next.js Rewrite Rule

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  async rewrites() {
    return [{ source: "/uploads/:path*", destination: "/api/uploads/:path*" }];
  },
};
```

## Dependencies

```bash
bun add @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Files upload but return 403 | Railway ignores ACL | Use proxy endpoint |
| Build fails with missing env vars | S3 client at module level | Use lazy initialization |
| "Invalid endpoint" error | Missing forcePathStyle | Add `forcePathStyle: true` |
| Images don't update after upload | Browser/React Query caching | Add `invalidateQueries()` |

## URL Format

Store proxy URLs in database, not direct S3 URLs:
- **Correct:** `/uploads/{teamId}/avatar/{filename}`
- **Wrong:** `https://storage.railway.app/bucket/{key}`
