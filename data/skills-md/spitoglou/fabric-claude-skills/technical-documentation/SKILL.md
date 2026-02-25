---
name: technical-documentation
description: Create and improve technical documentation including architecture designs, PRDs, API docs, code explanations, and visual diagrams. Use when asked to document systems, explain codebases, create design documents, write PRDs, generate Mermaid/PlantUML diagrams, review architecture, write user stories, or create pull request descriptions. Triggers include "document this", "create a design doc", "explain this code", "write a PRD", "create a diagram", "architecture overview", "user story for", "PR description".
---

# Technical Documentation

Generate professional technical documentation from specifications, code, or requirements.

## Pattern Selection

| Intent | Pattern | When to Use |
|--------|---------|-------------|
| System architecture | `create_design_document` | New system design, C4 model, security posture |
| Improve existing design | `refine_design_document` | Enhance clarity, fill gaps in design docs |
| Review architecture | `review_design` | Evaluate designs for scalability, security |
| Product requirements | `create_prd` | Feature specs, product planning |
| User stories | `create_user_story` | Agile stories with acceptance criteria |
| Code explanation | `explain_code` | Understand codebases, configs, tool outputs |
| Doc improvement | `explain_docs` | Transform technical docs into clearer versions |
| Visual diagrams | `create_mermaid` | Flowcharts, sequence diagrams, ERDs |
| PR descriptions | `write_pull_request` | Summarize code changes for review |
| Git summaries | `summarize_git_diff` | Explain what changed in commits |

**Decision flow:**
1. **New system/feature?** → `create_design_document` or `create_prd`
2. **Existing design needs work?** → `refine_design_document` or `review_design`
3. **Code to explain?** → `explain_code`
4. **Need visuals?** → `create_mermaid`
5. **Agile artifacts?** → `create_user_story`
6. **Git/PR work?** → `write_pull_request` or `summarize_git_diff`

## Pattern References

See `references/` for full patterns:
- [create_design_document.md](references/create_design_document.md) - C4 architecture docs
- [create_prd.md](references/create_prd.md) - Product requirements
- [create_user_story.md](references/create_user_story.md) - Agile stories
- [explain_code.md](references/explain_code.md) - Code walkthroughs
- [create_mermaid.md](references/create_mermaid.md) - Diagram generation
- [write_pull_request.md](references/write_pull_request.md) - PR descriptions
- [review_design.md](references/review_design.md) - Architecture review

## Output Guidelines

- Use consistent heading hierarchy (H1 for title, H2 for sections)
- Include diagrams where they add clarity (Mermaid preferred)
- For code: always specify language in fenced blocks
- For designs: address security, scalability, and failure modes
- Keep PRDs focused on what, not how (implementation details in design docs)

## Chaining Patterns

Offer logical follow-ups:
- After `create_prd` → offer `create_design_document` for implementation
- After `create_design_document` → offer `create_mermaid` for diagrams
- After `explain_code` → offer to generate documentation or tests
- After `review_design` → offer `refine_design_document` to address issues
