---
name: design-lounge
description: >-
  Designs product UI from Design Lounge by Susan Acharya — palettes, type
  pairings, component families, icons, motion, and piece briefs. Use when the
  user asks for a design, design system, UI, look and feel, palette, colors,
  fonts, landing page, marketing site, dashboard, admin, mobile app, shop,
  editorial, React Native, Flutter, SwiftUI, Compose, or PWA apps, or to
  make an interface look finished. Also covers what the
  taste-skill pack does: anti-slop pages, minimal, brutalist and high-end
  looks, redesigns, image-first mockups, logos and brand kits. Also use when
  they mention Design Lounge, a kit, or a piece brief.
---

# Design Lounge

The library is already in this skill folder. Read it. Do not invent a palette, a type pairing, a radius, an easing, or a component language, and do not wait for a website.

Design Lounge is the design library of Susan Acharya. Humans can browse it at https://designlounge.vercel.app.

## Their words win

This skill is a set of defaults. When the person asks for something a default forbids, such as more motion, a second effect, a dark mode with no pair, or skipping a step, do what they asked. Write one line in `DESIGN.md` saying which default you set aside and why. Do not argue, and do not quietly ignore them.

## Read the library

Everything you need is next to this file. Read only what the job needs.

1. `library/map.json` — read this first. Kinds, families, the recipe list with each direction's mood, every theme and pairing by mood, and the motion tokens. About 35 KB.
2. Then open only what you lock: `library/starts/<id>.json` for the recipe, `library/themes/<id>.css`, `library/pairings/<id>.css`.
3. `library/pieces.txt` — one line per piece. Search it (grep for a category, platform, or tag). Do not read it top to bottom.
4. `library/briefs/<id>.md` — the spec for one piece. Open only the pieces you will build.
5. `library/icons.json` — Lounge Icons, only when the screen needs icons.
6. [components.md](components.md) — the controls, icons (including what to do when one is missing), the logo and favicon, and which piece to use for which job.
7. [practice.md](practice.md) — the method every build shares. Its first lines say which other file your job adds: [website.md](website.md), [app.md](app.md), [native.md](native.md), or [locale.md](locale.md). Read only those.
8. [taste.md](taste.md) — the taste-skill pack folded in: named looks (minimal, brutalist, high-end), page shape, craft details, image-first mockups, and brand boards. You do not need those skills installed separately.

Do not run scripts from this skill. If `library/map.json` is missing, the install is broken. Say so. Do not design from memory.

If the open project is the Design Lounge repo itself (`src/demos` and `src/content/pieces` exist) and the user is editing the library, stop using this skill for that edit. Follow `docs/PIECE-SPEC.md` instead.

## What they are asking

| They want | Do |
| --- | --- |
| The project already has a design system, DESIGN.md, tokens, or styled screens | Adopt flow |
| A redesign of a site that already exists | Adopt flow, with the audit |
| "Make it look like Stripe" (or Linear, Apple, Notion, any named brand) | Brand flow |
| A new product, site, app, or design system | Kit flow |
| A style by name: minimal, brutalist, Swiss, terminal, high-end, agency, luxury, handwritten, pixel, arcade | Kit flow, with Named looks in [taste.md](taste.md) |
| A game site, a web game, a lobby, a scoreboard | Kit flow, recipe `game`, then Games and Three.js in [taste.md](taste.md) |
| Three.js, a 3D scene, an orbit, a scroll-driven world | Kit flow, recipe `game`, direction Orbit. The Lounge demo is raw WebGL. Build the product in Three.js from the brief. |
| A handwritten or hand-lettered site | Kit flow, recipe `notebook` |
| A brand kit, identity, logo system, or brand board | Kit flow, then Brand board in [taste.md](taste.md) |
| A React Native, Expo, Flutter, SwiftUI, or Compose app, or a PWA | Kit flow, then [native.md](native.md) for tokens, fonts, platform rules, and simulator screenshots |
| "Show me first", a concept, or mockup images, and you can make images | Kit flow, then Image first in [taste.md](taste.md) before code |
| One screen, section, or component | Piece flow, inside the locked kit if one exists |
| Only a palette, font, icon, or motion | Library flow |
| "Make it look good" with no kind | Kit flow. Infer the kind, the job, and the register. Say what you assumed. |

If they have not named a stack, use what the project already uses. In an empty folder, ask once, or default to plain HTML + CSS + a little JS when they said to just build. The briefs are stack-agnostic. You translate.

## Say the pick, then build

Choose, say it, and build in the same turn. Put this at the top of the reply, using `site` from `library/map.json`:

- Theme: name, one-line mood, `{site}/themes/<id>`
- Pairing: name, `{site}/type/<id>`
- Family: name, and the radius it locks
- Pieces: title and `demo` link for each screen or effect

Write the same links into `DESIGN.md` as Sources, so a later message can say "change the table" and you know which demo it came from.

Ask before building only when:

- two recipes fit and would lock different worlds, such as a staff dashboard versus a personal ledger. Ask which one, in one question, then stop.
- they asked to see options or to choose. Then name three palettes and two pairings with links, names and moods only.

