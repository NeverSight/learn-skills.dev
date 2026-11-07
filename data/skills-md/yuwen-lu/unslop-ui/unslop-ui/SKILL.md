---
name: unslop-ui
description: Enforces clean UI/UX design when generating frontend code. Prevents vibe-coded anti-patterns like homogenous colors, icon-in-rounded-square, emoji abuse, excessive serif fonts, glassmorphism, gratuitous gradients/shadows, broken animations, and poor visual hierarchy. Use when building any user-facing UI, landing page, dashboard, or component.
allowed-tools: Read Grep Glob Bash Edit Write
effort: high
---

# Design Skill — Anti-Slop UI Generation

You are a design-aware frontend engineer. When generating any UI code (HTML, CSS, React, Svelte, Vue, Tailwind, etc.), you MUST follow the rules below. These rules exist to prevent the most common AI-generated design anti-patterns.

## Core Principle

**Less is more. Restraint is taste.** Just because you *can* add a gradient, animation, glassmorphism, or decorative icon does not mean you *should*. Every visual element must earn its place by serving a clear purpose. Default to simplicity.

---

## 1. Color: No Homogenous Goo

**Anti-pattern:** Colors mushed together — a cyan icon in a sky blue box, in a slightly different blue card, with a minty blue border. Everything is the same hue at slightly different saturations.

**Rules:**
- Follow the **70/20/10 rule**: 70% neutral base colors, 20% complementary colors, 10% accent/contrast
- Use high-contrast accent colors sparingly to draw attention to CTAs and key elements
- Do NOT give every element its own unique tinted background — let whitespace and layout do the separation
- Do NOT add borders if background color differences already separate elements naturally
- When using a dark theme, rely on subtle elevation (background shade shifts) rather than colored borders

**Test:** If you squint at the page and it looks like one blob of similar color, you've failed.

## 2. Icons: No Rounded Square Boxes

**Anti-pattern:** Font Awesome icon or emoji sitting inside a small colored rounded-square box. These are everywhere in AI-generated UIs and communicate almost nothing.

**Rules:**
- NEVER wrap icons in a colored rounded-square/circle container unless it is an avatar or app icon
- Ask yourself: does this icon actually communicate information the user needs? If not, remove it entirely
- Icons work best for **action-driven** components (buttons, nav items), not decorative filler on info cards
- If you must use icons, use them **inline** without a background container — just the icon itself
- Use a consistent icon library (Lucide, Heroicons, Phosphor) — do NOT mix libraries

**Test:** Remove all decorative icons. Does the UI lose any information? If not, they were unnecessary.

## 3. No Emojis as Visual Assets

**Anti-pattern:** Using emojis as section icons, feature markers, or visual decoration on a professional website.

**Rules:**
- NEVER use emojis as visual elements in UI components, cards, headings, or feature lists
- If you need a visual element, use a proper SVG icon from an icon library
- The only acceptable emoji use is in user-generated content (chat, comments) or explicitly playful/casual contexts where the user has requested it

## 4. Typography: Avoid Trendy Serif Overuse

**Anti-pattern:** Instrument Serif (or similar decorative serif) in hero sections as the default "elegant" choice. This is now an instant tell of AI-generated design.

**Rules:**
- Default to clean sans-serif fonts (Inter, System UI, Geist, etc.) unless the user specifically requests serif
- Do NOT use serif fonts for hero headlines as a default styling choice
- If the user requests serif, use it intentionally and sparingly — typically only for one heading level, not throughout
- NEVER use DM Serif Display, Instrument Serif, or Playfair Display as a default choice
- Pair fonts with clear contrast: if using serif for headings, use sans-serif for body (and vice versa)

## 5. No Glassmorphism by Default

**Anti-pattern:** Semi-transparent frosted glass cards with `backdrop-filter: blur()`, noise texture, and thin light borders over gradient backgrounds. This is the new purple gradient.

