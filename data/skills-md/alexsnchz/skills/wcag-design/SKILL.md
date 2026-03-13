---
name: wcag-design
description: "Create accessible, production-grade frontend interfaces that conform to WCAG 2.2 AA standards while maintaining high design quality. Use this skill when building any web component, page, dashboard, or application where accessibility compliance (WCAG, ADA, Section 508, EN 301 549) is required or desired, or when auditing/fixing accessibility issues in existing UI code. Combines comprehensive W3C WAI accessibility knowledge with distinctive frontend design principles."
---

# WCAG-Design Skill

This skill guides the creation of **accessible, visually distinctive** frontend interfaces that conform
to WCAG 2.2 AA standards. Accessibility and design quality are not opposing forces — the best
accessible interfaces are also beautifully designed.

---

## Part 1 — WCAG Fundamentals

### What is WCAG?

The **Web Content Accessibility Guidelines (WCAG)** is the global standard for web accessibility,
published by the W3C through the Web Accessibility Initiative (WAI). WCAG defines how to make web
content accessible to people with disabilities including blindness, low vision, deafness, hearing
loss, limited movement, photosensitivity, speech disabilities, and cognitive/learning disabilities.

### Version History

| Version | Year | Notes |
|---------|------|-------|
| WCAG 1.0 | 1999 | First W3C accessibility recommendation |
| WCAG 2.0 | 2008 | Major restructure with testable success criteria |
| WCAG 2.1 | 2018 | +17 new criteria for mobile, low vision, cognitive |
| WCAG 2.2 | 2023 | +9 new criteria, removed 4.1.1 Parsing; **current standard** |
| WCAG 3.0 | ~2028 | Draft; plain language, outcome-oriented model |

**Backward compatibility**: Content conforming to WCAG 2.2 also conforms to 2.1 and 2.0.

---

## Part 2 — The Four POUR Principles

Every WCAG success criterion maps to one of four principles:

### 1. Perceivable (P)
All information and UI components must be presentable in ways users can perceive.
- Text alternatives for non-text content
- Captions and audio descriptions for media
- Adaptable content presentation
- Sufficient color contrast and readability

### 2. Operable (O)
All UI components and navigation must be operable.
- Full keyboard accessibility
- No keyboard traps
- Sufficient time for interactions
- No seizure-inducing content
- Multiple input modalities (keyboard, touch, voice)
- Accessible focus management

### 3. Understandable (U)
Users must understand the content and how the interface works.
- Readable and understandable text
- Predictable, consistent behavior
- Input assistance and error recovery
- Clear language and definitions

### 4. Robust (R)
Content must work reliably with current and future technologies, especially assistive technologies.
- Valid, well-formed markup
- Compatible with browsers and assistive technologies
- Proper semantic structure

---

## Part 3 — Conformance Levels

| Level | Criteria Count | Description |
|-------|---------------|-------------|
| **A** | 32 | Minimum — basic accessibility, foundational compliance |
| **AA** | +24 (56 total) | Recommended — most legal requirements; addresses common barriers |
| **AAA** | +31 (87 total) | Enhanced — highest level; not always required |

**Target: WCAG 2.2 AA** — This is the level required by most accessibility laws (ADA, EN 301 549,
Section 508, Accessibility for Ontarians with Disabilities Act, etc.).

---

## Part 4 — Complete WCAG 2.2 Success Criteria Reference

### PRINCIPLE 1: PERCEIVABLE

#### Guideline 1.1 — Text Alternatives
| Criterion | Level | Rule |
|-----------|-------|------|
| 1.1.1 Non-text Content | A | All non-text content has a text alternative (images, icons, charts, buttons) |

#### Guideline 1.2 — Time-based Media
| Criterion | Level | Rule |
|-----------|-------|------|
| 1.2.1 Audio-only and Video-only (Prerecorded) | A | Provide transcript or audio description |
| 1.2.2 Captions (Prerecorded) | A | Captions for all prerecorded audio in multimedia |
| 1.2.3 Audio Description or Media Alternative (Prerecorded) | A | Provide audio description or full text alternative |
| 1.2.4 Captions (Live) | AA | Captions for all live multimedia |
| 1.2.5 Audio Description (Prerecorded) | AA | Audio description for all prerecorded video |
| 1.2.6 Sign Language (Prerecorded) | AAA | Sign language interpretation for prerecorded audio |
| 1.2.7 Extended Audio Description (Prerecorded) | AAA | Extended audio description where pauses are insufficient |
| 1.2.8 Media Alternative (Prerecorded) | AAA | Full text alternative for all prerecorded media |
| 1.2.9 Audio-only (Live) | AAA | Alternative for all live audio-only content |

#### Guideline 1.3 — Adaptable
| Criterion | Level | Rule |
|-----------|-------|------|
| 1.3.1 Info and Relationships | A | Structure and relationships conveyed through presentation must be programmatically determinable |
| 1.3.2 Meaningful Sequence | A | Reading and navigation order is logical |
| 1.3.3 Sensory Characteristics | A | Instructions don't rely solely on color, size, shape, visual location, or sound |
| 1.3.4 Orientation | AA | Content not restricted to portrait or landscape orientation |
| 1.3.5 Identify Input Purpose | AA | Input fields have programmatically identified purpose (autocomplete) |
| 1.3.6 Identify Purpose | AAA | Purpose of buttons, links, and controls can be programmatically determined |

