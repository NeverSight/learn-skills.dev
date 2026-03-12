---
name: website-devtools
description: Use browser tools to inspect rendering and troubleshoot website issues with the Maintainer.
---

# Skill Instructions

## Purpose
Provide a repeatable way to use browser tools during website work to validate rendering, diagnose layout or CSS issues, and troubleshoot together with the Maintainer.

## Hard Rules
### Must
- [ ] Use the `browser/*` tools when diagnosing rendering, layout, or interaction issues.
- [ ] Capture concrete findings (console errors, computed styles, DOM structure) and summarize them in the PR/issue.

### Must Not
- [ ] Do not guess at rendering behavior when you can verify it in the browser preview.

## Golden Example

```text
Use browser tools to:
- Inspect computed styles and layout for a problematic element
- Check console for errors
- Verify responsive behavior by simulating viewports
```

## Actions
1. Ensure the site is available via the VS Code preview server (`http://127.0.0.1:3000/website/dist/`), then open the relevant page with `browser/openBrowserPage`.
2. Use `browser/readPage`, `browser/clickElement`, `browser/hoverElement`, `browser/typeInPage`, `browser/runPlaywrightCode`, and screenshots as needed to inspect:
   - DOM structure and element attributes
   - Computed CSS and layout metrics
   - Console logs and runtime errors
   - Network requests (if applicable)
3. When a shared layout, component, partial, or client-side module is under investigation, validate more than one consuming page.
4. Share findings with the Maintainer and propose the smallest fix.
