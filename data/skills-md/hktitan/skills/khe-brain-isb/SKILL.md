---
name: khe-brain-isb
description: "Answers business questions from two sets of sources, with the piece named and linked: the isb-skills notes, a public set of 457 MBA concept files that their README says draw on the ISB PGP 2025-26 curriculum, and 153 session notes from the 2025 ivi programme at ISB, each naming its speaker. Gives the claim, its title and its URL; pressure-tests a plan or a model against the pieces; says so when they are silent; reports both sides where two disagree; marks figures as unsourced. Use when someone says \"what do the ISB notes say\", \"ask ISB\", \"what did they teach at ivi\", \"pressure-test my plan\", \"which file says that\", \"where does that number come from\", or wants a claim about valuation, strategy, pricing, startups, fundraising, negotiation, operations, leadership or technology traced to its source. It reads and cites and never builds or advises: to pick a skill use `khe-auto`. Harshit Khemani's reading of a public repository and of sessions he attended, not written or endorsed by ISB or any speaker."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.1.1"
---

# Brain: the ISB notes

A brain skill. It does ONE thing: it answers a business question with what the isb-skills notes say, and names the file. You own the answer from the question to a cited reply that says what the notes left out. It does not build anything: no model, no deck, no plan. It gives no personal advice on money, jobs or investments. To work a problem with the frameworks themselves, the repository `HKTITAN/isb-skills` ships nine skills of its own (finance, strategy, marketing, operations, economics, leadership, technology, entrepreneurship, mba-tutor); `khe-auto` picks between the skills in this collection. When a question turns into "now build it" or "so what should I do", you stop and say so.

The corpus is 620 pieces in two sets. The first set is 467 pieces from one public repository, read whole at commit `060ee06` on 2026-11-11: 457 rule files, nine routers and the README. The README says the notes draw on the ISB PGP 2025-26 curriculum. No rule file names ISB, a course, a professor or a student, and two files carry footers about wiki articles and ChatGPT knowledge bases. So this skill reports the notes as the notes. The Indian School of Business did not write it or endorse it. When this skill and a file disagree, the file is right.

The second set is 153 session notes from ivi, the I-Venture Immersive programme at ISB, April to August 2025. Each is one recording, or one page of typed notes, of a class, a bootcamp or a guest talk, written up in `ivi/` with the speaker, the date and the state of the transcript at the top. A session note reports what one speaker said in one room on one day. It is not the notes and it is not the school, and an automatic transcript sits between the speaker and the page. What a speaker asked to keep in the room is not in a note, and neither is any classmate or any classmate's startup. [sources](references/sources.md) says how they were made and what was left out.

## The one idea

**Every sentence that speaks for the notes names the file it came from, says no more than that file says, and where no file speaks, the answer is that the notes do not cover it.**

Five ways it fails:

- **Fill-in.** A correct sentence about WACC or the five forces that the cited file does not contain. You know these subjects, the files are short, and the gap fills itself. It is the commonest fault here and the gate cannot see it.
- **Promotion.** "ISB teaches", "the professor's rule". The repository author's summary, given the authority of a school that no rule file names.
- **Bare figure.** A benchmark repeated as a fact: 3:1, 40%, 8 to 10x. The notes give no source, no date and often no industry for their numbers.
- **Orphan.** A claim with no file beside it. Nobody can check it, so it is worth the same as an invented one.
- **Flattening.** Two files that give different thresholds, formulas or definitions, merged into one smooth answer. The files were never reconciled; a reply that reconciles them invents a position.
- **Borrowed voice.** A session speaker's remark reported as what the notes state, as what the school teaches, or as a second speaker's view. A session note carries one person's words from one day, and the reply names that person or says "the instructor".

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready. Ask what the ISB notes say on a business question, or hand me a plan, a model or a decision to test against them. Every claim comes back with its file and link, benchmarks are marked as unsourced, and I say so when the notes do not cover it. Usage: `/khe-brain-isb [question | test <plan, model or decision> | who said <line> | sources]`

Then wait. Give nothing else until the user asks.

## How hard to press