#### Guideline 1.4 — Distinguishable
| Criterion | Level | Rule |
|-----------|-------|------|
| 1.4.1 Use of Color | A | Color is not the only visual means of conveying information |
| 1.4.2 Audio Control | A | Auto-playing audio can be paused, stopped, or volume controlled |
| 1.4.3 Contrast (Minimum) | AA | **4.5:1** for normal text; **3:1** for large text |
| 1.4.4 Resize Text | AA | Text can be resized to 200% without loss of content |
| 1.4.5 Images of Text | AA | Use actual text instead of images of text where possible |
| 1.4.6 Contrast (Enhanced) | AAA | **7:1** for normal text; **4.5:1** for large text |
| 1.4.7 Low or No Background Audio | AAA | Audio-only content clearly audible over background |
| 1.4.8 Visual Presentation | AAA | Text width limited, line spacing adjustable, no full justification |
| 1.4.9 Images of Text (No Exception) | AAA | No images of text except logos |
| 1.4.10 Reflow | AA | Content presentable without horizontal scrolling at 320px wide |
| 1.4.11 Non-text Contrast | AA | UI components and graphical elements have **3:1** contrast ratio |
| 1.4.12 Text Spacing | AA | No loss of content when line height ≥1.5×, spacing ≥0.12em, word spacing ≥0.16em |
| 1.4.13 Content on Hover or Focus | AA | Hoverable/focusable content is dismissible, hoverable, and persistent |

---

### PRINCIPLE 2: OPERABLE

#### Guideline 2.1 — Keyboard Accessible
| Criterion | Level | Rule |
|-----------|-------|------|
| 2.1.1 Keyboard | A | All functionality operable via keyboard |
| 2.1.2 No Keyboard Trap | A | User can navigate away from any component using keyboard |
| 2.1.3 Keyboard (No Exception) | AAA | All functionality operable via keyboard — no exceptions |
| 2.1.4 Character Key Shortcuts | A | Single-character shortcuts can be disabled or remapped |

#### Guideline 2.2 — Enough Time
| Criterion | Level | Rule |
|-----------|-------|------|
| 2.2.1 Timing Adjustable | A | Time limits can be turned off, adjusted, or extended (≥10× default) |
| 2.2.2 Pause, Stop, Hide | A | Auto-moving/blinking/scrolling content can be paused, stopped, or hidden |
| 2.2.3 No Timing | AAA | No time restrictions except for real-time events |
| 2.2.4 Interruptions | AAA | User can postpone or suppress all interruptions |
| 2.2.5 Re-authenticating | AAA | No data lost when re-authenticating after timeout |
| 2.2.6 Timeouts | AAA | Users warned about session inactivity timeout |

#### Guideline 2.3 — Seizures and Physical Reactions
| Criterion | Level | Rule |
|-----------|-------|------|
| 2.3.1 Three Flashes or Below Threshold | A | No flashing content more than 3 times/second (or below threshold) |
| 2.3.2 Three Flashes | AAA | All content restricted to ≤3 flashes/second |
| 2.3.3 Animation from Interactions | AAA | Motion animation triggered by interaction can be disabled |

#### Guideline 2.4 — Navigable
| Criterion | Level | Rule |
|-----------|-------|------|
| 2.4.1 Bypass Blocks | A | Mechanism to skip repeated blocks (skip nav link) |
| 2.4.2 Page Titled | A | Web pages have descriptive titles |
| 2.4.3 Focus Order | A | Focus order is logical and meaningful |
| 2.4.4 Link Purpose (In Context) | A | Link purpose clear from link text or context |
| 2.4.5 Multiple Ways | AA | Multiple ways to locate a page (search, sitemap, navigation) |
| 2.4.6 Headings and Labels | AA | Headings and labels describe topic or purpose |
| 2.4.7 Focus Visible | AA | Keyboard focus indicator is visible |
| 2.4.8 Location | AAA | User knows their location within a set of pages |
| 2.4.9 Link Purpose (Link Only) | AAA | Link purpose clear from link text alone |
| 2.4.10 Section Headings | AAA | Section headings organize content |
| 2.4.11 Focus Not Obscured (Minimum) ⭐ NEW 2.2 | AA | Focused element not entirely hidden by sticky/fixed content |
| 2.4.12 Focus Not Obscured (Enhanced) ⭐ NEW 2.2 | AAA | Focused element fully visible |
| 2.4.13 Focus Appearance ⭐ NEW 2.2 | AAA | Focus indicator: ≥2px outline, ≥3:1 contrast change |

#### Guideline 2.5 — Input Modalities
| Criterion | Level | Rule |
|-----------|-------|------|
| 2.5.1 Pointer Gestures | A | Path-based gestures have single-pointer alternative |
| 2.5.2 Pointer Cancellation | A | Pointer actions activate on "up" event, not "down" |
| 2.5.3 Label in Name | A | Accessible name contains the visible label text |
| 2.5.4 Motion Actuation | A | Motion-triggered functions have UI alternative and can be disabled |
| 2.5.5 Target Size (Enhanced) | AAA | Touch targets ≥44×44 CSS pixels |
| 2.5.6 Concurrent Input Mechanisms | AAA | No restriction on input modality |
| 2.5.7 Dragging Movements ⭐ NEW 2.2 | AA | Drag-only functionality has single-pointer alternative |
| 2.5.8 Target Size (Minimum) ⭐ NEW 2.2 | AA | Touch targets ≥24×24 CSS pixels or adequate spacing |

