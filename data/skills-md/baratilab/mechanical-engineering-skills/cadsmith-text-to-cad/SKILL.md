---
name: cadsmith-text-to-cad
description: Generates dimensionally exact CadQuery CAD from natural language with the CADSmith multi-agent method — Planner, RAG-assisted Coder, sandboxed Executor, kernel-metric + three-view vision Validator, and Refiner in two nested loops (≤3 error repairs, ≤5 geometric refinements). Use when the user wants a part generated from a text description with verified dimensions, a STEP/STL from a spec, or wants to benchmark text-to-CAD output (Chamfer distance, F1, IoU).
---

# CADSmith: text → validated CadQuery

Paper: J. Barkley, R. Loghmani, A. Barati Farimani, *CADSmith: Multi-Agent CAD Generation with Programmatic Geometric Validation*, arXiv:2603.26512. On their 100-prompt benchmark it reached a 100% execution rate (versus 95% zero-shot), median IoU 0.963 (versus 0.809), and mean Chamfer distance 0.74 (versus 28.4).

Use this skill when correctness is checked against a stated spec. For quick parametric parts, `parametric-part-cad` is lighter. For FreeCAD macros, use `query2cad-freecad`.

Setup: `pip install cadquery trimesh scipy rtree matplotlib`.

## Workflow
`S=scripts/cadsmith.py`. Keep everything for a part in `runs/<name>/`.

1. **Plan.** Write `plan.json` following `references/agents.md`: components, target bbox (mm), holes (diameter, count), expected `n_solids`, and constraints. Convert the prompt's diameters and pitch-circle diameters explicitly. Don't write code yet.
2. **Retrieve.** `python $S kb "<keywords from the plan: polarArray hole revolve keyway ...>"`. Read the entries, especially the pitfalls.
3. **Code.** Write `part.py` with named dimensions, ending with `result = ...`.
4. **Execute (inner loop, at most 3 repairs).**
   ```bash
   python $S execute runs/x/part.py --out runs/x/v0
   ```
   On failure, save the traceback, run `python $S kb "<keywords>" --errors runs/x/v0_metrics.json`, fix only what it implicates, and log with `python $S log --run runs/x --stage inner --note "..."`. After 3 failed repairs, stop and report a code-execution failure.
5. **Validate (outer loop).**
   ```bash
   python $S check  --plan runs/x/plan.json --metrics runs/x/v0_metrics.json   # deterministic
   python $S render runs/x/v0.stl --out runs/x/v0_views.png                     # iso / high-rear / front
   ```
   Then run the **Judge** from `references/agents.md` with the prompt, code, metrics, check result, and image. Spawn an independent subagent for this when you can; the paper's point is that the generator mustn't grade itself. A kernel hard-fail (invalid or not watertight) fails regardless of the judge.
6. **Refine (at most 5).** Log each attempt with `python $S log --run runs/x --stage outer --note "<feedback>"`. When the ledger returns `escalate: true` (iteration 3 and later), change the construction approach.
7. **Deliver**: STEP, STL, the three-view image, `part.py`, the plan, and a table comparing the kernel bbox, volume, and hole counts with the spec. Say whether the judge was independent, and list any feature the renders couldn't confirm (small gaps at joints are the paper's documented near-miss).

## Benchmarking (optional)
With a reference model: `python $S eval gen.stl ref.stl` gives the Chamfer distance (sum of the two directional mean squared nearest-neighbour distances over 10k points), F1 at τ = 1 mm, and voxel IoU at 1 mm (coarsened above 100 mm). Everything is in absolute mm after bbox-centring and ICP, as in the paper.

## Prompt conventions that help (from the benchmark)
Explicit mm dimensions, axis-annotated orientation (XY base, Z up), origin-centred geometry, and coordinates for holes and slots. If the user's prompt lacks these, state the assumptions in the plan before coding.
