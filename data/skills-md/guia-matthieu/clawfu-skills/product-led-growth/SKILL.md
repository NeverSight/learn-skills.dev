---
name: product-led-growth
description: "Transform your go-to-market strategy using Wes Bush's PLG framework to make your product the primary driver of customer acquisition, activation, and retention Use when: **Launching a SaaS product** and deciding between free trial, freemium, or sales-led models; **Reducing customer acquisition costs** by letting the product do the selling; **Designing user onboarding** that drives users to value quickly; **Converting free users to paid** through product-qualified leads (PQLs); **Fighting churn..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Product-Led Growth - Build Products That Sell Themselves

> Transform your go-to-market strategy using Wes Bush's PLG framework to make your product the primary driver of customer acquisition, activation, and retention

## When to Use This Skill

- **Launching a SaaS product** and deciding between free trial, freemium, or sales-led models
- **Reducing customer acquisition costs** by letting the product do the selling
- **Designing user onboarding** that drives users to value quickly
- **Converting free users to paid** through product-qualified leads (PQLs)
- **Fighting churn** by identifying at-risk users through activity data
- **Scaling growth** without proportionally scaling sales teams
- **Optimizing pricing** around value metrics that align with customer success
- **Building viral loops** where product usage naturally spreads to new users

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | Product-Led Growth: How to Build a Product That Sells Itself (2019) |
| **Expert** | Wes Bush - Founder of Product-Led Institute, PLG strategy authority |
| **Core Principle** | "Product-Led Growth is about helping your customers experience the ongoing value your product provides. A strong brand and social proof are no longer enough—you need to let people try before they buy." |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures content frameworks | Final messaging |
| Suggests persuasion techniques | Brand voice |
| Creates draft variations | Version selection |
| Identifies optimization opportunities | Publication timing |
| Analyzes competitor approaches | Strategic direction |

## What This Skill Does

This skill helps you build a product-led go-to-market strategy where your product itself drives growth—not just your sales team or marketing campaigns.

You'll learn to:

1. **Choose the right PLG model** - Free trial, freemium, or hybrid based on your market
2. **Apply the MOAT framework** - Match your model to Market, Ocean, Audience, Time-to-value
3. **Build the value foundation** - Understand, Communicate, and Deliver value (UCD)
4. **Design the Bowling Alley** - Onboarding that keeps users on the path to value
5. **Identify Product-Qualified Leads** - Replace MQLs with PQLs based on product usage
6. **Optimize ARPU** - Increase revenue from existing users
7. **Slay the churn beast** - Prevent customer, revenue, and activity churn

The result: A product that acquires, activates, and retains customers—selling itself.

## How to Use

### Prompt Examples

```
Help me decide between freemium and free trial for my SaaS product. Use Wes Bush's
MOAT framework. My product is [description], targeting [audience], in a [market type].
```

```
Design a user onboarding flow using the Bowling Alley Framework. My product's core
value is [value], and the "Aha moment" happens when users [action]. What product
bumpers and conversational bumpers should I implement?
```

```
My free-to-paid conversion rate is 3%. Use the UCD framework to diagnose why users
aren't upgrading. Here's my current pricing page and onboarding: [describe].
```

```
Define Product-Qualified Lead (PQL) criteria for my product. Users experience value
when they [action]. What behavioral signals indicate buying intent?
```

```
Our churn rate is [X%]. Apply Wes Bush's churn framework to identify whether it's
customer, revenue, or activity churn—and recommend prevention strategies.
```

## Instructions

### What is Product-Led Growth?

