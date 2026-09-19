---
name: stelow-product-marketplace-playbook
description: Strategies and tactics for stimulating marketplaces by balancing supply and demand. Covers 19 proven tactics from getting the harder side first to creating urgency through constraints.
metadata:
  frequency: rare
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# Stimulating Marketplace: Supply and Demand

## 19 Tactics to Stimulate Marketplaces

### Getting the Core Dynamics Right

1. **Get the harder side first.** When the harder side (supply or demand) reaches its critical activity point, network effects kick in and value is created organically for the easier side. Discovering this through the sales and onboarding process, typically the harder side is the most valuable — once you have enough of them, the other side is 2-3 times easier to bring aboard.

2. **Strongly attract to a niche and repeat.** Find the small groups in your community that care most about your market ("white-hot center") and go after them. Usually, this is discovered by going broad enough to collect data that shows the most activity.

3. **Subsidize the most valuable side of the market.** Pay in cash to the most valuable side of the market — or to the most valuable niche within the most valuable side — to join the marketplace.

### Building Initial Supply

4. **Make supply look bigger with automation.** Start the supply side by aggregating as much web data as possible to create a "perceived aura of activity".

5. **Build one side as an email list.** An easy and cheap way to start a market, especially if many buyers are also sellers and vice versa.

6. **Hold meetups and gatherings.** In the beginning, they can be effective for generating community, demonstrating activity, and getting direct customer feedback.

7. **Create a SaaS tool for one side of the market.** When you give or sell a SaaS tool to one side of the market, it helps keep them in the market, giving time to attract the other side.

8. **Provide software to third parties who can bring one side of the market.**

9. **Find a giant user for initial supply or demand.**

10. **Make only one side change their behavior.**

### Creating Momentum

11. **Make something free suddenly.** Transforming something that used to cost money into something free will attract users.

12. **Create a product first and then open a market.**

13. **Connect the two sides manually.**

14. **Prefer markets where buyers are also sellers.** Avoid building a single-sided market altogether.

### Leveraging Constraints

15. **Create exclusive access.** Restrict access and create fear of missing supply or demand can generate strong word of mouth and rush of participation when the idea goes viral. However, this almost never works.

16. **Define a geographic constraint.** It's easier to generate a lot of activity when limiting the operating area at launch.

17. **Define a time constraint.** One can program enthusiasm into the market with time constraints.

18. **Define a demand constraint.**

19. **Pay users with tokens.** If you create a token for the market, you can pay people to join, even when there's no activity.

## Research First (market context)

Tactics fail most often from wrong context, not wrong execution. Before picking tactics, establish market type, sides, and comparables via the shared web-research contract (`../stelow-workflow-orchestrator/references/cli-tools/web-research.md`): host search for market facts and comparable marketplaces first, `last30days` as a recency check on the shortlisted tactics ("has anyone tried tactic N in this niche recently, and what happened?"). Skip when the user already supplied context.

## Completeness contract

The host validates these minima — never submit fewer:

- 2–3 tactics ordered by effort, each with the side-constraint it removes, grounded in the market context.
- At least 600 words and 3 headings.

## Examples

### Example: tutors won't join the tutoring marketplace

**Input:** "We have students waiting, no tutors. What now?"

**Steps:**
0. Establish context via Research First (tutoring vertical, supply-constrained, comparables) — skip if already known.
1. Name the harder side (supply: tutors).
2. Pull supply-side tactics (guaranteed first earnings, concierge onboarding, single-player value).
3. Sequence: unblock supply before stimulating more demand.

**Output:** 2-3 tactics ordered by effort, with the side-constraint each removes.

## Edge Cases

### Both sides are thin
- Constrain geography or niche first; a thin everywhere marketplace dies.
### Supply joins but doesn't transact
- The problem is trust/matching, not acquisition — switch tactic families.
### One side subsidizes forever
- Name the path to take-rate; permanent subsidy is a bug, not a model.
### Picked tactics without market context
- Go back to Research First; a thin-everywhere diagnosis without comparables is a guess.

## Entry (mode detection)

When this skill loads, check for the stelow workflow marker:

```bash
if [ -n "$STELOW_WORKFLOW" ] && [ -n "$STELOW_STATE" ]; then
  echo "stelow: workflow mode (state=$STELOW_STATE)"
else
  echo "stelow: standalone mode (no STELOW_WORKFLOW marker)"
fi
```

In **standalone mode** (no marker), run the existing skill body unchanged.
In **workflow mode**, skip to `### Workflow slice` and emit a complete
`## Hand-off (workflow mode)` block at the end. See
`../stelow-workflow-entry/SKILL.md` for the full marker protocol.

## Hand-off (workflow mode)

```
stage          : shape
description    : Shape stage. Define appetite, hill chart, rabbit holes.
status         : <done|partial|blocked>
artifacts      : <paths created or modified>
next-candidate : critique
gate           : none
rework-on      : shape
```

Workflow mode: emit the above Hand-off block verbatim, then stop. The
router skill consumes the next-candidate field and calls
`scripts/stelow advance <next-candidate>` to move state forward.

### Workflow slice

Workflow mode for the **shape** stage. Standalone behavior lives in
the rest of this file (unchanged). Summary:

> Shape stage. Define appetite, hill chart, rabbit holes.

Primary actions (per stages.yaml): `read, write`. Run only the actions that
produce the artifacts promised in `## Hand-off`; skip anything that does
not advance the workflow.

