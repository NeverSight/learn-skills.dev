---
name: tk-pr-image
description: "[user/auto] 기존 GitHub PR body 또는 지정된 comment에 local evidence image를 업로드합니다. 명시적 이미지 요청이나 정확한 evidence handoff에만 사용합니다."
disable-model-invocation: false
argument-hint: "<PR and local image path(s)>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# GitHub PR Image Upload

Handle explicit local-image evidence requests for an existing GitHub PR or an exact
`tk-pr-open` generic manifest handoff with `evidence_required: true`. Only the parent handoff is an
automatic trigger.

## Scope

Handle one bounded upload: validate and stage local images, upload
repository-scoped GitHub attachments, minimally update the PR body or selected
comment, and verify source/render output. The default target is the PR body.

For `tk-pr-open`, validate the producer-neutral evidence fields and never branch on, whitelist, or require a producing
skill name. If required evidence is missing or invalid, mark the evidence handoff `Blocked`; do not revert an
already-created `tk-pr-open` PR.

Use [references/gh-attach.md](references/gh-attach.md) to classify and run the
extension route. Read [references/cdp-fallback.md](references/cdp-fallback.md)
only after CDP is selected or the extension route cannot use target write
capability. Invoke `tk-wizard` only for an exact human-only host setup,
authentication, permission, or restart step; preserve this skill's upload target and route
across the handoff. Use `tk-browser-verify` for browser-controlled runtime verification.

## 🔴 CHECKPOINT · 🛑 STOP · Upload mutation boundary

Before any upload or PR body/comment update, reverify the explicitly selected target, valid local evidence or producer handoff, authenticated route, and requested write scope; stop as `Blocked` or `Unverifiable` when those preconditions cannot be established.

## Workflow

1. Confirm `origin`, the current PR, and the executing repository from regular
   local image file(s) or a valid producer evidence handoff. Read the existing PR
   body.
2. Reuse the existing `## 스크린샷` heading. If absent, insert it before the AI
   footer or append it at the end. Preserve unrelated body content. For manifest artifacts, use the supplied criterion,
   role, exact `display_route`, state/region, viewport, and comparison in the caption; never derive them from a filename,
   OCR, raw URL, or producer identity. Keep `visual-preservation` baseline and after visibly labeled as one pair.
3. Select and execute an eligible route using
   [gh-attach](references/gh-attach.md), or read
   [CDP fallback](references/cdp-fallback.md) only after CDP is selected.
   Repository visibility is not a routing signal, and a route that may have created
   remote state cannot silently fall back to the other route.
4. When the selected route needs a human-only host action, pass a bounded handoff to
   `tk-wizard` and perform no upload until its completion signal. Agent-approved reviewed
   extension installation remains here. Resume the exact repository, target, image set, and
   route after the wizard completes.
5. Update only the requested body or comment through the GitHub API or equivalent.
   Before `Pass`, verify the source Markdown, every asset's image bytes and actual browser-session rendering, and the
   upload ref. An image element in API-rendered HTML alone is insufficient.
6. Remove only owned staging files on every exit path.

## Execution Receipt · Single Evidence Record

Record every upload attempt in the single receipt below. It is not a separate lifecycle
output; it is the sole evidence record used for the `## GitHub image upload` result and
approval/verification decisions. Use `none` or `unavailable` for absent values; never guess.

```text
Repository: <owner>/<repo>
PR / Target: <pr-number> / body | existing comment <comment-id>
Source images: <absolute path list>
Route: gh-attach | CDP
Entry: <exact reviewed command | browser route>
Generated Markdown: <asset refs | none>
Remote ref: <refs/uploads/issues/<pr-number> | none | unknown>
Verification: <source body/comment | rendered HTML/page | unavailable>
Changed: <body/comment changed | unchanged | unknown>
Cleanup: <owned staging path removed | failed | not applicable>
Status: Pass | Fail | Pending | Blocked | Unverifiable
```

## Evidence Manifest Handoff

When `evidence_required: true`, require all of the following:

- `verification_status: Pass`, a non-empty criterion, evidence kind, comparison result, and limitations.
- Every artifact has a role, non-empty image, absolute path, run-owned evidence directory, state/region, and viewport.
- Every image is marked `inspected: true` and has an exact origin-free `display_route` or an explicit safe omission
  limitation. Never reconstruct or mask a missing route.
