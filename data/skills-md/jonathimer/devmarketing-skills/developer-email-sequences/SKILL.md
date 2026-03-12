---
name: developer-email-sequences
description: When the user wants to create email sequences for developers including onboarding, product updates, re-engagement, or changelog communications. Trigger phrases include "developer emails," "onboarding sequence," "email drip," "developer newsletter," "changelog email," "re-engagement campaign," or "email cadence."
metadata:
  version: 1.0.0
---

# Developer Email Sequences

This skill helps you craft email sequences that developers actually read. No spam, no fluff — just useful content delivered at the right frequency.

---

## Before You Start

1. **Load your developer audience context**:
   - Check if `.agents/developer-audience-context.md` exists
   - If not, run the `developer-audience-context` skill first
   - Understanding your developers' tech stack, pain points, and communication preferences is essential for effective email

2. **Audit existing emails**:
   - What emails are you currently sending?
   - What are open rates, click rates, unsubscribe rates?
   - Any feedback from developers about your emails?

---

## The Developer Email Reality

Developers are ruthless with email:

| Behavior | Implication |
|----------|-------------|
| Preview pane scanning | Subject line and first line are everything |
| Aggressive unsubscribing | One irrelevant email = unsubscribe |
| Plain text preference | Many prefer plain text over HTML |
| Code snippet love | Useful code examples get clicked |
| Transactional trust | They open receipts, not "newsletters" |

**Golden rule**: Every email must provide immediate value or solve a problem.

---

## Email Sequence Types

### 1. Onboarding Sequence

**Goal**: Get developers to their first "Hello World" moment.

**Timing**:
- Email 1: Immediately after signup
- Email 2: 24 hours (if no activation)
- Email 3: 3 days (if no activation)
- Email 4: 7 days (if no activation)
- STOP if they activate

**Structure**:

| Email | Purpose | Content |
|-------|---------|---------|
| Welcome | Confirm signup, one clear CTA | Link to quickstart, nothing else |
| First nudge | Address common blockers | "Here's where most devs get stuck..." |
| Value reminder | Show what's possible | Customer example or code snippet |
| Last chance | Direct ask | "Need help? Reply to this email" |

**Template: Welcome Email**

```
Subject: Your API key is ready

Hey [NAME],

Your API key: [KEY]

Quickstart (2 minutes):
[LINK TO QUICKSTART]

That's it. Hit reply if you get stuck.

— [SENDER NAME]
```

**Template: First Nudge**

```
Subject: Quick question about your setup

Hey [NAME],

Noticed you haven't made your first API call yet.

Where'd you get stuck?

[ ] Didn't have time yet
[ ] Confused about authentication
[ ] Can't find the right SDK
[ ] Something else

Just reply — I read every response.

— [SENDER NAME]
```

### 2. Activation Sequence

**Goal**: Turn first-time users into regular users.

**Trigger**: After first successful API call or integration.

**Timing**:
- Email 1: Immediately after first success
- Email 2: 3 days later
- Email 3: 7 days later
- Email 4: 14 days later

**Structure**:

| Email | Purpose | Content |
|-------|---------|---------|
| Celebration | Acknowledge progress | "Your first call worked!" |
| Next step | Show natural progression | "Most devs do X next..." |
| Deep feature | Introduce advanced capability | Tutorial or code example |
| Integration | Suggest production use | Case study or deployment guide |

### 3. Changelog / Product Update Emails

**Goal**: Keep developers informed without overwhelming them.

**Frequency**: Weekly digest or per-release (never more than 2x/week).

**Structure**:

```markdown
Subject: [Product] v2.3 — Faster webhooks, TypeScript 5 support

What's new:

## Breaking changes (read first)
- Webhook signature algorithm changed (migration guide)

## New
- TypeScript 5.0 support
- Batch API for bulk operations

## Improved
- Webhook delivery 3x faster
- Better error messages for auth failures

## Fixed
- Memory leak in long-running connections

Full changelog: [LINK]

---

Need help upgrading? Reply or join #support in Discord.
```

