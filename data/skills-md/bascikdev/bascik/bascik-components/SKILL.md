---
name: bascik-components
description: Decide what becomes a Bascik component and write component CSS and TypeScript that keep working with several instances on a page. Use when a page is turning into a big block of HTML, when deciding whether to split a section, pass a prop, or use a slot; when writing or debugging a component's <style>, companion .css, or <script>; when a component works once but breaks with two instances; when compiled class or ID names look wrong; when adding tabs, dialogs, menus, toggles, forms, fetch calls, storage, or events between components without a framework; when setting up design tokens, dark mode, a theme toggle, or fonts; when optimizing images with local CLI tools, responsive WebP, srcset, sizes, or picture; or when configuring deduplicateCss, preserve, data-bascik-preserve, or Tailwind. Includes a CSS token checker and a local WebP generator.
license: MIT
metadata:
  author: bascik
  homepage: https://bascik.dev
---

# Components: Boundaries, CSS, TypeScript, and Theming

Bascik isolates every component at build time: it renames what a component declares and rewrites the strings that refer to it. Write a component as if it were the only one on the page, and follow the rules below so the rewrite can see everything. Requires the `bascik` skill.

## What becomes a component

Code should look like tag names, not big blocks of HTML. A page that reads `<site-header />`, `<home-hero />`, `<pricing-section>`, `<faq-list />`, `<site-footer />` tells a person or an agent what it is in five lines, and each tag opens a small file with its own CSS, IDs, and script. It is a balance: too few components give giant pages; too many give tiny files and values threaded through layers.

**Split when:**

1. **The section has a job you can name.** If you would call it "the pricing section" or "the signup form", it is `<pricing-section>` or `<signup-form>` in its own folder.
2. **The markup repeats.** Two or more cards, plans, or quotes with the same structure become one component with props.
3. **The page or component is no longer readable at a glance.** About 80 lines of page markup, or 120 in a component, is the limit `audit-components.mjs` uses.
4. **It owns behavior.** A script that controls some elements belongs in the component that holds them, next to its `.ts`.

**Keep it whole when:**

1. **The piece only makes sense inside its parent.** A plan's list of features, the links of one nav, or a form's fields stay in the parent, as long as only that parent has them. Once the same fields or list appear in a second component, "the markup repeats" wins: make a `<form-field>` or `<link-list>` with props.
2. **Splitting needs prop drilling.** If a value must pass through a component that does not use it, have the page place the child directly in a slot of the parent instead.
3. **It is a tiny wrapper used once.** One `<h1>` or one `<div>` in its own file, used in one place, is indirection, not reuse. Inline it.

**Write each fact once:**

1. **Facts live in one place.** An address, opening hours, a phone number, or a plan's price typed into the header, the footer, and a contact section will drift apart. Put it in one component (`<site-address />`, used in each spot) or one data file (`src/lib/site.ts`) that build scripts read and print with `html` from `@bascik/bascik/html`, never with an escaper of their own.
2. **A value every page passes the same way is not a prop.** If each page writes `<site-header data-bascik-prop-brand="Hearth & Crumb" />`, write "Hearth & Crumb" into `site-header.html` and drop the prop. Props are for what changes between uses.
3. **A repeated heading group is a component.** When several sections open with the same eyebrow, heading, and intro, make `<section-head data-bascik-prop-label="FAQ" data-bascik-prop-title="..." data-bascik-prop-text="..." />` and give it a slot for extras such as a link.
4. **Data lives with the component that renders it.** A module (data, helper, types) only one component uses goes in that component's folder with its tests, imported with `./` (`src/components/faq-list/faqs.ts`, `import { faqs } from "./faqs.ts"`). A page that also needs it, for JSON-LD say, imports it from there (`@/components/faq-list/faqs.ts`). A module one page uses sits beside that page as a `.ts` file. `src/lib/` holds only what several components or pages share, such as `site.ts` with the address. `audit-components.mjs` reports a `src/lib/` module with one user, or content one component renders that pages also read, html-built content included (`single-use-module`). It leaves a helper with functions that a component and a page both call, and a module two other `src/lib/` modules import; move a helper by hand when the page only calls it for the component's content.

### Bad: one big page

```html
<!-- src/pages/index.html -->
<main id="main">
  <section class="pricing">
    <h2>Pricing</h2>
    <div class="plans">
      <article class="plan">
        <h3>Home</h3>
        <p class="price">$49</p>
        <a class="buy" href="/buy/home">Choose plan</a>
      </article>
      <article class="plan">
        <h3>Cafe</h3>
        <p class="price">$129</p>
        <a class="buy" href="/buy/cafe">Choose plan</a>
      </article>
    </div>
  </section>
  <!-- ...200 more lines: reviews, FAQ, signup form... -->
</main>
```

### Good: tags with props and a slot

