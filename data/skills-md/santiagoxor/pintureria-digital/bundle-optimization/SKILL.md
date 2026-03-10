---
name: bundle-optimization
description: Specialized skill for analyzing JavaScript bundle sizes, identifying optimization opportunities, detecting unused code, and monitoring performance budgets. Use when bundle size exceeds limits, analyzing code splitting, identifying heavy dependencies, or optimizing JavaScript payload.
---

# Bundle Analysis & Optimization

## Quick Start

When analyzing bundles:

1. **Full Analysis**: `npm run analyze`
2. **Bundle Optimization Check**: `npm run bundle-optimization:check`
3. **Detailed Report**: `npm run bundle-optimization:report`
4. **Recharts Analysis**: `npm run analyze:recharts`

## Commands

### Full Bundle Analysis

```bash
# Complete bundle analysis with visual report
npm run analyze
```

**Output**: Opens interactive bundle analyzer in browser  
**Shows**: Chunk sizes, dependencies, code splitting effectiveness

### Bundle Optimization Analysis

```bash
# Quick check without report
npm run bundle-optimization:check

# Detailed analysis with report
npm run bundle-optimization:analyze

# Generate report files
npm run bundle-optimization:report
```

**Output**: Console analysis + optional report files  
**Shows**: Bundle size, first load JS, chunk analysis, violations

### Specific Library Analysis

```bash
# Analyze Recharts chunk
npm run analyze:recharts

# Analyze all chunks
npm run analyze:chunks

# Verify Recharts imports
npm run verify:recharts-imports
```

## Performance Budgets

### Current Limits

- **First Load JS**: < 128KB (warning: 100KB)
- **Total Bundle Size**: < 500KB (warning: 400KB)
- **CSS Bundle Size**: < 50KB (warning: 40KB)
- **Chunk Count**: < 20 (warning: 15)

### Budget Configuration

Budgets are defined in:
- `performance-budgets.config.js`
- `src/lib/optimization/performance-budget-monitor.ts`
- `.github/workflows/performance-budgets.yml`

## Analysis Workflow

### 1. Run Analysis

```bash
npm run analyze
```

### 2. Review Bundle Analyzer

Check the interactive report for:
- **Large chunks**: > 150KB
- **Duplicate code**: Same library in multiple chunks
- **Unused code**: Dead code elimination opportunities
- **Code splitting**: Effectiveness of async chunks

### 3. Identify Issues

Common issues to look for:

- **Heavy dependencies**: Libraries > 50KB
- **Duplicate modules**: Same code in multiple chunks
- **Missing code splitting**: Large initial chunks
- **Unused imports**: Dead code in bundle

### 4. Optimize

Based on findings:

- **Lazy load heavy components**: Use `dynamic()` imports
- **Remove unused dependencies**: Clean up imports
- **Optimize imports**: Use modular imports
- **Split large chunks**: Configure webpack splitChunks

## Code Splitting Analysis

### Current Configuration

Code splitting is configured in `next.config.js`:

- **Framer Motion**: `chunks: 'async'`, `maxSize: 20KB`
- **Swiper**: `chunks: 'async'`, `maxSize: 20KB`
- **Recharts**: `chunks: 'async'`, `maxSize: 100KB`
- **React Query**: `chunks: 'async'`, `maxSize: 20KB`
- **Redux**: `chunks: 'async'`, `maxSize: 20KB`

### Verifying Code Splitting

```bash
# Check if libraries are in async chunks
npm run analyze

# Look for:
# - Framer Motion in separate async chunk
# - Swiper in separate async chunk
# - Recharts in separate async chunk
```

## Optimization Strategies

### Reduce Bundle Size

1. **Lazy Load Heavy Components**
   ```typescript
   const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
     ssr: false,
     loading: () => <Skeleton />
   })
   ```

2. **Use Modular Imports**
   ```typescript
   // ❌ Bad: imports entire library
   import _ from 'lodash'
   
   // ✅ Good: imports only needed function
   import debounce from 'lodash-es/debounce'
   ```

3. **Remove Unused Dependencies**
   ```bash
   # Find unused dependencies
   npx depcheck
   
   # Remove unused packages
   npm uninstall <package>
   ```

### Optimize Code Splitting

1. **Configure Webpack SplitChunks**
   - See `next.config.js` for current configuration
   - Adjust `maxSize` for optimal chunk sizes
   - Use `chunks: 'async'` for non-critical code

2. **Use Dynamic Imports**
   - Route-based code splitting (automatic in Next.js)
   - Component-based lazy loading
   - Library-based async chunks

## Analysis Checklist

When analyzing bundles:

- [ ] First Load JS < 128KB
- [ ] Total Bundle Size < 500KB
- [ ] No duplicate modules across chunks
- [ ] Heavy libraries in async chunks
- [ ] Code splitting working correctly
- [ ] No unused code in bundle
- [ ] CSS bundle size < 50KB

## Key Metrics

### Critical Metrics

- **First Load JS**: JavaScript loaded on initial page load
- **Total Bundle Size**: Sum of all JavaScript chunks
- **Chunk Count**: Number of separate chunks
- **Duplicate Modules**: Code duplicated across chunks

### Performance Impact

- **Bundle Size**: Affects download time
- **Parse Time**: Affects TTI (Time to Interactive)
- **Code Splitting**: Affects initial load vs. total size

## Troubleshooting

### Bundle Size Too Large

1. Run analysis: `npm run analyze`
2. Identify largest chunks
3. Lazy load heavy components
4. Remove unused dependencies
5. Optimize imports

### Code Splitting Not Working

1. Check `next.config.js` configuration
2. Verify `chunks: 'async'` for heavy libraries
3. Ensure dynamic imports use `ssr: false` when needed
4. Check webpack splitChunks configuration

### Duplicate Modules

1. Identify duplicated libraries
2. Check for multiple versions in package.json
3. Use webpack alias to force single version
4. Verify code splitting configuration

## Key Files

- `next.config.js` - Webpack and code splitting configuration
- `performance-budgets.config.js` - Performance budget limits
- `scripts/performance/analyze-bundle-optimization.js` - Analysis script
- `src/lib/optimization/bundle-optimization-manager.ts` - Bundle manager
