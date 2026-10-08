---
name: help-center-markdown
description: >
  Build a markdown-backed help center in a Next.js App Router app: category
  folders of frontmatter articles, statically rendered landing, category, tag
  and article pages, client-side search with ranking and keyboard navigation,
  locale-aware routing with default-locale fallback, tags with slug identity
  and per-tag pages, related articles, breadcrumbs, JSON-LD and sitemap
  entries, plus a content validator for CI. Use when: (1) building or
  extending a help center, knowledge base, docs section, support articles or
  FAQ hub from markdown files in the repo, (2) adding article search, tag pages
  or tag chips, translated articles with fallback, hreflang/canonical rules,
  related links, or a collapsible article sidebar, (3) the user mentions: help
  center, knowledge base, docs site, support articles, markdown content,
  frontmatter, gray-matter, content/help, validate:help, tags, article search,
  hreflang, i18n content, "help articles". Carries a loader with a CI validator
  that fails the build on unreachable or malformed articles, search that
  tolerates trailing spaces, punctuation and diacritics, and tags grouped by
  slug so every spelling variant reaches one page. Next.js App Router; the
  content source is a seam behind one getHelpIndex(locale), so a CMS can
  replace the filesystem. Not a blog skill, not a CMS integration and not docs
  generated from code.
---

# Help Center: markdown articles, search, i18n

A help center is a small static site with one hard requirement: **every
article must be reachable**, from the sidebar, from search, and from a
translated locale that does not have it yet. Written by the engineer who has
shipped this module, which holds that requirement as verified properties: the
sidebar shows every article, search ranks a query however it is typed, related
links resolve or the validator fails the build. The loader, search and tag
suites cover each; the record is in `references/provenance.md`.

## When to use

Building or extending a help center, docs section or knowledge base whose
articles are markdown files in the repository, on Next.js App Router, with or
without multiple locales.

## When NOT to use

- **A blog**: dated, authored posts are another content model.
- **Docs generated from code** (OpenAPI, TypeDoc): use their generators.
- **A CMS-backed help site** publishing at runtime: the index contract holds,
  the loader changes; see the CMS note in [extensions.md](references/extensions.md).
- **Marketing pages that happen to be markdown**: reuse the host's renderer.

## Architecture

```
content/help/<[locale]/><category>/<slug>.md
        |  gray-matter + normalisation
        v
getHelpIndex(locale)      React cache(): one parse per request
  categories, articles (sorted), byKey, tags, byTag, skipped
        |
        +-- pages: landing / category / tag / article: metadata, JSON-LD, canonical/hreflang
        +-- HelpShell: toSummary for the nav tree (sidebar + drawer)
        |              toSearchDoc for HelpSearch (client, tokenised prefix search)
        +-- helpSitemapEntries()
        +-- validate:help (CI): unresolved related, order ties, bad dates, bad slugs, tag drift
```

Everything reads from the index. Nothing else touches the filesystem.

## Critical facts

1. **The filesystem is the schema.** Folder = category, filename = slug;
   frontmatter `slug`/`category` are validated against the path, never used.
2. **Only summaries cross to the client.** `toSummary`/`toSearchDoc` strip the
   body; a `HelpArticle` in a client component ships the corpus in every page.
3. **An untranslated page is a duplicate.** It renders from the default
   locale, keeps its place in navigation, shows a notice, canonicalises to the
   default-locale URL, and is absent from hreflang and the sitemap.
4. **The runtime forgives; CI does not.** Bad references are dropped, missing
   orders sort last, and `validate:help` fails the build for the author.
5. **Search is client-side by design.** ~1 KB per article, already in the page
   for navigation, results on the first keystroke. Body search is an extension.
6. **The templates are copied, not rewritten.** Only the seam values in
   [adaptation.md](references/adaptation.md) change. `gray-matter`,
   `react-markdown`, `remark-gfm` and `vitest` come from npm, which is not an
   external service: an unattended run installs and lists them. The five test
   files run unmodified: 27 tests. The loader stays as shipped when Turbopack
   warns about its trace. Without Tailwind, the host's global stylesheet styles
   the layout utilities ([ui.md](references/ui.md)).

## Hard rules

The same eight, in order, as the README and [adaptation.md](references/adaptation.md).

