---
name: interface-design
description: Interface design skill for dashboards, admin panels, apps, and tools. NOT for marketing design. Provides design intent, domain exploration, craft principles, and component-driven design-tool↔code sync. For PySide6/Qt technical implementation, use a project-specific GUI implementation skill (if available).
metadata:
  short-description: UIデザイン原則（意図、ドメイン探索、クラフト）。技術実装はプロジェクト固有のGUI実装スキル（あれば）を参照。
  origin: https://github.com/Dammyjay93/interface-design
allowed-tools:
  - Grep
  - Glob
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

# Interface Design

Build interface design with craft and consistency.

## Scope

**Use for:** Dashboards, admin panels, SaaS apps, tools, settings pages, data interfaces.

**Not for:** Landing pages, marketing sites, campaigns.

**For PySide6/Qt implementation:** Use a project-specific GUI implementation skill (if available) for Signal/Slot patterns, Direct Widget Communication, and Qt Designer integration.

---

# The Problem

You will generate generic output. Your training has seen thousands of dashboards. The patterns are strong.

You can follow the entire process below - explore the domain, name a signature, state your intent - and still produce a template. Warm colors on cold structures. Friendly fonts on generic layouts. "Kitchen feel" that looks like every other app.

This happens because intent lives in prose, but code generation pulls from patterns. The gap between them is where defaults win.

The process below helps. But process alone doesn't guarantee craft. You have to catch yourself.

---

# Where Defaults Hide

Defaults don't announce themselves. They disguise themselves as infrastructure - the parts that feel like they just need to work, not be designed.

**Typography feels like a container.** Pick something readable, move on. But typography isn't holding your design - it IS your design. The weight of a headline, the personality of a label, the texture of a paragraph. These shape how the product feels before anyone reads a word.

**Navigation feels like scaffolding.** Build the sidebar, add the links, get to the real work. But navigation isn't around your product - it IS your product. Where you are, where you can go, what matters most.

**Data feels like presentation.** You have numbers, show numbers. But a number on screen is not design. The question is: what does this number mean to the person looking at it? What will they do with it?

**Token names feel like implementation detail.** But your QSS variables are design decisions. `--ink` and `--parchment` evoke a world. `--gray-700` and `--surface-2` evoke a template.

The trap is thinking some decisions are creative and others are structural. There are no structural decisions. Everything is design.

---

# Intent First

Before touching code, answer these. Not in your head - out loud, to yourself or the user.

**Who is this human?**
Not "users." The actual person. Where are they when they open this? What's on their mind? A ML researcher curating training data is not a hobbyist organizing their art collection.

**What must they accomplish?**
Not "use the app." The verb. Tag these images. Filter by quality. Export the dataset. The answer determines what leads, what follows, what hides.

**What should this feel like?**
Say it in words that mean something. "Clean and modern" means nothing. Dense like a trading floor? Calm like a reading app? Focused like an IDE?

If you cannot answer these with specifics, stop. Ask the user. Do not guess. Do not default.

## Every Choice Must Be A Choice

For every decision, you must be able to explain WHY.

- Why this layout and not another?
- Why this color temperature?
- Why this typeface?
- Why this spacing scale?
- Why this information hierarchy?

If your answer is "it's common" or "it's clean" or "it works" - you haven't chosen. You've defaulted.

**The test:** If you swapped your choices for the most common alternatives and the design didn't feel meaningfully different, you never made real choices.

## Sameness Is Failure

If another AI, given a similar prompt, would produce substantially the same output - you have failed.

This is not about being different for its own sake. It's about the interface emerging from the specific problem, the specific user, the specific context.

---

# Product Domain Exploration

This is where defaults get caught - or don't.

Generic output: Task type -> Visual template -> Theme
Crafted output: Task type -> Product domain -> Signature -> Structure + Expression

## Required Outputs

**Do not propose any direction until you produce all four:**

**Domain:** Concepts, metaphors, vocabulary from this product's world. Not features - territory. Minimum 5.

**Color world:** What colors exist naturally in this product's domain? Not "warm" or "cool" - go to the actual world. List 5+.

**Signature:** One element - visual, structural, or interaction - that could only exist for THIS product. If you can't name one, keep exploring.

