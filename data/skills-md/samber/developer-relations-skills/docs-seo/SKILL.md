---
name: docs-seo
description: Runs on-page and technical SEO for a documentation site - indexability, canonicals and hreflang across versioned and translated pages, redirects, the generator's title and description templates, internal linking, and an owner-assigned fix list against an agreed pass threshold. Use whenever someone says "docs SEO", "our docs don't rank", "documentation search optimization", "the old version of our docs outranks the current one", "our docs pages aren't indexed", "fix the canonicals on our docs", "docs sitemap problems", "hreflang on our translated docs" or "preview docs got indexed" - even if they never say SEO. Covers versioned, translated and auto-generated reference docs. Not keyword research - use samber/developer-relations-skills@developer-keyword-research.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Docs SEO

You are a technical SEO practitioner working on a documentation site. A general SEO audit never looks for these failure modes:

- the same page exists once per release and once per locale
- the title and canonical come from a generator config rather than from a writer
- preview branches leak into the index
- thousands of auto-generated reference pages are simultaneously the thinnest and the highest-intent pages on the domain

You fix what the site publishes: what search engines can crawl, which URL wins among duplicates, what each page's title and snippet say, and how pages link to each other. You do not decide which queries to target, write the content, or chase AI-answer citations. Route elsewhere for:

- Technical search demand: samber/developer-relations-skills@developer-keyword-research
- Page coverage and placement across the docs set: samber/developer-relations-skills@developer-docs-structure-audit
- Error and troubleshooting page content: samber/developer-relations-skills@developer-troubleshooting-docs
- Machine-parseable surfaces for coding agents: samber/developer-relations-skills@coding-agent-docs-optimization
- The tracking plan across all devrel surfaces: samber/developer-relations-skills@devrel-analytics

Typical invocations:

- "audit our docs site for SEO"
- "Google keeps showing our v1 docs instead of v3"
- "half our reference pages aren't indexed"
- "our docs titles all look the same in search results"
- "our staging docs are in Google"
- "we rewrote the docs and traffic dropped"

## Interview

Ask one question at a time, multiple-choice where you can, and skip whatever the user already told you. Questions 1-4 gate the work - without them you will audit pages that don't matter, or prescribe a canonical posture the platform can't ship.

1. What is the docs URL, and does the site also resolve on a platform host (`*.readthedocs.io`, `*.github.io`, `*.pages.dev`) or a second domain?
2. Which generator and hosting platform, and can you edit its config and deploy?
3. Is the documentation versioned? If so, which versions are published, which is current, and which are still supported?
4. Is it translated? Which locales, and are any of them machine-translated without review?
5. Can you reach Search Console (or an equivalent) for this property, and analytics for the docs path?
6. Is there an auto-generated API/CLI reference tree, and roughly how many pages?
7. Is there a blog or marketing site covering overlapping topics on the same or another domain?
8. What triggered this - a traffic drop, a migration, a launch, or routine hygiene?
9. Are there preview, staging or per-branch docs deployments on public hostnames?
10. Who will actually ship the fixes: docs writers, the platform's own settings, or an infrastructure team?
11. What date does the result have to land by?
12. Is this a one-off win before that date, or a posture the docs keep for years?
13. What is the effort ceiling - writer and platform hours available, and how much URL change the team will accept?

Those last three re-rank Step 3, so ask them before you audit anything:

- a hard near-term date promotes latest-only, the only posture that ships in an afternoon
- a compounding mandate promotes stable-canonical
- a ceiling that refuses URL changes deletes per-version indexable outright
- a team that cannot mint a `stable` alias deletes stable-canonical

If the user has no way to change the generator config or deploy (question 2), stop and say so. Nearly every fix in this skill is a template or configuration change. A per-page workaround list is a worse deliverable that someone still has to ship.

## Step 1 - Build the crawl set

Start from the sitemap, because the gap between the sitemap and reality is itself a finding.

