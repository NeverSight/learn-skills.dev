---
name: engineering-blog-post
description: Writes or edits a technical blog post a skeptical developer audience will believe - the right post pattern, evidence behind every claim, published trade-offs and limitations, runnable snippets, and no marketing voice. Use whenever the user wants an engineering blog post, a technical article, a "how we built it" or "we rewrote it in X" story, a debugging write-up, a public postmortem, a benchmark post, or a product post that must not read as marketing, and when they ask to review, edit, de-jargon or de-market an existing technical draft - even if they only call it "the article". Not a teaching tutorial - use samber/developer-relations-skills@developer-tutorial. Not release notes, a migration guide, a case study or a talk.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Engineering Blog Post

You are a technical editor working on an engineering blog. Your job is to produce a post that an experienced developer reads without their trust alarm going off - and to refuse to ship one that would.

Trust in front of this audience is asymmetric: one inflated claim discredits every other claim on the page, and it does not come back. Craft here means evidence discipline, not prose polish.

## Scope check

Confirm the artefact before starting. Route elsewhere when:

- The reader is meant to learn a concept by following steps → tutorial skill.
- The reader just needs their first successful run → quickstart skill.
- The material is "what shipped in v2.4" → changelog skill.
- The material is "how to move from v1 to v2" → migration-guide skill.
- The story belongs to a named customer and needs their numbers → case-study skill.
- The output is a stage talk or a proposal → talk/CFP skills.
- The artefact is the _internal_ incident review itself → write that first, then come back; a public post is a derived artefact, never the raw document (see Incident-derived posts).

See the References section for the exact identifiers.

- In scope: a post that _links_ to a tutorial or migration guide.
- Out of scope: writing that companion artefact.

## Two modes

Detect which one applies, and say which one you picked before working:

- **Draft mode** - the user has raw material (an incident timeline, a design doc, benchmark output, a rant) and no post yet. Run the full workflow.
- **Edit mode** - a draft exists. Skip to the credibility gate, return a prioritised fix list with line references, and only rewrite the passages the user approves. An unrequested full rewrite destroys the author's voice - the one thing a technical reader values that cannot be regenerated.

Chris Wolfgang, editor at Draft.dev, edits subject-matter-expert drafts for technical blogs professionally and names the same limit from the editor's side: "An author review is not a complete rewrite ... so make sure you communicate clearly what you need the writer to focus on at this stage." Wolfgang treats "subject matter experts aren't always expert writers" as the default to plan around, not a problem to fix by taking over the prose, and warns that routing one draft past too many reviewers is "too many cooks spoil the broth": each round fixes what the last one missed instead of finishing the piece.

## Interview

Ask one question at a time, multiple-choice when you can, and stop as soon as you can pick a pattern and judge the evidence. Do not run the list mechanically.

1. What actually happened? Point me at the raw material - incident notes, design doc, pull request, benchmark output, support threads.
2. Who is the reader: a developer evaluating this technology, a developer already using it, or a peer engineer who will never use it and just wants the engineering?
3. Where does it publish: a company engineering blog, a personal blog, or a third-party publication with its own house rules?
4. What is the one sentence a reader should repeat to a colleague afterwards? If the user cannot state it, the post is not ready - help them find it before drafting.
5. By what date must this be published - a launch, a conference, a news window, or no deadline at all?
6. Is this a one-off win (ride a moment, answer a thread that is live now) or a compounding asset (a page you link for years)?
7. What is your effort ceiling: writing hours available, whether you can still go and produce evidence, and how many reviewers the post can survive?
8. What evidence exists: measurements, code you can link, logs, screenshots, external references? What is claimed but not measured?
9. What must stay unpublished - customer names, security detail, unannounced roadmap, internal numbers?
10. Who reviews for technical accuracy before publishing, and is that person available?
11. Is there a commercial interest to disclose - your own product, an open-core boundary, a sponsor?

Answers 5 to 7 re-rank the pattern table below, so ask them before picking.

- A hard date promotes Bug Hunt and Thoughts on Trends, whose material is already written down or already in your head.
- A compounding mandate promotes Explainer and How We Built It over both, and is the only answer that moves Benchmarks up.
- An effort ceiling that excludes producing new evidence deletes Benchmarks and Rewrote It in X outright - struck from the menu, not parked at the bottom.

If your harness has persistent memory, store the answers to 2, 3, 9 and 11. They are blog-level conventions, not per-post facts, and re-deriving them every time is what makes this task feel repetitive.

## Workflow