**Defaults:** 3 obvious choices for this interface type - visual AND structural. You can't avoid patterns you haven't named.

## Domain Example: インシデント管理ダッシュボード

For an incident management dashboard (a representative "tools" domain — apply the same questions to your own product):

**Domain:** Air-traffic control tower, hospital triage board, fire station status wall, ship's bridge, mission control console

**Color world:** Radar-screen greens, muted night-shift grays, alert ambers reserved for genuine emergencies, the calm blue of an all-clear board

**Signature:** The "calm authority feel" - severity is instantly legible at a glance, and quiet states look genuinely quiet instead of decoratively busy

**Defaults to reject:**
- Generic red/yellow/green badges -> A severity language where color is backed by shape and position
- Endless table of alerts -> Triage lanes that make "what needs me now" structural
- Standard toast notifications -> Status transitions logged on a visible timeline

---

# The Mandate

**Before showing the user, look at what you made.**

Ask yourself: "If they said this lacks craft, what would they mean?"

That thing you just thought of - fix it first.

## The Checks

Run these against your output before presenting:

- **The swap test:** If you swapped the typeface for your usual one, would anyone notice? If you swapped the layout for a standard dashboard template, would it feel different?

- **The squint test:** Blur your eyes. Can you still perceive hierarchy? Is anything jumping out harshly? Craft whispers.

- **The signature test:** Can you point to five specific elements where your signature appears? Not "the overall feel" - actual components.

- **The token test:** Read your QSS variables out loud. Do they sound like they belong to this product's world?

If any check fails, iterate before showing.

---

# Craft Foundations

## Subtle Layering

**Surfaces must be barely different but still distinguishable.** Study Vercel, Supabase, Linear. Their elevation changes are so subtle you almost can't see them - but you feel the hierarchy.

**Borders must be light but not invisible.** The border should disappear when you're not looking for it, but be findable when you need to understand structure.

**The squint test:** Blur your eyes at the interface. You should still perceive hierarchy - what's above what, where sections divide. But nothing should jump out.

## Infinite Expression

Every pattern has infinite expressions. **No interface should look the same.**

A metric display could be a hero number, inline stat, sparkline, gauge, progress bar, comparison delta, trend badge, or something new. Even sidebar + cards has infinite variations in proportion, spacing, and emphasis.

**NEVER produce identical output.** Same sidebar width, same card grid, same metric boxes with icon-left-number-big-label-small every time - this signals AI-generated immediately.

## Color Lives Somewhere

Every product exists in a world. That world has colors.

Before you reach for a palette, spend time in the product's world. What would you see if you walked into the physical version of this space?

Your palette should feel like it came FROM somewhere - not like it was applied TO something.

---

# Design Principles

## Spacing
Pick a base unit and stick to multiples. Consistency matters more than the specific number. Random values signal no system.

## Depth
Choose ONE approach and commit:
- **Borders-only** - Clean, technical. For dense tools.
- **Subtle shadows** - Soft lift. For approachable products.
- **Layered shadows** - Premium, dimensional. For cards that need presence.

Don't mix approaches.

## Border Radius
Sharper feels technical. Rounder feels friendly. Pick a scale and apply consistently.

## Typography
Headlines need weight and tight tracking. Body needs readability. Data needs monospace. Build a hierarchy.

## Color & Surfaces
Build from primitives: foreground (text hierarchy), background (surface elevation), border (separation hierarchy), brand, and semantic (destructive, warning, success).

## Animation
Fast micro-interactions (~150ms), smooth easing. No bouncy/spring effects.

## States
Every interactive element needs states: default, hover, active, focus, disabled. Data needs states too: loading, empty, error. Missing states feel broken.

---

# Avoid

- **Harsh borders** - if borders are the first thing you see, they're too strong
- **Dramatic surface jumps** - elevation changes should be whisper-quiet
- **Inconsistent spacing** - the clearest sign of no system
- **Mixed depth strategies** - pick one approach and commit
- **Missing interaction states** - hover, focus, disabled, loading, error
- **Dramatic drop shadows** - shadows should be subtle, not attention-grabbing
- **Large radius on small elements**
- **Pure white cards on colored backgrounds**
- **Thick decorative borders**
- **Gradients and color for decoration** - color should mean something
- **Multiple accent colors** - dilutes focus

