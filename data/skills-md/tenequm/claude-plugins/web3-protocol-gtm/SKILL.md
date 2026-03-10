---
name: web3-protocol-gtm
description: Go-to-market strategy for web3 builders - protocols, products, services, and solo founders. Use when planning growth for a crypto protocol, product, or service, building developer community, crafting CT narrative, planning ecosystem partnerships, preparing grant applications, measuring protocol traction, sequencing testnet to mainnet launch, launching tokens, pricing crypto-native products, optimizing landing page conversion, selling to AI agents, or growing as a solo founder in web3. Covers community-led growth, Crypto Twitter strategy, developer relations, hackathon playbooks, ecosystem composability, standards adoption, protocol metrics, solo founder GTM, token launch tactics, CT growth for small accounts, dual-rail payments, micropayment pricing, embedded wallet UX, and agent-as-customer models. Triggers on web3 GTM, protocol marketing, crypto growth, developer relations, community building, CT narrative, ecosystem partnerships, standards adoption, protocol launch, grant application, hackathon strategy, solo founder, token launch, pump.fun, building in public, CT growth, reply strategy, crypto SaaS, product launch, micropayment pricing, landing page conversion, x402 pricing, agent customers.
metadata:
  version: "0.2.0"
---

# Web3 Protocol GTM

Go-to-market playbook for web3 builders - infrastructure protocols, products, and solo founders. Built for the February 2026 landscape.

Web3 GTM is not B2B SaaS marketing. No MQLs, no SDRs, no enterprise sales cycles, no gated whitepapers. Growth comes from composability, developer adoption, CT narrative, and community. This skill provides actionable frameworks for builders at every stage - from solo hackers launching at a hackathon to protocol teams pursuing ecosystem-wide adoption.

## When to Use

- Planning go-to-market for a web3 protocol, product, or hackathon project
- Building developer community around an SDK or protocol
- Crafting Crypto Twitter narrative and growing a small founder account
- Evaluating ecosystem partnership opportunities
- Preparing grant applications (Solana Foundation, Superteam, ecosystem grants)
- Planning hackathon participation, bounty strategy, or hackathon-to-fund pipeline
- Defining protocol metrics and KPIs
- Sequencing testnet, mainnet, and token launch
- Launching tokens (Pump.fun, Bags.fm, Believe, Moonshot, etc.)
- Solo founder GTM - prioritizing channels, time allocation, AI-assisted workflows
- Standards adoption strategy (getting other protocols to implement your spec)
- Positioning against competitors in the CT narrative

---

## Web3 GTM Principles

**1. Product IS the GTM**

Code quality, uptime, gas efficiency, composability - these are your marketing. Hyperliquid grew to $40B valuation and $550M annualized revenue with zero VC backing and zero marketing spend - they airdropped 31% of supply after proving product-market fit. Jupiter became Solana's default DEX aggregator through execution speed and routing quality, not ads. Your SDK's developer experience is your best growth lever.

**2. Signal Over Size**

50 engaged developers building on your protocol are worth more than 5,000 Discord members from a giveaway campaign. Quality signals: GitHub stars from real developer accounts, repeat contributors, organic testimonials on CT, teams that ship integrations without being asked.

**3. Composability IS the Partnership Strategy**

Every protocol that integrates yours becomes your distribution channel. Make integration trivially easy (one SDK call, clear docs, working examples). Your integration surface area equals your total addressable market. Morpho grew fee share from 0% to 10% of the lending sector by composing on top of Aave. Meteora went from zero to #1 by fees on Solana by being composable with the broader DeFi stack.

**4. Narrative Before Revenue**

In web3, mindshare precedes market share. The protocol that owns the narrative ("the identity layer for AI agents") wins integrations before the one with marginally better tech. Positioning is everything - define your category before competitors define it for you.

**5. Product vs Protocol - Know Your Motion**

If you're building infrastructure for developers to compose on, this entire skill applies directly. If you're selling a hosted service or product directly to end users (paid in crypto), the principles above still apply but your distribution, pricing, and metrics are fundamentally different. See `references/crypto-native-product-gtm.md` for adapted frameworks: dual-rail payments, embedded wallet UX, micropayment pricing psychology, landing page conversion, agent-as-customer models.

