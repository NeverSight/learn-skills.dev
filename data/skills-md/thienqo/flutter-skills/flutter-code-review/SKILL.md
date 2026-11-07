---
name: flutter-code-review
description: Review Flutter and Dart diffs, commits, pull requests, focused code scopes, or completed implementations for concrete defects and regression risks. Use for an explicit change review or bounded delivery review; report evidence without edits. Not for broad threat audits, performance diagnosis, or test authoring.
---

# Flutter Code Review

Find defects and implementation residue that materially affect behavior, users, delivery, or maintainability. A review is an evidence-backed risk assessment, not a style tour or an implicit rewrite.

## Establish the review boundary

1. Determine the requested diff, commit range, pull request, working tree, completed implementation, or module and the intended behavior.
2. Read repository instructions and inspect enough nearby code, tests, generated boundaries, and configuration to understand changed behavior.
3. Review changed lines first, but follow their data flow and lifecycle when evidence requires surrounding context.
4. For a standalone review, do not edit files, post comments, approve, merge, or expand into remediation unless the user authorizes those actions. Within an authorized implementation workflow, return findings to that workflow so it can fix only issues inside the original scope.

## Review by risk

Prioritize data loss, security exposure, crashes, incorrect results, broken lifecycle, concurrency races, inaccessible flows, release failures, missing regression coverage, weakened quality gates, and residue introduced by the change. Then consider architecture or maintainability issues that have a concrete cost.

Do not report preferences, hypothetical rewrites, unchanged legacy issues, or framework behavior that current code already handles. Validate API and package claims against the project's SDK and resolved dependencies, using Dart and Flutter MCP semantic lookup and analysis when available; otherwise inspect source and resolved package versions directly.

Treat compatibility and safety claims as proof obligations. Compare changed inputs, outputs, defaults, schemas, exit behavior, and supported callers with the base revision; accepting an old input alone does not prove backward compatibility. For redaction, escaping, validation, or other security-sensitive transforms, test ordering and boundary conditions instead of trusting the happy-path example.

## Load references conditionally

- Read [review workflow](references/review-workflow.md) for gathering the change, tracing impact, calibrating severity, and formatting findings.
- Read [Flutter review checklist](references/flutter-review-checklist.md) only for the technical domains touched by the change.

Load available specialists only when their domain is materially changed or a claim needs deeper verification. A review touching storage does not automatically require every quality skill.

## Output

Lead with findings ordered by severity. Each finding must name the affected file and tight line range, explain the failure path and impact, and propose a proportionate correction. Keep separate sections for open questions and a short summary only when useful.

Before responding, challenge and deduplicate the candidate findings. Drop any claim defeated by a guard, ownership rule, version constraint, test, or framework guarantee. Anchor a finding to the smallest changed range that introduced or exposes it; cite unchanged code only as supporting evidence.

If there are no actionable findings, say so directly and identify meaningful verification gaps. Never invent findings to make the review appear thorough.

When reviewing a completed implementation, finish with a bounded outcome: material findings to resolve before completion, external or out-of-scope items to report, and the focused checks that must be rerun after corrections.

## Sources

- [Flutter testing](https://docs.flutter.dev/testing)
- [Flutter performance](https://docs.flutter.dev/perf)
- [Flutter architecture](https://docs.flutter.dev/app-architecture)
- [Effective Dart](https://dart.dev/effective-dart)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
