---
name: stitch-astro-wp-delivery
description: SOP for delivering client websites using Google Stitch for design, Astro for frontend, and headless WordPress CMS for dynamic content.
---

# Stitch → Astro + WordPress Website Delivery

Complete workflow for AI-generated designs → production websites.

## Stack
| Component | Technology | Purpose |
|-----------|------------|---------| 
| Design | Google Stitch | AI mockup generation |
| Frontend | Astro | Static site generation |
| Styling | Tailwind CSS | Stitch-native |
| CMS | WordPress (headless) | Blog, portfolio |
| SEO | RankMath | Meta, schema |
| Hosting | Cloudflare Pages | Frontend CDN |

---

## Phase 1: Design Generation (1-2 hrs)

### 1.1 Write Stitch Prompts
Use detailed prompts with: sections, colors, typography, content.

### 1.2 Generate in Stitch
```bash
# Use Stitch MCP tools:
mcp_stitch_create_project
mcp_stitch_generate_screen_from_text
mcp_stitch_fetch_screen_code
```

### 1.3 Organize Exports
```
client-name/
├── stitch-exports/
│   ├── homepage.html
│   ├── about.html
│   └── ...
```

---

## Phase 2: WordPress Setup (2-3 hrs)

### 2.1 Install WordPress
- Subdomain: `wp.clientdomain.com`
- Plugins: RankMath, ACF, Classic Editor

### 2.2 Configure
```php
// wp-config.php - CORS
header("Access-Control-Allow-Origin: *");
```

---

## Phase 3: Astro Setup (1 hr)

```bash
npm create astro@latest client-name
npx astro add tailwind sitemap
```

### Project Structure
```
src/
├── components/
├── layouts/MainLayout.astro
├── lib/wordpress.js
├── pages/
│   ├── index.astro
│   └── blog/[...slug].astro
```

---

## Phase 4: Convert Stitch HTML (4-8 hrs)

### 4.1 WordPress API Helper
```javascript
// src/lib/wordpress.js
const WP_URL = 'https://wp.clientdomain.com/wp-json/wp/v2';

export async function getPosts(count = 10) {
  const res = await fetch(`${WP_URL}/posts?per_page=${count}&_embed`);
  return res.json();
}

export async function getPost(slug) {
  const res = await fetch(`${WP_URL}/posts?slug=${slug}&_embed`);
  const posts = await res.json();
  return posts[0];
}
```

### 4.2 Convert Pages
1. Create `.astro` file for each Stitch export
2. Wrap with MainLayout
3. Extract reusable components

---

## Phase 5: Testing (1-2 hrs)

```bash
npm run dev
```

**Checklist:**
- [ ] All pages load
- [ ] Blog pulls from WordPress
- [ ] Mobile responsive
- [ ] SEO meta present

---

## Phase 6: Deployment (30 min)

```bash
npm run build
npx wrangler pages deploy ./dist --project-name=client-name
```

Or connect GitHub to Cloudflare Pages.

---

## Phase 7: Handoff (1 hr)

Provide client:
- WordPress admin URL + credentials
- Brief editing guide
- Support contact

---

## Time Estimate

| Phase | Hours |
|-------|-------|
| Design | 2-4 |
| WordPress | 2-3 |
| Astro | 1 |
| Conversion | 4-8 |
| Testing | 1-2 |
| Deploy | 0.5 |
| Handoff | 1 |
| **Total** | **12-20** |

---

## Maintenance

**Requires Rebuild:**
- Homepage changes, new pages, service updates

**Auto-Reflects:**
- Blog posts (from WP API)
- Portfolio items

---

## Final Checklist

- [ ] All Stitch exports converted
- [ ] WordPress + RankMath configured
- [ ] Blog pulling from WordPress
- [ ] Sitemap + robots.txt
- [ ] Deployed to Cloudflare
- [ ] Custom domain + SSL
- [ ] Client has credentials
