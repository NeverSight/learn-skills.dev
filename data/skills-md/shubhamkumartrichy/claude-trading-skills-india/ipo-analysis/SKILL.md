---
name: ipo-analysis
description: |
  Evaluate Indian IPOs (mainboard and SME): reading the RHP, price band and lot size, issue structure
  (fresh issue vs OFS), category quotas (QIB, NII sHNI/bHNI, retail, employee, shareholder), anchor
  book, subscription data interpretation, allotment odds, grey market premium caveats, valuation vs
  listed peers, T+3 timeline, UPI mandate, listing-day pre-open and post-listing lock-in expiries.

  Use when the user asks: "should I apply for X IPO", "IPO review", "GMP of X", "subscription status",
  "chances of allotment", "SME IPO", "listing gain or long term", "when does X list", or "anchor
  lock-in expiry".
---

# IPO Analysis (India)

Indian IPO frenzies are driven by listing-gain expectations. Separate the **listing trade**
(sentiment: subscription, market mood) from the **investment case** (business quality, valuation).

## Timeline (T = issue close)

| Day | Event |
|---|---|
| T−1 | Anchor allocation announced (names and amounts) |
| T−3 … T | Bidding (usually 3 working days), UPI mandate must be approved by the cut-off |
| T+1 | Basis of allotment (check on the registrar's site or the exchange) |
| T+2 | Shares credited to demat; unallotted funds unblocked |
| T+3 | **Listing.** Special pre-open 09:00–10:00, trading from 10:00 |

## Issue structure checklist (from the RHP)

- **Fresh issue vs OFS.** Fresh issue money goes to the company (capex, debt repayment). OFS money goes
  to selling shareholders. A large OFS by promoters or PE investors at a high valuation is a caution.
- **Use of proceeds.** Growth capex or debt reduction is better than "general corporate purposes".
- **Price band, lot size, minimum application.** SEBI sets the mainboard minimum application at
  ₹10,000–15,000.
  Retail maximum is ₹2 lakh, sHNI ₹2–10 lakh, bHNI above ₹10 lakh.
- **Quotas (book-built mainboard):** QIB ~50% (anchors up to 60% of it), NII ~15% (one-third sHNI,
  two-thirds bHNI), retail ~35%. There may also be employee and parent-shareholder quotas, often with a
  discount.
- **Financials:** 3-year revenue and profit trend, margins, ROCE, debt, cash flow, and contingent
  liabilities. Note any restatements and pre-IPO "window dressing" (a sudden profit jump in the last year).
- **Valuation:** P/E and EV/EBITDA on post-issue shares vs listed peers in the RHP's peer table.
  Pricing above the best listed peer needs a clear growth or quality reason.
- **Pre-IPO placements:** a recent placement price far below the IPO price suggests aggressive pricing.
- **Risk factors section:** litigation, customer concentration, regulatory dependence.

## Reading subscription data

| Signal | Reading |
|---|---|
| QIB subscription high (>50×) | Institutions see value. The single most informative number |
| NII very high, QIB modest | Leveraged HNI money chasing listing gains (fragile) |
| Retail high, QIB weak | Retail euphoria. Poor listing odds historically |
| Final-day surge | Normal. Most institutional bids come on the last day |
| Quality anchors (long-only MFs, sovereign funds) | Positive. Watch the anchor lock-in expiries |

## Allotment odds (retail and sHNI use a lottery)

Each successful retail applicant gets **one minimum lot**. Approximate odds:

```
Retail lots available = (retail quota shares) ÷ (lot size)
P(allotment) ≈ retail lots available ÷ number of retail applications      (cap at 100%)
```
With 50× retail subscription, odds are often only 2–5%. Applying with more lots does not improve retail
odds. Separate applications from family members' own PANs do. sHNI also uses a lottery for the
minimum sHNI size.

## Grey market premium (GMP)

GMP is an unofficial, unregulated off-market quote. It is easily manipulated, it swings daily, and it
often collapses near listing. Mention it only as sentiment colour, never as a basis for decisions, and
say it is unofficial.

## SME IPOs (NSE Emerge, BSE SME)

High risk: tiny free float, large minimum applications (₹2 lakh-plus), thin post-listing liquidity
(trade-for-trade, large lots), and a history of operator activity. SEBI tightened SME IPO rules in 2025
(eligibility, OFS limits and listing-day controls). Treat SME IPOs as speculative and size them as such.

## After listing

- **Listing day:** price discovery happens in the 09:00–10:00 call auction. Mainboard IPOs list in the
  normal segment; SME IPOs are on the SME platform.
- **Lock-in expiries** bring supply: anchors 50% after 30 days and 50% after 90 days, pre-IPO
  shareholders after 6 months, and promoters' minimum contribution after 18 months (3 years in some
  cases). These dates are known in advance. Traders watch them for supply pressure.
- Many hyped IPOs trade below the listing price within 6–12 months. Evaluate as a normal stock
  (`fundamental-screening`, `technical-analysis`) once 2–3 months of price history exist.

## Output

```markdown
# [Company] IPO — [dates], price band ₹a–b, lot n (₹ min)
Issue: ₹x cr (fresh ₹y / OFS ₹z) | Post-issue m-cap ₹.. cr | P/E .. vs peers ..
Business & financials: …
Subscription (as of [time]): QIB ..× | NII ..× | Retail ..× | Total ..×
Allotment odds (retail): ~..%
Listing view: [strong/moderate/weak] — why | Long-term view: [apply/avoid/wait for listing]
Key risks: … | Lock-in dates: 30d [date], 90d [date]
(GMP if mentioned: unofficial, unreliable.)
```
