---
name: r2-storage
description: S3-compatible object storage for files, images, and large data. Load when handling file uploads, storing images/videos/documents, generating presigned URLs, using multipart uploads for large files, migrating from S3, or serving static assets from buckets.
---

# R2 Object Storage

Store and retrieve objects at scale using Cloudflare's S3-compatible object storage.

## When to Use

- File uploads (images, videos, documents)
- AI assets and model artifacts
- Image and media asset storage
- Structured data (JSON, CSV, logs)
- User-facing uploads and downloads
- Static asset hosting
- Backup and archival storage
- S3-compatible workflows with existing tools

## FIRST: Create R2 Bucket

```bash
# Create bucket
wrangler r2 bucket create my-bucket

# Create with location hint
wrangler r2 bucket create my-bucket --location wnam

# List buckets
wrangler r2 bucket list
```

## Quick Reference

| Operation | API |
|-----------|-----|
| Upload object | `await bucket.put(key, data, { httpMetadata })` |
| Download object | `const obj = await bucket.get(key); const data = await obj.text()` |
| Delete object | `await bucket.delete(key)` |
| List objects | `const list = await bucket.list({ prefix, limit })` |
| Get metadata | `const obj = await bucket.head(key)` |
| Multipart upload | `const upload = await bucket.createMultipartUpload(key)` |
| Generate signed URL | Use presigned URL patterns with R2's S3 compatibility |

## Wrangler Configuration

```jsonc
// wrangler.jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01",
  "r2_buckets": [
    {
      "binding": "BUCKET",
      "bucket_name": "my-bucket"
    }
  ]
}
```

**TypeScript Types** (run `wrangler types` to generate):

```typescript
export interface Env {
  BUCKET: R2Bucket;
}
```

## Basic Upload and Download

```typescript
import { R2Bucket } from "@cloudflare/workers-types";

export interface Env {
  BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1); // Remove leading /

    // Upload
    if (request.method === "PUT") {
      await env.BUCKET.put(key, request.body, {
        httpMetadata: {
          contentType: request.headers.get("content-type") || "application/octet-stream",
        },
      });
      return new Response("Uploaded", { status: 201 });
    }

    // Download
    if (request.method === "GET") {
      const object = await env.BUCKET.get(key);
      
      if (!object) {
        return new Response("Not found", { status: 404 });
      }

      return new Response(object.body, {
        headers: {
          "Content-Type": object.httpMetadata?.contentType || "application/octet-stream",
          "ETag": object.httpEtag,
          "Cache-Control": object.httpMetadata?.cacheControl || "public, max-age=3600",
        },
      });
    }

    // Delete
    if (request.method === "DELETE") {
      await env.BUCKET.delete(key);
      return new Response("Deleted", { status: 204 });
    }

    return new Response("Method not allowed", { status: 405 });
  },
};
```

## Multipart Form Upload Handler

Handle file uploads from HTML forms or multipart requests.

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    const formData = await request.formData();
    const file = formData.get("file") as File;

    if (!file) {
      return new Response("No file provided", { status: 400 });
    }

    // Generate unique key
    const key = `uploads/${crypto.randomUUID()}-${file.name}`;

    // Upload to R2
    await env.BUCKET.put(key, file.stream(), {
      httpMetadata: {
        contentType: file.type,
      },
      customMetadata: {
        originalName: file.name,
        uploadedAt: new Date().toISOString(),
      },
    });

    return Response.json({
      success: true,
      key,
      url: `/files/${key}`,
    });
  },
};
```

## List Objects with Pagination

```typescript
async function listAllObjects(
  bucket: R2Bucket,
  prefix: string = ""
): Promise<R2Object[]> {
  const objects: R2Object[] = [];
  let cursor: string | undefined;

  do {
    const listed = await bucket.list({
      prefix,
      cursor,
      limit: 1000,
    });

    objects.push(...listed.objects);
    cursor = listed.truncated ? listed.cursor : undefined;
  } while (cursor);

  return objects;
}

