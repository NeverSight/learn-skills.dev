---
name: generate-docs-from-source
description: Generate accurate DocsPress-compatible Markdown documentation from an existing source-code repository, including maintained API versions when required. Use when a project has incomplete, stale, or no documentation and an agent must derive installation, configuration, guides, API or CLI references, architecture, troubleshooting, DocsPress Gutenberg blocks, and a safe publication workflow from code and tests.
---

# Generate Docs from Source

Build documentation from evidence in the repository, not assumptions. Produce a navigable Markdown tree that DocsPress can convert into WordPress Pages, then hand publication setup to `$docspress-install`.

## 1. Establish the source of truth

1. Resolve the repository root and preserve unrelated working-tree changes.
2. Inventory the project with `rg --files`. Inspect package manifests, lockfiles, entrypoints, exports, command definitions, schemas, environment examples, tests, examples, release configuration, and existing docs.
3. Identify the intended audience and supported public surface from repository evidence.
4. Determine whether the project currently supports multiple API releases. Require explicit evidence such as maintained release branches, versioned schemas, compatibility tests, or existing versioned docs; do not treat package history as a reason to publish old documentation.
5. Build an internal coverage map before writing:
   - installation commands → package manifests and lockfiles;
   - configuration and environment variables → schemas, defaults, and code reads;
   - API signatures → exported source and type declarations;
   - CLI commands and flags → parser definitions and help output;
   - behavior and edge cases → tests;
   - operational steps → scripts and CI workflows.
6. Treat tests and executable examples as stronger evidence than comments. Mark contradictions for resolution instead of choosing silently.

Do not document private helpers as public APIs. Do not invent commands, options, URLs, support guarantees, performance claims, or output text.

## 2. Reuse and plan the docs tree

Preserve useful existing documentation and its voice. Update stale pages in place rather than replacing the whole directory.

Scale the tree to the project. A typical structure is:

```text
docs/
  index.md
  getting-started/
    index.md
    installation.md
    configuration.md
  guides/
    index.md
    first-real-workflow.md
  reference/
    index.md
    api.md
    cli.md
  troubleshooting.md
```

Create only pages supported by the source. Small libraries may need only an overview, installation, usage, and API reference. Applications may need architecture, deployment, operations, and troubleshooting.

Map `docs/index.md` to the Docs root. Use folder `index.md` files for section landing pages. Avoid multiple files that normalize to the same route.

### Plan maintained API versions

Keep a single unversioned tree unless readers genuinely need multiple maintained API contracts. When they do, preserve the repository’s natural layout and add an ordered registry such as `docs-versions.json`:

```json
{
  "latest": "v3",
  "versions": [
    { "id": "v3", "source": { "type": "root" } },
    { "id": "v2", "source": { "type": "directory", "path": "v2" } },
    { "id": "v1", "source": { "type": "suffix", "suffix": ".v1" } }
  ]
}
```

The named latest can own unclaimed Markdown at the root. Other versions may use directories, filename suffixes, or repository-relative manifests with their own redirects. Give every source file exactly one owner and every version a unique logical route per Page. Link counterparts within the same version. When a Page does not exist in another version, let the Version Switcher fall back to that version’s root rather than inventing a counterpart.

## 3. Write DocsPress-compatible Markdown

Use this page pattern:

```markdown
---
title: Clear page title
---

One short paragraph explaining the outcome of this page.

## First section

Verified instructions and examples.
```

Follow these constraints:

- Prefer frontmatter `title` and begin body sections at `##`; the DocsPress theme supplies the Page `h1`.
- Use `.md` or `.markdown` files and relative Markdown links between pages.
- Keep paths stable and slugs readable; directories become parent Pages.
- Use fenced code blocks with accurate language labels.
- Use standard Markdown for ordinary prose, headings, lists, links, tables, and images. Use the DocsPress blocks below whenever their documentation-specific semantics apply.
- Use a serialized `core/image` block when an image needs Gutenberg-managed width, size, caption, or link behavior; keep ordinary Markdown image syntax for unconstrained images.
- Preserve existing serialized Gutenberg block comments when valid. Validate their attributes before reusing them.
- Prefer `docspress/code-tabs` over Gutenberg Handbook-style `{% codetabs %}` when the DocsPress Blocks plugin is part of the target installation.
- Explain prerequisites before commands and verification after commands.
- Keep examples minimal but runnable. Never use real credentials or production identifiers.
- Link conceptual claims to the relevant reference page instead of duplicating long explanations.

