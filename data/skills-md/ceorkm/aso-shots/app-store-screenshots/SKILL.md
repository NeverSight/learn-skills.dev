---
name: app-store-screenshots
description: Turn an app's raw screenshots into high-converting App Store (and Google Play) screenshot sets. Use when the user wants App Store screenshots, store listing images, screenshot designs or mockups for an app, or wants to recreate a screenshot style they like. Writes the copy, offers 3 style directions, generates assets with AI (Codex or an image API), builds the set in HTML and exports store-ready PNGs.
---

# App Store Screenshots

Make store screenshots that get installs. **The words come first, the design second.** Every set is built in HTML/CSS/JS, checked side by side, and exported at store size.

Files in this skill:
- `copywriting.md`: what to write on each screenshot (read before Step 3)
- `STYLES.md` + `styles/NN-*/design.md`: the 18 proven styles
- `assets.md`: how to get images (AI generation first) and how to use them
- `build.md`: technical recipes (frames, tilted phones, text fitting, 3D, glass, export)

---

## Step 0: Image generation setup (once per session)

Organic assets (hands holding phones, people, mascots, fur, food, products, scenery) are generated with AI. Find a provider in this order:

1. **Codex plugin** (uses the user's ChatGPT plan; Codex generates images with GPT Image). If the `codex:codex-rescue` subagent or `/codex:rescue` exists, use it (see `assets.md`). If it's missing, tell the user how to install it:
   ```
   /plugin marketplace add openai/codex-plugin-cc
   /plugin install codex@openai-codex
   /codex:setup
   ```
2. **API key.** Check for `OPENAI_API_KEY` or `GEMINI_API_KEY`. If neither is set, ask the user for one. Current models (Oct 2026):
   - OpenAI **`gpt-image-2.5-flare`** (fast, everyday) and **`gpt-image-2.5-sunburst`** (most precise; use it for edits with reference images). Real transparent PNG output.
   - Google **`gemini-nano-banana-2.1`** (Nano Banana 2.1). Up to 14 reference images, 1K/2K/4K. No transparent output: generate on green, then key it out.
   - Model IDs change often. Before generating, check the provider's model list and use the newest image model.
3. **Free stock photos.** Only if the user asks for stock, or has no generator.

Say in one line which provider will be used.

---

## Step 1: Intake

Ask in one message (skip anything already given):

1. **Screenshots of your app** (required): the main screens, as images.
2. **What the app does and who it's for**, in 1–2 sentences.
3. **Inspiration** (optional): a screenshot set you like.
4. **Proof you have** (optional): star rating and review count, number of users, press coverage, awards.
5. **Logos to show** (optional): press that covered you, apps you connect with, partners.
6. **Brand**: colours, font and logo (or "use what's in the app").
7. **How many screenshots** (default 6), **stores** (App Store / Google Play / both) and **languages**.

---

## Step 2: Understand the app

Study the screenshots and list:
- the core promise (the one outcome users want);
- the 3–6 strongest features, as benefits;
- the most impressive screen (it becomes the hero);
- the category and audience (they guide the style choice).

---

## Step 3: Storyboard (copy). Get it approved before designing.

Follow `copywriting.md`. Show the user a table, one row per screenshot: job, headline, small line, app screen shown, extra visual, proof.

- Screenshot 1 hooks, 2 explains, 3 proves (or gives a second benefit), then one benefit each, and the last builds trust.
- Use only real numbers from the user.

Wait for approval or edits.

---

## Step 4: Pick the style

- **Inspiration given:** extract its design system the way the `styles/*/design.md` files were made: measure the panels, sample the colours, identify the fonts, describe the layout and decoration. Apply that style to the user's app and copy. Don't copy the inspiration's content.
- **No inspiration:** choose the 3 best-fitting styles from `STYLES.md` for the category, audience and brand colours. Pick 3 that differ clearly from each other, including in **what the hero is**: a phone is only one option. Most styles open with no phone (a big headline with an object, a person, or UI cards pulled out of the app).
- **Fit the brand.** Use a mascot or character only if the app already has one, or the user asks for one. Use people only if the app is about people.

---

## Step 5: Three directions, screenshot 1 only

Build **only screenshot 1** in each of the 3 directions, at preview quality, and show them side by side in one page. The user picks one, or mixes ("B with A's colours"). Never build 3 full sets.

---

## Step 6: Assets

Follow `assets.md`:
- **The app's screens:** a phone frame is optional; most top sets show the UI full-frame. If the user's screenshots look rough or dated, **redraw the UI cleanly in HTML/CSS** (same features, same flows, fictional sample data) instead of pasting the old images. Redrawing replaces only the screen content: the screenshot around it still follows the chosen `design.md` (layout, type, frames, decoration). Never copy the old screenshots' visual style.
- **AI-generated:** hands, people, mascots and characters, products, food and scenery. Ask for a transparent background, or a flat chroma colour that you key out.
- **Hand-held phones:** generate with a flat green screen, then map the real screen onto it from its 4 corners.
- **Mascots:** generate once, then reuse that image as the reference for every other pose.
- **Code:** text, cards, pills, glass, doodles, icons, and simple 3D (coins, gems, logo marks).

---

## Step 7: Build the full set

Follow `build.md` and the chosen `design.md`:
- one HTML page; each screenshot is a panel at the style's geometry;
- headlines are placed per line and per word, using the measured widths;
- the real app screens go inside the frames;
- AI assets are placed and checked against the storyboard.

---

## Step 8: Check, then export

- Run the chosen style's fidelity checklist and the copy checklist (`copywriting.md` §9).
- Look at every screenshot at thumbnail size (about 230 px wide): is the headline readable, and is the hero clear?
- Export with `scripts/export.js` (official sizes in `build.md` → Export):
  - **App Store:** `ios-6.9` (1320 × 2868) and `ios-6.3` (1206 × 2622, the **required** size class); `ipad-13` (2064 × 2752) if the app runs on iPad. 1–10 screenshots per size, PNG/JPEG, **no alpha channel**.
  - **Google Play:** `play-phone` (1080 × 1920, 9:16), 2–8 screenshots per device type, **no alpha**, plus **alt text** (140 characters or less) per screenshot, the 1024 × 500 **feature graphic**, and tablet sets (`play-tablet`, at least 4) if the app supports tablets. Build Play as its own 9:16 layout, Play-safe (`copywriting.md` §7).
- Deliver a preview page showing all screenshots in a row, plus a folder per size of files named `01.png`, `02.png`, …, and a `alt-text.txt` for Play.

---

## Step 9: Revise

Change what the user asks for. Keep the copy, style and assets consistent across the set. Re-export after every change.

---

## Rules

- **Copy before design.** Never design an unapproved storyboard.
- **Real proof only.** Never invent ratings, reviews, user counts or press.
- **Generated people and objects must match what the storyboard describes** (pose, clothing, colours). Regenerate rather than settle.
- **3D only for things that are 3D.** Flat things stay flat.
- **Never invent a mascot** for an app that doesn't have one.
- **Keep the brand colour.** The palette comes from the app's brand (icon, main accent), not from the chosen style; take only the style's layout, type and decoration.
- **Pick the frame that makes sense, per screenshot:** no frame (UI cards on their own), a **soft frame** (rounded screen, soft light bezel, gentle shadow; no metal or buttons), or a realistic phone (real frame PNG; only when the shot needs a physical device, such as a hand-held or tilted hero). Never a realistic phone by default, and never a badly hand-drawn "realistic" phone.
- **Every app gets its own type voice.** When building several apps, never reuse another app's headline font or accent device (underline swash, highlighter, sticker) through a shared helper. Pick the font pairing and the accent mark per app, from its brand and style.
- **Use a style's DNA, not a fixed layout.** From a `design.md`, take the palette logic, type pairing, panel treatment, decoration vocabulary and device treatment. Invent a new composition for the user's app every time.
- **A style is its structure, not its colours.** Each style has a layout grammar (panorama across panels, scrapbook, glass sheets crossing seams, colour blocks with tilted phones, floating UI…). Swapping colours and fonts on one skeleton is still one style. When making sets for several apps, give each app a structurally different style and show that style's signature.
- **Styles are guides, not templates.** Take what makes sense for this app and this message; don't repeat the same forms from app to app.
- **No prices in App Store screenshots.** Follow each store's rules.
