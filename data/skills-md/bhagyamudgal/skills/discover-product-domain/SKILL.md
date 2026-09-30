---
name: discover-product-domain
description: Generate, remix, and rank product or app names, then verify their exact standard-price .com domains. Use when naming an app or product, remixing name fragments or an existing name, or checking a name shortlist.
---

# Discover product domains

Turn a product idea into memorable names whose exact `.com` domains are confirmed at a registrar. I treat human combinations such as `Vids` + `Jar` as a core discovery mechanism, not an afterthought.

## Mode

Start in guided mode. Extract known facts first, then ask one unresolved high-impact question at a time with 2-4 options and the recommended choice first. Use rapid mode only when the user explicitly asks for a quick, autonomous, or single-pass result. In rapid mode apply the defaults below and skip the human remix turn.

Registrar and account interactions stay read-only. Search and verify domains, but stop before sign-in, cart, offer, purchase, registration, handle creation, or any other external mutation. Write a local markdown report only when the user requests one.

## Entry route

Choose the shortest route that preserves work the user already supplied. This table owns which steps a route runs. No later step re-decides it.

| Route | Steps | What the route starts from |
|---|---|---|
| **Greenfield** | 1-8 | an idea; run the full funnel |
| **Verification or ranking only** | 1, 4, 6-8 | a shortlist to score, screen, confirm, and rank. Never generates, remixes, or expands |
| **Shortlist plus alternatives** | 1, 2, 4-8 | a shortlist that is itself the human reaction; the step 2 atom bank comes from it and the brief |
| **Remix or refinement** | 1, 2, 5-8 | names, fragments, or one name as the human reaction, satisfying the guided-mode remix requirement; the atom bank comes from them and the brief |

Do not replace, silently expand, or ignore a supplied candidate set. Generate beyond it only when the request asks for alternatives or the user approves loosening an insufficient shortlist.

## Funnel

### 1. Lock the naming brief

Capture these fields from the conversation before asking anything:

- what is being named and its one-sentence job;
- primary audience and market language;
- core promise and desired emotional signal;
- three-year expansion boundary;
- desired and forbidden tones, words, sounds, and associations;
- whether the name should describe the product or work as an abstract mark;
- other languages the audience reads, the field whose jargon it speaks, and any existing brand this name must not collide with.

Default unresolved preferences to warm, clear, credible, globally pronounceable, 5-10 characters, 2 syllables where natural, and no hyphens or digits. Default the describe-or-abstract field to no requirement to describe, and read `${CLAUDE_SKILL_DIR}/references/naming-lenses.md`, section "Description is optional", before generating. When the audience's other languages, jargon field, or brand-collision targets go unstated, default to the market language plus English, the audience's own field as the jargon source, and every brand the user has named in this conversation. Record those defaults, because the "Wart check" in `${CLAUDE_SKILL_DIR}/references/naming-lenses.md` runs on them. In guided mode, ask only when a different answer would materially change the candidate set.

The step is complete when every field is answered or carries an explicit default.

### 2. Build the atom bank

Read the "Atom bank" section of `${CLAUDE_SKILL_DIR}/references/naming-lenses.md`, then extract at least 12 distinct atoms across at least four of its semantic buckets. Mark each atom's source and type so later remixes preserve their provenance.

The step is complete when the atom bank holds enough direct, suggestive, metaphorical, emotional, and phonetic material for all three naming lenses.

### 3. Generate independently

Dispatch three naming agents in parallel when subagents are available. Read the complete lens contracts in `${CLAUDE_SKILL_DIR}/references/naming-lenses.md`. Send one lens to each agent:

1. Compounder
2. Positioner
3. Phonetic inventor

Give each agent the same brief and atom bank, but none of the other agents' candidates. Embed that agent's complete lens rules and the required output shape from `${CLAUDE_SKILL_DIR}/references/naming-lenses.md` in its task. Do not assume a subagent can resolve this skill's relative paths. Each agent returns its allocated share of a 36-name pool. Section "Description is optional" in `${CLAUDE_SKILL_DIR}/references/naming-lenses.md` owns the split and when it shifts. When subagents are unavailable, run the three lenses sequentially and keep their pools separate until synthesis.

The step is complete when 36 raw names exist, split across the three independent lenses by the brief's allocation.

### 4. Synthesize or assess

Read `${CLAUDE_SKILL_DIR}/references/domain-verification.md` before any lookup. It owns the two-rung evidence ladder. First screen with a registry lookup, then confirm at a registrar. It also owns the status vocabulary both rungs record.

Score every candidate with the "Brand score" table in `${CLAUDE_SKILL_DIR}/references/naming-lenses.md`. Domain availability is the domain gate. It means the exact standard-price `.com`, confirmed at a registrar, and it sits outside that score.

For a greenfield route, deduplicate the pool, apply the remix operators from `${CLAUDE_SKILL_DIR}/references/naming-lenses.md`, and select 12 names spanning all three lenses. For a supplied shortlist, preserve and score every supplied candidate without demanding 12 names or artificial lens coverage. Preserve strong atoms from rejected names. A taken compound can still contain half of the winner.

Screen the current candidate set's canonical `.com` domains and account for every lookup with the status vocabulary.

