---
name: tk-blind-comparison
description: "[user/auto] 후보 이름을 가린 블라인드 비교·청취 갤러리를 요청하면 사용합니다. 취향·품질 후보 중 사람이 판단해야 할 때는 실행 전에 갤러리를 제안만 합니다. 단일 변경 QA, 장단점을 공개하는 설계 질문, 자동 지표 비교에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<candidate/item/output manifest or exported ratings>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Blind Comparison

Own human comparison of existing candidates, never candidate generation or an agent's
quality verdict. When a user requests blind comparison, build it. When merely facing
subjective alternatives, propose a blind gallery and wait for acceptance without choosing
or creating files. Single-change checks belong to `tk-qa-sheet`; disclosed tradeoff questions
to `tk-grill`; candidate creation to `tk-prototype`, `tk-tts` or the relevant producer.

1. Confirm the shared comparison question, candidates, items and equivalent source inputs
   from available evidence. Require at least two candidates; preserve failed outputs.
   Read [manifest and commands](references/manifest.md). Keep originals immutable and
   record content revisions: changed outputs need fresh ratings, unchanged outputs retain them.
2. Before writing, apply Artifact Paths. Use `.tigerkit/tmp/tk-blind-comparison/<run-id>/`
   for HTML, display copies and the separate answer key; use
   `.tigerkit/evidence/tk-blind-comparison/<run-id>/` for returned ratings and summaries.
   Honor an explicit destination. Read [HTML output](references/html-output.md) and inline
   the package theme assets. Keep the gallery interface rather than adding document navigation.
3. Prepare identity-neutral display copies. Read only the applicable
   [audio](references/audio.md), [images and UI captures](references/images.md),
   [text](references/text.md), or [video](references/video.md) reference.
   Strip surface identifiers and metadata without erasing the dimension being compared.
   Record transformations and residual cues visibly. A failed normalization remains a
   failed card with a neutral reason; preserve diagnostic details privately in the answer key.
4. Run the bundled builder with the prepared manifest. Reuse the same study ID and previous
   answer key when adding/removing/reordering candidates; create a new output directory.
   Preserve opaque stable candidate IDs, item IDs and content fingerprints. Use seeded
   per-item shuffles and neutral labels disjoint from candidate names. Candidate identity
   must not appear in filenames, DOM IDs, accessibility names, default text or sorting.
   Keep a separate answer key and an explicit reveal toggle; offline blinding prevents casual
   cues, not source inspection. Never claim cryptographic or exam security.
   Keep the comparison topic, item title, shared script and evaluation guide visible within
   the active item's sticky context; bound long context height so scoring stays reachable.
5. Verify the saved local HTML through `tk-browser-verify`: desktop/mobile and both themes,
   media decode, all failure cards, keyboard controls, native 1-5 score selection, notes, optional favorite,
   reload, candidate addition, JSON import/export, rating copy and clipboard refusal,
   partial-reveal confirmation/cancellation, reveal-only averages and storage refusal.
   Copy uses the same blind-key payload as
   export; if clipboard access fails, retain ratings and offer file export.
   The builder embeds media; open via `file://` without hosting. Browser `localStorage` on
   local files varies: show save failures and offer JSON backup/import; file relocation or a
   different browser may require importing the previous export. Report unrun checks honestly.
6. Return the local HTML and answer-key paths, revision/counts, transformations, actual checks
   and remaining human evaluation. Publish only on explicit request. Wait for actual ratings;
   never fabricate scores. Read [results](references/results.md) when copied JSON or a JSON export arrives,
   validate against its matching key, aggregate counts/means and item tables, and state evaluator
   count, missing scores, failures and sample limitations. Compare available objective metrics
   against low-scoring items without treating subjective means as statistical proof.

No servers, shared database, live multi-rater collection, statistical tests, automatic winner,
source changes, model installation or synthesis. Existing audio/video comparisons do not authorize
new TTS; ask about TTS only if the user separately requests new narration and its choice is unresolved.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Artifacts require task authority. Before writes/checkout/transport/ignore setup, read [artifact paths](references/artifact-paths.md) for Git exclusion/path/ownership checks. Reuse identical in-context content; hash-check uncertainty and reread changes/loss; always recheck safety. Use `.tigerkit/` unless a destination is explicit. Chat-only: skip file/ignore setup and this reference. This grants no unrelated mutation/publication authority. Prefer fresh directories and supported trash for authorized non-secret cleanup; target only recorded literal resolved absolute run-owned paths, never `cd` plus glob/relative deletion.

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
