---
name: brand
description: "The entry point for any brand work. Gathers the brand's existing assets itself from just a URL (crawling the site, following its links to social and press) — or, for a brand that doesn't exist yet, starts from the name and the idea — diagnoses how much should change, routes to the right path, and gets-or-makes the brand context document every other design skill reads. Use at the start of any design project, or when the user mentions 'brand context,' 'set up the brand,' 'brand guidelines,' 'our visual identity,' 'rebrand,' 'refresh our brand,' 'what's our brand,' 'starting a new brand,' 'we don't have a website yet,' or wants to stop re-explaining their colors, type, and visual direction on every task. Creates and maintains `.agents/brand.md`."
metadata:
  version: 1.29.0
---

# Brand

This is the **front door** for any brand work, and it has two jobs:

1. **Understand what exists, diagnose how much should change, and route.** The depth of the work — a ground-up build, a refresh, or just better execution — is *your* diagnosis to make from the evidence. The user does not need to know the framework behind it.
2. **Own the record.** Get-or-make **`.agents/brand.md`** — the single source of truth for the brand's visual identity that every other design skill reads first, so the user never re-explains their colors, type, muses, or latitude.

> `brand` always runs. `brand-strategy` is the deep generative path it *routes to* — and when the brand is already sound, it routes away from strategy entirely. That's why they're separate skills: one runs without the other.

## Step 1: Gather the Assets — Do the Legwork Yourself

Start here, always — and **take this off the user's plate.** Don't hand them a homework assignment ("send me your logo files, your colors, your social links, your decks…"). Get the one thing you actually need to begin — **the website URL** (or, failing that, the company name) — and go find the rest yourself.

### No website yet — a brand that doesn't exist

If there's no URL — pre-launch, a new company, a side project — don't fake a crawl. Gather what exists instead: the **name**, a **one-liner**, the **category**, and anything already made (a logo sketch, a pitch deck, a domain, a social handle). Source and confirm the competitor set exactly as below. Then:

- **Skip the nine-category scorecard.** There's nothing to score, and a column of zeros tells a founder nothing. Show the **competitive visual landscape** instead: the confirmed competitors' sites side by side, with the lane they all share named plainly ("everyone is dark mode with one neon accent"). That lane is what the founder is deciding whether to leave.
- **The depth is a Revolution by default** — not a judgement; there's simply nothing to keep yet. Say so in plain words. If they already have something they love (a name, a mark, a color), record it as **Fixed core** and treat it as equity.
- **Stub `.agents/brand.md`** — Brand at a glance, the competitor set, the landscape finding, the Toolkit — and route to `brand-strategy`.

**From just the domain, gather autonomously:**
- **Crawl the key pages**, not only the homepage — home, product/features, pricing, about, blog. Each surface uses the brand differently.
- **Extract real values from the rendered pages** — computed colors, `font-family` names, type scale, spacing, button/CTA treatment, radii, shadows.
- **Capture the logo — and make sure it's the *current* one.** The source of truth for the live mark is the **navigation bar / header of the rendered site**, nothing else. Inspect the actual `<header>`/`<nav>` and pull the exact asset it uses — the `<img src>`, the inline `<svg>`, or the CSS `background-image`. A plain text/markdown fetch strips this out, so read the raw HTML/DOM or screenshot the nav and confirm what you extracted matches what's on screen.
  - **Favicons, apple-touch-icons, manifest icons, OG images, social avatars, and press-kit downloads are frequently outdated** — teams refresh the nav logo and forget the rest. Treat them as *secondary*: useful for collecting the other implementations (small, square, reversed), but **reconcile every one against the nav logo**. If they disagree, the live nav wins as "current," and the mismatch is itself a finding (stale assets to fix).
  - You still want the full set — a mark's *simplicity* is judged by whether it's the **same** mark across all of them — but the **nav logo is the reference**, not the favicon. Don't let an old favicon or a stale press kit stand in for the current identity.