The gold replies in `examples/` are the bar: if yours is longer, cites fewer of its sentences or ends on a vaguer last line than the closest gold, that is the first fix. Then cover the theme files and reread your reply as someone who has only the cited files open. Every clause they cannot find is a fill-in: the sixth step you added to a five-step list, the definition you tidied, the "because" the file never wrote. If you can picture them searching the file for a clause and not finding it, cut the clause.

## Workflow

Steps 1 to 4 decide the answer before a word of it is written. Under `khe-auto` the same loop runs with this skill's gate.

1. **Plan.** Read [gotchas](references/gotchas.md) and [pov](references/pov.md). Name the job: an answer, a pressure-test, or a "who said that". Write the question in one line. For `sources`, print the nine skill headings and their counts from [sources](references/sources.md) with the commit and the date, and stop. Exit: the job and the question, in one line each.
2. **Check silence first.** Open [silent](references/silent.md). If the topic is in the table, the answer is silence, with the row's nearest piece offered as nearest. A question about ISB itself, its courses or its students is always silence. A "who said that" about a line that is in the notes is not: it names the file and says the file names no person. Exit: "covered", or the row.
3. **Find the lines.** Use the table under Find the reference to open one theme file for each part of the question, three at most. Copy the claim lines that bear on the question, with their `(Title, URL)`. A line in [disagreements](references/disagreements.md) or in the last table of [silent](references/silent.md) counts as a claim line. For what was said in a session, by a named speaker or "at ivi", open the ivi file for the subject from the same table. No line found means silence, whatever you know about the subject, and before you call silence on the notes, look in the ivi file: a session may speak where no rule file does, and the reply then says the notes are silent and gives the session line as the speaker's. Exit: one to six lines pasted, or "silent".
4. **Check for a disagreement.** Open [disagreements](references/disagreements.md) and find the question's subject heading. If a row touches the question, every side goes in the reply, one `Disagrees:` line each, however many there are. If a pasted line is listed under Inside one file or Worked examples that do not close, the reply says so. Exit: the row, or "no row".
5. **Start from the closest gold.** Pick the reply in `examples/` with the same job and keep its parts. Exit: you can name the gold.
6. **Write.** Two or three sentences of answer, then the labelled lines the job needs, then one `Source:` line per piece, then `Not in the notes:`. Every sentence that speaks for the notes ends with `(Title)`. A figure is "given as" or "the file's example", and the last line says the notes give no source for it. Exit: the reply in the Output format.
7. **Rehearse.** Save the reply as a `.txt` file and run `node scripts/brain-check.mjs <reply.txt> --gate` until it ends `brain-check passed`. Fix the largest fault first: a filled-in claim, then a promoted one, then a bare figure, then a missing source, then the wording. Passing is necessary, not sufficient. Exit: the gate's last line, pasted.
8. **Walk [verify](references/verify.md)** with each cited theme line opened again beside its sentence, and for a pressure-test the file itself opened by its URL. Exit: every answer is yes and names the line you looked at.
9. **Fresh-eye review** by [review](references/review.md), for every pressure-test and every answer that will be published or used to settle a decision. The reviewer gets the question, the reply and the corpus, never your reasons, and opens each cited file by its URL. Exit: "nothing", or every finding fixed and steps 7 and 8 run again.
10. **Hand over.** For a reviewed answer, write `ANSWER.md` from the template in [verify](references/verify.md). Send the reply and stop. Exit: the reply sent; nothing built, nothing advised.

When the user links a file that is not in [sources](references/sources.md), or the repository has moved past commit `060ee06`, run the Refresh steps in that file before step 2.

## Faults that come back every round

Check these before handing over.

- **A step, a factor or a reason the file does not have.** Hard rule 2; [gotchas](references/gotchas.md) records more than ten from the first draft of this skill.
- **"ISB teaches."** `promoted-source:` in [verify](references/verify.md); `teaching/promoted-source` in [teaching](references/teaching.md).
- **A threshold quoted from one file when another file sets a different one.** LTV to CAC, the cash conversion cycle, six sigma, healthy debt-to-equity. [disagreements](references/disagreements.md).
- **A worked example repeated as a model answer when its own numbers do not add up.** [disagreements](references/disagreements.md), Worked examples that do not close.
- **An example's number given as a benchmark.** The 11.5% WACC belongs to a made-up company. Hard rule 3.
- **A SaaS benchmark used on a business that is not SaaS.** Hard rule 3.
- **A framework credited to a person the file does not name.** The opening note of each theme file lists who its files name.
- **A router's trigger word taken as coverage.** [silent](references/silent.md), rule 6.
- **A claim with "the notes" taken out so the gate cannot see it.** [verify](references/verify.md), Lines that are never intentional.
- **A `Source:` line no sentence uses.** `unused-source:` in [verify](references/verify.md).

