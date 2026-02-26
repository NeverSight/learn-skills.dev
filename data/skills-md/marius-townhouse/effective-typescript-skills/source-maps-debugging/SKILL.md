---
name: source-maps-debugging
description: Use when debugging TypeScript in browser. Use when setting up build tools. Use when stack traces show compiled code. Use when breakpoints don't work. Use when deploying to production.
---

# Use Source Maps to Debug TypeScript

## Overview

Source maps bridge the gap between your TypeScript source code and the compiled JavaScript that actually runs. They allow debuggers to show your original TypeScript code, set breakpoints in .ts files, and provide meaningful stack traces. Without source maps, you're debugging compiled JavaScript, which is frustrating and error-prone.

Proper source map configuration is essential for productive debugging of TypeScript applications.

## When to Use This Skill

- Debugging TypeScript in browsers or Node.js
- Setting up build tools (webpack, vite, rollup)
- Stack traces show compiled JavaScript
- Breakpoints not working in TypeScript files
- Configuring production builds

## The Iron Rule

**Enable source maps in development for debugging. Consider separate source maps in production for error reporting while keeping bundle sizes small.**

## Detection

Watch for these debugging issues:

```
// Stack trace shows compiled JavaScript:
Error: Something went wrong
    at Object.<anonymous> (app.js:42:15)
    at Module._compile (internal/modules/cjs/loader.js:1137:30)

// Should show TypeScript:
Error: Something went wrong
    at fetchUser (api.ts:15:10)
    at async loadData (app.ts:42:5)
```

## Enabling Source Maps

### TypeScript Compiler

```json
// tsconfig.json
{
  "compilerOptions": {
    "sourceMap": true,        // Generate .js.map files
    "inlineSourceMap": false, // Don't inline (for development)
    "inlineSources": false,   // Include source in map
    "sourceRoot": "/",        // Root for source paths
    "mapRoot": "/"            // Root for map paths
  }
}
```

### Build Tools

```javascript
// webpack.config.js
module.exports = {
  devtool: 'source-map',  // or 'eval-source-map' for faster builds
};

// vite.config.ts
export default {
  build: {
    sourcemap: true,
  },
};

// rollup.config.js
export default {
  output: {
    sourcemap: true,
  },
  plugins: [typescript({ sourceMap: true })],
};
```

## Source Map Options

| Option | Use Case | Build Speed | Quality |
|--------|----------|-------------|---------|
| `source-map` | Production | Slow | Best |
| `eval-source-map` | Development | Fast | Good |
| `inline-source-map` | Single file | Medium | Good |
| `hidden-source-map` | Production (error reporting) | Slow | Best |
| `nosources-source-map` | Production (no code) | Slow | Stack traces only |

## Production Considerations

```javascript
// webpack.config.js - different for dev/prod
module.exports = (env) => ({
  devtool: env.production 
    ? 'hidden-source-map'  // Separate file, not referenced
    : 'eval-source-map',   // Fast, good for development
});
```

Upload source maps to error reporting services:

```javascript
// Sentry example
Sentry.init({
  dsn: 'your-dsn',
  release: process.env.RELEASE,
  // Source maps uploaded separately
});
```

## Verifying Source Maps

```bash
# Check if source map was generated
ls dist/*.js.map

# Inspect source map content
npx source-map-explorer dist/app.js

# Test in browser DevTools
# 1. Open DevTools
# 2. Go to Sources tab
# 3. Look for original .ts files
# 4. Set breakpoint in TypeScript
```

## Pressure Resistance Protocol

When configuring source maps:

1. **Enable in development**: Essential for debugging
2. **Choose production strategy**: Hidden, nosources, or none
3. **Test breakpoints**: Verify they work in TypeScript files
4. **Check stack traces**: Should show .ts files and line numbers
5. **Monitor bundle size**: Source maps can be large

## Red Flags

| Symptom | Problem | Solution |
|---------|---------|----------|
| Breakpoints in .ts don't work | Source maps not loaded | Enable in build config |
| Stack traces show .js | Source maps not generated | Check tsconfig/build tool |
| Wrong line numbers | Outdated source maps | Regenerate with build |
| Huge bundle size | Inline source maps | Use separate files |

## Common Rationalizations

### "Source maps slow down builds"

**Reality**: Use `eval-source-map` in development for speed. Only use full source maps for production builds.

### "I don't need them, I can read JS"

**Reality**: Debugging compiled JS with types, async/await transforms, etc. is painful. Source maps save hours.

### "They expose my source code"

**Reality**: Use `hidden-source-map` or `nosources-source-map` for production. Upload to error reporting service only.

## Quick Reference

| Environment | Recommended | Notes |
|-------------|-------------|-------|
| Development | `eval-source-map` | Fast rebuilds |
| Production + debugging | `source-map` | Best quality |
| Production + error reporting | `hidden-source-map` | Upload to service |
| Production (minimal) | `nosources-source-map` | Stack traces only |

## The Bottom Line

Enable source maps for debugging TypeScript. Use fast options in development, consider hidden/nosources in production. They make debugging dramatically easier.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 73: Use Source Maps to Debug TypeScript
