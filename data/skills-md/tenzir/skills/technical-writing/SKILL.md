---
name: technical-writing
description: >-
  Write clear technical documentation following Tenzir's style conventions. Use
  when writing or editing docs, README files, API documentation, user guides,
  changelog descriptions, or error messages. Also use when the user asks about
  writing style, tone, formatting, capitalization rules, inclusive language, or
  how to structure technical content — even if they don't mention
  "documentation" explicitly.
---

# Technical Writing

Write clear, consistent technical documentation based on Google's developer
documentation style guide.

## Core Principles

- **Clarity over cleverness**: Prioritize understandable prose over elegant
  writing
- **Consistency matters**: Apply rules uniformly throughout a document
- **Audience-first**: Write for developers with varying English proficiency

## Voice and Tone

**Use second person**: Address the reader directly with "you."

Good: "You can configure the server by editing `config.yaml`."
Bad: "We can configure the server by editing `config.yaml`."

**Use active voice**: Make clear who performs the action.

Good: "The function returns an error code."
Bad: "An error code is returned by the function."

**Be conversational but professional**: Write naturally without slang, jargon,
or excessive formality. Use common contractions like "you're," "don't," and
"it's" to maintain an informal tone.

## What to Avoid

- **Jargon and buzzwords**: "leverage," "utilize," "synergy"
- **Filler phrases**: "please note that," "it should be noted"
- **Exclamation marks**: Reserve for genuinely exciting moments
- **Implying simplicity**: "simply," "just," "easy" (frustrates struggling
  readers)
- **Latin abbreviations**: Write "for example" not "e.g.", "that is" not "i.e."
- **Directional language**: Use "earlier/later" not "above/below"
- **Anthropomorphic language**: Don't attribute human qualities to software
  ("the system wants," "the server thinks")
- **Skipping articles**: Always include "a," "an," and "the"—even in headings

## Inclusive Language

| Avoid               | Use Instead                            |
| ------------------- | -------------------------------------- |
| blacklist/whitelist | denylist/allowlist, blocklist/safelist |
| master/slave        | primary/replica, leader/follower       |
| man-hours           | person-hours                           |
| guys                | everyone, folks, team                  |
| sanity check        | quick check, coherence check           |

## Capitalization

- **Sentence case** for headings: Capitalize only the first word and proper
  nouns
- **Product names**: Always capitalize (Tenzir, Kubernetes, Docker)
- **Acronyms**: Use standard capitalization (API, HTTP, JSON)

## Headings

- **Task headings**: Use bare infinitives ("Create an instance")
- **Concept headings**: Use noun phrases ("User authentication")
- **Hierarchy**: Don't skip levels (h1 to h3 without h2)
- **No links**: Avoid hyperlinks within headings

## Lists

**Numbered lists**: For sequential steps or ordered items.

**Bulleted lists**: For non-sequential items.

**List guidelines**:

- Introduce with a complete sentence followed by a colon
- Start each item with a capital letter
- Use parallel structure across items
- End with periods if items contain verbs or are complete sentences
- Don't use single-item lists

## Procedures

**Structure**:

1. Introduce with context
2. Number each step
3. Start steps with imperative verbs
4. State location before action

**Guidelines**:

- "In the Settings panel, click **Save**." (location before action)
- Mark optional steps with "Optional:" at the start
- Document one accessible procedure, not multiple alternatives
- Avoid "please" in instructions

## Code in Text

**Use code font** (backticks) for:

- Command-line input and output
- Filenames and paths
- Class, method, and function names
- Keywords, variables, and parameters
- HTTP status codes and methods

**Don't use code font** for:

- Product names and services
- URLs meant to be followed in a browser
- Domain names

**Grammar**: Don't inflect code elements. Write "send a `POST` request" not
"`POST` the data."

## Word Choices

| Avoid                   | Use Instead                       |
| ----------------------- | --------------------------------- |
| aka                     | also known as, or use parentheses |
| allows you to           | lets you                          |
| config                  | configuration                     |
| admin                   | administrator                     |
| click on                | click                             |
| check (checkbox)        | select                            |
| uncheck                 | clear                             |
| higher/lower (versions) | later/earlier                     |

## Formatting

- **UI elements**: Bold (**File > Save**)
- **User input**: Code font or bold, depending on context
- **New terms**: Italics on first use
- **Emphasis**: Use sparingly; prefer restructuring sentences

## Links

- Use descriptive link text that makes sense out of context
- Avoid "click here" or "this page"
- Good: "See the [authentication guide](...)."
- Bad: "Click [here](...) for more information."

## Reference Hierarchy

When style questions arise, consult in order:

1. Project-specific guidelines
2. Google Developer Documentation Style Guide
3. Merriam-Webster (spelling)
4. Chicago Manual of Style (general)
5. Microsoft Writing Style Guide (technical)
