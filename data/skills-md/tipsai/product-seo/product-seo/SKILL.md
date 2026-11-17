---
name: product-seo
description: Grows search traffic that turns into signups for a product website, working from real Search Console data instead of guesses. Use when the user asks about SEO, organic or search traffic, Google or Bing rankings, Search Console, keyword research, which pages to write, rewrite, merge or remove, titles and meta descriptions (CTR), use-case or landing pages for a specific query, free tools, comparison and alternatives pages, 301 redirects for thin or duplicate pages, backlinks and directory listings, llms.txt or showing up in ChatGPT and other AI search answers, or checking whether an SEO change worked and should be rolled back.
license: MIT
compatibility: Scripts need Node.js 18+ and internet access. Without them the skill works from a Search Console CSV export.
metadata:
  version: "0.1.0"
---

# Product SEO

SEO for a website that sells a product. The goal is signups from search. Impressions and clicks are only evidence on the way there.

The method: take the site's own search data, sort topics by whether the product is the answer, work on the ones where it is, across the whole site, then measure each change and undo the ones that hurt.

## Rules that always apply

1. **Data before opinions.** Start from Search Console. For a site with no impressions yet, use keyword data. Never guess what people search for.
2. **Judge by signups.** Every topic goes into one of two piles: "the product is the answer" or "traffic only". Work the first pile. See `references/triage.md`.
3. **Look at what ranks before choosing what to build.** If the first ten results for a query are tools, an article will not rank there.
4. **Fewer, better pages.** One page that answers the query better than the current top ten beats ten pages that repeat them. Improve or merge an existing page before adding a new one. Never produce pages in volume.
5. **No invented facts.** About the user's product: only what is in `seo/product-facts.md`. About other products: only from their official pages, with the exact quote, the URL and the date. No source, no claim. See `references/facts.md`.
6. **No statistics taken from the product's users in public text.** A number from user data tells readers their data is being read.
7. **A human approves every change that goes live**: publishing, redirects, removals, outgoing messages. Humans submit forms and send emails. You prepare everything up to that point.
8. **Save before changing.** Back up the old version, change one thing per page, and log the change with the dates when it will be checked.
9. **Languages.** Reply in the language the user writes in. Write site content in the site's language. Never mix two languages in one file or one message.
10. **Report plainly.** Verdict first, then the evidence with its date range, then what to do next. When something could not be checked, say so instead of filling the gap.

## First run

Look for `seo/site-profile.md` in the project.

If it is missing:
1. Read `references/setup.md`.
2. Ask the user, in a few short questions: what the product does in one line, who pays for it, what must never be claimed about it, which language the site is in, how pages get published.
3. Create the `seo/` workspace from the templates in `assets/` and fill `seo/site-profile.md` and `seo/product-facts.md` with the user. Ask where product changes show up and which analytics exist, and record both in the profile.
4. Add the short block from `assets/agents-block.md` to the project's `CLAUDE.md` or `AGENTS.md`, after showing it to the user. Every later session then knows where the SEO notes are, even when this skill is not loaded.
5. Check what data is available. A CSV export from Search Console is enough to start. If the site is not in Search Console yet, or has almost no impressions, help connect it (`references/setup.md`) and follow the "New site" plan in `references/triage.md`.
6. Run triage (`references/triage.md`) and show the two piles.

If it exists, at the start of every session:
1. Read `seo/site-profile.md`, `seo/change-log.md` and `seo/lessons.md`.
2. Tell the user which checks in the change log are due or overdue.
3. Check what changed in the product since the date in the profile, update `seo/product-facts.md`, and list live pages that mention a changed fact. See `references/facts.md`, "Keeping up with the product".

## Pick the play

| Situation | Play | Read |
|---|---|---|
| "Where do I start?", "audit my SEO", no plan yet | Triage: two piles and an ordered list | `references/triage.md` |
| "What should we write about?", the list of ideas has run out | Sources of ideas, page types, what to avoid | `references/content-ideas.md` |
| "Check our existing pages", old pages nobody has re-read, a product fact changed | Audit live pages: text, phone view, facts, links, calls to action | `references/page-audit.md` |
| Product queries stuck at positions 8–20 | Rewrite the page | `references/page-workflow.md` |
| Page is on page one but few people click | New title and description | `references/titles-and-snippets.md` |
| Several pages compete for one query, or many thin pages | Clean up, merge with 301 | `references/cleanup-and-merge.md` |
| The results for a query are tools or landing pages | A page where the visitor does the task, or a small free tool | `references/task-pages-and-tools.md` |
| "X vs Y", "alternatives to X", "best X" | Honest comparison page | `references/comparison-pages.md` |
| Few sites mention the product | Listings, mention exchange, getting into lists | `references/links-and-listings.md` |
| "How do I show up in ChatGPT?", llms.txt | AI search basics | `references/ai-search.md` |
| A change went live one or three weeks ago | Measure, keep or roll back | `references/measure-and-rollback.md` |
| New site with no impressions | Keyword data, then the same two piles | `references/triage.md`, section "New site" |

