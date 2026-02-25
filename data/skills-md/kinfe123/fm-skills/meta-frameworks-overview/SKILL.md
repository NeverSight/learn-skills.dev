---
name: meta-frameworks-overview
description: Explains meta-frameworks like Next.js, Nuxt, SvelteKit, Remix, Astro, and their architectural patterns. Use when comparing frameworks, choosing a framework for a project, or understanding what features meta-frameworks provide beyond base UI libraries.
---

# Meta-Frameworks Overview

## What is a Meta-Framework?

A meta-framework builds on top of a UI library (React, Vue, Svelte) to provide:

```
UI Library (React, Vue, Svelte)
    ↓ adds
Meta-Framework Features:
├── File-based routing
├── Server-side rendering (SSR)
├── Static site generation (SSG)
├── API routes / backend integration
├── Code splitting & bundling
├── Image optimization
├── Deployment optimizations
└── Full-stack capabilities
```

## Why Meta-Frameworks?

### Without a Meta-Framework (Manual Setup)

```
Create React App
├── Configure Webpack/Vite
├── Set up React Router
├── Configure SSR manually (complex)
├── Set up Express/Node server
├── Configure code splitting
├── Set up environment variables
├── Configure production build
└── Handle deployment
```

### With a Meta-Framework

```
npx create-next-app / npm create astro
├── Routing: ✓ automatic
├── SSR/SSG: ✓ built-in
├── API routes: ✓ included
├── Bundling: ✓ optimized
├── Deployment: ✓ streamlined
└── Start building: ✓ immediately
```

## Framework Comparison Matrix

| Framework | UI Library | Rendering | Philosophy |
|-----------|------------|-----------|------------|
| **Next.js** | React | SSR, SSG, ISR, CSR | Full-stack React |
| **Remix** | React | SSR, progressive enhancement | Web standards, forms |
| **Nuxt** | Vue | SSR, SSG, ISR | Full-stack Vue |
| **SvelteKit** | Svelte | SSR, SSG, CSR | Compiler-first |
| **Astro** | Any (React, Vue, Svelte, etc.) | SSG, SSR, Islands | Content-first, minimal JS |
| **Solid Start** | Solid | SSR, SSG | Fine-grained reactivity |
| **Qwik City** | Qwik | Resumable | Zero hydration |

## Next.js

**Full-stack React framework by Vercel.**

### Key Features

- **App Router** (new): React Server Components, nested layouts
- **Pages Router** (legacy): Traditional file-based routing
- **Rendering options:** SSG, SSR, ISR, CSR per route
- **API Routes:** Backend endpoints within the same project
- **Image/Font optimization:** Built-in components

### Routing Model

```
app/
├── page.tsx          → /
├── about/page.tsx    → /about
├── blog/
│   ├── page.tsx      → /blog
│   └── [slug]/page.tsx → /blog/:slug
└── api/
    └── route.ts      → API endpoint
```

### Rendering Decision

```tsx
// Static (default - SSG)
export default function Page() {
  return <div>Static content</div>;
}

// Dynamic (SSR)
export const dynamic = 'force-dynamic';

// ISR
export const revalidate = 60; // seconds
```

### Best For

- Production React applications
- E-commerce, SaaS, marketing sites
- Teams wanting batteries-included solution
- Vercel deployment (optimized)

## Remix

**Full-stack React framework focused on web fundamentals.**

### Key Features

- **Nested routes:** Parallel data loading
- **Progressive enhancement:** Works without JavaScript
- **Form handling:** Built-in `<Form>` with server actions
- **Error boundaries:** Per-route error handling
- **Web standards:** Uses fetch, FormData, Response

### Philosophy

```
Traditional SPA:
  Click → JS preventDefault → Fetch API → Update State → Re-render

Remix:
  Click → Form submits → Server action → Return data → Re-render
  (Works without JS, enhanced with JS)
```

### Routing Model

```
app/
├── routes/
│   ├── _index.tsx        → /
│   ├── about.tsx         → /about
│   ├── blog._index.tsx   → /blog
│   └── blog.$slug.tsx    → /blog/:slug
└── root.tsx              → Root layout
```

### Data Loading

```tsx
// Parallel loading of nested route data
export async function loader({ params }) {
  return json(await getPost(params.slug));
}

export async function action({ request }) {
  const formData = await request.formData();
  // Handle form submission
}
```

### Best For

- Form-heavy applications
- Progressive enhancement requirements
- Teams preferring web standards
- Apps that should work without JS

## Nuxt

**Full-stack Vue framework.**

