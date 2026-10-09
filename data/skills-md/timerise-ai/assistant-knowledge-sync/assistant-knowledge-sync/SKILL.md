---
name: assistant-knowledge-sync
description: >
  Update what a site's AI chat assistant knows after the site changes: find
  the gap between the pages and the assistant, move page copy into one data
  module both read, add the new pages to the assistant's knowledge pack and
  searchable corpus, derive its site map from the sitemap source, write the
  routing and "never quote" guardrails, and prove it with unit tests and live
  probes. Use when: (1) a page, section, program, catalog or route was added or
  rewritten and the assistant should know about it, (2) the assistant answers
  with stale facts, wrong links, invented prices or sends people to the wrong
  form, (3) the sitemap changed and the assistant's site map did not, (4) the
  user mentions: update the assistant's knowledge, teach the chatbot about, the bot
  doesn't know about the new page, sync the AI assistant with the site,
  knowledge pack, system prompt facts, searchKnowledge, readKnowledgeDocument,
  KnowledgeDocument, tool description, site map for the assistant, sitemap.ts,
  the bot invents prices, never quote, probe the assistant. Carries the seven
  surfaces where assistant knowledge lives, the single-source refactor that
  keeps page and assistant reading the same words, guardrail templates, and
  regex probes that check routes and numbers. Next.js App Router sites whose
  assistant prompt is assembled in code from repository content (AI SDK or
  similar, with search and read tools); the host's prompt, knowledge, tools and
  probe modules are the seam. Not for building a chatbot, not vector or RAG
  infrastructure, not fine-tuning, and not for writing the page copy itself.
---

# Assistant knowledge sync

A site's assistant goes stale the day a page ships without it. The fix is not a longer prompt: **the
assistant must read what the page renders, never a retyped copy of it.** Every fact gets one source of
truth in the repository, the page and the assistant both import it, and a probe proves the assistant
uses it.

Written by the engineer who has shipped this work. The earlier implementation it was audited against was
the assistant of a marketing site answering on more than one channel from one knowledge module. The facts
and rules below are what the unit tests, the render check and the probes verify;
[provenance.md](references/provenance.md) has the record.

## When to use

- A page, section, partner program, product, catalog entry or route was added or rewritten.
- The sitemap changed and the assistant's site map did not.
- The assistant gives stale versions, wrong links, invented numbers, or routes people to the wrong form.
- After a content sync (a catalog pulled from another repository) the assistant still lists the old one.

## When NOT to use

| Instead of this | Use |
|---|---|
| Building the assistant, its widget or its transport | `ai-sdk` (chat on the site) or `slack-ai-bot` |
| Embeddings, a vector store or hosted RAG | a RAG stack; this skill keeps an in-repo pack and keyword corpus |
| Writing or editing the page copy | the host's content workflow; this skill moves copy, never rewrites it |
| Changing the model, provider or failover | the host's AI config |
| A one-word fact fix in the hand-written prompt | edit it; the full procedure is for new surfaces |

## Architecture

```
 repo content (markdown, i18n, data/*.ts)        page.tsx <--- data module (plain text)
              |                                                     |
              v                                                     v
   +----------------------- knowledge module ----------------------------+
   | corpus: documents {kind, title, url, summary, tags, content} ---------> search and read tools
   | pack:   sections + site map + indexes ---------------------------------> system prompt
   | live:   external index joined with local facts ------------------------> system prompt, list tool
   +---------------------------------------------------------------------+
 prompt module: hand-written facts + routing, link and "never quote" rules, per channel
 probe script:  question, expect[] and reject[] regexes against the running assistant
```

The knowledge module is the host's; this skill extends it. The seam table, the three knowledge functions
the templates call and the rename table are in [adaptation.md](references/adaptation.md).

## Critical facts

1. **Tool descriptions gate retrieval.** If the search tool's description lists "help, blog, case
   studies", the model will not search for a page of a kind you just added to the corpus.
2. **A hand-written site map drifts.** Only a site map built from the arrays and routes the sitemap uses
   gains a route when the sitemap does.
3. **Copy inline in a TSX file is invisible to the assistant.** The knowledge module can import a data
   module but not the constants inside a component.
4. **An external index can lag the synced content.** When both exist, the visitor sees the page's
   version, so the assistant must show the same one.
