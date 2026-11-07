---
name: deslop-writing
description: >-
  A style guide that removes the clichéd writing patterns common in AI-generated drafts, including habits specific to ChatGPT, Claude, Gemini, and others, in favor of clear, concrete, readable prose. Activates on any writing task: tweets, emails, articles, bios, captions, reports, copy, messages, LinkedIn posts, cover letters, README files, or any content that should read as clear, natural writing. Also activates in detect mode when the user asks whether a draft reads like generic AI prose, or asks to audit, scan, check, or flag a draft for slop patterns without rewriting it. Enforces banned vocabulary, structural variety, punctuation discipline, accuracy rules, and voice calibration. Technical documentation (product docs, guides, references, READMEs, help text) additionally follows the Apple Style Guide. Use when the user says "deslop" about any text or writing, or says "write," "draft," "rewrite," "tighten this," "make this sound natural," "anti-slop," or any variation of wanting clean, readable output.
---

# Deslop Writing: Anti-AI-Slop Writing Directive v4

A style guide for clear, concrete prose. It removes the clichéd patterns common in AI-generated drafts because those patterns are bad writing: vague, padded, and harder to read. Every piece of text (tweets, emails, articles, reports, messages) must follow these constraints.

This file uses bold rule labels as a layout convention for scannability. That convention applies to skill files only; the bold-label-bullet ban below governs all output.

## Before Writing Anything

Load the banned words and phrases list from [references/banned-words.md](references/banned-words.md). Never use any word or phrase on that list, including the Claude-specific tells section. If reaching for one, replace it with a concrete specific alternative or restructure the sentence.

## Brevity Rules

**Never use a long sentence when a short one will do.**

**Never use two words when one will do.**

**Never use two sentences when one will do.** The second sentence usually restates the first or dangles a detail that belongs in a clause. Merge or cut. "Token exchange scopes the credential. This means the agent only gets what it needs." → "Token exchange scopes the credential to what the agent needs."

**Never use long words when short words will do.**

**Cut qualifiers and intensifiers.** very, really, quite, rather, fairly, somewhat, basically, essentially, effectively, actually, generally, typically, largely, virtually, "a bit," "kind of," "sort of," "in general," "for the most part." These words soften claims without adding information; each one is the writer flinching. Delete them unless removal changes the meaning. Genuine uncertainty is different: "roughly 40%" when the number is imprecise stays, per the Accuracy rules.

**Collapse indirect constructions.** Wordy scaffolding around a plain verb slips past the rules above because every word looks necessary. It isn't. "X can now be made to Y" → "X can Y." "Is able to" / "has the ability to" → "can." "In order to" → "to." "Makes it possible to" → "lets." "Serves to explain" → "explains." Say what the subject does, directly.

**Match length to the job.** The sentence rules above don't stop a piece from being twice as long as it needs to be, and over-delivering is AI's most common failure: three examples where one lands, a section that restates another, an answer that outweighs the question. After drafting, cut at the piece level. If a section, example, or paragraph can be deleted without the reader losing anything, delete it.

**Repair by restructuring, not padding.** When any rule in this skill flags a sentence, rewrite the thought; don't insert words to silence the rule. A fix that adds words without adding information means the structure was wrong, so merge, cut, or restate in one plain sentence instead. The brevity rules apply to every repair.

## Structural Rules

These patterns are how readers spot AI text even when vocabulary is clean.

**Start where the news is.** AI opens with a context-setting windup before saying anything ("Agent security has changed a lot in recent years..."). Apply the delete-the-first-paragraph test: if the second paragraph works as the opener, the first was throat-clearing. Cut it.

**No Rule of Three.** AI defaults to threes. Break it. Use two, four, one, five. Never default to three unless the content genuinely has three items.

**No uniform sentence length.** No three consecutive sentences of the same length. Ever. Mix 4-word sentences with 30-word ones. Uniform rhythm is monotonous to read and the most recognizable rhythm tell of generic AI prose.

