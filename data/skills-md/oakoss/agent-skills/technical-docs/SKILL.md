---
name: technical-docs
description: 'Technical documentation writing and diagram generation. Use when creating docs, syncing documentation with code changes, building Mermaid diagrams, running doc coverage audits, or establishing writing style guides. Use for doc-as-code workflows, ERD generation, sequence diagrams, documentation gap analysis, and AI-assisted drafting.'
license: MIT
metadata:
  author: oakoss
  version: '1.2'
---

# Documentation

Technical writing, diagram-as-code, and documentation lifecycle management. Treats docs as code: version-controlled, linted, and CI-verified.

**When to use**: Creating or updating technical documentation, generating Mermaid diagrams (flowcharts, ERDs, sequence diagrams), auditing documentation coverage against code, or establishing style guides.

**When NOT to use**: Writing marketing copy, blog posts, or content that does not live alongside code.

## Quick Reference

| Task                 | Approach                                        | Key Point                                    |
| -------------------- | ----------------------------------------------- | -------------------------------------------- |
| Doc sync audit       | `git diff main...HEAD` + export scan            | Compare symbols against doc coverage         |
| Sequence diagram     | Mermaid `sequenceDiagram` + `autonumber`        | Map messages to function calls               |
| ERD                  | Mermaid `erDiagram` + Crow's Foot               | Derive from Drizzle/Prisma schemas           |
| Gitgraph             | Mermaid `gitGraph`                              | Standardize on main/develop/feature branches |
| Feature release doc  | Overview + Config + Examples + Troubleshooting  | Checklist for every new feature              |
| API reference        | Generate from JSDoc/TSDoc annotations           | Never write API refs manually                |
| Style guide          | Active voice + present tense + direct address   | Conversational but precise                   |
| AI-assisted drafting | Inventory + gap analysis + draft + human review | AI drafts, humans verify accuracy            |
| Markdown standard    | YAML frontmatter + language-tagged code blocks  | Always specify code block language           |
| Complex diagrams     | Split into focused sub-diagrams + subgraphs     | Limit to 15-20 nodes per diagram             |
| README template      | Badges + description + quick start + API link   | First thing users see; keep under 200 lines  |
| ADR format           | Status, context, decision, consequences         | Numbered, immutable once accepted            |
| Runbook              | Symptoms, diagnosis, resolution, escalation     | Written for 3 AM incidents; no ambiguity     |

## Common Mistakes

| Mistake                                     | Correct Pattern                                                   |
| ------------------------------------------- | ----------------------------------------------------------------- |
| Using static images for technical diagrams  | Write Mermaid syntax inline in Markdown                           |
| Generic participant names like `Agent1`     | Use specific service or role names matching the architecture      |
| Manually writing API reference docs         | Generate from JSDoc/TSDoc annotations in source code              |
| Diagrams with 20+ nodes and no grouping     | Use subgraphs to group related nodes; limit to 15-20              |
| Documentation referencing outdated defaults | Run doc sync audit comparing exports against coverage             |
| Using "Click here" link text                | Use descriptive anchor text for accessibility and clarity         |
| Skipping heading hierarchy levels           | Never go from H2 to H4; keep hierarchy sequential                 |
| Mixing wall-of-text paragraphs              | Use bullet points, tables, and diagrams for scannability          |
| No ADRs for architectural decisions         | Record decisions with context, status lifecycle, and consequences |

## Delegation

- **Scan codebase for undocumented exports and documentation gaps**: Use `Explore` agent
- **Generate a full documentation site with diagrams from an existing codebase**: Use `Task` agent
- **Plan documentation architecture and information hierarchy for a new project**: Use `Plan` agent

> If the `mermaid-diagrams` skill is available, delegate complex diagram creation and advanced Mermaid syntax questions to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill mermaid-diagrams`
> If the `tldr-expert` skill is available, delegate summary and brief generation to it.

## References

- [Writing Style](references/writing-style.md) -- Voice, tone, formatting rules, error message guidelines, and structural standards
- [Mermaid Diagrams](references/mermaid-diagrams.md) -- Sequence, ERD, gitgraph, flowchart patterns with anti-patterns and troubleshooting
- [Doc Coverage](references/doc-coverage.md) -- Feature inventory, gap analysis, code-first and doc-first audit workflows
- [AI Collaboration](references/ai-collaboration.md) -- AI-human doc workflow, hallucination handling, documentation-as-code practices
- [Markdown Standards](references/markdown-standards.md) -- Frontmatter, headings, code blocks, tables, callouts, and link conventions
- [Runbooks and Onboarding](references/runbooks-and-onboarding.md) -- Incident runbook templates, escalation paths, and developer onboarding guides
