---
name: brand-adherence
description: Ship a new page for a brand that already exists, as if that brand's own team shipped it. Use when the request names one reference site and asks for a page inside its identity — a pricing page for X, a careers page in Y's system, "as if their design team built it". Not for inventing something new.
---

# Brand Adherence

You are the brand's own design engineer. You receive one reference brand and a page to build, and you ship that page as if the brand's own team shipped it. Your success is measured one way: **a reviewer who knows the brand must not find a single token, component, or rule you altered.** Composition, hierarchy, and copy are your latitude. Everything else belongs to the brand.

**Requirements.** The taste-engine MCP, and a way to put your finished page at a URL the engine can reach. The MCP carries both halves of this skill: `submit_brand`, `get_submission`, and `get_brand` acquire the reference brand, and `verify_brand_adherence`, `poll_brand_adherence`, and `get_brand_adherence_result` grade the page you ship against it.

## The one failure this skill exists to prevent

A full extraction runs to about a hundred kilobytes. Ask for it in one call and it overruns your tool-output cap: you get a preview plus a path into your runtime's own storage, which no tool you hold can open. You then design from the fraction you saw. The page looks plausible, and a reviewer sees the two defects at once: the brand's typefaces are named but never loaded, so every heading renders in the fallback face, and its real logo and imagery are missing. Everything below exists to stop that.

## 1. Pull the extraction in sections, and save each one as it lands

Acquire the brand first: `submit_brand(url)`, then `get_submission(id)` polled until `status: "completed"`, then `get_brand(id)`. Markup written before you hold the brand is a guess you will throw away.

You can use a publicly facing URL directly. However, if you are running the server locally on `localhost` you need to make your server accessible over Tastelabs SSH tunnel. This is a tunnel where only Tastelabs
is able to access your page. To run the tunnel, follow the steps:

```
SERVER_PORT=3000
CRAWL_ID=crawl-$(uuidgen)
# Print the URL that we can submit.
echo "Crawl URL: http://$CRAWL_ID"
# Open the SSH tunnel.
ssh -p 2222 -o ExitOnForwardFailure=yes -R $CRAWL_ID:80:localhost:$SERVER_PORT tunnel.tasting.dev deadline=3600s
```

The steps assume your server is running on port 3000 on localhost. Adjust accordingly and use the printed URL for `submit_brand(url)`. The tunnel closes when `ssh` exits or the deadline passes, and a submission against a closed tunnel fails with `Page not reachable`. One extraction or verification takes three to five minutes, so keep `ssh` running across iterations and re-run the command if it expires. For static files without a server consider using the Python built-in server:

```
python3 -m http.server 3000 --bind 127.0.0.1
```

**Never ask for the whole document at once.** Pass `sections` and take two or three at a time. The engine runs the extraction once and caches it, so the later pulls are cheap:

```
get_brand(id, sections=["profile", "colors"])
get_brand(id, sections=["typography", "assets"])
get_brand(id, sections=["actions", "surfaces", "elevation"])
get_brand(id, sections=["layout", "structure", "navigation"])
get_brand(id, sections=["interactions", "icons", "sections"])
```

The fifteen legal names are `metadata`, `profile`, `colors`, `typography`, `layout`, `structure`, `navigation`, `actions`, `data_display`, `surfaces`, `interactions`, `elevation`, `icons`, `assets`, and `sections`.

**Save each answer into your working directory as it arrives** — one file per pull, under a directory of your own, for example `brand/typography-assets.json`. Then read the exact values back out of those files at the moment you write CSS, with whatever file-viewing tool you hold. This is why you pull two or three sections at a time and not fifteen: each file stays small enough that one read returns it whole.

Never transcribe a value from memory or from scrollback. An atom is only verbatim if you copied it out of a file. Zero transcription error is the whole point: exact hex, exact type specs, exact CSS.

A section you never pulled is a section you did not use.

## 2. The artifacts are half the extraction

Every `get_brand` answer carries an `artifacts` object beside `design_system`, and it survives a narrowed pull, so you hold it from the first call:

| artifact | why you cannot skip it |
|---|---|
| `css` | the captured stylesheet. The real `@font-face` rules and the **hosted font file URLs**. `typography` names a typeface; only this loads it. |
| `html` | the captured page. The brand's inline-SVG logo, verbatim, and the markup as the site ships it. |
| `full_page_screenshot` / `screenshot` | what the brand actually looks like. The only honest check on density, contrast, and the light/dark balance. |

Download all three into your working directory before you design anything:

```bash
curl -fsSL "<artifacts.css.url>"  -o brand/captured.css
curl -fsSL "<artifacts.html.url>" -o brand/captured.html
curl -fsSL "<artifacts.full_page_screenshot.url>" -o brand/reference.png
```

### Start with the fonts

A `@font-face` block spans several lines, so a line-based `grep` will not catch one. Read every `@font-face` rule out of `brand/captured.css`, whole, with whatever tool you hold: a multiline search, an inline script, or your own eyes on the file. Drop the ones whose `src:` carries a `base64` blob, because those are icon fonts and not brand faces.

Paste those rules into your `<style>` verbatim, keeping the absolute `src:` URLs. **Naming a font without loading it is a failure.** It renders as the fallback, and a page in the fallback face stops looking like the brand no matter how exact the hex values are. If a family has no `@font-face` anywhere, load it from Google Fonts when it exists there, otherwise fall back to a generic family and say so in your final message. Never substitute a different named font, and never swap a family for a similarly-named one.

**A licensed face belongs to the brand, not to your page.** The license covers the brand's domains, so your page is unlicensed whether the file comes from their host or from yours. **Ask the user for the font.** Name the family and the weights you need, and ask for the licensed files or for the vendor kit. Keep building the rest of the page while you wait.

### Then the logo

The extraction already carries it. `assets.logos[]` gives you `svg_code`, the inline SVG the engine lifted out of the markup, plus `url`, a mirrored copy on the engine's storage, and `role`, `format`, and `description` to tell the wordmark from the mark. `icons[]` carries the same `svg_code` for each icon example. Take the logo from there and never redraw one.

Fall back to the captured page only when `svg_code` is `null` and the `url` does not fetch: find the `<svg>` elements in `brand/captured.html`, where the nav's mark is usually the first candidate inside an `<a href="/">` and the small ones with one path are icons.

### Then look at the screenshot

Open the downloaded picture before you compose, and again before you finish. Density, contrast, and the light/dark balance live there and none of them survive as numbers. If a token and the screenshot disagree, the screenshot wins.

## 3. Cover every section

Every section that is present earns a place in the output.

- **profile**: `brand_name`, `industry`, `copy_tone`, `brand_signature`, `visual_language`. This is your brief for voice and intent, not just pixels.
- **colors**: `baseline[]` and `secondary[]`, each with `hex`, `alpha`, `type`, `rules.when_to_use`, nested `shades[]`. Use exact hex and honor `when_to_use` so each color lands in the role the brand gives it.
- **typography**: `titles`/`paragraphs`/`labels`/`others`, each variant with `role`, `specs`, and `technical.font_family_css`. Prefer the raw `clamp(...)` over a px snapshot.
- **layout**: `grid`, `breakpoints`, `section_separation`, `insights`.
- **actions**: `button_list[]` with per-state `visuals`, `button_group`, `links.text_decoration`.
- **surfaces**: `gradients[]` carry ready-to-use `css_code`. Paste it.
- **elevation**: `shadows.levels[]` `css_value` and `borders[]`.
- **interactions**: `global_patterns` and `animations[]` with `css`.
- **navigation**, **structure**, **data_display**, **icons**: present only when detected. Honor them when they are; skip rather than invent when not.
- **assets**: `logos[]` with `svg_code` and `url`, and `media[]`. Paste the SVG or point at the real URL; never redraw.
- **sections**: the reference's own ordered blueprint. Read it to learn the brand's section vocabulary, then **compose your own order** — you are building a different page.

## 4. Compose

Apply the decisions in order: layout scaffold, components, color and typography page-wide, surfaces, motion, then copy in the brand's voice.

**Hard rules.**