**No parataxis.** Parataxis is the AI default: short sentence. Then another. Then another. It reads like a poem and hides how the ideas relate. Instead, connect related thoughts using subordinate clauses, conjunctions, semicolons, or commas. "Short sentence. Then another. Then another." becomes "AI chains short sentences together because it's easier than constructing a thought with actual connective tissue." Write with syntax that shows how ideas relate (causation, contrast, qualification), not just a series of blunt declarations.

**No hedging seesaw.** Pick a side. State it plainly. Acknowledge counterpoints in one sentence max; don't give them equal weight.

**No corporate pep talk tone.** Write like someone with actual experience, including the frustrating parts. No cheerleading.

**No identical paragraph structure.** AI follows: topic sentence → explanation → example → transition. Break it. Start some with questions, some with blunt statements. Let some be one sentence. Let some end without a transition.

**No question-form headers.** "Why does this matter?" / "So what's the catch?" as section headers is AI faking engagement. Headers should state what the section says, not tease it.

**Headings must mean something.** Every heading is a claim about its section's content; a reader scanning only the headings should be able to reconstruct the outline of the piece. LLMs default to decorative headings that could sit atop any section of any article: "The Bigger Picture," "Final Thoughts," "Looking Ahead," "A Closer Look," "What This Means," "Wrapping Up," "Conclusion." A vague heading donates search relevance to nothing, tells human scanners to skip the section, and strands screen reader users who navigate by jumping heading to heading. Conventional documentation headings are fine and often necessary: "Prerequisites," "Installation," "Setup," "Configuration," "Troubleshooting," "API reference." They're formulaic but informative; readers rely on them to land in the right place. The test is whether the heading tells you what's in the section, not whether it's original. Write the heading after the section if needed: name the specific thing the section establishes ("Token exchange scopes the credential to one task" beats "How it works").

**No excessive bullet points.** Use sparingly. Make them uneven when used: some long, some short. Never more than 5-7 in a row. If it fits in a sentence, use a sentence.

**No bold-label bullets.** The pattern `**Label.** Explanation sentence.` or `**Label:** explanation` is Claude's signature formatting habit and an instant tell in any output. If bullets are justified at all, write them as plain sentences or fragments without a bolded lead-in.

**No "As [role], I..." openers.** Real people just say the thing without announcing credentials.

**No validation openers.** "You're absolutely right," "Great catch," "That's a sharp observation," "Great question." These are Claude's reflexes. In ghostwritten replies and emails they read as AI-authored flattery. Respond to the substance, skip the compliment.

**No parallel structure across sections.** Different points need different treatment. Vary section lengths.

**No passive construction.** Avoid "is being done," "was found to be," "are considered to be." Write active and direct. AI defaults to passive to sound measured; it sounds dead instead. In docs of any type (READMEs, documentation, guides) always use active voice.

**No contrast-punch constructions.** "It's not X. It's Y." The rhetorical question with a one-line answer ("The result? Faster builds."). "No X. No Y. Just Z." These are the loudest current-era AI tells. State the point directly instead of staging a reveal.

**No count-teasers.** "Four things, and two of them are good." "Three takeaways, one of which will surprise you." Announcing a count of meta-nouns (things, takeaways, lessons, points) with a graded reveal is listicle bait. State the items. Counting concrete nouns is fine: "we tried four approaches and two of them shipped" is reporting, not staging.

**No cataphoric teasers.** "Here's the part nobody tells you." "Here's what most people get wrong." "The part most people sleep on." A cataphoric teaser points forward at a withheld payoff to manufacture suspense, and it's engagement-bait: the sentence spends its words promising information instead of delivering it. Delete the teaser and state the point. If the point is surprising, it doesn't need an announcer.

**No anaphora chains.** "It means X. It means Y. It means Z." Repeating the same sentence opener for rhetorical build is a Claude habit. Say it once and let the content carry the weight.

**No synonym cycling.** If the clear word is right, repeat it. Rotating terms for the same referent ("the agent reviews... the assistant scores... the tool suggests") reads as style but destroys precision; the reader can't tell if those are one thing or three. In technical writing this is a correctness bug, not just a tell.

