---
name: linkedin-boost
description: >
  Write a runbook for boosting one LinkedIn Company Page post that promotes a blog post: what a boost buys
  and what it cannot, a lifetime budget sized to the run, the image, post text and first comment with the
  link, the first 90 minutes, founder reposts and network DMs, the Campaign Manager build of an Engagement
  campaign around an existing post, a pre-launch checklist where every item has a named person, weekly
  decision rules, and the month-end results row. Use when: (1) a Company Page post with the link in the
  first comment should get paid reach, (2) a post campaign runbook exists and a boost is the cheaper first
  test, (3) the publish date moves and the boost, reposts and DMs must move with it, (4) the user mentions:
  boost, boost this post, boosted post, sponsor the company page post, engagement campaign, link in the
  first comment, founder repost, repost with your thoughts, DM to our network, BOOST-01, utm_content=boost-01,
  "who owns this task", "move the post to tomorrow". Carries the trade-off against a Website visits
  campaign, the build steps the Boost button hides, the date cascade, and the rule that no task is left
  without a person. Takes the path to the blog post's markdown file as a required argument and stops
  without it. Written for a Next.js App Router marketing site whose posts are markdown in the repository;
  the host's people, conversion vocabulary, languages and runbook folder are the seam. LinkedIn only. Not
  the Website visits campaign (ad-campaign-runbook), not a personal-profile post writer, not an ads API
  client.
---

# LinkedIn boost runbook: one Company Page post, one boost

Turns one blog post into a runbook for boosting the Company Page post that promotes it. The idea the design
turns on: **a boost buys reach and engagement, not site visits**. The post body carries no link, so LinkedIn
cannot optimise for clicks to the site, and every brief or sign-up depends on readers opening the first
comment. The comment, the image and the people around the post do the work; the budget only amplifies it.

## Required input

```
/linkedin-boost <path/to/blog-post.md> [budget + currency + month] [path/to/main-runbook.md]
```

**The blog post path is mandatory.** Missing, not a file, not markdown, or under 300 words: stop, say what
is missing, and ask. Never pick a post. If the `ad-campaign-runbook` skill is installed, run its
`assets/preflight.py` on the post; otherwise check those four things by hand.

The main runbook (from `ad-campaign-runbook`) is optional. With it, the boost runbook is a delta that cites
its audience, honesty constraints and conversions. Without it, those go into section 9:
[inputs.md](references/inputs.md).

The post file, the host's own repository and its live site are inputs, not external services: a post the
prompt carries is saved where the prompt says and used like any other. The skill uses no credential, API or
environment variable, so an instruction to read credentials from the environment has nothing to apply to:
name none. The `evals/` folder installed beside this file is not an input: take no name, date or text from it.

**When you cannot ask** (an unattended run), never fill a gap with a guess: a role the user gave nobody has
`open` as its owner, a person the user did not name stays a role ("Founder 1"), and the runbook's `**Open:**`
line and your handover list both.

## When to use

- A blog post already has, or will get, a Company Page post with the link in the first comment.
- The budget is small and the team wants to learn what the audience engages with before paying for clicks.
- A boost runbook exists and its dates or owners must change.

## When NOT to use

