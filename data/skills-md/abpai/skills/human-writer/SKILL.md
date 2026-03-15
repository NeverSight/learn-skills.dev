---
name: human-writer
description: >
  Edit text to remove signs of AI-generated writing. Use when reviewing or
  revising prose to make it sound natural, specific, and human-written. Detects
  and rewrites AI vocabulary, significance inflation, promotional language,
  -ing padding, em dash overuse, rule-of-three, negative parallelisms,
  pseudo-profound flourishes, dying metaphors, vague attributions, filler
  phrases, sycophantic tone, extrapolation to universal principles, and
  formulaic structure. Triggers include
  "humanize this", "make this sound human", "remove AI patterns",
  "edit for voice", "deslop this", or any request to clean up AI-sounding text.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
license: MIT
metadata:
  author: Andy Pai
  version: "1.2"
  upstream_skill: "https://github.com/blader/humanizer"
  tags: "writing editing humanize voice anti-slop GEO"
---

# Human Writer

Edit text so it reads like a person wrote it, not a language model.

Adapted from the [Humanizer](https://github.com/blader/humanizer) skill (based
on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)),
with additions from Andi Search's AI-slop classification system, Orwell's
"Politics and the English Language" (1946), and Paul Graham's writing advice.

---

## Why This Matters

AI search tools (ChatGPT, Perplexity, etc.) cite few sources per response.
Graphite (2025) found 82% of those citations are human-written. Content that
reads as AI-generated gets filtered or deprioritized. If you want AI systems to
surface your writing, it has to pass as human.

Andi Search filters 40-50 million pages of AI slop per day from their index.
The patterns below are the same ones classifiers use to bin content.

If you are a non-native English speaker, pay extra attention. You are less
likely to notice AI tells in your own output because the phrasing may sound
fine to you even when it screams "machine-generated" to native readers.

---

## The One Rule

Let AI help with drafts and structure. Keep the thinking yours.

Original ideas and genuine expertise still beat any style fix. If the thinking
is generic, no amount of polish will help.

Hemingway called this the iceberg theory: "The dignity of movement of an iceberg
is due to only one-eighth of it being above water." His point: you have to know
more than you write in order to write well.

Two corollaries:

**Be specific.** "$15K MRR, growing 50% month over month" beats "experiencing
significant growth." Numbers, names, and concrete details are persuasive because
readers can verify them. "Commitment to excellence" says nothing.

**Use short words.** That is how people actually talk. "We built this" instead of
"this was constructed by our team." If you would not say "utilize" out loud,
write "use."

---

## Voice and Personality

Avoiding AI patterns is half the job. Sterile, voiceless writing is just as
obvious as slop.

### Signs of soulless writing (even when "clean")

- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No first-person perspective when it would be natural
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to add voice

**Have opinions.** "I genuinely don't know how to feel about this" is more human
than neutrally listing pros and cons.

**Vary rhythm.** Short punchy sentences. Then longer ones that take their time.
Mix it up.

**Acknowledge complexity.** Real humans have mixed feelings. "This is impressive
but also kind of unsettling" beats "This is impressive."

**Use "I" when it fits.** First person is not unprofessional. "I keep coming
back to..." or "Here's what gets me..." signals a real person thinking.

**Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and
half-formed thoughts are human. Text that perfectly follows every writing rule is
itself a tell. One reader correctly identified an AI-written post because "there's
no sentence or paragraph that doesn't follow some clear/concise chain of thought."
Humans write messily.

**Be specific about feelings.** Not "this is concerning" but "there's something
unsettling about agents churning away at 3am while nobody's watching."

**Be inconsistent on purpose.** AI is unnervingly consistent about small style
choices — punctuation always inside quotes, or always outside. Parallel
structure in every list. Humans are naturally inconsistent about these things.
If you notice robotic consistency in punctuation, capitalization, or list
structure, break the pattern.

---

## Audit Priority

