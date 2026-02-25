---
name: mvp-planning
description: Plan and scope a Minimum Viable Product for a solopreneur. Use when deciding what to build first, what to cut, how to prioritize features, how to define "done" for a first launch, and how to structure the MVP build process. Covers the MVP definition, feature ruthless-cutting framework, build-vs-buy decisions, launch criteria, and post-launch learning loops. Trigger on "plan my MVP", "minimum viable product", "what should I build first", "scope my product", "MVP roadmap", "what features to include", "first version", "launch something".
---

# MVP Planning

## Overview
An MVP is not a product with every feature you can imagine stripped down. It is the smallest thing you can build that tests your core business hypothesis and delivers real value to real customers. If you build too much, you waste time on features nobody asked for. If you build too little, you launch something that doesn't actually solve the problem. This playbook defines the line precisely and gives you a repeatable process to find it.

---

## Step 1: Restate Your Core Hypothesis

Before scoping anything, write down the single hypothesis your MVP must test. Everything you include must serve this hypothesis. Everything that doesn't gets cut.

**Format:**
```
IF we build [specific product that does X for Y customers],
THEN [specific outcome we expect — e.g., Z% will pay, W% will return weekly].
```

**Example:**
"IF we build an automated client progress report tool for freelance developers, THEN at least 30% of beta users will use it weekly within the first month, and at least 10% will convert to a paid plan."

The hypothesis has two parts: a behavior signal (usage) and a revenue signal (payment). Both must be measurable. If you can't measure it, you can't learn from it.

---

## Step 2: Define What "Viable" Means for Your Specific Situation

"Viable" is not universal. It depends on your hypothesis. Map your hypothesis to the minimum experience needed to test it.

**Ask these questions:**
1. What is the absolute minimum a customer needs to experience to decide "this is valuable" or "this is not"?
2. What is the one core interaction that delivers the value proposition?
3. What can be manual, ugly, or missing and still test the hypothesis? (These things get cut or faked.)
4. What CANNOT be missing without the product feeling broken or useless? (These are non-negotiable.)

**Label every feature as:**
- 🔴 **Must-have:** Product is meaningless without this. Hypothesis cannot be tested without it.
- 🟡 **Nice-to-have:** Improves experience but hypothesis can still be tested without it.
- 🟢 **Cut:** Not needed for the hypothesis at all. Build later if validated.

---

## Step 3: Feature Ruthless-Cutting

Take your full feature wishlist and run every item through this filter. Be brutal. Solopreneurs have limited build time — every unnecessary feature is time stolen from the core value.

**The Four Cuts:**

### Cut 1: The Hypothesis Cut
Does this feature directly serve testing your core hypothesis?
- Yes → Keep (for now, pending further cuts)
- No → Cut. No exceptions.

### Cut 2: The "Fake It" Cut
Can this feature be faked or done manually for the first N customers without them knowing or caring?

Examples of things you can fake:
- A "dashboard" that's actually a shared Google Sheet for your first 10 customers
- "Real-time" updates that are actually sent on a 1-hour delay
- "AI-powered" recommendations that are actually you manually curating them for beta users
- An "API integration" that's actually a scheduled script running every few hours

If you can fake it convincingly for beta scale, fake it. Build the real version only after you've confirmed people actually want it.

### Cut 3: The Sequencing Cut
Is this feature something that MUST exist at launch, or can it be added in v1.1 (within 2 weeks of launch)?

If it can wait 2 weeks and the product is still usable and testable without it → cut it from MVP scope. Move it to "Week 2" backlog.

### Cut 4: The Delight Cut
Is this feature a "delight" — something nice but not expected?

Delights are great for retention but terrible for MVPs. Cut them all. Your MVP should be functional and clear, not delightful. Delight is a v2 luxury.

**After all four cuts, you should have a dramatically smaller feature list than you started with.** If it still feels like a lot, cut again. The most common MVP mistake is building too much.

---

## Step 4: Define Your MVP Scope Document

Write a single-page document that locks the scope. This prevents scope creep and gives you a clear "done" line.

