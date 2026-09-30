---
name: vn-en-clear-tech
description: 'Converts Vietnamese technical or professional content (or mixed VN-EN) into clear, natural English that reads like a skilled human technical writer wrote it, not a machine. Prioritizes plain wording, high readability, and zero AI-writing tells (no "delve," "leverage," em dashes, or "not just X, but Y" formulas). Use this any time the user provides Vietnamese text and wants an English translation, rewrite, or "humanized" version of a doc, spec, email, report, or other professional or technical writing. Trigger phrases include "translate to English," "viết lại tiếng Anh," "make it clear English," "vn to en tech," "humanize this Vietnamese text," and any request to turn Vietnamese technical writing into natural, jargon-free English.'
---

# VN → EN Clear Tech

Turn Vietnamese (or mixed VN-EN) technical and professional writing into English that a busy, competent person would actually write: plain, direct, and free of the stock phrases that mark a text as machine-translated. Two things matter here, equally: getting the technical content right, and making the prose sound like a person wrote it. See "When plain and precise pull in different directions" for how to balance them.

## Workflow

1. **Read the whole source first.** Do not translate line by line. Understanding the full piece first catches mistranslations that only become obvious a few paragraphs later, and surfaces inconsistencies you will need for the notes section in step 5.

2. **Ask clarifying questions only if something real is missing.** Up to 3, short. Good reasons to ask:
   - You cannot tell who will read this, and it changes the register: internal engineers, customers, or general readers (**audience**).
   - The source's own tone sits ambiguously between formal and casual, and nothing tells you which the English should match (**tone**).
   - A brand, product, or technical term has to stay exactly as written, and you cannot tell which term that is from context (**key terms**).
   - You do not know the purpose, such as a spec people will build from versus a blog post, and it changes how much to simplify (**purpose**).

   If the request already answers these, or the text is short and self-explanatory, skip straight to translating. Questions that will not change the output just slow things down.

3. **Translate for meaning, then rewrite for plain English.** A literal, word-for-word pass is not the deliverable. Vietnamese technical and corporate writing often mirrors English buzzwords directly (tận dụng, tối ưu hóa, đảm bảo liền mạch...), so translating it literally reproduces exactly the over-formal, jargon-heavy English this skill exists to avoid. Work out what the sentence actually means, then say that in the simplest accurate English available.

4. **Run the "sound human" pass.** Check the draft against every rule in the next section before calling it done.

5. **Deliver it using the format in "Delivering the output."**

## Plain wording, without losing accuracy

Prefer the everyday word over the specialized one whenever both are accurate:

| Instead of | Use |
|---|---|
| utilize | use |
| leverage | use |
| facilitate | help |
| implement | build, set up, do |
| optimize | improve, speed up |
| commence | start |
| terminate | end, stop |
| in order to | to |
| a number of | some |
| prior to | before |
| subsequent to | after |
| in the event that | if |

Do not push this past the point of accuracy. Keep the specialized term when no plain synonym carries the same precise meaning: product names, API and library names, protocol and standard names (OAuth, gRPC, TLS 1.3), units, version numbers, and domain terms a reader in that field expects, such as latency, throughput, or a database index. Much Vietnamese technical writing already borrows these terms straight from English (server, framework, API, deploy). Keep them as they are instead of inventing an English paraphrase for something that already has a standard name. If a term is genuinely obscure, keep it and add a short plain-English gloss in parentheses the first time it appears.

## Sound like a person wrote it

This is where machine-translated or over-polished text usually gives itself away.

**Cut these words.** They make up the strongest single AI tell in English right now, and a plainer word is almost always available: delve, tapestry, pivotal, underscore(s), foster, testament, enhance, crucial, intricate, landscape, leverage, robust, seamless, holistic, paradigm, synergy, nuanced, multifaceted, paramount, meticulous, notable / notably, showcase, spearhead, boast(s), stands as, serves as.

**Cut these fillers.** Openers that announce content instead of giving it ("In today's [X] world," "In an increasingly [X] landscape," "Without further ado," "Let's delve into"). Closers that just restate what was already said ("In conclusion," "Overall," "To sum up"). Hedges that add no real information ("it's important to note that," "arguably," "at the end of the day"). And filler adverbs that carry no meaning: really, actually, simply, basically, essentially, quite, very. Adverbs that carry real technical or timing information stay: automatically, manually, immediately, directly, asynchronously.

**Break these structures.** They read as a template running, not a person thinking:

| Pattern | Fix |
|---|---|
| "It's not just X, it's Y" | State Y. Drop the setup. |
| Three-item lists for everything ("fast, reliable, and secure") | Use two items, or one. |
| "From X to Y" implying a spectrum that is not really there | Name the two things directly. |
| Passive voice or an inanimate subject acting ("the issue was resolved," "the system ensures reliability") | Name who did it: "we fixed the issue." "The system retries failed requests automatically." |
| "..., highlighting / underscoring / reflecting the importance of..." tacked onto a sentence | Make it its own sentence, with a real subject. |
| "Plays a vital role in," "serves as a testament to," "marks a pivotal moment" | Say what actually happened. |
| Vague claims ("the implications are significant," "this is crucial") | Name the specific implication. |
| Sweeping words standing in for evidence ("always," "never," "every user") | Use the real scope, or cut the claim. |
| Rhetorical setups ("Here's what this means:", "Think about it:") | Cut straight to the point. |

**Watch the formatting.** AI-generated text tends to bold every key term, turn every list into a "Term: definition" pattern, add a header where a sentence would do, and lean on em dashes for emphasis. Skip the em dash entirely and use a comma, period, or colon instead: it is one of the most reliable tells, since people reach for it far less often than language models do. Use bullets only where a list genuinely helps, such as steps or parameters. Otherwise, write paragraphs.

**Vary the rhythm.** A tell of machine-smoothed text is every sentence landing in the same 12-to-18-word range. Put a short sentence next to a longer one, the way someone explaining this out loud actually would.

## When plain and precise pull in different directions

Accuracy wins. A simpler word that changes the technical meaning is a translation error, not an improvement. When a smoother sentence would cost an exact number, a condition, a scope boundary ("only for authenticated users," not "for users"), or a causal link from the source, keep the precise version and simplify what is around it instead.

## Delivering the output

Give the rewritten English text first, with no preamble such as "Here is the translation." Just the text, formatted to match the source: a doc stays a doc, an email stays an email, a short paragraph stays a short paragraph.

Then always add this section, titled exactly as shown, even when nothing needs flagging:

```
## Notes on potential issues
- [one specific issue: a factual error, an internal inconsistency, an outdated-looking claim, or a genuinely unclear sentence in the source]
- [repeat for each issue found]

Want me to fix or adjust any of these?
```

If nothing needs flagging, write "No factual errors, inconsistencies, or unclear statements spotted in the source." instead of the bullet list, and skip the closing question.

Keep each note to one line. This section covers the content of the source (things that look wrong, contradictory, or ambiguous), not your own translation choices. Do not use it to explain word-choice decisions you already made silently.

## Example

**Vietnamese input:**
Hệ thống của chúng tôi tận dụng kiến trúc microservices để tối ưu hóa hiệu suất và đảm bảo khả năng mở rộng liền mạch cho người dùng.

**Weak, literal, AI-sounding:**
Our system leverages a microservices architecture to optimize performance and ensure seamless scalability for users.

**What this skill should produce:**
We built the system on microservices, so it runs fast and scales easily as more users join.

Same meaning, roughly half the syllables, no stock phrases, and an actual subject doing something.
