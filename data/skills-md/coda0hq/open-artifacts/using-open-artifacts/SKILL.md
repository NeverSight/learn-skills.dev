---
name: using-open-artifacts
description: "Publish and maintain self-contained HTML, Markdown, or React artifacts as shareable URLs. Use when a user asks to publish a report, writeup, dashboard, prototype, visualization, or document; update an existing artifact; inspect a published artifact; or review watched-source drift in .artifacts/manifest.json or manifest.local.json. Artifacts support stable channel URLs, version history, light/dark themes, optional client-side password encryption, and deterministic Recipe builds. Source changes are detected by status and an optional Claude Code Stop hook; they are not edited or republished automatically. Do not trigger for generic file uploads, screenshots, SBOMs, build tarballs, Linear items, or Claude API content blocks."
---

# Open Artifacts

Publish a self-contained HTML, Markdown, or React artifact the user can share
by URL. The viewer keeps the artifact body in a sandboxed iframe and owns the
service chrome, theme switcher, version picker, comments, and optional Live or
Handoff controls. Artifacts keep immutable versions; a channel can keep one URL
across later publishes.

The publishing CLI is bundled at `scripts/artifact.mjs` next to this file. Skill
install locations vary by agent (for example, `.claude/skills/` or another
Agent Skills directory), so resolve the directory containing this `SKILL.md`
as `SKILL_DIR`, then use a task-local `ARTIFACT_CLI="$SKILL_DIR/scripts/artifact.mjs"`.
Run `node "$ARTIFACT_CLI" ...` from the project root. There is no globally
installed `artifact` binary, and Recipe paths are resolved relative to the
project-root working directory. The CLI requires Node.js 22 or newer.

## Setup (once per project)

The CLI needs an instance URL, resolved in this order: `--api` flag,
`OPEN_ARTIFACTS_URL`, project `.artifacts/config.json` or
`.artifacts/config.local.json`, then `~/.config/open-artifacts/config.json`.
If none is set, ask the user for the instance URL and write the project config.
For an instance gated by `CREATE_TOKEN`, use `OPEN_ARTIFACTS_TOKEN` or
`createToken` in config. For a hosted/SaaS instance such as coda0.com, run
`node "$ARTIFACT_CLI" login`; see [auth.md](references/auth.md) for the
browser flow. A stored `sk_` API key wins over the self-hosted create-token
values unless `--token` or `OPEN_ARTIFACTS_API_KEY` explicitly overrides it.

Every artifact is built from a JSON Recipe plus ordered fragments. Read
[recipe.md](references/recipe.md) before creating or updating one.
Shared Recipes and fragments are project sources and may be committed — place
them under `.artifacts/recipes/` and `.artifacts/fragments/`. Local or
encrypted sources live under `.artifacts/recipes.local/` and
`.artifacts/fragments.local/`.

State lives in `.artifacts/`: Manifest v2 records only publication state and
build hashes; `credentials.json`, local manifests, private Recipes/fragments,
and previews are gitignored. On the **first `create` in a project**, ask
whether the artifact should be local and **recommend local**. Record the
choice in `artifact.local` and place the Recipe/fragments accordingly.

**Run state-mutating commands one at a time — never concurrently.** This
includes `create`, `update`, `delete`, `migrate`, `ack`, `auto-update`,
`login`, and `logout`; `install-hook` also writes project settings.
`credentials.json` and the manifests are updated with an unlocked
read-modify-write. The write re-reads immediately beforehand, which closes the
window around each command's network round-trip, but two commands whose writes
truly interleave can still lose one. A lost write token is unrecoverable — no
endpoint re-issues one — so serialize them. This matters most for a
"regenerate everything" pass: loop, don't fan out.

If the user has no instance yet, point them at
[deployment.md](references/deployment.md) — it has the three ways to get
one (use the public shared instance with zero deployment setup, self-host on their own
Cloudflare account, or share a team instance) and a trust-model table to help
them choose based on content sensitivity. Don't deploy on their behalf unless
they ask.