5. **The model fills silence with numbers.** Anything not yet published (payouts, prices, dates) needs
   an explicit "not published; never quote" line, or it will be invented.
6. **Routing is knowledge too.** "Who goes where" (join, buy, support) belongs next to the facts, because a
   correct answer with the wrong next step still loses the visitor.

## Hard rules

> **Never retype page copy into the prompt.** Import it from the module the page renders. A retyped copy is
> correct for one deploy.

> **Never rewrite the copy while moving it.** A single-source refactor is byte-for-byte and the page renders
> identically. Wording changes are a separate commit and a separate decision.

> **Never add a document kind without updating the tool descriptions and link rules.** The model searches
> by the description, not by what the corpus holds.

> **Never ship without a probe per new fact and one per guardrail.** Unit tests prove the pack contains
> the line; only a live probe proves the model uses it.

> **Never let the pack grow unbounded.** Indexes and summaries go in the pack; full bodies stay behind the
> read tool. Measure the pack's size before and after.

## Working unattended

The skill needs the host's assistant code. When it is not in the repository, it is cloned from a public
repository or carried in the task, and neither a clone nor the package registry is an external service in
an eval's sense. With no model key in the environment, live probes are written and reported as not run,
never as passing; every other layer still runs (see [verification.md](references/verification.md)).

- **Commit nothing and create no branch.** Leave the refactor and the knowledge change in the working tree;
  the operator commits them, in that order, from the file lists in the handover.
- **A seam the host lacks stays absent.** No sitemap source: add the route to the site map the pack already
  has. No transport to the assistant: `scripts/ask.mjs` throws until it is wired. Never invent a routes
  module, an endpoint or an environment variable, and never copy a host file to a canonical path. The docs
  line is the exception: a host without one gets it, as a line in its `README.md`.
- **Copy the shipped tests whose seams the host has**, assertions unchanged: with no catalog, the program
  and pack tests, 2 of the 4. Extra tests go beside them. The host's search scorer stays; tags are the lever.
- **Hand over**: each probe as written and not run, with its command; the absent seams; the pack's size
  before and after; which shipped tests ran; and the files of each of the two commits.

## Quick start

1. **Probe the host** and fill the seam table: [surfaces.md](references/surfaces.md),
   [adaptation.md](references/adaptation.md).
2. **Audit the gap**: what changed, which facts are new, what the assistant says today:
   [gap-audit.md](references/gap-audit.md).
3. **Single-source the copy** that lives only in components, as its own commit:
   [single-source.md](references/single-source.md).
4. **Extend corpus, pack, site map and live index**: [pack-and-corpus.md](references/pack-and-corpus.md).
5. **Write the guardrails**: routing, links, unpublished facts, kinds, tool descriptions, every
   channel: [guardrails.md](references/guardrails.md).
6. **Verify**: typecheck, lint, unit tests, pack dump, render check, live probes:
   [verification.md](references/verification.md).
7. **Update the project docs line** that says what the assistant knows (add it when there is none), then
   commit the refactor and the knowledge change as two commits (unattended: list them in the handover).

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Fitting this to the host's assistant | seam, rename, knowledge interface, searchKnowledge, getKnowledgePack, i18n, locale, channels, order of work | [adaptation.md](references/adaptation.md) |
| Where the assistant's knowledge lives in this host | system prompt, knowledge pack, corpus, tools, channel, Discord, MCP, host probe | [surfaces.md](references/surfaces.md) |
| What the assistant is missing | stale, doesn't know, new page, git log, sitemap diff, baseline | [gap-audit.md](references/gap-audit.md) |
| Page copy only exists inside a component | inline constants, FAQ array, roles, cards, data module, drift, metadata | [single-source.md](references/single-source.md) |
| Making a page searchable and listed | KnowledgeDocument, kind, catalogOffer, site map, sitemap.ts, live index, version, pack size | [pack-and-corpus.md](references/pack-and-corpus.md) |
| The assistant says the wrong thing | invents prices, wrong form, wrong link, never quote, tool description, allowed topics | [guardrails.md](references/guardrails.md) |
| Proving it | vitest, bun test, pack dump, render check, probe, expect, reject, regex, no model key | [verification.md](references/verification.md) |
| The audit ledger: what changed, was kept and was added | provenance, fixed, kept deliberately, added, fix order | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
