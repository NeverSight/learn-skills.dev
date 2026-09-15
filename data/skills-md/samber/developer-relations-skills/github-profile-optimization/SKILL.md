---
name: github-profile-optimization
description: Audits and rebuilds a personal or organization profile on GitHub as a developer-relations surface - the profile README, the six pinned items, bio and social fields, the organization profile repository, and the contribution signals visitors read as evidence. Use whenever someone says "optimize my GitHub profile", "profile README", "our GitHub org page is empty", "what should I pin", "nobody knows what our company builds on GitHub", or is preparing a launch, a talk or a job search - even if they only mention their GitHub page. Covers solo maintainers, company organizations, and engineers whose profile gets read during hiring. GitHub-scoped: the audit script and pin/contribution-graph mechanics are GitHub-specific, though the checklist reasoning transfers by hand to another forge. Not a single repository's README - use samber/developer-relations-skills@readme-optimization.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# GitHub Profile Optimization

You are working on the page a developer lands on after a talk, a package listing, a search result, or a job posting; it's the one an evaluator opens to decide whether the people behind a project are real. Your job is to diagnose that page against evidence, then rebuild it around a single outcome the owner names out loud.

Two constraints shape everything:

- The profile README and the six pinned items are the only editorial control the account has; everything else on the page (stars, languages, the contribution graph) is generated and cannot be argued with.
- The generated parts are weak evidence in both directions: forks, non-default branches, and unlinked commit emails never reach the graph, so a heavy contributor can look idle and a trivial one can look prolific.

## Calibrate what you promise

Most advice in this genre comes from people with a tool or a course to sell, and the independent evidence is thinner than they let on. Read [./references/published-findings.md](./references/published-findings.md) before quoting a figure or forecasting a result. What it settles:

- The profile is a **verification** surface, not a discovery one. Reviewers who open it arrive already curious and check whether something claimed elsewhere holds up. The best-evidenced signals, drawn from interview studies that predate profile READMEs entirely - are a real activity history and work on projects other people already use; a sparse profile tells a reviewer nothing either way.
- **Every threshold here is self-set.** No published rubric, cadence or benchmark exists for profile work, so the pass marks below are working defaults, labelled as such in the evidence file. Offer them as defaults the owner can move, never as an industry standard.
- **No validated framework exists either** - the one coined acronym in circulation has no adoption beyond its own post. Do not repeat it and do not invent a replacement; the audience question below plus the scorecard do the work a framework would claim to do.

Promise what the work actually delivers: a page that stops contradicting the owner's other material and routes a visitor deliberately. Do not promise interviews, stars or signups - no study measures whether a profile rewrite produces any of them. And note the scope: the published evidence here is English-language and US-centric; say so when the owner's hiring or market context is elsewhere.

Stay on the profile surfaces. Route to a sibling skill when the user's real problem is one of these, rather than stretching the profile to carry it:

- A single repository's README: samber/developer-relations-skills@readme-optimization
- The launch announcement: samber/developer-relations-skills@oss-launch
- Ongoing channel presence: samber/developer-relations-skills@oss-distribution-strategy
- The first-contribution path: samber/developer-relations-skills@oss-contributor-onboarding
- Sponsorship tiers and funding goals: samber/developer-relations-skills@oss-sponsors-fundraising
- Career positioning, interviews and progression: samber/developer-relations-skills@devrel-career

Typical invocations: "audit my GitHub profile", "rewrite our org profile README", "which six repos should we pin", "our GitHub looks abandoned but we ship weekly", "make my profile readable by a conference organizer".

Some asks deserve a redirect rather than a rewrite. "Get me more stars" and "fill my contribution graph" are requests to manufacture evidence, and "make my profile rank" asks for a lever the platform does not have. Say which it is, explain what it would cost in front of the reviewers who matter, and offer the audit instead - the goal underneath is usually legitimate even when the ask is not.

## Interview

Ask one question at a time, offer choices where you can, and skip anything you can determine yourself from the audit output. Questions 1-4 gate the rewrite: do not draft prose before they are answered.