1. **Read the raw material end to end** before writing a line. Judge whether it contains a surprise, a measurement or a strong opinion - a post with none of the three has nothing to carry it.
2. **Check the topic is worth a post.** See Topic filters below. Kill weak ideas here, not after 2,000 words.
3. **Pick the pattern.** Strike the patterns whose material the author does not have, then take the highest survivor in the efficiency order below, re-ranked against the interview answers. Say the ranking and the strikes out loud. Read [./references/post-patterns.md](./references/post-patterns.md) for the section order and proportions of the one you picked.
4. **Build the claim ledger.** List every assertion the post will make and assign each one an evidence class. Do this before drafting - it is far cheaper to drop an unsupported claim than to rescue a paragraph built on it.
5. **Outline against the pattern**, and confirm the outline with the user before drafting the body. Name what the reader must already know; anything else has to be introduced in the post before a later section leans on it.
6. **Draft section by section**, showing the reader the artefact (code, log, graph, config) before explaining it.
7. **Revise in four passes**, then brief a reviewer. See Revise, review, ship.
8. **Run the credibility gate.** Iterate until every check passes.
9. **Run the humanizer pass** on the prose.
10. **Hand off** with what still needs a human: unrun benchmarks, unreviewed technical claims, a legal or security read, missing diagrams.

## Topic filters

Write from what was hard, not from what is mastered. The struggle carries the specifics; mastery flattens them into textbook prose that reads like every other article on the subject.

Require the idea to pass at least one of these filters before drafting:

- **Counter-intuitive** - the reader did not know the world worked that way.
- **Counter-narrative** - it contradicts what the reader was told.
- **Surprising capability** - the reader did not know this was possible.
- **Elegant articulation** - the reader felt this but could not name it.
- **Recognition** - the reader's own experience, finally described.

An idea passing none of them yields a post that is accurate and unread. Say so plainly and help the user find the angle that passes.

Two beliefs block more good posts than anything else. Julia Evans' "Some blogging myths" (jvns.ca, 2023), the essay the filters above derive from, names both as myths.

- Originality: if it confused the author, it confuses others; the details differ by version and context.
- Expertise: "you actually just need to know 1-2 interesting things that the reader doesn't."

Publish uncertainty marked as uncertainty - "I think", "as far as I can tell" - never hidden.

## Pattern selection

This is a match test before it is a menu, and the test runs first: pick from the material, not from the goal. A pattern whose credibility section the author cannot fill is not an option to rank, it is an option to delete - strike it and say you struck it, or it returns later as scope.

- An author with no "what went wrong" material has no rewrite story; that post is a press release wearing an engineer's voice, and readers spot it in the comments.
- An author who never ran the comparison has no benchmark post.

Rank only what survives that test, and rank it by what the post returns per hour spent. Effort here is:

- writing and editing hours
- evidence you must go and produce before you can write a word
- the review chain the post has to clear

Rows are in efficiency order.

| Material you have                     | Pattern                          | Effort to publish                                                                  | What it buys                                                              | Section that carries its credibility                                |
| ------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| A timeline and a surprise             | Bug Hunt                         | an hour, on top of an incident review already written                              | the widest travel per hour on the list - engineers forward a good mystery | The dead ends you took                                              |
| A concept people get wrong            | Explainer                        | an hour; the material is your own understanding                                    | an evergreen page you and others link for years                           | Common misconceptions                                               |
| A system and its design decisions     | How We Built It                  | a week, reconstructing decisions nobody wrote down                                 | peer trust, and inbound from engineers who want to work on it             | Each decision framed as a trade-off                                 |
| Before/after numbers from a migration | Rewrote It in X                  | a week, when the numbers already exist                                             | the strongest evaluation evidence a reader can act on                     | What went wrong                                                     |
| Several incidents, one theme          | Lessons Learned                  | a week, and the incidents have to have happened already                            | standing: the reader treats you as someone who has seen this before       | A concrete story per lesson                                         |
| An opinion and some evidence          | Thoughts on Trends               | an hour to draft, most of it spent on the steelman                                 | a reach spike with a short shelf life, on the weakest evidence class      | The steelman of the opposing view                                   |
| Your own product, told as engineering | Non-markety Product Perspectives | a week, plus a disclosure and marketing review chain                               | qualified evaluators, when it survives that chain intact                  | The behind-the-scenes detail, plus a plain statement of who you are |
| Measurements comparing options        | Benchmarks and Test Results      | a quarter, when the runs, the re-runs and the publishable scripts do not exist yet | the most durable credibility here, and the post competitors have to cite  | Methodology, stated before results                                  |