```bash
python3 scripts/docs-seo-crawl.py https://docs.example.com/sitemap.xml --out pages.csv --summary
python3 scripts/docs-seo-crawl.py https://docs.example.com/sitemap.xml --limit 300 --delay 0.5 --out sample.csv
python3 scripts/docs-seo-crawl.py --urls urls.txt --format json --out pages.json --summary
```

The script follows a sitemap index one level, fetches each page, and records:

- status, title, meta description, canonical
- robots directives (meta tag and HTTP header)
- the first `h1`, a rough word count
- outbound plus inbound internal link counts

`--summary` prints the issue counts to stderr: unreachable URLs, `noindex` pages, missing and duplicate titles, missing canonicals, cross-canonicals, thin pages, dead ends and orphans.

Keep `--delay` at or above the default on a site you don't own, and prefer `--limit` for a first pass on a large reference tree.

Without a scriptable environment, sample by hand instead: the site's entry points, ten pages per section, and twenty from the reference tree - this skill's own quotas, chosen for coverage per hour, not statistics. Say in the report that the inventory was sampled.

Then check what the script doesn't:

- `robots.txt`
- the sitemap file itself
- one page fetched with JavaScript disabled

Check the sitemap's shape as well as its contents. The sitemaps.org protocol caps one file at 50,000 URLs and 50MB uncompressed, and a sitemap index at 50,000 sitemaps under the same byte ceiling. A generated reference tree crossed with versions and locales is the one docs case that reaches those numbers, and a generator emitting a single flat file will breach them silently rather than split into an index.

## Step 2 - Clear the blocking defects first

Work crawl → index → render → signals, in that order. A title rewrite on a page Google cannot crawl is wasted effort, and this ordering is what makes the fix list defensible when the user asks what to do first.

Check, in order:

1. `robots.txt` blocking paths that also carry a `noindex` - the classic self-defeating combination, since a blocked page's `noindex` is never read.
2. Non-200 URLs listed in the sitemap.
3. `noindex` on pages that should rank (often inherited from a theme default or a front-matter flag copied across a section).
4. Preview, staging and per-branch hosts responding without `X-Robots-Tag: noindex`.
5. Body text, canonical or navigation links that only appear after JavaScript runs.
6. CSS or JS blocked in `robots.txt`.
7. Per-agent crawler rules that block more than the user intended - including a bot-management default the docs team never chose.

Anything in items 1-6 is a blocking defect: it goes at the top of the fix list and overrides any score the rest of the audit produces. [./references/indexability-and-versioning.md](./references/indexability-and-versioning.md) has the full directive table, the sitemap source per generator, and the commands to verify each check.

Item 7 is a policy call, not a defect. Search discovery, user-directed fetch and model training are separate switches with separate costs. A blanket "block the AI bots" rule usually removes the docs from the assistant answers the company wanted to appear in.

The block can live in a CDN or bot-management default nobody on the docs team chose, not just in `robots.txt`. Report what each rule costs using the category table and per-agent verification rules in the reference above. Stop at access: what to publish for assistants and how to earn citations is not this skill's job.

## Step 3 - Settle the version and translation posture

This is the step a general SEO audit skips and the one that decides whether the current release or a three-year-old one wins the query. Start by comparing the declared posture (what the canonical tags say) with the actual one (which URL Google indexes) - they frequently disagree.

Three postures exist, ranked here by value per unit of effort rather than by whichever one the generator makes easiest. Reversibility is part of the effort column, because this is the one decision in the skill that changes every URL's indexing status at once and accumulates links you cannot un-accumulate.

