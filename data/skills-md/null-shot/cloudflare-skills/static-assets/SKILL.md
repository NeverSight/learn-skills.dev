---
name: static-assets
description: Serve static files and single-page applications from Workers. Load when hosting React/Vue/Angular SPAs, building hybrid Workers with API routes and frontend, configuring SPA fallback routing, or deploying Vite/Next.js/Remix static exports.
---

# Cloudflare Static Assets

Serve static files, single-page applications (SPAs), and build hybrid Workers that combine API routes with frontend hosting.

## FIRST: Project Setup

Static Assets require a `public/` directory and configuration in `wrangler.jsonc`:

```bash
# Create public directory for your build output
mkdir public

# Add your static files
echo "<h1>Hello World</h1>" > public/index.html
```

## When to Use

| Use Case | Description |
|----------|-------------|
| **Single-Page Applications** | React, Vue, Angular apps with client-side routing |
| **Static Sites** | HTML/CSS/JS sites, generated static content |
| **Hybrid Apps** | Worker API routes + frontend in one deployment |
| **Framework Integration** | Next.js, Vite, Remix build outputs |

## Quick Reference

| Task | Configuration |
|------|---------------|
| Basic static hosting | `"assets": { "directory": "./public/" }` |
| SPA routing (404 → index) | `"not_found_handling": "single-page-application"` |
| Custom 404 page | `"not_found_handling": "404-page"` |
| Custom binding name | `"binding": "ASSETS"` (default) |
| Access in Worker | `env.ASSETS.fetch(request)` |

## wrangler.jsonc Configuration

### Basic Static Hosting

```jsonc
{
  "name": "my-static-site",
  "compatibility_date": "2024-01-01",
  "assets": {
    "directory": "./public/"
  }
}
```

### SPA with Custom 404 Handling

```jsonc
{
  "name": "my-spa",
  "compatibility_date": "2024-01-01",
  "assets": {
    "directory": "./public/",
    "not_found_handling": "single-page-application"
  }
}
```

**not_found_handling options:**
- `"single-page-application"` - Routes all 404s to `/index.html` (default for SPAs)
- `"404-page"` - Serves `/404.html` for missing files
- `"none"` - Returns standard 404 responses

## Hybrid Worker with Static Assets

Combine API routes with static file serving in a single Worker:

```typescript
// src/index.ts

interface Env {
  ASSETS: Fetcher;
}

export default {
  fetch(request, env) {
    const url = new URL(request.url);

    // Handle API routes in the Worker
    if (url.pathname.startsWith("/api/")) {
      return Response.json({
        name: "Cloudflare",
        timestamp: Date.now()
      });
    }

    // Serve static assets for all other routes
    return env.ASSETS.fetch(request);
  },
} satisfies ExportedHandler<Env>;
```

**wrangler.jsonc for hybrid app:**

```jsonc
{
  "name": "my-app",
  "main": "src/index.ts",
  "compatibility_date": "2024-01-01",
  "assets": {
    "directory": "./public/",
    "not_found_handling": "single-page-application",
    "binding": "ASSETS"
  },
  "observability": {
    "enabled": true
  }
}
```

## SPA Routing

Single-page applications need all routes to resolve to `index.html` for client-side routing to work:

```jsonc
{
  "assets": {
    "directory": "./public/",
    "not_found_handling": "single-page-application"
  }
}
```

**What this does:**
- `/` → serves `/index.html`
- `/about` → serves `/index.html` (client-side router handles /about)
- `/contact` → serves `/index.html`
- `/styles.css` → serves actual file if it exists
- Missing file → serves `/index.html`

## API Routes Pattern

Common pattern: Handle API requests in Worker, serve everything else as static assets:

```typescript
interface Env {
  ASSETS: Fetcher;
  DB: D1Database;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // API Routes
    if (url.pathname.startsWith("/api/")) {
      switch (url.pathname) {
        case "/api/users":
          const users = await env.DB.prepare("SELECT * FROM users").all();
          return Response.json(users.results);
        
        case "/api/health":
          return Response.json({ status: "ok" });
        
        default:
          return Response.json({ error: "Not found" }, { status: 404 });
      }
    }

    // Static Assets
    return env.ASSETS.fetch(request);
  },
} satisfies ExportedHandler<Env>;
```