### Key Features

- **Auto-imports:** Components, composables auto-imported
- **File-based routing:** Vue components as routes
- **Nitro server:** Universal deployment
- **Modules ecosystem:** Rich plugin system

### Routing Model

```
pages/
├── index.vue         → /
├── about.vue         → /about
└── blog/
    ├── index.vue     → /blog
    └── [slug].vue    → /blog/:slug
```

### Data Fetching

```vue
<script setup>
// Runs on server, cached
const { data } = await useFetch('/api/posts');

// Always fresh
const { data } = await useFetch('/api/posts', { fresh: true });
</script>
```

### Best For

- Vue.js teams
- Content sites, applications
- Teams wanting Vue-specific optimizations

## SvelteKit

**Full-stack Svelte framework.**

### Key Features

- **Compiler-first:** Svelte compiles to vanilla JS
- **Adapters:** Deploy anywhere (Node, Vercel, Cloudflare, etc.)
- **Load functions:** Unified data loading
- **Form actions:** Built-in form handling

### Routing Model

```
src/routes/
├── +page.svelte          → /
├── +layout.svelte        → Shared layout
├── about/+page.svelte    → /about
└── blog/
    ├── +page.svelte      → /blog
    └── [slug]/+page.svelte → /blog/:slug
```

### Data Loading

```javascript
// +page.server.js - runs on server only
export async function load({ params }) {
  return {
    post: await getPost(params.slug)
  };
}
```

### Best For

- Performance-critical applications
- Teams preferring Svelte's approach
- Smaller bundle size requirements

## Astro

**Content-first framework with islands architecture.**

### Key Features

- **Zero JS by default:** Ships no JavaScript unless needed
- **Islands architecture:** Hydrate only interactive components
- **Framework agnostic:** Use React, Vue, Svelte together
- **Content collections:** First-class Markdown/MDX support

### Routing Model

```
src/pages/
├── index.astro           → /
├── about.astro           → /about
└── blog/
    ├── index.astro       → /blog
    └── [slug].astro      → /blog/:slug
```

### Islands Pattern

```astro
---
import Header from './Header.astro';     // No JS
import Counter from './Counter.jsx';      // React
import Search from './Search.vue';        // Vue
---

<Header />

<!-- Islands: only these ship JS -->
<Counter client:load />
<Search client:visible />
```

### Client Directives

| Directive | When Hydrates |
|-----------|---------------|
| `client:load` | Immediately on page load |
| `client:idle` | When browser is idle |
| `client:visible` | When component is visible |
| `client:media` | When media query matches |
| `client:only` | Skip SSR, client render only |

### Best For

- Content-heavy sites (blogs, docs, marketing)
- Performance-first approach
- Teams using multiple UI frameworks
- Static sites with some interactivity

## Qwik City

**Framework with resumability (zero hydration).**

### Key Features

- **Resumability:** No hydration cost
- **Lazy loading:** Loads JS only when needed
- **Familiar syntax:** JSX-like templates

### How Resumability Works

```
Traditional SSR:
  Server render → Download all JS → Hydrate (re-execute) → Interactive

Qwik:
  Server render + serialize state → Load tiny runtime → Resume → Interactive
  (No re-execution, state already in HTML)
```

### Best For

- Performance-critical applications
- Large applications with many components
- Teams wanting to eliminate hydration cost

## Framework Selection Guide

### By Project Type

| Project Type | Recommended |
|--------------|-------------|
| Marketing site | Astro, Next.js (SSG) |
| Blog/Docs | Astro, Next.js, SvelteKit |
| E-commerce | Next.js, Remix, Nuxt |
| Dashboard/App | Next.js, SvelteKit, Remix |
| Highly interactive app | Next.js, SvelteKit, Remix |
| Performance-critical | Astro, Qwik, SvelteKit |

### By Team Expertise

| Team Knows | Recommended |
|------------|-------------|
| React | Next.js, Remix, Astro |
| Vue | Nuxt, Astro |
| Svelte | SvelteKit, Astro |
| Multiple / Learning | Astro |

### By Priorities

| Priority | Recommended |
|----------|-------------|
| SEO | Any (all support SSR/SSG) |
| Minimal JavaScript | Astro, Qwik |
| Progressive enhancement | Remix |
| Largest ecosystem | Next.js |
| Fastest runtime | SvelteKit, Qwik |
| Most flexible | Astro |

## Common Patterns Across Frameworks

### File-Based Routing

All meta-frameworks use file structure for routes:

