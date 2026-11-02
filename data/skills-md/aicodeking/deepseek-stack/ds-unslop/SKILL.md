---
name: ds-unslop
description: "Remove AI writing tells from prose and code comments, then rewrite in plain, specific English. Use when writing or editing replies, docs, READMEs, PR descriptions, commit messages, or comments, or when the user types /ds-unslop."
---

# Unslop

Write clean as you draft. Then scan for these tells and rewrite. Keep the meaning and tone.

## Tells to remove

Words
- Inflated vocabulary: delve, crucial, pivotal, robust, seamless, leverage, utilize, showcase, underscore, tapestry, landscape, testament, vibrant, intricate. Use the plain word.
- "Serves as", "stands as", "boasts". Say "is" or "has".
- Abstract metaphor nouns: paradigm, north star, flywheel, substrate, bedrock. Name the concrete thing.
- Adverbs that prop up weak verbs: "significantly improves". Give the number or a stronger verb.

Sentences
- "Not just X, but Y." State Y.
- Forced groups of three. Use the real count.
- Trailing "-ing" clauses: "ensuring reliability", "highlighting the need". Delete them or make a real claim.
- Vague sources: "experts say", "many believe". Name the source or cut it.
- Filler: "in order to", "it is important to note that", "due to the fact that".
- Stacked hedges: "could potentially". Pick one qualifier or none.
- Passive voice that hides the actor. Name who does it.
- Feelings instead of mechanisms. If a sentence fits any project's docs unchanged, cut it.
- Generic endings: "the future looks bright". End on a fact or the next step.
- Over-compressed fragments, arrows, and symbol shorthand. Write full sentences with articles and verbs.

Formatting
- Em dashes. Use a period or a comma.
- Colons used as mid-sentence connectors. Keep colons before lists.
- Bold on every term, and "**Label:** label restated" bullets.
- Title Case Headings. Use sentence case.
- Decorative emojis and curly quotes.

Chat habits
- Openers and closers: "Great question", "Certainly", "I hope this helps", "Let me know if".
- Agreement as a reflex. Give your actual judgment.

Code comments
- Comments that narrate the next line, banner comments, and commented-out code. Delete them.
- Keep only comments that explain a reason the code cannot show.

## Rewrite procedure

1. Name the reader and what they need to do or know after reading.
2. Delete every sentence that does not serve that need.
3. Replace synonyms for one thing with a single name. Use the real file, flag, or command name.
4. Split sentences that carry two ideas. Vary sentence length.
5. Put conditions before instructions: "To reset the cache, run `make clean`."
6. Make every "it" and "this" point at one clear noun.
7. Replace vague claims with a number, a command, or a concrete example.
8. Reread once for the tells. A stiff sentence that follows every rule still needs a fix.

## Example

Before: "This robust tool serves as a powerful way to seamlessly streamline your workflow, ensuring efficiency."

After: "`sync.sh` copies changed files to the server in about two seconds."