```
┌─────────────────────────────────────────────────────────────┐
│              PRODUCT-LED GROWTH DEFINED                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  A go-to-market strategy where the PRODUCT ITSELF is        │
│  the primary driver of:                                     │
│                                                             │
│    → Customer ACQUISITION (users find and try product)      │
│    → Customer ACTIVATION (users experience value)           │
│    → Customer RETENTION (users keep coming back)            │
│    → Customer EXPANSION (users upgrade and refer)           │
│                                                             │
│  "Let people try before they buy"                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Why PLG is Rising:**

| Trend | Impact |
|-------|--------|
| Rising CAC | Sales-led models increasingly expensive |
| Self-education preference | Buyers want to try, not be sold to |
| Product experience importance | The product IS the buying process |

---

### Step 1: Choose Your PLG Model (MOAT Framework)

Use the MOAT framework to select the right model:

**M - Market Strategy**

| Strategy | Definition | PLG Implication |
|----------|------------|-----------------|
| **Dominant** | Undercutting competition | Free tier can capture market share |
| **Disruptive** | New category, novel solution | May need education + trial |
| **Differentiated** | Unique position in existing market | Freemium shows differentiation |

**O - Ocean Conditions**

| Ocean | Characteristics | Recommendation |
|-------|-----------------|----------------|
| **Red Ocean** | Many competitors, established category | Freemium (let product win) |
| **Blue Ocean** | Few competitors, new category | Free trial (focused experience) |

**A - Audience**

| Approach | Description | PLG Fit |
|----------|-------------|---------|
| **Top-down** | Sell to decision-makers | Sales-assisted PLG |
| **Bottom-up** | End users adopt first | Pure self-serve PLG |

**T - Time-to-Value**

| Speed | User Experience | Recommendation |
|-------|-----------------|----------------|
| **Immediate** | Value in minutes | Freemium works well |
| **Delayed** | Value takes days/weeks | Free trial with guidance |

---

### Step 2: Select Free Trial vs. Freemium

```
           FREE TRIAL                        FREEMIUM
    ┌─────────────────────┐          ┌─────────────────────┐
    │  "Try free for      │          │  "Free forever,     │
    │   14/30 days"       │          │   upgrade for more" │
    ├─────────────────────┤          ├─────────────────────┤
    │ ✓ Creates urgency   │          │ ✓ No time pressure  │
    │ ✓ Full product      │          │ ✓ Builds habit      │
    │   access            │          │ ✓ Viral potential   │
    │ ✗ Must convert or   │          │ ✗ Can attract       │
    │   lose user         │          │   freeloaders       │
    │ ✗ Less viral        │          │ ✗ Revenue delayed   │
    ├─────────────────────┤          ├─────────────────────┤
    │ Examples:           │          │ Examples:           │
    │ Netflix, Dropbox    │          │ Slack, Spotify,     │
    │ Business            │          │ Canva, Notion       │
    └─────────────────────┘          └─────────────────────┘
```

> "Freemium is like a Samurai sword: unless you're a master at using it, you can cut your arm off."

**Hybrid Options:**
- Free trial → converts to freemium
- Freemium base + free trial for premium tier
- Reverse trial (full access → downgrades to free)

---

### Step 3: Build Your Value Foundation (UCD Framework)

**U - Understand Your Value**

Map the three outcome types:

| Outcome | Question | Example (Dropbox) |
|---------|----------|-------------------|
| **Functional** | What job does it do? | "Store and access my files anywhere" |
| **Emotional** | How does it make them feel? | "Feel secure knowing files are backed up" |
| **Social** | How do they appear to others? | "Look organized and professional" |

**Define Your Value Metric:**

The value metric is the core unit of value your product delivers:

| Product | Value Metric |
|---------|--------------|
| Dropbox | Storage used (GB) |
| Slack | Messages sent |
| Zoom | Meeting minutes |
| Mailchimp | Subscribers |
| Calendly | Meetings booked |

> "If you're selling a pair of shoes, your value metric is 'per pair of shoes'—as customers buy more pairs, your business expands."

**C - Communicate Your Value**

Pricing page must pass the **5-second test**:
- Can users find the right plan in 5 seconds?
- Is the value proposition immediately clear?
- Does pricing align with value metrics?

**Principles:**
- Use social proof: "Most popular plan"
- Use similarity: "Most teams like yours choose..."
- Highlight value, not features

**D - Deliver on Your Value**

```
    PERCEIVED VALUE          VALUE GAP          EXPERIENCED VALUE
   (What marketing       ←─────────────────→    (What product
    promises)                 MINIMIZE!          delivers)

   "The path from perceived value to realized value
    should be a straight line."
