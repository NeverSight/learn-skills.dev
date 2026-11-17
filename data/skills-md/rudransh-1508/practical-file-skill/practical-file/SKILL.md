---
name: practical-file
description: Writes a college lab practical file (lab record) as a formatted .docx from the user's list of experiments, in any subject, on macOS. Theory and case-study experiments are answered in prose and tables; programming experiments get the program text, flowcharts and real Terminal screenshots of their output. Use when asked to make a practical file, lab file or lab record.
---

# Practical file

Produces `<Subject> Practical File.docx` by writing `content.md` in this skill's Markdown syntax and building it with `build.py`. `build.py` and `template.docx` carry every formatting value, measured from a reference Software Requirements Engineering (SRE) lab file. Every subject uses this format unless the user gives a reference file for that subject, which then decides what goes in the file (front pages, section names and order, captions). Write content in Markdown and leave the formatting to the builder.

`<skill>` below is this skill's folder, the one holding this SKILL.md. It runs on macOS only: the screenshots drive Terminal through AppleScript and the page check exports through Pages. One-time setup: `brew install graphviz librsvg uv`, and Screen Recording permission for the app running the agent.

## Steps

1. **Experiment list.** The user's list and order are authoritative: number the experiments exactly as the user does, and do exactly the experiments they ask for. Classify each one as **written** (theory, case study, hardware procedure, a design artefact) or **code** (it asks for a program). Look for code the user already has for these experiments (a lab folder in their home directory) and use it unchanged. For a Software Requirements Engineering (SRE) lab, also read [sre/SRE.md](sre/SRE.md), which adds a shared case study and a blueprint per experiment. Done when every experiment has its number, title, kind and section list (see Layouts).
2. **Programs** (code experiments only). Follow Code experiments below. Done when every program compiles without warnings and runs, its output answers the aim, and every Output screenshot shows the prompt with user name and path, the command, any typed input in its right place, and the full output.
3. **Figures.** Draw every flowchart and diagram as a PNG in a `diagrams/` folder next to `content.md` (see Diagrams). Done when every image the content uses exists, and you have looked at each one and found no overlapping shapes, no labels on lines, no clipped edges, and printed text of at least 7 pt.
4. **Content.** Write `content.md` one experiment at a time (for a long file, as `parts/*.md` joined in order), in its layout and the voice below. Answer each question as stated: cover every part it asks for, and nothing it does not. Every number in a Conclusion comes from the real output. Done when every experiment has exactly its `##` headings in order.
5. **Build.** `uv run --with python-docx python <skill>/build.py content.md "<Subject> Practical File.docx"`
6. **Check every page.** Export a PDF through Pages (`osascript`: `tell application "Pages"` to `open` the .docx, `export` it `as PDF`, then `close` it `saving no`). Render the pages with `uv run --with pymupdf --with pillow` and look at all of them, a contact sheet of 8 to 12 pages at a time. Done when no page is blank, no heading or single line is stranded at a page end, no table cell breaks a word, all figure and screenshot text is readable, no code line wraps, and `grep -c $'\xe2\x80\x94' content.md` (the em dash) prints 0. Then open the .docx (`open "<file>.docx"`) so the user can review it.

## Layouts

