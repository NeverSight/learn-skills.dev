---
name: vai-custom-op-candidates
description: Find customOperator optimization chains and their ONNX node boundaries
license: Apache-2.0 WITH LLVM-exception
compatibility: Requires VitisAI 6.3+
metadata:
  version: 6.3.0
  stage: beta
---
<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
-->

# Finding customOperator optimization opportunities

Goal: find every place in a compiled model where one custom AIE kernel could replace a group of operators, and report them ranked, each with the ONNX start and end node that bound it.

Work through sections 1–6 in order, format with section 7, then run the checklist in section 8 before replying. Each rule is stated once, in its own section; where another section needs it, it is referenced by number rather than repeated.

---

## 0. Output contract

The entire reply is these things, in this order, and nothing else:

1. the summary table (§7.1)
2. the context block (§7.4)
3. **the dominant-operator line** — the gather call's `headline` string, printed verbatim when it is non-empty, after the context block (§7.4)
4. the topology drawing (§7.5)

The order is fixed. The question asked is where a custom op would help, so the table answers it first; the dominating operator is context for that answer rather than a preface to it. It still has to appear, and in full: when one operator takes more of the model's time than every fusion in the table combined, a reader who never reaches it has been misled. Print it after the context block, never inside it as a bullet, and never as a substitute for a row. The sentence itself comes back from the tool, so printing it is a copy, not a composition — five wordings of a placement rule did not hold before that.

**Write for someone who has never seen this skill or its tools.** No tool names, no field names, no section numbers. `zero_gain_count`, `no_span_count`, `nodes_without_timing`, `get_fusion_candidates` and "this is the §6.4 case" all appeared in shipped replies; every one of them asks the reader to know how the answer was produced. Say the thing in English: "4 regions were found and dropped for having nothing absorbable", "3 of its 7 operators have no timing row of their own". Node names, operator types and shapes are the model's vocabulary, not ours — those stay.

**Say nothing while working.** No "I'll start by gathering…", no "Let me fetch…", no "Good, 100% offload confirmed", no announcing the next step. Text emitted between tool calls is part of the reply and counts against this. Run the tools silently; the table is the first thing you write.

**No prose dumps.** Extracted timing rows, per-node cost lists, chain-walk findings, span-tracing steps, commentary on what a tool returned — working material, not output.

**But facts still get reported.** Several rules require disclosing something (breaker types, truncated timing, unresolved shapes, match coverage). Those are results: they go in the context block or a table cell, one clipped line each. This is a ban on narration, not on disclosure. Where the base rules require saying you did not read a whole paginated table, the context block is where that goes.

**Stop after the topology.** No "Key observation", no summary of the table, no restating a caveat, no "the real lever here is…". If the analysis found nothing worth a row, that is still a table — one row reading `*(none reportable)*` — plus the context block and the topology, not a paragraph of apology.

**Compose the answer once, when the data is in.** Everything above is written after the last tool call, in one pass. Do not begin the table and revise it: two replies shipped with a half-written row ending `... wait |  |  |  |`, a line reading "Let me correct:", and a second table underneath. Both tables render. A reader sees an abandoned draft and cannot tell which one is the answer. Working out that a grouping was wrong is fine — doing it in the reply is not.

---

## 1. Gather (one call)

```
get_fusion_candidates(folder)
```

It returns everything the reply needs: every fusible region in the model already costed, spanned, linked and ranked, plus `npu_time_us` (the denominator for every `% of NPU`) and `reason_counts`. **The regions you report come from here and nowhere else, and so do their figures.**

A candidate's `total_us` and `gain_us` are summed across its `occurrences`. `get_region_cost` costs **one instance** of the nodes you hand it. The two are therefore not comparable, and calling `get_region_cost` on a candidate to "confirm" it does not confirm anything — on `ssd_resnet34` it replaced a correct `169585.48 µs` row with `575.67 µs`, a figure that also covered only 2 of the region's 3 nodes. **Never overwrite a candidate's `total_us` or `gain_us` with a `get_region_cost` result.** That tool is for a region the user named that is not in the candidate list.

Rows go in `rank` order, `rank: 1` first, and `rank: 1` is the row you bold. Do not re-order on a judgement about which region is more interesting.

Make it your first call and do not follow it with `get_subgraph_reasons` or `get_npu_time_summary` for figures it has already given you — each extra round-trip costs about six seconds of the reader's time, measured across the P0 set, and buys nothing.