1. Which account, and is it a personal profile or an organization?
2. Are you a maintainer after adoption and contributors, a company building developer awareness, or an engineer whose profile faces hiring scrutiny? Everything downstream branches on this answer.
3. What is the one outcome this page should produce more of: project adoption, contributors, inbound from companies, speaking and collaboration invitations, job or client leads, or sponsorship?
4. Who lands here most: developers arriving from a repository or package page, developers arriving from a talk or article, hiring managers and recruiters, or company evaluators sizing up the team behind a tool?
5. Individual adoption or company adoption? A developer deciding alone reads for capability; a team reads for maintenance, licensing and who to call when it breaks. Both is a valid answer.
6. What must the reader be able to do next - open a specific repository, read the docs, join a community, book a call, or contact you?
7. What is honestly true right now about activity: shipping weekly, maintaining, between projects, or dormant?
8. Anything on the page you are attached to and do not want touched?
9. For an organization: what is open source and what is commercial, and do you want that stated plainly?
10. Who owns this page after today, and what event will trigger the next review?
11. Is there a date this has to be right by - a launch, a talk, a funding round, an interview loop - or is it just overdue?
12. Do you want a one-off clean-up before that date, or a page that keeps working: a positioning sentence and a review habit you reuse for years?
13. What is your ceiling - an afternoon, a week of someone's time, a standing owner, a sign-off from legal or marketing on what you can say publicly?

Question 10 is not administrative. An unowned profile keeps a claim that was true when written, and a stale claim costs more trust than an empty page.

Answers 11-13 re-rank the fix order in Step 2; say which answer moved which fix when presenting it:

- A hard date promotes the near-zero fixes and drops the full page rebuild from this pass.
- A compounding mandate promotes the positioning sentence, which propagates into the bio, the org tagline and every link unfurl, and promotes the review habit that would otherwise never win on ratio.
- A ceiling with no standing owner deletes that habit outright rather than logging it as future work.

If question 2 lands on the hiring case, check the target before recommending much work. The one survey in this space with a disclosed methodology (from 2018, so treat it as dated) found portfolio weight concentrated at small and founder-led companies, and the recruiter testimony on record is largely indifferent to the surface.

A candidate aiming at large employers should invest in the resume first and use the profile only to avoid contradicting it. The staged, per-audience guidance is in [./references/published-findings.md](./references/published-findings.md).

## Step 1 - Collect the facts

Never audit from memory of what good profiles look like.

1. Run `scripts/profile-audit.py <account>` if the profile lives on GitHub and you can execute commands and reach the network - the script calls GitHub's own REST and GraphQL APIs and has no equivalent for GitLab, Codeberg or a self-hosted forge. It reports profile fields against their limits, whether the profile README renders and where it lives, its word/link/image counts, third-party widgets, time-bound phrasing, and the repositories a visitor finds when pins are unset. Set `GITHUB_TOKEN` to include pinned items and raise the rate limit. On any other host, apply the same checklist by hand from the profile page itself.
2. If you cannot run the script, open the profile page yourself (browse it, or ask the user to paste the README and list the pins). Say plainly which facts you could not verify instead of assuming them.
3. Open every link on the page and record the dead ones - a dead link fails a blocking check and takes minutes to fix.
4. Read the pinned repositories as a stranger would: does each have a description, topics, and a recent push?
5. If your environment has persistent memory, load any stored positioning statement, audience definition or competitor list for this account and reuse it rather than re-deriving it.

The script reports facts, not judgements. Fifteen images is not automatically wrong; it is a question to answer.

## Step 2 - Score the page

Work through [./references/profile-scorecard.md](./references/profile-scorecard.md) and produce its report format verbatim: four blocking checks, eight scored checks worth two points each, then the fix order below.

Attach evidence to every line - a quoted sentence, a field value, a line of script output. Present the score and get the owner's agreement before rewriting. A constraint you cannot see from outside (an employer policy, a deliberate minimalism) can justify a check you scored zero, and the owner is sometimes right.

Say once, when presenting the score, that the checks and the pass mark are this skill's own baseline rather than a published standard. An owner who moves the bar with a reason is not failing the audit; an owner who moves it because the page is easier to leave alone is.

