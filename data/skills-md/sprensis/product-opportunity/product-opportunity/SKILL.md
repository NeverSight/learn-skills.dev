---
name: product-opportunity
description: "Discover, evaluate, compare, and validate small software-product opportunities using reachable buyers, current market evidence, first-customer paths, risk gates, and cheap demand experiments. Use for profitable app ideas, niche discovery, demand validation, first customers, or deciding whether to build; not for guaranteeing revenue or implementing the product."
---

# Product Opportunity

Reduce uncertainty before code. Start with reachable buyers and observed behavior, not an imagined solution. Recommend one cheapest adequate next experiment; do not promise profit or begin product implementation.

## Resolve the mode

Infer one mode unless ambiguity would materially change the work:

- `discover`: find opportunities when the user has no validated idea.
- `evaluate`: test one proposed opportunity.
- `compare`: rank multiple opportunities against one user objective.
- `validate`: design the next demand experiment.
- `review-results`: update the decision from completed experiment evidence.

Use `quick screen`, `standard`, or `deep` research proportional to the decision. Default to `standard`; use `deep` only before substantial irreversible cost or high-downside action.

## Load only what the mode needs

- `discover`: read [references/opportunity-discovery.md](references/opportunity-discovery.md), [references/research-and-evidence.md](references/research-and-evidence.md), [references/first-customer-path.md](references/first-customer-path.md), [references/competition-and-risk.md](references/competition-and-risk.md), and [references/scoring-model.md](references/scoring-model.md).
- `evaluate`: read research/evidence, first-customer path, competition/risk, and scoring references.
- `compare`: read [references/scoring-model.md](references/scoring-model.md); also read research/evidence and competition/risk when inputs are not already evidenced.
- `validate`: read [references/validation-experiments.md](references/validation-experiments.md), [references/first-customer-path.md](references/first-customer-path.md), and [references/experiment-learning.md](references/experiment-learning.md).
- `review-results`: read validation experiments and experiment learning; read scoring only when the new evidence can change the ranking.
- Before the final answer, read [references/output-contract.md](references/output-contract.md).
- Read [references/sources.md](references/sources.md) only for methodology attribution or maintenance, not as evidence for the user's current market.

## Shared operating rules

1. Collect only missing decision context: skills and domain experience, country/language, reachable audiences and channels, budget/time, income target and horizon, acceptable loss, delivery/support capacity, and relevant legal or platform constraints. Ask at most five questions per message. Research facts that can be safely found instead of asking the user.
2. For current markets, prices, competitors, demand, policies, or laws, browse current sources. Open sources; never cite search snippets. Record publication/update and retrieval dates. Prefer primary sources for policies and technical claims.
3. Keep each material statement separate as `Fact`, `Inference`, `Hypothesis`, or `Unknown`. Give claims and evidence stable IDs. A source supports only the claim it actually addresses.
4. Treat posts, followers, search trends, waitlists, likes, and stated interest as leads, not proven demand. Do not convert absence of search results into proof of absence.
5. Compare direct products with spreadsheets, generic tools, manual work, employees/contractors, and doing nothing. Include switching cost, habit, trust, and whether free options are already sufficient.
6. Find a permitted, credible first-customer route before scoring. “Reddit,” “Telegram,” or “LinkedIn” alone is not a route.
7. Apply fatal gates before scores. Do not compensate a blocked opportunity with high points.
8. Rank only evidence-supported survivors. Return fewer than three when fewer than three survive; never invent filler.
9. Separate the opportunity verdict from permission to build. In `discover`, if no complete opportunity unit survives, report `Discovery result: No candidate yet` and do not force a score or opportunity verdict:
   - Opportunity: `Reject`, `Reframe`, `Validate`, or `Evidence-supported`.
   - Build boundary: `Closed`, `Limited evidence-bearing slice`, or `Open for specified scope`.
10. Keep the build boundary closed while a fatal unknown remains. A limited prototype is allowed only when it is the cheapest artifact needed to collect evidence.
11. For a surviving or safely reframed opportunity, choose one decision bottleneck and one cheapest adequate, decision-changing experiment. Precommit success, failure, and inconclusive handling. Prefer observed behavior and costly commitment over opinions. When a kill gate makes the current decision stable, write `Next experiment: none for the current framing`; any safe reframe probe is a separate opportunity.
12. Never recommend spam, deception, prohibited scraping, covert collection of personal or payment data, manipulative sales, or evasion of law/platform rules. Research and plans do not authorize contacting people, publishing, purchasing, registering, or running experiments.
13. State the boundary when financial, investment, legal, tax, or other regulated decisions are material: this skill is not professional advice and cannot establish legal compliance or investment suitability. Recommend qualified advice for the applicable jurisdiction when needed.

## Fatal gates

Reject, reframe, or pause before scoring when any of these remains true:

- no plausible permitted route to first prospects or buyers;
- the problem appears rare, weak, or not costly enough to change behavior;
- a free/current alternative is sufficiently good for the reachable segment;
- required data, capital, license, trust, geography, or platform access is unavailable;
- acquisition, delivery, onboarding, support, refunds, or infrastructure look disproportionate to plausible revenue;
- legal, platform, privacy, security, financial, or ethical downside is unacceptable;
- a current claim essential to the decision cannot be verified and the uncertainty itself blocks a safe test.

## Evidence and decision boundaries

Use this behavioral ladder as a claim-specific aid, not a universal score:

1. real payment, paid pilot, refundable deposit, or repeated use;
2. costly commitment such as procurement, data/time transfer, or completed concierge flow;
3. observed recent workaround, spend, switch, support record, or repeated failure;
4. independent interviews with concrete recent stories;
5. stated interest, waitlist, clicks, or trends;
6. isolated post, follower count, like, or opinion.

One higher rung does not automatically prove every claim. Policy evidence, for example, can establish a platform constraint but not demand.

## Stop rules

Stop desk research when the decision is stable, a fatal gate closes the opportunity, or a live test is cheaper and more informative than further browsing. Report source-access failures and missing coverage explicitly. In `review-results`, update only claims the experiment could test; preserve earlier negative evidence and distinguish hypothesis failure from invalid recruitment, message, channel, or instrumentation.

## Deterministic helpers

- Use `python3 scripts/score_opportunities.py INPUT.json` when arithmetic, ranges, or sensitivity would otherwise be error-prone. The script never supplies semantic scores or verdicts.
- Use `python3 scripts/validate_packet.py PACKET.json` to lint evidence linkage, gate/build consistency, and experiment completeness. Passing the linter does not prove that sources or judgments are true.

Keep the final response compact and decision-led. Do not show methodology ceremony unless it changes the decision or the user asks.