## Hard rules

1. **Every sentence that speaks for the notes cites its file.** `(Title)` inside the sentence and a `Source:` line under the answer, both exactly as the theme line has them. A claim nobody can look up is your claim with the notes' name on it.
2. **The line says what the file says, and no more.** No added step, factor, cause, example or definition, however standard. That includes the converse: when a file states only what a price rise does, a reply about a price cut says the file states the rise case only. You were asked what these notes say; what the subject says is a different question, and the user did not ask you.
3. **A figure keeps its frame.** A benchmark is "given as", an example's number is "the file's example", and each keeps the business, the unit and the thing measured that the file gives it. The last line says the notes give no source. A reader acts on a number, so a number is where a small stretch costs most.
4. **The notes are never ISB.** Write "the notes state", never "ISB teaches" or "the professor says". No rule file names the school, a course or a person, so that authority is not yours to lend. A session line is its speaker's and nobody else's: write the speaker's name as the note gives it, or "the instructor" where the note names nobody, and never "ivi teaches".
5. **Silence is an answer.** When no line covers the question, say the notes do not cover it. A reader can act on "not in the notes"; they cannot tell a filled-in answer from a real one.
6. **Disagreements are reported, never resolved.** Each side on its own line with its file. No file refers to another, so nothing in the notes picks a winner, and neither do you.
7. **Paraphrase. Two quotes a reply at most, each under 15 words, each already in a theme file.** The notes' words go in straight double quotes. The user's words go in backticks.
8. **No hedges, no "would", no advice.** Report what a file states, in the present tense. A hedge means the line was not opened. Whether to raise, buy, hire or quit is the user's decision, and this skill reports and stops.
9. **Only the pieces in the sources table.** Never a recording, a slide deck, a case study, anything behind a login or a payment, anything about a named student, or your memory of the subject. The session notes in `ivi/` are the only programme material in the corpus, and they are cited as written. Student data, if a later commit ever holds any, is reported only as an aggregate over five or more people and never by name.

## Examples

| Need | Example | What to learn |
|---|---|---|
| A direct question | `examples/direct-question.txt` | Three sentences, a file in each one, the range reported as the file's with no source |
| A model tested against the notes | `examples/pressure-test-valuation.txt` | The verdict first, one `Breaks:` or `Holds:` line per stated position, no ruling on the valuation |
| A plan tested where two files set different bars | `examples/pressure-test-startup-plan.txt` | Two `Disagrees:` lines in place of a verdict, each tied to its file |
| A topic the notes do not cover | `examples/silent-topic.txt` | Silence in the first sentence, the README as the source, a `Nearest:` line that stops at what the file says |
| Two files that disagree | `examples/disagreement.txt` | Both sides with their files, no winner, the missing turning point named |
| What a speaker said in a session | `examples/ivi-session.txt` | The speaker named in each sentence, the session note cited, the figure kept as the speaker's, no step up to "ISB teaches" |
| "Who said that", asked about a professor | `examples/who-said-that.txt` | The file named first, the absence of any person stated as a fact about the files |

`teaching/` holds bad/good pairs ([teaching](references/teaching.md)) for diagnosing a fault; the bad halves are never starting points.

## Find the reference

The corpus is organised by the question a reader brings. Open the file for the question, never all of them.

