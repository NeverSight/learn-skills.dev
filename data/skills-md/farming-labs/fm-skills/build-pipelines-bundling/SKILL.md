---
name: build-pipelines-bundling
description: Explains JavaScript bundling, code splitting, chunking strategies, tree shaking, and build pipelines. Use when optimizing bundle size, understanding how modern build tools work, configuring Webpack/Vite/esbuild, or debugging build output.
---

# Build Pipelines and Bundling

## Overview

Build pipelines transform your source code into optimized assets for browsers. Understanding this process is essential for performance optimization and debugging.

## Why Bundling Exists

Browsers historically couldn't handle modern JavaScript development patterns:

```javascript
// YOUR CODE: Many small files with imports
// src/
// ├── index.js (imports App)
// ├── App.js (imports Header, Main, Footer)
// ├── Header.js (imports Logo, Nav)
// ├── Nav.js (imports NavLink)
// └── ... 100+ files

// PROBLEM 1: HTTP/1.1 could only load 6 files in parallel
// 100 files = 17 round trips = SLOW

// PROBLEM 2: Browsers didn't support import/export (until ES modules)
import { Component } from './Component.js';  // Didn't work!

// PROBLEM 3: npm packages live in node_modules
import React from 'react';  // Browser can't resolve this path!

// SOLUTION: Bundle everything into fewer files
// dist/
// ├── index.html
// ├── main.js (all your code + dependencies)
// └── main.css
```

## The Build Pipeline

```
SOURCE CODE                    BUILD PIPELINE                      OUTPUT
─────────────────────────────────────────────────────────────────────────────

src/                                                               dist/
├── index.tsx     ───┐                                        ┌─► index.html
├── App.tsx          │    ┌──────────────────────────────┐    │
├── components/      ├───►│  1. Resolve imports          │    ├─► main.[hash].js
│   ├── Header.tsx   │    │  2. Transform (TS, JSX, etc) │    │
│   └── Button.tsx   │    │  3. Bundle modules           │───►├─► vendor.[hash].js
├── styles/          │    │  4. Optimize (minify, etc)   │    │
│   └── main.css     │    │  5. Output files             │    ├─► main.[hash].css
└── assets/          │    └──────────────────────────────┘    │
    └── logo.png ────┘                                        └─► assets/logo.[hash].png
```

## Bundler Comparison

| Bundler | Speed | Configuration | Best For |
|---------|-------|---------------|----------|
| **Webpack** | Slower | Complex, powerful | Large apps, legacy |
| **Vite** | Fast (dev) | Minimal | Modern apps, DX |
| **esbuild** | Fastest | Limited | Build step, library |
| **Rollup** | Medium | Plugin-focused | Libraries |
| **Parcel** | Fast | Zero-config | Quick prototypes |
| **Turbopack** | Fast | Webpack-compatible | Next.js |

## Core Bundling Concepts

### Module Resolution

How bundlers find your imports:

```javascript
// Relative imports - resolved from current file
import { Button } from './components/Button';
// → src/components/Button.js

// Bare imports - resolved from node_modules
import React from 'react';
// → node_modules/react/index.js

// Alias imports - resolved via config
import { api } from '@/lib/api';
// → src/lib/api.js (@ mapped to src/)

// RESOLUTION ORDER (Node-style):
// 1. Exact path: ./Button.js
// 2. Add extensions: ./Button → ./Button.js, ./Button.ts, ./Button.tsx
// 3. Index files: ./Button → ./Button/index.js
// 4. Package.json "main" or "exports" field
```

### Dependency Graph

Bundlers build a graph of all dependencies:

```
Entry: src/index.tsx
         │
         ▼
    ┌─────────┐
    │ index   │
    └────┬────┘
         │ imports
         ▼
    ┌─────────┐     ┌─────────┐
    │   App   │────►│  React  │
    └────┬────┘     └─────────┘
         │ imports
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│ Header │ │ Footer │
└───┬────┘ └────────┘
    │ imports
    ▼
┌─────────┐
│  Logo   │
└─────────┘

// Bundler walks this graph:
// 1. Start at entry point
// 2. Parse file, find imports
// 3. Recursively process each import
// 4. Build complete dependency graph
// 5. Output bundle in correct order
```

## Code Splitting

Breaking your bundle into smaller pieces loaded on demand.

### Why Code Split?

```
WITHOUT CODE SPLITTING:
┌─────────────────────────────────────────┐
│              main.js (2MB)              │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌───────────┐ │
│  │Home │ │About│ │Blog │ │ Dashboard │ │
│  └─────┘ └─────┘ └─────┘ └───────────┘ │
└─────────────────────────────────────────┘
User visits /home → Downloads 2MB (includes unused Dashboard code)


WITH CODE SPLITTING:
┌──────────────┐
│ main.js (50KB)│ ← Core app, router
└──────────────┘
     │
     ├─► home.js (30KB)      ← Loaded on /home
     ├─► about.js (20KB)     ← Loaded on /about
     ├─► blog.js (40KB)      ← Loaded on /blog
     └─► dashboard.js (500KB) ← Loaded only on /dashboard

User visits /home → Downloads 80KB (main + home)
```

### Split Strategies

**1. Route-Based Splitting**

```javascript
// React with lazy loading
import { lazy, Suspense } from 'react';

// Each route becomes a separate chunk
const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Dashboard = lazy(() => import('./pages/Dashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Suspense>
  );
}

// Build output:
// main.js - core app
// pages-Home-[hash].js - home chunk
// pages-About-[hash].js - about chunk
// pages-Dashboard-[hash].js - dashboard chunk
```

**2. Component-Based Splitting**

```javascript
// Heavy components loaded on demand
const HeavyChart = lazy(() => import('./components/HeavyChart'));
const MarkdownEditor = lazy(() => import('./components/MarkdownEditor'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);
  
  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      
      {showChart && (
        <Suspense fallback={<ChartSkeleton />}>
          <HeavyChart />  {/* Loaded only when needed */}
        </Suspense>
      )}
    </div>
  );
}
```

**3. Vendor Splitting**

```javascript
// Webpack config
optimization: {
  splitChunks: {
    cacheGroups: {
      // Separate node_modules into vendor chunk
      vendor: {
        test: /[\\/]node_modules[\\/]/,
        name: 'vendors',
        chunks: 'all',
      },
      // Separate large libraries
      react: {
        test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
        name: 'react',
        chunks: 'all',
      },
    },
  },
}

// Output:
// main.js - your code
// vendors.js - all node_modules
// react.js - react + react-dom (cached separately)
```

## Chunking Strategies

### Chunk Types

