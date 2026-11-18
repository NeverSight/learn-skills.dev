---
name: refactor-safe
description: Use when user asks for safe refactoring suggestions, refactor opportunities, or cleanup ideas. Analyzes codebase patterns (duplicate blocks, long functions, magic values, unused code, simple type improvements) and proposes low-risk refactors grouped by safety level. Does not execute changes — suggests only.
allowed-tools: [Bash, Read, Grep, Glob]
---

Execute the following steps:
1. Check if current directory is a valid project (package.json, requirements.txt, etc.)
2. Analyze code patterns and identify safe refactoring opportunities:
   - Duplicate code blocks that can be extracted into functions
   - Long functions that can be broken down
   - Magic numbers/strings that should be constants
   - Unused imports or variables
   - Simple type improvements (TypeScript/Python)
   - Dead code that can be removed safely

3. Prioritize suggestions by safety level:
   - **Safe**: No behavior change (extract constants, remove unused code)
   - **Low Risk**: Mechanical refactoring (extract functions, rename variables)
   - **Medium Risk**: Structural changes that need testing

4. For each suggestion provide:
   - Location (file:line)
   - What to refactor
   - Why it's safe
   - Estimated effort (small/medium/large)

Safety criteria:
- Only suggest refactoring for code patterns, not business logic changes
- Prioritize mechanical transformations over subjective improvements
- Flag any suggestions that require tests to verify safety
- Exclude files that look like generated code or vendor libraries
- Focus on maintainability improvements with clear benefits

Output format:
- Group suggestions by safety level
- Show file locations with line numbers
- Provide brief rationale for each suggestion
- Include rough effort estimates
- Limit to top 10 most impactful suggestions