### Order the fixes

Order the fix list by what each returns per hour spent, not by how much damage it undoes and not by how fast it is to finish - the three orderings disagree, so state them and lead with the last:

- effort, least first: `false claims == render prerequisites > private-contribution toggle > pins > positioning sentence > page rebuild > review habit`
- value, most first: `false claims > positioning sentence > pins > page rebuild > render prerequisites > review habit > private-contribution toggle`
- efficiency, do first: `false claims == render prerequisites > pins > positioning sentence > private-contribution toggle > page rebuild > review habit`

Killing a false claim and repairing the render tie on both axes, which is why they tie on efficiency. Each takes minutes, each is blocking, and each fixes a page that is _wrong_ rather than one that is merely weak - a reader cannot evaluate either kind of broken page at all. The private-contribution toggle sits lower than its near-zero effort suggests because it only helps the specific account whose public graph misrepresents real private work; for everyone else it changes nothing.

Default to the top three, an afternoon between them. Move to the positioning sentence when the owner can already say what the account is for, and to the page rebuild only when the cold-reader test fails on questions the top rungs do not touch.

The review habit is what this order starves: it is a standing job against fixes that land in minutes, so it loses every round. It is the only item that stops the page drifting false again, the failure this whole skill treats as most expensive.

Promote it above everything when:

- Answer 7 is "shipping weekly" or the account belongs to an organization, where the page goes stale fastest and nobody notices.
- This is the second audit of the same account.

The ordering is a default, not a law, and it shifts with who executes it. Re-rank it against what you already know:

- An owner with an existing positioning sentence from a launch or a talk gets that rung nearly free and should take it first.
- An account whose pins are already deliberate drops that row rather than re-deciding it.

Delete every fix answer 13's ceiling rules out instead of listing it last - an organization with no marketing sign-off does not get a "state what is commercial" line parked at the bottom of the plan, it gets that row removed and the reason recorded.

## Step 3 - Fix what is false before improving what is weak

These are the top rung of the fix order, and they hold that place on the ratio rather than in spite of it: each costs minutes, and each removes something that makes the page actively wrong instead of merely weak.

1. Remove or update every claim a reader can disprove: archived "currently building" projects, former employers, dead links, superseded roles.
2. Repair anything that breaks the render - see [./references/platform-mechanics.md](./references/platform-mechanics.md) for the four prerequisites that make a profile README appear at all, and the organization equivalents.
3. Replace a stale time-bound line with a dated one, or delete it. "Currently exploring X" with no date is a claim about today that nobody updates.

Only then move on to positioning and structure.

## Step 4 - Brainstorm the positioning before writing it

Do not reach for the first phrasing. Draft three candidate positioning sentences on different axes - what you build mechanically, what problem you remove for the reader, what the reader can stop doing. Present them with the trade-off of each plus your recommendation. Let the owner choose.

This sentence propagates into the bio, the organization tagline, link unfurls and search listings, so it earns the extra pass. Test each candidate against one question: could a competitor's account paste this sentence unchanged? If yes, it says nothing.

## Step 5 - Rebuild the page

Pick the skeleton from [./references/profile-skeletons.md](./references/profile-skeletons.md) that matches what the reader is deciding - maintainer, DevRel practitioner, engineer building credibility, or organization. Draft one section at a time and get agreement before moving on; a profile rewritten in one pass gets rejected in one pass.

Adjust for how adoption happens, because the two motions diverge after the first screen:

|                    | Individual developer adopts alone                 | Team or company adopts                                             |
| ------------------ | ------------------------------------------------- | ------------------------------------------------------------------ |
| Dominant question  | Can this person build the thing I need?           | What are we depending on, and who answers when it breaks?          |
| Must surface early | The work itself, running, with an entry point     | Licensing stance, maintenance cadence, support and security routes |
| Proof that lands   | Merged pull requests, a demo, a readable codebase | Named users, release cadence, funding model, team visibility       |
| Fatal omission     | No obvious first repository                       | No answer to "who maintains this"                                  |

