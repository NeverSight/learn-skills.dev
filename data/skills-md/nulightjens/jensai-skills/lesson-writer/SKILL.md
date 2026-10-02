---
name: lesson-writer
description: Write course lesson content with structural variety, in a configurable voice, output ready for course platforms. Use when drafting a new lesson, reformatting an existing one, turning an outline or transcript into teachable content, or fixing a course where every lesson reads the same. Triggers on "write a course lesson," "format course content," "rewrite this lesson," "turn this outline into a lesson," or "write lessons for my course."
argument-hint: "[source-file.md or lesson topic]"
---

# Lesson Writer

Write course lessons that teach cleanly and do not all read the same.

Most generated course content collapses into one shape: hook, "here is how it works," three bullets, a summary that restates the hook. Twelve lessons in, the reader is skimming. This skill fixes that with a **section palette** you draw from per lesson and a rotation rule that forbids two lessons in a row from using the same shape.

Two things are separated here. The **engine** (section variety, procedural rules, HTML output) lives in this file. The **voice** (word choices, stance, phrasing) lives in a single file you swap out.

## Step 0: Load the voice profile

Before writing anything, read the voice profile:

1. If the project has `voice-profile.md` at its root or in `.claude/`, use that one.
2. Otherwise read `${CLAUDE_SKILL_DIR}/voice-profile.md`, the profile shipped with this skill.
3. If the user names a different profile file, that one wins.

Everything in the profile beats everything in this file. When the profile says "no rhetorical questions" and a section below suggests one, follow the profile.

State which profile you loaded in one line before the draft, so the user knows what they are getting.

## Step 1: Set the reading level

The voice profile carries a target reading level. If it does not, default to a Flesch-Kincaid reading ease of 60 to 70, which is roughly a 7th-grade level. Short sentences, plain words. If a thirteen-year-old would stumble on a word, pick a simpler one.

Course content is read by people who are tired, on a phone, halfway through a work day. Write for that reader, not for a reviewer.

## Step 2: Pick the lesson type

Five common types, each with a different natural shape:

- **Concept lesson.** Introduces an idea or a term.
- **Build lesson.** Walks through making something.
- **Philosophy lesson.** Sets expectations or frames a module.
- **Comparison lesson.** Weighs two tools or two approaches.
- **Technical lesson.** Explains a mechanism or a setting.

The type suggests which sections fit. It does not lock them.

## The section palette

Every lesson draws 3 to 6 sections from this palette. **No two consecutive lessons use the same section order.** Track what the previous lesson used before you start the next one.

| ID | Section type | When to use | Heading style |
|----|---|---|---|
| A | Hook / opener | Every lesson, 1 to 3 sentences | No heading, just start |
| B | Concept definition | A new term or idea | Bold the term inline, no heading |
| C | Why this matters | After something abstract | h2 or h3, vary the wording each time |
| D | Analogy | A concept that needs grounding | Woven into prose, never its own heading |
| E | The flow | Build and project lessons | h2: "The flow" or "How this actually goes" |
| F | Numbered build steps | Sequential walkthrough | Numbered list under a heading |
| G | Concept breakdown | Several sub-terms to define | Bold term plus paragraph, repeated |
| H | Comparison | Tool against tool, approach against approach | h2 or h3: "X vs Y" |
| I | Example or template | A prompt, an email, a config | h3, or just a code or quote block |
| J | Gotcha / warning | A common mistake or edge case | Inline parenthetical, or bold "Warning:" |
| K | Bottom line | Wraps a section or a lesson | h2: "Bottom line", 1 to 3 sentences |
| L | Bridge to the next lesson | End of lesson | No heading. "Now let's..." / "Next up..." |
| M | Aside | Break the tension, add texture | Parenthetical or inline "Worth knowing:" |
| N | When X still makes sense | Nuance, exception, edge case | h3: "When [X] still makes sense" |
| O | Vibe / framing | Opening a module | h2: "How to think about this", or plain prose |

## Procedural rules

**Rule 1: Vary the section order between lessons.** If lesson one runs A, D, E, F, then lesson two opens somewhere else. Keep a running list of the orders you have used in this module.

**Rule 2: Three to six sections per lesson.** Not every section appears in every lesson. A concept lesson and a build lesson should not draw the same cards.

**Rule 3: No standing heading.** "Here is how it works" is one option among several, not the default. Rotate through "The flow," "How this actually goes," or no heading at all, launching straight into the steps.

**Rule 4: Analogies go into prose.** No lesson gets a heading like "The big idea" or "The analogy." Weave it into the paragraph where the concept lands.

**Rule 5: Lessons bridge into each other.** Close with a forward move: "Now let's..." / "That takes us to..." / "Next up we are going to..." A course is a sequence, not a pile.

**Rule 6: Hyperlink every external reference.** Every tool, platform, or resource gets `<a href="URL">text</a>`. Never name a tool without linking it when a URL exists.

**Rule 7: Bold for emphasis, not for structure.** Bold individual words inside paragraphs. Never build a vertical list of "**Term:** description" lines. That pattern is the single loudest sign of machine-assembled course copy.

**Rule 8: Vary list types.** Bullets for unordered ideas, numbers for sequential steps, no list at all when there are only two or three items. Mix within a lesson. Never make every list exactly five items long.

**Rule 9: Exercises live in the module wrap-up.** Lessons carry instruction. Practice prompts, homework, and "try this now" blocks collect in the wrap-up page so learners know where to find them.