## When to publish an artifact

Publish when the user asks for something shareable or standalone: reports,
dashboards, documentation pages, visualizations, demos, long-form writeups.
Do not publish for short answers, code snippets, or content the user will
read once in the conversation. When unsure, answer inline and offer to
publish.

## Isolate content generation when the harness supports it

Publishing or republishing means reading project resources and design
references, authoring a Recipe and fragments, validating the deterministic
build, and running the CLI. If the host provides a sub-agent or task primitive,
use it for this content-generation workflow so the parent conversation only
needs the result. This is a workflow optimization, not a CLI requirement; when
the host has no sub-agent facility, do the same workflow in the current agent.

Use a separate task for both `create` (first publish) and `update` (republish),
and for the design work that leads to them, when available. In Claude Code this
can be an Agent task; other harnesses may provide an equivalent. Do not invent
a fake isolation boundary when the current agent is the only available worker.

Give the worker everything it needs to work alone, then let it work:

- The brief: what's being published or updated, for whom, and why.
- If updating: the artifact id. The worker runs
  `node "$ARTIFACT_CLI" show <id>` to read the current published version as its
  starting reference —
  for a locked design, the direction comment at the top of that page states
  what must not change. "Locked" means the **visual direction** (register,
  palette hue family, layout posture) must not change — it does **not** exempt
  the artifact from validation gates. A contrast or CSP check added after the
  original publish can retroactively fail a previously-passing token; the
  refresh must then nudge the offending token within the same hue (e.g. darken
  the light-theme `--accent` a few lightness steps) so the page passes the gate
  while staying visually the same direction. (For an encrypted artifact, `show`
  decrypts locally with the password stored at create time in
  `credentials.json`, so the plaintext is recovered without re-prompting the
  user.) It then reads the Recipe recorded in Manifest v2, its fragments, and
  the project files its `scope` covers.
- Any explicit publication requirements. Put title, description, favicon,
  scope, channel, watch globs, level, Canvas mode, locality, and auto-update
  in the Recipe. Keep passwords out of it.

The worker does the entire rest of the workflow itself — explore resources,
plan, read [design.md](references/design.md), [recipe.md](references/recipe.md),
and relevant mode references;
write the Recipe and fragments; run `validate`; optionally build a preview;
run `create`/`update`; verify; and return **only** a short summary: the URL,
version number, and one line on what changed. The parent relays that to the
user and should not independently rerun the publish or carry the design
reasoning in its own context.

The lightweight bookkeeping commands — `status`, `ack <id>`,
`auto-update <id> on|off`, `list`, `show <id>`, `whoami`, `logout`, and
`install-hook` — don't author content and can run directly; only the
content-generation part of `create` and `update` benefits from isolation.

## Optional reference DNA (agent-side only)

When the user explicitly says **“study this as reference DNA for the artifact”**,
**“use this design DNA”**, or asks to extract an Artifact direction from a
screenshot or public URL, read [reference-dna.md](references/reference-dna.md)
before authoring. A normal citation, source URL, or link collection does not
trigger this workflow.

For a URL, the parent conversation obtains the user's ownership/public-reference
attestation before delegating a study task. The study task produces a diagnosis
only; it never publishes or writes a sidecar without a later explicit adoption
decision. The approved sidecar is a static Recipe input, is hashed and watched,
and never appears in the Artifact body or runtime. Read
[study.md](references/study.md) for source safety rules.

## How to design the page

You are an expert designer producing design artifacts in HTML. **HTML is your
tool, not your medium**: when the brief is a dashboard, be an information
designer; when it's a report, be an editorial designer; when it's a
prototype, be an interaction designer. Don't default to "a web page"
treatment for everything.

