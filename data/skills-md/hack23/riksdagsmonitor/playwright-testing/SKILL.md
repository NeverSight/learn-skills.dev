---
name: playwright-testing
description: Browser automation, visual regression testing, screenshot capture, and cross-browser testing for static websites
license: Apache-2.0
---

# Playwright Testing

## Purpose

Enable comprehensive browser-based testing and validation for static HTML/CSS websites using Playwright automation framework. Supports visual regression testing, accessibility audits, screenshot capture, and cross-browser validation.

## Core Principles

1. **Headless First**: Default to headless mode for CI/CD efficiency
2. **Visual Evidence**: Capture screenshots for all test failures and audits
3. **Accessibility Integration**: Combine with axe-core for WCAG testing
4. **Cross-Browser Coverage**: Test on Chromium, Firefox, and WebKit
5. **Responsive Testing**: Validate across device viewports (mobile, tablet, desktop)
6. **Performance Monitoring**: Track Core Web Vitals (LCP, FID, CLS)

## Enforces

### Test Environment Setup
- **Xvfb Display**: Virtual framebuffer for headless rendering (DISPLAY=:99)
- **Chrome Stable**: Google Chrome with WebGL support for rendering
- **Playwright Installation**: `npx playwright install --with-deps`
- **Dependencies**: System fonts (Noto), graphics libraries (libgbm, libgtk)

### Test Patterns
- **Page Navigation**: `await page.goto('http://localhost:8080/')`
- **Element Interaction**: `await page.locator('selector').click()`
- **Screenshot Capture**: `await page.screenshot({ path: 'evidence.png', fullPage: true })`
- **Accessibility Audit**: `await axe.analyze()` with axe-playwright
- **Visual Comparison**: Compare screenshots for regression detection

### Multi-Language Testing
```javascript
// Test all 14 language versions
const languages = ['index.html', 'index_sv.html', 'index_da.html', ...];
for (const lang of languages) {
  await page.goto(`http://localhost:8080/${lang}`);
  await page.screenshot({ path: `screenshots/${lang}.png` });
}
```

### Accessibility Testing
```javascript
// WCAG 2.1 AA compliance check
const { injectAxe, checkA11y } = require('axe-playwright');
await injectAxe(page);
await checkA11y(page, null, {
  detailedReport: true,
  detailedReportOptions: { html: true }
});
```

### Responsive Design Testing
```javascript
// Test breakpoints
const viewports = [
  { width: 320, height: 568, name: 'mobile' },
  { width: 768, height: 1024, name: 'tablet' },
  { width: 1920, height: 1080, name: 'desktop' }
];
for (const viewport of viewports) {
  await page.setViewportSize(viewport);
  await page.screenshot({ path: `screenshots/${viewport.name}.png` });
}
```

### Core Web Vitals
```javascript
// Measure performance
const metrics = await page.evaluate(() => ({
  LCP: performance.getEntriesByType('largest-contentful-paint')[0]?.renderTime,
  FID: performance.getEntriesByType('first-input')[0]?.processingStart,
  CLS: performance.getEntriesByType('layout-shift').reduce((sum, entry) => sum + entry.value, 0)
}));
```

## When to Use

- **Quality Assurance**: Automated UI testing for PRs
- **Visual Regression**: Detect unintended UI changes
- **Accessibility Audits**: Verify WCAG 2.1 AA compliance across all pages
- **Cross-Browser Testing**: Ensure compatibility (Chrome, Firefox, Safari)
- **Issue Validation**: Capture evidence for bug reports
- **Performance Monitoring**: Track Core Web Vitals over time
- **Multi-Language Validation**: Test all 14 language versions

## Examples

### Good Pattern: Comprehensive Page Audit
```javascript
// test/audit-homepage.spec.js
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('Homepage audit - WCAG 2.1 AA', async ({ page }) => {
  await page.goto('http://localhost:8080/');
  
  // Visual evidence
  await page.screenshot({ 
    path: 'screenshots/homepage-full.png', 
    fullPage: true 
  });
  
  // Accessibility audit
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();
  
  expect(results.violations).toEqual([]);
  
  // Link integrity
  const brokenLinks = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('a'))
      .filter(link => !link.href.startsWith('http'))
      .map(link => link.href);
  });
  expect(brokenLinks).toEqual([]);
});
```

### Good Pattern: Multi-Language Testing
```javascript
// test/multi-language.spec.js
const languages = [
  { file: 'index.html', lang: 'en', name: 'English' },
  { file: 'index_sv.html', lang: 'sv', name: 'Swedish' },
  { file: 'index_ar.html', lang: 'ar', dir: 'rtl', name: 'Arabic' }
];

