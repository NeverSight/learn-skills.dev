---
name: codebase-packager
description: 'Performs semantic code intelligence and token optimization through context engineering and automated context packing. Use when reducing token overhead for large codebases, creating repository digests with Gitingest, packaging code context with Repomix, or tracing cross-file dependencies with llm-tldr.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# TLDR Expert

## Overview

Achieves high-fidelity codebase comprehension at a fraction of the token cost through semantic layers, structured digests, and advanced context packaging. Combines Repomix for context packing, Gitingest for repository digests, and llm-tldr for graph-based code analysis.

**When to use:** Reducing prompt overhead for large codebases, onboarding to unfamiliar repositories, mapping cross-file dependencies, creating AI-optimized context bundles.

**When NOT to use:** Small single-file tasks, final implementation debugging (read the full file), real-time code editing.

## Quick Reference

| Pattern            | Tool / Command                          | Key Points                                             |
| ------------------ | --------------------------------------- | ------------------------------------------------------ |
| Context packing    | `repomix --include "src/**" --compress` | Package subdirectories into AI-optimized bundles       |
| Signatures only    | `repomix --include "src/**" --compress` | Compression extracts signatures via Tree-sitter        |
| Repository digest  | `gitingest . -o digest.txt`             | Prompt-friendly summary for quick onboarding           |
| Dependency context | `tldr context funcName --project .`     | LLM-ready context for a function with 95% token saving |
| Caller tracing     | `tldr impact functionName .`            | Reverse call graph to assess change blast radius       |
| Forward call graph | `tldr calls .`                          | Build forward call graph across the project            |
| Semantic search    | `tldr semantic "session expiry" .`      | Find logic by meaning when naming is inconsistent      |
| Architecture audit | `tldr arch .`                           | Detect circular deps, layer violations, dead code      |
| Dead code finder   | `tldr dead .`                           | Find unreachable functions with zero callers           |
| File extraction    | `tldr extract src/file.ts`              | Extract AST (functions, classes, imports) from a file  |
| Secret scanning    | Repomix built-in secretlint             | Ensure context bundles contain no keys or PII          |

## Common Mistakes

| Mistake                                                     | Correct Pattern                                                                |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Reading entire large files without checking structure first | Run `tldr extract` to get signatures before reading full files                 |
| Using `grep` for dependency tracing across files            | Use `tldr impact` for reverse call graph that understands dynamic imports      |
| Packing `node_modules` or `dist` into context bundles       | Configure Repomix ignore-list to exclude generated and vendor directories      |
| Assuming semantic search results are exhaustive             | Verify top matches against actual source and cross-reference with `rg`         |
| Running Repomix without compression on large directories    | Use `--compress` flag to stay within context window limits                     |
| Including irrelevant context that dilutes signal quality    | Follow top-down priority: index, signatures, core logic, then adjacent context |

## Delegation

- **Repository structure discovery**: Use `Explore` agent to map directory layout and identify key modules before building context bundles
- **Multi-step context packing workflow**: Use `Task` agent to run Gitingest digest, Repomix compression, and llm-tldr indexing in sequence
- **Architecture analysis and planning**: Use `Plan` agent to design context engineering strategy for large monorepos

## References

- [Context Engineering Patterns](references/context-engineering-patterns.md) -- packing strategies, XML tagging, signal-to-noise optimization, warm-up prompts
- [Repomix and Gitingest Mastery](references/repomix-gitingest-mastery.md) -- configuration, compression mode, digest generation, Tree-sitter extraction
- [Semantic Graph Analysis](references/semantic-graph-analysis.md) -- llm-tldr CLI tools, impact analysis, semantic search, architectural audits
