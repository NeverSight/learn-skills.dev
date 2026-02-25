---
name: routing-patterns
description: Explains client-side routing, server-side routing, file-based routing, and navigation patterns in web applications. Use when implementing routing, understanding how navigation works in SPAs vs MPAs, or configuring routes in meta-frameworks.
---

# Routing Patterns

## Overview

Routing determines how URLs map to content and how navigation between pages works. The approach differs significantly between traditional server-rendered apps and modern SPAs.

## Server-Side Routing

**Server determines what to render based on the URL.**

### How It Works

```
1. User navigates to /about
2. Browser sends request to server
3. Server matches /about to handler
4. Server renders HTML
5. Server sends complete HTML response
6. Browser loads new page (full reload)
```

### Characteristics

```
Request: GET /products/123

Server:
  Route table:
    /            → HomeController
    /about       → AboutController
    /products/:id → ProductController  ← matches

  ProductController:
    - Fetches product 123
    - Renders HTML
    - Returns response
```

### Pros and Cons

| Pros | Cons |
|------|------|
| SEO-friendly (full HTML) | Full page reload |
| Simple mental model | Slower navigation |
| Works without JavaScript | State lost between pages |
| Direct URL to content mapping | Server must handle every route |

## Client-Side Routing

**JavaScript handles routing in the browser, no server round-trip for navigation.**

### How It Works

```
1. Initial: Browser loads app shell + JS
2. User clicks link
3. JavaScript intercepts click (preventDefault)
4. JS updates URL using History API
5. JS renders new view/component
6. No server request for HTML
```

### The History API

```javascript
// Push new URL to history (no page reload)
history.pushState({ page: 'about' }, '', '/about');

// Replace current URL
history.replaceState({ page: 'home' }, '', '/');

// Listen for back/forward navigation
window.addEventListener('popstate', (event) => {
  // Render based on current URL
  renderRoute(window.location.pathname);
});
```

### Basic Router Implementation

```javascript
// Simplified client-side router concept
class Router {
  constructor() {
    this.routes = {};
    window.addEventListener('popstate', () => this.handleRoute());
  }

  register(path, component) {
    this.routes[path] = component;
  }

  navigate(path) {
    history.pushState({}, '', path);
    this.handleRoute();
  }

  handleRoute() {
    const path = window.location.pathname;
    const component = this.routes[path] || this.routes['/404'];
    component.render();
  }
}

// Usage
router.register('/about', AboutComponent);
router.register('/products/:id', ProductComponent);
```

### Link Interception

```javascript
// Intercept link clicks for client-side navigation
document.addEventListener('click', (e) => {
  const link = e.target.closest('a');
  if (link && link.href.startsWith(window.location.origin)) {
    e.preventDefault();
    router.navigate(link.pathname);
  }
});
```

## File-Based Routing

**Route structure derived from file system layout.**

### Common Patterns

```
File System                          URL
──────────────────────────────       ─────────────
pages/index.tsx                  →   /
pages/about.tsx                  →   /about
pages/blog/index.tsx             →   /blog
pages/blog/[slug].tsx            →   /blog/:slug
pages/docs/[...path].tsx         →   /docs/*
pages/[category]/[id].tsx        →   /:category/:id
```

### Framework Implementations

**Next.js (App Router):**
```
app/
├── page.tsx                    → /
├── about/page.tsx              → /about
├── blog/[slug]/page.tsx        → /blog/:slug
└── (marketing)/                → Route group (no URL segment)
    └── pricing/page.tsx        → /pricing
```

**SvelteKit:**
```
src/routes/
├── +page.svelte                → /
├── about/+page.svelte          → /about
├── blog/[slug]/+page.svelte    → /blog/:slug
└── [[optional]]/+page.svelte   → / or /:optional
```

**Remix:**
```
app/routes/
├── _index.tsx                  → /
├── about.tsx                   → /about
├── blog._index.tsx             → /blog
├── blog.$slug.tsx              → /blog/:slug
└── $.tsx                       → Catch-all (splat)
```

## Dynamic Routes

### Parameter Types

```
Static:     /about          → Exact match
Dynamic:    /blog/[slug]    → Single parameter
Catch-all:  /docs/[...path] → Multiple segments
Optional:   /[[locale]]/    → With or without parameter
```

### Parameter Access

**Concept (framework-agnostic):**
```javascript
// URL: /products/shoes/nike-air-max

// Route: /products/[category]/[id]
// Parameters: { category: 'shoes', id: 'nike-air-max' }

// Route: /products/[...path]
// Parameters: { path: ['shoes', 'nike-air-max'] }
```

