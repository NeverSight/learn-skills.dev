---
name: og-image
description: Generate social media preview images (Open Graph) and configure meta tags. Creates a screenshot-optimized page using the project's existing design system, captures it at 1200x630, and sets up all social sharing meta tags.
---

This skill creates professional Open Graph images for social media sharing. It analyzes the existing codebase to match the project's design system, generates a dedicated OG image page, screenshots it, and configures all necessary meta tags.

## Workflow

### Phase 1: Codebase Analysis

Explore the project to understand:

1. **Framework Detection**
   - Check `package.json` for Next.js, Vite, Astro, Remix, etc.
   - Identify the routing pattern (file-based, config-based)
   - Find where to create the `/og-image` route

2. **Design System Discovery**
   - Look for Tailwind config (`tailwind.config.js/ts`) for color palette
   - Check for CSS variables in global styles (`:root` definitions)
   - Find existing color tokens, font families, spacing scales
   - Look for a theme or design tokens file

3. **Branding Assets**
   - Find logo files in `/public`, `/assets`, `/src/assets`
   - Check for favicon, app icons
   - Look for existing hero sections or landing pages with branding

4. **Product Information**
   - Extract product name from `package.json`, landing page, or meta tags
   - Find tagline/description from existing pages
   - Look for existing OG/meta configuration to understand current setup

5. **Existing Components**
   - Find reusable UI components that could be leveraged
   - Check for glass effects, gradients, or distinctive visual patterns
   - Identify the overall aesthetic (dark mode, light mode, etc.)

### Phase 2: OG Image Page Creation

Create a dedicated route at `/og-image` (or equivalent for the framework):

**Page Requirements:**
- Fixed dimensions: exactly 1200px wide × 630px tall
- Self-contained styling (no external dependencies that might not render)
- Hide any dev tool indicators with CSS:
```css
[data-nextjs-dialog-overlay],
[data-nextjs-dialog],
nextjs-portal,
#__next-build-indicator {
  display: none !important;
}
```

**Content Structure:**
- Product logo/icon (prominent placement)
- Product name with distinctive typography
- Tagline or value proposition
- Visual representation of the product (mockup, illustration, or abstract design)
- URL/domain at the bottom
- Background that matches the project aesthetic (gradients, patterns, etc.)

**Design Principles:**
- Use the project's existing color palette
- Match the typography from the main site
- Include visual elements that represent the product
- Ensure high contrast for readability at small sizes (social previews are often small)
- Test that text is readable when the image is scaled down to ~400px wide

### Phase 3: Screenshot Capture

Use Playwright to capture the OG image:

1. Navigate to the OG image page (typically `http://localhost:3000/og-image` or similar)
2. Resize viewport to exactly 1200×630
3. Wait for any animations to complete or fonts to load
4. Take a PNG screenshot
5. Save to the project's public folder as `og-image.png`

**Playwright Commands:**
```
browser_navigate: http://localhost:{port}/og-image
browser_resize: width=1200, height=630
browser_take_screenshot: og-image.png (then copy to /public)
```

### Phase 4: Meta Tag Configuration

Audit and update the project's meta tag configuration. For Next.js App Router, update `layout.tsx`. For other frameworks, update the appropriate location.

**Required Meta Tags:**

```typescript
// Open Graph
openGraph: {
  title: "Product Name - Short Description",
  description: "Compelling description for social sharing",
  url: "https://yourdomain.com",
  siteName: "Product Name",
  locale: "en_US",
  type: "website",
  images: [{
    url: "/og-image.png",  // or absolute URL
    width: 1200,
    height: 630,
    alt: "Descriptive alt text for accessibility",
    type: "image/png",
  }],
},

// Twitter/X
twitter: {
  card: "summary_large_image",
  title: "Product Name - Short Description",
  description: "Compelling description for Twitter",
  creator: "@handle",  // if provided
  images: [{
    url: "/og-image.png",
    width: 1200,
    height: 630,
    alt: "Descriptive alt text",
  }],
},

// Additional
other: {
  "theme-color": "#000000",  // match brand color
  "msapplication-TileColor": "#000000",
},

appleWebApp: {
  title: "Product Name",
  statusBarStyle: "black-translucent",
  capable: true,
},
```

**Ensure `metadataBase` is set** for relative URLs to resolve correctly:
```typescript
metadataBase: new URL("https://yourdomain.com"),
```

### Phase 5: Verification & Output

1. **Verify the image exists** at the public path
2. **Check meta tags** are correctly rendered in the HTML
3. **Provide cache-busting instructions:**
   - Facebook/LinkedIn: https://developers.facebook.com/tools/debug/
   - Twitter/X: https://cards-dev.twitter.com/validator
   - LinkedIn: https://www.linkedin.com/post-inspector/

4. **Summary output:**
   - Path to generated OG image
   - URL to preview the OG image page locally
   - List of meta tags added/updated
   - Links to social preview debuggers

## Prompting for Missing Information

Only ask the user if these cannot be determined from the codebase:

1. **Domain/URL** - If not found in existing config, ask: "What's your production domain? (e.g., https://example.com)"

2. **Twitter/X handle** - If adding twitter:creator, ask: "What's your Twitter/X handle for attribution? (optional)"

3. **Tagline** - If no clear tagline found, ask: "What's a short tagline for social previews? (1 sentence)"

## Framework-Specific Notes

**Next.js App Router:**
- Create `/app/og-image/page.tsx`
- Update metadata in `/app/layout.tsx`
- Use `'use client'` directive for the OG page

**Next.js Pages Router:**
- Create `/pages/og-image.tsx`
- Update `_app.tsx` or use `next-seo`

**Vite/React:**
- Create route via router config
- Update `index.html` meta tags or use `react-helmet`

**Astro:**
- Create `/src/pages/og-image.astro`
- Update layout with meta tags

## Quality Checklist

Before completing, verify:
- [ ] OG image renders correctly at 1200×630
- [ ] No dev tool indicators visible in screenshot
- [ ] Image saved to public folder
- [ ] Meta tags include og:image with absolute URL capability
- [ ] Meta tags include twitter:card as summary_large_image
- [ ] Meta tags include dimensions (width/height)
- [ ] Meta tags include alt text for accessibility
- [ ] theme-color is set to match brand
- [ ] User informed of cache-busting URLs