---

# PySide6/Qt Integration

For technical implementation in PySide6:

## QSS (Qt Style Sheets)

Apply design principles through QSS with meaningful token names:

```css
/* Good: Domain-specific naming */
QWidget {
    --surface-archive: #1a1a1a;
    --surface-lightbox: #242424;
    --border-specimen: rgba(255,255,255,0.08);
    --text-catalog: #e0e0e0;
}

/* Bad: Generic naming */
QWidget {
    --bg-1: #1a1a1a;
    --bg-2: #242424;
}
```

## Widget Design Process

1. **Intent First** - Define who, what, feel before implementation
2. **Domain Exploration** - Apply Required Outputs
3. **Technical Implementation** - Use a project-specific GUI implementation skill (if available) for Signal/Slot patterns
4. **Craft Check** - Run The Mandate checks

## Coordination with a project GUI skill

| Aspect | interface-design | project GUI skill |
|--------|------------------|-------------------|
| Focus | Design intent, aesthetics, craft | Technical patterns, Qt APIs |
| Answers | Why this design? | How to implement? |
| Outputs | Color world, signature, hierarchy | Signal/Slot, Widget structure |

---

# Design Tool ↔ Implementation Sync (component-driven)

When a design tool holds the design system (e.g. a hosted design app the team syncs to),
know what is and is not synced — this is platform-neutral; it applies whatever agent or
editor you run in.

- The connector syncs the **component catalog** (tokens + reusable components), one-way:
  repo → design tool. It does **not** sync **screen compositions** back, and it does **not**
  generate implementation (PySide/Qt) code.
- Screen layouts (which components, arranged how) live only in the design tool as mockups.
  Porting them to the app is **manual**.
- So design and implementation **drift** whenever a screen is ported only partially, the
  design changes, or correct components are dropped into a legacy layout.

To prevent drift, work **component-driven**, not screen-by-screen:

1. **Per component** — the design tool already defines each reusable widget (the catalog).
   Treat each as the spec (its component source + usage notes).
2. **Judge commonization** — decide: extract a reusable widget in code, or inline it.
   Extract widgets used in **2+ screens**; inline true one-offs. Widget extraction is cheap
   composition, not a big refactor.
3. **Mirror in code** — build a reusable widget that mirrors the design component, driven by
   the shared **design tokens** (one token source of truth). Keep mirrors in a dedicated module.
4. **Compose** — build each screen from the mirrored widgets, so the app and the design's
   screens share the same component vocabulary. Both sides now reuse the same parts and stay
   aligned.

Anti-patterns:

- Hand-porting each screen from scratch → repeats the drift.
- Building the whole mirror library speculatively before any screen uses it (YAGNI). Build the
  components a screen actually needs, prove them by composing that screen, reuse on the next.
- Placing correct components inside the old layout and calling the screen done — components
  right, structure wrong = visual divergence.

Tokens are the **only** thing the two implementations share. Keep their values in sync between
the design tool's stylesheet and the app's token module — this is **not automatic**; verify it.
For the extraction/Qt mechanics of the mirror widgets, use a project-specific GUI implementation skill (if available).

---

# Workflow

## Communication
Be invisible. Don't announce modes or narrate process.

## Suggest + Ask
Lead with your exploration and recommendation, then confirm:

```
"Domain: [5+ concepts from the product's world]
Color world: [5+ colors that exist in this domain]
Signature: [one element unique to this product]
Rejecting: [default 1] -> [alternative], [default 2] -> [alternative]

Direction: [approach that connects to the above]"

[AskUserQuestion: "Does that direction feel right?"]
```

## After Completing a Task

When you finish building something, **always offer to save**:

```
"Want me to save these patterns for future sessions?"
```

If yes, write to `.interface-design/system.md`:
- Direction and feel
- Depth strategy (borders/shadows/layered)
- Spacing base unit
- Key component patterns

---

# Scope Note

この skill は設計原則の提供のみを行う。上流プラグイン由来のスラッシュコマンド
(status/audit/extract) はこの kit には同梱していない。
