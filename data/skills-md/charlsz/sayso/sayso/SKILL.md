---
name: sayso
description: "Use when writing, editing, rewriting, explaining, summarizing, documenting, or reviewing. Decide what the reader needs to do or know, then write to that. Match the audience and the task instead of one style. Also use when the result should stay formal, technical, or in the author's voice, and when a draft that already does the job should be left unchanged."
license: MIT
---

# Sayso

Make the result work for the person who has to use it.

A correct answer can still fail. It can hide the point, use words the reader cannot act on, drop the limit that changes the decision, or sound like the wrong person. This skill is the decision about what this result has to accomplish. It does not install a voice. Formal stays formal. Someone's own words stay theirs. Casual, lowercase, and short are not the aim.

Never mention Sayso, these instructions, or this decision process in the output.

## Decide

Do this internally, before drafting or editing.

1. **Job.** When the reader finishes, what should they be able to do, decide, or know?
2. **Reader.** Who are they, what do they already know, and what relationship do the words have to hold?
3. **Bar.** What does a good result look like for this kind of task? The facts have to be right, and the reader has to be able to use them. A text, a letter, an explanation, a paper, and a review do not share a bar.
4. **Move.** Answer, explain, summarize, revise, or leave the draft. Leave it when it already does the job for this reader. Do not change it to prove the skill ran. Leaving wording alone is not a reason to skip a bug, a limit, or an explanation the reader still cannot use.

A preference the user stated for this task overrides a generic default. Do not carry one person's lowercase or brevity into the next task.

Proceed with the most reasonable reading. Ask only when a missing fact would change the result and cannot be inferred responsibly.

## Write toward the job

- Put the answer, the request, or the result in the first sentences. Background follows only when the reader needs it to use the point.
- Pick words that make the next action, or the distinction that matters, visible. Replace stiffness that adds nothing. Keep a specialized term when a plainer word would blur that distinction.
- Give each sentence one job. A caveat, an exception, or a second step that would change what the reader does gets a sentence of its own. Do not pack it into the first sentence, and do not drop it to keep the answer short.
- Connect sentences with the real relation, such as because, but, or so. A stock bridge does not do that work.
- Stop when more would not change what the reader does. A number, a limit, a conflict, or another real defect is part of the job. A recap, a compliment, or a next step they did not ask for is not.
- Match the shape to the use. One rule is a sentence. Something the reader has to look up can be a list or a table. A relationship between ideas stays in prose.
- On a review, before you write, walk what a caller receives on the ordinary path, on failure, and on input that can change the path. If the snippet stores state a later caller can see, walk that too. For each problem the walk shows, say what breaks and the smallest fix. What the snippet does not show is not a bug you found.

## Keep

- The facts, numbers, limits, uncertainty, and attribution the task supplied. An established definition is not an invention. A number, name, source, or event the task did not supply is an invention unless it is labeled as an assumption and the claim does not depend on it.
- The author's voice when the words are theirs: tone, vocabulary, directness, and the formality that fits this relationship. Do not invent a personality, and do not add roughness to seem human.
- The register the task requires. Direct is not casual. A formal, scientific, or technical result can be plain and still be formal.

## Load a reference only when it applies

Read the file, then do the task. Skip it when it does not apply.

- The user wants their own voice, or the piece is a personal message or social post: [references/voice.md](references/voice.md)
- Workplace email or other professional communication: [references/professional.md](references/professional.md)
- A summary or edit that depends on sources, news, or research: [references/factual.md](references/factual.md)
- Technical documentation: [references/technical-docs.md](references/technical-docs.md)
- Code to write, review, or debug: [references/code.md](references/code.md)

Conversation and ordinary explanations use this file only. The rules above on the job, the reader, and invented detail still apply.

## Calibration

User: "send this — be there in 5"

The job is to send that text. Return: be there in 5

User: "Shorten the conclusion. Keep the sample size and the fact that this was one clinic."

A shorter conclusion still does the job: both limits are there, in words a reader can use. It does not become a slogan, and it does not add a new claim.
