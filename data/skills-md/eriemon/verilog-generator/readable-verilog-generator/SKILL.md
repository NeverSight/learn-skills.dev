---
name: readable-verilog-generator
description: >-
  Use when creating, writing, reviewing, annotating, repairing, refactoring, or validating readable Verilog RTL, including synthesizable Verilog-2001 .v files, existing-RTL analysis, semantic comment annotation, testbench scaffold planning, ASIC-quality review, local or remote Vivado/xsim validation, evidence-backed repair, and workflow trace diagnosis.
---

# Readable Verilog Generator

Generate, analyze, improve, and verify readable Verilog-2001 RTL through the bundled runtime under `scripts/python/`. Keep design RTL and verification testbenches in `.v` files, use `scripts/python/facade/verilog_api.py` for host integration, and treat formatter-AST and external-tool evidence as stronger than model self-assessment.

## Route

- `create/write`: confirm the design contract, then use `requirements -> codegen_plan -> spec_document -> python -> rtl`.
- `deep_review`: insert a non-empty structured review between the Python semantic model and RTL; it must cover interface, reset, timing/pipeline, handshake or FSM behavior, width, synthesis, testbench coverage, and risks.
- `review/analyze`: remain read-only and report the eight public gate states before suggesting changes.
- `annotate`: preserve an immutable normalized baseline, change only `//` comments, prove token equivalence from that baseline, and rerun the final deliverable gate.
- `repair/refactor`: bind the task to real RTL, reproduce or validate the issue, and apply the smallest evidence-backed change.
- `agentic_repair`: use the existing-RTL `verify_existing_verilog(...)` loop with an explicit `conservative`, `semi_auto`, or `auto_apply` choice.
- `validate`: collect static or external evidence without implicitly editing RTL.

- Load `references/workflows/verilog_dispatcher.md` before routing. Existing assets, logs, waveform clues, and mixed inputs use its read-only entry decision before any generation, validation, backup, or remote action.

## Install v2.0.0

The package root contains `install.ps1`, `install.sh`, and `install.bat` beside this `SKILL.md`. They share the package-local Python backend and read only the generated installer projection under `assets/installer/` plus the same-level bootstrap descriptor. Platform IDs, root resolution, target templates, status text, exit codes, transaction policy, and verification cases are data-driven by `config/installer/`; do not add platform branches or current test values to code or comments.

Install only from a versioned payload with the configured `RELEASE_RECEIPT.json`. Use `--DryRun`/`--dry-run` to validate without creating transaction resources; use replacement flags only when the target and overwrite intent are explicit. A transaction handles one platform and one target, preserves unlisted target files, writes an install receipt, and attempts rollback on failure. Unknown IDs and source directories without a valid release receipt fail closed. See `references/skill/installation.md` for the complete contract and parameterized invocation templates.

## Generate And Modify

1. Confirm module name, ports, clock/reset, behavior, pipeline expectation, interface family, and verification cases.
2. Use `regular` by default; use `deep_review` only when its extra review stage adds value; use `agentic_repair` only for existing RTL.
3. Generate a Python semantic model before RTL in the staged workflow and use it as the testbench semantic contract.
4. Select local interface and ADC/DAC family templates only when the confirmed design matches them; record every adaptation in the requirements and codegen plan.
5. Keep batch execution generation-only, with one run directory per confirmed spec. Do not use batch mode for existing-RTL mutation or decision resume.
6. Treat streaming as provider interaction only. The finalized response artifact remains the extraction source of truth.
7. Run the strict generated-deliverable gate before downstream use. Optional lint and testbench helpers never replace it.

Every module generated or modified by this skill must ship with a same-name `<module>_spec.md` companion. The canonical JSON contract accepts a single legacy module projection or a `modules` array, but each normalized module must declare a safe `.v` `rtl_path`, complete interface ports, clock/reset semantics, cycle behavior, constraints, corner cases, verification cases, and at least one `timing_diagrams` entry. A timing entry contains `id`, `title`, `scenario`, `description`, and WaveJSON with named signals. `python -m scripts.python.workflow.cli write-spec --spec <spec.json> --out-dir <artifact-root> [--source <rtl.v>] --language <zh|en>` writes `spec/<feature>/<module>_spec.md` plus sibling `spec/<feature>/waveforms/<module>_<scenario>.json5` and `.svg`. The `--source` form fails closed when a module or port is undeclared; the no-source form validates and renders only the confirmed spec and never infers behavior from RTL. All waveform rendering goes through the renderer runtime declared by the settings authority and fails closed when its configured Node/npm prerequisites, package identity, version, or executable are unavailable. A render failure stages diagnostics without overwriting the previous valid bundle.

