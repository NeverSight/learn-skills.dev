---
name: nextjs-og-image
description: "Generate dynamic Open Graph (OG) social preview images for Next.js App Router projects using the next/og library and ImageResponse. Use when asked to: create OG images, fix social sharing previews, add og:image support, set up opengraph-image.tsx, configure metadata for social sharing, fix OG images not showing logo, fix broken text in OG images, or support multiple domains in OG metadata. Handles multi-domain deployments (e.g. Vercel serving wemoova.com + wemoova.cl), Satori rendering quirks, favicon configuration, and title/description length limits."
---

# Next.js OG Image

Generates production-quality dynamic OG images using `next/og` (Satori under the hood) and wires up all necessary metadata. Covers multi-domain support, image rendering gotchas, and SEO best practices.

## Workflow

### 1. Audit existing setup

Read:
- `app/layout.tsx` — check for `metadata` vs `generateMetadata()`, `metadataBase`, icon config
- `app/opengraph-image.tsx` — if it exists, look for Satori gotchas (see `references/satori-gotchas.md`)
- `public/` — find the logo file and note its exact pixel dimensions (use `python3 -c "import struct; d=open('public/images/logo.png','rb').read(); w,h=struct.unpack('>II',d[16:24]); print(f'{w}x{h}')"`)

### 2. Create `app/opengraph-image.tsx`

Use the template in `assets/og-image-template.tsx` as the starting point.

Key rules (see `references/satori-gotchas.md` for full list):
- Set `export const runtime = "nodejs"` to allow `fs` reads for the logo
- All image dimensions must be **explicit integers** — never `"auto"`, `"100%"`, or `maxWidth`
- Multi-color text: use **separate `<span>` elements in a flex column**, never inline spans inside `<h1>` text nodes
- Every element needs `display: "flex"` — Satori ignores `block`, `inline`, etc.

### 3. Configure `generateMetadata()` for multi-domain

When the project serves multiple domains (e.g. `example.com` + `example.cl`):

```ts
// app/layout.tsx
import { headers } from 'next/headers'

function getSiteUrl(headersList) {
  const forwardedHost = headersList.get('x-forwarded-host') // Vercel proxy sets this
  const host = forwardedHost ?? headersList.get('host') ?? null
  if (host) {
    const protocol = host.startsWith('localhost') ? 'http' : 'https'
    return `${protocol}://${host}`
  }
  return process.env.NEXT_PUBLIC_SITE_URL ?? 'https://example.com'
}

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers()
  const siteUrl = getSiteUrl(headersList)
  return {
    metadataBase: new URL(siteUrl),
    openGraph: {
      images: [{ url: `${siteUrl}/opengraph-image`, width: 1200, height: 630 }],
    },
    twitter: {
      card: 'summary_large_image',
      images: [`${siteUrl}/opengraph-image`],
    },
  }
}
```

> **Why**: Hardcoding `metadataBase` to one domain breaks OG image URLs when the same deployment serves multiple domains. `x-forwarded-host` is set by Vercel and reflects the original domain the user hit.

### 4. Title and description length

| Field | Optimal | Hard limit |
|-------|---------|------------|
| `<title>` | 50–60 chars | 70 |
| `og:description` / `meta description` | 110–160 chars | 200 |
| `twitter:description` | 60–100 chars | 200 |

Measure with: `"Your title here".length`

### 5. Favicon / icons config

```ts
icons: {
  icon: [
    { url: '/ico/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
    { url: '/ico/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
    { url: '/ico/favicon.ico', sizes: 'any' },
  ],
  apple: '/ico/apple-touch-icon.png',
},
manifest: '/ico/site.webmanifest',
```

Update `site.webmanifest` with real `name`, `short_name`, brand `theme_color`, and `start_url: "/"`.

### 6. Verify build

```bash
./node_modules/.bin/next build
```

Check that `/opengraph-image` appears as `○ (Static)` in the route table. If it appears as `ƒ (Dynamic)`, remove any `headers()` or `cookies()` calls from the image file.

## References

- **`references/satori-gotchas.md`** — Full list of Satori CSS limitations and fixes. Read this when the OG image renders incorrectly (missing elements, broken text, invisible images).
- **`assets/og-image-template.tsx`** — Boilerplate `opengraph-image.tsx` to copy and customize.