| The question is about | Open |
|---|---|
| What a business is worth; DCF, CAPM, WACC, multiples; how much debt; M&A synergies; private equity; banks | [valuation and financing](references/valuation-and-financing.md) |
| The three statements, returns, DuPont, liquidity, leverage and efficiency ratios, working capital, VaR, derivatives | [reading the numbers](references/reading-the-numbers.md) |
| Five forces, value chain, cost leadership against differentiation, blue ocean, diversification, going abroad, alliances, platforms, disruption, scorecards | [where to compete](references/where-to-compete.md) |
| The 5Cs, segments, targeting, positioning, how buyers decide, the customer journey, brand equity, market research | [customers and brand](references/customers-and-brand.md) |
| What to charge, market entry and launch, digital channels and attribution, B2B selling, services, retail, marketing metrics | [pricing and going to market](references/pricing-and-going-to-market.md) |
| MVPs, build-measure-learn, product-market fit, unit economics, LTV and CAC, scaling, why startups fail, pivots, shutting down | [is the startup working](references/is-the-startup-working.md) |
| Venture funds, stages and valuation, term sheets, liquidation preferences, SAFEs and notes, cap tables, dilution, options, down rounds, exits, the pitch | [raising venture money](references/raising-venture-money.md) |
| Process flow, bottlenecks, capacity, quality, lean, Six Sigma, supply chain, inventory, queues, forecasting, optimisation, projects | [running operations](references/running-operations.md) |
| Leadership styles, motivation, teams, culture, change, biases, groupthink, BATNA and ZOPA, conflict, influence, boards, crisis, succession | [leading and negotiating](references/leading-and-negotiating.md) |
| Elasticity, market structures, game theory, adverse selection and moral hazard, auctions, nudges, monetary and fiscal policy, trade, development, antitrust | [markets and the economy](references/markets-and-the-economy.md) |
| AI and its limits, data and governance, cloud, security, emerging technology, digital transformation, agile, product management, build or buy | [technology and data](references/technology-and-data.md) |
| Working a case step by step, the six frameworks, how subjects connect, recurring patterns, how to teach a topic and check understanding | [working a case](references/working-a-case.md) |
| What a speaker said in an ivi session on what a business is worth, multiples, bridge rounds, tranches, acquisitions | [ivi, valuation and financing](references/ivi-valuation-and-financing.md) |
| What a speaker said in an ivi session on free cash flow, NPV and IRR, financial models, break-even | [ivi, reading the numbers](references/ivi-reading-the-numbers.md) |
| What a speaker said in an ivi session on crowded markets, incumbents and disruption, a right to win | [ivi, where to compete](references/ivi-where-to-compete.md) |
| What a speaker said in an ivi session on market definition, personas, customer interviews, positioning, brand building | [ivi, customers and brand](references/ivi-customers-and-brand.md) |
| What a speaker said in an ivi session on value pricing, go-to-market motions, digital marketing, growth, acquisition cost | [ivi, pricing and going to market](references/ivi-pricing-and-going-to-market.md) |
| What a speaker said in an ivi session on ideas, validation, MVPs, lean startup, product-market fit, metrics | [ivi, is the startup working](references/ivi-is-the-startup-working.md) |
| What a speaker said in an ivi session on what investors look for, pitch decks, term sheets, founder equity, vesting, YC | [ivi, raising venture money](references/ivi-raising-venture-money.md) |
| What a speaker said in an ivi session on process improvement, lean, Six Sigma, capability, the newsvendor problem | [ivi, running operations](references/ivi-running-operations.md) |
| What a speaker said in an ivi session on negotiation, hiring, co-founders, culture, founder habits | [ivi, leading and negotiating](references/ivi-leading-and-negotiating.md) |
| What a speaker said in an ivi session on behavioural pricing, adoption, regulation, Bitcoin and blockchain | [ivi, markets and the economy](references/ivi-markets-and-the-economy.md) |
| What a speaker said in an ivi session on AI tools and automation, product management, verification | [ivi, technology and data](references/ivi-technology-and-data.md) |
| What a speaker said in an ivi session on how a named founder built a company, in their own telling | [ivi, founder journeys](references/ivi-founder-journeys.md) |
| Two files give different numbers, steps or definitions; a file contradicts itself; a worked example does not close | [disagreements](references/disagreements.md) |
| A topic that is in no file; ISB itself; professors, courses, students | [silent](references/silent.md) |
| Every piece, its URL, its commit, whose words the notes are, what was not used, how to refresh | [sources](references/sources.md) |
| The last pass, every gate line, the symptom table, the `ANSWER.md` template | [verify](references/verify.md) |
| The brief for a fresh-eye reviewer | [review](references/review.md) |
| Which teaching pair matches a fault | [teaching](references/teaching.md) |