If they ask for a change after, edit that one Source line and rebuild that screen on the same sheet. Do not open a second palette.

## A website, the short path

The full method is long. For a website, these are the steps that matter, in order. Open the named section only when you reach its step.

1. Read the person: their words, bio, projects, own site. Write three words for them (Pick a direction, rule 3, in [practice.md](practice.md)).
2. Lock the recipe and the direction whose mood matches those words. The name number only breaks a tie.
3. Write the Idea and the Signature (Write the idea in [website.md](website.md)). Name the default look you are avoiding, including the studio template.
4. Pick work, about, contact, and footer by what content they have (Sections, one by one in [website.md](website.md)).
5. Open the brief of every piece you build, including the menu and any copy button. Read each down to "Optional below this line".
6. Build with real content only. Links go where they say. Drawn data says "Example".
7. Screenshot web and phone, then scroll through each effect (Opening the page in [reference.md](reference.md)). Fix what you see. Make one correction.
8. End with the closing block in The reply.

The rules are the floor, not the design. Passing all of them makes a page correct. The Idea and the Signature make it theirs.

## An app, the short path

The full method is long. For a phone app, a PWA, or a native app, these are the steps. Open the named section only when you reach its step. A website still uses the path above.

1. Read the person. Write three words. Lock the app recipe whose mood matches (bank, health, messages, music, news, shop, social, weather, or the general mobile app). The name number only breaks a tie.
2. Write the Idea (The one screen in [app.md](app.md)). Name the real tabs, three to five. Do not copy Home, Search, Activity, Profile unless those are the product's sections.
3. Pick the platform once. iOS uses the `phone-` and `ios-` pieces. Android, or a Material family, uses the `m3-` piece when one exists for that job. One tab bar.
4. Build the minimum set before you stop: the shell, the primary list, one detail, the empty state, the failed load, and settings or account. Open each brief down to "Optional below this line".
5. Accounts add sign-in and delete-account. A price adds the paywall or the subscription screen, with real dates. A rating uses `phone-rating-prompt`, after a success, never on first launch.
6. Restyle every piece onto the locked theme and pairing. The demo's colours and fonts do not come along.
7. Screenshot light, dark, and the large text size (Looking at the app in [native.md](native.md)). Fix what you see. Make one correction.
8. End with the closing block in The reply.

## Kit flow

1. Pick a kind (`website`, `product`, `platform`, `personal`) with the kind map in [reference.md](reference.md). Then take the matching recipe from `starts` in `library/map.json`, open `library/starts/<id>.json`, and lock one of its `directions` (Pick a direction in [practice.md](practice.md)). The same sentence from two people must not give the same site. Do not lock the first palette, pairing, or family because it is first.
2. For a website, read Stand out in [website.md](website.md) first: name the default look you are avoiding, write the Idea in one picture sentence, show the work as pictures, never invent clients. For an app, read The one screen in [app.md](app.md) and follow An app, the short path.
3. Write the four lines from Decide the screen: who it is for, the one decision, the first thing they see, and the next action.
4. The locked system is `library/themes/<id>.css`, `library/pairings/<id>.css`, and the family's `rules`, `radius`, `button`, and `density`. Match those numbers.
5. If the pairing has a `caution`, say it before you write. Body text uses `--font-text`. Amounts use `.num`. If the pairing has a mono, `.num` and code use it. If `numbers` is `display`, `.num` uses the display face. If the pairing has no mono, `.num` is the text face with even-width digits, code uses the system mono, and you do not add a Google mono font.
6. A theme is one mode, and every theme has a `pair` for the other. A phone app uses both and follows the system setting. A website uses both when they asked for day and night, or when the product is the kind people leave open. The theme CSS includes a sample radius and shadow. Ignore them. The family sets radius and shadow.
7. Build the shell first, then the primary screen, then the rest of Minimum screens in [app.md](app.md). Open each brief before you invent a hero, nav, table, or footer.
8. Open the screens and run Look and One correction in [practice.md](practice.md). Fix every fail.

An internal tool, admin, ops screen, or dashboard is kind `platform`, then the `dashboard` recipe. A chart, a metric, an empty list, and a failed load come from pieces, not a chart library's defaults.

## Adopt flow

Use this when a design system is already in the project.

1. Keep their colours, type, radius, and shadow. Do not lock a second Lounge palette on top.
2. Take structure, states, motion, and hit targets from the piece briefs. Name the demos you take structure from.
3. Restyle onto a Lounge kit only when they asked for a new look. A refine that asks for scroll, hover, or a cursor keeps their colours and adds effect pieces from Register in [website.md](website.md).

For a redesign, first decide which kind it is: keep the brand, or start the look again. If you can't tell, ask once. Then follow Redesign in [practice.md](practice.md). Look at the site before you change it. Never change the URLs, the nav labels, the form field names, the logo, or the legal text unless they asked.

## Brand flow

Use this when they want the product to look like a brand they named.