**1.1 is the analysis.** It removes the heavy-compute operators from the operator graph and takes the connected runs that remain, so the region set is exhaustive by construction and identical on every call. Use its `candidates` in the order given.

This replaces walking the graph. Do not call `get_operator_edges` to look for regions it missed, do not assemble a region by hand, and do not report a region that is not in its list. Enumerating by hand is what made this analysis unrepeatable: on `ssd_resnet34` three runs of this same question put the top opportunity at **4715, 433 and 8739 µs**, and on `yolo12m` one run said nothing was reportable while the next found a 15.5% win. Neither run was careless; the search simply started somewhere different.

A candidate whose span cannot be cut is already gone from the list (counted in `no_span_count`), so every entry you are given can be reported as-is.

Also read from 1.1:

- `dominant_operators` — single operators above 5% of NPU time. **§7.4 requires reporting these.**
- `cpu_operators` — anything not on the NPU (§2.4).
- `zero_gain_count` — regions found and dropped for having nothing absorbable (§2.3). Report the number in English, never the field name.
- `zero_gain_regions` — the costliest of those, named. **Report each one in the context block**: what the block is, its span, its cost, and its `ceiling_us` described as a ceiling in words. On `Anduril_yolox_l` the SPP block — a Sigmoid, three MaxPools and a Concat — costs 628.74 µs and scored zero, and a bare count let a reader conclude the model had nothing in it worth looking at.
  A ceiling is not a gain. Write "a fused kernel could not save more than 272 µs of it", never "expected gain 272 µs", and never put it in the table: a fused SPP still pools three times, and what fusion actually removes is the traffic between those pools, which sits inside the pools' own measured time where it cannot be separated out.

Do not call `get_single_timing_dataframe`: it is paginated, mixes leaf operators with containers and `PM Load` rows, and carries a duplicate of every operator row on the CPU timeline, so a hand lookup understates some regions and double-counts others while looking entirely plausible.

**Divide every `% of NPU` by `npu_time_us`.** Call `get_subgraph_reasons` only if you need the per-subgraph list rather than the counts, and `get_npu_time_summary` only for `operators_overlap` or the end-to-end figure.

That value is the NPU time the **Performance Summary tab displays**, so the analysis and the UI agree about the same model. Do not compute a denominator yourself: the timing table mixes leaf operators, program-memory loads, host phases, nested containers and a duplicate of every operator row on the CPU timeline, and a subset sum still looks plausible when it is wrong.

The tool also returns `operator_sum_us` — the per-operator npu-category total — and `operators_overlap`. When operators overlap, that sum exceeds `npu_time_us`, because overlapping work is counted once per operator but only once in the busy span. Region costs are built from per-operator times, so in that case the region percentages can add up to more than 100%. Still divide by `npu_time_us`; if `operators_overlap` is true, say so in one clause in the context block so the reader is not surprised by the arithmetic.

`inference_time_us` is end-to-end including host time. It is context only — never the denominator.

State the `npu_time_us` you used, in µs, in the context block.

---

## 2. What is a candidate

### 2.1 Size

At least two operators, **not** counting those whose reason is `PseudoOp`. When presenting a candidate, still show all its elements including the `PseudoOp` ones.

**A single operator is not a fusion candidate** — there is nothing to fuse — so exclude it when it already runs on the NPU, whatever it costs. The one exception is §2.4: a lone operator that fell back to the **CPU** is a genuine opportunity, because moving it onto the NPU is the win. Excluded single NPU operators are not opportunities and do not appear in the table.

**This rule applies to a whole candidate, never to a part of one.** It asks "is this entire candidate one operator?" — not "does this candidate contain a one-operator branch?". A split-and-rejoin or fan-in region (§3) is a multi-operator candidate no matter how short its individual branches are: three parallel MaxPools feeding a Concat is a four-operator region, not four single operators, and excluding it is wrong. Count the operators in the merged region and apply the rule to that number alone.

### 2.2 Boundaries — break at any heavy compute operator

Heavy compute means the ops doing the model's real arithmetic, as opposed to the data-movement operators a custom op absorbs. Match case-insensitively and include at least `conv`, `gemm`, `matmul`, `lstm`, `gru`, `rnn`, `attention`, `einsum`. Elementwise and shape ops (`Mul`, `Add`, `Reshape`, `Slice`, `Concat`, `Transpose`, `Pad`, …) are **not** breakers.

