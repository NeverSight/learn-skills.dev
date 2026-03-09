---
name: resumx
description: Work with Resumx, a Markdown-to-PDF resume renderer. Use when creating, editing, converting, building, styling, or tailoring resumes. Covers syntax, CLI, style options, icons, tags, views, variables, multi-language, page fitting, validation, custom CSS, JSON Resume conversion, and AI-assisted resume writing.
---

# Resumx

Resumx renders resumes from Markdown to PDF, HTML, PNG, and DOCX. It auto-fits content to a target page count, supports tags and views for tailored output from a single source file, and uses style options for styling.

## Resources

This skill includes reference documents for specific workflows. Read them when applicable:

| Resource                                                           | When to use                                                                                   |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| [json-resume-to-markdown.md](resources/json-resume-to-markdown.md) | Converting between Resumx Markdown and JSON Resume format (either direction)                  |
| [writing-resume.md](resources/writing-resume.md)                   | Interactive resume creation, guiding users step-by-step to collect info and generate a resume |
| [tagging-resume.md](resources/tagging-resume.md)                   | Systematically tagging a resume for tailored output, including hierarchical tag taxonomy      |

## Markdown Syntax

Standard Markdown with extensions for inline columns, bracketed spans, and fenced divs.

### Structure

| Element  | Syntax                                              |
| -------- | --------------------------------------------------- |
| Name     | `# Full Name`                                       |
| Contact  | `email@example.com \| github.com/user \| linkedin…` |
| Section  | `## Section Name`                                   |
| Entry    | `### Title \|\| Date`                               |
| Subtitle | `_Role or Degree_ \|\| Location`                    |
| Bullets  | `- Achievement with \`tech\` tags`                  |
| Skills   | Definition list (`Term` + `: values`)               |

### Inline Columns

`||` splits a line into columns, pushing them to opposite sides. Simplest way to right-align a date or location:

```markdown
### Google || Jan 2020 - Present

_Senior Software Engineer_ || San Francisco, CA
```

More than two columns: `A || B || C`. Escape with `\||`.

### Inline Formatting

| Syntax          | Result            |
| --------------- | ----------------- |
| `**Bold**`      | Bold              |
| `_Italic_`      | Italic            |
| `` `Code` ``    | Tech tag/badge    |
| `==Highlight==` | Highlighted text  |
| `H~2~O`         | Subscript         |
| `E = mc^2^`     | Superscript       |
| `--` / `---`    | En-dash / Em-dash |
| `"text"`        | Smart quotes      |

### Definition Lists

```markdown
Languages
: JavaScript, TypeScript, Python

Frameworks
: React, Node.js, Express
```

Also used as inline metadata below entries:

```markdown
### Google || June 2022 - Present

Senior Software Engineer
: Infrastructure Platform Team
: San Francisco, CA
```

### Tables

```markdown
| Category  |           Technologies |
| :-------- | ---------------------: |
| Languages | Python, TypeScript, Go |
```

### Horizontal Rule

`---` renders as a standard thematic break or section divider.

### Comments

HTML comments (`<!-- -->`) are stripped from output.

## Classes, IDs & Fenced Divs

### Bracketed Spans

`[text]{.class}` wraps text in a `<span>` with classes/IDs/attributes:

```markdown
### Google [2022 - Present]{.right}

_Senior Software Engineer_ [San Francisco, CA]{.right}
```

### Element Attributes

`{...}` at end of a block element applies to the whole element:

```markdown
- Built interactive dashboards {.@frontend}
```

### Fenced Divs

`:::` applies attributes to block content. Single child: attributes go directly on it (no wrapper div). Multiple children: auto-wraps in a `<div>`.

```markdown
::: {.grid .grid-cols-3}

- JavaScript
- TypeScript
- Python
  :::
```

Prefix a tag name for a specific HTML element: `::: footer {.text-center}`.

## Frontmatter

YAML (`---`) or TOML (`+++`). CLI flags always override frontmatter.

### Render Fields