## Route Groups and Layouts

### Nested Layouts

```
app/
├── layout.tsx              → Root layout (applies to all)
├── (shop)/
│   ├── layout.tsx          → Shop layout (header, cart)
│   ├── products/page.tsx   → /products (uses shop layout)
│   └── cart/page.tsx       → /cart (uses shop layout)
└── (marketing)/
    ├── layout.tsx          → Marketing layout (different nav)
    ├── about/page.tsx      → /about (uses marketing layout)
    └── pricing/page.tsx    → /pricing (uses marketing layout)
```

### Parallel Routes

Load multiple views simultaneously:

```
app/
├── @sidebar/
│   └── page.tsx            → Sidebar content
├── @main/
│   └── page.tsx            → Main content
└── layout.tsx              → Renders both in parallel
```

### Intercepting Routes

Handle routes differently in different contexts:

```
app/
├── photos/[id]/page.tsx        → Full page view
├── @modal/(.)photos/[id]/       → Modal overlay (when navigating internally)
│   └── page.tsx
└── feed/page.tsx                → Grid with links to photos
```

## Navigation Patterns

### Declarative Navigation

```jsx
// React Router / Next.js
<Link href="/about">About</Link>

// Vue Router
<router-link to="/about">About</router-link>

// SvelteKit
<a href="/about">About</a>  <!-- Enhanced automatically -->
```

### Programmatic Navigation

```javascript
// React Router
const navigate = useNavigate();
navigate('/dashboard');

// Next.js
const router = useRouter();
router.push('/dashboard');

// Vue Router
router.push('/dashboard');

// SvelteKit
import { goto } from '$app/navigation';
goto('/dashboard');
```

### Navigation Options

```javascript
// Replace history (no back button)
router.replace('/login');

// With query parameters
router.push('/search?q=term');

// With hash
router.push('/docs#section');

// Scroll to top
router.push('/page', { scroll: true });

// Shallow routing (no data refetch)
router.push('/page', { shallow: true });
```

## Route Protection

### Authentication Guards

```javascript
// Middleware pattern (Next.js)
export function middleware(request) {
  const token = request.cookies.get('auth-token');
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}

// Route-level check
export async function loader({ request }) {
  const user = await getUser(request);
  if (!user) {
    throw redirect('/login');
  }
  return { user };
}
```

### Authorization Patterns

```javascript
// Role-based routing
if (!user.roles.includes('admin')) {
  redirect('/unauthorized');
}

// Feature flags
if (!features.newDashboard) {
  redirect('/legacy-dashboard');
}
```

## URL State Management

### Query Parameters

```javascript
// Read query params
const searchParams = useSearchParams();
const query = searchParams.get('q');

// Update query params
const params = new URLSearchParams(searchParams);
params.set('page', '2');
router.push(`/products?${params.toString()}`);
```

### Hash-Based State

```javascript
// URL: /docs#installation
// Scroll to section
useEffect(() => {
  const hash = window.location.hash;
  if (hash) {
    document.querySelector(hash)?.scrollIntoView();
  }
}, []);
```

### State in URL vs Component

```
URL State (shareable, bookmarkable):
  - Current page, filters, search query
  - Tab selection
  - Modal open state (sometimes)

Component State (ephemeral):
  - Form input before submission
  - Hover/focus states
  - Temporary UI state
```

## Performance Patterns

### Prefetching

```jsx
// Next.js - automatic on hover
<Link href="/about" prefetch={true}>About</Link>

// Manual prefetch
router.prefetch('/dashboard');
```

### Code Splitting by Route

```javascript
// Lazy load route components
const Dashboard = lazy(() => import('./Dashboard'));

// Routes load only when accessed
<Route path="/dashboard" element={
  <Suspense fallback={<Loading />}>
    <Dashboard />
  </Suspense>
} />
```

### Route Transitions

```javascript
// Loading states during navigation
const navigation = useNavigation();

{navigation.state === 'loading' && <LoadingBar />}
```

## Common Routing Pitfalls

### 1. Breaking the Back Button

```javascript
// Bad: Replaces every navigation
router.replace('/page');  // Can't go back

// Good: Push for normal navigation
router.push('/page');  // Back button works
```

### 2. Not Handling 404s

```javascript
// Ensure catch-all route exists
// app/[...not-found]/page.tsx or pages/404.tsx
```

### 3. Client-Only Routes in SSR

```javascript
// Bad: useSearchParams in server component
// Causes hydration mismatch

// Good: Use in client component or read in middleware
```