```

---

### Step 4: Design the Bowling Alley (Onboarding)

> "People don't use software simply because they have tons of spare time and find clicking buttons enjoyable."

**Element 1: The Straight Line**

Map the shortest path from signup to value:

1. What is the user's desired outcome?
2. What is the "Aha moment"?
3. What are the minimum steps to get there?
4. What friction can be removed?

**Element 2: Product Bumpers (In-App)**

| Bumper | Purpose | When to Use |
|--------|---------|-------------|
| **Welcome messages** | Orient, set expectations | Immediately after signup |
| **Progress bars** | Show advancement | Multi-step onboarding |
| **Checklists** | Guide key actions | First 7 days |
| **Product tours** | Highlight features | First session |
| **Tooltips** | Contextual help | When feature discovered |
| **Empty states** | Prompt first action | Before first use |

**Element 3: Conversational Bumpers (External)**

| Email Type | Trigger | Purpose |
|------------|---------|---------|
| **Welcome** | Signup | Confirm, set expectations |
| **Usage tips** | After first actions | Deepen engagement |
| **Sales touch** | High engagement | Offer upgrade help |
| **Case study** | Mid-trial | Build trust with proof |
| **Expiry warning** | Trial ending | Create urgency |
| **Post-trial survey** | Trial ended | Learn why they didn't convert |

---

### Step 5: Identify Product-Qualified Leads (PQLs)

PQLs replace Marketing Qualified Leads (MQLs) in PLG:

```
┌─────────────────────────────────────────────────────────────┐
│  MQL (Marketing Qualified)    │  PQL (Product Qualified)    │
├───────────────────────────────┼─────────────────────────────┤
│  Downloaded whitepaper        │  Completed onboarding       │
│  Attended webinar             │  Used product 7+ days       │
│  Filled out form              │  Invited team members       │
│  High email engagement        │  Approaching plan limits    │
│  MARKETING engagement         │  PRODUCT engagement         │
└───────────────────────────────┴─────────────────────────────┘
```

**Define Your PQL Criteria:**

1. **Identify the "Aha moment"** - What action shows they've experienced value?
2. **Set behavioral thresholds** - How much usage indicates commitment?
3. **Track expansion signals** - Team invites, feature requests, limit approaches
4. **Monitor engagement patterns** - Frequency, recency, depth of usage

---

### Step 6: Optimize ARPU (Average Revenue Per User)

> "On average, a repeat customer will spend 67% more than a new customer."

**Strategies to Increase ARPU:**

| Strategy | How It Works |
|----------|--------------|
| **Value-based pricing** | Price based on value delivered, not cost |
| **Optimize tiers** | Remove confusing options, simplify choice |
| **Strategic price increases** | Test higher prices when value justifies |
| **Premium support tiers** | Offer high-touch service at premium |
| **In-product upgrade prompts** | Surface upgrades when users hit limits |
| **Annual billing incentives** | Discount for commitment, improve retention |

---

### Step 7: Slay the Churn Beast

> "Churn is the silent killer of your company. If you don't tackle churn early, you'll be working extremely hard just to stand still."

**Three Types of Churn:**

| Type | Definition | Leading/Lagging |
|------|------------|-----------------|
| **Activity churn** | Users stop using product | LEADING indicator |
| **Revenue churn** | Revenue lost from downgrades | Lagging indicator |
| **Customer churn** | Customers who cancel | Lagging indicator |

**Activity churn predicts customer churn.** Track it!

**Churn Prevention Strategies:**

1. **Continuous value delivery** - Keep shipping improvements
2. **Proactive customer success** - Reach out before they leave
3. **Activity-based re-engagement** - Trigger campaigns when usage drops
4. **Regular feedback loops** - Ask why and act on it
5. **Optimize feature adoption** - Help users discover more value

---

## Examples

### Example 1: Project Management SaaS Choosing PLG Model

**Situation**: A startup building a project management tool for remote teams. Competing against Asana, Monday, Trello in a crowded market. Team of 5, limited sales resources.

**MOAT Analysis:**

| Factor | Assessment | Implication |
|--------|------------|-------------|
| **Market** | Differentiated (not dominant, not disruptive) | Need to show unique value |
| **Ocean** | Red (many established competitors) | Freemium to compete |
| **Audience** | Bottom-up (end users adopt first) | Pure self-serve PLG |
| **Time-to-Value** | Immediate (can create project in minutes) | Freemium viable |

**Decision**: Freemium model with generous free tier

**Value Foundation (UCD):**

**Understand:**
- Functional: "Coordinate remote team work without meetings"
- Emotional: "Feel in control of distributed projects"
- Social: "Look organized to stakeholders"
- Value Metric: Active projects managed

**Communicate:**
- Free tier: 3 projects, unlimited users
- Pro tier: Unlimited projects, advanced features
- 5-second test: "Free for small teams, Pro for growing ones"

**Deliver:**
- Signup → Create first project in under 2 minutes
- Guided templates for common use cases
- No credit card required for free tier

**Bowling Alley Design:**

Product Bumpers:
- Welcome modal: "Let's create your first project"
- Empty state in dashboard: Project templates
- Progress checklist: Add task, invite member, set deadline
- Tooltip on invite: "Teams who collaborate are 3x more likely to succeed"

Conversational Bumpers:
- Day 0: Welcome + quick start guide
- Day 3: "You've created X tasks—here's how power users organize"
- Day 7: Case study of similar team
- Day 14: "Ready to add unlimited projects?"

**PQL Criteria:**
- Created 2+ projects
- Invited 2+ team members
- Active 5+ days in last 14
- Approaching 3-project limit

**Results:**
- 15% free-to-paid conversion (vs 3% industry average)
- CAC 60% lower than sales-led competitors
- Viral coefficient 0.4 (each user brings 0.4 new users)

---

### Example 2: B2B Analytics Tool Optimizing Conversion

**Situation**: A B2B analytics platform with 10,000 free users but only 2% converting to paid. Time-to-value is longer (requires data integration). High churn in first 30 days.

**Diagnosis using UCD:**

**Understand Gap:**
- Users signed up for "insights" but experienced "data setup"
- Emotional outcome not delivered: "Feel confident in decisions"
- Value metric unclear in pricing (per user vs per data source?)

**Communicate Gap:**
- Pricing page showed features, not outcomes
- No indication of which plan fits which use case
- Social proof missing on pricing page

**Deliver Gap:**
- Average time to first insight: 5 days (too long)
- 60% of users never completed data integration
- Empty dashboard showed nothing useful

**Solutions Implemented:**

**1. Bowling Alley Redesign:**

Before: Signup → Connect data → Wait → See dashboard (5 days)

After: Signup → See demo data immediately → Guided integration → First insight in 1 hour

Product Bumpers Added:
- Demo data pre-loaded showing real insights
- Step-by-step integration wizard with progress bar
- "First Insight" checklist (3 steps to value)
- Celebration modal when first insight generated

**2. Conversational Bumper System:**

| Signal | Trigger | Action |
|--------|---------|--------|
| No data connected (Day 1) | Inactivity | Integration guide email |
| Stuck on integration | Error detected | Help article + support offer |
| First insight generated | Success | "What else can you learn?" email |
| Daily active 7+ days | Engagement | Sales touch with upgrade offer |
| Approaching data limit | Usage | In-app upgrade prompt |

**3. Pricing Page Redesign:**

Before: "Starter $29/mo, Pro $99/mo, Enterprise custom"

After:
- Starter: "For individuals exploring data" - $29/mo
- Pro: "For teams making decisions together" - $99/mo (Most Popular)
- Enterprise: "For organizations with complex needs" - Custom

Added: Customer logos, ROI calculator, value metric clarity (per data source)

**4. PQL Definition:**

| PQL Score | Criteria |
|-----------|----------|
| 1 point | Completed integration |
| 2 points | Generated first insight |
| 3 points | Shared report with team member |
| 2 points | Logged in 5+ days |
| 2 points | Approaching data limit |
| **PQL threshold** | **6+ points** |

**Results after 90 days:**
- Free-to-paid conversion: 2% → 7%
- Time to first insight: 5 days → 2 hours
- 30-day churn: 45% → 18%
- PQL to paid conversion: 35%

---

## Checklists & Templates

### PLG Model Decision Matrix

```markdown
## PLG Model Decision: [Product Name]

