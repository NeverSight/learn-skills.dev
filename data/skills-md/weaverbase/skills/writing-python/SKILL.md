---
name: writing-python
description: Use when writing, changing, or reviewing Python code that involves type hints (Optional, Union), merging dictionaries, reading, rendering, or generating PDFs, FastAPI endpoints or Depends dependencies, async database access, Uvicorn or application logging setup, print() debugging, choosing pytest or unittest, or deciding whether to introduce typing.Protocol for an internal contract, adapter, plugin boundary, or test seam.
---

# Writing Python

## Overview

Modern Python conventions for new or requested changes: current syntax, async-safe FastAPI patterns, a shared logging configuration, `pytest`, and explicit nominal contracts instead of `Protocol`.

**Core principle:** Working code is not the same as current convention. Follow the rules below unless a concrete tool or platform constraint requires otherwise. Familiarity and old examples are not constraints.

These rules apply to new or requested changes. Do not migrate existing working code unless asked.

## Quick Reference

| Area | Do | Do not |
| --- | --- | --- |
| Type hints | Use `X \| None` and `A \| B` (Python 3.10+) | Use `typing.Optional` or `typing.Union` |
| Dict merging | `merged = defaults \| overrides` | `{**defaults, **overrides}`, or `defaults.update(overrides)` to build a merged value |
| Reading or rendering PDFs | Prefer `pypdfium2` | `pdf2image` or PyMuPDF (`fitz`), because of their licenses |
| Writing PDFs | A license-compatible PDF generation library, or pre-rendered HTML printed by a headless browser | PyMuPDF (`fitz`) |
| FastAPI dependencies | `Annotated[T, Depends(fn)]` | `Depends()` as a parameter default |
| Async apps | Async database drivers and async ORM sessions | Synchronous drivers or blocking calls inside async handlers |
| Logging | Standard `logging` with `logging.getLogger(__name__)`; copy the bundled log config into the app | `print()` for application logging, a freshly invented log format, or a runtime path into this skill |
| Internal contracts | Concrete typed classes, framework contracts, `abc.ABC`, standard inheritance, or callable aliases | `typing.Protocol` for internal contracts, adapters, plugin boundaries, or test seams |
| Tests | `pytest` for new Python projects | `unittest` for new projects, unless maintaining an existing `unittest` suite or a project constraint requires it |

## Type Hints

Use Python 3.10+ union syntax with `|`. Avoid `typing.Union` and `typing.Optional`.

Good:

```python
def process(value: str | None) -> dict[str, int | float]:
    ...
```

Bad:

```python
from typing import Dict, Optional, Union


def process(value: Optional[str]) -> Dict[str, Union[int, float]]:
    ...
```

## Dictionary Merging

Use the dict merge operator. Avoid unpacking merges and mutation when creating a merged value.

Good:

```python
merged = defaults | overrides
```

Bad:

```python
merged = {**defaults, **overrides}
defaults.update(overrides)
```

## PDF Libraries

**Reading PDFs and rendering pages to images:** prefer `pypdfium2`. Avoid `pdf2image` and PyMuPDF (`fitz`) because of their licenses: PyMuPDF is AGPL-licensed (or commercial), and `pdf2image` depends on GPL-licensed Poppler. Either can impose obligations on a project that does not otherwise accept them.

Good:

```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("input.pdf")
page = pdf[0]
text = page.get_textpage().get_text_range()
image = page.render(scale=2).to_pil()
```

Bad:

```python
from pdf2image import convert_from_path
import fitz
```

**Writing or generating PDFs:** `pypdfium2` may not be enough. Use another PDF generation library, or render pre-built HTML to PDF with a headless browser. Before adding a library, check that its license fits the project, and still avoid PyMuPDF.

```python
from playwright.async_api import async_playwright


async def html_to_pdf(html: str) -> bytes:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        try:
            page = await browser.new_page()
            await page.set_content(html, wait_until="networkidle")
            return await page.pdf(format="A4", print_background=True)
        finally:
            await browser.close()
```

Escape untrusted values when building the HTML, and do not let rendered content load arbitrary external resources.

## Testing

Use `pytest` for Python tests. Avoid `unittest` for new Python projects unless you are maintaining an existing `unittest` suite or a project constraint requires it.

