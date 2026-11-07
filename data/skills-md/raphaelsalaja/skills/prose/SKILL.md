---
name: prose
description: Writes posts and breakdowns that open on where the author stands, show the options that lost, give exact numbers and mark every guess as a guess.
---

# Prose

This skill writes and reviews long-form text: posts, breakdowns, case studies and design notes. It explains each decision through the problem it solved and the options it beat, in plain sentences told by the person who did the work.

## Facts are exact, the voice is the author's

A guess stated as fact, an uncited claim and an experience the author never described are findings every time. Style rules bend to the author's draft. Their tense and register stay, and so does their choice of I or we.

Interface labels, em dashes and ellipses belong to `copy`. Commit messages belong to `ship`.

## Open on where you stand

The first paragraph says what the piece is about and where the author stands: they built it, rebuilt it, use it or noticed it. The problem it answers arrives by the end of that paragraph. A line on what the piece isn't is welcome.

A contents list, "In this post I'll cover" or a feature tour as the opener is `prose-open-with-context`.

## Tell it in the first person

The author is in the piece. "I" covers their own work and "we" a team's, saying what they built, tried, saw and dropped. A breakdown nobody seems to have written is `prose-first-person`.

## Each decision names what it beat

State the choice, then at least one option that was considered and why it lost. "The highlight is an inset pill" with nothing beside it is `prose-show-the-alternatives`.

The reason is what the choice does for the person using it. "This makes it feel snappy" is `prose-reason-for-the-person`.

## Numbers, not adjectives

Where a value exists, write the value. "A really fast spring" is `prose-specifics`. Words like seamless, robust, powerful, blazing and delightful are `prose-no-hype`.

## Sentences carry their reasons

A fact travels with its consequence in the same sentence, joined by so, but or because. A reason left for the next sentence, or for the reader to supply, is `prose-link-the-reason`.

There is no word limit. Length is judged by ear, and a sentence that needs a second read is split. A run of short sentences or fragments for emphasis is `prose-no-fragment-runs`.

## Lists live in the sentence

A list of two to four items goes inside one sentence, after a colon. A row of fragments standing in for that sentence is `prose-list-in-the-sentence`.

When the items need explaining, each one carries its gloss in brackets: spacing (a scale someone chose and stuck to), type (a size and line height tuned together). Glosses split into separate sentences are `prose-gloss-in-brackets`.

## Tell what happened

Process is told as what the author did, in the past tense: I'd record the screen, play it back slowly and rebuild it beside the recording. Present-tense advice with no account of doing it is `prose-tell-what-happened`.

## Talk about the work, not at the reader

Describe what the thing does and what the author did. Address the reader as you only when they are about to act, such as trying a demo. A run of instructions to the reader is `prose-fewer-you`.

## Admit the limits of your own work

Say in passing where the author's own work falls short, without apology: the first version is always close and always wrong. A piece about the author's own work that claims no limits is `prose-admit-the-limits`.

Delete throat-clearing such as "It's worth noting", "Let's dive in" and "Not just X, but Y". That is `prose-no-filler`.

## Asides sit in brackets

An aside steps out of the argument for a moment: an admission, a credit or a joke. It sits in brackets, runs under 15 words and appears at most once a section. A gloss on a list item is not an aside.

An aside that carries the argument, or a second aside in one section, is `prose-asides`.

## Footnotes hold asides as well as sources

A footnote can carry a personal aside: the caveat, the attempt that failed, the story behind a number. A caveat that breaks the main line moves to a footnote. Leaving it inline is `prose-footnote-the-caveat`.

## Say how you know

Each fact says where it came from: inspected, measured, read in the source or quoted. A value with no method is `prose-say-how-you-know`.

A claim from someone else carries a footnote linking the original. "Navigation got 30% faster" with no link is `prose-cite-claims`.

## Mark guesses as guesses

An inference reads as one: "I think", "my guess is", "the way I read it". A motive stated as fact is `prose-mark-the-guess`. A measured fact wrapped in "I believe" is `prose-no-hedged-facts`.

## Never invent the author's experience

Writing for someone else, add no anecdote, feeling or attempt they did not describe. That covers asides, footnote stories, accounts of what happened and admitted limits. "At first I wondered why" is `prose-no-invented-experience`. Ask for the real moment or leave the line out.

## Edit the words, keep the voice

Fix spelling, grammar and order in the author's draft. Rewriting their register into yours is `prose-keep-the-voice`.

## Spelling is British

Running text uses British spelling: colour, behaviour, centre, grey, favourite, customise, recognise, organise and judgement. Code, CSS and API names, interface labels and quoted titles keep their own spelling. "Color" in a sentence is `prose-british-spelling`.

## Show what has shape

