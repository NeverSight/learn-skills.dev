---
name: hrt-change-size-gate
description: "Change-size check run inside the tempa-spec schema's `proposal` phase, before the \"What Changes\" list is finalized. Detects when a draft bundles several independent changes that each deserve their own change, stops and asks the user whether to split (default: one change; the agent never splits on its own), and when the user splits, records the deferred slices in proposal.md's Out of Scope section, discovery.md's Key Decisions, and openspec/BACKLOG.md. Rationale is in docs/research/2026-08-27-mattpocock-skills-gate-and-seams.md."
---

# hrt-change-size-gate

A change that bundles several independent user stories inflates every downstream phase (specs, design, tasks, apply) at once, and quality drops. This gate catches it at `proposal`, before any artifact is written.

The gate biases toward **one change**. Over-decomposition is the more common failure — a single broad story spanning many layers or capabilities is normal, not a split signal. The agent MUST NOT split on its own: it proposes, the user decides.

## When to run

Inside the `proposal` phase, after "What Changes" and "Capabilities" are drafted as working content, before either is finalized.

## The check

The agent MUST test the draft "What Changes" list for **two or more items** that satisfy ALL three conditions:

1. **Independently shippable** — shipping only that item (not the others) still gives a user something to use and verify.
2. **No dependency** — the item has no code or data dependency on another item in the list.
3. **Distinct capability** — no two of the items fall under the same capability in the **Capabilities** section being drafted. (`specs/**` does not exist yet this phase — check the Capabilities list, not disk.)

Example — independent: "add CSV export" + "add a dark-mode toggle" (ship either alone). Not independent: "add CSV export" + "add a permission check for export" (the check is meaningless without export — one slice).

- **Fewer than two such items** → the gate MUST NOT fire. Continue as one change, silently.
- **Two or more** → this materially affects scope. The agent MUST stop, MUST ask the user "one change or several?" (naming which items look independent and why), and MUST NOT proceed until the user answers. Silence is not an answer. The question MUST follow the `plain-language-writing` skill's COMMS rules.

In dark mode (`dark.md` exists) the gate still escalates to the user — it MUST NOT route to `hrt-dark-mode-decision-gate`. The answer depends on the user's capacity and priorities, which no grounding artifact holds.

## If the user keeps it as one change

Continue the proposal unchanged. Record nothing.

## If the user splits

Do these in order. Steps 1–3 run now; steps 4–5 run later in the same phase, as noted.

1. Ask which slice to build now. Write `proposal.md` for that slice only.
2. Add an `## Out of Scope` section to `proposal.md` — one line per excluded slice.
3. Add one entry to `discovery.md`'s **Key Decisions** (not Open Questions — this is a resolved scope decision with a rejected alternative):

   > Scope: build slice `<X>` only — slices `<Y, Z>` split to separate changes (decided at the proposal size-gate). Alternative rejected: one combined change (too large; downstream phases inflate).

   This entry MUST stay permanently — a later change that picks up slice `Y` MUST NOT remove it. It records what this discovery session covered.
4. When the phase's `hrt-adversarial-authoring` step runs: if its Destructive Critic narrows scope further, add the newly-excluded slice(s) to `## Out of Scope`.
5. Once `## Out of Scope` is final, sync `openspec/BACKLOG.md`:
   - If an existing entry is now covered by this change (judge its "Slice" line against the final `proposal.md`), delete that entry.
   - Append one entry per remaining `## Out of Scope` slice:
     ```
     ## <slug-kebab>
     - Raised by: <this change-id> (<YYYY-MM-DD>)
     - Slice: <1–2 sentences: what a user can demo when this slice is done>
     - Deferred because: <blocking dependency / scope / capacity>
     ```
   - If the file does not exist, create it with a `# Deferred Slices` title and one line:

     > Slices raised while planning another change, deliberately deferred. Not proposals — just enough to start a `discovery` session. Delete an entry when it becomes a change.

   - If a deletion empties the file of entries, leave the header — MUST NOT delete the file.

`## Out of Scope` in `proposal.md` is canonical (archived with the change); `BACKLOG.md` is derived from it and persistent (for pickup later). The redundancy is deliberate.

## Fallback

The gate needs an interactive user. In a non-interactive run the ask cannot resolve — proceed as one change and note in `proposal.md` that the gate could not run. This is a general OpenSpec limitation, not gate-specific.