```
ENTRY CHUNKS:
- Starting points of your application
- Usually one per "page" or entry point

ASYNC CHUNKS:
- Created by dynamic imports: import('./module')
- Loaded on demand

COMMON/SHARED CHUNKS:
- Code used by multiple chunks
- Extracted to avoid duplication

VENDOR CHUNKS:
- Third-party code from node_modules
- Changes less frequently = better caching
```

### Optimal Chunking

```javascript
// Webpack splitChunks configuration
optimization: {
  splitChunks: {
    chunks: 'all',
    minSize: 20000,        // Minimum chunk size (20KB)
    maxSize: 244000,       // Try to keep under 244KB
    minChunks: 1,          // Minimum times a module is shared
    maxAsyncRequests: 30,  // Max parallel requests for async chunks
    
    cacheGroups: {
      defaultVendors: {
        test: /[\\/]node_modules[\\/]/,
        priority: -10,
        reuseExistingChunk: true,
      },
      default: {
        minChunks: 2,      // Split if used 2+ times
        priority: -20,
        reuseExistingChunk: true,
      },
    },
  },
}
```

## Tree Shaking

Removing unused code from the bundle.

### How It Works

```javascript
// utils.js - exports multiple functions
export function usedFunction() {
  return 'I am used';
}

export function unusedFunction() {
  return 'I am never imported anywhere';
}

export const USED_CONSTANT = 42;
export const UNUSED_CONSTANT = 999;


// app.js - only imports some exports
import { usedFunction, USED_CONSTANT } from './utils';

console.log(usedFunction(), USED_CONSTANT);


// AFTER TREE SHAKING:
// Bundle only contains usedFunction and USED_CONSTANT
// unusedFunction and UNUSED_CONSTANT are removed
```

### Requirements for Tree Shaking

```javascript
// ✓ WORKS: ES modules (static structure)
import { specific } from 'library';
export function myFunction() {}

// ✗ DOESN'T WORK: CommonJS (dynamic structure)
const library = require('library');
module.exports = myFunction;

// ✗ DOESN'T WORK: Dynamic imports of specific exports
const { specific } = await import('library');  // Can tree shake the import
// But the library must use ES modules internally


// SIDE EFFECTS: Code that runs on import
// package.json
{
  "sideEffects": false  // All files are pure, safe to tree shake
}

// Or specify which files have side effects:
{
  "sideEffects": [
    "*.css",           // CSS imports have side effects
    "./src/polyfills.js"  // This file runs code on import
  ]
}
```

## Minification

Reducing code size without changing behavior.

### Techniques

```javascript
// ORIGINAL CODE:
function calculateTotalPrice(items) {
  let totalPrice = 0;
  for (let i = 0; i < items.length; i++) {
    totalPrice += items[i].price * items[i].quantity;
  }
  return totalPrice;
}

// AFTER MINIFICATION:
function calculateTotalPrice(e){let t=0;for(let l=0;l<e.length;l++)t+=e[l].price*e[l].quantity;return t}

// TECHNIQUES APPLIED:
// 1. Whitespace removal
// 2. Variable name shortening (mangling)
// 3. Dead code elimination
// 4. Constant folding: 1 + 2 → 3
// 5. Boolean simplification: !!x → x (in boolean context)
```

### Minifiers

| Tool | Speed | Compression | Use Case |
|------|-------|-------------|----------|
| **Terser** | Slow | Best | Production builds |
| **esbuild** | Fastest | Good | Development, fast builds |
| **SWC** | Very fast | Good | Next.js, Rust-based |
| **UglifyJS** | Slow | Good | Legacy projects |

## Source Maps

Mapping minified code back to source for debugging.

```javascript
// MINIFIED CODE (main.js):
function a(e){throw new Error("Invalid: "+e)}

// SOURCE MAP (main.js.map):
{
  "version": 3,
  "sources": ["src/validation.ts"],
  "names": ["throwValidationError", "message"],
  "mappings": "AAAA,SAASA,EAAoBC..."
}

// BROWSER DEVTOOLS:
// Shows original source with meaningful names:
function throwValidationError(message) {
  throw new Error("Invalid: " + message);
}
// With correct line numbers!
```

### Source Map Types

```javascript
// Webpack devtool options:

// Development:
devtool: 'eval-source-map'      // Fast rebuild, full source maps
devtool: 'eval-cheap-source-map' // Faster, line-only mapping

// Production:
devtool: 'source-map'           // Full source maps (separate file)
devtool: 'hidden-source-map'    // Source maps generated but not linked
devtool: false                  // No source maps
```

## Asset Handling

Processing non-JavaScript assets.

### Images

```javascript
// Webpack (with asset modules)
{
  test: /\.(png|jpg|gif|svg)$/,
  type: 'asset',
  parser: {
    dataUrlCondition: {
      maxSize: 8 * 1024  // Inline if < 8KB
    }
  }
}

// Vite (automatic)
import logo from './logo.png';  // Returns URL
import icon from './icon.svg?raw';  // Returns SVG content

// Output:
// Small images → Inlined as data URLs
// Large images → Copied to dist with hash
```

### CSS

```javascript
// CSS Processing Pipeline:
// 1. PostCSS (autoprefixer, future CSS)
// 2. CSS Modules (scoped class names)
// 3. Minification (cssnano)
// 4. Extraction (separate .css files)

// Vite handles this automatically
import styles from './Button.module.css';

function Button() {
  return <button className={styles.button}>Click</button>;
}

// Output:
// .button → .Button_button_x7h3j (scoped)
```

## Content Hashing

Cache busting with content-based filenames.

```javascript
// WITHOUT HASHING:
// main.js - browser caches indefinitely
// Update code → browser still uses old cached version!

// WITH CONTENT HASHING:
// main.a1b2c3d4.js - hash based on content
// Update code → new hash → new filename → browser fetches new version

// Webpack configuration:
output: {
  filename: '[name].[contenthash].js',
  chunkFilename: '[name].[contenthash].chunk.js',
}

// Benefits:
// - Unchanged files keep same hash = cached
// - Changed files get new hash = fresh download
// - Long cache headers possible (immutable)
```

## Build Performance Optimization

### Caching

```javascript
// Webpack persistent caching
cache: {
  type: 'filesystem',
  buildDependencies: {
    config: [__filename],  // Invalidate on config change
  },
}

// First build: 30 seconds
// Subsequent builds: 5 seconds (cache hit)
```

### Parallelization

```javascript
// Webpack thread-loader for expensive loaders
{
  test: /\.tsx?$/,
  use: [
    'thread-loader',  // Run in worker pool
    'babel-loader',
  ],
}

// esbuild/SWC are parallel by default (Rust/Go)
```

### Excluding node_modules

```javascript
// Don't transform node_modules (already compiled)
{
  test: /\.js$/,
  exclude: /node_modules/,
  use: 'babel-loader',
}
```

