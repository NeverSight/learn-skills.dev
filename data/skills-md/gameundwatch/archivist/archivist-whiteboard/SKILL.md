---
name: archivist-whiteboard
description: Build docs/archivist/whiteboard.html, one page showing the whole reference graph with every document readable on it. Use when the document set has to be read as a graph rather than file by file, or after documents were added or rewritten.
---

# archivist-whiteboard

## Input

Every `.md` under `docs/archivist/`, and `docs/archivist/index.csv` when it is
there. Nothing else.

The index is read for speed, never as a premise. **Missing index is not an error.**
Walk the documents and build the same graph from them.

## Output

`docs/archivist/whiteboard.html`, rewritten whole on every run. It sits beside the
index, outside the six layer directories: it is generated, and no layer holds it.

**Write nothing else**, except one line in `.gitignore`. Not one document is
touched, renamed or reordered. The board reads the graph; it never decides it.

The page is not tracked by git. `docs/archivist/whiteboard.html` goes into the
`.gitignore` at the project root.

## What it does

1. Collect, for every document: its path relative to `docs/archivist/`, the text of
   its first `# ` heading, the documents it links to, and its whole body.
2. Fetch the libraries and hold them as text. Pin every version:

   ```
   curl -sS -L https://cdn.jsdelivr.net/npm/marked@14.1.3/marked.min.js
   curl -sS -L https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js
   curl -sS -L https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js
   ```

   Fetching happens **here, once, at generation**. The page never fetches anything
   when it is opened. A fetch that fails leaves its marker empty, and the page is
   built without what that library did: no markdown, no diagrams, or no search.
   Nothing of ours stands in for any of them.
3. Read `TEMPLATE.html` from this skill. **Check that each marker below occurs
   exactly once before replacing anything** — a marker that moved or was renamed
   makes a replacement pass silently, and the page is then built without it.

   | Marker | Replaced with |
   | --- | --- |
   | `__TITLE__` | the project's name |
   | `__GRAPH__` | a JSON array, one object per document: `{p, t, r, x}` — path, title, refs, body |
   | `__MARKED__` | the markdown library text, or nothing |
   | `__MERMAID__` | the diagram library text, or nothing |
   | `__FUSE__` | the search library text, or nothing |

4. Write the result to `docs/archivist/whiteboard.html`.
   Then make sure `.gitignore` at the project root has the line
   `docs/archivist/whiteboard.html`. If the line is already there, change nothing.
   Otherwise append that one line, creating the file if needed. Leave every other
   line as it is.
5. Run the page's script once against a stub document object and confirm it raises
   nothing. Parsing alone does not catch a name that went missing: the board renders
   empty and the file still looks well formed.
6. Serve `docs/archivist/` in the background and say the URL. Do this on every run,
   including when `archivist` calls this skill.

   Start at port 8765. For each port, probe it first:

   ```
   curl -sf -o /dev/null http://127.0.0.1:PORT/whiteboard.html
   ```

   - **It answers**: a server is already serving the board. Use it; start nothing
   - **Connection refused**: the port is free. Start the server there, in the
     background, so the run does not wait on it:

     ```
     python3 -m http.server PORT --bind 127.0.0.1 --directory docs/archivist
     ```

   - **Something else answers**: go to the next port

   Then say `http://127.0.0.1:PORT/whiteboard.html`. **Bind to `127.0.0.1` only.**
   Never stop the server; the person does. Without `python3`, serve nothing and say
   the path of the file instead: it opens on its own.

## What the page holds

`TEMPLATE.html` is one file in fourteen labelled sections. The ones a change is
most likely to touch:

- **PINS** — the single table of colour and shape. Colour carries the layer; shape
  carries the split inside it
- **GROUPS** — which documents belong together, by greedy modularity over the
  references with the direction dropped. Computed once; every layout that needs
  groups reads the same result
- **LAYOUTS** — one function per slot, each returning `0..1` coordinates per
  document. **No simulation.** Every slot resolves a position from the graph
  directly, so the same documents always give the same board

The three slots share their axes, which is what lets a reader switch without
losing their place:

| slot | radius | angle |
| --- | --- | --- |
| gravity | rank by how often the document is referenced | its group |
| cluster | (the group's own place) — a group is a small ring view inside | its group |
| radial | the layer | its group |

## Rules

- **One page.** The output opens on its own, with no network and no neighbouring
  file. Everything it shows is inside it.
- **A layout is a slot.** One function, coordinates only; it never reads the size of
  the board. Adding one is adding a function, and touches no other layout.
- **The pin table is single.** The board, the paper, the reference inside the text
  and the legend all read that one table. A second place to state a colour is a
  defect, not a duplicate.
- **Colour carries the layer; shape carries the split inside it.** Never ask colour
  alone to separate six things.
- **Nothing survives the tab.** No position, no zoom, no open paper is written
  anywhere. What the reader arranges is theirs for as long as the page is open.

## What it does not do

- **No writing back.** A board that can edit documents makes the board the
  authority, and the reduction runs the wrong way
- **No syntax of its own.** Neither markdown, nor diagrams, nor search are
  implemented here. Keeping up with any of them is not this project's work: the
  libraries do it, or it is not done
- **No judgement.** Broken links, skipped layers and missing realizations are
  `archivist-check`'s. The board draws the graph as written

## Standing

The page is generated. Deleting it must lose nothing, so nothing may be written
anywhere that only holds while it exists.
