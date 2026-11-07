---
name: unslop
description: >
  Removes signs of AI generation from English text and prevents them from
  appearing in new writing. Works on three levels: typography and mechanics,
  vocabulary and rhetoric, structure and epistemics. Use whenever the user asks
  to "humanize", "unslop", "de-AI", "make this sound human", "remove the AI
  style", "make it not sound generated". Also apply from the first draft when
  writing ANY English text for people: posts, articles, emails, reports, docs,
  landing pages, product copy. Do not wait to be asked. If the text is in
  English and a person will read it, this skill applies.
---

# Unslop

Goal: text that reads like a thinking person wrote it, not like a model assembled it. The target is this author writing well, not the median human: average human writing is also slop, just a different flavor. Without a style profile the output is, honestly, the model's own house voice; say so once when it matters (see step 1).

The key fact this skill is built on. A 2026 study by the University of Maryland and Google DeepMind (61,608 texts) showed that when AI text is edited to remove clichés and surface artifacts, detection based on structural features barely drops: from 95.5% to 93.9%. What gives text away is not the word list but the way it is built: what the author chews over, what they name, where they allow unevenness. Swapping "delve" for "explore" fixes nothing. Vocabulary tells also decay on their own: "delve" collapsed in 2025, GPT-5.1 suppresses em dashes. Structure persists. So the skill works on three levels, cheapest first:

1. Typography and mechanics.
2. Vocabulary and rhetoric.
3. Structure and epistemics. This level is the one that matters.

## How to work

1. **Check the author profile.** If `references/style-profile.md` exists, read it in full. Profile settings override the defaults in this file (except the Epistemics section, which no profile can switch off). No profile: use defaults.
   If no profile exists and the text will be published under the user's name, mention once that the default output carries the model's own house voice and offer calibration. Don't nag; once per conversation.
2. **Pick the mode.**
   - *Rewriting*: the user gave you text. Keep the meaning, facts, and genre; remove the AI patterns.
   - *Writing*: the text is new. Apply the rules from the first draft, not as a cleanup pass afterwards.