## 4. Use DocsPress Gutenberg blocks

Always review the complete plugin catalog—two landing blocks, thirteen documentation blocks, and two version-interface blocks—before writing the docs and make a page-by-page block plan. Use every relevant block, but do not force a block where ordinary Markdown communicates the material better.

DocsPress preserves serialized Gutenberg comments in Markdown and normalizes HTML-sensitive attribute characters to WordPress-safe Unicode escapes during conversion. These plugin blocks are dynamic, so write one self-closing comment with valid compact JSON and no rendered HTML body:

```html
<!-- wp:docspress/block-name {"attribute":"value"} /-->
```

In generated Markdown, emit the comment directly, without the surrounding code fence. JSON-escape quotes, backslashes, control characters, and literal newlines inside attribute strings. Never add trailing commas, JavaScript object syntax, invented attributes, or custom colors. The plugin inherits colors, typography, radius, borders, and light/dark presentation from the active DocsPress preset.

### Block selection and schemas

| Editor block | Serialized name | Use for | Supported attributes |
| --- | --- | --- | --- |
| DocsPress: Hero | `docspress/hero` | A landing-page introduction with actions and an image or built-in synchronization diagram | `eyebrow`, `title`, `description`, `primaryLabel`, `primaryUrl`, `primaryNewTab`, `secondaryLabel`, `secondaryUrl`, `secondaryNewTab`, `mediaId`, `mediaUrl`, `mediaAlt`, `visualLabel`, `visualVariant`, `layout`, `mediaPosition`, `mediaWidth`, `imageScale`, `height`, `tone`, `textAlign`, `showGrid`, `showOrbit`, `panelColor`, `visualColor`, `accentColor` |
| DocsPress: Audience Paths | `docspress/audience-paths` | One to six cards routing distinct reader audiences to the right workflow | `eyebrow`, `title`, `description`, `paths`, `columns`, `tone`, `textAlign`, `compact`, `showNumbers`, `panelColor`, `accentColor`; each path has `title`, `description`, `url`, `cta`, `icon`, `accent`, `newTab` |
| DocsPress: Colorful Code | `docspress/colorful-code` | One source, annotated example, or unified diff that benefits from filename, highlighting, line numbers, caption, and copy | `language`, `filename`, `code`, `highlightedLines`, `showLineNumbers`, `caption`, `diffMode`, `copyMode`, `annotations`; each annotation has `line`, `content` |
| DocsPress: Code Tabs | `docspress/code-tabs` | Two to eight equivalent implementations, package managers, languages, or platforms | `tabs`, `showLineNumbers`, `caption`; each tab has `label`, `language`, `filename`, `code` |
| DocsPress: Callout | `docspress/callout` | Important notes, tips, warnings, hazards, or success guidance | `tone`, `title`, `content`, `collapsible`, `open` |
| DocsPress: Flow | `docspress/flow` | A connected, automatically numbered procedure | `start`, `steps`; each step has `title`, `content` |
| DocsPress: API Request / Response | `docspress/api-request` | A verified HTTP request and its response as one unit, optionally runnable in the browser | `method`, `endpoint`, `headers`, `requestBody`, `requestBodyFormat`, `responseStatus`, `responseBody`, `responseBodyFormat`, `runnable`, `editable`, `allowUnsafe`, `baseUrl`, `allowedOrigins`, `timeout` |
| DocsPress: Fields / Schema | `docspress/fields` | Typed API parameters, configuration keys, environment variables, CLI options, or response properties | `title`, `description`, `fields`, `searchable`, `compact`; each field has `name`, `type`, `required`, `defaultValue`, `description`, `values`, `deprecated` |
| DocsPress: Live Code Playground | `docspress/code-playground` | A small self-contained HTML, CSS, and JavaScript example readers should edit and run | `title`, `html`, `css`, `javascript`, `height`, `autoRun`, `showConsole`, `allowNetwork` |
| DocsPress: Diagram | `docspress/diagram` | A compact flow or sequence diagram without an external rendering dependency | `title`, `type`, `source`, `caption` |
| DocsPress: Troubleshooter | `docspress/troubleshooter` | A short branching support or onboarding flow | `title`, `intro`, `startId`, `questions`, `outcomes`, `showProgress`; questions route by ID and outcomes have `status`, `title`, `content` |
| DocsPress: Terminal Session | `docspress/terminal-session` | A copyable command with optional read-only output | `title`, `shell`, `prompt`, `command`, `output` |
| DocsPress: Result | `docspress/result` | A concise verified outcome after a build, check, command, or procedure | `status`, `title`, `content`, `meta` |
| DocsPress: File Tree | `docspress/file-tree` | A relevant project or generated-directory structure | `root`, `tree`, `caption` |
| DocsPress: Prompt | `docspress/prompt` | A reusable AI prompt with model, mode, context, and caption | `prompt`, `model`, `mode`, `thinking`, `context`, `caption` |
| DocsPress: Version Switcher | `docspress/version-switcher` | Switching API versions by logical route; normally place in a Site Editor template rather than Page Markdown | `label`, `showLabel`, `presentation`, `showLatestBadge`, `hideSingle`, `unavailableLabel` |
| DocsPress: Version Notice | `docspress/version-notice` | Warning only on historical API versions; normally place below the Header in the Page template | `message`, `latestLinkLabel`, `showIcon`, `dismissible` |