---

### PRINCIPLE 3: UNDERSTANDABLE

#### Guideline 3.1 — Readable
| Criterion | Level | Rule |
|-----------|-------|------|
| 3.1.1 Language of Page | A | Default human language programmatically identified (lang attribute) |
| 3.1.2 Language of Parts | AA | Language changes in content are marked |
| 3.1.3 Unusual Words | AAA | Definitions for jargon, idioms, technical terms |
| 3.1.4 Abbreviations | AAA | Abbreviations expanded on first use |
| 3.1.5 Reading Level | AAA | Text at lower secondary education level or simplified version available |
| 3.1.6 Pronunciation | AAA | Pronunciation provided for ambiguous words |

#### Guideline 3.2 — Predictable
| Criterion | Level | Rule |
|-----------|-------|------|
| 3.2.1 On Focus | A | No context change when component receives focus |
| 3.2.2 On Input | A | Changing settings doesn't automatically submit form |
| 3.2.3 Consistent Navigation | AA | Navigation mechanisms in same relative order across pages |
| 3.2.4 Consistent Identification | AA | Components with same function identified consistently |
| 3.2.5 Change on Request | AAA | Context changes only at user request |
| 3.2.6 Consistent Help ⭐ NEW 2.2 | A | Help mechanisms in same location across pages |

#### Guideline 3.3 — Input Assistance
| Criterion | Level | Rule |
|-----------|-------|------|
| 3.3.1 Error Identification | A | Errors identified and described in text |
| 3.3.2 Labels or Instructions | A | Labels or instructions provided for all inputs |
| 3.3.3 Error Suggestion | AA | Suggestions provided for input errors where known |
| 3.3.4 Error Prevention (Legal, Financial, Data) | AA | Critical submissions are reversible, checked, or confirmed |
| 3.3.5 Help | AAA | Context-sensitive help available |
| 3.3.6 Error Prevention (All) | AAA | All inputs can be reversed, checked, or confirmed |
| 3.3.7 Redundant Entry ⭐ NEW 2.2 | A | Previously entered info not required again in same session |
| 3.3.8 Accessible Authentication (Minimum) ⭐ NEW 2.2 | AA | Authentication without cognitive function test or memory requirement |
| 3.3.9 Accessible Authentication (Enhanced) ⭐ NEW 2.2 | AAA | Enhanced alternatives to cognitive function tests |

---

### PRINCIPLE 4: ROBUST

#### Guideline 4.1 — Compatible
| Criterion | Level | Rule |
|-----------|-------|------|
| ~~4.1.1 Parsing~~ | ~~A~~ | **Removed in WCAG 2.2** — obsolete due to HTML5 error correction |
| 4.1.2 Name, Role, Value | A | All components have accessible name, role, and state/value |
| 4.1.3 Status Messages | AA | Status messages announced to screen readers without focus change |

---

## Part 5 — Implementation Reference

### 5.1 Color Contrast Rules

| Context | AA Minimum | AAA Enhanced |
|---------|-----------|-------------|
| Normal text (<18px or <14px bold) | **4.5:1** | **7:1** |
| Large text (≥18px or ≥14px bold) | **3:1** | **4.5:1** |
| UI components & graphics | **3:1** | **3:1** |
| Placeholder text | **4.5:1** | — |
| Disabled elements | Exempt | Exempt |
| Decorative elements | Exempt | Exempt |

**Dark Mode Note:** Dark themes must still meet contrast ratios. Avoid pure black `#000000`
(causes halation/eye strain); use soft blacks like `#0f0f0f` or `#121212`.
High-saturation colors on dark backgrounds may vibrate visually — reduce saturation.

**Tools:** WebAIM Contrast Checker, Colour Contrast Analyser, axe DevTools, Chrome DevTools.

---

### 5.2 Semantic HTML — Use Native Elements First

Always prefer semantic HTML over ARIA. ARIA is a **supplement**, not a replacement.

```html
<!-- ✅ CORRECT: Semantic HTML -->
<header>…</header>
<nav aria-label="Main navigation">…</nav>
<main>
  <article>…</article>
  <aside>…</aside>
</main>
<footer>…</footer>

<!-- ❌ WRONG: div soup -->
<div class="header">…</div>
<div class="nav">…</div>
```

**Semantic element → landmark mapping:**
| Element | ARIA Landmark Role |
|---------|-------------------|
| `<header>` | `banner` |
| `<nav>` | `navigation` |
| `<main>` | `main` |
| `<aside>` | `complementary` |
| `<footer>` | `contentinfo` |
| `<section aria-label="...">` | `region` |
| `<form>` | `form` |

**Heading hierarchy rule:** Never skip levels. `<h1>` → `<h2>` → `<h3>` (not h1 → h3).
Multiple `<h1>` elements are acceptable but first should be page/section title.

---

### 5.3 WAI-ARIA Quick Reference

Use ARIA only when semantic HTML is insufficient. The **First Rule of ARIA**: don't use ARIA
if you can use a native HTML element or attribute with the semantics built in.

#### Landmark Roles
```html
<div role="banner">…</div>        <!-- Same as <header> -->
<div role="navigation">…</div>    <!-- Same as <nav> -->
<div role="main">…</div>          <!-- Same as <main> -->
<div role="complementary">…</div> <!-- Same as <aside> -->
<div role="contentinfo">…</div>   <!-- Same as <footer> -->
<div role="search">…</div>        <!-- Search region -->
<div role="region" aria-label="…">…</div> <!-- Generic named region -->
```