```
pages/about.tsx  →  /about
pages/[id].tsx   →  /123, /abc (dynamic)
pages/[...slug].tsx  →  /a/b/c (catch-all)
```

### Layouts

Shared UI across routes:

```
layout.tsx (Next.js)
+layout.svelte (SvelteKit)
layouts/default.vue (Nuxt)
```

### Data Loading

Fetching data before render:

```
getServerSideProps / loader functions (Next.js)
loader functions (Remix)
load functions (SvelteKit)
useFetch (Nuxt)
frontmatter + getStaticProps (Astro)
```

### API Routes

Backend endpoints in the same project:

```
app/api/route.ts (Next.js)
app/routes/api.$.ts (Remix)
server/api/ (Nuxt)
src/pages/api/ (Astro)
```

## Migration Considerations

### From SPA to Meta-Framework

1. Choose framework matching your UI library
2. Migrate routing to file-based
3. Move data fetching to server (loaders)
4. Update build/deploy pipeline
5. Add SSR/SSG as needed

### Between Meta-Frameworks

- Routing patterns are similar (map file structure)
- Data fetching patterns differ (loaders, getServerSideProps, useFetch)
- Styling approaches may vary
- Deployment adapters differ

---

## Deep Dive: Understanding Meta-Frameworks From First Principles

### What Problems Do Meta-Frameworks Solve?

To understand meta-frameworks, you must understand the problems of building production apps WITHOUT them:

```
PROBLEM 1: Build Configuration Hell

// React alone gives you:
import React from 'react';
function App() { return <div>Hello</div>; }

// But browsers don't understand JSX. You need:
// - Babel (transpile JSX → JavaScript)
// - Webpack/Vite (bundle modules)
// - PostCSS (process CSS)
// - Asset handling (images, fonts)
// - Environment variables
// - Development server with HMR
// - Production build optimization

// That's ~500 lines of config before writing any app code


PROBLEM 2: Routing is Non-Trivial

// React gives you components, not routes
// You need React Router or similar:
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// But then:
// - How to code-split per route?
// - How to preload routes?
// - How to handle nested layouts?
// - How to protect routes?
// - How to handle 404s?


PROBLEM 3: Data Fetching Complexity

// Basic fetching seems simple:
useEffect(() => {
  fetch('/api/data').then(setData);
}, []);

// But production needs:
// - Loading states
// - Error handling
// - Caching
// - Deduplication
// - Revalidation
// - SSR considerations


PROBLEM 4: Server-Side Rendering is HARD

// SSR manually requires:
// - Node.js server (Express/Fastify)
// - renderToString on server
// - Hydration on client
// - Different entry points (server.js, client.js)
// - Matching router on both sides
// - Data serialization between server/client
// - Handling streaming
// - Environment differences (window undefined on server)


META-FRAMEWORK SOLUTION:
All of the above is pre-configured and optimized.
Just write your components and routes.
```

### The Layered Architecture Model

Meta-frameworks are built in layers:

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR APPLICATION CODE                         │
│         (Pages, Components, API routes, Business Logic)         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     META-FRAMEWORK LAYER                         │
│   (Next.js / Nuxt / SvelteKit / Remix / Astro)                  │
│                                                                  │
│   ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐      │
│   │  Router   │ │  Builder  │ │  Server   │ │ Optimizer │      │
│   │  System   │ │  System   │ │  Runtime  │ │  Layer    │      │
│   └───────────┘ └───────────┘ └───────────┘ └───────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      UI LIBRARY LAYER                            │
│              (React / Vue / Svelte / Solid)                      │
│                                                                  │
│   ┌───────────┐ ┌───────────┐ ┌───────────┐                     │
│   │ Component │ │   State   │ │  Virtual  │                     │
│   │   Model   │ │   Mgmt    │ │    DOM    │                     │
│   └───────────┘ └───────────┘ └───────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     PLATFORM LAYER                               │
│                  (Node.js, Deno, Bun, Edge)                     │
└─────────────────────────────────────────────────────────────────┘
```

### How File-Based Routing Works Under the Hood

The magic of "file = route" is compile-time transformation:

```javascript
// YOUR FILE STRUCTURE:
// app/
// ├── page.tsx
// ├── about/page.tsx
// └── blog/[slug]/page.tsx

// AT BUILD TIME, framework generates something like:

const routes = [
  {
    pattern: /^\/$/,
    component: () => import('./app/page.tsx'),
    type: 'page',
  },
  {
    pattern: /^\/about$/,
    component: () => import('./app/about/page.tsx'),
    type: 'page',
  },
  {
    pattern: /^\/blog\/([^/]+)$/,
    component: () => import('./app/blog/[slug]/page.tsx'),
    type: 'page',
    params: ['slug'],
  },
];