**6. Revenue Is the North Star**

The industry has moved from TVL to revenue as the primary success metric. In 2025, 1,124 protocols achieved profitability, 71 exceeded $100M in on-chain ARR, and value distributed to token holders hit all-time highs for three consecutive quarters (1kx 2025 Onchain Revenue Report). Track: protocol revenue, integrations shipped, developer activity (GitHub commits/contributors), active wallets, transaction volume. Ignore: TVL (easily gamed through recursive loops), Discord member count, Twitter followers (without engagement), "partnerships signed" (only count shipped integrations).

---

## Quick Start: 90-Day GTM Sprint

### Phase 1: Foundation (Days 1-30)

```
Week 1-2: Positioning + Docs
- [ ] Define ICP using web3 ICP framework (see below)
- [ ] Write positioning statement (one sentence, "X for Y" format)
- [ ] Audit docs for AI-readability (structured markdown, working code blocks)
- [ ] Create "getting started in 5 minutes" tutorial
- [ ] Set up founder CT account (or audit existing one)

Week 3-4: First Outreach
- [ ] Identify 10 potential first integrators
- [ ] Send 5 partnership outreach messages
- [ ] Submit to 2 grant programs (Solana Foundation, Superteam)
- [ ] Post 3x/week on CT (insights, building updates, ecosystem commentary)
- [ ] Join 3 relevant developer communities (Discord/TG)
```

### Phase 2: Traction (Days 31-60)

```
Week 5-6: Integrations + Content
- [ ] Ship first integration with a complementary protocol
- [ ] Publish 2 technical deep-dive threads on CT
- [ ] Host or join 1 developer workshop
- [ ] Get 1 notable CT account to try your protocol organically

Week 7-8: Hackathons + Proof
- [ ] Enter or sponsor 1 hackathon with a bounty using your protocol
- [ ] Publish metrics dashboard (even if numbers are small)
- [ ] Second integration shipped or in progress
- [ ] Start tracking weekly metrics (see Metrics Framework)
```

### Phase 3: Amplification (Days 61-90)

```
Week 9-10: Case Studies + Partnerships
- [ ] Write case study from first 2-3 integrators
- [ ] Submit grant milestone report
- [ ] Co-announce partnerships (joint CT threads)
- [ ] Identify next 10 integration targets

Week 11-12: Evaluate + Plan
- [ ] Do you have 3+ teams building on your protocol? (early PMF signal)
- [ ] Is developer activity growing week-over-week?
- [ ] Plan next quarter based on what worked
- [ ] Kill what did not work (be ruthless)
```

---

## Web3 ICP Framework

SaaS ICP uses firmographics (employee count, revenue, industry). Web3 ICP uses builder profiles.

### Three Questions

1. **What are they building?** (Agent marketplace, DeFi protocol, payment system, data indexer)
2. **What primitives do they need?** (Identity, reputation, payments, storage, compute, oracles)
3. **Where do they live?** (CT, GitHub, Discord, Telegram, hackathons, ecosystem DAOs)

### Builder Persona Template

```
Protocol: [your protocol name]

Target Builder Profile:
  Building: [category]
  Needs: [primitive you provide]
  Current solution: [what they use now - or "nothing"]
  Pain: [specific gap your protocol fills]
  Where they are: [channels]
  Integration effort: [e.g., "npm install + 3 SDK calls"]
  Decision maker: [individual dev, team lead, DAO vote]
```

### User Persona Template (for products/services)

```
Product: [name]
Target User: [who] doing [what task]
Current solution: [what they use now / nothing]
Pain: [friction you eliminate]
Crypto comfort: [holds crypto / curious / needs fiat option]
Where: [channels]
Price sensitivity: [impulse <$10 / considered $10-50 / enterprise $50+]
Conversion path: [email signup / wallet connect / direct payment]
```

For full ICP framework with examples, see `references/icp-positioning.md`.