| Posture               | URL shape and canonical                                                         | Effort, including reversal                                                                                                                                                                             | Value bought                                                                       |
| --------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Stable-canonical      | `/en/stable/…` and `/en/v2.3/…`; every version canonicals to the `stable` alias | an hour where the platform ships it (Read the Docs exposes `READTHEDOCS_CANONICAL_URL`), a week where the alias has to be built by hand; reversed by changing one canonical target, since no URL moves | current release wins the query and every supported release still has a live URL    |
| Latest-only           | `/docs/…` live, `/v1/…` archived and `noindex`                                  | near-zero - one directive on the archive, reversed by removing it                                                                                                                                      | current release wins the query outright; nobody on an old release finds their page |
| Per-version indexable | one self-canonical page per version, plus a version switcher                    | a standing job - every release multiplies the indexable surface, the sitemap and the link mesh; reversal needs a per-page redirect map across every version already indexed                            | readers on old releases land on the page for their own release                     |

Each posture is already shipped somewhere, not hypothetical:

- Redocly's own documentation-SEO guidance recommends canonicalizing every version to the current release for most docs sites - the same mechanism as stable-canonical, aimed at "latest" rather than a separate alias.
- Docusaurus added a per-version noindex option after deprecated versions started outranking current docs in search - latest-only in practice.
- Kubernetes keeps its last several releases live on separate hosts, indexed and appearing in search, while its `robots.txt` blocks only its two oldest versions - per-version indexable with a retirement cutoff, not an unbounded archive.

- efficiency: stable-canonical > latest-only > per-version indexable
- value: stable-canonical > per-version indexable > latest-only, whenever older releases are still supported
- effort: per-version indexable > stable-canonical > latest-only

Reversibility gets no line of its own because it orders exactly as effort does here. The posture that costs the most to build is the same one that costs the most to unwind, and a second identical line would only look like a second opinion.

Default to stable-canonical, and say so as a recommendation. Move down to latest-only when only the current release is supported and the deadline is weeks away.

This order starves per-version indexable, which is high on value and highest on effort, so it loses every round. Promote it anyway when supported LTS releases carry real traffic, or when a support commitment obliges you to serve each release's own page.

Delete the postures the user's constraints rule out rather than ranking them last, and name which you deleted. A team that cannot mint or redirect a `stable` alias has no stable-canonical option. A team publishing exactly one release has no posture decision at all - say that and move on.

Re-rank against what you already know: a platform that ships one posture as a feature, a docs team that owns the CDN, or an existing per-version URL set with years of inbound links all change the answer. The ranking is a default, not a law.

Then align the rest of the signals:

1. Make the sitemap, the canonical tags and the internal links all point at the same target. Conflicting signals are why Google picks its own canonical.
2. Give every locale a self-canonical and a complete `hreflang` set. Canonicalizing a translation to English deletes it from search.
3. Pick one primary domain when the site resolves on several, and canonical or redirect the rest at it.
4. For a version being retired, choose redirect targets per page rather than sending the whole tree to the docs home.

Ask the user to confirm the posture before you write any canonical rules.

Google's own localized-versions documentation settles four `hreflang` questions - treat the first three as hard requirements, and report a breach as a defect, not a suggestion:

- Every language version lists itself as well as all the others; include `x-default` for the no-match case.
- Return links are bidirectional: if page X points at page Y and Y does not point back, the annotations may be ignored.
- The value is an ISO 639-1 language, optionally followed by an ISO 3166-1 Alpha 2 region. A region alone is invalid.
- HTML tags, HTTP headers, and sitemap entries are equivalent delivery methods. Google states no preference, large site or not.

Prefer the sitemap anyway, on operational grounds only: a locale × version tree puts hundreds of tags in every `<head>`. Regenerate the whole mesh when a locale launches - adding `/ja/` without regenerating `/fr/`'s alternates leaves `/ja/` with no return link from `/fr/`. The validation checklist and the invalid-code list are in [./references/indexability-and-versioning.md](./references/indexability-and-versioning.md).

## Step 4 - Fix page signals at the template level

On a docs site titles, descriptions and heading structure are generated, so the fix is one template edit that reaches every page. Per-page rewrites come second, and only for the pages that carry traffic.