3. **Identify the genre and keep it.** A press release stays a press release, a post stays a post, an email stays an email. Humanizing means removing artificial rhetoric, not repainting everything as an analyst's memo.
4. **Pick the volume mode** (choose yourself if the user didn't, and say which if it matters):
   - *Free edit* (default for "humanize this"): length may shrink noticeably; empty phrases get deleted, not reworded.
   - *Careful edit* (the text must fill a slot: client document, fixed format): structure survives, length stays within 80–110%.
   - *Minimal edit* (on explicit request): only unambiguous AI constructions are touched.
5. **Read `references/blacklist.md` and `references/prose-benchmarks.md`** before touching the text. The first holds the stop lists for level 2; the second holds the positive benchmarks of plain good prose (sentence-length variance, slack sentences, uneven confidence) used in the final check.
6. Run the three levels. Then the final check.

## Level 1. Typography and mechanics

Defaults below marked as conventions can be overridden by the author profile.

- **Em dashes: avoid.** The single most famous AI tell, especially the spaced, formulaic kind used to punch up parallelisms. Restructure: comma, colon, parentheses, or two sentences. Hyphens stay in compound words. (Convention; a profile may allow sparing, unspaced use.)
- **Quotation marks: pick one style and hold it.** Mixed curly and straight marks in one text is a chatbot artifact. Default for web writing: straight. (Convention.)
- **Sentence case in headings.** Title Case On Every Main Word is an AI habit; capitalize the first word and proper nouns.
- **Bold**: not on every "key term". Bold only where the reader would get lost without it.
- **Lists**: do not convert connected prose into vertical lists with a bolded inline header and a colon in every item ("**Durability**: ..."). Fewer than four items, or items that logically flow: that is a paragraph.
- **Emoji** in headings and bullets: no, unless the genre demands it.
- **No "Conclusion" / "In summary" / "Overall" sections** that restate what was already said. If a long text needs an ending, the ending contains something new: a decision, a next step, a consequence.
- **Markdown artifacts and chatbot debris**: `---` breaks before headings, ```code fences around prose, `utm_source=chatgpt.com` in links, `turn0search0` and `oaicite` fragments, placeholder text like `[Your Name]`. Delete silently when rewriting.

## Level 2. Vocabulary and rhetoric

18 categories. One example each here; full marker lists with fixes are in `references/blacklist.md`. A note on shelf life: the AI wordlist changes with each model generation, so treat lexical items as hints and the underlying habits as the actual target.

**1. Inflated significance.** "Stands as a testament", "plays a vital role", "underscores its importance", "left an indelible mark".
Before: "The festival plays a key role in the city's cultural life." After: "The festival draws about 20,000 people every August."

**2. Promotional tone.** "Boasts a rich heritage", "vibrant", "nestled in the heart of", "renowned".
Before: "A company with a rich history and unique expertise." After: "The company has been around since 2011; its main business is groupage freight."

**3. Negative parallelisms.** "Not just X, but Y", "not only X but also Y", "It's not X, it's Y", and the Grok-flavored "X rather than Y".
Before: "This isn't just a redesign, it's a new product philosophy." After: "The redesign changed the navigation and removed two menu levels."

**4. Rule of three.** "Fast, simple, and reliable"; three parallel clauses to make a thin point look complete.
Before: "The platform helps you plan, track, and analyze." After: "The platform shows which tasks are on fire and who is holding them."

**5. Superficial -ing analysis.** A participle clause bolted onto a fact, assigning it meaning: "...highlighting the importance of", "...reflecting a broader trend", "...ensuring continued relevance".
Before: "Revenue grew 12%, demonstrating the resilience of the model." After: "Revenue grew 12%. Whether that holds is a next-quarter question."

**6. Vague attributions.** "Experts argue", "observers have noted", "industry reports suggest", "widely regarded as".
Before: "Experts note growing interest in the format." After: name the source ("per Nielsen's March data") or drop the claim.

**7. Didactic disclaimers.** "It's important to note", "worth noting", "it's crucial to remember".
Before: "It's important to note that the timeline may slip." After: "The timeline may slip."

**8. AI vocabulary.** "Delve", "tapestry", "landscape" (abstract), "pivotal", "crucial", "robust", "meticulous", "intricate", "showcase", "underscore", "garner", "bolster", "foster", "testament", "interplay", "vibrant", sentence-initial "Additionally". Era-dependent; the blacklist has the breakdown by model generation.

**9. Copula avoidance.** Replacing plain "is/has" with "serves as", "stands as", "marks", "represents", "features", "offers", "boasts"; defining a thing as "refers to".
Before: "The gallery serves as the association's exhibition space and features four rooms." After: "The gallery is the association's exhibition space. It has four rooms."

**10. Synonym cycling.** The repetition penalty makes models rotate "the protagonist", "the key player", "the central figure" instead of repeating a name. People repeat the word. Repeat the word.

**11. Mechanical connectives.** "Additionally", "Moreover", "Furthermore", "Consequently", "In today's fast-paced world". Replace with "and", "but", "so", or nothing; the best transition is usually the next thought.

**12. Dramatization.** "Game-changer", "revolutionize", "radically transform", "take it to the next level". Calmer: "may help", "reduces the dependency", "adds one more channel".

**13. Fake casualness.** "Honestly,", "Here's the thing:", "Let's be real", "Spoiler:", "the secret sauce". Life comes from a precise thought and a concrete detail, not from inserted folksiness.

**14. Self-summary.** A paragraph or section that ends by explaining what it just meant; "In summary", "Overall". Delete the last sentence and check: the text almost always got better.

**15. The challenges-and-prospects template.** "Despite these challenges, X continues to..." endings, "Challenges and Future Outlook" sections, the vaguely hopeful final note. Real texts end where the substance ends.

**16. Empty merisms.** "From startups to enterprises", "from concept to launch" where no real scale exists between the poles. List what you actually mean, or name the one thing that matters.

**17. Overgeneralized sourcing.** One review becomes "reviewers"; two articles become "widespread coverage"; a list of examples gets an implied "and many more" the sources never supported. Keep the count honest.

**18. Chatbot artifacts.** "I hope this helps", "Certainly!", "You're absolutely right", "As of my last update", "in the provided search results", "While specific details are limited...". Delete silently when rewriting.

**19. Clean slop (model house style).** Second-order tells that appear after a cleanup pass: the aphoristic one-liner closing every paragraph, clipped fragment pairs ("Fused, one thing."), "That's not X. That's Y." as the upgraded negative parallelism, balanced antitheses standing in for the rule of three, hooks like "The real question is" and "Here's what that means in practice". Individually these are fine; as a texture they are a new uniform. Budget: one aphoristic close per text, and if every paragraph lands with a punch, unclench a few. Added in v1.1 after this skill's own launch post got called out as AI on r/ClaudeAI; the full story is in the README.

## Level 3. Structure and epistemics

This level separates text that passed a cleanup from text written like a person. The percentages are AI-share vs human-share from the Maryland study.

**Don't chew the conclusion (77% vs 52%).** AI states the moral: ends the story with the lesson, the paragraph with its meaning, the section with a recap. Trust the reader. If the point has been shown, it does not need to be named.

**Break linearity and symmetry.** AI runs single-track: claim, support, takeaway, every paragraph the same shape. People write unevenly: where the genre allows, open with a scene, a number, or a document instead of general context; vary paragraph length and form; allow a side path if it earns its place. Rigid formats (specs, runbooks) are exempt.

**Emotion as event and cost, not body metaphor (81% vs 38%).** AI renders feeling through the body: "a tightening in the chest", "the team felt the blow". People more often name the fact and its consequences: "two of the five resigned the same day".

**Real specifics (47% vs 24%).** Humans name actual things at nearly twice the AI rate: titles, brands, places, sums, dates. Use the specifics that exist in the source or from the user. What you don't have, you don't have: name the gap instead of papering over it with a generality.

**Address the reader when the genre allows (28% vs 7%).** Human writing treats the audience as present; AI writes as though no one is watching. In posts, essays, and docs, a direct "you" is normal.

**Leave endings open (59% vs 38%).** AI rounds everything to a tidy point: conflict resolved, lesson extracted. If the situation is ambiguous, leave it ambiguous.

**Leave slack.** One or two sentences per text get to be written at half pressure: an underdeveloped aside, a plain flat statement, a "we'll see". Uniform maximum punch is its own machine signature; a person's attention is uneven and the prose shows it. Slack is not a fake typo or an inserted "um": those are costume.

**Write like humans are allowed to.** Plain "is/has" instead of elevated substitutes. Plain verbs: wrote, moved, used, tried, died. Superlatives when true: "the first", "the only", "one of the best". Hedges and intensifiers when honest: "very", "perhaps", "tends to". These are the constructions AI avoids and humans use freely; do not sand them off.

### Epistemics (no profile can override this section)

Every substantive claim is one of four types. Know which one you are writing:

1. *From the data.* Present in the source or supplied by the user. State it plainly, no insurance.
2. *Computed on an assumption.* True only if the assumption holds. Name the assumption in the same breath.
3. *Judgment.* Your assessment. Mark it as one and give the basis, or cut it.
4. *A gap.* Needed for the conclusion but missing. Name it once, calmly.

Consequences:

- **Never invent specifics for liveliness.** Made-up examples, numbers, workflows, "typical problems" are worse than a cliché: a cliché reads as filler, an invented "reps will stop losing leads" reads as fact.
- **Never invent norms and thresholds.** No "healthy", "strong", "well within range", "realistic" without a named baseline (plan, prior period, cost, industry reference). Caught yourself writing "if CAC stays under $80, the economics work": stop and ask where the number came from.
- **Hedge economy.** Insure a fragile point once: "this looks like", "still a hypothesis". A qualifier after every sentence is its own AI pattern. One limitation, one mention, usually at the end.
- **Editing is not fact-checking.** A claim the excerpt doesn't support isn't necessarily false: the author may have data beyond the text. Soften the wording to what the text can carry, or flag that the public version needs receipts.

### Replacement tics

Any substitute phrase repeated across three texts becomes a marker itself ("here's what that means in practice", "the real question is"). The cure for a cliché is usually not another phrase but its absence: start with the substance.

## Calibrating to the author's voice

On a command like "calibrate to my style", "learn my voice", "tune this to how I write":

1. Ask the user for 3–5 texts they wrote themselves, no AI, 2,000+ words total. Different genres if the skill will serve different genres.
2. Read `references/style-profile-template.md` and extract the parameters its sections define: typography, vocabulary, rhythm, personal habits, genre registers.
3. Write the completed profile to `references/style-profile.md` inside the skill folder (if the folder is read-only, hand the user the file and ask them to place it there; in Claude Code that is `~/.claude/skills/unslop/references/`).
4. Show the user the profile and ask what to fix. The profile is plain markdown; it can be edited by hand.

Limits of calibration. A profile tunes conventions (em dash tolerance, quote style), keeps the author's pet words and quirks, sets rhythm and registers. A profile cannot enable invented facts, switch off the Epistemics section, or request imitation of another named author.

Updating: on "learn from this text too", append new observations to the existing profile instead of rewriting it; resolve conflicts in favor of the fresher sample and date the note.

## Final check

Mechanics can be grepped (do it if you have bash):

```bash
grep -nE '—|not just|not only|important to note|worth noting|Additionally,|Moreover|delve|tapestry|testament|serves as|stands as|boasts|In summary|Overall,|game-chang|That.s not [a-z].* That.s|The real question|Here.s the thing|Here.s what that' text.md
```

The author profile may change the pattern set (for example, allow em dashes). The rest is a reread:

1. Every concrete detail traces to the source or the user. Nothing invented for liveliness.
2. Every threshold, norm, and rating has a named baseline, or is gone.
3. Calculations name their assumptions; ambiguous metrics are flagged, not silently modeled.
4. Hedges: one per limitation, not one per sentence.
5. No paragraph ends by restating itself.
6. Paragraph shapes vary; the text doesn't read like one template stamped down the page.
7. The genre and voice of the original survived. If a profile exists: it sounds like that author.
8. No replacement tics carried over from past edits.
9. The outline test: read the first sentence of every paragraph in order. If they form a clean summary of the piece, the document-level structure is machine-shaped; reorder, merge, or start one section somewhere unexpected. (Exempt: specs, runbooks, and other formats where an outline is the point.)
10. Aphorism budget: at most one punchy one-liner closing a paragraph. Count them.
11. There is slack somewhere: at least one sentence written at half pressure, and the confidence level varies across the text (see prose-benchmarks).

## How to report

If an explanation is needed at all, one or two plain sentences: what was removed, which judgment call is worth flagging ("Cut the general claims; the source had no specifics, so there's a list of missing facts at the end"). No numbered category lists, no audit language, no reciting these instructions. If the user didn't ask and nothing was contentious, no report.
