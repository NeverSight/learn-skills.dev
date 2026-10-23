---
name: experience-lwc-widget-migrate
description: "Convert a specific existing Lightning web component (LWC) into a declarative HXL / Agentforce widget, end to end. Gates on experience-lwc-widget-assess and stops when a widget cannot serve the LWC's purpose; otherwise hands the derived field shape to platform-widget-generate and wires the widget as the Lightning Type renderer. TRIGGER when: the user wants to convert, migrate, port, rebuild, or turn a named LWC into a widget or declarative Agentforce widget, or asks for a widget built from an existing LWC component. DO NOT TRIGGER when: the user only wants to know whether an LWC can become a widget (use experience-lwc-widget-assess), or wants a widget for a data shape, entity, or Lightning Type with no existing LWC (use platform-widget-generate or platform-lightning-type-widget-coordinate)."
metadata:
  version: "1.0"
  domains: ["Experience", "Platform", "Agentforce"]
  minApiVersion: "68.0"
  relatedSkills:
    - "experience-lwc-widget-assess"
    - "platform-widget-generate"
    - "platform-custom-lightning-type-generate"
    - "platform-lightning-type-widget-coordinate"
  mcpTools:
    metadata-experts:
      tools: ["execute_metadata_action"]
      semver: ">=1.0.0"
---

# Migrate an LWC to a widget

Use the LWC to recover the **user's goal and data contract**, then build the closest useful widget. A widget is its own declarative artifact. `platform-widget-generate` authors it; a Lightning Type renderer may need separate wiring to make it reachable. This skill owns the comparison, handoff, integration check, and honest final status.

## 1. Decide whether to proceed

Read and apply `experience-lwc-widget-assess` to the component, its action output, and any existing Lightning Type/renderer. Preserve its verdict and the key findings from its report (blockers, contract change, lost interactions) in your report; do not write the assessment's own `verdict.json` or `report.md` files. Stop on `pointless`, `blocked`, `review`, or `needsHumanReview: true`. Proceed on `viable` only when the intended change is explicit:

- For `port-declarative`, preserve the current visible fields and actions.
- For `needs-IA-contract-change`, identify the exact bounded output fields or pre-shaped values required. A widget against a **proposed** contract is a draft until the action returns that contract; do not call it working.
- For `not-portable` with a viable adaptation, describe the replacement UX and each lost interaction. Call it a rebuild, not a faithful port.

## 2. Derive the generator handoff

Trace each value the proposed widget displays to the actual or proposed action output. Before authoring, verify the action contract rather than relying only on an assessment prompt's description. Pass `platform-widget-generate` an ordered field shape (`name`, `type`, `required`), nested/list item fields, the intended tile role of each visible element, and supported terminal actions. Preserve render order and field paths. Use its discovery results for tile definitions and attributes, its documented formula catalog for expressions, and its instructions for schema types and bundle layout; do not maintain a second catalog here. A formula can cover supported scalar/date/regex operations, while collection restructuring may require pre-shaped output.

If an LWC fixture or action example contains sample data, it can help infer the shape; sample data is optional and is **not** a documented generator input or a substitute for the action contract. Do not invent sample fields. For an action such as `sendMessage`, verify that the required context reaches the agent and that the agent has a way to perform the requested work. Do not assume a widget input form can submit collected values without a discovered, validated mechanism.

## 3. Generate and connect

Load `platform-widget-generate` and follow its mandatory live `discoverUiComponents` and `getUiComponentSchemas` calls. If the `metadata-experts` MCP or discovery is unavailable, stop before authoring a bundle; report the completed assessment and proposed field shape. The generator owns its three widget files and self-validation. Do not copy its UEM syntax or validation checklist into this skill.

For an Agentforce renderer migration, also establish the Lightning Type that receives the action output. A bundle alone is not connected to the action:

- **Existing compatible Lightning Type:** inspect its schema and current `renderer.json`. After generation, read `platform-custom-lightning-type-generate/references/widget-rendition.md`, wire the widget with field mappings, and follow `platform-lightning-type-widget-coordinate`'s renderer checks. If the existing renderer points to another widget or LWC, surface the replacement/merge decision before changing it.
- **No compatible Lightning Type:** resolve the action's output class and a Lightning Type name from the project or the user's request. For the coordinator's supported Apex-backed route, use `platform-lightning-type-widget-coordinate` with that type and the assessed output shape; let it own bundle generation and renderer wiring. That coordinator does not cover every type. If the output/type route cannot be established, stop and identify the missing integration step. Do not claim a complete migration.

If the user requested a **bundle only**, report it explicitly as an unconnected bundle. Otherwise, completion requires both the bundle and renderer wiring.

## 4. Check the result

Use the generator's bundle self-validation. Then compare the result to the assessed candidate: every retained visible field has a binding to the real/proposed payload; list item paths and supported actions match; omitted behavior and contract changes are stated; and, for a renderer migration, the Lightning Type points to this widget with matching attributes. Static checks establish structure and mapping, not deployed runtime behavior. Report assessment, created paths, validation results, and one of: `migrated and wired`, `bundle only`, `draft pending IA contract`, or `stopped`, with the reason.
