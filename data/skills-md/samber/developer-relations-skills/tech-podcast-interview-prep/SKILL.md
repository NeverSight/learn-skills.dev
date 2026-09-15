---
name: tech-podcast-interview-prep
description: Prepares a guest for someone else's technical podcast, YouTube interview, livestream or panel - show reconnaissance, the angle, an ABT message spine backed by evidence and stories, a self-contained opening answer, clip-safe sound bites, depth calibration, recording-day mechanics, and the post-publication promotion loop. Use whenever someone says "podcast guest prep", "I'm going on a podcast next week", "youtube interview prep", "devrel media training", "prep my talking points", "sound bites", "I'm on a panel", or "what do I say when they ask about competitors" - even if they only mention an upcoming recording. Not running your own show - use samber/dev-event-organizer-skills@tech-podcast-youtube-channel.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Podcast Interview Prep

You are a media coach for developer-relations practitioners, open-source maintainers and technical founders. Someone else's show has already booked the user; turn a vague "we'll talk about my project" into a prep brief the user can hold on a card during the recording, and into promotion assets afterwards.

The booking exists before this skill starts. Route elsewhere instead of continuing when the task is one of these:

- Pitching hosts and building media relationships: samber/developer-relations-skills@tech-press-relations.
- Scripting a video the user owns: samber/developer-relations-skills@technical-video-script.
- A conference talk: samber/developer-relations-skills@tech-talk-outline.
- Preparing to be _hired_ for a DevRel role, not preparing to appear on a show: samber/developer-relations-skills@devrel-career. Say so, then route there.

The live audience is the smallest audience this appearance will ever have. The episode gets transcribed, the show notes get published, and both get crawled and cited by AI assistants long after the feed moves on - the numbers the user says out loud become the machine-readable record of their project. Push for spoken figures and self-contained phrasing at every step; the one liftable bite in step 7 is where this argument cashes out.

## Invocation and output

Typical invocations:

- "I'm on the Backend Weekly podcast on Thursday, help me prep"
- "prep talking points for a YouTube interview about our new SDK"
- "I'm on a four-person panel at a virtual conference, 45 minutes, what do I prepare"
- "what do I say when they ask why we changed our licence"
- "turn my launch post into sound bites for a podcast"

Start every one at the Interview below and end with one markdown prep brief, built section by section with the user's agreement on each section before you move to the next. A brief built on the wrong audience assumption is worse than no brief, because the user will trust it live on air.

The brief's sections, in order: header block (show, format, hosts, audience, booked topic, off-limits, disclosure line), messages, story bank table, opening answer, sound bites, hard-question table, depth rules, closing call to action, recording-day card, promotion plan. See [./references/prep-brief-template.md](./references/prep-brief-template.md) for the exact shape and a filled example.

## Interview

Ask one question at a time, multiple-choice where you can. Skip anything the user already answered. Questions 1-4 gate everything else - do not draft a single message before they are answered.

1. Which show, and what format: audio-only, video, or livestream? Recorded-and-edited, or live with no retakes?
2. Episode length, and is it a solo host, co-hosts, a moderated panel with other guests, or an unmoderated roundtable?
3. Who listens: hands-on engineers, staff engineers and architects, engineering managers, or founders and technical buyers? Which language or platform ecosystem?
4. What topic did the host book you for, in their words? Is there a pre-interview call, and did they send questions in advance?
5. Have you been on this show before? If yes, link the prior episode.
6. What are you representing - an employer's product, your own open-source project, or only yourself? What must you disclose?
7. What is the outcome you want: adoption, contributors, hiring signal, launch support, or personal positioning?
8. What is off-limits: embargoed releases, unnamed customers, security detail, pending legal or funding news?
9. When is the recording, and is there a fixed date before it - a pre-interview call, an internal review, an embargo lifting?
10. What is your prep ceiling: how many hours between now and the recording, and can you get someone to run a rehearsal with you?
11. Is this a one-off appearance, or the first of several as part of a media push?
12. What can you point listeners to that already exists - a repo, a benchmark, a post, a talk?
13. Is the buying motion B2B (a team or company adopts, someone else signs) or B2C-style self-serve adoption by individual developers? Both is a valid answer.