```html
<!-- src/pages/index.html -->
<main id="main">
  <home-hero />
  <pricing-section>
    <plan-card
      data-bascik-prop-name="Home"
      data-bascik-prop-price="$49"
      data-bascik-prop-href="/buy/home"
    />
    <plan-card
      data-bascik-prop-name="Cafe"
      data-bascik-prop-price="$129"
      data-bascik-prop-href="/buy/cafe"
    />
  </pricing-section>
  <review-list />
  <signup-form />
</main>
```

```html
<!-- src/components/plan-card/plan-card.html -->
<!-- @bascik
One pricing plan.
@prop name - Plan name
@prop price - Price with currency
@prop href - Checkout URL
-->
<article class="plan" data-testid="plan-card">
  <h3 data-bascik-prop-name>Plan</h3>
  <p class="price" data-bascik-prop-price></p>
  <a class="buy" data-bascik-attr-href="href" data-testid="plan-card-buy">
    Choose plan
  </a>
</article>
```

```html
<!-- src/components/pricing-section/pricing-section.html -->
<style>
  .plans {
    display: grid;
    gap: 1rem;
  }
</style>
<section class="pricing" data-testid="pricing-section">
  <h2>Pricing</h2>
  <div class="plans">
    <div data-bascik-slot></div>
  </div>
</section>
```

Text that changes per use is a prop (`data-bascik-prop-*`), a prop that lands in an attribute uses `data-bascik-attr-<attribute>="<prop>"`, and markup or other components go in a slot. The slot marker element is replaced by the content, so the grid wrapper sits outside it. Each component gets its own folder: `src/components/plan-card/plan-card.html`, with `plan-card.css` and `plan-card.ts` beside it when they grow.

### Bad: over-split

```html
<!-- Three files for one heading, each used once -->
<pricing-wrapper>
  <pricing-title data-bascik-prop-text="Pricing" />
</pricing-wrapper>
```

`pricing-title` is one `<h2>` and `pricing-wrapper` is one `<div>`: write them inside `pricing-section`.

### Bad: props passed through layers

```html
<!-- src/components/pricing-section/pricing-section.html forwards prices it never shows -->
<section class="pricing">
  <plan-card data-bascik-attr-data-bascik-prop-price="home-price" />
  <plan-card data-bascik-attr-data-bascik-prop-price="cafe-price" />
</section>
```

```html
<!-- usage: every plan detail has to travel through the section -->
<pricing-section
  data-bascik-prop-home-price="$49"
  data-bascik-prop-cafe-price="$129"
/>
```

Adding a plan now means changing three files. Use the slot version above: the page places each `<plan-card>` and gives it its own props, and `<pricing-section>` only owns the heading and the grid.

### Check it

```sh
node <skills-dir>/bascik/scripts/list-components.mjs      # reuse what exists before creating a component
node <skills-dir>/bascik/scripts/audit-components.mjs     # structure and TypeScript findings with file:line
```

