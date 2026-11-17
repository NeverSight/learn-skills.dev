---
name: technical-blog-doc
license: Apache-2.0
description: Create or revise evidence-backed technical tutorials, integration guides, deployment articles, engineering walkthroughs, and project documentation in Markdown. Use when the user asks for a technical blog post or tutorial that combines concepts, prerequisites, implementation, runnable commands, verification, troubleshooting, and sources. Do not use for a product-documentation suite or API-only reference.
---

# Technical Blog Documentation

Write reproducible technical content whose claims, code, commands, and versions can be traced to evidence.

## Routing

- Product documentation suite or PRD hierarchy: hand off to the **`full-stack-doc`** skill. Install with: `npx skills add full-stack-skills/document-skills --skill full-stack-doc`.
- API-only documentation: hand off to the **`api-doc-generator`** skill. Install with: `npx skills add full-stack-skills/document-skills --skill api-doc-generator`.
- Collaborative proposal/RFC drafting: hand off to the **`doc-coauthoring`** skill. Install with: `npx skills add full-stack-skills/document-skills --skill doc-coauthoring`.

## Evidence model

Classify material before drafting:

| Label | Meaning |
|---|---|
| 官方事实 | Supported by current official documentation or release notes |
| 源码观察 | Confirmed in the inspected repository |
| 运行验证 | Confirmed by an executed command or test in the current environment |
| 推断 | Reasonable interpretation that is not directly verified |
| 待确认 | Missing, conflicting, or unstable information |

Do not present `推断` or `待确认` as verified fact. Browse authoritative sources when versions, APIs, support matrices, or other time-sensitive claims matter.

## Workflow

### 1. Define the reader contract

Identify the target reader, expected starting knowledge, promised outcome, target environment, and artifact location. Inspect the actual repository when the article describes a local implementation.

### 2. Build a verification matrix

Record the facts the article will depend on:

- operating system and architecture;
- language/runtime and package-manager versions;
- framework, SDK, model, or service versions;
- required credentials and external services;
- commands that must run;
- expected output and failure modes;
- sources for benchmarks, limits, and compatibility claims.

### 3. Select a structure

Copy [`assets/technical-blog-template.md`](assets/technical-blog-template.md) when a complete article scaffold is useful. Remove irrelevant sections rather than filling them with generic prose.

Typical structure:

1. Outcome and scope
2. Prerequisites and verified environment
3. Architecture or request flow
4. Step-by-step implementation
5. Configuration and security
6. Run and verify
7. Troubleshooting
8. Limitations and production considerations
9. Verification record and sources

### 4. Write from executable artifacts

- Prefer code and configuration from the current repository over reconstructed snippets.
- Keep snippets minimal but syntactically complete.
- Use placeholders for secrets and redact tokens, personal data, and internal endpoints.
- Explain why a step is needed, not merely what to paste.
- Tie screenshots and diagrams to a concrete explanatory purpose.
- Use Mermaid for Markdown-native flows and PlantUML for precise UML/C4 notation.

### 5. Verify

Run safe commands and tests when authorized. Record actual commands and results. If execution is impossible, say so and provide a precise verification procedure without claiming success.

Add a verification section:

```markdown
## 验证记录

- 验证日期：{YYYY-MM-DD}
- 操作系统：{系统与架构}
- 运行时版本：{版本}
- 框架/SDK 版本：{版本}
- 执行命令：`{命令}`
- 结果：{实际结果}
- 未验证内容：{无/列表}
- 官方资料：{链接列表}
```

### 6. Cold-read the article

Check whether a reader without conversation context can identify prerequisites, distinguish commands from output, reproduce the result, recover from common failures, and verify external claims.

## Quality rules

- Use one H1 and a coherent heading hierarchy.
- Specify the shell/language on every fenced code block.
- Keep version-sensitive claims dated and sourced.
- Do not copy official images unless redistribution is allowed; link or recreate an original explanatory diagram when appropriate.
- Validate relative links and local image references.
- Avoid universal production claims based only on a development example.
- Preserve the user's existing article structure unless a change materially improves comprehension.

## Completion contract

Report the output file, verified commands/tests, source links used, environment tested, and all remaining `推断` or `待确认` items.