for (const { file, lang, dir, name } of languages) {
  test(`${name} version accessibility`, async ({ page }) => {
    await page.goto(`http://localhost:8080/${file}`);
    
    // Verify lang attribute
    const htmlLang = await page.getAttribute('html', 'lang');
    expect(htmlLang).toBe(lang);
    
    // Verify RTL if applicable
    if (dir === 'rtl') {
      const htmlDir = await page.getAttribute('html', 'dir');
      expect(htmlDir).toBe('rtl');
    }
    
    // Accessibility audit
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toHaveLength(0);
    
    // Screenshot
    await page.screenshot({ path: `screenshots/${lang}.png` });
  });
}
```

### Anti-Pattern: No Error Handling
```javascript
// ❌ BAD: No error handling or cleanup
test('Bad test', async ({ page }) => {
  await page.goto('http://localhost:8080/');
  // Test crashes if server not running
});

// ✅ GOOD: Proper error handling
test('Good test', async ({ page }) => {
  try {
    await page.goto('http://localhost:8080/', { timeout: 5000 });
  } catch (error) {
    console.error('Server not available:', error.message);
    throw new Error('Test environment not ready');
  }
});
```

### Anti-Pattern: Missing Screenshots on Failure
```javascript
// ❌ BAD: No visual evidence
test('Bad test', async ({ page }) => {
  await page.goto('http://localhost:8080/');
  await expect(page.locator('.missing')).toBeVisible(); // Fails silently
});

// ✅ GOOD: Capture evidence
test('Good test', async ({ page }) => {
  await page.goto('http://localhost:8080/');
  
  try {
    await expect(page.locator('.element')).toBeVisible();
  } catch (error) {
    await page.screenshot({ path: 'evidence/failure.png', fullPage: true });
    throw error;
  }
});
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
- name: Start local server
  run: |
    python3 -m http.server 8080 &
    sleep 2

- name: Run Playwright tests
  run: npx playwright test
  env:
    DISPLAY: ":99"

- name: Upload screenshots
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: playwright-screenshots
    path: screenshots/
```

## Remember

- **Always capture screenshots** for failures and audits
- **Test all 14 languages** including RTL (Arabic, Hebrew)
- **Verify accessibility** with axe-core on every page
- **Test responsive design** across mobile/tablet/desktop breakpoints
- **Use headless mode** for CI/CD efficiency
- **Run local server** before tests (`python3 -m http.server 8080`)
- **Clean up processes** after tests (kill server, Xvfb)
- **Upload artifacts** on failure (screenshots, accessibility reports)

## References

- [Playwright Documentation](https://playwright.dev/)
- [axe-core Playwright Integration](https://www.npmjs.com/package/@axe-core/playwright)
- [WCAG 2.1 AA Guidelines](https://www.w3.org/WAI/WCAG21/quickref/?currentsidebar=%23col_customize&levels=aa)
- [Core Web Vitals](https://web.dev/vitals/)
- [Hack23 ISMS - Testing Requirements](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)

---

**Version**: 1.0  
**Last Updated**: 2026-02-06  
**Maintained by**: Hack23 AB