- `visual-preservation` contains both a baseline and after artifact from its verified pair.

Reject arbitrary screenshots, missing paths, non-`Pass` results, uninspected artifacts, incomplete preservation pairs,
and artifacts not tied to the current run. If required evidence is missing or invalid, return `Blocked` before upload.

## Prohibitions

- Do not create or merge a PR, change reviewers, publish a release, or insert a
  comment unless the user explicitly selected that comment target.
- Do not bypass `tk-browser-verify` or use Orca or screen control as an automatic
  browser fallback.
- Do not overwrite a pre-existing draft or click comment, close-with-comment, or
  any other submit button.
- Do not choose a route based on public/private visibility or claim success from
  only a placeholder, Markdown presence, fixed delay, or unrendered API response.
- Do not log or return a signed URL, JWT, or raw secret-bearing query string. This does not prohibit a verified-safe,
  origin-free `display_route`; preserve its pathname, query, and fragment exactly as supplied by the manifest.
- Redact only secret-bearing values (signed parameters, JWTs, tokens) in displayed output; preserve rendering parameters
  such as `raw=true`. Keep the extension's generated Markdown privately for the authorized body/comment mutation and
  insert it verbatim, with captions outside that block; never rebuild links from redacted or summarized output. Do not
  copy secret-bearing originals into logs, receipts, or evidence artifacts.

## Failure Handling

Return `Pending` while waiting for an absent-extension or unreviewed-upstream choice or a
human-only `tk-wizard` completion signal. Return `Blocked` for `unknown` provenance, a draft, or a rejected
installation without a selected CDP route. Return `Unverifiable` if neither route
has authentication or render evidence, and `Fail` for upload, remote ref
verification, or cleanup errors. State whether the selected body/comment changed
and whether an upload ref may remain.

For `tk-pr-open`, preserve the separate PR operation result and return the
evidence state as `uploaded` or `blocked`. While required evidence remains
blocked, the parent cannot claim full completion.

## Result

Start the terminal response with `## GitHub image upload`. Include `## Uploaded`,
`## Verification`, and `## Cleanup` when applicable. End the result-owning section with exactly
one `Status: Pass|Fail|Pending|Blocked|Unverifiable` line. Expose asset URLs only when safe and
redact signed parameters.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Create artifacts only when this skill's task authorizes them. Before any artifact write, temporary checkout/transport, or ignore setup, read [artifact paths](references/artifact-paths.md) and apply its Git exclusion, safe-path, and ownership checks. Default repository-owned output to `.tigerkit/`; honor explicit final destinations. Conversation-only work skips this reference and performs no file or ignore setup. Artifact handling grants no unrelated mutation or publication authority.

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering such as `(1) Item` or `1. Item`, with a space after the marker, in generated headings, lists, choices, tables, diagrams, and summaries. Use `- Item` for unordered items. Do not generate Unicode circled/enclosed numbers, single-character parenthesized numbers, or keycap emoji as item markers; they can overlap adjacent text in terminal renderers. Preserve exact code, commands, URLs, quotations, identifiers, and verified UI labels unless explicitly authorized to edit them; apply this rule to the surrounding explanation instead.

For an authorized user-editable temporary input file, consistently provide a plain JSON object template with the needed keys and empty strings for missing text values, rather than an empty or raw-text file. The initial template's non-zero size is not an input-completion signal. Apply the owning package's Artifact Paths input branch before creation and consumption; this notation rule grants no artifact-writing authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Before sending any user-owned clarification, choice, or approval, read [question rounds](references/questions.md) in this turn. Ask the whole answerable frontier in one plain-chat round; resolve facts first, preserve existing authorization, and skip question ceremony when no decision remains. Do not use question tools for ordinary TigerKit questions.

Minimum shape, even when already familiar:

```text
❓ **Q1 · <short title>**: <question and relevant choices>

➡️ <recommendation and reason, when supported>
```

Separate questions with `---`. Put context before the question block and make it the final substantive block: no plan, promise, or “answer and I will proceed” line afterward, except one short reply-format hint. An approval request is its own numbered `Q`, never buried in the proposal. Defer approval whose scope still depends on an unresolved answer.
<!-- /tigerkit:questions -->
