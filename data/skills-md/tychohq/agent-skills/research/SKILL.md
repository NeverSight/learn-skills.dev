---
name: research
slug: research-agent
version: 1.0.0
description: Conduct open-ended research on a topic, building a living markdown document. Supports interactive and deep research modes.
---

# Research Skill

## Description
Conduct open-ended research on a topic, building a living markdown document. The conversation is ephemeral; the document is what matters.

## Trigger
Activate when the user wants to:
- Research a topic, idea, or question
- Explore something before committing to building it
- Investigate options, patterns, or approaches
- Create a "research doc" or "investigation"
- Run deep async research on a complex topic

## Research Directory
Each research topic gets its own folder:
```
~/.openclaw/workspace/research/<topic-slug>/
├── prompt.md          # Original research question/prompt
├── research.md        # Main findings (Parallel output or interactive notes)
├── research.pdf       # PDF export (when generated)
└── ...                # Any other related files (data, images, etc.)
```

---

## Two Research Modes

### 1. Interactive Research (default)
For topics you explore together in conversation. You search, synthesize, and update the doc in real-time.

### 2. Deep Research (async)
For complex topics that need comprehensive investigation. Uses the Parallel AI API via `parallel-research` CLI. Takes minutes to hours, returns detailed markdown reports.

**When to use deep research:**
- Market analysis, competitive landscape
- Technical deep-dives requiring extensive source gathering
- Multi-faceted questions that benefit from parallel exploration
- When user says "deep research" or wants comprehensive coverage

---

## Interactive Research Workflow

### 1. Initialize Research

1. **Create the research folder** at `~/.openclaw/workspace/research/<topic-slug>/`

2. **Create prompt.md** with the original question:
   ```markdown
   # <Topic Title>

   > <The core question or curiosity>

   **Started:** <date>
   ```

3. **Create research.md** with the working structure:
   ```markdown
   # <Topic Title>

   **Status:** Active Research
   **Started:** <date>
   **Last Updated:** <date>

   ---

   ## Open Questions
   - <initial questions to explore>

   ## Findings
   <!-- Populated as we research -->

   ## Options / Approaches
   <!-- If comparing solutions -->

   ## Resources
   <!-- Links, references, sources -->

   ## Next Steps
   <!-- What to explore next, or "graduate to project" -->
   ```

4. **Confirm with user** - Show the folder was created and ask what to explore first.

### 2. Research Loop

For each exchange:

1. **Do the research** - Web search, fetch docs, explore code
2. **Update the document** - Add findings, move answered questions, add sources
3. **Show progress** - Note what was added (don't repeat everything)
4. **Prompt next direction** - End with a question or suggestion

**Key behaviors:**
- Update existing sections over creating new ones
- Use bullet points for findings; prose for summaries
- Note uncertainty ("seems like", "according to X", "unverified")
- Link to sources whenever possible

### 3. Synthesis Checkpoints

Every 5-10 exchanges, offer to:
- Write a "Current Understanding" summary
- Prune redundant findings
- Reorganize if unwieldy
- Check blind spots

### 4. Completion

When research is complete, update the status in `research.md`:

- **"Status: Complete"** — Done, stays in place as reference
- **"Status: Ongoing"** — Living doc, will be updated over time

**If the research is specifically for building a project:**
- Graduate to `~/specs/<project-name>.md` as a project spec
- Or create a project directly based on findings
- Update status to **"Status: Graduated → ~/specs/..."**

Most research is just research — it doesn't need to become a spec. Only graduate if you're actually building something from it.

---

## Deep Research Workflow

### 1. Start Deep Research

```bash
parallel-research create "Your research question" --processor ultra --wait
```

**Processor options:**
- `lite`, `base`, `core`, `pro`, `ultra` (default), `ultra2x`, `ultra4x`, `ultra8x`
- Add `-fast` suffix for speed over depth: `ultra-fast`, `pro-fast`, etc.

**Options:**
- `-w, --wait` — Wait for completion and show result
- `-p, --processor` — Choose processor tier
- `-j, --json` — Raw JSON output

### 2. Schedule Auto-Check (optional)

Deep research tasks take minutes to hours. You'll want to poll for results automatically rather than checking manually.

**Options:**
- **OpenClaw users:** See `OPENCLAW.md` for cron-based auto-check scheduling
- **Other setups:** Use any scheduler (cron, systemd timer, CI job) to periodically run `parallel-research status <run_id>` and `parallel-research result <run_id>` until complete
- **Simple approach:** Just use `parallel-research create "..." --wait` to block until done (works for shorter tasks)

### 3. Manual Check (if needed)

```bash
parallel-research status <run_id>
parallel-research result <run_id>
```

### 4. Save to Research Folder

Create the research folder and save results:
```
~/.openclaw/workspace/research/<topic-slug>/
├── prompt.md          # Original question + run metadata
├── research.md        # Full Parallel output
```

**prompt.md** should include:
```markdown
# <Topic Title>

> <Original research question>

**Run ID:** <run_id>
**Processor:** <processor>
**Started:** <date>
**Completed:** <date>
```

**research.md** contains the full Parallel output, plus any follow-up notes.

---

## PDF Export

**All PDFs go in the research folder** — never save to `tmp/`. Whether using `export-pdf`, the browser `pdf` action, or any other method, the output path must be `research/<topic-slug>/`.

Use the `export-pdf` script to convert research docs to PDF:

```bash
export-pdf ~/.openclaw/workspace/research/<topic-slug>/research.md
# Creates: ~/.openclaw/workspace/research/<topic-slug>/research.pdf
```

For browser-generated PDFs (e.g. saving a webpage as PDF):
```
browser pdf → save to research/<topic-slug>/<descriptive-name>.pdf
```

**Note:** Tables render as stacked rows (PyMuPDF limitation). Acceptable for research docs.

---

## Commands

- **"new research: <topic>"** - Start interactive research doc
- **"deep research: <topic>"** - Start async deep research
- **"show doc"** / **"show research"** - Display current research file
- **"summarize"** - Synthesis checkpoint
- **"graduate"** - Move research to next phase
- **"archive"** - Mark as complete reference
- **"export pdf"** - Export to PDF
- **"check research"** - Check status of pending deep research tasks

---

## Document Principles

- **Atomic findings** - One insight per bullet
- **Link everything** - Sources, docs, repos
- **Capture context** - Why did we look at this?
- **Note confidence** - Use qualifiers when uncertain
- **Date important findings** - Especially for fast-moving topics

---

## Setup

See `SETUP.md` for first-time installation of:
- `parallel-research` CLI
- PDF export tools (pandoc, PyMuPDF)