The list is **open**: if a model's arithmetic sits in a type not listed, that type is a breaker too. Sanity-check before starting — if breakers are under roughly a tenth of the operators, the set is too narrow for this model and the whole graph will come back as one candidate. Widen it once, then proceed; do not loop. Name the types you used in the context block.

Elsewhere in this skill "Conv/Gemm boundary" means a boundary at any heavy compute operator.

**Arithmetic that is not a boundary.** Some operators do real arithmetic but are not chain breakers, because fusing the region around them is still worthwhile — pooling is the common case, and an SPP block's parallel MaxPools feeding a Concat is the common case. Those regions are valid candidates, but the arithmetic inside them is **not** absorbable: a custom op replacing three MaxPools and a Concat still has to pool. Treat `pool`, `resize`, `interpolate`, `softmax`, `layernorm` and similar as arithmetic for §6's gain exclusion while leaving them as non-breakers here. Two different questions — where a region ends, and what inside it can disappear — and they do not have the same answer.

### 2.3 Other restrictions

- Break a chain if it has multiple outputs (the candidate list already keeps these together).
- The candidate's measured **cost** must be greater than 0. A region whose cost could not be fetched has _unknown_ cost, not zero (§6.1).
- **The Expected gain cell is always a number.** `see note`, `n/a`, a dash or a sentence is not a gain, and a row a reader cannot rank is not a suggestion. If there is no number to write, the region belongs in the context block, not the table.
- **`reportable: false` from `get_region_cost` settles it.** The gain is zero, so the row offers a reader nothing to act on. Do not restyle it into the table — a `0.00`, a dash, or a live gain cell with the caveat parked in another column are all the same row.
- **A region whose gain is `0.00` is not a suggestion.** The table is a list of things worth building; a row offering nothing to gain is noise in it, however interesting the region. Keep the finding, move it out of the table: one line in the context block naming the region and why nothing is absorbable (§7.4). This is not the same as dropping it silently — "the SPP block looks fusible but its three MaxPools are the work" is worth a reader's time, just not a row.

### 2.4 CPU fallback

If offload is below 100%, every operator running on CPU is an opportunity in its own right, single or not. List these first, ranked by their cost, before the fusion candidates. They use the same table (§7.1); their "region" is the CPU operator or the run of adjacent CPU operators.

---

## 3. Reading the candidate list

`get_fusion_candidates` has already done the parts that used to go wrong here: a region is a maximal connected run, so a split-and-rejoin, a fan-in on a Concat and a plain chain all arrive as **one** candidate with every leg included, and no two candidates share a node. Nothing needs merging, extending or de-duplicating.

What is left for you:

### 3.1 A region can still be too large to be one custom op

A candidate covering more than roughly a quarter of the model's operators is not a kernel — it says the model is poorly partitioned. Report that once in the context block and do not give it a row. Check §5.1 first: N copies of a small repeating unit is a motif, not an oversized region.

### 3.2 Occurrences are already grouped

Repeats of one region arrive as a single candidate with its `occurrences` count and its cost and gain summed across them — one kernel serves them all, including repeats that differ only in shape, which arrive with a `boundary_shapes` list. Do not group or split them yourself: doing it by hand was the least repeatable part of the answer, with one model giving seven grouped rows in one run and six ungrouped rows plus a `+7 more` footnote in the next, from identical figures.

### 3.3 The list is ranked by gain, not by interest

Take the candidates in the order given. If you reorder them, you are substituting a judgement for a measurement, and the reader is looking at row one.

### 3.4 Name each region for someone who did not write the model

The tool gives node names and operator types; it cannot tell you that a `Split → Slice → Neg → Concat → Mul → Add` run is a rotary embedding, or that a `Mul → Add` after every convolution is a learnable-affine block. That recognition is the most useful thing in the reply — an engineer who has never seen this model should be able to tell from the Region cell what code the kernel would replace. Use `get_onnx_model_topology` names, which carry the original module paths, and say what the block _is_, not just which operators it contains.

---

## 4. ONNX span — ask the backend, do not compose it

For each merged region, call:

```
get_onnx_span(folder, region_nodes=[<the region's operator-DAG node names>])
```

Report its `start` and `end` **verbatim**. They are real node names, verified against this model.

