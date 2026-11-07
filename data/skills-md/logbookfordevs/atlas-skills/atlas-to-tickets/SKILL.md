---
name: atlas-to-tickets
description: "Break a plan, specification or conversation into tracer-bullet implementation tickets with explicit dependencies. Save locally by default; publish to a tracker when requested."
metadata:
  short-description: Create tracer-bullet tickets with explicit blocking edges.
disable-model-invocation: true
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets** — tracer-bullet vertical slices, each declaring the tickets that **block** it.

Tickets are written as local ticket files by default. They may be mirrored to an external tracker when requested, but the local files are the planning source of truth unless the user chooses another destination.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests) — vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges** — the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket — green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)
- **What it delivers**: the end-to-end behavior this checkpoint makes work
- **Test seam**: the public interface and behavior the ticket will prove, or why TDD has no meaningful seam

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any tickets be merged or split further?
- Should approved tickets be written as local checkpoint files, external tracker issues, or both?

Iterate until the user approves the breakdown.

### 5. Write the tickets

Write the approved tickets. **How** depends on the user requested or default — the tickets are the same either way, only the shape of the blocking edges changes. Follow the active repo or user artifact convention for local paths.

Every ticket derived from source artifacts must include a compact `Source` reference naming the relevant artifacts and locating exact material with named sections, quoted headings, line ranges, or a combination. Use the most stable and precise reference available, and include related links or exclusions when useful. Inline a small, decision-critical contract when it governs acceptance or would be costly to misread.

Include approved prototypes or design references when they govern implementation or acceptance, identifying the relevant frames, states, or flows.

After the user approves the breakdown and destination, read [ticket-templates.md](references/ticket-templates.md) completely and use the matching local or remote template.

- **Local files** → write one file per ticket in the scope's tickets folder, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below — one ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking / sub-issue relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Publish new tracker issues only when the user requested tracker publication or existing project context clearly expects it. If writing both local tickets and external issues, create local files first and add tracker links after publication.

Do NOT close or modify any parent issue.
