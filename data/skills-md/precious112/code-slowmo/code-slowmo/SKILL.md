---
name: code-slowmo
description: Explains code with an interactive visual page instead of a wall of text. It builds one HTML file with a clickable map of the system, a step-by-step timeline of what each part tells the others, and a line-by-line run of the real code that shows changing values, a log and a mock of the screen. Everything is written in short, plain sentences. Use this whenever someone wants to understand how code works, such as "how does X work", "walk me through this flow", "explain this codebase", "what happens when I click Y", "help me understand the architecture" or "I'm new to this repo". Use it even if they never ask for a picture. Do not use it for writing, fixing or reviewing code.
license: MIT
compatibility: Needs Python 3.8 or newer to build pages. The finished page is a single HTML file that opens in any browser.
metadata:
  author: precious112
  version: "0.1.0"
  opencode/slash: "true"
---

# code-slowmo

Code is easier to understand when you can watch it run slowly. This skill turns a question about code into one interactive HTML page. The page works at up to three zoom levels, written for someone who has never opened the code:

1. **System map:** the main parts and which parts talk to each other. You click into an area to see its parts.
2. **Timeline:** one action from start to end. Each arrow is one part telling another part something. A small mock of the screen and the data change with every step.
3. **Line by line:** the real code runs one line at a time. Beside it you see the running functions, the values (yellow when they change), a log and the screen.

You write the content as a JSON data file. `scripts/build.py` checks the data and the writing, then turns it into the page. You never hand-write the page's HTML or JavaScript.

## Plain writing comes first

Readers come to this skill because a long technical explanation lost them. If the page reads like jargon, it has failed, however good the pictures are. **Read [references/writing.md](references/writing.md) before you write any text for a page, every time.** The short version:

- Put the point first. One idea per sentence, about 15 to 20 words. Keep each step under 40 words.
- Use everyday words and active voice: "Puck saves the block", not "the block is persisted".
- Name things the way the reader sees them, like "the drop line", not `LinePlaceholder`. Show the code name once, as a secondary label.
- Explain every code name and technical word where it first appears. Each `<code>` term in the text needs a plain explanation in `terms`, which readers see when they hover the term.
- Don't invent shorthand labels. Say what happens concretely: who does what, and when.

The build stops on writing errors, such as overlong steps, unexplained code names or filler words. Treat warnings as errors unless you have a real reason not to.

## Workflow

### 1. Pin down the question
One page answers one question, for example "What happens between dropping a block and seeing it on the page?". If the request is broad ("explain this repo"), start with a map page and offer the deeper pages afterwards. Ask the user only when two very different questions are equally likely.

### 2. Read the real code before you write anything
Everything on the page must be true of this codebase at this version.
- Find the parts, who calls whom, and the order things happen in. Note `file:line` for each claim.
- For a line-by-line run, copy the code exactly from the file, with its real starting line number. Follow the actual path the code takes, with realistic values.
- Note the version, commit or date, so the page can say what it describes (`subject`).
- If you can't confirm something, leave it out or say plainly that you're unsure. Tag any made-up value, such as a generated id, with `<span class="example">example</span>`.

For a large codebase, use search tools or sub-agents to map it. The page itself shows only the 5 to 12 parts the question needs.

### 3. Choose the zoom levels
| The reader asks… | Use |
|---|---|
| What are the parts, and how do they connect? | `map` (with a `tour` that follows one action) |
| What happens, in what order, when I do X? | `flow` |
| What exactly does this function do? | `trace` |
| What's the difference between two approaches? | `compare` |
| What do these words mean? | `glossary` (put it first if the page uses 3 or more new terms) |
| Something no section type covers, like a figure you can drag | `custom` |

A strong page usually goes glossary → map → flow → trace, zooming in on one action. Shorter is fine: a trace alone can answer "what does this function do?". See [references/choosing-pictures.md](references/choosing-pictures.md) for more on choosing and on planning a series of pages.

### 4. Choose plain names and colors
- Give each part a plain name the reader can picture ("Drag store", "Page data store"). Use the same name everywhere on the page.
- Pick up to 5 **roles**: groups like "You", "the library", "our code", "the data", "the screen". Every part, lane, link, function and log line uses one role's color, and the colors mean the same thing in every section. Yellow is reserved for "just changed". Don't color anything else.

### 5. Write the page data
Write `<slug>.json` following [references/page-format.md](references/page-format.md). [assets/examples/puck-drop.json](assets/examples/puck-drop.json) is a complete working example; copy its shape. Rules that matter most:
- `question`, `takeaway` and one plain `say` per step are required.
- A trace needs at least one guess-first question (`ask`) at a key moment, such as just before the surprising line.
- Give each step `screen` (a small HTML mock of what the user would see) and `state` (the data that matters) whenever they help. The page carries both forward to later steps and turns changed values yellow on its own.
- Keep `vars` to the values a reader needs. Show values the way a person would read them, like `[Hero-1, Text-2]`.
- For pages with many steps, write a short script that generates the JSON, with helper functions for repeated screen mocks. Copy code into `files` straight from the source files so it stays exact. Keep the script outside the output folder.

### 6. Build, then fix what the checker reports
```bash
python3 <skill-dir>/scripts/build.py <slug>.json <slug>.html
```
Fix every ERROR. Read every WARN and fix it unless you have a clear reason not to. To check the writing alone, run `scripts/check_text.py <slug>.json`.

### 7. Re-read the page as a newcomer
Open the page if you can, or reread the JSON. For each step, check:
- Could someone who has never seen this code follow it?
- Does every sentence say who does what, and when?
- Is every value on screen what the real code would hold at that step?

Then check that the steps tell one continuous story, with no jumps.

### 8. Hand it over
- Save the page in an `explainers/` folder at the project root, unless the user names another place. Keep the JSON next to the HTML so the page can be edited and rebuilt. Open the page in the browser if you can (`open` on macOS, `xdg-open` on Linux, `start` on Windows).
- Tell the user where the page is. Give two or three plain sentences on what it shows, and name the deeper or wider page you could build next.
- Don't repeat the whole explanation in chat. The page is the explanation.

## Files in this skill
- [references/writing.md](references/writing.md): the writing rules, with before/after examples. Read it every time.
- [references/page-format.md](references/page-format.md): every field of the page data, and the HTML allowed inside text and screens.
- [references/choosing-pictures.md](references/choosing-pictures.md): which section to use, how to plan a series, and how to build a `custom` figure.
- [references/design-principles.md](references/design-principles.md): why the pages look and behave as they do (pace control, guess-first questions, fixed layouts). Read it before changing the template or writing a `custom` section.
- `scripts/build.py`: validates the page data and builds the HTML.
- `scripts/check_text.py`: the plain-writing checker that the build runs.
- `assets/template.html`: the page engine. Don't edit it per page.
- `assets/examples/puck-drop.json`: a full example covering how a drag-and-drop editor commits a drop.
