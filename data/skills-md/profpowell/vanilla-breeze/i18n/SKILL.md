---
name: i18n
description: Write internationalization-friendly HTML pages. Use when creating multilingual content, setting lang attributes, handling RTL languages, or preparing content for translation.
allowed-tools: Read, Write, Edit
---

# Internationalization (i18n) Skill

This skill ensures HTML pages are properly structured for internationalization and localization.

## Essential Attributes

### The `lang` Attribute (REQUIRED)

Every HTML document MUST have a language declaration:

```html
<html lang="en">
```

Use BCP 47 language tags:

| Tag | Language |
|-----|----------|
| `en` | English |
| `en-US` | American English |
| `en-GB` | British English |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `zh` | Chinese |
| `zh-Hans` | Simplified Chinese |
| `zh-Hant` | Traditional Chinese |
| `ja` | Japanese |
| `ko` | Korean |
| `ar` | Arabic |
| `he` | Hebrew |
| `ru` | Russian |
| `pt` | Portuguese |
| `pt-BR` | Brazilian Portuguese |

### Inline Language Changes

Mark content in different languages:

```html
<p>The French phrase <span lang="fr">c'est la vie</span> means "that's life".</p>

<blockquote lang="de">
  <p>Die Grenzen meiner Sprache bedeuten die Grenzen meiner Welt.</p>
  <footer>— Ludwig Wittgenstein</footer>
</blockquote>
```

### The `dir` Attribute (RTL Languages)

For right-to-left languages (Arabic, Hebrew, Persian, Urdu):

```html
<html lang="ar" dir="rtl">
```

For mixed content:

```html
<p dir="rtl" lang="ar">مرحبا بالعالم</p>
<p dir="ltr" lang="en">Hello World</p>
```

Use `dir="auto"` for user-generated content:

```html
<input type="text" dir="auto" name="comment"/>
<textarea dir="auto"></textarea>
```

## Language Alternatives

### The `hreflang` Attribute

Link to alternate language versions:

```html
<head>
  <!-- Self-referential -->
  <link rel="alternate" hreflang="en" href="https://example.com/page"/>

  <!-- Other languages -->
  <link rel="alternate" hreflang="es" href="https://example.com/es/page"/>
  <link rel="alternate" hreflang="fr" href="https://example.com/fr/page"/>
  <link rel="alternate" hreflang="de" href="https://example.com/de/page"/>

  <!-- Default/fallback -->
  <link rel="alternate" hreflang="x-default" href="https://example.com/page"/>
</head>
```

### Language Switcher Pattern

```html
<nav aria-label="Language selection">
  <ul>
    <li><a href="/en/" hreflang="en" lang="en">English</a></li>
    <li><a href="/es/" hreflang="es" lang="es">Español</a></li>
    <li><a href="/fr/" hreflang="fr" lang="fr">Français</a></li>
    <li><a href="/ar/" hreflang="ar" lang="ar" dir="rtl">العربية</a></li>
  </ul>
</nav>
```

## Character Encoding

### UTF-8 (REQUIRED)

Always declare UTF-8 encoding as the first element in `<head>`:

```html
<head>
  <meta charset="utf-8"/>
  <!-- Other meta tags after -->
</head>
```

### Special Characters

Use actual Unicode characters, not HTML entities when possible:

```html
<!-- Prefer actual characters -->
<p>Price: €50 • Copyright © 2024 • Température: 20°C</p>

<!-- Entities only when needed for markup -->
<p>&lt;tag&gt; shows a tag</p>
```

## Translation-Friendly Markup

### Avoid Concatenation

Do not build sentences from fragments:

```html
<!-- BAD: Fragments break translation -->
<p><span>You have</span> <span class="count">5</span> <span>items</span></p>

<!-- GOOD: Complete translatable unit -->
<p>You have <data value="5">5 items</data> in your cart.</p>
```

### Use `<data>` for Values

Separate translatable text from raw values:

```html
<p>Price: <data value="49.99">$49.99</data></p>
<p>Status: <data value="active">Active</data></p>
```

### Avoid Text in Images

Text in images cannot be translated:

```html
<!-- BAD -->
<img src="welcome-banner.jpg" alt="Welcome to our site"/>

<!-- GOOD -->
<figure>
  <img src="banner-background.jpg" alt=""/>
  <figcaption>Welcome to our site</figcaption>
</figure>
```

### Use `translate` Attribute

Mark content that should not be translated:

```html
<!-- Brand names, code, proper nouns -->
<p>Download <span translate="no">Acme Pro</span> today.</p>
<code translate="no">npm install my-package</code>
<p>Contact: <span translate="no">support@example.com</span></p>
```

## Date, Time, and Numbers

### Semantic Time Element

Always use `<time>` with machine-readable `datetime`:

```html
<!-- Dates -->
<time datetime="2024-12-25">December 25, 2024</time>
<time datetime="2024-12-25">25/12/2024</time>
<time datetime="2024-12-25">25 décembre 2024</time>

<!-- Times -->
<time datetime="14:30">2:30 PM</time>
<time datetime="14:30">14:30</time>
<time datetime="14:30">14h30</time>

<!-- Full datetime -->
<time datetime="2024-12-25T14:30:00Z">December 25, 2024 at 2:30 PM UTC</time>

<!-- Durations -->
<time datetime="PT2H30M">2 hours and 30 minutes</time>
```

### Numbers and Currency

Use `<data>` to preserve raw values:

```html
<!-- Currency -->
<data value="USD 99.99">$99.99</data>
<data value="EUR 99.99">99,99 €</data>
<data value="JPY 10000">¥10,000</data>

<!-- Numbers -->
<data value="1000000">1,000,000</data>
<data value="1000000">1 000 000</data>
<data value="1000000">1.000.000</data>
```

## Pluralization

### Structure for Translation Systems

Avoid English-specific plural logic:

```html
<!-- BAD: Assumes English plural rules -->
<p>You have <span class="count">1</span> item(s)</p>

<!-- GOOD: Complete phrases for each case -->
<p data-plural-zero="You have no items"
   data-plural-one="You have 1 item"
   data-plural-other="You have {count} items">
  You have 5 items
</p>
```

### CLDR Plural Categories

Different languages have different plural rules:

| Category | English | Russian | Arabic |
|----------|---------|---------|--------|
| zero | - | - | 0 items |
| one | 1 item | 1, 21, 31... | 1 item |
| two | - | - | 2 items |
| few | - | 2-4, 22-24... | 3-10 items |
| many | - | 5-20, 25-30... | 11-99 items |
| other | 2+ items | - | 100+ items |

## Accessibility for i18n

### Language Changes for Screen Readers

Screen readers switch pronunciation based on `lang`:

```html
<p>The German word <span lang="de">Weltanschauung</span> has no English equivalent.</p>
```

### Reading Direction

Ensure logical reading order in RTL:

```html
<article dir="rtl" lang="ar">
  <h1>عنوان المقال</h1>
  <p>نص الفقرة هنا.</p>

  <!-- LTR content within RTL -->
  <pre dir="ltr"><code>console.log("Hello");</code></pre>
</article>
```

## Content Structure for Translation

### Meaningful IDs

Use semantic IDs that survive translation:

```html
<!-- BAD -->
<section id="section-1">
<h2 id="welcome-message">Welcome!</h2>

<!-- GOOD -->
<section id="introduction">
<h2 id="hero-heading">Welcome!</h2>
```

### Consistent Structure

Maintain parallel structure across languages:

```html
<!-- All language versions should have same structure -->
<article>
  <header>
    <h1><!-- Translated title --></h1>
    <p class="byline"><!-- Translated byline --></p>
  </header>
  <div class="content">
    <!-- Translated content -->
  </div>
  <footer>
    <!-- Translated footer -->
  </footer>
</article>
```

## Meta Tags for i18n

```html
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>

  <!-- Language/locale -->
  <meta http-equiv="content-language" content="en"/>
  <meta property="og:locale" content="en_US"/>
  <meta property="og:locale:alternate" content="es_ES"/>
  <meta property="og:locale:alternate" content="fr_FR"/>

  <!-- hreflang links -->
  <link rel="alternate" hreflang="en" href="https://example.com/"/>
  <link rel="alternate" hreflang="es" href="https://example.com/es/"/>
  <link rel="alternate" hreflang="x-default" href="https://example.com/"/>
</head>
```

## i18n Checklist

Before finalizing internationalized content:

- [ ] `<html lang="...">` attribute set correctly
- [ ] `<meta charset="utf-8"/>` is first in `<head>`
- [ ] `dir="rtl"` set for RTL languages
- [ ] `hreflang` links for all language versions
- [ ] Inline `lang` attributes for foreign phrases
- [ ] `<time datetime="...">` for all dates/times
- [ ] `<data value="...">` for numbers and currency
- [ ] `translate="no"` on brand names and code
- [ ] No text concatenation that breaks translation
- [ ] No text embedded in images
- [ ] Consistent structure across language versions

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Missing `lang` | Screen readers use wrong pronunciation | Always set `<html lang="...">` |
| Missing `dir` | RTL text displays incorrectly | Add `dir="rtl"` for Arabic, Hebrew, etc. |
| Hardcoded dates | "12/25/2024" means different things | Use `<time datetime="...">` |
| Text in images | Cannot be translated | Use HTML text with CSS styling |
| Concatenation | Word order varies by language | Use complete translatable phrases |
| Entity overuse | Harder to read/edit | Use actual Unicode characters |

## Related Skills

- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **javascript-author** - Write vanilla JavaScript for Web Components with function...
- **accessibility-checker** - Ensure WCAG2AA accessibility compliance
- **metadata** - HTML metadata and head content
