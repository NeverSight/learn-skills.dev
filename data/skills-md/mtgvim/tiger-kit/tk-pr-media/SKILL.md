---
name: tk-pr-media
description: "[user/auto] 기존 GitHub PR 본문 또는 지정된 댓글에 로컬 이미지·GIF·MP4를 첨부합니다. 명시적 미디어 요청이나 정확한 근거 인계에만 사용합니다."
disable-model-invocation: false
argument-hint: "<PR and local media path(s)>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# GitHub PR Media Upload

Handle explicit local image/video evidence requests for an existing GitHub PR or an exact
`tk-pr-open` generic manifest handoff with `evidence_required: true`. Only the parent handoff is an
automatic trigger.

## Optional motion supplements

For a selected MP4, read [native video attachments](references/video-upload.md); it owns the distinct upload/byte/player checks instead of the image-only extension steps. A valid optional supplement carries media type, run-owned path, criteria/head, duration/viewport, inspected frames and sampling warnings; never require it to impersonate the required image manifest. Upload it only when `publication_selected: true` or the user explicitly selected that exact artifact/target.

For selected GIF frame assembly, use the reviewed extension with `--gif`, an explicit `.gif` name and delay matching the frame sequence. Capture stderr separately without `--json` at v0.7.0. Preserve all frame-cap/reduction/oversize warnings, verify actual image/gif bytes and multiple decoded frames, and inspect animation when claiming playback. The 5MiB target is not a hard limit; disclose oversize and altered timing. Existing required screenshot pairs remain unchanged.

## Scope

Handle one bounded upload: validate and stage local images, upload
repository-scoped GitHub attachments, minimally update the PR body or selected
comment, and verify the source Markdown and uploaded image objects. The default target is the PR body.

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
   For every pair, with or without a manifest, add a title naming the verified route/screen,
   one expected-behavior sentence, role headers such as `수정 전` / `수정 후`, one image row,
   and a caption row beneath describing each image's observation. Carry supplied evidence;
   disclose missing route/screen evidence rather than inventing it. Staging filenames are
   not headers, captions or an adequate description.
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
   Before `Pass`, reread the target and verify every generated image token appears byte-for-byte exactly once,
   the pair roles/captions remain correctly associated, decodable `image/*` bytes from an authenticated fetch for
   every asset, and reachability of every linked upload object from the upload ref. Browser-session rendering is
   optional; report whether it was checked in the receipt without making it a `Pass` prerequisite.
6. Remove only owned staging files on every exit path. Write each deletion with the literal, fully resolved absolute run-owned staging path already recorded in this run; never derive the target from command substitution, a path file read back, or a glob piped through `head` or `tail`. If the exact literal path is unknown, list the candidates and stop instead of deleting.

## Execution Receipt · Single Evidence Record

Record every upload attempt in the single receipt below. It is not a separate lifecycle
output; it is the sole evidence record used for the `## GitHub media upload` result and
approval/verification decisions. Use `none` or `unavailable` for absent values; never guess.

```text
Repository: <owner>/<repo>
PR / Target: <pr-number> / body | existing comment <comment-id>
Source images: <absolute path list>
Route: gh-attach | CDP
Entry: <exact reviewed command | browser route>
Generated Markdown: <asset refs | none>
Remote ref: <refs/uploads/issues/<pr-number> | none | unknown>
Verification: image-token byte match and single occurrence: <Pass | Fail | unavailable>; image bytes/type: <Pass | Fail | unavailable>; upload ref reachability: <Pass | Fail | unavailable>; rendering: <checked | not performed | unavailable>
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
  such as `raw=true`. Keep each generated image Markdown token byte-for-byte, including its alt,
  URL and rendering parameters; surrounding table layout may be recomposed with captions beneath the images.
  Never rebuild links from redacted or summarized output. Do not
  copy secret-bearing originals into logs, receipts, or evidence artifacts.

## Failure Handling

Return `Pending` while waiting for an absent-extension or unreviewed-upstream choice or a
human-only `tk-wizard` completion signal. Return `Blocked` for `unknown` provenance, a draft, or a rejected
installation without a selected CDP route. Return `Unverifiable` if authentication,
image-byte validation, or upload-ref reachability cannot be verified; rendered-page
evidence is optional. Return `Fail` for upload, remote ref
verification, or cleanup errors. State whether the selected body/comment changed
and whether an upload ref may remain.

For `tk-pr-open`, preserve the separate PR operation result and return the
evidence state as `uploaded` or `blocked`. While required evidence remains
blocked, the parent cannot claim full completion.

## Result

Start the terminal response with `## GitHub media upload`. Include `## Uploaded`,
`## Verification`, and `## Cleanup` when applicable. End the result-owning section with exactly
one `Status: Pass|Fail|Pending|Blocked|Unverifiable` line. Expose asset URLs only when safe and
redact signed parameters.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Artifacts require task authority. Before writes/checkout/transport/ignore setup, read [artifact paths](references/artifact-paths.md) for Git exclusion/path/ownership checks. Reuse identical in-context content; hash-check uncertainty and reread changes/loss; always recheck safety. Use `.tigerkit/` unless a destination is explicit. Chat-only: skip file/ignore setup and this reference. This grants no unrelated mutation/publication authority. Prefer fresh directories and supported trash for authorized non-secret cleanup; target only recorded literal resolved absolute run-owned paths, never `cd` plus glob/relative deletion.

<!-- tigerkit:result-summary -->
## Reader-facing Result Summary

Return a brief result with the outcome, actual verification, material limitations
and direct deliverable links. Distinguish plans/skipped checks from executed work;
retain outstanding manual checks and real cleanup, blocker or human-action details.
Never claim unverified completion or cleanup. Preserve the owner's required artifact,
publication preview, approval boundary, machine return, exact status/footer and final
question block; keep nested returns compact and omit empty sections.
<!-- /tigerkit:result-summary -->

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering (`1. Item`, `(1) Item`) and `- Item`, not enclosed/keycap numerals.
Show complete absolute clickable file paths, including examples, without ellipses.
Preserve exact code, commands, identifiers, URLs, quotations and verified UI labels
unless their edit is authorized.

For chat comparisons with multiple shared attributes, use narrow GFM pipe tables
(about four columns, header, short cells); otherwise use lists. No box-drawing,
fenced or empty tables. Owner-specific previews take precedence; publication bodies
and file artifacts retain their own table formats.

In rendered Markdown prose, use hyphens for ranges and escape literal tildes as `\~`;
preserve exact code, quotations and identifiers.

For authorized temporary input files, follow Artifact Paths before creation and
consumption; a prefilled template is not completed input. This grants no write authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Investigate facts; reuse authorization. For user-owned decisions read
[question rounds](references/questions.md); otherwise proceed.
Plain chat, even one approval: standalone `---`, then
`❓ **Q<n> · <title>**: <question>` and `➡️ <recommendation>` per item.
Ask only settled-prerequisite questions; separate approval.
Questions come last; put status, risks and plans before them.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

For a reusable incident, retain minimal non-secret evidence in the current conversation
and suggest `tk-retro`; do not write it to persistent memory unless the user asks.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
<!-- /tigerkit:skill-feedback -->