```
MVP SCOPE DOCUMENT
==================

HYPOTHESIS: [from Step 1]

CORE VALUE DELIVERED: [one sentence — what the user gets]

MUST-HAVE FEATURES (🔴):
  1. [Feature] — because [why it's essential to the hypothesis]
  2. [Feature] — because [why]
  3. [Feature] — because [why]

FAKED / MANUAL FEATURES (🟡 deferred to real implementation):
  1. [Feature] — faked as [how] — real build in [when]
  2. [Feature] — faked as [how] — real build in [when]

CUT FROM MVP (🟢 — revisit after launch):
  1. [Feature]
  2. [Feature]
  ...

LAUNCH CRITERIA (all must be true before you call this "launched"):
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
  - [ ] [Criterion 3]

WHAT SUCCESS LOOKS LIKE (measured in the first 30 days):
  - [Metric 1]: target = [number]
  - [Metric 2]: target = [number]
```

---

## Step 5: Build vs. Buy Decisions

For every piece of technology your MVP needs, decide: build it yourself, buy/use an existing tool, or use a no-code/low-code solution.

**Decision framework:**

| If this is... | Then... |
|---|---|
| Your core differentiator | BUILD. This is what makes you unique. Outsourcing it = outsourcing your advantage. |
| Commodity infrastructure (hosting, payments, auth, email) | BUY. Use established tools (Stripe, Auth0, SendGrid, Vercel, etc.). Building these yourself wastes months. |
| A workflow you'll do 100+ times but isn't your core product | AUTOMATE with no-code (Zapier, Make, n8n). Build only if the automation tools can't handle it. |
| Something you need once or very rarely | BUY or use a freelancer. Don't build a tool you'll use once. |

**Solopreneur rule:** The fewer custom-built components, the faster your MVP ships. Ruthlessly use existing tools for everything except the one thing that is uniquely yours.

---

## Step 6: Estimate and Schedule the Build

For each must-have feature, estimate:
- **Build time** (hours — be honest, then add 50% buffer)
- **Dependencies** (does feature B require feature A to be done first?)
- **Complexity risk** (is there a part you're unsure about? Build that part FIRST to de-risk)

**Build order rules:**
1. Build the riskiest technical piece first. If it turns out to be impossible or takes 3x longer, you want to know now — before you've built everything around it.
2. Build the core value loop second. This is the single interaction that delivers your value proposition. Everything else connects to this.
3. Build supporting features last. Auth, onboarding copy, polish — these come after the core works.

**Timeline:**
- Set a hard launch date (create external pressure — tell someone, set up a waitlist).
- Work backward from launch date to today. Does the build time fit?
- If it doesn't fit, cut more features (back to Step 3) or extend the date. Do NOT compromise on the core value loop to hit an arbitrary deadline.

---

## Step 7: Launch Criteria Checklist

Do not launch until every item is checked:

- [ ] Core value loop works end-to-end (a real user can go from signup to experiencing the value)
- [ ] No data-losing bugs (you can lose polish, not data)
- [ ] Payment works (if monetized at launch — even if it's just a "pay later" promise)
- [ ] You can onboard a stranger in under 5 minutes without helping them (test with 3 real strangers)
- [ ] You have a way to collect feedback (in-app survey, email, or Slack channel)
- [ ] You have a way to monitor basic health (uptime, error rates, basic analytics)
- [ ] You have a plan for the first 48 hours post-launch (who you notify, how you monitor, how you respond to feedback)

---

## Step 8: Post-Launch Learning Loop

The MVP is not the end — it is the beginning of a learning loop.

**Week 1 post-launch:**
- Talk to every single early user. Not a survey — a real conversation. What confused them? What delighted them? What did they expect that wasn't there?
- Watch them use the product if possible (screen share, session recordings). Where do they hesitate? Where do they drop off?

**Week 2-4:**
- Measure your success metrics (from the scope document). Are you on track?
- Identify the single biggest gap between what you built and what users actually need.
- Decide: iterate on the current MVP, or pivot the hypothesis?

**Decision rules:**
- If usage metrics are strong but revenue is weak → pricing or conversion problem. Iterate on that.
- If usage metrics are weak → the core value isn't landing. Potentially a pivot situation.
- If both are strong → you have product-market fit signals. Scale up (more users, more marketing, more features).

---

## MVP Mistakes to Avoid
- Building features because they're fun to build, not because they test the hypothesis.
- Launching to your friends first. Friends are too polite to give useful feedback. Launch to strangers.
- Perfecting the UI before confirming the value. A ugly product that solves a real problem beats a beautiful product nobody needs.
- Treating the MVP as the final product. It isn't. It's a learning machine. Expect to rebuild 60-80% of it in v2.
- Not shipping. The best MVP is a shipped MVP. An unshipped MVP teaches you nothing.
