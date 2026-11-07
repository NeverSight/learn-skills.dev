---
name: ponytail-graphify
description: Ponytail rung-2 reuse check via the Graphify knowledge graph. Before
  writing any new component, hook, util, service, or helper, query the graph to find
  existing code that already does it. Reuse over rebuild. Invoke when the user asks
  to build, add, create, or implement anything new.
---

# ponytail-graphify

Ponytail's rung 2: **"Already in this codebase? Reuse it."**

Before writing a single line, check the knowledge graph. If something already
exists, point to it. Only proceed with new code if nothing fits.

## Prerequisites

`graphify-out/graph.json` must exist. If it doesn't:
```bash
graphify .        # or: graphify src/
```
If graphify isn't installed: `uv tool install graphifyy` then retry.

## Steps

1. **Extract the intent** from the user's request — the thing they want to build
   (e.g. "a modal", "a date formatter", "a loading skeleton", "an auth guard").

2. **Check for god nodes** — high-degree nodes touch everything and are almost
   always the right answer for their domain. Find them first:
   ```bash
   graphify query "graphify-out/graph.json" --top-nodes 5
   ```
   If the intent clearly maps to a god node, surface it immediately and stop.

3. **Query the graph:**
   ```bash
   graphify query "<intent>"
   ```
   If the query returns candidates, also run:
   ```bash
   graphify explain "<candidate name>"
   ```

4. **Decide:**

   | Result | Action |
   |--------|--------|
   | Strong match (same purpose, similar API) | **Stop. Point to it.** Show the file path and how to use it. Do not write new code. |
   | Partial match (overlaps but doesn't cover it) | **Extend it.** Show what exists, propose the minimal addition to the existing file. |
   | No match | **Proceed.** Implement the shortest thing that works (ponytail full). |

5. **Output format:**

   - **Reuse found:** `Already exists: [Name] at [path:line]. Use it like: [one-liner].`
   - **Extend:** `Closest match: [Name] at [path]. Missing: [X]. Add [minimal diff].`
   - **Nothing found:** `Graph clear. Building minimal version:` → then code.

## Rules

- Never skip the graph query to save time. That's the whole point.
- One query is enough — don't run five variations trying to find a match. If the
  first query misses, proceed with implementation.
- If the graph is stale (last built >1 week ago per GRAPH_REPORT.md date), warn
  the user and suggest `/graphify . --update` before trusting results.
- Don't reuse something just because it exists — it must actually fit the intent.
  A partial match forced into the wrong shape is worse than new code.
