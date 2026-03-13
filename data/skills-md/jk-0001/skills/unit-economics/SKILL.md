---
name: unit-economics
description: Calculate, understand, and improve the unit economics of a solopreneur business. Use when figuring out if the business is actually profitable per customer, when CAC or LTV numbers are needed, when evaluating whether a pricing or acquisition strategy is sustainable, or when making data-driven decisions about marketing spend and pricing. Covers CAC, LTV, payback period, contribution margin, and the feedback loops between them. Trigger on "unit economics", "CAC", "customer acquisition cost", "LTV", "lifetime value", "payback period", "is my business profitable", "contribution margin", "am I making money per customer", "should I spend more on marketing".
---

# Unit Economics

## Overview
Unit economics answer one question: does the business make money per customer? Everything else in business — marketing spend, pricing, growth targets — should be informed by this answer. For solopreneurs, unit economics are especially critical because there's no VC money to burn through while you figure it out. This playbook teaches you how to calculate, interpret, and improve your numbers.

---

## The Three Core Metrics

Every unit economics conversation starts with these three numbers. Calculate all of them before making any marketing or pricing decisions.

### 1. CAC — Customer Acquisition Cost
**What it is:** The total amount you spend to acquire one new customer.

**Formula:**
```
CAC = Total Marketing & Sales Spend / Number of New Customers Acquired
```

**What counts as "marketing & sales spend":**
- Ad spend (Google, Facebook, LinkedIn, etc.)
- Content creation costs (freelance writers, designers, tools)
- Your own TIME spent on marketing and sales (value it at your hourly rate)
- Conference or event costs
- Outreach tool subscriptions
- Any other cost directly tied to acquiring customers

**What does NOT count:**
- Product development costs
- Hosting / infrastructure
- Customer support
- General business overhead

**Calculate it monthly.** CAC changes as your channels mature and your brand grows.

**Example:**
```
Ad spend:                  $400
Content tool costs:        $50
Your time (10 hrs × $75):  $750
New customers acquired:    25

CAC = $1,200 / 25 = $48 per customer
```

### 2. LTV — Customer Lifetime Value
**What it is:** The total revenue you expect to earn from one customer over the entire time they stay with you.

**Formula:**
```
LTV = ARPC × Average Customer Lifespan (in months)
```
Where ARPC = Average Revenue Per Customer per month.

**How to calculate average lifespan:**
- If you have churn data: Lifespan = 1 / Monthly Churn Rate. Example: 5% churn/month → average lifespan = 1/0.05 = 20 months.
- If you're pre-churn (just launched): Estimate conservatively. Use 6 months as a starting assumption for SaaS. Adjust as real data comes in.

**Example:**
```
ARPC: $29/month
Monthly churn rate: 4%
Average lifespan: 1 / 0.04 = 25 months

LTV = $29 × 25 = $725 per customer
```

### 3. Payback Period
**What it is:** How many months it takes for a customer to "pay back" what it cost to acquire them.

**Formula:**
```
Payback Period = CAC / ARPC (monthly revenue per customer)
```

**Example:**
```
CAC: $48
ARPC: $29/month

Payback Period = $48 / $29 = 1.7 months
```

---

## Step 1: Calculate Your Numbers