// The framework's router uses this table at runtime
function matchRoute(pathname) {
  for (const route of routes) {
    const match = pathname.match(route.pattern);
    if (match) {
      return {
        component: route.component,
        params: extractParams(route.params, match),
      };
    }
  }
  return null; // 404
}
```

### Server Components: A Paradigm Shift

React Server Components (used by Next.js App Router) fundamentally change the component model:

```javascript
// TRADITIONAL REACT (All components run everywhere):

// This runs on server (for SSR) AND client (for hydration)
function ProductPage() {
  const [product, setProduct] = useState(null);
  
  useEffect(() => {
    // Runs only on client
    fetch('/api/product').then(r => r.json()).then(setProduct);
  }, []);
  
  return <div>{product?.name}</div>;
}

// SHIPPED TO CLIENT:
// - ProductPage component code
// - useState implementation
// - useEffect implementation
// - All dependencies


// REACT SERVER COMPONENTS:

// This runs ONLY on server, never shipped to client
async function ProductPage() {
  // Direct database access! No API needed!
  const product = await db.products.findById(123);
  
  // This HTML is sent, not the component code
  return <div>{product.name}</div>;
}

// SHIPPED TO CLIENT:
// - Only the rendered HTML
// - Zero JavaScript for this component

// BUT INTERACTIVITY NEEDS CLIENT COMPONENTS:
'use client';  // This directive makes it a client component

function AddToCartButton({ productId }) {
  const [loading, setLoading] = useState(false);
  
  async function handleClick() {
    setLoading(true);
    await addToCart(productId);
    setLoading(false);
  }
  
  return <button onClick={handleClick}>{loading ? '...' : 'Add'}</button>;
}
// This component IS shipped to client
```

**The composition model:**

```jsx
// Server Component (default in App Router)
async function ProductPage({ params }) {
  const product = await getProduct(params.id);  // Server-only
  
  return (
    <div>
      <h1>{product.name}</h1>           {/* Static, no JS */}
      <p>{product.description}</p>      {/* Static, no JS */}
      <AddToCartButton id={product.id} /> {/* Client Component, has JS */}
    </div>
  );
}

// Rendered output:
// <div>
//   <h1>Product Name</h1>              ← Plain HTML
//   <p>Description here</p>            ← Plain HTML  
//   <button>Add to Cart</button>       ← Hydrated with JS
// </div>
```

### Data Loading: The Core Pattern Differences

Each framework has a different philosophy:

```javascript
// NEXT.JS APP ROUTER:
// Data fetching in the component itself (async components)

async function ProductPage({ params }) {
  // This fetch is automatically deduplicated and cached
  const product = await fetch(`/api/products/${params.id}`).then(r => r.json());
  return <Product data={product} />;
}

// Caching controls:
// fetch(url, { cache: 'force-cache' })  // SSG-like
// fetch(url, { cache: 'no-store' })     // SSR-like
// fetch(url, { next: { revalidate: 60 } })  // ISR-like


// REMIX:
// Explicit loader/action separation

export async function loader({ params }) {
  // Runs on server for GET requests
  const product = await db.products.find(params.id);
  return json(product);
}

export async function action({ request }) {
  // Runs on server for POST/PUT/DELETE
  const formData = await request.formData();
  await db.products.update(formData);
  return redirect('/products');
}

export default function ProductPage() {
  const product = useLoaderData();  // Data from loader
  return <Product data={product} />;
}


// SVELTEKIT:
// Separate load files

// +page.server.ts
export async function load({ params }) {
  return {
    product: await getProduct(params.id)
  };
}

// +page.svelte
<script>
  export let data;  // Receives load() return value
</script>

<h1>{data.product.name}</h1>


// ASTRO:
// Frontmatter-based (build-time by default)

---
const product = await fetch('...').then(r => r.json());
---

<h1>{product.name}</h1>
```

### Adapter Pattern: Deploy Anywhere

SvelteKit pioneered the adapter pattern, now common across frameworks:

```
YOUR CODE
    │
    ▼
┌─────────────────────────────┐
│       Build Process          │
│  (Framework-specific)        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         Adapter              │
│  (Platform-specific)         │
└──────────────┬──────────────┘
               │
    ┌──────────┼──────────┬──────────┐
    ▼          ▼          ▼          ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│ Node  │ │Vercel │ │ CF    │ │Netlify│
