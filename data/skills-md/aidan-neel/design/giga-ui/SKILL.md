---
name: giga-ui
description: Use when building, redesigning, or polishing any user interface (a component, landing page, dashboard, app screen, mobile UI, onboarding or auth flow), especially from a short or vague prompt. Gives you a complete visual language, design tokens, component recipes, and a motion and micro-interaction system so the result looks and feels premium. The style is inspired by product designer @marcelkargul.
---

# GIGA UI: calm, precise, alive

This skill turns a one-line UI request into a polished, production-quality interface. The visual language is **inspired by the public design work of @marcelkargul** (Kargul Studio): quiet, near-monochrome product UI, very careful typography, soft layered shadows instead of heavy borders, one confident accent color, and motion that is fast, physical, and never decorative for its own sake.

It works with any coding model and any stack. Examples use React + Tailwind + Motion (`motion/react`), and each one has a plain-CSS equivalent.

> Provenance legend used below:
> **[seen]** directly observed in his posts/images or stated in his captions.
> **[inferred]** a reasonable extrapolation from what was seen (measured from screenshots, or implied).
> **[expert]** general motion/UX best practice from Motion docs, Emil Kowalski, Apple HIG. Not from his posts.

---

## 1. Design philosophy

1. **If it can be removed, remove it.** [seen, caption: "every screen. every component. every frame. if it doesn't need to be there, it shouldn't be. simple is always hard, but simple always wins."]
2. **Typography does the heavy lifting.** [seen: "just master typography and you can make anything look good."] Use one family (Inter by default on the web, Geist as an optional alternative; SF Pro Rounded for iOS-flavored mobile) and **at most 2 weights** [seen: "sf pro rounded, maximum 2 font weights, keep it simple"].
3. **White, black, and shadows.** [seen: "No animations, no gradients, no fancy effects. Just FFFFFF, 000000, and some shadows. This is design at its peak."] Most of the palette is neutral greys. Color is used for meaning, like state, category, or the one primary action.
4. **Depth comes from soft layered shadows and hairlines, not thick borders.** [seen: "this button only requires 3 shadows!" and the secondary-button recipe in §3]
5. **Motion is part of the product, not decoration.** [seen: "micro-interactions throughout", "subtle loading animation. not overdone, just perfect", "every website needs this level of animation", "idea → design → animation"]. Animate only to explain a change, confirm an action, or guide attention [expert].
6. **Craft the last 10% by hand.** [seen: his process is "design in figma, build with the help of claude, spend hours fixing small details manually and improving code quality"]. The QA checklist in §9 is that last 10%.
7. **Clean beats clever.** His captions keep returning to the words "clean", "calm", and "simple" (for example, "Every task in one calm list"). Even when there's a lot of data, the screen should feel calm.

---

## 2. The observed style (what his work actually looks like)

### 2.1 Typography
- **Families:** Inter (the default in this skill) and Geist (optional alternative). [seen: "After using 100s of different fonts, I realized nothing beats Inter and Geist."; joke post: junior and senior designers both use "Inter, Geist"]. SF Pro Rounded for mobile apps [seen, several posts]. He also recommends Google Sans Rounded as a cross-platform alternative to SF Pro Rounded [seen, reply]. A **monospace** (Geist Mono-like) shows up for big numbers, tickers, and code [seen: crypto app balances, Statsnap KPI cards, sidebar nav variant]. Brand and marketing work sometimes uses a **serif display** face (editorial transitional serif, light weight) [seen: fintech landing "Every payment protected…", VC landing page].
- **Tracking (his exact numbers, demoed with Geist; apply the same to Inter, which he also demoed at −6%)** [seen]:
  - 16px → 0%
  - 36px → −3%
  - 100px+ → −5% to −6%
  - "The never-go-negative rule is for body text. At 100px+ the default spacing looks loose."
  - SF Pro Rounded: +1% letter spacing [seen, type specimen].
