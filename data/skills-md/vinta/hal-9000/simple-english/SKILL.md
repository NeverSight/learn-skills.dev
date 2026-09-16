---
name: simple-english
description: Use when the user explicitly asks for simple English, plain English, or for text a non-native English speaker can read easily — rewrites docs, READMEs, issues, comments, or UI text into plain words and translation-friendly grammar, still native-sounding. Prose the user signs in their own voice goes to write-like-me instead
argument-hint: [text, file, or pointer to rewrite]
user-invocable: true
model: claude-opus-4-6
effort: medium
---

# Simple English

Write or rewrite the given text in Global English: the global-audience tier that Google, Microsoft, MDN, Red Hat, and GitLab documentation follows. Clear structure, unambiguous words, translation-friendly grammar, no controlled dictionary, no hard word caps. The rewrite must give the same technical facts as the source and still sound like a native speaker wrote it.

## Ground rules

- **Meaning is untouchable.** Every fact, value, condition, and caveat in the source survives the rewrite. Softened obligations stay soft: "should" stays a recommendation unless the source means a requirement.
- **Never invent specifics.** Keep each fact at its original precision and flag gaps. Do not fabricate values, names, or conditions.
- **Quoted text is frozen.** Code spans and blocks, commands, config keys, file paths, UI labels, error messages, and identifiers stay exactly as they are. Rewrite the prose around them.
- **Voice survives.** Clarity edits that flatten prose into choppy fragments are regressions. Filler drops freely ("it should be noted that"), personality stays.

## Workflow

1. **Load the rules.** Read [references/writing-rules.md](references/writing-rules.md) in full: sentence structure, word choice, the clarity helpers, tone, and the substitution table.

2. **Collect the source.** Take the text from the conversation, or Read the files or sections the user pointed at. When the user wants new text drafted instead of existing text rewritten, collect the facts to state (from the conversation, code, or files) and treat them as the source for every later step. Done when you hold every passage to rewrite or every fact to state.

3. **Sort each passage** into procedure (imperative work steps), description (declarative prose), or micro-text (headings, UI labels, error messages). Procedures get imperative mood and condition-first ordering. Micro-text gets a verb when clarity needs one.

4. **Map the terminology.** List each concept that appears under more than one name, pick one term per concept (prefer the project's established names), and use it everywhere. Done when no concept has two names and no word carries two meanings.

5. **Rewrite sentence by sentence.** Subject-verb-object with the subject early, one idea per sentence, active voice and present tense, conditions first, small words kept ("that", "who", articles), pronouns with more than one possible referent replaced by their nouns, noun stacks broken at two modifiers, hidden verbs uncovered ("install", not "perform an installation"), idioms and phrasal-verb bloat swapped per the substitution table. Kohl's main rule decides every edit: no change that sounds unnatural to a native speaker.

6. **Verify every paragraph and sentence** against the checklist:
   - One topic per paragraph, the point stated in its first sentence
   - Subject and verb early, at most three linked clauses, no "there is/are" openers
   - Procedures imperative with conditions first
   - Every pronoun's referent unambiguous, every abbreviation defined at first use
   - Terminology consistent with the map from step 4, parallel ideas in parallel form
   - No idioms, culture-specific references, Latin abbreviations, or directional cross-references ("above", "below")
   - The sentence still reads naturally aloud
     Done when every sentence passes, or its deviation is deliberate and appears in the report.

7. **Deliver.** Present the rewrite. Edit files in place only when the user asked for the files to change. After the rewrite, report only what applies:
   - The terminology map, so the user can veto term choices
   - Judgment calls where the source was ambiguous and the rewrite picks one reading
   - Gaps where the source lacks specifics the reader will need
