---
name: marketplace-build-component
description: Builds UI components using the Blok design system for Sitecore Marketplace apps. Use when the user wants to create UI, add components, build a page layout, or work with Blok/shadcn components in a marketplace app.
---

# Build UI with Blok Design System

You are helping the user build UI components for a Sitecore Marketplace app using the Blok design system (Sitecore's shadcn-based component library).

## Key Principles

1. **Always use Blok components** — they match the Sitecore host UI and support light/dark themes automatically
2. **SDK data integration** — use loading states (Skeleton) and error states (Alert) when fetching SDK data
3. **Extension point awareness** — different extension types have different UI constraints (see below)
4. **Responsive** — components render inside iframes of varying sizes

## Installing Components

Blok components are installed via the shadcn CLI:

```bash
# Install the Blok theme (required first)
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/blok-theme.json

# Install individual components
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/<component-name>.json
```

See [blok-components.md](references/blok-components.md) for the full component catalog with install commands.

## UI Patterns by Extension Type

### Compact Field (custom-field)
- Very limited space (~300px wide, variable height)
- Use: Input, Select, Badge, small inline components
- Avoid: Tables, large layouts, modals

### Dashboard Widget
- Medium space (~400x300px default, resizable)
- Use: Cards, Charts, Stats, compact Tables
- Good for: Summary data, quick actions

### Pages Context Panel
- Side panel (~350px wide, full height)
- Use: Vertical layouts, Lists, Accordion, Tabs
- Good for: Contextual info about current page, actions

### Fullscreen
- Full viewport within the Sitecore shell
- Use: Any components, complex layouts, Tables, Forms
- Good for: Full CRUD interfaces, dashboards, settings

### Standalone
- Independent page, not in Sitecore shell
- Use: Any components, full creative freedom
- Good for: Public-facing pages, OAuth callbacks

## SDK Data Integration Pattern

```tsx
"use client";

import { useEffect, useState } from "react";
import { useSitecoreClient } from "@/hooks/use-sitecore";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";

export function MyComponent() {
  const client = useSitecoreClient();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const result = await client.query("app.context");
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [client]);

  if (loading) return <Skeleton className="h-32 w-full" />;
  if (error) return <Alert variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>;

  return <div>{/* Render data */}</div>;
}
```

## Reference Files
- [Blok Components](references/blok-components.md) — Full component catalog with install commands