---

## CT Narrative Playbook

Crypto Twitter remains the primary narrative channel for web3 protocols, but the landscape shifted hard in January 2026. X cracked down on paid crypto promotion - post-to-earn farms are dead, bot-boosted engagement is dying, and undisclosed shilling is radioactive. This makes organic, founder-led content the only credible approach.

### Founder-Led Narrative

Founder accounts outperform brand accounts 5-10x on engagement. Post as yourself, not "the protocol." Post-crackdown, this is no longer optional - it's the only approach that works.

**Content mix:** 60% thinking/insights, 25% building in public, 15% ecosystem commentary.

### Weekly Content Calendar

```
Monday:    Technical insight or problem you solved
Tuesday:   Ecosystem commentary (react to relevant news)
Wednesday: Building in public (screenshot, metric, milestone)
Thursday:  Thread: deep dive on your problem space (not your product)
Friday:    Community highlight (who is building on you, what they shipped)
```

### Thread Templates

**"The Problem" Thread:**
```
Hook: "[Thing everyone assumes works] is broken. Here's why."
Body: 3-5 tweets explaining the problem with data/examples
Turn: "We built [protocol] to fix this. Here's how."
Proof: Architecture decision, benchmark, or user quote
CTA: "Try it: [link to quickstart]"
```

**"How We Built X" Thread:**
```
Hook: "We shipped [feature] this week. The hardest part was [X]."
Body: Technical decisions, trade-offs, what you tried and discarded
Lesson: What you learned that others can apply
CTA: "Full docs: [link]"
```

### KOL Strategy (Post-January 2026 Crackdown)

The January 2026 X crackdown on paid crypto promotion changed the rules. Undisclosed paid shilling is now actively penalized. The old playbook of paying 5-figure checks for "this project is amazing" posts is a guaranteed way to damage your reputation.

- Audience-product fit matters more than follower count
- 10K genuine followers in your niche outperform 100K generic crypto audience
- Never pay for "this project is cool" posts - get them to actually use your protocol
- Target: protocol-specific KOLs (agent builders, infra devs, Solana contributors)
- Test with 1 KOL first ($3-5K), track qualified signups, validate before scaling
- All paid promotions must be disclosed - undisclosed shilling is "radioactive" post-crackdown
- Shift from per-post paid deals to long-term ambassador relationships (ongoing, not transactional)

For full CT playbook and KOL evaluation framework, see `references/community-ct-playbook.md`.

---

## Developer Relations

For infrastructure protocols, DevRel IS the growth engine. Traditional DevRel is also your biggest bottleneck - 5 DevRel people serving 5,000 developers means each developer gets 5 minutes of attention per month (DoraHacks, Feb 2026).

### The DevRel Hierarchy

```
1. Docs         - AI-readable, working examples, 5-min quickstart
2. SDK          - One npm install, typed, minimal config
3. Examples     - Working reference implementations
4. Support      - Fast response in dev channels (<30 min during business hours)
5. Content      - Technical threads, tutorials, architecture posts
6. AI Agents    - Agentic DevRel: AI force-multipliers for human DevRel
```

Invest in this order. Great docs with no DevRel headcount beats a DevRel team with broken docs.

### Agentic DevRel

One DevRel person augmented by AI agents can do what used to require a team of twenty. Use agents for:

- **Proactive tracking**: Monitor GitHub commits, follow up on inactive builders automatically
- **Smart triage**: Flag high-potential builders for human follow-up
- **24/7 support**: Instant answers in all languages, escalate edge cases to humans
- **Data-driven insights**: Which builders are stuck, which are about to churn, which deserve attention
- **Personalized outreach**: Context-aware messages based on what each builder is actually building

Hackathons are the acquisition engine. Agentic DevRel is the retention engine.

### Docs Quality Checklist

```
- [ ] AI-readable (structured headings, code blocks, no images-as-docs)
- [ ] 5-minute quickstart that actually works (copy-paste, run, see result)
- [ ] Code examples with real values (not <PLACEHOLDER>)
- [ ] Error handling examples (not just happy path)
- [ ] API reference with types and return values
- [ ] Changelog maintained
- [ ] llms.txt or equivalent for AI tool discovery
```

