---
name: fasaha
version: 1.2.0
author: Adel Ben Yahia (adelpro)
license: MIT
description: "Review and fix AI-generated or AI-translated Arabic so it reads as fluent, native Modern Standard Arabic (MSA) instead of translated/calqued output. Trigger on translating INTO Arabic, writing in Arabic (اكتب بالعربية / اكتبلي بالعربية), writing original Arabic, or reviewing/correcting/proofreading Arabic (‘راجع لي هذا’, 'صحح العربية', 'ترجم هذا للعربية', any Arabic quality check), and proactively before outputting Arabic prose longer than 2-3 sentences. Covers: Latin-script leakage, English sentence-structure calque, word choice/terminology, morphology/agreement, punctuation, hamza spelling, dialectal leakage into MSA. Ships a self-maintained register profile (voice-profile.md) for tone and MSA-vs-Darija choice, a runnable checklist, a terminology glossary, and an accumulating failure log. Register-focused; a separate style/voice skill may layer after it."
metadata:
  version: 1.2.0
  tags: [arabic, translation, editing, quality, msa]
---

# Fasaha (فصاحة) — Arabic Fluency & Correction

Fasaha (فصاحة) means eloquence and correctness of expression in Arabic — text that reads as if
it was written by a native speaker, not translated. This skill fixes AI-generated or AI-translated
Arabic so it reaches that bar.

**Relationship to style/voice skills:** this skill fixes structural/linguistic correctness only.
For register and tone on top (MSA vs Darija, formality, terminology), fasaha now ships a
self-contained profile at `references/voice-profile.md` — generic, editable by any agent, updated
as the user states preferences. Run `fasaha` first (make the Arabic correct and native-sounding),
then apply the matching register profile second. If the user has a separate skill defining their
personal tone/voice, that may be used instead of the built-in profile (or layered after it) — the
built-in file is the default when no separate voice skill exists. Either way they compose — don't
skip one because the other ran.

**Grounded in:** the QALB (Qatar Arabic Language Bank) annotation guidelines — the closest thing
to a published standard for correcting AI/MT-generated Arabic — plus patterns specific to LLM
translation failures that predate/postdate QALB's 2013 scope (see Section 6). Primary source:
Zaghouani, Habash & Mohit, *QALB Guidelines v0.90*, CMU-Qatar/Columbia, 2013 —
http://nlp.qatar.cmu.edu/qalb/QALB-guidelines_0.90.pdf. Full bibliography with links in
`references/sources.md`.

## When to use this

- The user asks to translate something into Arabic
- The user asks to write in Arabic (اكتب بالعربية / اكتبلي بالعربية) or write original Arabic content
- The user asks to review, correct, or proofread existing Arabic text (their own or AI-generated)
- Claude is about to output more than 2-3 sentences of original Arabic prose (article, README,
  community post, forum reply, commit message translation, etc.) — run this before finalizing,
  don't wait to be asked
- The user asks why their Arabic output "feels off" or "sounds translated"

## The Process

1. **Read `references/llm-failure-log.md` first.** Known failures are checked before the general
   checklist, so a pattern already caught once is never missed twice.
2. Draft or obtain the Arabic text (literal translation is fine as a first pass — don't try to
   get it right in one shot)
3. Run the checklist in `references/checklist.md` — Sections 1-7 below plus the register pass —
   against the draft
4. Rewrite based on what the checklist catches
5. Apply the matching register profile from `references/voice-profile.md` for tone and formality
   (MSA vs Darija), fall back to a separate personal voice skill if one exists
6. **Append any genuinely new pattern to `references/llm-failure-log.md`** using its entry schema.
   One entry per *new* pattern, never one per run, and never delete an existing entry. This is the
   feedback edge — it is what makes the next review faster.

Don't skip straight to a "polished" single-pass translation — the calque problem (Section 2) is
much easier to catch by explicitly checking sentence boundaries against the source than by trying
to write well the first time.

## 1. Latin Script Leakage

**The single most common and most visible error.** Any English word that isn't a proper noun,
product name, or standard technical identifier must be translated into Arabic.