#### Widget Roles (Interactive Components)
```html
role="button"      <!-- Clickable element -->
role="checkbox"    <!-- Checkable input -->
role="radio"       <!-- Radio button -->
role="combobox"    <!-- Dropdown / autocomplete -->
role="listbox"     <!-- List for selection -->
role="option"      <!-- Item within listbox -->
role="menu"        <!-- Menu container -->
role="menuitem"    <!-- Menu item -->
role="tab"         <!-- Tab button -->
role="tablist"     <!-- Tab container -->
role="tabpanel"    <!-- Tab content panel -->
role="dialog"      <!-- Modal dialog -->
role="alertdialog" <!-- Alert modal -->
role="slider"      <!-- Range input -->
role="progressbar" <!-- Progress indicator -->
role="tooltip"     <!-- Tooltip -->
role="tree"        <!-- Tree widget -->
role="treeitem"    <!-- Tree item -->
role="grid"        <!-- Interactive data grid -->
role="gridcell"    <!-- Grid cell -->
```

#### Live Region Roles (Dynamic Content)
```html
role="alert"       <!-- Assertive: important time-sensitive info -->
role="status"      <!-- Polite: advisory info (status messages) -->
role="log"         <!-- Polite: ordered sequence of updates -->
role="timer"       <!-- Timer announcements -->

<!-- Equivalent ARIA live properties -->
aria-live="polite"    <!-- Announces after current speech -->
aria-live="assertive" <!-- Interrupts current speech (use sparingly) -->
aria-live="off"       <!-- No announcements (default) -->
aria-atomic="true"    <!-- Announce entire region on update -->
aria-relevant="additions text" <!-- What triggers announcement -->
```

#### Essential ARIA Properties
```html
<!-- Labeling -->
aria-label="Close dialog"
aria-labelledby="heading-id"
aria-describedby="description-id help-text-id"

<!-- State -->
aria-expanded="true|false"       <!-- Collapsible element open state -->
aria-selected="true|false"       <!-- Selection state -->
aria-checked="true|false|mixed"  <!-- Checkbox/switch state -->
aria-pressed="true|false|mixed"  <!-- Toggle button state -->
aria-disabled="true"             <!-- Disabled state -->
aria-hidden="true"               <!-- Hidden from AT -->
aria-invalid="true|false|grammar|spelling" <!-- Validation state -->
aria-busy="true|false"           <!-- Loading state -->

<!-- Relationships -->
aria-controls="panel-id"         <!-- Controls another element -->
aria-owns="list-id"              <!-- Owns child elements -->
aria-haspopup="true|menu|listbox|tree|grid|dialog" <!-- Has popup -->
aria-autocomplete="none|inline|list|both"  <!-- Autocomplete behavior -->

<!-- Range -->
aria-valuemin="0"
aria-valuemax="100"
aria-valuenow="50"
aria-valuetext="50 percent"      <!-- Human-readable value -->

<!-- Current location -->
aria-current="page|step|location|date|time|true|false"
```

---

### 5.4 Keyboard Navigation Implementation

Every interactive component must be fully keyboard-accessible.

#### Focus Management Rules
```css
/* NEVER do this without a custom replacement */
*:focus { outline: none; }

/* ✅ Custom focus indicator — meets WCAG 2.4.7 and 2.4.13 */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
  border-radius: 2px;
}

/* Different styles for mouse vs keyboard */
:focus:not(:focus-visible) { outline: none; }
:focus-visible { outline: 2px solid #005fcc; outline-offset: 2px; }
```

#### Tab Order
```html
<!-- ✅ Natural DOM order (preferred) -->
<!-- ✅ Use tabindex="0" to add element to tab order -->
<div role="button" tabindex="0">Custom Button</div>

<!-- ❌ NEVER use positive tabindex (breaks natural order) -->
<button tabindex="3">Bad</button>

<!-- Remove from tab order (but still scriptable) -->
<div tabindex="-1" id="modal-content">…</div>
```

#### Skip Navigation Link
```html
<!-- First element in <body> — visible on focus -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: 0.5rem 1rem;
  background: #000;
  color: #fff;
  z-index: 9999;
  transition: top 0.1s;
}
.skip-link:focus { top: 0; }
</style>

<main id="main-content">…</main>
```

#### Keyboard Patterns by Component
| Component | Key | Action |
|-----------|-----|--------|
| All | Tab | Move focus forward |
| All | Shift+Tab | Move focus backward |
| Button | Enter / Space | Activate |
| Link | Enter | Follow link |
| Checkbox | Space | Toggle |
| Radio Group | Arrow Keys | Select option |
| Select/Dropdown | Arrow Keys | Navigate; Enter select |
| Dialog | Escape | Close |
| Dialog | Tab | Cycle within dialog only |
| Menu | Arrow Keys | Navigate items |
| Menu | Escape | Close |
| Menu | Enter / Space | Activate item |
| Slider | Arrow Keys | Increment/Decrement |
| Slider | Home / End | Min / Max value |
| Tabs | Arrow Keys | Switch tabs |
| Tree | Arrow Keys | Expand/collapse/navigate |

