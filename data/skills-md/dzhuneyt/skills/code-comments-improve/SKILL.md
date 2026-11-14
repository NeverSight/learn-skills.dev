---
name: code-comments-improve
description: Use when user asks to improve, add, or clean up code comments, focusing on WHY over WHAT. Reads specified files (or recently modified ones), adds strategic inline comments for non-obvious logic, removes redundant ones, and converts WHAT-comments to WHY-comments. Accepts optional $ARGUMENTS for target files.
allowed-tools: [Read, Edit, MultiEdit, Grep, Glob]
argument-hint: "[file1] [file2] ..."
---

Improve code comments in the specified files (or recently worked on files if none provided):

1. **Analyze the code structure and existing comments**
   - Read specified files or detect recently modified files
   - Identify functions, classes, and complex logic blocks
   - Evaluate existing comments for clarity and usefulness

2. **Add strategic inline comments where beneficial**:
   - Complex business logic that isn't obvious from code alone
   - Non-obvious algorithmic choices or optimizations
   - Important assumptions or constraints
   - Edge cases and their handling
   - Integration points with external systems

3. **Improve existing comments**:
   - Simplify overly verbose or technical jargon
   - Remove redundant comments that just restate the code
   - Fix outdated comments that don't match current implementation
   - Convert WHAT comments to WHY comments when appropriate

4. **Focus on the WHY, not the WHAT**:
   - Explain business reasons and decision rationale
   - Document why this approach was chosen over alternatives
   - Clarify non-obvious requirements or constraints
   - Avoid commenting obvious code with good naming

5. **Comment guidelines**:
   - Keep comments concise and focused
   - Use clear, simple language
   - Ensure comments add value beyond what code conveys
   - Place comments close to relevant code
   - Use consistent comment style for the project

**Output**: Present the improved code with enhanced comments, explaining the reasoning behind each comment addition or change.