## Framework Integration

### Vite (React, Vue, Svelte)

```bash
# Build output goes to dist/
npm run build

# Move to public/
mv dist/* public/
```

**vite.config.ts:**
```typescript
export default {
  build: {
    outDir: 'public'
  }
}
```

### Next.js (Static Export)

```bash
npm run build
```

**next.config.js:**
```javascript
module.exports = {
  output: 'export',
  distDir: 'public'
}
```

### Remix

```bash
npm run build
```

**remix.config.js:**
```javascript
module.exports = {
  assetsBuildDirectory: "public/build"
}
```

## ASSETS Fetcher API

The `ASSETS` binding is a `Fetcher` that handles static file requests:

```typescript
interface Env {
  ASSETS: Fetcher;
}

// Direct pass-through
env.ASSETS.fetch(request)

// Modify request before serving
const modifiedRequest = new Request(request.url, {
  headers: { "Cache-Control": "max-age=3600" }
});
env.ASSETS.fetch(modifiedRequest)

// Serve specific file
env.ASSETS.fetch(new Request("https://example.com/index.html"))
```

## Cache Control

Static assets are cached by default. Customize caching behavior:

```typescript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // API routes - no cache
    if (url.pathname.startsWith("/api/")) {
      return Response.json({ data: "dynamic" }, {
        headers: { "Cache-Control": "no-store" }
      });
    }
    
    // Get asset response
    const response = await env.ASSETS.fetch(request);
    
    // Customize cache headers for specific files
    if (url.pathname.endsWith(".js") || url.pathname.endsWith(".css")) {
      const newResponse = new Response(response.body, response);
      newResponse.headers.set("Cache-Control", "public, max-age=31536000, immutable");
      return newResponse;
    }
    
    return response;
  },
} satisfies ExportedHandler<Env>;
```

## Detailed References

- **[references/configuration.md](references/configuration.md)** - Full assets configuration options, binding details
- **[references/frameworks.md](references/frameworks.md)** - Framework-specific build configurations
- **[references/testing.md](references/testing.md)** - buildPagesASSETSBinding, testing SPA fallback, ASSETS binding

## Best Practices

1. **Use SPA mode for client-side routing**: Set `"not_found_handling": "single-page-application"`
2. **Prefix API routes**: Use `/api/*` pattern for clear separation from static routes
3. **Configure framework output**: Point build output directly to `./public/`
4. **Cache immutable assets**: Add cache headers for hashed files (`app.abc123.js`)
5. **Enable observability**: Track Worker analytics with `"observability": { "enabled": true }`
6. **Test locally**: Use `wrangler dev` to test both Worker and assets together
7. **Handle errors gracefully**: Return proper status codes for API routes vs static assets

## Common Patterns

### Authentication Check Before Assets

```typescript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Public routes
    if (url.pathname === "/login" || url.pathname.startsWith("/public/")) {
      return env.ASSETS.fetch(request);
    }
    
    // Check authentication
    const token = request.headers.get("Authorization");
    if (!token) {
      return new Response("Unauthorized", { status: 401 });
    }
    
    // API or authenticated assets
    if (url.pathname.startsWith("/api/")) {
      return handleAPI(request, env);
    }
    
    return env.ASSETS.fetch(request);
  },
};
```

### Custom Error Pages

```typescript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname.startsWith("/api/")) {
      try {
        return await handleAPI(request, env);
      } catch (error) {
        return Response.json({ error: error.message }, { status: 500 });
      }
    }
    
    const response = await env.ASSETS.fetch(request);
    
    // Serve custom 404 page
    if (response.status === 404) {
      return env.ASSETS.fetch(new Request(`${url.origin}/404.html`));
    }
    
    return response;
  },
};
```

## Local Development

```bash
# Start dev server with assets
wrangler dev

# Specify custom port
wrangler dev --port 8787

# Auto-rebuild on changes (if using framework)
# Terminal 1: Framework watch mode
npm run dev

# Terminal 2: Wrangler
wrangler dev
```

## Deployment

```bash
# Deploy Worker + Assets together
wrangler deploy

# View deployment
wrangler deployments list
```

The Worker and static assets are deployed as a single unit. All files in the `assets.directory` are uploaded and served from Cloudflare's global network.