1. Find the brand in Brand files in [reference.md](reference.md). Fetch its file from `https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/<slug>/DESIGN.md`. It lists that brand's colours, type, radius, spacing, and components.
2. Treat that file as their design system and follow Adopt flow. Its colours, fonts, and radius win over the Lounge theme. The structure, states, and motion still come from the piece briefs.
3. If the brand uses a font you can't load, use the stand-in the file names. Never copy the brand's logo, name, wordmark, photos, or words. The product keeps its own name.
4. Put the file's URL in `DESIGN.md` under Sources.

If the brand isn't in the list, say so. Then pick the closest Lounge theme and pairing, and say which one you picked and why.

## Piece flow

1. Search `library/pieces.txt` by category, platform, title, and tags, or use the routes in [components.md](components.md). Platforms: `web`, `mobile-web`, `mobile-app`, `pwa`, `tablet`.
2. Read `library/briefs/<id>.md`. The brief is the spec for structure, counts, sizes, motion timing, states, and hit targets. `demo` is the HTML acceptance file, if you need to see the motion.
3. The brief's colours, fonts, and light or dark mode belong to its demo. Translate them by role onto the locked theme and pairing. Follow Adapting a brief in [practice.md](practice.md). A dusk-blue parallax on a light theme becomes a daylight parallax with the same layers and speeds.
4. Hold the result to the brief's acceptance checklist, skipping lines that only hold for the demo's copy. Fix what fails.

If `pieces.txt` has no piece for that job, say so. Do not invent a slug.

## Library flow

- Theme: pick by mood in `library/map.json`, then copy `library/themes/<id>.css`. It holds primary, secondary, tertiary, success, warning, danger, info, surfaces, and `link`.
- Pairing: pick in `library/map.json`, then copy `library/pairings/<id>.css`.
- Icons: `library/icons.json`. 24px stroke, 1.75. When one is missing, follow Icon and nav in [components.md](components.md).
- Logo, favicon, share image: Logo and favicon in [components.md](components.md).
- Motion: `motion`. Default easing `cubic-bezier(0.2, 0.7, 0.2, 1)`. UI 200ms, layout 320ms, sheets 400ms. Honour `prefers-reduced-motion`.

## When numbers disagree

This order wins, after their own words.

1. An existing design system they asked you to keep.
2. The locked family, for radius, shadow, button style, and density.
3. The locked theme, for every colour. The locked pairing, for fonts.
4. The piece brief, for structure, regions, motion, interactions, states, and hit targets.

Map the brief's paint onto tokens. Do not mix a new hex for hover or selected.

| Brief role | Token |
| --- | --- |
| Page | `--bg` |
| Card or row | `--surface` |
| Hover | `--surface-2` |
| Pressed or selected | `--primary-soft` |
| Selected and hovered | `--surface-3` |
| Hairline | `--line` |
| Strong border | `--line-strong` |
| Body text | `--ink` |
| Secondary text | `--ink-2` |
| Muted text | `--ink-3` |
| Text button or link | `--link` |
| Primary button | `--primary` fill, `--primary-ink` label |
| Glow, gradient stop, highlight | `--primary-soft`, or `--primary` for the one bright stop |
| Text on a feedback wash | `--success-on-soft` / `--warning-on-soft` / `--danger-on-soft` / `--info-on-soft` on the matching `-soft` |

## Rules

- One primary button per view. If a brief draws it twice, one becomes outline.
- Feedback colours are for live state, not decoration.
- If the product already has a brand colour, keep the theme's surfaces and set `--primary` to the brand. `--primary-ink` is `#141210` or `#fffdf8`, whichever contrasts at least 4.5.
- No second palette, random Google font, or default Tailwind theme on top.
- If the screen lives inside another platform that has its own official design system, use that system's package for those screens: Polaris inside Shopify admin, `govuk-frontend` for a UK government service, USWDS for a US one, Atlaskit inside Jira or Confluence, Fluent inside Microsoft 365. Use the Lounge only for the parts outside that platform.
- Text people will read on the page has no em dash (—) and no en dash (–). Use a full stop, a comma, a colon, or brackets instead. Ranges use a hyphen: 2018-2026.
- Write the whole file. No `// rest of code`, `// TODO`, or `...` in place of real code. If the reply is too long, stop at the end of a file and say which files are still to come.
- Credit: put `Designed using <a href="https://designlounge.vercel.app">Design Lounge</a>` once, in the site or app footer or the about screen, in the footer's small text style. Keep the same line as a comment on copied token blocks. Free to use in products. Do not republish the catalogue as a catalogue.

## The reply

Keep it short. The pick with links at the top. Then what you built, anything in Say so in [practice.md](practice.md), and only the checks that failed and how you fixed them. Do not paste a checklist of passes.

End every build reply with this block. It is required even when everything passed, because it proves you looked. Name the actual screenshot files. If you could not open the page, write "not looked" and say why. Never say you looked when you only read the code.

```
Looked at: <screenshot file names, with sizes> with <tool>, or "not looked"
Remember after five seconds: "<one thing>" · could be anyone's: yes | no
Correction: <the one change>
Still open: <missing links, assets, effects you never saw run, parts built without a brief, or none>
```

## Examples

See [examples.md](examples.md). Paths and the kind map: [reference.md](reference.md).