| Field          | Type                                    | Default             | Description                                                                           |
| -------------- | --------------------------------------- | ------------------- | ------------------------------------------------------------------------------------- |
| `css`          | `string \| string[]`                    | None                | CSS file path(s) or inline CSS string(s). Ends with `.css` = file, otherwise = inline |
| `output`       | `string`                                | Input filename stem | Output path (name, directory with `/`, or template with `{view}`/`{lang}`/`{format}`) |
| `pages`        | `positive integer`                      | No clamping         | Target page count                                                                     |
| `sections`     | `{ hide?: string[], pin?: string[] }`   | All in source order | Section visibility and ordering                                                       |
| `bullet-order` | `none \| tag`                           | `none`              | Bullet ordering strategy                                                              |
| `style`        | `Record<string, string>`                | No overrides        | Style option overrides                                                                |
| `tags`         | `Record<string, string[] \| TagConfig>` | No composed tags    | Tag composition and tag view configuration                                            |
| `vars`         | `Record<string, string>`                | No variables        | Template variables for `{{ }}` placeholders                                           |
| `icons`        | `Record<string, string>`                | No custom icons     | Custom icon definitions (SVG, URL, or base64)                                         |
| `extra`        | `Record<string, unknown>`               | No custom data      | Arbitrary user-defined data                                                           |

### Validate Fields

Under a `validate` key:

| Field              | Type                                | Default             |
| ------------------ | ----------------------------------- | ------------------- |
| `validate.extends` | `string`                            | `recommended`       |
| `validate.rules`   | `Record<string, Severity \| 'off'>` | Per-preset defaults |

Presets: `recommended`, `minimal`, `strict`, `none`.

Available rules: `missing-name`, `missing-contact`, `no-sections`, `no-entries`, `empty-bullet`, `long-bullet`, `single-bullet-section`, `unknown-fenced-div-tag`, `non-pt-font-size`.

### Unknown Fields

Unknown top-level keys error. Use `extra` for custom data.

### Full Example

```yaml
---
pages: 1
output: ./out/Jane_Smith-{view}
bullet-order: tag
style:
  link-color: '#0ea5e9'
tags:
  fullstack: [frontend, backend]
  leadership: false
vars:
  tagline: 'Full-stack engineer with 8 years of experience'
validate:
  extends: recommended
  rules:
    long-bullet: warning
    single-bullet-section: off
extra:
  name: Jane Smith
  target-role: Senior SWE
---
```

## CLI

```bash
resumx <file>              # Render (defaults to resume.md, PDF)
resumx init [filename]     # Create template resume
```

### Sandbox Requirement

Resumx uses Playwright with Chromium for PDF rendering. Chromium cannot launch inside Cursor's default sandbox because the sandbox blocks syscalls Chromium needs to initialize. **Always run resumx commands with `required_permissions: ["all"]`** to disable the sandbox. Without this, rendering will fail with "Chromium not found" even though Chromium is installed.

### Render Options

| Flag                       | Description                                                                      |
| -------------------------- | -------------------------------------------------------------------------------- |
| `--css <path>`             | Path to custom CSS file, repeatable, comma-separated                             |
| `-o, --output <value>`     | Output path (name, directory, or template)                                       |
| `-f, --format <name>`      | `pdf`, `html`, `docx`, `png`, repeatable, comma-separated                        |
| `-s, --style <name=value>` | Override style property, repeatable                                              |
| `--for <name-or-glob>`     | Tag view name, custom view name, glob pattern, or `default` for the default view |
| `-v, --var <key=value>`    | Override a template variable, repeatable                                         |
| `--hide <list>`            | Hide sections (comma-separated `data-section` values)                            |
| `--pin <list>`             | Pin sections to top in order (comma-separated `data-section` values)             |
| `--bullet-order <value>`   | Bullet ordering: `none` (default) or `tag`                                       |
| `-l, --lang <tag>`         | Language filter (BCP 47), repeatable, comma-separated                            |
| `-p, --pages <number>`     | Target page count                                                                |
| `-w, --watch`              | Auto-rebuild on changes                                                          |
| `--check`                  | Validate only, no render                                                         |
| `--no-check`               | Skip validation                                                                  |
| `--strict`                 | Fail on any validation error                                                     |
| `--min-severity <level>`   | Filter validation output                                                         |

### Stdin

```bash
cat resume.md | resumx
git show HEAD~3:resume.md | resumx -o old
```

### Output Naming

| Scenario          | Output                   |
| ----------------- | ------------------------ |
| No view, no langs | `resume.pdf`             |
| With tag/view     | `resume-frontend.pdf`    |
| With langs        | `resume-en.pdf`          |
| Tag/view + langs  | `frontend/resume-en.pdf` |

Template variables: `{view}`, `{lang}`, `{format}`.

## Style Options

Override via frontmatter `style:` or CLI `--style`.

**Typography:** `font-family`, `title-font-family`, `content-font-family`, `font-size` (default `11pt`), `line-height` (default `1.4`).

