---
name: processon-mindmap
license: Apache-2.0
description: Design a ProcessOn-ready mind-map outline for ideas, requirements, knowledge systems, meeting notes, learning plans, or hierarchical analysis. Use when the user explicitly requests a ProcessOn mind map, editable mind map, or a hierarchical outline intended for ProcessOn. Do not trigger for ordinary diagrams, generic prose outlines, or Mermaid mind maps unless ProcessOn is requested.
---

# ProcessOn Mind Maps

Turn source material into a concise hierarchy that can be recreated or imported in ProcessOn.

## Workflow

1. Identify the map's central question and intended reader.
2. Extract major themes and group related facts before naming branches.
3. Limit the first level to roughly five to nine branches unless the source requires more.
4. Keep one idea per node and use parallel wording among sibling nodes.
5. Add priority, status, owner, or relationship markers only when supported by the source.
6. Deliver the structured outline and state any assumptions or omitted low-value detail.

## Structure rules

- Use nouns for concept maps and verb phrases for action plans.
- Keep sibling branches at comparable levels of abstraction.
- Avoid duplicating the same fact under several branches; use a cross-reference marker when needed.
- Put evidence, examples, and implementation detail below the concept they support.
- Split oversized maps into a navigation map plus focused submaps.
- Preserve the user's terminology and language.

## Output format

Default to an indented Markdown outline that is easy to paste or recreate:

```markdown
- 中心主题
  - 一级主题 A
    - 要点 A1
    - 要点 A2
  - 一级主题 B
    - 要点 B1
```

If the user needs a rendered ProcessOn diagram rather than an outline, hand off to the **`processon-diagram-generator`** skill and use its API workflow. Install with: `npx skills add full-stack-skills/document-skills --skill processon-diagram-generator`.

## Quality checks

- The root expresses one clear subject.
- No branch mixes unrelated concerns.
- Sibling depth and wording are consistent.
- The map remains readable without hidden context.
- Unsupported conclusions are marked as assumptions.
