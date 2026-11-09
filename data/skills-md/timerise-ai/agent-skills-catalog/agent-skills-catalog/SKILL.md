---
name: agent-skills-catalog
description: >
  Build a public catalog of Agent Skills in a Next.js App Router site, generated at build time from each skill
  repository's own files: a sync script that mirrors SKILL.md, README.md, CHANGELOG.md, provenance.md and
  evals/ into the repository, a loader that reads rules, releases and the provenance ledger from them, a
  catalog page with search and category filter, one page per category and per skill, the agent eval results
  (newest run per agent and prompt, failing runs included), JSON-LD, sitemap entries and a content validator.
  Use when: (1) a site should list the Agent Skills an organization publishes on GitHub, with install
  commands, rules, versions and agent eval results, (2) skill pages show an old version after a release, or
  an eval run never appears on the page, (3) adding agent eval results, prompts or a provenance ledger to
  existing skill pages, (4) the user mentions: skills catalog, Agent Skills page, skill directory, SKILL.md,
  skills.sh, npx skills add, evals/prompts.md, eval results, agent evals, Claude Code, Codex CLI, Gemini CLI,
  skills:sync, sync.json, raw.githubusercontent.com, provenance.md, CHANGELOG.md, Keep a Changelog,
  TechArticle, SoftwareSourceCode. Carries a sync that reads every file of a skill at one commit and swaps
  the mirror in whole, a loader that never fetches, an eval parser that rejects a malformed run with its
  reason instead of dropping it, and a validator that fails the tests on it. Next.js App Router; where the
  skills come from is a seam (GitHub or local checkouts) and the section layout it reads is one table. Not a
  way to write a skill, not an eval runner and not a package registry.
---

# Agent Skills catalog: synced skill files, pages, eval results

A skills catalog is a set of pages about files that live somewhere else, so **the page must say exactly
what the skill's repository says, at one commit, and nothing else.** Written by the engineer who has shipped
this module, which holds that as verified properties: the sync reads every file of a skill at one commit
and swaps it in whole, the build reads the disk and never the network, every eval file either renders or
fails the tests with its reason, and the eval cards show the recorded result of the newest run per agent
and prompt. The record is in `references/provenance.md`.

## When to use

Building or extending pages on a Next.js App Router site that list Agent Skills published as repositories
(each with `SKILL.md`, `README.md`, `CHANGELOG.md` and an `evals/` folder), with their rules, releases,
install commands and agent eval results.

## When NOT to use

- **Writing or hardening a skill itself**: that is the skill's own repository; to fix one from its eval
  runs, the sibling `skill-eval-loop` skill.
- **Running agent evals**: the runs are made elsewhere and committed to each skill's `evals/`; this module
  only reads them.
- **A blog or a help center from markdown in the repository**: the sibling `blog-markdown` and
  `help-center-markdown` skills. Here the markdown is someone else's and is never edited.
- **A package registry or marketplace** with accounts, uploads or downloads: different trust model.

## Architecture

```
skill repositories (GitHub, or local checkouts)
        |  npm run skills:sync   head sha first, every file at that sha, staged, swapped in whole
        v
content/skills/<slug>/meta.md          host-written: category, tagline, related
content/skills/<slug>/upstream/        sync-written only: SKILL.md README.md CHANGELOG.md
                                       references/provenance.md evals/*.md sync.json
content/skills/_index/README.md        optional index table: Builds and Backend cells
        |  build time, no network
        v
lib/skills/catalog.ts   getSkill(slug), getAllSkills(), categories, related     React cache()
  markdown.ts + upstream.ts   sections, rules, tables, releases, provenance (SKILL_LAYOUT)
  evals.ts                    prompts, parseEval (ok or reason), sortRuns, latestRuns
  validate.ts                 every problem the loader forgives, as errors and warnings
        |
        +-- /skills                 catalog: SkillSummary[] to a client search and filter
        +-- /skills/[slug]          a skill page, or a category page when the slug is a category
        +-- sitemap, JSON-LD        dates from the changelog, never from the build
        +-- catalog.test.ts         validateCatalog() errors fail npm test
```

## Critical facts

1. **Each skill has two halves.** `meta.md` holds what the repository does not (category, tagline, related)
   and only the host writes it; `upstream/` holds the repository's files and only the sync writes it.
2. **The layout is the parser's contract.** `SKILL_LAYOUT` names the headings the loader reads; a skill that
   strays loses that section and the validator says which. Nothing is guessed from prose.
3. **Upstream links are relative to their repository.** `references/x.md` does not exist on the site, so
   `SkillMarkdown` resolves every relative link against the file's folder on GitHub.
4. **One `[slug]` segment serves skills and categories.** `dynamicParams = false` keeps every page static
   (a host with `cacheComponents` removes that one line: [adaptation.md](references/adaptation.md)), and the
   validator fails on a skill slug that equals a category id.
5. **A run file is free text anyone can propose.** Only an Actions run URL in the organization's own
   repositories becomes an "Agent log" link; JSON-LD escapes `<`.
6. **Run files do not sort as text.** `-p1.md` sorts after `-p1-2.md`, so the order is date, then
   `runNumber`, then name.
