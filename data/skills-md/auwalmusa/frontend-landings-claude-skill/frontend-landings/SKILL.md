---
name: frontend-landings
description: Generate beautiful, production-ready, animated single-file HTML landing pages. Use this skill whenever the user asks to create a landing page, marketing page, product page, startup homepage, SaaS landing, app launch page, waitlist page, or any promotional single-page site. Also trigger when user says "make a landing for...", "generate landing page", "build me a homepage", "create a product page", "landing page for my startup", or asks to improve/redesign an existing landing page. Covers both "from scratch" generation and "improve/convert" workflows. Outputs one self-contained HTML file with Tailwind CSS, vanilla JS animations, responsive design, dark/light mode, and curated visual style presets. Always use this skill even for simple landing requests — it ensures premium, non-generic output.
license: MIT
---

# Frontend Landings

Generate stunning, zero-build, single-file HTML landing pages with curated style presets, smooth animations, responsive design, and dark/light mode — all in one self-contained file.

## Before You Start

Read the style presets reference file to understand available aesthetics:
```
references/STYLE_PRESETS.md
```

## Two Modes of Operation

### Mode 1: From Scratch
User provides product details → generate a complete landing page.

**Gather these inputs** (ask if not provided):
1. **Product/brand name** (required)
2. **Tagline / hero headline** (required)
3. **3–6 key features or benefits** (required)
4. **Target audience** (helpful)
5. **Primary CTA** (e.g., "Start Free Trial", "Join Waitlist") — default: "Get Started"
6. **Color preferences** (optional — preset will handle this)
7. **Style preset** (show the preset menu if not specified)

### Mode 2: Improve / Convert
User provides existing HTML, a description, a screenshot, or a URL → enhance with better design, animations, and responsiveness.

**Workflow:**
1. Analyze the existing design (structure, colors, typography, layout)
2. Identify improvements (animations, responsiveness, accessibility, visual hierarchy)
3. Ask which style preset to apply (or preserve existing aesthetic)
4. Regenerate as a single-file HTML with all enhancements

---

## Style Preset System

**ALWAYS offer the preset menu** at the start of any landing page task unless the user has already chosen one or explicitly described a specific aesthetic.

Present presets like this:

```
Pick a visual style for your landing page (type number or name):

 1. ☁️  Clean SaaS Minimal     — Crisp whites, subtle shadows, system-native feel
 2. 🔮  Glassmorphic Modern     — Frosted glass panels, gradients, translucency
 3. 🏗️  Bold Brutalist          — Raw concrete textures, monospace type, stark contrast
 4. 🌆  Cyberpunk Neon          — Dark backgrounds, electric glow, scanline effects
 5. ✒️  Elegant Serif Premium   — Editorial luxury, serif headlines, gold accents
 6. 🎨  Playful Gradients       — Bouncy animations, mesh gradients, rounded everything
 7. 🌙  Dark Mode First         — Deep blacks, neon accents, OLED-optimized
 8. 📻  Vintage Retro           — Warm sepia tones, retro type, nostalgic textures
 9. 🌿  Organic Nature          — Earth tones, organic shapes, botanical illustrations
10. 🏢  Corporate Professional  — Navy/slate palette, structured grid, trust-building

Or describe your own custom aesthetic!
```

After the user picks, read `references/STYLE_PRESETS.md` for the detailed CSS variables, font stacks, animation styles, and design tokens for that preset.

---

## Output Requirements

### Single-File HTML Architecture

Every output MUST be one complete, self-contained HTML file. Structure:

```html
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- SEO Meta Tags -->
  <title>{Product Name} — {Tagline}</title>
  <meta name="description" content="{Concise product description}">
  <meta property="og:title" content="{Product Name}">
  <meta property="og:description" content="{Description}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Anime.js for animations -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.2/anime.min.js"></script>
  
  <!-- Google Fonts (preset-specific) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family={Preset+Fonts}&display=swap" rel="stylesheet">
  
  <!-- Tailwind Config + Custom Theme -->
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          // Preset-specific extensions
          fontFamily: { /* from preset */ },
          colors: { /* from preset */ },
        }
      }
    }
  </script>
  
  <style>
    /* CSS Custom Properties from preset */
    :root { /* light theme vars */ }
    .dark { /* dark theme vars */ }
    
    /* Scroll-triggered animation base classes */
    .reveal { opacity: 0; transform: translateY(30px); transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1); }
    .reveal.active { opacity: 1; transform: translateY(0); }
    
    /* Preset-specific custom styles */
  </style>
</head>
<body>
  <!-- All content here -->
  
  <script>
    // Dark mode toggle
    // Scroll reveal observer
    // Anime.js entrance animations
    // Interactive components (FAQ accordion, pricing toggle, etc.)
  </script>
</body>
</html>
```

### CDN Stack (no others allowed)
- **Tailwind CSS**: `https://cdn.tailwindcss.com` (with inline config)
- **Anime.js**: `https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.2/anime.min.js`
- **Google Fonts**: Only preset-specific fonts
- **Icons**: Inline SVG only (Heroicons-style). NEVER use icon font CDNs.

### Mandatory Features in Every Output

1. **Responsive Design** — Mobile-first. Test mental model at 375px, 768px, 1280px.
2. **Dark/Light Mode** — `prefers-color-scheme` auto-detection + manual toggle button in nav.
3. **Scroll Animations** — IntersectionObserver-based reveal animations on all sections.
4. **Smooth Scrolling** — `scroll-smooth` on html + JS for nav anchors.
5. **Accessibility** — Semantic HTML5, ARIA labels on interactive elements, focus-visible styles, skip-to-content link, sufficient color contrast.
6. **SEO Meta Tags** — title, description, og:title, og:description, og:type, twitter:card.
7. **Performance** — Lazy-load images, efficient CSS, minimal JS.

---

## Section Generation

Based on user input, intelligently include these sections. Not all are required — match to the product context:

### Always Include:
1. **Navigation** — Sticky/fixed nav with logo, links, dark mode toggle, primary CTA button
2. **Hero** — Large headline + sub-headline + CTA button(s) + visual element (gradient, abstract shape, or image placeholder)
3. **Features** — 3–6 feature cards/grid with inline SVG icons
4. **Final CTA** — Full-width call-to-action banner with headline + button
5. **Footer** — Links, copyright, social icons (inline SVG)

### Include When Relevant:
- **Social Proof / Logos** — "Trusted by" logo bar (use placeholder boxes with company-style names)
- **Testimonials** — 2–3 quote cards with avatar placeholders
- **Pricing** — 3 tiers with monthly/annual toggle (JS-powered)
- **FAQ** — Accordion with smooth open/close animations
- **How It Works** — 3-step process with numbered steps
- **Stats / Metrics** — Animated counters (e.g., "10k+ users", "99.9% uptime")

---

## Animation Playbook

Use these animation patterns consistently:

### Scroll Reveal (IntersectionObserver)
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('active');
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### Staggered Entrance (Anime.js)
```javascript
anime({
  targets: '.feature-card',
  opacity: [0, 1],
  translateY: [40, 0],
  delay: anime.stagger(100, { start: 300 }),
  easing: 'easeOutCubic',
  duration: 800
});
```

### Hero Text Animation
```javascript
anime({
  targets: '.hero-title .word',
  opacity: [0, 1],
  translateY: [20, 0],
  delay: anime.stagger(80),
  easing: 'easeOutExpo',
  duration: 1200
});
```

### Hover Micro-interactions
Use CSS transitions for hovers — Anime.js only for complex sequences:
```css
.card { transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease; }
.card:hover { transform: translateY(-4px); box-shadow: 0 20px 40px -12px rgba(0,0,0,0.15); }
```

### Counter Animation
```javascript
function animateCounter(el) {
  const target = parseInt(el.dataset.target);
  anime({
    targets: el,
    innerHTML: [0, target],
    round: 1,
    easing: 'easeInOutExpo',
    duration: 2000
  });
}
```

---

## Dark Mode Implementation