Fill in this template with real data (or best estimates if you're early):

```
UNIT ECONOMICS SNAPSHOT
========================

REVENUE
  Monthly ARPC:                   $________
  Annual ARPC:                    $________

ACQUISITION
  Monthly marketing spend:        $________
  New customers this month:       ________
  CAC:                            $________ (spend ÷ customers)

RETENTION
  Monthly churn rate:             ________% (customers lost ÷ customers at start of month)
  Avg customer lifespan:          ________ months (1 ÷ churn rate)

KEY RATIOS
  LTV:                            $________ (ARPC × lifespan)
  LTV:CAC ratio:                  ________x (LTV ÷ CAC)
  Payback period:                 ________ months (CAC ÷ ARPC)
```

---

## Step 2: Interpret Your Numbers

These are the benchmarks. Compare your numbers against them:

| Metric | Healthy | Concerning | Critical |
|---|---|---|---|
| **LTV:CAC ratio** | > 3x | 1.5x – 3x | < 1.5x |
| **Payback period** | < 12 months | 12-24 months | > 24 months |
| **Monthly churn** | < 5% | 5-10% | > 10% |
| **CAC trend** | Stable or decreasing | Slowly increasing | Rapidly increasing |

**LTV:CAC ratio is the single most important number.** If it's below 1x, you are losing money on every customer. If it's below 3x, the business is technically viable but fragile — one bad month can erase your margin.

---

## Step 3: The Four Levers

If your unit economics are unhealthy, you have exactly four levers to pull. Pull them in this order of priority (top = highest impact, least effort):

### Lever 1: Reduce Churn (Increases LTV)
Churn has a compounding effect on LTV. Reducing churn from 10% to 5% doubles your average customer lifespan and therefore doubles LTV.

**How to reduce churn:**
- Identify WHY customers cancel (exit survey, usage data, support tickets).
- Improve onboarding — most churn happens in the first 30 days because customers never got value.
- Increase product stickiness — make the product part of their daily workflow so leaving feels costly.
- Proactively reach out to at-risk customers (low usage = danger signal) before they cancel.

### Lever 2: Increase ARPC (Increases LTV and Revenue)
More revenue per customer = higher LTV without acquiring more customers.

**How to increase ARPC:**
- Raise prices (if LTV:CAC supports it — see pricing-strategy skill).
- Upsell or cross-sell: offer upgrades, add-ons, or complementary products to existing customers.
- Add a premium tier that a % of customers migrate to.

### Lever 3: Reduce CAC (Improves LTV:CAC ratio)
Spending less to acquire each customer is the most direct path to healthy unit economics.

**How to reduce CAC:**
- Improve conversion rates at every stage of your funnel (better landing page copy, better onboarding flow).
- Double down on your lowest-CAC channel and cut or reduce spend on high-CAC channels.
- Invest in word-of-mouth and referral programs (these have near-zero marginal CAC at scale).
- Improve content quality so organic/SEO channels drive more traffic without paid spend.

### Lever 4: Increase New Customer Volume (Amortizes Fixed Costs)
If you have fixed marketing costs (team, tools, content infrastructure), acquiring more customers spreads those costs across a larger base, reducing effective CAC.

---

## Step 4: Build a Monthly Unit Economics Dashboard

Track these numbers every month in a simple table:

```
MONTH | New Customers | CAC | ARPC | Churn% | LTV | LTV:CAC | Payback
------|---------------|-----|------|--------|-----|---------|--------
Jan   |               |     |      |        |     |         |
Feb   |               |     |      |        |     |         |
Mar   |               |     |      |        |     |         |
...
```

**Trends matter more than snapshots.** A single bad month is noise. Three bad months in a row is a signal. Watch the direction of each metric, not just the current value.

---

## Step 5: Unit Economics for Non-Subscription Businesses

If your business is project-based, one-time product sales, or service-based, the formulas shift slightly:

**Project / Service business:**
```
CAC = same formula (marketing spend ÷ new clients)
Revenue per client = average project value (not monthly)
LTV = average project value × average number of projects per client over their lifetime
Payback period = CAC ÷ average project value
```

**One-time product sales:**
```
CAC = same
LTV = average order value × average number of purchases per customer lifetime
      (For truly one-time products, LTV = average order value. Unit economics 
       must work on a single transaction.)
```

**Rule for one-time products:** If CAC > average order value, you are losing money on every sale. Either raise the price, reduce CAC, or add a recurring revenue component (updates, community access, premium tier).

---

## Unit Economics Mistakes to Avoid
- Forgetting to include your own time in CAC. If you spend 20 hours/month on marketing, that's a real cost even if you don't pay yourself for it.
- Using optimistic churn estimates when you have no data. Be conservative. Assume higher churn until real data proves otherwise.
- Optimizing CAC while ignoring churn. A cheap customer who leaves in 2 months is worth less than an expensive customer who stays for 2 years.
- Only calculating unit economics once. These numbers change monthly. Track them religiously.
- Ignoring unit economics because you're "early stage." Early is exactly when you should understand these numbers — before you scale a broken model.