- Keep in Latin script: model/product names, benchmark names, library/API identifiers, and true
  abbreviations with no common Arabic equivalent (e.g. `IBM`).
- Translate everything else: adjectives, common nouns, verbs — even when the English word feels
  "technical." Don't leave a word untranslated out of habit just because it's a common tech term.
- Check every list/table item individually — a missing translation on one row while the rest are
  fine is a common miss (formatting-consistency error, not just a vocabulary one).

## 2. Sentence-Structure Calque

The most damaging error because it's invisible sentence-by-sentence but obvious paragraph-by-paragraph.
Symptom: every Arabic sentence mirrors one English sentence, in the same order, with the same
boundaries. Grammatically correct, but it reads as translated rather than composed.

Fix by restructuring, not by translating harder:
- Chain related ideas with connectives instead of stacking short standalone sentences:
  `فـ` / `إذ` / `حيث` / `بينما` / `مما` / `وذلك لأن`
- Merge sentences that share one subject or one cause-effect relationship in the English original
  into a single Arabic sentence with a connective, rather than keeping them as two sentences.
- It's fine — often better — for one English sentence to become half an Arabic sentence, or for
  two English sentences to merge into one Arabic sentence.
- After drafting, read only the Arabic (cover the English) and ask: would a native writer covering
  this topic from scratch have grouped ideas this way? If every paragraph break falls exactly where
  the English paragraph broke, look again.

## 3. Word Choice / Terminology

Generic-but-wrong translations that are grammatically valid but semantically off, especially for
technical or domain terms.

- ❌ `تشغيل يتم` (a generic/mechanical rendering of "run" in "museums are run by") when a more
  precise verb like `تُدار` fits the institutional context better (worked example in
  `references/mt-examples.md`).
- When a technical term has a standard Arabic rendering in the relevant domain, use the
  domain-standard term, not a generic dictionary translation.
- Check: does the chosen word carry the same specific meaning as the source, or just a plausible
  general one? If in doubt, prefer the more specific/technical term over the safe/common one.

## 4. Morphology, Agreement, and Syntax

Standard MSA grammatical correctness — gender/number agreement, broken plurals, missing obligatory
prepositions, definite article consistency, redundant/missing words.

- Gender agreement: `الجامعة الجديدة` not `الجامعة الجديد`
- Broken plural vs. incorrect sound plural: `حدائق` not `حديقات`
- Obligatory prepositions after certain verbs: `تخرج من الجامعة` not `تخرج الجامعة`
- Missing definite articles carried over from English's lack of them: `تغير لون الجلد والتصبغ`
  not `تغير لون جلد وتصبغ`
- Check every pronoun (`هذا`, `هذه`, `ذلك`) has a clear antecedent that survived the translation —
  translation/compression sometimes drops the sentence a pronoun was pointing back to.

## 5. Punctuation, Hamza, and Numbers

Mechanical but highly visible if wrong — these are the errors a native reader notices instantly.

- Use Arabic punctuation marks, not Latin ones: `،` not `,` / `؛` not `;` / `؟` not `?`
- Hamza spelling is one of the most common AI/MT error sources. Quick checks:
  - Initial hamzat wasl vs. qat': test by prefixing و or ف — if the hamza is pronounced, it's qat'
    (write `أ`/`إ`); if silent, it's wasl (write bare `ا`)
  - Medial hamza seat depends on the stronger of the two surrounding vowels (kasra > damma > fatha)
  - See `references/qalb-spelling-rules.md` for the full hamza/punctuation/number rule set if a
    specific case is unclear
- Numbers: keep the source's numeral system and grouping convention consistent; don't silently
  convert between Eastern Arabic and Western Arabic numerals mid-document.

## 6. Dialectal Leakage into MSA

AI output can slip into dialect, especially when the prompt, source material, or context contains
dialectal Arabic. QALB Section 5.6 classifies dialectal words into six categories — knowing which
category a word falls into determines whether it needs correcting to MSA at all.

