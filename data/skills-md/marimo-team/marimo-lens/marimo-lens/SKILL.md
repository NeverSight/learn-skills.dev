---
name: marimo-lens
description: >-
  Add Lens to a live notebook, explain a notebook with a guided Trail, or
  address a user's selection on a rendered output or configured DOM target.
  Use when asked to enable Lens, give a walkthrough, explain results in place,
  or act on selected points, regions, and notes. The address mode handles every
  open selection. Requires the live marimo notebook kernel, reached through
  marimo pair or the editor's code-mode sidebar.
---

# Work with marimo Lens

Lens adds visual collaboration to a live notebook. It can show a Trail through
the notebook's results or connect a selected surface to its source, context,
and captured image. The active code-mode integration owns notebook inspection,
editing, and execution.

## Choose the workflow

| User intent                                                | Action                                                                                |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| "Add Lens" or "I can't see Lens"                           | Reuse an existing instance or [add Lens](#add-lens-when-missing).                     |
| "Walk me through this notebook" or "Explain these results" | Inspect the relevant cells and [show a Trail](#explain-the-notebook-with-a-trail).    |
| "Change this" or "Address my selections"                   | [Read the selected request](#address-a-selection), verify the result, and resolve it. |

Route from the user's request. A general explanation can use a Trail even when
there are no selections. Existing selections do not turn an explicit
walkthrough request into permission to edit or resolve them.

This core skill contains the complete ordinary mounting and Trail workflows.
Read a reference only when its task or exception applies.

Run each Python block in this skill as one call in the live notebook kernel.
From a terminal, that call is one `marimo pair execute` with the block on
stdin, and printed results arrive in its JSON `stdout`.
[Run Lens through marimo pair](references/setup.md#run-lens-through-marimo-pair)
covers targeting, errors, and concurrency. In the editor's code-mode sidebar,
each block is one `execute_code` call. Reuse instructions already loaded for
the same environment and Lens installation.

Speak as a colleague in chat, activity, popovers, and summaries. Describe what
you changed or found and the evidence behind it. Use concrete labels and a
short supporting message. On a read-only tour, describe existing findings.
Use a teaching tone when requested.

## Begin with the requested work

After the integration's required first call, such as `help(cm)` for marimo
pair, combine connection with the first useful operation: check availability
for an add request, inspect relevant cells and values for a Trail, or read the
current selection snapshot. A separate call that prints only an identity is
unnecessary.

`connect(ctx)` reuses authored and automatically mounted instances. When one
browser-ready Lens owns the visible dock, it selects that Lens even if the
context contains other Lens objects. Keep its opaque identity when work spans
calls. Each call has a fresh scratchpad, so reimport `cm` and `marimo_lens`,
reacquire the context, and select that same Lens using `identity=` in later
calls.

For `lens_ambiguous`, inspect `marimo_lens.agent.discover(ctx)` and choose the identity
matching the request and visible surface. Ask the user if those clues cannot
distinguish the instances.

## Add Lens when missing

Check availability during the mounting call. Retry an unavailable connection
only when a Lens cell or host mount is still being created or rendered. Once
you establish that no Lens exists and no mount is pending, add it immediately.

For an ordinary notebook with no pending mount, reuse an available Lens or
queue one cell:

```python
import marimo._code_mode as cm
import marimo_lens

async with cm.get_context() as ctx:
    available = marimo_lens.agent.discover(ctx)
    if available:
        print({"identities": [mounted.identity for mounted in available]})
    else:
        print({"cell_id": marimo_lens.agent.add_lens_cell(ctx)})
```

End the call so the queued cell can run and the browser can render the dock.
Reconnect in a fresh call and confirm the dock is available. The helper reuses
its previously added Lens cell and reruns it when it holds no live Lens. A host
with a custom mounting policy mounts Lens through its own integration, as
described in [setup](references/setup.md).

A notebook reopened in a new kernel, for example after a server restart, can
show every cell as stale. None of its cells have run, so no Lens exists and
selections from the previous kernel are gone. A code-mode call runs notebook
cells only through `ctx.run_cell()`. Run the cell that mounts Lens: a cell that
imports marimo, or an authored Lens cell. Otherwise use the helper.

If the user only asked to add Lens, report that it is ready and finish. Continue
to a Trail or selection workflow when that is part of the request.

## Explain the notebook with a Trail

A Trail is an ordered explanation attached to notebook cells. Each step brings
its result into view with a label and message. Use it for introductions,
walkthroughs, and explanations so the user can follow the evidence in place.

Reuse verified context from the conversation. If the route is unknown, connect
and inspect a compact outline of `ctx.cells` in one call: IDs, names, statuses,
and first code lines. Batch-read the relevant landmark cells, their errors, and
the needed live values in `ctx.globals`. Explain the question, evidence, main
result, and next step in notebook order. Once those findings are verified,
send one Trail and return control.

Use `ctx.graph.cells` to check executable graph membership. A narrative cell
outside that graph can inform the explanation but cannot be a reveal target.
Before presenting a result, verify its source and values and confirm the cell
is idle and free of relevant errors.

After inspecting the results, choose a short route. For a notebook with cells
named `inputs`, `analysis`, and `summary`, this complete call shows a Trail.
Substitute the actual cell names and explanations supported by their values:

```python
import marimo._code_mode as cm
import marimo_lens

ctx = cm.get_context()
mounted = marimo_lens.agent.connect(ctx)
route = [
    ("inputs", "Inputs", "Start with the values used by this notebook."),
    ("analysis", "Calculation", "Follow how the inputs become a result."),
    ("summary", "Conclusion", "Review the result and what it supports."),
]
steps = []
for name, label, message in route:
    cell = ctx.cells[name]
    if cell.id not in ctx.graph.cells or cell.status != "idle" or cell.errors:
        raise RuntimeError(f"Verify {name} before revealing it")
    steps.append({"target": cell.id, "label": label, "message": message})
mounted.reveal(steps, duration_ms=None)
```

Put the explanation in each step's message, using concrete findings from the
notebook. `reveal()` accepts 1–16 ordered steps and returns `None`. Each step has a target, an
optional label of up to 40 UTF-16 units, and an optional message of up to 1,000.
The user navigates the popover at their own pace. Return control after showing
the route. A text/data walkthrough requires no selection snapshot, PNG capture,
resolution, or timing loop. Edit or rerun cells only when requested.

A Trail is transient. Dismissal, refresh, another attention event, or changes
to referenced cells or their upstream inputs end it. A finite `duration_ms`
limits the entire route, and navigation does not restart that timer. Verify
changed results before showing another Trail.

## Address a selection

Read the open selections and their notes in one call. The selections live in
`snapshot.references["selections"]`, and `snapshot.current` is the likely
referent for "this" or "here":

```python
import json

import marimo._code_mode as cm
import marimo_lens

mounted = marimo_lens.agent.connect(cm.get_context())
snapshot = mounted.context()
print(
    json.dumps(
        {
            "identity": mounted.identity,
            "revision": snapshot.revision,
            "currentId": (snapshot.current or {}).get("id"),
            "selections": [
                {"id": s["id"], "label": s["label"], "note": s["note"]}
                for s in snapshot.references["selections"]
            ],
        },
        ensure_ascii=False,
    )
)
```

An empty list means this notebook holds no open selections. The editor's
code-mode sidebar reaches only its own notebook, so tell the user and add that
notes in another notebook are addressed from that notebook's sidebar or
through marimo pair.

Follow [selection work](references/selections.md) for the complete lifecycle:
read context, inspect evidence, start activity, apply the requested change,
verify, reveal, and resolve. Preserve these boundaries:

- Use the stored `SelectionReference` and its captured revision as the
  presentation target. Its producing cells are provenance and edit locations.
  DOM targets can have zero or several producing cells.
- Inspect captured images before making visual claims about a selected mark.
  Verify changes against fresh runtime and browser evidence. Report the
  coverage limit when image inspection is unavailable.
- Keep activity visible through verification. Reveal replaces it. Call
  `reveal()` before `resolve()` with the same captured revision in one kernel
  call, then return control to the browser.
- Resolve with a concrete summary of the outcome and verification. Keep
  ambiguous, blocked, or unverified selections open. On revision conflict,
  stop owned activity, reconnect, and reassess fresh context.
- A Lens belongs to one notebook session. When the connected Lens holds none
  of the selections the user refers to, check the other notebooks as
  described in
  [selections in other notebooks](references/selections.md#selections-in-other-notebooks).

`$marimo-lens address` handles every open selection, including each note and
its evidence. For other requests, the user's instruction takes priority over
an older selection note. An empty selection list still permits a requested
overview or walkthrough.

## Read further

Use [setup](references/setup.md) for a missing package or notebook connection, or a custom mount,
[target authoring](references/targets.md) when creating selectable HTML or
widgets, and [code-mode recipes](references/workflow.md) for image transfer,
feedback across calls, and recovery.

For selection work, read its reference inside the notebook:

```python
import marimo_lens

print(
    marimo_lens.agent.skill()
    .file("references/selections.md")
    .read_text(encoding="utf-8")
)
```

Use `help(mounted)` or `help(mounted.reveal)` for precise operation contracts.
The [documentation index](https://marimo-team.github.io/marimo-lens/llms.txt)
routes broader examples and API guidance. Check published APIs against the
installed version.
