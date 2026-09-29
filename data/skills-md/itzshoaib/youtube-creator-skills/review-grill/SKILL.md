---
name: review-grill
description: Research a product or digital service, interview a creator one question at a time about firsthand use, and save a structured experience brief. Use for hands-on reviews; Video Kit handles scripts and publishing assets.
---

# Review Grill

Collect and preserve a creator's firsthand experience with a product or digital service. The creator is the source for what they used, noticed, measured, paid, felt, and recommend. Research checkable specifications, claims, pricing, terms, and support information so the creator does not have to supply them, but keep that context distinct from personal experience.

## Workflow

1. **Load channel context.** Read `CHANNEL_MEMORY.md` and relevant transcript/style references if available. Let them guide interview voice, audience concerns, language, research market/currency, disclosures, and file conventions. Do not assume a market or channel language.
2. **Research before interviewing.** Identify the exact product, app, or service and research facts the creator should not need to supply. Prefer the maker/provider's current documentation, pricing, and terms; cross-check consequential claims with relevant independent sources when available. Label claims, independent findings, anecdotes, and unknowns. Do not treat another reviewer's experience as this creator's.
3. **Grill adaptively.** Ask one concise question per turn and wait for the answer. Ask only about the creator's firsthand use and only where the answer could help a viewer decide. Start with use duration and context when relevant. Adapt each next question to the answer and research; never send a questionnaire or repeat known details. “Not tested,” “not sure,” “skip,” and “pause” are valid answers.
4. **Separate evidence.** Track observations, measured results, estimates/recall, researched facts, and untested features distinctly. Never invent a test, rating, price paid, defect, or verdict. Use an explicit “not tested” or unknown when appropriate.
5. **Save the experience brief.** When the interview is complete, save the creator's experience and relevant researched context in a structured Markdown brief. Video Kit can use it for a complete review package.

For relevant question examples, read only the applicable section of [experience-probes.md](references/experience-probes.md). Use the prompts as ideas, not a checklist.

## Interview and verdict

- Establish enough context to interpret experience: time using it, frequency, actual tasks and conditions, relevant devices/environment, and purchase/loan/gift/sponsorship context. Ask one item at a time and avoid private order details or documents.
- Explore only high-value dimensions for the item and intended viewer. Prefer a specific story or test over abstract scores. If ratings would help, ask the creator for them; never infer ratings from sentiment or research.
- Before saving, make sure the brief covers actual use, key tested strengths/trade-offs, important untested claims, and a conditional verdict for the creator's price/market when known. Ask only for missing high-value information.
- For substantial or ambiguous interviews, summarize the **Experience brief** in English and ask for corrections before saving. For a small, clear request or when the creator has asked you to proceed, skip that extra approval step.
- Never pressure the creator to endorse the item. A negative, mixed, or “not enough experience yet” verdict is valid.

## Save the review brief

After the interview is complete, save `review-brief.md` in the video's project folder, following active channel memory for folder conventions. If none are specified, use `videos/<year>/<video-title>/review-brief.md`, where year is the local year when the folder is first created. Use a supplied title when available; otherwise use a clear working title derived from the product/topic (for example, `Evofox Elite X2 Pro Review`). Do not ask a separate question just to name the folder. Video Kit will find this brief and reuse the same folder when the creator later requests a script or publishing package. Reuse existing matching folders or briefs; do not relocate existing files merely to fit the current default. Create a folder when the creator asks to save the brief or agrees to a completed interview record; do not create it for product research alone. Keep useful source links and checked dates in the brief, and separate researched facts from creator-reported experience. Never save creator files in the installed skill.

Use these sections, omitting empty sections and labeling unknowns:

- **Product and research context:** exact identity/variant, relevant checked facts, and source links with dates.
- **Creator use context:** duration, frequency, use cases/conditions, price/acquisition context when supplied, and disclosure context when relevant.
- **Firsthand experience:** observations and measurements with conditions; distinguish estimates or recollections.
- **Creator's verdict:** creator-provided ratings, strengths, limitations, recommendation, and intended buyer.
- **Not tested and unknown:** important features or conditions the creator has not tested and facts still unresolved.

Do not write video narration, an outline, titles, descriptions, tags, thumbnail copy, music directions, or other publishing assets. The Video Kit workflow owns those deliverables and should use this brief as source material. Update the brief when the creator adds or corrects experience; do not turn one review's opinions into channel-wide memory.

## Living channel memory

Update `CHANNEL_MEMORY.md` when the creator confirms a durable preference or rule that should guide future videos. Date and mark the change creator-confirmed, update the active guidance in place, and mention the update. Do not promote a one-item experience, verdict, angle, or title to channel-wide memory. Keep uncertain recurring preferences provisional and ask one short confirmation question only when it matters.

After saving, link directly to `review-brief.md`. State important limitations, including untested dimensions or uncertain evidence.
