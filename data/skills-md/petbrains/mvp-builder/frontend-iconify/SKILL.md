---
name: frontend-iconify
description: Image sourcing strategy for UI projects. Use FREE resources first - DiceBear/Boring Avatars for avatars, Unsplash/Picsum for photos, unDraw/Storyset for illustrations, Haikei for backgrounds. AI generation (DALL-E) only when custom branded assets needed and no free alternative exists.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Iconify

200,000+ open-source icons through single API. Search by concept, use any icon set.

## When to Use

- Find icon by concept ("dashboard", "settings")
- Need icons from specific set (Lucide, Heroicons)
- Download SVGs for project
- Dynamic icon component

## Process

**SEARCH → SELECT → INTEGRATE**

1. Search: `curl "https://api.iconify.design/search?query=dashboard"`
2. Select from results
3. Use via component or download SVG

## API Quick Reference

```bash
# Search icons
curl "https://api.iconify.design/search?query=home&limit=10"

# Get SVG directly
curl "https://api.iconify.design/lucide/home.svg"

# With custom color (URL-encode #)
curl "https://api.iconify.design/lucide/home.svg?color=%236366f1"
```

## Recommended Sets

| Set | Prefix | Style | Best For |
|-----|--------|-------|----------|
| Lucide | `lucide` | Outline 24px | Default, shadcn |
| Heroicons | `heroicons` | Outline+Solid | Tailwind |
| Phosphor | `ph` | 6 weights | Weight variants |
| Tabler | `tabler` | Outline 24px | Large variety |
| Simple Icons | `simple-icons` | Logos | Brand logos |

## Integration Methods

### React Component (Recommended)

```bash
npm install @iconify/react
```

```tsx
import { Icon } from '@iconify/react';

<Icon icon="lucide:home" width={24} />
<Icon icon="lucide:settings" className="w-5 h-5 text-primary" />
```

### Download SVG

```bash
curl -o ./public/icons/home.svg "https://api.iconify.design/lucide/home.svg"
```

### Batch Download

```bash
ICONS="home settings user search menu"
for icon in $ICONS; do
  curl -o "./public/icons/$icon.svg" "https://api.iconify.design/lucide/$icon.svg"
done
```

## Common Icon Names

```yaml
Navigation:  home, menu, x, chevron-right, arrow-right, search
Actions:     plus, minus, check, edit, trash-2, copy, download
Objects:     file, folder, image, calendar, mail, link
Users:       user, users, bell, lock, key, shield
Media:       play, pause, volume-2, camera, mic
Data:        bar-chart, trending-up, database, server
Status:      check-circle, x-circle, alert-triangle, info
```

## Quick Pattern

```tsx
// Icon utility wrapper
function AppIcon({ name, ...props }) {
  return <Icon icon={`lucide:${name}`} {...props} />;
}

// Usage
<AppIcon name="home" className="w-5 h-5" />
```

## Style Matching

| Project Style | Recommended |
|---------------|-------------|
| Modern/Clean | Lucide, Feather |
| Enterprise | Heroicons, Material |
| Playful | Phosphor (fill) |
| Brand logos | Simple Icons |

**Browser:** https://icon-sets.iconify.design