Use only these allowed values:

- Code `language`: `bash`, `css`, `html`, `javascript`, `json`, `jsx`, `markdown`, `php`, `plaintext`, `python`, `shell`, `sql`, `tsx`, `typescript`, or `yaml`.
- `highlightedLines`: comma-separated one-based lines and ranges such as `2,4-6`.
- Colorful Code `diffMode`: `none` or `unified`; `copyMode`: `all` or `final`. Annotations use one-based line numbers and formatted content.
- Callout `tone`: `note`, `tip`, `warning`, `danger`, or `success`. Set `open` only when `collapsible` is `true`.
- API `method`: `GET`, `POST`, `PUT`, `PATCH`, or `DELETE`. Write headers as one `Name: value` pair per line. Body formats are `json` or `raw`. Runnable examples should default to a same-origin GET, must never contain real credentials, and may use an external origin only when `allowedOrigins` explicitly includes it. Mutating requests require `allowUnsafe: true` and still show reader confirmation.
- Field `type`: `string`, `number`, `boolean`, `object`, `array`, `enum`, `url`, `date`, or `any`.
- Playground `height`: 180–720. Keep `allowNetwork: false` unless the verified example requires network access; never put secrets in iframe source.
- Diagram `type`: `flow` or `sequence`. Write one `Source -> Target: optional label` relationship per source line.
- Troubleshooter outcome `status`: `success`, `neutral`, `warning`, or `error`. Every answer destination must match a question or outcome ID.
- Result `status`: `success`, `neutral`, `warning`, or `error`.
- Prompt `mode`: `chat`, `code`, `ask`, or `plan`. `context` is a comma-separated list of at most 12 items; `$` denotes an installed skill, `@` a mention, `#` an image, `http://` or `https://` a URL, and other values a file. Always invoke installed skills as `$skill-name`, never as a `SKILL.md` file path inside a user-facing prompt.
- File trees use two spaces per depth level and a trailing slash for folders.
- Hero `visualVariant`: `image` or `sync-diagram`; `layout`: `split` or `editorial`; `mediaPosition`: `left` or `right`; `height`: `compact`, `standard`, or `tall`; `tone`: `theme`, `midnight`, `paper`, or `brand`; `textAlign`: `left` or `center`. Keep media width at 34–58 and image scale at 60–120.
- Audience Paths `columns`: 1–3; `tone`: `theme`, `paper`, `ink`, or `blueprint`; `textAlign`: `left` or `center`; path `accent`: `blue`, `gold`, `coral`, or `green`.
- Version Switcher `presentation`: `select` or `links`. Version Notice `message` may contain only the safe `{current}` and `{latest}` placeholders.

### Canonical examples

