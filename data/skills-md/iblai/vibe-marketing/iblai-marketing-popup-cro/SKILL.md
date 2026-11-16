---
name: iblai-marketing-popup-cro
description: When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also use when the user mentions "exit intent," "popup conversions," "modal optimization," "lead capture popup," "email popup," "announcement banner," "overlay," "collect emails with a popup," "exit popup," "scroll trigger," "sticky bar," or "notification bar." Use this for any overlay or interrupt-style conversion element. For forms outside of popups, see iblai-marketing-form-cro. For general page conversion optimization, see iblai-marketing-page-cro.
globs:
alwaysApply: false
metadata:
  version: 1.1.0
---

# /iblai-marketing-popup-cro

Build popups and modals that convert without annoying users or damaging
the brand.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Pin down before recommending:

1. **Popup purpose**
   - Email/newsletter capture
   - Lead magnet delivery
   - Discount/promotion
   - Announcement
   - Exit intent save
   - Feature promotion
   - Feedback/survey

2. **Current state**
   - Existing popup performance
   - Triggers in use
   - User complaints or feedback
   - Mobile experience

3. **Traffic context**
   - Traffic sources (paid, organic, direct)
   - New vs. returning visitors
   - Page types where shown

---

## Core Principles

1. **Timing is everything.** Too early = annoying interruption. Too late = missed opportunity. Right time = helpful offer at moment of need.
2. **Value must be obvious.** Clear, immediate benefit. Relevant to page context. Worth the interruption.
3. **Respect the user.** Easy to dismiss. Don't trap or trick. Remember preferences. Don't ruin the experience.

---

## Trigger Strategies

### Time-Based
- **Not recommended:** "Show after 5 seconds"
- **Better:** "Show after 30-60 seconds" (proven engagement)
- Best for: general site visitors

### Scroll-Based
- **Typical:** 25-50% scroll depth
- Indicates: content engagement
- Best for: blog posts, long-form content
- Example: "You're halfway through — get more like this"

### Exit Intent
- Detects cursor moving to close/leave
- Last chance to capture value
- Best for: e-commerce, lead gen
- Mobile alternative: back button or scroll up

### Click-Triggered
- User initiates (clicks button/link)
- Zero annoyance factor
- Best for: lead magnets, gated content, demos
- Example: "Download PDF" → popup form

### Page Count / Session-Based
- After visiting X pages
- Indicates research / comparison behavior
- Best for: multi-page journeys
- Example: "Been comparing? Here's a summary..."

### Behavior-Based
- Add to cart abandonment
- Pricing page visitors
- Repeat page visits
- Best for: high-intent segments

---

## Popup Types

### Email Capture Popup
**Goal:** newsletter / list subscription

**Best practices:**
- Clear value prop (not just "Subscribe")
- Specific benefit of subscribing
- Single field (email only)
- Consider an incentive (discount, content)

**Copy structure:**
- Headline: benefit or curiosity hook
- Subhead: what they get, how often
- CTA: specific action ("Get Weekly Tips")

### Lead Magnet Popup
**Goal:** exchange content for email

**Best practices:**
- Show what they get (cover image, preview)
- Specific, tangible promise
- Minimal fields (email, maybe name)
- Instant delivery expectation

### Discount/Promotion Popup
**Goal:** first purchase or conversion

**Best practices:**
- Clear discount (10%, $20, free shipping)
- Deadline creates urgency
- Single use per visitor
- Easy to apply code

### Exit Intent Popup
**Goal:** last-chance conversion

**Best practices:**
- Acknowledge they're leaving
- Different offer than the entry popup
- Address common objections
- Final compelling reason to stay

**Formats:**
- "Wait! Before you go..."
- "Forget something?"
- "Get 10% off your first order"
- "Questions? Chat with us"

### Announcement Banner
**Goal:** site-wide communication

**Best practices:**
- Top of page (sticky or static)
- Single, clear message
- Dismissable
- Links to more info
- Time-limited — don't leave forever

### Slide-In
**Goal:** less intrusive engagement

**Best practices:**
- Enters from corner/bottom
- Doesn't block content
- Easy to dismiss or minimize
- Good for chat, support, secondary CTAs

---

## Design Best Practices

### Visual Hierarchy
1. Headline (largest, first seen)
2. Value prop / offer (clear benefit)
3. Form / CTA (obvious action)
4. Close option (easy to find)

### Sizing
- Desktop: 400-600px wide typical
- Don't cover the entire screen
- Mobile: full-width bottom or center, not full-screen
- Leave space to close (visible X, click outside)

### Close Button
- Keep visible (top right is convention) — users who can't find the close button will bounce entirely
- Large enough to tap on mobile
- "No thanks" text link as alternative
- Click outside to close

### Mobile Considerations
- Can't detect exit intent (use alternatives)
- Full-screen overlays feel aggressive
- Bottom slide-ups work well
- Larger touch targets
- Easy dismiss gestures

### Imagery
- Product image or preview
- Face if relevant (increases trust)
- Minimal for speed
- Optional — copy can carry alone

---

## Copy Formulas

### Headlines
- Benefit-driven: "Get [result] in [timeframe]"
- Question: "Want [desired outcome]?"
- Command: "Don't miss [thing]"
- Social proof: "Join [X] people who..."
- Curiosity: "The one thing [audience] always get wrong about [topic]"

### Subheadlines
- Expand on the promise
- Address an objection ("No spam, ever")
- Set expectations ("Weekly tips in 5 min")

### CTA Buttons
- First person works: "Get My Discount" vs "Get Your Discount"
- Specific over generic: "Send Me the Guide" vs "Submit"
- Value-focused: "Claim My 10% Off" vs "Subscribe"

