---
name: gap-finder
description: Finds viable product, business, or project ideas in any domain by generating candidates in batches, rigorously validating each against real competitors and market data, and killing weak ideas with documented reasons. Use when the user asks to brainstorm ideas, find market gaps, identify business opportunities, figure out what to build, come up with side project ideas, or find underserved niches. Works for SaaS, open source, MCP servers, apps, tools, APIs, or any product category.
---

# Gap Finder

Finds viable ideas through adversarial generation-and-kill cycles. Generates batches of 5, validates every idea against real market data, kills failures with documented reasons, and loops until survivors emerge.

## Workflow

1. **Establish the domain** — identify the space the user wants ideas in (e.g., "MCP servers", "developer tools", "mobile apps for nurses"). Extract any constraints (tech stack, budget, solo founder, etc.) and previously killed ideas. Write these to a scratchpad file in the current working directory (`gap-finder-state.md`).
2. **Generate a batch of 5 ideas** — each must be concrete and specific to the domain. Follow the idea template in [GENERATION.md](GENERATION.md). Draw from at least 3 different angles per batch.
3. **Run the kill chain on every idea** — execute all 6 validation checks from [VALIDATION.md](VALIDATION.md). Search the web for each check. Kill on first fatal failure.
4. **Record killed ideas** — append every killed idea + specific kill reason to `gap-finder-state.md`. This prevents re-proposing.
5. **Present survivors** — if any ideas survive all 6 checks, present them with full evidence. See [SURVIVOR-FORMAT.md](SURVIVOR-FORMAT.md).
6. **Widen on saturation** — if 2 consecutive batches have 0 survivors AND >80% died at Check 1 (competitors), the current sub-space is saturated. Do NOT stop. Instead: (a) note the saturated sub-space in state file, (b) expand the domain — go more niche, go adjacent, change the target user, change the business model, or combine two domains. Keep generating. The goal is survivors, not a saturation report.
7. **Loop until 3 survivors** — go to step 2. There is no batch limit. Keep generating until 3 survivors are found. After every 5 dead batches, radically pivot: change the domain, the target user, the business model, or the geography. The answer exists — you haven't looked hard enough yet.
8. **Report survivors as they emerge** — present each survivor immediately when it passes all 6 checks (don't wait for 3). After 3 survivors, write the final ranked summary.

## Self-review checklist

Before delivering results, verify ALL:

- [ ] Every proposed idea was searched on at least 3 relevant sources (varies by domain — e.g., npm+Smithery+GitHub for dev tools, App Store+ProductHunt+Google for apps)
- [ ] Every killed idea has a specific, one-sentence kill reason (not "didn't seem viable")
- [ ] Every survivor has competitor search evidence showing < 2 direct competitors, or a clear differentiation from existing ones
- [ ] Every survivor answers "what recurring pain point does this solve?" with a concrete user scenario
- [ ] Every survivor has a realistic monetization or growth path described in one sentence
- [ ] No survivor is something trivially solved by existing free tools or LLMs without external data
- [ ] At least 3 batches were generated (15+ ideas evaluated)
- [ ] Each idea is specific (names concrete features/tools, not just a category)
- [ ] Killed ideas are tracked in gap-finder-state.md to prevent re-proposing

## Golden rules

Hard rules. Never violate these.

1. **Search before you pitch.** Never present an idea without first searching for existing implementations. Every idea gets 3+ web searches across relevant platforms. No exceptions. No "I believe there aren't competitors" — show the search results.
2. **Kill fast, document why.** The moment an idea fails any validation check, kill it. Record the specific kill reason. Do not soften failures into "could work with modifications."
3. **Recurring pain or death.** If the pain point occurs less than weekly for the target user, the idea is dead. Quarterly pain is not a business. Daily frustration is.
4. **Existing-solution-already-works is fatal.** If a free, widely-adopted tool already solves this well enough, the idea is dead. "But ours would be slightly better" is not a gap — it's a feature request on the existing tool.
5. **Never stop until survivors are found.** There is no batch limit. Keep generating and validating until 3 survivors emerge. No early exits. No "the market is saturated" conclusions. When obvious ideas die, get weirder. When a sub-space is crowded, move to an adjacent one. Parallelize validation across multiple agents when possible — each idea's kill chain is independent and can run concurrently.
6. **Concrete features, not categories.** "A developer tool" is not an idea. "A CLI that takes a package.json and returns a dependency upgrade plan with breaking change warnings by cross-referencing changelogs" is an idea.
7. **No resurrections.** Once an idea is killed, it stays dead. Do not re-propose killed ideas with minor variations. If "Postgres optimizer" is dead, "MySQL optimizer" dies for the same structural reason.
8. **Evidence over intuition.** Every claim about market size, competitor count, or user demand must be backed by a search result or concrete data point. "I think developers would want this" is not evidence.

## Reference files

| File | Contents |
|------|----------|
| [GENERATION.md](GENERATION.md) | How to generate idea batches, the idea template, angle diversity requirements |
| [VALIDATION.md](VALIDATION.md) | The 6-check kill chain with search strategies and pass/fail criteria |
| [SURVIVOR-FORMAT.md](SURVIVOR-FORMAT.md) | Output format for surviving ideas with required evidence sections |