#### Focus Trap for Modals
```javascript
// Trap focus within modal while open
function trapFocus(modal) {
  const focusable = modal.querySelectorAll(
    'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
  );
  const firstEl = focusable[0];
  const lastEl = focusable[focusable.length - 1];

  modal.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;
    if (e.shiftKey) {
      if (document.activeElement === firstEl) {
        e.preventDefault(); lastEl.focus();
      }
    } else {
      if (document.activeElement === lastEl) {
        e.preventDefault(); firstEl.focus();
      }
    }
  });
}
```

---

### 5.5 Accessible Component Patterns

#### Modal / Dialog
```html
<dialog
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
  id="my-modal"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-desc">Are you sure you want to delete this item?</p>
  <button type="button" autofocus>Cancel</button>
  <button type="button">Delete</button>
</dialog>
```
```javascript
// HTML5 <dialog> — built-in focus management + Escape handling
const modal = document.getElementById('my-modal');
const trigger = document.getElementById('open-btn');

trigger.addEventListener('click', () => modal.showModal());
modal.addEventListener('close', () => trigger.focus()); // Restore focus
```

#### Accessible Button (Custom)
```html
<!-- Prefer <button> whenever possible -->
<button type="button" aria-pressed="false" id="dark-toggle">
  <svg aria-hidden="true" focusable="false">…</svg>
  Dark Mode
</button>

<!-- Icon-only button: needs aria-label -->
<button type="button" aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false">…</svg>
</button>
```

#### Accordion
```html
<div class="accordion">
  <h3>
    <button
      type="button"
      aria-expanded="false"
      aria-controls="panel-1"
      id="btn-1"
    >Section Title</button>
  </h3>
  <div id="panel-1" role="region" aria-labelledby="btn-1" hidden>
    Panel content here
  </div>
</div>
```

#### Tabs
```html
<div role="tablist" aria-label="Settings sections">
  <button role="tab" aria-selected="true" aria-controls="panel-a" id="tab-a" tabindex="0">General</button>
  <button role="tab" aria-selected="false" aria-controls="panel-b" id="tab-b" tabindex="-1">Privacy</button>
</div>

<div role="tabpanel" id="panel-a" aria-labelledby="tab-a">…</div>
<div role="tabpanel" id="panel-b" aria-labelledby="tab-b" hidden>…</div>
```

#### Combobox / Autocomplete
```html
<label for="city-input">City</label>
<input
  type="text"
  id="city-input"
  role="combobox"
  aria-expanded="false"
  aria-haspopup="listbox"
  aria-autocomplete="list"
  aria-controls="city-list"
/>
<ul id="city-list" role="listbox" aria-label="Cities">
  <li role="option" id="opt-1">New York</li>
  <li role="option" id="opt-2">Los Angeles</li>
</ul>
```

#### Alert / Status Message
```html
<!-- Polite announcement (most cases) -->
<div role="status" aria-live="polite" aria-atomic="true">
  Form saved successfully.
</div>

<!-- Assertive announcement (errors only) -->
<div role="alert" aria-live="assertive" aria-atomic="true">
  Error: Please enter a valid email address.
</div>
```

---

### 5.6 Forms — Accessible Patterns

```html
<!-- ✅ Complete accessible form field -->
<div class="field">
  <label for="email">
    Email address
    <span aria-hidden="true" class="required">*</span>
    <span class="sr-only">(required)</span>
  </label>
  <input
    type="email"
    id="email"
    name="email"
    autocomplete="email"
    aria-required="true"
    aria-describedby="email-hint email-error"
    aria-invalid="false"
  />
  <p id="email-hint" class="hint">We'll never share your email.</p>
  <p id="email-error" class="error" role="alert" hidden>
    Please enter a valid email address.
  </p>
</div>

<!-- ✅ Grouped radio buttons -->
<fieldset>
  <legend>Notification preferences</legend>
  <label><input type="radio" name="notif" value="email"> Email</label>
  <label><input type="radio" name="notif" value="sms"> SMS</label>
  <label><input type="radio" name="notif" value="none"> None</label>
</fieldset>
```

**Form validation rules:**
- Validate on `blur` or `submit`, not on every keystroke
- Mark invalid fields with `aria-invalid="true"`
- Link error messages to fields via `aria-describedby`
- Use `role="alert"` on dynamically inserted error messages
- Never use placeholder text as the only label
- Provide autocomplete attributes for common fields

---

### 5.7 Images and Alt Text

```html
<!-- ✅ Informative image -->
<img src="chart.png" alt="Sales by region 2024: North 35%, South 28%, East 22%, West 15%">

<!-- ✅ Decorative image — empty alt required -->
<img src="divider.png" alt="">

<!-- ✅ Icon button — label on button, not image -->
<button aria-label="Search">
  <img src="magnifier.svg" alt="">
</button>

<!-- ✅ Complex diagram — short alt + detailed description -->
<figure>
  <img src="architecture.png" alt="System architecture diagram" aria-describedby="arch-desc">
  <figcaption id="arch-desc">
    Three-tier architecture: client tier connects to API gateway,
    which routes to microservices cluster, backed by PostgreSQL and Redis.
  </figcaption>
</figure>

<!-- ✅ CSS background image (decorative) — no alt needed -->
<div class="hero-bg" role="img" aria-label="Abstract blue wave">…</div>
<!-- OR if purely decorative: aria-hidden="true" -->
```

**Alt text guidelines:**
- Keep concise (≤125 characters typical; up to 250 for complex)
- Don't start with "Image of" or "Picture of"
- Describe purpose and content, not appearance alone
- For charts: include key data points
- For logos: use company name only

