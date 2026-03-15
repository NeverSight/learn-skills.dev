---
name: find-examples
description: Find and inspect real-world code examples from GitHub for specific dependencies and languages. Use when you need to understand how a library or framework is used in production or community projects.
---

# Find Examples

This skill helps you find credible and recent code examples on GitHub for specific dependencies.

## Workflow

### 1. Search for Repositories (Multi-Language)
Run the `github_search.py` script. If examples in your target language are scarce, include related languages supported by the SDK.

```bash
python3 scripts/github_search.py <dependency> --lang <lang1,lang2> --limit 5
```

**Example (Genkit Go/JS):**
```bash
python3 find-examples/scripts/github_search.py "genkit" --lang "go,typescript"
```

### 2. Prioritize and Select
Review the results. The script tags each repo with its language. 
- **Direct Match**: Prefer the target language if high-quality results exist.
- **Polyglot Translation**: If your language has few results, select a high-credibility repo from a related language (e.g., use a TypeScript Genkit example to inform a Go implementation).

### 3. Create Examples Directory
```bash
mkdir -p _examples
```

### 4. Clone and Inspect
Clone the selected repositories into the `_examples` folder.

```bash
cd _examples && git clone <repo_url>
```

Once cloned, use `list_files`, `smart_read`, or `grep_search` to find relevant implementation details.

## Polyglot Translation Strategy
When using an example from a different language:
1. **Identify the Core API**: Look for the primary classes or functions (e.g., `DefineFlow` in JS usually maps to `DefineFlow` in Go).
2. **Translate Data Structures**: Map objects/interfaces to Go structs or Python classes.
3. **Bridge Patterns**: Observe how authentication, configuration, and error handling are handled; these patterns are often consistent across an SDK's supported languages.

## Tips
- **Credibility**: Look for high star counts and official or well-known organizations.
- **Recency**: Prefer repositories that have been updated in the last 6 months to ensure compatibility with modern versions of the dependency.
- **Context**: If searching for a large framework, use `grep_search` within the cloned repo to find specific symbol usages.
