---
name: analyze-codebase-for-improvements
description: "Analyze a codebase or project to identify actionable improvements, architectural enhancements, and optimization opportunities. Use this skill when the user asks to review code quality, suggest improvements, identify bottlenecks, audit a system, or get recommendations for enhancing a project. Generates a prioritized list of improvements with problem statements, solutions, and impact analysis."
---

# Analyze Codebase for Improvements

## Input Parameters

| Parameter      | Required | Description                                                                                               | Example                                    |
| -------------- | -------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `project_path` | Yes      | Path to the root directory of the project or codebase to analyze                                         | ~/Code/GitHub/phpbot                       |
| `focus_areas`  | No       | Comma-separated list of specific areas to prioritize                                                      | performance, error-handling, documentation |
| `project_type` | No       | Type of project for context-aware recommendations                                                         | PHP application                            |

## Procedure

1. Confirm the project path, scope, and priority areas with the user if not provided
2. Examine directory layout, file counts, and key components:

   ```bash
   ls -la {{PROJECT_PATH}}
   find {{PROJECT_PATH}}/src -name "*.{{EXTENSION}}" | wc -l
   grep -r "TODO\|FIXME\|HACK" {{PROJECT_PATH}}/src 2>/dev/null | head -20
   ```

3. Review README, configuration files, and recent changes to identify architectural pain points
4. Generate 8–12 actionable improvements organized by impact and effort — each with a problem statement, proposed solution, and expected benefit
5. Rank by value-to-effort ratio; surface quick wins first, then strategic long-term enhancements
6. Deliver as structured markdown with code examples and implementation steps where relevant

## Notes

- Each improvement must have a clear problem statement to justify the recommendation
- Consider the project's current maturity level and team capacity when scoping changes

## Example

```
what are 10 things I could do to improve this codebase
audit this project and suggest architectural improvements
identify technical debt and quick wins in this repo
review code quality and suggest optimizations
what are the biggest bottlenecks in this codebase
```