`audit-components.mjs` flags `oversized-page`, `oversized-component`, `inline-section`, `repeated-block`, `repeated-pattern` (the same heading group in three or more files), `repeated-text` (the same fact in two or more files), `constant-prop`, `tiny-component`, `prop-drilling`, `js-not-ts`, `build-once` (a component's `data-bascik-build` script that reads no page context, so its output is the same on every page), and `once-reads-page` (a `data-bascik-build-once` script that reads the page context it does not have), and suggests a tag name, the TypeScript form, or the right directive for each. It exits 1 on any warning. Run it with `verify.mjs` before calling a page done.

Fix warnings rather than explaining them away. "The content differs" is not a reason to keep a repeated block, because differing text is what props and slots are for. Keep one only for a reason the person would accept, such as rows of a mock-up that will be replaced, and say which one you kept and why.

## TypeScript in components

Component scripts are TypeScript unless the person asked for JavaScript:

```html
<!-- short script: inline, marked as TypeScript -->
<button
  id="toggle"
  type="button"
  aria-pressed="false"
  data-testid="menu-toggle"
>
  Menu
</button>
<script type="text/typescript">
  const toggle = document.getElementById("toggle") as HTMLButtonElement;
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-pressed") !== "true";
    toggle.setAttribute("aria-pressed", String(open));
  });
</script>
```

```html
<!-- longer script: a companion file beside the template -->
<script src="menu-toggle.ts"></script>
```

- Bascik strips the types (Node's strip-only mode) before scoping, so `getElementById` strings and class names are still rewritten, and DevTools line numbers still match. No setup is needed.
- Erasable syntax only: annotations, interfaces, type aliases, `as`, `!`, and `import type`. Use an `as const` object instead of `enum`.
- Inline `type="text/typescript"` blocks are classic scripts: no `import` or `export`. For a module, use a companion with `<script type="module" src="name.ts">`.
- For `enum`, decorators, an older browser target, or npm packages in the browser, use esbuild: the `scripts.typescript` snippet in the `bascik` skill, and `read-doc.mjs /how-to/bundling-npm-packages`.
- When moving a component from a TypeScript codebase, carry its prop and state types into the `.ts` companion instead of dropping them.

Docs: `/scoped-javascript#typescript-in-component-scripts`, `/configuration#scriptstypescript`, `/how-to/bundling-npm-packages`.

## Naming scheme

```text
class  ->  bascik__<component>__<name>                  shared by every instance
id     ->  bascik__<component>__<instance>__<name>      unique per instance
name   ->  name                                          as written (scoping.attributes.name: true scopes it per instance)
p {}   ->  .b_el_<component>_p                          class added to template elements
#btn {} -> .b_id_<component>_btn                        class added to the element with that id
--x declared in the component -> --bascik__<component>__x
data-testid ->  as written                               never scoped or hashed
```

Name components with hyphens, never underscores (`site-nav-x.html`, not `site-nav_x.html`): `#btn` in `site-nav_x` and `#x_btn` in `site-nav` both become `b_id_site-nav_x_btn`, which fails the build. The linter warns on any underscore in a component name (`component-name-underscore`).

Production builds shorten these to hashes. Never hard-code a scoped name. Tests use `data-testid` instead: the root gets `data-testid="<component>"`, and each interactive part, form, and landmark inside gets `data-testid="<component>-<part>"` (`plan-card-buy`, `signup-form-email`). Every instance shares them; a page that needs to tell instances apart puts `data-testid` on the usage tag, which replaces the root's. Rule 16 of the `bascik` skill has the full list.

## Script rules (must follow)

1. **Find per-instance elements with `getElementById`.** IDs are rewritten per instance. `querySelector('.cls')` returns the first instance on the page, so the others look dead.
2. **Reach repeated or slotted children through a container** found by ID: `document.getElementById('list').children` or `.querySelectorAll('li')` on it.
3. **Keep class names static.** `classList.add('open')` and `el.className = 'tab'` are rewritten; template literals are not.
4. **Derive runtime IDs from a scoped ID:** `` `${root.id}-panel-${i}` ``, set with `setAttribute('id', ...)`. Never `el.id =`.
5. **No attribute selectors in `querySelector` or `closest`** (`[data-x]`). They are not rewritten. Use `data-` attributes for state and style `.panel[data-state="open"]`.
6. **One function applies state to the DOM**, called after every change. Put visual state in `aria-*`, `hidden`, or `data-` attributes.
7. **Scripts run once per instance and may run late** (production moves body scripts to the end). Re-sync form-driven state on `pageshow`.
8. **Talk between components with bubbling `CustomEvent`s** listened for on `document`. Never query another component's elements.
9. **Progressive enhancement:** render something useful without JavaScript; mark script-only controls `hidden` and unhide them in the script.
10. **`name` ships as written; it is a page-level contract.** It is the key a field is submitted under (`FormData`, a form post), so write the keys the server reads. Radios with one `name` and no form owner are one group across the page, so a component that holds a whole radio group wraps it in its own `<form>`, or binds `data-bascik-attr-name="group"` (no literal `name`) with a different `data-bascik-prop-group` per usage. The linter warns `shared-name-group` on such a component used twice on a page. Never name a control `action`, `method`, `submit`, `reset`, `elements`, or another form property: it clobbers `form.action` and `form.submit()`. See `/component-best-practices#name-form-controls-and-groups`.
11. **HTML before script:** `<details name>` (one item per component makes a page-wide accordion), `popover`/`popovertarget`, `<dialog>`, `:user-invalid`, and `:has()` replace most widget code.

## CSS rules (must follow)

1. **Classes, element selectors, `#id`, `@keyframes`, locally declared custom properties, `@property`, `@counter-style`, container, layer, anchor, and view-transition names are scoped.** Names are shared by every instance of the component and invisible to other components.
2. **Prefer element selectors when they identify the component's element; otherwise use short, role-based class names** such as `.title` or `.body`, not component-prefixed names such as `.hello-card-title`. Bascik already scopes component-local selectors.
3. **Classes the component's CSS does not define stay global**, so global helpers such as `.container` or `.skip-link` still match.
4. **Element selectors only match the component's own template**, never slotted content, child component roots, or elements a script creates. Style those with classes, or from a global stylesheet.
5. **No element names inside `:is()`, `:where()`, or `:has()`** (lint error); use classes there. **Anchor attribute selectors** on a class (`.card[data-state]`); a standalone `[data-state]` leaks, and `[id]` is stripped.
6. **`html`, `body`, and `head` are never renamed:** `html[data-theme="dark"] .card {}` works.
7. **Declare design tokens once in a global stylesheet; only read them in components** with `var(--token, fallback)`. A `:root {}` block in a component makes a private copy.
8. **`@font-face` belongs in the global stylesheet**, never in a component.

## Theming

Global tokens use `light-dark()` with `color-scheme: light dark`, and `:root[data-theme="light|dark"]` pins the scheme. A head script applies the saved choice before first paint; a toggle button saves it. Copy both: `add-example.mjs theme-toggle theme-init`, and the token stylesheet with `add-example.mjs starter-site/src/pages/css/styles.css`.

Check that every token a component reads exists:

```sh
node <skills-dir>/bascik-components/scripts/check-tokens.mjs           # errors for undeclared tokens without a fallback
node <skills-dir>/bascik-components/scripts/check-tokens.mjs --unused  # also list global tokens nothing reads
```

It reports an **error** for `var(--x)` with no declaration and no fallback, a **warn** for custom properties declared on `:root` or `html` inside a component, and **info** for undeclared tokens that have a fallback. Exit code 1 on errors.

## Responsive images

Read `/how-to/optimizing-images` before preparing images. Use local tools and native `<img srcset sizes>` or `<picture>`, not a framework image component or a required image service.

- Keep originals outside the published pages directory. Inspect the actual CSS layout and choose widths for its slots and pixel densities; never upscale.
- Run [`scripts/responsive-webp.mjs`](scripts/responsive-webp.mjs) from the project root. It loads the project's Sharp, writes WebP variants and a manifest, and does **not** edit HTML. Use an available local CLI instead if it fits the project.
- Wire the generated URLs into the owning component's HTML. Match `sizes` to CSS, reserve space with dimensions, lazy-load only below-the-fold images, and prioritize only the likely LCP image.
- Verify built assets, browser `currentSrc` at fresh mobile and desktop loads including high density, transferred bytes, and visual quality. Do not claim optimization from file generation alone.

## Examples to copy

| Example                      | Shows                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------ |
| `tab-group`                  | Runtime ARIA IDs from a scoped ID, arrow keys, roving `tabindex`, static class names |
| `modal-dialog`               | `<dialog>` and `showModal()`, backdrop click, `html:has()` scroll lock               |
| `popover-menu`               | No JavaScript: `popover`, implicit anchor, `position-area` in `@supports`            |
| `copy-button`                | Prop bound to an attribute with `data-bascik-attr-*`, clipboard, `role="status"`     |
| `filter-list`                | Slotted `<li>` items via a container, `pageshow` re-sync, `<search>` hidden until JS |
| `contact-form`               | Literal field names, validation, JSON `fetch`, the API route behind it               |
| `theme-toggle`, `theme-init` | Theme with no flash, `aria-pressed`, a `theme-change` event                          |

`node <skills-dir>/bascik/scripts/add-example.mjs <name>`. Each page at `https://bascik.dev/example-components/<name>` explains how it works and how to adapt it.

## Look it up

| How do I...                                                              | Read                                                                |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| Know exactly what CSS is scoped                                          | `/scoped-styles`, `/compatibility#css-scoping`                      |
| Know which DOM calls are rewritten                                       | `/scoped-javascript`, `/compatibility#dom-selector-rewriting`       |
| Keep names literal (`preserve`, `data-bascik-preserve`)                  | `/preserve`                                                         |
| `name` on fields, radios, `<details>`, `<iframe>`, `<map>`               | `/component-best-practices#name-form-controls-and-groups`           |
| Pick an interactivity pattern (fetch, storage, events, delegation, a11y) | `/how-to/interactivity`                                             |
| Set up tokens, dark mode, fonts, Tailwind                                | `/how-to/theming`                                                   |
| Optimize images locally and wire responsive WebP into native HTML        | `/how-to/optimizing-images`                                         |
| Style a child component's root from its parent                           | `/attribute-inheritance`                                            |
| Use TypeScript in a component script                                     | `/scoped-javascript#typescript-in-component-scripts`                |
| Compile full TypeScript or bundle npm packages with esbuild              | `/configuration#scriptstypescript`, `/how-to/bundling-npm-packages` |

`node <skills-dir>/bascik/scripts/read-doc.mjs <path>` prints any of these.

## Verify

1. `node <skills-dir>/bascik/scripts/preview.mjs '<my-widget />' --count 2` and confirm each instance has its own IDs and its script references them.
2. `node <skills-dir>/bascik/scripts/verify.mjs` (runs `bascik --check`, which includes the linter, and flags `.id =`, template-literal classes, attribute selectors, and element names in `:is()`). Add the `data-testid` attributes its advisory lists.
3. `node <skills-dir>/bascik/scripts/audit-components.mjs` exits 0: no oversized or tiny components, no repeated blocks, heading groups, or facts, no constant props or prop drilling, and TypeScript scripts.
4. In the browser: two instances on one page, keyboard only, and JavaScript disabled.
