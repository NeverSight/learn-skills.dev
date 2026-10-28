---
name: bouncer-feed-filter
description: AI-powered browser extension that filters unwanted posts from Twitter/X feeds using natural language rules and multiple AI backends
triggers:
  - add a filter to bouncer
  - configure bouncer ai backend
  - build the bouncer extension
  - filter twitter posts with ai
  - set up bouncer with openai
  - how does bouncer classify posts
  - integrate local model with bouncer
  - customize bouncer feed filtering
---

# Bouncer Feed Filter

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Bouncer is a browser extension (Chrome/Edge/iOS) that uses AI to filter unwanted posts from Twitter/X feeds in real time. Users define filters in plain language ("crypto", "engagement bait", "rage politics"), and Bouncer classifies and hides matching posts using AI models — local (WebGPU via WebLLM) or cloud (OpenAI, Gemini, Anthropic, OpenRouter, Imbue).

## Repository Structure

```
Bouncer/                  # Main extension source
  src/
    background/           # Service worker / background scripts
    content/              # Content scripts (Twitter DOM interaction)
    popup/                # Extension popup UI
    adapters/             # Site adapters (Twitter/X)
    models/               # AI backend integrations
    utils/                # Shared utilities
  icons/                  # Extension icons
  manifest.json           # Chrome extension manifest
  package.json
  tsconfig.json
```

## Installation & Build

### From Source (Chrome/Edge)

```bash
git clone https://github.com/imbue-ai/bouncer.git
cd bouncer/Bouncer
npm install
npm run build
```

Load in Chrome:
1. Go to `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked** → select `Bouncer/` folder
4. Navigate to `twitter.com` or `x.com`

### Development Build (watch mode)

```bash
cd Bouncer
npm run dev        # watch mode with hot rebuild
```

### Production Build

```bash
npm run build      # outputs to Bouncer/dist or inline
```

## AI Backend Configuration

Bouncer supports multiple providers. Configure via the extension popup Settings panel.

### Provider / Model Matrix

| Provider | Model IDs | Auth |
|----------|-----------|------|
| Local WebGPU | `Qwen3-4B`, `Qwen3.5-4B`, `Qwen3.5-4B Vision` | None |
| OpenAI | `GPT-5 Nano`, `gpt-oss-20b` | API key |
| Google Gemini | `2.5 Flash Lite`, `2.5 Flash`, `3 Flash Preview` | API key |
| Anthropic | `Claude Haiku 4.5` | API key |
| OpenRouter | `Nemotron Nano 12B VL`, `Ministral 3B` | Account token |
| Imbue | Default | None (built-in) |

API keys are stored in Chrome's `chrome.storage.local` — never hardcoded.

## Core Architecture

### 1. MutationObserver — Content Script

The content script watches the Twitter feed for new posts:

```typescript
// src/content/feedObserver.ts
const observer = new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    for (const node of mutation.addedNodes) {
      if (node instanceof HTMLElement) {
        const post = extractPost(node);
        if (post) classifyAndFilter(post);
      }
    }
  }
});

observer.observe(document.body, { childList: true, subtree: true });
```

### 2. Post Extraction — Twitter Adapter

```typescript
// src/adapters/twitter.ts
export interface ExtractedPost {
  id: string;
  text: string;
  authorHandle: string;
  imageUrls: string[];
  element: HTMLElement;
}

export function extractPost(element: HTMLElement): ExtractedPost | null {
  const article = element.querySelector('article[data-testid="tweet"]');
  if (!article) return null;

  const tweetText = article.querySelector('[data-testid="tweetText"]')?.textContent ?? '';
  const handle = article.querySelector('[data-testid="User-Name"] a')?.getAttribute('href') ?? '';
  const images = [...article.querySelectorAll('img[src*="pbs.twimg.com/media"]')]
    .map(img => (img as HTMLImageElement).src);

  return {
    id: article.closest('[data-testid]')?.getAttribute('data-testid') ?? crypto.randomUUID(),
    text: tweetText,
    authorHandle: handle.replace('/', ''),
    imageUrls: images,
    element: article as HTMLElement,
  };
}
```

### 3. Classification Request

```typescript
// src/models/classify.ts
export interface ClassificationResult {
  filtered: boolean;
  matchedCategory: string | null;
  reasoning: string;
}

export async function classifyPost(
  post: ExtractedPost,
  filters: string[],
  model: ModelConfig
): Promise<ClassificationResult> {
  const prompt = buildClassificationPrompt(post.text, filters, post.imageUrls);
  const response = await model.provider.complete(prompt);
  return parseClassificationResponse(response);
}

function buildClassificationPrompt(
  text: string,
  filters: string[],
  imageUrls: string[]
): string {
  return `You are a content filter. Given a social media post, determine if it matches any of the user's filter categories.

Filter categories: ${filters.map(f => `"${f}"`).join(', ')}

Post text:
${text}

${imageUrls.length > 0 ? `The post contains ${imageUrls.length} image(s).` : ''}

Respond with JSON:
{
  "filtered": boolean,
  "matchedCategory": "category name or null",
  "reasoning": "brief explanation"
}`;
}
```

### 4. Hiding Filtered Posts

```typescript
// src/content/filterUI.ts
export function hidePost(element: HTMLElement, reason: string): void {
  element.style.transition = 'opacity 0.3s ease-out';
  element.style.opacity = '0';
  setTimeout(() => {
    element.style.display = 'none';
    element.dataset.bouncerFiltered = 'true';
    element.dataset.bouncerReason = reason;
  }, 300);
}

