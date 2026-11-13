---
name: ux-activity-feed
description: Design or critique an activity feed / stream — a scannable list of updates where what matters stands out and noise fades. Gates the feed-type choice (chronological vs. algorithmic/ranked) and levers like notification aggregation, follow recommendations, and per-entry controls, while applying the always-true core (curated entries, legible text, relative timestamps, no empty feed, visible refresh status). Trigger when the user asks to design or review an activity feed, news/social feed, activity stream, notifications feed, or timeline.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Activity Feed Skill

## How this skill behaves (read first)

This is a **generative** skill. A feed's job is to surface what matters and let the noise fade — and the defaults work against that: each entry crammed with every available field, loud exact timestamps, every social control on every row, ungrouped notifications buzzing one-by-one, and a blank feed greeting brand-new users in the exact window where they decide whether to stay. There's also a consequential upfront choice — **chronological vs. algorithmic/ranked** — that teams often make by accident. So this skill gates:

1. **Establish the feed type and what the feed is for** — chronological vs. ranked is hard to change later and reshapes everything downstream.
2. **Apply the always-true core** — curate each entry, keep text legible, downplay timestamps, never show an empty feed, show refresh status.
3. **Surface the context-dependent decisions** (notification aggregation, follow recommendations, per-entry controls) with trade-offs.

Then it **hands off to `ux-aesthetics-audit`, `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-microcopy-audit`, `ux-dark-patterns-audit`, and `ux-mobile-responsiveness-audit`** for validation.

Scope & composition (per `docs/orchestration-policy.md` §9): this skill covers the **feed screen and its entries** and composes lower-scope skills rather than re-deriving them. **Core children (built as part of the feed):** per-entry **card anatomy** via `ux-cards`. **Peers that own a sub-part (defer):** **notification component** behavior to `ux-notifications-and-toasts` and **loaders/skeletons** to `ux-loaders-and-progress` (they own those sub-parts if reached). **Downstream (offer, don't auto-build):** the **empty-feed screen** craft via `ux-empty-states`. **Inherit, don't regenerate:** under an existing design system, take color/type/spacing from its tokens — only set those when designing from scratch.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **Chronological or ranked?** **Chronological** (newest→oldest) presents a true timeline — right when *when it happened* is the point (a transaction log, a team activity history). **Ranked/algorithmic** curates by relevance, trending, sponsored, or editorial picks — right when *what's worth seeing* matters more than recency. Key warning: **don't ship a chronological feed you intend to replace with an algorithm later** — that switch upsets users badly. Choose deliberately now.
- **What's the feed for?** Social engagement, transactional/account updates, or a notifications digest — this sets which controls and content each entry needs.
- **What will a new or quiet account see?** New users with no connections, or a lull in activity, will hit an empty feed — plan for it from the start (the post-install window to hook users is ~3–7 days).

---

## The always-apply core (correct for almost every feed)

- **Curate each entry — minimalism over completeness.** A feed item may have lots of data behind it; show only what a user needs to decide and move on. Overcrowded rows, mismatched fonts, and verbose labels pull attention off the task. Clarity lets users scan fast.
- **Keep text legible.** Feeds exist to be consumed quickly — large, clear fonts and strong background contrast, tested with accessibility tools. This matters most for users with visual impairments.
- **Downplay timestamps.** They're a *tertiary* signal — a rough "how long ago," not an exact clock. Abbreviate ("3h," "2d") and don't let them compete with the content.
- **Never show an empty feed.** A blank feed at first run or during a lull kills engagement. Seed it: "suggested people to follow" during onboarding, popular/trending content, an invite-friends prompt, or a nudge to complete the profile — anything that produces immediate activity.
- **Only the essential controls per entry.** Include the interactions that matter (e.g. like/comment/share for social; maybe none for a read-only updates feed) and trim the rest — every extra control is overhead that clutters the row.
- **Show feed status on refresh.** When users pull-to-refresh or load more, a clear loading indicator (spinner/skeleton) keeps them informed of system status rather than staring at a frozen screen.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Feed type: chronological vs. ranked** | Chronological when recency *is* the value (logs, histories, real-time team activity); ranked when relevance/volume makes pure recency noisy | Pure chronological if you'll later switch to an algorithm (the change upsets users); ranked where users expect a literal timeline | Pick by whether *when* or *what* matters most — and commit, don't retrofit |
| **Aggregate / group notifications** | High-volume or power users — combine similar alerts ("256 people followed you today") by time, type, or interaction | Low-volume feeds where each event is individually meaningful | Group similar updates once volume would otherwise bombard |
| **Personalized follow recommendations** | Social/discovery products — suggest profiles from connections, shared interests, or influential accounts to spark exploration | Letting recommendations narrow into a filter bubble | Offer suggestions, but deliberately mix in diverse/cross-interest content |
| **Per-entry control set** | Social feeds: like/comment/share; transactional feeds: maybe a single "view" or none | Copying social controls onto a feed that doesn't need them | Match controls to the feed's purpose; fewer is usually better |
| **Sponsored / editorial injection** (ranked only) | When the business model requires promoted items | Disguising ads as organic activity | Clearly label sponsored/promoted entries (→ dark-patterns) |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `microcopy`, and `dark-patterns` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — entry density and scannability, one consistent treatment across rows, timestamps subordinate, clutter-free composition.
- **`ux-heuristics-audit`** *(Tier A)* — visibility of system status (refresh/loading), recognition over recall, match between feed order and user expectation (especially for ranked feeds).
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — text size and contrast for fast reading, control labels and targets, screen-reader order of feed items.
- **`ux-microcopy-audit`** *(Tier A)* — abbreviated timestamps, aggregated-notification phrasing ("256 people followed you today"), entry labels, empty-feed prompts.
- **`ux-dark-patterns-audit`** *(Tier A)* — the feed-specific traps: undisclosed sponsored content dressed as organic, engagement-maximizing manipulation, and filter-bubble narrowing. Ranking should serve the user, not just time-on-app.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer)* — pull-to-refresh and infinite-scroll behavior, tap targets on per-entry controls, legibility and one-handed reach on small screens.

If the audits surface a conflict (e.g., business wants more promoted entries vs. a trustworthy stream), resolve back toward the primary task: **the user opened the feed to catch up on what matters — protect signal over noise.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Pick chronological vs. ranked by default | Choose deliberately by whether *when* or *what* matters — and commit |
| Start chronological, then swap in an algorithm | Decide upfront; the surprise switch upsets users |
| Cram every available field into each entry | Curate to what's needed to decide and move on |
| Loud, exact timestamps | Abbreviated, relative, visually subordinate |
| One buzz per follower/like | Aggregate similar notifications ("256 people followed you today") |
| Greet new users with a blank feed | Seed it: follow suggestions, popular content, invite/profile prompts |
| Every social control on every row | Only the controls the feed's purpose needs |
| Promoted items disguised as organic | Clearly labeled sponsored/editorial entries (→ dark-patterns) |
| Frozen screen on refresh | Visible loading indicator / skeleton |
| Ship without checking | Hand off to aesthetics + heuristics + accessibility + microcopy + dark-patterns + mobile-responsiveness |

---

## Source lessons (Uxcel)

- [How to Design Engaging Activity Feeds](https://uxcel.com/lessons/activity-feed-best-practices-646)
