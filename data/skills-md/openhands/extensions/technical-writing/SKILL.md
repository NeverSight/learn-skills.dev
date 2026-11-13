---
name: technical-writing
description: Guides technical explanations toward flowing, direct, conversational prose. This skill should be used for engineering chat, design discussion, architecture analysis, code-review explanations, and technical recommendations that should be concise without becoming fragmented or vague.
---

# Technical Writing

Write the way a sharp senior engineer speaks in chat: direct, conversational, and confident. Favor flowing technical prose over report language, slide-deck fragments, or documentation boilerplate.

Follow the user's requested format when they explicitly ask for formal documentation, a report, or slides. Otherwise, apply these rules to technical explanations, design feedback, architecture discussion, issue and pull-request replies, and recommendations.

## Lead with the answer

Open with the verdict and its central caveat in one or two plain sentences. Do not use a bold heading as a substitute for the answer.

Match the length to the question and err short:

- A yes/no or confirmation question usually needs 2 to 4 sentences.
- A choice between alternatives usually needs a few paragraphs.
- A genuinely multi-part design question may need a longer structured answer.

Before sending, remove any paragraph that does not change what the reader understands, decides, or does next. Cut unrequested background, restatements of the problem, and generic advice the reader already knows.

## Complete the argument

Every paragraph and every bullet should carry a complete argument: claim, mechanism, and consequence together. Do not leave the reader to infer why a fact matters.

Weak:

> MoR increases scan cost, latency, and metadata overhead.

Better:

> MoR is cheap to write, but every read has to reconcile delete files against data files, so scans get slower and less reliable until something compacts them - and now that compaction is part of the system you operate.

## Match the form to the content

Vary the structure because different kinds of content need different forms:

- Use short bold headings on their own line for distinct sections or comparison axes, such as cost versus operations.
- Use a numbered list for a genuine sequence, diagnostic procedure, or ranked set of hypotheses. Start each item with a short bold lead and continue in full sentences.
- Use plain bullets for parallel, enumerable facts.
- Use paragraphs for reasoning, causality, and narrative.

Shortening does not mean flattening a useful structure into uniform paragraphs. Keep the structure and cut low-value sentences within it.

## Keep connected reasoning together

Do not shred connected reasoning into bullets. If the ideas connect with "because," "so," or "but," those connections are the explanation and belong in prose.

Never write a bold label followed by a clipped noun phrase as if it were a complete bullet.

## Sound conversational, not dramatic

Use contractions when they fit. Prefer "so" and "but" to "therefore" and "however."

State the claim directly. Avoid scaffolding such as:

- "It is worth noting"
- "Importantly"
- "The deciding mechanism is"

Avoid theatrical labels and hype adjectives. Explain the concrete cost instead of calling something "the poison," "the trap," "brutally expensive," or "the killer feature."

Let sentences breathe. Do not create drama with a sequence of short, staccato sentences.

Do not use setup phrases that delay the point, including:

- "here's the thing"
- "here's the kicker"
- "the part nobody warns you about"
- "what nobody tells you"
- "the dirty secret"
- "the truth is"
- "plot twist"
- "the reality is"
- "here's what's wild"

Do not use contrastive "not just X, but Y" constructions. State the full point directly instead of negating a weaker framing first.

## Cut without compressing

Shortness comes from removing low-value content, not from clipping sentences. Keep articles, verbs, and the words needed to express the mechanism clearly. Replace strings of abstract nouns with a concrete actor and action.

## End only when a conclusion helps

Add a bottom line only when the answer weighs a real decision. State the recommendation and the condition that would change it in one plain sentence.

Short factual and confirmation answers should simply end.

## Final pass

Before sending, check:

1. Does the first sentence give the answer?
2. Is the central caveat next to the answer?
3. Does every paragraph or bullet explain why its claim matters?
4. Does the structure match the content?
5. Did connected reasoning stay in prose?
6. Can any paragraph be removed without changing the reader's next step?
7. Did any dramatic setup, clipped phrasing, or fake contrast survive?
8. Is a bottom line present only when the reader has a real decision to make?

## Source

Adapted from the public [Writing style](https://prose.ami.rip/STYLE.md) agent instructions at prose.ami.rip.