---

### 5.8 Typography Accessibility

```css
/* ✅ Accessible base typography */
html {
  font-size: 100%; /* Don't fix to px — respects user browser setting */
}

body {
  font-size: 1rem;      /* = 16px by default */
  line-height: 1.5;     /* Readable line spacing */
  max-width: 75ch;      /* Limit line length for readability */
  font-family: /* Choose a readable, designed typeface */;
}

/* ✅ Allow text spacing override (WCAG 1.4.12) */
* {
  line-height: inherit !important;    /* only in text-spacing tests */
  letter-spacing: inherit !important;
  word-spacing: inherit !important;
}

/* ✅ Respect zoom — use relative units */
h1 { font-size: clamp(1.5rem, 4vw, 2.5rem); }
p  { font-size: clamp(1rem, 1.2vw, 1.125rem); }
```

| Guideline | Minimum | Recommended |
|-----------|---------|-------------|
| Body text size | 14px (0.875rem) | 16px (1rem) |
| Line height | 1.4 | 1.5–1.6 |
| Max line length | — | 65–75 characters |
| Letter spacing | — | 0 to +0.05em |
| Paragraph spacing | — | 1.5× font-size |

**Font selection for accessibility:**
- Choose typefaces with clear letterform differentiation (b/d/p/q distinction)
- Avoid decorative fonts for body text
- Avoid light weights (< 300) at small sizes
- Ensure sufficient x-height for readability

---

### 5.9 Motion and Animation

```css
/* ✅ Respect prefers-reduced-motion — implement always */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* ✅ Progressive enhancement pattern */
.card { /* base — no motion */ }

@media (prefers-reduced-motion: no-preference) {
  .card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  }
}
```

**Motion rules:**
- Never autoplay videos with motion — use `prefers-reduced-motion`
- Flashing content: max 3 flashes/second (WCAG 2.3.1)
- Parallax, full-page scroll jacking → provide `prefers-reduced-motion: reduce` alternative
- Loading spinners are acceptable; full-page animated transitions are not without alternative

---

### 5.10 Responsive and Mobile Accessibility

```css
/* ✅ WCAG 1.4.10 Reflow — no horizontal scroll at 320px */
@media (max-width: 320px) {
  .container { width: 100%; padding: 0 1rem; }
  table { display: block; overflow-x: auto; }
}

/* ✅ WCAG 2.5.8 Minimum target size — 24×24px with spacing */
button, a, [role="button"] {
  min-height: 44px;      /* Meet WCAG 2.5.5 AAA for comfort */
  min-width: 44px;
  padding: 0.5rem 1rem;
}

/* ✅ Ensure focus remains visible at all sizes */
:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 3px;
}
```

**Mobile-specific considerations:**
- Use appropriate `type` attributes: `type="email"`, `type="tel"`, `type="number"`
- Don't disable zoom: `<meta name="viewport" content="width=device-width, initial-scale=1">` — NEVER add `user-scalable=no`
- Test with VoiceOver (iOS) and TalkBack (Android)
- Avoid hover-only interactions (no hover on touch devices)
- `inputmode` attribute for numeric, decimal, tel, email, url, search inputs

---

### 5.11 Tables

```html
<!-- ✅ Accessible data table -->
<table>
  <caption>Q4 2024 Sales by Region</caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Sales (USD)</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">North America</th>
      <td>$1,240,000</td>
      <td>+12%</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$3,890,000</td>
      <td>+8%</td>
    </tr>
  </tfoot>
</table>
```

Rules:
- Use `<caption>` to title every table
- Use `<th scope="col|row|colgroup|rowgroup">` for all header cells
- Use `<thead>`, `<tbody>`, `<tfoot>` for structure
- Don't use tables for layout; use CSS Grid/Flexbox instead

---

## Part 6 — Design with Accessibility: Frontend Aesthetic Guidelines

### 6.1 Design Thinking for Accessible Interfaces

Before coding, commit to a **bold, intentional aesthetic direction** while planning for accessibility:

- **Purpose**: What problem does this solve? Who uses it? What disabilities might users have?
- **Tone**: Choose an aesthetic extreme: brutally minimal, maximalist typographic, organic/natural,
  editorial, brutalist, retro-futuristic, luxury/refined, playful, industrial, etc.
- **Constraints**: Framework, performance, WCAG level (target AA), contrast requirements
- **Differentiation**: What makes this unforgettable AND accessible? Bold design and WCAG are compatible.

**Accessibility informs design**, it doesn't constrain it. The best accessible designs use:
- Strong color contrast as a design feature, not a liability
- Clear typographic hierarchy as a visual system
- Visible focus states as intentional design elements
- Semantic structure as compositional logic

### 6.2 Color System Design for Accessibility

