---
name: shopify-theme-builder
description: Builds a Creator's own Shopify theme from Shopify's Skeleton theme and a catalog of prebuilt sections, styled with their brand, and opens a local Studio with a live preview. Use when someone wants a new Shopify theme, a custom Shopify store design, or to restyle a Shopify shop from their website, screenshot or moodboard.
---

# Shopify Theme Builder

You build a **Theme** for one Shopify shop with the **Creator** (the person you're talking to). The Theme starts from the **Base Theme** (Shopify's Skeleton), adds sections from the **Section Catalog**, and carries the **Brand** (colors, fonts, logo) in Shopify's native theme settings, so the Merchant can keep editing it in Shopify's Theme Editor. The **Studio** is a local app where the Creator adjusts the Brand and composes pages while `shopify theme dev` shows the real rendered Theme.

`<skill-dir>` below is the folder holding this `SKILL.md`. It holds `base-theme/`, `catalog/sections/` and `studio/`. The Theme lives in its own folder outside it; the Theme's files never go in `<skill-dir>`.

Talk with the Creator in their language. Work through steps 1 to 5 in order; steps 6 and 7 run when the Creator asks. Each ends on its **done** line.

Never publish a theme: no `shopify theme publish`, no `--publish`, `--live` or `--allow-live` flag, no Publish button in the admin. Publishing changes the Merchant's live shop, and only the Merchant decides that.

## 1. Prerequisites

Check each; when one fails, tell the Creator the fix and wait until it passes.

| Check | Passes when | Fix |
| --- | --- | --- |
| `node --version` | 22.12 or newer | Install the current LTS from https://nodejs.org (or `nvm install --lts`). |
| `git --version` | 2.28 or newer | Install from https://git-scm.com. |
| `shopify version` | 4.8.0 or newer | `npm install -g @shopify/cli@latest` (or `brew install shopify-cli`). |
| Studio dependencies | `<skill-dir>/node_modules` exists | Run `npm ci --omit=dev` in `<skill-dir>`; again after updating the skill. |
| Store access | `shopify theme list --store <shop>.myshopify.com` lists themes | See below. |

**Store access.** The preview renders on a real store, so the Creator needs one where they are the owner, or have a staff or collaborator account with theme permissions. Ask for its `<shop>.myshopify.com` address. Without one, offer to create a free **development store** for them:

1. Ask for the store's name (like the shop's name).
2. Run `shopify organization list --json` for the Creator's organizations; when it lists more than one, ask which to use.
3. Run the command below, allowing it up to 10 minutes: it waits until the store is ready, then prints its `<shop>.myshopify.com` address. Without a terminal the CLI needs all of `--name`, `--organization-id` and `--plan`, even with a single organization; `--demo-data` adds sample products so the preview looks like a shop.

   ```sh
   shopify store create dev --name "<name>" --organization-id <id> --plan basic --demo-data --json
   ```

The Creator can also create one in Shopify's Dev Dashboard (https://dev.shopify.com) › Stores › Create store.

A development store can't be transferred to a Merchant; for a Merchant's shop, use the Merchant's store with a collaborator account. Give each Theme its own store: the Shopify CLI keeps one development theme per store per machine, so two Themes previewed on one store overwrite each other.

When a `shopify` command asks to log in, have the Creator run `shopify auth login` in their own terminal, then check again.

Recommend, without requiring it, Shopify's AI Toolkit (https://github.com/Shopify/Shopify-AI-Toolkit) for later Liquid work. Its `shopify-liquid` skill sends prompts and code to Shopify unless the Creator opts out: create `~/.config/shopify-ai-toolkit/opt-out` or set `OPT_OUT_INSTRUMENTATION=true`.

**Done** when every check passes and you have the store address.

## 2. Brand capture

Gather seven things: **colors**, **fonts**, **logo**, **style**, **shop language**, the **shop name**, and the **author** (the Creator's name or business, shown as the Theme's author).

1. Ask for a reference first: the Creator's current website, a screenshot, or a moodboard.
   - A website: open it and read the colors (background, text, buttons, accent), font families and logo file from its pages and CSS.
   - An image: derive the palette and the font mood from it.
