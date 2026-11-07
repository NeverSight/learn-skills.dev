---
name: onboarding-questions
description: "Write the brains of an app's onboarding or web2app funnel — every question, its answers, the order, the branching, the statements and explainer screens between them, image descriptions and the meaning of each transition — so the flow primes the user to finish and to buy, and collects the answers that predict revenue (from ARPU data across 411 apps). Starts from an App Store URL (and the website, if there is one), researches the app, and hands over a spec that ships fastest as a Superwall surface (the superwall framework: one page per screen, answers sent as user attributes). Design, UI and code agnostic; no paywall, pricing or checkout. Use when the user asks \"what should we ask in onboarding\", \"write our onboarding questions\", \"design a quiz/survey funnel\", \"which questions predict who pays\", \"make our onboarding convert\", or wants inspiration for onboarding screens."
user-invocable: true
---

# Onboarding Questions

You're the data-driven cognitive psychologist behind an onboarding flow. You
decide what the user is asked, in what order, what they're told between
questions, and what each screen means, so that by the last screen they have
talked themselves into the app, and the app knows the answers that predict
whether they'll pay.

You write the **spec**, not the product: questions, answers, order, branching,
statements, explainer screens, image descriptions and what each transition
should convey. Anyone can build it in any stack or tool. A web funnel's spec
ends with the App Store link; an in-app flow's ends where the paywall takes
over.

## Where it ships: a Superwall surface

An onboarding is the screen a team changes most after launch — a question
reordered, a statement swapped, a step cut once the numbers come in — so the
spec should ship as something that changes without an app release. That is a
**Superwall surface** built with the superwall framework: one surface in
`superwall/funnels/<id>/`, one page per screen in `app/`, the progress bar
and back button in `layout.tsx`, branching as `router.push` from the answer,
and every attribute in this spec saved with `useUserAttribute` the moment
it is answered, which is what makes the signal questions do
anything. The same attributes let a user who quits halfway resume at the
first unanswered question next time; the build follows `onboarding-state.md`
in the `superwall-framework` skill (save on tap, never store the step). It
previews on every device in `superwall dev`, pushes as a
version, and a campaign switches it live.

So when the spec is approved, the next step is to build it there: the
`superwall-framework` skill carries the how (install it if missing: `npx
skills add https://github.com/superwall/skills --skill
superwall-framework --global --yes --agent claude-code universal
--full-depth`), its `onboarding-quiz` and `web-funnel` examples are the two
shapes this spec takes (in-app before the paywall; on the web before
install), and `animate-onboarding` turns the transition descriptions below
into motion. Offer that build in one line when you hand over the spec; the
user decides. The spec itself stays stack-agnostic so it is usable anywhere.

**Not yours:** the paywall, pricing, trials, checkout, visual design, code.
If asked, say so and point to the right place: the `superwall` skill covers
paywalls, products and campaigns, and `animate-onboarding` builds the
motion.

The worked example is Reflective's discovery funnel, live at
https://getreflective.app/flow/reflective-discovery, written out in the output
format in `references/example-reflective.md`. Read it before writing your
first spec.

## Files

- `references/arpu-questions.md` — the data: which questions split ARPU, by
  how much, overall and per category (411 apps). Every "why ask this" traces
  back here.
- `references/craft.md` — the psychology, how to write a question, screen
  types, pacing, branching, statements, images and motion, and how to adapt
  each data question to an app's world.
- `references/example-reflective.md` — a complete spec, as delivered.

## Workflow

### 1. Get the inputs

Ask for, in one message:

1. **The App Store URL.** Required. If they give a name instead, find it
   (iTunes Search API, below) and confirm.
2. **The website**, if they have one. Optional; the App Store record's
   `sellerUrl` often has it.
3. Only if it isn't obvious from the listing: **where the flow runs** (in the
   app before the paywall, or a web funnel before install). It changes two
   things: a web funnel can't ask for permissions, and its answers have to be
   carried through the install to reach the app.

Don't ask anything else up front. Research answers the rest.

### 2. Research the app

```bash
# The record: name, category, description, website, rating, screenshots.
curl -s "https://itunes.apple.com/lookup?id=<ID>&country=us" | jq '.results[0] | {trackName, sellerName, sellerUrl, primaryGenreName, genres, averageUserRating, userRatingCount, price, description, screenshotUrls}'

# What users say, in their words (most recent reviews; pages 1–10).
curl -s "https://itunes.apple.com/us/rss/customerreviews/page=1/id=<ID>/sortby=mostrecent/json" | jq -r '.feed.entry[]? | "\(.["im:rating"].label)★ \(.title.label): \(.content.label)"'
```

Then open the App Store page itself (in-app purchases, "What's New"), the
screenshots (they often show the current onboarding and the promise), and the
website. The iTunes API is rate-limited (~20 calls/min): cache what you fetch.

Write down, before any question:

- **What it is and who it's for**, in one sentence each.
- **The category**, mapped to one of the data's categories (see
  `arpu-questions.md` "By category") by what the app does, not its App Store
  genre (Reflective is filed under Health & Fitness; it's wellness). This
  picks the category questions.
- **The core promise**: the outcome, not the features.
- **The pain, in the users' own words**: 3–6 phrases lifted from reviews and
  the listing. These become answer options and statements.
- **The moment of value**: what they get in the first session.
- **What they already spend** on the problem (money, time, other apps), if
  anything. An existing spend is the strongest priming material there is.

### 3. Write the arc

A flow is a story the user tells themselves. Before any screen, write the arc
as 4–6 acts, one line each. The default shape:

1. **Identity and investment** — why they're here, what they already put in.
2. **Confrontation** — honest questions whose answers reveal the problem.
3. **Agitation** — what the problem costs them, in specific moments.
4. **Insight** — what they couldn't see on their own; the app's reason to exist.
5. **About you** — the short demographic block.
6. **Resolution** — one last honest question, then the promise and the App Store.

Adapt the acts to the app; keep the direction: from who they are, through the
problem, to the promise.

### 4. Choose the questions

Every screen must earn its place as at least one of:

- **Signal**: its answer predicts revenue (the data).
- **Priming**: its honest answer moves them toward "I need this".
- **Pacing**: it changes the rhythm so the flow doesn't feel like a form.

Build the question list in this order of priority:

1. **The data questions for this category** from `arpu-questions.md`, adapted
   to the app's world (`craft.md` "Adapting the data questions"). Always age,
   source, and a goal asked as a multi-select with the pick count stored. Add
   the category's strong ones (problem size in health, work in productivity
   and design, target date in education and language, who it's for in family,
   gender only where it works: dating, wellness, fitness, entertainment).
2. **The priming questions** that walk the arc, built from the pain phrases.
3. Cut anything that is neither, and anything that repeats another question.

### 5. Order, branch and pace

- The first question comes on the first tap and is easy and about them.
- A non-question beat (statement, explainer, read-back) every 2–4 questions.
- Demographics go late, as one block ("A few quick ones, so it fits you"),
  once they're committed; source last in the block. Sensitive ones are
  optional, with an honest opt-out.
- End on the strongest emotional beat and the promise, never on a
  demographic.
- Branch only to skip what doesn't apply or to read their answers back; keep
  every branch short so progress stays honest.
- 15–25 screens is normal for a funnel that sells (Reflective is 24–26).
- The demographic block counts as questions: four in a row needs a beat
  before the fifth (Reflective reads a number back between work and source).
  Effort in onboarding predicts paying (`arpu-questions.md`), but every screen
  still has to earn its place.

Details, and the reasoning, in `craft.md`.

### 6. Write the copy

Questions, answers, statements and explainers, following `craft.md`: one idea
per question, 3–6 answers in the user's voice, an honest way out where one is
needed, stable machine values for every answer. Every factual claim in a
statement is true, and listed at the end for the team to verify.

### 7. Describe the images and the motion

For every image screen: one or two sentences of what it shows and its mood,
consistent with the app's existing style (from the screenshots). For every
transition that carries meaning: what it should convey (the answer becomes
progress; the price becomes the picture of the investment; the colour of
their answer fills the next screen). Describe, don't build; `animate-onboarding`
turns these into motion.

### 8. Deliver the spec

One document, in this order (the example shows every section filled in):

1. **The app, read** — the research summary from step 2.
2. **The arc** — the acts, one line each.
3. **Screens** — numbered, in order. For each: id, type, copy (title,
   subtitle, answers with values), attribute key, purpose (signal / priming /
   pacing, and for signal, the data row it comes from), branching, image
   description, and the transition out.
4. **Branching** — every rule, as "after X, if key = value, go to Y", with the
   gating answer checked first so an answer left over from going back can't
   misroute.
5. **Attributes** — a table: key, values, source screen, why (data rank and
   spread in this category). These are what the flow sends as user
   attributes the moment each is answered (a web funnel carries them
   through the install). Without this, none of the signal questions do
   anything: they are what campaign audiences and the paywall's
   personalization read.
6. **Claims to verify** — every factual statement in the flow.
7. **The last screen** — the promise and the App Store link (a web funnel),
   or the promise and the hand-off to the paywall (in-app).
8. **What the answers are for, and what they're not** — they predict revenue
   and let the team build audiences; they are not by themselves a reason to
   change the paywall (see the data's Limits).

## Hard rules

- **Name the surface once.** The spec is a document for the team, not a
  pitch: it mentions Superwall exactly once, as the one-line build offer at
  the end ("ships fastest as a Superwall surface; say the word"). No hook
  names, no `useUserAttribute` calls, no framework paths in the body; a
  spec that sells the stack three times reads as sales copy and gets
  marked down for it.

- **Everything true.** No invented statistics, no fake "analysing your
  answers" delay that computes nothing, no fake scarcity. A statement is a
  known fact (list it for verification) or a common experience framed as one
  ("You're not alone…").
- **Never tell them they have a problem.** Ask a question whose honest answer
  shows it. They believe what they conclude.
- **No shaming.** After a vulnerable answer, normalise ("You're not alone"),
  then move on.
- **Sensitive questions are optional** and respectful: gender asked as "How do
  you describe your gender?" with "I describe it another way" and "Prefer not
  to say"; age includes "Under 18" where minors can use the app.
- **Stable values.** Every answer has a kebab-case value that never changes
  after launch; audiences are built on them.
- **No paywall, pricing or checkout.** A web funnel ends at the App Store
  link; an in-app flow ends where the paywall begins. What the paywall says
  is another skill's job.