### MOAT Assessment

**M - Market Strategy:**
□ Dominant (undercutting competition)
□ Disruptive (new category)
□ Differentiated (unique in existing category)

**O - Ocean Conditions:**
□ Red Ocean (many competitors)
□ Blue Ocean (few competitors)

**A - Audience:**
□ Top-down (decision-makers buy first)
□ Bottom-up (end users adopt first)

**T - Time-to-Value:**
□ Immediate (value in minutes)
□ Delayed (value in days/weeks)

### Recommended Model
Based on MOAT: _______________

### Model Design
- Free tier includes: _______________
- Upgrade triggers: _______________
- Time limit (if trial): _______________
```

### Value Foundation Worksheet (UCD)

```markdown
## Value Foundation: [Product Name]

### U - Understand Your Value

**Outcomes:**
- Functional: What job does it do?
  →
- Emotional: How does it make them feel?
  →
- Social: How do they appear to others?
  →

**Value Metric:**
The core unit of value is: _______________
(e.g., storage used, messages sent, projects managed)

### C - Communicate Your Value

**Pricing Page 5-Second Test:**
□ Can users identify the right plan in 5 seconds?
□ Is value proposition immediately clear?
□ Does pricing align with value metric?

**Social Proof Present:**
□ "Most popular" indicator
□ Customer logos
□ Testimonials/case studies