│Server │ │Funcs  │ │Workers│ │Funcs  │
└───────┘ └───────┘ └───────┘ └───────┘
```

**How adapters work:**

```javascript
// Framework produces platform-agnostic output:
// - Static files (HTML, CSS, JS, images)
// - Server functions (request handlers)
// - Prerender information

// ADAPTER transforms to platform-specific format:

// adapter-node:
// Creates Node.js server with Express/Polka

// adapter-vercel:
// Creates Vercel Functions configuration
// Outputs to .vercel/output directory

// adapter-cloudflare:
// Creates Worker script
// Uses Cloudflare's fetch handler format

// adapter-static:
// Generates only static files
// No server runtime needed
```

### Edge Runtime: The Modern Frontier

Edge computing brings code execution to CDN nodes:

```javascript
// TRADITIONAL SSR:
// Request: Tokyo user → CDN (Tokyo) → Origin Server (Virginia)
//                                          ↓
//                                    Render HTML
//                                          ↓
// Response: Tokyo user ← CDN (Tokyo) ← Origin Server (Virginia)
// 
// Latency: 150-300ms for server response

// EDGE SSR:
// Request: Tokyo user → Edge Node (Tokyo)
//                            ↓
//                      Render HTML locally
//                            ↓
// Response: Tokyo user ← Edge Node (Tokyo)
//
// Latency: 10-50ms for server response
```

**Edge runtime limitations:**

```javascript
// Edge runtime is NOT full Node.js
// It's a minimal JavaScript environment

// AVAILABLE:
// - fetch() API
// - Web Crypto API
// - Basic JavaScript APIs

// NOT AVAILABLE:
// - fs (file system)
// - Native Node modules
// - Full npm ecosystem
// - Long-running processes

// NEXT.JS EDGE RUNTIME:
export const runtime = 'edge';

export async function GET(request) {
  // Must use fetch-based APIs
  const data = await fetch('https://api.example.com/data');
  return Response.json(await data.json());
}
```

### Framework Philosophies Explained

**Next.js Philosophy: "The Platform for React"**
```
- Embrace React fully (including experimental features)
- Provide every possible rendering mode
- Deep Vercel integration
- Enterprise-ready out of the box
```

**Remix Philosophy: "Web Standards First"**
```
- Use browser APIs, not framework abstractions
- Forms work without JavaScript
- Progressive enhancement by default
- Don't fight the platform
```

**Astro Philosophy: "Less JavaScript is More"**
```
- Static by default, dynamic when needed
- Islands of interactivity, not oceans
- Use any UI framework, or none
- Content sites deserve great tools
```

**SvelteKit Philosophy: "Compiled, Not Runtime"**
```
- Move work to compile time
- Smaller bundles through compilation
- Unified platform via adapters
- Developer experience matters
```

### Build Process: What Actually Happens

When you run `npm run build`:

```
┌──────────────────────────────────────────────────────────────────┐
│                     BUILD PIPELINE                                │
└──────────────────────────────────────────────────────────────────┘

STEP 1: ROUTE ANALYSIS
├── Scan file system for routes
├── Identify static vs dynamic routes
├── Build route manifest
└── Determine data dependencies

STEP 2: CODE TRANSFORMATION
├── Transpile TypeScript → JavaScript
├── Transform JSX → createElement calls
├── Process CSS (PostCSS, Tailwind, etc.)
└── Optimize imports (tree shaking)

STEP 3: BUNDLING
├── Create entry points per route
├── Code split appropriately
├── Generate chunk hashes
└── Create source maps

STEP 4: STATIC GENERATION (SSG routes)
├── Execute getStaticProps / load functions
├── Render components to HTML strings
├── Write HTML files to output directory
└── Copy static assets

STEP 5: SERVER BUNDLE (SSR routes)
├── Bundle server-side code separately
├── Exclude client-only code
├── Generate server entry points
└── Create serverless function bundles (if applicable)

STEP 6: OPTIMIZATION
├── Minify JavaScript (Terser, ESBuild)
├── Minify CSS
├── Optimize images
├── Generate asset manifests
└── Create preload hints

