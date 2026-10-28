---
name: gpt-image-playground
description: AI coding agent skill for GPT Image Playground — a React/TypeScript web app for OpenAI image generation and editing using gpt-image-1 and related APIs.
triggers:
  - set up gpt image playground
  - add image generation to my app
  - configure openai image editing tool
  - deploy gpt image playground with docker
  - integrate gpt-image-2 api in react
  - build image generation ui with openai
  - use responses api for image generation
  - customize gpt image playground settings
---

# GPT Image Playground

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A React 19 + TypeScript + Vite web application for generating and editing images via OpenAI's Images API (`/v1/images`) or Responses API (`/v1/responses`). Features a responsive UI with waterfall task cards, IndexedDB local storage, PWA support, bulk selection, history management, and ZIP export/import.

---

## What It Does

- **Text-to-image**: Generate images from prompts via `images/generations` or `responses` with `image_generation` tool
- **Reference image editing**: Upload up to 16 reference images, call `images/edits` or multimodal Responses API
- **Smart size selector**: Auto-calculates resolutions for 1K/2K/4K at common aspect ratios; custom sizes auto-snapped to 16px multiples, max 3840px, max ratio 3:1, pixel range 655360–8294400
- **Parameter control**: Quality (low/medium/high), format (PNG/JPEG/WebP), compression, moderation level
- **History**: IndexedDB storage with SHA-256 image deduplication, bulk ops, favorites, search/filter
- **Data portability**: ZIP export/import with raw image files + `manifest.json`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | React 19 + TypeScript |
| Build | Vite |
| Styling | Tailwind CSS 3 |
| State | Zustand |
| Storage | Browser IndexedDB API |

---

## Installation & Setup

### Prerequisites

- Node.js 18+
- npm

### Clone and Run Locally

```bash
git clone https://github.com/CookSleep/gpt_image_playground.git
cd gpt_image_playground
npm install
npm run dev
# Visit http://localhost:5173
```

### Environment Variables

Create `.env.local` in the project root:

```bash
# Optional: pre-fill default API URL at build time
VITE_DEFAULT_API_URL=https://api.openai.com/v1
```

### Build for Production

```bash
npm run build
# Output in dist/ — deploy to any static file server
```

### Docker

```bash
# Single container
docker run -d -p 8080:80 \
  -e API_URL=https://api.openai.com/v1 \
  ghcr.io/cooksleep/gpt_image_playground:latest

# Docker Compose
cat > docker-compose.yml << 'EOF'
services:
  gpt-image-playground:
    image: ghcr.io/cooksleep/gpt_image_playground:latest
    environment:
      - API_URL=https://api.openai.com/v1
    ports:
      - "8080:80"
    restart: unless-stopped
EOF
docker compose up -d
```

Update to latest:
```bash
docker compose pull && docker compose up -d
```

---

## Vercel One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FCookSleep%2Fgpt_image_playground&project-name=gpt-image-playground&repository-name=gpt-image-playground)

Add environment variable in **Settings → Environment Variables**:

```
VITE_DEFAULT_API_URL=https://api.openai.com/v1
```

---

## API Configuration

### In-App Settings

Open settings (top-right gear icon) and configure:

| Field | Images API | Responses API |
|-------|-----------|---------------|
| Endpoint | `/v1/images/generations`, `/v1/images/edits` | `/v1/responses` |
| Model example | `gpt-image-1` | `gpt-4o`, `gpt-5.5` |

### URL Query Parameters (Deep-link Config)

Pre-fill settings via URL — useful for bookmarks or sharing:

```
https://gpt-image-playground.cooksleep.dev?apiUrl=https://your-proxy.com&apiKey=sk-xxxx
https://cooksleep.github.io/gpt_image_playground?apiUrl=https://your-proxy.com&apiKey=sk-xxxx
```

Parameters:
- `apiUrl` — API base URL
- `apiKey` — OpenAI API key

---

## Local Development Proxy (CORS Bypass)

When your API endpoint doesn't allow browser CORS, use the Vite dev proxy:

```bash
cp dev-proxy.config.example.json dev-proxy.config.json
```

Edit `dev-proxy.config.json`:

```json
{
  "enabled": true,
  "prefix": "/api-proxy",
  "target": "http://127.0.0.1:3000",
  "changeOrigin": true,
  "secure": false
}
```

Request flow:
```
Browser → http://localhost:5173/api-proxy/v1/images/generations
       → Vite proxy forwards to →
         http://127.0.0.1:3000/v1/images/generations
```

**Note**: Proxy only works with `npm run dev`. Not included in production builds.