It does, in code, everything this step used to ask you to do by hand: maps `_Duplicated#N` and compiler-generated names back to ONNX, walks **every** path between the region's nodes so a branching region keeps all its legs, pulls in the glue that the compiled graph fused away, widens the boundary across adjacent Quantize/Dequantize pairs to a fixed point, and checks the span is a legal cut.

Use what it returns:

| Field                                                             | Use                                                                 |
| ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| `start`, `end`                                                    | the Region cell's `start → end` line, verbatim                      |
| `nodes`                                                           | the region's ONNX node list — use it for the `original` graph link  |
| `node_count`                                                      | the **Nodes** column                                                |
| `is_fusion_candidate`, `heavy_compute_inside`, `rejection_reason` | **if false, this is not a row.** See below                          |
| `cuttable`, `cut_error`                                           | if false, say so in the context block; the span is not usable as-is |
| `unresolved`                                                      | region names with no ONNX counterpart; if non-empty, say so         |
| `extended_over_quant`                                             | true when the boundary moved to enclose a quantize pair             |

**`is_fusion_candidate: false` is a rejection, not a warning.** It means a heavy compute operator sits _inside_ the region rather than bounding it (§2.2), so the region is at least two regions that were joined through a Conv/Gemm/MatMul. Do not cost it, do not rank it, do not report it. Split at each name in `heavy_compute_inside`, call the tool again on each piece, and report the pieces that come back clean. A region of a dozen Convs and Resizes is the model's arithmetic — reporting it as a fusion candidate claims a kernel can absorb the convolutions, and then the gain honestly computes to `0.00`, which reads as "no opportunity here" when the truth is "the region was wrong".

If every candidate in a model is rejected this way, the answer is that the model has no fusion opportunity — say that in one line. It is a real finding, and far better than a row that had to be zeroed to be true.

**Never write a span the tool did not give you.** Measured across 179 hand-composed spans, about half were unusable: abbreviated (`attn/MatMul`), a placeholder for a repeated block (`blocks.N`), a tensor name rather than a node (`..._output_0`), or absent. Those are all failure modes of composing the answer; none of them survive reporting what the tool returns.

If the call fails for a region, that region has no reportable span — say so in the context block rather than inventing one.

## 5. Motifs — one row per pattern, not per occurrence

The same structural region usually appears many times. One kernel serves every occurrence, so reporting each separately floods the table and buries the winner.

### 5.1 Decompose a repeated region into its repeating unit

Before anything else here: if a merged region is **N copies of the same short sub-pattern chained together**, it is not one big region. It is that sub-pattern with `Occurrences = N`. The compiler produces these routinely by unrolling — one source operator becomes a cascade of `_Duplicated#N` steps, each step identical in structure.

Report the **unit**, not the cascade: `Nodes` is the unit's operator count, `Occurrences` is the number of steps, and cost and gain sum across them. Getting this wrong cascades into three other problems — the over-merge guard (§3.1) fires on a region that is not really oversized, the graph links (§7.3) become an unusable list of every node in the cascade, and the binding check cannot be satisfied. If you find yourself writing a node count in the dozens with `Occurrences 1`, and the region visibly repeats, decompose it first.

A region that genuinely is one large unique block stays as it is — this rule is about repetition, not size.

**Key** = (ONNX `op_type` sequence, boundary shapes, boundary dtypes). Get shapes and dtypes from `get_onnx_model_topology` with `include_shapes=true` (`output_shape` / `output_dtype`, null when unresolved). Use only **boundary** shapes — the input of the span's first node and the output of its last; intermediates are implied by the op sequence and splitting on them separates identical regions for no reason.

Shape and dtype are in the key deliberately: a kernel written for one activation shape or dtype does not serve another, so the same op sequence at two shapes is **two rows**, each with its own occurrences and gain. Never merge across shapes or dtypes.

If shapes are unresolved, group on op-type sequence + dtype and note it in the context block.

Rank on **aggregate** gain across occurrences: the implementation cost is paid once, so a modest motif appearing 12 times can beat a single expensive one-off.

---

## 6. Expected gain — absorbing data movement

### 6.1 Cost and gain — ask the backend, do not add it up

For each merged region, call:

```
get_region_cost(folder, region_nodes=[<the same names given to get_onnx_span>])
```

Report what it returns. Do not recompute any of it:

| Field                                 | Use                                                                                          |
| ------------------------------------- | -------------------------------------------------------------------------------------------- |
| `total_us`                            | the **Current cost** cell, verbatim                                                          |
| `gain_us`                             | the **Expected gain** for one occurrence, verbatim — absorbable time already held to the cap |
| `cap_us`                              | the ceiling that produced it (§6.3); quote it if you explain the gain                        |
| `largest_node`, `largest_us`          | the operation the cap keeps; name it if you explain the cap                                  |
| `reportable`, `not_reportable_reason` | **false means this is not a table row** — §2.3, and check §6.4 first if the region repeats   |
| `missing_siblings`                    | **non-empty means the region is incomplete — see below**                                     |
| `nodes_without_timing`                | region nodes with **no timing row at all**                                                   |
| `nodes`                               | per-node `name`, `type`, `us` and `absorbable`, most expensive first                         |
| `matched` / `requested`               | the coverage figure                                                                          |

**`missing_siblings` is a stop, not a note.** The compiler unrolls one source operator into a run of `X_Duplicated#0..#N`, and they are one fusible unit. If the list is non-empty you named some and dropped others, so every figure for this region is understated. Add them to `region_nodes`, call `get_onnx_span` and `get_region_cost` again, and report the second answer. On petrv2-bevseg the same tail region came out at 434 µs, 649 µs and 1079 µs on three runs; only the run that named all five siblings was right.

**A node in `nodes_without_timing` costs nothing here.** It was fused into a neighbour and its time already sits in that neighbour's row, so `total_us` is right without it. Never give it a nearby node's value to fill the gap — that inflated one region by 20% and the wrong figure was indistinguishable from a measured one. If the list is non-empty, say so in the context block as `N of M nodes have no timing row (fused)`.

If the call fails for a region, that region's cost is unknown: its gain cell is `unmeasured`, which sorts below every measured gain. Never print `0.00` for a cost you could not fetch.

### 6.2 Why `gain_us` is the gain

You do not compute this — §6.1 returns it — but the row has to be defensible, so:

- A fusion absorbs **data movement**. It does not absorb arithmetic: the kernel still has to convolve, pool, resize and normalise. `get_region_cost` marks each node `absorbable` from its measured operator type, sums those, and holds the result to `cap_us`.
- The classification is done there rather than from `get_onnx_span`'s `data_movement_ops` because the two lists are in different name spaces. Costs are keyed by operator-DAG names (`Concat_3399_Duplicated#4`, type `BufferUnpadInnermostAdf`, 360 µs); the ONNX span lists `Concat_3399`. Intersecting them sums whichever names happen to appear in both, which is not a quantity with a meaning. Use `get_onnx_span`'s classification to _understand_ a region and `gain_us` to _report_ it.
- A motif's gain is `gain_us` times its occurrences.

> **Arithmetic is never gain, whatever its subgraph reason says.** A subgraph reason describes how something was compiled, not whether a fused kernel absorbs it — on a recurrent model the LSTM cells are themselves `TemplatedGraph`, and counting them claims the network computes itself for free. The `absorbable` flag is the authority, and the arithmetic it excludes covers both region boundaries (conv, gemm, matmul, lstm, …) and arithmetic that sits _inside_ a region without ending it (pooling, resize, softmax, normalisation). An SPP block of three MaxPools feeding a Concat is a legitimate candidate whose pooling is not absorbable.

### 6.3 Why there is a cap

`cap_us` is `total_us` minus the single most expensive node in the region. Whatever that operation does — arithmetic or moving data — the fused kernel still has to do it, so the best a fusion can achieve is eliminating everything _except_ that one operation.

It binds hardest exactly where this analysis looks hardest. A region of pure data movement has every node absorbable, so the raw sum equals the region cost _by construction_, and without the cap the table would claim the region becomes free. `gain_us` already has the cap applied; a gain equal to region cost means it came from somewhere else.

**The figures must agree.** `total_us`, `cap_us` and `gain_us` come from one call. If a sentence anywhere in the reply quotes a cost, cap or gain that differs from the cell beside it, it was derived rather than reported — an earlier reply managed three mutually inconsistent caps for one region this way. Quote each once, from the tool.

### 6.4 Regions priced against a kernel the model already has

`get_fusion_candidates` does this for you: a candidate carrying `gain_source` was priced against a fused kernel this model already emits elsewhere, and its `occurrences` covers every place the motif appears. Report those figures and say in the context block that the target came from an existing kernel, naming it. The rest of this section is why that number is trustworthy.

#### Why such a region scores zero without it