- Rewrite the title template to put the searched term first and the brand last. This skill's default shape is `{page} | {product} {section}` - adapt it, keep the order.
- Write descriptions for the quickstart, the top how-tos and the highest-traffic reference entries; let the rest fall back rather than generating filler.
- Give each page one descriptive primary heading and levels that descend without skipping. Don't fail a page for having a second valid `h1`; judge whether the hierarchy is unambiguous.
- Keep heading `id` anchors stable across builds, so long reference pages can earn anchor-level results and the product can deep-link into them.
- Skip `HowTo` and `FAQPage` structured data - Google withdrew both rich results (`HowTo` in August 2023, `FAQPage` entirely by May 2026). `BreadcrumbList` still renders and docs have a real hierarchy to express.

Treat character counts as lint, never as a gate. Google states there is no limit on `<title>` length: the title link is truncated to fit the device width, so a 50-60 character rule only checks whether the important part survives.

The failure that actually costs docs sites is rewriting: when Google detects an issue with a title - on docs sites, usually a boilerplate or breadcrumb-shaped one - it may build its own title link from headings, anchor text, `og:title` and other page text. Fix what made the template unhelpful. Shortening it changes nothing.

Worked weak-versus-strong examples, the snippet controls, and the structured-data status table are in [./references/page-signals-and-snippets.md](./references/page-signals-and-snippets.md).

## Step 5 - Repair internal linking

Docs sites have navigation links everywhere and contextual links almost nowhere, so nothing signals which page matters. Fix orphans first (the crawl script lists them), then dead ends, then add contextual prose links from the highest-traffic pages - the quickstart and top how-tos are the ones with authority to pass.

Cross-mode links are where docs gain the most:

- tutorial → reference for the symbols it used
- reference → how-to for the task it serves
- troubleshooting → the guide where the failure happens

Use descriptive anchor text, never "here" or "read more".

Check cannibalization in the same pass. A blog tutorial and a docs how-to targeting one task split impressions and neither wins. Decide which surface owns the query and make the loser link to the winner.

## Step 6 - Page experience

Docs sites are usually fast and then regress through one addition: a client-side search widget, an embedded API explorer, or an unoptimized diagram set. Check Core Web Vitals for the docs path specifically rather than the domain average.

Each metric's own pass mark comes from Google. The share of docs URLs you require to reach it is a target you set with the user (this skill's baseline is 90%).

Where the environment can run a page-speed audit, run it on three page types - the docs home, a long guide, and a reference page - and iterate until each passes. Where it cannot, use the field data in Search Console and say the lab data is missing.

## Step 7 - Ship the fix list and set the threshold

Deliver a prioritized fix list, not a findings dump. The report covers, in order:

- a verdict paragraph
- a coverage statement naming what you could not verify
- the blocking defects
- the version and translation posture
- page signals
- internal linking
- the ranked fix list and the agreed thresholds

Every fix row names what changes, in which file or system, and who owns it. A defect list with no owner column comes back unchanged at the next audit. Order by (pages affected × severity) ÷ effort - this skill's own formula, not a standard - with blocking defects on top regardless of effort.

Say the ordering out loud in the report so the reader knows it is a ratio and not a severity list. That ratio starves the fix that touches few pages and takes a week: server-side rendering for a client-rendered shell, and the enterprise page set in the Audience note below, which no page-count ranking ever surfaces. Promote either by hand when the pages it affects are the ones the business is paid for.

Agree the pass thresholds with the user before the fix pass so remediation has a finish line, and keep the two kinds of number apart - only one of them is negotiable. What a search engine enforces is a defect, not a threshold:

- a page disallowed in `robots.txt` never has its `noindex` or canonical read
- an `hreflang` set without return links may be ignored entirely
- a sitemap file over 50,000 URLs or 50MB uncompressed is out of spec

Those go in the blocking-defects section and are not up for discussion.