Workflow: (1) understand the brief — output kind, fidelity, audience, any
brand/design system; (2) explore resources & find what only this subject has —
identify the authentic domain data, physical metaphors, and unique vocabulary
(the artifact-subject-first ethos); (3) plan out loud — a one-line design read,
the core idea tying that unique subject to the layout, the scene sentence that
picks light vs dark, 4–6 named OKLCH values, type roles, and a layout concept;
(4) build with real content, never lorem ipsum, applying mathematical concentric
radii (`outerRadius = innerRadius + padding + borderWidth`), optical alignment,
and mobile-native touch ergonomics (100dvh, `@media (hover: hover)`,
`-webkit-tap-highlight-color: transparent`, `touch-action: manipulation`, inputs
≥ 16px); (5) run the ship gate from `design.md` once at the end — structural
grep, the P0 checklist (contrast in both themes, 360px viewport, concentric
radii, mobile-native ergonomics, high-contrast resilience, banned tropes,
states, reduced motion, copy audit), the 14-pass visual critique, the break-ui
worst-case data check (from `quality.md`), and the five-dimension critique
(philosophy / hierarchy / execution / specificity / restraint) — fix anything
under 3/5, re-score once, publish. Do not loop on renders.

**Read [design.md](references/design.md) before writing a page.** It
has the full design philosophy: the brand-vs-product register split (earned
familiarity vs distinctiveness), the three waves of anti-AI-slop bans, the shared token
contract (`references/tokens.css`, injected by the Recipe
builder; override identity tokens in the theme fragment), an
installed-font specimen library (the CSP blocks *downloading* fonts, not the
OS library — Iowan, Charter, Avenir, Optima and friends are available), a
20-direction library with ready-to-paste OKLch palettes, concentric border-radius
and optical alignment math, surface depth and shadow recipes, guidance for visual material
under the CSP (SVG charts/diagrams/typographic set-pieces instead of
text-only slabs), a component contract written against tokens, the viewer
frame specifics (sticky header height, theme stamping), and the ship gate
run before every publish.

**For an HTML Artifact with a visual direction, read
[quality.md](references/quality.md) before writing fragments.** It supplies a
format-aware Design Brief, the 14-pass visual critique, the Break-UI worst-case data
resilience catalog (people/locales, unbreakable URLs/strings, numbers/currencies,
empty/volume states), structural choices for brand-register artifacts, CSP-safe
visual-material decisions, the build's static quality profile, and the `smoke` command for 320/375/414/768px
rendering. Canvas remains governed by `canvas.md`; Markdown retains the
viewer-owned `.oa-md` treatment. When a user explicitly asks to learn from a
screenshot or URL, read [reference-dna.md](references/reference-dna.md) before
inspecting the reference. It routes to [study.md](references/study.md) for
source safety, keeps remote content untrusted and agent-side, and never puts a
fetch or remote asset in an Artifact.

### Production level (1 / 2 / 3)

Every artifact is built at one of three levels. Pick from the brief and record
it as `artifact.level: 1|2|3` in the Recipe:

- **Level 1 — simple:** typography-led documents (reports, articles, API
  references, notes). No flashy hero, minimal JS. Default for "read once"
  content. Wrap the body in `<main class="oa-prose">` — the contract's prose
  baseline (measure cap, padding, heading/code styling) — so a doc that
  defines tokens but forgets structure does not ship bare.
