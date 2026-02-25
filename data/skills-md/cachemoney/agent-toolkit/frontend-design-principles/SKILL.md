---
name: frontend-design-principles
description: Create polished, intentional frontend interfaces. Use this skill when building any UI — dashboards, admin panels, landing pages, marketing sites, or web applications. Routes to specialized guidance based on context.
---

# Frontend Design Principles

Build frontend interfaces with craft and intention.

## Scope & Routing

After reading this file, load additional guidance based on what you're building:

**Load `app.md` when building:**
- Dashboards and admin interfaces
- Settings panels and configuration screens
- Internal tools and SaaS products
- Data-heavy interfaces with tables, forms, lists
- Any interface where users work repeatedly

**Load `marketing.md` when building:**
- Landing pages and marketing sites
- Promotional materials and announcements
- Creative artifacts and posters
- Public-facing pages meant to impress
- Any interface where first impression matters most

If unclear, ask. Some projects blend both — a SaaS marketing site needs `marketing.md`, but its actual product dashboard needs `app.md`.

## Why This Process Exists

You will generate generic output. Your training has seen thousands of dashboards, landing pages, marketing sites. The patterns are strong.

You can follow the entire process below — explore the domain, name a signature, state your intent — and still produce a template. Warm colors on cold structures. Friendly fonts on generic layouts. "Kitchen feel" that looks like every other app.

This happens because intent lives in prose, but code generation pulls from patterns. The gap between them is where defaults win.

The process below helps. But process alone doesn't guarantee craft. You have to catch yourself.

## Where Defaults Hide

Defaults don't announce themselves. They disguise themselves as infrastructure — the parts that feel like they just need to work, not be designed.

**Typography feels like a container.** Pick something readable, move on. But typography isn't holding your design — it IS your design. The weight of a headline, the personality of a label, the texture of a paragraph. These shape how the product feels before anyone reads a word. A bakery management tool and a trading terminal might both need "clean, readable type" — but the type that's warm and handmade is not the type that's cold and precise. If you're reaching for your usual font, you're not designing.

**Navigation feels like scaffolding.** Build the sidebar, add the links, get to the real work. But navigation isn't around your product — it IS your product. Where you are, where you can go, what matters most. A page floating in space is a component demo, not software. The navigation teaches people how to think about the space they're in.

**Data feels like presentation.** You have numbers, show numbers. But a number on screen is not design. The question is: what does this number mean to the person looking at it? What will they do with it? A progress ring and a stacked label both show "3 of 10" — one tells a story, one fills space. If you're reaching for number-on-label, you're not designing.

**Token names feel like implementation detail.** But your CSS variables are design decisions. `--ink` and `--parchment` evoke a world. `--gray-700` and `--surface-2` evoke a template. Someone reading only your tokens should be able to guess what product this is.

The trap is thinking some decisions are creative and others are structural. There are no structural decisions. Everything is design. The moment you stop asking "why this?" is the moment defaults take over.

## Required: Before Generating

Do not write code until you complete these steps.

### 1. Answer the Intent Questions

Answer these out loud — to yourself or the user. If you cannot answer with specifics, ask the user. Do not guess. Do not default.

- [ ] **Who is this human?** Not "users." The actual person. Where are they when they open this? What's on their mind? What did they do 5 minutes ago, what will they do 5 minutes after?
- [ ] **What must they accomplish?** Not "use the dashboard." The verb. Grade these submissions. Find the broken deployment. Approve the payment.
- [ ] **What should this feel like?** Say it in words that mean something. "Clean and modern" means nothing — every AI says that. Warm like a notebook? Cold like a terminal? Dense like a trading floor? Calm like a reading app?

### 2. Produce the Four Required Outputs

Do not propose any direction until you produce all four:

- [ ] **Domain:** Concepts, metaphors, vocabulary from this product's world. Not features — territory. Minimum 5.
- [ ] **Color world:** What colors exist naturally in this product's domain? Not "warm" or "cool" — go to the actual world. If this product were a physical space, what would you see? List 5+.
- [ ] **Signature:** One element — visual, structural, or interaction — that could only exist for THIS product. If you can't name one, keep exploring.
- [ ] **Defaults to reject:** 3 obvious choices for this interface type — visual AND structural. You can't avoid patterns you haven't named.

### 3. Propose Direction and Confirm

Your proposal must explicitly reference:
- Domain concepts you explored
- Colors from your color world exploration
- Your signature element
- What replaces each default you're rejecting

**The test:** Read your proposal. Remove the product name. Could someone identify what this is for? If not, it's generic. Explore deeper.

Format:
```
Domain: [5+ concepts from the product's world]
Color world: [5+ colors that exist in this domain]
Signature: [one element unique to this product]
Rejecting: [default 1] → [alternative], [default 2] → [alternative], [default 3] → [alternative]

Direction: [approach that connects to the above]

Does that direction feel right?
```

Wait for confirmation before generating code.

## Required: Before Showing

