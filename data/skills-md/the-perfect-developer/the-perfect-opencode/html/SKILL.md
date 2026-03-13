---
name: html
description: Apply Google HTML style guide conventions to HTML code
---

# HTML Style Guide

This skill applies Google's HTML style guide conventions to ensure clean, semantic, and maintainable HTML code.

## Core Principles

### Document Structure

Always use HTML5 doctype and UTF-8 encoding:
```html
<!doctype html>
<meta charset="utf-8">
<title>Page Title</title>
```

### Semantic HTML

Use elements according to their purpose:
- Headings (`h1`-`h6`) for hierarchical structure
- `p` for paragraphs
- `a` for links and navigation
- `button` for interactive actions
- Avoid `div` for clickable elements

```html
<!-- Not recommended -->
<div onclick="goToRecommendations();">All recommendations</div>

<!-- Recommended -->
<a href="recommendations/">All recommendations</a>
```

### Separation of Concerns

Keep structure (HTML), presentation (CSS), and behavior (JavaScript) strictly separated:
- No inline styles (`style` attribute)
- No inline event handlers (`onclick`, etc.)
- Link minimal CSS and JavaScript files

```html
<!-- Not recommended -->
<h1 style="font-size: 1em;">HTML sucks</h1>
<center>Centered content</center>

<!-- Recommended -->
<!doctype html>
<title>My first CSS-only redesign</title>
<link rel="stylesheet" href="default.css">
<h1>My first CSS-only redesign</h1>
```

## HTML Style Rules

### Valid HTML

- Use valid HTML code tested with [W3C HTML validator](https://validator.w3.org/nu/)
- Ensure proper opening and closing tags
- Nest elements correctly

```html
<!-- Not recommended -->
<title>Test</title>
<article>This is only a test.

<!-- Recommended -->
<!doctype html>
<meta charset="utf-8">
<title>Test</title>
<article>This is only a test.</article>
```

### Protocol

Always use HTTPS for embedded resources:

```html
<!-- Not recommended -->
<script src="//ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>

<!-- Recommended -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
```

### Multimedia

Provide alternative content for accessibility:
- Use meaningful `alt` text for images
- Provide transcripts/captions for video/audio
- Use `alt=""` for purely decorative images

```html
<!-- Not recommended -->
<img src="spreadsheet.png">

<!-- Recommended -->
<img src="spreadsheet.png" alt="Spreadsheet screenshot.">
<img src="decorative-border.png" alt="">
```

### Entity References

Do not use entity references (except for special HTML characters):
- Exception: `<`, `&`, and invisible characters
- Use UTF-8 encoding directly

```html
<!-- Not recommended -->
The currency symbol for the Euro is &ldquo;&eur;&rdquo;.

<!-- Recommended -->
The currency symbol for the Euro is "€".
```

### Optional Tags

Consider omitting optional tags for file size optimization:

```html
<!-- Not recommended -->
<!doctype html>
<html>
  <head>
    <title>Spending money, spending bytes</title>
  </head>
  <body>
    <p>Sic.</p>
  </body>
</html>

<!-- Recommended -->
<!doctype html>
<title>Saving money, saving bytes</title>
<p>Qed.
```

### Type Attributes

Omit `type` attributes for CSS and JavaScript (HTML5 defaults):

```html
<!-- Not recommended -->
<link rel="stylesheet" href="styles.css" type="text/css">
<script src="script.js" type="text/javascript"></script>

<!-- Recommended -->
<link rel="stylesheet" href="styles.css">
<script src="script.js"></script>
```

### ID Attributes

Minimize use of `id` attributes:
- Prefer `class` for styling
- Prefer `data-*` for scripting
- When required, always include hyphen (e.g., `user-profile` not `userProfile`)
- Prevents global `window` namespace pollution

```html
<!-- Not recommended: window.userProfile conflicts -->
<div id="userProfile"></div>

<!-- Recommended -->
<div aria-describedby="user-profile">
  <div id="user-profile"></div>
</div>
```

## Formatting Rules

### Indentation

Indent by 2 spaces (no tabs):

```html
<ul>
  <li>Fantastic
  <li>Great
</ul>
```

### Capitalization

Use only lowercase for:
- Element names
- Attributes
- Attribute values (except text/CDATA)

```html
<!-- Not recommended -->
<A HREF="/">Home</A>

<!-- Recommended -->
<img src="google.png" alt="Google">
```

### Whitespace

Remove trailing whitespace:

```html
<!-- Not recommended -->
<p>What?_

<!-- Recommended -->
<p>Yes please.
```

### Block Elements

Use new line for every block, list, or table element:

```html
<blockquote>
  <p><em>Space</em>, the final frontier.</p>
</blockquote>

<ul>
  <li>Moe
  <li>Larry
  <li>Curly
</ul>

<table>
  <thead>
    <tr>
      <th scope="col">Income
      <th scope="col">Taxes
  <tbody>
    <tr>
      <td>$ 5.00
      <td>$ 4.50
</table>
```

### Line Wrapping

Break long lines for readability (optional but recommended):

```html
<button
  mat-icon-button
  color="primary"
  class="menu-button"
  (click)="openMenu()"
>
  <mat-icon>menu</mat-icon>
</button>
```

### Quotation Marks

Use double quotes for attribute values:

```html
<!-- Not recommended -->
<a class='maia-button maia-button-secondary'>Sign in</a>

<!-- Recommended -->
<a class="maia-button maia-button-secondary">Sign in</a>
```

## Code Quality Guidelines

### Comments

Use comments to explain complex sections:

```html
<!-- TODO: Remove optional tags -->
<ul>
  <li>Apples</li>
  <li>Oranges</li>
</ul>
```

### Action Items

Mark todos with `TODO:` keyword:

```html
{# TODO: Revisit centering. #}
<center>Test</center>
```

## Quick Reference

| Rule | Convention |
|------|------------|
| Doctype | `<!doctype html>` |
| Encoding | UTF-8 with `<meta charset="utf-8">` |
| Protocol | HTTPS for all resources |
| Indentation | 2 spaces |
| Case | Lowercase only |
| Quotes | Double quotes (`"`) |
| Type attributes | Omit for CSS/JS |
| Semantic elements | Use elements for their purpose |
| Accessibility | Always provide `alt` for images |
| IDs | Minimize use, include hyphens |

## Additional Resources

- **`references/html-detailed.md`** - Comprehensive HTML patterns and edge cases
- [W3C HTML Validator](https://validator.w3.org/nu/)
- [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)

## Summary

Write HTML that is:
- **Valid**: Passes W3C validation
- **Semantic**: Uses elements for their intended purpose
- **Accessible**: Includes alt text and proper structure
- **Separated**: No inline styles or scripts
- **Consistent**: Follows formatting conventions
- **Lowercase**: All element/attribute names
- **Secure**: HTTPS for all resources
