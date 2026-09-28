---
name: design-hierarchy
description: Generate UI that has clear visual and information hierarchy. Use whenever
  emitting UI code that displays data (dashboards, CRM/lead cards, tables, lists,
  detail views) or general product UI. Prevents flat rows of undifferentiated
  elements, bare unlabeled metrics, undefined scores, competing encodings, and
  inconsistent vocabulary.
---

# Visual & Information Hierarchy — Skill

You tend to converge toward generic, "on distribution" outputs: flat rows of chips,
every element the same weight, bare numbers, mystery scores, and decorative dots.
Do not do this. Follow the rules below and run the self-review checklist before
emitting any UI code.

## CORE PRINCIPLE
Emphasizing everything emphasizes nothing. Every screen must have a deliberate
hierarchy: exactly one primary element, then secondary, then tertiary. If you
cannot say which element is primary, the design has failed.

## DECISION PROCEDURE (run in order, before writing markup)

1. STATE THE JOB. Write one sentence: "The user looks at this to <decide/answer X>."
   If you can't, stop and ask. Every element must earn its place by serving that job.

2. RANK EVERY FIELD into exactly three tiers:
   - PRIMARY (1 per card/row): the thing the user scans for (usually the entity name).
   - SECONDARY (2-4 items): needed to act or disambiguate.
   - TERTIARY (the rest): provenance, timestamps, meta — de-emphasized or hidden
     behind progressive disclosure.
   If more than ~4 fields feel "primary," you have not ranked; force the choice.

3. FOR EACH VALUE, make it self-describing: label + value + unit + referent.
   A number with no referent is a bug. "4h" is forbidden; "Last contacted 4h ago"
   is required.

4. FOR EACH DERIVED/MODEL SCORE (confidence, fit, health, etc.):
   - Show the scale inline (e.g., "82/100" or "High").
   - Give a one-line definition on hover/tooltip: what it measures + inputs + as-of date.
   - Never show a bare number or bare word with no scale.
   - If you can't define it, do not render it.

5. CHOOSE ENCODINGS: one visual variable per data variable. Never show the same
   datum two ways (dots AND a bar) in one view. Every glyph system (dots, pips,
   chips, colored bars) needs a legend or inline label, or it is deleted.

6. GROUP with whitespace and common region (proximity), not a forest of borders
   and dividers. Related fields sit close; unrelated groups get more space.

7. PICK THE CONTAINER: if the user compares many records across the same fields,
   use a TABLE with aligned columns (right-align numbers). Use a CARD GRID only
   when each item is scanned individually and has heterogeneous content.

8. SUBTRACT: remove elements one at a time until removing one more breaks the job.
   Ship that version.

## HARD RULES (checkable)

- HIERARCHY VIA WEIGHT/COLOR FIRST, SIZE LAST. Establish tiers with font-weight and
  text color/contrast before reaching for larger font sizes. Use at most ~3 text
  colors: near-black (primary), medium gray (secondary), light gray (tertiary).
- CONTRAST TIERS: primary text full contrast; secondary ~#374151 / 70-80% weight;
  tertiary ~#6b7280–#9ca3af. Push the gap wide enough to see; do not set body #333
  and captions #555.
- NEVER grey text on a colored background. To de-emphasize on color, pick the same
  hue and lower saturation/lightness toward the background — do not just lighten to grey.
- TWO FONT WEIGHTS are usually enough (e.g., 400/600). No weights under 400 for UI text.
- DE-EMPHASIZE TO EMPHASIZE. If the primary element doesn't pop, dim the competitors
  rather than enlarging the primary.
- COMBINE LABEL + VALUE into one unit when possible ("12 left in stock", "3 bedrooms",
  "Last contact 4h ago"), not "Label: value". When you must keep a label (scannable
  dense data), make the label the tertiary/supporting element, not co-equal.
- ONE ENCODING PER VARIABLE. Color means one thing per view. If color = status,
  it cannot also = category elsewhere in the same view.
- LEGEND OR DEATH. Any non-textual mark (dot, pip, ring, mini-bar, colored chip)
  must be explained by a visible legend, an inline label, or a tooltip. Unlabeled
  decorative glyphs are deleted.
- CONSISTENT SCHEMA. For a given entity type, define a FIXED ordered set of fields
  and FIXED labels. Never let the label vary between instances (not "Job ads" on one
  card and "Crunchbase" on another for the same slot — that slot is "Source", and its
  VALUE varies, not its label).