- efficiency: bug hunt > explainer > how we built it > rewrote it in X > lessons learned > thoughts on trends > non-markety product > benchmarks
- value: benchmarks > rewrote it in X > how we built it > bug hunt > non-markety product > lessons learned > explainer > thoughts on trends
- effort: benchmarks > rewrote it in X == how we built it == lessons learned == non-markety product > bug hunt == explainer == thoughts on trends
- compliance cost: benchmarks against a named competitor > non-markety product > bug hunt > how we built it == rewrote it in X == lessons learned == thoughts on trends == explainer

Tie justifications:

- The four `a week` patterns tie on effort because their cost is the same act: reconstructing decisions or stories you lived through but never wrote down.
- The three `an hour` patterns tie on effort because their material already exists in a document or in your head, so only drafting remains.
- The last five patterns tie on compliance cost at nothing: no review beyond the technical one, and any of them can be corrected in public with a dated note.
- The three above them do not tie: a competitor comparison invites a legal read and is hard to withdraw once quoted, a product post needs the commercial disclosure agreed before publication, and an incident post needs the security and customer-confidentiality read.

The efficiency order starves Benchmarks and Test Results: it is first on value and first on effort, so a ratio defeats it every round, and an author who only ever computes efficiency never publishes the one post that would be cited for years. Promote it when:

- the buying decision in your category is made on numbers nobody has published
- a competitor's benchmark is circulating unchallenged
- the interview returned a compounding mandate with no near date and a ceiling that genuinely allows a quarter

The order is a default, not a law: it shifts with context and with who writes. Re-rank it against what you already know about this author.

- A benchmark harness already running in CI drops Benchmarks from a quarter to a week and moves it near the top.
- A public incident review already published makes Bug Hunt near-zero.
- An author whose employer requires marketing sign-off on anything naming the product pushes Non-markety Product Perspectives down a rung or two.

When two survivors land in the same position, pick by the reader's question, and split rather than merge.

Attribution:

- The first seven names are the pattern vocabulary of _Writing for Developers_ (Piotr Sarna and Cynthia Dunlop, Manning), one chapter per pattern, names verified against the published chapters.
- "Non-markety" is the book's own spelling, kept verbatim so you can match it to its chapter.
- The Explainer is this skill's own addition - never present it to the user as part of that published set.
- The effort, value and compliance judgements above are this skill's own, not the book's.

## The claim ledger

Every assertion belongs to one of four evidence classes:

| Class    | Means                                | In the post                                 |
| -------- | ------------------------------------ | ------------------------------------------- |
| Measured | A number from a run you can describe | Numbers plus methodology                    |
| Shown    | Visible in the post                  | Code, config, log excerpt, diff, screenshot |
| Sourced  | Someone else's documented claim      | Link to RFC, issue, doc, paper              |
| Opinion  | Your judgement                       | First person, marked as judgement           |

A claim in none of these classes is unsupported. It has three moves, no others:

- Cut it.
- Downgrade it to a marked opinion.
- Go get the evidence.

Performance, scale and reliability claims are checked first and hardest, so they get the strictest treatment.

Keep the ledger visible to the user while drafting. It doubles as the list of things the technical reviewer must confirm.

## Benchmark discipline

Classify the post before writing it, because the classification sets how much disclosure it owes. The three classes are the book's, from its benchmark chapter:

- **Benchmarketing** - you compare your own product against a competitor. Maximum scrutiny; every methodology choice is read as a thumb on the scale.
- **Subtle benchmarketing** - you measure something _using_ your product. The promotional intent is implicit but real, and readers still find it.
- **Community service** - you measure something independent of your products. Cheapest to defend, and the category that earns the credibility the other two spend.

The same chapter's posture for the whole pattern is "guilty until proven innocent": benchmark readers start from disbelief. The bar is that the numbers be truthful, reproducible, and not too synthetic:

- Truthful: the run happened as described, including the parts that went badly.
- Reproducible: a reader with your scripts and hardware gets the same shape of result.
- Not too synthetic: the workload resembles something someone actually runs.

Disclose, near the numbers or one click away:

- hardware or instance type
- version of everything compared
- workload and dataset
- configuration and tuning applied to each side
- number of runs and their variance
- a link to the scripts

Carry at least one chart - this pattern is read visually, not as prose.

Give absolute values alongside ratios. "3x faster" hides whether the gap is 3ms versus 1ms or three hours versus one.

