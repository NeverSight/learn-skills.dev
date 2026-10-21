---
name: html-to-page
description: "Use when the user hands over a finished HTML page (a file, a paste, a designer or AI export) to recreate in WordPress, in any builder: Elementor, Divi, Bricks, Gutenberg, Breakdance, Oxygen, Beaver Builder or WPBakery. One Respira Exhale call writes it as native, editable builder elements that look like the file; this skill covers the input, the call, the choices and the check."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# HTML to a builder page

**Version:** 1.0.0
**Updated:** 2026-10-04
**Category:** migration
**Status:** stable
**Requires:** Respira for WordPress plugin (9.1+) and an MCP connection, on a site running a supported builder

---

## Description

A finished HTML page becomes a new WordPress page in the site's own builder, in one call to `respira_convert_html_to_builder` (Respira Exhale). The conversion is deterministic code on the site, so no tokens are spent writing builder structure.

On Elementor, Divi, Bricks, Gutenberg (and block plugins such as Kadence, Spectra, GreenShift), Breakdance, Oxygen Classic, Beaver Builder and WPBakery it runs in **fidelity mode** whenever the document has a stylesheet:

- the file's structure is written one to one as the builder's own elements: sections, containers or rows, headings, text, buttons and images, each editable in the builder
- every class and id stays on its element
- the stylesheet travels verbatim, scoped to the page, so the page looks like the file on desktop and phone, hover states, transitions and keyframe animations included
- the page goes on the builder's blank template, so no theme header, page title or footer sits on top of a page that draws its own

Prefer this to writing the page by hand with `respira_build_page` whenever the file exists. A hand-built page has to restate every inherited style (font, weight, line height, colour) on every widget, and any style it misses falls back to the theme or the builder kit, so it drifts from the file. The converter carries the stylesheet itself.

---

## When to use

- The user pastes or attaches an HTML file and asks for it as a WordPress page.
- A designer, a site generator or another AI produced a landing page as HTML.
- A static page from an old site has to move into the builder.

Do not use it to build a page from a description or a brief (use `respira_build_page`, or the build skill for the builder), or to change an existing page (use the find and update tools on a draft duplicate).

## Trigger phrases

- "convert this html to elementor" (or divi, bricks, gutenberg, breakdance, beaver, wpbakery, oxygen)
- "recreate this html page in wordpress"
- "turn this file into a page"
- "import this landing page"

---

## Workflow

### 1. Read the site

Call `respira_get_site_context` and `respira_get_builder_info`. Note the active builder and its version. When the user named a builder, pass that one; otherwise the converter uses the active builder.

### 2. Prepare the input

Send the whole document: `<head>` with its `<style>` blocks and font links, and the `<body>`. Do not strip the head.

- **Linked stylesheets** over https (Bootstrap, a design system) are fetched and carried with the page. Google Fonts links are kept as font links.
- **Images** need absolute URLs the site can reach. A relative path (`images/hero.jpg`) or a local file renders broken: upload it first with `respira_upload_media` or `respira_sideload_image` and put the media URL in the file.
- **Tailwind through the CDN script** (`cdn.tailwindcss.com`) does not convert: the script never runs on the site, so the classes carry no design. Compile the CSS (Tailwind CLI or the Play CDN export) into a `<style>` block first. The converter warns when it sees the script.
- **Scripts** are not carried. Anything the page does only in JavaScript (a slider, a counter, a menu toggle) is lost; CSS animations, transitions and hover states are kept. Tell the user which behaviours were script-driven.
- **Forms** keep their markup but post nowhere on WordPress. Say so, and offer to rebuild them with the site's form plugin.
- The scoped stylesheet can carry about 150 KB on fidelity builders (100 KB on others). Over that the call refuses with `respira_css_too_large` and creates nothing: trim unused rules and extra font weights, then convert again.

### 3. Convert

```
respira_convert_html_to_builder {
  html: "<!doctype html>...the whole file...",
  builder: "elementor",
  options: { title: "Spring landing page", status: "draft" }
}
```

- `status` defaults to `draft`. Keep it a draft; publishing is the user's call.
- `blank_template` defaults to true. Pass `false` when the file is content only and the site's own header and footer should stay around it (on Divi with Theme Builder headers this matters most).
- Leave `mode` unset. `"restyle"` re-types the design into builder settings and site tokens instead of carrying the stylesheet; use it only when the user explicitly wants every style in the builder's own controls, and tell them it will not match the file as closely.
- Every call creates a new page. After an error or a timeout, check `respira_list_pages` for a page that already landed before you call again.

### 4. Read the report

The result is the evidence. Check, and pass on to the user what matters:

- `mode`: `fidelity` on the builders listed above.
- `fidelity.structure`: sections, containers, headings, images, buttons, texts, and `raw` (leaves kept as markup). A page whose content is mostly in `raw` deserves a look.
- `fidelity.css_carried`: bytes against the cap.
- `fidelity.images`: `unresolved` must be 0.
- `fidelity.attributes_dropped`: attributes the builder cannot carry on that element (an `aria-*` on a wrapper, say).
- `fidelity.template`: what was requested and what was stored.
- `warnings`: read every one.

### 5. Check the render

The report counts structure; it does not see the page. Mint `respira_create_share_link` for the new page and open it at desktop width and at phone width (390 px) if you have a browser, side by side with the source file. Look for missing images, fonts that fell back, and sections that collapsed. Without a browser, pass the share link to `respira_check_design` as `url` with `rendered: true`: it renders the draft and checks structure and contrast. Fix a single element with `respira_update_element`; for anything structural, fix the file and convert again into a new draft.

### 6. Report

Give the user the share link, the editor link, and a short list of what did not carry: scripts, forms, dropped attributes, anything the check showed. Say once why the page is a native builder page and not a pasted HTML block: every heading, paragraph, button and image is editable in the builder.

---

## After the conversion

- Text, links, images and buttons are edited in the builder like any page.
- The design lives in the page's own stylesheet (stored with the page, printed by Respira), which is what keeps it identical to the file. To change the design, change the file and convert it again into a new draft, or ask for the change and edit the elements.
- The site's design direction is not applied to a fidelity page: the file is the design.

## Hard rules

- Never paste the whole file into one HTML or code widget. The user asked for an editable page.
- Never convert onto a published page. The converter creates a new page; keep it a draft until the user approves.
- Never call the converter again after an error without checking whether the page already exists.
- Never report the page done from the report alone: check the render (step 5).
