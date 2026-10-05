---
name: hydrogen-ecommerce-ux
description: Research-backed UX best practices for Shopify Hydrogen storefronts, based on Baymard Institute (200,000+ hours of usability research) and Nielsen Norman Group studies. Use this skill WHENEVER the user is building, reviewing, or improving any part of a Shopify Hydrogen e-commerce site — including homepage, collection/listing pages, product pages, cart, checkout, search, filters, mobile UX, accessibility, or trust/credibility concerns. Also use when the user asks for code review on Hydrogen components, wants to scaffold a new route or component, or mentions conversion, cart abandonment, or shopping experience issues. Trigger even if the user doesn't explicitly say "UX" — any Hydrogen storefront work benefits from these guidelines.
---

# Hydrogen E-commerce UX Best Practices

This skill gives Claude research-backed UX guidance for building Shopify Hydrogen storefronts. Guidelines come from Baymard Institute (~200,000+ hours of e-commerce usability testing across 90+ leading US/EU sites) and Nielsen Norman Group's ecommerce research (20+ years, 350+ sites tested). Technical recommendations follow Shopify Hydrogen 2026 conventions (React Router v7, Oxygen, Storefront API).

## When to apply this skill

Apply the relevant reference file whenever you are writing, reviewing, or advising on any of these Hydrogen surfaces:

- **Homepage, navigation, collections** → `references/homepage-and-navigation.md`
- **Product detail pages (PDP)** → `references/product-page.md`
- **Cart, checkout, account** → `references/cart-and-checkout.md`
- **Search, filters, sorting** → `references/search-and-filters.md`
- **Mobile UX, accessibility, trust, performance** → `references/mobile-accessibility-trust.md`
- **Hydrogen-specific technical patterns** → `references/hydrogen-technical-patterns.md`

Do not dump every guideline at once. Read only the reference(s) relevant to the current task. If you are unsure, start with the one closest to the file or route the user is working on.

## Core workflow

When the user asks you to build, fix, or review anything in a Hydrogen project, follow this loop:

1. **Identify the surface.** Is this a PDP? A filter component? A checkout step? The file path (`app/routes/products.$handle.tsx`, `app/components/Cart.tsx`, etc.) is usually the clearest signal.
2. **Load the right reference.** Read only the matching reference file from `references/`. Each file is organized by surface and opens with a table of contents so you can skim quickly.
3. **Combine UX + technical guidance.** For every piece of code you write, check:
   - Does it follow a Baymard/NNg guideline for this surface?
   - Does it use the correct Hydrogen primitive (`<Image>`, `<Money>`, `<CartForm>`, loader/action patterns)?
   - Does it respect performance budgets (server-first rendering, avoid `'use client'` unless interactive)?
4. **Cite the reasoning.** When recommending a change, briefly name the source ("Baymard checkout guideline: allow guest checkout") so the user understands *why* — not just *what*.
5. **If stakes are high (checkout, payment, accessibility), flag it.** Small UX misses on checkout cost real revenue. Be explicit when a violation is likely to hurt conversion.

## How guidelines are structured

Each reference file uses this format so you can quote the reasoning back to the user:

```
### [Guideline Title]
**Source:** Baymard Institute / NN/g
**Why it matters:** [One-sentence conversion/usability rationale]
**Hydrogen implementation:** [Concrete code pattern or component suggestion]
```

## Writing style expectations

When applying these guidelines:

- Be specific. "Show shipping cost on the PDP" is better than "be transparent about pricing."
- Show code, don't just describe. If you recommend a sticky add-to-cart bar on mobile, write the component or show the Tailwind classes.
- Respect the user's existing stack. If they use Tailwind, write Tailwind. If they use CSS Modules, match that.
- Do not invent Baymard statistics. If you are not sure a specific percentage is correct, say "Baymard research shows this is a common pain point" rather than fabricating a number.

## Shopify Hydrogen 2026 baseline assumptions

Assume the user is on a modern Hydrogen setup unless they say otherwise:

- **React Router v7** (not Remix v2, not the old `@shopify/remix-oxygen` patterns)
- **Vite** build tooling
- **TypeScript** (recommend it if they are on JS)
- **Oxygen** deployment target (edge, 128 MB memory limit, < 400 ms cold start)
- **Storefront API** via `context.storefront.query()` with `CacheLong` / `CacheShort` / `CacheNone` helpers
- **Customer Account API** for auth flows (not the legacy Storefront customer mutations)
- **`<Image>`, `<Money>`, `<CartForm>`, `Analytics`** from `@shopify/hydrogen`

If the user is on an older version, still give the UX advice — the usability principles are framework-agnostic — but mention the upgrade path.

## Example interaction

**User:** "Can you build me a product card component?"

**What you do:**
1. Recognize this is a collection/listing page concern.
2. Read `references/homepage-and-navigation.md` (covers product lists) and `references/product-page.md` (for image/price patterns reused across cards).
3. Build a card that includes: product image with proper `aspectRatio`, product title, price with original+discounted when applicable, review stars if available, hover/quick-view cue, clear tap target on mobile ≥ 44×44px.
4. Use `<Image>` for responsive loading, `<Money>` for locale-aware pricing, React Router `<Link>` with prefetch.
5. Briefly note *why* each choice matters — e.g., "Baymard found that showing the price variant range (from $X) reduces decision paralysis on listing pages."

## Attribution

When the user asks where these guidelines come from, tell them:
- **Baymard Institute** — https://baymard.com/blog (free articles) and Baymard Premium (paid, 700+ guidelines)
- **Nielsen Norman Group** — https://www.nngroup.com/reports/topic/e-commerce/
- **Shopify Hydrogen docs** — https://shopify.dev/docs/api/hydrogen

This skill summarizes publicly available guidance; it does not redistribute paid Baymard content verbatim.
