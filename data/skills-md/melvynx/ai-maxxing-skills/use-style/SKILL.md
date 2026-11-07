---
name: use-style
description: Apply a named visual style to anything the user will look at - landing pages, apps, dashboards, HTML reports, documents, visuals. Use for /use-style, "list styles", a style name (vercel, stripe, linear, raycast, anthropic, gumroad, new-york-times, dusk, luma, testspirite, grid, black-grid, ios-app), or whenever you create a file with a visual design and the global rules name a default style.
user-invocable: true
---

Load a named style before designing or building anything visual. Parse the name from `$ARGUMENTS` or the message. Aliases: `ios`/`iphone`/`expo` → `ios-app`; `geist` → `vercel`; `old vercel`/`black grid` → `black-grid`; `testsprite`/`test sprite` → `testspirite`; `lu.ma` → `luma`; `nyt`/`newspaper` → `new-york-times`; `claude` → `anthropic`; `attio` → `dusk`.

With no name, use the style in the `## Style` section of the global rules (`~/.agents/AGENTS.md`). Without one, pick by what you build: Expo / React Native screens → `ios-app`. Builder or course landings → `grid`. Developer infrastructure marketing → `vercel`. Austere monochrome tools → `black-grid`. Issue tracker or dense app shell → `linear`. Newspaper, magazine, long read → `new-york-times`. Warm calm AI product → `anthropic`. Loud creator commerce → `gumroad`. Glossy dark marketing → `raycast`. Data-rich dark dashboard → `dusk`. Light paper dashboard → `testspirite`. Events and RSVP → `luma`. Clean light product UI and payments → `stripe`.

If the name is `list` or nothing matches, list the styles in `styles/` with one line each and stop until the user chooses. To let the user see them, open `examples/gallery.html` from this skill folder (`open` on Mac, `xdg-open` on Linux, `start` on Windows): it shows a live preview of each style.

1. Read `styles/<name>.md` from this skill folder.
2. Prefer project overrides when they exist: `.agents/styles/<name>.md`, `<name>-theme.md`.
3. Treat the loaded style as hard constraints. Reuse the project's existing components and tokens before writing new ones.

Match the vibe exactly. Honor the style file's anti-patterns. Scaffold the page shell first on landing pages.
