---
name: expo-to-figma
description: Capture Expo/React Native app screens and export them to Figma as editable designs. Handles web preview setup, SQLite mocking for web, and automated screen capture using Playwright and Figma MCP.
version: 1.0.0
author: burhanusman
triggers:
  - "/expo-to-figma"
  - "export to figma"
  - "capture to figma"
  - "send screens to figma"
  - "figma capture"
tools:
  - mcp__figma__generate_figma_design
  - mcp__plugin_playwright_playwright__*
  - Bash
  - Read
  - Write
  - Glob
---

# Expo to Figma

Export your Expo/React Native app screens to Figma as editable vector designs.

## What This Skill Does

1. **Starts Expo Web Server** — Launches your app in web mode (`expo start --web`)
2. **Creates Web Mocks** — Generates `.web.ts` files for native-only modules (expo-sqlite, etc.)
3. **Captures Screens** — Uses Playwright to navigate and capture each screen
4. **Exports to Figma** — Sends captures to your Figma file using Figma MCP

## Prerequisites

- **Expo project** with web support (`react-native-web` installed)
- **Figma MCP** configured and authenticated
- **Playwright MCP** for browser automation
- **Figma account** with Full/Dev seat (for reasonable API limits)

## Quick Start

```
/expo-to-figma
```

Or say: "export my app to figma", "capture screens to figma"

## Configuration

Add this to your project's `CLAUDE.md` to always export to the same Figma file:

```markdown
## Figma

Design file for this project:
- **fileKey:** your-figma-file-key
- **fileUrl:** https://www.figma.com/design/your-file-key/Your-File-Name
```

Extract the fileKey from your Figma URL: `figma.com/design/{fileKey}/...`

## How It Works

### Step 1: Check Project Config

The skill reads your `CLAUDE.md` for Figma file configuration:
- If `fileKey` found → adds screens to existing file
- If not found → creates a new Figma file

### Step 2: Start Expo Web Server

```bash
# Check if already running
curl -s -o /dev/null -w "%{http_code}" http://localhost:8081

# Start if needed
npx expo start --web --port 8081 &
```

### Step 3: Create Web Mocks (if needed)

For apps using native-only modules like `expo-sqlite`, create `.web.ts` versions:

| Native File | Web Mock |
|-------------|----------|
| `src/db/client.ts` | `src/db/client.web.ts` |
| `src/db/seed.ts` | `src/db/seed.web.ts` |
| `src/hooks/useFoods.ts` | `src/hooks/useFoods.web.ts` |
| `src/store/index.ts` | `src/store/index.web.ts` |

Metro bundler automatically picks `.web.ts` files for web builds.

### Step 4: Get Capture IDs

For each screen, request a capture ID from Figma MCP:

```
mcp__figma__generate_figma_design:
  outputMode: "existingFile" (or "newFile")
  fileKey: "from-claude-md"
```

Since the file exists, you can request multiple capture IDs in parallel.

### Step 5: Capture with Playwright

Navigate to each screen and inject the Figma capture script:

```javascript
async (page) => {
  // Bypass CSP
  await page.route('**/*', async (route) => {
    const response = await route.fetch();
    const headers = { ...response.headers() };
    delete headers['content-security-policy'];
    await route.fulfill({ response, headers });
  });

  // Navigate and wait for render
  await page.goto('http://localhost:8081/your-route');
  await page.waitForTimeout(3000);

  // Inject capture script
  const script = await page.context().request.get(
    'https://mcp.figma.com/mcp/html-to-design/capture.js'
  );
  await page.evaluate((s) => {
    const el = document.createElement('script');
    el.textContent = s;
    document.head.appendChild(el);
  }, await script.text());

  // Trigger capture
  await page.waitForTimeout(2000);
  return await page.evaluate(() =>
    window.figma.captureForDesign({
      captureId: 'YOUR_CAPTURE_ID',
      endpoint: 'https://mcp.figma.com/mcp/capture/YOUR_CAPTURE_ID/submit',
      selector: 'body'
    })
  );
}
```

### Step 6: Poll for Completion

```
mcp__figma__generate_figma_design:
  captureId: "your-capture-id"
```

Returns the Figma file URL when complete.

## Common Screens to Capture

For typical Expo apps:

| Route | Description |
|-------|-------------|
| `/` | Home/main screen |
| `/profile` | Profile/settings |
| `/[collection]` | List/collection views |
| `/item/[id]` | Detail screens |
| Modal routes | Picker modals, forms |

## Handling Native Modules

### expo-sqlite

Create `client.web.ts` that returns mock data:

```typescript
// src/db/client.web.ts
import { FOOD_LIST } from "@/src/constants/foods";

const mockFoods = FOOD_LIST.map((food, i) => ({
  id: i + 1,
  ...food,
}));

export const db = {
  select: () => ({
    from: (table) => ({
      orderBy: () => mockFoods,
      where: () => mockFoods,
    }),
  }),
  // ... other methods
};
```

### Zustand with AsyncStorage

Create `store/index.web.ts` without persistence:

```typescript
// src/store/index.web.ts
import { create } from "zustand";

export const useAppStore = create((set) => ({
  hasOnboarded: true, // Skip onboarding for preview
  // ... other state
}));
```

## Rate Limits

Figma MCP has usage limits based on your plan:

| Plan + Seat | Daily Limit |
|-------------|-------------|
| Starter / View/Collab | 6 calls/month |
| Pro/Org + Full/Dev | 200 calls/day |
| Enterprise + Full/Dev | 600 calls/day |

Each screen capture uses ~2-3 API calls (get ID + poll status).

## Troubleshooting

### "Unable to resolve module expo-sqlite"
Create web mock files (`.web.ts`) for native modules.

### Screens look different on web
Web uses mock data, native uses real database. Update mock data to match.

### Capture not updating after code changes
Reload the page before capturing:
```javascript
await page.reload();
await page.waitForTimeout(3000);
```

### Figma MCP rate limited
Upgrade to Pro plan with Full/Dev seat, or space out captures.

## Example Project Config

```markdown
## Figma

Design file for this project (use with `/expo-to-figma`):
- **fileKey:** `jL9hl5qaaU0qN7wwJVznjG`
- **fileUrl:** https://www.figma.com/design/jL9hl5qaaU0qN7wwJVznjG/MyApp-Screens

## Web Preview

Web mocks exist for SQLite:
- `src/db/client.web.ts`
- `src/hooks/useData.web.ts`
- `src/store/index.web.ts`

Run web preview: `npx expo start --web`
```

## Output

After successful capture, you'll receive:
- Figma file URL for each captured screen
- Screens added as new pages in your Figma file
- Editable vector designs (not screenshots)
