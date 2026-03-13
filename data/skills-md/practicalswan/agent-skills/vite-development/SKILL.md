---
name: vite-development
description: Vite 6+ build tooling — HMR, fast builds, plugins, and optimized production assets. Use when configuring Vite, setting up React/Vue projects with Vite, or optimizing frontend build performance.
license: Complete terms in LICENSE.txt
---

# Vite Development

Expert guidance for using Vite 6+ as the build tool for React and other web applications with modern frontend development patterns. Documentation grounded in the official Vite docs at https://vite.dev/.

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

**Project Setup & Configuration:**
- Initializing new Vite projects
- Configuring `vite.config.js` with plugins
- Setting up development server with custom options
- Configuring build optimization and bundling

**Performance & Optimization:**
- Optimizing bundle size and code splitting
- Configuring lazy loading and dynamic imports
- Setting up asset optimization (images, CSS)
- Enabling CSS code splitting and module resolution

**Development Experience:**
- Configuring Hot Module Replacement (HMR)
- Setting up proxy for API calls in dev
- Environment variable handling
- Source map configuration

**Plugin Ecosystem:**
- Using official Vite plugins (React, Vue)
- Community plugins for specific needs
- Writing custom Vite plugins
- Configuring plugin options and hooks

---

## Part 1: Project Configuration

### Basic Vite Config

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'api-client': ['./src/api/client'],
        },
      },
    },
  },
});
```

### Environment-Specific Config

```javascript
// vite.config.js
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());

  return {
    base: mode === 'production' ? '/app-base-path/' : '/',
    server: {
      proxy: {
        '/api': {
          target: env.VITE_API_URL || 'http://localhost:8080',
          changeOrigin: true,
        },
      },
    },
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    },
  };
});
```

---

## Part 2: Build Optimization

### Code Splitting

```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            // React and ReactDOM
            if (id.includes('react') || id.includes('react-dom')) {
              return 'react-vendor';
            }
            // Other large libraries
            if (id.includes('axios')) {
              return 'api-lib';
            }
            return 'vendor';
          }
        },
      },
    },
  },
});
```

### Lazy Loading Routes

```javascript
// Lazy loading route components
const RecipeDetail = lazy(() => import('./pages/RecipeDetail'));
const RecipeList = lazy(() => import('./pages/RecipeList'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/recipes/:id" element={<RecipeDetail />} />
        <Route path="/recipes" element={<RecipeList />} />
      </Routes>
    </Suspense>
  );
}
```

---

## Part 3: Development Server

### Proxy Configuration

```javascript
// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/auth': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
});
```

### HMR Configuration

```javascript
// vite.config.js
export default defineConfig({
  server: {
    hmr: {
      overlay: true,
    },
    watch: {
      usePolling: true,
      interval: 100,
    },
  },
});
```

---

## Part 4: Assets and Plugins

### Image Optimization

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import viteImagemin from 'vite-plugin-imagemin';

export default defineConfig({
  plugins: [
    viteImagemin({
      gifsicle: { optimizationLevel: 7 },
      optipng: { optimizationLevel: 7 },
      mozjpeg: { quality: 80 },
      pngquant: { quality: [0.65, 0.9], speed: 4 },
      svgo: {
        plugins: [
          {
            name: 'removeViewBox',
            active: false,
          },
        ],
      },
    }),
  ],
});
```

---

## Vite Development Best Practices

### Configuration
- [ ] Use `defineConfig` for type-safe configuration
- [ ] Separate dev and production concerns
- [ ] Enable sourcemaps for debugging
- [ ] Configure proper base path for deployment
- [ ] Set up proxy for API during development

### Build Optimization
- [ ] Implement code splitting for vendors
- [ ] Use lazy loading for heavy routes/components
- [ ] Configure manual chunks for better caching
- [ ] Optimize assets (images, fonts)
- [ ] Enable minification for production builds

### Performance
- [ ] Monitor bundle size with Vite bundle analyzer
- [ ] Use tree-shaking to remove unused code
- [ ] Configure dynamic imports for better time-to-interactive
- [ ] Enable CSS code splitting for faster page loads
- [ ] Use compression middleware for production

### Development
- [ ] Configure HMR for faster iteration
- [ ] Set up environment variables for different environments
- [ ] Use proxy for local API development
- [ ] Enable source maps for better debugging
- [ ] Configure clear port and open options

## References & Resources

### Documentation
- [Vite 2026 Config Reference](./references/vite-2026-config-reference.md) — Comprehensive Vite configuration guide
- [Vite Official Excerpts - HMR Config](./references/vite-official-excerpts-hmr-config.md) — Hot Module Replacement configuration

### Examples
- [Vite Config Examples](./examples/vite-config-examples.md) — Example Vite configurations for different use cases

### Scripts
- [Vite Plugin Template](./scripts/vite-plugin-template.ts) — Template for creating custom Vite plugins

### Official Documentation
- [Vite Documentation](https://vite.dev/)
- [Vite Plugins](https://vite.dev/plugins/)
- [Rollup Options](https://vite.dev/config/build-options.html#build-rollupoptions)


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [react-development](../react-development/SKILL.md) | React projects built with Vite |
| [javascript-development](../javascript-development/SKILL.md) | JS/TS code that Vite bundles |
| [frontend-design](../frontend-design/SKILL.md) | Design patterns for Vite-powered frontends |