### Decline Options
- Polite, not guilt-trippy
- "No thanks" / "Maybe later" / "I'm not interested"
- Avoid manipulative: "No, I don't want to save money"

---

## Frequency and Rules

### Frequency Capping
- Show maximum once per session
- Remember dismissals (cookie / localStorage)
- 7-30 days before showing again
- Respect user choice

### Audience Targeting
- New vs. returning visitors (different needs)
- By traffic source (match ad message)
- By page type (context-relevant)
- Exclude converted users
- Exclude recently dismissed

### Page Rules
- Exclude checkout / conversion flows
- Consider blog vs. product pages
- Match offer to page context

---

## Compliance and Accessibility

### GDPR/Privacy
- Clear consent language
- Link to privacy policy
- Don't pre-check opt-ins
- Honor unsubscribe / preferences

### Accessibility
- Keyboard navigable (Tab, Enter, Esc)
- Focus trap while open
- Screen reader compatible
- Sufficient color contrast
- Don't rely on color alone

### Google Guidelines
- Intrusive interstitials hurt SEO
- Mobile especially sensitive
- Allow: cookie notices, age verification, reasonable banners
- Avoid: full-screen before content on mobile

---

## Measurement

### Key Metrics
- **Impression rate** — visitors who see the popup
- **Conversion rate** — impressions → submissions
- **Close rate** — how many dismiss immediately
- **Engagement rate** — interaction before close
- **Time to close** — how long before dismissing

### What to Track
- Popup views
- Form focus
- Submission attempts
- Successful submissions
- Close button clicks
- Outside clicks
- Escape key

### Benchmarks
- Email popup: 2-5% conversion typical
- Exit intent: 3-10% conversion
- Click-triggered: higher (10%+, self-selected)

---

## Output Format

### Popup Design
- **Type:** email capture, lead magnet, etc.
- **Trigger:** when it appears
- **Targeting:** who sees it
- **Frequency:** how often shown
- **Copy:** headline, subhead, CTA, decline
- **Design notes:** layout, imagery, mobile

### Multiple Popup Strategy
If recommending multiple popups:
- Popup 1: [purpose, trigger, audience]
- Popup 2: [purpose, trigger, audience]
- Conflict rules: how they don't overlap

### Test Hypotheses
Ideas to A/B test with expected outcomes.

---

## Common Popup Strategies

### E-commerce
1. Entry/scroll: first-purchase discount
2. Exit intent: bigger discount or reminder
3. Cart abandonment: complete your order

### B2B SaaS
1. Click-triggered: demo request, lead magnets
2. Scroll: newsletter / blog subscription
3. Exit intent: trial reminder or content offer

### Content/Media
1. Scroll-based: newsletter after engagement
2. Page count: subscribe after multiple visits
3. Exit intent: don't miss future content

### Lead Generation
1. Time-delayed: general list building
2. Click-triggered: specific lead magnets
3. Exit intent: final capture attempt

---

## Experiment Ideas

### Placement & Format

**Banner Variations**
- Top bar vs. banner below header
- Sticky banner vs. static banner
- Full-width vs. contained banner
- Banner with countdown timer vs. without

**Popup Formats**
- Center modal vs. slide-in from corner
- Full-screen overlay vs. smaller modal
- Bottom bar vs. corner popup
- Top announcements vs. bottom slideouts

**Position Testing**
- Popup sizes on desktop and mobile
- Left corner vs. right corner for slide-ins
- Visibility without blocking content

---

### Triggers

**Timing**
- Exit intent vs. 30-second delay vs. 50% scroll depth
- Optimal time delay (10s vs. 30s vs. 60s)
- Scroll depth percentage (25% vs. 50% vs. 75%)
- Page count trigger (show after X pages viewed)

**Behavior**
- Intent prediction
- Specific page visits
- Return visitor vs. new visitor targeting
- Referral source

**Click**
- Click-triggered popups for lead magnets
- Button-triggered vs. link-triggered modals
- In-content triggers vs. sidebar triggers

---

### Messaging & Content

**Headlines & Copy**
- Attention-grabbing vs. informational headlines
- "Limited-time offer" vs. "New feature alert" messaging
- Urgency-focused vs. value-focused copy
- Headline length and specificity

**CTAs**
- Button text variations
- Button color for contrast
- Primary + secondary CTA vs. single CTA
- Decline text (friendly vs. neutral)

**Visual Content**
- Countdown timers for urgency
- With/without images
- Product preview vs. generic imagery
- Social proof in popup

---

### Personalization

**Dynamic Content**
- Popup based on visitor data
- Industry-specific content
- Tailor to pages visited
- Progressive profiling (ask more over time)

**Audience Targeting**
- New vs. returning visitor messaging
- Segment by traffic source
- Target by engagement level
- Exclude already-converted visitors

---

### Frequency & Rules

- Frequency capping (once per session vs. once per week)
- Cool-down period after dismissal
- Different dismiss behaviors
- Escalating offers over multiple visits

---

## Task-Specific Questions

1. Primary goal for this popup?
2. Current popup performance (if any)?
3. Traffic sources you're optimizing for?
4. Incentive you can offer?
5. Compliance requirements (GDPR, etc.)?
6. Mobile vs. desktop traffic split?

---

## Related Skills

- **iblai-marketing-lead-magnets**: Planning lead magnets to promote via popups
- **iblai-marketing-form-cro**: Optimizing the form inside the popup
- **iblai-marketing-page-cro**: Page context around popups
- **iblai-marketing-email-sequence**: What happens after popup conversion
- **iblai-marketing-ab-test-setup**: Testing popup variations