### 4. Hash URLs for SEO Content

```javascript
// Bad: /#/products/123 (not indexable)
// Good: /products/123 (indexable)
```

---

## Deep Dive: Understanding Routing From First Principles

### What is a URL? Anatomy of Web Addresses

Before understanding routing, you must understand URLs (Uniform Resource Locators):

```
https://www.example.com:443/products/shoes?color=red&size=10#reviews
│       │              │   │              │                    │
│       │              │   │              │                    └─ Fragment (client-only, not sent to server)
│       │              │   │              │
│       │              │   │              └─ Query String (key-value pairs)
│       │              │   │
│       │              │   └─ Pathname (the route)
│       │              │
│       │              └─ Port (usually implicit: 80 for http, 443 for https)
│       │
│       └─ Hostname (domain)
│
└─ Protocol (scheme)
```

**Key insight:** Only `protocol`, `hostname`, `port`, `pathname`, and `query` are sent to the server. The `fragment` (#hash) stays in the browser.

### The History of Web Routing

**Era 1: File-Based (1990s)**
```
URL: /products/shoes.html
Server: Find file at /var/www/products/shoes.html, return it
```
URLs literally mapped to files on disk.

**Era 2: Dynamic Routing (2000s)**
```
URL: /products.php?id=123
Server: Execute products.php, which reads $_GET['id'] = 123
```
Server-side scripts processed parameters.

**Era 3: RESTful Routes (2010s)**
```
URL: /products/123
Server: Route pattern /products/:id matches, extract id=123
```
Clean URLs with pattern matching.

**Era 4: Client-Side Routing (2010s-present)**
```
URL: /products/123
Client: JavaScript intercepts, renders Product component with id=123
Server: May never see this request (after initial load)
```

### How Server-Side Routing Actually Works

When a server receives a request, it must decide what to do:

```javascript
// Express.js example - simplified internal logic
class Router {
  constructor() {
    this.routes = [];
  }
  
  // Register route
  get(pattern, handler) {
    this.routes.push({
      method: 'GET',
      pattern: this.parsePattern(pattern),  // /users/:id → regex
      handler
    });
  }
  
  // Pattern to regex conversion
  parsePattern(pattern) {
    // /users/:id → /^\/users\/([^\/]+)$/
    // /posts/:id/comments → /^\/posts\/([^\/]+)\/comments$/
    const regexStr = pattern
      .replace(/:([^/]+)/g, '([^/]+)')  // :param → capture group
      .replace(/\//g, '\\/');            // Escape slashes
    return new RegExp(`^${regexStr}$`);
  }
  
  // Handle incoming request
  handle(req, res) {
    const { method, url } = req;
    const pathname = new URL(url, 'http://localhost').pathname;
    
    // Find matching route
    for (const route of this.routes) {
      if (route.method !== method) continue;
      
      const match = pathname.match(route.pattern);
      if (match) {
        // Extract params
        req.params = this.extractParams(route.pattern, match);
        return route.handler(req, res);
      }
    }
    
    // No match - 404
    res.status(404).send('Not Found');
  }
}
```

**Route matching order matters:**
```javascript
// These are checked in order
app.get('/users/new', newUserHandler);     // Must be BEFORE :id
app.get('/users/:id', getUserHandler);     // Would match "new" as id otherwise

// Request: GET /users/new
// Check 1: /users/new matches! → newUserHandler
// Never reaches /users/:id

// Request: GET /users/123
// Check 1: /users/new doesn't match
// Check 2: /users/:id matches! → getUserHandler with id=123
```

### How Client-Side Routing Intercepts Browser Behavior

The browser has default navigation behavior. Client-side routing overrides it:

```javascript
// DEFAULT BROWSER BEHAVIOR:
// 1. User clicks <a href="/about">
// 2. Browser sees href attribute
// 3. Browser sends GET request to /about
// 4. Browser receives HTML response
// 5. Browser replaces entire page

// SPA INTERCEPTION:
document.addEventListener('click', (event) => {
  // Find the link element (might be nested: <a><span>Click</span></a>)
  const anchor = event.target.closest('a');
  if (!anchor) return;  // Not a link click
  
  // Check if it's an internal link
  const url = new URL(anchor.href);
  if (url.origin !== window.location.origin) return;  // External link
  
  // Check for special cases
  if (anchor.hasAttribute('download')) return;  // Download link
  if (anchor.target === '_blank') return;       // New tab
  if (event.metaKey || event.ctrlKey) return;   // Cmd/Ctrl+click
  
  // NOW we intercept
  event.preventDefault();  // STOP browser's default behavior
  
  // Handle navigation ourselves
  navigateTo(url.pathname + url.search + url.hash);
});

function navigateTo(path) {
  // Update URL bar without page reload
  window.history.pushState({ path }, '', path);
  
  // Render the appropriate component
  renderRoute(path);
}
```

### The History API in Detail

The History API is what makes SPAs possible without hash URLs:

```javascript
// The history stack is like browser tabs' back/forward buttons
// But for a single tab:

// Initial state
// History: [ {url: '/'} ]
//                  ↑ current

// User navigates to /about
history.pushState({ page: 'about' }, '', '/about');
// History: [ {url: '/'}, {url: '/about'} ]
//                              ↑ current

// User navigates to /contact
history.pushState({ page: 'contact' }, '', '/contact');
// History: [ {url: '/'}, {url: '/about'}, {url: '/contact'} ]
//                                              ↑ current

// User clicks back button
// Browser fires 'popstate' event
// History: [ {url: '/'}, {url: '/about'}, {url: '/contact'} ]
//                              ↑ current (moved back)

// User clicks forward button
// Browser fires 'popstate' event again
// History: [ {url: '/'}, {url: '/about'}, {url: '/contact'} ]
//                                              ↑ current (moved forward)

// IMPORTANT: pushState does NOT fire popstate
// Only back/forward buttons fire popstate
// Your router must handle both!
```

**Handling popstate:**
```javascript
window.addEventListener('popstate', (event) => {
  // event.state contains the state object from pushState
  // If user used back button, this fires with previous state
  
  // The URL has ALREADY changed when this fires
  const currentPath = window.location.pathname;
  
  renderRoute(currentPath);
});
```

### Hash Routing vs History Routing

Before the History API (HTML5, ~2010), SPAs used hash-based routing:

```javascript
// HASH ROUTING:
// URLs look like: /#/about, /#/products/123

// Why hashes? The hash fragment is NEVER sent to server
// So changing it doesn't trigger page reload

// Navigation:
window.location.hash = '#/about';

// Listening for changes:
window.addEventListener('hashchange', () => {
  const route = window.location.hash.slice(1);  // Remove #
  renderRoute(route);
});

// PROBLEMS WITH HASH ROUTING:
// 1. SEO: Crawlers ignore hash fragments
//    /products/shoes and /products/shoes#/details are same URL to Google
//
// 2. Ugly URLs: example.com/#/products/shoes vs example.com/products/shoes
//
// 3. Server can't respond to routes: everything goes to root
```

**History routing advantages:**
```javascript
// HISTORY ROUTING:
// URLs look like: /about, /products/123 (clean!)

// Navigation:
history.pushState({}, '', '/about');

// Server sees the real URL
// SEO works properly
// Clean, professional URLs

// REQUIREMENT: Server must handle all routes
// Server must return the SPA for ANY route
// Otherwise: /products/123 → 404 if user refreshes
```

### File-Based Routing: How It Works Internally

Meta-frameworks use file system as routing configuration:

```javascript
// At build time, the framework scans your files:

// File structure:
// app/
// ├── page.tsx          → /
// ├── about/page.tsx    → /about
// └── blog/[slug]/page.tsx → /blog/:slug

// Framework generates route table:
const routes = [
  { pattern: /^\/$/, component: () => import('./app/page.tsx') },
  { pattern: /^\/about$/, component: () => import('./app/about/page.tsx') },
  { pattern: /^\/blog\/([^/]+)$/, component: () => import('./app/blog/[slug]/page.tsx') },
];

// Dynamic segments become route parameters:
// [slug] → :slug → captured as params.slug
// [id] → :id → captured as params.id
// [...path] → * → captured as params.path (array)
```

**Why file-based routing became popular:**

```
EXPLICIT ROUTING (React Router, Express):
- Route definitions separate from components
- Easy to have mismatched routes/files
- Must manually update both

// routes.tsx
<Route path="/products/:id" component={ProductPage} />

// ProductPage.tsx (might be anywhere)
export function ProductPage() { ... }


FILE-BASED ROUTING:
- Location IS the route
- Impossible to have orphan components
- Adding page = adding route automatically

// app/products/[id]/page.tsx (location defines route)
export default function ProductPage() { ... }
```

### Route Parameters: Extraction and Typing

Understanding how parameters flow from URL to code:

```javascript
// URL: /products/shoes/nike-air-max/reviews

// Route pattern: /products/[category]/[productId]/reviews
// Regex: /^\/products\/([^/]+)\/([^/]+)\/reviews$/

// Matching process:
const match = url.match(pattern);
// match = [
//   '/products/shoes/nike-air-max/reviews',  // Full match
//   'shoes',                                   // Group 1: category
//   'nike-air-max'                            // Group 2: productId
// ]

// Framework extracts to params object:
const params = {
  category: 'shoes',
  productId: 'nike-air-max'
};

// Your component receives these:
function ProductReviewsPage({ params }) {
  console.log(params.category);   // 'shoes'
  console.log(params.productId);  // 'nike-air-max'
}
```

**Catch-all routes:**
```javascript
// Route: /docs/[...path]
// URL: /docs/getting-started/installation/windows

// The [...path] captures EVERYTHING after /docs/
const params = {
  path: ['getting-started', 'installation', 'windows']  // Array!
};

// Useful for:
// - Documentation with arbitrary depth
// - File browsers
// - Fallback/404 routes
```

### Nested Routes and Layouts: The Component Tree

Nested routing creates component hierarchies:

```
URL: /dashboard/settings/profile

Route hierarchy:
app/
├── layout.tsx           ← Root layout (nav, footer)
└── dashboard/
    ├── layout.tsx       ← Dashboard layout (sidebar)
    └── settings/
        ├── layout.tsx   ← Settings layout (tabs)
        └── profile/
            └── page.tsx ← Profile content

Renders as:
<RootLayout>              {/* Always present */}
  <DashboardLayout>       {/* Present for /dashboard/* */}
    <SettingsLayout>      {/* Present for /dashboard/settings/* */}
      <ProfilePage />     {/* The actual content */}
    </SettingsLayout>
  </DashboardLayout>
</RootLayout>
```

**Why nested layouts matter:**

```jsx
// WITHOUT nested layouts:
// Every page must include all wrappers

function DashboardSettingsProfilePage() {
  return (
    <RootLayout>
      <DashboardSidebar />
      <SettingsTabs />
      <ProfileForm />   {/* Actual unique content */}
    </RootLayout>
  );
}

function DashboardSettingsSecurityPage() {
  return (
    <RootLayout>           {/* Duplicated */}
      <DashboardSidebar /> {/* Duplicated */}
      <SettingsTabs />     {/* Duplicated */}
      <SecurityForm />     {/* Actual unique content */}
    </RootLayout>
  );
}

// WITH nested layouts:
// Layouts persist, only inner content changes

// Navigating from /dashboard/settings/profile
// to /dashboard/settings/security:
// - RootLayout: PRESERVED (no re-render)
// - DashboardLayout: PRESERVED (no re-render)
// - SettingsLayout: PRESERVED (no re-render)
// - Only ProfilePage → SecurityPage changes!
```

### Route Guards and Middleware: The Request Pipeline

Routes often need protection or preprocessing:

```javascript
// THE MIDDLEWARE CHAIN:
// Request flows through layers before reaching handler

// Request: GET /dashboard/admin

// Layer 1: Logging middleware
function loggingMiddleware(request, next) {
  console.log(`${request.method} ${request.url}`);
  return next(request);  // Continue to next middleware
}

// Layer 2: Authentication middleware
function authMiddleware(request, next) {
  const token = request.cookies.get('auth-token');
  if (!token) {
    return redirect('/login');  // Short-circuit: stop here
  }
  request.user = decodeToken(token);
  return next(request);  // Continue to next middleware
}

// Layer 3: Authorization middleware
function adminMiddleware(request, next) {
  if (!request.user.isAdmin) {
    return redirect('/unauthorized');
  }
  return next(request);
}

// Layer 4: Route handler
function adminDashboardHandler(request) {
  return renderPage(<AdminDashboard user={request.user} />);
}

// Request flows:
// loggingMiddleware → authMiddleware → adminMiddleware → adminDashboardHandler
//                           ↓
//                    (if no token)
//                           ↓
//                    redirect('/login')
```

### Prefetching: How Routers Optimize Navigation

Modern routers predict user navigation:

```javascript
// HOVER PREFETCHING:
// When user hovers over a link, likely to click

<Link href="/about" prefetch>About</Link>

// Framework behavior:
link.addEventListener('mouseenter', () => {
  // Start loading the /about route code and data
  router.prefetch('/about');
});

// VIEWPORT PREFETCHING:
// Prefetch links visible on screen

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const href = entry.target.getAttribute('href');
      router.prefetch(href);
    }
  });
});

document.querySelectorAll('a[prefetch]').forEach((link) => {
  observer.observe(link);
});

// WHAT PREFETCH ACTUALLY DOES:
// 1. Loads the route's JavaScript chunk
// 2. May also preload data (framework-dependent)
// 3. Stores in memory for instant navigation
```

### Scroll Restoration: The Hidden Complexity

When navigating, browsers must manage scroll position:

```javascript
// BROWSER DEFAULT BEHAVIOR:
// - New navigation: scroll to top
// - Back/forward: restore previous scroll position

// SPA CHALLENGE:
// Browser doesn't know we "navigated" - URL changed via JavaScript
// Must manually handle scroll:

function navigateTo(path) {
  // Save current scroll position
  const scrollPosition = window.scrollY;
  history.replaceState(
    { ...history.state, scrollY: scrollPosition },
    ''
  );
  
  // Navigate
  history.pushState({ path, scrollY: 0 }, '', path);
  
  // Scroll to top for new navigation
  window.scrollTo(0, 0);
}

window.addEventListener('popstate', (event) => {
  renderRoute(window.location.pathname);
  
  // Restore scroll position for back/forward
  if (event.state?.scrollY !== undefined) {
    // Wait for content to render
    requestAnimationFrame(() => {
      window.scrollTo(0, event.state.scrollY);
    });
  }
});
```

### The Edge Cases Every Router Must Handle

```javascript
// 1. TRAILING SLASHES
// /about vs /about/ - are they the same?
// Your router must decide and be consistent
// Usually: redirect one to the other

// 2. CASE SENSITIVITY
// /About vs /about - same route?
// URLs are technically case-sensitive
// Best practice: lowercase, redirect others

// 3. ENCODED CHARACTERS
// /products/running%20shoes = /products/running shoes
// Router must decode: decodeURIComponent(path)

// 4. DOUBLE SLASHES
// /products//shoes - valid?
// Should probably normalize: /products/shoes

// 5. DOT SEGMENTS
// /products/../about = /about
// May need to resolve relative paths

// 6. QUERY STRING HANDLING
// /search?q=foo vs /search?q=bar
// Same route, different parameters
// Router matches path, your code handles query

// 7. HASH FRAGMENTS
// /products#reviews
// Hash not sent to server
// Client must scroll to #reviews element
```

---

## For Framework Authors: Building Routing Systems

> **Implementation Note**: The patterns and code examples below represent one proven approach to building routing systems. Different frameworks take different approaches—React Router uses a declarative model, Next.js uses file-based routing, and SvelteKit combines both. The direction shown here provides core concepts that most routers share. Adapt these patterns based on your framework's component model, build pipeline, and developer experience goals.

### Implementing a Route Matcher

```javascript
// ROUTE MATCHING IMPLEMENTATION

class RouteMatcher {
  constructor() {
    this.routes = [];
  }
  
  // Add route with pattern
  add(pattern, handler, meta = {}) {
    const { regex, paramNames, score } = this.compilePattern(pattern);
    this.routes.push({ pattern, regex, paramNames, handler, meta, score });
    // Keep sorted by specificity
    this.routes.sort((a, b) => b.score - a.score);
  }
  
  // Compile pattern to regex
  compilePattern(pattern) {
    const paramNames = [];
    let score = 0;
    
    const regexStr = pattern
      .split('/')
      .filter(Boolean)
      .map(segment => {
        // Catch-all: [...param]
        if (segment.startsWith('[...') && segment.endsWith(']')) {
          paramNames.push(segment.slice(4, -1));
          score += 1; // Lowest priority
          return '(.+)';
        }
        
        // Optional: [[param]]
        if (segment.startsWith('[[') && segment.endsWith(']]')) {
          paramNames.push(segment.slice(2, -2));
          score += 5;
          return '([^/]*)';
        }
        
        // Dynamic: [param]
        if (segment.startsWith('[') && segment.endsWith(']')) {
          paramNames.push(segment.slice(1, -1));
          score += 10;
          return '([^/]+)';
        }
        
        // Static segment
        score += 100;
        return escapeRegex(segment);
      })
      .join('/');
    
    return {
      regex: new RegExp(`^/${regexStr}/?$`),
      paramNames,
      score,
    };
  }
  
  // Match URL to route
  match(pathname) {
    for (const route of this.routes) {
      const match = pathname.match(route.regex);
      if (match) {
        const params = {};
        route.paramNames.forEach((name, i) => {
          const value = match[i + 1];
          // Handle catch-all as array
          if (route.pattern.includes(`[...${name}]`)) {
            params[name] = value ? value.split('/') : [];
          } else {
            params[name] = value;
          }
        });
        
        return { route, params };
      }
    }
    return null;
  }
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
```

### Building a File-Based Router Generator

```javascript
// FILE-BASED ROUTING GENERATOR (Build Tool)

import { glob } from 'glob';
import path from 'path';
import { parse } from '@babel/parser';

async function generateRouteManifest(config) {
  const { pagesDir, extensions = ['.tsx', '.jsx', '.ts', '.js'] } = config;
  
  // Find all route files
  const pattern = `**/*{${extensions.join(',')}}`;
  const files = await glob(pattern, { cwd: pagesDir });
  
  const routes = [];
  
  for (const file of files) {
    // Skip special files
    if (file.startsWith('_') || file.includes('/_')) continue;
    
    const route = await processRouteFile(pagesDir, file);
    if (route) routes.push(route);
  }
  
  // Sort by specificity
  routes.sort((a, b) => b.score - a.score);
  
  return routes;
}

async function processRouteFile(pagesDir, file) {
  const fullPath = path.join(pagesDir, file);
  const content = await fs.readFile(fullPath, 'utf-8');
  const ast = parse(content, { sourceType: 'module', plugins: ['jsx', 'typescript'] });
  
  // Extract route metadata from exports
  const meta = extractRouteMeta(ast);
  
  // Convert file path to route pattern
  let route = file
    .replace(/\.(tsx?|jsx?)$/, '')    // Remove extension
    .replace(/\/index$/, '')           // /index -> /
    .replace(/\[\.\.\.(\w+)\]/g, '*')  // [...slug] -> *
    .replace(/\[\[(\w+)\]\]/g, ':$1?') // [[id]] -> :id?
    .replace(/\[(\w+)\]/g, ':$1');     // [id] -> :id
  
  if (!route) route = '/';
  else if (!route.startsWith('/')) route = '/' + route;
  
  return {
    path: route,
    file: fullPath,
    ...meta,
    score: calculateScore(route),
  };
}

function extractRouteMeta(ast) {
  const meta = {};
  
  // Look for exported config
  for (const node of ast.program.body) {
    if (node.type === 'ExportNamedDeclaration') {
      if (node.declaration?.declarations?.[0]?.id?.name === 'config') {
        // Extract static config
        meta.config = evaluateStaticObject(node.declaration.declarations[0].init);
      }
    }
  }
  
  return meta;
}

// Generate route manifest code
function emitRouteManifest(routes) {
  return `
// Auto-generated route manifest
export const routes = [
${routes.map(r => `  {
    path: ${JSON.stringify(r.path)},
    component: () => import(${JSON.stringify(r.file)}),
    meta: ${JSON.stringify(r.meta || {})},
  }`).join(',\n')}
];
`;
}
```

### Implementing Nested Routes and Layouts

```javascript
// NESTED ROUTING IMPLEMENTATION

class NestedRouter {
  constructor() {
    this.root = { children: [], layout: null, page: null };
  }
  
  // Build route tree from flat routes
  buildTree(routes) {
    for (const route of routes) {
      this.insertRoute(route);
    }
  }
  
  insertRoute(route) {
    const segments = route.path.split('/').filter(Boolean);
    let node = this.root;
    
    for (let i = 0; i < segments.length; i++) {
      const segment = segments[i];
      let child = node.children.find(c => c.segment === segment);
      
      if (!child) {
        child = { segment, children: [], layout: null, page: null };
        node.children.push(child);
      }
      
      node = child;
    }
    
    // Assign component based on file type
    if (route.file.includes('layout')) {
      node.layout = route.component;
    } else if (route.file.includes('page')) {
      node.page = route.component;
    }
  }
  
  // Match and collect all layouts + page
  match(pathname) {
    const segments = pathname.split('/').filter(Boolean);
    const matched = [];
    let node = this.root;
    const params = {};
    
    // Always include root layout
    if (node.layout) matched.push({ component: node.layout, params: {} });
    
    for (const segment of segments) {
      // Find matching child
      let child = node.children.find(c => c.segment === segment);
      
      // Try dynamic match
      if (!child) {
        child = node.children.find(c => c.segment.startsWith(':'));
        if (child) {
          const paramName = child.segment.slice(1);
          params[paramName] = segment;
        }
      }
      
      if (!child) return null; // No match
      
      if (child.layout) {
        matched.push({ component: child.layout, params: { ...params } });
      }
      
      node = child;
    }
    
    // Add final page
    if (node.page) {
      matched.push({ component: node.page, params: { ...params }, isPage: true });
    }
    
    return { matched, params };
  }
}

// Render nested routes with outlet pattern
async function renderNestedRoute(matched) {
  let content = null;
  
  // Render inside-out (page first, then wrap with layouts)
  for (let i = matched.length - 1; i >= 0; i--) {
    const { component, params, isPage } = matched[i];
    const Component = await component();
    
    if (isPage) {
      content = createElement(Component.default, { params });
    } else {
      // Layout receives children as outlet
      content = createElement(Component.default, { 
        params, 
        children: content,
      });
    }
  }
  
  return content;
}
```

### Route Preloading System

```javascript
// ROUTE PRELOADING IMPLEMENTATION

class RoutePreloader {
  constructor(router) {
    this.router = router;
    this.preloaded = new Set();
    this.preloading = new Map();
  }
  
  // Preload on hover
  setupHoverPreload() {
    document.addEventListener('mouseenter', (e) => {
      const link = e.target.closest('a[href]');
      if (!link) return;
      
      const href = link.getAttribute('href');
      if (href.startsWith('/') && !this.preloaded.has(href)) {
        this.preload(href);
      }
    }, true);
  }
  
  // Preload visible links
  setupViewportPreload() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const href = entry.target.getAttribute('href');
          if (!this.preloaded.has(href)) {
            // Use requestIdleCallback for low-priority preload
            requestIdleCallback(() => this.preload(href));
          }
        }
      });
    }, { rootMargin: '200px' });
    
    document.querySelectorAll('a[href^="/"]').forEach(link => {
      observer.observe(link);
    });
  }
  
  async preload(pathname) {
    if (this.preloading.has(pathname)) {
      return this.preloading.get(pathname);
    }
    
    const match = this.router.match(pathname);
    if (!match) return;
    
    const preloadPromise = (async () => {
      // Preload component code
      const componentPromises = match.matched.map(m => m.component());
      
      // Preload data if route has loader
      const route = match.matched.find(m => m.isPage);
      const dataPromise = route?.loader?.({ 
        params: match.params, 
        preload: true 
      });
      
      await Promise.all([...componentPromises, dataPromise]);
      this.preloaded.add(pathname);
    })();
    
    this.preloading.set(pathname, preloadPromise);
    
    try {
      await preloadPromise;
    } finally {
      this.preloading.delete(pathname);
    }
  }
}
```

### Navigation State Management

```javascript
// NAVIGATION STATE IMPLEMENTATION

class NavigationManager {
  constructor() {
    this.state = 'idle'; // idle | loading | submitting
    this.location = window.location.pathname;
    this.listeners = new Set();
  }
  
  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
  
  notify() {
    this.listeners.forEach(l => l({
      state: this.state,
      location: this.location,
    }));
  }
  
  async navigate(to, options = {}) {
    const { replace = false, state = {} } = options;
    
    this.state = 'loading';
    this.notify();
    
    try {
      // Run before navigation hooks
      for (const hook of this.beforeHooks) {
        const result = await hook(this.location, to);
        if (result === false) {
          this.state = 'idle';
          this.notify();
          return;
        }
        if (typeof result === 'string') {
          to = result; // Redirect
        }
      }
      
      // Update URL
      if (replace) {
        history.replaceState(state, '', to);
      } else {
        history.pushState(state, '', to);
      }
      
      this.location = to;
      
      // Load and render route
      await this.renderRoute(to);
      
      // Scroll to top or hash
      if (to.includes('#')) {
        document.querySelector(to.split('#')[1])?.scrollIntoView();
      } else {
        window.scrollTo(0, 0);
      }
      
    } catch (error) {
      console.error('Navigation failed:', error);
      throw error;
    } finally {
      this.state = 'idle';
      this.notify();
    }
  }
}

// React hook for navigation state
function useNavigation() {
  const [state, setState] = useState({ state: 'idle', location: '' });
  
  useEffect(() => {
    return navigationManager.subscribe(setState);
  }, []);
  
  return state;
}

// Usage in components
function LoadingBar() {
  const { state } = useNavigation();
  
  return state === 'loading' ? <ProgressBar /> : null;
}
```

## Related Skills

- See [web-app-architectures](../web-app-architectures/SKILL.md) for SPA vs MPA routing
- See [meta-frameworks-overview](../meta-frameworks-overview/SKILL.md) for framework-specific routing
- See [seo-fundamentals](../seo-fundamentals/SKILL.md) for SEO-friendly URLs