## Build Analysis

Understanding your bundle contents.

```bash
# Webpack Bundle Analyzer
npm install --save-dev webpack-bundle-analyzer

# Add to webpack config:
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

plugins: [
  new BundleAnalyzerPlugin()
]

# Generates interactive treemap of bundle contents
```

```
# source-map-explorer
npx source-map-explorer dist/main.js

# Vite
npx vite-bundle-visualizer
```

---

## Deep Dive: Understanding Bundling From First Principles

### What Bundlers Actually Do: Step by Step

Let's trace through exactly what happens when you run `npm run build`:

```javascript
// YOUR SOURCE FILES:

// src/index.js
import { greet } from './utils.js';
import React from 'react';
console.log(greet('World'));

// src/utils.js
export function greet(name) {
  return `Hello, ${name}!`;
}
export function unused() {
  return 'Never called';
}
```

**Step 1: Parse Entry Point**

```javascript
// Bundler parses index.js into AST (Abstract Syntax Tree)
{
  type: 'Program',
  body: [
    {
      type: 'ImportDeclaration',
      source: { value: './utils.js' },
      specifiers: [{ imported: { name: 'greet' } }]
    },
    {
      type: 'ImportDeclaration', 
      source: { value: 'react' },
      specifiers: [{ imported: { name: 'default' }, local: { name: 'React' } }]
    },
    // ... rest of AST
  ]
}
```

**Step 2: Resolve Dependencies**

```javascript
// For each import, resolve to actual file path

// './utils.js' 
// → Current dir: /project/src/
// → Resolved: /project/src/utils.js ✓

// 'react'
// → Not relative, check node_modules
// → /project/node_modules/react/package.json
// → "main": "index.js"
// → Resolved: /project/node_modules/react/index.js ✓
```

**Step 3: Build Dependency Graph**

```javascript
// Graph structure (simplified)
const graph = {
  '/project/src/index.js': {
    dependencies: [
      '/project/src/utils.js',
      '/project/node_modules/react/index.js'
    ],
    code: '...',
    exports: [],
    imports: ['greet', 'React']
  },
  '/project/src/utils.js': {
    dependencies: [],
    code: '...',
    exports: ['greet', 'unused'],
    imports: []
  },
  // ... react and its dependencies
};
```

**Step 4: Transform Code**

```javascript
// Each file goes through loaders/plugins

// TypeScript → JavaScript
// TSX/JSX → React.createElement calls
// Modern JS → Compatible JS (Babel)

// Input (TSX):
const Button: React.FC = () => <button>Click</button>;

// Output (JS):
const Button = () => React.createElement("button", null, "Click");
```

**Step 5: Tree Shake**

```javascript
// Analyze what's actually used

// utils.js exports: ['greet', 'unused']
// index.js imports from utils: ['greet']
// 
// 'unused' is never imported anywhere
// Mark for removal

// After tree shaking, only 'greet' is included
```

**Step 6: Concatenate Modules**

```javascript
// Combine all modules into bundle format

// IIFE wrapper (Immediately Invoked Function Expression)
(function(modules) {
  // Module cache
  var installedModules = {};
  
  // Module loader
  function __webpack_require__(moduleId) {
    if (installedModules[moduleId]) {
      return installedModules[moduleId].exports;
    }
    var module = installedModules[moduleId] = { exports: {} };
    modules[moduleId](module, module.exports, __webpack_require__);
    return module.exports;
  }
  
  // Start at entry point
  return __webpack_require__('./src/index.js');
})({
  './src/index.js': function(module, exports, __webpack_require__) {
    var utils = __webpack_require__('./src/utils.js');
    var React = __webpack_require__('react');
    console.log(utils.greet('World'));
  },
  './src/utils.js': function(module, exports) {
    exports.greet = function(name) {
      return 'Hello, ' + name + '!';
    };
    // Note: unused() is gone!
  },
  // ... react modules
});
```

**Step 7: Minify**

```javascript
// Terser/esbuild minification

// Before:
function greet(name) {
  return 'Hello, ' + name + '!';
}

// After:
function greet(n){return"Hello, "+n+"!"}

// Or with further optimization:
const greet=n=>"Hello, "+n+"!";
```

**Step 8: Output with Hashing**

```
dist/
├── index.html
├── main.7f8a2b3c.js      ← Hash based on content
├── main.7f8a2b3c.js.map  ← Source map
└── index.html            ← References hashed files
```

### Module Formats: A History Lesson

Understanding why we have multiple module systems:

```javascript
// 1. NO MODULES (Pre-2009)
// Everything in global scope
// script.js
var myApp = {};
myApp.utils = {
  greet: function(name) { return 'Hello, ' + name; }
};

// Problem: Global namespace pollution, dependency order matters


// 2. COMMONJS (2009, Node.js)
// Synchronous, designed for servers
// utils.js
module.exports.greet = function(name) { return 'Hello, ' + name; };

// index.js
const { greet } = require('./utils');

// Problem: Synchronous require() doesn't work in browsers


// 3. AMD - Asynchronous Module Definition (2011, RequireJS)
// Async loading for browsers
define(['./utils'], function(utils) {
  console.log(utils.greet('World'));
});

// Problem: Verbose, non-standard


// 4. UMD - Universal Module Definition (2014)
// Works everywhere (browser global, CommonJS, AMD)
(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['dep'], factory);  // AMD
  } else if (typeof module === 'object') {
    module.exports = factory(require('dep'));  // CommonJS
  } else {
    root.myLib = factory(root.dep);  // Browser global
  }
}(this, function(dep) {
  return { greet: function(name) { return 'Hello, ' + name; } };
}));

// Problem: Complex wrapper for every file


// 5. ES MODULES (2015, ES6)
// Official JavaScript standard
// Static structure enables tree shaking
export function greet(name) { return 'Hello, ' + name; }
import { greet } from './utils.js';

// Now supported natively in browsers and Node.js!
```

### Why Vite is Fast: Native ES Modules

Traditional bundlers (Webpack) vs Vite approach:

```
WEBPACK DEVELOPMENT:

Your Code                   Webpack                    Browser
────────────────────────────────────────────────────────────────
  src/
  ├── index.js  ─┐
  ├── App.js     ├─► Bundle ALL ─► bundle.js ─────► Load bundle
  ├── Header.js  │    files
  └── 100+ more ─┘    together

Time: Parse + transform + bundle ALL files = 10-30 seconds
Change 1 file → Rebundle everything = 2-5 seconds


VITE DEVELOPMENT:

Your Code                     Vite                     Browser
────────────────────────────────────────────────────────────────
  src/
  ├── index.js  ──────────────────────────────────► Request each
  ├── App.js    ─► Transform ─► Serve directly ──► file when needed
  ├── Header.js   on demand                        via native ES
  └── 100+ more ─► (only if requested)             module imports

Time: Transform only requested files = 300-500ms
Change 1 file → Transform only that file = <100ms


WHY THIS WORKS:

<!-- Browser requests via native ES modules -->
<script type="module" src="/src/index.js"></script>

// index.js (served directly, not bundled)
import { App } from './App.js';  // Browser makes another request

// Browser's network tab:
// GET /src/index.js
// GET /src/App.js      (from import in index.js)
// GET /src/Header.js   (from import in App.js)
// ...
```

### Dynamic Imports: How Code Splitting Works

The magic behind `import()`:

```javascript
// STATIC IMPORT (resolved at build time)
import { heavy } from './heavy.js';
// Always included in main bundle

// DYNAMIC IMPORT (resolved at runtime)
const heavy = await import('./heavy.js');
// Creates a separate chunk, loaded on demand
```

**What the bundler does:**

```javascript
// Your code:
button.onclick = async () => {
  const { HeavyComponent } = await import('./HeavyComponent.js');
  render(HeavyComponent);
};

// Bundler output:

// main.js
button.onclick = async () => {
  const { HeavyComponent } = await __webpack_require__.e("HeavyComponent")
    .then(__webpack_require__.bind(__webpack_require__, "./HeavyComponent.js"));
  render(HeavyComponent);
};

// HeavyComponent.a1b2c3.chunk.js (separate file)
(self["webpackChunk"] = self["webpackChunk"] || []).push([
  ["HeavyComponent"],
  {
    "./HeavyComponent.js": (module, exports) => {
      exports.HeavyComponent = function() { /* ... */ };
    }
  }
]);

// At runtime:
// 1. User clicks button
// 2. __webpack_require__.e creates <script> tag
// 3. Browser fetches HeavyComponent.a1b2c3.chunk.js
// 4. Script executes and registers module
// 5. Promise resolves with exports
// 6. Component renders
```

### Magic Comments: Controlling Chunk Behavior

```javascript
// Name the chunk (for debugging/analysis)
const Admin = () => import(/* webpackChunkName: "admin" */ './Admin');
// Output: admin.a1b2c3.js

// Prefetch (load in background after main content)
const Settings = () => import(/* webpackPrefetch: true */ './Settings');
// Adds: <link rel="prefetch" href="settings.chunk.js">

// Preload (load immediately, needed soon)
const Critical = () => import(/* webpackPreload: true */ './Critical');
// Adds: <link rel="preload" href="critical.chunk.js">

// Control loading mode
const Lib = () => import(/* webpackMode: "lazy-once" */ `./lib/${name}`);
// Modes: lazy (default), lazy-once, eager, weak
```

### Tree Shaking Deep Dive: Static Analysis

Why ES modules can be tree shaken but CommonJS cannot:

```javascript
// ES MODULES - STATIC STRUCTURE
// Imports/exports are determined at parse time (before execution)

import { a, b } from './utils';  // ALWAYS imports a and b
export { x, y };                  // ALWAYS exports x and y

// The bundler can statically analyze:
// "This file exports x and y"
// "This file imports a and b"
// No code execution needed!


// COMMONJS - DYNAMIC STRUCTURE
// Imports/exports determined at runtime

const utils = require('./utils');    // What does this export? Depends on runtime
module.exports = something;          // What is 'something'? Depends on runtime

// Examples that break static analysis:
if (condition) {
  module.exports = optionA;
} else {
  module.exports = optionB;
}

const name = 'foo';
module.exports[name] = value;  // Dynamic property

require('./' + dynamicPath);   // Path not known until runtime
```

**The side effects problem:**

```javascript
// utils.js
console.log('Utils loaded!');  // SIDE EFFECT - runs on import

export function used() { return 'used'; }
export function unused() { return 'unused'; }

// Even if 'unused' is never called, we import the file
// The console.log runs!
// Bundler can't remove the file entirely

// SOLUTION: Mark as side-effect free
// package.json
{
  "sideEffects": false
}
// Now bundler knows: if no exports are used, skip the entire file
```

### Scope Hoisting: Module Concatenation

Modern bundlers can merge modules for smaller bundles:

```javascript
// WITHOUT SCOPE HOISTING:
// Each module wrapped in function

(function(modules) {
  function __require__(id) { /* ... */ }
  
  // Module 0
  (function(module, exports, __require__) {
    var utils = __require__(1);
    console.log(utils.greet('World'));
  });
  
  // Module 1
  (function(module, exports) {
    exports.greet = function(name) { return 'Hello, ' + name; };
  });
})();


// WITH SCOPE HOISTING (Module Concatenation):
// Modules merged into one scope

(function() {
  // From utils.js (inlined)
  function greet(name) { return 'Hello, ' + name; }
  
  // From index.js
  console.log(greet('World'));
})();

// Benefits:
// - Smaller bundle (no module wrappers)
// - Faster execution (no function call overhead)
// - Better minification (variables can be renamed together)
```

### Chunk Splitting Algorithms

How bundlers decide what goes in which chunk:

```javascript
// WEBPACK'S SPLITCHUNKS ALGORITHM (Simplified)

// For each module, track:
// - Which chunks include it
// - Size of the module
// - Whether it's from node_modules

// Decision process:
for (module of allModules) {
  const chunks = module.usedInChunks;
  
  // Rule 1: Shared by multiple chunks?
  if (chunks.length >= minChunks) {
    // Candidate for extraction
    
    // Rule 2: Big enough to be worth a separate request?
    if (module.size >= minSize) {
      
      // Rule 3: Won't create too many parallel requests?
      if (currentAsyncRequests < maxAsyncRequests) {
        
        // Extract to common chunk!
        createCommonChunk(module);
      }
    }
  }
}

// RESULT:
// Shared code in common chunks
// Route-specific code in route chunks
// Vendor code in vendor chunks
// Balance between: cache efficiency vs request count
```

### Long-Term Caching Strategy

Optimal caching requires careful chunk design:

```javascript
// PROBLEM: Any change invalidates entire bundle
// main.js contains: app code + vendor code
// Change 1 line of app code → new hash → users re-download everything

// SOLUTION: Separate by change frequency

// 1. Runtime chunk (tiny, rarely changes)
output: {
  filename: '[name].[contenthash].js',
},
optimization: {
  runtimeChunk: 'single',  // Webpack runtime in separate file
}

// 2. Vendor chunk (medium, changes on npm update)
optimization: {
  splitChunks: {
    cacheGroups: {
      vendor: {
        test: /[\\/]node_modules[\\/]/,
        name: 'vendors',
        chunks: 'all',
      },
    },
  },
}

// 3. App chunks (changes frequently)
// Default behavior - your code

// RESULT:
// runtime.a1b1b1.js (1KB)   - Almost never changes
// vendors.c2c2c2.js (200KB) - Changes on npm update
// main.d3d3d3.js (50KB)     - Changes on each deploy
// page-home.e4e4e4.js (10KB) - Changes when home page changes

// User has cached vendors.js
// You deploy change to home page
// User only downloads: main.js + page-home.js (60KB vs 260KB)
```