```html
<!-- wp:docspress/hero {"eyebrow":"Developer documentation","title":"Build your first integration","description":"Choose a verified workflow and ship a working request.","primaryLabel":"Get started","primaryUrl":"/docs/getting-started/","primaryNewTab":false,"secondaryLabel":"API reference","secondaryUrl":"/docs/reference/api/","secondaryNewTab":false,"visualVariant":"sync-diagram","layout":"split","mediaPosition":"right","mediaWidth":44,"imageScale":100,"height":"standard","tone":"theme","textAlign":"left","showGrid":false,"showOrbit":false} /-->

<!-- wp:docspress/audience-paths {"eyebrow":"Choose a path","title":"What are you building?","description":"Start with the workflow that matches your integration.","paths":[{"title":"Server integration","description":"Authenticate and call the API from a trusted backend.","url":"/docs/guides/server/","cta":"Build on the server","icon":"api","accent":"blue","newTab":false},{"title":"Browser application","description":"Use the supported public client flow.","url":"/docs/guides/browser/","cta":"Build for the browser","icon":"code","accent":"gold","newTab":false}],"columns":2,"tone":"theme","textAlign":"left","compact":false,"showNumbers":false} /-->

<!-- wp:docspress/colorful-code {"language":"typescript","filename":"src/client.ts","code":"import { Client } from \"pkg\";\n\nconst client = new Client();","highlightedLines":"3","showLineNumbers":true,"caption":"Create the client."} /-->

<!-- wp:docspress/code-tabs {"tabs":[{"label":"npm","language":"bash","filename":"Terminal","code":"npm install example"},{"label":"pnpm","language":"bash","filename":"Terminal","code":"pnpm add example"}],"showLineNumbers":false,"caption":"Install with the package manager used by the project."} /-->

<!-- wp:docspress/callout {"tone":"warning","title":"Protect credentials","content":"<p>Store the token in a secret manager.</p>","collapsible":false} /-->

<!-- wp:docspress/flow {"start":1,"steps":[{"title":"Configure","content":"<p>Set the verified options.</p>"},{"title":"Run","content":"<p>Execute the documented command.</p>"},{"title":"Verify","content":"<p>Confirm the expected result.</p>"}]} /-->

<!-- wp:docspress/api-request {"method":"GET","endpoint":"/wp-json/","headers":"Accept: application/json","requestBody":"","requestBodyFormat":"json","responseStatus":"200 OK","responseBody":"{\n  \"name\": \"WordPress\"\n}","responseBodyFormat":"json","runnable":true,"editable":true,"allowUnsafe":false,"timeout":10000} /-->

<!-- wp:docspress/fields {"title":"Configuration","fields":[{"name":"site","type":"string","required":true,"defaultValue":"","description":"WordPress site domain.","values":"","deprecated":false}],"searchable":true,"compact":false} /-->

<!-- wp:docspress/code-playground {"title":"Live example","html":"<button>Run</button>","css":"button { color: blue; }","javascript":"console.log( 'Ready' );","height":320,"autoRun":true,"showConsole":true,"allowNetwork":false} /-->

<!-- wp:docspress/diagram {"title":"Publishing flow","type":"flow","source":"Markdown -> DocsPress: collect\nDocsPress -> WordPress: publish","caption":"Verified system relationships."} /-->

<!-- wp:docspress/troubleshooter {"title":"Find the next step","startId":"source","questions":[{"id":"source","question":"Do docs exist?","yesLabel":"Yes","yesNext":"sync","noLabel":"No","noNext":"generate"}],"outcomes":[{"id":"sync","status":"success","title":"Publish","content":"<p>Run a draft sync.</p>"},{"id":"generate","status":"neutral","title":"Generate docs","content":"<p>Create source-grounded Markdown first.</p>"}],"showProgress":true} /-->

<!-- wp:docspress/terminal-session {"title":"Run the checks","shell":"bash","prompt":"$","command":"npm test","output":"Tests: 24 passed"} /-->

<!-- wp:docspress/result {"status":"success","title":"Verification passed","content":"<p>All documented examples completed successfully.</p>","meta":"24 tests"} /-->

<!-- wp:docspress/file-tree {"root":"project/","tree":"docs/\n  index.md\n  guides/\n    first-task.md","caption":"Generated documentation tree."} /-->

<!-- wp:docspress/prompt {"prompt":"Use $generate-docs-from-source to review the public API and identify undocumented error cases.","model":"GPT-5","mode":"code","thinking":true,"context":"$generate-docs-from-source, @repository, src/index.ts, test/api.test.ts","caption":"API coverage review prompt"} /-->
```

Use verified source values in real docs instead of copying these placeholders. Keep secrets fake. Use HTML only in the `content` and `caption` attributes that support formatted text, and keep it minimal and valid.

This catalog matches the DocsPress Blocks source shipped with the skill revision. If a verified target plugin revision differs, inspect its `blocks/*/block.php` registrations and render allow-lists, then use that revision as the source of truth.

### Keep template-owned features out of ordinary Page content

Use the Site Editor for shared reading-interface blocks. The bundled Header places Version Switcher before Command Search, and the Page template places Version Notice as a full-width bar below the Header. The theme also owns `docspress/was-this-helpful`, which is movable and customizable in the Page template and stores aggregate Helpful/Not helpful totals per Page. Native WordPress comments provide optional threaded discussions through the editable Comments template part.