Newer models have largely fixed the obvious vocabulary tells ("delve", "in the
realm of"). They have gotten worse at structural patterns: contrastive negation,
pseudo-profound flourishes, elegant variation, and rule-of-three. Prioritize
those during review. The vocabulary list still matters because models regress
unpredictably and because older drafts may use older models.

---

## Patterns to Fix

### 1. AI Vocabulary

Delete on sight:

> delve, crucial, pivotal, vibrant, vital, foster, showcase, underscore,
> landscape (abstract), tapestry (abstract), testament, intricate,
> interplay, garner, enhance, boasts, groundbreaking (figurative), renowned,
> nestled, Additionally

Delete these phrases:

> "in the realm of", "excited to announce", "let's dive in", "plays a key
> role", "commitment to excellence", "it's important to note", "in
> conclusion"

Replace:

| AI version    | Write instead |
| ------------- | ------------- |
| serves as     | is            |
| stands as     | is            |
| utilize       | use           |
| facilitate    | help          |
| leverage      | use           |
| in order to   | to            |
| due to the fact that | because |
| at this point in time | now    |
| has the ability to | can       |

### 2. Significance and Legacy Inflation

AI puffs up importance by claiming everything "marks a pivotal moment" or
"underscores the significance of broader trends."

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989,
> marking a pivotal moment in the evolution of regional statistics in Spain.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect
> and publish regional statistics independently from Spain's national
> statistics office.

Words to watch: stands/serves as, is a testament/reminder, vital/significant/
crucial/pivotal role, underscores/highlights importance, reflects broader,
symbolizing ongoing/enduring, setting the stage for, represents a shift,
evolving landscape, indelible mark, deeply rooted. See also pattern 15 for the
rhetorical variant in editorial and tech writing.

### 3. Promotional Language

AI struggles to keep a neutral tone. Everything becomes a tourist brochure.

**Before:**
> Nestled within the breathtaking region of Gonder, Alamata stands as a
> vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata is a town in the Gonder region of Ethiopia, known for its weekly
> market and 18th-century church.

Words to watch: boasts, vibrant, rich (figurative), profound, enhancing,
showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart
of, groundbreaking, renowned, breathtaking, must-visit, stunning.

### 4. Superficial -ing Padding

AI tacks present-participle phrases onto sentences to simulate depth.

**Before:**
> The temple's colors resonate with the region's beauty, symbolizing local
> bluebonnets and the Gulf coast, reflecting the community's deep connection
> to the land.

**After:**
> The temple uses blue, green, and gold. The architect said these reference
> local bluebonnets and the Gulf coast.

Watch for: highlighting, underscoring, emphasizing, ensuring, reflecting,
symbolizing, contributing to, cultivating, fostering, encompassing, showcasing.

### 5. Vague Attributions

AI attributes opinions to unnamed authorities instead of citing sources.

**Before:**
> Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The river supports several endemic fish species, according to a 2019 survey
> by the Chinese Academy of Sciences.

Name sources. "Graphite found" beats "studies show." Numbers and named customers
work because readers can verify them.

### 6. Copula Avoidance

AI substitutes elaborate constructions for "is" and "are."

**Before:**
> Gallery 825 serves as LAAA's exhibition space. The gallery features four
> spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space. The gallery has four rooms totaling
> 3,000 square feet.

Replace: serves as, stands as, marks, represents, functions as, boasts,
features, offers -> is, are, has.

### 7. Rule of Three

AI forces ideas into groups of three to appear comprehensive.

**Before:**
> The event features keynote sessions, panel discussions, and networking
> opportunities. Attendees can expect innovation, inspiration, and industry
> insights.

**After:**
> The event includes talks and panels. There's also time for informal
> networking between sessions.

Vary list lengths. Three is not always wrong, but always three is a tell.

### 8. Negative Parallelisms and Contrastive Negation

"Not only X but Y" and "It's not just X, it's Y" are AI favorites. So is
reframing a straightforward point as a "real question" to sound deeper.

**Before:**
> It's not just about the beat; it's part of the aggression and atmosphere.
> It's not merely a song, it's a statement. The real question isn't whether
> we should adopt AI, it's whether we can afford not to.

**After:**
> The heavy beat adds to the aggressive tone.
> We plan to adopt AI tools next quarter.

Use these constructions only when making genuine distinctions, not to sound deep.

### 9. Elegant Variation (Synonym Cycling)

AI has repetition-penalty code that forces synonym substitution. Just repeat
the word.

**Before:**
> The protagonist faces challenges. The main character must overcome obstacles.
> The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns
> home.

### 10. False Ranges

AI uses "from X to Y" where X and Y are not on a meaningful scale.

**Before:**
> Our journey has taken us from the singularity of the Big Bang to the grand
> cosmic web, from the birth of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about
> dark matter.

### 11. Em Dash Overuse

AI uses em dashes more than humans, mimicking punchy sales writing. Use commas
and periods instead.

**Before:**
> The term is primarily promoted by Dutch institutions — not by the people
> themselves. You don't say "Netherlands, Europe" — yet this continues —
> even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people
> themselves.

### 12. Inline-Header Lists and Boldface

AI outputs lists with bolded headers + colons. Rewrite as prose or simple lists.

**Before:**
> - **User Experience:** The UX has been significantly improved.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized
> algorithms, and adds end-to-end encryption.

Also: avoid emojis in headings or bullet points, and prefer sentence case over
Title Case in headings.

Bulleted checklists themselves are becoming an AI tell. When possible, rewrite
bullet lists as prose or at least vary their structure. A wall of tidy bullets
reads like AI copy-editing even if the words are fine.

### 13. Filler, Hedging, and Generic Conclusions

**Filler to cut:**
- "In order to achieve this goal" -> "To achieve this"
- "It is important to note that the data shows" -> "The data shows"
- "The system has the ability to process" -> "The system can process"

**Hedging to fix:**

Before: "It could potentially possibly be argued that the policy might have
some effect."
After: "The policy may affect outcomes."

**Generic conclusions to kill:**

Before: "The future looks bright. Exciting times lie ahead as we continue this
journey toward excellence."
After: "The company plans to open two more locations next year."

### 14. Communication Artifacts

Delete chatbot artifacts that got pasted into content:
- "Great question!", "I hope this helps!", "Let me know if you'd like..."
- "Certainly!", "Of course!", "You're absolutely right!"
- "As of my last training update..."
- "While specific details are limited based on available information..."

### 15. Pseudo-Profound Flourishes

AI loves grand framing that says nothing. State what something does. Skip the
grandiose.

Delete:
> "This changes everything." "The implications are staggering." "We're
> witnessing the emergence of..." "This is just the beginning." "The future
> of X is Y."

### 16. Dying Metaphors

Orwell (1946): never use a metaphor you are used to seeing in print. Worn-out
metaphors have lost their power to evoke images.

Avoid: "toe the line", "Achilles' heel", "level playing field", "play into the
hands of", "hotbed", "at the end of the day."

Use simple verbs (break, stop, mend, kill) instead of phrases built around
prove, serve, form, play, render.

### 17. Staccato and Monotone Rhythm

Avoid 4+ short declarative sentences in a row. Connect ideas with "because",
"so", "which means" instead of listing isolated statements.

**Before:**
> The experiment produced interesting results. The agents generated 3 million
> lines of code. Some developers were impressed. Others were skeptical. The
> implications remain unclear.

**After (informal editorial register; adjust voice to fit your context):**
> I genuinely don't know how to feel about this one. 3 million lines of code,
> generated while the humans presumably slept. Half the dev community is
> losing their minds, half are explaining why it doesn't count.

### 18. Extrapolation to Universal Principles

AI generalizes a specific observation into a sweeping universal claim.

**Before:**
> Once you experience fast deploys, slow CI feels completely unacceptable.
> After switching to TypeScript, going back to plain JavaScript feels wrong.

**After:**
> Fast deploys cut our release cycle from two weeks to a day.
> We switched to TypeScript because it caught three bugs in the first week.

Just state what you did and what happened. Skip the "once you X, you can never
go back" framing.

---

## Quick Reference: Orwell's Rules (1946)

1. Never use a metaphor you are used to seeing in print.
2. Never use a long word where a short one will do.
3. If you can cut a word, cut it.
4. Never use passive where you can use active.
5. Never use jargon if you can think of an everyday equivalent.
6. Break any of these rules sooner than say anything barbarous.

If you wouldn't say it that way to a friend, rewrite it. (Paul Graham)

---

## Process

Work in two passes. A single pass rarely catches everything because models
actively resist style corrections — they will ignore explicit instructions about
voice and structure even when those instructions are right there in the prompt.
This is why the second pass matters.

**Pass 1: Draft with awareness**

1. Start from the writer's own ideas, thinking, and specific details. Inject
   research and source material. The quality of input determines the quality of
   output — a vague prompt produces generic slop regardless of style rules.
2. Draft with the patterns above in mind.
3. Preserve meaning and match the intended tone (formal, casual, technical).

**Pass 2: Audit against the checklist**

4. Scan the draft for every pattern above. Fix each one.
5. Revise for voice. Ask: "What makes this so obviously AI-generated?" Fix
   remaining tells.
6. Read aloud. Does it sound like a person or a press release?

Em dashes and elegant variation are the hardest patterns to suppress. If the
text still has them after revision, run a targeted third pass for just those.
Em dashes in particular are "baked in pretty hard" to current models.

## Output Format

Provide:
1. Revised text
2. Brief list of remaining AI tells (if any) and how you fixed them
3. Summary of changes (optional, if helpful to the user)

---

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup)
- [Orwell: Politics and the English Language (1946)](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/)
- Andi Search AI-slop classification insights (Jed White, Bookface 2026-02-26)
- [Humanizer skill](https://github.com/blader/humanizer) by blader
- [Ahrefs: What percentage of new content is AI-generated?](https://ahrefs.com/blog/what-percentage-of-new-content-is-ai-generated/) (900k pages)
- Strunk & White, "The Elements of Style"
- Zinsser, William. "On Writing Well" — practical advice on clear nonfiction
- Ogilvy, David. "How to Write" — commercial and persuasive writing
- Hemingway, Ernest. "Death in the Afternoon" (1932) — iceberg theory
- [Hemingway App](https://hemingwayapp.com/) — readability editor