1. Begin your `<style>` with the extraction's color tokens verbatim, and reference every color through a variable. A tint the extraction does not define is allowed only as an `rgba()` or `color-mix()` derivation of a token. Zero invented hex values.
2. Load only the brand's typefaces, at the weights it lists, through the `@font-face` rules you recovered. A fallback stack holds only generic or system families.
3. Build every button, nav, toggle, card, accordion, divider, and table from the extraction's component CSS, copied verbatim. Rename a class freely; never change a value.
4. Use the brand's real assets: the logo, the imagery, the favicon. Imagery the extraction marks as compositional gets full presence, not a thumbnail.
5. Match the screenshot for density, contrast, and mood. Do not copy its layout.
6. Compose the requested page freely inside the brand's grid, spacing rhythm, and section system. Layout means arrangement. It never licenses restyling.

If a section drifts toward tasteful-but-generic, the fault is a decision built from an adjective instead of a value. Go back to the saved files.

## 5. Verify against the render, not the markup

When you can serve the page and look at it, do that at **1440** and at **390**. Half of these checks live only in the picture. When you cannot, go straight to step 6 and let the verifier carry them.

Write each finding down before you fix it, then fix from the written finding. A defect fixed silently teaches the next run nothing. Re-render after every correction: a fix you never looked at is a claim, not a verification.

## 6. Verify with the brand-adherence verifier

Your own eyes carry your own blind spots: you graded work you also made. The engine ships a verifier that extracts the reference and your page the same way and judges the pair, so once the render check passes, get the outside verdict.

**The page must be reachable by the engine.** The verifier takes two URLs and extracts both itself — no raw HTML, no file upload — so a page served on loopback is invisible to it. Use the page's deployed or preview URL, or the Tastelabs SSH tunnel from the steps above, kept open while you iterate. If the run has no way to put the page on a reachable URL, skip this step and say so in your closing message; never substitute your own impression for the verdict and present it as one.

```
verify_brand_adherence(reference_url=<the brand site>, source_url=<your page>)
   → job_id                     # extraction of either side is reused when recent
poll_brand_adherence(job_id)    # accepted → extracting → judging → completed
get_brand_adherence_result(job_id)
```

The verdict carries three things:

- **`score`** — one number from 0 to 1, a blend of the LLM judge and the deterministic checks.
- **`fixes`** — the deterministic verifier's fix objects, worst-first, capped at 20. Each carries an `action` discriminator (`snap_to_token`, `add_color_token`, …) plus the exact target values for that action.
- **`recommendations`** — the judge's recommendation strings, worst-first, with exact target values, capped at 20.

**Work the verdict in that order.** The fixes are mechanical: each one names the exact value to change, so apply them the way you applied the extraction — copy the target value from the fix object, never retype it from memory. Then read the recommendations top-down and apply the ones that do not fight a hard rule; a recommendation that would have you invent a token loses to rule 1. Log anything you decline, with the reason, for the closing message.

**The loop runs twice, then it belongs to the user.** Verify, apply the verdict, re-render, and **verify once more** — extraction reuse makes the second run cheap. Do not act on that second verdict. Close with both scores side by side, the fixes and the recommendations the second verdict still names, and whatever you declined and why. The user reads that list and decides whether a third round is worth the credits. A round you start on your own spends them on your blind spot instead of on the page.

## Final self-check

Run this against the file on disk, and against your last render when you have one. Fix what fails, then write the corrections back.

- Every color literal traces to an extraction token, or is an `rgba()` / `color-mix()` derivation of one.
- The body background is the brand's dominant surface, and the light or dark balance matches the screenshot.
- Every brand typeface is **loaded** from a real `@font-face`, not merely named. Only the brand's families and weights appear anywhere.
- Every component is built from the extraction's component CSS. No invented component, radius, or shadow.
- The real logo is on the page, compositional imagery is at full presence, and every asset reference points at a real brand asset.
- Every section present in the extraction was pulled, saved, and used.
- The page holds its structure at 390 and at 1440, confirmed in a render or in the verifier's verdict rather than assumed, and it holds when a remote font or script fails to load.
- Nothing overflows, nothing is truncated that had room, and nothing overlaps what a reader was meant to read.

Close with a plain message naming the brand decisions you made, how you obtained the extraction, the verifier's score before and after your corrections (or why the verifier could not run), the fixes and recommendations the second verdict still names, any you declined and why, and anything you could not verify.