export function showFilteredIndicator(count: number): void {
  const indicator = document.getElementById('bouncer-filtered-count');
  if (indicator) indicator.textContent = `${count} filtered`;
}
```

## Adding a New AI Provider

```typescript
// src/models/providers/myProvider.ts
import type { ModelProvider, CompletionRequest, CompletionResponse } from '../types';

export class MyProvider implements ModelProvider {
  private apiKey: string;
  private endpoint = 'https://api.myprovider.com/v1/chat/completions';

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  async complete(request: CompletionRequest): Promise<CompletionResponse> {
    const response = await fetch(this.endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: request.model,
        messages: [{ role: 'user', content: request.prompt }],
        max_tokens: 256,
      }),
    });

    const data = await response.json();
    return {
      text: data.choices[0].message.content,
      usage: data.usage,
    };
  }
}
```

Register it in the provider registry:

```typescript
// src/models/registry.ts
import { MyProvider } from './providers/myProvider';

export function createProvider(config: StoredConfig): ModelProvider {
  switch (config.provider) {
    case 'my-provider':
      return new MyProvider(config.apiKey);
    // ... other cases
  }
}
```

## Result Caching

Bouncer caches classification results so repeated posts don't trigger new inference calls:

```typescript
// src/utils/cache.ts
const CACHE_KEY = 'bouncer-post-cache';

export async function getCachedResult(postId: string): Promise<ClassificationResult | null> {
  const stored = await chrome.storage.local.get(CACHE_KEY);
  const cache = stored[CACHE_KEY] ?? {};
  return cache[postId] ?? null;
}

export async function cacheResult(postId: string, result: ClassificationResult): Promise<void> {
  const stored = await chrome.storage.local.get(CACHE_KEY);
  const cache = stored[CACHE_KEY] ?? {};
  cache[postId] = result;
  // Limit cache size
  const keys = Object.keys(cache);
  if (keys.length > 1000) delete cache[keys[0]];
  await chrome.storage.local.set({ [CACHE_KEY]: cache });
}
```

## Filter Management

Filters are stored and retrieved via `chrome.storage.sync`:

```typescript
// src/utils/filters.ts
export async function getFilters(): Promise<string[]> {
  const result = await chrome.storage.sync.get('bouncerFilters');
  return result.bouncerFilters ?? [];
}

export async function addFilter(topic: string): Promise<void> {
  const filters = await getFilters();
  if (!filters.includes(topic)) {
    await chrome.storage.sync.set({ bouncerFilters: [...filters, topic] });
  }
}

export async function removeFilter(topic: string): Promise<void> {
  const filters = await getFilters();
  await chrome.storage.sync.set({
    bouncerFilters: filters.filter(f => f !== topic),
  });
}
```

## Local WebGPU Models (WebLLM)

Local models run entirely in-browser via WebGPU — zero data sent externally:

```typescript
// src/models/providers/webllm.ts
import { CreateMLCEngine, type MLCEngine } from '@mlc-ai/web-llm';

let engine: MLCEngine | null = null;

export async function loadLocalModel(modelId: string, onProgress?: (p: number) => void): Promise<void> {
  engine = await CreateMLCEngine(modelId, {
    initProgressCallback: (report) => onProgress?.(report.progress),
  });
}

export async function localComplete(prompt: string): Promise<string> {
  if (!engine) throw new Error('Local model not loaded');
  const response = await engine.chat.completions.create({
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 256,
  });
  return response.choices[0].message.content ?? '';
}
```

## Chrome Extension Manifest Key Points

```json
{
  "manifest_version": 3,
  "permissions": ["storage", "activeTab", "scripting"],
  "host_permissions": ["https://twitter.com/*", "https://x.com/*"],
  "background": { "service_worker": "background.js" },
  "content_scripts": [{
    "matches": ["https://twitter.com/*", "https://x.com/*"],
    "js": ["content.js"],
    "run_at": "document_idle"
  }]
}
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Extension not loading | Ensure `npm run build` completed without errors; reload unpacked extension |
| Posts not being filtered | Check that filters are saved in popup; open DevTools on x.com and check console for errors |
| API key errors | Verify key is stored via Settings panel, not hardcoded; check provider dashboard for quota |
| Local model not loading | Browser must support WebGPU (`chrome://flags/#enable-unsafe-webgpu`); first load downloads model (~2-4GB) |
| Filtered count not updating | MutationObserver may have detached; reload the page |
| TypeScript errors on build | Run `npm install` to ensure all types are present; check `tsconfig.json` target is `ES2020+` |

## Common Patterns

**Check if a post should be processed (before API call):**

```typescript
async function classifyAndFilter(post: ExtractedPost): Promise<void> {
  // Skip if already processed
  if (post.element.dataset.bouncerProcessed) return;
  post.element.dataset.bouncerProcessed = 'true';

  // Check cache first
  const cached = await getCachedResult(post.id);
  if (cached) {
    if (cached.filtered) hidePost(post.element, cached.reasoning);
    return;
  }

  const filters = await getFilters();
  if (filters.length === 0) return;

  const config = await getModelConfig();
  const result = await classifyPost(post, filters, config);

  await cacheResult(post.id, result);
  if (result.filtered) hidePost(post.element, result.reasoning);
}
```

**Storing API key securely (popup UI):**

```typescript
// Never log or expose the key — store only via chrome.storage.local
async function saveApiKey(provider: string, key: string): Promise<void> {
  await chrome.storage.local.set({ [`${provider}_api_key`]: key });
}

async function getApiKey(provider: string): Promise<string> {
  const result = await chrome.storage.local.get(`${provider}_api_key`);
  return result[`${provider}_api_key`] ?? '';
}
```
