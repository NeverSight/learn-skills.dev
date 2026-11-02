---
name: signal-integrity-review
description: RAG-backed. Review DipTrace PCB impedance, stackup, routed geometry, return paths, and configured external-solver evidence without inventing targets. Use for controlled-impedance, stackup, and return-path review of named nets; «проверь импеданс», «целостность сигналов», «возвратные токи». Use when the user says “Review impedance and return-path evidence for these PCB nets.”
---

Read [runtime access](../shared/runtime.md) before choosing between explicit-path
MCP, a live bridge session, and native/headless CLI. Their availability is separate.

# Signal-integrity review

RAG: **engineering memory by default** — [shared workflow](../shared/rag.md).
Use the indexed transmission-line, grounding and EMC material to justify the model,
assumptions and return-path checklist; solver output does not replace that basis.

Keep analytical equations, geometry heuristics, and external solver output in separate evidence
classes. No result is fabrication sign-off.
Use public `tools/list` for exact callable names and `get_capabilities` for document/configured
feature and adapter availability.

## Scope selection

- `microstrip`: supported single-ended analytical model for an outer-layer trace.
- `differential_microstrip`: supported coupled analytical model with explicit gap.
- `symmetric_stripline`: supported single-ended analytical estimate within its published range.
- Differential stripline: unavailable; return `blocked_by_capability`.
- `run_openems_stripline_analysis`: a registered typed external adapter, not a bundled solver.
- `run_ngspice_simulation`: a registered batch adapter for a caller-supplied netlist, not a PCB
  geometry extractor.

## Workflow

1. Call `diptrace_status`, `get_capabilities`, and `get_document_info`; freeze the PCB SHA-256.
2. Read `get_stackup` and `get_route_details`. Require explicit net, layer, dielectric
   height/permittivity, copper width/thickness, reference conductor, and target/tolerance when a
   pass/fail judgment is requested.
3. Use `calculate_impedance` for standalone inputs,
   `analyze_stackup_for_impedance` for complete outer-layer microstrip stackups, and
   `validate_impedance_constraints` for named routed nets.
4. Use `analyze_return_path` only as a caller-radius geometry heuristic. Disclose boundary-only
   pour geometry, layer-transition ambiguity, and confidence limits. If native refill evidence
   is needed, use the PCB headless profile on a copy and retain its exported geometry and verdict;
   do not call all native work unavailable based on the MCP tool list. Even refilled geometry
   does not turn this heuristic into a field solution.
5. Invoke ngspice/openEMS only when runtime discovery says the configured adapter is available.
   For openEMS retain request SHA-256, solver version, convergence, result SHA-256, and resources.
   For ngspice retain the netlist SHA-256, job status, return code/log summary, and resources; its
   current API exposes no executable version, convergence field, or result SHA-256, so record those
   fields as unavailable instead of inventing them.
6. Emit [`../shared/result.schema.json`](../shared/result.schema.json). Put impedance, effective
   permittivity, length/skew, frequency, and return-path coverage values in `measurements`, each
   with a unit, evidence class, and evidence IDs; do not hide numeric evidence in prose.

## Published and implementation boundaries

- Coupled microstrip validity requires `0.1 <= width/height <= 10` and
  `gap/height >= 0.01`; outside it, report unavailable/low-confidence metadata rather than forcing
  the permittivity-order invariant.
- Single-ended microstrip effective-permittivity validity uses
  `0.01 <= width/height <= 100`.
- Symmetric stripline uses `width/free_height < 0.35` and
  `thickness/free_height < 0.25`.
- Finite copper thickness is not corrected in the coupled branch. Do not use its wide-gap
  decoupling asymptote as a thickness validation.
- Every distance is millimetres; impedance is ohms.

These bounds and citations are returned by
[`impedance.py`](https://github.com/fireostendere/mcp_diptrace/blob/20e4bc107e3810945f729d3c81d0a379d9af8012/src/diptrace_mcp/impedance.py).
Adapter behavior is implemented in
[`external_adapters.py`](https://github.com/fireostendere/mcp_diptrace/blob/20e4bc107e3810945f729d3c81d0a379d9af8012/src/diptrace_mcp/external_adapters.py)
and mapped truthfully in
[`../capability-map.json`](../capability-map.json).

Use `analytical`, `heuristic`, and `external_solver` exactly as appropriate; never collapse them
into one confidence label.