A sequence of steps, a comparison or a set of values goes in a list, table or figure. Five shortcuts strung through one paragraph is `prose-show-the-shape`.

## Captions say what happens

A caption under a demo or figure describes what happens in it, in order: the menu grows out of the button, the shadow arrives on the fourth frame and the content on the sixth. A caption that states the lesson is `prose-caption-the-action`.

## End modestly

The last line of a piece is plain: what the work does for now, what is next or how the author feels about it. A punchline, an aphorism or a summary of the headings as the ending is `prose-modest-ending`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `prose-open-with-context` | `In this post I'll cover anatomy, motion and keys.` | `I rebuilt a command menu I open a hundred times a day. This isn't a tutorial. It's what I found taking it apart.` |
| `prose-first-person` | `The menu was rebuilt from inspect element and the source.` | `I rebuilt the menu from inspect element and the source.` |
| `prose-show-the-alternatives` | `The highlight is an inset pill.` | `A full-width stripe reads like a table. An inset pill reads like something you hold.` |
| `prose-reason-for-the-person` | `This makes it feel snappy.` | `The height moves on the same keystroke that changed the list.` |
| `prose-specifics` | `A really fast spring` | `A stiffness of 20000, settled in about a tenth of a second` |
| `prose-no-hype` | `A seamless, powerful menu` | `A menu that never makes you wait` |
| `prose-link-the-reason` | `Rows have fixed heights. The frame never measures itself.` | `Rows have fixed heights, so the frame never has to measure itself.` |
| `prose-no-fragment-runs` | `The page works. You don't want to stay.` | `The page works, but nobody wants to stay on it.` |
| `prose-list-in-the-sentence` | `Spacing that's off. A hover that scales. Copy that says nothing.` | `What it misses is small: spacing that's off, a hover that scales and copy that says nothing.` |
| `prose-gloss-in-brackets` | `Under the surface there's a spacing scale. Someone chose it and stuck to it.` | `Under the surface sit spacing (a scale someone chose and stuck to) and type (a size and line height tuned together).` |
| `prose-tell-what-happened` | `Record it, then rebuild it beside the recording.` | `I'd record it, then rebuild it beside the recording until I couldn't tell them apart.` |
| `prose-fewer-you` | `You open the menu. You watch it grow. You notice the corner.` | `The menu grows from the corner of the button that opened it.` |
| `prose-admit-the-limits` | A breakdown of your own rebuild that claims it matches the original | `My version only covers part of it, but it was enough to understand how it works.` |
| `prose-no-filler` | `It's worth noting that rows are 46 tall.` | `Rows are 46 tall.` |
| `prose-asides` | `Note that this is not a criticism of the team that built it.` | `(Not a knock on the team, who ship careful work.)` |
| `prose-footnote-the-caveat` | `The list is pinned to the top, though at first it was centred and that moved every card.` | `The list is pinned to the top.[^1]` with the centred version in the footnote |
| `prose-say-how-you-know` | `The spring has a stiffness of 20000.` | `The spring has a stiffness of 20000, the number in their code.` |
| `prose-cite-claims` | `Navigation got 30% faster.` | `Navigation got 30% faster.[^1]` with the source linked |
| `prose-mark-the-guess` | `They did this to stop the highlight flickering.` | `I think they did this to stop the highlight flickering.` |
| `prose-no-hedged-facts` | `I believe rows are 46 tall.` | `Rows are 46 tall.` |
| `prose-no-invented-experience` | `At first I wondered why there's no bounce.` | `Why no bounce at all?` |
| `prose-keep-the-voice` | `I thought I might try my hand` rewritten as `This project explores` | `I thought I'd try my hand` |
| `prose-british-spelling` | `The color fades from the center.` | `The colour fades from the centre.` |
| `prose-show-the-shape` | Five shortcuts in one paragraph | A keymap table |
| `prose-caption-the-action` | `The second version has fewer things in it.` | `The card loses its gradient, its sparkle and its entrance, and the button answers a press.` |
| `prose-modest-ending` | `The best compliment a tool can get is that someone forgets it's there.` | `That's why I keep coming back to quiet software, and it's the kind I try to build.` |

## Reporting

**Severity.** `HIGH` is an invented experience, a guess stated as fact or an uncited claim. `MEDIUM` is a decision with no alternative, an adjective where a number exists, hype or filler. It is also an opener with no context, a breakdown with nobody in it or a rewritten voice. So is advice with no account of doing it, or own work with no limits. `LOW` is an unlinked reason, a fragment run, a list or gloss split into sentences or too much you. It is also an American spelling, an inline caveat, a misused aside, a lesson caption, prose that should be a table or a punchline ending.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Never `Approve` a file you did not read. Mark every check you could not run as `Not verified`.
