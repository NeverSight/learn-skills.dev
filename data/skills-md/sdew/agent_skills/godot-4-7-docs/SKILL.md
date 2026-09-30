---
name: godot-4-7-docs
description: Use the bundled official Godot Engine 4.7 Markdown documentation to write, modify, review, explain, or troubleshoot Godot projects and code; look up Godot classes, APIs, settings, signals, lifecycle behavior, and errors; and answer explicit local Godot documentation questions with bounded source evidence. Default code examples to C#. Do not use for general C# work unrelated to Godot.
metadata:
  note: Used the document extracted by "小爱孤辰"@Bilibili
---

# Godot 4.7 Docs

## Corpus location

- Resolve the directory containing this loaded `SKILL.md`, then use its `references` child. Never assume the current working directory is the Skill directory or embed a machine-specific absolute path.
- Treat filesystem enumeration as the authoritative catalog. Use `references/README.md` only as an optional query target; never load it in full as a catalog.

## Preflight

1. Inspect relevant project files before documentation retrieval. Preserve the project's language, organization, naming, and style.
2. Verify that `references` exists, `rg` is executable, and `rg --files references --glob '*.md'` enumerates at least one Markdown file.
3. On failure, print and log the problem, stop local retrieval, and neither search a repository-root fallback nor access the network.
4. Default to C# unless the user or project explicitly establishes another language. Use Godot C# PascalCase APIs.
5. Warn only when explicit evidence identifies a project version other than 4.7. Accept a user statement, project documentation, CI configuration, an available Godot command result, or unambiguous project metadata as evidence. Never interpret `config_version=5` as Godot 5. When no explicit version evidence exists, silently use this corpus. Do not run or install Godot solely to detect its version.

## Choose a retrieval branch

Select exactly one initial branch per task, then use the shared bounded protocol:

- **API lookup:** Start with class references. Identify the class document, then locate the exact member or structural section.
- **Conceptual guidance:** Start with getting-started and tutorial material. Narrow by topic and language.
- **Exact-error diagnosis:** Search the exact error first, then stable fragments, involved classes or members, and finally the narrowest relevant subsystem. Retrieve both the failing method and any value type whose semantics are essential to the error, such as a path type in a lookup failure. If the exact error is absent, label the diagnosis as inference.
- **Code authoring:** Inspect the project and identify the Godot classes, methods, and properties involved. Before answering, retrieve their `Method Descriptions` or `Property Descriptions` evidence plus one target-language usage example that directly performs the requested operation. A class description or summary table is insufficient. If the class reference contains that example, use its demonstrated API sequence and stop searching for alternative APIs. If it does not, search narrowed relevant tutorials for the example. Do not replace a matching example's longer sequence with an unillustrated convenience API unless project requirements or documented behavior require the alternative. Never mechanically rename a GDScript example and present it as verified C# usage.

Search both C# PascalCase and Godot snake_case API forms where applicable.

## Bounded retrieval

1. Extract class names, API names, stable error fragments, and topic terms before searching.
2. Search titles and filesystem paths before bodies. Naturally narrow to at most 8 unique candidate files. Never use an arbitrary first-8 truncation as relevance ranking; add semantic terms or directory constraints when more than 8 match.
3. Search the narrowed files first. If evidence is insufficient, expand within the same documentation subtree, then across the complete corpus.
4. Use at most 3 body-search rounds across the entire task. Count each scope level as a round; preflight, path enumeration, and title lookup do not count. Combining or splitting equivalent queries does not change the allowance.
5. Start body retrieval with `-C 6 --max-count 5`. If context is incomplete, choose one unique anchor and expand no farther than `-B 4 -A 30`.
6. Treat an anchor and its bounded context as one excerpt. Use at most 3 evidence excerpts and never exceed 12,000 cumulative characters of documentation body output per task. Candidate paths, titles, and line numbers remain bounded by the candidate cap but do not count toward the body budget.
7. Stop as soon as evidence is sufficient. Near the body limit, stop and state what critical evidence remains missing.

Treat evidence as sufficient when:

- A class reference supplies the relevant API signature or authoritative behavior.
- Code authoring has the relevant `Method Descriptions` and `Property Descriptions` evidence plus one directly matching target-language usage example. Do not count a class overview or summary table as sufficient behavior evidence, and do not answer before collecting the example.
- A tutorial section directly discusses the requested concept.
- Related API or tutorial evidence supports a troubleshooting cause or repair; label it inference when the exact error is absent.

Resolve source conflicts by authority: class references govern API existence, signatures, parameters, returns, and documented behavior; dedicated tutorials govern workflows and composition; introductory examples are illustrations; project files establish the project's actual configuration and version but not 4.7 API behavior. Report unexplained conflicts as possible version or snapshot discrepancies. Never merge incompatible claims.

When the user asks why an optional parameter should be enabled or disabled, retrieve its method-description behavior and cost or side effects; do not infer the answer from its signature or default value alone.

## Navigation

- Locate a known generated basename exactly. When its number is unknown, search semantic filename suffixes, parent directories, and H1 titles; never guess a generated number.
- Disambiguate duplicate titles using parent-directory meaning, user intent, and targeted body terms. Prefer class references for APIs and tutorials for concepts and examples. Retain multiple genuinely useful candidates only within the global limits and explain their roles.
- Treat relative HTML links as hints: remove query parameters, fragments, and `.html`; retain directory meaning; search the page name or visible link text. Treat `index.html` as a landing-page hint.
- Treat official Godot URLs as versioned hints. Extract the version, path, page, class, and member when available. Never assume `3.6`, `4.0`, `stable`, or `latest` equals this 4.7 snapshot. Do not map non-Godot URLs into the corpus.
- Follow a necessary plain-text cross-reference at most one hop. Do not recursively traverse optional “See also” references.
- Skip each complete Markdown image line, including its target and alternative text. Do not test image existence, warn, download, or infer unseen content.
- For unresolved navigation, try one path-derived lookup and one semantic-text lookup, then stop. Ignore an unresolved optional target; report a required missing target and follow the network policy.

## Answer contract

- Complete the requested coding, explanation, review, or troubleshooting task first.
- Preserve project style. For code, use simple explicit checks for common invalid states such as missing nodes, null resources, and invalid paths. Add clear comments for key variables, parameters, returns, loops, branches, and exception handling. Avoid unrelated abstractions, frameworks, or complex tests.
- On a confirmed version mismatch, warn on the first related answer and again when an API may have changed, while clearly limiting claims to 4.7 evidence.
- State direct documentation claims normally. Label conclusions combined from sources as inference. If an exact error is absent, explicitly say the diagnosis is inferred from related API documentation.
- When local documentation materially supports the answer, append at most 3 concise sources and cite every material source actually used. Give each complete Skill-relative path and section. Add line numbers only when retrieval produced reliable line numbers. Omit unsupported claims rather than using an uncited fourth source. Do not fabricate citations, quote long passages, or retrieve extra content solely for citation.

## Failure handling

- Treat non-empty `rg` output as a match even if an early-closing downstream display cap leaves exit code 1.
- Treat empty output with exit code 1 as a normal miss and proceed to the next bounded query; do not log it as an error.
- Treat exit codes greater than 1, invalid regular expressions, path or permission failures, missing dependencies, and failed preflight checks as runtime problems. Never treat stderr as documentation evidence.
- After at most 3 local body-search rounds, state the missing critical evidence. If the user already authorized network access for this task, query only official Godot documentation or repositories. Otherwise request permission before any lookup. Separate online and bundled sources and warn when the online version is not explicitly 4.7. If permission is declined, stop at the locally supported conclusion rather than presenting prior knowledge as certain.

## Runtime logging

- Print every runtime warning, error, and exception to the console and append it to the current project's `.scratch/godot-4-7-docs/runtime.log`.
- Log the time, failure stage, sanitized command summary, exit code, stderr, and stop or correction action.
- If the log directory cannot be created, print both the original problem and the log-write failure, then stop without recursively logging the logging failure.
