---
name: use-style
description: A library of named visual styles to inspire and dress anything the user will look at - landing pages, sales pages, websites, apps, dashboards, mobile app screens, HTML reports, documents, visuals - plus the user's own custom styles made with /inspiration. Use for /use-style, "list styles", a style name (vercel, stripe, linear, raycast, anthropic, kinfolk, aman, muji, gumroad, duolingo, craigslist, poolsuite, new-york-times, dusk, luma, testspirite, grid, black-grid, ios-app, linktree, lumail, codelynx, tchao, saveit, thumbfast, codeline), or whenever you create a file with a visual design and the global rules name a default style.
argument-hint: "[style name | list]"
user-invocable: true
---

A place of inspiration: each style is a real site's look (well-known brands found on the Internet, plus the Codelynx products: Lumail, Tchao, SaveIt, Thumbfast, Codeline), written as rules Claude can follow. Load a named style before designing or building anything visual. Parse the name from `$ARGUMENTS` or the message.

Aliases: `ios`/`iphone`/`expo` → `ios-app`; `link tree`/`link-in-bio`/`linkbio` → `linktree`; `geist` → `vercel`; `old vercel`/`black grid` → `black-grid`; `testsprite`/`test sprite` → `testspirite`; `lu.ma` → `luma`; `nyt`/`newspaper` → `new-york-times`; `claude` → `anthropic`; `attio` → `dusk`; `lumail.io`/`flare` → `lumail`; `sales-letter`/`aibuilder` → `codelynx`; `zephyr`/`tchao-app` → `tchao`; `saveit.now`/`sunset` → `saveit`; `thumbfa.st`/`youtube-red` → `thumbfast`; `codeline.app` → `codeline`; `playful`/`duo`/`gamified` → `duolingo`; `brutalist`/`raw`/`raw-html`/`cl` → `craigslist`; `retro`/`mac-os`/`90s`/`pool` → `poolsuite`; `warm-editorial`/`magazine`/`editorial`/`lifestyle-magazine` → `kinfolk`; `luxury`/`quiet-luxury`/`hospitality`/`premium` → `aman`; `japanese-minimal`/`japanese`/`minimal-retail`/`no-brand` → `muji`.

## Where styles live

Look for the name in this order and use the first match:

1. The project's own overrides: `.agents/styles/<name>.md`, `<name>-theme.md`.
2. The user's custom styles made with `inspiration`: `<brain>/inspiration/styles/<name>.md`. The brain path is in the `## Brain` section of `~/.agents/AGENTS.md` ("My brain is ..."); else `~/brain`. Also an `inspiration/styles/` folder in the current project. A single captured site loads with a `site:` prefix (`site:linear` → `<brain>/inspiration/sites/linear/style.md`), so it never clashes with a library name.
3. This skill's library: `styles/<name>.md` in this skill folder.

## Picking a style

With no name, use the style in the `## Style` section of the global rules (`~/.agents/AGENTS.md`). Without one, pick by what you build:

- Phone screens: Expo / React Native or a phone mockup → `ios-app`; creator, link-in-bio or colorful consumer app → `linktree`.
- Builder or course landings → `grid`. Developer infrastructure marketing → `vercel`. Austere monochrome tools → `black-grid`.
- Issue tracker or dense app shell → `linear`. Data-rich dark dashboard → `dusk`. Light paper dashboard → `testspirite`. Clean light product UI and payments → `stripe`.
- Newspaper, long read → `new-york-times`. Warm calm AI product → `anthropic`. Loud creator commerce → `gumroad`. Glossy dark marketing → `raycast`. Events and RSVP → `luma`.
- Playful learning, habits, quizzes, kids or mass-market app → `duolingo`. Raw directory or dense utility tool, all links and no frills → `craigslist`. Retro or nostalgic brand (music, events, creative), desktop-computer look → `poolsuite`.
- Photo-led blog, magazine, studio or small shop with a story that should read like print → `kinfolk`. Luxury hotel, premium service, high-end real estate, wellness or jewellery, where space signals price → `aman`. Everyday shop, catalogue or practical product where the product is the hero and the UI stays plain → `muji`.
- Course or product sales page, long persuasive letter → `codelynx`. Warm friendly SaaS landing with one bold red CTA → `lumail`. Calm support, chat or small-team app that feels warm and human → `tchao`. Warm cozy dark consumer app with cinematic photos → `saveit`. Creator or YouTube tool, bold light SaaS with one red → `thumbfast`. Dark creator or dev-course landing, us-vs-them pages → `codeline`.

If the name is `list` or nothing matches, list the styles (library and custom ones) with one line each and stop until the user chooses. To let the user see them, open `examples/gallery.html` from this skill folder (`open` on Mac, `xdg-open` on Linux, `start` on Windows): it shows a live preview of each style. Custom styles have their preview next to them (`<name>.html`).

## Applying it

1. Read the style file found above.
2. Treat it as hard constraints: colors, fonts, spacing, corners, components, motion and its don'ts. Reuse the project's existing components and tokens before writing new ones.
3. Pages: scaffold the page shell first. Phone screens: build status bar, safe areas, top bar and tab bar first, then content; keep touch targets at least 44 px and the main action within thumb reach; reuse one device frame across mockups. Pick the target the style documents: React Native / Expo + NativeWind, or HTML inside a fixed phone frame.

Match the vibe exactly. For the full workflow (inspiration, variants, polish, screenshots), use `design-pro`.