OUTPUT:
├── .next/ or .output/ or dist/
│   ├── static/           (CDN-served assets)
│   ├── server/           (Server functions)
│   ├── routes-manifest   (Route configuration)
│   └── build-manifest    (Asset mapping)
```

### Choosing the Right Framework: Decision Tree

```
START: What UI library does your team know?
│
├─► React
│   │
│   └─► What's your priority?
│       ├─► Maximum flexibility, enterprise features → Next.js
│       ├─► Web standards, progressive enhancement → Remix
│       └─► Static content with some interactivity → Astro (with React islands)
│
├─► Vue
│   │
│   └─► Full-stack Vue app → Nuxt
│       Static with Vue components → Astro (with Vue islands)
│
├─► Svelte
│   │
│   └─► Full-stack Svelte → SvelteKit
│       Static with Svelte components → Astro (with Svelte islands)
│
├─► None / Learning
│   │
│   └─► What are you building?
│       ├─► Content site (blog, docs) → Astro
│       ├─► Web application → SvelteKit (easiest learning curve)
│       └─► Enterprise app → Next.js (most resources, hiring)
│
└─► Maximum Performance
    │
    └─► Static content → Astro (zero JS by default)
        Interactive app → Qwik (resumable, no hydration)
```

---

## For Framework Authors: Building Meta-Frameworks

> **Implementation Note**: The patterns and code examples below represent one proven approach to building meta-frameworks. Meta-framework architecture varies significantly—Next.js tightly integrates with React, Nuxt builds on Vue's ecosystem, and Astro is UI-agnostic. The direction shown here provides foundational architecture that most meta-frameworks share. Your implementation will depend on your target UI framework, deployment strategy, and the developer experience you want to provide.

### Core Meta-Framework Architecture

```javascript
// META-FRAMEWORK CORE ARCHITECTURE

class MetaFramework {
  constructor(config) {
    this.config = config;
    this.plugins = [];
    this.hooks = new HookSystem();
    this.router = new FileBasedRouter();
    this.bundler = new Bundler();
    this.renderer = new UniversalRenderer();
  }
  
  // Plugin system
  use(plugin) {
    this.plugins.push(plugin);
    plugin.install?.(this);
  }
  
  // Development server
  async dev() {
    await this.hooks.call('beforeDev');
    
    // Scan routes
    const routes = await this.router.scan(this.config.pagesDir);
    
    // Start HMR bundler
    await this.bundler.startDev({
      routes,
      onUpdate: (updates) => this.handleHMR(updates),
    });
    
    // Start dev server
    const server = await this.createDevServer(routes);
    
    await this.hooks.call('afterDev', { server });
  }
  
  // Production build
  async build() {
    await this.hooks.call('beforeBuild');
    
    const routes = await this.router.scan(this.config.pagesDir);
    
    // Client build
    const clientManifest = await this.bundler.buildClient(routes);
    
    // Server build  
    const serverManifest = await this.bundler.buildServer(routes);
    
    // Static generation
    await this.generateStatic(routes, { clientManifest, serverManifest });
    
    // Generate deployment artifacts
    await this.adapter.generate(this.config);
    
    await this.hooks.call('afterBuild');
  }
}

// Hook system for extensibility
class HookSystem {
  constructor() {
    this.hooks = new Map();
  }
  
  on(name, handler) {
    if (!this.hooks.has(name)) {
      this.hooks.set(name, []);
    }
    this.hooks.get(name).push(handler);
  }
  
  async call(name, context = {}) {
    const handlers = this.hooks.get(name) || [];
    for (const handler of handlers) {
      await handler(context);
    }
  }
}
```

### Building the Plugin System

```javascript
// PLUGIN SYSTEM IMPLEMENTATION

class PluginManager {
  constructor(framework) {
    this.framework = framework;
    this.plugins = [];
  }
  
  async register(plugin) {
    // Validate plugin
    if (!plugin.name) {
      throw new Error('Plugin must have a name');
    }
    
    // Check dependencies
    for (const dep of plugin.dependencies || []) {
      if (!this.plugins.find(p => p.name === dep)) {
        throw new Error(`Plugin ${plugin.name} requires ${dep}`);
      }
    }
    
    // Initialize plugin
    const instance = await plugin.setup?.(this.framework) || {};
    
    // Register hooks
    if (plugin.hooks) {
      for (const [hook, handler] of Object.entries(plugin.hooks)) {
        this.framework.hooks.on(hook, handler.bind(instance));
      }
    }
    
    // Add Vite plugins
    if (plugin.vitePlugins) {
      this.framework.bundler.addPlugins(plugin.vitePlugins);
    }
    
    this.plugins.push({ ...plugin, instance });
  }
}