When the request does not say which play, run triage first and propose one.

## The loop for one page

Every page, new or rewritten, goes through the same steps. Each step has its file.

1. **Queries.** What this page is found for, and which words carry the impressions. `references/page-workflow.md`
2. **Facts.** Product facts from the file, competitor facts collected by a separate agent. `references/facts.md`
3. **Draft.** Form, length and text rules. `references/page-workflow.md`
4. **Images.** `references/images.md`
5. **Review by a second model** until the "sounds like AI" score is 3 or lower, then a reader pass on screenshots, then your own full read. `references/review.md`
6. **The owner sees the page as it will look and says "ok".** Nothing goes live before that.
7. **It goes live.** The owner pastes it in, or you publish that single item if they gave you access. `references/publishing.md` (optional)
8. **Log it** with check dates at one and three weeks. `references/measure-and-rollback.md`
9. **Write down what you learned** in `seo/lessons.md`. The next page starts by reading it.

## Second model for review

A different model catches more than the one that wrote the text.

- Running in Claude Code with the Codex CLI installed: send the review to Codex.
- Running in Codex with Claude Code installed: send it to Claude.
- Neither: use a fresh subagent that has not seen the drafting. Say in the report that the review was done by the same model.

## Workspace

The skill keeps its state in a `seo/` folder in the user's project, so nothing depends on one session's memory. Create it from `assets/` on first run; `assets/workspace-readme.md` becomes `seo/README.md`.

```
seo/
  README.md          one line per file and folder
  site-profile.md    product, who pays, the two piles, standing decisions; read every session
  change-log.md      every change, its backup, check dates, results; read every session
  lessons.md         what to do differently; read before every new page
  product-facts.md   the only source for claims about the product; dated lines
  experiments.md     one hypothesis per page
  sources/           facts about other products: quote, URL, date
  backups/           old versions of changed pages
  audits/            page audit reports
  listings/          directory texts and the checklist of places
  data/  shots/      Search Console rows, screenshots; not in git
```

## Scripts

Scripts live in `scripts/` in this skill folder. Run them, do not read them into context; each prints its options with `--help`. They need Node.js 18 or newer and no packages, except `shoot.mjs` and `brand.mjs`, which need Playwright installed in the project. Run them with the user's project as the working directory so that `seo/` and `.env` resolve, and call each one by its full path inside this skill folder: `node <this skill's folder>/scripts/opportunities.mjs --help`. In the reference files `scripts/…` means that path.

`opportunities.mjs`, `coverage.mjs` and `measure.mjs` also read the CSV tables of a Search Console export, so they work without API access.

| Script | Use it to |
|---|---|
| `scripts/gsc-fetch.mjs` | Download Search Console rows through the official API |
| `scripts/opportunities.mjs` | List positions 8–20, weak CTR on page one, pages competing for one query, queries with no page |
| `scripts/coverage.mjs` | Check that the words people search with are in a page's title and headings |
| `scripts/measure.mjs` | Compare a page before and after a change and apply the rollback rule |
| `scripts/indexnow.mjs` | Tell Bing and other IndexNow search engines about new or changed URLs |
| `scripts/shoot.mjs` | Screenshot a page at three widths, or turn an HTML file into an image |
| `scripts/brand.mjs` | Read the site's colours, fonts and logo into `seo/brand.md`, so images match the site |

No Node, no credentials, or a sandbox without internet: work from the CSV files the user exports from Search Console and do the same analysis by hand. Say which numbers come from an export and what its limits are.

## What this skill does not do

- It does not produce an "SEO score". There is no honest way to compute one.
- It does not generate pages in bulk.
- It does not promise positions or traffic.
- It does not publish, redirect, delete or send anything without the owner's "ok".
