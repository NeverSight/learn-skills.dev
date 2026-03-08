---
name: favicon
displayName: Favicon Generator
description: Generate emoji-based favicons, Apple touch icons, and OG images using emojico. Use when adding or updating favicons for any project. Never use a default emoji — always ask Joel which emoji to use.
version: 0.1.0
author: joel
tags:
  - favicon
  - seo
  - branding
  - emojico
disable-model-invocation: true
---

# Favicon Generation with emojico

Generate complete favicon sets from emoji. **Never pick a default emoji** — always ask Joel which emoji to use for the project.

## When to Use

Triggers: `favicon`, `add favicon`, `update favicon`, `site icon`, `emojico`, `touch icon`, or any request to add/change a site's icon.

## Install

```bash
npm install -g emojico
```

Verify: `emojico --help`

## Usage

```bash
# Generate full set into project's public/ dir
emojico 🧙 --out ./public --all

# Generates:
# public/favicon.ico
# public/favicons/favicon-16x16.png
# public/favicons/favicon-32x32.png
# public/favicons/favicon-48x48.png
# public/apple-touch-icon/apple-touch-icon-{57,60,72,76,114,120,144,152,180}x{...}.png
# public/og-image.png
```

## Wiring Into Frameworks

### Next.js (App Router)

`favicon.ico` in `public/` is auto-served. Add metadata in `layout.tsx`:

```ts
export const metadata: Metadata = {
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon/apple-touch-icon-180x180.png',
  },
}
```

### TanStack Start

Add to `__root.tsx` head config:

```ts
links: [
  { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
  { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon/apple-touch-icon-180x180.png' },
]
```

## Rules

1. **NEVER use a default emoji.** Always ask Joel to pick the emoji for the project.
2. **Always use `--all`** to generate the complete set (ico + png + apple + og).
3. **Output to `public/`** in the target app directory.
4. **Wire head tags** after generating — emojico generates files but doesn't modify source.
5. **Prefer dynamic OG images** over the static `og-image.png` for sites with multiple pages — use the emojico OG as a fallback only.