> **Never pass an article to a client component.** Only `toSummary` and
> `toSearchDoc` shapes cross, so a page carries summaries, not the corpus.

> **Never cap a collapsible list's height.** A `max-h-*` + `overflow-hidden`
> pair clips whatever does not fit and reports nothing. Use `hidden` or a real
> collapsible primitive, so a list renders every link or none.

> **Never index an untranslated page as its own.** It canonicalises to the
> default-locale URL and stays out of hreflang and the sitemap.

> **Never ship without `validate:help` in CI.** The runtime drops a bad
> `related` reference invisibly; the validator is the only place an author
> learns a slug was renamed.

> **Never sort by `order` alone.** Ties fall through to `readdir` order, which
> differs between filesystems. Break ties by title, then slug.

> **Never search an untrimmed query, and never search title alone.** Trim,
> tokenise, fold diacritics, include tags and headings, rank by field.

> **Never hardcode chrome strings** in a host with an i18n system. Every
> string goes through `HelpStrings`, so the header, footer and notices switch
> locale together.

> **Never key a tag by its spelling.** Case, hyphens and plurals drift across
> authors. Group by `tagSlug` so every variant lands on one page, and let the
> validator report the drift.

## Quick start

1. Fill in the seam contract and settle the category ids:
   [adaptation.md](references/adaptation.md).
2. Choose the content layout and write the config:
   [content-model.md](references/content-model.md).
3. Copy the loader and parser, wire `"prebuild": "npm run validate:help"` and
   run it on the real content now: [content-loader.md](references/content-loader.md).
4. Wire strings and paths to the host's i18n: [i18n.md](references/i18n.md).
5. Add the three pages, SEO helpers and sitemap entries
   ([routes.md](references/routes.md)), then the tag page and linked chips
   ([tags.md](references/tags.md)).
6. Build the shell, navigation and drawer ([ui.md](references/ui.md)), the
   breadcrumb, cards, lists and renderer ([ui-content.md](references/ui-content.md)),
   then search and its hook ([search.md](references/search.md)).
7. Run the shipped tests, then check the behaviour contract: longest category
   fully reachable, trailing-space query, accented query, untranslated page's
   canonical. The final message, not only a README, hands over the category ids
   and that renaming one needs redirects, which articles are placeholders, that
   `siteUrl` must be set before deploying (a literal in `HELP_CONTENT`, never an
   environment variable), that `validate:help` runs before every build, and
   `reportHelpSearchMiss` to wire to analytics. Next: [extensions.md](references/extensions.md);
   before simplifying anything, [provenance.md](references/provenance.md).

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Fitting this into an existing app | adapt, seam, rename categories, host probe, integrate, dependencies | [adaptation.md](references/adaptation.md) |
| Frontmatter, folders, slugs, validation | frontmatter, slug, category, order, related, updatedAt, featured, validate, CI | [content-model.md](references/content-model.md) |
| Reading files into the index | loader, gray-matter, cache, fallback, headings, sort, index, fs | [content-loader.md](references/content-loader.md) |
| Search box and ranking | search, combobox, ranking, tokenize, diacritics, prefix, keyboard, no results | [search.md](references/search.md) |
| Tags, tag pages, chips, tag cloud | tag, tags, tag page, chip, tag slug, spelling, plural, browse by tag | [tags.md](references/tags.md) |
| Locales, strings, dates, canonicals | i18n, locale, translation, fallback, hreflang, strings, plural, Intl | [i18n.md](references/i18n.md) |
| Pages, metadata, JSON-LD, sitemap | route, page.tsx, generateStaticParams, dynamicParams, notFound, canonical, TechArticle, sitemap | [routes.md](references/routes.md) |
| Shell, header, sidebar, drawer | layout, sidebar, mobile menu, drawer, focus trap, collapsible, sticky, HelpShell | [ui.md](references/ui.md) |
| Breadcrumb, cards, lists, renderer, style hooks | breadcrumb, category card, article list, react-markdown, data-help, styling | [ui-content.md](references/ui-content.md) |
| Beyond the shipped module | full-text, Pagefind, TOC, feedback, git dates, MDX, CMS, redirects | [extensions.md](references/extensions.md) |
| Why the templates differ from the earlier implementation | provenance, audit, ledger, kept deliberately, fixing the earlier implementation | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