The first screen is identical in both cases: who this is, what they build, which project to open first. Serve both audiences by adding a short evaluation block lower down, not by rewriting the top twice.

Rules that apply to every skeleton:

1. Put one sentence of prose above every image, badge and widget.
2. Cap decoration at three visual elements, each with alt text and each earning its place. Third-party stats and streak cards are external dependencies that the host's image proxy can cache stale indefinitely; a frozen widget is worse than no widget.
3. Say what is _not_ true: what you are not maintaining, what is commercial, what you will not take feature requests on. This is the highest-trust content on the page and it costs one line.
4. Give each pinned repository a description and topics before pinning it - a bare pin wastes one of six slots. This skill only requires that they exist; for how to write them well, see samber/developer-relations-skills@readme-optimization's furniture step.
5. Keep the page readable where rendered HTML is stripped: no meaning encoded in colour alone, no instruction that exists only inside an image.

Run the finished prose through your preferred humanizer skill. Profile copy that reads as generated undercuts the exact credibility the page exists to build.

## Step 6 - Set the pins deliberately

Six pins (six public plus six member-visible for an organization) are the only control you have over what a visitor clicks next. Choose them against the goal from question 3, not by star count.

These four sets are not ranked against each other and should not be: answer 3 selects one outright, and every pin costs the same nothing to set, so an efficiency order across them would be invented precision. The order _within_ each set is real - it decides which repository a visitor opens first.

- **Adoption**: flagship first, then the SDK or integration a new user needs second.
- **Contributors**: the repository with curated good-first-issues, then the one with the best contributor docs.
- **Credibility or hiring**: the work that shows judgement, even at low stars - a well-reviewed tool beats a popular list of links.
- **Organization**: an entry-point tour rather than a leaderboard; cover repositories the README prose does not already name, so the two surfaces together give a fuller picture.

Never pin an archived repository, a fork you did not substantially change, or an empty placeholder. Leaving pins unset is worse: the platform then auto-selects "Popular repositories", which often surfaces something abandoned.

## Step 7 - Handle contribution signals honestly

Read [./references/platform-mechanics.md](./references/platform-mechanics.md) before commenting on the graph or the achievements.

Three honest moves are available, and they are an order of magnitude apart:

- efficiency, do first: `private-contribution toggle > mechanical graph causes > merged pull requests elsewhere`

- Reach for the private-contribution toggle first when an employed developer's graph looks dead. It is one setting, and most of their work is private - so "freshness" here is a setting, not new public work.
- Fix the mechanical causes of a misleadingly empty graph next: unlinked commit emails, work that only ever lands on feature branches, contributions made in forks that never merged upstream. An hour to diagnose, then a habit to keep.
- Merged pull requests in other people's repositories are what this order starves: a quarter of real work, so they never win on ratio. They are still the single best-evidenced signal in the whole skill, since reviewers in the interview studies weight work on projects other people already use above everything else on the page. Promote them to first when answer 3 is credibility, hiring or collaboration invitations - nothing cheaper substitutes for them there, and they are checkable where the graph is not.
- Never advise commit padding, streak farming, star buying, or gaming the achievements. Reviewers who follow this space already discount all three signals:
  - Backdating a commit takes one environment variable.
  - Public tools paint pictures into the graph.
  - Star fraud runs at industrial scale: a five-and-a-half-year study of public event data counted roughly six million suspected fake stars across more than eighteen thousand repositories.
- Refuse these asks by name when an owner makes one: say what the tactic is, that reviewers discount it, and what you would do instead. They are deleted from the menu, not ranked last on it - a tactic parked at the bottom of a plan comes back as scope, and this one comes back as fabricated evidence.
- Treat streak and trophy widgets as a credibility trade, not a neutral decoration: they read as noise to senior technical reviewers and cannot see private work at all.

## Step 8 - Verify, then keep it alive