- SPARE COLOR FOR MEANING. Neutral/gray by default; reserve saturated color for the
  one thing that needs attention (alert, primary action, the outlier).
- RIGHT-ALIGN NUMBERS in tables/columns so digits line up for comparison.
- NO EXCESSIVE PRECISION. Round to the precision the decision needs ($3.8M, not
  $3,848,305.93; "4h ago", not "4h 12m 7s ago").
- PROVIDE CONTEXT FOR MEASURES. A lone number ("$736,502") needs a comparison
  (target, prior period, or qualitative state) or it means nothing.
- TOUCH TARGETS: interactive controls stay ≥ 24×24 CSS px (WCAG 2.2 minimum floor);
  prefer ≥ 44–48px even in dense rows by extending the hit area beyond the visual mark.

## WORKED EXAMPLE — CRM company/lead card

### BAD (what to never emit)
```html
<div class="card">
  <div class="row">acme.com · San Francisco · ●●●● · confidence · ▮▮▮▯▯</div>
  <div class="row">headquarters · listing · ●●●● · job ads · 4 hours</div>
</div>
```
Why it fails: no primary element; "acme.com" (secondary) leads instead of the company
name; "●●●●" and "▮▮▮▯▯" are two undefined encodings for possibly the same thing;
"confidence" has no scale or definition; "4 hours" has no referent; "job ads" is a
value sitting where another card puts "Crunchbase," implying the label changes;
everything is the same weight/size/color in one undifferentiated line.

### GOOD (target output)
```html
<article class="card" aria-label="Acme Inc lead">
  <!-- PRIMARY -->
  <header>
    <h3 class="name">Acme Inc</h3>
    <a class="domain" href="https://acme.com">acme.com</a>
  </header>

  <!-- SECONDARY: fixed schema, self-describing values -->
  <dl class="facts">
    <div><dt>HQ</dt><dd>San Francisco, CA</dd></div>
    <div><dt>Funding</dt><dd>Series B · $45M</dd></div>
    <div>
      <dt>Data confidence</dt>
      <dd>
        <span class="score">82<span class="scale">/100</span></span>
        <button class="info" aria-label="How confidence is calculated"
          title="Likelihood this record is accurate and current. Based on number of
          corroborating sources, email validation, and recency. As of Jul 24, 2026.">ⓘ</button>
      </dd>
    </div>
  </dl>

  <!-- TERTIARY: provenance + recency, de-emphasized -->
  <footer class="meta">
    <span>Last contacted 4h ago</span>
    <span aria-label="Sources">Verified by 2 sources · Crunchbase, job postings</span>
  </footer>
</article>
```
Why it works: the company NAME is primary (largest weight); domain is secondary link;
each fact is a fixed labeled slot with a self-describing value; "Data confidence"
shows its scale (/100) and a hover definition with inputs + as-of date; the single
provenance line replaces the mystery dots with a defined "Verified by N sources"
plus the named sources as the VALUE of a fixed "Sources" slot; timestamps are
tertiary meta. One encoding per variable; no unlabeled glyphs.

## SELF-REVIEW CHECKLIST (run before emitting; all must pass)
[ ] I can name the ONE primary element per card/row.
[ ] There are at most 3 emphasis levels, created by weight/color before size.
[ ] Every displayed value has label + value + unit + referent (no bare numbers).
[ ] Every derived score shows its scale AND has an inline/tooltip definition with
    inputs and as-of date.
[ ] No datum is shown via two different encodings in the same view.
[ ] Every glyph/dot/bar/chip has a legend, inline label, or tooltip — else removed.
[ ] Field labels are identical across all instances of this entity type (fixed schema);
    only values vary.
[ ] Color is neutral by default; saturated color used only for meaning.
[ ] Groups are formed by whitespace/common region, not a maze of dividers.
[ ] Numbers are right-aligned in columns; precision matches the decision.
[ ] If comparing many records on the same fields → I used a table, not a card grid.
[ ] I removed every element that does not serve the stated user job.
[ ] SQUINT TEST: blurring the screen, the hierarchy is still legible.
[ ] COVER-THE-LABELS TEST: values are still interpretable from format/context.
[ ] 5-SECOND TEST: a new user can state what the screen is for and where to look first.