`cap_us` is `total_us` minus the largest node, so a region with exactly **one** timed node has a cap of zero and scores `0.00` however expensive it is. That is not always a real absence of opportunity. It is what a region looks like when the compiler folded the rest of it into a neighbour: the surviving node carries the cost, and the region cannot be scored from the inside.

Before writing such a region off, ask whether this model already fuses the sequence somewhere else:

```
get_fusion_precedent(folder, op_types=[<the span's ONNX op types, in order>])
```

If `found` is true, the model contains a kernel that already does this fusion, and `fused_avg_us` is what one occurrence costs when it happens — measured, on this hardware, in this model. The gain is then `total_us - fused_avg_us` per occurrence, floored at zero, and it replaces the cap-derived `0.00`. Say in the context block that the target came from an existing kernel and name it.

For the motif as a whole the tool has already done the arithmetic: report `motif_cost_us` as Current cost, `motif_gain_us` as Expected gain and `motif_occurrences` as Occurrences, all verbatim. Do not subtract one kernel's total from another's — they cover different numbers of occurrences, and doing it that way overstated dfine_m's affine motif by 15%.

This is worth the call whenever a `0.00` region repeats. D-FINE's learnable-affine `Mul → Add` is the case that motivated it: 25 occurrences, 3325 µs, 10% of NPU time, every one scored `0.00` because the Mul had been folded into the preceding convolution — while the same model emitted the fused `Mul`+`Add` kernel 15 times elsewhere at a quarter of the cost.

If `found` is false there is no measured target, and `0.00` stands.

**Two different things can make a gain cell look empty. Use the right one — they are not interchangeable.**

| Cell         | Means                                                                                                      | When                                                                                                                                                      |
| ------------ | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `unmeasured` | Cost unknown: `get_region_cost` failed for this region                                                     | §6.1 only. Sorts below every measured gain.                                                                                                               |
| `0.00`       | Measured, and nothing in the span is absorbable — every layer in it is heavy compute, or the span is empty | Never a table row (§2.3): report it in the context block. If a _data-movement_ region scores `0.00`, suspect the span or check §6.4 before writing it off |

Do not conflate the two. `unmeasured` hides a fetch failure; `0.00` is a finding.

- **Count each node once.** Gains are never added across rows that share nodes; if two rows share one, the merge was not applied.

**What this number covers** (context block, one line, not a paragraph): the data movement a fused kernel absorbs. It does **not** include per-subgraph launch overhead or program-memory reload, both of which a fusion also removes, so the figure is conservative. Report `reason_counts` and the absorbable share of NPU time — `PseudoOp` + `TemplatedGraph` excluding heavy compute — and let the reader conclude.

---

## 7. Output

### 7.1 Table

Write the header row exactly as the first column below — `Occurrences`, not `Occ.`; `Expected gain`, not `Gain`. A reader meeting the table for the first time should not have to ask what a column is, and there is nowhere in a static reply to expand an abbreviation.

| Column            | Contents                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Region            | Short name and operator types, then the ONNX span `start → end` on a second line in the same cell. **The two lines are not interchangeable.** A label such as `Concat → Add → Sigmoid → ScatterND` names operator _types_; the span names the two ONNX _nodes_ the cut runs between (`Concat_5315 → ScatterND_5991`). A row that carries only the type chain cannot be cut from, and one shipped that way. Every row has both. |
| Shape / dtype     | The candidate's `boundary_shape` and `boundary_dtype`, verbatim. When a motif spans several shapes the candidate carries `boundary_shapes` — list them, since one kernel source is instantiated at each. A dtype on its own (`int8`, `bf16`) is not an answer — a reader sizing a kernel needs the shape, and it is in the candidate                                                                                           |
| Nodes             | The candidate's `node_count` — its operators in the compiled graph, including pseudo-ops. **Not** the ONNX span's node count, which counts different things and differs: one reply printed 31 here and "9 of 27 region nodes" three lines later                                                                                                                                                                                |
| Occurrences       | Instances of this motif                                                                                                                                                                                                                                                                                                                                                                                                        |
| Current cost      | Measured cost of the region, µs                                                                                                                                                                                                                                                                                                                                                                                                |
| **Expected gain** | **µs, and % of NPU time**                                                                                                                                                                                                                                                                                                                                                                                                      |
| Graphs            | `original · optimized` — two links, one cell (§7.3)                                                                                                                                                                                                                                                                                                                                                                            |

