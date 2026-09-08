---
name: pptx-rich
description: "Use this skill any time a .pptx file is involved — as input, output, or both. Covers creation, editing, template-based decks, content extraction, design guidance, anti-monotony rules, and QA. Trigger whenever the user mentions \"deck\", \"slides\", \"presentation\", \"pptx\", \"PowerPoint\", or asks to read/build/edit/inspect a .pptx file. Runs locally on Windows using Microsoft PowerPoint (COM) for rendering and QA; does NOT depend on LibreOffice/OpenOffice."
---

# PPTX Rich Skill

A local PowerPoint skill that produces **professional decks with controlled variation**, so the output doesn't look like the same AI-generated template every time. Patterns are available (and recommended for corporate decks), but they're applied **with intention** instead of being the default for everything.

This skill replaces LibreOffice-based rendering with **Microsoft PowerPoint COM automation** for PDF/PNG export and visual QA.

---

## Quick Reference

| Task | Guide |
|------|-------|
| Read/extract content from a .pptx | `python -m markitdown deck.pptx` (text) + `python scripts\office\thumbnail.py deck.pptx` (visuals) |
| Create a new deck from scratch | Read [guides/creating.md](guides/creating.md) |
| Edit / build from a template | Read [guides/editing.md](guides/editing.md) |
| Pick a design direction | Read [guides/design.md](guides/design.md) (catalog: `themes\`) |
| Avoid the "AI-clone deck" look | Read [guides/anti-monotony.md](guides/anti-monotony.md) |
| Build an Azure architecture diagram | Read [guides/azure-architecture.md](guides/azure-architecture.md) |
| Run QA (content + visual via PowerPoint) | Read [guides/qa.md](guides/qa.md) |
| Render PPTX → PDF/PNG via PowerPoint | Read [guides/powerpoint-com.md](guides/powerpoint-com.md) |
| Build a full deck from a recipe | Use `recipes\families\<family>\build.js` (see [recipes README](recipes/README.md)) |

---

## Setup (run once)

```powershell
pip install pywin32 "markitdown[pptx]" Pillow defusedxml
npm install
```

This installs `pptxgenjs`, `lucide` (icon library), and `sharp` (SVG → PNG rasterizer for the icon system).

Microsoft PowerPoint desktop must be installed (any modern version). Then validate the environment:

```powershell
python scripts\office\powerpoint.py check-env
```

If `powerpoint_com` is `OK`, you're ready.

---

## End-to-End Workflow

Use this loop for any non-trivial deck:

1. **Decide intent and profile** (see [anti-monotony.md](guides/anti-monotony.md)):
   - `conservative` — board, investor, compliance, regulated industries
   - `balanced` — default internal/external decks
   - `creative` — launch, marketing, keynote
2. **Pick a theme** from `themes\` (see [themes README](themes/README.md)):
   - `microsoft-azure`, `microsoft-fabric`, `microsoft-collaboration`, `microsoft-architecture` — Microsoft-derived
   - `mckinsey`, `deloitte`, `ir-classic` — consulting/finance
   - `premium-keynote`, `modern-saas` — launch/SaaS
3. **Pick a recipe** family from `recipes\families\` or compose individual layouts from `recipes\layouts\`. The same content + recipe + different theme produces visually distinct decks.
4. **Plan style** deterministically when *not* using a family:
   ```powershell
   python scripts\style\style_planner.py plan --profile balanced --slides 12 --seed 42 --out style-plan.json
   ```
5. **Generate the deck**:
   - Family build: `node recipes\families\pitch-deck\build.js --theme microsoft-azure --out deck.pptx`
   - From scratch → [guides/creating.md](guides/creating.md) (PptxGenJS).
   - From a template → [guides/editing.md](guides/editing.md) (unpack/edit XML/pack).
6. **Validate layout** (catches overflow/overlap before render):
   ```powershell
   python scripts\validate\validate_layout.py --input deck.pptx
   ```
7. **Run QA** (content + visual):
   ```powershell
   python scripts\qa\run_qa.py --input deck.pptx --out-dir qa-out --profile balanced --seed 42 --render
   ```
   This produces `qa-out\qa-report.json`, a `qa-out\render\deck.pdf`, and per-slide PNGs.
8. **Inspect visually** (use a fresh-eyes sub-agent if available — see [guides/qa.md](guides/qa.md)).
9. **Fix → re-render → re-inspect**. Never declare done after a single render.

> **Note on script paths.** All paths above are **relative to the root of this skill folder** (where `SKILL.md` lives). If you cd elsewhere, prefix them with the skill root.

---

## Design Principles (the short version)

These are deliberately opinionated. For depth, read [guides/design.md](guides/design.md) and [guides/anti-monotony.md](guides/anti-monotony.md).

### Do
- **Pick a content-informed palette.** Colors should feel chosen for *this* topic. If the same palette would work on a totally unrelated deck, it's too generic.
- **Commit to a visual motif** (icon-in-circle, side stripe, cutout photo, gradient orb, stat callouts) and repeat it with variation.
- **Use dominance, not equality.** One color ~60% weight; one supporting tone; one sharp accent.
- **Vary layout rhythm.** Mix titles, two-column, KPI rows, image-quote, timeline, cards, comparison.
- **Add a visual element on every slide** (image, icon, chart, shape). Text-only slides are forgettable.
  - Icons are now auto-rendered on `kpi-row`, `three-cards`, `stat-callout`, `process-flow`, and `agenda`. Override with `icon: "rocket"` (Lucide name) or `icon: "azure:cosmos-db"` (Azure service); pass `icon: null` to suppress.
- **Bold all titles, section headers, and inline labels.** Use real weight (700+), not faux bold.
- **For technical / solution decks**, use the `azure-architecture` layout to draw architecture diagrams with official Microsoft Azure icons in the Microsoft Learn style (see [guides/azure-architecture.md](guides/azure-architecture.md)).

### Don't
- **Don't repeat the same layout** more than the profile allows (`max_repeat_layout` in `style_profiles.json`).
- **Don't default to blue.** Pick colors that match the topic, not the toolkit default.
- **Don't add a thin accent line under every title.** That's the #1 AI-deck tell.
- **Don't make every slide a 2×2 card grid.** Another AI tell.
- **Don't center body text or paragraphs.** Center only titles.
- **Don't use Unicode bullets (•).** Use real bullet formatting.
- **Don't use 8-character hex with opacity (`"00000020"`).** Use the `opacity` property. PptxGenJS treats 8-char hex as a corrupt file signal.
- **Don't reuse PptxGenJS option objects across calls** — PptxGenJS mutates them in place.

---

## Scripts (overview)

All scripts are Windows-native and use PowerPoint (not LibreOffice).

| Script | Purpose |
|--------|---------|
| `scripts\office\powerpoint.py` | Preflight + render PPTX → PDF/PNG via PowerPoint COM |
| `scripts\office\thumbnail.py` | Generate a thumbnail grid (PNG) for template analysis |
| `scripts\office\unpack.py` | Extract a `.pptx` into a working folder (pretty-printed XML) |
| `scripts\office\pack.py` | Repack a working folder into a valid `.pptx` |
| `scripts\office\add_slide.py` | Duplicate a slide or instantiate a layout (handles `Content_Types.xml`, rels, notes refs) |
| `scripts\office\clean.py` | Remove orphaned slides, media, rels |
| `scripts\style\style_planner.py` | Deterministic style planning (palette/font/motif/layout sequence) |
| `scripts\style\style_profiles.json` | Profile definitions (conservative/balanced/creative) |
| `scripts\style\palettes.json` | Extended palette catalog (extra material for the planner) |
| `scripts\style\motifs.json` | Motif catalog (icon-in-circle, side stripe, etc.) |
| `scripts\qa\run_qa.py` | Content + render QA, writes `qa-report.json` |
| `scripts\validate\validate_layout.py` | Pre-render geometry validator (overflow/overlap, severity tiers) |
| `scripts\azure\download_icons.ps1` | Refresh the bundled Azure icon set from the official V21 zip |
| `recipes\lib\style_apply.js` | Theme → PptxGenJS helpers (titles, stats, cards, motifs, icons) |
| `recipes\lib\pptx_factory.js` | `createPresentation({themePath, ...})` boilerplate |
| `recipes\lib\icon_render.js` | Async Lucide + Azure SVG → PNG (cached, base64 data URLs) |
| `recipes\lib\icon_keywords.js` | Keyword-based auto-icon inference for KPIs, cards, steps, agenda items |
| `recipes\layouts\*.js` | 14 single-slide layout recipes (title-message, agenda, kpi-row, timeline, comparison, image-quote, chart-focus, process-flow, stat-callout, split-hero, three-cards, two-column, summary, azure-architecture) |
| `recipes\families\*\build.js` | 9 multi-slide deck builders (pitch-deck, product-keynote, case-study, roadmap, conference-talk, all-hands, tech-deep-dive, finance, azure-solution) |
| `themes\*.json` | 9 named theme JSONs (Microsoft Azure/Fabric/Collaboration/Architecture, McKinsey, Deloitte, IR Classic, Premium Keynote, Modern SaaS) |
| `assets\azure-icons\` | 95 official Microsoft Azure service SVGs + manifest + license |

---

## QA Loop (required)

**Assume there are problems. Your job is to find them.** First render is almost never correct.

1. Generate slides → run `run_qa.py --render`.
2. Inspect `qa-out\render\slides\slide-*.png` (use a sub-agent with fresh eyes if available).
3. Look for: overflow, overlap, low contrast, cramped spacing, leftover placeholders, monotonous layout sequence.
4. Fix → re-render the affected slides:
   ```powershell
   python scripts\office\powerpoint.py render --input deck.pptx --out-dir qa-out\render --png --slides 3,5-7
   ```
5. Re-verify. Repeat until a full pass surfaces no new issues.

Detailed prompts and checklists: [guides/qa.md](guides/qa.md).

---

## Anti-Monotony In One Paragraph

The skill defends against the "AI deck smell" with three mechanisms:

1. **Profile-driven variation rules** — `max_repeat_layout`, `pattern_weight`, and motif selection vary by profile.
2. **Seed-based determinism with re-roll on monotony** — the planner refuses to emit the same layout more times than allowed in a row.
3. **Explicit anti-patterns** — title-underline rules, identical openings, 2×2 grid overuse, and bullet-only slides are flagged.

Full rationale: [guides/anti-monotony.md](guides/anti-monotony.md).

---

## When NOT To Use This Skill

- If you don't have Microsoft PowerPoint installed on Windows, the render/QA pipeline won't run. Either install PowerPoint or fall back to a LibreOffice-based skill.
- If the user wants `.key` (Keynote) or `.odp` output, use a different tool.
- If the user wants a static HTML deck (Reveal.js), use a different tool.
