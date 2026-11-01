---
name: pixso-design-to-code
description: "Use Pixso MCP `design_to_code` to convert Pixso design nodes, screens, components, or Pixso URLs into target-framework code, save generated files, localize assets, and run safe cleanup without changing visual output."
disable-model-invocation: false
references:
  - ./references/cleanup.md
  - ./references/html-framework-bridge.md
  - ./references/resource-handling.md
---

# Pixso Design to Code

Use this skill when converting Pixso designs, pages, components, selected nodes, or Pixso URLs into frontend / client code.

## Required tools

- Use `design_to_code` for React, Vue, HTML, Flutter, and ArkUI.
- If the target framework is not supported above, generate HTML with `design_to_code`, then convert it to the target framework by following `references/html-framework-bridge.md`; the converted target-framework output must still continue through cleanup.
- After generation, follow `references/resource-handling.md` to save files, download image / font assets, and replace temporary URLs. Prefer its recommended cross-platform Node script, `references/resource-fetch.mjs`, for fetching code, downloading assets, and replacing URLs; fall back to its manual strategy only if the script fails.
- Use `get_screenshot` after generation to understand visual context for safe cleanup.
- Follow `references/cleanup.md` for class semanticization, DOM / CSS paired replacement, unused `id` cleanup, and cleanup audit.
- Use `refine_generated_code` only when the user explicitly asks for responsive layout, CSS variables, Tailwind, DRY extraction, or project design-system alignment.
- Keep `design_to_code` as the default entry point. Enter `pixso-read-dsl` directly for explicit DSL/reference/full-data requests. If `design_to_code` genuinely fails or returns output that cannot be used, fall back to `pixso-read-dsl` and combine node DSL with `get_screenshot` visual context for code generation and verification.
- Compact DSL is not raw Kiwi, decoded JSON, or a complete design-file snapshot. Do not treat it as a full raw input to the code-generation pipeline.

## Input rules

- Extract Pixso URL `item-id` values as node GUIDs; never pass full Pixso URLs to `design_to_code`.
- If multiple Pixso URLs are provided, extract every `item-id`, preserve input order, and include all GUIDs. Do not process only the first URL unless explicitly requested.
- `design_to_code.guids` must always be an array: `['node:id']` for one node, or multiple GUIDs for multiple nodes.
- Use `[]` only when the user explicitly asks for the current Pixso selection, or no concrete node is provided and the current selection is the intended target.
- For related pages / flows, pass multiple GUIDs together in one `design_to_code` call by default to preserve prototype links, navigation, and interaction context.
- Split GUIDs into separate `design_to_code` calls only when the user explicitly asks for independent pages / screens, standalone outputs, or no cross-page relationships.
- If the target framework is unclear, infer it from the project; if uncertain, ask or default to HTML and explain.
- Do not pass unsupported framework names to `clientFrameworks`; use the HTML bridge instead.

## Required workflow

1. **Confirm target and framework.** Determine GUIDs from URLs / selection and decide whether the target is `react`, `vue`, `html`, `flutter`, or `arkui`.
2. **Call `design_to_code`.** For supported frameworks, set the matching `clientFrameworks`; for unsupported frameworks, set `html` first and convert by following the HTML bridge rules. Use `get_variants` first only when the user asks for states, interactions, or variants. If the call genuinely fails or its result cannot be used, record the reason, use `pixso-read-dsl` to retrieve node structure and referenced data, call `get_screenshot(guid)` for visual context, and generate code from both sources. Continue fallback output through the same resource, cleanup, and verification workflow.
3. **Build a page manifest.** For every generated page / code entry, track `guid`, output file, and status.
4. **Process every output file.** Each file must complete: save -> resource handling -> `get_screenshot(guid)` -> Phase A cleanup -> Phase B cleanup -> verification.
5. **Fix necessary integration issues.** Fix asset paths, invalid code, or project-entry issues without rewriting or redesigning.
6. **Refine only on request.** Do not apply optional refinement when the user did not ask for it.
7. **Report per file.** Include output location, framework, resource status, cleanup audit, retained-item reasons, and known differences.

