---
name: vocs-documentation
description: >-
  Rules and patterns for writing comprehensive, high-quality SDK documentation for public libraries
  on Vocs (vocs.dev). Covers documentation architecture, narrative tone, user guides, API references,
  and Vocs' agent-readable outputs (llms.txt, Markdown routes, MCP).
  Use when: (1) Writing or reviewing documentation for a public SDK/library,
  (2) Creating API reference pages for hooks/functions/classes,
  (3) Writing getting-started guides or tutorials,
  (4) Structuring a documentation site from scratch,
  (5) Reviewing documentation quality and consistency,
  (6) Setting up or configuring a Vocs documentation site for an SDK.
---

# SDK Documentation Best Practices (Vocs)

Rules for writing clear, scannable, code-forward documentation for public SDKs, targeting
[Vocs](https://vocs.dev) as the documentation framework.
Derived from analysis of best-in-class SDK documentation (wagmi, viem, TanStack). Rules are domain-agnostic; examples use generic SDK patterns with occasional web3 illustrations.

## Two Audiences, One Source

Vocs ships every page twice: rendered HTML for humans, raw Markdown for agents (`.md` routes,
`llms.txt`, `llms-full.txt`, MCP). You do not write two versions — you write Markdown that is
good enough to survive both surfaces. Everything below serves that goal, and it changes three
habits:

- **Structure is machine-readable.** Task-based headings, one topic per page, and a real
  `description` are what a retriever matches on. A page called "Overview" with three unrelated
  sections is worse in `llms.txt` than three focused pages.
- **Prose density is a token cost.** Padding that a human skims past is context an agent spends
  budget on. Terse fragments beat full sentences in reference material.
- **Interactive components must degrade.** Any custom MDX component in a page needs a `toMarkdown`
  hook, or it reaches agents as an opaque JSX tag. Run `vocs markdown-audit` to catch these.

See [references/agent-readable-docs.md](references/agent-readable-docs.md) for the mechanics.

## Documentation Type Router

The four types come from [Diátaxis](https://diataxis.fr): a craft has exactly two dimensions —
action vs cognition, and acquisition (study) vs application (work) — so there are exactly four
kinds of documentation, one per quadrant. When a page resists classification, use the compass: ask
*does this inform action or cognition?* and *does it serve the user's study or their work?*

| Informs… | Serves… | Type |
|---|---|---|
| action | study | Tutorial |
| action | work | How-to Guide |
| cognition | work | Reference |
| cognition | study | Explanation |

Before writing, identify which type of page you're creating. Each type has different rules.

| Question you're answering | Doc type | Template | Key rule |
|---------------------------|----------|----------|----------|
| "Help me learn this SDK" | **Tutorial** (Getting Started) | [guides.md → Tutorials](references/guides.md) | Learning-oriented: guide the reader, eliminate choices, show destination early |
| "Help me accomplish X" | **How-to Guide** (Task Guide) | [guides.md → How-to Guides](references/guides.md) | Task-oriented: assume competence, action-only, address real-world complexity |
| "What does X do / accept / return?" | **API Reference** | [api-reference.md](references/api-reference.md) | Information-oriented: describe only, zero explanation, mirror product structure |
| "Why does X work this way?" | **Explanation** (Concept/Why page) | [tone.md → Explanation Pages](references/tone.md) | Understanding-oriented: provide context, make connections, admit tradeoffs |

**The cardinal sin is mixing types.** A tutorial that stops to explain architecture loses the learner. A reference page that teaches loses the practitioner looking up a parameter. An explanation page that includes step-by-step instructions belongs in a how-to guide. Blur happens between map neighbors — the most common conflation in software docs is tutorial ↔ how-to guide; the subtlest is reference examples growing into explanation. The axis separating tutorial from how-to is study vs work, **never** basic vs advanced. See [references/diataxis.md](references/diataxis.md) for the boundary tests, per-type ground truths, and workflow guidance (guide, not plan — never scaffold four empty sections; improve one small thing at a time and let structure emerge).

## Core Philosophy

| Principle | Meaning |
|-----------|---------|
| Code is the star | Prose exists to introduce, contextualize, and connect code examples |
| Scannable over narrative | Readers skim for answers; structure for rapid lookup |
| Show, don't tell | Diff annotations and working examples beat explanations |
| One concept per step | Never introduce multiple ideas simultaneously |
| Full files, not snippets | Every code block should be runnable in isolation |
| Template rigidly | Predictable structure is a feature, not a limitation |
| Retrievable by default | A page an agent can't find or parse is a page that doesn't exist |

## Quick Reference: Critical Rules

| Category | DO | DON'T |
|----------|-----|-------|
| Voice | "you" for concepts, "we" for tutorials | Passive voice |
| Tone | Professional-casual, confident | Humorous, condescending, or stiff |
| Sentences | 10-25 words, active voice | 35+ word run-on sentences |
| Headings | `# Title [Subtext]` on every page; task-based `##` | Vague headings like "Overview", "Notes" |
| Frontmatter | `title` + `description` (feeds `llms.txt`) | Tags, categories, sidebar metadata |
| Code examples | Complete runnable files with `// [!code focus]` | Partial snippets missing context |
| Parameters | One `###` heading per param with full example | Tables or lists of parameters |
| Optional params | Indicate via `\| undefined` in type | "Optional" badges or markers |
| Jargon | SDK-specific terms explained; ecosystem terms assumed | Over-explaining industry basics |
| Sections | Rigid ordering: Import → Usage → Parameters → Return Type | Freeform section ordering |
| Cross-refs | Link to related APIs inline and in dedicated sections | "See also" dump at bottom |
| Warnings | `:::warning` callout directive | Inline bold warnings in prose |
| Navigation | Update `vocs.config.ts` `sidebar` in the same change as the page | Orphan pages reachable only by URL |
| Verification | `vocs build` after every docs change | Shipping unbuilt MDX |

## Detailed Guidance by Topic

- **Diátaxis ground truths**: See [references/diataxis.md](references/diataxis.md) for the compass, type-boundary tests (tutorial vs how-to, reference vs explanation), per-type principles sourced from diataxis.fr, iterative workflow, and structure at scale
- **Documentation structure**: See [references/structure.md](references/structure.md) for site architecture, page templates, navigation config, shared content systems
- **Narrative tone & explanation pages**: See [references/tone.md](references/tone.md) for voice, style, sentence patterns, jargon handling, and explanation/concept page guidance
- **Tutorials & how-to guides**: See [references/guides.md](references/guides.md) for tutorial rules (learning-oriented), how-to guide rules (task-oriented), progressive disclosure, framework variants
- **API references**: See [references/api-reference.md](references/api-reference.md) for parameter docs, return types, TypeScript presentation, OpenAPI, cross-referencing
- **Vocs setup & syntax**: See [references/vocs.md](references/vocs.md) for project init, config, markdown extensions, code annotations, twoslash, snippets, layouts
- **Agent-readable docs**: See [references/agent-readable-docs.md](references/agent-readable-docs.md) for `llms.txt`, Markdown routes, MCP server, `toMarkdown`, `markdown-audit`, search priority