Script: `scripts/brain-check.mjs` checks a saved reply against the sources table (`--help` lists its lines). Its `--self-test` also checks every citation in the theme files and the count of pieces stated here.

## Never ship

| Never | Instead |
|---|---|
| "ISB teaches that", "the ISB view" | "The notes state", then `(Title)`, then its `Source:` line |
| "The notes say", with no file | The claim, then `(Title)`, then its `Source:` line |
| "A healthy LTV to CAC is 3:1" | "One file gives 3:1 or higher as sustainable", its `(Title)`, the other file's threshold, and "no source" on the last line |
| The five forces explained from memory, with a file's title attached | Only the forces, examples and limits the cited file lists |
| An 11.5% WACC quoted as typical | "The file's example, a company it calls ABC, comes to 11.5%" |
| One threshold where two files set two | Two `Disagrees:` lines, each with its file |
| "Porter says", when the file does not name Porter | The claim with no author, or "the file's title credits Porter" where it does |
| "A professor would say" | What the file states, in the present tense |
| "The notes have no view on NPV" filled with a DCF lecture | "The notes do not cover capital budgeting", and a `Nearest:` line that stops at the file |
| "You should raise now" | The lines that bear on the question, then a stop. The decision is the user's |
| A reply that ends on a link | `Not in the notes:` and what the question asked that no file answers |
| The model or the deck built after a pressure-test | The findings, and a stop |
| "ivi teaches", "ISB says", for a line from a session | The speaker's name as the note gives it, or "the instructor", then `(Title)` and its `Source:` line |
| A session figure given as a fact | "His figure" or "her example", and on the last line that it was heard through a transcript and has no source |
| Two speakers merged into one view | One sentence per speaker, each with its own note |
| A classmate, a classmate's startup, or anything a speaker asked to keep in the room | Nothing. It is in no note, and it goes in no reply |
| This skill described as ISB's, or as course material | Harshit Khemani's reading of a public repository of notes |

## Output

Plain lines, in this order. The gate reads the labels.

1. The answer: two or three sentences. Every sentence that speaks for the notes ends with `(Title)`, or `(Title; Title)` for two pieces.
2. Labelled lines, only the ones the job needs, each ending with its `(Title)`:
   - `Breaks:` and `Holds:` for a pressure-test, largest fault first. What the plan does, then what the file says.
   - `Disagrees:` when [disagreements](references/disagreements.md) has a row. One line per file.
   - `Nearest:` for a silent topic. What the nearest file does say, and no further.
3. `Yours:` one line, only when [pov](references/pov.md) has an entry on the topic. It carries no citation and is never the notes'.
4. `Source: <Title>, <URL>` one line per piece cited, copied from the theme line.
5. `Not in the notes:` the last line. What the question asked that no file answers, that the notes give no source for any figure used, and what was not read.

For "who said that": the first sentence names the file, or says the line is in none of the pieces read. It names a person only if the file does. A session note does name its speaker, in its `speaker` line, and that is the only name a reply gives.

## Tone

Plain and exact. Report, with the file. Never speak as ISB, never praise the notes, never guess, never advise.

## Yours to edit

Read both before answering. They outrank the defaults in this skill and never change what the corpus says.

- [gotchas](references/gotchas.md): answers that got the notes wrong, one line each. Append one when it happens.
- [pov](references/pov.md): where you part ways with the notes, and what to press on first.

## Pairs with

- The nine skills in `HKTITAN/isb-skills` (the repository this skill reads): they load the rule files so an agent can apply a framework to a problem. This skill tells you what a file says and where; those do the work. Install them with `npx skills add HKTITAN/isb-skills`.
- `khe-brain-emil` and `khe-brain-benji`: the same job for two designers' public writing. Use them when the question is about an interface, not a business.
- `khe-auto`: picks the skill when the request names none, and runs this skill's loop when it routes here.

Harshit Khemani. MIT. The notes: `https://github.com/HKTITAN/isb-skills`.