**Rule 10: The wrap-up is the one page with a fixed format.** Consistency helps here because learners return to it:

1. `<h2>Try these now</h2>`, the exercises from every lesson in the module
2. `<h2>What you built in this module</h2>`, a bullet summary
3. `<h2>Share what you made</h2>`, a prompt to post the result

## Structural craft

Surface bans (word swaps, banned phrases) do not remove the structural fingerprint of generated writing. Light editing changes the vocabulary and leaves the shape intact. These four rules work on the shape.

**Teach the concept once, early, clearly.** Do not restate it as a moral at the end of the section. The closing lesson-statement is the most common structural tell in generated teaching content, and it also insults the reader, who just read the thing.

**Ration the "Bottom line" section to one lesson in three.** A wrap-up slot that appears every single time is a template, and learners feel it by lesson four even if they cannot name it.

**Name feelings plainly when a story calls for one.** "That one stung" reads as human. "My stomach dropped" reads as performed. Physical emotion writing is where generated prose overreaches hardest.

**Name real things.** Actual tools, prices, versions, dates, people. "A popular automation tool" is a tell. "Zapier, on the $29 plan" is teaching.

## Example lesson shapes

These show variety, not a menu to cycle through in order.

**Concept lesson:** A (hook), D (analogy in prose), G (breakdown with bold inline terms), C (why this matters), L (bridge)

**Build lesson:** A (hook), C (why this matters, with numbers), E (the flow), F (numbered steps), J (gotcha), K (bottom line), L (bridge)

**Philosophy lesson:** A (hook), O (framing), D (analogy), C (why we care), G (concepts), L (bridge)

**Comparison lesson:** A (hook), D (analogy), H (comparison), N (when X still makes sense), K (bottom line)

**Technical lesson:** A (hook), B (concept defined inline), F (steps), M (aside), L (bridge)

## Banned content

See [references/banned-content.md](references/banned-content.md) for the full list of words, phrases, and patterns to keep out of lessons regardless of the voice profile.

Headline bans: delve, leverage as a verb, comprehensive, transformative, crucial, em dashes, "In today's fast-paced world," formal connectives (Moreover, Furthermore, Additionally), formal closers (In conclusion, In summary), Title Case In Headings.

## Output format

Output clean HTML that pastes into a course platform editor. Most editors, including Skool, Teachable, and Circle, accept a narrow set of tags:

- `<h2>` for major sections, `<h3>` for subsections
- `<p>` for paragraphs
- `<strong>` for emphasis
- `<a href="URL">text</a>` for links
- `<ol>` and `<ul>` for lists
- `<code>` for inline technical terms
- Sentence case for every heading

Keep a lesson under roughly 3,000 characters of HTML. Some editors, Skool among them, cap the field, and a lesson longer than that is usually two lessons anyway.

If the target platform accepts Markdown instead, say so and emit Markdown with the same section structure.

## Workflow

1. Read the source: an outline, a transcript, a draft, or a topic brief.
2. Load the voice profile and name it in one line.
3. Pick the lesson type, then select 3 to 6 sections that fit the content.
4. Check the section order against the previous lesson. If it matches, change it.
5. Write the lesson at the target reading level.
6. Run the banned content list and the pre-publish checklist.
7. Emit the HTML.

## Pre-publish checklist

- [ ] Voice profile loaded and named at the top of the response
- [ ] Section order differs from the previous lesson
- [ ] Between 3 and 6 sections used
- [ ] Opens in 1 to 3 sentences with no throat-clearing
- [ ] Reading level hits the profile's target
- [ ] Sentence and paragraph lengths vary noticeably
- [ ] Every tool and resource is hyperlinked
- [ ] Bold used for emphasis only, no "**Term:** description" lists
- [ ] Lists vary in type and length, none of them exactly five items
- [ ] "Bottom line" appears in at most one lesson of every three
- [ ] The concept is taught once and not restated as a closing moral
- [ ] Every reference names a real thing, not a category
- [ ] No em dashes, use commas, colons, or parentheses
- [ ] Nothing from the banned words and phrases list
- [ ] Exercises pushed to the module wrap-up, not left in the lesson
- [ ] Lesson closes with a bridge into the next one
- [ ] Headings are sentence case
- [ ] HTML uses only the supported tags

## Building your own voice profile

Copy `voice-profile.md`, keep the section headings, and replace the contents. The headings are the contract the engine reads, so do not rename them.

If you have 5 or more pieces of the instructor's existing writing or transcripts, mine those instead of guessing. Pull the recurring words, the way they open an explanation, their average sentence length, and the moves they never make. A real corpus beats self-description, because people describe the voice they want rather than the one they have.

The `brand-voice-extractor` skill in this collection runs an interview that produces a structured profile you can paste straight into `voice-profile.md`.

## Working with the user

- Ask what the lesson teaches and what the learner should be able to do afterward. Two questions, not an intake form.
- Ask for the specifics: the tool names, the prices, the settings, the screenshots. A lesson with no specifics is where a model starts inventing.
- If a module has a running section-order log, read it before writing. If it does not, start one.
- Deliver the lesson, then offer one concrete revision angle rather than a list of options.

## Related skills

- `skool-course` publishes the resulting HTML to a Skool classroom through browser automation.
- `brand-voice-extractor` generates the `voice-profile.md` this skill reads.
- `blog-writer` applies the same engine-plus-profile split to long-form posts.