**Rules**:
- Breaking changes ALWAYS at the top
- Code examples for new features
- Link to full changelog, don't dump everything in email
- No marketing fluff — just facts

### 4. Re-engagement Sequence

**Goal**: Win back developers who've gone quiet.

**Trigger**: No activity for 30/60/90 days.

**Timing**:
- Email 1: Day 30 of inactivity
- Email 2: Day 45
- Email 3: Day 60
- Email 4: Day 90 (sunset warning)

**Structure**:

| Email | Purpose | Content |
|-------|---------|---------|
| Check-in | Soft touch | "Everything okay?" |
| What's new | Show progress | Recent features they missed |
| Direct ask | Understand why | Survey or reply request |
| Sunset | Account warning | "We'll pause your account..." |

**Template: Check-in**

```
Subject: Did something break?

Hey [NAME],

Haven't seen you in a while.

Quick check:

- Did you run into a problem? (Reply and I'll help)
- Building something else? (Totally fine)
- Found a better solution? (Genuinely curious what)

No hard feelings either way — just want to make sure
you're not stuck on something we can fix.

— [SENDER NAME]
```

**Template: Sunset Warning**

```
Subject: Pausing your account in 14 days

Hey [NAME],

Your [PRODUCT] account has been inactive for 90 days.

To keep things tidy, we'll pause your account on [DATE].

What this means:
- Your API keys will stop working
- Your data stays safe (we don't delete anything)
- You can reactivate anytime by logging in

If you're still using [PRODUCT], just log in once to keep
your account active: [LOGIN LINK]

No action needed if you've moved on.

— [SENDER NAME]
```

---

## Frequency Guidelines

| Email Type | Maximum Frequency | Notes |
|------------|-------------------|-------|
| Transactional | As needed | Receipts, password resets, usage alerts |
| Onboarding | 4 emails over 7 days | Stop when activated |
| Changelog | 1x/week maximum | Digest preferred over per-release |
| Re-engagement | 4 emails over 60 days | Then stop |
| Marketing/Newsletter | 2x/month maximum | Must provide genuine value |

**The unsubscribe test**: If a developer would feel relieved to unsubscribe from this email type, you're sending too many.

---

## Technical Content in Emails

### Code Snippets

**Do**:
- Keep snippets under 10 lines
- Use syntax highlighting (if HTML email)
- Test that code actually works
- Include language/framework version

**Don't**:
- Assume a specific environment
- Include secrets or realistic-looking API keys
- Use outdated syntax

**Example: Good code snippet**

```
# Python 3.8+
import yourapi

client = yourapi.Client("your-api-key")
result = client.analyze("Hello, world!")
print(result.sentiment)  # "positive"
```

### API Updates

When announcing API changes:

```markdown
## New endpoint: POST /v2/batch

Process up to 100 items in a single request.

```python
client.batch([
    {"text": "First item"},
    {"text": "Second item"},
    # ... up to 100 items
])
```

Rate limit: 10 batch requests/minute
Docs: [LINK]
```

---

## Transactional vs Marketing Emails

| Transactional | Marketing |
|---------------|-----------|
| Triggered by user action | Sent on schedule |
| Expected and wanted | Needs opt-in |
| Higher deliverability | More spam filtering |
| No unsubscribe required | Must have unsubscribe |
| CAN-SPAM exempt (mostly) | Full CAN-SPAM compliance |

**Examples**:

| Transactional | Marketing |
|---------------|-----------|
| Password reset | Newsletter |
| Payment receipt | Product announcement |
| Usage alert (95% quota) | Case study promotion |
| API key rotation reminder | Webinar invitation |
| Security notification | Feature highlight |

**Gray area**: Onboarding emails can be transactional (user signed up) but should still have easy unsubscribe.

---

## Measuring Email Effectiveness

### Metrics That Matter

| Metric | Good | Warning | Action |
|--------|------|---------|--------|
| Open rate | >40% | <25% | Fix subject lines |
| Click rate | >10% | <3% | Fix content/CTA |
| Unsubscribe rate | <0.2% | >0.5% | Reduce frequency or improve targeting |
| Reply rate | >1% | N/A | Celebrate! |
| Activation (onboarding) | >30% | <15% | Rethink sequence |

