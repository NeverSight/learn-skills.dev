---
name: writing-for-interfaces
description: >
  Use when someone asks to write, rewrite, review, or improve text that appears inside a
  product or interface. Examples: "review the UX copy", "is there a better way to phrase
  this", "rewrite this error message", "write copy for this screen/flow/page", reviewing
  button labels, improving CLI output messages, writing onboarding copy, settings
  descriptions, or confirmation dialogs. Trigger whenever the request involves wording shown
  to end users inside software — apps, web, CLI, email notifications, modals, tooltips,
  empty states, or alerts. Also trigger for vague requests like "review the UX" where
  interface copy review is implied. Do NOT trigger for content marketing, blog posts, app
  store listings, API docs, brand guides, cover letters, or interview questions — this is a
  technical writing skill for interface language.
---

# Writing for Interfaces

Good interface writing is invisible. When words work seamlessly with design, people don't
notice them.

Writing should be part of the design process from the start, not something filled in at the
end. When words are considered alongside layout, interaction, and visual design, the result
feels seamless. When they're an afterthought, product experiences feel stitched together.

Every piece of text in an interface is a small act of communication: it should respect the
person's time, meet them where they are, and help them move forward.

---

## When triggered

### Step 1: Establish voice and personality

Voice is the foundation. All copy decisions — what to say, how to say it, what to leave
out — flow from a clear understanding of who this product is, who it's for, and how it
should sound. Without a defined voice, copy becomes inconsistent and the product loses coherency.

**Search for an existing voice definition.** Check for any of the following:

- A `CLAUDE.md`, `AGENTS.md`, or similar project configuration file that defines voice and/or tone
- A style guide, design system documentation, or brand guidelines
- A word list or terminology reference

**If a voice definition exists**, use it as the lens for all copy work. Confirm it still
feels consistent with the copy you're being asked to work on. If it doesn't, flag the
drift.

**If no voice definition exists**, evaluate the existing copy to infer the current voice.
Look for patterns: is the language formal or casual? Technical or plain? Warm or
matter-of-fact? If the existing copy is inconsistent or there isn't enough to infer from,
help the user establish a voice before writing anything.

#### Establishing voice through conversation

Walk the user through these questions. The answers shape everything that follows.

1. **What does the product do and who is it for?** A banking app for professionals and a
   savings app for kids serve similar purposes but should sound completely different. The
   audience determines vocabulary, complexity, and register.

2. **Why do people use it, and where?** Someone using a health app during a crisis needs
   calm clarity. Someone browsing a game at home can handle playfulness. The context of use
   — physical environment, emotional state, competing attention — shapes how much text
   people can absorb and what tone they need and which voice is appropriate.