### Build Performance: What Makes Builds Slow?

```
SLOW OPERATIONS (in order of cost):

1. TYPESCRIPT COMPILATION
   - Type checking is expensive
   - Solution: Use transpileOnly, run tsc separately

2. BABEL TRANSFORMS  
   - Parsing + transforming every file
   - Solution: Exclude node_modules, cache results

3. MINIFICATION
   - Complex AST analysis
   - Solution: Use esbuild/SWC instead of Terser

4. SOURCE MAP GENERATION
   - Creating mapping data
   - Solution: Use simpler source map types in dev

5. LARGE DEPENDENCIES
   - Parsing huge node_modules
   - Solution: Externalize, use pre-bundled versions


OPTIMIZATION CHECKLIST:

□ Enable persistent caching (cache: { type: 'filesystem' })
□ Exclude node_modules from babel/typescript
□ Use thread-loader for parallel processing
□ Use esbuild for minification
□ Use 'eval-source-map' in development
□ Analyze bundle to find unexpected large dependencies
```

---

## The Future: VoidZero and the Unified Rust Toolchain

### The Fragmentation Problem

Today's JavaScript tooling is fragmented across many tools:

```
CURRENT STATE (2024):

Parsing:      Babel, TypeScript, SWC, esbuild (each has own parser)
Transforming: Babel, SWC, esbuild, TypeScript (duplicated work)
Bundling:     Webpack, Rollup, esbuild, Parcel (different algorithms)
Minifying:    Terser, esbuild, SWC (yet more parsers)
Linting:      ESLint (slow, JavaScript-based)
Formatting:   Prettier (slow, JavaScript-based)
Type Check:   TypeScript (can't be parallelized easily)

PROBLEMS:
1. Each tool parses your code separately = redundant work
2. Different tools have different bugs/behaviors
3. JavaScript tools are inherently slow (single-threaded, interpreted)
4. Configuration complexity across many tools
5. Inconsistent error messages and source locations
```

### VoidZero's Vision

VoidZero, founded by Evan You (creator of Vue.js and Vite), is building a unified JavaScript toolchain in Rust:

```
VOIDZERO UNIFIED TOOLCHAIN:

                    ┌─────────────────────────────────────────┐
                    │              OXC (Core)                  │
                    │  Rust-based JavaScript/TypeScript        │
                    │  Parser, Linter, Transformer, Resolver   │
                    └─────────────────┬───────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │    Rolldown     │    │   oxc-linter    │    │  oxc-transform  │
    │  (Bundler)      │    │   (ESLint alt)  │    │  (Babel alt)    │
    └────────┬────────┘    └─────────────────┘    └─────────────────┘
             │
             ▼
    ┌─────────────────┐
    │      Vite       │
    │ (Dev + Build)   │
    └─────────────────┘

SHARED BENEFITS:
- Single parser for all operations
- Consistent AST representation
- Native speed (Rust, parallelized)
- Unified configuration
- Coherent error messages
```

### Oxc (Oxidation Compiler)

Oxc is a collection of high-performance JavaScript/TypeScript tools written in Rust:

```
OXC COMPONENTS:

┌─────────────────────────────────────────────────────────────────┐
│                         oxc_parser                               │
│  - Parses JavaScript, TypeScript, JSX, TSX                      │
│  - 3x faster than SWC, 5x faster than Babel                     │
│  - Produces identical AST for all downstream tools              │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  oxc_linter   │    │ oxc_transformer│   │  oxc_minifier │
│               │    │                │    │               │
│ 50-100x faster│    │ TypeScript →JS │    │ Compresses    │
│ than ESLint   │    │ JSX → JS       │    │ output code   │
│               │    │ Modern → Legacy│    │               │
└───────────────┘    └───────────────┘    └───────────────┘

┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ oxc_resolver  │    │ oxc_sourcemap │    │ oxc_prettier  │
│               │    │               │    │  (planned)    │
│ Module        │    │ Source map    │    │               │
│ resolution    │    │ generation    │    │ Code          │
│               │    │               │    │ formatting    │
└───────────────┘    └───────────────┘    └───────────────┘
```

**Performance comparison:**

```
PARSING BENCHMARK (large codebase):

Tool          Time        Relative
────────────────────────────────────
oxc_parser    45ms        1.0x (baseline)
swc_parser    150ms       3.3x slower
esbuild       180ms       4.0x slower
babel         900ms       20x slower
typescript    1200ms      26x slower


LINTING BENCHMARK (ESLint rules):

Tool          Time        
────────────────────────────────────
oxc_linter    0.5s        
ESLint        50s         (100x slower)

WHY SO FAST?
1. Rust: No garbage collection pauses
2. Parallelization: Uses all CPU cores
3. Zero-copy parsing: Minimal memory allocation
4. SIMD: CPU vectorization for string operations
5. Single pass: Parse once, analyze everything
```

### Rolldown: The Rollup Replacement

Rolldown is a Rust-based bundler designed as a drop-in Rollup replacement:

```
ROLLDOWN VS ROLLUP:

┌─────────────────────────────────────────────────────────────────┐
│                           ROLLUP                                 │
│                                                                  │
│  Language:     JavaScript                                        │
│  Speed:        Medium (single-threaded JS)                       │
│  Plugins:      Rich ecosystem (established)                      │
│  Output:       Excellent tree-shaking and code quality          │
│  Use case:     Libraries, ES module output                       │
│                                                                  │
│  LIMITATIONS:                                                    │
│  - Can't parallelize (JavaScript)                                │
│  - Large projects = slow builds                                  │
│  - Memory-intensive for big codebases                           │
└─────────────────────────────────────────────────────────────────┘

                              │
                              ▼

┌─────────────────────────────────────────────────────────────────┐
│                          ROLLDOWN                                │
│                                                                  │
│  Language:     Rust                                              │
│  Speed:        10-30x faster than Rollup                        │
│  Plugins:      Rollup-compatible (most plugins work)            │
│  Output:       Same quality as Rollup                           │
│  Use case:     Applications + Libraries                          │
│                                                                  │
│  ADVANTAGES:                                                     │
│  - Fully parallelized (Rust + Rayon)                            │
│  - Built on Oxc (shared parser/resolver)                        │
│  - esbuild-level speed with Rollup-quality output               │
│  - Native code splitting                                         │
│  - Built-in transforms (no separate Babel needed)               │
└─────────────────────────────────────────────────────────────────┘
```