- **Weights:** Regular (400) and Medium (500) carry nearly all product UI. Semibold (600) is for headings and numbers. Bold/Black only for large display headlines [inferred from screenshots].
- **Sizes in product UI** [inferred, measured from screenshots at 1×]: body and table text 13–14px, secondary/meta 12–13px, section labels 11–12px uppercase or small-caps grey (e.g. "WORKSPACE", "PINNED TOOLS"), page titles 18–24px Medium, KPI numbers 24–32px, hero headlines 48–72px with negative tracking. Buttons are 14px Medium [seen: "Geist/14/Medium"].
- **Color of text:** primary near-black (#171717–#1F1F1F), secondary mid-grey (#6B6B6B–#737373), tertiary/placeholder (#A3A3A3). Tags use **dark tinted text on a light tint** instead of white text on saturated fills [seen: "Do / Don't" post: "Dark text improves overall readability greatly."].

### 2.2 Color
Sampled from screenshots (approximate) [seen/inferred]:

| Role | Light | Dark |
|---|---|---|
| Canvas / page | `#FFFFFF` | `#0D0D0D`–`#121212` |
| Subtle surface (sidebar, panels, mobile bg) | `#F7F7F7` / `#F4F4F4` / `#FAFAFA` | `#1A1A1A`–`#1E1E1E` |
| Presentation backdrop behind mockups | `#E5E5E5`–`#EDEDED`, mid grey `#8A8A8A` | `#1F1F1F`–`#262626` |
| Hairline border | `#ECECEC` / `#EBEBEB` | `rgba(255,255,255,0.08)` |
| Primary text | `#171717` | `#FAFAFA` |
| Secondary text | `#737373` | `#A1A1A1` |

**Accents** (one per product, never several at once) [seen]:
- Violet `#7B3AEC` (Underlay signup, onboarding), also an indigo `#5B5BF0` variant
- Blue `#255CD1` / iOS blue `#2F7BF6` (calculator, calendar, Statsnap)
- Orange `#FF5A1F` / `#F97316` (Plunio, Nexora)
- Teal `#0F766E`-ish (AI pipeline, AIData)
- Lime `#B4F05A` on near-black (code editor "Start" button, Soma brand)
- Coral/red `#F2435A` (sleep app)
- Pure black `#0A0A0A` as the primary button color in neutral apps (sleep app, calculator "=", "Deploy v13", "New event") [seen]

**Semantic tints** [seen]: green `#16A34A` text on `#ECFDF3`; red `#DC2626` on `#FEF2F2`; amber/orange on `#FFF4E5`; blue on `#EEF4FF`. Avatar initials sit on pastel circles with darker same-hue text ("SW", "AJ", "MP").

**Gradients:** used rarely but well [seen: "the art of using gradients"]. Buttons get a subtle top-to-bottom gradient (`#FFFFFF → #F7F7F7` for secondary; a slightly lighter top for primary). Hero art uses blurred multi-color blobs with Plus-Darker blending plus a **noise/grain overlay** [seen: hero illustration thread].

### 2.3 Shape, spacing, depth
- **Radii** [seen and inferred]: small controls and buttons 8–10px [seen: "30px height, 10px radius"]; inputs 10–12px; cards 12–16px; modals and command palettes 20–24px; mobile sheets and phone cards 24–32px; pills and chips fully rounded. Mobile buttons are often full pills [seen].
- **Spacing:** a 4px base grid. Common gaps are 4/8/12/16/24/32/48 [inferred]. Lots of air around content; dense tables still get ~40–48px rows [inferred].
- **Control heights** [seen/inferred]: compact desktop buttons 30–32px, standard 36–40px, mobile primary CTA 48–56px.
- **Borders:** 1px hairlines in very light grey. Often the border is **made from a 0-blur 1px spread shadow** instead of `border` [seen: secondary button recipe].
- **Shadows** [seen]: secondary button = `0 1px 2px rgba(40,40,40,.08), 0 0 0 1px #ECECEC`. Floating surfaces (popovers, palettes, tooltips) use a large, very soft ambient shadow plus a hairline. Dark tooltips sit over light UIs [seen: Statsnap chart tooltip, "Task completed · Undo" toast].
- **Mobile:** artboard 430×932 [seen], round 40–44px icon buttons in the top bar, grouped "inset" list cards on a grey canvas, floating pill tab bars [seen].

### 2.4 Layout patterns [seen]
- **SaaS app shell:** left sidebar (220–260px) on a subtle grey, grouped nav with small uppercase grey labels, active item = white pill with soft shadow (light) or `#1E1E1E` fill (dark); main content on white with a thin top bar (breadcrumb `Home > Transaction`, search with `/` hint, icon buttons). Sometimes there's a slim icon rail (48–56px) instead.
- **Filter-chip row** above tables: `Range Last 30 days ▾`, `Scope All tools ▾`. The label is grey and the value is dark.
- **Tables:** no zebra stripes, hairline row dividers, small grey header text, tinted status pills, avatar + name + email stacks, right-aligned numbers, tabular figures.
- **KPI cards:** label, big number (often mono), delta pill (`▲ +14.7% vs last year`).
- **Auth/onboarding:** split card. Form on the left (logo in a soft circle, title, subtitle, Google button, "or" divider, input, primary), product preview on the right in a grey panel with carousel dots [seen: "just designed the perfect signup page"].
- **Command palette:** 24px radius, search row with `ESC` keycap, filter pills, grouped results, keyboard legend footer [seen].
- **Mobile onboarding:** segmented progress bar + "1/5", centered bold question, selectable option rows with circle checks, sticky pill CTA [seen].
- **Landing heroes:** floating pill navbar, small "Backed with X" badge, short punchy headline (sometimes all-caps grotesk, sometimes a serif), dark primary + white secondary button, big illustration underneath [seen].

### 2.5 Iconography and illustration [seen]
- Icons: thin-stroke outline icons (Lucide/Phosphor-like, ~1.5px stroke, 16–18px in UI), grey by default, darker when active.
- Small colored **app-icon tiles** (rounded squares with a gradient and a glyph) for feature cards and categories.
- Illustration styles: (a) **isometric line art** on a dashed grid, monochrome; (b) **vivid gradient ribbons/streams** on a grainy pastel background with an isometric grid and floating confetti; (c) friendly flat-shaded spot illustrations and 3D-ish emoji icons for consumer and mobile apps; (d) skeuomorphic touches (a stitched leather wallet holding a card).
- His animation pipeline: "Draw the illustrations in Figma → Animate in AE/Rive → Export to lottie if using AE → Implement onto the website". On one project he used "Figma… Rive for animation, Next.js + Sanity". Hero sections often take "design + illustration + animation" [seen].

### 2.6 Dark vs light [seen]
He uses both and ships matching sets ("light/dark mode", "figma tokens are so useful!"). Light is the default for productivity SaaS. Dark is used for crypto/trading, code editors, sidebars, and marketing banners. Dark surfaces step up in ~6–10 lightness increments (`#0D0D0D → #121212 → #1A1A1A → #222`), not pure black everywhere.

---

## 3. Design tokens (CSS variables)

Paste this into the global stylesheet. Tailwind users can map these in `@theme` (v4) or `theme.extend` (v3).

```css
:root {
  /* Type */
  --font-sans: "Inter", "Geist", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, "Geist Mono", "SF Mono", Menlo, monospace;
  --font-rounded: "SF Pro Rounded", ui-rounded, "Google Sans Rounded", var(--font-sans);

  --text-xs: 12px;   --text-sm: 13px;  --text-base: 14px; --text-md: 16px;
  --text-lg: 18px;   --text-xl: 24px;  --text-2xl: 32px;  --text-3xl: 48px;
  --text-4xl: 64px;  --text-5xl: 96px;
  --tracking-body: 0;       /* <= 16px */
  --tracking-tight: -0.01em;/* 18–24px */
  --tracking-title: -0.03em;/* ~36px  (his rule) */
  --tracking-display: -0.055em; /* 100px+ (his rule: -5% to -6%) */
  --weight-regular: 400; --weight-medium: 500; --weight-semibold: 600;

  /* Neutrals (light) */
  --bg: #ffffff;
  --bg-subtle: #f7f7f7;
  --bg-muted: #f0f0f0;
  --bg-backdrop: #e8e8e8;
  --border: #ececec;
  --border-strong: #e0e0e0;
  --fg: #171717;
  --fg-secondary: #737373;
  --fg-tertiary: #a3a3a3;
  --fg-inverse: #ffffff;

  /* Accent: pick ONE per product */
  --accent: #7b3aec;             /* violet; alternatives: #255cd1 blue, #ff5a1f orange, #0a0a0a black */
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-soft: color-mix(in oklab, var(--accent), white 90%);
  --accent-fg: #ffffff;
  --ring: color-mix(in oklab, var(--accent), transparent 65%);

  /* Semantic (dark text on soft tint) */
  --success: #16a34a; --success-soft: #ecfdf3;
  --danger:  #dc2626; --danger-soft:  #fef2f2;
  --warning: #d97706; --warning-soft: #fff7e6;
  --info:    #2563eb; --info-soft:    #eef4ff;

  /* Spacing (4px grid) */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-5: 20px; --space-6: 24px; --space-8: 32px; --space-10: 40px;
  --space-12: 48px; --space-16: 64px; --space-24: 96px;

  /* Radii */
  --radius-xs: 6px; --radius-sm: 8px; --radius-md: 10px; --radius-lg: 12px;
  --radius-xl: 16px; --radius-2xl: 20px; --radius-3xl: 24px; --radius-full: 9999px;

  /* Heights */
  --h-control-sm: 30px; --h-control: 36px; --h-control-lg: 44px; --h-cta-mobile: 52px;

  /* Shadows (layered, soft; hairline via spread) */
  --hairline: 0 0 0 1px var(--border);
  --shadow-xs: 0 1px 2px rgb(40 40 40 / 0.08);
  --shadow-btn: 0 1px 2px rgb(40 40 40 / 0.08), 0 0 0 1px #ececec;     /* his secondary button */
  --shadow-btn-primary: inset 0 1px 0 rgb(255 255 255 / 0.18), 0 1px 2px rgb(0 0 0 / 0.16), 0 0 0 1px color-mix(in oklab, var(--accent), black 12%);
  --shadow-card: 0 1px 2px rgb(0 0 0 / 0.04), 0 0 0 1px var(--border);
  --shadow-pop: 0 0 0 1px rgb(0 0 0 / 0.06), 0 8px 24px -4px rgb(0 0 0 / 0.10), 0 2px 6px rgb(0 0 0 / 0.04);
  --shadow-modal: 0 0 0 1px rgb(0 0 0 / 0.06), 0 24px 64px -12px rgb(0 0 0 / 0.18);
  --shadow-focus: 0 0 0 3px var(--ring);

  /* Motion (see §5) */
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);       /* strong ease-out (Emil Kowalski) */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);   /* for on-screen movement */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);    /* iOS-like sheet (Vaul) */
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --dur-instant: 100ms; --dur-fast: 150ms; --dur-base: 200ms;
  --dur-moderate: 250ms; --dur-slow: 350ms; --dur-page: 500ms;
}

[data-theme="dark"], .dark {
  --bg: #0d0d0d;
  --bg-subtle: #141414;
  --bg-muted: #1c1c1c;
  --bg-backdrop: #0a0a0a;
  --border: rgb(255 255 255 / 0.08);
  --border-strong: rgb(255 255 255 / 0.14);
  --fg: #fafafa;
  --fg-secondary: #a1a1a1;
  --fg-tertiary: #6b6b6b;
  --shadow-btn: inset 0 1px 0 rgb(255 255 255 / 0.06), 0 0 0 1px rgb(255 255 255 / 0.08);
  --shadow-card: 0 0 0 1px rgb(255 255 255 / 0.07);
  --shadow-pop: 0 0 0 1px rgb(255 255 255 / 0.08), 0 16px 40px -8px rgb(0 0 0 / 0.6);
}

html { -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
body { font-family: var(--font-sans); font-size: var(--text-base); color: var(--fg); background: var(--bg);
       font-feature-settings: "cv11", "ss01"; }
.tabular { font-variant-numeric: tabular-nums; }
```

Tracking helper: `h1{font-size:var(--text-4xl);letter-spacing:var(--tracking-display);line-height:1.02}`. Line-height rule of thumb: body 1.5, UI labels 1.3, headings 1.1, display 1.0–1.05 [expert].

---

## 4. Component recipes

All snippets assume `import { motion, AnimatePresence, MotionConfig } from "motion/react"` and a `cn()` class joiner.

### 4.1 Secondary button (his exact recipe, adapted) [seen]
Figma recipe from his post: frame 30px tall, 10px radius, text Geist 14 Medium, vertical gradient `#FFFFFF → #F7F7F7`, stroke removed, then 2 effects: drop shadow (0,1) blur 2 `#282828` at 8%, plus drop shadow (0,0) spread 1 blur 0 `#ECECEC` at 100%.

```tsx
export function Button({ variant = "secondary", className, ...props }) {
  return (
    <motion.button
      whileTap={{ scale: 0.97 }}
      transition={{ type: "spring", visualDuration: 0.15, bounce: 0 }}
      className={cn(
        "inline-flex h-[30px] items-center gap-1.5 rounded-[10px] px-3 text-[14px] font-medium select-none",
        "transition-[background,box-shadow,color] duration-150 ease-out outline-none",
        "focus-visible:shadow-[var(--shadow-focus),var(--shadow-btn)]",
        variant === "secondary" &&
          "bg-gradient-to-b from-white to-[#F7F7F7] text-[#171717] shadow-[var(--shadow-btn)] hover:to-[#F2F2F2]",
        variant === "primary" &&
          "bg-[var(--accent)] text-white shadow-[var(--shadow-btn-primary)] hover:bg-[var(--accent-hover)]",
        className
      )}
      {...props}
    />
  );
}
```

```css
.btn { height:30px; padding:0 12px; border-radius:10px; font:500 14px/1 var(--font-sans);
  display:inline-flex; align-items:center; gap:6px; border:0; cursor:pointer; user-select:none;
  transition: transform 150ms var(--ease-out), box-shadow 150ms var(--ease-out), background 150ms var(--ease-out); }
.btn:active { transform: scale(0.97); }
.btn:focus-visible { outline:none; box-shadow: var(--shadow-focus), var(--shadow-btn); }
.btn--secondary { background: linear-gradient(#fff, #f7f7f7); color: var(--fg); box-shadow: var(--shadow-btn); }
.btn--primary { background: var(--accent); color: var(--accent-fg); box-shadow: var(--shadow-btn-primary); }
@media (hover:hover) { .btn--primary:hover { background: var(--accent-hover); } }
```

### 4.2 Input with soft focus ring
```tsx
<input
  className="h-10 w-full rounded-[10px] bg-white px-3 text-[14px] text-[#171717] placeholder:text-[#A3A3A3]
             shadow-[var(--shadow-btn)] outline-none transition-shadow duration-150 ease-out
             focus:shadow-[0_0_0_1px_var(--accent),0_0_0_4px_var(--ring)]"
  placeholder="name@company.com"
/>
```
```css
.input { height:40px; width:100%; border:0; border-radius:10px; padding:0 12px; font-size:14px;
  background:#fff; box-shadow: var(--shadow-btn); transition: box-shadow 150ms var(--ease-out); }
.input:focus { outline:none; box-shadow: 0 0 0 1px var(--accent), 0 0 0 4px var(--ring); }
.input[aria-invalid="true"] { box-shadow: 0 0 0 1px var(--danger), 0 0 0 4px rgb(220 38 38 / .15); }
```
This works for a bare input. Once the input sits inside a visible box (search bar, composer, input with an icon or button), the **box** gets the ring and the input gets none. See §4.13.

### 4.3 Sidebar nav with sliding active pill (layout animation)
A minimal version is below. For any real sidebar, use the full recipe in **§4.12**.
```tsx
function Nav({ items, active, onSelect }) {
  return (
    <nav className="flex flex-col gap-0.5">
      {items.map((it) => (
        <button key={it.id} onClick={() => onSelect(it.id)}
          className="relative flex h-8 items-center gap-2 rounded-lg px-2.5 text-[14px] text-[#737373] hover:text-[#171717]">
          {active === it.id && (
            <motion.span layoutId="nav-pill"
              className="absolute inset-0 rounded-lg bg-white shadow-[var(--shadow-btn)]"
              transition={{ type: "spring", visualDuration: 0.25, bounce: 0.15 }} />
          )}
          <it.icon className="relative size-4" strokeWidth={1.5} />
          <span className={cn("relative", active === it.id && "text-[#171717]")}>{it.label}</span>
          {it.count != null && <span className="relative ml-auto text-[12px] tabular-nums text-[#A3A3A3]">{it.count}</span>}
        </button>
      ))}
    </nav>
  );
}
```
CSS-only equivalent: keep one absolutely positioned `.pill` element and move it with `transform: translateY(var(--y))` using `transition: transform 250ms var(--ease-out)`. Set `--y` from JS to the active item's `offsetTop`.

### 4.4 Segmented control / tabs (Daily · Weekly · Monthly)
Same `layoutId` technique as 4.3 inside a `bg-[#F4F4F4] p-1 rounded-[10px]` track. The thumb is `bg-white rounded-lg shadow-[var(--shadow-btn)]`. Labels are 13px Medium, inactive `#737373`.

### 4.5 Card / KPI tile
```tsx
<motion.div
  initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.35, ease: [0.23, 1, 0.32, 1] }}
  className="rounded-2xl bg-white p-4 shadow-[var(--shadow-card)]">
  <p className="text-[13px] text-[#737373]">Total balance</p>
  <p className="mt-2 font-mono text-[28px] font-medium tracking-[-0.02em] tabular-nums">$83,820.35</p>
  <span className="mt-2 inline-flex items-center gap-1 rounded-md bg-[#ECFDF3] px-1.5 py-0.5 text-[12px] font-medium text-[#16A34A]">▲ +30.5%</span>
  <span className="ml-1.5 text-[12px] text-[#A3A3A3]">since Jan 1</span>
</motion.div>
```

### 4.6 Status pill / tag (dark text on soft tint) [seen]
```css
.tag { display:inline-flex; align-items:center; height:22px; padding:0 8px; border-radius:6px;
  font:500 12px/1 var(--font-sans); }
.tag--success { color:#15803d; background:#ecfdf3; box-shadow: inset 0 0 0 1px #d1fadf; }
.tag--danger  { color:#b91c1c; background:#fef2f2; box-shadow: inset 0 0 0 1px #fde0e0; }
.tag--info    { color:#1d4ed8; background:#eef4ff; box-shadow: inset 0 0 0 1px #dbe6ff; }
```
Never put white text on a saturated tag fill. His "Don't" example shows why.

### 4.7 Popover / dropdown / command palette
```tsx
<AnimatePresence>
  {open && (
    <motion.div
      initial={{ opacity: 0, scale: 0.96, y: -4 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.98, transition: { duration: 0.12, ease: "easeIn" } }}
      transition={{ type: "spring", visualDuration: 0.2, bounce: 0 }}
      style={{ transformOrigin: "var(--radix-popover-content-transform-origin, top)" }}
      className="rounded-xl bg-white p-1 shadow-[var(--shadow-pop)]"
    />
  )}
</AnimatePresence>
```
Rules: scale from **0.95–0.97, never from 0** [expert, Emil]. The origin should be the trigger, except modals, which scale from center. Exits are faster than enters. Command palette: 24px radius, `ESC` keycap (`h-6 px-1.5 rounded-md bg-[#F7F7F7] shadow-[var(--hairline)] text-[12px]`), hovered row `bg-[#F5F5F5] rounded-lg`. **Do not animate a palette opened by keyboard shortcut**, or keep it under 120ms opacity only [expert, Emil: "never animate keyboard initiated actions"].

```css
.pop { transform-origin: var(--origin, top); animation: pop-in 200ms var(--ease-out); }
.pop[data-state="closed"] { animation: pop-out 120ms ease-in forwards; }
@keyframes pop-in { from { opacity:0; transform: scale(.96) translateY(-4px); } }
@keyframes pop-out { to { opacity:0; transform: scale(.98); } }
```

### 4.8 Modal / bottom sheet
- Desktop modal: overlay `rgb(0 0 0 / .4)` fades in 200ms. Panel goes from `opacity 0, scale .96, y 8` to rest, spring `visualDuration .3, bounce .1`. Radius 20–24px.
- Mobile sheet: `y: "100%" → 0` using `cubic-bezier(0.32,0.72,0,1)` at 400–500ms, or spring `{ stiffness: 400, damping: 40 }`. Draggable down to dismiss (see §5.7). Radius 24–32px top, with a grab handle 36×5px `#D4D4D4`.

### 4.9 Toast (with undo) [seen: dark "Task completed · Undo"]
Dark pill on light UI: `bg-[#171717] text-white rounded-[10px] h-9 px-3 text-[13px] shadow-[var(--shadow-pop)]`, with an `Undo` keycap button `bg-white/10`. Enter from `y: 16, opacity: 0, scale: .96` with spring `visualDuration .35, bounce .15`. Exit `opacity 0, y 8` in 150ms. Stacked toasts scale down by 0.05 per level and peek 8px (Sonner pattern) [expert].

### 4.10 Skeleton & loading [seen: "subtle loading animation. not overdone"]
```css
.skeleton { border-radius: 8px; background: linear-gradient(90deg, #f2f2f2 0%, #e9e9e9 50%, #f2f2f2 100%);
  background-size: 200% 100%; animation: shimmer 1.4s linear infinite; }
@keyframes shimmer { to { background-position: -200% 0; } }
@media (prefers-reduced-motion: reduce) { .skeleton { animation: none; } }
```
Skeletons copy the **final layout exactly** (same heights, radii, gaps). When the real content arrives, crossfade it in over 200ms. Don't pop it in. Only show a spinner after ~300ms of waiting so fast loads never flash [expert]. In-button loading: keep the button width fixed, swap the label for a 14px spinner with `AnimatePresence mode="popLayout"` (blur 2px→0, y 6→0).

### 4.11 Mobile primary CTA (pill)
`h-[52px] w-full rounded-full bg-[var(--accent)] text-white text-[16px] font-medium` with a subtle top gradient highlight and `active:scale-[0.98]`. Fix it to the bottom with 16px side insets and a fade-to-bg gradient behind it [seen: onboarding, calendar, sleep "Hold to quit"]. "Hold to quit" style: fill a progress overlay with `scaleX 0→1` over 1.2s linear while held, reverse on release with 200ms ease-out [inferred from the label].

---

### 4.12 Sidebar & nav rail: the full recipe

Models tend to get sidebars wrong. Read this whole recipe before you write a sidebar, then compare your result with 2 or 3 files in `./references/sidebars/`.

Tags: **[seen]** means it is visible in Marcel's images. **[inferred]** means it is estimated from screenshots that have no known pixel scale, so treat it as a ratio and not as an exact value. **[expert]** means it is a common product-design default, not taken from him.

**Two good shells. Pick one per product; neither is the default.**
- **Inset:** the app background is tinted (`#F7F7F7`–`#F4F4F5` light, or the app base in dark). The sidebar has **no background of its own** and shares that tint. The content sits in a separate panel: white (or `#0f0f0f`–`#111` in dark), about 8px from the viewport top, right and bottom, radius 12–16px, a hairline plus a soft shadow (`0 0 0 1px rgb(0 0 0/.06), 0 1px 2px rgb(0 0 0/.04)`), with its own scroll [seen: Minto, Uniops, Timelines]. Suits calm products where the content should float: CRMs, inboxes, docs, AI chat.
- **Flush:** the sidebar is a full-height surface of its own, edge to edge, separated from the content by one hairline; the content is not inset [seen: Snaplytics, the dark actions panel]. Suits dense tools that want every pixel: analytics, admin, IDE-like screens, embedded views. A flush sidebar is just as finished as an inset one when the rows, spacing and active pill are right.

Whichever you pick, everything below (rows, columns, pill, collapse) is the same.

**What his sidebars have in common [seen]** (see `sidebars/` files for 2106499785813360687, 2106500336081063986, 2110467790343737666_3, 2113384174924988778, 2113997498008117362)
- **The sidebar is quieter than the content.** It sits on the canvas tone (`#F7F7F7`–`#FAFAFA` light, or the app's base in dark). The main content area is a white panel with a large radius and a hairline or soft shadow, so the *content* floats and the sidebar doesn't. He confirmed this in a reply: "different color sidebar than the main block" is "a great design pattern" (xpages p020).
- **Top block:** a workspace or brand switcher. It has a 20–28px rounded-square logo, the name in Medium, sometimes a muted handle on a second line (`Uniops / @kargulstudio`), and a small `⌄`/`⇅` chevron or a collapse icon (`⊟`/sidebar icon) at the right edge.
- **Search or primary action under the switcher.** Either a search input with a `/` keycap on the right (Snaplytics, Timelines), or a full-width white secondary button ("+ New timeline") that uses the §4.1 button recipe.
- **Section labels** are small and muted ("Navigation", "Reports & Management", "Other Tools", "Projects"). Some designs use sentence case. Others use small uppercase with tracking ("WORKSPACE", "UTILITY", "PINNED TOOLS", and "MESSAGES / DATA / DELAYS" in the dark Actions panel). Pick one style per product.
- **Items:** a 16px outline icon plus a 14px label in grey (`#525252`–`#737373`). There is no border, no background at rest, and the icons are monochrome. Color appears only for project dots or swatches (small rounded squares) and for brand logos of pinned tools.
- **Active item:** a soft grey fill pill (`#EDEDED`-ish on a `#F7F7F7` sidebar) or a white raised pill with a soft shadow, plus a darker label. He also shows high-contrast variants: a black pill with white text and a count badge (2106852842342375894), and a white rounded pill in a grey sidebar (Minto). There is **never** a left accent bar with a colored background.
- **Trailing meta** is right-aligned: counts in a small rounded badge or tabular grey numbers, a `›` chevron on the active item that opens a sub-view (Uniops "Team ›"), and `⠿` drag handles on pinned items.
- **Nesting:** child items are indented by roughly one icon width plus gap so that child icons line up under the parent's label. Children keep icons, and there are no tree lines (Timelines "Reports → All Reports, Performance Trends…").
- **Groups are separated by whitespace or a hairline divider.** In Minto the divider is a dashed hairline. Group gaps are clearly bigger than gaps between items.
- **Footer** is pinned to the bottom. It holds secondary links (Guide editor / Open docs / Back to home) or settings plus a round avatar.
- **Icon rail variant** (inbox app 2107869459142914419): a narrow rail with the logo tile at the top, a round "+" button, about 8 icon-only buttons in 2 groups split by a short hairline, an active icon in a soft tinted square, and settings plus an avatar at the bottom. A second "list" column (Inbox with filter pills) sits next to the rail.
- **Dark variant** (2107505914345603127): a `#1A1A1C` panel with 16–20px radius, uppercase muted section labels, and colored 16px icons. A dragged item lifts as a raised card with a grip `⠿`, and the footer row ends in `›`.

**Measurements**
| Token | Value | Tag |
|---|---|---|
| Expanded width | 240–264px (Width relative to the 1440 canvas ≈ 16–18%, consistent with this) | [inferred] ratio / [expert] px |
| Collapsed rail width | 56–64px (Icon centred, 32–36px hit square) | [expert]; rail shape [seen] |
| Item height | 32px desktop (28 dense, 36 roomy) | [expert]; "compact, single-line" [seen] |
| Item radius | 8px (pill-like, matches control tier) | [inferred] |
| Item padding-x | 8–10px; icon→label gap 8px | [inferred] |
| Icon | 16px, stroke 1.5, same grey as label | [seen] style / [expert] size |
| Item gap | 2px between items; 16–24px between groups | [inferred] |
| Section label | 11–12px, Medium, `#A3A3A3`, 8px below previous group gap, 4px above first item | [inferred] |
| Sidebar padding | 12px horizontal, 12–16px top | [inferred] |
| App background | Tinted `#F7F7F7`/`#F4F4F5`; the sidebar has no fill of its own and shares this tint | [seen] tone / [expert] hex |
| Inset main panel | margin 8px top/right/bottom (8px gap from sidebar optional), radius 12–16, white, 1px `rgb(0 0 0/.06)` ring + `0 1px 2px rgb(0 0 0/.04)` shadow, `overflow:auto` inside | [seen] shape / [inferred] px |
| Mobile panel | Inset removed below 768px (margin 0, radius 0); sidebar becomes a drawer | [expert] |

**Behavior & motion [expert unless marked]**
- **Hover:** the background goes to `rgb(0 0 0 / .04)` and the label goes to `#171717` within 120ms. There is no movement and no scale on nav items.
- **Active change:** one shared pill slides between items using the §4.3 `layoutId` spring (`visualDuration .25, bounce .15`). Do not fade one pill out while another fades in. Without Motion, measure the current item (`[aria-current="page"]`) against the scroll container and move one absolutely positioned pill with `transform`; skip the transition on first paint so it doesn't fly in from the top. Items need `position: relative` to paint above it.
- **Rows share two columns.** Every row (switcher, nav items, settings, account) puts its icon, logo tile or avatar in one **icon column** and its text in one **text column**. With 10px sidebar padding and a 60px rail: 16px icons sit 12px into the row (centre 30px from the edge), 24px tiles and avatars 8px into the row (also centre 30px), and all text starts at 48px. Measure it (`getBoundingClientRect().left` on each icon and label) rather than eyeballing. Because the columns never move, collapsing to the rail is just hiding text [expert].
- **Triggers are rows.** A workspace or account trigger is a full-width row button the same height and inset as the rows around it, with `text-align: start`. A narrower, shorter button whose label sits a few px off the nav labels below is the most common sidebar misalignment [expert].
- **Collapse:** animate `width` (240→60) with 220ms `var(--ease-out)`. This is the one place where a width animation is acceptable. If you animate a CSS grid column, use `grid-template-columns`. Labels fade or clip with `opacity` over 120ms, and they must *not* wrap while shrinking (`white-space: nowrap; overflow: hidden`). Icons must not move horizontally, so keep a fixed icon column. In collapsed mode, show a tooltip on hover (right side, same delay as every other tooltip, §6) and show none on touch or when expanded. Save the collapsed state in localStorage. The toggle sits at the right of the switcher row while expanded and moves to the start of the topbar while collapsed; `⌘B` / `Ctrl+B` toggles from anywhere except rich-text fields, where it means bold.
- **Resize [expert]:** a resizable sidebar has an 8px invisible handle on its right edge (`cursor: col-resize`) that shows a 2px line only after ~150ms of hover, so passing the edge doesn't flash it. Drag with pointer capture and clamp between a min and max (e.g. 200–320px). Dragging well past the minimum (~56px) snaps it to the rail or closed, dragging back out reopens it. Double-click resets the width. Turn the width transition off while dragging so it tracks the pointer 1:1. Make the handle a focusable `role="separator"` with `aria-valuenow`, ←/→ to resize, and Enter to toggle.
- **Nesting:** expanding a group animates the height of the children (Motion `height: "auto"`) and rotates the chevron 90° in 150ms. Children stagger by 20ms at most.
- **Workspace switcher:** opens a popover (§4.7) anchored to the switcher and scaling from 0.96 at its top-left origin. It lists workspaces with logo tiles and a check on the current one, followed by "Create workspace" and "Log out".
- **Keyboard:** the whole sidebar is a `<nav aria-label>`. Items are `<a>` with `aria-current="page"`, and a group toggle is a `<button aria-expanded>`. Focus-visible gets a 2px ring inside the pill.
- **Mobile (<768px):** hide the sidebar. Open it as a left drawer (85% width, max 320) over a dimmed `rgb(0 0 0 / .3)` scrim, slide it in with `translateX` 280ms `cubic-bezier(.32,.72,0,1)`, and close it by tapping the scrim, pressing Esc, or swiping. Items grow to 44px height. In consumer mobile apps use his **floating pill tab bar** with 4–5 items instead [seen].

**Common mistakes (seen in AI output; fix all of them)**
1. A shell that is neither inset nor flush: an inset panel with no radius or margin, an inset sidebar that also has its own fill and border, a heavy shadow on the panel, or the whole page scrolling instead of the panel. Flush done badly is the same white on both sides of a 1px border with no tonal difference; give the sidebar its own surface (`#FAFAFA`, or one step up in dark).
2. A colored active state (`bg-indigo-600 text-white`) or a 3px left accent bar.
3. Mixed icon sizes and styles, or emoji used as icons. Icons that are not vertically centered with the text.
4. Labels that wrap to two lines. Missing truncation (`text-overflow: ellipsis`).
5. The same spacing between every item, so groups don't read as groups. Or the opposite: huge 48px items.
6. Section labels in heavy bold, or at the same size and color as the items.
7. The footer floats mid-height because the sidebar isn't `height: 100dvh; display:flex; flex-direction:column` with a `margin-top:auto` footer.
8. Collapse animation where labels squish or wrap, icons jump sideways, or the content reflows in steps.
9. No hover, focus, or active differentiation. A missing `aria-current`.
10. Fifteen top-level items with no groups. Instead, group them into 3–4 sections of 3–6 items each and put rarely used links in the footer.

**Code (React + Motion + Tailwind; tokens from §3)**
```tsx
const groups = [
  { label: "Workspace", items: [
    { id:"dash", label:"Dashboard", icon: LayoutGrid },
    { id:"inbox", label:"Inbox", icon: Inbox, count: 3 },
    { id:"team", label:"Team", icon: Users, children: [
      { id:"members", label:"Members", icon: User }, { id:"roles", label:"Roles", icon: Shield } ] } ] },
  { label: "Projects", items: [
    { id:"q4", label:"Q4 Growth Plan", swatch:"#7B3AEC" }, { id:"brand", label:"Brand Awareness", swatch:"#F5A524" } ] },
];

export function Sidebar({ active, onSelect }) {
  const [collapsed, setCollapsed] = useLocalStorage("sb-collapsed", false);
  const [open, setOpen] = useState<Record<string, boolean>>({ team: true });
  return (
    <motion.aside animate={{ width: collapsed ? 60 : 248 }} transition={{ duration: .22, ease: [.23,1,.32,1] }}
      className="sticky top-0 hidden h-dvh shrink-0 flex-col overflow-hidden bg-transparent px-3 pt-3 md:flex">{/* no own fill: shares the app tint */}
      {/* workspace switcher */}
      <div className="flex h-10 items-center gap-2 px-1">
        <button className="flex min-w-0 flex-1 items-center gap-2 rounded-lg px-1.5 py-1 hover:bg-black/[.04]">
          <span className="grid size-6 shrink-0 place-items-center rounded-md bg-[#171717] text-[11px] font-semibold text-white">A</span>
          {!collapsed && <span className="truncate text-[14px] font-medium tracking-[-0.01em] text-[#171717]">Acme Inc</span>}
          {!collapsed && <ChevronsUpDown className="ml-auto size-3.5 text-[#A3A3A3]" strokeWidth={1.5} />}
        </button>
        <button aria-label="Toggle sidebar" onClick={() => setCollapsed(!collapsed)}
          className="grid size-7 shrink-0 place-items-center rounded-md text-[#A3A3A3] hover:bg-black/[.04] hover:text-[#171717]">
          <PanelLeft className="size-4" strokeWidth={1.5} />
        </button>
      </div>
      <nav aria-label="Main" className="mt-3 flex flex-1 flex-col gap-5 overflow-y-auto">
        {groups.map((g) => (
          <div key={g.label}>
            {!collapsed && <div className="mb-1 px-2.5 text-[12px] font-medium text-[#A3A3A3]">{g.label}</div>}
            <ul className="flex flex-col gap-0.5">
              {g.items.map((it) => (
                <li key={it.id}>
                  <NavItem it={it} active={active} collapsed={collapsed}
                    onClick={() => it.children ? setOpen({ ...open, [it.id]: !open[it.id] }) : onSelect(it.id)}
                    expanded={it.children ? !!open[it.id] : undefined} />
                  <AnimatePresence initial={false}>
                    {it.children && open[it.id] && !collapsed && (
                      <motion.ul initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }} transition={{ duration: .2, ease: [.23,1,.32,1] }}
                        className="ml-[26px] flex flex-col gap-0.5 overflow-hidden pt-0.5">
                        {it.children.map((c) => <li key={c.id}><NavItem it={c} active={active} onClick={() => onSelect(c.id)} /></li>)}
                      </motion.ul>)}
                  </AnimatePresence>
                </li>))}
            </ul>
          </div>))}
      </nav>
      {/* footer / user block */}
      <div className="mt-auto flex items-center gap-2 border-t border-black/[.06] px-1 py-3">
        <img src="/avatars/maya.jpg" alt="" className="size-7 shrink-0 rounded-full" />
        {!collapsed && <div className="min-w-0 leading-tight"><div className="truncate text-[13px] font-medium text-[#171717]">Maya Patel</div>
          <div className="truncate text-[12px] text-[#A3A3A3]">maya@acme.co</div></div>}
      </div>
    </motion.aside>
  );
}

function NavItem({ it, active, collapsed = false, onClick, expanded }) {
  const isActive = active === it.id;
  return (
    <button onClick={onClick} aria-current={isActive ? "page" : undefined} aria-expanded={expanded}
      /* collapsed: wrap this button in your Tooltip primitive (side="right"), not `title` */
      className="group relative flex h-8 w-full items-center gap-2 whitespace-nowrap rounded-lg px-2.5 text-[14px] text-[#737373] transition-colors duration-[120ms] hover:bg-black/[.04] hover:text-[#171717] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring)]">
      {isActive && <motion.span layoutId="sb-pill" className="absolute inset-0 rounded-lg bg-white shadow-[var(--shadow-btn)]"
        transition={{ type: "spring", visualDuration: .25, bounce: .15 }} />}
      {it.swatch ? <span className="relative size-2.5 shrink-0 rounded-[3px]" style={{ background: it.swatch }} />
                 : <it.icon className="relative size-4 shrink-0" strokeWidth={1.5} />}
      <span className={cn("relative truncate transition-opacity duration-[120ms]", collapsed && "opacity-0", isActive && "text-[#171717]")}>{it.label}</span>
      {!collapsed && it.count != null && <span className="relative ml-auto rounded-md bg-black/[.05] px-1.5 text-[11px] tabular-nums text-[#737373]">{it.count}</span>}
      {!collapsed && expanded != null && <ChevronRight className={cn("relative ml-auto size-3.5 text-[#A3A3A3] transition-transform duration-150", expanded && "rotate-90")} strokeWidth={1.5} />}
    </button>
  );
}
```
Inset shell layout:
```tsx
<div className="flex h-dvh overflow-hidden bg-[#F7F7F7]">          {/* tinted app bg, shared by sidebar */}
  <Sidebar />
  <main className="my-2 mr-2 flex-1 overflow-auto rounded-[14px] bg-white
                   shadow-[0_0_0_1px_rgb(0_0_0/.06),0_1px_2px_rgb(0_0_0/.04)]
                   max-md:m-0 max-md:rounded-none">…</main>       {/* inset, slightly elevated panel */}
</div>
```
Flush shell: drop the margins and radius on `<main>` and keep it white, and give the sidebar its own surface: `bg-[#FAFAFA] border-r border-black/[.06]` (one step up from the base in dark). On mobile, render the same `<nav>` inside a §4.8 sheet from the left, and put a hamburger in a sticky 56px top bar.

---

### 4.13 Focus rings: one ring, on the box you can see [expert]
Agents break focus in two opposite ways: they delete it (`outline: none` with nothing in its place, which X users now treat as an error [X]) or they draw it twice. Every focusable control shows exactly **one** ring, and it traces the shape the user sees as the control.

- **Composite fields get one ring, on the outer box.** A search bar, chat composer, input with an icon, or input with a button inside is one control to the user. Draw the ring on the wrapper with `:focus-within` (or `:has(textarea:focus)` when the box also holds buttons that shouldn't light it up) and give the inner `input`/`textarea` `outline: none`. The classic failure is the textarea's ring sitting a few px inside the composer's ring: two concentric, misaligned rounded rectangles.
- **Text fields are not buttons.** A global rule like `.app :focus-visible { outline: 2px solid }` also hits inputs, which match `:focus-visible` on mouse click as well. Scope it: `:focus-visible:not(input, textarea, [contenteditable])`, and let fields style their own wrapper.
- **Match the shape.** `outline` follows `border-radius` in all current browsers; use `outline-offset: 2px` for buttons and `-2px` (inset) for rows inside a scroll container, where an outer ring gets clipped by `overflow: hidden/auto`.
- **Mind the cascade.** Unlayered CSS beats Tailwind's layered utilities and resets, and scoped component CSS doesn't reach child components. Check that the ring you wrote is the one that renders (inspect the computed `outline` and `box-shadow`), especially on third-party primitives.
- **Menus and lists use their highlight, not a ring.** Menu items, options and command rows show focus through the same background as hover (`[data-highlighted]`). A ring there doubles up.
- **Error state replaces the ring color, not the ring.** `aria-invalid` turns the same ring red; it doesn't add a second one.

```css
.composer { border-radius: 16px; box-shadow: 0 0 0 1px var(--line); transition: box-shadow 150ms var(--ease-out); }
.composer:has(textarea:focus) { box-shadow: 0 0 0 1px var(--accent), 0 0 0 4px var(--ring); }
.composer textarea { outline: none; }
.app :focus-visible:not(input, textarea) { outline: 2px solid var(--accent); outline-offset: 2px; }
```
**Check it:** Tab through the screen and screenshot every input, button and row. Each shows one ring, aligned to its own edge, not clipped.

### 4.14 Field errors that move, not jump [expert]
- Validate on blur or submit, never on every keystroke. Once a field is in error, clear the error **as they type** the moment it becomes valid ("reward early, punish late").
- The message animates its height open: wrap it in a grid that goes `grid-template-rows: 0fr → 1fr` with opacity `0 → 1` and `translateY(-4px) → 0` over ~200ms. Nothing below the field jumps.
- Keep the last message rendered while it animates closed, so the text doesn't vanish before the box collapses.
- The ring turns red with the same transition as focus (§4.13). One short line in danger color with a 14px alert icon, directly under the field [X: "form errors next to the field"].
- On a failed sign-in, shake the form once (translateX ±6px, ~320ms) and select the password. Skip the shake under reduced motion. Don't shake for ordinary validation.
- Focus the first invalid field on submit. Announce messages with `aria-live="polite"` and link them with `aria-describedby`.

```css
.field-error { display: grid; grid-template-rows: 0fr; opacity: 0; transform: translateY(-4px);
  transition: grid-template-rows 200ms var(--ease-out), opacity 160ms var(--ease-out), transform 200ms var(--ease-out); }
.field-error[data-visible] { grid-template-rows: 1fr; opacity: 1; transform: none; }
.field-error > div { overflow: hidden; }
```

---

## 5. Motion system [expert unless marked]

His captions show motion matters a lot ("idea → design → animation", "bento animations… 5hrs", "every website needs this level of animation", "micro-interactions throughout"), but they don't publish curve values. Everything numeric below comes from Motion docs, Emil Kowalski, and Apple HIG, tuned to fit his calm, precise style.

### 5.1 Principles
1. **Purpose first:** animate to show where something came from, confirm an action, or connect states. Frequency matters: things seen 100×/day get little or no motion.
2. **Fast:** most UI motion takes 150–300ms. Emil: "Your animations should also usually be shorter than 300ms."
3. **Ease-out for entering and reacting.** Ease-in-out for things moving on screen. Never ease-in on enter, because it feels laggy.
4. **Springs for anything gesture-driven or interruptible.** They carry velocity and retarget smoothly.
5. **Interruptible:** prefer CSS transitions (which retarget) or Motion over CSS keyframes for state changes.
6. **Only `transform` and `opacity`** (plus `filter: blur` sparingly). They stay on the compositor.
7. **Respect reduced motion** (see 5.9).

### 5.2 Easing tokens
| Token | Value | Use |
|---|---|---|
| `--ease-out` | `cubic-bezier(0.23, 1, 0.32, 1)` | default for enter, hover, press, popovers |
| `--ease-in-out` | `cubic-bezier(0.77, 0, 0.175, 1)` | elements moving or morphing on screen |
| `--ease-drawer` | `cubic-bezier(0.32, 0.72, 0, 1)` | sheets, drawers (iOS-like) |
| `--ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` | general purpose, Material-style |
| `ease` (CSS) | `cubic-bezier(0.25, 0.1, 0.25, 1)` | slower, elegant toasts (Sonner uses `ease`) |
| exit | `ease-in` or `cubic-bezier(0.4, 0, 1, 1)` | short exits only |

Motion equivalents: pass arrays, e.g. `ease: [0.23, 1, 0.32, 1]`. Named Motion easings: `"easeOut"`, `"easeInOut"`, `"circOut"`, `"backOut"`, `"anticipate"`.

### 5.3 Duration scale
| Token | ms | Examples |
|---|---|---|
| instant | 100 | color/background hover, checkbox tick |
| fast | 150 | button press, tooltip, focus ring, exits |
| base | 200 | popover/dropdown enter, tab switch, toggle |
| moderate | 250–300 | modal enter, accordion, layout shifts |
| slow | 350–500 | sheets/drawers, page transitions, hero reveals |
| showcase | 600–1200 | marketing hero choreography, illustration loops (Rive/Lottie) |

Motion's tween default is `duration: 0.3` (0.8 with multiple keyframes) [Motion docs]. Exit ≈ 60–75% of enter. Larger distance gets slightly longer, but cap it.

### 5.4 Spring presets (Motion `transition`)
Motion supports **duration-based springs** (`visualDuration` + `bounce`, easy to reason about and coordinate with tweens) and **physics springs** (`stiffness`/`damping`/`mass`, which use gesture velocity). Motion's default `bounce` is `0.25`, and `0` means critically damped, no overshoot [Motion docs]. If stiffness, damping, or mass are set, they override bounce/duration.

```ts
export const spring = {
  snappy:  { type: "spring", visualDuration: 0.2,  bounce: 0 },     // press, toggles, popovers
  smooth:  { type: "spring", visualDuration: 0.3,  bounce: 0.1 },   // modals, layout, tabs
  gentle:  { type: "spring", visualDuration: 0.45, bounce: 0.15 },  // toasts, cards entering
  bouncy:  { type: "spring", visualDuration: 0.4,  bounce: 0.3 },   // playful success, likes (sparingly)
  sheet:   { type: "spring", stiffness: 400, damping: 40, mass: 1 },// drag-release sheets
  layout:  { type: "spring", stiffness: 500, damping: 40 },         // layoutId pills/indicators
} as const;
```
Keep bounce ≤ 0.15 for productivity UI. Save visible overshoot for celebratory moments. Apple's guidance matches this: SwiftUI's `.smooth` spring has no bounce, `.snappy` has a small bounce, and `.bouncy` has more, all with a default duration of around 0.5s. Use bounce to signal playfulness, not as a default.

**CSS springs without JS:** Motion can generate a duration-based spring as a CSS `linear()` easing (`import { spring } from "motion"`, then `transition: transform ${spring(0.3, 0.1)}`), or use a pre-baked `linear(...)` string.

### 5.5 Enter / exit patterns
| Element | Enter | Exit |
|---|---|---|
| Page section | `opacity 0→1, y 12→0, (blur 4px→0)` 400ms ease-out | n/a |
| List item | `opacity 0, y 6` → rest, spring.smooth | `opacity 0, scale .98`, 150ms |
| Popover / menu | `opacity 0, scale .96, y -4` → rest, 200ms from trigger origin | `opacity 0, scale .98` 120ms |
| Modal | overlay fade 200ms. Panel `scale .96, y 8` → rest, spring.smooth | 150ms ease-in |
| Toast | `y 16, scale .96` → rest, spring.gentle | `opacity 0, y 8` 150ms |
| Tooltip | delay 400–600ms first time, then instant for neighbors. `opacity, scale .97` 120ms | 80ms |
| Sheet | `y 100%→0` 450ms `--ease-drawer` | 300ms same curve |
| Number change | per-digit roll: `y ±100%` with mask, 250ms | n/a |

Text swaps (labels, button states): `AnimatePresence mode="popLayout"` with `initial {opacity:0, y:6, filter:"blur(2px)"}` → `{opacity:1, y:0, filter:"blur(0)"}` → exit `{opacity:0, y:-6, filter:"blur(2px)"}`, about 200ms.

### 5.6 Layout animations
- `layout` prop on elements whose size or position changes (accordion containers, reflowing grids, expanding cards). `layoutId` for shared elements (active pills, tab underlines, card → detail morphs).
- Wrap related siblings in `<LayoutGroup>`. Use `layout="position"` for text to avoid squash. Put `layout` on child text too so it scale-corrects.
- Height auto: animate `height: 0 → "auto"` with Motion, or use CSS `interpolate-size: allow-keywords` / `grid-template-rows: 0fr → 1fr` trick.
- If the main thread will be busy (route change), consider a CSS transition instead of JS layout animation. Emil notes Vercel's tab indicator dropped frames with shared layout animation during navigation.

### 5.7 Gestures
- `whileHover` (guarded: only on `(hover: hover)` devices), `whileTap={{ scale: 0.97 }}`, `whileFocus`.
- Drag: `drag="y"`, `dragConstraints`, `dragElastic={0.2}`. On release, dismiss if `offset.y > 120 || velocity.y > 500`, otherwise spring back with spring.sheet.
- Swipe actions on list rows: reveal under the row, snap points via `dragTransition.modifyTarget`.
- Momentum: Motion inertia defaults `power: 0.8, timeConstant: 700` [Motion docs]. Lower timeConstant (~200–300) feels tighter.
- Press feedback must start on pointer-down, not click.

### 5.8 Scroll effects
- Reveal on view: `whileInView={{ opacity: 1, y: 0 }}` from `{opacity: 0, y: 16}`, `viewport={{ once: true, amount: 0.3 }}`, 500ms ease-out, stagger children 0.06s. Use it once, not every time the element scrolls past.
- Parallax: subtle only (`useScroll` + `useTransform`, max ±40px). Never parallax body text.
- Sticky header: background goes from transparent to `bg/80 + backdrop-blur(12px)` and a hairline shadow after 8px of scroll.
- Native CSS: `animation-timeline: view()` / `scroll()` for progress bars and reveals where supported, with a static fallback.
- Hero illustration loops (Rive/Lottie) should pause offscreen (IntersectionObserver) and when `prefers-reduced-motion`.

### 5.9 Stagger
`delayChildren: stagger(0.04–0.06)` for lists of 3–10 items. Cap total stagger at ~300ms (only stagger the first ~8, then show the rest together). Grids: `stagger(0.05, { grid: [cols, rows], from: "center" })` [Motion docs]. Don't stagger on data refresh, only on first reveal.

### 5.10 Reduced motion & accessibility
```tsx
<MotionConfig reducedMotion="user">{children}</MotionConfig>
```
With `reducedMotion="user"`, Motion turns off transform and layout animations while keeping opacity and color. For custom logic use `useReducedMotion()` and swap `x: "-100%"` for `x: 0` (fade only), as Emil shows.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important;
    transition-duration: .01ms !important; scroll-behavior: auto !important; }
  .fade-ok { transition: opacity 150ms linear !important; } /* keep gentle fades */
}
```
Apple HIG: let people turn motion off. Avoid large-scale zoom, spin, and parallax for them, and never use motion as the only way to convey information.

### 5.11 Performance
- Animate `transform` and `opacity` only. Avoid width/height/top/left/margin/box-shadow in loops (fade a pseudo-element's opacity to animate a shadow).
- Add `will-change: transform` **only** while animating or on elements that animate constantly. Remove it afterwards, because too many layers waste memory.
- Prefer CSS/WAAPI for simple, always-on animations, since they stay hardware-accelerated when the main thread is busy [Emil]. Motion uses WAAPI for opacity/transform where it can.
- `backdrop-filter` and large `filter: blur` are expensive. Use them on small areas and few at once.
- Test at 4× CPU throttle. Aim for 60fps (120 on ProMotion), no layout shift (CLS 0) from animations.

---

## 6. Micro-interaction checklist

Every interactive element must have these states. Go through them one by one.

- [ ] **Hover** (pointer devices only): color/bg shift 100–150ms. Cursor pointer on clickable non-buttons. No layout shift.
- [ ] **Press**: `scale(0.97)` (buttons) or `0.98` (large cards/CTAs) at pointer-down, 150ms ease-out, spring back.
- [ ] **Focus-visible**: 3px soft accent ring (`--shadow-focus`) plus the hairline. Never remove focus without a replacement. One ring per control, on the outer box of composite fields (§4.13).
- [ ] **Disabled**: 50% opacity, `cursor: not-allowed`, no hover/press.
- [ ] **Loading**: fixed width, inline spinner or label crossfade. Disable double-submit.
- [ ] **Success/error feedback**: inline (checkmark draw-in via `pathLength 0→1` in 300ms, or red ring plus helper text). A toast for async results, with Undo for destructive actions [seen: "Task completed · Undo", "Couldn't save Company… Retry"].
- [ ] **Empty states**: friendly line plus primary action, optionally a small illustration.
- [ ] **Toggles/checkboxes**: thumb slides with spring.snappy. Check icon scales .8→1 plus fade.
- [ ] **Tabs/segmented**: sliding indicator via `layoutId`.
- [ ] **Inputs**: focus ring transition, character counter ("198/200"), inline validation after blur, not on every keystroke. OTP boxes auto-advance and paste-fill [seen: 6-digit verify screen].
- [ ] **Numbers**: tabular figures. Animated count/roll on change, not on every render.
- [ ] **Tooltips/keycaps**: show shortcuts (`/` in search, `ESC`, `C`) [seen]. Every icon-only button has one. Open after ~500ms of hover; once one is open, neighbours open instantly for ~400ms (skip delay), so scanning a toolbar doesn't make you wait each time. Only the first one animates in (~120ms fade and 2px rise); instant ones just appear. No tooltip when focus returns to a trigger after its menu closes, none on touch, and they close on scroll and pointer-down [expert].
- [ ] **Every control does something**: each button, menu item, chip and link either works or isn't there. Filters filter, search searches, "Share" copies a real link, "Export" downloads a real file, nav items change the view. A toast that claims an action happened when nothing changed is a dead button [X: "looks finished, doesn't work"]. Use a real menu primitive (Radix, bits-ui, Base UI, Ariakit) for menus, popovers and tooltips, not hand-rolled `div`s.
- [ ] **Lists**: new rows fade/slide in, removed rows collapse height plus fade, reorder animates with `layout`.
- [ ] **Hover cards in tables**: row hover `bg-[#FAFAFA]`, row actions (`…`) appear on hover with an opacity fade.
- [ ] **Carousel dots**: active dot stretches into a pill (`width` via `layout`) [seen on signup preview].
- [ ] **Copy buttons**: icon cross-fades copy → check (scale .5→1, blur 2px→0, ~200ms) for ~1.6s. If it has a tooltip, the tooltip stays open and its text changes to "Copied" instead of closing on click. Await the clipboard write: on failure show a cross and "Copy failed", never a false check. Announce the result in a `role="status"` region. A labelled variant reserves the width of its longest label so it doesn't resize [expert].
- [ ] **Undo over confirm**: deletes, archives and bulk edits apply at once and show a toast with Undo for ~5s; reserve confirm dialogs for things undo can't reverse. Errors don't auto-dismiss [X: toast grouping, errors must not collapse].
- [ ] **Touch targets**: ≥ 44×44pt on mobile (Apple HIG). Hit area may exceed the visual size.
- [ ] **Haptics-feel on web**: tiny overshoot (bounce 0.2) only on toggles/likes and success.

---

## 7. Workflow: basic prompt → polished result

1. **Classify the request:** SaaS app screen, mobile app, landing page, auth/onboarding, or single component. Pick the matching layout pattern from §2.4.
2. **Choose the theme:** light by default for productivity. Dark for trading, dev tools, or media. Pick **one accent** from §2.2 that fits the domain (finance → blue/black, creative → violet, data/ops → teal/orange, playful consumer → coral/lime).
3. **Pick the type:** Inter for web by default (Geist is an optional alternative) (load via `next/font` or Fontsource). SF Pro Rounded / `ui-rounded` for iOS-feel mobile. Two weights. Apply the tracking rules.
4. **Write the content first.** Use realistic, specific data, not lorem ipsum: names, amounts, dates, statuses (his mocks always use believable data like "Sophia Williams", "$83,820.35", "Oct 10 · Overdue"). Short sentence-case labels.
5. **Block out the layout** on the 4px grid with tokens only (no ad-hoc hex/px). Hierarchy: one H1, one primary action per view.
6. **Build the components** from §4. Prefer hairline shadows over borders. Check tags (tinted), tables (no zebra), and numbers (tabular/mono).
7. **Remove things.** Delete any divider, icon, label, or color that isn't needed. Merge redundant actions.
8. **Add motion in this order:** (a) press/hover/focus states everywhere, (b) enter/exit for overlays, (c) layout animations for indicators and reflow, (d) a single orchestrated page-load reveal (stagger ≤ 300ms), (e) one "hero moment" if it's a landing page (illustration loop, bento animations).
9. **Handle states:** loading skeletons, empty, error, success, disabled, long text truncation, responsive (mobile first: ≥ 360px, then 768, 1024, 1280).
10. **Dark mode pass** with the token overrides. Check contrast.
11. **Accessibility pass:** semantic elements, labels, keyboard paths, focus order, `prefers-reduced-motion`, contrast ≥ 4.5:1 body / 3:1 large.
12. **Polish pass** with §9. Fix small details by hand. This is where it becomes excellent.
13. **Verification round (§9.5):** screenshot at 1440 and 390 plus the hover, focus, and mid-animation states. Check the shots against the §9.5 checklist, fix, and re-shoot. Do at most 2 rounds.

### Prompt-expansion template (use internally)
> "Build {thing} for {domain}. Light theme, accent {hex}, Inter with -3% tracking on titles. Layout: {pattern}. Components: {list}. Realistic data: {examples}. Motion: press scale .97, popovers 200ms ease-out from origin, sliding active indicators with layoutId, staggered first reveal 40ms. States: loading/empty/error. Reduced-motion safe."

---

## 8. Anti-AI-slop rules (from Marcel + popular X sentiment)
Marcel has a post titled "unslopping an ai dashboard" (xpages p004). In October and November 2026, X users repeatedly named the same "AI-built" tells. The most common was the combination of purple gradient, untuned default type, and three cards. Rules below are tagged **[X]** when post sentiment supports them, and **[seen]**/**[expert]** as elsewhere in this skill. Every rule is a hard **don't** with a **do** instead.

1. **No default purple/indigo/violet gradients** (hero, buttons, text, or backgrounds) [X: the most cited tell]. *Do:* use a neutral UI plus one flat accent with a job. A violet accent is fine if it's flat and intentional (his `#7B3AEC` CTA) [seen].
2. **No gradient text and no "one colored word" in the headline** [X]. *Do:* use solid `#171717` and get emphasis from size, weight, or tracking.
3. **No untuned type.** Don't ship default tracking at every size, random weights, or a flat hierarchy where everything looks the same [X: "untuned Inter", "inter at every size", "6 font weights on one screen"; the complaint is about defaults, not the typeface]. *Do:* use Inter (the default here) and tune it. Use −2% to −4% tracking on display sizes, 500–600 for headings, at most 2 weights on screen, and a clear size step between title, body and meta (§2.1).
4. **No emoji as icons, and no emoji status pills ("🟢 LIVE")** [X]. *Do:* use one stroke icon set at 16/20px with stroke 1.5. Don't use Lucide by reflex: Phosphor, Iconoir, or a custom set reads less "default" [X: "lucide everywhere" was named as a tell].
5. **No default shadcn look** (stock zinc grays, stock radius, untouched components) [X]. *Do:* use the §3 tokens, his button recipe (§4.1), and your own radius tiers.
6. **No "centered hero → three icon feature cards → testimonials → CTA" template** [X]. *Do:* build an asymmetric layout with a real product screenshot or UI preview as the hero visual, and use content-specific sections.
7. **No fake social proof** ("Sarah K., Founder" testimonials, made-up logos, "Trusted by 10,000+ teams") and no lorem ipsum [X]. *Do:* use realistic, domain-specific data. Label sample data as sample.
8. **No random radial glow orbs, gradient blobs, dot-grid or neon backgrounds, or glow cards** [X]. *Do:* use a quiet canvas. Use grain or texture only when it carries the brand (his ribbon hero is deliberate and art-directed) [seen].
9. **No drop shadows on everything and no hairline border on every box** [X][seen]. *Do:* use soft layered shadows on elevated layers only, with tonal separation instead of borders.
10. **No card inside a card inside a card** [X: "a card in a card"]. *Do:* give content one container level and use whitespace and hairlines inside it.
11. **No eyebrow label above every heading and no spaced-out uppercase everywhere** [X]. *Do:* use an eyebrow at most once per page. Small uppercase belongs on sidebar section labels only.
12. **No "everything hover-scales" and no fade-up on every scroll section** [X]. *Do:* use purposeful motion: press scale .97 on buttons, sliding indicators, and origin-aware popovers (§5). Reveal on scroll only once and only for hero-level content.
13. **No rainbow or neon palettes and no several competing accents** [X][seen]. *Do:* use one accent, and semantic green/red only for deltas.
14. **No uneven, eyeballed spacing** [X: "uneven spacing… out"]. *Do:* use a strict 4px grid and keep larger gaps between groups than within groups.
15. **No generic beige/cream "AI warm" background or pure-white flatness by default** [X]. *Do:* use a cool neutral canvas `#F7F7F7`/`#FAFAFA` with white panels, or a deliberate brand tone.
16. **No buzzword copy** ("Build faster with AI", "Supercharge your workflow") and no em-dash-heavy marketing voice [X]. *Do:* write concrete, plain, product-specific copy.
17. **No bento grid unless the content is truly heterogeneous** [X]. *Do:* let the content decide the layout.
18. **No glassmorphism by default** [seen in the old list; sentiment groups it with "glow"]. *Do:* use solid surfaces, and blur only for overlays over imagery.
19. **No twin CTAs and no filler cards** ("Get started" + "Learn more" side by side, a fourth stat card to fill the row, an icon in a rounded square on every card) [X]. *Do:* one primary action per view; as many cards as there are real numbers.
20. **No "Welcome back, Alex! 👋" and no exclamation-mark copy** [X]. *Do:* lead with the user's work ("3 deals close this week").
21. **No `"No data"` empty states** [X]. *Do:* say what will appear here and give the action that makes it appear; test with zero items, one item and very long names.
22. **No dead UI** [X]. *Do:* see §6, "Every control does something". Click through every control before you hand it over.

The old list still applies: white text on saturated pills, 600ms+ transitions, scale-from-0 popovers, bouncy springs everywhere, and 1px `#D1D5DB` borders on every box.

**Sentiment sources (X, Oct–Nov 2026):**
- https://x.com/shipper_now/status/2110637576935891122 (≈2.1k likes: no emojis, no "🟢 LIVE" badges, 0 blue/purple gradients)
- https://x.com/tomilola_ng/status/2114078495487729986 (≈190 likes: avoid default Lucide icons and default shadcn colours)
- https://x.com/future_coded/status/2111403845779931591 (same default purple gradient homepage)
- https://x.com/denizdoingstuff/status/2114407641963237633 (lucide everywhere, shadcn grays, one font size/tracking everywhere, same gradient hero)
- https://x.com/tanujbuilds/status/2115834588551594431 (emoji-icon feature cards, "Sarah K., Founder" testimonial)
- https://x.com/AnylancerInc/status/2114401436071043088 (label above every heading, spaced caps, one coloured word, card in a card)
- https://x.com/erramix01/status/2113937292863602955 (radial orbs, dot grids, bento, neon, drop shadows on everything)
- https://x.com/lokidotdev/status/2117188486034063507 (everything hover-scales, 6 font weights)
- https://x.com/_def/status/2115188253863071921 (untuned type, emoji status pills; tabular nums, 4px grid, one accent)
- https://x.com/Zephyr_hg/status/2117371426600784071 (a checkable banned list beats "make it clean"; twin CTAs, fake "10K+" proof)
- https://x.com/preetsuthar17/status/2117540786791493802 (twin CTAs, second primary button, "no data" empty states)
- https://x.com/sinanyorulmazz/status/2116531845839851723 (design checker flags a removed focus ring as an error, "Welcome back 👋" copy)
- https://x.com/equalworld_ai/status/2117349679700623510 (a stray `outline: none` is one of the most common quiet regressions)
- https://x.com/Mr_Buzzoni/status/2106320604634702070 (dead buttons, errors next to the field, keyboard-only pass, real loading/empty/error screens)
- https://x.com/keviduk/status/2109645687176495258 (group background-job toasts; errors must not collapse)

Not found in X posts (Aug–Nov 2026) and tagged [expert] here instead: tooltip delays, double focus rings on composite fields, sidebar collapse/resize.

---

## 9. Final QA checklist

**Visual**
- [ ] One accent color. Everything else neutral or semantic.
- [ ] One font family (+ optional mono), ≤ 2 weights in body UI. Tracking matches size rules.
- [ ] All spacing on the 4px grid. Consistent radii per tier (control 8–10, card 12–16, overlay 20–24).
- [ ] Hairlines via light borders or spread shadows. No harsh borders. Shadows layered and soft.
- [ ] Tags use dark text on light tint. Numbers tabular. Text contrast passes.
- [ ] Realistic content. Truncation with ellipsis and title tooltips.
- [ ] Icons the same stroke (1.5) and size (16/18/20), optically aligned with text.
- [ ] Light and dark both checked.

**Motion & interaction**
- [ ] Every interactive element has hover, press, focus-visible, disabled, and loading states.
- [ ] UI transitions ≤ 300ms. Exits faster than enters. Ease-out or springs, no ease-in on enter.
- [ ] Popovers scale from ≥ 0.95 at the trigger origin. Modals from center.
- [ ] Active indicators slide (layoutId). Lists animate add/remove/reorder.
- [ ] Interruptible: rapidly toggling never jumps or queues.
- [ ] No animation on keyboard-triggered frequent actions.
- [ ] Only transform/opacity animated. `will-change` only where needed. No CLS.
- [ ] `prefers-reduced-motion` honored (MotionConfig `reducedMotion="user"` + CSS media query).
- [ ] Looped/hero animations pause offscreen.

**UX**
- [ ] One primary action per view. Clear hierarchy in a 3-second squint test.
- [ ] Keyboard: tab order, Enter/Escape, shortcuts shown as keycaps where useful.
- [ ] Focus pass: Tab through every control and screenshot it. One ring each, on the outer box of composite fields, not clipped (§4.13).
- [ ] Function pass: click every button, menu item, chip, link and row action. Each one does what its label says (§6).
- [ ] Alignment pass: in sidebars and lists, icons share one column and labels share another; trigger rows match the rows below in width, height and inset.
- [ ] Touch targets ≥ 44px on mobile. Sticky CTA doesn't cover content.
- [ ] Error messages say what happened and how to fix it ("Couldn't save Company. Check your connection. Retry").
- [ ] Review it again the next day with fresh eyes (Emil's advice), or at least do a second full pass.

---

## 9.5 Verification round (screenshot → check → fix, max 2 rounds)
Don't hand over UI you haven't looked at. After building it, render it, look at it, fix it, and look again.

**1. Render.** `pip install playwright && playwright install chromium` (or `npm i -D playwright && npx playwright install chromium`), then start the dev server or open the HTML file directly.
```python
# shots.py: python shots.py http://localhost:3000  (or file:///abs/path/index.html)
import sys, asyncio
from playwright.async_api import async_playwright
URL = sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, w, h in [("desktop", 1440, 900), ("mobile", 390, 844)]:
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            await pg.goto(URL, wait_until="networkidle"); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f"shot-{name}.png", full_page=True)
            if name == "desktop":
                btn = pg.locator("button, a").first           # hover + focus state
                await btn.hover(); await pg.wait_for_timeout(200); await pg.screenshot(path="shot-hover.png")
                await pg.keyboard.press("Tab"); await pg.wait_for_timeout(200); await pg.screenshot(path="shot-focus.png")
                await pg.reload(); await pg.wait_for_timeout(120)  # mid-animation frame of the entrance
                await pg.screenshot(path="shot-midanim.png")
                # geometry dump for the no-vision fallback
                bad = await pg.evaluate("""() => [...document.querySelectorAll('body *')].filter(e => {
                  const r = e.getBoundingClientRect(), s = getComputedStyle(e);
                  return r.width && (r.right > innerWidth + 1 || e.scrollWidth > e.clientWidth + 1 && s.overflowX === 'visible');
                }).slice(0, 20).map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().right))""")
                print("overflow:", bad)
            await pg.close()
        await b.close()
asyncio.run(main())
```

**2. Look.** Open each PNG with your image or file-view tool. Compare the desktop shot side by side with one similar file in `./references/` (and `./references/sidebars/` if the UI has a sidebar).

**3. Check (each item passes or fails, with nothing in between):**
- [ ] **Alignment:** left edges line up on a few shared x-positions. Icons are vertically centered with their text. Numbers are right-aligned in tables.
- [ ] **Spacing rhythm:** every gap is a multiple of 4. Gaps inside a group are smaller than gaps between groups. No cramped edge padding.
- [ ] **Type hierarchy:** one clear title. At most 2 weights. Display tracking is negative. Muted grey is used for secondary text, not for the primary text.
- [ ] **Contrast:** body text ≥ 4.5:1, and nothing important in `#A3A3A3` on white. The focus ring is visible in `shot-focus.png`.
- [ ] **Overflow/clipping:** nothing cut off or scrolling sideways at 390px. No wrapped buttons or labels. Long text truncates with an ellipsis.
- [ ] **Sidebar** (if present): passes §4.12 "Common mistakes" 1–10. It is cleanly **inset** (sidebar on the tinted app background with no fill of its own; content a panel with an even ~8px gap to the top, right and bottom edges, 12–16px radius on all 4 corners, a subtle ring/shadow, and its own scroll) or cleanly **flush** (sidebar on its own surface, one hairline, content edge to edge), never a mix. It has a quiet active pill, a footer pinned to the bottom, and becomes a drawer or tab bar on mobile.
- [ ] **Slop rules:** none of the §8 tells are present (do a quick squint for a purple gradient, emoji, three centered cards, glow orbs, or fake testimonials).
- [ ] **Motion present:** `shot-hover.png` differs from the rest state. `shot-midanim.png` shows elements partly in (opacity or translate between states). The code includes press scale, sliding indicators, and a `prefers-reduced-motion` branch.
- [ ] **Mobile:** touch targets are ≥ 44px, the primary CTA is reachable, and nothing overlaps the sticky bars.

**4. Fix and re-shoot.** Fix every failed item, run the script again, and check again. Stop after **2 rounds**. If anything still fails, list it in your hand-off and don't call the UI done.

**No vision? Use this fallback.** If you can't view images, rely on the DOM instead. Print the `overflow:` list, which must be empty. Use `page.evaluate` to dump `getBoundingClientRect()` for headings, buttons, and nav items, then check that `left` values cluster, `height` of nav items is consistent (e.g. all 32), gaps are multiples of 4, and button heights are equal per row. Read `getComputedStyle` to confirm font-family, weights used (count distinct values ≤ 2–3), `letter-spacing` on h1, `transition`/`animation` present on interactive elements, and compute text contrast from `color` vs. background. Diff the hover and rest screenshot bytes (`!=`) to prove a hover state exists.

---

## 10. Reference images (`./references/`)

All images are from @marcelkargul's public posts and are included for style reference only.

| File | Why it matters |
|---|---|
| `2026-11-03_2117435880021561852_1.png` | "Perfect signup page": split auth card, violet `#7B3AEC` CTA, soft hairline inputs, product preview with carousel dots. |
| `2026-10-30_2116131638916854067_1.png` | Step-by-step secondary button: 30px, 10px radius, Geist 14 Medium, `#FFF→#F7F7F7`, two shadows (exact values). |
| `2026-10-11_2109273659038650501_1.png` | Geist tracking demo at 100px: −6% vs −3% vs 0. Basis of the tracking rules. |
| `2026-10-13_2110066751866089488_1.png` | SF Pro Rounded at +1% letter spacing, his mobile typeface of choice. |
| `2026-10-06_2107619825719910460_2.png` | Command palette: 24px radius, filter pills, grouped results, keycap legend footer. |
| `2026-10-26_2114761395946311853_1.png` | Statsnap dashboard: sidebar shell, mono KPI numbers, delta pills, dark chart tooltip, clean table. |
| `2026-10-03_2106500278157795628_1.png` | Mobile calendar: grey canvas, inset white cards, round icon buttons, pastel event blocks, blue pill CTA. |
| `2026-10-03_2106500391672393990_1.png` | Dark crypto app: `#0D0D0D` base, `#1A1A1A` cards, mono prices, floating pill tab bar. |
| `2026-10-29_2115949035009814905_1.png` | Do/Don't: tinted tags with dark text beat white text on saturated fills. |
| `2026-10-31_2116628486571938143_1.png` | Sleep tracker: black pill CTAs, coral accent, segmented settings lists, theme/color pickers. |
| `2026-11-01_2116933228481433739_1.png` | Landing hero: floating pill nav, grainy gradient ribbons on isometric grid, dark plus white CTAs. |
| `2026-10-25_2114315909817065784_1.png` | Mobile onboarding: segmented progress, selectable rows with check circles, violet pill CTA. |

---

**`./references/sidebars/`** contains 36 sidebar and nav-rail examples from his posts. Look at 2–3 of them before you build any app shell. Recommended starting points:
| File | Why it matters |
|---|---|
| `2026-10-03_2106499785813360687_1.png` | Snaplytics: switcher, search with `/` keycap, sentence-case groups, color-swatch projects, grey active pill. |
| `2026-10-03_2106500336081063986_1.png` | Timelines: "+ New timeline" button, nested Reports children, grey sidebar against white content. |
| `2026-10-14_2110467790343737666_3.png` | Uniops: uppercase group labels, active item with `›`, pinned tools with drag handles. |
| `2026-10-22_2113384174924988778_1.png` | Minto: dashed dividers, rounded active pill, content panel floating on the right. |
| `2026-10-24_2113997498008117362_1.png` | macOS-window app: footer links pinned bottom, translucent sidebar, white content panel. |
| `2026-10-07_2107869459142914419_1.png` | Icon rail (≈8 icons, 2 groups) + list column + detail: the collapsed-rail pattern. |
| `2026-10-06_2107505914345603127_1.png` | Dark actions panel: uppercase labels, colored icons, drag-lifted item, `›` footer row. |
| `2026-10-04_2106852842342375894_1.png` | Close-up: black active pill with white label and count badge. |

---

## Sources
- Anti-slop sentiment: the X posts cited at the end of §8 (searched Nov 3, 2026 via the X API).
- @marcelkargul posts and captions on X (style, typography rules, button recipe, process quotes). Style **inspired by** his work. This skill is not affiliated with him.
- Motion docs, Transitions: https://motion.dev/docs/react-transitions (tween default 0.3s; spring `bounce` default 0.25; `visualDuration`; inertia `power 0.8`, `timeConstant 700`; `stagger` with `grid`/`from`).
- Emil Kowalski, "Great Animations": https://emilkowal.ski/ui/great-animations (ease-out, < 300ms, transform/opacity, interruptibility, reduced motion, no animation on keyboard actions). Also his easing curves `cubic-bezier(0.23,1,0.32,1)` and `(0.77,0,0.175,1)` and the Vaul drawer curve `(0.32,0.72,0,1)`.
- Apple Human Interface Guidelines, Motion and Accessibility (purposeful motion, honor Reduce Motion, 44pt targets) and SwiftUI spring presets (`smooth`/`snappy`/`bouncy`).