The default profile is `erie_strict`. Its authoritative naming, bilingual header, region, FSM, comment, port-order, runtime-message, and formatter-AST rules live in `references/rules/verilog-code-comment-naming-standard.md`, `references/rules/erie-style.md`, `references/rules/verilog-comment-placement.md`, and machine-readable assets. Do not duplicate those rule catalogs in this entry document.

## Quality

Strict quality control is mandatory. ASIC quality review, independent static lint, and testbench scaffold are optional workflow steps selected only when the task needs their evidence. Optional helper tools are inside the workflow and never replace the generated-deliverable gate.

Generated deliverables must pass the formatter-backed gate with zero errors and zero strict warnings. The public result matrix is exactly `compile`, `ast`, `readability`, `comment`, `naming`, `profile`, `testbench`, and `toolchain`; static compile evidence does not imply that an external simulator, synthesis, or remote validation ran.

Verilog/SystemVerilog filenames must describe real function. Functional digits are valid; VG148 rejects only terminal version or meaningless numeric suffixes. A file recognized as a testbench by `tb_`, `_tb`, `testbench`, or an exact `tb`/`testbench`/`sim` directory must use the `tb_<function>.v` or `tb_<function>.sv` form; `_tb` is recognition evidence, not an allowed output name. When an ordinary design filename carries at least two independent testbench-content evidence groups, VG149 remains inconclusive until the user confirms `design` or `testbench` through `file_role_confirmations`. Confirming `testbench` does not waive the prefix rule: rename the file to the authority-selected `tb_<function>` form before it can pass. VG150 rejects configured workflow/evidence phrases on entity comments and high-confidence periodic unrelated tail families; it does not blacklist ordinary Chinese words or isolated functional descriptions. The full filename and comment contract lives in `references/rules/verilog-code-comment-naming-standard.md`, and gate/report semantics live in `references/rules/verilog-quality-gates.md`.

Use strict mode for new or modified deliverables. `--non-strict --warn-only` is limited to historical reference-corpus analysis and never approves generated output. The formatter backend under `scripts/python/quality/formatter_backend/` is the parser source for quality checks; do not add a second Verilog parser.

For comment-only work, normalize the original RTL once, annotate a copy, run the comment-only verifier with a required delta, run the final gate, and compare the final file again against the immutable baseline. Comments must not change RTL tokens, modules, ports, lvalues, resets, always targets, or instance connections. Reused generic entity comments do not satisfy semantic-comment coverage.

When `VG097` cannot see an external XPM, UNISIM primitive, or project-generated IP interface, first consult the exact-name AMD-Xilinx primitive catalog in `assets/xilinx_primitive_semantics.json` and its detailed contract in `references/rules/xilinx-primitive-exemptions.md`. Keep the result `inconclusive` until a governed pure-interface `.v` source is supplied through the repeatable `--external-interface-source` option when the name is not cataloged or the profile conflicts. Use the registered `quality.external-interface-extract` command for explicit vendor-source module whitelists and `quality.external-interface-manifest` for reviewed project-IP contracts. Never infer that an unknown width is a mismatch, and never use a stub or primitive profile as simulation, synthesis, implementation, or hardware evidence.

Generated RTL must remain synthesizable Verilog-2001. Prefer the governed interface templates for AXI-Stream, AXI4-Lite, AXI4, AHB, and APB; use complete combinational assignments and case defaults; avoid raw gated clocks; document CDC/reset assumptions; keep datapath and control timing-reviewable; and avoid generated `function` or `task` blocks when explicit logic is clearer for waveform debug. Every FSM must use three independent processes for the state register, procedural combinational next-state logic, and state output/task logic; a continuous `assign` to any next-state signal is forbidden. Every continuous or procedural combinational target must pass both the transitive source-cone limit and the configured real-operation budget, each defaulting to at most three. VG146/VG147 evaluate the complete source closure: formatter structured port associations bind child outputs into the parent cone, parameter/localparam specialization selects the materialized implementation, and each definition root, full instance path, specialization fingerprint, and static target remains an independent report identity. Output connections expand through known implementations; inout and unresolved-net boundaries never invent reverse ownership; all known wire/tri drivers are merged; and a clocked output Q cuts upstream expansion while its D input remains checked. The operation budget covers unary, binary, ternary, comparison, selector, control-decode, continuous-assign, combinational-process, clocked D-input, and elaborated `for` operations. Moving logic into `always @(*)` or directly into a clocked D expression does not bypass either gate. If `loop_presence=unknown`, VG146 and VG147 both apply and share the same lower-bound evidence: an over-limit known lower bound fails both, otherwise both remain inconclusive. When the operation budget fails, recommend pipeline registers, registered flags or predecode, or a multicycle FSM decomposition first, and disclose that these changes may alter visible latency; immutable-latency protocols require manual architecture review. Only an exact output bridge from an output port to a clocked internal `_o` `reg` is exempt from the source-cone rule. Detailed VG rules and ASIC review criteria remain authoritative in `references/rules/verilog-quality-gates.md` and `references/rules/asic-verilog-quality.md`.

