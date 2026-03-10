---
name: explain
description: |
  Deep, systematic explanation of code, concepts, and system behavior.
  Always operates at advanced level with introspection markers and validation.
  Analyzes target thoroughly before explaining, verifies accuracy after.

  Use when:
  - User asks "what does this do", "how does this work", "explain this"
  - User wants to understand code, architecture, or a concept in depth
  - User points to a file, function, or system and asks for explanation
  - User says "explain", "walk me through", "teach me", "break down"

  Keywords: explain, understand, how, what, why, walk through, teach, break down, clarify
argument-hint: "[target: code/file/concept]"
---

# Explain — Deep Systematic Explanation

Advanced-level explanation with introspection markers, systematic analysis, and accuracy validation.

<essential_principles>

## Always Active

- **Advanced level**: Assume the reader is an experienced developer. No hand-holding.
  Explain the "why" and architectural reasoning, not just the "what"
- **Introspection markers**: Make reasoning visible throughout:
  - 🤔 Reasoning — "🤔 This pattern suggests..."
  - 🎯 Decision — "🎯 The author chose X over Y because..."
  - ⚡ Performance — "⚡ This has O(n²) complexity due to..."
  - 📊 Quality — "📊 This follows/violates the SRP principle"
  - 💡 Insight — "💡 This pattern can be applied to..."
- **Validate before presenting**: Never guess. Read the actual code. Check official docs
  when explaining library/framework behavior. Flag uncertainty explicitly
- **No project-specific rules**: This skill works across all projects and AI agents

</essential_principles>

## Phase 1: Analyze

Thoroughly examine the target before explaining anything.

1. **Identify scope**: Is this a file, function, class, concept, or system?
2. **Read the code**: Use Read, Grep, Glob to gather the actual source
3. **Trace dependencies**: Follow imports, references, and call sites to understand context
4. **Check external APIs**: Use Context7 or WebSearch for library/framework specifics if needed
5. 🤔 Form a mental model of how the target works

**Tools**: Read, Grep, Glob, `mcp__serena__find_symbol`, `mcp__serena__get_symbols_overview`, `mcp__context7__query-docs`

## Phase 2: Structure

Plan the explanation for maximum clarity.

1. Identify the **core insight** — the one thing that unlocks understanding
2. Decide explanation order:
   - **Top-down**: Start with the big picture, zoom into details
   - **Bottom-up**: Start with building blocks, compose into the whole
   - **Flow-based**: Follow data/execution flow from input to output
3. 🎯 Choose the approach that best fits the target

## Phase 3: Explain

Deliver the explanation with depth and clarity.

1. **Open with context**: What is this, and why does it exist?
2. **Core explanation**: How it works, with introspection markers throughout
3. **Key decisions**: Why was it built this way? What alternatives exist?
4. **Connections**: How does it relate to the broader system/pattern?
5. **Code examples**: Reference actual line numbers (`file:line`) when explaining code

### Explanation Format

Use the insight block format for key educational points:

```
`★ Insight ─────────────────────────────────────`
[2-3 key educational points]
`─────────────────────────────────────────────────`
```

## Phase 4: Validate

Verify the explanation is accurate and complete.

1. ✅ Cross-check claims against actual code (re-read if needed)
2. ✅ Verify library/framework behavior against official docs
3. ✅ Flag anything uncertain with "⚠️ Note: ..."
4. ✅ Ensure no oversimplification that would mislead

## Examples

```
/explain src/auth/middleware.ts
/explain "how does React Suspense work"
/explain the hook system in this project
/explain this error message: "Cannot read property of undefined"
```

## Boundaries

**Will:**
- Provide deep, accurate explanations with reasoning made visible
- Read and trace actual code rather than guessing from filenames
- Reference official documentation for framework/library specifics
- Flag uncertainty and knowledge gaps honestly

**Will Not:**
- Provide shallow or beginner-level explanations (use Claude directly for that)
- Guess at behavior without reading the source
- Modify any code (this is a read-only explanation skill)