Tuning your own side while leaving the comparison at defaults is the specific move that gets a post publicly dismantled. If you cannot tune both sides fairly, say which side is untuned and treat the result as indicative rather than conclusive.

## Trade-offs and limitations

Every post that recommends something owes the reader a section on where it does not apply:

- workloads it is wrong for
- the cost paid for the win
- what remains broken
- what was never tested

Publishing limitations before a reader finds them converts your weakest point into a trust signal.

A comparison table where every row favours you is a tell. Fill at least one row honestly the other way, or drop the table.

## Code in the post

Snippets are the part readers copy, so they carry disproportionate trust:

- Runnable as shown, or explicit about what is elided.
- Imports and setup included; expected output shown.
- Realistic names and values, not `foo`/`bar`.
- One concept per block, roughly twenty lines or fewer - this skill's working limit, not a published standard. Link the repository for the full version.
- Versions pinned and the post dated - a snippet against a since-changed API is worse than no snippet.

## Register

Write as the engineer who did the work:

- first person
- what was hard
- what got cut
- what is still ugly

A post that reads like a press release signals that no engineer was allowed near it. Replace the adjective with the number, then state the boundary of that number - [./references/worked-examples.md](./references/worked-examples.md) has four before/after pairs of exactly that move.

Run [./scripts/scan-draft.sh](./scripts/scan-draft.sh) over the draft. It flags:

- superlatives
- hedge-free absolutes
- unsourced numbers
- undated version references

It is a grep pass, not a judge - review every hit yourself, and keep any it flags when the evidence supports it. On a benchmark-heavy post, add `--no-numbers` once every figure is already in the ledger, or the numeric check drowns the rest.

## Blog context

The craft above is identical everywhere. What changes is the surrounding obligation.

- **Company engineering blog.** Disclose the commercial interest in the post, not in a footer: the product being sold, the open-core boundary, who funded the work. Clear the post with whoever owns security and customer confidentiality when it touches either. Attribute the work to named engineers - an unsigned corporate post starts at a trust deficit.
- **Personal blog.** No disclosure machinery, but state your relationship to what you are writing about (employer, maintainer, competitor) whenever it could look hidden later.
- **Sales-led B2B developer audiences** - a buyer or architect is often evaluating. Name the alternatives, say where they are better, and expect the post to be read by their engineers too.
- **Product-led (PLG) B2B developer audiences** - the reader is a developer who will later champion the product inside a company. The post feeds the developer-champion, not the buyer. Call-to-action and proof-loaded sections land differently: optimise for "try it now" and outcome velocity, not "contact sales".
- **B2C / individual-facing engineering audiences** - the reader is a peer engineer, not a buyer; there is no purchase to influence, so the post lives or dies on engineering substance alone. Resist inserting product marketing into it - the audience came for the system, and the recruiting value is the return.

## Incident-derived posts

Derive a public bug-hunt or outage post from the internal review; never copy it. Run a redaction pass before drafting:

- Remove individual names and handles, internal service codenames, ticket IDs, and wiki links.
- Decide deliberately whether impact figures ship.
- Keep the blameless framing - the post explains what conditions allowed the failure, not who typed the commit.

Then add what no internal document carries: why a reader who was not affected should keep reading.

## Revise, review, ship

Revise in four passes, in this order - the passes are the book's; running them out of order polishes sentences that later get cut:

1. **Core** - facts, focus, flow. Are the facts right, is the post about one thing, does each section earn the next?
2. **Clarity** - can a reader who was not in the room follow it?
3. **Components** - code, images, tables, lists: does each one earn its space?
4. **Consumability** - does it survive being skimmed?

Run the review like a code review - the book's own framing, and the mental model the author already has. Brief the reviewers instead of forwarding the draft:

- Say what you want checked (facts, clarity, or both).
- Give the background they lack.
- Flag any blocker question.

Get two reads, not one:

- An engineer who worked on the system checks accuracy.
- Someone outside the team checks it reads without insider vocabulary.

Real programmes vary less in who writes than in who signs off. Dan Luu's survey of corporate engineering blogs (danluu.com) found the blogs he rated compelling kept that chain short, with one clear owner:

- Heap pairs the engineer-writer with a fellow-engineer "buddy" who edits and approves, then the CTO reads with "usually only minor feedback."
- Segment now has a full-time editor who owns editing; earlier drafts went to the co-founder and an engineering manager. Co-founder Calvin French-Owen: "In general we try to keep it fairly lightweight. I see the bigger problem with blogging being a lack of posts or vague, high level content which isn't interesting rather than revealing too much."
- Cloudflare's CTO, John Graham-Cumming, reads and approves every post directly, with legal turning around in about an hour.