```javascript
// Check system preference and saved preference
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const saved = localStorage.getItem('theme');
if (saved === 'dark' || (!saved && prefersDark)) {
  document.documentElement.classList.add('dark');
}

// Toggle function (bind to button)
function toggleDark() {
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme',
    document.documentElement.classList.contains('dark') ? 'dark' : 'light'
  );
}
```

Toggle button in nav:
```html
<button onclick="toggleDark()" aria-label="Toggle dark mode" class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
  <!-- Sun icon (shown in dark mode) -->
  <svg class="hidden dark:block w-5 h-5" ...>...</svg>
  <!-- Moon icon (shown in light mode) -->
  <svg class="block dark:hidden w-5 h-5" ...>...</svg>
</button>
```

---

## Typography & Anti-Generic Rules

**NEVER use these fonts**: Inter, Roboto, Arial, Helvetica, Open Sans, system-ui defaults.

Each preset specifies its own distinctive font pairing. Always load from Google Fonts CDN.

**NEVER use default Tailwind colors** without customization. Every preset defines a custom palette via CSS variables AND tailwind.config extend.

**NEVER output a page that looks like every other AI-generated landing page.** Each preset has specific differentiators — honor them.

---

## Inline SVG Icons

Use Heroicons-style inline SVGs. Here's the pattern:
```html
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="..." />
</svg>
```

Include 6–8 commonly needed icons directly in the HTML. Choose contextually relevant icons for the product's features.

---

## FAQ Accordion Implementation

```javascript
document.querySelectorAll('.faq-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const content = btn.nextElementSibling;
    const icon = btn.querySelector('.faq-icon');
    const isOpen = content.style.maxHeight && content.style.maxHeight !== '0px';
    
    // Close all others
    document.querySelectorAll('.faq-content').forEach(c => { c.style.maxHeight = '0px'; });
    document.querySelectorAll('.faq-icon').forEach(i => { i.style.transform = 'rotate(0deg)'; });
    
    if (!isOpen) {
      content.style.maxHeight = content.scrollHeight + 'px';
      icon.style.transform = 'rotate(45deg)';
    }
  });
});
```

---

## Pricing Toggle Implementation

```javascript
const toggle = document.getElementById('pricing-toggle');
const monthlyPrices = document.querySelectorAll('.price-monthly');
const annualPrices = document.querySelectorAll('.price-annual');

toggle.addEventListener('change', () => {
  const isAnnual = toggle.checked;
  monthlyPrices.forEach(el => el.classList.toggle('hidden', isAnnual));
  annualPrices.forEach(el => el.classList.toggle('hidden', !isAnnual));
});
```

---

## Final Output Instructions

After generating the HTML, ALWAYS append this guidance:

```
✅ Your landing page is ready!

To use it:
1. Copy the entire code above into a file called `index.html`
2. Open it in any browser — it works standalone, no build step needed

To deploy for free:
• Vercel: vercel.com → New Project → drag & drop your index.html
• Netlify: app.netlify.com → drag & drop your index.html
• GitHub Pages: Push to a repo → Settings → Pages → Deploy from main

To customize further:
• Colors: Edit the CSS variables in :root { } and .dark { }
• Content: All text is directly in the HTML — find and replace
• Fonts: Swap the Google Fonts link and font-family values
• Animations: Adjust timing in the Anime.js calls and CSS transitions
```

---

## Quality Checklist

Before delivering, mentally verify:
- [ ] Single file, no external dependencies beyond CDN links
- [ ] Responsive at 375px, 768px, 1280px
- [ ] Dark mode works (toggle + system preference)
- [ ] All animations fire on scroll
- [ ] Navigation links scroll smoothly to sections
- [ ] All interactive elements have hover/focus states
- [ ] ARIA labels on buttons, toggles, and interactive elements
- [ ] No default Tailwind look — preset aesthetic is distinct
- [ ] Meta tags present for SEO and social sharing
- [ ] Footer includes current year via JS: `new Date().getFullYear()`
- [ ] CTA buttons are prominent and styled per preset
- [ ] Icons are inline SVG, not external fonts
- [ ] Page loads fast — no blocking resources
