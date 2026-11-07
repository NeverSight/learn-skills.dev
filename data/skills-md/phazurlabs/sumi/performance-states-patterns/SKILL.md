---
name: performance-states-patterns
description: "Perceived performance and state design: skeleton screens, optimistic UI, progressive loading, notification architecture (toast, banner, badge, push), and empty, error, offline, and onboarding states. Use when a UI feels slow, or when specifying what a screen shows before, during, and after data arrives."
---

# Performance, States & Patterns

Every interface exists somewhere on a spectrum of states. The difference between an application that feels polished and one that feels fragile lies almost entirely in how it handles the moments *between* the ideal. Loading, emptiness, failure, first contact, disconnection — these transitional states collectively occupy more of a user's lived experience than the "happy path" designers typically obsess over. This skill addresses that full spectrum with rigor, providing concrete patterns, code, and architectural guidance for every in-between moment.

## The State Spectrum Philosophy

An interface element moves through a predictable lifecycle of states. Designing for all of them is not optional — it is the baseline for professional-grade UX.

```
EMPTY -> LOADING -> SKELETON -> PARTIAL -> COMPLETE -> ERROR -> OFFLINE
  |         |          |           |          |          |         |
  v         v          v           v          v          v         v
First-use  Spinner   Shimmer    Streaming   Ideal     Recovery  Cached
guidance   or bar    placeholders  data      render    + retry   fallback
```

**Empty** is the starting point: the user has arrived but there is no content yet. This could be a brand-new account, a search with no results, or a list that has been cleared. Empty states are opportunities to guide, teach, and motivate.

**Loading** is the state of uncertainty. The system is working, but the user cannot yet see results. The perceived duration of this state is more important than its actual duration — perceived performance is a design problem, not just an engineering one.

**Skeleton** is a specific loading sub-state where placeholder shapes mirror the eventual content layout. Skeleton screens reduce perceived wait time by giving the brain structural information to process, making the transition to real content feel faster and less jarring.

**Partial** is the state where some data has arrived but not all. Streaming server-side rendering, progressive image loading, and paginated lists all produce partial states. The key design challenge is making partial content usable without misleading users about completeness.

**Complete** is the happy path — all data loaded, all interactions available. This is the state most mockups depict, but it represents only one moment in the lifecycle.

**Error** is the state where something went wrong. Network failures, server errors, validation problems, permission issues, rate limits — each error type demands a different response. The goal is always: tell the user what happened, what it means for them, and what they can do next.

**Offline** is the state where network connectivity is lost. Modern applications must handle this gracefully, serving cached content where possible and queuing actions for later synchronization.

## Perceived Performance: The Psychological Foundation

Users do not experience milliseconds — they experience *feelings* about speed. Research consistently shows that perceived performance matters more than actual performance for user satisfaction. A 3-second load that feels fast (because of skeleton screens and progressive rendering) outperforms a 2-second load that feels slow (because of a blank screen followed by a sudden content dump).

The three pillars of perceived performance are:

1. **Immediate feedback** — acknowledge every user action within 100ms
2. **Visual continuity** — maintain spatial relationships during transitions so the brain can track what is happening
3. **Progressive disclosure of content** — show something useful as early as possible, then enhance

Skeleton screens, optimistic UI updates, pre-fetching, and progressive loading are all implementations of these principles. Detailed patterns, code examples, and implementation guidance are provided in the reference material.

See: `references/perceived-performance-patterns.md`

## Notification Architecture: Reaching Users at the Right Moment

Notifications are the interface's voice — the mechanism by which an application communicates with users across time and context. A well-designed notification system respects attention as a finite resource. A poorly designed one trains users to ignore everything, or worse, to uninstall.

The notification taxonomy spans six channels, each with different characteristics:

| Channel | Persistence | Urgency | Context |
|---|---|---|---|
| Toast | Ephemeral (3-8s) | Low to medium | In-app, immediate |
| Banner/Alert | Until dismissed | Medium to high | In-app, contextual |
| Badge | Until addressed | Low (ambient) | In-app, persistent |
| Push | Until opened | Medium to high | OS-level, external |
| Notification Center | Permanent list | Varies | In-app, on-demand |
| Email/SMS | Permanent | Varies | External, asynchronous |

The architectural challenge is building a unified system where a single event can be routed to the appropriate channel based on urgency, user preferences, and context. A new message from a colleague might appear as a toast if the app is open, a push notification if it is not, and an email if the user is offline for hours — all from a single notification event.

Urgency must be calibrated carefully. If everything is marked critical, nothing is. The "crying wolf" anti-pattern — overusing high-urgency styling — is one of the most common notification design failures.

See: `references/notification-system-design.md`

## First-Run Experience: The Onboarding Spectrum

Onboarding is not a single screen or a tooltip tour. It is a spectrum of patterns that help users move from unfamiliarity to competence. The best onboarding serves the user's goal, not the product's feature tour.

The onboarding spectrum, from least to most intrusive:

1. **Progressive disclosure** — features reveal themselves as users naturally encounter them. No explicit onboarding UI at all; the interface teaches by being well-designed.
2. **Contextual hints** — subtle, one-time tooltips that appear when a user first encounters a specific feature area.
3. **Checklist model** — a visible list of setup tasks (often with endowed progress — starting at "1 of 5 complete" rather than "0 of 5") that guides users through initial configuration.
4. **Interactive sandbox** — a safe, pre-populated environment where users can experiment without consequences before committing to real data.
5. **Guided tour** — a step-by-step walkthrough with coach marks highlighting specific UI elements. Must be skippable, should be fewer than 5 steps, and should focus on the one or two actions that deliver the product's core value fastest.
6. **Video walkthrough** — a short (under 90 seconds) video demonstrating the product's core workflow. Always skippable, always optional.