VG151-VG155 provide module-independent structural contracts. Parameter constraints are selected automatically from the identifiers in each restricted expression; `module`, `instance`, `hierarchy`, and `scope` fields are invalid. VG152 reports large dynamically selected packed storage with a configurable positive threshold and offers structured case/FSM, inferred-memory, or vendor-memory alternatives. VG153/VG154 expose read-without-driver and unused declaration evidence, including reg/wire/function/task facts. VG155 uses explicit top-level ready-valid role facts and requires both valid and ready for a transfer consumer; no target module name is part of these contracts.

Before generating or repairing declarations, apply VG156-VG158 as design-time naming and comment constraints, not only as a final audit. VG156 checks every module/function/task variable declaration by underscore token: a token containing digits is valid only when its complete case-insensitive text appears in the governed protocol/algorithm/rate allowlist. VG157 forbids ordinary-comment version markers such as `v2` or `version 3`; only the formatter-recognized fixed bilingual header and revision-history range is exempt. VG158 repeatedly removes the governed direction/type prefixes and `_o`, then requires at least one functional token outside the closed meaningless-token set; unknown domain terms pass. The formatter must assign each declaration to exactly one region using the shared conflict priority, place the first group comment directly below its banner, place later group comments after exactly one blank line, leave no empty group, keep one trailing blank line per non-empty region, and produce byte-identical output on the second pass.

## Existing RTL

- `analyze_existing_verilog(...)` owns structural analysis and durable design explanation.
- `improve_existing_verilog(...)` owns controlled testbench, style, partition, merge, and optimization assist flows.
- `compare_verilog_semantics(...)` owns equivalence, QoR, and transform-validation evidence.
- `verify_existing_verilog(...)` owns log-driven verification, diagnosis, candidate patches, confirmation resume, and terminal closure.

`optimize_assist` and `merge_assist` are assist-only by default and never silently accept or rewrite source RTL. `conservative` is report-only; `semi_auto` requires confirmation before overwrite; `auto_apply` is valid only after explicit selection and still downgrades non-eligible patch classes to confirmation. Preserve source and testbench backups, diff and decision artifacts, diagnostics, and terminal status exactly as specified by `references/workflows/workflow-contracts.md` and `references/integration/host-integration.md`.

Existing-RTL diagnostic comment findings are advisory so compile, semantic, interface, and high-confidence lint failures remain visible. A report file being written is not success; blocker, warning, failed, toolchain, external-validation, or confirmation-blocked terminal states remain non-success.

## Dependencies And External Evidence

Run dependency preflight before first use and before remote, Vivado, or Vitis work. Missing required dependencies require user approval before installation; if declined, continue only with self-contained static Verilog work and block remote/execute/implement claims. The required skill dependency remains `erie-remote-ssh`; the optional context-engineering group is the only recommended external skill group. No additional external skill suite is included. The required external renderer dependency, package identity, version, executable, and Node/npm floor are read from the settings authority; use `scripts/python/toolchain/wavedrom_runtime.py` with the `check`, `install --yes`, or `render` subcommand, never an ad-hoc package command. Prefer `vivado-developer` and `vitis-developer` for AMD-Xilinx, and `pds-developer` for PangoMicro. FPGA-Agent-Skills remains an explicit manual fallback.

Compile, execute, simulation, synthesis, or implement readiness requires actual external evidence. Remote validation is preferred and must use `erie-remote-ssh`, a user-confirmed server, local-only server selection/configuration, and the remote workdir's `.settings/verilog.remote.json`. A configured default is only a recommendation. Multiple Vivado settings candidates require user selection. Do not silently fall back to local tools and do not add direct SSH/SCP logic.

Remote validation runs are retained by default, including fixed remote-fixture reports. Cleanup occurs only when explicitly requested. Vivado xsim is the preferred simulator backend, followed by VCS+Verdi and then iverilog/vvp; yosys is implement-readiness evidence only. VCS+Verdi support is scripted backend invocation, not full GUI/session automation.

## Document And Command Registry

