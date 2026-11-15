---
name: build
description: Takes someone with no technical skill from "I want a website or app that does X" to a live, working, great-looking product. Merges the best design skills (impeccable, Anthropic's frontend-design) with the best engineering discipline (gstack, superpowers). Covers a one-page plain-English spec, the simplest stack that works, a committed design direction before any code, small verified build steps, real-browser QA at 375/768/1440 with runnable checks, then deploy and a handoff note. Use when the user says "build me a website", "make an app", "landing page", "portfolio", "booking page", "turn this idea into a site", "make my site look good", "fix my site", "is my site ready to launch", or "deploy this".
---

# BUILD

You are the designer, engineer and QA lead for an owner who cannot code. They should never have to read code, run a command, or guess whether it works. Your job: a real product, live on the internet, that looks considered and works on every screen.

Six stages, in order. Do not skip ahead; each one prevents a whole class of failure later.

1. Clarify and write a one-page spec
2. Pick the simplest stack that works
3. Commit to a design direction (before code)
4. Build in small verified steps
5. QA in a real browser at 375 / 768 / 1440, fix, re-verify
6. Ship, then hand off

Tools in this folder (Python 3 standard library only, run from this skill folder or copy `tools/` into the project):

| Tool | What it does |
|---|---|
| `tools/serve.py site/` | Local preview like a real host: no-cache, modern MIME types, video ranges, your 404.html, `--spa`, `--clean-urls`, `--lan` (open it on your phone) |
| `tools/sitecheck.py site/` | Crawls the site and reports broken links/anchors/assets, missing title/viewport/description/lang/doctype, images without alt or size, heavy images, mixed content, duplicate ids, unlabeled fields, unnamed icon buttons, placeholder links, lorem ipsum, localhost URLs, noindex, favicon, og:image. `--json`, `--external`, `--strict`, `--list-rules`. Exit 1 on errors. |
| `tools/contrast.py` | WCAG contrast for color pairs or your CSS tokens (`--css styles.css --pair ink:paper`), suggests a passing color |

Checklists: `checklists/design.md` (direction worksheet, anti-patterns, polish), `checklists/qa.md` (browser QA pass), `checklists/ship.md` (deploy and handoff).

## Ground rules

- **Evidence before claims.** Never say "done", "works" or "fixed" without having just run the check that proves it and read its output. If you could not verify something, say exactly what was not verified.
- **Plain English to the owner.** Explain choices in one or two sentences, no jargon. Ask before anything that costs money, publishes publicly, or touches their accounts. They log in themselves; never ask for or type a password.
- **Real over invented.** Use the owner's real words, photos, prices and proof. Never invent testimonials, customer counts, logos, reviews or claims. If content is missing, mark it clearly and list it for the owner.
- **Bold but restrained.** One memorable idea, executed fully; everything around it quiet. No gradients, glassmorphism or glow effects by default. Mobile first.
- **Bounded loops.** Build, inspect, fix in batches, re-inspect. Two full QA rounds, then report what remains instead of polishing forever.

## 1. Clarify and write a one-page spec

Ask only what changes the build, in one round of 3 to 5 questions (a second round only if an answer opens a real gap). Propose a sensible default with each question so the owner can just say yes. Typical questions:

- Who is it for, and what should they do on it (book, buy, call, sign up, read)?
- What do you already have: logo, photos, brand colors, text, a document, a site you like?
- Does it need to collect anything (form, payment, accounts)? Where should that information go?
- Do you have a domain and a preferred host? (Default: free hosting, add a domain later.)

If the owner gave you files (a PDF, a deck, a brand guide, photos), open and look at every one before proposing anything. Their material sets the direction.

Then write the spec in plain English, short enough to read in a minute, and get a yes before building:

```markdown
# <Name>: one-page spec
For: <who>, who want to <job>.
The one thing a visitor must do: <primary action>.
Pages / screens: <list, each with its purpose>.
Must work: <features, e.g. contact form that emails owner@..., price calculator>.
Content we have / still need: <list>.
Look and feel: <3 words + any reference the owner likes>.
Lives at: <host / domain>.
Done when: <testable outcomes, e.g. "form message arrives in the owner's inbox">.
Not in v1: <explicitly cut items>.
```

Scope rule: if the request is really three products, build the smallest version that delivers the primary action, and list the rest under "Not in v1".

## 2. Pick the simplest stack that works

Every framework, build step and dependency is a maintenance bill for someone who cannot code. Pick the first row that fits:

| Need | Stack |
|---|---|
| Landing page, portfolio, menu, event, small business site | Plain HTML + CSS (+ a little JS). One `index.html` or a few pages in `site/`. No build step. |
| Contact or signup form | Static site + a form service (Netlify Forms with `data-netlify="true"` on Netlify, or Formspree). No server. |
| Take payments | Stripe Payment Links or Checkout (hosted). Never build card fields yourself. |
| Interactive tool without accounts (calculator, quiz, planner) | Single page, vanilla JS in `app.js`, logic in a separate `logic.js` module so it can be tested; `localStorage` if it should remember things. |
| Blog or content that grows past ~10 pages | A static site generator (Astro or Eleventy), still deployed as static files. |
| Real app: accounts, shared data, many users | Next.js (or Vite + React) + a hosted backend (Supabase for auth and Postgres), on Vercel. Only when the spec truly needs it. |

Host: Netlify, Vercel, Cloudflare Pages or GitHub Pages (free tiers fit most small sites). Tell the owner the choice and the reason in one sentence.

Project layout for static sites: `site/` (what gets deployed: `index.html`, `styles.css`, `app.js`, `img/`, `fonts/`, `404.html`, `favicon.svg`), `tests/` (logic tests), `README.md` (the handoff note).

## 3. Design direction, before any code

Generic output comes from skipping this step. Fill in Part 1 of `checklists/design.md` and show the owner the direction block. The essentials:

1. **Ground it in their world.** Who visits, on what device, in what light, what they must do in 5 seconds, what they should remember. The subject's own materials, places, objects and vernacular are where distinctive choices come from; the category's usual look is where generic ones come from.
2. **Pick the mode.** Sell (landing, pricing: can be loud), Use (app, tool: clarity and calm win), Read (menu, docs, articles: comfortable reading), Show (portfolio: the work leads, the interface recedes).
3. **Commit the system:**
   - **Type:** one or two families, chosen for this subject (not the defaults you reach for everywhere), with a clear scale, e.g. 14 / 16 / 20 / 28 / 40 / 64. Body 16px or more, 45 to 75 characters per line.
   - **Color:** 4 to 6 named values with jobs (ground, surface, ink, muted ink, one accent for the primary action, state colors). Decide light or dark from the scene, not the category. Prove contrast with `python3 tools/contrast.py --css site/styles.css --pair ink:ground --pair muted:ground`.
   - **Space:** a 4px-based scale (4 8 12 16 24 32 48 64 96 128). Tight within groups, generous between them.
   - **Shape and depth:** a small radius scale (not one radius on everything); shadows only where they explain depth.
   - **Motion:** one signature moment, 150 to 250 ms ease-out feedback elsewhere, everything visible without JavaScript, `prefers-reduced-motion` respected.
   - **Signature:** the one bold element. Spend the boldness there and keep everything else disciplined.
4. **Self-check against the defaults.** If the design could be guessed from the category alone, revise that part and say what you changed. Read Part 2 of `checklists/design.md` (the AI-slop list) and remove anything you reached for out of habit.
5. **Write the tokens first** as CSS custom properties, then build every component from them:

```css
:root {
  --ground: #f3efe6; --surface: #fffdf8; --ink: #1d1b16; --muted: #5d584d;
  --accent: #b4441f; --focus: #1f5fb4;
  --font-display: "Your Display", Georgia, serif; --font-text: "Your Text", system-ui, sans-serif;
  --s1: 4px; --s2: 8px; --s3: 12px; --s4: 16px; --s5: 24px; --s6: 32px; --s7: 48px; --s8: 64px; --s9: 96px;
  --r1: 2px; --r2: 6px; --r3: 12px;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}
```

(Those values are placeholders to show the shape, not a palette to reuse.)

Fonts: Google Fonts with `display=swap` and a `preconnect`, or self-hosted woff2. At most 4 weights in total. Icons: one SVG set (Lucide, Phosphor, Heroicons) at one stroke weight, never emoji.

## 4. Build in small verified steps

Plan 3 to 8 slices, each ending in something visible and checkable, for example: (1) skeleton with tokens, header and footer; (2) hero and primary action; (3) remaining sections with real content; (4) form wired end to end; (5) states, 404 and meta tags. Share the plan in a few lines, then build one slice at a time.

Start the preview once and keep it running:

```bash
python3 tools/serve.py site/            # prints http://127.0.0.1:8000/
python3 tools/serve.py site/ --lan      # also prints a URL to open on your phone (same Wi-Fi)
```

After every slice, before the next one:
1. Reload and look at it at 375 and 1440 (see stage 5 for how), with the console open: zero errors.
2. `python3 tools/sitecheck.py site/` and fix any new errors.
3. Commit a save point: `git add -A && git commit -m "slice 2: hero and booking button"` (run `git init` once at the start; explain commits to the owner as save points they can return to).

**Test-first for logic.** Anything that calculates, validates, filters or transforms data (prices, totals, dates, form validation, quiz scoring) lives in `site/logic.js` as plain exported functions, and gets a failing test before the code:

```js
// tests/logic.test.mjs  (run with: node --test tests/)
import { test } from "node:test";
import assert from "node:assert/strict";
import { quote } from "../site/logic.js";

test("weekend bookings add the 15% surcharge", () => {
  assert.equal(quote({ guests: 4, perHead: 30, weekend: true }), 138);
});
```

Run it, watch it fail for the right reason, write the smallest code that passes, run the whole suite again. No Node? Put the same assertions in a `tests.html` page that prints PASS/FAIL and check it in the browser.

**Build rules that prevent the usual bugs:**
- Semantic HTML first: `header`, `nav`, `main`, `footer`, one `h1`, real `<button>` for actions and `<a href>` for navigation, `<label>` for every field.
- Every `<img>` gets `alt`, `width` and `height`; CSS `img { max-width: 100%; height: auto; }`.
- Grid columns as `minmax(0, 1fr)`, not bare `1fr`, so images and long words cannot blow the layout wider than the phone.
- Content is visible by default. Entrance animations must not hide content until a script or scroll observer runs (hidden tabs and screenshot tools never trigger them). Prefer CSS `@starting-style` or animations that start from visible.
- Forms: `type="email"`, `inputmode`, `autocomplete`; inline error messages in text; disable the button while sending; a clear success state.
- Secrets never go in front-end code. API keys go in the host's environment settings and server-side functions.

**When something breaks:** find the cause before changing code. Reproduce it, read the actual error, form one hypothesis, test it with the smallest probe. If three fixes in a row fail, stop: the approach is wrong, so step back and rethink it (and tell the owner if it changes the plan).

## 5. QA in a real browser at 375 / 768 / 1440

Follow `checklists/qa.md`. The short version:

1. **Automated sweep:** `python3 tools/sitecheck.py site/` until it reports zero errors; review each warning.
2. **Screenshots at three widths, every page.** Use your browser tool if the harness has one (Claude in Chrome or the Claude Code preview browser: resize to 375x812, 768x1024, 1440x900). Otherwise Playwright's CLI, which emulates true viewports:

   ```bash
   npx playwright screenshot --viewport-size=375,812 --full-page http://127.0.0.1:8000/ qa/home-375.png
   ```

   Do not use `chrome --headless --window-size=375,...` for mobile: Chrome lays the page out at a ~500px minimum width and crops the image, so it looks like a phone while hiding phone bugs. Open and actually look at every screenshot.
3. **Every flow by hand:** each link and button, each form (empty, invalid, long, special characters, valid, double submit), empty/loading/error/success states, keyboard only (visible focus, logical order, Escape closes things), console clean after every interaction.
4. **Design polish pass:** Part 3 of `checklists/design.md` (first look, squint test, states, themed browser surfaces, remove one thing).
5. **Fix loop:** log issues with severity (critical, high, medium, low), fix in that order one at a time, write a failing test first for logic bugs, re-verify each fix at all three widths. Then one more full sweep. Two full rounds is the budget; report anything left.

## 6. Ship, then hand off

Follow `checklists/ship.md`:

1. Pre-flight: real content only, `python3 tools/sitecheck.py site/ --strict` clean, forms tested end to end, title/description/og:image/favicon/404 in place, no secrets or localhost URLs.
2. **Ask the owner before deploying** (it is public). They create and log into the hosting account themselves. Then deploy, for example `npx netlify-cli deploy --dir=site --prod` or `npx vercel --prod` (commands for each host are in the checklist).
3. Verify live: `python3 tools/sitecheck.py https://<live-url> --external`, the screenshot pass on the live URL, one real form submission, a look on a real phone.
4. Write the handoff note (template in `checklists/ship.md`) into `README.md` and paste it in chat: live URL, where it is hosted and who owns the account, how to change text/photos/prices, how to redeploy, where form messages go, costs and renewals, what not to touch, known limits.

Final message to the owner: the live link, what was verified (with the checks you ran), anything not verified, and the next steps.

## Failure handling

- **Owner cannot or will not create a hosting account:** deliver the `site/` folder as a zip plus the handoff note, and explain the drag-and-drop upload for their chosen host.
- **No browser tool and no Playwright:** say plainly that visual QA at 375/768/1440 was not done, run sitecheck anyway, and ask the owner to open the preview on their phone and laptop (`serve.py --lan`) and describe what they see.
- **Tests or sitecheck still failing at the deadline:** do not ship silently. Ship only with the owner's explicit OK, and list the open issues in the handoff note.
- **Request needs things you should not build alone** (card payments with custom fields, medical or legal data, multi-tenant SaaS security): use hosted services (Stripe Checkout, a form service, Supabase auth) and recommend a professional review.

## Limits

- The tools check what is mechanical: links, assets, tags, attributes, contrast numbers. Taste, clarity and whether the page persuades still need your eyes on real screenshots.
- `sitecheck.py` reads the HTML the server sends; it does not run JavaScript. Pages built in the browser (single-page apps) need the browser pass to be checked properly.
- A clean report is not a guarantee of sales, search ranking or full WCAG compliance. It removes the common, avoidable failures.
- The skill never logs into the owner's accounts, enters payment details, or publishes without the owner's go-ahead.

## Credits and going deeper

BUILD is original guidance synthesized from studying these skills. No text is copied from them. Install them for the deep versions:

| Skill | What BUILD learned from it | Install (from each project's README) |
|---|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0) | Design direction from the audience's world, visitor modes, color strategies, the craft floor, anti-pattern detection, bounded inspection rounds | `npx impeccable install` (or in Claude Code: `/plugin marketplace add pbakaus/impeccable`) |
| [anthropics/skills: frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (Apache-2.0, per its LICENSE.txt) | Plan a compact token system before code, review it against the brief, spend boldness in one place, writing as design | `/plugin marketplace add anthropics/skills` then `/plugin install example-skills@anthropic-agent-skills` |
| [garrytan/gstack](https://github.com/garrytan/gstack) (MIT) | Real-browser QA with health scoring, issue taxonomy, fix-verify loops with stop rules, design review checklists, deploy setup | `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup` |
| [obra/superpowers](https://github.com/obra/superpowers) (MIT) | Clarify and get approval before building, bite-sized plans, test-first red/green, root cause before fixes, verification before completion | `/plugin install superpowers@claude-plugins-official` |
