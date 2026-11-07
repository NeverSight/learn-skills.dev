---
name: code-reviewing
description: Reviews code changes for bugs, structural problems, performance issues, and unintended behavior. Use when reviewing uncommitted changes, commits, branches, or pull requests.
---

When doing a code review, follow these rules.

Note this document uses keywords from RFC 2119 (MUST, MUST NOT, SHOULD, SHOULD NOT, etc.).

## Process

### 1. Preparation

- You MUST read applicable `AGENTS.md` files and linked review instructions.
- You MUST follow the repository's instructions for fetching the specifications; e.g., rules for fetching external resources that may require authentication.

### 2. Determine what to review

Choose the review scope from the user's request:

1. **No target**: The staged and unstaged diffs, plus untracked files and their contents.
2. **Commit**: The commit metadata and patch.
3. **Branch or base ref**: The merge-base, commits since that base, and the branch diff. If the branch is already merged, its historical base and head from pull-request metadata.
4. **Pull request URL or number**: The pull-request context, base and head commits, commit list, and historical diff. For a merged pull request, include its historical iteration or merge metadata. Treat a bare number as a pull request only when the request or repository provider makes this clear.

If the requested target or provider metadata is unavailable, report that instead of choosing a different review scope.

### 3. Identify the specification sources

Specification review is essential to assessing correctness.

- You MUST follow the repository's specification-discovery instructions.
- You MUST discover and read all applicable specifications. Do not stop at the first source.
- You MUST follow relevant links to requirements, acceptance criteria, and design specifications.

If the repository does not prescribe a discovery process, search all of these sources in order:

1. A path, URL, issue or work-item ID, or requirements text supplied by the user.
2. Specifications and work items linked from the pull request, including its description and discussion.
3. Issue references in commit messages, using the repository's configured issue-tracker workflow.
4. Repository-local specifications and requirements documentation relevant to the changed code.

If repository-directed discovery is blocked by unavailable tools, missing permissions, inaccessible sources, or unresolved required references:

1. Explain the blocker.
2. You MUST ask the user whether an incomplete specification review is acceptable.
3. You MUST stop and await for explicit approval before proceeding; MUST NOT use a fallback.

If specifications are unavailable or discovery is blocked:

- You MUST report it to the user, stop and await further instructions; MUST NOT use a fallback.

### 4. Identify the standards sources

- You MUST search for anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.
- You MUST include applicable `AGENTS.md` files and the conventions files found while gathering context.
- You SHOULD read [the smell baseline](references/coding-standards.md), but repository-specific standards take precedence.

### 5. Start the review

The review will look at two separate axes that are considered independently:
1. Spec
2. Standards

#### 5.1. Delegation to sub-agents

How to delegate:
- If the user asks for parallelism per axis, then start 2 sub-agents in parallel with fresh context, one for each axis.
- If the user asks just for fresh context, without parallelism per axis, then start a single sub-agent with fresh context to handle both axes sequentially.
- Otherwise do not delegate and proceed with the review yourself.

Any sub-agent responsible for the "Spec" review MUST receive:
- The resolved scope of the review (e.g., `git diff <base>...HEAD`)
- Full specifications, already gathered during discovery at step 3; this includes any local files, included collected ones.

Any sub-agent responsible for the "Standards" review MUST receive:
- The resolved scope of the review (e.g., `git diff <base>...HEAD`)
- References to this repo's coding standards and conventions, discovered during step 4.

#### 5.2. The "Spec" review

Look for the following categories of issues:

* Spec compliance
  - You MUST review the changes against all applicable specifications read during discovery.
  - Flag missing or incorrectly implemented requirements.
  - Cite the relevant requirement for each finding.
* Bugs
  - Logic errors, off-by-one mistakes, incorrect conditionals
  - If-else guards: missing guards, incorrect branching, unreachable code paths
  - Edge cases: null/empty/undefined inputs, error conditions, race conditions
  - Security issues: injection, auth bypass, data exposure
  - Broken error handling that swallows failures, throws unexpectedly or returns error types that are not caught.
* Performance - Only flag if obviously problematic.
  - O(n²) on unbounded data, N+1 queries, blocking I/O on hot paths
* Behavior Changes
  - If a behavioral change is introduced, raise it if it's not in the specification.

**Be certain.** If you're going to call something a bug, you need to be confident it actually is one.

- Only review the changes - do not review pre-existing code that wasn't modified
- Don't flag something as a bug if you're unsure - investigate first
- Don't invent hypothetical problems - if an edge case matters, explain the realistic scenario where it breaks
- If you need more context to be sure, then gather it.

#### 5.3. The "Standards" review

Rules:

- You MUST review the code against the discovered repository standards and the supplied smell baseline.
- You MUST report documented-standard violations with the standard's file and rule.
- You MUST name the smell and quote the relevant hunk for baseline smells.
- You SHOULD not be a zealot about style:
  - Verify the code is _actually_ in violation.
  - Some "violations" are acceptable when they're the simplest option.
  - Don't flag personal style preferences. Report established-project-convention violations or baseline smell judgments.

### 6. Report findings

General template:

```
## Standards

...

## Spec

...

## Spec sources

...
```

#### 6.1. Aggregation

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings, because the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

#### 6.2. Classification

Use `Critical`, `High`, `Medium`, or `Low` severity, based on your judgment and applicable repository documentation. Assess severity, not whether the PR should merge or a finding should block it.

#### 6.3. Bug reporting guidelines

1. If there is a bug, be direct and clear about why it is a bug.
2. Clearly communicate severity of issues. Do not overstate severity.
3. Critiques should clearly and explicitly communicate the scenarios, environments, or inputs that are necessary for the bug to arise. The comment should immediately indicate that the issue's severity depends on these factors.
4. Your tone should be matter-of-fact and not accusatory or overly positive. It should read as a helpful AI assistant suggestion without sounding too much like a human reviewer.
5. Write so the reader can quickly understand the issue without reading too closely.
6. AVOID flattery, do not give any comments that are not helpful to the reader. Avoid phrasing like "Great job ...", "Thanks for ...".
7. Cite the affected file and line for each finding.

#### 6.4. How to report findings

Use a numbered level-three heading for each finding, containing its severity in square brackets and a short, specific title. Follow it with a **Location:** field containing the file and line range, then explain the finding and its impact. Coding standards findings also include a **Standard:** field citing the rule's file and lines when available. For unwritten conventions or structural concerns, identify the established pattern or explain the concern instead of inventing a standards citation.

#### 6.5. Reporting reviewed specifications

Append `## Spec sources` to every report, even when there are no findings:

- You MUST list every specification reference or URL discovered, not just those cited by findings.
- Include all specifications read. Preserve exact URLs, repository paths, and issue or work-item IDs.
- Identify the origin of user-supplied requirements that have no reference.
- Mark each source as read or unread.
- State discovery limitations, blockers, and any user approval to proceed.
- If no specifications were found, say so.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
