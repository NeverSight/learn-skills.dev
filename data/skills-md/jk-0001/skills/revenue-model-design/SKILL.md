---
name: revenue-model-design
description: Design a revenue model for a solopreneur business — how money flows in, from whom, and on what cadence. Use when deciding how to monetize a product or service, choosing between revenue streams, structuring recurring vs one-time income, or diversifying revenue. Covers all major revenue model types, selection criteria, revenue stream stacking, and the relationship between revenue model and product design. Trigger on "how will I make money", "revenue model", "monetization strategy", "revenue streams", "recurring revenue", "how to monetize", "business revenue model", "diversify income".
---

# Revenue Model Design

## Overview
A revenue model is not just "how much do I charge" — it is the complete system of how value translates into money. The wrong model can make a great product fail (people love it but won't pay the way you structured it). The right model turns a good product into a sustainable business. This playbook helps you choose, design, and validate the right model for your specific situation.

---

## Step 1: Understand the Revenue Model Landscape

Know your options before choosing. Each model has different implications for cash flow, customer behavior, product design, and growth.

### Recurring Revenue Models
Money comes in on a predictable schedule. The backbone of sustainable solopreneur businesses.

**Subscription (monthly/annual):** Customer pays a fixed amount per period for ongoing access.
- Pros: Predictable cash flow. Compounds over time. Customers amortize the cost mentally (feels cheaper than one-time).
- Cons: Churn is constant. Must continuously deliver value or people cancel.
- Best for: SaaS products, tools, services with ongoing value delivery.

**Retainer:** Customer pays a fixed monthly fee for a defined scope of ongoing work or access.
- Pros: Guaranteed income. Simplifies scoping conversations.
- Cons: Can become a trap if the customer expects unlimited work within the retainer.
- Best for: Consulting, managed services, ongoing advisory relationships.

**Membership:** Customer pays to be part of a group that provides ongoing value (community, content, access).
- Pros: Low churn if community is strong. Scales well.
- Cons: Requires consistent content or community value delivery.
- Best for: Courses + community, mastermind groups, niche professional networks.

### One-Time Revenue Models
Single payments. Great for cash flow spikes, less predictable long-term.

**Product sale:** Customer buys a product once and owns it.
- Pros: No churn. Simple. High margin if digital.
- Cons: Must constantly acquire new customers. No revenue compounds.
- Best for: Digital products (templates, ebooks, courses without updates), software with perpetual licenses.

**Service/project:** Customer pays for a defined deliverable.
- Pros: High revenue per transaction. Flexible scope.
- Cons: Time-capped. Must sell the next project constantly. No recurring base.
- Best for: Consulting projects, freelance work, custom builds.

### Usage-Based Models
Revenue scales with how much the customer actually uses the product.

**Per-transaction:** Customer pays each time they complete an action (e.g., per invoice sent, per email sent).
- Pros: Aligns cost with value received. Low barrier to entry.
- Cons: Unpredictable revenue. Customers may cap usage to control costs.
- Best for: Payment processing, marketplace platforms, API products.

**Tiered usage:** Customer pays based on usage bands (e.g., up to 100 transactions = $X, up to 500 = $Y).
- Pros: More predictable than pure per-transaction. Still usage-aligned.
- Cons: Slightly more complex to communicate.
- Best for: SaaS products where usage varies significantly between customers.

### Marketplace / Commission Models
Revenue comes from facilitating a transaction between two parties.

**Commission:** You take a percentage of each transaction on your platform.
- Pros: Scales with the marketplace's GMV. Low upfront cost for users.
- Cons: Requires two-sided network effects. Chicken-and-egg problem at launch.
- Best for: Platforms connecting buyers and sellers.

**Lead generation:** You send qualified leads to businesses and charge per lead or per conversion.
- Pros: Scales well with content/SEO.
- Cons: Dependent on advertiser budgets. Can be commoditized.
- Best for: Content-heavy businesses in high-value verticals (finance, real estate, B2B services).

---

## Step 2: Match Model to Your Situation

Answer these questions to narrow your options:

| Question | If Yes → Lean Toward |
|---|---|
| Does my product deliver value continuously (not just once)? | Subscription or membership |
| Is my product digital with near-zero marginal cost per user? | Subscription or one-time sale |
| Do customers' usage levels vary wildly? | Usage-based or tiered usage |
| Am I selling my time or expertise directly? | Retainer or project/service |
| Do I need predictable monthly income? | Subscription or retainer |
| Am I early and need to reduce purchase friction to get first customers? | Freemium (free tier) or usage-based |
| Can I connect two groups who want to transact? | Marketplace or commission |

---

## Step 3: Design Your Revenue Stream Stack

Most sustainable solopreneur businesses have 2-3 revenue streams, not one. A single stream is fragile — if it dips, everything dips.

**Revenue stream stacking rules:**

1. **One primary stream (60-70% of revenue):** Your main product or service. This is where you focus growth efforts.
2. **One secondary stream (20-30%):** A complementary revenue source that serves the same customers or ecosystem. Often lower-effort or more passive.
3. **One opportunistic stream (5-10%):** Something that generates revenue when opportunity arises. Can be inconsistent.

**Common solopreneur stack patterns:**

| Primary | Secondary | Opportunistic |
|---|---|---|
| SaaS subscription | Digital course or template pack | Consulting/speaking |
| Consulting retainers | Productized service (fixed scope, fixed price) | Affiliate revenue from tool recommendations |
| Digital product (one-time) | Subscription upgrade (premium features or updates) | Freelance projects |
| Content/newsletter | Sponsored posts or affiliate links | Workshops or cohorts |

**Stack design rule:** Every stream should serve the same core customer or ecosystem. Revenue streams that pull you in different directions dilute your focus and brand.

---

## Step 4: Design the Payment Flow

For each revenue stream, map the exact payment experience:

```
REVENUE STREAM: [name]
MODEL: [subscription / one-time / usage / etc.]
PRICE: [amount and cadence]
PAYMENT TRIGGER: [what action causes the charge — signup, usage threshold, renewal]
PAYMENT METHOD: [credit card, invoice, etc.]
BILLING TOOL: [Stripe, Paddle, Lemon Squeezy, etc.]
FREE TRIAL: [yes/no, length, requires card?]
CANCELLATION FLOW: [how easy is it to cancel? — make this frictionless or you'll get chargebacks]
UPGRADE PATH: [how does a customer move to a higher tier or add a stream?]
```

**Solopreneur billing tool recommendations:**
- **Stripe** — most powerful, best developer experience, industry standard
- **Paddle** — handles tax/VAT globally, good for digital products sold internationally
- **Lemon Squeezy** — simpler than Stripe, good for digital products, handles EU VAT
- **Gumroad** — simplest for one-time digital product sales

---

## Step 5: Model Your Revenue Projections

For each stream, build a simple projection:

```
STREAM: [name]
CUSTOMERS MONTH 1: [number]
MONTHLY GROWTH RATE: [%]
AVERAGE REVENUE PER CUSTOMER: [$/month]
CHURN RATE: [%/month] (for recurring streams)

MONTH 1 REVENUE: customers × ARPC
MONTH 3 REVENUE: [calculate with growth and churn]
MONTH 6 REVENUE: [calculate]
MONTH 12 REVENUE: [calculate]
```

**Churn math for recurring models:** If you have 100 customers and 5% churn, you lose 5/month. To grow, your new customer acquisition must exceed your churn. This is why retention matters as much as acquisition.

**Sanity check:** Sum all streams. Does total projected revenue cover your costs and provide a livable income within 12 months? If not, either the projections are wrong (re-examine growth assumptions) or the model needs rethinking.

---

## Step 6: Validate Before Building

Before investing heavily in building out a revenue model, validate the core assumption:

**"Will customers actually pay this way?"**

Test methods:
- **Pre-sales:** Offer the product at a discounted "founding member" price before it's built. If people pay, the model works.
- **Fake checkout:** Build a landing page with a real checkout button. When someone clicks, show a "coming soon" page and capture their email. Measure how many click the buy button.
- **Manual first version:** Deliver the product manually (by hand) at the planned price to 5-10 customers. If they pay and come back, the model is validated.

---

## Revenue Model Mistakes to Avoid
- Choosing a model because it sounds impressive, not because it fits your product and customers.
- Ignoring churn when projecting subscription revenue. Churn compounds painfully.
- Building a marketplace model as a solopreneur. Two-sided markets require significant scale to work. Start with a one-sided model first.
- Never testing alternative models. If subscription isn't working, try one-time + upgrade. Revenue models are experiments.
- Stacking too many streams too early. Master one stream first, then layer in a second once the first is stable.