// Usage
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const prefix = url.searchParams.get("prefix") || "";

    const objects = await listAllObjects(env.BUCKET, prefix);

    return Response.json({
      count: objects.length,
      objects: objects.map((obj) => ({
        key: obj.key,
        size: obj.size,
        uploaded: obj.uploaded,
      })),
    });
  },
};
```

## Conditional Operations (ETags)

Use ETags for conditional reads/writes to prevent race conditions.

```typescript
// Conditional write (only if not modified)
const existingObject = await env.BUCKET.head("config.json");

if (existingObject) {
  // Update only if ETag matches
  await env.BUCKET.put("config.json", newData, {
    httpMetadata: {
      contentType: "application/json",
    },
    onlyIf: {
      etagMatches: existingObject.httpEtag,
    },
  });
}

// Conditional read (If-None-Match)
const object = await env.BUCKET.get("image.jpg", {
  onlyIf: {
    etagDoesNotMatch: cachedEtag,
  },
});

if (object === null) {
  // Object not modified - return 304
  return new Response(null, {
    status: 304,
    headers: { "ETag": cachedEtag },
  });
}
```

## Custom Metadata

Store application-specific metadata alongside objects.

```typescript
// Store with custom metadata
await env.BUCKET.put("document.pdf", pdfData, {
  httpMetadata: {
    contentType: "application/pdf",
  },
  customMetadata: {
    userId: "user-123",
    documentType: "invoice",
    version: "2",
    tags: "finance,2024",
  },
});

// Read metadata without downloading body
const object = await env.BUCKET.head("document.pdf");
console.log(object.customMetadata?.userId); // "user-123"
```

## Range Requests (Partial Downloads)

Efficiently download portions of large files.

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const key = new URL(request.url).pathname.slice(1);
    const rangeHeader = request.headers.get("range");

    if (rangeHeader) {
      // Parse range: "bytes=0-1023"
      const match = rangeHeader.match(/bytes=(\d+)-(\d*)/);
      if (match) {
        const start = parseInt(match[1], 10);
        const end = match[2] ? parseInt(match[2], 10) : undefined;

        const object = await env.BUCKET.get(key, {
          range: { offset: start, length: end ? end - start + 1 : undefined },
        });

        if (!object) {
          return new Response("Not found", { status: 404 });
        }

        return new Response(object.body, {
          status: 206,
          headers: {
            "Content-Type": object.httpMetadata?.contentType || "application/octet-stream",
            "Content-Range": `bytes ${start}-${end || object.size - 1}/${object.size}`,
            "Content-Length": object.size.toString(),
          },
        });
      }
    }

    // Regular full download
    const object = await env.BUCKET.get(key);
    if (!object) {
      return new Response("Not found", { status: 404 });
    }

    return new Response(object.body, {
      headers: {
        "Content-Type": object.httpMetadata?.contentType || "application/octet-stream",
      },
    });
  },
};
```

## AWS SDK Integration (S3 Compatible)

R2 is fully compatible with the AWS S3 API. Use the official AWS SDK v3.

**Install dependencies:**

