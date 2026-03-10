---
name: lighthouse-audit
description: Specialized skill for running Lighthouse audits, analyzing Core Web Vitals, identifying performance opportunities, and generating performance reports. Use when auditing performance, analyzing Lighthouse metrics, optimizing Core Web Vitals, or generating performance reports.
---

# Lighthouse Audit

## Quick Start

When running Lighthouse audits:

1. **Mobile Audit**: `npm run lighthouse`
2. **Desktop Audit**: `npm run lighthouse:desktop`
3. **JSON Output**: `npm run lighthouse:json`
4. **Analysis**: `npm run lighthouse:analyze`
5. **Diagnostic Report**: `npm run lighthouse:diagnostic`

## Commands

### Mobile Audit (Default)

```bash
# Interactive mobile audit
npm run lighthouse
```

**Configuration**:
- Throttling: 4x CPU slowdown, 150ms RTT, 1600 Kbps
- Screen: 412x915 (mobile)
- Opens interactive report in browser

### Desktop Audit

```bash
# Interactive desktop audit
npm run lighthouse:desktop
```

**Configuration**:
- Throttling: 1x CPU slowdown, 40ms RTT, 10240 Kbps
- No screen emulation
- Opens interactive report in browser

### JSON Output

```bash
# Generate JSON report
npm run lighthouse:json
```

**Output**: `lighthouse-report.json`  
**Use**: For automated analysis and CI/CD

### Automated Analysis

```bash
# Analyze Lighthouse results
npm run lighthouse:analyze
```

**Output**: Console analysis of metrics  
**Shows**: Scores, Core Web Vitals, opportunities

### Diagnostic Report

```bash
# Generate diagnostic report
npm run lighthouse:diagnostic

# Local diagnostic (localhost:3000)
npm run lighthouse:diagnostic:local
```

**Output**: Markdown report in `lighthouse-reports/`  
**Format**: Detailed analysis with recommendations

## Core Web Vitals

### Target Metrics

| Metric | Target | Good | Needs Improvement | Poor |
|--------|--------|------|-------------------|------|
| **LCP** | < 2.5s | < 2.5s | 2.5s - 4.0s | > 4.0s |
| **FID** | < 100ms | < 100ms | 100ms - 300ms | > 300ms |
| **CLS** | < 0.1 | < 0.1 | 0.1 - 0.25 | > 0.25 |
| **FCP** | < 1.8s | < 1.8s | 1.8s - 3.0s | > 3.0s |
| **TBT** | < 300ms | < 300ms | 300ms - 600ms | > 600ms |
| **SI** | < 3.4s | < 3.4s | 3.4s - 5.8s | > 5.8s |

### Current Performance

**Mobile** (05/02/2026, post-deploy; tras hero en servidor). URL: **https://www.pintemas.com**
- Performance: 67/100 🟡
- LCP: 7.48s 🔴
- FCP: 1.26s 🟢
- TBT: 297ms 🟡
- SI: 4.18s 🟡
- CLS: 0 ✅
- Accessibility: 82/100 | Best Practices: 96/100 🟢 | SEO: 100/100 🟢

**Mobile baseline** (23/01/2026): Performance 38, LCP 17.3s, FCP 3.2s, TBT 1,210ms, SI 7.9s. Mejoras: lazy Swiper, IntersectionObserver, hero en servidor (HeroImageServer) → FCP 1.26s, SI 4.18s.

**Desktop**:
- Performance: 93/100 🟢
- LCP: 3.2s 🟡
- FCP: 0.7s 🟢
- TBT: 60ms 🟢
- SI: 2.0s 🟢
- CLS: 0 ✅

## Analysis Workflow

### 1. Run Audit

```bash
# Mobile audit
npm run lighthouse:json
```

### 2. Analyze Results

```bash
# Automated analysis
npm run lighthouse:analyze
```

### 3. Review Opportunities

Check the report for:
- **Reduce unused JavaScript**: Largest opportunity
- **Defer offscreen images**: Image optimization
- **Reduce unused CSS**: CSS optimization
- **Avoid legacy JavaScript**: Modern browser support
- **Server response time**: Backend optimization