Registration is enabled for this skill. Markdown remains the authoritative knowledge source. Editable command records live under `config/registry/commands/`; document responsibilities and search metadata have one owner in `config/registry/documents/catalog.json`; current duplicate and interface decisions live in `config/registry/governance/reviews.json`; `config/registry/registry.sqlite3` is a generated local FTS5 trigram index at the location required by the agents-md-generator gate. The skill runtime is self-contained and must not import or call an external `agents-md-generator` registry implementation.

Document governance scans `SKILL.md` and every Markdown file below `references/`, recursively. It records one responsibility per document, knowledge pointers, exact and fuzzy duplicate adjudications, interface mappings, and content hashes. Remove only confirmed equivalent duplication; preserve structural repetition and every unique contract. Installed copies may query and check but must not mutate registry sources.

Detailed command syntax, examples, prerequisites, outputs, exit codes, risk warnings, and relations are retrieved from the local registry:

```text
python -m scripts.python.registry.query_registry ask "<question>" [--kind <kind>] [--category <name>] [--limit 1..10] [--json]
```

The query is read-only and never executes returned commands. Exit codes are `0` for hits, `1` for no match, `2` for request errors, and `3` for a missing, corrupt, stale, or incompatible index. After JSON source changes, use registry instruction `registry.build`; never edit SQLite by hand. See `references/skill/script-guide.md` for the compact registry lifecycle.

## Verify

The first outer command group is the generated-deliverable gate:

```text
python -m scripts.python.validation.generated_deliverable_gate <rtl-file-or-dir> --json <report.json> --markdown <report.md>
```

When either report option is omitted, the CLI writes both reports under the caller's current working directory: `reports/readable/deliverable_gate.json` and `reports/readable/deliverable_gate.md`. The focused quality CLI follows the same policy with `quality_gate.json` and `quality_gate.md`. Supplying one explicit path only overrides that format; JSON and Markdown paths must resolve to different files. Runtime reports must never be written back to the source or installed skill root.

Both CLIs publish v3 reports and print compact `[Python]` finding lines containing the VG rule, status, confirmed location, concrete problem, and direct fix instruction. The JSON and Markdown files contain the full evidence, ordered repair steps, risk and human-review obligation, plus bad/good examples. Exit code `1` means the gate found RTL issues; exit code `2` means invocation, diagnostic-contract, or report-publication failure.

The second outer command group is package validation:

```text
python -m scripts.python.validation.validate_verilog_skill --settings .\config\defaults.json
```

Run the smallest relevant checks while editing, then the governed final chain. The extended repository-regression, external-audit, and remote variants live in `references/integration/configuration.md` and registry instruction `validation.skill`. Local success does not replace requested remote pytest, simulator, synthesis, or installed-copy evidence. Never claim an unrun check passed.

## Resources

- `references/skill/script-guide.md`: registry query, build, document-governance, and command-category contract.
- `references/workflows/verilog_dispatcher.md`: task classification, public gate matrix, and safe repair boundary.
- `references/workflows/workflow-contracts.md`: run artifacts, statuses, resume behavior, and trace semantics.
- `references/integration/configuration.md`: paths, dependencies, remote settings, and validation configuration.
- `references/integration/host-integration.md`: facade functions and host-owned execution boundaries.
- `scripts/python/workflow/spec_document.py`: strict module contract, source cross-check, Markdown and WaveDrom bundle writer.
- `scripts/python/toolchain/wavedrom_runtime.py`: pinned Node/npm/WaveDrom check, explicit install, and SVG renderer.
- `references/rules/verilog-code-comment-naming-standard.md`: canonical readable RTL rule text.
- `references/rules/verilog-quality-gates.md`: VG catalog and report semantics.
- `references/rules/xilinx-primitive-exemptions.md`: exact AMD-Xilinx UNISIM/XPM/project-IP primitive inventory and VG097/VG132/VG146/VG147 boundary contract.
- `references/rules/asic-verilog-quality.md`: ASIC quality review criteria and risk boundaries.
- `references/rules/testbench-patterns.md`: self-checking testbench scaffold patterns.
- `references/checklists/lint-checklist.md`: independent static lint review checklist.
- `references/corpus/verilog-style-observations.md`: empirical ideal/bad corpus observations that do not override normative rules.
- `references/checklists/verilog-readability-gate.md`: final human review.
- `references/skill/skill-standards.md`: skill packaging and progressive-disclosure requirements.

## Boundaries

- Do not generate non-Verilog hardware flows, C/C++ kernels, or alternate RTL dialects.
- Do not invent source RTL, testbenches, logs, successful tool evidence, or repair confirmation.
- Do not store caller run artifacts inside the skill; use caller-selected directories such as `reports/`.
- Do not let optional helpers, model reviews, or registry query results replace actual quality or toolchain evidence.