### What to Track

1. **Onboarding sequence**: % who activate within 7 days
2. **Changelog emails**: Click-through to docs/release notes
3. **Re-engagement**: % who return to product
4. **All emails**: Unsubscribe rate by email type

### A/B Testing Priorities

1. Subject lines (biggest impact)
2. Send time
3. Email length
4. Plain text vs HTML
5. CTA wording

---

## Unsubscribe Handling

### Preference Center

Let developers control what they get:

```
Email Preferences for [EMAIL]

[ ] Product updates (new features, changelog)
[ ] Security alerts (always recommended)
[ ] Community news (events, meetups)
[ ] Tips and tutorials

Or: Unsubscribe from all marketing emails
(You'll still receive transactional emails like receipts and security alerts)
```

### Graceful Unsubscribe

When someone unsubscribes, confirm simply:

```
Subject: You're unsubscribed

You've been removed from [EMAIL TYPE] emails.

You'll still receive:
- Security alerts
- Payment receipts
- Usage notifications

Changed your mind? Update preferences: [LINK]
```

### Re-subscribe Flow

After unsubscribe, don't:
- Send "We miss you" emails
- Ask them to reconsider
- Add them back to other lists

Do:
- Make it easy to re-subscribe from your site
- Remember their preference if they return

---

## Email Templates Library

### Account Security

```
Subject: Action required: Unusual login detected

We detected a login from a new location:

Location: [CITY, COUNTRY]
Device: [BROWSER/OS]
Time: [TIMESTAMP]

If this was you, no action needed.

If this wasn't you:
1. Change your password immediately: [LINK]
2. Rotate your API keys: [LINK]
3. Review recent API activity: [LINK]

Questions? Reply to this email.

— [PRODUCT] Security Team
```

### Usage Alert

```
Subject: Heads up: You've used 80% of your API quota

Your usage this month: [CURRENT] / [LIMIT] requests

At your current rate, you'll hit your limit around [DATE].

Options:
- Upgrade your plan: [LINK]
- Optimize your usage: [DOCS LINK]
- Wait for reset on [RESET DATE]

We'll send another alert at 95%.

— [PRODUCT]
```

### Payment Failed

```
Subject: Payment failed — update your card to avoid interruption

We couldn't charge your card ending in [LAST4].

Update your payment method: [LINK]

We'll retry in 3 days. If unsuccessful, your account will be
downgraded to the free tier on [DATE].

Your API will continue working until then.

Questions about billing? Reply to this email.

— [PRODUCT]
```

---

## Common Mistakes

| Mistake | Why it fails | Fix |
|---------|--------------|-----|
| "Just checking in" | No value, wastes time | Every email needs a purpose |
| Weekly newsletter with nothing new | Trains devs to ignore you | Only send when you have content |
| HTML-heavy design | Looks like marketing spam | Plain text or minimal HTML |
| Multiple CTAs | Confuses, reduces clicks | One clear action per email |
| Fake personalization | "Hi [FNAME]" feels robotic | Use personalization meaningfully or not at all |
| Celebrating your milestones | Developers don't care about your funding | Focus on what matters to them |

---

## Tools

| Tool | Use Case |
|------|----------|
| **[Octolens](https://octolens.com)** | Monitor developer sentiment about your emails — see if people complain about frequency or praise specific updates on Twitter, Reddit, Hacker News |
| **Customer.io** | Sophisticated automation for developer-focused email |
| **Postmark** | High deliverability transactional email |
| **Buttondown** | Developer-friendly newsletter platform |
| **Resend** | Modern email API built for developers |
| **Loops** | Email for SaaS with good segmentation |

---

## Related Skills

- `developer-audience-context` — Foundation for knowing what content resonates
- `developer-churn` — Re-engagement strategies for at-risk users
- `changelog-updates` — Structuring product updates
- `developer-onboarding` — Full onboarding strategy beyond just email