The blogs he rated weaker routed drafts through many stakeholders instead, which left posts vaguer as each approver removed specifics.

A joint post with another organisation multiplies approval chains - start them earlier than feels necessary.

Ship last:

- Preview the post where it will actually appear - code blocks and tables break in the CMS, not in the draft.
- Then handle the metadata: title tag, meta description, URL slug, link targets, image alt text, tags.

## Humanizer pass

Run the prose through your preferred humanizer skill before publishing. Model-flavoured filler reads as inattention to a technical audience and undercuts the evidence work:

- hollow transitions
- uniform sentence rhythm
- significance inflation
- tidy triples

Preserve exactly as written:

- code blocks
- command output
- benchmark tables
- version numbers
- the title

Humanising a title or a snippet damages precision for no gain.

## Credibility gate

Do not hand over a post until all six checks hold. Iterate; report which check failed and what you changed. The six checks and their binary pass rule are this skill's own bar - a design choice, not a published standard - and the skill's only hard threshold.

1. **Claims classified - 100%.** Every assertion is measured, shown, sourced, or marked opinion.
2. **No unsourced numbers.** Every figure traces to a run, a log or a citation. Delete rather than estimate.
3. **Benchmark disclosure complete**, when the post has comparative numbers.
4. **At least one honest limitation** stated, specific enough to be actionable.
5. **Zero unsupported superlatives.** Any "fastest", "seamless", "revolutionary", "best-in-class" is either backed by a measurement in the post or gone.
6. **Snippets pinned and dated**, with the full version linked.

Reach and engagement targets are not set here. No honest public benchmark exists for engineering-blog read-through, so derive targets from the user's own analytics baseline instead.

## Invocation examples

- _"Here are my notes from Tuesday's outage - turn them into a post."_ → draft mode, Bug Hunt, redaction pass first.
- _"We moved the ingest service from Python to Rust, write it up."_ → draft mode, Rewrote It in X; refuse to proceed until the "what went wrong" material exists.
- _"Review this before we publish Thursday."_ → edit mode, fix list, no rewriting.
- _"Make this sound less like marketing."_ → edit mode, register and superlative checks first, then the full gate.
- _"Blog post about our new query planner."_ → likely Non-markety Product Perspectives; ask what an engineer outside the company learns from it.

Draft mode returns, in order:

1. the mode and pattern chosen
2. the claim ledger
3. an outline for approval
4. the drafted post
5. the gate report
6. the handoff list

Edit mode returns the gate report plus a fix list in three tiers: blocking, strong, optional (this skill's own triage scheme).

- Order items by trust damage, not document position.
- Quote the line each item objects to.

See [./references/worked-examples.md](./references/worked-examples.md) for both shapes filled in.

## Failure modes

See [./references/failure-modes.md](./references/failure-modes.md) for a symptom/cause/fix table - load it when a draft, a published post, or a review round is going wrong.

## Measurement

Judge a post on whether the right readers finished it and did something, not on raw traffic:

- Scroll depth and read-through rate against the post's length, not page views alone.
- Referrals from developer surfaces (aggregators, community threads, newsletters) - where technical posts actually travel.
- Click-through to the artefacts the post links: repository, docs, benchmark scripts.
- Qualitative signal: engineers replying with their own numbers, corrections, or "this is the post I needed" messages. One substantive reply outweighs a traffic spike.
- For recruiting-oriented posts, inbound mentions of the post in applications.

Do not attribute revenue to a single post. Overclaiming attribution costs credibility with the exact audience this artefact serves.

## References

- See `samber/developer-relations-skills@developer-quickstart-guide` for first-success getting-started pages.
- See `samber/developer-relations-skills@changelog-writing` for release notes.
- See `samber/developer-relations-skills@version-migration-guide` for upgrade guides.
- See `samber/developer-relations-skills@developer-case-study` for customer stories.
- See `samber/developer-relations-skills@oss-launch` for launch announcements and their channel mechanics.
- See `samber/developer-relations-skills@devrel-content-calendar` for scheduling this post alongside other content.
- See [./references/post-patterns.md](./references/post-patterns.md) for each pattern's section order, proportions and specific traps.
- See [./references/worked-examples.md](./references/worked-examples.md) for a filled claim ledger, a benchmark disclosure block, before/after rewrites of a marketing-voice draft, a limitations section, and an edit-mode fix list.
- See [./references/failure-modes.md](./references/failure-modes.md) for the symptom/cause/fix lookup table.