Do not duplicate these blocks into every Markdown Page. Do not serialize `docspress/was-this-helpful` unless the target uses the DocsPress theme revision that registers it. Keep presentation under Global Styles and block supports instead of adding custom colors to generated content.

## 5. Generate from evidence

### Overview and getting started

Explain what the project does, who it is for, its real prerequisites, installation, and the smallest useful workflow. Derive package-manager commands from the checked-in package metadata and lockfile.

### Configuration

Document only settings read by the application. Include name, required/default state, accepted values, effect, and security sensitivity. Distinguish build-time, runtime, client-visible, and secret values.

### Guides

Choose workflows demonstrated by examples, tests, or normal source composition. Make each guide outcome-oriented and verify every referenced file and command.

### API or CLI reference

Enumerate public exports or registered commands from source. Preserve exact spelling, types, defaults, exit behavior, and errors. Generate help output locally when a safe `--help` command exists.

### Troubleshooting

Include failures evidenced by tests, explicit error messages, issue templates, or defensive branches. Pair symptoms with concrete checks and safe recovery steps.

## 6. Verify before calling the docs complete

Run the cheapest relevant checks first and record exact results.

1. Confirm every generated page is nonempty and has a unique route and title.
2. Resolve every relative link and local image path from the file containing it.
3. For a version registry, run the pinned DocsPress collector and verify source ownership, safe paths, unique logical routes, latest ownership, per-version redirects, and version-aware links.
4. Search for placeholders such as `TODO`, `TBD`, `YOUR_*`, fake domains, and unverified version numbers. Keep deliberate placeholders only inside clearly labeled templates.
5. Match documented exports, flags, environment variables, filenames, and defaults back to source.
6. Run code samples when they are safe and practical. Prefer examples already covered by tests.
7. Parse every `wp:docspress/*` attribute object as JSON. Confirm the block name, attributes, enum values, tab count, tree indentation, and required plugin support against this catalog or the verified plugin source.
8. Run representative generated Markdown through the pinned DocsPress converter and confirm every custom block comment is preserved byte-for-byte.
9. Inspect repository scripts and dependency lifecycle hooks before executing them. Run the existing formatter, lint, typecheck, tests, and build in proportion to the changes; isolate commands that rewrite generated files in a temporary copy or worktree when practical.
10. Run `git diff --check` and inspect the complete docs diff for accidental source changes or copied secrets.
11. If a check cannot run, state why and narrow the claim. Never present an unrun example as verified.

Do not weaken tests or alter product behavior merely to make documentation examples pass. If source behavior is broken or ambiguous, report it separately.

## 7. Configure publication when missing

Search `.github/workflows/` for an existing DocsPress action. If none exists:

1. Invoke `$docspress-install`.
2. Create one `.github/workflows/sync-docs.yml` targeting the generated docs directory.
3. Start with `status: draft`, `dry-run: true`, and `delete-mode: trash`.
4. Reference `${{ secrets.WP_ACCESS_TOKEN }}`; never create a plaintext credential file.
5. Resolve checkout and DocsPress actions to verified immutable commit SHAs, then validate all inputs against `action.yml` at the pinned DocsPress revision.
6. Detect the repository default branch rather than hard-coding `main`, but begin with `workflow_dispatch` only. Add a default-branch push trigger after the manual dry-run and draft-write lifecycle succeeds and the user approves ongoing synchronization.
7. If any `wp:docspress/*` blocks are present, require the verified matching `plugins/docspress-blocks/` plugin on the WordPress target. Ask separately before installing or activating it.
8. When a registry exists, pass it as `versions-file`, include it in workflow path filters, and require the matching DocsPress Blocks plugin even when Page bodies use no plugin blocks.
9. Validate the workflow locally. Do not push, dispatch, add secrets, install or activate plugins, activate a theme, or write WordPress Pages unless the user separately authorized those external changes.

Documentation generation must still complete when WordPress credentials are unavailable. Leave the workflow ready and report the exact authentication step the user must perform.

## Completion report

Report:

- pages created, updated, and intentionally preserved;
- source files used as evidence;
- code examples and commands actually executed;
- DocsPress blocks used, their locations, serialization validation, and plugin requirement;
- version registry, source layouts, repository latest, logical-route validation, and intentionally missing counterparts;
- lint, test, build, link, and workflow validation results;
- DocsPress workflow state;
- any unverified claims, source contradictions, or required user decisions.
