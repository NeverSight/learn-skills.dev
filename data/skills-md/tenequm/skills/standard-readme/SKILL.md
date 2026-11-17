---
name: standard-readme
description: Writes or audits READMEs against the Standard Readme spec. Use whenever the user asks to create, rewrite, improve, audit, or fix a README, or asks about README quality or structure - even if they never mention "standard readme".
metadata:
  version: "0.1.6"
  categories: "knowledge, development"
  topics: "readme, documentation, standard-readme, markdown, open-source"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/standard-readme
    emoji: "📖"
---

# Standard Readme

Generate and audit README.md files that comply with the [Standard Readme](https://github.com/RichardLitt/standard-readme) specification.

## Two Modes

**Write mode** (default): Generate a new README or rewrite an existing one.
**Audit mode**: When the user asks to "check", "audit", "review", or "lint" a README, analyze it against the spec and report issues without rewriting.

---

## The Specification

A compliant README has sections in this exact order. Some are required, some optional. Optional sections should be included only when they add real value for the project - don't pad the README with empty sections.

### Section Order

```
1.  Title                    REQUIRED   (H1)
2.  Banner                   optional   (image, no heading)
3.  Badges                   optional   (no heading)
4.  Short Description        REQUIRED   (plain text, no heading)
5.  Long Description         optional   (no heading)
6.  Table of Contents        REQUIRED*  (H2)
7.  Security                 optional   (H2)
8.  Background               optional   (H2)
9.  Install                  REQUIRED** (H2)
10. Usage                    REQUIRED** (H2)
11. [Extra Sections]         optional   (H2, custom titles)
12. API                      optional   (H2)
13. Maintainer(s)            optional   (H2)
14. Thanks / Credits         optional   (H2)
15. Contributing             REQUIRED   (H2)
16. License                  REQUIRED   (H2, always last)
```

`*` Table of Contents is only required when the README exceeds 100 lines (excluding the ToC itself).
`**` Install and Usage are optional for documentation-only repositories (no functional code).

### Section Rules

#### Title (required)

H1 heading. Must match the repository/package name. If using a different display title, include the repo name in italics and parentheses:

```markdown
# My Awesome Project _(my-awesome-project)_
```

#### Banner (optional)

Image placed directly after the title, no heading. Must reference a local image in the repository, not an external URL.

```markdown
![banner](assets/banner.png)
```

Include only if the project actually has a banner image.

#### Badges (optional)

One badge per line, directly after banner (or title if no banner). No heading.

```markdown
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![npm version](https://img.shields.io/npm/v/my-package.svg?style=flat-square)](https://npmjs.org/package/my-package)
```

Include when the project uses CI, has a published package, or benefits from status indicators. Always include the Standard Readme compliance badge.

#### Short Description (required)

A single line of plain text, under 120 characters. No heading, no blockquote (`>`). Must match the description in the package manager and GitHub repo settings.

```markdown
A CLI tool that converts Markdown files to PDF with custom styling.
```

#### Long Description (optional)

One or more paragraphs after the short description. No heading. Use this to explain motivation, goals, or context that doesn't fit in 120 characters. If the title doesn't match the repo/package name, explain why here.

#### Table of Contents (required if >100 lines)

H2 heading. Links to every subsequent section. Does not include the title or the ToC itself. At minimum, list all H2 headings; optionally include H3/H4.

```markdown
## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Contributing](#contributing)
- [License](#license)
```

#### Security (optional)

H2 heading. Include only if the project has security considerations important enough to highlight before install/usage (cryptographic software, auth libraries, tools handling secrets). Otherwise, put security notes in an Extra Section or omit.

#### Background (optional)

H2 heading. Motivation, history, intellectual context. A `### See Also` subsection fits here.

#### Install (required)

H2 heading. Must contain a code block showing how to install.

````markdown
## Install

```sh
npm install my-package
```
````

Add a `### Dependencies` subsection if there are unusual or manual dependencies. Consider an `### Updating` subsection for projects where upgrades need special steps.

#### Usage (required)

H2 heading. Must contain a code block showing common usage.

- CLI tool: show the command and typical flags
- Library: show import + basic usage
- Both: include a `### CLI` subsection

````markdown
## Usage

```js
import { convert } from 'my-package'

const pdf = await convert('README.md', { style: 'github' })
```
````

#### Extra Sections (optional)

Zero or more custom H2 sections between Usage and API. Use descriptive titles relevant to the project (e.g., "Architecture", "Configuration", "Deployment"). This is the right place for project-specific content that doesn't fit the standard sections.

#### API (optional)

H2 heading. Document exported functions, classes, types. Include signatures, return types, and notable caveats. For large APIs, point to a separate `API.md`.

Include when the project exports a programmatic API that users call directly.

#### Maintainer(s) (optional)

H2 heading (`## Maintainer` or `## Maintainers`). List project maintainers with at least one contact method (GitHub profile link or email). Keep this small - people who are responsible, not everyone with commit access.

#### Thanks (optional)

H2 heading (`## Thanks`, `## Credits`, or `## Acknowledgements`). Recognize significant contributions, inspirations, or dependencies.

#### Contributing (required)

H2 heading. Must state:
1. Where to ask questions (issues, discussions, Discord, etc.)
2. Whether PRs are accepted
3. Any requirements (e.g., signing commits, running tests first)

```markdown
## Contributing

Feel free to open an issue or submit a PR. Bug reports and feature requests are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.
```

Link to a CONTRIBUTING.md if one exists. Link to the Code of Conduct if one exists.

#### License (required, always last)

H2 heading. Must be the final section. State the license name (or SPDX identifier), the copyright holder, and link to the LICENSE file.

```markdown
## License

[MIT](LICENSE) (c) 2024 Jane Smith
```

Use `UNLICENSED` if no license. Use `SEE LICENSE IN <filename>` for complex/multi-license situations.

---

## Write Mode Workflow

When creating or rewriting a README:

1. **Gather context** - Read the project's existing files to understand what it is: package.json/Cargo.toml/pyproject.toml (name, description, dependencies), existing README, LICENSE, CONTRIBUTING.md, source code structure, CI config. Don't ask the user for information you can derive from the codebase.

2. **Determine relevant sections** - Start with the required sections. Add optional sections only when the project justifies them:
   - Banner: only if an image already exists in the repo
   - Badges: if CI, package registry, or other status indicators are set up
   - Long Description: if the short description can't convey the purpose alone
   - Table of Contents: if the final README will exceed 100 lines
   - Security: only for security-sensitive projects
   - Background: if the project has non-obvious motivation or history
   - API: if the project exports functions/classes for programmatic use
   - Maintainers: if the project has identified maintainers
   - Thanks: if there are notable acknowledgements
   - Extra Sections: for project-specific content (config, architecture, deployment) that genuinely helps users

3. **Write the README** - Follow the section order exactly. Make sure:
   - Short description is under 120 characters
   - Install and Usage both have code blocks
   - Code examples actually work (match the project's real API/CLI)
   - No broken internal links
   - License matches the actual LICENSE file
   - ToC links match all H2 sections (if ToC is included)

4. **Self-check** - Before presenting the result, verify the section order matches the spec, all required sections are present, and no empty sections were added just for completeness.

---

## Audit Mode Workflow

When checking an existing README:

1. **Read the README** and identify each section by heading and position.

2. **Check against the spec**, reporting:
   - Missing required sections
   - Sections in wrong order
   - Short description over 120 characters or formatted as blockquote
   - Install/Usage missing code blocks
   - License not being the last section
   - Broken internal links (anchors that don't match headings)
   - ToC missing or incomplete (if README >100 lines)
   - Banner referencing an external URL instead of a local image

3. **Present findings** as a numbered list, grouped by severity:
   - **Must fix**: violations of required rules
   - **Should fix**: violations of optional-but-recommended rules
   - **Suggestions**: improvements that would strengthen the README

4. **Offer to fix** - After presenting the audit, ask if the user wants you to rewrite the README to fix the issues.

---

## Things to Avoid

- Don't add empty sections. If Background has nothing to say, omit it.
- Don't invent package names or CLI commands. Derive them from the actual project files.
- Don't use blockquote (`>`) for the short description.
- Don't place License anywhere except last.
- Don't add a ToC to READMEs under 100 lines unless the user specifically asks.
- Don't include the Title or ToC heading in the Table of Contents links.
- Don't use external URLs for the banner image.
