---
name: prose
description: Draft, revise, or audit human-facing prose to remove obvious AI writing tropes while preserving meaning and voice. Use when the user explicitly invokes prose or asks to check writing for AI tells such as em dashes, contrastive pivots, forced three-item lists, abstract cliches, false suspense, patronizing analogies, pompous connector phrases, generic warmth, or grand conclusions.
disable-model-invocation: true
---

# Prose

Remove obvious AI habits without sanding away the writer's voice.

## Set the content contract

Before writing, identify the source facts, opinions, uncertainty, fixed text, and requested format. Keep this inventory private unless the user asks for it.

Treat supplied facts as a closed set when the user says to use only those facts. Every factual, causal, instructional, or benefit claim in the result must trace directly to that set. Do not add plausible usage steps, recommendations, outcomes, or product behavior.

Preserve the strength of each claim. Do not turn uncertainty into opposition, preference into certainty, possibility into fact, or a limited observation into a general conclusion.

Preserve source-supported relationships and context. Keep what causes what, what happens next, and which domain or subject the writer is discussing. When a vague conclusion contains a real topic or personal reaction, rewrite that part plainly instead of dropping it with the cliche.

Salvage concrete content embedded inside a banned pattern. Names, domains, tools, dates, and unresolved questions remain part of the source even when the surrounding sentence needs replacement. For example, rewrite "Ultimately, that tension is a testament to the changing field of X" as "I am still unsure what that tension means for X" when the source supports that uncertainty.

## Preserve the source

Keep the meaning, facts, uncertainty, stance, citations, technical terms, and requested format. Do not invent evidence, opinions, examples, or transitions.

Prefer the smallest edit that removes the problem. Do not delete concrete context merely to make the result shorter. Direct prose still needs enough source-supported detail for its audience to understand the behavior, decision, or tradeoff.

Treat quotations, code, commands, logs, citations, technical identifiers, and requested verbatim text as fixed unless the user asks to edit them. A banned pattern inside fixed text is not a prose violation.

## Revise

Scan every draft for the patterns below. Rewrite each hit or record why it is intentional.

### Dash punctuation

Do not use em dashes. Do not substitute an en dash or spaced hyphen for an em dash. Rewrite with a period, comma, colon, or cleaner sentence structure. Hyphens in compound words are fine. Preserve an en dash only when it expresses a real range or established notation.

Also remove dash clauses that staple together thoughts, introduce a dramatic pivot, or add repeated asides. Splitting the sentence is usually cleaner.

### Manufactured contrast

Remove formulas such as "not just X, but Y," "more than X," "it is not about X; it is about Y," and "this is not merely X." State the point directly. Keep a contrast only when the distinction or tradeoff matters, then name it plainly.

### Forced groups of three

Do not arrange adjectives, concepts, verbs, or examples into threes for cadence. Keep the number the subject requires. One natural three-item list is fine. Repeated tricolons are not.

### Abstract cliches

Replace portable metaphors and vague scene-setting such as "rich tapestry," "ever-evolving landscape," "vibrant ecosystem," "dynamic world," and "rapidly changing space." Name the domain, tool, event, problem, or constraint.

### False suspense

Remove teaser transitions such as "The best part?", "Here is where it gets interesting," "But the real surprise was," and "That is when everything changed." Move directly to the fact or use a modest transition tied to the source.

### Patronizing analogies

Remove "Think of it as," generic comparisons, Swiss Army knife metaphors, and "Imagine a world where." Explain the subject directly. Keep an analogy only when the audience needs it or the source depends on it.

### Pompous connector phrases

Replace "serves as," "acts as," "functions as," and "stands as" with the real verb. Prefer "shows," "connects," "revealed," or another concrete verb that matches the claim.

### Grand conclusions

Do not end by restating the theme at a higher altitude. Remove openings such as "Ultimately," "At the end of the day," "This reminds us that," "It is a testament to," and "In a world where." End with the useful next step, a concrete result, the detail that stuck, or a simple close.

### Empty human-centered polish

Replace phrases such as "deeply human," "meaningful connection," "thoughtful experience," "intentional design," and "empowering users" with the decision, behavior, quote, constraint, or result that supports the claim. If no evidence supports it, cut it.

## Keep the prose alive

Do not solve AI-sounding prose by making it sterile. Preserve specific opinions, natural rhythm, first person, useful detail, and honest uncertainty when the source supports them. Prefer concrete nouns and direct verbs. Trust the reader with straightforward ideas.

Do not replace a banned phrase with generic filler. Use a source-supported fact or end the thought earlier. Do not pad a requested length by repeating facts or inventing benefits. If the available material cannot support the requested length, favor accuracy over padding.

Meet requests for a warm, energetic, or approachable tone through word choice and rhythm. Do not turn the tone request into an unsupported claim that something is easy, friendly, empowering, or good for everyone.

Avoid slogan fragments and empty assurances such as "made easy," "a simple way," and "a friendly way." In product copy, create warmth through direct address and a useful source-supported detail. In explanations, connect the supplied facts so the reader knows what happens and what to do next, but do not add advice that the source does not support.

## Finish

Read the result once more and ask what still makes it sound generated. Correct every unintentional hit before returning it. Apply this check to every assistant-authored line, including audit items, labels, prefatory text, and exception notes.

Run these checks in order:

1. Compare each claim with the content contract. Remove additions and restore any fact, qualification, opinion, context, or degree of uncertainty lost during cleanup.
2. Remove repeated claims, including conclusions that restate an earlier sentence. In short prose, state each supplied fact once unless repeating it prevents a real ambiguity.
3. Scan every assistant-authored line for the targeted tropes.
4. Confirm the requested length, tone, and output format.

For the first check, trace every content-contract item to its wording in the result. Revise if an item has no match. Then trace every factual or benefit claim in the result back to the source. Remove anything without a match. Keep this trace private.

Search the finished response for em dashes before returning it. Check each en dash and hyphen surrounded by spaces. Keep only a legitimate range, established notation, compound-word hyphen, or punctuation inside fixed text.

For a draft or rewrite, return the requested prose in its requested format. Add an `Intentional exceptions` note only when a flagged pattern remains outside fixed text. Name the exact phrase and why it earns its place.

For an audit, use this structure for every hit:

`1. "[phrase]": [Pattern]. Why it weakens this passage: [specific reason]. Proposed revision: [specific direction or replacement].`

Use a colon or full sentence between the quoted phrase and its explanation, never dash punctuation. If the user asked you to revise the text, apply the changes instead of merely listing them.