### Hackathon Strategy

Hackathons are the #1 developer pipeline. Colosseum's Solana hackathons have produced 50+ venture-backed startups, with alumni raising $700M+ in cumulative funding. Notable graduates: Tensor, Drift, Jito, Marinade, Squads, STEPN. 1inch went from ETHGlobal NYC 2019 to unicorn status in 18 months.

**The hackathon-to-fund pipeline is now formalized:** Colosseum hackathon -> Eternal program -> Accelerator ($250K pre-seed, 0.67% acceptance rate). Alliance runs MVP Tournaments feeding directly into their accelerator ($500K funding).

```
Pre-hackathon (2 weeks before):
- [ ] Create bounty: "$X for best project using [your protocol]"
- [ ] Run a 30-min workshop showing integration in real-time
- [ ] Prepare "hackathon quickstart" docs (stripped-down, copy-paste ready)
- [ ] Create boilerplate repo teams can fork (working example with your SDK)
- [ ] Ensure your SDK works well with AI coding tools (Cursor, Claude Code)

During:
- [ ] Staff engineers at the event (instant unblocking is highest-ROI activity)
- [ ] Response time target: < 30 minutes for technical questions
- [ ] Run office hours (2x during hackathon)
- [ ] Engage with every team building on your protocol

Post-hackathon:
- [ ] Follow up within 48 hours (the conversion window closes fast)
- [ ] Offer to help teams ship to mainnet
- [ ] Feature their projects on your CT and docs
- [ ] Track: hackathon teams that become ongoing integrators
- [ ] Only ~15% of winning projects continue development - your follow-up determines if yours are in that 15%
```

**Sponsor bounty structure that works:**
- Pool prizes ($100-500 per qualifying project) for maximum adoption
- Track prizes ($5K-15K for top 3) for quality
- Follow-on grants ($30K+) to keep winning teams building
- Blockscout at ETHGlobal Prague: pool prizes got 37% of all projects to integrate

For full DevRel playbook, see `references/developer-relations.md`.

---

## Ecosystem Partnerships

### Outreach Template

```
Subject: [Your Protocol] + [Their Protocol] integration

[Name],

I'm building [protocol] - [one-line description].

Your [product] needs [primitive you provide] to [specific benefit].
Integration is [X lines of code / one SDK call].

I built a working demo: [link or screenshot].

Want to see it?

[Your name]
```

### Standards Adoption

Standards get adopted through working code, not spec documents.

```
1. Ship reference implementation (nobody adopts a spec without running code)
2. Get 3-5 high-profile early adopters building on your standard
3. Make forking/implementing trivially easy (MIT license, clear docs)
4. Show up consistently to working groups and governance discussions
5. Write educational content on WHY the standard exists (the problem it solves)
```

For full partnership and standards playbook, see `references/ecosystem-partnerships.md`.

---

## Metrics Framework

### Protocol Health Metrics

| Metric | What It Measures | Good Signal (first 90 days) |
|--------|------------------|----------------------------|
| Protocol revenue | Sustainability | Any revenue > $0 (nearly 400 protocols hit $1M+ ARR in 2025) |
| Integrations shipped | Protocol adoption | 3+ live integrations |
| GitHub contributors | Developer interest | Growing monthly (full-time crypto devs rose 5% YoY) |
| Active wallets | Real usage | Consistent, not spike-driven (273M monthly active wallets in H1 2025) |
| Transaction volume | Core usage | Week-over-week growth |
| Paying users | Product conversion | Any > 0, growing weekly (product GTM) |
| Conversion rate | Landing page / onboarding | 5-10% good, 15%+ with embedded wallets |
| Churn rate | Product stickiness | <10% monthly (crypto products avg 30-50%) |
| Agent API calls | Machine customer adoption | Growing, x402-discoverable (product GTM) |
| SDK downloads | Developer reach | npm weekly downloads trending up |
| Fee-to-valuation ratio | Market efficiency | DeFi median 17x (Artemis standard) |
| Value to token holders | Real yield | Buybacks + burns + staking net of emissions |

