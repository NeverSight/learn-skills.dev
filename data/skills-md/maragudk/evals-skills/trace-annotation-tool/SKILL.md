---
name: trace-annotation-tool
description: >
  Generate a custom trace annotation web app for open coding during LLM error analysis.
  Use when the user wants to review LLM traces, annotate failures with freeform comments,
  and do first-pass qualitative labeling (open coding). Also use when the user mentions
  "annotate traces", "trace review tool", "open coding tool", "label traces",
  "build an annotation interface", "review LLM outputs", or wants to manually inspect
  pipeline traces before building a failure taxonomy. This skill produces a tailored
  Python web application using FastHTML, TailwindCSS, and HTMX.
---

# Trace Annotation Tool Generator

Generate a custom local web application for **open coding** of LLM traces — the first
qualitative pass of error analysis in the Analyze phase of the evaluation lifecycle.

## Core Workflow

### Step 1: Understand the User's Trace Data

1. Ask the user to point to their trace data file (CSV, JSONL, JSON, or any structured format).
2. Read a sample of the data to understand its structure: field names, nesting depth, which
   fields represent the user query, intermediate steps, tool calls, and final output.
3. Identify a unique trace identifier field (or generate sequential IDs if none exists).
4. Confirm the structure with the user: "I see fields X, Y, Z — which represent the trace
   steps, and which is the user query?"

### Step 2: Ask About Additional Features

The tool includes these features by default:

- **Trace viewer**: One trace at a time, with tailored visual rendering of the trace structure
- **Freeform notes**: Text field for open coding observations
- **Pass / Fail / Defer**: Binary judgment with a defer option for uncertain traces
- **Keyboard shortcuts**: Navigation and annotation hotkeys
- **Progress indicator**: "17 / 100 reviewed" with pass/fail/defer counts
- **Auto-save**: Annotations saved to a separate JSONL file on every action

Ask the user: "These are the default features. Do you want anything else before I generate
the tool?" Then incorporate any additional requests.

### Step 3: Generate the Application

Generate a single-directory Python web application with this structure:

```
trace-annotator/
├── app.py          # FastHTML application (single file, all routes)
├── requirements.txt # Dependencies (fasthtml, python-fasthtml)
└── README.md        # Brief usage instructions
```

#### Technology Stack

- **FastHTML** for the web framework (HTMX is built-in)
- **TailwindCSS via CDN** (`<script src="https://cdn.tailwindcss.com">`) for styling
- **Vanilla JavaScript** only for keyboard shortcut bindings

#### Application Architecture

**`app.py`** — a single-file FastHTML app with these routes:

- `GET /` — main annotation view showing the current trace, annotation form, and progress
- `POST /annotate` — save annotation (notes + pass/fail/defer) and advance to next trace
- `GET /trace/{n}` — navigate to a specific trace (used by prev/next and keyboard nav)
- `GET /progress` — return progress stats (for HTMX partial updates)

**Data flow:**

1. On startup, read the trace data file from a path specified via command-line argument or
   environment variable.
2. Load existing annotations from `annotations.jsonl` (if it exists) to preserve prior work.
3. On each annotation action, append/update the entry in `annotations.jsonl` immediately.
4. The annotations file is separate from the source data — the original file is never modified.

**Annotations file format** (`annotations.jsonl`):

```json
{"trace_id": "abc-123", "status": "fail", "notes": "SQL query missed the pet-friendly constraint", "timestamp": "2025-01-15T10:32:00Z"}
{"trace_id": "abc-124", "status": "pass", "notes": "", "timestamp": "2025-01-15T10:32:45Z"}
{"trace_id": "abc-125", "status": "defer", "notes": "Not sure if tone is appropriate for investor", "timestamp": "2025-01-15T10:33:12Z"}
```

#### Trace Rendering

This is the most important part of the tool. Tailor the HTML rendering to the user's
specific trace structure. Apply these principles from HCI research on LLM review interfaces:

- **Visual hierarchy**: Emphasize the user query and final output. Use distinct visual
  blocks (background colors, borders, indentation) for different trace components.
- **Collapsible sections**: For multi-step traces, make intermediate steps (tool calls,
  reasoning, retrieval) collapsible — expanded by default for the first trace, then
  respecting the user's toggle state.
- **Domain-appropriate rendering**: If the trace contains emails, render them like emails.
  If it contains SQL, syntax-highlight the SQL. If it contains JSON tool calls, format
  them as structured blocks. Match the visual presentation to the content type.