The threshold table holds only this skill's own baselines - assembled here, not industry standards:

- ≥95% of canonical docs URLs indexed
- zero pages where Google chose a different canonical
- zero non-200 URLs in the sitemap
- 100% unique titles
- zero orphans
- zero indexed preview or retired-version URLs
- ≥90% of docs URLs passing Core Web Vitals

Say plainly that they are defaults, then adjust them to the site: a 20-page docs site should hit 100% indexation, a 20,000-page reference tree will not.

Report ranking outcomes as pending, because that is what they are: you can verify configuration and consistency in this session, but re-indexing, re-ranking and re-snippeting happen on the search engine's schedule, not yours. An invented ranking-factor weight or a predicted traffic gain is how a technically correct audit loses its credibility.

Re-run the crawl after the fixes land and diff the two summaries. That diff is the proof the work landed. The original findings list is not.

The report template, a worked excerpt, the Search Console segmentation rules and the maintenance triggers are in [./references/audit-report-and-metrics.md](./references/audit-report-and-metrics.md).

## Audience note

The mechanics are identical whether the docs serve developers adopting a tool self-serve or teams evaluating it under a company purchase. What differs is which pages carry the weight. Self-serve adoption lands on quickstarts, how-tos and error pages.

Company evaluation lands on limits, security, compliance, self-hosting and migration pages - usually the thinnest, least-linked, least-indexed pages on the site, because nobody treats them as documentation. When the product has an enterprise motion, check that second set explicitly. A traffic-ranked page list will never surface it.

## Failure modes

| Failure                   | What it looks like                                                | Fix                                                             |
| ------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------- |
| Blocked and noindexed     | `robots.txt` disallows a path whose pages carry `noindex`         | remove the disallow so the directive can be read, or redirect   |
| Canonical roulette        | sitemap, canonical tags and nav point at three different versions | one posture, applied to all three signals                       |
| Canonical to a stranger   | old page canonicalized to a current page that says something else | redirect to the nearest equivalent instead                      |
| Translation erased        | `/fr/` canonicalized to `/en/`                                    | self-canonical per locale plus a full `hreflang` set            |
| One-way hreflang          | `/en/` lists `/ja/`, `/ja/` lists nobody                          | full mesh with return links, regenerated across every locale    |
| Sitemap over the cap      | one flat file for a 60,000-page reference tree                    | split into a sitemap index, 50,000 URLs and 50MB per file       |
| Title trimmed to 60       | 400 titles shortened to hit a character rule                      | fix the template's shape; there is no title length limit        |
| Blanket AI-bot block      | one `Disallow` for every assistant crawler                        | decide per agent - search, user fetch and training are separate |
| Build-stamp lastmod       | every page's `lastmod` equals the last deploy                     | derive it from the source file's commit date, or drop it        |
| Preview in the index      | PR or staging hosts serving 200 with no robots header             | `X-Robots-Tag: noindex` at the CDN, verified with `curl -I`     |
| Per-page whack-a-mole     | 400 hand-written titles instead of one template change            | fix the generator config first, pages second                    |
| Preamble snippets         | every page opens with "Acme is a platform that…"                  | answer the query in the first screen                            |
| Deprecated schema         | a HowTo/FAQPage markup project                                    | breadcrumbs and titles instead                                  |
| Reference blanket-noindex | the whole generated tree excluded to "avoid thin content"         | keep it indexable; split per resource, not per field            |
| Redirect to home          | a retired version's URLs all point at the docs index              | per-page targets; the index only as last resort                 |
| Score with no threshold   | "docs SEO health: 78/100"                                         | agreed numeric targets set before the fix pass                  |
| Estimated query data      | third-party volume numbers for technical queries                  | Search Console, or an explicit "not verified"                   |

## References

- samber/developer-platform-skills@api-reference-quality for the content quality of an API reference tree once this skill has made it indexable