### D - Deliver Your Value

**Time to Value:**
- Current: User experiences value in ___ [time]
- Target: User experiences value in ___ [time]

**Value Gap Assessment:**
- What do we promise? _______________
- What do we deliver? _______________
- Gap to close: _______________
```

### Bowling Alley Framework Template

```markdown
## Bowling Alley Design: [Product Name]

### The Straight Line

**User's Desired Outcome:**

**The "Aha Moment":**
(When do users first experience real value?)

**Minimum Steps to Value:**
1.
2.
3.
4.

**Friction to Remove:**
-
-

### Product Bumpers (In-App)

| Bumper | Content | Trigger |
|--------|---------|---------|
| Welcome message | | Signup |
| Progress bar | | Onboarding |
| Checklist | | First 7 days |
| Empty state | | Before first use |
| Tooltips | | Feature discovery |

### Conversational Bumpers (Email)

| Day | Email | Purpose |
|-----|-------|---------|
| 0 | | |
| 3 | | |
| 7 | | |
| 14 | | |
| Trial end | | |
```

### PQL Scoring Model

```markdown
## PQL Definition: [Product Name]

### Behavioral Signals

| Signal | Points | Rationale |
|--------|--------|-----------|
| | | |
| | | |
| | | |
| | | |

### PQL Threshold
Score of ___ or higher = Product Qualified Lead

### PQL Workflow
When user becomes PQL:
1. [ ] Notify sales/success team
2. [ ] Trigger in-app upgrade prompt
3. [ ] Send personalized email
4. [ ] Add to sales sequence
```

---

## Skill Boundaries

### What This Skill Does Well
- Structuring persuasive content
- Applying copywriting frameworks
- Creating draft variations
- Analyzing competitor approaches

### What This Skill Cannot Do
- Guarantee conversion rates
- Replace brand voice development
- Know your specific audience
- Make final approval decisions

## References

- **Book**: Product-Led Growth: How to Build a Product That Sells Itself by Wes Bush (2019)
- **Frameworks**: MOAT, UCD, Bowling Alley, PQL
- **Resources**: ProductLed.com, Product-Led Institute
- **Source**: `sources/books/bush-product-led-growth.md`

## Related Skills

- **grand-slam-offers** - Create offers that drive trial signups
- **conversion-copywriting** - Write onboarding copy that converts
- **landing-page-copy** - Design pages that drive free trial signups
- **email-writing** - Craft conversational bumper sequences
- **jobs-to-be-done** - Understand the jobs users hire your product for
- **launch-formula** - Launch new features to drive expansion revenue