**Rolldown architecture:**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Rolldown Build Pipeline                     │
└─────────────────────────────────────────────────────────────────┘

Entry Points
     │
     ▼
┌─────────────────┐
│   oxc_resolver  │ ← Resolve all imports (parallelized)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   oxc_parser    │ ← Parse all files (parallelized)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ oxc_transformer │ ← Transform TS/JSX (parallelized)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Link & Bundle  │ ← Scope hoisting, tree shaking
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  oxc_minifier   │ ← Minify output (parallelized)
└────────┬────────┘
         │
         ▼
    Output Chunks

EVERYTHING shares the same AST representation
NO re-parsing between steps
```

### How Vite Will Use Rolldown

Vite currently uses different tools for dev vs production:

```
VITE TODAY (2024):

Development:
  - Native ES modules (fast)
  - esbuild for dependency pre-bundling
  - esbuild for TypeScript/JSX transform

Production:
  - Rollup for bundling
  - Terser or esbuild for minification
  
PROBLEM: Different tools = different behaviors
  - Dev and prod can have subtle differences
  - Configuration split across tools
  - Can't share optimizations between modes


VITE FUTURE (with Rolldown):

Development:
  - Native ES modules (fast)
  - Rolldown for dependency pre-bundling
  - Oxc for TypeScript/JSX transform

Production:
  - Rolldown for bundling
  - Oxc minifier for minification

BENEFIT: Same tool for dev and prod
  - Consistent behavior
  - Unified configuration
  - Shared caching between modes
  - Even faster production builds
```

### The Complete VoidZero Ecosystem

```
┌─────────────────────────────────────────────────────────────────┐
│                    VOIDZERO ECOSYSTEM                            │
└─────────────────────────────────────────────────────────────────┘

USER FACING:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      Vite       │    │     Vitest      │    │    VitePress    │
│  Build Tool     │    │   Test Runner   │    │  Documentation  │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                    INFRASTRUCTURE:
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Rolldown     │    │   oxc-linter    │    │   Lightning     │
│    Bundler      │    │    (Linter)     │    │   CSS (CSS)     │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                       CORE FOUNDATION:
                                │
                                ▼
                    ┌─────────────────────┐
                    │         OXC         │
                    │  Parser, Resolver,  │
                    │ Transformer, etc.   │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │        NAPI-RS      │
                    │  Rust ↔ Node.js     │
                    │  bindings           │
                    └─────────────────────┘
```

### Why Rust for JavaScript Tooling?

```javascript
// JAVASCRIPT LIMITATIONS FOR TOOLING:

// 1. SINGLE-THREADED
// JavaScript can only use one CPU core for computation
for (const file of files) {
  parse(file);  // Sequential, can't parallelize
}

// 2. GARBAGE COLLECTION PAUSES
// GC stops the world periodically
parseHugeFile();  // Allocates memory
// ... GC pause ... build freezes for 50-200ms

// 3. INTERPRETED OVERHEAD
// Even with JIT, slower than native code
const ast = parse(source);  // ~10x slower than native


// RUST ADVANTAGES:

// 1. TRUE PARALLELISM
// Rust can use all CPU cores safely
files.par_iter().map(|file| parse(file)).collect()  // 8x speedup on 8 cores

// 2. NO GC PAUSES
// Memory managed at compile time, deterministic
// No random freezes during builds

// 3. NATIVE SPEED
// Compiles to machine code
// ~10-100x faster for parsing/transforming

// 4. MEMORY SAFETY
// Rust's ownership system prevents:
// - Memory leaks
// - Use after free
// - Data races
// Without sacrificing performance

// 5. SIMD/VECTORIZATION
// Rust can use CPU vector instructions
// String operations 4-8x faster with SIMD
```

### Migration Path: Rollup to Rolldown

Rolldown aims for Rollup compatibility:

```javascript
// CURRENT ROLLUP CONFIG:
// rollup.config.js
import { defineConfig } from 'rollup';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import typescript from '@rollup/plugin-typescript';

export default defineConfig({
  input: 'src/index.ts',
  output: {
    dir: 'dist',
    format: 'esm',
  },
  plugins: [
    resolve(),
    commonjs(),
    typescript(),
  ],
});


// FUTURE ROLLDOWN CONFIG (mostly compatible):
// rolldown.config.js
import { defineConfig } from 'rolldown';
import resolve from '@rollup/plugin-node-resolve';  // Works!
import commonjs from '@rollup/plugin-commonjs';      // Works!
// typescript() not needed - Rolldown handles TS natively via Oxc

export default defineConfig({
  input: 'src/index.ts',
  output: {
    dir: 'dist',
    format: 'esm',
  },
  plugins: [
    resolve(),
    commonjs(),
    // Built-in: TypeScript, JSX, minification
  ],
});

// COMPATIBILITY STATUS:
// ✓ Most Rollup plugins work (via compatibility layer)
// ✓ Same configuration format
// ✓ Same output quality
// ✗ Some plugins need updates (low-level AST manipulation)
// ✗ Plugin hooks have some differences
```

### Comparing Modern Bundlers

```
┌────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│            │ Webpack  │ Rollup   │ esbuild  │ Rolldown │ Turbopack│
├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Language   │ JS       │ JS       │ Go       │ Rust     │ Rust     │
├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Speed      │ Slow     │ Medium   │ Fast     │ Fast     │ Fast     │
├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Tree Shake │ Good     │ Best     │ Good     │ Best     │ Good     │
├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Code Split │ Best     │ Good     │ Basic    │ Good     │ Good     │
├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Plugins    │ Huge     │ Large    │ Limited  │ Rollup*  │ Webpack* │
├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Config     │ Complex  │ Simple   │ Simple   │ Simple   │ Low-level│
├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Maturity   │ Mature   │ Mature   │ Mature   │ Alpha    │ Beta     │
├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Used By    │ Legacy   │ Vite,    │ Vite,    │ Vite     │ Next.js  │
│            │ projects │ libs     │ many     │ (future) │          │
└────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

* Rolldown: Rollup plugin compatibility
* Turbopack: Webpack plugin compatibility (planned)
```

### The Tooling Evolution Timeline

```
2012: Webpack created (JS, comprehensive but slow)
      └─► Dominated build tooling for years

2017: Parcel created (JS, zero-config)
      └─► Popularized zero-config bundling

2018: Rollup gains popularity (JS, tree-shaking focus)
      └─► Became standard for libraries