**Design accessible color systems:**
```css
:root {
  /* Accessible palette using HSL for easier contrast calculation */
  --color-bg: hsl(220, 15%, 10%);        /* Near-black background */
  --color-surface: hsl(220, 12%, 15%);   /* Elevated surface */
  --color-border: hsl(220, 10%, 25%);    /* Subtle border */
  --color-text-primary: hsl(220, 10%, 95%);   /* High contrast text: >7:1 */
  --color-text-secondary: hsl(220, 8%, 70%);  /* Medium contrast: ~4.5:1 */
  --color-text-muted: hsl(220, 6%, 55%);      /* Low contrast: ~3:1 (large text only) */
  --color-accent: hsl(210, 100%, 65%);        /* Action color: verify contrast */
  --color-accent-hover: hsl(210, 100%, 72%);  /* Hover state */
  --color-error: hsl(0, 80%, 65%);            /* Error — verify 4.5:1 on bg */
  --color-success: hsl(145, 60%, 55%);        /* Success — verify 4.5:1 on bg */
  --color-warning: hsl(45, 90%, 55%);         /* Warning — verify 4.5:1 on bg */

  /* Focus ring — must contrast 3:1 with adjacent colors (WCAG 2.4.7) */
  --color-focus: hsl(210, 100%, 65%);
  --focus-ring: 0 0 0 3px var(--color-focus);
}

/* ✅ Color-scheme support */
@media (prefers-color-scheme: light) {
  :root {
    --color-bg: hsl(0, 0%, 99%);
    --color-text-primary: hsl(220, 20%, 8%);
    /* ... recalculate all contrasts */
  }
}
```

**Multi-modal communication** (never color alone):
```css
/* ❌ Color only for error */
.input-error { border-color: red; }

/* ✅ Color + icon + text + pattern */
.input-error {
  border-color: var(--color-error);
  border-width: 2px;
  background-image: url("error-icon.svg");
  background-position: right 12px center;
  background-repeat: no-repeat;
  padding-right: 40px;
}
```

### 6.3 Typography Design System

```css
/* ✅ Accessible, distinctive type scale */
:root {
  /* Scale: Major Third (1.25) or Perfect Fourth (1.333) */
  --text-xs:   0.75rem;    /* 12px — captions, labels */
  --text-sm:   0.875rem;   /* 14px — secondary text */
  --text-base: 1rem;       /* 16px — body */
  --text-lg:   1.125rem;   /* 18px — lead text */
  --text-xl:   1.25rem;    /* 20px */
  --text-2xl:  1.5rem;     /* 24px */
  --text-3xl:  1.875rem;   /* 30px */
  --text-4xl:  2.25rem;    /* 36px */
  --text-5xl:  3rem;       /* 48px */
  --text-6xl:  3.75rem;    /* 60px */

  /* Accessible line heights */
  --leading-tight:  1.25;
  --leading-snug:   1.375;
  --leading-normal: 1.5;
  --leading-relaxed:1.625;
  --leading-loose:  2;

  /* Weights */
  --font-light:    300;  /* Use sparingly, large sizes only */
  --font-normal:   400;
  --font-medium:   500;
  --font-semibold: 600;
  --font-bold:     700;
  --font-black:    900;
}
```

**Font selection for accessible uniqueness:**
- Avoid Inter, Roboto, Arial, system-ui for display — too generic
- Choose typefaces with strong optical size range: DM Sans, Fraunces, Bricolage Grotesque,
  Playfair Display, Syne, General Sans, Cabinet Grotesk, Instrument Serif
- Pair distinctive display fonts with clean, readable body fonts
- Verify chosen fonts render legibly at body sizes (14–18px)
- Always have a readable fallback stack

### 6.4 Focus Indicator as Design Element

Make focus indicators **intentional design features**, not afterthoughts:

```css
/* Option 1: Solid outline */
:focus-visible {
  outline: 3px solid var(--color-accent);
  outline-offset: 3px;
  border-radius: var(--radius-sm, 4px);
}

/* Option 2: Box shadow (inset for contained elements) */
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--color-bg), 0 0 0 5px var(--color-accent);
}

/* Option 3: High visibility for text links */
a:focus-visible {
  outline: none;
  background-color: var(--color-accent);
  color: var(--color-bg);
  text-decoration: none;
  border-radius: 2px;
  padding: 0 2px;
}

/* Verify contrast: focused vs unfocused → must be ≥3:1 change */
```

### 6.5 Spacing and Layout for Motor Accessibility

```css
/* ✅ Generous interactive targets */
.btn {
  /* Minimum visually 44×44 (WCAG 2.5.5 AAA) */
  min-height: 44px;
  padding-inline: 1.25rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

/* ✅ Inline links — guaranteed minimum height */
a {
  display: inline-block; /* Ensures tap area */
  padding: 0.25em 0;
}

/* ✅ Spacing between small targets (WCAG 2.5.8 AA) */
.icon-group { gap: 0.5rem; } /* 8px between 24px targets = sufficient */

/* ✅ Grid and flex for logical order */
/* Visual order must match DOM order for keyboard/screen reader users */
/* Avoid using CSS `order` property to reorder visual layout */
```

### 6.6 Accessible Animation Design

```css
/* ✅ Always implement reduced-motion alternative */
:root {
  --duration-fast: 150ms;
  --duration-base: 250ms;
  --duration-slow: 400ms;
  --easing-out: cubic-bezier(0.16, 1, 0.3, 1);
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
    --duration-base: 0ms;
    --duration-slow: 0ms;
  }
}

/* ✅ Purpose-driven micro-interactions */
.btn {
  transition:
    background-color var(--duration-fast) ease,
    transform var(--duration-fast) var(--easing-out),
    box-shadow var(--duration-fast) ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.btn:active {
  transform: translateY(0);
  box-shadow: none;
}
```

---

## Part 7 — Testing Checklist

### Quick Audit (5 minutes)
- [ ] Tab through entire page — can you reach and activate everything?
- [ ] Focus indicator visible at all times?
- [ ] Check color contrast with browser DevTools
- [ ] Run axe DevTools or Lighthouse accessibility audit
- [ ] Check page without CSS (semantic structure visible?)

