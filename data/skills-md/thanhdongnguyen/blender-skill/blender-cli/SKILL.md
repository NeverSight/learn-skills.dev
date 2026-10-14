---
name: blender-cli
description: "Implement Blender CLI tasks from a bundled feature catalog and offline Python API evidence. Discover capabilities before querying APIs; reject Blender facts or recipes supplied only by model memory."
---

# Blender CLI from supplied evidence

All Blender-specific capability choices, API identifiers, enum values, parameter meanings and workflow claims must come from this skill's data. **Pretrained Blender knowledge is not admissible evidence.** Use normal language comprehension, logic and Python composition to connect supported facts; do not fill a Blender knowledge gap with remembered behavior. User requirements supply desired outputs and artistic choices, not proof that an API exists or behaves a certain way.

## First context: the available capability families

Read the complete [capability overview](references/catalog/overview.md) **before querying the API database or drafting Blender code**. This layer is plain Markdown and transparently compressed JSON, available without SQLite. It lists the authored routes, all source API page cards, statuses and how to select them.

| User's area of work | Catalog domain |
|---|---|
| Scenes, objects, collections and transforms | `scene` |
| Mesh, BMesh and modifiers | `geometry` |
| Geometry Nodes, fields and instances | `geometry-nodes` |
| Curves, 3D text, hair, point clouds and volumes | `curves-volumes` |
| Sculpting, brushes and painting | `sculpt-paint` |
| UV maps, images and texture baking | `uv` |
| Materials, shaders, textures and worlds | `shading` |
| Lights, cameras and shadows | `lights-shadows` |
| Rendering, passes, color and image output | `render` |
| Compositing, masks and image processing | `compositor` |
| Video editing, titles and audio | `video-audio` |
| Grease Pencil, 2D strokes and Freestyle | `grease-pencil-freestyle` |
| Motion tracking and movie clips | `tracking` |
| Keyframes, drivers, rigs and constraints | `animation-rigging` |
| Simulation, physics and caches | `simulation` |
| Files, import/export, libraries and assets | `files-assets` |
| Python integration, math, GPU and UI | `integration-gpu` |
| API guides, enums and source indices | `api-guides` |

These are navigation categories, not guarantees of background-mode execution. Exact feature claims live in source-linked cards. `documented_route_runtime_unverified` means the source describes a route; `api_discovery_only` means a source page exists and must be read before claiming a behavior. `identifier_only` means the introductory source text does not describe enough behavior. Do not turn those latter statuses into implementation promises.

## Evidence workflow

1. **Discover before querying.** Read the overview, then the relevant domain file linked there. `python3 scripts/features.py match "the user request"` searches supplied Vietnamese/English aliases without opening SQLite. Read each candidate with `features.py show ID`; compare its `choose_when`, evidence excerpts and gaps. The presence of the same keyword is not enough to select it. Clarify output if several documented routes remain plausible.
2. **Handle unknowns explicitly.** If no authored route fits, use `features.py pages DOMAIN` and `features.py symbols TEXT` to discover source-provided names/descriptions outside the database. Select an `api:...` page card only as a discovery step. If no source supports the requested behavior, return `insufficient_skill_evidence` and name the missing fact. Do not invent an English Blender term, API, parameter or recipe from memory. External search is not a silent fallback: new material must be incorporated with provenance into the skill before it becomes task evidence.
3. **Make the selection reviewable.** Create a plan with `features.py plan --request "..." --feature ID --output /absolute/path/plan.json`. Repeat `--feature` for combined work. Its initial API queries come directly from the selected cards, not guessed identifiers.
4. **Read the API evidence.** Use `docs.py read REF --plan /absolute/path/plan.json` with a card's `next_queries`. The plan records the actual source hash and displayed line ranges. Continue pagination until the relevant selected passage is complete. Follow links actually exposed by read evidence, or select another documented feature/card when more context is needed. `docs.py search`/`symbol` may refine terminology already found in this supplied context; never treat a search hit or a matching identifier as behavioral proof.
5. **Implement only supported operations.** Record each Blender operation's source and what that source establishes in the plan's `bindings`; keep missing facts in `unresolved`. A property with only a type/default proves that limited contract, not an undocumented renderer effect. Node socket labels, dynamic enums and operator context must be inspected when the source leaves them open. Do not reuse a familiar recipe without grounding its Blender-specific statements. See [evidence workflow](references/evidence-workflow.md) for the exact plan format.
6. **Verify the selected runtime.** Follow [CLI workflow](references/cli-workflow.md). The bundled probe can collect observed RNA/version data; it cannot provide missing conceptual workflow semantics. Runtime observations are task evidence only when recorded, and any newly used Blender fact must still be explained from those observations and/or supplied source. If it remains undocumented, stop that dependent operation. Keep a missing executable or unresolved runtime fact explicit.
7. **Bind, execute and verify.** `evidence.py inspect` lists operations to review; `evidence.py seal` validates recorded reads/bindings and binds the script hash. `run_blender.py --plan ...` rejects missing/stale plans, unresolved facts, unrecorded citations and uncovered operation lines. Only the bundled probe is exempt. Read the actual result, reopen important saved data and inspect visual outputs before claiming success. These checks enforce traceability; they cannot prove arbitrary code semantics or that a model's internal knowledge was never activated.

## Commands

Paths below are relative to **this installed skill**, not the user's project. Host helpers use Python 3.10+ and the standard library; API lookups also require SQLite FTS5. Use absolute script paths when working elsewhere.

```sh
python3 scripts/features.py overview
python3 scripts/features.py match "text strip shadow"
python3 scripts/features.py show FEATURE_ID
python3 scripts/features.py pages lights-shadows
python3 scripts/features.py plan --request "..." --feature FEATURE_ID --output /tmp/blender-plan.json
python3 scripts/docs.py read SOURCE_REF --plan /tmp/blender-plan.json
python3 scripts/evidence.py inspect --script /absolute/path/task.py
python3 scripts/evidence.py seal --plan /tmp/blender-plan.json --script /absolute/path/task.py
python3 scripts/run_blender.py --script /absolute/path/task.py --plan /tmp/blender-plan.json --timeout 900 -- --output /absolute/path/result.blend
```

Use real IDs/refs returned by the catalog. The runner does not install Blender, save automatically, or make undocumented operations valid. Do not bypass this evidence workflow with raw CLI, remembered snippets, old forward-test examples or a fabricated binding. A citation must support its associated statement; a valid hash alone is insufficient.

## Data scope and maintenance

The supplied snapshot identifies API 5.2 and inventory project `Blender 5.2.1 LTS Python API`. It is not proof of the installed version. The [catalog coverage](references/catalog/coverage.json) distinguishes authored feature routes, all source page cards and unresolved description gaps. `references/api/api.sqlite3` is the packaged source of truth for API text, anchors, links, symbols, search and coverage metadata; see the [corpus guide](references/corpus.md).

The indexed reference is deliberately packaged for offline evidence reads. Read only the selected evidence in a task. The catalog is built from SQLite, not from embeddings or model memory. Raw HTML/assets, Blender Manual, upstream repository and extension pages are not packaged. Rebuild/update instructions live in the corpus guide; updating semantic source content invalidates prior evidence plans and requires reviewing the affected feature claims.
