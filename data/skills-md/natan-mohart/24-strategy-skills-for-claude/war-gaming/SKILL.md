---
name: war-gaming
description: Models competitor and market response scenarios as a decision tree with real probabilities, computing expected value per strategic option through a bundled calculator that also flags when the highest-EV choice has a worst case the business might not survive. Use whenever the user wants to war-game a competitive move, needs a scenario-planning exercise, is choosing between options with genuinely uncertain competitor/market reactions, or has done "scenario planning" that was really just a written narrative with no probabilities or payoffs attached.
---

# War Gaming

## When to use
Use before a major move where competitor or market reaction is genuinely uncertain and the stakes are high enough that "we'll figure it out" isn't good enough — pricing moves, market entry, product launches into a contested category. Also use to upgrade a narrative-only scenario exercise ("here are three things that might happen") into an actual decision tool with probabilities and payoffs.

## What it does
Structures the decision as a tree: your strategic options as the first branch, each followed by chance-node scenarios (the ways the market/competitors could respond) with assigned probabilities and payoffs. The bundled calculator computes expected value per option and separately checks the maximin (best worst-case) option — because the EV-maximizing choice and the safest choice are sometimes different, and that's a risk-tolerance decision the business needs to make consciously, not one a spreadsheet should make silently.

## Method
1. **Define the strategic options** being compared (the same discipline as strategic-options — genuinely distinct paths, not variations on one theme).
2. **For each option, build a comparable set of response scenarios** — ideally drawing on competitive-intel's capability/incentive/constraint profiles so the scenarios are grounded in what a competitor would plausibly do, not a brainstormed list.
3. **Assign probabilities to each scenario within an option**, summing to 1.0. Where real data doesn't exist, use structured expert elicitation (ask multiple people independently, then reconcile) rather than one person's gut number — and label the confidence level of the probabilities explicitly.
4. **Assign a payoff to each scenario** in a consistent unit (usually $ impact over a defined time horizon) — include downside scenarios with real negative payoffs, not just "less upside," or the tree can't do its job.
5. **Run the bundled calculator** (`scripts/decision_tree_ev.py`) to compute expected value per option, plus worst-case and best-case bounds, and a maximin comparison.
6. **When EV-best and maximin-best disagree, treat that as the central finding**, not a footnote: ask explicitly whether the business could survive the EV-maximizing option's worst case. If not, expected value is the wrong decision criterion here regardless of how favorable the average looks.
7. **Stress-test the probabilities**: rerun with a plausible pessimistic shift in probabilities (more weight on the bad scenarios) to see if the ranking is robust or fragile to being wrong about the odds.
8. **Translate into a monitoring plan**: name the early signals that would indicate which scenario is actually unfolding, so the team can react in real time rather than waiting for the full outcome.

## Inputs
- Strategic options under consideration
- Plausible response scenarios per option (ideally sourced from a competitive-intel profile)
- Probability estimates per scenario (labeled with confidence level)
- Payoff estimates per scenario, including realistic downside cases
- Config saved as JSON matching the format documented at the top of `scripts/decision_tree_ev.py`

## Output format
Decision tree with options, scenarios, probabilities, and payoffs; EV, worst-case, and best-case per option; explicit flag and discussion when EV-best and maximin-best diverge; probability-stress-test result; monitoring plan tied to early signals per scenario.

## Example
An aggressive price cut shows the highest expected value (470,000) but a worst case of -200,000 if the competitor matches; holding price and adding value shows a lower EV (420,000) but a worst case of +300,000. The calculator flags the divergence explicitly. If a -200,000 outcome would breach a covenant or force a difficult follow-on fundraise, that changes the decision even though the aggressive option "wins" on paper — a conversation the raw EV number alone would never force.

## Common pitfalls
- Running scenario planning as a narrative exercise with no probabilities or payoffs, so it can't actually be compared to an alternative.
- Defaulting to the highest-EV option without checking whether the business can survive its worst case.
- Assigning probabilities without labeling their confidence, letting a guess be treated with the same weight as measured data.