### Vanity Metrics to Ignore

- **TVL** (the biggest lie in crypto - easily gamed through recursive loops; a user deposits $100 ETH, borrows $80, redeposits = $180 TVL from $100 real capital)
- Total Discord members (easily gamed with bots)
- Twitter follower count (meaningless without engagement)
- "Partnerships signed" (only shipped integrations count)
- Waitlist signups (without conversion tracking)
- Kaito mindshare score (gameable, disrupted by X crackdown)

### Weekly Tracking Template

```
Week | Integrations | GitHub Stars | npm Downloads | Active Wallets | Revenue
  1  |      0       |     12       |      45       |       0        |   $0
  2  |      0       |     18       |      89       |       3        |   $0
  3  |      1       |     25       |     156       |      12        |   $0
  4  |      1       |     31       |     234       |      28        |  $12
```

For full metrics instrumentation and dashboard guide, see `references/metrics-launch.md`.

---

## Launch Sequencing

Web3 launches are not one event - they are a sequence.

```
Devnet/Testnet (Month 1-3)
  - Internal testing, security review
  - First 3-5 alpha testers (hand-picked builders)
  - Bug bounty (even small: $500-$5K range)
  - Docs and SDK stabilized

Mainnet Beta (Month 4-6)
  - Audited code deployed
  - First integrations go live
  - Public docs + SDK published
  - Grant milestone report submitted
  - CT announcement (understated - show metrics, not hype)

Mainnet GA (Month 6-9)
  - 5+ integrations live
  - Public metrics dashboard
  - Standards body submission (if applicable)
  - Ecosystem partnership co-announcements

Token (Month 12+, only if needed)
  - Only after proven utility and real usage
  - Only if tokenomics serve protocol function (governance, staking, fees)
  - Anti-sybil measures from day 1
  - Legal review completed
  - Never use token launch to generate interest in a product without PMF
```

### Grant Application Checklist

```
- [ ] Clear problem statement (one paragraph, no jargon)
- [ ] Working code (testnet deployment at minimum)
- [ ] Milestone-based budget (not lump sum request)
- [ ] Team credentials (GitHub profiles, past shipped work)
- [ ] Ecosystem benefit (why this helps the ecosystem broadly)
- [ ] Measurable success criteria per milestone
- [ ] Realistic timeline (grants reviewers reject optimistic timelines)
- [ ] Hackathon results if applicable (strong signal for reviewers)
```

**Major Grant Programs (2026):**
- Solana Foundation ($100M+ distributed, 500+ projects)
- Colosseum Accelerator ($250K pre-seed for hackathon graduates)
- Optimism Retro Funding (continuous algorithm-driven rewards, Season 7-8)
- Arbitrum ($10M audit program, ArbiFuel gas sponsorship, Gaming Catalyst)
- Alliance DAO ($500K funding, $3.5M median post-program raise)
- Gitcoin Grants ($60M+ distributed to date)

For full launch timeline and grant application guide, see `references/metrics-launch.md`.

---

## Solo Founder GTM

Solo-founded startups are 36.3% of all startups (2025), but 80.9% make less than $500 MRR. The difference between the surviving 5-13% is GTM execution from day one.

### Time Allocation: 50/25/25

- **50%** Product/Engineering
- **25%** Distribution/Marketing (CT, hackathons, partnerships, content)
- **25%** Everything else (community, support, ops, learning)

### AI-Augmented Solo Founder ($210-385/month)

Claude Code ($150-300) + Cursor ($20) + v0 ($20) + Claude.ai ($20) + n8n (free). Automate: content drafts, code shipping, dev support triage. Keep human: CT engagement, relationship DMs, strategic decisions, community vibe (first 100 members).

### First 100 Users

1. **Weeks 1-4:** Map 20-30 CT accounts, engage genuinely, join 3-5 Telegram groups
2. **Weeks 5-6:** Launch via CT + Telegram + hackathon communities + Reddit
3. **Weeks 6-12:** Personally onboard every user, ask for 1 referral each, create case studies