**Colors:** `text-color`, `link-color`, `background-color`.

**Headings:** `name-size`, `name-caps` (`small-caps`, `all-small-caps`, `petite-caps`, `unicase`, `normal`), `name-weight`, `name-italic`, `name-color`, `section-title-size`, `section-title-caps`, `section-title-weight`, `section-title-italic`, `section-title-color`, `section-title-border`, `header-align`, `section-title-align`, `entry-title-size`, `entry-title-weight`, `entry-title-italic`.

**Links:** `link-underline` (`underline`, `none`).

**Spacing:** `gap` (unitless scale factor for all vertical gaps), `page-margin-x`, `page-margin-y`, `section-gap`, `entry-gap`, `row-gap`, `col-gap`, `list-indent`.

**Lists:** `bullet-style` (`disc`, `circle`, `square`, `none`).

**Features:** `auto-icons` (`inline`, `none`).

### Custom CSS

Your CSS cascades on top of the default stylesheet, so you only write overrides:

```css
:root {
	--font-family: 'Inter', sans-serif;
	--section-title-color: #2563eb;
}

h2 {
	letter-spacing: 0.05em;
}
```

Reference by path: `css: my-styles.css` or `--css my-styles.css`. For small overrides, inline CSS avoids creating a file:

```yaml
css: |
  h2 { letter-spacing: 0.05em; }
```

Mix file paths and inline CSS in an array:

```yaml
css:
  - base.css
  - |
    h2::after { content: ''; flex: 1; border-bottom: var(--section-title-border); }
```

For building a stylesheet from scratch, `@import` bundled modules: `common/base.css` (reset, typography, layout), `common/icons.css` (icon sizing), `common/utilities.css` (`.small-caps`, `.sr-only`, `.max-N`).

## Fit to Page

Set `pages: N` to auto-fit. Shrinks in order of visual impact (least noticeable first):

1. **Gaps** (row-gap, entry-gap, section-gap)
2. **Line height**
3. **Font size**
4. **Margins** (page-margin-x, page-margin-y, last resort)

For `pages: 1`, gaps also expand to fill remaining space.

**Minimums:** font-size 9pt, line-height 1.15, section-gap 4px, entry-gap 1px, page-margin-y 0.3in, page-margin-x 0.35in.

When `pages:` is set, `style:` values are starting points that may be reduced. Without `pages:`, they apply as-is.

## Icons

### Syntax

`:icon-name:` for built-in icons, `:set/name:` for Iconify (200k+ icons), standard emoji shortcodes as fallback.

### Auto-Icons

Links to recognized domains get icons automatically:

`mailto:` (Email), `tel:` (Phone), `linkedin.com`, `github.com`, `gitlab.com`, `bitbucket.org`, `stackoverflow.com`, `x.com`/`twitter.com`, `youtube.com`/`youtu.be`, `dribbble.com`, `behance.net`, `medium.com`, `dev.to`, `codepen.io`, `marketplace.visualstudio.com`.

Disable with `style: { auto-icons: none }`.

### Custom Icons (Frontmatter)

```yaml
icons:
  mycompany: '<svg>...</svg>'
  partner: 'https://example.com/logo.svg'
```

Resolver order: Frontmatter > Built-in > Iconify > Emoji.

## Tailwind CSS

Resumx compiles Tailwind CSS v4 on-the-fly. Apply via `{.class}` syntax:

```markdown
[React]{.bg-blue-100 .text-blue-800 .px-2 .rounded}
```

Works with bracketed spans, element attributes, and fenced divs. Supports arbitrary values: `.text-[#ff6600]`.

Built-in utilities: `.small-caps`, `.sr-only`, `.max-1` – `.max-16` (hide children beyond the Nth).

## Tags

Tags filter content. Add `{.@name}` to any element to mark it for a specific audience. Untagged content always passes through. Tagged content only appears when rendering for a matching tag.

```markdown
- Shared bullet
- Frontend-only bullet {.@frontend}
- Backend-only bullet {.@backend}
```

Multiple tags: `{.@backend .@frontend}`.

Render with `--for frontend` or `--for backend`.

### Hierarchical Tags

Use `/` to nest tags when a domain spans multiple ecosystems:

```markdown
- Designed REST APIs with OpenAPI documentation {.@backend}
- Built microservices with `Express` {.@backend/node}
- Migrated `Spring Boot` monolith {.@backend/jvm}
```