## Logging Basics

- Use the standard `logging` module with appropriate log levels. Do not use `print()` for application logging.
- Apply the bundled default as app-local startup configuration, never as a runtime dependency on skill files. Read the logging reference for its Uvicorn dependency, standard-library variant, and access-log sanitization requirements.

Details and examples: [references/logging.md](references/logging.md).

## References

Read every applicable reference before writing, reviewing, or advising on a topic. If unsure whether a reference applies, read it.

| Situation | Reference |
| --- | --- |
| FastAPI `Depends`, async database drivers, Uvicorn startup and log config | [references/fastapi.md](references/fastapi.md) |
| Application logging defaults, the bundled log config template, app-local config files, `print()` | [references/logging.md](references/logging.md) |
| `Protocol`, internal contracts, interfaces, adapters, plugin boundaries, test seams, structural typing | [references/avoiding-protocol.md](references/avoiding-protocol.md) |

For a FastAPI app, read both `references/fastapi.md` and `references/logging.md`.

## Red Flags

Stop and re-read the rule if you think or see:

- "Use `typing.Optional` because the old style is familiar."
- "Merge with `{**a, **b}` or `update()`, it is what everyone writes."
- "Use `pdf2image` or PyMuPDF (`fitz`) to read or render PDFs because they are familiar."
- "`pypdfium2` cannot write this PDF, so any library will do." Check the license first.
- "Put `Depends(...)` as the default value, it is shorter."
- "Use a synchronous database driver inside an async API or worker."
- "Use `print()` for application logging."
- "Create a new Python logging format instead of copying and applying the bundled `log-config.json`, even though no other preference was specified."
- "Point app code, Dockerfiles, or Uvicorn startup commands at the skill file path instead of an app-local copied config."
- "Start a FastAPI app without passing the app-local copied logging config to Uvicorn, then fix logging after startup."
- "Use `Protocol` for this internal contract because it feels flexible."
- "A protocol is enough to show who implements this contract."
- "Start a new Python test suite with `unittest` by default."
- "Legacy reason" meaning personal familiarity or old examples rather than a concrete tool or platform constraint.

## Rationalizations to Reject

| Rationalization | Response |
| --- | --- |
| "The legacy syntax still works, so it is fine." | Working code is not the same as current convention. Use the modern Python syntax unless a real constraint requires otherwise. |
| "The PDF library does not matter as long as it renders pages." | Licenses matter. Prefer `pypdfium2` for reading and rendering; avoid AGPL PyMuPDF (`fitz`) and Poppler-based `pdf2image`. |
| "This async endpoint only does one blocking call." | Blocking calls in async paths are still event-loop hazards. Use async drivers and async ORM/database APIs. |
| "I will set up Python logging later after the app starts." | Copy and apply the bundled `log-config.json` into the app repository unless another preference is specified. FastAPI apps pass that app-local config to Uvicorn so startup logs use the configured format. |
| "I'll define this internal contract as a `Protocol` so implementations stay flexible." | Prefer concrete typed external classes, framework contracts/registration, `abc.ABC`, or standard inheritance when readers need to find implementers. Use `Protocol` only when a concrete alternative is insufficient and the structural boundary is intentionally small. |

## Common Mistakes

- Keeping outdated Python style because it still runs, instead of using the current convention.
- Reaching for `pdf2image` or PyMuPDF (`fitz`) to read or render PDFs instead of `pypdfium2`.
- Forcing PDF generation through `pypdfium2` when a license-compatible generation library or a headless browser fits better, or adding a generation library without checking its license.
- Using synchronous database operations in async request handlers or workers.
- Using `print()` logging in application code.
- Skipping the bundled `log-config.json` template for a Python app when the user or project has not specified another logging preference.
- Referencing the bundled `log-config.json` from app runtime code, Dockerfiles, or deployment commands instead of copying it into the app repository first.
- Letting FastAPI/Uvicorn start before applying the app-local copied logging config.
- Using `Protocol` for internal contracts where parent/child inheritance would make implementers easier to discover, or for test seams just because mocks and fakes feel easier.
- Starting a new Python project's tests with `unittest` instead of `pytest`.
