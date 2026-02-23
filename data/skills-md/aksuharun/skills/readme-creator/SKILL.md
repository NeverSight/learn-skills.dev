---
name: readme-creator
description: Creates high-quality, standardized README.md files for software projects suitable for open-source repositories. Use when asked to create or update a README.
---

# README Creator

Create clear, professional README.md files grounded in the actual project.

## Required Sections (always include)

1. **Title + Description** — Project name as `# Title`, followed by 1–3 sentences: what it does and its purpose. No badges unless provided.
2. **Features** — Bulleted list of key capabilities. Be specific; don't invent features.
3. **Installation** — Exact commands to install the project and its dependencies.
4. **Usage** — Minimal working example(s) with code blocks. Show the most common use case first.
5. **Contributing** — Brief guide: fork → branch → PR. One short paragraph or 3–4 bullets.
6. **License** — State the license. Default to MIT if unspecified: `Distributed under the MIT License.`

## Conditional Sections (include only when justified)

- **Prerequisites** — Only if the project requires specific runtimes, accounts, environment variables, or non-obvious tools. Skip if setup is standard (e.g., just `npm install`).

## Optional Sections (include when they add clear value)

These sections are not limited to the items listed below. Add any section that would genuinely benefit readers of this specific project.

- **Getting Started / Quickstart** — When a more guided walkthrough helps beyond Installation + Usage.
- **Documentation / Docs** — When there's an external docs site or extensive API reference to link to.
- **Learn More** — When there are tutorials, blog posts, videos, or community resources worth linking to.

## Constraints

- No "Project Structure" section
- No invented commands, flags, or capabilities
- No filler text ("Feel free to...", "This project aims to...")
- No generic disclaimers or boilerplate paragraphs
- Omit any section that would be empty or redundant
- No ASCII diagrams — use Mermaid instead

## Input Sources

Use only information from:
- User description
- Provided files or repository contents
- `package.json`, README drafts, or source code

If information is missing, omit the section instead of guessing.

## Procedure

1. Analyze the provided project information (description, source code, `package.json`, etc.).
2. Identify the project's purpose, core features, and intended users.
3. Extract real installation steps and usage examples from the project — do not invent them.
4. Include all Required Sections.
5. Include Conditional and Optional Sections only when justified.
6. Run the Validation Checklist before returning output.
7. Return only the final README.md content — no preamble, no explanation.

## Style Guidelines

- **Professional** — clear, authoritative, not casual
- **Direct** — lead with what matters; no slow build-up
- **Concise** — one sentence where one sentence suffices
- **Technical and precise** — use correct terminology for the domain
- No marketing language ("powerful", "seamless", "blazing fast")

## Output Format

- Standard Markdown, GitHub-flavored
- Fenced code blocks with language tags (` ```bash `, ` ```js `, etc.)
- Flat heading hierarchy: `##` for sections, `###` only when a section genuinely needs subsections
- Blank line between sections for readability
- When a visual diagram adds value (architecture, flow, sequence, git graph, etc.), use a fenced Mermaid block (` ```mermaid `). Never use ASCII art for diagrams.

## Validation Checklist (internal)

Before returning the README, verify:

- [ ] All Required Sections are present
- [ ] No forbidden sections included (e.g., Project Structure)
- [ ] No invented features, commands, or capabilities
- [ ] Conditional sections are included only when justified
- [ ] Markdown formatting is correct and consistent
- [ ] Content is concise and non-redundant
- [ ] No ASCII diagrams present (Mermaid used where diagrams appear)