2020: esbuild released (Go, 100x faster)
      └─► Proved native speed was possible

2021: Vite 2.0 released (esbuild + Rollup)
      └─► Combined fast dev + quality production

2022: Turbopack announced (Rust, Vercel)
      └─► Next.js-focused, Webpack successor

2023: Oxc development accelerates (Rust, VoidZero)
      └─► Unified toolchain vision emerges

2024: Rolldown alpha (Rust, VoidZero)
      └─► Rollup replacement for Vite

FUTURE: Unified toolchain
      └─► One parser, one resolver, one transformer
      └─► Consistent behavior dev → prod
      └─► 10-100x faster than current tools
```

### When to Use What (2024 Recommendations)

```
BUILDING A LIBRARY:
├─► Small/Medium: Rollup (mature, great tree-shaking)
├─► Large: Rolldown when stable, or esbuild for speed
└─► TypeScript: tsup (esbuild wrapper) or unbuild (Rollup wrapper)

BUILDING AN APPLICATION:
├─► New project: Vite (best DX, uses Rollup + esbuild)
├─► Next.js: Turbopack (experimental) or Webpack (stable)
├─► Large legacy: Webpack (ecosystem, stability)
└─► Performance critical: Consider Vite with Rolldown (when stable)

BUILDING A MONOREPO:
├─► Turborepo + Vite (caching + fast builds)
├─► Nx + any bundler (task orchestration)
└─► pnpm workspaces + Vite (simple, fast)

LINTING:
├─► Today: ESLint (comprehensive rules)
├─► Future: oxc-linter (when rule coverage is sufficient)
└─► Consider: Biome (Rust-based, fast, integrated)

FORMATTING:
├─► Today: Prettier (de facto standard)
├─► Alternative: Biome (faster, combined lint+format)
└─► Future: Oxc prettier (planned)
```

---

## For Framework Authors: Building Bundler Integrations

> **Implementation Note**: The patterns and code examples below represent one proven approach to building bundler integrations. Plugin APIs differ across bundlers—Rollup/Vite use a hook-based system, Webpack uses tapable, and esbuild has a simpler API. The direction shown here focuses on the Rollup/Vite pattern (most common for modern frameworks). Adapt based on which bundlers you need to support and whether you're building plugins or a custom bundler.

### Writing Bundler Plugins

```javascript
// VITE/ROLLUP PLUGIN STRUCTURE

function myPlugin(options = {}) {
  return {
    name: 'my-plugin',
    
    // Called when config is resolved
    configResolved(config) {
      this.config = config;
    },
    
    // Transform source code
    transform(code, id) {
      if (!id.endsWith('.special')) return null;
      
      // Transform the code
      const transformed = processSpecialFile(code);
      
      return {
        code: transformed,
        map: null, // Source map
      };
    },
    
    // Resolve import paths
    resolveId(source, importer) {
      if (source.startsWith('virtual:')) {
        return '\0' + source; // Prefix with \0 for virtual modules
      }
      return null; // Let other plugins handle
    },
    
    // Load virtual modules
    load(id) {
      if (id.startsWith('\0virtual:')) {
        return `export default ${JSON.stringify(getVirtualContent(id))}`;
      }
      return null;
    },
    
    // Build hooks
    buildStart() {
      console.log('Build starting...');
    },
    
    buildEnd(error) {
      if (error) console.error('Build failed:', error);
    },
    
    // Generate bundle output
    generateBundle(options, bundle) {
      // Modify or add to bundle
      this.emitFile({
        type: 'asset',
        fileName: 'manifest.json',
        source: JSON.stringify(generateManifest(bundle)),
      });
    },
  };
}

// Vite-specific hooks
function vitePlugin() {
  return {
    name: 'vite-specific',
    
    // Dev server middleware
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url === '/__my-plugin') {
          res.end(JSON.stringify({ status: 'ok' }));
          return;
        }
        next();
      });
    },
    
    // HMR handling
    handleHotUpdate({ file, server, modules }) {
      if (file.endsWith('.custom')) {
        // Custom HMR logic
        server.ws.send({
          type: 'custom',
          event: 'custom-update',
          data: { file },
        });
        return []; // Don't do normal HMR
      }
    },
    
    // Transform index.html
    transformIndexHtml(html) {
      return html.replace(
        '</head>',
        `<script>window.__VERSION__="${Date.now()}"</script></head>`
      );
    },
  };
}
```

### Implementing Code Splitting Logic

```javascript
// CUSTOM CODE SPLITTING STRATEGY

class ChunkSplitter {
  constructor(options = {}) {
    this.options = {
      minChunkSize: options.minChunkSize || 20000,
      maxChunkSize: options.maxChunkSize || 250000,
      vendorPattern: options.vendorPattern || /node_modules/,
    };
    this.chunks = new Map();
  }
  
  // Analyze module graph
  analyzeGraph(modules) {
    const graph = {
      nodes: new Map(),
      edges: new Map(),
    };
    
    for (const mod of modules) {
      graph.nodes.set(mod.id, {
        id: mod.id,
        size: mod.code.length,
        isVendor: this.options.vendorPattern.test(mod.id),
        imports: mod.imports,
        importedBy: [],
      });
    }
    
    // Build reverse edges
    for (const [id, node] of graph.nodes) {
      for (const imp of node.imports) {
        const target = graph.nodes.get(imp);
        if (target) {
          target.importedBy.push(id);
        }
      }
    }
    
    return graph;
  }
  
  // Determine chunks
  splitChunks(graph, entries) {
    const chunks = [];
    
    // Create vendor chunk
    const vendorModules = [...graph.nodes.values()]
      .filter(n => n.isVendor);
    
    if (vendorModules.length > 0) {
      chunks.push({
        name: 'vendor',
        modules: vendorModules.map(n => n.id),
      });
    }
    
    // Create chunks per entry
    for (const entry of entries) {
      const reachable = this.getReachableModules(graph, entry);
      const nonVendor = reachable.filter(id => !graph.nodes.get(id)?.isVendor);
      
      // Split large chunks
      const subChunks = this.splitBySize(nonVendor, graph);
      chunks.push(...subChunks.map((mods, i) => ({
        name: `${entry}-${i}`,
        modules: mods,
      })));
    }
    
    // Find shared chunks
    const sharedChunks = this.findSharedChunks(chunks, graph);
    chunks.push(...sharedChunks);
    
    return chunks;
  }
  
  getReachableModules(graph, entry) {
    const visited = new Set();
    const queue = [entry];
    
    while (queue.length > 0) {
      const id = queue.shift();
      if (visited.has(id)) continue;
      visited.add(id);
      
      const node = graph.nodes.get(id);
      if (node) {
        queue.push(...node.imports);
      }
    }
    
    return [...visited];
  }
  