2. Tell the Creator what you took from the reference, then ask only about what it left open. Ask one question at a time. Without a reference, ask about all seven.
3. Turn the answers into Brand values:
   - **Color schemes.** Each scheme has four hex colors (`#RRGGBB`): `background`, `text`, `button`, `button_label`. Make `scheme-1` the main light scheme and `scheme-2` its dark inverse; add `scheme-3` for an accent color when the Brand has one. Keep text-on-background and label-on-button contrast at 4.5:1 or more.
   - **Fonts.** A heading font and a body font, each a handle from `<skill-dir>/studio/server/shopify-fonts.json` (Shopify's font library), like `work_sans_n4` (`n4` is regular 400, `n7` bold, `i4` italic). When the reference's font isn't there, pick the closest family and tell the Creator.
   - **Logo.** A PNG, JPEG, WebP or SVG file, at most 2 MB. Take the file the Creator gives, or download it from their website when that site is their own brand. None is fine: the header shows the shop name.
   - **Style** (like minimal, bold, playful, luxurious) guides the fonts, the schemes and which home sections you pick in step 4.
   - **Shop language**: the language the shop's customers read, as the ISO code Shopify admin › Settings › Languages shows (`it`, `de`, `pt-BR`).

**Done** when every Brand value above has a concrete value (or "no logo") and the Creator has confirmed them.

## 3. Create the Theme

1. Ask where the Theme goes. Default: a new folder named after the shop (like `acme-theme`) in the Creator's current directory. It must be outside `<skill-dir>`, and must not exist yet or be empty; pick another name rather than write into a folder with files.
2. Copy every file of the Base Theme, including its dotfiles, then the catalog's header, footer and footer group over the Base Theme's own. On macOS or Linux (on Windows, use the shell's equivalent):

   ```sh
   mkdir -p <theme> && cp -R <skill-dir>/base-theme/. <theme>/
   cp <skill-dir>/catalog/sections/header.liquid <skill-dir>/catalog/sections/footer.liquid <skill-dir>/catalog/sections/footer-group.json <theme>/sections/
   ```

   Then delete `<theme>/PROVENANCE.md`: it describes the skill's own copy of Skeleton. The Theme keeps Shopify's folder layout at its root (`layout/`, `sections/`, `templates/` …), which Shopify's GitHub integration requires, and has no build step. `LICENSE.md` is Skeleton's license and stays with the Theme. The other catalog sections are added through the Studio in step 4, which copies only the ones the Theme uses.
3. In `<theme>/config/settings_schema.json`, set the first entry's `theme_name` to the shop's name (at most 50 characters) and `theme_author` to the author.
4. When the shop language isn't English, add it:
   1. Copy `locales/en.default.json` to `locales/<code>.json` and translate every value. Keep every key, and keep `{{ variables }}` and the HTML of `_html` keys as they are. Plural keys (`one`, `other`) get the forms the language needs (`zero`, `two`, `few`, `many`).
   2. Copy `locales/en.default.schema.json` to `locales/<code>.schema.json` and translate it the same way, so the Merchant sees the Theme Editor in that language.
   3. Keep `en.default.json` as is: English stays the default, and the storefront shows `<code>.json` to customers once the shop publishes that language.
5. Run `git init -b main` in `<theme>`, so the Creator can connect it to Shopify's GitHub integration later.

**Done** when `<theme>` holds the Base Theme with the catalog header and footer, the Theme's name, and (when not English) both locale files of the shop language.

## 4. Open the Studio, write the Brand, compose the pages

1. Start the Studio as a background process that keeps running after your command returns, with its output going to a log file outside the Theme folder:

   ```sh
   node <skill-dir>/studio/bin/studio.mjs --theme <theme> --store <shop>.myshopify.com > <log-file> 2>&1
   ```

   To stop this Studio and its `theme dev`, run `pkill -f "studio.mjs --theme <theme> "`, with `<theme>` exactly as in the start command and the trailing space kept. It matches only this Theme's Studio, so Studios and `theme dev` runs of other projects on the machine keep running.

   Read the Studio's URL from the log (`Local: http://localhost:5173/`); the port may differ. The Studio also starts `shopify theme dev` for the preview, and its output goes to the same log. While sections are being added, that log may show failed uploads (a template naming a section file not uploaded yet); they resolve within seconds, so judge by `GET /api/preview` and `validation` instead.
2. Write the Brand and compose the pages through the Studio's API at that URL. It checks every value, copies catalog sections into the Theme with the locale keys they need, and runs Theme Check after each write. Every call returns the Theme's state as JSON (the pages, their section ids, the Brand and `validation`); an error returns `{ "error": "…" }` saying what to fix.

   | Call | Body |
   | --- | --- |
   | `PUT /api/brand` | `{"colorSchemes": {"scheme-1": {"background": "#FFFFFF", "text": "#1A1A1A", "button": "#1A1A1A", "button_label": "#FFFFFF"}}, "headingFont": "<handle>", "bodyFont": "<handle>"}` |
   | `PUT /api/brand/logo` | the image file, with its `Content-Type` (`image/png`, `image/jpeg`, `image/webp`, `image/svg+xml`) |
   | `POST /api/<page>/sections` | `{"type": "<catalog section>"}`; `<page>` is `home`, `product` or `collection` |
   | `DELETE /api/<page>/sections/<id>` | none |
   | `PATCH /api/<page>/sections/<id>` | `{"colorScheme": "scheme-2"}` |
   | `PUT /api/<page>/order` | `{"order": ["<id>", …]}`, every section id of the page exactly once; a new section is added at the end, so move it with this |
   | `GET /api/theme` | none; the current state, with the catalog sections each page can take under `catalog` and the Custom Sections under `custom` |

   For example: `curl -X PUT <studio>/api/brand/logo -H 'Content-Type: image/png' --data-binary @logo.png`.
3. Compose the pages. A page keeps at least one section, so add the new sections before removing the Base Theme's `main`:
   - **home**: pick 4 to 6 sections that fit the style from `catalog.home` in `GET /api/theme`. Start with `hero`. Then remove `main`.
   - **product**: add `main-product` and `related-products`, then remove `main`.
   - **collection**: add `main-collection`, then remove `main`.

   Alternate the color schemes down the home page (`PATCH`) so neighbouring sections don't share one background.
4. Check `GET /api/theme`: `validation` must hold no offense with `"severity": "error"`. Fix any error in the file and line it names, then check again.
5. Check `GET /api/preview`: `{"status": "running", "url": …}` gives the preview link. `login-required` means the Shopify CLI printed a login link in the log: give it to the Creator and check again after they log in. `error` carries a message saying what to fix. When it asks for the store password, ask the Creator for the storefront password, under Password protection at `https://admin.shopify.com/store/<shop>/online_store/preferences` (development stores always have one), stop the Studio, and start it again with `--store-password <password>` added.
6. Commit the Theme in `<theme>` (`git add -A && git commit -m "Create the Theme"`).

**Done** when the Brand and the three pages are written, `validation` has zero errors, the preview is `running`, and the Theme is committed.

## 5. Hand-off

Tell the Creator, in a few lines:

1. Open the Studio at its URL to adjust colors, fonts and logo, and to add, remove, reorder or recolor sections on the home, product and collection pages.
2. Open the preview link in a separate Chrome window: it shows the real Theme and refreshes after each change. Section text and images are edited in Shopify's Theme Editor; products and menus in the Shopify admin.
3. The Theme lives in `<theme>`, with its own Git history. You can keep changing it: the Studio picks up your edits while it runs.
4. To stop the Studio, end its process; to start it again, run the command from step 4.1 (with `--store-password` if you added it).
5. Ask you for a section the catalog doesn't have (step 6), and to deliver the Theme to the store when it's ready (step 7).

## 6. Custom Sections

When the Creator wants something no catalog section does, write a **Custom Section**: a section file in the Theme only, never in `<skill-dir>`.

1. Pick a kebab-case name (like `size-guide`) that no file in `<theme>/sections/`, `<skill-dir>/base-theme/sections/` or `<skill-dir>/catalog/sections/` has, and write `<theme>/sections/<name>.liquid`.
2. Follow the conventions of the catalog sections; open one in `<skill-dir>/catalog/sections/` (like `image-with-text.liquid`) as the model:
   - **Brand only through settings.** No hardcoded colors or fonts: use the CSS variables the Theme sets from the Brand (`--color-background`, `--color-foreground`, `--color-button`, `--color-button-label`, `--font-heading--*`, `--font-body--*`).
   - **Color scheme.** The schema has `{"type": "color_scheme", "id": "color_scheme", "label": "t:labels.color_scheme", "default": "scheme-1"}` and the outer element carries `class="color-{{ section.settings.color_scheme }}"`.
   - **Placeholders.** A blank image, product or collection renders Shopify's placeholder (`{{ 'image' | placeholder_svg_tag: 'placeholder' }}`, `'product-1'` to `'product-6'`, `'collection-1'` to `'collection-6'`, `'lifestyle-1'`/`'lifestyle-2'` for large media), so an empty store still looks like a shop.
   - **Presets.** The schema has a `presets` entry, so the Merchant can add the section in the Theme Editor.
   - **Pages.** A section that needs the product or collection sets `"enabled_on": {"templates": ["product"]}` (or `["collection"]`); `"limit": 1` when a page shows it once.
   - **Text.** Text the Creator writes is a setting with a default. Fixed storefront text uses `{{ 'key' | t }}`, and every `name`, `label`, `info` and `content` in the schema is a `t:` key. Add each new key to `locales/en.default.json` (or `locales/en.default.schema.json`) and, translated, to the shop language's files.
   - **Limits.** At most 50 blocks (`max_blocks`) and 256 KB per file.
3. Check Theme Check: `validation` in `GET /api/theme` (or `shopify theme check --path <theme>` when the Studio isn't running) must hold no error. Fix each one and check again. Don't tell the Creator the section is done before this passes.
4. When the Creator said which page it goes on, add it with `POST /api/<page>/sections` and `{"type": "<name>"}`. Either way, the Studio lists it under Custom Sections in the section picker of each page it can go on, where the Creator can add it.
5. Ask the Creator to check it in the preview; its text and images are edited in the Theme Editor. Then commit it in `<theme>`.

**Done** when the section file passes Theme Check with zero errors, shows in the Studio, and is committed.

## 7. Delivery

When the Creator says the Theme is ready, deliver it. Delivery uploads a copy; it never publishes.

1. Run `shopify theme check --path <theme>`. It must exit 0 (zero errors); fix every error first. Deliver nothing until it passes.
2. Commit any open change in `<theme>`.
3. Deliver it one way; the first is the default:
   - **Push unpublished** (default), to the Merchant's store. When step 1 used a development store for the preview, ask for the Merchant's `<shop>.myshopify.com` and check access to it the same way; a development store can't be handed to a Merchant. `<theme name>` is the `theme_name` from step 3.3:

     ```sh
     shopify theme push --path <theme> --store <shop>.myshopify.com --unpublished --theme "<theme name>" --json
     ```

     It creates a new unpublished theme, and its output holds the theme's id and its preview and editor links; give both links to the Creator. When it reports files that failed to upload, fix them and push again with `--theme <id>` in place of `--unpublished --theme "<theme name>"`, so no second copy is created.
   - **Zip**, when the Creator can't push to the Merchant's store. Run `shopify theme package --path <theme>`: it writes `<theme_name>-<theme_version>.zip` (both from `config/settings_schema.json`) into `<theme>`. Move it next to the Theme folder, so Git doesn't track it. The Merchant uploads it in Shopify admin › Online Store › Themes › Add theme › Upload zip file, and it arrives unpublished.
   - **GitHub integration**, when the Creator deploys from Git. Tell them to:
     1. Create an empty GitHub repository, then in `<theme>` run `git remote add origin <repo-url>` and `git push -u origin main`.
     2. In Shopify admin › Online Store › Themes › Add theme › Connect from GitHub, log in to GitHub, and pick the repository and the `main` branch. The theme arrives unpublished.
     3. From then on each push to `main` updates that theme, and changes saved in the Theme Editor are committed back to `main`: run `git pull` before editing locally.
4. Tell the Creator that the Merchant publishes the theme in Shopify admin › Online Store › Themes, after reviewing it.

**Done** when Theme Check passed and the theme is on the store unpublished, the zip is ready, or the Creator has the GitHub steps, and nothing was published.