Set `API URL` in the app settings to match `target`. The app rewrites matching requests to use the proxy prefix.

> If `target` or `API URL` already includes `/v1`, the path won't be duplicated — requests become `/api-proxy/responses` not `/api-proxy/v1/responses`.

---

## Key Source Code Patterns

### Project Structure

```
src/
├── components/          # React UI components
├── hooks/               # Custom React hooks
├── store/               # Zustand state stores
├── utils/               # Helpers (IndexedDB, image processing, etc.)
├── types/               # TypeScript type definitions
└── main.tsx             # App entry point
```

### Using the Images API Directly (TypeScript)

```typescript
// Pattern matching how the app calls OpenAI Images API
async function generateImage(params: {
  prompt: string;
  model: string;
  size: string;
  quality: "low" | "medium" | "high";
  n: number;
  outputFormat: "png" | "jpeg" | "webp";
  outputCompression?: number;
  apiKey: string;
  apiUrl: string;
}) {
  const response = await fetch(`${params.apiUrl}/images/generations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${params.apiKey}`,
    },
    body: JSON.stringify({
      model: params.model,
      prompt: params.prompt,
      n: params.n,
      size: params.size,
      quality: params.quality,
      output_format: params.outputFormat,
      ...(params.outputFormat !== "png" && {
        output_compression: params.outputCompression,
      }),
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error?.message ?? "Generation failed");
  }

  return response.json();
}
```

### Using the Images Edit API with Reference Images