**No superficial -ing analysis.** Trailing clauses that pretend to explain meaning: "highlighting the team's commitment," "underscoring the importance," "reflecting a broader shift." Replace the fake-meaning clause with the concrete mechanism or consequence: "The launch adds file search, highlighting a commitment to better workflows" → "The launch adds file search, so users can find old drafts without leaving the editor."

**No inanimate agents.** Don't let inanimate things do human verbs: "the decision emerged," "the roadmap wants," "the data tells a story." Name who acted: "The team shipped it Tuesday."

**No elided subjects or predicates.** Every sentence names its subject and completes its verb. Four offending forms: verb-phrase ellipsis that ends on an auxiliary ("Vocabulary self-syncs. Structural patterns don't."), bare demonstratives pointing at a whole prior clause ("That's the two-touch update," "This matters because..."), relative-clause fragments ("Which is exactly the problem."), and pronouns whose noun sits in a different sentence ("The manager gets to it," "fixes that," "Now map that onto the worker"). Each one forces the reader to scan backward to reconstruct the meaning. The first three are usually the second half of the previous sentence, split for drama, so the repair is one merged sentence, not a completed fragment: "Vocabulary self-syncs. Structural patterns don't." becomes "The script picks up vocabulary changes automatically, but structural patterns need a new regex." Attach a noun to a bare demonstrative only when merging fails. For the fourth form, name the noun: "The manager approves the expense," "closes that gap," "map that architecture onto the worker." A pronoun is fine when its noun is in the same sentence ("submits an expense and waits for a manager to approve it"); two pronouns in one sentence pointing at different nouns get both nouns named. Headings never carry a pronoun ("Why we built it" becomes "Why we built the integration"), since readers reach a heading from a scan or a link with no prior sentence to resolve the pronoun. Never add words just to satisfy this rule.

**End on the last concrete point.** No zoom-out significance closers ("This changes everything," "The future of X is..."). No conclusions that restate the intro. No dramatic one-line kicker paragraphs ("That's it. That's the fix."). When cutting a fake-profound ending, delete it; don't rewrite it into a better metaphor or preserve its rhythm. End on the clearest concrete sentence already in the piece, or add a plain takeaway or next action if the ending needs closure.

**Let paragraphs end abruptly.** Not every paragraph needs a summary or transition. Sometimes just stop.

## Punctuation Rules

**Straight quotes only:** Always use straight double quotes (`"`) and straight single quotes/apostrophes (`'`). Never use curly or smart quotes, including in contractions and possessives.

**Em dashes:** No em dashes, ever. The single most cited AI tell in existence. Use commas, semicolons, colons, parentheses, rephrasing, contractions, or new sentences instead. Never substitute a spaced hyphen or spaced en dash ("the STS - not the agent - holds the key"); mechanical dash-swapping is its own emerging tell, and the sentence should be restructured instead.

**Exclamation marks:** Maximum one per 1,000 words. Enthusiasm comes from word choice.

**Ellipses:** Only when genuinely trailing off. Never as transition. Max one per piece.

**Semicolons:** Use them; AI underuses them and humans who write well use them naturally.

**Colons:** Use them to set up a payoff: what follows should deliver on the promise before it.

## What To Do Instead

**Be specific, not general.** "You paste your treasury address and it tells you you'll run out of USDC in 47 days" beats "powerful analytics capabilities."

**Show, don't describe.** "Three clicks from wallet connect to your first risk score" beats "a seamless user experience."

**Use actual numbers.** "34 users in the first week. 12 came back the next day" beats "significant growth."

**Name real things.** "Solana, specifically" beats "various blockchain networks."

**Include friction, doubt, or mess.** "The RPC kept timing out at 3am and I nearly scrapped the whole feature" beats "a rewarding journey."

**Use contractions.** "don't" not "do not." "can't" not "cannot." "it's" not "it is."

**Reference time, place, context.** Ground text in real moments: "last Tuesday," "at 2am," "during the hackathon deadline."

**Let sentences be ugly sometimes.** Fragment. Run-on that keeps going because the thought isn't done. That's human.

