---
name: resumx
description: Work with Resumx, a Markdown-to-PDF resume renderer. Use when creating, editing, converting, building, styling, or tailoring resumes. Covers syntax, CLI, style options, icons, tags, views, variables, multi-language, page fitting, validation, custom CSS, and AI-assisted resume writing.
---

# Resumx

Markdown → PDF/HTML/PNG/DOCX resume renderer. Auto-fits to target page count, tags + views for tailored output from one source file.

**Coming from another renderer or builder?** Convert and quickstart in one step: [resumx.dev/#import](https://resumx.dev/#import). Drop PDF, DOCX, LaTeX, JSON Resume, or RenderCV YAML to get Markdown you can edit and render with Resumx.

## Resources

| Resource                                         | When                                                              |
| ------------------------------------------------ | ----------------------------------------------------------------- |
| [writing-resume.md](resources/writing-resume.md) | Interactive step-by-step resume creation                          |
| [tagging-resume.md](resources/tagging-resume.md) | Systematic tagging for tailored output, hierarchical tag taxonomy |

## Markdown Syntax

Standard Markdown + inline columns, bracketed spans, fenced divs.

**Structure:** `# Name` → `email | github | linkedin` (contact) → `## Section` → `### Title || Date` → `_Subtitle_ || Location` → `- Bullets` → definition lists for skills (`Term` + `: values`).

**Inline columns:** `||` splits into left/right columns. `### Google || Jan 2020 - Present`, `_Senior SWE_ || San Francisco, CA`. 3+ columns: `A || B || C`. Escape: `\||`.

**Formatting:** `**Bold**`, `_Italic_`, `H~2~O` (sub), `E = mc^2^` (super), `--`/`---` (en/em-dash).

**Tables:** Standard markdown tables.

## Classes, IDs & Fenced Divs

**Bracketed spans:** `[text]{.class}` → `<span>`. Example: `### Google [2022 - Present]{.right}`.

**Element attributes:** `{...}` at end of block applies to whole element: `- Built dashboards {.@frontend}`.

**Fenced divs:** `:::` wraps block content. Single child = no wrapper div; multiple = auto `<div>`. Prefix tag name: `::: footer {.text-center}`.

```markdown
::: {.grid .grid-cols-3}

- JavaScript
- TypeScript
  :::
```

## Frontmatter

YAML (`---`) or TOML (`+++`). CLI flags always override.

| Field          | Type                                    | Default      | Description                                               |
| -------------- | --------------------------------------- | ------------ | --------------------------------------------------------- |
| `css`          | `string \| string[]`                    | None         | CSS path(s) or inline (`.css` suffix = file, else inline) |
| `output`       | `string`                                | Input stem   | Output path/template (`{view}`, `{lang}`, `{format}`)     |
| `pages`        | `positive integer`                      | No clamping  | Target page count                                         |
| `sections`     | `{ hide?: string[], pin?: string[] }`   | Source order | Section visibility/ordering                               |
| `bullet-order` | `none \| tag`                           | `none`       | Bullet ordering strategy                                  |
| `style`        | `Record<string, string>`                | —            | Style option overrides                                    |
| `tags`         | `Record<string, string[] \| TagConfig>` | —            | Tag composition / tag view config                         |
| `vars`         | `Record<string, string>`                | —            | Template variables for `{{ }}`                            |
| `icons`        | `Record<string, string>`                | —            | Custom icons (SVG, URL, base64)                           |
| `extra`        | `Record<string, unknown>`               | —            | Arbitrary user data (unknown keys error otherwise)        |

**Validation** (`validate` key): `extends` (default `recommended`; presets: `recommended`, `minimal`, `strict`, `none`). Rules: `missing-name`, `missing-contact`, `no-sections`, `no-entries`, `empty-bullet`, `long-bullet`, `single-bullet-section`, `unknown-fenced-div-tag`, `non-pt-font-size`.

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
resumx <file>           # Render (defaults to resume.md, PDF)
resumx init [filename]   # Create template
```

**⚠ Always run with `required_permissions: ["all"]`.** Playwright/Chromium needs syscalls blocked by Cursor's sandbox. Without this, rendering fails with "Chromium not found".

**Flags:** `--css <path>` (repeatable, comma-sep), `-o/--output <value>`, `-f/--format <pdf|html|docx|png>` (repeatable, comma-sep), `-s/--style <k=v>` (repeatable), `--for <name-or-glob>` (tag/custom view name, glob, or `default`), `-v/--var <k=v>` (repeatable), `--hide <list>`, `--pin <list>`, `--bullet-order <none|tag>`, `-l/--lang <bcp47>` (repeatable, comma-sep), `-p/--pages <n>`, `-w/--watch`, `--check` (validate only), `--no-check`, `--strict`, `--min-severity <level>`.

**Stdin:** `cat resume.md | resumx` or `git show HEAD~3:resume.md | resumx -o old`.

**Output naming:** no view/langs → `resume.pdf`; with view → `resume-frontend.pdf`; with lang → `resume-en.pdf`; both → `frontend/resume-en.pdf`. Template vars: `{view}`, `{lang}`, `{format}`.

## Style Options

Override via `style:` or `--style`.

- **Typography:** `font-family`, `title-font-family`, `content-font-family`, `font-size` (11pt), `line-height` (1.4)
- **Colors:** `text-color`, `link-color`, `background-color`
- **Headings:** `name-size`, `name-caps` (small-caps/all-small-caps/petite-caps/unicase/normal), `name-weight`, `name-italic`, `name-color`, `section-title-size`, `section-title-caps`, `section-title-weight`, `section-title-italic`, `section-title-color`, `section-title-border`, `header-align`, `section-title-align`, `entry-title-size`, `entry-title-weight`, `entry-title-italic`
- **Links:** `link-underline` (underline/none)
- **Spacing:** `gap` (unitless scale), `page-margin-x`, `page-margin-y`, `section-gap`, `entry-gap`, `row-gap`, `col-gap`, `list-indent`
- **Lists:** `bullet-style` (disc/circle/square/none)
- **Features:** `auto-icons` (inline/none)

### Custom CSS

Cascades on top of defaults. Reference: `css: my-styles.css` or `--css`. Inline: `css: | h2 { letter-spacing: 0.05em; }`. Mix in array:

```yaml
css:
  - base.css
  - |
    h2::after { content: ''; flex: 1; border-bottom: var(--section-title-border); }
```

Bundled `@import` modules: `common/base.css` (reset, typography, layout), `common/icons.css`, `common/utilities.css` (`.small-caps`, `.sr-only`, `.max-N`).

## Fit to Page

`pages: N` auto-fits. Shrink order (least visible first): 1) Gaps 2) Line height 3) Font size 4) Margins (last resort). For `pages: 1`, gaps also expand to fill.

**Minimums:** font-size 9pt, line-height 1.15, section-gap 4px, entry-gap 1px, page-margin-y 0.3in, page-margin-x 0.35in. With `pages:` set, `style:` values are starting points that may shrink. Without `pages:`, applied as-is.

## Icons

`:icon-name:` (built-in), `:set/name:` (Iconify, 200k+), emoji shortcodes as fallback. Resolver: Frontmatter > Built-in > Iconify > Emoji.

**Auto-icons** on links: `mailto:`, `tel:`, `linkedin.com`, `github.com`, `gitlab.com`, `bitbucket.org`, `stackoverflow.com`, `x.com`/`twitter.com`, `youtube.com`/`youtu.be`, `dribbble.com`, `behance.net`, `medium.com`, `dev.to`, `codepen.io`, `marketplace.visualstudio.com`. Disable: `style: { auto-icons: none }`.

**Custom icons:** `icons: { mycompany: '<svg>...</svg>', partner: 'https://example.com/logo.svg' }`.

## Tailwind CSS

Tailwind v4 compiled on-the-fly. Apply via `{.class}`: `[React]{.bg-blue-100 .text-blue-800 .px-2 .rounded}`. Works on spans, element attrs, fenced divs. Arbitrary values: `.text-[#ff6600]`. Built-in: `.small-caps`, `.sr-only`, `.max-1`–`.max-16`.

## Tags

`{.@name}` filters content for audiences. Untagged always passes. Tagged appears only for matching tag. Multiple: `{.@backend .@frontend}`. Render: `--for frontend`.

**Hierarchical:** `/` nesting (`{.@backend/node}`). A view includes ancestors + self + descendants + untagged; siblings excluded. `--for backend/node` → `@backend` + `@backend/node` + untagged (no `@backend/jvm`). `--for backend` → all descendants + untagged. Unlimited depth.

**Composition** in frontmatter: `fullstack: [frontend, backend]`. Hierarchical works as constituents, lineage expands per constituent. Recursive expansion (`startup-cto` includes `frontend`/`backend` via `fullstack`). Typos error with suggestion.

```yaml
tags:
  fullstack: [frontend, backend]
  node-fullstack: [frontend, backend/node]
  tech-lead: [backend, leadership]
  startup-cto: [fullstack, leadership, architecture]
```

## Views

Tags = what to show. Views = how to show it. Every render uses a view.

| Kind      | Where                     | Nature                      |
| --------- | ------------------------- | --------------------------- |
| Default   | Frontmatter render fields | Base config                 |
| Tag view  | `tags:` expanded form     | Per-tag overrides, implicit |
| Custom    | `.view.yaml` files        | Per-application             |
| Ephemeral | CLI flags                 | One-off                     |

**Tag views:** Every tag auto-generates a view. Expanded form adds render overrides. Shorthand `fullstack: [frontend, backend]` = `fullstack: { extends: [frontend, backend] }`.

```yaml
tags:
  frontend:
    sections: { hide: [publications], pin: [skills, projects] }
    pages: 1
  fullstack:
    extends: [frontend, backend]
    sections: { pin: [work, skills] }
    pages: 2
```

**Custom views:** `.view.yaml` files, auto-discovered recursively. Fields: `selects` (tags to include), `sections`, `pages`, `bullet-order`, `vars`, `style`, `css`, `format`, `output`. No `selects` = all content; `selects: []` = untagged only. Render: `--for stripe-swe`. Batch: `--for '*'`/`--for 'stripe-*'`. `--for default` = default view (no filtering); combine: `--for default,frontend`. Don't name a view `default`.

```yaml
# stripe.view.yaml
stripe-swe:
  selects: [backend, distributed-systems, leadership]
  sections: { hide: [publications], pin: [skills, work] }
  vars:
    tagline: 'Stream Processing, Event-Driven Architecture, Go, Kafka'
```

**Ephemeral:** CLI flags inline: `resumx resume.md --for backend -v tagline="Stream Processing, Go" --pin skills,work -o stripe.pdf`.

**Cascade:** Built-in defaults → Default view → Tag/Custom view → Ephemeral (CLI).

## Template Variables

`{{ name }}` placeholders. Define in `vars:`, custom view, or `-v`. Undefined/empty → line removed. Values can contain markdown. Variable with no matching placeholder → error.

```markdown
# Jane Doe

jane@example.com | github.com/jane
{{ tagline }}
```

## Sections

`sections: { hide: [publications, volunteer], pin: [skills, work] }`. `hide` removes, `pin` moves to top in order, rest follow source order. Values: `work`, `education`, `skills`, `projects`, `awards`, `certificates`, `publications`, `volunteer`, `languages`, `interests`, `references`, `basics`. CLI: `--hide publications --pin skills,work`.

## Multi-Language

`{lang=xx}` (BCP 47). Untagged appears in all. Combine with tags: `{lang=en .@backend}`. Filter: `--lang en` or `--lang en,fr`. Dimensions multiply: 2 langs × 2 tags = 4 PDFs.

```markdown
## [Experience]{lang=en} [Expérience]{lang=fr}

### Google

- [Reduced API latency by 60%]{lang=en}
  [Réduction de la latence API de 60%]{lang=fr}
```

## Semantic Selectors

Auto-generated HTML attributes: **Header:** `[data-field='name|email|phone|profiles|location|url']`, `[data-network='github']`. **Sections:** `section[data-section='work|education|skills|projects|awards|certificates|publications|volunteer|languages|interests|references|basics']` (fuzzy keyword match). **Entries:** `.entries` (container), `.entry` (`<article>`). **Dates:** `<time datetime="ISO8601">`, `.date-range`.

## Git Integration

Setup alias (once):

```bash
git config alias.resumx '!f() { spec="$1"; shift; case "$spec" in *:*) ;; *) spec="$spec:resume.md";; esac; tag="${spec%%:*}"; header=$(git tag -l --format="%(refname:short)" "$tag" 2>/dev/null); subject=$(git tag -l --format="%(contents:subject)" "$tag" 2>/dev/null); [ -n "$header" ] && printf "\033[2m%s\033[0m\n\033[1m%s\033[0m\n\n" "$header" "$subject"; git show "$spec" | resumx "$@"; }; f'
```

Tag applications: `git tag -a sent/stripe-2026-02 -m "Tailored for L5 infra, emphasized Kafka + distributed systems"`. Annotated tags print name + note before rendering.

```bash
git resumx sent/stripe-2026-02:resume.md              # from tag
git resumx HEAD~3:resume.md --css my-styles.css -o stripe  # past commit
git show :resume.md | resumx -o staged                # staged changes
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