- **Follow the footer.** Almost every site links its own social profiles, app-store listings, and sometimes a press or brand page down there. Harvest those links and follow them.
- **Check the common brand/press paths** — `/brand`, `/brand-assets`, `/press`, `/media-kit`, `/about/brand`. Companies routinely publish logos, palettes, and usage rules there.
- **Screenshot and actually *look* at the rendered design — don't score from tokens alone.** A brand's identity often lives in things a CSS/token dump or a product-UI Figma never expose: a recurring **graphic motif** (a radial, shape, or texture repeating across the hero, sections, and social), the **accent colors** used only in the hero or social art, and the **logo's symbol/glyph**. Examine the hero, feature graphics, and social posts directly. Never conclude "no pattern" or "wordmark-only, no mark" from tokens — confirm with your eyes. These feed Pattern & Texture, Color, and Logo, and missing them is how a strong brand gets mis-scored as weak.
- **Read the codebase if you're in it.** A site repo's CSS / Tailwind config / design-token files are the most precise source there is — prefer them over anything inferred from a screenshot.
- **Pull Figma** if a link or connected file is available.
- **Source the competitor set from the marketing context — don't freelance it.** Identifying competitors by gut is hit-or-miss; pull the authoritative set instead, in this order:
  1. **`.agents/product-marketing.md`** (from the marketing-skills library) — if it exists, use its **Competitive Landscape**: direct / secondary / indirect competitors, with why each falls short. The audit scores distinctiveness against the **direct** set; secondary/indirect inform the landscape but aren't the visual peer group.
  2. **The `competitor-profiling` skill** — if there's no marketing context, run it (`/competitor-profiling`) to research and profile competitors properly, rather than guessing.
  3. **Autonomous discovery** — fallback only: infer the direct competitors from the category, the positioning, and the brand's own comparison/alternative pages.

  Then capture each direct competitor's identity across the nine audit categories — the comparison set the Step 2 audit scores against (see [references/brand-audit.md](references/brand-audit.md)) — and confirm the list with the user (below).

**Confirm the competitor set before any scoring.** Your idea of "direct competitors" is often wrong, and the entire distinctiveness verdict rides on it. Present the list you assembled — *"Here's who I'm treating as your direct competitors: … Anyone to add, remove, or swap?"* — and get the user's sign-off before running the Step 2 scorecard. Don't score against an unverified set.

**Then show the user what you found, and ask only for the gaps you genuinely can't reach yourself:**
- Private or internal material — a Figma you don't have access to, sales decks, print collateral, photography libraries not on the site
- The **why** behind decisions you can only see the *what* of
- Anything the Step 2 diagnosis hinges on that the assets don't answer

**Build the asset inventory** from all of it — what you gathered, what the user added, and what's still missing. Gaps are findings: they show where the brand is undefined, and how much exists is the first input to the diagnosis.

**As you ingest** (see [references/asset-intake.md](references/asset-intake.md)):
- Extract concrete values — hex codes, named typefaces, spacing, logo lockups, photo treatment — not impressions
- **Watch how the brand behaves across mediums.** The site may be buttoned-up while social runs loose — that contrast *is* data; it reveals what's truly **fixed** vs. what already **flexes**.
- **Stated ≠ practiced.** A style guide claims one thing; the live assets often show another. Capture both and flag the drift.

If little or nothing exists, that itself is the key finding — carry it into the diagnosis.

## Step 2: Diagnose How Much Should Change

**This is your diagnosis, not a question for the user — and you make it with a critical eye, not a generous one.** A client has no idea what "Revolution / Evolution / Optimization" mean — never ask them to pick or lead with the jargon. Read the situation from the assets in Step 1 plus a few plain questions, then conclude. These are *your* internal scoping labels:

**The verdict is a phased recommendation anchored to the client's appetite and timeline — not a single label derived from the scores.** Ask, plainly, how much they want to change *now* vs. later, and whether they want incremental polish or a transformational break; that appetite isn't visible in the assets and it's the *primary* driver. A brand can score low and still be **"Optimization now, deeper work later."** Diagnose honestly (competitor similarity + scores) to shape the *roadmap*, then recommend a path — often sequenced:

- **Optimization** — the immediate design-fundamentals work on the *existing* assets (typography, hierarchy, contrast, layout, palette rationalization, consistency). The right starting point for **any client moving incrementally — even a generic-foundation one** — with deeper work teed up for later; also the terminal answer when assets are strong and only execution lags (the strong-assets-badly-built case). *(Or the low-scoring, genuinely generic brand whose client wanted "optimization now, bigger later" → Optimization now, refine what exists, sequence creative-direction later.)*
- **Evolution** — keep the equity, do generative build-out (creative direction, motif, deploy missing pieces) — the equity-in-a-drawer case.
- **Revolution** — rebuild the foundation: colliding/undifferentiated with little to keep (the lookalike case), or the client wants a transformational break and has the appetite for it.

**Never override the client's incremental appetite with a diagnosis-driven verdict, and never argue against the depth they asked for.** Be honest about what each phase buys: Optimization-now makes a generic brand *tidier*, not *distinct* — distinctiveness comes from the creative-direction phase. Don't sell polish as distinctiveness; don't refuse polish because distinctiveness needs more. The common shape is **micro now (Optimization) → macro later (creative direction)**.

**Optimization vs Evolution:** in an Optimization you change only *how existing assets are implemented* (design fundamentals on what's there); in an Evolution you also *create, define, or deploy* pieces that are missing, unanchored, or sitting in a drawer.

At **moderate** similarity it's a genuine **fork the client chooses by appetite**: Optimization (content with the overlap → keep the assets, execute higher, shore the gaps) vs Revolution (want to break away → a wholesale shift, not incremental). Weigh their stated ambition; never assume it.

**Hold a high bar — coherent is not the same as good** (see `design-principles` → Coherent Is Not the Same as Good):

- Consistency, intentionality, and "not dated" are *table stakes*, not proof of a sound brand. A tidy brand is usually just *fine* — and "fine" is an **Evolution**, not an Optimization.
- **Test distinctiveness, not just coherence.** Look outward — scan the category, the direct competitors, and the prevailing design trend. A brand is only distinct *relative to them*. With the logo covered, would anyone know it was them?
- **Name the default.** A polished execution of the current category or AI-startup aesthetic — near-black canvas, high-contrast serif display, a single jewel-tone accent, parchment warmth, a tasteful mono — is *generic*, not sound. Reading as "deliberate" doesn't save it; everyone is deliberate in the same way. Flag the trend as a finding, not a strength.
- **Assess the logo specifically** with `logo-design` against the SAD bar — **Simple** (it must hold in plain black & white; if it leans on color or a gradient to read, that's a failure), **Appropriate** (to the emotional target), **Distinct** (against the competitor logos you gathered, not in isolation). A weak or generic mark is a real part of the diagnosis — don't wave it through because it's "their logo." And **the mark is always on the table**: if the creative direction is shifting significantly (Revolution or serious Evolution), the logo is in scope for change too — flag that rather than treating it as untouchable equity.
- **Lead with the critique — but separate diagnosis from recommendation.** Your value is catching "this is fine" dressed up as "this is good": a generic or competitor-colliding foundation is *not* a sound brand — don't declare it fundamentally fine. That's the honest *diagnosis* (the scores). It's separate from the *recommendation*, which is phased and appetite-anchored — you can diagnose a weak foundation *and* still recommend Optimization-now (fundamentals first), with the creative-direction work sequenced later. Don't confuse "the foundation is weak" (a scoring truth) with "so we must Revolutionize now" (a recommendation the client's appetite may not support).
- **Don't be fooled by rank or drift.** "We're #2 in the category" is not distinctiveness if the category is a lookalike cluster — best-in-cluster is still generic (this applies to the logo too: least-plain wordmark in a plain set ≠ distinct). And finding execution problems (stale press kit, half-finished font migration, fragmenting color) does *not* mean the foundation is *sound* — drift routinely sits on top of an undifferentiated foundation, so don't let it inflate the foundational *scores*. (It's fine for those execution fixes to become the Optimization-now *phase* of the roadmap — just don't mistake them for evidence the foundation is strong.)
- **Implementation flaws are not weak assets.** Look *through* a rough site. A distinctive pattern shown at blown-out contrast is a *strong asset, badly executed* — an Optimization signal — not a weak pattern; a great typeface buried in banded layouts is still a great typeface. Assess each asset's intrinsic quality and distinctiveness *separately* from how well the current site implements it. Slop-ish execution (banding, over-contrast, screenshot bleed) sitting on strong, distinct, *deployed* assets means fix the build (Optimization) — not a weak foundation.

**Run the brand audit — don't eyeball it.** Work through the nine categories ([references/brand-audit.md](references/brand-audit.md)) against the **confirmed** competitor set, with named comparisons (whose palette/mark/motif it resembles or collides with). Score on **two axes**: the foundational categories (Creative Direction, Color, Logo, Pattern) on *distinctiveness* against the field; the craft categories (Typography & Layout, Graphics, Icons, Application, Style Guide) on *execution quality* — where well-made, consistent work reaches 4–5 even with a common typeface or stock icons. **Creative Direction does NOT cap the craft scores.** Then read **competitor similarity** — the heaviest-weighted pivot — and let it plus the client's appetite drive the path (split fork at moderate similarity). Present the recommended path with rationale **and the alternative's tradeoff**. Write the audit into `.agents/brand.md`.

**Run the AI-slop check** ([../design-principles/references/ai-slop.md](../design-principles/references/ai-slop.md)) on the brand and the whole set. Tropes — a left accent rail, a purple-to-blue gradient, a cramped center container, no variety between section layouts, `rounded-lg` on everything — are findings that **cap a dimension's score**, however "clean" it looks. Name each one you find.

**Diagnose from plain signals** (ask only what the assets don't answer):
- Is the brand *wrong/off-strategy*, just *dated*, *coherent but generic*, or *genuinely strong and distinct but poorly applied*?
- Is it actually distinct in its category, or a tidy version of the current trend?
- What's real equity worth protecting, vs. what only *looks* finished?
- How much exists, and how good is it, honestly?
- **What's the appetite and timeline?** Do they want to change a lot now, or move incrementally — fundamentals now, bigger moves later? This drives the recommended path more than the scores do. *Ask it; don't infer it* — it isn't visible in the assets.

This also sets your **mode**: a genuinely strong brand → *ingest and protect the equity*; an okay-or-absent one → *raise or generate it through discovery*.

**Reflect your conclusion back in plain terms, honestly** — e.g., *"Your brand is coherent and clearly intentional, but right now it looks a lot like the rest of the AI-tools category — serif-on-black with a single green accent is everywhere this year. That's not a broken brand, but it's not a distinct one yet. So I'd treat this as an evolution: keep the name and the bones, push the look somewhere only you could own."* Don't flatter coherent-but-generic work into "sound." Use the REO word only if it helps; the honest read and the routing are what matter.

### Present the full assessment — don't skip to the verdict

**The per-category breakdown is the deliverable, not a byproduct.** Always present it in the response — never collapse the audit into a one-line verdict or only write it to a file. Show, in this order:

1. **The scorecard table** — all nine categories with their scores, a blank **"Your score"** column for the user, plus the **Competitor similarity** read and the **verdict + recommended path**.
2. **The per-category breakdown** — for each of the nine: the score, **Why it matters**, **Current status** (with named competitor comparisons), and **Moving forward**.
3. **The competitor set** used, the **name / verbal-identity** flag, and the **AI-slop** findings.
4. **The split paths** — the recommended depth with rationale *and* the alternative's tradeoff.

The one-line verdict is a header on top of this breakdown, never a replacement for it. Also save it as a standalone artifact (e.g. `<brand>-brand-audit-scorecard.md`) alongside `.agents/brand.md` so the user keeps a copy — but presenting it in full comes first.

**On the appetite question — present the scorecard first, then confirm appetite.** Appetite is the primary driver of the *recommendation*, but asking it cold, before the client has seen a single score, feels arbitrary to them ("why are you asking how much I want to change before you've told me what's wrong?"). Do the diagnosis and **show the scorecard**, then have the appetite conversation with the score in front of you — the number is the concrete thing they react to ("21/45 and colliding with three competitors — how much of that do you want to take on now vs. later?"). If you gathered a preliminary appetite read earlier, revisit and confirm it against the score rather than treating the early answer as final.

**Findings in plain language — no unexplained jargon.** Every line the client reads should be self-evident. If a category note would land as a cryptic fragment ("Application: unavoidable"), rewrite it as a plain sentence that says what you mean and why it matters. A finding the client can't parse is a finding that does nothing.

## Step 3: Route by Depth

### Revolution → define it from scratch
There's little to capture. Send the user to **`brand-strategy`** for full discovery (vision, muses, emotional target, distinct concepts, and the fixed-core / flexible-range latitude), then **`creative-direction`** to build the visual system. `.agents/brand.md` starts mostly empty and fills as those skills produce answers. Stub it now so the structure is ready.

### Evolution → capture, then change only the deltas
1. **Capture what exists** (from the assets ingested in Step 1) into `.agents/brand.md` — the real current colors, type, assets, voice. Be accurate; this is the baseline.
2. **Separate what stays from what changes.** Make the equity explicit (this becomes much of the **Fixed core**), and name the specific things being refreshed.
3. Route to **`brand-strategy` *focused only on the deltas*** — don't re-run a full from-scratch discovery on a brand that already has equity. Then **`creative-direction`** evolves the system, carrying the fixed parts forward.

### Optimization → capture, audit, fix execution
1. **Capture what exists** (from the assets ingested in Step 1) into `.agents/brand.md` — accurately, as the constraint.
2. **Audit the execution against the sound identity** — where is the good brand being applied poorly? This is the gap.
3. Route **straight to the medium skills** (`web-design`, `collateral-design`, etc.) to fix and expand the application. Little or no new strategy — the brand is the answer, not the question. `brand-strategy` is usually skipped here.

Match effort to depth. Treating a sound brand as a rebuild throws away hard-won equity; treating a broken one as a polish job just refines a bad foundation.

## Step 4: Get or Make `.agents/brand.md`

The document lives at **`.agents/brand.md`**. Check first whether it exists (also `.claude/brand.md` or a legacy `brand-guidelines.md`; offer to move it if found elsewhere). If it exists, read it, summarize, and update only the sections in play.

Otherwise, **get it or make it**:
- **Get it** (a brand already exists) — derive the document directly from the assets you ingested in Step 1. The brand is already out there in the world; your job is to read it accurately and write it down.
- **Make it** (little exists) — the document is an *output* of `brand-strategy` and `creative-direction`. Stub it now and fill it as those skills produce answers.

Either way, draft from the asset inventory (plus `.agents/product-marketing.md` if present), then ask *"What's wrong, and what's missing?"* Prefer concrete specifics (a hex value, a named typeface, a real treatment) over adjectives.

Use the template in [references/brand-doc-template.md](references/brand-doc-template.md). Sections:

1. **Brand at a glance** — name, one-liner, category, and the depth you diagnosed in Step 2
2. **Emotional target** — the few feelings the brand must produce; the rubric everything is judged against
3. **Muses** — each with its *stealable visual cue*
4. **Audience** — who it must feel right *to* (link `.agents/product-marketing.md` rather than duplicating)
5. **Visual system** — color (by role, with ramps + action-color protection), typography (faces by role, weight/style rules), composition, pattern & texture, illustration, iconography, photography — established in `creative-direction`
6. **Logo** — lockups, clear space, minimum size, misuse
7. **Voice** — tone and personality (link `.agents/product-marketing.md` if present)
8. **Fixed core vs. flexible range** — what must **always** hold vs. where the brand is free to flex. In an Evolution this is partly *given* by the equity you're keeping. Without it, no later critique can tell a legitimate flex from a drift.
9. **In use** — examples of correct application
10. **Toolkit** — what the operator can use to produce assets (see below)

### Capture the Toolkit — once

Every downstream skill forks on what the operator can actually generate with, so record it here and no skill has to ask again.

- **Detect what you can see yourself.** Check which generator and canvas MCPs are connected in this session (Flora, Adobe, Figma, Paper…) and whether keys like `QUIVER_API_KEY` are set. Don't ask the operator about things you can check.
- **Ask one plain question about the rest** (skip it if they've already told you) — the tools they run by hand: *"Which image tools do you use yourself — ChatGPT, Gemini, Midjourney, anything else? And do you design in Claude Design, Figma, or anything like that?"* Most people have at least ChatGPT or Gemini; that's a full working tier, not a degraded one.
- **Set the tier** — **0** Claude only · **1** plus a generator they run by hand (the agent writes prompts, they run them and bring results back) · **2** a generator connected to the agent (it generates directly). Record it with the date.

### Where the record lives — with and without a project folder

The `.agents/` documents live in the user's project folder. Any agent working in a folder (Claude Code, Codex, Cursor, a desktop agent with a folder open) writes them there. **In the Claude app** — a chat or a Claude Project — there is no folder you can keep files in, so:

- **Read** the documents from the Project's knowledge (or the conversation's attachments) by their filenames — `brand.md`, `brand-strategy.md`, `design.md` — exactly as if they were in `.agents/`.
- **Hand back the complete updated file** whenever a session changes one, named exactly as it would be in `.agents/`, and tell the user plainly: *"Replace `brand.md` in your Project's knowledge with this one."* Asset folders (the logo files, the imagery library) come back as a zip with the same structure.
- **Never leave the record only in chat history.** A conversation isn't a source of truth; the next one starts blank. Each template carries this rule in its header, so every skill that reads the file inherits it.

## Step 5: Confirm and Save

Show the document, ask what needs adjusting, save to `.agents/brand.md`, and tell the user: *"Other design skills will use this automatically. Run `/brand` anytime to update it."*

## How Other Skills Use This

- `brand-strategy` writes **Emotional target**, **Muses**, **Fixed core vs. flexible range** (Revolution, and the deltas in Evolution)
- `creative-direction` writes the **Visual system** into this doc and produces the full **`.agents/design.md`** creative-direction spec
- `art-direction` writes the distilled **Photography**, **Illustration**, **Iconography**, and **Pattern & Texture** lines (the full specs live in `.agents/design.md`)
- `logo-design` writes the **Logo** section
- The application skills (`web-design`, `collateral-design`, `motion-design`) *read* this and apply it
- **Every skill reads the Toolkit** before picking a tool path, asks only when it's missing or doesn't cover what it needs, and writes back what it learns (a newly connected MCP, a new generator)
- A later critique pass *judges* against the **Emotional target** and the **Fixed-core / Flexible-range** latitude

## Tips

- **Diagnose, don't quiz.** The user describes their situation in plain words; *you* decide the depth and the path. Reflect it back, don't make them choose it.
- **Specifics, not adjectives.** "Confident" is not a spec; "Akzidenz-Grotesk Bold, all-caps, tight tracking, ink-black on bone" is.
- **Record the *why*.** "The action color is the one warm hue in a cool palette, so a button always reads as the one place to go" survives a redesign; a bare hex doesn't.
- **Capture before you change.** An accurate baseline is the whole game — you can't protect equity you haven't written down.
- **Keep it current.** This is a living document; update it whenever a project establishes something new.

## Related Skills

- `design-principles` — the craft beliefs the audit scores against (designed-vs-assembled, coherent-isn't-good, judge-your-own-work-on-the-competitor's-bar)
- `brand-strategy` — the deep generative path this routes *to* for a Revolution / heavy Evolution; supplies the emotional target and muses this records
- `creative-direction` — turns the routed direction into the concrete visual system; its output is scored against this audit's own categories
- `logo-design` — assesses the mark against SAD as part of the diagnosis; this skill gathers the logo in all its forms and the competitor set it's judged against
- `competitor-profiling` — sourced for the confirmed competitor set when there's no `.agents/product-marketing.md` to pull it from
- `design-critique` *(planned — not yet shipped)* — will judge later work against the Emotional Target and the Fixed-core / Flexible-range latitude recorded here. Until it ships, run that judgement yourself against this document.