### 7.2 Table rules

- One row per motif of merged regions. Never per occurrence, never per pre-merge fragment.
- Sort by Expected gain descending, ties by Current cost. Show the **top 5–10**; if more qualify, add `(+N more, together X µs)` as a line of text **below the table**. It is not a row: written as one it becomes a single cell in a seven-column table and renders as a broken row.
- **Bold the highest-gain row.**
- Percentages are **% of NPU time only**. Do not add an end-to-end column or an e2e figure.
- No prompt / "create a customOp with…" column — the Region cell's `start → end` already carries the boundary nodes. No separate ONNX span column.
- Exclude anything failing §2, any subchain of a longer chain, and any pre-merge fragment.

### 7.3 Graph links

`get_onnx_span` returns them built. Paste `links.markdown` into the Graphs cell, verbatim:

```
[original](…&graphType=original) · [optimized](…&graphType=optimized)
```

Two links, one cell — **the Graphs cell, and nowhere else**. The Region cell is plain text — **both of its lines**. Naming the block as a link there (`[Mul, Add + Reshape glue](aianalyzer://op?names=…)`) puts a second, differently-scoped link in the row and the reader cannot tell which one the Graphs column duplicates; writing the span as two links (`[/…/lab/Mul](aianalyzer://op?name=…) → [/…/lab/Add](…)`) is the same mistake, and it makes the span unreadable as text. Write it as `` `/…/lab/Mul → /…/lab/Add` ``. Both shipped, on the same model, in separate sweeps. Do not compose a link yourself, do not edit the ones you are given, and do not add a third: `original` shows what you would cut to build the kernel and `optimized` shows the region as the compiler sees it, which is what the decision needs. A `mapped` link answers a placement question at the cost of a third name space to get wrong.

They are built rather than described because every part of them was got wrong while it was described. Across 21 replies: `name=` — which highlights one node of a multi-node region and renders identically to a correct link — appeared in 8; one reply used the same URL for both graphs, so "optimized" showed the reader exactly what "original" did; `#` was left unencoded, which truncates the URL; and node lists were cut short with no sign of it. None of that is visible in the rendered table. The link is blue either way.

The two graphs do **not** share a name space — `original` takes ONNX names, `optimized` takes operator-DAG names with their `_Duplicated#N` suffixes — which is the trap the built links exist to remove.

If `links.truncated` is non-zero the region was too large to link whole; label the cell `optimized (30 of 87)` so the reader can tell a partial highlight from a small region.

### 7.4 Context block

A few short lines under the table, one fact each, no paragraphs.

**The first line is fixed.** Write it exactly in this shape, so a reader can check any percentage in the table against it at a glance:

```
NPU time: <npu_time_us> µs/inference (Performance Summary)
```

Append `; operator sum <operator_sum_us> µs — operators overlap, so region percentages can exceed 100%` when `operators_overlap` is true, and nothing extra when it is false. Use the figures from `get_npu_time_summary` verbatim; do not round them differently or restate them elsewhere in the reply.

**Link a single operator with `name=` and no `graphType`.** The dominating-operator line and any operator named in prose may link to that one node, but adding `graphType` to such a link tells the viewer to open that graph immediately — and the reply then opens the optimized graph before the reader has looked at the table. The Graphs cell is where a reader chooses which graph to open.

**A dominating operator goes after this block, on its own.** The gather call returns `headline`: when it is a non-empty string, print that sentence **verbatim** immediately after the context block and before the topology. Do not rewrite it, shorten it, merge it into a context bullet, or fold it into a table row. It is empty when no operator dominates, and then the context block is followed straight by the topology. You may add a link on the operator it names (`name=` only, no `graphType` — see above).

**When the best row is under about 1% of NPU time, say so in the first context line.** A table led by a 0.07 µs-per-cent row answers "where would a custom op help?" with "nowhere, technically here", and the reader deserves that in words rather than having to read the percentage and infer it.

Then the remaining lines. Always: the subgraph reason counts; the absorbable share of NPU time. Add only when applicable: nodes with no timing row (§6.1); heavy-compute types used (§2.2); a region whose cost could not be fetched (§6.1); shapes unresolved (§5); a region capped or mis-scoped (§6.3); a region too large to be a custom op (§3.1). Past about six lines you are explaining — cut back.

### 7.5 Topology

A drawing of the full optimized graph with the selected regions marked, **below** the table. It shows where each opportunity sits and is checkable evidence you walked the whole graph, so cover it end to end.

