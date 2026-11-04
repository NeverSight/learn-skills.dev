---
name: simplified-technical
description: Write or rewrite text in Simplified Technical English at roughly 80% ASD-STE100 strictness. Use when the user asks to "simplify this", "rewrite for clarity", "explain like an aircraft manual", "use STE / ASD-STE100 / simplified technical English", "de-jargon this", "make this unambiguous", or wants plain-language technical documentation. Not for creative or marketing copy.
metadata:
  author: mikekusold
  version: "1.1.0"
---

# Simplified Technical English

Write technical English that is hard to misread. Apply the high-value rules of [ASD-STE100](https://www.asd-ste100.org/) — the aerospace controlled-language standard — at about 80% strictness, an informal style target rather than a measured compliance score. Write for a reader with basic English and no context. When a rule fights clarity or natural flow, clarity wins.

## Preserve Meaning

A rewrite changes style, not facts.

- Keep every fact, condition, number, scope qualifier, time relationship, and degree of certainty from the source. Preserve the strength of requirements and recommendations.
- Never add a cause, a frequency, or a mechanism that the source did not state.
- Preserve commands, code, identifiers, paths, URLs, and exact UI labels. Rewrite the surrounding prose; do not apply word substitutions inside these literals.
- Do not guess what an ambiguous pronoun, condition, or technical term means. Keep the ambiguity if a faithful rewrite is possible. If the requested result requires resolving it, ask a focused question instead of inventing a meaning.
- If a shorter phrasing would lose precision, keep the longer phrasing. Say which phrase you kept and why.

## Words

- Use the simplest word that is correct: "use" not "utilize", "show" not "demonstrate".
- Prefer one plain verb over a phrasal verb when the meaning stays the same: "start" for "spin up", "contact" for "reach out". Keep familiar technical terms such as "back up" when a replacement would be less clear.
- Use the verb, not a noun made from the verb. Write "analyze the log", not "perform an analysis of the log".
- Cut marketing adjectives ("seamless", "robust", "cutting-edge"). Delete the adjective, or use a supporting measurement if the source supplies one. Do not invent evidence.
- Pick one meaning per word and keep it. If "enter" means "type into a field", do not also use it to mean "go into".
- Keep technical nouns and domain terms exactly as they are ("JWT", "Kubernetes pod", "cache invalidation"). Do not simplify terminology the reader needs.
- Do not drop articles (a, an, the) to save space.
- Avoid noun stacks longer than three words, except inside an exact technical term or UI label. Rewrite "database connection pool max size setting" as "the max size setting for the database connection pool" when it is prose, not a literal label.

## Sentences

- Aim for 20 words or fewer per sentence (25 for descriptive text). Preserve meaning and exact terms when these limits conflict with precision.
- One idea or one instruction per sentence.
- Do not use semicolons. Split the sentence into two sentences.
- Paragraphs: one topic, six sentences maximum.
- Put the main point first.

## Verbs

- Prefer imperative, simple present, simple past, and simple future ("will") when they preserve meaning.
  - "The job has completed" → "The job is complete" when the current state is the point.
  - Keep "The service is restarting" if the restart is in progress.
  - Keep conditional forms such as "would have been triggered" when they express a hypothetical event.
- Write in the active voice. Use passive only when the actor is unknown or irrelevant.
- Use "must" for a requirement, "should" for a recommendation, and "can" for ability or permission. Replace "shall" with "must" only when it expresses a requirement; replace permission-related "may" with "can" only when the meaning is unchanged. Preserve quoted or formally defined normative language.
- Keep hedges that report uncertainty. A hedge is content, not style. "The request may have failed" must not become "The request failed". When the tense rules conflict with a hedge, keep the hedge.
- Remove stacked hedges: "this may potentially help" → "this may help".
- Avoid unnecessary "-ing" constructions: "Close the valve by turning the handle" → "Turn the handle to close the valve." Keep progressive verbs when they convey an ongoing action, and keep technical nouns and modifiers ("the cooling fan").

## Procedures

- Write steps as a numbered list. One action per step.
- Start each step with an imperative verb ("Install...", "Check...", "Remove...").
- Preserve existing warnings and put them before the step they apply to, prefixed with "WARNING:" or "CAUTION:". Do not invent hazards in a rewrite.
- When a step has a condition, put the condition first: "If the indicator is red, stop the pump."

## Word Substitutions

Consider these substitutions only when they preserve the meaning in context:

| Instead of            | Use            |
| --------------------- | -------------- |
| additional            | more           |
| approximately         | about          |
| assist, facilitate    | help           |
| attempt               | try            |
| commence, initiate    | start          |
| concerning, regarding | about          |
| demonstrate           | show           |
| determine             | decide, find   |
| ensure                | make sure      |
| insufficient          | not enough     |
| leverage, utilize     | use            |
| may (permission)      | can            |
| obtain                | get            |
| prior to              | before         |
| provide               | give           |
| purchase              | buy            |
| require               | need           |
| shall (requirement)   | must           |
| subsequent to         | after          |
| terminate             | stop           |
| transmit              | send           |
| verify                | check          |

## Examples

**Exact label — before:**

> Prior to initiating the service, verify the Database Connection Pool Maximum Size setting.

**After:**

> Before you start the service, check the Database Connection Pool Maximum Size setting.

The setting name stays unchanged so the reader can find it in the interface.

**Description — before:**

> The authentication service utilizes JSON Web Tokens in order to facilitate stateless verification of user identity, with expired tokens being automatically refreshed.

**After:**

> The authentication service uses JSON Web Tokens to help verify user identity without keeping state. Expired tokens are refreshed automatically.

**Procedure — before:**

> Before initiating the migration, you should ensure that a backup has been created and that all active connections are terminated.

**After:**

> Before you start the migration, you should:
>
> 1. Make sure a backup exists.
> 2. Make sure all active connections are closed.

**Status message — before:**

> The deployment may have failed due to a possible timeout while the service was starting, which could be caused by insufficient resources.

**After:**

> The deployment may have failed because of a timeout during service startup. Not enough resources could have caused the timeout.

The possible deployment failure, timeout, and resource-related cause remain uncertain. A rewrite that says "The deployment failed" makes a different claim than the source.

## Stay at 80%

The goal is clarity, not compliance. Do not:

- Replace a precise technical term with vague simple words. "Authenticate" stays; do not write "make an identity check".
- Break every sentence into robotic fragments. A short sentence with a conjunction reads better than three choppy ones.
- Cut useful context or caveats to shorten text. Move them to a note instead.

For tool descriptions, error messages, and inter-agent instructions, prioritize precise conditions and terminology. Preserve machine-readable syntax and identifiers. This skill is an informal style guide, not a compliance check. When full ASD-STE100 compliance is required, use the current official standard and appropriate expert review.

## Output

- Give the rewritten text only. Do not add a preamble, a change summary, or an offer to explain more.
- If unresolved source ambiguity prevents the requested result, ask the necessary question instead of presenting a guessed rewrite.
- When you keep a longer phrasing to preserve precision, add one line after the text: "Kept as-is: <phrase> (<reason>)".
- When the user asks what changed ("show the diff", "what did you change"), give a table of rule, before, and after.
- When the input already complies, say so. Do not force changes onto clean text.
