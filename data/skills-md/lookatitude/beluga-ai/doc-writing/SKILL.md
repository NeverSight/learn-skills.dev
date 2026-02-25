---
name: doc-writing
description: Documentation writing patterns for Beluga AI v2. Use when creating package docs, tutorials, API guides, or teaching-oriented content.
---

# Documentation Patterns

## Package Doc Structure

1. **Header**: One paragraph — what it does, who uses it, why.
2. **Quick Start**: Minimal working example (3-10 lines), full imports, compiles.
3. **Core Interface**: Go interface definition.
4. **Usage Examples**: Basic, with middleware, with hooks, custom implementation.
5. **Configuration**: All `WithX()` options with defaults.
6. **Extension Guide**: Implement interface → register via init() → map errors → write tests.

## Rules

- Every concept needs a code example.
- Examples must compile with full import paths (`github.com/lookatitude/beluga-ai/...`).
- Handle errors explicitly — never `_` for error returns.
- No marketing language, filler words, or emojis.
- Professional, active voice, present tense, imperative for instructions.
- Cross-reference related packages and `docs/`.
- Use mermaid diagrams sparingly (< 15 nodes).
- Tutorials: progressive complexity (basic 5min, intermediate 10min, advanced 15min).

## Don'ts

- No phase references or timeline language.
- Don't duplicate architecture docs — link to them.
- Don't list every provider — point to `docs/providers.md`.
- Don't show incomplete examples that won't compile.