7. **The build never needs GitHub.** An unattended run with no network commits the example skill from
   `assets/content/` so the pages, validator and tests have content, and hands over `npm run skills:sync`.
   `gray-matter`, `react-markdown`, `remark-gfm` and `vitest` come from npm, which is not an external
   service. The templates are copied, not rewritten: only the seam values in
   [adaptation.md](references/adaptation.md) change, and `vitest.config.mts` and the five test files run
   unmodified: 24 tests.

## Hard rules

The same eight, in order, as the README and [adaptation.md](references/adaptation.md).

> **Never fetch a skill at build or request time.** The sync writes files into the repository and the build
> reads the disk, so a deploy never depends on GitHub's rate limit or its cache.

> **Read every file of a skill at one commit.** Resolve the head sha first and fetch each file at that sha;
> a raw URL on the branch name is cached for minutes and mixes two commits.

> **Swap a skill's mirror in whole or not at all.** Stage the folder, then rename it into place, so a
> failed sync leaves the previous copy and a file deleted upstream disappears here.

> **Never drop an eval file silently.** `parseEval` returns the reason it cannot show a file, and
> `validateCatalog()` turns each one into an error that fails `npm test`.

> **Show the recorded result of the newest run per agent and prompt.** Failing runs render like passing
> ones, nothing is recomputed or picked for looking better, and an agent with no run is named.

> **Normalize YAML dates before reading frontmatter as text.** An unquoted `date: 2026-09-26` is a Date,
> and a Date read as text is an empty string that rejects the run.

> **Never retype a skill's text on the site.** Rules, releases, prompts and results come from `upstream/`;
> `meta.md` carries only what the repository does not, and the sync never touches it.

> **Only summaries cross to the client.** The catalog's search gets `SkillSummary[]`; a whole `Skill` in a
> client component ships every README to every visitor.

## Quick start

1. Fill in the seam contract, the organization and the categories: [adaptation.md](references/adaptation.md).
2. Write the config, categories and types, and lay out `content/skills/`:
   [data-model.md](references/data-model.md).
3. Copy the sync and wire `npm run skills:sync`; run it, or with no network copy `assets/content/` into the
   app: [sync.md](references/sync.md).
4. Copy the frontmatter, layout, markdown and upstream readers: [parsing.md](references/parsing.md).
5. Copy the eval parser: [evals.md](references/evals.md).
6. Copy the loader and the validator: [loader.md](references/loader.md).
7. Add the catalog and `[slug]` pages, JSON-LD and the sitemap: [routes.md](references/routes.md). The pages
   stay as shipped; an intro or a notice goes in a `layout.tsx` beside them.
8. Add the components, then style them through the `data-skill-*` hooks: [ui.md](references/ui.md).
9. Copy `vitest.config.mts` and the five test files, wire `npm test`, and run it with `npm run typecheck` and
   `npm run build`: [testing.md](references/testing.md).
10. The final message itself states each of these in full, with its file or number, even when a README
    repeats them: the organization and branch, set in both `config.ts` and the sync; that
    `npm run skills:sync` runs after every skill release and its result is committed; `GITHUB_TOKEN` for more
    than about thirty skills; that `siteUrl` must be set before deploying (a literal, never an environment
    variable); that the example skill is deleted after the first real sync; the placeholders left in place;
    every dependency added. Next:
    [extensions.md](references/extensions.md); before simplifying anything,
    [provenance.md](references/provenance.md).

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Fitting this into an existing app | adapt, seam, organization, rename, host probe, categories, dependencies | [adaptation.md](references/adaptation.md) |
| Config, categories, types, folders | config, SKILLS_CATALOG, category, meta.md, Skill, SkillSummary, content/skills | [data-model.md](references/data-model.md) |
| Pulling skills into the repository | sync, skills:sync, GitHub, raw.githubusercontent.com, sha, GITHUB_TOKEN, rate limit, sync.json, local | [sync.md](references/sync.md) |
| Reading SKILL.md, README, changelog | gray-matter, frontmatter, Date, heading, SKILL_LAYOUT, list, table, release, provenance, index table | [parsing.md](references/parsing.md) |
| Prompts and eval runs | evals, prompts.md, parseEval, result, partial, runNumber, latestRuns, runUrl, interventions | [evals.md](references/evals.md) |
| Loading the catalog and validating it | getSkill, getAllSkills, cache, related, validateCatalog, warning, error | [loader.md](references/loader.md) |
| Pages, metadata, JSON-LD, sitemap | route, page.tsx, generateStaticParams, dynamicParams, category page, TechArticle, BreadcrumbList, sitemap | [routes.md](references/routes.md) |
| Cards, search, eval cards, markdown | SkillCatalog, search, filter, EvalRuns, SkillMarkdown, relative links, urlTransform, data-skill | [ui.md](references/ui.md) |
| Tests and the content validator | vitest, npm test, catalog.test, fixture, example skill, alias | [testing.md](references/testing.md) |
| Beyond the shipped module | Markdown copy, llms.txt, price, call to action, assistant, eval collection, badges | [extensions.md](references/extensions.md) |
| Why the templates differ from the earlier implementation | provenance, audit, ledger, kept deliberately, added | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
