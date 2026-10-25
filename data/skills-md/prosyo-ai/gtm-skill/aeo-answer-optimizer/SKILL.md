---
name: aeo-answer-optimizer
description: "Use this skill when you want your brand recommended and cited by AI assistants and answer engines (ChatGPT, Claude, Gemini, Perplexity, AI Overviews): \"answer engine optimisation\", \"get cited by ChatGPT\", \"AEO audit\", \"why doesn't AI recommend us\", \"generative engine optimization\". Finds the questions buyers ask assistants in your category, checks how answers describe you today, and rewrites pages so they give extractable, factual, well-structured answers with clear entities, comparisons, schema and third-party corroboration."
license: MIT
metadata:
  title: AEO answer optimizer
  category: content-seo
  tags: "Marketing, Founders, Demand Gen"
  author: prosyo
  version: "1.0.0"
  keywords: "answer engine optimization, aeo checklist, get cited by chatgpt, generative engine optimization, claude aeo skill, ai search visibility"
  inputs: "Category and product, Key pages, Buyer questions"
  outputs: "Question map, Current answer audit, Page rewrites, Structured data and corroboration plan"
---

Use this when buyers ask AI assistants which tool to use and your brand is missing or described wrongly. AI answers favour sources that state facts clearly, answer the question directly and are confirmed by other sources.

## Inputs

- The category, product and the facts that define it (who it is for, pricing model, key capabilities, integrations).
- The pages that should be cited: home, product, pricing, comparisons, docs.
- The questions buyers ask (from sales calls, search and support).

## The play

### 1. Map the questions
Group buyer questions by type: "what is", "best tools for", "x vs y", "how to", "how much does", "is x good for <use case>". Prioritise commercial questions where a recommendation is made.

### 2. Audit current answers
Ask several assistants the top questions. Record whether you are mentioned, what is said, which sources are cited and what is wrong or outdated. Repeat monthly; answers change.

### 3. Rewrite pages for extraction
Read [references/aeo-checklist.md](references/aeo-checklist.md) for the page-level checklist. The core:
- Lead each section with a direct, one or two sentence answer, then the detail.
- State facts plainly and consistently across pages: what it is, who it is for, price, limits.
- Use comparison tables with clear criteria; assistants reuse tables well.
- Name entities precisely: product names, categories, integrations, use cases.
- Keep facts fresh and dated where they change.

### 4. Make it machine-readable
Organization, Product or SoftwareApplication, FAQPage and Article schema; a clean sitemap; fast, crawlable HTML (key text not hidden behind scripts); an `llms.txt` summary with links to the most important pages; and no blocking of the AI crawlers you want to be cited by.

### 5. Build corroboration
Assistants trust facts confirmed elsewhere: review sites, directories, partner pages, community answers, credible articles. Make sure third-party descriptions match your own.

## Output format

```
Question map: <question - type - priority - currently mentioned? - cited sources>
Wrong or missing facts: <...>
Page fixes: <page - change - why>
Schema and technical: <...>
Corroboration targets: <sources to update or earn>
Re-check: <date and questions to re-run>
```

## What good looks like

- One consistent fact sheet about the product, reused everywhere.
- Comparison and "best for" pages that are honest about fit; assistants pick up balanced sources.
- Progress measured by mentions and citations on the priority questions, checked monthly.
- The common mistake is writing for keywords alone, with answers buried in paragraph four of a long intro.

## Rules

- MUST keep every claim accurate and consistent across pages.
- MUST measure with repeatable question sets over time, not one-off screenshots.
- NEVER publish fake reviews, fake third-party pages or hidden text aimed at AI crawlers.
- NEVER make claims about competitors you cannot support.

## Example prompts

- "Audit how AI assistants describe us for 'best AI SDR tools' and fix our pages."
- "Rewrite our pricing page so answer engines quote it correctly."
- "Build a monthly AEO tracking sheet for our 20 most important buyer questions."