The pattern chosen should match the product's complexity and the user's likely familiarity with the domain. A developer tool can assume higher baseline literacy than a consumer social app. A complex B2B platform may need a checklist; a simple utility may need nothing beyond a well-designed empty state.

Empty states and onboarding are deeply connected. The first-use empty state is often the user's first onboarding moment — it should answer "What is this?" and "What do I do first?"

See: `references/empty-error-onboarding-states.md`

## Cross-References to Related Skills

This skill intersects heavily with other areas of the UX/UI knowledge base:

- **Component Patterns & Code** (`component-patterns-code`) — Foundational component architecture for buttons, forms, modals, and other elements referenced throughout the state patterns here. Loading buttons, form validation states, and modal error displays all build on component-level patterns.

- **Interaction & Motion Design** (`interaction-motion-design`) — Animation timing, easing curves, and transition choreography for skeleton shimmer effects, toast enter/exit animations, progress indicator motion, and onboarding tour transitions. Motion is the connective tissue that makes state changes feel natural rather than jarring.

- **Mobile UX Design** (`mobile-ux-design`) — Mobile-specific considerations for notification positioning, pull-to-refresh loading patterns, offline handling on unreliable cellular connections, and touch-optimized error recovery. Mobile constraints (smaller screens, intermittent connectivity, OS-level notification rules) shape many of the patterns here.

- **Accessibility & Inclusive Design** (`accessibility-inclusive-design`) — ARIA live regions for dynamic notification announcements, screen reader behavior during loading states, focus management after error recovery, and ensuring skeleton screens do not confuse assistive technology. Every state pattern must be accessible or it is incomplete.

- **Cognitive Psychology & UX** (`cognitive-psychology-ux`) — The psychological foundations underlying perceived performance (the perception of time), notification urgency calibration (attention and interruption science), empty state motivation (goal-gradient effect, endowed progress), and error message framing (loss aversion, self-efficacy).

## Guiding Principles

1. **Every state is a design opportunity.** Empty states guide. Loading states reassure. Error states teach. Offline states demonstrate reliability. None of these are edge cases — they are core experiences.

2. **Perceived speed trumps actual speed.** Invest in skeleton screens, optimistic updates, and progressive loading. Users remember how fast something *felt*, not how fast it was.

3. **Notifications are a finite resource.** Every notification you send withdraws from a trust account. Send too many, and users revoke permission or uninstall. Earn the right to interrupt.

4. **Error messages are a conversation.** Write them in plain language. Tell the user what happened, why it matters to them, and what they can do about it. Never show raw error codes or stack traces.

5. **Onboarding should be invisible when possible.** The best onboarding is an interface so clear it does not need a tour. When explicit onboarding is necessary, make it serve the user's first goal, not the product's feature list.

6. **Offline is not an error — it is a state.** Modern applications should handle disconnection as a normal operating condition, not an exception. Cache aggressively, queue writes, and synchronize gracefully.

## State Design Audit Checklist

When designing any new feature, view, or component, walk through this checklist to ensure every state has been considered. Incomplete state coverage is the single most common source of "unpolished" feelings in production software.

**For every data-dependent view, verify you have designed:**

- **First-use empty state** — What does a new user see before creating any content? Is there an illustration, explanation, and CTA? Does the empty state educate or at least orient?
- **No-results state** — If the user searches or filters and nothing matches, what do they see? Are there suggestions for broadening the search?
- **Loading state** — What does the user see during the data fetch? Is it a skeleton (preferred for content-heavy views) or a spinner (acceptable for brief waits)? Is the loading indicator accessible to screen readers?
- **Partial loaded state** — If data arrives in stages (paginated, streamed), does the partial view look intentional? Can users interact with the content that has arrived?
- **Complete state** — The standard "happy path" design. This is what most mockups show.
- **Error state** — What happens if the data fetch fails? Is there a retry button? Is the error message human-readable? If cached data exists, is it shown with a staleness indicator?
- **Offline state** — If the user loses connectivity, what degrades? What remains functional? Is there a clear indicator that the user is offline?
- **Permission-required state** — If the view depends on a user permission (location, notifications, camera), what does the user see before granting it?

**For every user action, verify you have designed:**

- **Immediate feedback** — Does something visible change within 100ms of the action? This could be a button state change, a spinner, or an optimistic update.
- **Success confirmation** — How does the user know the action succeeded? Is it a toast, an inline change, a redirect?
- **Failure handling** — If the action fails, what does the user see? Is there a retry path? Is their input preserved?
- **Undo mechanism** — For destructive or significant actions, is there a brief undo window?

**For every notification event, verify you have designed:**

- **Channel routing** — Which channel(s) will deliver this notification? Does it change based on user context (in-app vs. away)?
- **Urgency classification** — Is the urgency level appropriate? Would a user agree that this level of interruption is warranted?
- **Preference respect** — Can the user control whether they receive this notification, and through which channel?
- **Accessibility** — Does the notification announce itself to screen readers via the appropriate ARIA live region?

This checklist is not exhaustive, but completing it for every new feature will eliminate the vast majority of state-related UX gaps that erode user trust over time.