3. **Imagine the product as a person. What personality traits make them unique?** Encourage
   the user to brainstorm freely — smart, playful, calm, authoritative, warm, no-nonsense —
   then group similar words into themes. Discard traits that are table stakes ("not
   confusing") and keep the ones that genuinely differentiate the product's personality.
   Aim for 3–4 key qualities that define the voice.

4. **Look for productive tensions.** The best voice definitions have qualities that push
   against each other in useful ways. "Friendly" and "concise" create a tension that helps
   modulate tone — if you add a word for friendliness, you sacrifice some brevity, and vice
   versa. These tensions become the dials you turn when adjusting tone for different
   situations.

5. **Capture it.** Suggest the user write the voice definition somewhere durable — a
   `CLAUDE.md`, a design doc, a style guide — so it persists across sessions and
   contributors. A word list pairs well with this and helps prevent terminology drift.

### Step 2: Evaluate the request

With the voice established, identify what kind of copy work is needed:

- **New copy**: Writing from scratch for a screen, flow, or component.
- **Review**: Evaluating existing copy for clarity, consistency, and tone.
- **Rewrite**: Improving specific text that isn't working.
- **Terminology**: Building or maintaining a word list.

Then identify which interface patterns are involved
and consult `references/patterns.md` for the relevant sections.

### Step 3: Apply voice, then principles

For every piece of copy, work in this order:

1. **Does it sound like the voice?** Read it against the 3–4 qualities. If you read it
   aloud, would you recognise it as coming from this product?
2. **Which qualities need dialing up or down for this situation?** Think of each voice
   quality as a dial. A celebratory moment turns up warmth; an error turns up clarity.
   No quality should ever be fully off — you never want to be unclear, or unhelpful, or
   cold. It's about emphasis.
3. **Apply the core principles** (purpose, anticipation, context, empathy — detailed below).
4. **Apply the craft rules** (remove filler, avoid repetition, be specific, lead with the
   why — detailed below).

When reviewing copy across multiple screens or files, flag terminology inconsistencies and
suggest word list entries for new, missing or ambiguous terms.

### Step 4: Deliver changes

Provide specific rewrites inline — show the original, then the rewrite, with a brief
rationale tied to the voice and principles. Prioritise changes that confuse or block users
before polish. The user should be able to review the changes and approve or reject them.

---

## Voice and tone

### Voice vs. tone

**Voice** is the consistent personality of the product — the 3–4 qualities that define how
it always sounds. These don't change.

**Tone** is how the voice adapts to the situation. Think of each voice quality as a dial you
can turn up or down depending on the moment:

- Celebrating a milestone? Turn up warmth, dial back brevity.
- Reporting an error? Turn up clarity and helpfulness, dial back friendliness.
- Onboarding a new user? Balance helpfulness with warmth.
- Confirming a destructive action? Turn up direct, keep calm and concise.

No quality should ever be turned all the way off.

### Applying tone: a practical method

1. Pick the 3–4 qualities that define the voice.
2. For the specific situation, decide which qualities need emphasis.
3. Place each quality on a spectrum from low to high emphasis.
4. Write with that balance.

**Example**: For an error where someone can't connect to the network, clarity and
helpfulness go way up — the person needs to know exactly what to do. Simplicity stays
moderate because they need the most important details. Friendliness dials back because getting them
unstuck is more important than sounding warm.

### Voice should never override usefulness

Personality shines in moments where it can — welcome screens, milestones, empty states.
Don't force it into error messages or critical flows. If voice gets in the way of clarity,
clarity wins every time. This is especially true for error messages, destructive actions and
situations where the writing is articulating a problem.

---

## Core principles

These four principles — Purpose, Anticipation, Context, Empathy — form a framework for
thinking about what to write, how to write it, and when. They apply through the lens of
your voice.

### 1. Purpose

Every screen, every message, every label exists to help someone do something or understand
something. Before writing, answer: **what is the single most important thing the person
needs to know right now?**

- **Use information hierarchy to signal what matters most.** Headlines and buttons carry the
  primary message. Supporting text fills in detail. People often read headers and buttons
  first — if someone reads only those, they should understand the situation.
- **Know what to leave out.** If information doesn't serve the purpose of this moment, move
  it elsewhere or cut it. When a screen is trying to do too much, go back to its purpose
  and strip away everything that doesn't serve it.
- **Have a purpose for every screen in a flow.** Define the purpose of the entire flow and
  each screen within it. This prevents redundant steps and keeps things brief.
- **Tell people the purpose — it's not a secret.** When introducing a feature, tell them
  why it exists and why it matters to them using the voice and tone as appropriate
  to the situation.

### 2. Anticipation

Think of the interface as a conversation. In any good conversation there's a natural back
and forth — listening, responding, anticipating what the other person needs to hear next.

- After telling someone about a problem, tell them how to fix it.
- After asking someone to do something, make it obvious how to do it.
- After someone completes something, acknowledge it and point forward.
- **Lead with the "why".** Put the benefit or reason before the instruction. "To get
  reservation updates, enter your phone number" is stronger than the reverse — the benefit
  is front-loaded where it has the most impact.

### 3. Context

People use products in wildly different circumstances — on a busy train, mid-conversation,
one-handed, in a crisis, at 2am. The usage context shapes the writing

- **Think outside the app.** Consider the physical and emotional situation. Someone getting
  a health alert needs calm clarity; someone mid-exercise needs ultra-brief text they can
  read at a glance.
- **Match density to available attention.** Mid-task text should be ultra-brief. Setup flows
  can afford a bit more. Bigger screens require brevity too, because text must be large for
  people to see it from a distance.
- **Timing matters.** Show information when it's relevant, not before. Place instructions
  where the person is looking — if they're focused on a camera viewfinder, overlay the
  instruction near their focal point.
- **Write for the device.** Screen size, input method, and usage patterns differ across
  devices and media. Describe gestures correctly — don't say "click" on a touch device. Consider
  that phones and watches offer personalisation but demand brevity; shared screens like TVs
  may be seen by multiple people.

### 4. Empathy

You're writing for everyone who might use this product — different abilities, languages,
cultures, levels of technical fluency, and emotional states.

- **Use plain, direct language.** Avoid jargon, idioms, and culturally specific references
  that may not translate.
- **Design for accessibility from the start.** Labels, descriptions, and alt text aren't
  afterthoughts — for some people, they're the entire experience. Every interactive element
  and every meaningful visual needs a thoughtful text label (see patterns reference for
  detailed guidance).
- **Avoid unnecessary references to gender, age, or ability.** Use inclusive, neutral
  language.
- **Consider localisation.** Text expands and contracts across languages. Some languages
  read right-to-left. Abbreviations work differently. Your UI needs to accommodate these
  changes — design short copy, not compressed long copy.

---

## Writing craft

These are the practical editing moves that tighten copy. Apply them after you've confirmed
the voice and tone are right.

### Remove filler words

Interface text has no minimum word count. Every word must earn its place.

- **Adverbs and adjectives**: "Simply enter your license plate" → "Enter your license
  plate." Words like "simply," "quickly," "easily," "just", "yet", "successfully", "soon" promise
  something about the person's experience that you can't guarantee. However, a descriptive word
  that genuinely clarifies behaviour earns its place: "Feed your pets automatically" tells you something
  "Feed your pets" doesn't. The test: does the word add meaning in this context, or is it filler?
- **Interjections**: "Uh oh!", "Oops!", "Oh no!" in error messages can sound like you're
  not taking the problem seriously. Cut them.
- **Pleasantries**: "Sorry" and "please" can sound insincere in automated messages. Use
  them only when they genuinely add warmth, not as padding.
- **Unnecessary punctuation**: Exclamation marks should be rare. If everything is exciting,
  nothing is. Reserve them for genuinely celebratory moments.

**The test**: read the sentence without the word. If the meaning is unchanged, remove it.

### Avoid repetition

Saying the same thing twice in different words is filler. Combine overlapping ideas into one
clear statement.

"We're running late. Your delivery driver won't make it on time. They'll be there in 10
minutes." → "Delivery delayed 10 minutes. Check the app for your driver's location."

When headline and body say the same thing in different words, collapse them. Each element
on screen should add new information.

### Be specific, not vague

- Name the thing: "Can't open 'Quarterly Report.pdf'" not "Can't open this file."
- Name the action: "Cancel Subscription" / "Keep Subscription" not "Yes" / "No."
- Give real information: "Your card ending in 4242 was declined" not "There was a payment
  error."

### Lead with the why

Messaging is most effective when you tell people why the next step matters before telling
them what it is. Structure as: "To [benefit], [instruction]."

- "To keep your streak, solve today's crossword" beats the reverse.
- "To get reservation updates, enter your phone number" beats the reverse.

This small reordering front-loads the motivation and makes the instruction feel like a
reasonable ask instead of a demand.

### Keep a word list

Decide what you call things and stick to it. If you call it an "alias" on one screen, don't
call it a "username" on another.

A word list is a simple table: **Use** / **Don't use** / **Definition**. It prevents
terminology drift and helps anyone working on the product write consistently. Button labels
are especially good word list entries — if "Next" advances through a flow, use "Next"
everywhere, not "Continue" on one screen and "Proceed" on another.

Start small. Add a word at a time. As the list grows, it becomes a resource that defines how
the product sounds. The list should be exist as part of the product's documentation and
updated as the product evolves.

### Use possessive pronouns sparingly

"Favorites" conveys the same message as "Your Favorites" and is more succinct. If you do use
possessive pronouns, be consistent and try not to switch perspectives. Avoid "we" — it's
often unclear who "we" refers to, and in error messages ("We're having trouble loading this
content") it obscures what actually happened. "Unable to load content" is clearer.

### Sweat the details

Correct spelling, grammar, and punctuation make a product feel polished and trustworthy.
Inconsistent capitalisation, stray punctuation, or typos erode confidence — especially in
moments where trust matters (payments, permissions, health data).

Adopt capitalisation rules that align with the voice, then apply them consistently. Title
case reads as formal; sentence case reads as casual. Choose a style for each UI element type
and use it throughout.

Write for the space available. Buttons, notification titles, tooltips, and labels all have
limited screen real estate. If copy needs to be short, write a short sentence — don't
compress a long one.

### Build language patterns

Consistency builds familiarity. When the same type of situation always uses the same
structure, the product feels cohesive and intuitive. Define patterns for common moments —
how flows begin ("Get Started"), how they advance ("Next" or "Continue" — pick one), how
they end ("Done"). Return to these patterns every time.

---

## The simplest test

Read your writing out loud. If it sounds like how you'd explain something to a friend —
clear, natural, no filler — it's probably good. If it sounds like a robot, verbose, inconsistant, a legal
document, or an essay, keep editing.

---

## Patterns reference

For detailed guidance on specific interface patterns — alerts, errors, empty states,
onboarding flows, notifications, accessibility labels, destructive actions, buttons, and
instructional copy — see `references/patterns.md`.

---

## Sources and further reading

This skill draws on:

- [Apple HIG: Writing](https://developer.apple.com/design/human-interface-guidelines/writing/)
- [Apple HIG: Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts/)
- WWDC22: [Writing for Interfaces](https://developer.apple.com/videos/play/wwdc2022/10037)
  — the PACE framework (Purpose, Anticipation, Context, Empathy)
- WWDC24: [Add Personality to Your App Through UX Writing](https://developer.apple.com/videos/play/wwdc2024/10140)
  — voice/tone exercises, the dial metaphor
- WWDC25: [Make a Big Impact with Small Writing Changes](https://developer.apple.com/videos/play/wwdc2025/404)
  — filler words, repetition, lead with the why, word lists
- WWDC19: [Writing Great Accessibility Labels](https://developer.apple.com/videos/play/wwdc2019/254)
  — context-driven labelling, verbosity as a deliberate choice
- [Apple Style Guide](https://help.apple.com/applestyleguide/)