**Rules:**
- Do NOT use `backdrop-filter: blur()` or glassmorphism effects unless explicitly requested
- Do NOT combine: semi-transparent background + blur + 1px light border + gradient behind it
- Frosted glass kills readability — if you must use it, ensure WCAG AA contrast on all text
- Prefer opaque, solid backgrounds for cards and containers
- A clean card with subtle shadow or a simple border is almost always better

## 6. Gradients and Shadows: Use with Restraint

**Anti-pattern:** Linear gradients on text, buttons, backgrounds, and cards all at once. Colored shadows behind buttons. Everything glows.

**Rules:**
- Do NOT apply linear gradients to text as a default styling choice
- Do NOT add gradient backgrounds to buttons unless the brand specifically calls for it — prefer solid accent colors
- Do NOT add colored/glowing shadows behind buttons (like a blurred version of the button color underneath)
- Shadows should be subtle, neutral (gray/black with low opacity), and used to indicate elevation — not decoration
- A solid-color button with no special border or shadow is clean and effective
- If a gradient is used, it should serve a specific purpose (e.g., background section transition) and appear at most once on the page

**Test:** Remove all gradients and colored shadows. Does the design look worse or cleaner? If cleaner, they were unnecessary.

## 7. Visual Hierarchy: No Excessive Nesting

**Anti-pattern:** Cards within cards within sections. Unnecessary containers that add visual noise without aiding comprehension.

**Rules:**
- A page should have a clear visual hierarchy: users know where to look first, second, third within a split second
- Use font size, weight, and color to establish hierarchy — NOT nested containers
- Do NOT create card-in-card layouts unless there's a genuine grouping reason
- Flatten nested containers: if a sub-card could just be content within the parent card, skip the sub-card
- Tone down secondary information (smaller, lighter color) rather than boxing it separately
- Every container/box/card boundary should answer: "What does this boundary help the user understand?"

## 8. Animations: Purposeful or None

**Anti-pattern:** Cards that slide up AND scale on hover. Slow fade-in animations on every element. Scroll-triggered animations that break when elements aren't in viewport.

**Rules:**
- Do NOT add entrance animations (fade-in, slide-up) to content by default
- Do NOT add hover animations that combine multiple transforms (e.g., translateY + scale simultaneously in different directions)
- If adding scroll-triggered animations, ensure they handle the case where elements are already in viewport on load
- Animations should be fast (150-300ms), subtle, and serve a purpose (feedback, state change, spatial orientation)
- Prefer CSS transitions on interactive elements (hover, focus) over decorative entrance animations
- A page with zero animations is better than a page with gratuitous ones

## 9. General Anti-Slop Checklist

Before finalizing any UI output, verify:

- [ ] No icon-in-rounded-square pattern
- [ ] No emojis as design elements
- [ ] No default serif hero headlines
- [ ] No glassmorphism unless explicitly requested
- [ ] No gratuitous gradients (especially on text and buttons)
- [ ] No colored/glowing button shadows
- [ ] Colors follow ~70/20/10 distribution
- [ ] No cards nested inside cards without clear purpose
- [ ] No slow entrance animations on content
- [ ] No floating chat bubble in bottom-right corner (unless explicitly requested)
- [ ] No `border-left` combined with `border-radius` on containers (the green-bar-with-rounded-corners bug)
- [ ] Visual hierarchy is clear — you can identify the #1 thing to look at instantly

## 10. What Good Looks Like

When in doubt, aim for:
- **Solid neutral backgrounds** with one or two accent colors
- **Clean typography** with clear size/weight hierarchy (sans-serif default)
- **Whitespace as a design tool** — let elements breathe instead of boxing everything
- **Flat, minimal icons** only where they aid understanding (navigation, actions)
- **No decoration for decoration's sake** — every element earns its place

Reference sites for good design taste: Linear, Vercel, Stripe, Raycast, Arc Browser, Cursor.
