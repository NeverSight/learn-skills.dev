---
name: html-standards
description: Guidelines for writing HTML that is accessible, semantic, maintainable, and secure. Use when working with .html, .vue, .twig, .php, .cshtml, .svelte files, or when the user asks about HTML structure, semantic markup, accessibility, or web security best practices.
metadata:
    author: devbyray
    version: '1.0'
    languages: 'html, html5'
---

# HTML Standards & Best Practices

Apply these standards when writing HTML markup to ensure accessibility, semantics, maintainability, and security.

## Structure & Semantics

### 1. Use Semantic HTML Elements

Prefer semantic elements over generic divs and spans:

**Good:**

```html
<header>
	<nav>
		<ul>
			<li><a href="/">Home</a></li>
		</ul>
	</nav>
</header>

<main>
	<article>
		<h2>Article Title</h2>
		<section>
			<p>Content...</p>
		</section>
	</article>

	<aside>
		<h3>Related Links</h3>
	</aside>
</main>

<footer>
	<p>&copy; 2026 Company Name</p>
</footer>
```

**Bad:**

```html
<div class="header">
	<div class="nav">...</div>
</div>

<div class="main">
	<div class="article">...</div>
</div>
```

### 2. Document Structure

Always use proper HTML5 document structure:

```html
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>Page Title</title>
	</head>
	<body>
		<!-- Content -->
	</body>
</html>
```

### 3. Heading Hierarchy

- Use headings in logical order (H2, H3, H4, etc.)
- **Do NOT use `<h1>`** (reserved for page title generation)
- Don't skip heading levels

**Good:**

```html
<h2>Main Section</h2>
<h3>Subsection</h3>
<h4>Detail</h4>
```

**Bad:**

```html
<h1>Title</h1>
<!-- Don't use H1 -->
<h4>Content</h4>
<!-- Skipped H2, H3 -->
```

### 4. Code Organization

- Indent nested elements consistently (2 spaces)
- Use blank lines to separate logical sections
- Keep lines readable (max 120 characters)

## Accessibility

### 5. Images

All images must have descriptive alt text:

```html
<!-- Informative image -->
<img src="chart.png" alt="Sales chart showing 20% increase in Q4 2025" />

<!-- Decorative image -->
<img src="divider.png" alt="" />
```

### 6. Forms

Always label form controls:

```html
<form>
	<label for="email">Email address</label>
	<input type="email" id="email" name="email" required />

	<label for="password">Password</label>
	<input type="password" id="password" name="password" required />

	<button type="submit">Submit</button>
</form>
```

### 7. Keyboard Navigation

Ensure interactive elements are keyboard accessible:

```html
<button type="button">Clickable Button</button>
<a href="/page">Link to Page</a>

<!-- Only use tabindex="0" for custom interactive elements -->
<div role="button" tabindex="0" onclick="handleClick()">Custom Button</div>
```

### 8. ARIA Attributes

Use ARIA only when native HTML is insufficient:

```html
<!-- Good: Native HTML -->
<button>Click me</button>

<!-- OK: ARIA when needed -->
<button aria-label="Close dialog">×</button>

<!-- Good: ARIA for custom widgets -->
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
	<h2 id="dialog-title">Dialog Title</h2>
</div>
```

## Maintainability

### 9. Avoid Inline Styles and Scripts

Keep HTML clean by using external files:

**Bad:**

```html
<div style="color: red; font-size: 20px;" onclick="alert('clicked')">Content</div>
```

**Good:**

```html
<div class="error-text" data-action="show-alert">Content</div>
```

### 10. Consistent Naming

Use lowercase, hyphen-separated names:

```html
<div class="main-header"></div>
<nav class="site-navigation"></nav>
<button id="submit-button">Submit</button>
```

### 11. Code Comments

Use comments to organize sections:

```html
<!-- Header Section -->
<header>
	<!-- Navigation -->
	<nav>...</nav>
</header>

<!-- Main Content -->
<main>...</main>
```