- **Level 2 — interactive:** dashboards, docs sites, demos, prototypes.
  Stateful in-memory JS, navigation, copy buttons, expandable sections,
  subtle transitions. Default when unsure **and the brief is interactive** —
  if the brief is mostly text to read, level 1 is the safer pick (it carries a
  structure baseline; L2's structure is author-supplied). Before building L2+,
  read `references/interaction.md` for the eight-state
  contract, focus visibility, hit targets, form patterns, and waiting states.
- **Level 3 — rich:** landing/marketing pages, product showcases. Orchestrated
  motion — load sequences, scroll reveals, view transitions — **all native
  browser APIs, no external libraries** (the strict CSP blocks CDNs). Read
  `references/motion.md` for the native motion pattern
  library before building L3 (`interaction.md` applies here too).

Don't gold-plate a doc as L3; don't ship a landing page as L1. The level
sets the component contract and motion budget, not just "how much
animation."

### Canvas mode

Orthogonal to level, `artifact.canvas: true` swaps the page *shell* for an
infinite spatial plane of pan/zoom **frames**. It composes with any level:
level 1 is spatial notes, level 2 a multi-frame prototype (the default use),
and level 3 a canvas-as-showcase. Read
`references/canvas.md` before building one -- it has the
complete vendored runtime (CSS + vanilla JS) with momentum and pinch physics,
an optional presenter tour, connector spotlighting, and `#frame-id` deep
links, plus the frame and freeform contracts and a canvas ship-gate.

### Optional viewer workflows

Live editing is available only when the instance binds `LIVE_DO`; it requires
the artifact owner's `sk_` session and edits local Recipe sources before an
in-place `update --live`. Read [live.md](references/live.md) before starting a
live session. A deploy with `OPEN_ARTIFACTS_HANDOFF=1` may also expose host-side
webcam/microphone recording and playback; it is viewer chrome, not a Recipe
format or an artifact-side API. Both surfaces are optional and may be absent
on self-hosted instances.

## Authoring content — hard constraints

The artifact frame has a strict CSP: authored code cannot make external
requests (CDN scripts, remote images, fetch/XHR/WebSockets):

- Inline all CSS and JS; embed images and fonts as `data:` URIs. Use system
  font stacks or inline a face as a `@font-face` data URI. On a deploy that set
  `OPEN_ARTIFACTS_WEB_FONTS="1"`, a web font may also be loaded same-origin via
  the `/fonts/<family>--<weight>[--italic]` proxy or directly from an allowlisted
  font CDN (Fontshare / Google Fonts). Mermaid is always served from the
  self-hosted, allowlisted `<script src="/vendor/mermaid.runtime.js">` path
  (a regular, non-module script) when used — it is not tied to the web-font
  flag. See `references/fonts.md` and `references/scripts.md`. The build gate restricts
  `@font-face`/`@import` to those font hosts and `<script src>` to the
  allowlisted same-origin `/vendor/...` bundle, so no arbitrary external host is
  ever reachable.
- **Icons: prefer [Remix Icon](https://remixicon.com/).** Read
  `references/icons.md` for a vendored ~90-icon inline-SVG
  subset (navigation, actions, status, social, common UI). Copy the whole
  `<svg>` block inline — it uses `fill="currentColor"` so it inherits color.
  Never link the Remix Icon CDN (the CSP blocks it); only inline SVGs. To sit
  an icon next to text, wrap them in the contract's centered row
  (`<h2 class="oa-ico-text"><svg class="oa-ico">…</svg> Title</h2>`) — a bare
  icon in a heading sits low and the build fails it.
- Do not use localStorage/sessionStorage (the sandbox blocks them); keep
  state in memory.
- Put the concise title in `artifact.title`.
- Support both themes. The builder injects `references/tokens.css`; author a
  theme fragment with an unlayered `:root` block (light) plus a
  `:root[data-theme="dark"]` block, both mandatory. The token contract only
  supplies *variables* — it does not style your elements. For a level 1 HTML
  document, wrap the body in `<main class="oa-prose">` to pick up the prose
  baseline (measure cap, page padding, heading scale, `code`/`pre`/`table`
  styling) the contract ships. `validate` fails an L1 non-canvas page with no
  measure cap, since the default is a full-width doc with browser-default
  spacing. Markdown needs nothing — the viewer wraps it in `.oa-md`
  automatically. The viewer chrome (service header, theme toggle, brand chip,
  version picker, comments, and any deploy-enabled Live/Handoff controls) is
  injected by the host at serve time — never hand-author it.
  It follows your identity palette automatically via the token contract's
  chrome bridge, so do **not** override `--oa-*` viewer tokens in the theme
  fragment. L2/L3 may be full-bleed by design; author their structure
  explicitly.
- Responsive: no horizontal body scroll; wide tables/code get their own
  `overflow-x: auto` container.

### Authoring Markdown

Most of the hard constraints above are **HTML-specific and do not apply to
Markdown**. A Markdown Recipe publishes the body `.md` **verbatim** — the
builder does not inject `references/tokens.css`, does not wrap the content in
a `<style>` block, and runs none of the HTML validation gates (no theme
fragment, no `:root`/`[data-theme="dark"]` requirement, no contrast check, no
L1 measure-cap, no banned-trope grep). The viewer wraps the raw Markdown in
`.oa-md` and renders it client-side with the viewer's default tokens, so:

- `document.theme`, `document.fragments.theme`/`styles`/`scripts` must all
  be **omitted** — `validate` *rejects* a Markdown Recipe that carries a
  theme/styles/scripts fragment (error: "Markdown recipes only support body
  fragments"). Supply `document.fragments.body` with one or more `.md` files
  only; `document.theme` may be omitted or `null`.
- You cannot theme, style, or script a Markdown artifact; if you need
  interaction, identity tokens, or a measure cap beyond the default, author it
  as HTML instead.
- `artifact.title` still drives the page title and OG card; the first `#`
  heading is also extracted as a fallback title.
- Both-themes support is automatic (the viewer's `.oa-md` shell reads light/dark
  tokens); nothing for you to author.

Markdown files (`.md`) are rendered client-side; HTML is best for anything
interactive or designed.

**Avoid AI-slop tropes across all three waves** (`design.md` has the full
match-and-refuse registry):
- Wave 1 (SaaS clichés): violet/indigo hero gradients and glowing radial washes,
  gradient text (`background-clip: text`), decorative glassmorphism, 3 identical
  feature cards with circular icon badges, soft grey drop shadows.
- Wave 2 (Pseudo-system tells): side-stripe accent borders, an uppercase eyebrow
  above every single heading, pill badges above heroes ("New", "Beta"), one word of
  the headline forced into italic serif or accent color, bento grids as default.
- Wave 3 (The "fix" that became the look): terracotta/rust/clay accent on
  yellow-cream/linen/parchment ground; broadsheet cosplay (hairline rules everywhere,
  zero radius, fake archival posturing); monospace micro-labels as "technical"
  costume on non-technical briefs; index numbering scaffolding (`01 / 02 / 03`,
  `(001)`, `Step 02`).
- Copy & structure tells: marketing buzzwords ("unlock", "supercharge", "seamless",
  "elevate", "effortless", "cutting-edge", "all-in-one", "empower"), correction
  clichés ("not just X, it's Y"), tricolon headlines ("Design. Build. Ship."),
  staccato aphorisms ("Not X. Y."), stock section order, everything centered,
  headings that overflow at mobile width, and invented metrics/testimonials ("Acme Corp").
  An honest placeholder beats a fake stat. Verify contrast (body ≥ 4.5:1 in both themes)
  and never ship muted gray on a tinted near-white.
Full-viewport sections use `min-height: calc(100dvh - var(--oa-header-h,
0px))` — the viewer's header sits above the frame that holds your content, so
`--oa-header-h` is `0px` inside it. Modern CSS is fully available
inline — `text-wrap: pretty/balance`, CSS Grid, container queries,
`color-mix()`, `:has()`, view transitions, `clamp()` for fluid type.

## Publishing

*(Run this in the content-generation task when the harness provides one; run
from the project root.)*

Create a Recipe and ordered fragments, validate them, then publish:

```
node "$ARTIFACT_CLI" validate .artifacts/recipes/app-interactions.recipe.json
node "$ARTIFACT_CLI" create .artifacts/recipes/app-interactions.recipe.json
```

The Recipe owns favicon, scope, channel, watch globs, level, Canvas mode,
locality, and auto-update. Keep the favicon stable. Use a kebab-case channel
to reuse one URL across `create` calls; use `null` to mint a new URL. `create`
composes in memory and sends one final payload. It prints the shareable URL.

Manifest v2 records the Recipe path and Recipe/input/output hashes only after
the publish succeeds. Write tokens and channel tokens remain in the
gitignored credentials file.

### Live mode after publishing

On a live-capable instance (the CLI prints a "live mode" tip right after
`create` when the instance binds `LIVE_DO` and you are logged in), **start the
watcher by default** once the artifact is published:

```
node "$ARTIFACT_CLI" live <ID> --watch
```

Run it as a background task (per-harness patterns in
[references/live.md](references/live.md) — "Harness note") and keep it running
for the session. **Your only job in a live session is to poll** — you never
operate the viewer page yourself (no browser automation, no clicking Live,
picking elements, or typing prompts on the artifact page). The user drives the
viewer: they open the artifact URL, click Live, pick elements, then either type
a change for each (a `generate` event) or **edit the element's text inline**
("Edit text", an `edit` event) — see the Copy edits section in
[references/live.md](references/live.md). Your watcher prints each event for
you to act on (edit the Recipe sources, `update`, reply `done`). The viewer's
Live button shows `Connected` while your watcher is connected, so the user can
see an agent is online before they start picking; while a pending event is
leased to you, the toggle's accent dot pulses ("Agent is working on an edit");
if the watcher drops, the toggle shows an amber pulsing dot with the startup
hint. If no watcher is connected, clicking Live still opens the picker and
also shows a copyable startup prompt; start the watcher before submitting an
edit. Read [references/live.md](references/live.md) before the session.

## Updating

*(Run this in the content-generation task when the harness provides one; run
from the project root.)*

```
node "$ARTIFACT_CLI" update <id> [recipe.json] [--label "what-changed"]
```

Same URL, new version. Without a path, `update` uses the Recipe recorded in
Manifest v2. Update its fragments after reading project sources and, when
useful, compare with `show <id>`. The CLI rebuilds and validates in memory,
then publishes once. The first positional argument is the short artifact id,
not a Recipe path. A legacy Manifest v1 entry is migrated automatically; run
`migrate <id>` first only when you want to inspect or edit the generated sources
before publishing. A 409 version conflict means another writer published
first; review the current version and use `--force` only when overwriting it is
intentional. `--label` is capped at 60 UTF-8 bytes.

For a change requested through Live, use `node "$ARTIFACT_CLI" update <id> --live`
after editing the Recipe. This replaces the currently served version in place:
an artifact at v10 remains v10, and a later ordinary `update` creates v11.

`build <recipe> --output <path>` writes an explicit local preview; add
`--standalone` only for an HTML Recipe. `list`, `show <id> [--v N]`, and
`delete <id>` cover common read and cleanup operations. `delete` removes the
server artifact and its local manifest entry.

## Detecting stale artifacts (republish only with intent)

Source changes never edit or republish an artifact by themselves. After the
first `create` in a project, **ask the user** whether to install the optional
Claude Code Stop hook — don't install it silently. If they agree, run
`node "$ARTIFACT_CLI" install-hook`; it adds a `Stop` hook to
`.claude/settings.json` that surfaces drift at the end of a turn. Other agent
harnesses should use their own hook integration or run the manual check:

```
node "$ARTIFACT_CLI" status
```

For each artifact reported stale, decide whether the changed files affect its
recorded scope:

- **They affect it** → regenerate the page content to reflect the current state
  of the project and run `update`. That republishes and refreshes the snapshot.
  Regenerating is content generation, so use a separate task when the harness
  provides one, per "Isolate content generation when the harness supports it"
  above — including when this judgment call is made autonomously via the Stop
  hook, not just when a human asks directly.
- **They don't** (e.g. a refactor with no behavior change for a user-facing
  scope, or a design direction locked in the scope) → run
  `node "$ARTIFACT_CLI" ack <id>`. This advances the snapshot baseline offline —
  no republish — so the same unrelated change stops being reported every turn.
  `ack` is a pure manifest mutation, not content generation, so it's fine to
  run directly. Don't just leave it stale: with the hook installed it
  re-nudges on every future turn until the baseline moves via `update` or
  `ack`.

### Opting a specific artifact into the automatic loop

By default, the Stop hook (once installed) surfaces **every** stale, watched
artifact — the regenerate-vs-`ack` judgment above still applies to each one,
unchanged. If the user wants the hook to stay quiet about most artifacts and
only nudge about specific ones, turn on that artifact's auto-update flag:

```
node "$ARTIFACT_CLI" auto-update <id> on
```

This does not change how you decide what to do once an artifact is flagged —
it only changes **which artifacts the Stop hook is allowed to flag at all**:

- Opt-in, per-artifact, and fully isolated: it flips one manifest entry's
  `autoUpdate` field and never reads or writes any other entry's state. Off
  by default — artifacts never toggled (or created before this feature) are
  treated as off, and the hook stays completely silent about them even
  while stale.
- A plain, human-run `node "$ARTIFACT_CLI" status` (no `--hook`) is never
  filtered by this flag — it always reports every stale watched artifact.
  Only the autonomous, no-human-present Stop-hook path narrows to opted-in
  artifacts.
- Turning it **on** requires a write token to already exist for that artifact
  (fails clearly if not), and installs the Stop hook automatically if it
  isn't already present. Unlike `create`'s hook hint, which never installs
  anything for you, running `auto-update <id> on` *is* the user's consent to
  install it — go ahead, and the CLI prints a confirmation when it does.
- Turning it **off** (`node "$ARTIFACT_CLI" auto-update <id> off`) leaves any
  installed hook in place; it just stops mentioning this artifact.

## Password protection

```
node "$ARTIFACT_CLI" create .artifacts/recipes.local/q3.recipe.json --password "..."
```

Set `security.encrypted: true` and a kebab-case
`security.passwordCredential` in the Recipe. Encrypted Recipes and fragments
must use the private `.artifacts` source directories.

Content is encrypted locally (PBKDF2 600k + AES-256-GCM); the server stores
only ciphertext and viewers decrypt in the browser. Share the URL and the
password through different channels. Prefer the named environment variable or
gitignored credentials file over a command-line password when shell history or
process listings are a concern. The CLI resolves the named credential from
`--password`, its `OPEN_ARTIFACTS_PASSWORD_*` environment variable, or the
gitignored credentials file. Passwords never enter Recipes or Manifests.
Title and favicon remain plaintext service metadata, so keep them
non-sensitive.

## Reading back

Raw content lives under the **API path only** —
`GET <instance>/api/artifacts/<id>/raw`. The viewer path
`GET <instance>/a/<id>` serves the rendered viewer page (HTML), not the raw
bytes; `/a/<id>/raw` is not a route and returns 404. Don't confuse the two:
`/a/<id>` = the page a browser renders, `/api/artifacts/<id>/raw` = the stored
content as published.

`GET <instance>/api/artifacts/<id>` returns metadata and version history;
`GET <instance>/api/artifacts/<id>/raw` returns the stored content
(`?v=N` for older versions). For a non-encrypted artifact that is the page
itself (`text/plain`); for an encrypted artifact it is a JSON ciphertext
envelope — run
`node "$ARTIFACT_CLI" show <id> [--v N] [--password ...]` instead, which
decrypts locally using the supplied or stored credential. Viewer URLs also
accept `?v=N`.