  findSharedChunks(chunks, graph) {
    // Find modules used by multiple chunks
    const moduleUsage = new Map();
    
    for (const chunk of chunks) {
      for (const modId of chunk.modules) {
        if (!moduleUsage.has(modId)) {
          moduleUsage.set(modId, []);
        }
        moduleUsage.get(modId).push(chunk.name);
      }
    }
    
    // Extract frequently shared modules
    const shared = [];
    for (const [modId, usedBy] of moduleUsage) {
      if (usedBy.length >= 2) {
        shared.push(modId);
      }
    }
    
    if (shared.length > 0) {
      return [{ name: 'shared', modules: shared }];
    }
    
    return [];
  }
}
```

### Building a Module Transformer

```javascript
// AST-BASED MODULE TRANSFORMER

import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
import MagicString from 'magic-string';

class ModuleTransformer {
  transform(code, options = {}) {
    const ast = acorn.parse(code, {
      ecmaVersion: 'latest',
      sourceType: 'module',
    });
    
    const s = new MagicString(code);
    
    // Transform imports
    walk.simple(ast, {
      ImportDeclaration(node) {
        const source = node.source.value;
        
        // Resolve bare imports
        if (!source.startsWith('.') && !source.startsWith('/')) {
          const resolved = resolveNodeModule(source);
          s.overwrite(
            node.source.start,
            node.source.end,
            `"${resolved}"`
          );
        }
      },
      
      // Transform dynamic imports
      ImportExpression(node) {
        const source = node.source;
        if (source.type === 'Literal') {
          const resolved = resolvePath(source.value);
          s.overwrite(source.start, source.end, `"${resolved}"`);
        }
      },
      
      // Transform exports for HMR
      ExportDefaultDeclaration(node) {
        if (options.hmr) {
          const decl = node.declaration;
          s.appendLeft(decl.start, '__hmr_wrap(');
          s.appendRight(decl.end, ')');
        }
      },
    });
    
    return {
      code: s.toString(),
      map: s.generateMap({ hires: true }),
    };
  }
}

// Import analysis
function analyzeImports(code) {
  const ast = acorn.parse(code, { ecmaVersion: 'latest', sourceType: 'module' });
  const imports = [];
  const exports = [];
  
  walk.simple(ast, {
    ImportDeclaration(node) {
      imports.push({
        source: node.source.value,
        specifiers: node.specifiers.map(s => ({
          type: s.type,
          imported: s.imported?.name || 'default',
          local: s.local.name,
        })),
      });
    },
    
    ExportNamedDeclaration(node) {
      if (node.declaration) {
        if (node.declaration.type === 'VariableDeclaration') {
          for (const decl of node.declaration.declarations) {
            exports.push({ name: decl.id.name, type: 'named' });
          }
        } else if (node.declaration.id) {
          exports.push({ name: node.declaration.id.name, type: 'named' });
        }
      }
    },
    
    ExportDefaultDeclaration() {
      exports.push({ name: 'default', type: 'default' });
    },
  });
  
  return { imports, exports };
}
```

### Implementing Source Maps

```javascript
// SOURCE MAP GENERATION

class SourceMapGenerator {
  constructor() {
    this.mappings = [];
    this.sources = [];
    this.sourcesContent = [];
    this.names = [];
  }
  
  addSource(filename, content) {
    const index = this.sources.indexOf(filename);
    if (index !== -1) return index;
    
    this.sources.push(filename);
    this.sourcesContent.push(content);
    return this.sources.length - 1;
  }
  
  addMapping(generated, original, sourceIndex, name) {
    this.mappings.push({
      generatedLine: generated.line,
      generatedColumn: generated.column,
      originalLine: original.line,
      originalColumn: original.column,
      sourceIndex,
      nameIndex: name ? this.addName(name) : undefined,
    });
  }
  
  addName(name) {
    const index = this.names.indexOf(name);
    if (index !== -1) return index;
    this.names.push(name);
    return this.names.length - 1;
  }
  
  generate() {
    // Sort mappings
    this.mappings.sort((a, b) => 
      a.generatedLine - b.generatedLine || 
      a.generatedColumn - b.generatedColumn
    );
    
    // Encode mappings to VLQ
    const encodedMappings = this.encodeMappings();
    
    return {
      version: 3,
      sources: this.sources,
      sourcesContent: this.sourcesContent,
      names: this.names,
      mappings: encodedMappings,
    };
  }
  
  encodeMappings() {
    let result = '';
    let previousGeneratedLine = 1;
    let previousGeneratedColumn = 0;
    let previousOriginalLine = 0;
    let previousOriginalColumn = 0;
    let previousSourceIndex = 0;
    let previousNameIndex = 0;
    
    for (let i = 0; i < this.mappings.length; i++) {
      const mapping = this.mappings[i];
      
      // New lines
      while (previousGeneratedLine < mapping.generatedLine) {
        result += ';';
        previousGeneratedLine++;
        previousGeneratedColumn = 0;
      }
      
      if (i > 0 && this.mappings[i - 1].generatedLine === mapping.generatedLine) {
        result += ',';
      }
      
      // Encode segment
      let segment = this.encodeVLQ(mapping.generatedColumn - previousGeneratedColumn);
      previousGeneratedColumn = mapping.generatedColumn;
      
      segment += this.encodeVLQ(mapping.sourceIndex - previousSourceIndex);
      previousSourceIndex = mapping.sourceIndex;
      
      segment += this.encodeVLQ(mapping.originalLine - previousOriginalLine);
      previousOriginalLine = mapping.originalLine;
      
      segment += this.encodeVLQ(mapping.originalColumn - previousOriginalColumn);
      previousOriginalColumn = mapping.originalColumn;
      
      if (mapping.nameIndex !== undefined) {
        segment += this.encodeVLQ(mapping.nameIndex - previousNameIndex);
        previousNameIndex = mapping.nameIndex;
      }
      
      result += segment;
    }
    
    return result;
  }
  
  encodeVLQ(value) {
    const VLQ_BASE64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    let encoded = '';
    let vlq = value < 0 ? ((-value) << 1) + 1 : value << 1;
    
    do {
      let digit = vlq & 0x1f;
      vlq >>>= 5;
      if (vlq > 0) digit |= 0x20;
      encoded += VLQ_BASE64[digit];
    } while (vlq > 0);
    
    return encoded;
  }
}
```

## Related Skills

- See [meta-frameworks-overview](../meta-frameworks-overview/SKILL.md) for framework build setups
- See [rendering-patterns](../rendering-patterns/SKILL.md) for how bundles affect rendering
- See [hydration-patterns](../hydration-patterns/SKILL.md) for code splitting and hydration