Inheritance: **a view includes its entire lineage (ancestors + self + descendants) and untagged content. Siblings are excluded.**

- `--for backend/node` → `@backend` (ancestor) + `@backend/node` (self) + untagged. Excludes `@backend/jvm`.
- `--for backend` → `@backend` (self) + `@backend/node` + `@backend/jvm` (descendants) + untagged.

Depth is unlimited: `{.@data/ml/nlp}` nests three levels.

### Tag Composition

Define composed tags in frontmatter as unions of constituents:

```yaml
tags:
  fullstack: [frontend, backend]
  node-fullstack: [frontend, backend/node]
  tech-lead: [backend, leadership]
  startup-cto: [fullstack, leadership, architecture]
```

Hierarchical tags work as constituents. Lineage expands per constituent: `node-fullstack` includes `@frontend` (+ descendants), `@backend` (ancestor of `backend/node`), `@backend/node`, and untagged. Sibling `@backend/jvm` is excluded.

Compositions expand recursively (`startup-cto` includes `frontend` and `backend` via `fullstack`). Every constituent must exist as a content tag or another composed tag; typos produce an error with a suggestion.

## Views

Tags filter content (what to show). Views configure rendering (how to show it). Every render uses a view.

### Four Kinds of View

| Kind           | Where                             | Nature                                    |
| -------------- | --------------------------------- | ----------------------------------------- |
| Default view   | Frontmatter render fields         | Base config for all renders               |
| Tag view       | Frontmatter `tags:` expanded form | Per-tag overrides, implicit for every tag |
| Custom view    | `.view.yaml` files                | Per-application config                    |
| Ephemeral view | CLI flags                         | One-off, not persisted                    |

### Tag Views

Every tag implicitly generates a tag view. Configure with the expanded form:

```yaml
tags:
  frontend:
    sections:
      hide: [publications]
      pin: [skills, projects]
    pages: 1

  fullstack:
    extends: [frontend, backend]
    sections:
      pin: [work, skills]
    pages: 2
```

The shorthand `fullstack: [frontend, backend]` is sugar for `fullstack: { extends: [frontend, backend] }`.

### Custom Views

Custom views live in `.view.yaml` files, auto-discovered recursively relative to the resume:

```yaml
# stripe.view.yaml
stripe-swe:
  selects: [backend, distributed-systems, leadership]
  sections:
    hide: [publications]
    pin: [skills, work]
  vars:
    tagline: 'Stream Processing, Event-Driven Architecture, Go, Kafka'
```

Render with `--for stripe-swe`. Batch with `--for '*'` or `--for 'stripe-*'`. Use `--for default` to target the default view (no tag filtering); combine with named views, e.g. `--for default,frontend`, to render both. Do not name a view `default` (reserved).

Custom view fields: `selects` (content tags to include), `sections`, `pages`, `bullet-order`, `vars`, `style`, `css`, `format`, `output`.

A view without `selects` applies no content filter (all content renders). An explicit `selects: []` means only untagged content.

### Ephemeral Views

CLI flags create an ephemeral view inline without persisting:

```bash
resumx resume.md --for backend -v tagline="Stream Processing, Go" --pin skills,work -o stripe.pdf
```

### Cascade Order

```
Built-in defaults
  → Default view (frontmatter render fields)
    → Tag view OR Custom view (whichever --for resolves)
      → Ephemeral view (CLI flags)
```

## Template Variables

Inject per-application text via `{{ name }}` placeholders:

```markdown
# Jane Doe

jane@example.com | github.com/jane

{{ tagline }}
```

Define in frontmatter `vars:`, in a custom view, or via CLI `-v`:

```yaml
vars:
  tagline: 'Full-stack engineer with 8 years of experience'
```

When undefined or empty, the placeholder produces nothing (line removed). Variable values can contain markdown formatting. Defining a variable with no matching placeholder is an error.

## Sections

Control which sections appear and their order:

```yaml
sections:
  hide: [publications, volunteer]
  pin: [skills, work]
```

`hide` removes sections. `pin` moves them to the top in the specified order. Non-pinned sections follow in source order. Values are `data-section` types: `work`, `education`, `skills`, `projects`, `awards`, `certificates`, `publications`, `volunteer`, `languages`, `interests`, `references`, `basics`.

CLI: `--hide publications --pin skills,work`.

## Multi-Language Output

Tag content with `{lang=xx}` (BCP 47). Untagged content appears in all languages.