// Example plugin
const imageOptimizationPlugin = {
  name: 'image-optimization',
  
  async setup(framework) {
    return {
      cache: new Map(),
    };
  },
  
  hooks: {
    async beforeBuild() {
      console.log('Preparing image optimization...');
    },
    
    async transformAsset(context) {
      if (!isImage(context.path)) return;
      
      const optimized = await optimizeImage(context.content, {
        quality: 80,
        formats: ['webp', 'avif'],
      });
      
      return optimized;
    },
  },
  
  vitePlugins: [
    {
      name: 'vite-plugin-images',
      transform(code, id) {
        if (id.endsWith('.jpg') || id.endsWith('.png')) {
          // Transform image imports
        }
      },
    },
  ],
};
```

### Implementing Adapters (Deploy Anywhere)

```javascript
// ADAPTER SYSTEM IMPLEMENTATION

class AdapterManager {
  constructor() {
    this.adapters = new Map();
  }
  
  register(name, adapter) {
    this.adapters.set(name, adapter);
  }
  
  async build(adapterName, context) {
    const adapter = this.adapters.get(adapterName);
    if (!adapter) {
      throw new Error(`Unknown adapter: ${adapterName}`);
    }
    
    return adapter.adapt(context);
  }
}

// Node.js adapter
const nodeAdapter = {
  name: 'node',
  
  async adapt(context) {
    const { serverEntry, staticDir, outputDir } = context;
    
    // Generate Node.js server
    const serverCode = `
import { createServer } from 'http';
import { handler } from './handler.js';

const server = createServer(async (req, res) => {
  const response = await handler(req);
  res.writeHead(response.status, Object.fromEntries(response.headers));
  res.end(response.body);
});

server.listen(process.env.PORT || 3000);
`;
    
    await fs.writeFile(`${outputDir}/index.js`, serverCode);
    await fs.cp(staticDir, `${outputDir}/static`, { recursive: true });
    
    return { type: 'node', entry: 'index.js' };
  },
};

// Cloudflare Workers adapter
const cloudflareAdapter = {
  name: 'cloudflare',
  
  async adapt(context) {
    const { serverEntry, staticDir, outputDir } = context;
    
    // Generate Worker script
    const workerCode = `
import { handler } from './handler.js';

export default {
  async fetch(request, env, ctx) {
    // Try static files first
    const url = new URL(request.url);
    const staticResponse = await env.ASSETS.fetch(request);
    if (staticResponse.status !== 404) return staticResponse;
    
    // Fall back to SSR handler
    return handler(request, env, ctx);
  },
};
`;
    
    await fs.writeFile(`${outputDir}/_worker.js`, workerCode);
    
    // Generate wrangler.toml
    const wranglerConfig = `
name = "${context.config.name}"
main = "_worker.js"
compatibility_date = "2024-01-01"

[site]
bucket = "./static"
`;
    
    await fs.writeFile(`${outputDir}/wrangler.toml`, wranglerConfig);
    
    return { type: 'cloudflare-workers' };
  },
};

// Vercel adapter
const vercelAdapter = {
  name: 'vercel',
  
  async adapt(context) {
    const { routes, serverEntry, staticDir, outputDir } = context;
    
    // Generate Vercel config
    const vercelConfig = {
      version: 3,
      routes: [
        // Static assets
        { src: '/static/(.*)', dest: '/static/$1' },
        // API routes
        ...routes.filter(r => r.type === 'api').map(r => ({
          src: r.path,
          dest: `/api${r.path}`,
        })),
        // SSR routes
        { src: '/(.*)', dest: '/render' },
      ],
      functions: {
        'api/**/*.js': { runtime: 'nodejs20.x' },
        'render.js': { runtime: 'nodejs20.x' },
      },
    };
    
    await fs.writeFile(
      `${outputDir}/vercel.json`, 
      JSON.stringify(vercelConfig, null, 2)
    );
    
    // Generate serverless functions
    for (const route of routes) {
      if (route.type === 'api') {
        await generateAPIFunction(route, outputDir);
      }
    }
    
    // Generate SSR function
    await generateSSRFunction(context, outputDir);
    
    return { type: 'vercel' };
  },
};
```

### Server Component Architecture

```javascript
// SERVER COMPONENT IMPLEMENTATION

class ServerComponentRuntime {
  constructor() {
    this.componentCache = new Map();
    this.clientReferences = new Map();
  }
  
  // Mark component as client boundary
  registerClientReference(id, exportName) {
    this.clientReferences.set(`${id}#${exportName}`, {
      id,
      exportName,
      chunks: [], // Filled during build
    });
  }
  
  // Render server component to RSC payload
  async renderToPayload(element, context) {
    const payload = [];
    await this.walkTree(element, payload, context);
    return payload;
  }
  
