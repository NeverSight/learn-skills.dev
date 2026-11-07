---
name: c4-structurizr
description: Analyze a codebase and produce seven Structurizr-styled C4-PlantUML diagrams rendered with Java PlantUML.
metadata:
  version: 0.1.0
  license: MIT
  topics: [codex, architecture, c4, plantuml, documentation]
---

# C4 Structurizr

Generate an evidence-backed C4 architecture model for one focal system. Produce seven C4-PlantUML files, render them to SVG, and verify that every rendered diagram is nonblank and traceable to the codebase. Do not use default C4-PlantUML styling.

## Workflow

1. Determine the target project. Use the supplied project path, otherwise infer it from the current repository. If the project or focal system is ambiguous, stop and ask one concise question.
2. Read [references/model-analysis.md](references/model-analysis.md). Inventory people, software systems, containers, components, external systems, stores, queues, processes, deployments, and relationships from code, configuration, manifests, infrastructure files, tests, and existing documentation.
3. If the model, configuration, dependencies, prompts, agents, workflows, runtime executors, model adapters, context stores, or trace stores show an AI workflow, also read [references/ai-workflow-analysis.md](references/ai-workflow-analysis.md) and complete the AI inventory before drawing. If no such evidence exists, do not add AI semantics.
4. Read [references/view-catalog.md](references/view-catalog.md). Choose the seven views, including a domain-specific dynamic flow and critical path. If a view cannot be supported by evidence, stop and report the missing evidence instead of inventing it.
5. Create the diagram workspace. Use `docs/architecture/structurizr/plantuml` in the target project unless the user specifies another location. Copy `assets/c4-style.puml` into that directory and copy `assets/c4-plantuml/` into the sibling `docs/architecture/tools/c4-plantuml` directory. If the target layout is different, keep the include paths valid and tell the user where assets were staged.
6. Generate seven `.puml` files with concise, evidence-backed names. Prefer these canonical names: `system-landscape.puml`, `system-context.puml`, `container.puml`, `component.puml`, `dynamic-flow.puml`, `deployment.puml`, and `critical-path.puml`. A domain-specific suffix is acceptable when it improves clarity; an AI-driven system may use `ai-critical-path.puml` for the model-backed path.
7. Render with:

   ```bash
   python "<skill-directory>/scripts/render_c4.py" --source "<diagram-directory>"
   ```

   Add `--preview` when visual inspection needs PNG previews. Add `--plantuml-jar "<path>"` when the renderer cannot locate `plantuml.jar`.
8. Verify that all seven SVG files exist, are nonblank, use the expected white background and accent colors, and contain legible text. Read previews when layout complexity is high. Check relationships, element types, boundaries, and the critical-path order against the analysis inventory. For an AI system, verify that the runtime boundary, agent/workflow distinction, executor, model gateway, context, and trace path are visually identifiable without reading the PlantUML source.
9. Report the diagram directory, seven diagram names, rendering status, and the code paths that support the main architectural claims. Report unresolved evidence gaps explicitly.

## Diagram source rules

- Start every file with `@startuml <DiagramId>` and end with `@enduml`.
- Include one C4-PlantUML entrypoint first, then `!include c4-style.puml`.
- In the default workspace, use include paths such as `!include ../../tools/c4-plantuml/C4_Context.puml`.
- Make the `@startuml` id match the desired output filename, because PlantUML uses that id for the SVG and PNG file name.
- Use `SHOW_PERSON_OUTLINE()` and `HIDE_STEREOTYPE()` in every view.
- Use `left footer <b>...` for the diagram title. Do not use PlantUML `title`.
- Use `Person`, `System`, `System_Ext`, `Container`, `ContainerDb`, `Container_Ext`, `ContainerDb_Ext`, `Component`, and `Deployment_Node` according to C4 granularity.
- Add `$tags="OfficialRelationship"` to every `Rel` and `RelIndex` relationship.
- Keep people green, internal elements blue, generic external systems gray, boundaries blue and solid, relationships dashed and thick, and the background white. Project-specific semantic accent tags may be appended, but base style values must not be weakened.
- Use the shared AI tags only for evidence-backed elements: `AIWorkflow`, `AIAgent`, `AIExecutor`, `AIContext`, `AITrace`, `AIBoundary`, `AIFlow`, `ModelCall`, `AIContextFlow`, and `AITraceFlow`. Keep AI workflow semantics consistent across views and put the role in the element name or description so the diagram is not color-only.
- Use domain and technology terms from the target project. Do not put 6S-specific entities in a generated diagram for another project.

Do not replace the generated files with a one-off PlantUML style. If C4-PlantUML macros or style behavior differ from the expected result, inspect the staged C4-PlantUML assets and test one diagram before regenerating all seven.