1. Re-run the scorecard. Ship when all four blocking checks pass and the scored total reaches **13/16** - this skill's own baseline, not a published bar. Below it, iterate rather than shipping with a caveat.
2. Run the cold-reader test from the scorecard: 45 seconds on the page, then four questions (five for an organization). Every answer correct is the pass - four of four, five of five for an organization. A fresh agent session with no context on the account is an acceptable stand-in when no person is available; your own reading is not.
3. Record the owner and the **events** that trigger the next review - a launch, a talk, a funding round, a major release, a role change, a job search. No evidence supports a fixed calendar cadence, and a quarterly reminder nobody honours is worse than a trigger list the owner recognizes. Put the list and the last-reviewed date in the file as a comment if nothing else will hold it.
4. If your environment has persistent memory, store the agreed positioning sentence, the audience, the goal and the final score, so the launch post, the conference bio and the docs landing page start from the same words.

## What to track afterwards

- efficiency, track first: `tagged click-through > pinned-repository traffic > qualified inbound`

Build each of the three in the order above:

- **Tagged click-through**: tagged links from the profile to a destination the owner controls - docs, product, community. It costs an hour to set up, the destination's analytics belong to the owner, and it is the only number here that survives scrutiny.
- **Pinned-repository traffic**: free but nearly useless on its own, limited to a trailing 14-day window and to repositories the owner can push to.
- **Qualified inbound**: what this order starves - reading it takes a standing habit and a quarter before it says anything. For an organization it is the only evidence the page changed anyone's behaviour, so promote it there and start counting from the ship date.

Qualified inbound reads differently per audience: for an organization it is a prospect who already knows what you build instead of asking, and for a practitioner it is a speaking or collaboration approach that references something the profile surfaces.

Everything else is partial. No host offers profile-level analytics, and nothing here isolates the profile's effect - write down the date you shipped, and annotate every confounder.

Delete two numbers from the plan rather than ranking them last:

- A README view-counter badge counts image requests through an anonymizing proxy (bots and repeat loads included) and public scripts inflate it, so it is decoration, not data.
- Star growth after a profile change is unattributable and, at the company level, actively gamed. Stars are known to follow promotion (a release, a talk, a mention elsewhere) rather than the page.

Assume the same of every other number here.

## Common failure modes

- **Decorating before diagnosing.** Adding widgets to a page whose first claim is false makes the false claim prettier. Score first.
- **One checklist for every audience.** A streak widget signals engagement to an early-career peer group and noise to the maintainer or hiring manager the owner actually needs to reach. Answer question 2 before recommending a single element.
- **Overselling the surface.** Nobody has measured whether a rewrite produces interviews or contributors; promising either invents an effect, and the owner notices when it never arrives. Promise clarity and consistency - the page genuinely delivers those.
- **Star-ranked pins.** The platform already shows star counts. Pins ordered by popularity waste the one editorial lever on repeating information the visitor can see.
- **Widget dependency.** Every third-party card is a service that can go down, rate-limit, or freeze in the image proxy. Keep at most one, and check it renders from a logged-out session.
- **Writing the organization profile as a second marketing site.** The visitor came to GitHub for the code. The page's job is to say which repository to open first and what is open source - the website already does the rest.
- **Treating the contribution graph as a scoreboard.** Advising anyone to fill it is advising them to fake evidence, and readers who know the counting rules discount the graph anyway.
- **Leaving the page unowned.** An unowned profile drifts false: the claim that was true when written stays up long after it stops being true. Name the owner and the review triggers in the same session as the rewrite.
- **Copying a template wholesale.** A profile that reads like ten thousand others is a profile the reader skips. Skeletons set the order; the sentences have to be the account's own.

## Reference

- [./references/published-findings.md](./references/published-findings.md) - which figures are published, which are self-set, the per-audience staged guidance, and the claims to refuse
- [./references/profile-scorecard.md](./references/profile-scorecard.md) - blocking and scored checks, thresholds, cold-reader test and report format
- [./references/profile-skeletons.md](./references/profile-skeletons.md) - per-audience section orders, worked positive and negative examples, and patterns observed on shipped organization profiles
- [./references/platform-mechanics.md](./references/platform-mechanics.md) - README prerequisites, field and pin limits, contribution-graph counting rules, achievements and image-proxy behaviour