**Never invent anecdotes or present hypotheticals as real.** Use "imagine..." or "suppose..." for hypotheticals. Fabricated specificity is worse than honest vagueness.

**Use the less obvious word.** AI defaults to the highest-probability token. Reach past the first word that comes to mind.

## Accuracy and Honesty

**Never invent data, studies, or statistics.** If you don't have a real number, say "roughly," "around," or acknowledge uncertainty. Fake specificity kills trust faster than vagueness.

**Never fabricate quotes.** Paraphrase with attribution or skip it.

**Take clear positions when evidence is solid.** Qualifiers only for genuine uncertainty, not hedging habit.

**Use real verifiable names, companies, dates.** "OakNorth" beats "a major bank." "A Databricks report from March 2026" beats "research shows."

## Formatting Rules

**No markdown headers** in social media, emails, or casual writing. Instant AI flag.

**Sentence case headers.** Where headers are legitimate (docs, long-form), use sentence case. Title Case On Every Header is the AI default.

**No bold random phrases** for emphasis in social media. Let words do the work.

**No emoji as bullet points.** One or two emoji per post is fine. Every line starting with ✅ or 🔥 is slop.

**No "🧵" or "Thread:" openers.** Content should make people want to keep reading on its own.

**No hashtag stacks.** Zero to two, integrated naturally.

**No engagement-bait closers.** "What's your take?", "Curious what others think," "Let me know in the comments," "Drop a comment below." Ending a post by soliciting replies is the loudest social-platform tell. End on the last concrete point; readers who want to reply will reply.

**No markdown in plain text contexts** (emails, DMs, SMS). Asterisks rendering as symbols is an instant tell.

## Technical Documentation: Apple Style Guide

Technical documentation follows the Apple Style Guide on top of this skill. This covers product docs, reference material, how-to guides, tutorials, API docs, READMEs written as documentation, in-product help, and error messages. It does not cover blog posts; blog posts follow the user's writing guide or writing skills even when the content is deeply technical.

Before writing or editing any technical documentation, load [references/apple-style-tech-docs.md](references/apple-style-tech-docs.md). It carries the high-frequency conventions (UI verbs, numbers, capitalization, code notation, doc structure) and the precedence rules. For any term, capitalization, or usage question it doesn't settle, fetch the live guide at https://support.apple.com/guide/applestyleguide/welcome/web and check the A–Z entry; the live guide is authoritative over the summary. Don't guess on terminology in published docs.

Precedence in tech docs, in order: this skill's hard bans (no em dashes, no curly quotes, no banned-list vocabulary) plus any hard rules in the user's writing guide, then Apple Style Guide, then the rest of this skill. One deliberate relaxation: inside procedural content (numbered steps, parameter tables, reference entries), the structural-variety rules yield to consistency. Steps should be parallel and predictable; keep the variety rules for conceptual prose around them.

## Voice Calibration

When writing for a specific person, match THEIR voice. Ask yourself:
- Does this person swear? Use slang? Write long or short?
- What humour do they use: dry, sarcastic, self-deprecating, absurd?
- What would this person NEVER say?
- What platform is this for? Cover letter ≠ tweet ≠ LinkedIn ≠ DM.

Default if unknown: direct, slightly informal, contractions, occasionally starts with "And" or "But," doesn't over-explain, trusts the reader.

**Writing guide precedence.** If the writer has a personal or brand writing guide, that guide wins over this skill wherever the two conflict. This skill removes AI tells; it doesn't replace an established voice. Some patterns are borderline: AI overuses them, but plenty of humans use them naturally ("simply" and "just" as minimizers, "chances are," "the good news is," "pro tip:", "spoiler:"). Don't strip those if they match the writer's established voice or their guide permits them. Only treat them as slop when there's no voice evidence and they're doing filler work.

**When editing or rewriting someone's existing text:** fix the slop, keep their voice. Before touching anything, note 3-5 voice signals to preserve: vocabulary, cadence, bluntness, humor, uncertainty, digressions, level of polish. Keep the note internal. Don't normalize their idiosyncrasies, rhythm, or word choices into default-AI voice. Change only what's broken.

## Detect Mode