In guided greenfield mode, present the first pass and collect the one structured reaction defined in `${CLAUDE_SKILL_DIR}/references/naming-lenses.md`. In rapid mode, create an autonomous reaction. Retain the four strongest atoms or patterns, reject weaknesses shared by the bottom candidates, and record that you intentionally skipped the human remix turn and inferred no user preference.

The step is complete when a greenfield user supplied a remix reaction, rapid mode recorded its autonomous reaction, a shortlist-with-alternatives preserved the supplied set as its reaction, or a verification-only shortlist holds a screened status for every supplied name.

### 5. Produce eight remixes

A remix or refinement route reaches its first score and lookup here. Read both step 4 references before you score or look up anything.

Treat every user-created combination as a first-class seed. Apply the "Remix operators" in `${CLAUDE_SKILL_DIR}/references/naming-lenses.md`. Send the reaction to the original lens owners as follow-up tasks when possible, embedding the relevant remix operators and output contract in each task. Otherwise apply the operators locally. Produce eight new names that cross favored atoms while avoiding rejected patterns. Score the original supplied seeds and the eight remixes together, then screen every canonical `.com` not already checked.

The step is complete when eight non-cosmetic remixes have a recorded screened status.

### 6. Control expansion

A provisional name holds `candidate_available_rdap`. That means screened, not confirmed. That status permits registrar confirmation but does not prove anyone can buy the domain.

Use these transitions. Do not wait in step 6 for evidence that only step 7 can produce:

- **Invalid supplied spelling.** Request the exact `.com` spelling and stop with "Input blocked" until the user resolves it. Record and exclude invalid generated candidates without treating them as evidence failures.
- **Unknown evidence.** Retry once using the backoff in `${CLAUDE_SKILL_DIR}/references/domain-verification.md`. Keep a nonessential generated unknown recorded and exclude it when enough other candidates can still meet the domain gate. When an unknown belongs to a supplied shortlist or prevents the domain gate, stop with "Evidence blocked", naming the affected domains and the evidence boundary that failed. Do not spend naming rounds during an evidence outage.
- **Unconfirmed provisional names exist.** Proceed to step 7.
- **Short of three finalists with no provisional left to confirm.** A route that does not generate returns its survivors to step 8. Otherwise, when fewer than two expansion rounds have run, dispatch the three lenses with failed roots, registrar rejection reasons, favored atoms, and length constraints. Embed each lens's complete rules and output contract as in step 3. Deduplicate and score the new pool, select its strongest new names, screen them, then apply these transitions again.
- **Two expansion rounds exhausted.** Ask which naming constraint to loosen: atom vocabulary, tone, maximum length, or compound complexity. Do not weaken the domain gate. An answer resets the expansion counter once. A declined or fruitless loosening stops with "Generation shortfall".

Keep each lens independent during generation.

### 7. Confirm at the registrar

Follow the confirm stage in `${CLAUDE_SKILL_DIR}/references/domain-verification.md` and record the evidence fields it requires. On a generating route, confirm provisional names until three clear the domain gate. On a verification-only shortlist, confirm every provisional supplied name.

Exclude premium, aftermarket, reserved, taken, and unknown domains from the final three. Recheck a chosen name immediately before the user acts because no search reserves availability.

When fewer than three finalists survive and the active route generates, return to step 6. For a verification-only supplied shortlist, report the shortfall without inventing replacements.

The step is complete when a generation route holds three registrar-confirmed finalists or a step 6 "Generation shortfall", or every supplied domain in a verification-only shortlist holds a terminal status: `registered`, `registrar_confirmed_available`, or `premium_or_reserved`. A provisional name is never terminal. Identify the strongest survivor when one exists. Otherwise follow the step 6 transition that matches the current state.

### 8. Recommend

For a generation route, return exactly three finalists unless the user asks for more. When a "Generation shortfall" ended the funnel, return every survivor and report the shortfall instead of inventing replacements. For a verification-only shortlist, rank the registrar-confirmed survivors without inventing names to fill a quota. For each returned name, include:

- spelling and pronunciation;
- why it fits and its strongest downside;
- brand score out of 70;
- registrar-confirmed domain evidence and prices.

For generation, alternatives, remix, and refinement routes, also include the atom recipe, lens or user provenance, and two nearby remix directions. Verification-only results omit those generation artifacts.

Name a winner when at least one name survives. When at least two survive, also name a runner-up and state the deciding trade-off in one sentence. When none survive, report the shortfall without recommending a name. Keep user preference separate from the numeric brand score. Warn that the workflow performed no trademark clearance, social-handle verification, or legal review.

Save a durable report only when the user asks for one, and follow `${CLAUDE_SKILL_DIR}/references/durable-report.md` when you do.

## Completion gate

Stop only at a terminal state: step 7's completion condition, or a step 6 "Generation shortfall", "Evidence blocked", or "Input blocked". Account for every domain you actually queried by status.

A generated `unknown` or `invalid_candidate` that you recorded and excluded does not block completion. An `unknown` returns "Evidence blocked" only when it belongs to a supplied shortlist or prevents the domain gate, and an `invalid_candidate` returns "Input blocked" only for a supplied name.

The user's choice and step 7's pre-action recheck close the run. Only a separately authorized, successful registration could establish acquisition, and this skill never claims it.