Your first output is probably generic. That's normal. The work is catching it before the user has to.

**Before showing the user, look at what you made.** Ask yourself: "If they said this lacks craft, what would they mean?" That thing you just thought of — fix it first.

Run these checks. If any fails, iterate before showing:

- [ ] **The swap test:** If you swapped the typeface for your usual one, would anyone notice? If you swapped the layout for a standard template, would it feel different? The places where swapping wouldn't matter are the places you defaulted.
- [ ] **The squint test:** Blur your eyes. Can you still perceive hierarchy? Is anything jumping out harshly? Craft whispers.
- [ ] **The signature test:** Can you point to specific elements where your signature appears? Not "the overall feel" — actual components. A signature you can't locate doesn't exist.
- [ ] **The token test:** Read your CSS variables out loud. Do they sound like they belong to this product's world, or could they belong to any project?

## Principles

These shape how you think about design decisions.

### Every Choice Must Be A Choice

For every decision, you must be able to explain WHY.

- Why this layout and not another?
- Why this color temperature?
- Why this typeface?
- Why this spacing scale?
- Why this information hierarchy?

If your answer is "it's common" or "it's clean" or "it works" — you haven't chosen. You've defaulted. Defaults are invisible. Invisible choices compound into generic output.

**The test:** If you swapped your choices for the most common alternatives and the design didn't feel meaningfully different, you never made real choices.

### Sameness Is Failure

If another AI, given a similar prompt, would produce substantially the same output — you have failed.

This is not about being different for its own sake. It's about the interface emerging from the specific problem, the specific user, the specific context. When you design from intent, sameness becomes impossible because no two intents are identical.

When you design from defaults, everything looks the same because defaults are shared.

### Intent Must Be Systemic

Saying "warm" and using cold colors is not following through. Intent is not a label — it's a constraint that shapes every decision.

If the intent is warm: surfaces, text, borders, accents, semantic colors, typography — all warm. If the intent is dense: spacing, type size, information architecture — all dense. If the intent is calm: motion, contrast, color saturation — all calm.

Check your output against your stated intent. Does every token reinforce it? Or did you state an intent and then default anyway?

### Infinite Expression

Every pattern has infinite expressions. No interface should look the same.

A metric display could be a hero number, inline stat, sparkline, gauge, progress bar, comparison delta, trend badge, or something new. A dashboard could emphasize density, whitespace, hierarchy, or flow in completely different ways. Even sidebar + cards has infinite variations in proportion, spacing, and emphasis.

**NEVER produce identical output.** Same sidebar width, same card grid, same metric boxes with icon-left-number-big-label-small every time — this signals AI-generated immediately. It's forgettable.

Linear's cards don't look like Notion's. Vercel's metrics don't look like Stripe's. Same concepts, infinite expressions.

## Craft Foundations

These apply regardless of design direction. This is the quality floor.

### Subtle Layering

This is the backbone of craft.

**Surfaces must be barely different but still distinguishable.** Study Vercel, Supabase, Linear. Their elevation changes are so subtle you almost can't see them — but you feel the hierarchy. Not dramatic jumps. Not obviously different colors. Whisper-quiet shifts.

**Borders must be light but not invisible.** The border should disappear when you're not looking for it, but be findable when you need to understand structure. If borders are the first thing you notice, they're too strong. If you can't tell where regions begin and end, they're too weak.

### Color Lives Somewhere

Every product exists in a world. That world has colors.

Before you reach for a palette, spend time in the product's world. What would you see if you walked into the physical version of this space? What materials? What light? What objects?

Your palette should feel like it came FROM somewhere — not like it was applied TO something.

**Color Carries Meaning:** Gray builds structure. Color communicates — status, action, emphasis, identity. Unmotivated color is noise. One accent color, used with intention, beats five colors used without thought.

## Universal Anti-Patterns

These are always wrong regardless of context:

- **Dramatic drop shadows**: `box-shadow: 0 25px 50px...` looks cheap
- **Arbitrary asymmetric padding**: Every value should be intentional
- **Thick decorative borders**: 2px+ borders for visual weight
- **Multiple accent colors**: One accent, used consistently
- **Mixing depth strategies**: Pick borders OR shadows, not both randomly
- **Default thinking**: Reaching for familiar patterns without considering context
- **Harsh borders**: If borders are the first thing you see, they're too strong
- **Dramatic surface jumps**: Elevation changes should be whisper-quiet
- **Inconsistent spacing**: The clearest sign of no system

## Workflow

### Communication

Be invisible. Don't announce modes or narrate process.

**Never say:** "Let me explore the domain...", "Running the checks..."

**Instead:** Jump into work. State suggestions with reasoning.

## Deep Dives

For technical implementation details:
- `references/principles.md` — Spacing, depth, typography, color implementation, dark mode

For context-specific guidance:
- `app.md` — Dashboards, admin panels, SaaS products
- `marketing.md` — Landing pages, marketing sites, creative artifacts