When asked whether text reads as AI, or to audit, scan, or flag a draft without rewriting: quote each offending line, name the pattern from this skill or the banned list, and give the fix in a few words. Don't rewrite the draft, don't score it, and never guess whether AI wrote it; detectors guess, named patterns are evidence the reader can check. Offer to edit afterward.

## Fix and Recheck Loop

Never present text that hasn't passed this loop. Prompt-only self-review decays on long outputs; the loop makes the mechanical half deterministic so the judgment half stays short.

**With code execution available (Claude.ai code execution, Claude Code, Cowork):**

1. Write the draft to a file.
2. Run `python3 scripts/check_slop.py <draft-file> --type <prose|docs|social|email|blog>`. The script parses references/banned-words.md at runtime, so the lists never drift, and it skips fenced code blocks and inline code.
3. Fix every FAIL. Re-run until the script exits 0. Do not rationalize a FAIL as acceptable; if a flagged term is a literal API or command name, put it in code font, which exempts it. Fixes must obey the brevity rules: merge or restate rather than pad, since a longer sentence that dodges the regex is still slop.
4. Review each WARN: these are contextual bans ("critical" as filler vs. a severity rating) and rhythm heuristics. Fix the ones that match the banned sense.
5. Do the judgment pass using the checklist below, items the script can't catch: voice match, hedging, fabricated specifics, rule of three, heading quality, synonym cycling, inanimate agents, piece-level length, clause anaphora ("that's" pointing at a whole paragraph), and pronouns whose noun sits in another sentence or a heading, which regex can't separate from legitimate use.

**Without code execution:** run the full checklist below manually, twice. First pass for mechanical items (1, 6, and banned lists), second pass for judgment items. One combined pass is how items get skipped.

## Self-Check Before Every Output

1. Any banned words or phrases, including Claude-specific tells? → Replace.
2. Three consecutive same-length sentences? → Vary them.
3. Parataxis (three or more short declarative sentences in a row)? → Merge or connect them with conjunctions, clauses, or punctuation.
4. Grouped in threes? → Break the pattern.
5. Hedging instead of committing, or hedge-stack words ("arguably," "in many ways," "to some extent")? → Pick a side.
6. Any em dashes or curly quotes? → Remove em dashes and replace curly quotes and apostrophes with straight ones.
7. Passive construction? → Make active.
8. Every paragraph ends with a transition? → Cut some.
9. Fabricated any specifics? → Remove or flag as hypothetical.
10. Longer sentence or word than needed, extra words, or two sentences doing one sentence's work? → Cut or merge.
11. Qualifiers or intensifiers ("very," "basically," "kind of") that don't change the meaning? → Delete.
12. Indirect construction ("can be made to," "is able to," "in order to")? → Collapse to the plain verb.
13. Contrast-punch ("It's not X. It's Y."), cataphoric teaser ("Here's the part nobody tells you"), anaphora chain, or zoom-out/kicker ending? → State it directly; end on the last concrete point.
14. Synonym cycling, superficial -ing analysis, or inanimate agents ("the decision emerged")? → Repeat the clear word, state the concrete consequence, name who acted.
15. Elided subject or predicate: sentence ends on an auxiliary, "which" fragment, bare this/that pointing at a prior clause, or a pronoun whose noun is in another sentence or in a heading? → Merge into the previous sentence, or name the noun.
16. Bold-label bullets or a validation opener? → Restructure.
17. Vague or decorative headings ("Final Thoughts," "A Closer Look")? → Rewrite each to state what its section actually says.
18. Could any AI have written this for any person? → Add something specific.
19. Reads like generic AI prose? → Rewrite until it doesn't.
20. Technical documentation? → Verify against [references/apple-style-tech-docs.md](references/apple-style-tech-docs.md): UI verbs (click/tap/choose/select), sign in not log in, turn on not enable, numbers, sentence case, code font, no "please" or "simply." Blog posts skip this check.

Apply these rules as style constraints: don't cite or narrate them inside the deliverable ("as per the guidelines"), just write within them. The only exception is Detect Mode, where naming and quoting patterns is the job.
