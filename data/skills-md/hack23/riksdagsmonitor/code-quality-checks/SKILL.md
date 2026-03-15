---
name: code-quality-checks
description: Quality gates for static HTML/CSS websites (validation, linting, accessibility, link checking)
license: Apache-2.0
---

# Code Quality Checks

## Purpose

Enforce quality standards for Riksdagsmonitor static HTML/CSS website.

## Quality Gates

### HTML Validation (HTMLHint)
```bash
npm install -g htmlhint

# Validate all HTML files
htmlhint *.html

# Custom rules (.htmlhintrc)
{
  "tagname-lowercase": true,
  "attr-lowercase": true,
  "attr-value-double-quotes": true,
  "doctype-first": true,
  "tag-pair": true,
  "spec-char-escape": true,
  "id-unique": true,
  "src-not-empty": true,
  "attr-no-duplication": true
}
```

### CSS Validation (CSSLint)
```bash
npm install -g csslint

# Validate CSS
csslint styles.css

# Custom rules (.csslintrc)
{
  "adjoining-classes": false,
  "box-model": true,
  "box-sizing": false,
  "duplicate-properties": true,
  "empty-rules": true,
  "import": true,
  "important": false,
  "known-properties": true
}
```

### Link Checking (linkinator)
```bash
npm install -g linkinator

# Start local server
python3 -m http.server 8080 &

# Check all links
linkinator http://localhost:8080/ --recurse --silent
```

### Accessibility (axe-core)
```bash
npm install -g @axe-core/cli

# Check accessibility
axe https://riksdagsmonitor.com --tags wcag2a,wcag2aa
```

## Quality Standards

- ✅ 0 HTML validation errors
- ✅ 0 broken links
- ✅ 0 accessibility violations (WCAG 2.1 AA)
- ✅ CSS validation warnings only
- ✅ 4.5:1 color contrast minimum

## References

- **HTMLHint**: https://htmlhint.com/
- **linkinator**: https://github.com/JustinBeckwith/linkinator
- **axe-core**: https://github.com/dequelabs/axe-core-npm