Keep it a map, not a listing: show structure and mark regions; collapse repetition (`×N`, not N copies); no per-node costs, subtypes or reasons — those are the table's job. If it does not fit roughly a screen, collapse more repetition rather than truncating the graph.

---

## 8. Checklist before replying

- [ ] Reply is table → context block → topology, with no narration anywhere, nothing after the topology, and no
      abandoned or restarted table (§0).
- [ ] Every region's figures came from `get_region_cost`, quoted not recomputed; nodes with no timing row counted as
      zero and disclosed, never given a neighbour's value (§6.1).
- [ ] Every reported region came back `is_fusion_candidate: true`; rejected ones were split at `heavy_compute_inside` and
      re-resolved, not reported and not silently dropped (§4).
- [ ] Single-operator exclusion applied to whole candidates only, never to branches inside one; CPU operators listed as opportunities (§2.1, §2.4).
- [ ] Every reported region came from `get_fusion_candidates`; none was assembled by hand (§1.1).
- [ ] Rows are in the order the candidate list gave them; no region exceeds ~¼ of the operators (§3.1, §3.3).
- [ ] Each Region cell names what the block _is_, not just its operator types (§3.4).
- [ ] No Region cell contains a link — every graph link is in the Graphs cell (§7.3).
- [ ] Every row's cost and gain is the candidate's own `total_us` / `gain_us`, not a `get_region_cost` result (§1).
- [ ] Rows are in `rank` order and `rank: 1` is the bolded row (§1).
- [ ] Every Region cell carries the node-name span, not just the operator-type chain (§7.1).
- [ ] Every span came from `get_onnx_span` and is reported verbatim — none composed, abbreviated or invented (§4).
- [ ] Motifs split by shape and dtype (§5).
- [ ] No heavy-compute operator sits inside a region, and none of its time is counted as gain (§2.2, §6).
- [ ] Repeated cascades decomposed into their repeating unit with Occurrences (§5.1).
- [ ] Every row's cost and gain are `total_us` and `gain_us` as returned, and every figure quoted in prose matches the
      cell beside it (§6.1, §6.3).
- [ ] No region came back with a non-empty `missing_siblings` — each was re-resolved with the siblings added (§6.1).
- [ ] `% of NPU` divides by `npu_time_us` from `get_npu_time_summary`, stated verbatim in the first context line (§1.4, §7.4).
- [ ] No region's cost or gain includes a `PM Load` row — `PM Load` is not a graph node and never belongs in `region_nodes` (§6.1).
- [ ] `unmeasured` used only where `get_region_cost` failed, never for a measured region that simply has nothing absorbable (§6.1).
- [ ] Every Graphs cell is `links.markdown` from `get_onnx_span`, pasted verbatim — no hand-written link anywhere in the
      reply, and no `name=` (§7.3).
- [ ] No arithmetic counted as gain, including non-breaker arithmetic such as pooling (§2.2, §6).
- [ ] Rows are in descending Expected gain order — check the column top to bottom before sending; the largest gain
      must be row one, or the reader's eye lands on the wrong opportunity (§7.2).
- [ ] Percentages are % of NPU only (§7.2).
- [ ] When `headline` is non-empty, it appears **verbatim and unedited after the context block**, before the topology (§0, §7.4).
- [ ] No single-operator link carries `graphType` — that opens a graph unasked (§7.4).
- [ ] No tool name, field name or section number anywhere in the reply (§0).
- [ ] The Nodes column is the candidate's operator count, and any "N of M" in the context uses the same M (§7.1).
- [ ] The `(+N more …)` tail is a line below the table, not a row in it (§7.2).
- [ ] Every row came back `reportable: true`; regions with a zero gain are named in the context block (§2.3, §6.1).
- [ ] Every zero-gain region the tool named is reported in the context block, with its cost and its ceiling described as a ceiling (§1.1).
- [ ] Every Expected gain cell is a number, and none of them is `0.00` — zero-gain and unquantified regions are named
      in the context block instead (§2.3, §7.4).
- [ ] Any repeated region scoring `0.00` was checked with `get_fusion_precedent` before being written off (§6.4).
- [ ] Column headers are spelled out, not abbreviated (§7.1).
- [ ] Every operator name written anywhere in the reply came from a tool result — no name assembled from an
      operator type and a remembered index (§7.3).