## Multi-page / multi-node gate

When there are multiple GUIDs or multiple generated code entries:

- Each output file is an independent delivery unit.
- One file reaching `delivered` does not complete the whole task.
- Every file must complete resource handling, screenshot capture or reported failure, Phase A, Phase B, and verification.
- Final response must include a per-file cleanup audit table, not only a global summary.

## Hard gates - forbidden shortcuts

- **Forbidden:** using `get_node_dsl` for ordinary code generation before actually calling `design_to_code` or confirming that its result is unusable. Explicit DSL/reference requests are exempt; a post-failure code-generation fallback must enter `pixso-read-dsl`.
- **Forbidden:** passing unsupported framework names to `clientFrameworks`.
- **Forbidden:** skipping `references/html-framework-bridge.md` during HTML bridge work, or using the bridge as an excuse to redesign, refactor, or abstract components.
- **Forbidden:** delivering target-framework code immediately after HTML bridge conversion without continuing through resource handling, screenshot context, Phase A cleanup, and Phase B cleanup.
- **Forbidden:** passing full Pixso URLs or a string `guids` value to `design_to_code`.
- **Forbidden:** processing only the first GUID when multiple URLs / `item-id` values were provided.
- **Forbidden:** splitting related pages by default when it may lose prototype links, navigation, or interaction context.
- **Forbidden:** stopping after `design_to_code` or after resource handling without screenshot context and cleanup.
- **Forbidden:** treating multi-page work as complete when only one output file passed cleanup and verification.
- **Forbidden:** leaving unexplained temporary localhost / Pixso export URLs in final code.
- **Forbidden:** deleting `id` values still referenced by CSS, JavaScript, tests, anchors, ARIA, or `label for`.
- **Forbidden:** changing visual appearance, layout hierarchy, interaction semantics, CSS declarations, selector priority, state styles, or responsive behavior during cleanup.
- **Forbidden:** changing class token counts during cleanup. Each existing class token may only be renamed to one replacement token; do not turn one class into base + modifier tokens.
- **Forbidden:** adding inferred state / modifier classes such as `active`, `selected`, `current`, `disabled`, `open`, or `is-*` unless already present in the generated code or explicitly requested by the user.
- **Forbidden:** introducing unrequested dependencies, CSS frameworks, component libraries, design systems, naming systems, broad refactors, or refinement tags.
- **Forbidden:** reporting only one global cleanup audit when multiple output files were generated.

## Fallbacks

- If a Pixso URL lacks `item-id`, request a node-specific URL or confirm current selection.
- If `design_to_code` fails because a GUID is invalid, re-check the URL `item-id` or current selection.
- If parameters and GUIDs are correct but `design_to_code` still fails or returns unusable output, use `pixso-read-dsl` to retrieve node DSL and required references, then call `get_screenshot(guid)`. Use DSL for structural/layout constraints and the screenshot for visual verification, and explicitly report that fallback was used.
- If `get_screenshot` fails, continue static cleanup where safe and report that visual context was unavailable.
- If asset downloads fail, keep reproducible details and list missing assets explicitly.
- If the generated structure does not fit the project, make the smallest necessary adaptation and report it.

## Completion

Before final response, confirm:

- target GUIDs / current selection and target framework were identified;
- `design_to_code` was called with array `guids`; if it failed or returned unusable output, the reason was recorded and `pixso-read-dsl` node DSL, referenced data, and screenshot context were used for fallback generation and verification;
- if the target framework is unsupported by `design_to_code`, HTML bridge conversion was completed 1:1 by following `references/html-framework-bridge.md`, and the converted target-framework output continued through cleanup;
- all generated files were saved or returned as requested;
- assets were localized, or missing assets were reported;
- each output file got screenshot context or a stated screenshot failure;
- each output file completed Phase A and Phase B cleanup following `references/cleanup.md`;
- cleanup audit reports found / removed or replaced / retained counts for temporary URLs, Pixso node-style `id` values, and Pixso node-style classes;
- no inferred state / modifier classes were introduced;
- no unintended redesign, broad refactor, or new dependency was introduced.