Each experiment is `# Experiment <n>` (or the reference's wording, such as `# Experiment No. <n>`) followed by its `##` headings. When the user names the sections for this file, use exactly those names in that order. Otherwise:

- **Written**: Aim, Theory, Experiment, Conclusion.
- **Code**: Aim, Theory, Code, Output, Conclusion.

Variants of the user's list (for example Aim, Theory, Algorithm and Flowchart, Code, Output, Conclusion, Learning):

- Several programs: number the pairs, `## Code 1: <Program>`, `## Output 1`, `## Code 2: ...`, and give each program its own `###` sub-section inside shared sections such as the algorithm.
- Client and server: one Code section with `### Server (file.cpp)` and `### Client (file.cpp)`, and one Output section with a `### Server` and a `### Client` screenshot.
- A written experiment in a code file (a hardware or simulator procedure) keeps the user's sections minus Code and Output; the procedure goes in the algorithm section.

Captions follow the reference: the SRE reference numbers its figures ("Figure 7.1: ..."), and a reference without captions gets `![](file.png)`. Add no other headings, lines or elements (dates, signatures) that the reference lacks.

## Front pages

Reproduce whatever the reference has before Experiment 1 (cover, vision and mission, PEOs, POs, COs, index), with the user's name, roll number and teacher. Take a logo from the reference PDF with pymupdf (`page.get_images` / `extract_image`). Build them with the `>>` centred lines, `\newpage`, `{width=...}` images and `{table ...}` options in the `build.py` docstring; leave the index's date, page and remark columns empty, and size its rows so it fits on one page.

## Code experiments

- Save programs in the lab folder (the user's own, if they have one, so the path in the screenshots is theirs), named `exp<n>.cpp`, `exp<n>_server.cpp` and so on. Write plain, student-style code with short comments, standard library and POSIX only.
- **Code**: `@@code ../exp3.cpp@@` in the content pastes the file exactly as it ran. Measure every line in 12 pt Times New Roman (PIL `ImageFont.truetype(".../Times New Roman.ttf", 12).getlength`): lines over 468 pt (6.5") wrap, so split them in the source and run the program again.
- **Output**: a screenshot of a real Terminal run, taken with `<skill>/terminal_shot.py` (usage in its docstring). One program: `terminal_shot.py run --cwd <lab> --out shots/exp3.png --input 5 -- 'g++ exp3.cpp -o exp3 && ./exp3'`. Client and server: `open` two windows, `type` the server command, then the client command and each input (typing into the server window for a chat), `wait`, and `shot` both. A rerun of a program inside the same window is just another typed line (`--input ./exp4`). Compile and run in one command so both show.
- Look at every screenshot before embedding it: inputs must appear after their prompts, and the output must be complete.

Known traps:

- Screen Recording permission is needed for the app that runs the helper; without it the capture is only the desktop wallpaper. Ask the user to grant it in System Settings > Privacy & Security > Screen Recording.
- The agent's own shell sandbox may block sockets; run networked programs only through the Terminal helper.
- With `using namespace std;`, `bind(...)` calls `std::bind` and silently does nothing (the server then listens on a random port). Write `::bind` and check its result.
- Ports below 1024 need root, and macOS already uses UDP 5353 (mDNS); use ports such as 8053 or 1161 and say so in the theory.
- A simulator experiment can use real tools when Homebrew has them (`brew install ns-3`, then compile against `/opt/homebrew/lib`); plot its trace files as an extra Output figure.

## Markdown syntax

Read the docstring at the top of `build.py`. Put each list item on one line. Leave a blank line between blocks.

## Format (measured from the reference)

Everything is Times New Roman. The page is A4 (11910 x 16840 twips) with margins top 1360, bottom 280, left 992 and right 992 twips (0.94", 0.19", 0.69", 0.69"). Nothing appears in the header or footer.

| Element | Markdown | Size | Weight | Alignment | Spacing |
|---|---|---|---|---|---|
| Experiment title "Experiment 1" | `# ` | 16 pt | bold | centred | before 3.05 pt; starts a new page unless one just started (page-break-before, so a full page never leaves a blank one) |
| Section heading: Aim, Theory, Code, Output, ... | `## ` | 14 pt | bold | left, indented 7 pt | before 10.95 pt |
| Sub-heading or table caption "Table 8.1: ..." | `### ` | 12 pt | bold | justified | before 6 pt, after 4 pt |
| Body paragraph | plain text | 12 pt | regular | justified | after 6 pt, line 1.15 |
| Bullet item (•, left 0.5", hanging 0.25") | `- ` | 12 pt | regular, with "**Term:** text" allowed | justified | after 3 pt, line 1.15 |
| Numbered step (1., left 0.5", hanging 0.25") | `1. ` | 12 pt | regular | justified | after 4 pt, line 1.15 |
| Code line | fenced block or `@@code` | 12 pt | regular | left; indentation kept as spaces | single line spacing, none between lines, 6 pt after the block |
| Inline code or data (`01111110`) | `` `x` `` | Courier New 11 pt | regular | - | - |
| Figure or screenshot | `![caption](img.png)` | natural size from the file's DPI, at most 6.5" x 9" | - | centred | before 6 pt |
| Figure caption "Figure 7.1: ..." (the image alt text) | - | 12 pt | italic | centred | before 3 pt, after 10 pt |
| Table | `\| a \| b \|` | 12 pt | header row bold | left | total width 9026 twips; outer borders 0.5 pt auto, cell borders 0.5 pt grey 808080; cell padding 3 pt top and bottom, 4.5 pt left and right; text vertically centred; line 1.05; rows never split across pages; header row repeats on each page; empty 6 pt paragraph after the table |

Pagination is handled by the builder: headings, sub-headings (except before a table), images and bold label paragraphs stay with what follows, lists stay on one page, and paragraphs have widow control.

Column widths are set automatically: every column first gets room for its longest word, and the rest of the width is shared by text length. When a table with many columns is still too tight, shorten the wording in the cells (for example "DB Admin" instead of "Database Administrator") rather than accepting broken words.

All headings use title case, as in Experiments 7 to 13 of the SRE reference. Experiments 1 to 6 of that reference use upper case ("EXPERIMENT – 1", "AIM"), which came from a PDF conversion and is deliberately not copied.

## Voice

- Formal, impersonal academic English with British spelling (organise, prioritise, behaviour). Plain hyphen "-" in place of the em dash.
- **Aim**: one sentence beginning "To ...", restating the question and naming the system or problem in full.
- **Theory**: two to four paragraphs on the general concept, independent of the specific system or program. Add a bullet list of "**Term:** explanation" items where the concept has parts, and a small example with real values (`1101011011` with generator `10011` gives CRC `1110`). For a code experiment, explain the concept the program demonstrates and the choices the program makes (ports, message formats).
- **Experiment** (written): open with "The experiment was carried out according to the following action plan:", followed by five to eight numbered steps. Then give the artefacts in order, each under a `###` caption, with tables numbered `Table <exp>.<n>` and figures numbered `Figure <exp>.<n>`. Tables hold the substance: concrete, topic-specific rows, never placeholders. Refer to them in the steps ("(Table 8.1)").
- **Algorithm**: five to eight numbered steps that match the program, followed by its flowchart.
- **Conclusion**: one paragraph in the past tense that quantifies the result from the real output ("returned 120 as the factorial of 5, which was verified by hand") and states the lesson.
- **Learning** (when asked for): four bullets beginning "Learned ..." or "Implemented ...".

## Diagrams

- **Flowcharts**: copy [flowchart.py](flowchart.py) into `diagrams/`, write one chart per program, and render; its docstring has the chart format, the client-server two-column form and the rules for keeping charts readable.
- **Other diagrams**: draw them as SVG from fixed positions and convert with `rsvg-convert`; automatic layout tangles anything with more than a few crossing links. [sre/SRE.md](sre/SRE.md) has worked generators for use case, ER and DFD diagrams.
- Use Times font, a white background, black lines, and pale fills (`#E8EEF8`, `#FFF4D6`, `#E6F4E6`, `#F3E8F8`). Store the real DPI in every PNG (`sips -s dpiWidth 220 -s dpiHeight 220 file.png`) so the builder prints it at its natural size.
- Check the printed text size: font size x min(1, 6.5 / width in inches, 9 / height in inches) should be at least 7 pt. When it is smaller, shorten box text or simplify the layout; don't shrink the text.
