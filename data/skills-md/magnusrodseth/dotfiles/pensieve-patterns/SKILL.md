---
name: pensieve-patterns
description: Next.js AI chat patterns - GitHub API integration, shimmer loading states, @ mention autocomplete, PWA setup, Vercel deployment. Use for AI chat apps with vault/note integrations.
license: MIT
compatibility: opencode
---

# Pensieve Patterns

Reusable patterns from the Pensieve AI chat application.

## 1. GitHub Contents API for Note Search

Fetch markdown files from a private GitHub repo without cloning:

```typescript
// lib/github/api.ts
const GITHUB_API_BASE = "https://api.github.com";

async function fetchWithAuth(url: string): Promise<Response> {
  const token = process.env.GITHUB_TOKEN;
  const headers: HeadersInit = {
    Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
  };
  if (token) headers.Authorization = `Bearer ${token}`;
  return fetch(url, { headers, cache: "no-store" });
}

async function listDirectoryContents(owner: string, repo: string, path = "", branch = "main") {
  const encodedPath = path ? `/${encodeURIComponent(path)}` : "";
  const url = `${GITHUB_API_BASE}/repos/${owner}/${repo}/contents${encodedPath}?ref=${branch}`;
  const response = await fetchWithAuth(url);
  if (!response.ok) throw new Error(`GitHub API error: ${response.status}`);
  return response.json();
}

// Recursively fetch all .md files
export async function getMarkdownFiles(): Promise<{ path: string; title: string }[]> {
  const repoPath = process.env.GITHUB_REPO; // "owner/repo"
  const [owner, repo] = repoPath!.split("/");
  return getAllMarkdownFilesRecursive(owner, repo);
}
```

## 2. @ Mention Popup with Fuzzy Search

Custom popup positioned above the @ symbol:

```typescript
// Key features:
// - Positioned above @ using caret coordinates calculation
// - Fuzzy search with fuse.js
// - Keyboard navigation (arrows, enter, escape)
// - Backspace on empty closes popup and removes @

interface NoteMentionPopupProps {
  notes: Note[];
  onSelect: (note: Note) => void;
  onClose: () => void;
  onBackspaceEmpty: () => void;  // Remove @ and close
  inputRef: RefObject<HTMLTextAreaElement>;
  text: string;
  cursorPosition: number;
}

// Position calculation
const getCaretCoordinates = (element: HTMLTextAreaElement, position: number) => {
  // Create mirror div, copy styles, measure span position
  // Returns { top, left } relative to textarea
};
```

## 3. Shimmer Loading Indicator

Replace spinners with animated shimmer text:

```typescript
// components/ai-elements/thinking-indicator.tsx
import { Shimmer } from "./shimmer";
import { BrainIcon } from "lucide-react";

export function ThinkingIndicator({ message = "Thinking..." }) {
  return (
    <div className="flex items-center gap-2 text-muted-foreground text-sm py-2">
      <BrainIcon className="size-4 animate-pulse" />
      <Shimmer duration={1.5}>{message}</Shimmer>
    </div>
  );
}

// Usage in chat
{status === "submitted" && <ThinkingIndicator />}
```

## 4. Dark Mode Only Setup

Force dark mode in Next.js:

```tsx
// app/layout.tsx
<html lang="en" className="dark">

// globals.css - define .dark selector with CSS variables
.dark {
  --background: oklch(0.2478 0 0);
  --foreground: oklch(0.9851 0 0);
  // ... other variables
}
```

## 5. PWA Icons from Single Source

Generate all icons from one source image:

```bash
# Using macOS sips
sips -z 512 512 logo.png --out icon-512.png
sips -z 192 192 logo.png --out icon-192.png
sips -z 180 180 logo.png --out apple-touch-icon.png

# Favicon with ImageMagick
sips -z 32 32 logo.png --out favicon-32.png
sips -z 16 16 logo.png --out favicon-16.png
magick favicon-16.png favicon-32.png favicon.ico
```

Place in:
- `/public/` - icon-192.png, icon-512.png, apple-touch-icon.png, logo.png
- `/src/app/` - favicon.ico (Next.js App Router convention)

## 6. Vercel Env Vars from .env.local

Push local env to Vercel production:

```bash
# Link project
vercel link

# Add each variable
source .env.local
echo "$SESSION_SECRET" | vercel env add SESSION_SECRET production
echo "$GITHUB_TOKEN" | vercel env add GITHUB_TOKEN production
# ... repeat for each var

# Update existing
vercel env rm VAR_NAME production -y
echo "$NEW_VALUE" | vercel env add VAR_NAME production

# Verify
vercel env ls
```

## 7. AI SDK 6 Chat with Tools

```typescript
// app/api/chat/route.ts
import { streamText, tool } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

const vaultTools = {
  search: tool({
    description: "Search vault for content",
    inputSchema: z.object({ query: z.string() }),
    execute: async ({ query }) => searchVault(query),
  }),
};

export async function POST(req: Request) {
  const { messages } = await req.json();
  const result = streamText({
    model: anthropic("claude-sonnet-4-20250514"),
    messages: await convertToModelMessages(messages),
    tools: vaultTools,
    stopWhen: stepCountIs(5),
  });
  return result.toUIMessageStreamResponse({ sendReasoning: true });
}
```

## 8. Dexie.js for Client-Side Sessions

```typescript
// lib/db/dexie.ts
const db = new Dexie("Pensieve");
db.version(1).stores({
  sessions: "id, createdAt, updatedAt",
  messages: "id, sessionId, createdAt",
});

// lib/db/hooks.ts
export function useSessions() {
  return useLiveQuery(() => db.sessions.orderBy("updatedAt").reverse().toArray());
}

export async function saveMessage(sessionId: string, message: Message) {
  await db.messages.add({ ...message, id: nanoid(), sessionId, createdAt: new Date() });
  await db.sessions.update(sessionId, { updatedAt: new Date() });
}
```