```markdown
## [Experience]{lang=en} [Expérience]{lang=fr}

### Google

- [Reduced API latency by 60%]{lang=en}
  [Réduction de la latence API de 60%]{lang=fr}
```

Combines with tags: `{lang=en .@backend}`. Filter with `--lang en` or `--lang en,fr`.

Dimensions multiply: 2 langs × 2 tags = 4 PDFs.

## Semantic Selectors

Resumx auto-generates semantic HTML attributes for CSS targeting:

**Header:** `[data-field='name']`, `[data-field='email']`, `[data-field='phone']`, `[data-field='profiles']`, `[data-network='github']`, `[data-field='location']`, `[data-field='url']`.

**Sections:** `section[data-section='work']`, `section[data-section='education']`, `section[data-section='skills']`, `section[data-section='projects']`, `section[data-section='awards']`, `section[data-section='certificates']`, `section[data-section='publications']`, `section[data-section='volunteer']`, `section[data-section='languages']`, `section[data-section='interests']`, `section[data-section='references']`, `section[data-section='basics']`.

Headings are classified by fuzzy keyword matching.

**Entries:** `.entries` (container), `.entry` (individual `<article>`).

**Dates:** `<time>` with ISO 8601 `datetime`. `.date-range` wraps start/end `<time>` tags.

## Git Integration

If the user hasn't set up the `git resumx` alias yet, run this first:

```bash
git config alias.resumx '!f() { spec="$1"; shift; case "$spec" in *:*) ;; *) spec="$spec:resume.md";; esac; tag="${spec%%:*}"; header=$(git tag -l --format="%(refname:short)" "$tag" 2>/dev/null); subject=$(git tag -l --format="%(contents:subject)" "$tag" 2>/dev/null); [ -n "$header" ] && printf "\033[2m%s\033[0m\n\033[1m%s\033[0m\n\n" "$header" "$subject"; git show "$spec" | resumx "$@"; }; f'
```

Tag with a note when submitting an application:

```bash
git tag -a sent/stripe-2026-02 -m "Tailored for L5 infra, emphasized Kafka + distributed systems"
```

When the ref is an annotated tag, the alias prints the tag name and note before rendering:

```
sent/stripe-2026-02
Tailored for L5 infra, emphasized Kafka + distributed systems
```

Then render from git history:

```bash
git resumx sent/stripe-2026-02:resume.md              # render from tag
git resumx HEAD~3:resume.md --css my-styles.css -o stripe  # past commit
git show :resume.md | resumx -o staged      # staged changes
```

Pre-commit hook: `resumx --check` for validation.
Post-commit hook: auto-render on every commit.

## Using AI

Install agent skills: `npx skills add resumx/resumx`.

### Tailoring to Job Postings

1. Give the agent `resume.md` and the job posting URL
2. Agent reads the JD, maps each requirement to existing bullets (covered, weak, missing)
3. Agent decides what's durable vs ephemeral: will this change make the next 10 applications better, or just this one?
4. **Durable improvements** (better phrasing, new bullets, new tags) → edit `resume.md`
5. **Ephemeral adjustments** (keywords, section order, tagline) → create a view or use CLI vars
6. Render: `resumx resume.md --for stripe-swe -o out/stripe.pdf`

With `pages: 1`, layout auto-adjusts after every edit.

### Zero-File-Modification Rendering

For maximum speed and zero git diff, render entirely from CLI flags:

```bash
resumx resume.md --for backend -v tagline="Stream Processing, Go, Kafka" --pin skills,work -o stripe.pdf
```

### Resume Template

```markdown
---
pages: 1
---

# Full Name

email@example.com | [linkedin.com/in/user](https://linkedin.com/in/user) | [github.com/user](https://github.com/user)

{{ tagline }}

## Education

### University Name || Sept 2019 - June 2024

_Degree Name_

- GPA: 3.85

## Work Experience

### Company Name || Start - End

_Job Title_

- Achievement with quantified impact using `Technology`

## Projects

### Project Name _(Individual/Group)_

- Description of what was built

## Technical Skills

Languages
: Java, Python, TypeScript

Frameworks
: React, Node.js, FastAPI
```

### Writing Best Practices

- Start bullets with strong action verbs (Led, Developed, Engineered, Increased)
- Quantify results (20% improvement, 500+ users)
- Wrap technologies in backticks
- Use consistent date formats (`Jan 2020 - Present`)
- Use `\[Date\]` for literal brackets in dates: `[\[Jun 2024\]]{.right}`