### Standard Audit (WCAG 2.2 AA)
**Perceivable**
- [ ] All images have meaningful alt text (or `alt=""` for decorative)
- [ ] Color contrast ≥4.5:1 normal text, ≥3:1 large text and UI elements
- [ ] Color not the only way to convey information
- [ ] Content readable/functional at 200% zoom
- [ ] No horizontal scroll at 320px wide (reflow)
- [ ] Text spacing overrides don't break layout
- [ ] No auto-playing audio without controls

**Operable**
- [ ] All functionality keyboard-accessible
- [ ] No keyboard traps
- [ ] Focus indicator always visible
- [ ] Focus not obscured by sticky headers/footers
- [ ] Skip navigation link present
- [ ] All pages have descriptive `<title>`
- [ ] Focus order is logical
- [ ] Links have clear, descriptive text
- [ ] Touch targets ≥24×24px with adequate spacing
- [ ] No content flashes >3×/second

**Understandable**
- [ ] `<html lang="en">` set correctly
- [ ] Language changes marked with `lang` attribute
- [ ] No unexpected context changes on focus
- [ ] Navigation consistent across pages
- [ ] All form inputs have visible labels
- [ ] Errors identified, described, and suggestions offered
- [ ] Help mechanism in consistent location

**Robust**
- [ ] All form controls have name, role, value via HTML or ARIA
- [ ] Status messages announced without focus change
- [ ] Valid, well-structured HTML (no broken nesting)
- [ ] ARIA roles/states used correctly
- [ ] Dynamic content updates announced

### Screen Reader Testing
Test with: NVDA + Chrome (Windows), VoiceOver + Safari (Mac), TalkBack + Chrome (Android)
- [ ] Heading structure navigable and logical
- [ ] Landmarks navigable (nav, main, aside, footer)
- [ ] Form labels read correctly
- [ ] Error messages announced when fields are invalid
- [ ] Dynamic content (alerts, status) announced
- [ ] Modals: focus traps, Escape closes, focus returns

---

## Part 8 — Legal and Standards Context

| Standard | Jurisdiction | Based On |
|----------|-------------|----------|
| ADA (Americans with Disabilities Act) | USA | WCAG 2.1 AA |
| Section 508 | USA (Federal) | WCAG 2.0 AA |
| EN 301 549 | European Union | WCAG 2.1 AA |
| AODA | Ontario, Canada | WCAG 2.0 AA |
| Equality Act 2010 | UK | WCAG 2.1 AA |
| BS 8878 | UK | WCAG 2.1 |
| BITV 2.0 | Germany | WCAG 2.1 AA |

**Recommended target: WCAG 2.2 AA** — exceeds requirements of all major laws and is future-proof.

---

## Part 9 — Tools and Resources

### Testing Tools
| Tool | Type | Use For |
|------|------|---------|
| **axe DevTools** | Browser extension + CI | Most comprehensive automated checks |
| **WAVE** (WebAIM) | Browser extension | Visual error overlay |
| **Lighthouse** | Chrome DevTools | Quick baseline audit |
| **Colour Contrast Analyser** | Desktop app | Pixel-accurate contrast check |
| **WebAIM Contrast Checker** | Web tool | Quick contrast calculation |
| **NVDA** | Screen reader | Windows screen reader testing (free) |
| **VoiceOver** | Screen reader | Mac/iOS built-in |
| **TalkBack** | Screen reader | Android built-in |
| **Keyboard** | Manual | Always test keyboard-only navigation |

### Key References
- **WCAG 2.2 Specification**: https://www.w3.org/TR/WCAG22/
- **WAI-ARIA Authoring Practices Guide**: https://www.w3.org/WAI/ARIA/apg/
- **WebAIM Articles**: https://webaim.org/articles/
- **The A11Y Project**: https://www.a11yproject.com/
- **Deque University**: https://dequeuniversity.com/
- **MDN Accessibility**: https://developer.mozilla.org/en-US/docs/Web/Accessibility
- **Inclusive Components** (Heydon Pickering): https://inclusive-components.design/
- **A11y Coffee**: https://a11y.coffee/

---

## Summary: Non-Negotiable AA Rules

When building any frontend interface, these WCAG 2.2 AA rules are **always required**:

1. **Contrast**: 4.5:1 normal text, 3:1 large text and UI components
2. **Alt text**: Every informative image has descriptive alt; decorative has `alt=""`
3. **Keyboard**: 100% of functionality reachable and operable via keyboard alone
4. **Focus visible**: Visible focus indicator that is never removed
5. **Labels**: Every form input has an associated visible `<label>`
6. **Errors**: Errors identified in text, not color alone; aria-invalid used; suggestions provided
7. **Headings**: Logical hierarchy, no skipped levels
8. **Language**: `<html lang="...">` always set
9. **Semantic HTML**: Use `<button>`, `<a>`, `<nav>`, `<main>` etc., not `<div>` substitutes
10. **No color-only info**: Never use color as the sole means to convey any information
11. **Reflow**: Content usable at 320px width without horizontal scrolling
12. **Touch targets**: Interactive elements ≥24×24px or adequate spacing
13. **Focus not obscured**: Sticky headers/footers don't hide focused elements
14. **Status messages**: Dynamic status/error messages announced to screen readers
15. **Consistent help**: Help mechanisms in the same location across pages