**Needs correction to MSA (morphologically/phonologically close to an MSA word):**
- Morphological variants: `انتو جعلتوا` → `أنتم جعلتم`، `بيكتب` → `سيكتب`
- Phonological variants: `جذور` → `جزور`، `كهك` → `كعك`
- Closed-class dialectal words (pronouns, particles): `اللي` → `الذي/الذين`، `عم` → prefix removed
  (`عم ناكل` → `سنأكل`), `هذي`/`هايدي` → `هذه`، `مش`/`موش` → `ليس` (only `لم` when negating a past
  action — see `references/dialect-classification.md`)

**No correction needed, even though it looks dialectal:**
- Words that appear dialectal but are actually valid in standard dictionaries: `أوتوبيس`،
  `زعلان`، `أنت مزعوج` — check a dictionary (e.g. almaany.com) before "fixing" these
- Foreign loanwords and proper names, unless clearly misspelled: `كاتشيب`، `كانيلوني`،
  `جورج بوش` — only correct if the spelling itself is wrong, not the word choice
- Words specific to a regional dialect with no MSA equivalent at all (e.g. `كرهبة` in Tunisian
  dialect) — these have nothing to translate to; leave them if the source intends dialect

**When to flag instead of translate:** if a passage is more than roughly a third dialectal, or
uses a dialect the reviewer isn't confident in, don't attempt word-by-word MSA correction — flag
it. Partial, uncertain correction of heavy dialect usually makes the result worse, not better.
Full classification table and more examples: `references/dialect-classification.md`.

## 7. What QALB Doesn't Cover (LLM-specific gaps)

QALB's guidelines (2013) were built against older statistical/rule-based MT and human learner
text — they predate LLM translation, so their error distribution assumes MT output that's often
choppy or ungrammatical. LLM translations are usually grammatically clean but calqued (Section 2)
and prone to Latin leakage in specifically technical/marketing vocabulary (Section 1) — errors
QALB's annotators rarely saw. Don't assume QALB's category weights (spelling-heavy, from
2013-era MT) match what you'll actually find in modern LLM-generated Arabic — in practice,
Sections 1-3 above catch more real issues in LLM output than Sections 4-5. Dialect leakage
(Section 6) is more likely to come from dialectal source material or prompts than from the LLM
itself, since modern LLMs default to MSA unless steered otherwise.

## Reference Files

- `references/qalb-spelling-rules.md` — full hamza spelling rules, Arabic punctuation usage
  rules (comma/semicolon/colon/question mark contexts), and number-writing rules. Read when a
  specific spelling or punctuation case in Section 5 isn't resolved by the quick checks above.
- `references/mt-examples.md` — worked full-sentence MT correction examples (word order,
  missing articles, agreement, lexical choice) drawn directly from the QALB source. More useful
  than the spelling reference for calibrating Sections 2–4 (calque, word choice, agreement)
  against real cases rather than abstract rules.
- `references/dialect-classification.md` — QALB's full six-category dialect classification with
  correction/no-correction examples for each. Read when Section 6 flags a possible dialectal word
  and you need to determine which category it falls into.
- `references/voice-profile.md` — a generic, self-maintained register profile. After the
  correctness pass in Sections 1-6, apply the matching register (MSA vs Darija, formal vs casual,
  tone, terminology) from here. Any agent updates it directly as the user states register
  preferences or corrects output. If no profile fits the task, apply the caller's own voice skill
  when one is loaded; only ask which register when there is no such skill and the user has not
  stated a preference.
- `references/checklist.md` — the runnable quality gate: every Section 1-7 + register check as a
  single pass, with a prescribed output shape. Run this to enforce and audit the correction work.
- `references/terminology.md` — accumulating glossary of standard Arabic renderings for web-dev
  and e-commerce terms. Use it for consistency; any agent adds to it as terms get settled.
- `references/llm-failure-log.md` — accumulating log of real caught errors (bad → good → section).
  Check it for known patterns; append new ones so the skill improves over time.
- `references/sources.md` — the QALB source this skill is built on, with a direct link.