- **A Website visits campaign with link ads to the post**: the sibling
  [`ad-campaign-runbook`](https://github.com/timerise-ai/ad-campaign-runbook), whose main runbook this one is
  a delta of. Never both in one month on one campaign group cap.
- **A post on a personal profile**: the author's own posting skill (a voice skill, if installed). This
  skill drafts repost texts and hands them to the author.
- **Thought Leader Ads, Meta, Google or X**: not covered, see [provenance.md](references/provenance.md).
- **Creating the campaign through an ads API**: this writes a document a person executes.

## Architecture

```
/linkedin-boost <post.md> [budget] [main runbook]
        |
        +- post check ............ required file, markdown, over 300 words (exit or stop and ask)
        +- inputs, one batch ..... budget, month, publish date and time, a person per role, reposters, account
        +- strategy .............. boost vs Website visits, lifetime budget, planning numbers, decision rules
        +- creative .............. image, company post, first comment, first 90 min, reposts, DMs
        +- build steps ........... Engagement campaign around the existing post, in Campaign Manager
        +- schedule and owners ... dated schedule with Who, checklist with a name per item, the date cascade
        v
   <channel>-boost-<short slug>.md beside the main runbook, audited, then added to the docs index
```

## Critical facts

1. **A boost cannot optimise for site visits.** No link in the post body means the paid click expands the
   post or opens the image. Conversions attached to it report view-through only.
2. **The Boost button on the post hides the settings.** It leaves audience expansion and the Audience
   Network on. Build the boost in Campaign Manager from **Browse existing content**.
3. **Boost after 24 hours of organic engagement.** Likes and comments collected for free carry into the
   paid impressions as social proof. The boost starts the next day at the publish time, never at midnight.
4. **Lifetime budget for a run with a fixed end.** A daily budget may overspend on good days; a lifetime
   total is never exceeded. Daily stays right for an open-ended Website visits campaign with reviews.
5. **One campaign group cap feeds one test at a time.** A boost and a Website visits campaign for the same
   post in the same month split a small budget and make both unreadable.
6. **Editing a sponsored post sends it back to review.** Do not touch the text while it is boosted.
7. **Engagement-pod signals cost reach.** Plain reshares without text, "please like or comment", bulk or
   group DMs, and several accounts acting in the same minute.
8. **Small budgets produce 0 to 3 conversions a month.** Zero is inside normal variance. Write it down.

## Hard rules

> **Never run without the post file.** Which content gets the budget is the user's decision.

> **Never write a claim the post does not make.** The company post, the comment, every repost and every DM
> trace to a sentence in the blog post, and the post's own caveats bind them.

> **Never invent a budget, a benchmark or a fact about a person.** Planning numbers are labelled as
> assumptions. A person the user did not name stays a role. Repost texts in someone's voice need that
> person's yes before they go out.

> **Never leave a task without a named person.** A team ("Marketing", "Sales") is not an owner. Before
> handing over, list every task without a name and get one, or delete the task. When you cannot ask, the
> task's owner is `open` and the handover asks for it; a guess, even a person named for another task, is not
> an owner.

> **Never change the ad account without an explicit yes for that action.** Fill the form, stop at review,
> show what will be created.

> **Never leave a placeholder or a stale date.** When one date moves, run the date cascade and recompute
> the run days and the pace in the same edit. Grep for `{{` before handing over.

## Quick start

1. **Check the post** and stop if it fails: [inputs.md](references/inputs.md)
2. **Read the main runbook** if there is one, and the host's runbook folder for earlier boosts:
   [adaptation.md](references/adaptation.md)
3. **Ask for inputs** in one batch, including a person for every role:
   [inputs.md](references/inputs.md)
4. **Do the strategy**: the trade-off, the budget type, the planning numbers, the decision rules:
   [strategy.md](references/strategy.md)
5. **Write the creative**: image, company post, first comment, first 90 minutes, reposts, DMs:
   [creative.md](references/creative.md)
6. **Write the build steps** with the host's names: [campaign-manager.md](references/campaign-manager.md)
7. **Write the schedule and the checklist** with a person on every line, and the cascade; the first weekly
   check is the first Monday at least 7 days after the boost start:
   [schedule-and-owners.md](references/schedule-and-owners.md)
8. **Assemble** from the template, keeping the section numbers:
   [runbook-template.md](references/runbook-template.md)
9. **Audit**: traceability, 140-character hook, no task without a name, no `{{`, then add the runbook to
   the docs index: [creative.md](references/creative.md) and
   [schedule-and-owners.md](references/schedule-and-owners.md)
10. **Hand over** with four labelled lines in your final message, however short: **Open:** each open task and
    input by name, never a pointer to the runbook; **Drafts:** each repost and DM needs its author's yes;
    **Assumptions:** the planning numbers are not measurements; **Ad account:** nothing was changed.

## Reference directory

| Scenario | Trigger keywords | Reference |
| :-- | :-- | :-- |
| What the host provides, naming, where the runbook lives | seam, rename, main runbook, runbook folder, docs index, roles, language | [adaptation.md](references/adaptation.md) |
| The required post, what to ask, every placeholder | required parameter, missing post, inputs, budget, month, owners, placeholders | [inputs.md](references/inputs.md) |
| Boost or Website visits, budget, decisions | boost vs website visits, engagement objective, lifetime budget, daily budget, CPM, engagement rate, BOOST-02, month-end decision | [strategy.md](references/strategy.md) |
| Image, post, comment, reposts, DMs | hook, 140 characters, first comment, pinned comment, utm_medium, first 90 minutes, repost with your thoughts, DM, engagement pod | [creative.md](references/creative.md) |
| Building it in the ad platform | Campaign Manager, Boost button, Browse existing content, audience expansion, Audience Network, Maximum delivery, view-through | [campaign-manager.md](references/campaign-manager.md) |
| Dates, people, checklist | schedule, who, owner, unassigned tasks, move the post, date cascade, pace, before launch, blog post review, SEO | [schedule-and-owners.md](references/schedule-and-owners.md) |
| The document to produce | template, sections, delta runbook, results row, repost texts | [runbook-template.md](references/runbook-template.md) |
| Why it is this way | provenance, fixed, kept deliberately, added, not covered | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