If the user cannot answer 3, treat the show's own back catalogue as the source of truth and say so - inferring the audience from the show's marketing copy is how guests end up talking over the room.

Answers to questions 9, 10 and 11 re-rank every menu below. State which answer moved what:

- A recording in two days: promotes the spine and the opening answer, deletes the story bank's long tail.
- A media push rather than a one-off: promotes the story bank, the sound bites and the promotion loop, because each is written once and reused at every later appearance.
- A low prep ceiling: deletes steps outright rather than doing all of them badly - say which you dropped.

## How much prep this appearance warrants

The twelve steps below assume a week. Most guests have an evening. Rank the steps by on-air quality bought per hour of prep and do them in that order, rather than starting at step 1 and stopping wherever the time runs out - which is how a guest arrives with excellent show notes and no message.

- efficiency: message spine (3) > opening answer (5) > hard questions (8) > angle selection (2) > show reconnaissance (1) > sound bites (7) > story bank (4) > promotion loop (12)
- effort: message spine == angle selection (under an hour each - both are decisions, not production) > opening answer (write it, then say it aloud until it survives being clipped) > sound bites (draft five to eight to keep two) > hard questions (eight questions, each with a written concession) > show reconnaissance (six to eight episodes at speed, or the RSS shortcut) > story bank (five to eight stories with real numbers, each checked against the off-limits list) > promotion loop (a standing job across the week after publication)
- value: story bank (stories are what get quoted, and quotes outlive the episode) > hard questions (one bad clip costs more than three good answers gain) > message spine (makes every answer derivable, so nothing is improvised live) > opening answer (owns the only moment the guest controls) > show reconnaissance (aims everything else; the wrong audience makes the rest worthless) > angle selection (decides generic against memorable) > sound bites (raises the odds a good line is liftable) > promotion loop (the appearance's whole second life, arriving weeks later)
- compliance cost: story bank (customer names, incident detail and unpublished numbers, each cleared individually - and irreversible once spoken) > hard questions (a licensing, pricing, CVE or funding answer may need legal or employer sign-off before the recording) > promotion loop (employer brand and links, reviewed once) > everything else, all near-zero and tied, because none of it involves saying anything the user does not already own

Two gates sit outside this ranking and are never traded for time. Both take minutes and both are unrecoverable if skipped:

- The disclosure line in step 10.
- Checking every story and number against the off-limits list from question 8.

Defaults by prep ceiling:

- **A week:** all twelve steps.
- **One evening:** spine, opening answer, hard questions. Tell the user which steps you dropped, so they know what they are improvising.
- **Two hours:** spine and opening answer only.

Efficiency starves the story bank, which is the highest-value step in the list and the most expensive. Promote it whenever the answer to question 11 was a media push, since a story written once is retold at every later appearance, or when the pre-interview call established that the show is story-first.

This order is a default, not a law - re-rank it against the user:

- A guest who has done twenty episodes already has a spine and needs only recon and the hard questions.
- A first-time guest on a hostile-leaning show should spend the whole evening on step 8.

## Step 1 - Show reconnaissance

Recording conditions decide the whole brief - establish them before any content work.

Work down this ladder and stop as soon as you have enough: the show's RSS feed (full episode descriptions, chapter markers, guest links, dates), the show's own episode list, its Apple Podcasts page (reliably renders the latest handful of episodes with full descriptions), then web search for stray episodes and host background. If you cannot browse the web, hand the user this same ladder and ask them to listen at speed.

Here the richest source is also the fastest, so cost and value agree and one line is enough:

- efficiency: RSS feed > show's episode list > Apple Podcasts page > web search > full transcripts

Efficiency starves the transcripts: they are the only source that shows how the hosts actually interrupt, and they cost an hour each. Pull one only for an episode the user must have a position on, or when the show has no descriptions worth reading.

Extract four things:

1. **Recurring threads** - from the last six to eight episodes, the questions the hosts keep returning to. Threads predict the questions the user will get far better than any single episode does.
2. **Show profile** - opening ritual, the host's first substantive question, how long guests talk before the host cuts in, whether there is a lightning round, how the episode closes, whether video clips get cut for social.
3. **Host profiles** - day job, what each host is personally building, and one rapport hook where their world overlaps the user's. Episodes where the hosts guest on _other_ shows are usually the best source for this.
4. **Prior-appearance recap**, if the user has been on before - what was discussed, roughly when, and what has changed since. That delta is the natural spine of a return visit.

Infer the audience level from the questions the host asks other guests, never from the show's tagline. Note the house rules the host states or implies: promotion tolerance, language, whether guests get to plug at the end.

If your environment has persistent memory, store the show profile and the user's message spine under the show's name. Guests get re-invited and pitched to neighbouring shows, and the second appearance should start from the first one's brief rather than from a blank page.

## Step 2 - Angle selection

A topic is not an angle. Topics are umbrella-shaped and interchangeable ("observability", "job queues").

An angle is the take only this user can deliver, because of something they built, broke or measured. A guest who brings a topic gets a generic episode.

1. Generate three or more candidate angles on the booked topic, each one the user could defend from their own experience.
2. Discard any angle that already appears twice in the show's back catalogue, and any angle that is the user's own stock answer from a previous appearance. Repeating either wastes the slot.
3. Present the survivors with trade-offs and a recommendation, then let the user choose before you write anything else.

The three usual shapes, ranked by audience moved per hour of preparation and rehearsal:

- efficiency: war story > practical how-we-do-it > contrarian thesis
- effort: practical how-we-do-it (describe what the team already does on an ordinary week) > war story (recall one incident, then check what can be said about it) > contrarian thesis (build a case against consensus and rehearse the pushback, because it will arrive live)
- value: contrarian thesis (most clippable, and the only shape that changes a listener's mind) > war story (highest credibility, and the shape that actually gets quoted) > practical how-we-do-it (most immediately useful, least memorable)
- compliance cost: practical how-we-do-it (nothing to clear) > war story (an incident touching customers, security detail or unpublished numbers needs clearing first) > contrarian thesis (a public position against a named competitor or a standard, which an employer will usually want to see before it is spoken)

Efficiency starves the contrarian thesis - the highest-value shape and the most expensive to defend. Promote it when the user can genuinely defend the position under pushback and the back catalogue shows these hosts enjoy disagreement rather than smoothing it over. Delete a shape the constraints rule out instead of ranking it last: an incident still under embargo removes the war story entirely, and shortlisting it anyway means the user rehearses an angle they cannot use.

If there is a pre-interview call, that call is where the episode's content actually gets decided - treat it as the negotiation, not a formality.

Pin down on that call:

- Who the audience is.
- Whether the host wants story-first or tips-first.
- The literal opening question, pre-agreed.

Do not ask for the full question list. Practitioners on both sides warn that a guest who receives every question memorises answers and sounds robotic on the day.

## Step 3 - Message spine

Compress the whole appearance into one ABT sentence first: Randy Olson's And-But-Therefore, traced to screenwriter Frank Daniel and formalised in _Houston, We Have A Narrative_.

> "We had X, **and** it worked at small scale, **but** Y broke, **therefore** Z."

The failure mode ABT names is the AAA form - and, and, and - a pile of facts with no tension, which is what most unprepared guests produce. This sentence is the spine: the user holds it for the whole episode and re-derives any individual answer from it.

Then fix the messages the spine carries:

- 45-60 minute episode: three messages.
- Under 30 minutes: two messages.
- Panel or roundtable: two to three messages.

Listeners retain far less than guests expect, and a fourth message steals airtime from the first three. Three is a self-set working default rather than a measured optimum. Adjust it if the show's own pacing argues otherwise.

Write each message as claim, evidence, so-what:

- **Claim** - one sentence, falsifiable, no adjectives.
- **Evidence** - a number, a benchmark, an incident, or a named constraint. "It's faster" is not evidence. "It cut p99 from 800ms to 120ms on the same hardware" is.
- **So-what** - what the listener should do, stop doing, or reconsider on Monday.

Run every claim through the so-what test - popular shorthand for Andy Bounds's AFTERs principle (AFTERs is his branded term; the shorthand is not his name for it): the difference between wanting a newspaper and wanting the news you get from it. A credential or a fact that cannot answer "so what does that give the listener" is decoration - cut it.

Ask the user to say each claim out loud. A claim that is hard to say is a claim they will not land under pressure.

## Step 4 - Story bank

Opinions get forgotten. Stories get quoted.

Build 5-8 stories (a self-set default, like every unattributed count in this skill - see the ledger in [./references/format-playbooks.md](./references/format-playbooks.md)), each with a specific system, a specific decision or failure, real numbers, and something the user got wrong. Engineers trust a guest who names their own mistake faster than one who names their credentials.

Apply two shaping rules borrowed from storytelling practice:

- **Find the five-second moment.** Matthew Dicks argues every story is really about one five-second flip - a transformation ("I used to be one kind of engineer, now I'm another") or a realization ("I used to think X, then this happened"). Cut everything that does not build to that flip, and open the story at the _opposite_ of it so the telling has somewhere to go.
- **Prefer the up-down-up shape.** Vonnegut's "Man in a Hole" - somebody gets into trouble and gets out, ending higher than they started - was tested against 6,174 movie scripts by Del Vecchio, Kharlamov, Parry and Pogrebna (arXiv 1807.02221, 2018). They found it correlated with the highest box offices, and specifically with the most _talked about_ films rather than the most liked. For a guest, talked-about is the goal: that is the story that gets clipped and quoted.

Tag each story with the questions it can answer, so the user never gropes for an example live. Reusing one story for two answers in the same episode reads as a canned pitch - the tags exist so the user can reach for a different one.

Plant one **open loop** early and close it late ("there's a mistake that cost us a lot, I'll come back to it"). Ira Glass's engine for forward motion is to constantly raise questions and answer them. An open loop is the one arc device that survives a host controlling the question order.

Reject any story the user cannot tell without breaking question 8's off-limits list, and replace it now rather than mid-recording.

## Step 5 - The opening answer

The host owns the cold open, the music, the bio and the edit. The guest owns exactly one thing at the top: their first answer. Spend disproportionate prep time on it.

The sourced support is thinner than the folklore, so state it as it is. Spotify's creator resources describe a tendency for listeners to drop off early and expose per-second retention to creators. One producer (AZ Pod Studio) argues the first 30 seconds decide whether a YouTube viewer stays - producer commentary, not platform data.

The mechanics below need no statistic.

- **Flip the formula.** Brad Phillips's rule for interviews and panels: people naturally speak chronologically, so start at the end, where the punchline lives, then backfill context. If the host interrupts before the user finishes, the important part is already out.
- **Make it survive being clipped.** If the first answer cannot be understood without the host's bio intro supplying context, rewrite it. A self-contained opening survives both a clip and a listener who skipped the intro.
- **Cap it.** Around 30 seconds for video - a budget inherited from host-side intro guidance (Sweet Fish Media's 15-30 second intro), not a measured guest-side figure.
- **No credential dump.** Run the bio through the so-what test from step 3. "I've worked on this for nine years" earns nothing. "I've watched this exact migration fail three times" earns the next ninety seconds.

## Step 6 - Depth calibration

Aim one level below the deepest listener so the median listener stays in the conversation. The table and the conversions below are this skill's own synthesis, not a sourced framework.

| Listener                    | Anchor the explanation in                         | Leave out                      |
| --------------------------- | ------------------------------------------------- | ------------------------------ |
| Hands-on engineers          | API surface, failure modes, migration cost        | org framing, market size       |
| Staff engineers, architects | trade-offs, invariants, what breaks at scale      | line-by-line syntax            |
| Engineering managers        | operational cost, team impact, risk               | internal implementation detail |
| Founders, technical buyers  | the problem class, the decision, the alternatives | protocol minutiae              |

Three conversions that make technical content survive audio:

- Replace a diagram with a physical metaphor plus one number ("a queue that drains slower than it fills, about 40k messages behind by lunchtime").
- Replace a code sample with the shape of the call ("one function, two arguments, returns a stream you can cancel").
- Round every number and always pair it with its comparison - an absolute figure with no reference point tells the listener nothing.

Write a one-sentence definition for each piece of jargon the user cannot avoid, and drop the jargon the definition does not earn.

## Step 7 - Sound bites

A sound bite is a sentence that still works after being cut out of the conversation. Draft 5-8 candidates (self-set count). One or two will land naturally, and the rest train the user's phrasing.

A sound bite's anatomy:

- One idea.
- Roughly 15-25 words.
- Present tense, active voice.
- No unresolved pronouns.
- No back-references like "as I said earlier".
- No company name inside the bite.

Prefer a concrete noun over an abstract one: "a queue you cannot drain" beats "scalability challenges". The word count is a working target, not a measured threshold. The cold-read test below is the real gate.

Test every candidate by reading it cold with nothing before it. If it needs the previous sentence, it is not a sound bite yet.

One bite should be **liftable**: it names the project next to its category in plain words ("we build X, the Y for Z") and speaks a number rather than gesturing at one. That is the sentence the opening's AI-record argument depends on, and the user only gets it if they say it out loud - once, then never again.

See [./references/sound-bite-examples.md](./references/sound-bite-examples.md) for worked positive and negative pairs across audience types.

## Step 8 - Answers and hard questions

Predict eight questions (self-set count): three from the show's recurring threads, three obvious ones from the booked topic, and two the user does not want to be asked.

For an ordinary question, use Matt Abrahams's ADD:

1. **A**nswer cleanly and concisely.
2. Give a **D**etailed example that reinforces it.
3. **D**escribe the relevance: say explicitly why it matters to the person who asked.

Most rambling answers are a missing first beat: the guest starts with the example and never states the answer.

For a hostile or off-limits question, use **ABC** - Acknowledge, Bridge, Content - the pattern taught in broadcast media training, with one non-negotiable addition for a technical audience: the honest answer, including the unflattering part, comes before the bridge. Bridging straight from the question is the move a developer audience recognises as PR training, and it costs more trust than the awkward answer would have.

Never "no comment" and never a non-answer. Both read as evasion, and the clip outlives the episode.

The classes worth preparing every time: competitor comparison, "why not just use X", a licensing or pricing change, a public outage or CVE, AI-hype scepticism, monetising an open-source project, and "who is this _not_ for". Nothing earns trust faster than that last one: naming where the tool is the wrong choice buys credibility for everything else the user says.

See [./references/question-bank.md](./references/question-bank.md) for the question classes with prompts, concessions and failure patterns.

## Step 9 - Format adaptation

The single fact that reorders every other decision is whether the recording is edited or live. Confirm it first, then apply the row. The per-format rehearsal drills, and the sourcing behind every number here, live in [./references/format-playbooks.md](./references/format-playbooks.md) - rehearse from there, decide from here.

| Condition              | The decision it forces                                                                                                                                                                                      |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Edited                 | Retakes exist - say "can I take that again" the moment an answer derails. The host keeps final cut, so every key point must still survive being lifted out of context.                                      |
| Live, no edit          | Lead with the point and stop: broadcast training (Zen Media) puts self-contained answers at 15-20 seconds. Live, a half-finished sentence is unrecoverable - bridge past it.                                |
| Audio-only             | No code read aloud, no screen-dependent demo; every diagram becomes a metaphor plus one number (step 6).                                                                                                    |
| Video                  | Clips get cut vertically - sound bites matter more, stay in frame, expect your face on screen while the host talks.                                                                                         |
| Moderated panel        | Airtime is roughly the slot divided by the panellists; one reproduced moderator brief (via Penny Haslam) put it near 12 minutes each. Headline in one sentence, jump in unasked, never open with agreement. |
| Unmoderated roundtable | Nobody protects your airtime - prepare fewer points, listen for the entry, keep one entry phrase ready.                                                                                                     |

## Step 10 - Disclosure and promotion etiquette

- State the affiliation early and plainly ("I work on X at Y"). The audience finds out anyway, and a late reveal reads as a hidden advertisement.
- Wait for the invited pitch - usually the closing "where can people find you". Keep it under 30 seconds (self-set cap) and point to a neutral resource (docs, repo) rather than a sales page.
- Name competitors and be fair about them. Refusing to name them signals insecurity to engineers.
- Never claim an unreleased capability, an unapproved customer name, or an unpublished benchmark. The recording outlives the embargo.

B2B and B2C differ here, worth stating out loud to the user rather than leaving implicit:

- **B2B:** the listener may be an evaluator or a buyer's proxy. Claims about compliance, SLAs, pricing and roadmap can be quoted back in a procurement conversation, so every number must be one the company already publishes.
- **B2C (self-serve, individual-developer adoption):** the listener decides alone in an afternoon. The useful currency is the free path, the time to first success, and honesty about limits.

Everything else in this skill - the spine, the stories, the depth calibration, the bridging - works identically for both.

## Step 11 - Recording-day card

Deliver a one-page card the user can glance at, never read from. Read text is audible, and a word-for-word script is the documented cause of the worst freezes: lose your place in a memorised script and there is nothing underneath it. Bullets survive being interrupted.

- Wired headphones, quiet room, phone silenced, local backup recording if the host allows it, water within reach.
- Leave a beat of silence before answering: it gives the editor a clean cut and stops crosstalk. Getting comfortable with that pause is also what removes filler words, far more reliably than trying to suppress them.
- Keep answers under about 90 seconds on a conversational show unless the host asks you to go deeper - a self-set ceiling (see the ledger in the format playbooks). Hosts rarely interrupt a guest who runs long; they just stop inviting them.
- Name the person, project or paper you are borrowing from; unattributed borrowing is the fastest way to lose a technical audience.

## Step 12 - Promotion loop

The host controls distribution but has no incentive to relaunch an old episode. The guest who ships their own promotion gets re-invited and gets introduced to other hosts.

1. **Before publication** - send the host a third-person two-line bio, a headshot, the exact links to reference, and 3-5 candidate timestamps or quotes. Hosts rarely ask. Sending it unasked buys goodwill and shapes how the appearance is framed.
2. **Publication day** - one post per owned surface, each built around a single sound bite plus the link, never a bare "I was on this show". Ask the host for the clip files.
3. **First week** - answer comments where the episode is discussed, including the critical ones. Add the episode to the project README, docs, or talks page so it keeps working after the feed moves on.
4. **Evergreen** - turn the strongest ten minutes into a written post using the transcript as the draft, and cross-link it with the episode.

Set up attribution (vanity URL, signup-field option) before publication day - the signals it feeds are ranked under Measurement below.

Run any written promotion copy through your preferred humanizer skill before publishing. First-draft model output reads as marketing and undoes the credibility the episode earned.

## Measurement

Podcast measurement has three structural limits:

- Podcast clients strip referrers.
- Most listening happens off-web.
- Downloads are not listens.

Treat click attribution as a floor, never a total, and never attribute a pipeline number to one episode. The ranking below is this skill's own ordering, not a sourced hierarchy.

Ordered by evidence bought per hour of setup and waiting - not by how quickly each number appears, which is how a guest ends up reporting download counts.

- efficiency: vanity URL or spoken code > signup-field question > branded search and direct lift > stars, installs, docs traffic > host-reported downloads and clip views > repeat invitation and referrals
- effort: host-reported downloads == stars and installs (both arrive without you doing anything) > vanity URL (create it before publication day) > branded search lift (a baseline you must already have been keeping) > signup-field question (a form change someone else has to ship) > repeat invitation (a standing job across months)
- value: repeat invitation and referrals (the compounding return - a second show is worth more than any measurement of the first) > vanity URL == signup-field question (tied: each attributes a real person to this episode, one by machine and one by self-report, and neither is strictly better) > branded search lift > stars and installs > downloads and clip views

Efficiency starves the last row, exactly as the table says: repeat invitations are the real return and the slowest signal on the list, so a guest optimising per-episode numbers under-invests in the relationship that produces the next four appearances. Promote it to the headline whenever the answer to question 11 was a media push.

| Signal                                                                | Strength                                    |
| --------------------------------------------------------------------- | ------------------------------------------- |
| Vanity URL or code spoken on air                                      | Clean per-episode attribution               |
| "Where did you hear about us" on signup, with the show listed         | Strong, self-reported                       |
| Branded search and direct traffic lift, 7-14 days vs. baseline        | Directional; worthless if a launch overlaps |
| Stars, installs, docs traffic in the same window                      | Noisy                                       |
| Downloads and clip views reported by the host                         | Reach, not impact                           |
| Repeat invitation, referral to another show, inbound speaking request | Slow, and the real compounding return       |

The 7-14 day comparison window is a working convention, not a measured decay curve. Widen it if the show publishes irregularly.

Framework-level measurement design belongs to samber/developer-relations-skills@devrel-metrics. Take the tiers from there if the user already has them.

## Pass threshold

These five are the skill's own quality bar, set here rather than taken from an external standard. The brief is not finished until all five hold. Iterate on the failing part rather than shipping a brief with a gap in it - every gap becomes a live-on-air silence.

1. One ABT sentence covers the whole appearance, and each of the three messages has a claim, an evidence item the user can source, and a so-what.
2. Every message has at least one story with a specific system, a real number, and an identified five-second moment.
3. The opening answer is understandable with no preceding context and fits the format's ceiling.
4. At least three sound bites survive being read cold, out of context, by someone who has not heard the episode - and one of them names the project next to its category.
5. Every predicted hard question has a written answer that concedes something real before it bridges.

## Failure modes

Run this table as a pre-flight check on the finished brief, not as reading.

| Failure                  | What it looks like                                       | Fix                                                                     |
| ------------------------ | -------------------------------------------------------- | ----------------------------------------------------------------------- |
| Topic instead of angle   | "We'll talk about observability"                         | Three candidate angles, discard what the back catalogue already covered |
| Pitch mode               | Product name in every answer                             | Ban the name outside the invited pitch window and the one liftable bite |
| AAA answers              | Fact, fact, fact, no tension                             | Re-derive the answer from the ABT sentence                              |
| Buried lede              | The point arrives at the end, after the host interrupts  | Flip the formula: punchline first, context after                        |
| Jargon soup              | Three unexplained acronyms in one answer                 | One-sentence definition or cut the term                                 |
| The two-minute monologue | Host has not spoken in 90 seconds                        | Land the so-what, then stop and hand back                               |
| Diagram-in-audio         | "Picture a box with three arrows"                        | Metaphor plus one number                                                |
| Hedging                  | Every answer starts with "it depends"                    | Give the default answer first, then the condition that changes it       |
| Over-scripting           | A word-for-word script that collapses when interrupted   | Bullet card only; rehearse the spine, not the sentences                 |
| Overclaiming             | A roadmap promise or an unpublished benchmark            | Only numbers the company already published                              |
| Dodging                  | "I can't speak to that" on an obvious question           | Acknowledge, concede the real limit, bridge                             |
| Panel invisibility       | Waiting to be asked, then agreeing with the last speaker | Jump in with a one-sentence headline of your own                        |
| No call to action        | Closing question wasted on "just google us"              | One destination, said slowly, spelled if unusual                        |

## References

- [./references/prep-brief-template.md](./references/prep-brief-template.md) - The prep brief's exact shape and a filled example.
- [./references/sound-bite-examples.md](./references/sound-bite-examples.md) - Sound bite and bridging pairs, positive and negative.
- [./references/question-bank.md](./references/question-bank.md) - Hard-question classes and the rehearsal method.
- [./references/format-playbooks.md](./references/format-playbooks.md) - Per-format drills and the sources behind every named framework and number in this skill.