## Security

### 12. Escape User-Generated Content

Never inject raw user data into the DOM:

**Bad (XSS vulnerability):**

```javascript
element.innerHTML = userInput
```

**Good:**

```javascript
element.textContent = userInput
// OR use DOMPurify for HTML
element.innerHTML = DOMPurify.sanitize(userInput)
```

### 13. Security Meta Tags

Include security headers:

```html
<head>
	<meta charset="UTF-8" />
	<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'" />
	<meta http-equiv="X-Content-Type-Options" content="nosniff" />
	<meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains" />
</head>
```

## Performance

### 14. Optimize Images

```html
<!-- Modern formats with fallback -->
<picture>
	<source srcset="image.webp" type="image/webp" />
	<source srcset="image.jpg" type="image/jpeg" />
	<img src="image.jpg" alt="Description" loading="lazy" />
</picture>

<!-- Lazy loading for non-critical images -->
<img src="image.jpg" alt="Description" loading="lazy" />
```

### 15. Resource Hints

Use preload and prefetch for critical resources:

```html
<head>
	<!-- Preload critical CSS -->
	<link rel="preload" href="critical.css" as="style" />

	<!-- Prefetch next page -->
	<link rel="prefetch" href="/next-page" />

	<!-- DNS prefetch for external domains -->
	<link rel="dns-prefetch" href="https://api.example.com" />
</head>
```

## Complete Example

```html
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<meta name="description" content="Brief page description for SEO" />
		<meta http-equiv="Content-Security-Policy" content="default-src 'self'" />

		<title>Page Title - Site Name</title>

		<link rel="preload" href="styles.css" as="style" />
		<link rel="stylesheet" href="styles.css" />
	</head>
	<body>
		<!-- Header -->
		<header class="site-header">
			<nav class="main-navigation" aria-label="Main navigation">
				<ul>
					<li><a href="/" aria-current="page">Home</a></li>
					<li><a href="/about">About</a></li>
					<li><a href="/contact">Contact</a></li>
				</ul>
			</nav>
		</header>

		<!-- Main Content -->
		<main id="main-content">
			<article>
				<h2>Article Title</h2>

				<section>
					<h3>Section Heading</h3>
					<p>Content paragraph with <a href="/link">descriptive link text</a>.</p>

					<img src="image.jpg" alt="Detailed description of the image" loading="lazy" />
				</section>

				<section>
					<h3>Form Section</h3>
					<form action="/submit" method="post">
						<label for="name">Full Name</label>
						<input type="text" id="name" name="name" required />

						<label for="email">Email Address</label>
						<input type="email" id="email" name="email" required />

						<button type="submit">Send</button>
					</form>
				</section>
			</article>

			<aside class="sidebar">
				<h3>Related Content</h3>
				<ul>
					<li><a href="/related-1">Related Article 1</a></li>
					<li><a href="/related-2">Related Article 2</a></li>
				</ul>
			</aside>
		</main>

		<!-- Footer -->
		<footer class="site-footer">
			<p>&copy; 2026 Company Name. All rights reserved.</p>
		</footer>

		<script src="app.js" defer></script>
	</body>
</html>
```

## Validation

### Tools

- [W3C Markup Validator](https://validator.w3.org/)
- Browser DevTools accessibility audits
- [axe DevTools](https://www.deque.com/axe/devtools/)

### Checklist

- ✅ Valid HTML5 structure
- ✅ Proper DOCTYPE and language attribute
- ✅ Semantic elements used appropriately
- ✅ No H1 in content (reserved for page title)
- ✅ All images have alt text
- ✅ Forms have proper labels
- ✅ Keyboard navigation works
- ✅ Security meta tags included
- ✅ External CSS/JS files used
- ✅ Consistent naming conventions

## When to Apply

Apply these standards when:

- Creating HTML pages
- Building templates
- Writing component markup
- Reviewing HTML code
- User asks about HTML best practices
- Working with any HTML-based template engine