```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

**wrangler.jsonc** (add Node.js compatibility):

```jsonc
{
  "compatibility_flags": ["nodejs_compat_v2"],
  "r2_buckets": [
    { "binding": "BUCKET", "bucket_name": "my-bucket" }
  ]
}
```

**Using AWS SDK:**

```typescript
import { S3Client, PutObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

export interface Env {
  BUCKET: R2Bucket;
  R2_ACCESS_KEY_ID: string;
  R2_SECRET_ACCESS_KEY: string;
  R2_ACCOUNT_ID: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Create S3 client
    const s3 = new S3Client({
      region: "auto",
      endpoint: `https://${env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
      credentials: {
        accessKeyId: env.R2_ACCESS_KEY_ID,
        secretAccessKey: env.R2_SECRET_ACCESS_KEY,
      },
    });

    // Upload using S3 API
    await s3.send(
      new PutObjectCommand({
        Bucket: "my-bucket",
        Key: "file.txt",
        Body: "Hello R2",
        ContentType: "text/plain",
      })
    );

    // Generate presigned URL (valid for 1 hour)
    const command = new GetObjectCommand({
      Bucket: "my-bucket",
      Key: "file.txt",
    });
    const signedUrl = await getSignedUrl(s3, command, { expiresIn: 3600 });

    return Response.json({ signedUrl });
  },
};
```

**Note**: Using the native R2Bucket binding is more efficient than AWS SDK for basic operations. Use AWS SDK when you need presigned URLs or have existing S3 tooling.

## Presigned URLs for Direct Uploads

Allow clients to upload directly to R2 without going through your Worker.

```typescript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

export interface Env {
  R2_ACCESS_KEY_ID: string;
  R2_SECRET_ACCESS_KEY: string;
  R2_ACCOUNT_ID: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Generate presigned upload URL
    if (url.pathname === "/upload-url") {
      const filename = url.searchParams.get("filename");
      if (!filename) {
        return new Response("Missing filename", { status: 400 });
      }

      const s3 = new S3Client({
        region: "auto",
        endpoint: `https://${env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
        credentials: {
          accessKeyId: env.R2_ACCESS_KEY_ID,
          secretAccessKey: env.R2_SECRET_ACCESS_KEY,
        },
      });

      const key = `uploads/${crypto.randomUUID()}-${filename}`;
      const command = new PutObjectCommand({
        Bucket: "my-bucket",
        Key: key,
      });

      const signedUrl = await getSignedUrl(s3, command, { expiresIn: 300 }); // 5 minutes

      return Response.json({
        uploadUrl: signedUrl,
        key,
      });
    }

    return new Response("Not found", { status: 404 });
  },
};
```

**Client-side usage:**

```javascript
// 1. Get presigned URL from your Worker
const response = await fetch("/upload-url?filename=photo.jpg");
const { uploadUrl, key } = await response.json();

// 2. Upload file directly to R2
const file = document.querySelector('input[type="file"]').files[0];
await fetch(uploadUrl, {
  method: "PUT",
  body: file,
  headers: {
    "Content-Type": file.type,
  },
});

// 3. File is now available at key in R2
```

## Multipart Upload for Large Files

For files larger than 100MB, use multipart uploads:

```typescript
// Initiate multipart upload
const multipartUpload = await env.BUCKET.createMultipartUpload(key, {
  httpMetadata: { contentType: "application/zip" }
});

const uploadedParts: R2UploadedPart[] = [];
const chunkSize = 10 * 1024 * 1024; // 10MB chunks

// Upload parts
for (let offset = 0; offset < data.byteLength; offset += chunkSize) {
  const chunk = data.slice(offset, Math.min(offset + chunkSize, data.byteLength));
  const part = await multipartUpload.uploadPart(partNumber++, chunk);
  uploadedParts.push(part);
}

// Complete upload
const object = await multipartUpload.complete(uploadedParts);
```

See [references/operations.md](references/operations.md) for complete multipart upload patterns

## Detailed References

- **[references/operations.md](references/operations.md)** - Complete API reference, conditional operations, streaming, error handling
- **[references/s3-compat.md](references/s3-compat.md)** - S3 API compatibility, AWS SDK patterns, presigned URLs, migration guide
- **[references/limits.md](references/limits.md)** - Storage limits, rate limits, Workers integration limits, best practices
- **[references/testing.md](references/testing.md)** - Vitest integration, mocking R2, multipart uploads, test isolation

## Best Practices

1. **Set appropriate Content-Type**: Always specify `httpMetadata.contentType` for proper browser handling
2. **Use unique keys**: Prefix with UUIDs or timestamps to avoid collisions
3. **Leverage custom metadata**: Store searchable metadata without downloading objects
4. **Use ETags for consistency**: Implement conditional operations for race condition prevention
5. **Stream large uploads**: Use multipart uploads for files > 100MB
6. **Cache control headers**: Set appropriate `cacheControl` in httpMetadata
7. **Use presigned URLs for direct uploads**: Reduce Worker bandwidth and latency
8. **List with pagination**: Always handle truncated results when listing objects
9. **Use R2Bucket binding by default**: Only use AWS SDK when you need presigned URLs or S3-specific features
10. **Handle 404s gracefully**: `bucket.get()` returns `null` when object doesn't exist

## Common Patterns

See [references/operations.md](references/operations.md) for complete examples including:
- Image upload and optimization with metadata
- Structured data storage (JSON profiles)
- Backup and archival patterns
- Streaming large files
- Conditional operations with ETags