**What to skip:** Multi-channel marketing (pick CT for 90 days), paid ads ($2K = 15 signups), Discord (use TG initially), pitch decks (build traction first).

For full playbook, see `references/solo-founder-playbook.md`.

---

## Token Launch

### When to Launch

Only after: real users (even 50-100), token serves a protocol function, you can dedicate 72+ hours post-launch, and you have reviewed jurisdiction-specific legal requirements. If your product works without a token, seriously consider not launching one.

### The 72-Hour Rule

Tokens either graduate and gain traction within 72 hours or fade permanently. 97% of meme coins fail within 60 days. 60% are dead within 24 hours.

### Launchpad Selection (Solana, February 2026)

| Platform | Market Share | Best For |
|----------|-------------|----------|
| Pump.fun | 51.2% | Maximum exposure (1.15% graduation rate) |
| Bags.fm | 33.5% | Creator revenue (1% of all volume forever) |
| Believe | Growing | Leveraging X/Twitter following |
| Moonshot | Niche | Higher quality signal (500 SOL threshold) |

### The 30-Minute Window

Post-graduation on PumpSwap, you have 30 minutes before the token lives or dies. Add your own LP at minute 0-5. Ensure visible trading activity by minute 5-15. Be active on all channels by minute 15-30. Lock LP tokens for 6-12+ months. Revoke mint and freeze authority immediately.

### Hackathon + Token Timing

Build the product during the hackathon. Launch the token AFTER - ideally after validation (winning, accelerator acceptance, early users). Splitting focus between product quality and token management during a hackathon guarantees mediocrity at both.

For full mechanics, survival checklist, and launchpad comparison, see `references/token-launch-playbook.md`.

---

## Anti-Patterns

| Mistake | Why It Fails |
|---------|-------------|
| Marketing before product | No CT presence fixes broken code |
| Paid KOLs before PMF | Post-Jan 2026 crackdown, undisclosed shilling is actively penalized |
| Token launch as GTM | Attracts speculators, not builders |
| Enterprise sales motions | Web3 is bottom-up; developers choose tools, not procurement |
| Ignoring composability | Lose to the protocol that is easy to integrate |
| Airdrop farming incentives | 85% of value captured by sybils |
| Single-platform dependency | One algorithm change wipes out traction; diversify |
| Optimizing for TVL | Easily gamed; revenue is the metric that matters |
| Splitting hackathon + token launch | Guarantees mediocrity at both |

---

## Reference Documentation

**Deep-Dive Guides:**
- `references/solo-founder-playbook.md` - Time allocation, AI stack, first 100 users, leverage ranking, burnout prevention
- `references/token-launch-playbook.md` - Launchpad mechanics, 30-min window, sniper defense, failure modes, survival checklist
- `references/community-ct-playbook.md` - CT strategy, X algorithm weights, small account growth, thread frameworks, KOL evaluation
- `references/developer-relations.md` - DevRel stack, AI-readable docs, SDK design, hackathon playbook, developer funnel
- `references/ecosystem-partnerships.md` - Partnership evaluation, outreach sequences, standards adoption, composability strategy
- `references/icp-positioning.md` - Full ICP framework, April Dunford positioning for protocols, competitive mapping
- `references/crypto-native-product-gtm.md` - Dual-rail payments, embedded wallet UX, micropayment pricing, landing page conversion, agent customers, token timing for products
- `references/metrics-launch.md` - Protocol metrics instrumentation, public dashboard, launch checklists, grant applications

**External Resources:**
- Solana Foundation Grants: https://solana.org/grants
- Superteam: https://earn.superteam.fun
- Colosseum: https://www.colosseum.org
- Alliance DAO: https://alliance.xyz
- ETHGlobal: https://ethglobal.com
- Optimism Retro Funding: https://retrofunding.optimism.io
- Electric Capital Developer Report: https://developerreport.com
- 1kx Onchain Revenue Report: https://1kx.network
