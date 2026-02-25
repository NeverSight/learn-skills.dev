---
name: glb-compressor-server
description: HTTP server for compressing GLB/glTF 3D models via REST API and SSE streaming. Use when building web integrations, setting up a compression microservice, or adding real-time compression progress to a frontend.
license: MIT
compatibility: Requires Bun >= 1.3 or Node.js >= 18.17. Optional gltfpack binary for best compression.
---

# glb-compressor Server

HTTP compression server built on `Bun.serve()`. Provides synchronous and
streaming (SSE) compression endpoints with full CORS support.

## Starting the Server

```sh
# Production (from installed package)
glb-server

# Development (hot reload)
bun run dev

# Custom port
PORT=3000 bun run start
```

Default port: `8080` (override via `PORT` env var).

## Endpoints

### `GET /healthz`

Health check. Returns `200 ok`.

### `POST /compress`

Synchronous compression. Returns compressed GLB binary.

**Accepts:** `multipart/form-data` (field: `file`) or raw
`application/octet-stream`.

**Query params / form fields:**

- `preset` - Compression preset: `default`, `balanced`, `aggressive`, `max`
- `simplify` - Mesh simplification ratio `(0, 1)`, e.g. `0.5`

Form fields override query params when both are provided.

**Response headers:**

| Header                 | Description                        |
| ---------------------- | ---------------------------------- |
| `X-Request-ID`         | UUID tracking this request         |
| `X-Original-Size`      | Input file size in bytes           |
| `X-Compressed-Size`    | Output file size in bytes          |
| `X-Compression-Method` | `gltfpack` or `meshopt`            |
| `X-Compression-Ratio`  | Percentage reduction (e.g. `84.1`) |
| `Content-Disposition`  | Suggested download filename        |

**Example:**

```sh
# Multipart upload
curl -X POST -F "file=@model.glb" \
  "http://localhost:8080/compress?preset=aggressive" \
  -o compressed.glb

# Raw binary upload
curl -X POST --data-binary @model.glb \
  -H "Content-Type: application/octet-stream" \
  "http://localhost:8080/compress?preset=balanced" \
  -o compressed.glb
```

### `POST /compress-stream`

SSE streaming compression with real-time progress. **Multipart only.**

**Content-Type:** `text/event-stream`

**SSE events:**

| Event    | Data shape                                                                            |
| -------- | ------------------------------------------------------------------------------------- |
| `log`    | `{ message: string }`                                                                 |
| `result` | `{ requestId, filename, data (base64), originalSize, compressedSize, ratio, method }` |
| `error`  | `{ message, requestId, code }`                                                        |

Stream closes after `result` or `error` event.

**Example (JavaScript):**

```js
const form = new FormData();
form.append('file', glbFile);

const response = await fetch(
	'http://localhost:8080/compress-stream?preset=aggressive',
	{ method: 'POST', body: form },
);

const reader = response.body.getReader();
const decoder = new TextDecoder();

// Parse SSE events from the stream
while (true) {
	const { done, value } = await reader.read();
	if (done) break;
	const text = decoder.decode(value);
	// Parse "event: <type>\ndata: <json>\n\n" format
	console.log(text);
}
```

## Error Responses

All errors return structured JSON:

```json
{
	"error": { "code": "ERROR_CODE", "message": "Human-readable message" },
	"requestId": "uuid"
}
```

**Error codes:**

| Code                   | HTTP | Description                         |
| ---------------------- | ---- | ----------------------------------- |
| `NO_FILE_PROVIDED`     | 400  | No file in form data                |
| `INVALID_GLB`          | 400  | Failed GLB magic byte validation    |
| `FILE_TOO_LARGE`       | 413  | Exceeds 100 MB limit                |
| `INVALID_CONTENT_TYPE` | 415  | Non-multipart on streaming endpoint |
| `COMPRESSION_FAILED`   | 500  | Pipeline error during compression   |

## CORS

Full CORS enabled on all endpoints. Exposed headers: `X-Request-ID`,
`X-Original-Size`, `X-Compressed-Size`, `X-Compression-Method`,
`X-Compression-Ratio`.

## Limits

- **Max file size:** 100 MB
- **gltfpack timeout:** 60 seconds per file

## Architecture Notes

- `import.meta.main` guard: safe to import `server/main.ts` as a library without
  starting the server.
- Request ID (`X-Request-ID`) is generated per request and logged server-side.
- The `/compress-stream` endpoint sends the compressed GLB as base64 in the
  `result` SSE event (~33% larger than binary). For large files near the 100 MB
  limit, prefer `/compress`.
