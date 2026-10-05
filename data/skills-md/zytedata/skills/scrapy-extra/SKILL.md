---
name: scrapy-extra
description: >-
  Read this BEFORE writing, modifying, debugging, or explaining any Scrapy or
  web-poet code — spiders, page objects, pipelines, settings, selectors —
  down to a one-line fix, or scaffolding/configuring a Scrapy project,
  scrapy-poet, scrapy-zyte-api, or browser rendering. These libraries moved
  on since your training cutoff; invoke this FIRST. NOT for building a
  scraper for a given site (scrape), a saved HTML file (scrape-analyze-page),
  or Scrapy Cloud deploy/jobs (zyte).
---

This file is 172 lines long; read all of them.

`SKILL_DIR` below stands for the absolute path of the directory that contains this file.

You are doing hands-on Scrapy coding: writing or changing spiders, page
objects, items, pipelines, settings, or an entire project.

For a **new** spider, prefer web-poet page objects — isolating extraction
keeps the spider focused on crawling and makes it easier to maintain, test,
and reuse. How far to go depends on the project:

- Brand-new project, or one already configured with scrapy-poet: use page
  objects unless told otherwise.
- Existing project that has spiders but no scrapy-poet: suggest adding
  scrapy-poet support (unless the user has said they don't want it) rather
  than assuming it; a plain spider that yields dicts or items is the fallback.

Never migrate an existing spider to page objects, or add web-poet to a
project that doesn't use it, unless asked.

Don't reimplement what Scrapy already does: a spider needs no seen-URL set,
since the dupefilter drops duplicate requests on its own.

There is no fixed workflow, no required inputs or outputs. Read the task, read
the relevant reference(s) below, and write idiomatic code.

## References

Bundled in `SKILL_DIR/references/` — read only the ones the task
calls for, matched by what you are about to write; most tasks need one:

- Writing or debugging a spider, item, pipeline, selector, feed export or
  setting → `scrapy.md`.
- Writing or debugging a page object, or saving and running its fixtures →
  `web-poet.md`.
- Writing a spider callback that takes a page object or an item as a parameter
  (`handle_urls`, `DummyResponse`, `SCRAPY_POET_DISCOVER`) → `scrapy-poet.md`;
  which of the two to inject is the choice that shapes the callback.
- The site blocks requests or needs JavaScript → `scrapy-zyte-api.md`.

For anything beyond these, fetch the official docs rather than guessing —
`docs.scrapy.org`, `web-poet.readthedocs.io`, `scrapy-poet.readthedocs.io`,
`scrapy-zyte-api.readthedocs.io`, `docs.zyte.com`. These are LLM-friendly:
replace `.html` with `.md` in any URL for Markdown, and see `<host>/llms.txt`
for a table of contents.

## Environment

Use `uv` for all Python execution — never bare `python` or `pip`. Install
`uv` if missing.

```bash
cd PROJECT_DIR && uv run scrapy crawl <name>
cd PROJECT_DIR && uv run --with pytest python -m pytest fixtures/
```

The `pytest` command is for projects that have a `fixtures/` directory; there
is nothing to run without one.

`.venv/`, `uv.lock`, `*.egg-info` and `build/` are expected project state, not
temporary files: leave them in place. So are the leftovers of running things —
`.pytest_cache/`, `__pycache__/`, the `items.jsonl` of a test crawl: don't go
looking for them to clean up.

## Creating a project

Only when the task needs a fresh project. Use the bundled template — it ships
`settings.py` with scrapy-poet and Zyte API addons already configured, plus
`pages/`, `spiders/`, and `fixtures/` directories:

```bash
uvx cookiecutter --no-input SKILL_DIR/assets/project-template \
    -o PARENT_DIR project_name=PROJECT_NAME
cd PARENT_DIR/PROJECT_NAME && uv sync
```

For an **existing** project, work within it. If dependencies you need are
missing from `pyproject.toml`, tell the user what's missing and ask before
adding — don't silently rewrite their project.

## Writing extraction code

Whether in a spider callback or a page object `@field`, use the following
guidelines by default, i.e. unless they contradict other known project
guidelines:

- Keep it simple and domain-general — don't overfit to the specific pages you
  looked at (no hardcoded titles, no per-page `if`/`else`).
- When you have several sample pages, check your extracted output against
  **all** of them, not just the first — a selector that only works on the page
  you happened to open is overfitting. When pages disagree, prefer the more
  general selector or fall back (e.g. JSON-LD first, then CSS).
- Return `None` for missing data, not `""` or `False`.
- Guard before attribute access; check for `None`.
- Don't catch bare `Exception` — only the specific exception you expect. The
  one exception is per-item extraction when iterating a list of items: there,
  catch `Exception` around each item so one broken item doesn't sink the rest,
  and log it with `exc_info=True` (see `web-poet.md` → Nested item extraction).
- Prefer deterministic output (avoid sets; dedup a list if needed).
- Prefer structured data when present: `extruct` for JSON-LD / microdata /
  OpenGraph, `jmespath` for JSON queries, `price_parser` for prices.
- Ask for browser rendering only when the data needs JavaScript. With page
  objects, declare that need as the page object's input — subclass
  `BrowserPage`, i.e. depend on `BrowserResponse` — rather than enabling
  `browserHtml` through automap params or `custom_settings`. Without page
  objects, request it per-request via
  `meta={"zyte_api_automap": {"browserHtml": True}}`, on the requests that
  need it only (see `scrapy-zyte-api.md`).

**Extraction extracts; it never filters.** Even if the user asks to exclude or
limit results by value, do not put that logic in a page object or extraction
method. Filtering, deduplication, and validation belong in the spider or an
item pipeline; if the project has neither yet, leave the filter out entirely
rather than moving it into the page object. Say so in your summary if the
request implied otherwise.

## Testing

- Page objects: verify by running `to_item()` and comparing to the expected
  values — not by testing selectors in isolation, since `@field` methods,
  `Returns`, and output processing transform the raw selector value into the
  final field. Do it as a web-poet fixture checked by pytest: it exercises the
  real page object, works the same for `HttpResponse` and `BrowserResponse`
  pages, and leaves a regression test behind. Build the fixture from whatever
  input you have:
  - Live URL → `uv run scrapy savefixture <page.object.ClassPath> '<url>'`.
  - Only saved sample HTML (no URL) → build the input from each file and save a
    fixture with `web_poet.testing.Fixture.save` (see `web-poet.md` → Testing
    for the snippet — it also covers `BrowserResponse`).

  Set each `output.json` to the hand-verified expected values (correct the
  recording from `savefixture`, or pass them as `item=` to `Fixture.save`), then
  `uv run --with pytest python -m pytest fixtures/` — it re-runs `to_item()` on **every**
  saved page and fails if a field drifts. See `web-poet.md` → Testing for the
  full loop.
- Spiders: run a bounded test crawl and **inspect the items**, don't trust a
  clean exit code. Always bound it with `CLOSESPIDER_ITEMCOUNT` or
  `CLOSESPIDER_PAGECOUNT`; a handful of items is enough to tell whether the
  extraction works, and a full crawl of the site is never part of validating a
  spider:

  ```bash
  cd PROJECT_DIR && uv run scrapy crawl <name> -s CLOSESPIDER_ITEMCOUNT=5 -o items.jsonl
  ```

  Read `items.jsonl`. If a field is consistently `null` or values look wrong,
  the selector is the usual culprit. If the raw HTML turns out to be a
  JavaScript shell, switch to browser rendered input (`BrowserPage`) and
  re-save its fixtures — the saved inputs match whatever the page object
  depended on when they were recorded. Fix the root cause if it's in scope,
  even when it lives in a page object rather than the spider you were asked to
  write. After any fix, re-run the crawl and read `items.jsonl` **again** to
  confirm the field is now populated — a clean exit or the closing stats block
  is not evidence the fix worked, and never report field values you have not
  seen in the current run's output.

  Never present the spider as complete while a field is systematically `null`
  without accounting for it: either fix it, or say in your final answer why not
  — the fix is out of scope, or the data genuinely isn't on those pages. Name
  the affected field either way.