```typescript
async function editImage(params: {
  prompt: string;
  images: File[];
  model: string;
  size: string;
  quality: "low" | "medium" | "high";
  n: number;
  apiKey: string;
  apiUrl: string;
}) {
  const formData = new FormData();
  formData.append("model", params.model);
  formData.append("prompt", params.prompt);
  formData.append("n", String(params.n));
  formData.append("size", params.size);
  formData.append("quality", params.quality);

  // Up to 16 reference images
  params.images.forEach((file) => {
    formData.append("image[]", file);
  });

  const response = await fetch(`${params.apiUrl}/images/edits`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${params.apiKey}`,
      // Do NOT set Content-Type — browser sets multipart boundary automatically
    },
    body: formData,
  });

  return response.json();
}
```

### Using Responses API with image_generation Tool

```typescript
async function generateViaResponsesAPI(params: {
  prompt: string;
  model: string;
  size: string;
  quality: "low" | "medium" | "high";
  apiKey: string;
  apiUrl: string;
}) {
  const response = await fetch(`${params.apiUrl}/responses`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${params.apiKey}`,
    },
    body: JSON.stringify({
      model: params.model,
      input: params.prompt,
      tools: [
        {
          type: "image_generation",
          size: params.size,
          quality: params.quality,
        },
      ],
    }),
  });

  return response.json();
}
```

### Custom Size Validation (matches app logic)

```typescript
function sanitizeImageSize(width: number, height: number): {
  width: number;
  height: number;
} {
  // Snap to 16px multiples
  let w = Math.round(width / 16) * 16;
  let h = Math.round(height / 16) * 16;

  // Max edge 3840px
  const maxEdge = 3840;
  if (w > maxEdge) w = maxEdge;
  if (h > maxEdge) h = maxEdge;

  // Aspect ratio must not exceed 3:1
  if (w / h > 3) h = Math.ceil(w / 3 / 16) * 16;
  if (h / w > 3) w = Math.ceil(h / 3 / 16) * 16;

  // Total pixels: 655360 to 8294400
  const pixels = w * h;
  const minPixels = 655360;
  const maxPixels = 8294400;

  if (pixels < minPixels) {
    const scale = Math.sqrt(minPixels / pixels);
    w = Math.ceil((w * scale) / 16) * 16;
    h = Math.ceil((h * scale) / 16) * 16;
  }

  if (pixels > maxPixels) {
    const scale = Math.sqrt(maxPixels / pixels);
    w = Math.floor((w * scale) / 16) * 16;
    h = Math.floor((h * scale) / 16) * 16;
  }

  return { width: w, height: h };
}
```

### Adding IndexedDB Storage (pattern used by the app)

```typescript
import { openDB, IDBPDatabase } from "idb"; // App uses native IDB API directly

const DB_NAME = "gpt-image-playground";
const DB_VERSION = 1;

async function initDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      // Tasks store
      if (!db.objectStoreNames.contains("tasks")) {
        const tasks = db.createObjectStore("tasks", { keyPath: "id" });
        tasks.createIndex("createdAt", "createdAt");
        tasks.createIndex("status", "status");
        tasks.createIndex("favorited", "favorited");
      }
      // Images store with SHA-256 hash deduplication
      if (!db.objectStoreNames.contains("images")) {
        db.createObjectStore("images", { keyPath: "hash" });
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}
```

### Zustand Store Pattern (matching app architecture)

```typescript
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SettingsStore {
  apiKey: string;
  apiUrl: string;
  apiMode: "images" | "responses";
  model: string;
  setApiKey: (key: string) => void;
  setApiUrl: (url: string) => void;
  setApiMode: (mode: "images" | "responses") => void;
  setModel: (model: string) => void;
}

const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      apiKey: "",
      apiUrl: "https://api.openai.com/v1",
      apiMode: "images",
      model: "gpt-image-1",
      setApiKey: (apiKey) => set({ apiKey }),
      setApiUrl: (apiUrl) => set({ apiUrl }),
      setApiMode: (apiMode) => set({ apiMode }),
      setModel: (model) => set({ model }),
    }),
    { name: "gpt-image-settings" }
  )
);
```

---

## Common Workflows

### 1. Fork & Customize for a Specific Use Case

```bash
git clone https://github.com/CookSleep/gpt_image_playground.git
cd gpt_image_playground

# Set default API
echo "VITE_DEFAULT_API_URL=https://your-proxy.com/v1" > .env.local

npm install && npm run dev
```

### 2. Add a Custom Preset Size

In the size selector component, add to the presets array:

```typescript
const SIZE_PRESETS = [
  // existing presets...
  {
    label: "Banner 16:5",
    ratio: { w: 16, h: 5 },
    resolutions: {
      "1K": { width: 1024, height: 320 },
      "2K": { width: 2048, height: 640 },
    },
  },
];
```

### 3. Extend Task History with Custom Metadata

```typescript
interface TaskRecord {
  id: string;
  createdAt: number;
  prompt: string;
  status: "pending" | "success" | "failed";
  favorited: boolean;
  parameters: {
    model: string;
    size: string;
    quality: string;
    n: number;
    outputFormat: string;
  };
  // Add custom fields:
  tags?: string[];
  projectId?: string;
  outputImages: string[]; // SHA-256 hashes referencing images store
}
```

### 4. Export/Import Data Programmatically

The app exports a ZIP containing:
- Raw image files (not base64)
- `manifest.json` with task records and image metadata

```typescript
// manifest.json structure
interface ExportManifest {
  version: string;
  exportedAt: string;
  tasks: TaskRecord[];
  images: {
    hash: string;
    filename: string;
    mimeType: string;
    size: number;
  }[];
}
```

---

## Troubleshooting

### CORS Errors in Browser

**Cause**: API endpoint doesn't allow browser cross-origin requests.

**Fix (dev)**: Enable local proxy in `dev-proxy.config.json` (see above).

**Fix (production)**: Use a server-side proxy (Vercel Functions, Cloudflare Workers, or Nginx `proxy_pass`).

### `.dev` Domain HTTPS Requirement

The `gpt-image-playground.cooksleep.dev` deployment requires all resources to be HTTPS. If your API is HTTP-only, use the GitHub Pages version:
```
https://cooksleep.github.io/gpt_image_playground
```

### Custom Size Not Accepted by API

Ensure size passes validation:
- Width and height are multiples of 16
- Neither dimension exceeds 3840px
- Aspect ratio ≤ 3:1
- Total pixels between 655,360 and 8,294,400

Use the `sanitizeImageSize` function above to auto-correct.

### Responses API vs Images API

| Scenario | Use |
|----------|-----|
| Direct image generation | Images API + `gpt-image-1` |
| Codex CLI-derived APIs | Responses API |
| Text model + image tool | Responses API + text model (e.g. `gpt-4o`) |
| `images/edits` for multi-image input | Images API only |

### Docker: API URL Not Pre-filled

Ensure you pass the env variable at runtime (not build time):
```bash
docker run -e API_URL=https://api.openai.com/v1 ...
```
The container's entrypoint injects `API_URL` into the Nginx-served static files at startup.

### IndexedDB Orphaned Images

The app automatically cleans up orphaned image blobs on startup. If storage grows unexpectedly, use the in-app export → clear data → reimport workflow, or manually clear IndexedDB via DevTools → Application → IndexedDB.

---

## Live Deployments

| Version | URL |
|---------|-----|
| Vercel (HTTPS only) | https://gpt-image-playground.cooksleep.dev |
| GitHub Pages | https://cooksleep.github.io/gpt_image_playground |