### 4. Generate Diagnostic Report

```bash
npm run lighthouse:diagnostic
```

**Output**: `lighthouse-reports/diagnostic-report-*.md`

## Optimization Opportunities

*Última auditoría: 05/02/2026 (móvil, producción).*

### High Priority

1. **Reduce Unused JavaScript** (~170ms potential)
   - Lazy load heavy components
   - Use dynamic imports
   - Remove unused dependencies
   - Optimize code splitting

2. **Reduce Unused CSS** (~170ms potential)
   - Verify Tailwind purge configuration
   - Remove unused CSS rules
   - Use CSS chunking

3. **LCP** (7.27s — objetivo &lt; 2.5s)
   - Optimize hero image (preload, size, quality)
   - Reduce main-thread work and JS execution time
   - Defer offscreen images: `loading="lazy"`, `fetchPriority="low"`

### Medium Priority

4. **Avoid Legacy JavaScript**
   - Verify `.browserslistrc` configuration
   - Ensure modern browser support
   - Remove unnecessary polyfills

5. **Server Response Time** (~45ms potential)
   - Optimize database queries
   - Add database indexes
   - Implement caching

6. **Best Practices** (57/100 — deprecated APIs, third-party cookies)
   - Review report for specific audits and fix accordingly

## Performance Score Breakdown

### Scoring Categories

- **Performance**: 0-100 (weighted by Core Web Vitals)
- **Accessibility**: 0-100 (WCAG compliance)
- **Best Practices**: 0-100 (security, modern APIs)
- **SEO**: 0-100 (meta tags, structured data)

### Performance Score Calculation

Performance score is calculated from:
- **LCP**: 25% weight
- **FID**: 25% weight
- **CLS**: 15% weight
- **FCP**: 10% weight
- **TBT**: 10% weight
- **SI**: 10% weight
- **TTI**: 5% weight

## Report Analysis

### Reading Lighthouse Reports

1. **Scores**: Overall performance rating
2. **Metrics**: Core Web Vitals values
3. **Opportunities**: Optimization suggestions with savings
4. **Diagnostics**: Additional information
5. **Passed Audits**: What's working well

### Interpreting Opportunities

Each opportunity shows:
- **Savings**: Potential time saved (ms)
- **Impact**: High/Medium/Low priority
- **Description**: What needs to be done
- **Learn More**: Link to documentation

## Continuous Monitoring

### CI/CD Integration

Lighthouse CI is configured in:
- `.github/workflows/performance-budgets.yml`
- `lighthouserc.js`

### Automated Reports

Reports are saved to:
- `lighthouse-reports/` directory
- Timestamped filenames
- JSON and Markdown formats

## Troubleshooting

### Audit Fails or Times Out

1. Check server is running: `npm run start`
2. Verify URL is accessible
3. Increase timeout in Lighthouse config
4. Check network connectivity

### Inconsistent Results

1. Run multiple audits and average
2. Clear browser cache
3. Use consistent throttling settings
4. Check for external dependencies

### High LCP

1. Optimize hero image
2. Preload critical resources
3. Reduce server response time
4. Use CDN for static assets

### High TBT

1. Reduce JavaScript execution time
2. Code split heavy components
3. Defer non-critical JavaScript
4. Optimize third-party scripts

## Key Files

- `lighthouserc.js` - Lighthouse CI configuration
- `scripts/performance/analyze-lighthouse-results.js` - Analysis script
- `scripts/performance/lighthouse-diagnostic.js` - Diagnostic script
- `lighthouse-reports/` - Generated reports directory

## Best Practices

### When to Run Audits

- **Before releases**: Verify performance hasn't regressed
- **After optimizations**: Measure improvements
- **Regular monitoring**: Weekly or monthly audits
- **After major changes**: New features or dependencies

### Audit Environment

- **Production**: Best for accurate results
- **Staging**: Good for pre-release verification
- **Local**: Fast iteration, less accurate

### Comparing Results

- Use same throttling settings
- Run at similar times
- Average multiple runs
- Document changes between audits
