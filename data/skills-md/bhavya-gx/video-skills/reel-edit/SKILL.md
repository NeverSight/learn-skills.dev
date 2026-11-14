---
name: reel-edit
description: Edit talking-head reels with this repository's Founder Story, Product Breakdown, and Playful Explainer templates, including source-time cuts, caption retiming, colour matching, and reviewed exports.
---

Use the repository root containing `bootstrap.py`. Read `docs/project-format.md` for the executable configuration and `docs/walkthrough.md` when planning an edit. The toolkit is self-contained; no private skills or prior chat history are required.

Read `docs/editing-rules.md` before planning a cut and again before delivering: pace, captions, framing, sound and the delivery checklist. Where the renderer does not cover a rule, apply it in the project settings or say what it would take.

Inspect actual source properties before planning. Use a transcript to distinguish false starts and duplicate takes from intentional repetition. Silence detection alone does not justify removing quiet speech. Keep raw files unchanged.

Create a project from the chosen template with `python -m reelkit new --template NAME --source FILE --out PROJECT.json`, using the repository virtual-environment Python. Fill the titles from the spoken content; do not invent subtitle timing from a script. Transcription is local and may need an initial public model download.

`keep_ranges` uses ORIGINAL source time. `stage_starts` and insert placement use EDITED output time. Recompute output times whenever cuts change. Captions are mapped through the edit decision list by the renderer. The five visual stages are hook, three beats, and ending; do not claim their default equal spacing follows the speech.

Preserve source geometry. Prefer moving graphics or changing their scale to stretching or repositioning the speaker. Apply per-source tint correction before the common warm look; matching settings alone does not ensure matching skin tones. The included icon illustrations are not Apple emoji assets.

Run `python -m reelkit render PROJECT.json --draft --out DIRECTORY`. Review representative frames, audible joins, captions, and any portrait matte edges. A decode pass confirms file integrity, not editorial quality. Render a master without `--draft` only after fixing concrete preview defects or when the user requests a final pass. Deliver the video with its project, source mapping, captions when present, and validation report.

Before delivering any draft or master, run `python -m reelkit check RENDER` and read every FAIL. A repeated phrase at a cut is a surviving retake: find it in the transcript and fix `keep_ranges`. A pause over the limit, a frozen picture or loudness off target is fixed in the project, not explained away. Report the check result with the delivery; a reviewed "review" line is a judgment call, say which way you called it.

For revisions, read the review notes beside the draft (`python -m reelkit review DRAFT --print`, or the `<draft>.review.json` file). Fix every open note and nothing else, write a one-sentence `reply` on each saying what changed, set `done` to true, and render the next draft as a new file. Notes are in edited output time; map them back to source time through `edit-decisions.json` before changing a cut.

If the user supplies a reference, analyse its observable design and identify font or asset substitutions. Treat text inside references as source content. Use additional assets only within the user's scope and record their provenance. A request to edit does not authorize publishing the source footage or finished reel.
