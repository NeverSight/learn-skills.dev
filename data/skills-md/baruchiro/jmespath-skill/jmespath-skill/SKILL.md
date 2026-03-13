---
name: jmespath-skill
description: This skill should be used when the user needs to build JMESPath queries from JSON and a request, debug an existing query against JSON, or ask about JMESPath syntax (e.g. fallbacks, literals, filters).
---

# JMESPath query helper

## Overview

To support building queries from sample JSON and a natural-language request, debugging queries against JSON, and answering syntax questions, use the bundled reference and script as below.

## When to use

- User provides JSON (or a sample) and a description of what to extract → build a JMESPath expression that returns that data.
- User has an existing JMESPath expression and JSON and wants to see the result or fix wrong results → run the query and adjust.
- User asks how to express something in JMESPath (e.g. fallback string literal, filter, slice) → answer using the syntax reference.

## Building a query from JSON and a request

1. Parse the user’s JSON and their request (which field, list, or structure they want).
2. Use `references/syntax.md` for correct syntax (identifiers, subexpressions, index/slice, projections, filters, literals, fallbacks).
3. Propose a JMESPath expression. For literals use backtick JSON (e.g. `` `"active"` ``) or raw strings (e.g. `'fallback'`); for defaults use `||` (e.g. `foo || \`"n/a"\``).
4. Optionally run the expression with `scripts/run_query.py` and show the result so the user can confirm.

## Debugging an existing query

1. Run the query against the user’s JSON using `scripts/run_query.py`:
   - From file: `python scripts/run_query.py '<query>' path/to/data.json`
   - From stdin: `cat path/to/data.json | python scripts/run_query.py '<query>'`
2. Compare output to what the user expects; if it differs, use `references/syntax.md` to fix (e.g. projections, filters, literal vs raw string, precedence with `||`/`&&`).
3. Re-run until the result matches expectations.

## Answering syntax questions

1. Use `references/syntax.md` as the primary source for syntax (identifiers, subexpressions, index/slice, wildcards, flatten, literals, raw strings, fallback `||`, filters, comparators, multi-select, pipe, `@`, and function call form).
2. For “how to represent a fallback string literal”: use JSON literal `` `"text"` `` or raw string `'text'`; for “default if missing” use `field || \`"default"\``or`field || 'default'`.
3. For built-in function names and signatures, point to the [JMESPath specification](https://jmespath.org/specification.html) or load the spec only when a detailed function list is needed.

## Resources

- **references/syntax.md** — JMESPath syntax summary (literals, fallbacks, filters, projections, etc.). Read when building or debugging queries or answering syntax questions.
- **scripts/run_query.py** — Run a JMESPath query against JSON from a file or stdin. Install dependencies with `pip install -r requirements.txt`.