- **Readable text**: Use comfortable line lengths (max-w-prose or similar), adequate
  spacing, and readable font sizes. Traces can be long — don't cram them.

#### Keyboard Shortcuts

Bind these shortcuts via a small inline `<script>` block. Display them in a help tooltip
or footer so the user can reference them.

| Key | Action |
|-----|--------|
| `p` | Mark as Pass and advance |
| `f` | Mark as Fail and advance |
| `d` | Mark as Defer and advance |
| `n` | Next trace (without annotating) |
| `b` | Previous trace (back) |
| `e` | Focus the notes text field |
| `?` | Toggle keyboard shortcut help |

Shortcuts must be suppressed when the notes text field is focused (so the user can type
normally). Re-enable them on blur.

#### UI Layout

Use a clean, minimal layout with TailwindCSS:

- **Top bar**: Progress indicator ("17 / 100 reviewed — 12 pass, 3 fail, 2 defer"),
  trace navigation (prev/next buttons), and keyboard shortcut help toggle.
- **Main area**: The rendered trace, taking up most of the viewport. Scrollable if the
  trace is long.
- **Bottom panel** (sticky): Annotation controls — the notes text field, and pass/fail/defer
  buttons. Always visible so the user can annotate without scrolling back up.

#### Styling Guidelines

Use TailwindCSS utility classes. The visual design should be:

- Clean and minimal — this is a productivity tool, not a marketing page
- High contrast for readability during long annotation sessions
- Distinct visual treatment for different trace components (user input vs. LLM output
  vs. tool calls vs. metadata)
- Responsive but optimized for desktop — this is a sit-down-and-work tool

### Step 4: Provide Usage Instructions

After generating the tool, tell the user how to run it:

```bash
cd trace-annotator
pip install -r requirements.txt
python app.py path/to/traces.jsonl
```

Then explain the workflow:
1. Open the browser (FastHTML will print the local URL)
2. Read each trace carefully, noting the **point of first failure** (the most upstream issue)
3. Write a short freeform note describing the observation
4. Mark as pass, fail, or defer
5. Use keyboard shortcuts to move quickly through traces
6. Annotations are saved automatically — you can close and resume anytime

Mention that annotations are saved to `annotations.jsonl` in the same directory.

## What Open Coding Is (and Isn't)

Open coding is the qualitative, exploratory first pass through trace data. The user reads
traces and jots down raw observations about what's going wrong — without trying to
categorize or structure the observations yet. The goal is to surface a broad, honest view
of system behavior before imposing any taxonomy.

**What to annotate**: Focus on the **point of first failure** in each trace — the most
upstream issue. In multi-step traces, a single early error often cascades into multiple
downstream failures. Fixing the first error frequently resolves the entire chain.

**When to stop**: Continue until at least 20 failing traces are labeled and no fundamentally
new failure patterns are appearing (theoretical saturation).

**What comes next**: Once the user has a body of freeform annotations, they move to
**axial coding** — clustering those observations into structured, binary failure modes.
This is covered by the `failure-taxonomy` skill.

## Anti-Patterns to Avoid

- **Over-engineering the tool**: The annotation tool is a means to an end. Generate a
  working tool quickly and let the user start annotating. Don't add features they didn't
  ask for.
- **Premature structure**: Don't add structured failure mode checkboxes or tag systems
  to the initial tool. Open coding is deliberately unstructured — the taxonomy emerges
  later. See `references/beyond-open-coding.md` for when and how to add structure.
- **Generic trace rendering**: Don't just dump raw JSON. Take the time to understand
  the trace format and render it in a way that makes failures easy to spot.
- **Ignoring keyboard shortcuts**: The textbook is emphatic that annotation speed
  directly correlates with engineering velocity. Hotkeys are not optional.

## Connecting to Next Steps

After open coding, the user's workflow typically continues with:

1. **Failure taxonomy** (the `failure-taxonomy` skill): Cluster freeform annotations into
   structured, binary failure modes via axial coding.
2. **LLM-as-Judge evaluators** (the `llm-as-a-judge` skill): Once failure modes are
   defined, build automated evaluators for each one.
3. **Extending the tool**: The generated annotation tool can be extended to support
   structured failure tags after the taxonomy is built. See
   `references/beyond-open-coding.md` for guidance.

Mention these next steps when the tool is delivered.
