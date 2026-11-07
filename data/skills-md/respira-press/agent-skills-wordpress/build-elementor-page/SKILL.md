---
name: build-elementor-page
description: "Use when building an Elementor page by hand with respira_build_page: from a brief, a screenshot, a mockup, or a design you must restate as Elementor settings. Covers the template, the styles Elementor never inherits, reading a design's computed values instead of guessing, buttons, spacing, mobile, and checking the render. For a finished HTML file, use html-to-page instead."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.1.0
  mcp-server: respira-wordpress
  category: workflow
---

# Build an Elementor page

**Version:** 1.1.0
**Updated:** 2026-10-04
**Category:** workflow
**Status:** stable
**Requires:** Respira for WordPress plugin (9.1+) and an MCP connection, on a site running Elementor

---

## Description

A recipe for building an Elementor page through `respira_build_page` that looks like the design the first time. Elementor writes every style into the widget that shows it. Nothing cascades from the page the way CSS does, so whatever a widget's settings leave out comes from the theme or the Elementor kit: the theme's body size, the kit's heading colour, a default line height. Most of the distance between a hand-built page and its design comes from those gaps, not from the layout.

**Have the finished HTML?** Use the html-to-page skill. One `respira_convert_html_to_builder` call writes the page as native Elementor widgets and carries the file's stylesheet, so it matches the file without restating anything. Build by hand when there is no file, or when the user wants every style in Elementor's own controls.

---

## When to Use

- A page from a brief, a screenshot or a mockup.
- A design you can read but that has to land as Elementor settings, not a stylesheet.
- A first build looked off: wrong font size, light blue headings, buttons on separate lines, the theme header and title above the page.

## Trigger Phrases

- "build this page in elementor"
- "make an elementor landing page"
- "recreate this design in elementor by hand"

---

## Workflow

### 1. Read the site

`respira_get_site_context`, then `respira_get_builder_info` for the Elementor version and whether containers are on. You write the tree as section > column > widget; Respira writes it in the shape the site uses.

### 2. Pick the template

A landing page draws its own header and footer, so it should not sit inside the theme's. Pass `template` to `respira_build_page`:

- `"elementor_canvas"`: nothing but the page. No theme header, page title or footer.
- `"elementor_header_footer"`: the theme's header and footer, the page full width between them, no page title.
- omitted: the theme's default template, with its title and content width.

An older plugin ignores the option. If the share link (step 8) still shows the theme's header and page title, tell the user to pick the template in the editor's page settings.

### 3. Read the design's computed values

Write down what the browser shows, not what the stylesheet happens to declare. If you can open the design in a browser, read `getComputedStyle` for each kind of element. If you work from the CSS, apply these browser defaults yourself:

- A heading with no `font-weight` is **bold (700)**, not 600.
- A heading or paragraph with no `line-height` **inherits the body's** (a body at `line-height:1.6` makes a 38px h2 60.8px tall). Elementor's own default for headings is about 1.2, which shrinks every section.
- A `<p>` has `1em` top and bottom margins; an `h1` to `h3` has margins too unless the CSS removes them.
- `letter-spacing` in `em` becomes px against the element's own size: `.12em` at 13px is 1.56px.
- A colour, font family or size set on `body` applies to every element that does not set its own. Restate it on every widget.

### 4. Style every text widget completely

Typography keys only apply when `typography_typography` is `"custom"`. For every heading, text editor and button, set:

```
typography_typography: "custom",
typography_font_family: "Inter",
typography_font_size: { unit: "px", size: 16 },
typography_font_weight: "400",
typography_line_height: { unit: "em", size: 1.6 },
```

plus the colour (`title_color` on a heading, `text_color` on a text editor, `button_text_color` on a button), and `typography_letter_spacing` and `typography_text_transform` where the design has them. A widget without a colour shows the kit colour (often light blue headings or grey text).

Text editor paragraphs take the theme's paragraph margins; set `paragraph_spacing: { unit: "px", size: 16 }` (the gap between paragraphs), or keep one paragraph per widget and space with `_margin`.

### 5. Buttons

- Size and shape: `text_padding` (per side), `border_radius`, `background_color`, `button_text_color`, and the typography keys above. Elementor's button line height is about 1; set the design's (`typography_line_height`) or the button comes out shorter.
- Outline buttons: `border_border: "solid"`, `border_width`, `border_color`, and a `background_color` of `"transparent"`.
- Hover: `button_background_hover_color`, `hover_color`.
- Two buttons side by side: give each `_element_width: "auto"` so they sit inline in the same column, with `_margin` for the gap. Without it each button takes the full row.

### 6. Layout and spacing

- Sections: `padding` per side, `background_background: "classic"` with `background_color`, `stretch_section: "section-stretched"` for full bleed, `content_width` for the inner width.
- Columns: `_inline_size` in percent; column gaps through the section's `gap` and the columns' own `padding`.
- Space between widgets: `_margin` on the widget, as the design's margins, rather than spacer widgets. The kit adds its own widget spacing (20px by default) below every widget but the last in a column, on top of your margin: set each bottom margin to the design's gap minus that spacing (a 24px gap is `bottom: "4"`), or the page grows by 20px per widget.
- Nesting: on a site without flexbox containers a page is sections > columns > widgets, and an inner section nests one level deep only. A card that holds a row (a table, a flow of steps, a grid of stats) becomes an inner section of its own, or a row of widgets with `_element_width: "initial"` and a percent width.
- Tables: a `<table>` in a text editor keeps every cell editable as text and scrolls on a phone if you wrap it in `<div style="overflow-x:auto">`; rebuilding it as columns stacks the cells on a phone.
- Images: upload first (`respira_upload_media` with the URL; `respira_sideload_image` is for stock images), then `image: { url, id }`, `image_size: "full"`, `width: { unit: "%", size: 100 }`, `image_border_radius` for rounded corners.

### 7. Mobile

Check the phone render as carefully as the desktop one: a hand build drifts most there, because every desktop margin, line height and column that has no `_mobile` value carries over to a 390px screen.

Every size, padding and margin has `_tablet` and `_mobile` variants (`typography_font_size_mobile`, `padding_mobile`, `_margin_mobile`). Set `_inline_size_mobile: 100` on columns that stack. Without them the desktop values shrink into the phone width.

### 8. Build in parts, then check the render

Send the page in one `respira_build_page` call when it is small; for a long page, build the first sections and add the rest with `respira_inject_builder_content` and `mode: "append"` (without it the call replaces the page, and a page with content refuses the replace unless `confirm_replace: true`), checking the received counts each time. Then mint `respira_create_share_link` and look at the page at desktop width and at 390px, beside the design. Compare heading sizes, line heights, button sizes and the page height section by section; fix with `respira_update_element`. Without a browser, pass the share link to `respira_check_design` as `url` with `rendered: true`, which renders the draft and checks it.

Images the user supplied (on their site or any URL they gave) go in with `respira_upload_media` and the URL; `respira_sideload_image` takes stock image domains only.

---

## Hard rules

- Never put the design into one HTML widget. The user asked for an editable page.
- Never leave a text widget without its typography and colour.
- Never call a page done from the write result alone. Check the render.
- Keep the page a draft until the user approves it.