  async walkTree(element, payload, context) {
    if (!element) return null;
    
    // Primitive values
    if (typeof element !== 'object') {
      return element;
    }
    
    // Array of children
    if (Array.isArray(element)) {
      return Promise.all(element.map(e => this.walkTree(e, payload, context)));
    }
    
    const { type, props } = element;
    
    // HTML element
    if (typeof type === 'string') {
      return {
        $$typeof: Symbol.for('react.element'),
        type,
        props: {
          ...props,
          children: await this.walkTree(props.children, payload, context),
        },
      };
    }
    
    // Client component reference
    if (this.clientReferences.has(type.$$id)) {
      const ref = this.clientReferences.get(type.$$id);
      return {
        $$typeof: Symbol.for('react.client.reference'),
        $$id: ref.id,
        $$name: ref.exportName,
        props: await this.serializeProps(props),
      };
    }
    
    // Server component - execute
    const result = await type(props);
    return this.walkTree(result, payload, context);
  }
  
  // Serialize props for client
  async serializeProps(props) {
    const serialized = {};
    
    for (const [key, value] of Object.entries(props)) {
      if (typeof value === 'function') {
        // Server actions become references
        serialized[key] = {
          $$typeof: Symbol.for('react.server.reference'),
          $$id: registerServerAction(value),
        };
      } else {
        serialized[key] = value;
      }
    }
    
    return serialized;
  }
}

// Build-time transform for 'use client' directive
function transformClientDirective(code, id) {
  if (!code.startsWith("'use client'") && !code.startsWith('"use client"')) {
    return null;
  }
  
  // Parse exports
  const exports = parseExports(code);
  
  // Generate proxy module for server
  const serverProxy = exports.map(exp => 
    `export const ${exp} = { $$id: "${id}#${exp}", $$typeof: Symbol.for('react.client.reference') };`
  ).join('\n');
  
  return serverProxy;
}
```

### Build Pipeline Orchestration

```javascript
// BUILD PIPELINE ORCHESTRATION

class BuildPipeline {
  constructor(config) {
    this.config = config;
    this.steps = [];
  }
  
  addStep(step) {
    this.steps.push(step);
  }
  
  async run() {
    const context = {
      config: this.config,
      routes: [],
      assets: new Map(),
      manifest: {},
    };
    
    for (const step of this.steps) {
      console.log(`[build] ${step.name}...`);
      const start = Date.now();
      
      try {
        await step.execute(context);
        console.log(`[build] ${step.name} (${Date.now() - start}ms)`);
      } catch (error) {
        console.error(`[build] ${step.name} failed:`, error);
        throw error;
      }
    }
    
    return context;
  }
}

// Standard build steps
const buildSteps = [
  {
    name: 'scan-routes',
    async execute(ctx) {
      ctx.routes = await scanRoutes(ctx.config.pagesDir);
    },
  },
  {
    name: 'bundle-client',
    async execute(ctx) {
      ctx.clientBuild = await bundleClient({
        routes: ctx.routes,
        outDir: `${ctx.config.outDir}/client`,
      });
    },
  },
  {
    name: 'bundle-server',
    async execute(ctx) {
      ctx.serverBuild = await bundleServer({
        routes: ctx.routes,
        outDir: `${ctx.config.outDir}/server`,
      });
    },
  },
  {
    name: 'prerender-static',
    async execute(ctx) {
      const staticRoutes = ctx.routes.filter(r => !r.isDynamic);
      await Promise.all(staticRoutes.map(r => prerenderRoute(r, ctx)));
    },
  },
  {
    name: 'generate-manifest',
    async execute(ctx) {
      ctx.manifest = {
        routes: ctx.routes.map(r => ({
          path: r.path,
          type: r.type,
          prerendered: r.prerendered,
        })),
        assets: Object.fromEntries(ctx.assets),
        buildId: Date.now().toString(36),
      };
      
      await fs.writeFile(
        `${ctx.config.outDir}/manifest.json`,
        JSON.stringify(ctx.manifest, null, 2)
      );
    },
  },
  {
    name: 'adapt',
    async execute(ctx) {
      const adapter = getAdapter(ctx.config.adapter);
      await adapter.adapt(ctx);
    },
  },
];
```

## Related Skills

- See [web-app-architectures](../web-app-architectures/SKILL.md) for SPA vs MPA
- See [rendering-patterns](../rendering-patterns/SKILL.md) for SSR/SSG/ISR
- See [hydration-patterns](../hydration-patterns/SKILL.md) for hydration strategies
- See [routing-patterns](../routing-patterns/SKILL.md) for routing concepts
