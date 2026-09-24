---
name: ip-strategy
description: >
  Intellectual property structuring, migration, valuation, and licensing for
  tax-efficient IP management. USE THIS SKILL when the user asks about IP
  holding structures, IP licensing, IP migration, IP valuation for tax
  purposes, technology transfer, cost sharing arrangements, cost contribution
  arrangements, DEMPE analysis, royalty rate benchmarking, IP box eligibility,
  IP in M&A, IP carve-outs, defensive IP strategy, freedom to operate, or
  substance requirements for IP holding entities. Covers patents, trademarks,
  trade secrets, copyrights, know-how, and data assets.
---

# IP Strategy

## Required Inputs

- **IP Portfolio Inventory**: List of IP assets (patents, trademarks, trade secrets, copyrights, know-how, software, data assets) with registration details and current ownership.
- **Group Structure**: Entities, jurisdictions, and ownership chain.
- **DEMPE Functions**: Where IP Development, Enhancement, Maintenance, Protection, and Exploitation activities are currently performed.
- **IP-Related Financial Data**: Revenue attributable to IP, current royalty flows, R&D expenditure, IP-related costs by entity.
- **Strategic Objectives**: Tax optimization, IP centralization, M&A preparation, risk mitigation, or licensing monetization.
- **Jurisdictions of Interest**: Current and planned IP holding locations.
- **Existing Agreements**: Current license agreements, cost sharing arrangements, and R&D service agreements.
- **Regulatory Context**: Industry-specific IP regulations, data localization requirements, and export control considerations.

## Execution Steps

### 1. IP Asset Identification and Classification

Conduct a comprehensive IP inventory:

| IP Asset | Type | Description | Owner (Legal) | Owner (Economic) | Registration / Status | Jurisdiction | Revenue Attributable ($M) | Remaining Useful Life |
|---|---|---|---|---|---|---|---|---|
| [Asset 1] | Patent | [Description] | [Entity] | [Entity] | [Granted / Pending / Trade secret] | [Country] | $___M | ___ years |
| [Asset 2] | Trademark | [Description] | [Entity] | [Entity] | [Registered / Common law] | [Country] | $___M | Indefinite |
| [Asset 3] | Trade secret | [Description] | [Entity] | [Entity] | [Internal classification] | [Country] | $___M | N/A |
| [Asset 4] | Copyright | [Description] | [Entity] | [Entity] | [Auto / Registered] | [Country] | $___M | ___ years |
| [Asset 5] | Know-how | [Description] | [Entity] | [Entity] | [Documented / Undocumented] | [Country] | $___M | ___ years |
| [Asset 6] | Data asset | [Description] | [Entity] | [Entity] | [Proprietary / Licensed] | [Country] | $___M | ___ years |

**IP classification matrix**:

| Classification | Tax Relevance | Valuation Approach | Licensing Model |
|---|---|---|---|
| **Patents** | Qualify for IP box in most regimes; amortizable; can be contributed tax-free under certain conditions | Relief from royalty, excess earnings | Royalty as % of net sales (typical: 2-8%) |
| **Trademarks** | IP box eligibility varies (excluded in many post-BEPS regimes); indefinite life | Relief from royalty, market approach | Royalty as % of net sales (typical: 1-5%) |
| **Trade secrets** | May qualify as know-how for IP box; no registration = harder to transfer cleanly | Cost approach, excess earnings | Lump-sum or running royalty |
| **Copyrights / software** | Software copyrights qualify for IP box in many jurisdictions; finite life | Relief from royalty, cost approach | Per-unit, per-user, or % of revenue |
| **Know-how** | Qualifies if documented and transferable; DEMPE analysis critical | Cost approach, comparable transactions | Technical assistance fee or bundled royalty |
| **Data assets** | Emerging area; limited IP box coverage; privacy regulations create complexity | Cost approach, income approach | License fee, data-as-a-service pricing |

### 2. IP Ownership Structure Design

Evaluate alternative ownership structures:

| Structure | Description | Tax Advantages | Tax Risks | Best Suited For |
|---|---|---|---|---|
| **Centralized IP HoldCo** | Single entity owns all material IP; licenses to operating entities worldwide | IP box eligibility; consolidated royalty income; single licensing point | Substance challenge (DEMPE must be performed); withholding on royalties; CFC risk at parent level | Groups with globally exploited IP; post-M&A IP consolidation |
| **Regional IP HoldCos** | IP ownership split by region (e.g., EMEA, APAC, Americas) | Regional treaty access; reduced withholding; distributed risk | Complexity; fragmented ownership; potential for inconsistent policies | Large multinationals with distinct regional markets |
| **Distributed / local ownership** | Each operating entity owns IP it develops and uses locally | Simplest; no intercompany royalties; substance automatic | No centralized IP box benefit; no royalty deductions in high-tax jurisdictions | Early-stage companies; single-jurisdiction businesses |
| **Principal company model** | One entity is the entrepreneur/principal; owns IP and bears risk; other entities are limited-risk | Aligns with FAR analysis; residual profit in IP owner; routine returns to others | Principal must have genuine substance and decision-making authority | Groups with clear entrepreneurial entity |
| **Cost sharing arrangement** | Multiple participants jointly fund IP development and share ownership proportional to anticipated benefit | Each participant owns right to exploit in its territory; no ongoing royalty | Buy-in payment on existing IP; complex to maintain; IRS scrutiny (Section 482) | Joint development between US parent and foreign subsidiary |

**Recommended structure evaluation**:

| Factor | Option A: Centralized HoldCo in [Country] | Option B: Principal Model in [Country] | Option C: Cost Sharing |
|---|---|---|---|
| IP box rate available | ___% | ___% | N/A |
| Withholding on royalties (weighted avg) | ___% | ___% | N/A (no royalties) |
| DEMPE substance achievable? | [Assessment] | [Assessment] | Automatic (development = ownership) |
| CFC inclusion risk | [Assessment] | [Assessment] | [Assessment] |
| Implementation complexity | [Low/Med/High] | [Low/Med/High] | [Low/Med/High] |
| Ongoing compliance cost | $___K/year | $___K/year | $___K/year |
| Estimated annual tax savings | $___M | $___M | $___M |

### 3. IP Valuation Methodologies

Cross-reference to the `valuation` skill for full methodology. Key approaches for IP:

#### 3a. Relief from Royalty Method

```
IP Value = Sum of [Projected Revenue_t x Royalty Rate x (1 - Tax Rate) / (1 + r)^t] for t = 1 to N
         + Terminal Value

Where:
  Royalty Rate = arm's length royalty rate from comparable license agreements
  Tax Rate = tax rate of the hypothetical licensee
  r = discount rate (risk-adjusted; typically WACC + IP-specific premium)
  N = remaining useful life of the IP
```

| Parameter | Value | Basis |
|---|---|---|
| Projected revenue (Year 1) | $___M | Management forecast |
| Revenue growth rate | ___% | Historical + market analysis |
| Arm's length royalty rate | ___% | Comparable license analysis |
| Tax rate | ___% | Licensee jurisdiction |
| Discount rate | ___% | WACC + ___ bps IP premium |
| Remaining useful life | ___ years | Patent term / economic life |
| **IP Value (Relief from Royalty)** | **$___M** | |

#### 3b. Multi-Period Excess Earnings Method (MPEEM)

Used for primary intangible assets — isolates earnings attributable to the IP after deducting returns on all other assets:

```
Excess Earnings_t = Total Earnings_t
  - Contributory Asset Charge (working capital x required return)
  - Contributory Asset Charge (fixed assets x required return)
  - Contributory Asset Charge (workforce x required return)
  - Contributory Asset Charge (other intangibles x required return)

IP Value = Sum of [Excess Earnings_t / (1 + r)^t] for t = 1 to N + Terminal Value
```

#### 3c. Cost Approach

Used as a floor value or for early-stage IP where income data is limited:

```
IP Value = Sum of historical R&D costs to develop the IP
         x (1 + Entrepreneurial profit margin)
         x Obsolescence adjustment (functional, economic, technological)
```

| Cost Element | Amount ($M) | Period |
|---|---|---|
| Internal R&D labor | $___M | [Years] |
| External R&D (contractors) | $___M | [Years] |
| Materials and supplies | $___M | [Years] |
| Allocated overhead | $___M | [Years] |
| Opportunity cost / developer's profit | $___M | ___% markup |
| Less: Obsolescence adjustment | ($___M) | ___% reduction |
| **IP Value (Cost Approach)** | **$___M** | |

**Valuation reconciliation**:

| Method | IP Value ($M) | Weight | Weighted Value ($M) |
|---|---|---|---|
| Relief from royalty | $___M | ___% | $___M |
| Excess earnings (MPEEM) | $___M | ___% | $___M |
| Cost approach | $___M | ___% | $___M |
| **Concluded IP Value** | | | **$___M** |

### 4. Licensing Structure Design

#### 4a. License Framework

| Element | Inbound License (to IP HoldCo from developer) | Outbound License (from IP HoldCo to OpCo) |
|---|---|---|
| License type | Exclusive, worldwide, all fields of use | Non-exclusive, territory-specific, field-specific |
| Royalty basis | Lump-sum buy-in + ongoing royalty | Running royalty (% of net sales) |
| Royalty rate | Market rate benchmarked to comparable transactions | Market rate benchmarked to comparable transactions |
| Sub-licensing rights | Yes — enables outbound licensing | Limited — only within operating territory |
| Term | Perpetual or IP lifetime | 5-10 years, auto-renewing |
| Minimum royalty | [If applicable] | [If applicable to ensure substance of arrangement] |
| Payment timing | Quarterly in arrears | Quarterly in arrears |

#### 4b. Royalty Rate Benchmarking

| Comparability Factor | Comparable 1 | Comparable 2 | Comparable 3 | Subject Transaction |
|---|---|---|---|---|
| Industry | [Industry] | | | [Industry] |
| IP type | [Patent/TM/SW] | | | |
| Exclusivity | [Exclusive/Non-exclusive] | | | |
| Territory | [Scope] | | | |
| Development stage | [Early/Mature] | | | |
| Revenue base | [Net sales / Gross sales] | | | |
| Royalty rate | ___% | ___% | ___% | |
| **Arm's length range** | | | | **___% - ___%** |
| **Selected rate** | | | | **___%** |

**Data sources for royalty comparables**: RoyaltyStat, ktMINE, SEC filings (license agreements in 10-K/10-Q), BVR/Valuation Advisors, industry surveys.

#### 4c. Withholding Tax on Royalties

| Royalty Flow | From (Licensee) | To (Licensor) | Domestic WHT Rate | Treaty Rate | Treaty Cited | Beneficial Owner Test Met? |
|---|---|---|---|---|---|---|
| [Flow 1] | [Entity/Country] | [Entity/Country] | ___% | ___% | [Treaty article] | Yes/No |
| [Flow 2] | | | | | | |

**Net royalty income after WHT and IP box**:
```
Net income = Gross royalty
  - Withholding tax (net of foreign tax credits)
  x IP box effective rate (if applicable)
  = After-tax royalty income
```

### 5. IP Migration Planning

#### 5a. Migration Step Plan

| Step | Action | Tax Implication | Timeline |
|---|---|---|---|
| 1 | **IP valuation** — Determine arm's length value of IP to be transferred | Valuation sets the transfer price; affects gain/loss at transferor | Weeks 1-6 |
| 2 | **Exit tax analysis** — Quantify tax on deemed disposition at transferor jurisdiction | Transferor recognizes gain = FMV minus tax basis; exit tax may apply | Weeks 1-4 (concurrent) |
| 3 | **Transfer pricing documentation** — Prepare documentation supporting arm's length consideration | Required to defend transfer price; contemporaneous documentation essential | Weeks 4-8 |
| 4 | **Intercompany agreement execution** — IP assignment or license agreement at arm's length | Legal transfer of rights; consideration may be lump-sum, installment, or ongoing payment | Week 8 |
| 5 | **Regulatory filings** — Patent/trademark assignment recordings; tax authority notifications | Some jurisdictions require advance notification of IP transfers (e.g., Australia, India) | Weeks 8-12 |
| 6 | **Substance establishment** — Ensure receiving entity has DEMPE capability before or at transfer | Substance must exist before IP income flows; retroactive substance does not cure | Weeks 1-8 (must precede step 4) |
| 7 | **Post-migration monitoring** — Verify intercompany flows align with new structure | Ensure royalties are paid on schedule; TP documentation updated annually | Ongoing |

#### 5b. Exit Tax Analysis

| Jurisdiction | Exit Tax Rule | Applies to IP Transfers? | Rate | Deferral / Exemption Available? |
|---|---|---|---|---|
| United States | Section 367(d) — deemed royalty over useful life (not lump-sum) | Yes — outbound IP transfers to foreign corp | Ordinary income rates (up to 37% individual / 21% corporate) | No deferral; 20-year deemed income inclusion |
| Germany | Exit tax on unrealized gains when assets leave German tax jurisdiction | Yes | ~30% (corporate + trade tax) | EU/EEA deferral (5 annual installments) |
| France | Exit tax on unrealized gains | Yes | ~25% | EU/EEA deferral under conditions |
| Australia | CGT on deemed disposal; market value substitution rule | Yes | 30% (corporate) | No general deferral |
| India | Tax on IP transfer; requires prior AO approval for some transfers | Yes | As per transfer pricing + capital gains rates | No |
| Netherlands | Generally no exit tax on IP (participation exemption may apply to IP gains) | Limited | N/A | Participation exemption may shelter gain |
| UK | Degrouping charge if transferred within 6 years of intra-group transfer | Conditional | 25% (corporate) | Substantial shareholding exemption may apply |

**Exit tax cost estimate**:

| IP Asset | FMV ($M) | Tax Basis ($M) | Gain ($M) | Exit Tax Rate | Exit Tax ($M) | Mitigation |
|---|---|---|---|---|---|---|
| [Asset 1] | $___M | $___M | $___M | ___% | $___M | [Strategy] |
| [Asset 2] | $___M | $___M | $___M | ___% | $___M | [Strategy] |
| **Total exit tax** | | | | | **$___M** | |

**Break-even analysis**: Years to recoup exit tax through lower ongoing IP income taxation:
```
Break-even period = Exit tax cost / Annual tax saving from new structure
```

### 6. Cost Sharing / Cost Contribution Arrangement (CCA) Design

| Element | Design Decision | Rationale |
|---|---|---|
| **Participants** | [List entities and territories] | Each must reasonably anticipate benefit from IP |
| **Scope of IP** | [Specific IP being jointly developed] | Clearly defined to avoid scope creep disputes |
| **Cost pool** | [R&D costs, direct and indirect] | All costs related to developing the covered IP |
| **Allocation key** | [Reasonably anticipated benefits — typically projected revenue or operating profit by territory] | Must reflect anticipated benefit, not actual results |
| **Buy-in payment** | [Lump-sum or installment for pre-existing IP contributed] | Arm's length value of existing IP made available to the arrangement |
| **Buy-out provisions** | [Payment if participant exits arrangement] | Must reflect FMV of interest relinquished |
| **PCT payments** (US) | [Platform Contribution Transaction — arm's length consideration for existing IP] | Required under Section 482 cost sharing regulations |
| **Annual true-up** | [Mechanism to adjust if actual costs differ from projections] | Ensures ongoing arm's length allocation |

**CCA vs. licensing comparison**:

| Factor | Cost Sharing / CCA | Licensing Model |
|---|---|---|
| Upfront cost | High (buy-in for pre-existing IP) | Low (no buy-in) |
| Ongoing payments | Share of R&D costs (proportional to anticipated benefit) | Royalty (% of revenue or profits) |
| IP ownership | Each participant owns rights in its territory | Licensor retains ownership; licensee has use rights only |
| DEMPE alignment | Each participant must perform DEMPE for its territory | Licensor performs DEMPE; licensee performs exploitation only |
| Flexibility to exit | Buy-out payment required | License termination per agreement terms |
| IRS/tax authority scrutiny | High (Section 482 regulations; Altera case history) | Moderate (standard arm's length analysis) |
| Best for | Genuinely joint development with shared expertise | IP owner controls development; licensees exploit locally |

### 7. DEMPE Functions Substance Requirements

The OECD Guidelines (Chapter VI) require that the entity claiming IP income must perform — or control and bear the financial risk of — the DEMPE functions:

| DEMPE Function | Description | Substance Indicators | Minimum Requirements |
|---|---|---|---|
| **Development** | Creating and improving the IP | R&D personnel; lab/development facilities; decision authority over R&D direction | Qualified employees directing R&D strategy; budget authority |
| **Enhancement** | Upgrading and extending the IP | Engineers/scientists improving existing IP; versioning; feature additions | Personnel working on IP improvements; documented enhancement roadmap |
| **Maintenance** | Preserving the value and utility of the IP | Quality assurance; bug fixes; renewals; patent maintenance fees | Staff maintaining IP; budget for maintenance activities |
| **Protection** | Legal and practical protection of IP rights | IP counsel; patent prosecution; litigation management; trade secret programs | Legal team or supervised external counsel; IP protection policies |
| **Exploitation** | Commercializing and monetizing the IP | Licensing negotiations; marketing strategy; pricing decisions; distribution | Commercial decision-makers; licensing/sales team |

**Substance assessment per entity**:

| Entity | D | E | M | P | E | Overall Substance Rating | Gap |
|---|---|---|---|---|---|---|---|
| [IP HoldCo] | [Strong/Adequate/Weak] | | | | | [Sufficient / Insufficient] | [Description] |
| [R&D Entity] | [Strong/Adequate/Weak] | | | | | | |
| [OpCo 1] | [Strong/Adequate/Weak] | | | | | | |

**Minimum substance benchmarks for IP holding entities**:

| Requirement | Benchmark | Current Status | Action Needed |
|---|---|---|---|
| Qualified employees | 3-5 minimum with IP management expertise | [Current count] | [Hire / Relocate] |
| Board / management | Local directors with authority over IP decisions | [Current composition] | [Appoint / Empower] |
| Office and facilities | Genuine office (not just registered address) | [Current setup] | [Lease / Expand] |
| Operating expenditure | Proportional to IP income (no empty shell) | $___M current | [Increase / Justify] |
| Decision-making records | Board minutes documenting IP strategy decisions | [Available / Not available] | [Implement governance protocol] |
| Contracts with service providers | Outsourced DEMPE functions under HoldCo's control and direction | [In place / Missing] | [Draft service agreements] |

### 8. IP Box Regime Eligibility and Benefit Analysis

Assess eligibility for IP box in the IP holding jurisdiction:

| Requirement | Threshold | Entity Status | Eligible? |
|---|---|---|---|
| Qualifying IP type | [Per regime — patents, software, etc.] | [IP types held] | Yes/No |
| Nexus fraction | Must be >0%; benefit scales with fraction | ___% (see calculation below) | Yes — ___% of income qualifies |
| Income tracking | IP income must be tracked per qualifying asset | [System in place / Not in place] | Yes/No |
| Election / registration | [Per regime requirements] | [Filed / Not filed] | Yes/No |
| Minimum holding period | [If applicable] | [Holding period met?] | Yes/No |

**Nexus fraction calculation**:
```
Nexus Fraction = (QE + UPE) / OE

Where:
  QE = Qualifying Expenditure (in-house R&D + outsourced R&D to unrelated parties)
  UPE = Uplift (30% of QE, capped so QE + UPE does not exceed OE)
  OE = Overall Expenditure (QE + acquisition cost of IP + outsourced R&D to related parties)
```

| Component | Amount ($M) | Notes |
|---|---|---|
| In-house R&D expenditure | $___M | Employees performing qualifying R&D |
| Outsourced R&D (unrelated parties) | $___M | Third-party R&D contractors |
| **Qualifying Expenditure (QE)** | **$___M** | Sum of above |
| 30% Uplift (UPE) | $___M | Min(30% x QE, OE - QE) |
| **Numerator (QE + UPE)** | **$___M** | |
| IP acquisition cost | $___M | Purchase price of acquired IP |
| Outsourced R&D (related parties) | $___M | Intercompany R&D charges |
| **Overall Expenditure (OE)** | **$___M** | QE + acquisition + related-party outsourcing |
| **Nexus Fraction** | **___%** | (QE + UPE) / OE |

**Benefit calculation**:
```
IP box benefit = Qualifying IP income x Nexus fraction x (Standard rate - IP box rate)
Annual benefit = $___M x ___% x (___% - ___%) = $___M
```

### 9. Defensive IP Strategy

| Component | Analysis | Recommendation |
|---|---|---|
| **Freedom to operate (FTO)** | [Assessment of third-party IP that could block commercial activities] | [Obtain licenses / Design around / Challenge validity] |
| **IP audit** | [Review of all IP assets for proper documentation, registration, and protection] | [Register unregistered IP; document trade secrets; update assignments] |
| **Employee IP agreements** | [Status of IP assignment clauses in employment contracts] | [Standardize across jurisdictions; include post-employment restrictions] |
| **Contractor IP agreements** | [Status of IP ownership clauses in contractor agreements] | [Ensure work-for-hire or assignment; address pre-existing IP] |
| **IP insurance** | [Coverage for infringement claims, both defensive and offensive] | [Evaluate IP insurance policies; cost-benefit analysis] |
| **Trade secret program** | [Status of trade secret identification, classification, and protection measures] | [Implement classification system; access controls; NDA program] |
| **Enforcement strategy** | [Approach to monitoring and enforcing IP rights against infringers] | [Watch services; graduated enforcement (cease-and-desist, negotiation, litigation)] |
| **Open source compliance** | [Review of open source software usage and license compliance] | [Audit; implement approval workflow; ensure license compatibility] |

### 10. IP in M&A Context

| Scenario | Tax Considerations | Recommended Approach |
|---|---|---|
| **IP acquisition (asset deal)** | Buyer allocates purchase price to IP (Section 1060 allocation); amortizes over 15 years (Section 197) or useful life | Maximize allocation to short-lived / depreciable IP; step-up benefit calculation |
| **IP carve-out (pre-sale)** | Transfer IP out of target before sale; may trigger gain at target; affects target valuation | Evaluate exit tax vs. sale price impact; timing relative to deal signing |
| **IP contribution to JV** | Section 351 (US) or local equivalent for tax-free contribution; must control resulting entity | Verify control threshold; document FMV at contribution |
| **IP licensing post-deal** | New intercompany IP license between acquirer group and target; arm's length royalty required | Benchmark royalty rate; integrate into deal economics |
| **IP in spin-off** | Section 355 requirements; IP must be part of active trade or business | Verify IP is integral to spun-off business; avoid device |
| **IP representations & warranties** | Target reps on IP ownership, freedom from encumbrance, non-infringement | Tax indemnity for IP-related tax exposures (transfer pricing, IP box claims) |

**IP step-up benefit calculation (asset deal)**:

| IP Asset | Allocated Value ($M) | Tax Basis Before ($M) | Step-Up ($M) | Amortization Period | Annual Deduction ($M) | Tax Rate | Annual Tax Benefit ($M) | NPV of Step-Up ($M) |
|---|---|---|---|---|---|---|---|---|
| [Asset 1] | $___M | $___M | $___M | ___ years | $___M | ___% | $___M | $___M |
| [Asset 2] | $___M | $___M | $___M | ___ years | $___M | ___% | $___M | $___M |
| **Total** | | | | | | | | **$___M** |

### 11. Anti-Avoidance Considerations

| Risk | OECD Reference | Description | Mitigation |
|---|---|---|---|
| **Nexus approach (BEPS Action 5)** | Action 5 Final Report | IP box benefits limited by nexus fraction; substance required | Maximize in-house R&D; minimize related-party outsourcing |
| **DEMPE substance (BEPS Actions 8-10)** | Ch. VI, OECD Guidelines | IP income must be commensurate with DEMPE functions performed | Ensure IP HoldCo has real people, real decisions, real risk-bearing |
| **Hard-to-value intangibles (HTVI)** | Ch. VI, Section D.4 | Tax authorities may use ex-post outcomes to challenge ex-ante valuations | Conservative valuation; price adjustment clauses; contemporaneous documentation |
| **Recharacterization** | Ch. I, Section D.2 | Tax authority may recharacterize a transaction if it lacks commercial rationality | Ensure arrangement is commercially rational for all parties |
| **Principal Purpose Test (PPT)** | MLI Article 7 | Treaty benefits denied if principal purpose is to obtain treaty benefit | Document non-tax commercial reasons for structure |
| **CFC inclusion of IP income** | Various (Subpart F, GILTI, CFC rules per jurisdiction) | Passive royalty income may be included in parent's income currently | Active business exception; high-tax exclusion; check-the-box planning |
| **Transfer pricing on IP transfers** | Ch. IX, OECD Guidelines | IP migration must be at arm's length value; commensurate with income standard (US) | Robust valuation; consider price adjustment mechanism |
| **Economic substance legislation** | Cayman, BVI, Channel Islands, UAE, etc. | Entities must demonstrate adequate substance for IP holding activities | Meet minimum substance requirements per jurisdiction |

**Overall anti-avoidance risk rating**:

| Structure Element | Risk Level | Confidence in Defense | Priority Mitigation |
|---|---|---|---|
| IP ownership location | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |
| DEMPE substance | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |
| Royalty pricing | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |
| IP migration valuation | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |
| Treaty access / WHT reduction | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |
| CFC exposure | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |

### 12. Implementation Roadmap

| Phase | Timeline | Actions | Deliverables | Dependencies |
|---|---|---|---|---|
| **1. Assessment** | Weeks 1-4 | IP inventory; DEMPE mapping; current structure analysis; identify target structure | IP register; DEMPE matrix; options memo | Access to IP records, R&D team interviews |
| **2. Valuation** | Weeks 3-8 | Value IP assets using appropriate methodology; benchmark royalty rates | Valuation report; royalty benchmarking study | Financial data; comparable license data |
| **3. Structure Design** | Weeks 5-10 | Select IP holding location; design license/CCA structure; draft intercompany agreements | Structure memo; draft agreements | Tax opinion on structure; legal review |
| **4. Substance Building** | Weeks 6-16 | Hire/transfer qualified employees to IP HoldCo; establish office; implement governance | Employment contracts; office lease; board resolution | Recruitment; immigration (if cross-border) |
| **5. IP Migration** | Weeks 12-20 | Execute IP assignments; file regulatory recordings; implement transfer pricing documentation | Executed assignments; patent/TM recordings; TP local file | Valuation complete; substance in place |
| **6. Operational Launch** | Weeks 16-24 | Activate licensing flows; implement royalty payment processes; update accounting systems | First royalty invoices; updated intercompany accounts | IT/finance systems; banking setup |
| **7. Regulatory Filings** | Weeks 20-28 | IP box election; tax return filings; CbCR updates; any advance ruling applications | Filed elections; updated CbCR; ruling application | Local tax advisor; filing deadlines |
| **8. Monitoring** | Ongoing | Annual DEMPE review; TP documentation update; nexus fraction recalculation; substance audit | Annual compliance package | Internal tax team; external advisors |

**Regulatory filing checklist**:

| Filing | Jurisdiction | Deadline | Status |
|---|---|---|---|
| Patent/trademark assignment recording | [IP offices per jurisdiction] | [Varies — typically 3-6 months] | [ ] |
| IP box election | [IP HoldCo jurisdiction] | [With tax return] | [ ] |
| Transfer pricing documentation | [Each jurisdiction] | [With tax return or on request] | [ ] |
| CbCR update | [Parent jurisdiction] | [12 months after fiscal year end] | [ ] |
| Advance ruling application (if desired) | [IP HoldCo jurisdiction] | [Before implementation] | [ ] |
| Foreign investment notification | [If applicable] | [Varies] | [ ] |
| Export control license (if applicable) | [Transferor jurisdiction] | [Before IP transfer] | [ ] |

## Output Template

```markdown
## IP Strategy: [Client / Group Name]

**Date**: [Date] | **Prepared by**: Tax Advisory Practice
**Objective**: [IP structuring objective]

> This analysis provides a strategic framework for tax planning. It does not
> constitute tax advice or a legal opinion. Implementation requires review by
> qualified tax counsel in each relevant jurisdiction. Tax laws change
> frequently; all analysis is based on current rules as of the date provided.

---

### 1. IP Portfolio Summary

| IP Asset | Type | Owner | Revenue ($M) | Useful Life | Value ($M) |
|---|---|---|---|---|---|
| [Asset] | [Type] | [Entity] | $___M | ___ years | $___M |

**Total IP portfolio value**: $___M

### 2. Current DEMPE Analysis

| DEMPE Function | Currently Performed By | Substance Rating |
|---|---|---|
| Development | [Entity/Location] | [Strong/Adequate/Weak] |
| Enhancement | [Entity/Location] | [Strong/Adequate/Weak] |
| Maintenance | [Entity/Location] | [Strong/Adequate/Weak] |
| Protection | [Entity/Location] | [Strong/Adequate/Weak] |
| Exploitation | [Entity/Location] | [Strong/Adequate/Weak] |

### 3. Recommended IP Structure

[Narrative description with entity diagram]

**IP holding entity**: [Entity name, jurisdiction, role]
**Substance plan**: [Employees, office, governance]

### 4. IP Valuation

| Method | IP Value ($M) | Weight |
|---|---|---|
| Relief from royalty | $___M | ___% |
| Excess earnings | $___M | ___% |
| Cost approach | $___M | ___% |
| **Concluded value** | **$___M** | |

### 5. Licensing Design

| License | Licensor | Licensee | Royalty Rate | Annual Flow ($M) | WHT |
|---|---|---|---|---|---|
| [License] | [Entity] | [Entity] | ___% | $___M | ___% |

### 6. IP Migration Plan (if applicable)

| IP Asset | From | To | Value ($M) | Exit Tax ($M) | Break-Even (Years) |
|---|---|---|---|---|---|
| [Asset] | [Entity] | [Entity] | $___M | $___M | ___ |

### 7. IP Box Benefit

**Nexus fraction**: ___%
**Effective rate**: ___% (vs. standard ___%)
**Annual benefit**: $___M | **NPV (10-year)**: $___M

### 8. Anti-Avoidance Risk Assessment

| Risk | Level | Defense Strength | Mitigation |
|---|---|---|---|
| DEMPE substance | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |
| Nexus approach | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |
| CFC inclusion | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |
| HTVI challenge | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |
| Treaty PPT | [Low/Med/High] | [Strong/Adequate/Weak] | [Action] |

### 9. Defensive IP Strategy

[FTO assessment, IP audit findings, trade secret program recommendations]

### 10. Implementation Roadmap

| Phase | Timeline | Key Actions | Owner |
|---|---|---|---|
| Assessment | Weeks 1-4 | [Actions] | [Team] |
| Valuation | Weeks 3-8 | [Actions] | [Team] |
| Structure design | Weeks 5-10 | [Actions] | [Team] |
| Substance building | Weeks 6-16 | [Actions] | [Team] |
| Migration | Weeks 12-20 | [Actions] | [Team] |
| Operational launch | Weeks 16-24 | [Actions] | [Team] |

### Key Recommendations

1. [Priority recommendation with estimated benefit and timeline]
2. [Second priority recommendation]
3. [Third priority recommendation]

### Cross-References
- `valuation` skill for detailed IP valuation methodologies
- `tax-structure-advisory` skill for holding company jurisdiction selection
- `transfer-pricing` skill for royalty rate benchmarking and TP documentation
- `tax-incentive-analysis` skill for IP box eligibility and R&D credit interaction
```

## Quality Checks

- [ ] All analysis is clearly labeled as an analytical framework, not legal advice; disclaimer is included.
- [ ] Complete IP inventory with classification, ownership, jurisdiction, and revenue attribution for every asset.
- [ ] IP ownership structure options evaluated with at least three alternatives compared on tax savings, risk, and complexity.
- [ ] IP valuation uses at least two methodologies with reconciliation and concluded value.
- [ ] Royalty rate benchmarking uses comparable license agreements with documented comparability factors.
- [ ] Withholding tax on royalties is analyzed for each flow with treaty rates and beneficial ownership assessment.
- [ ] IP migration plan includes exit tax analysis with break-even calculation.
- [ ] Cost sharing / CCA design (if applicable) includes buy-in calculation, allocation key, and annual true-up mechanism.
- [ ] DEMPE substance analysis covers all five functions with specific indicators and minimum requirements per entity.
- [ ] Substance requirements include minimum headcount, local management, office, and operating expenditure benchmarks.
- [ ] IP box eligibility assessed with nexus fraction calculation per BEPS Action 5.
- [ ] Anti-avoidance assessment covers nexus approach, DEMPE, HTVI, recharacterization, PPT, CFC, and economic substance.
- [ ] Defensive IP strategy includes FTO, IP audit, employee/contractor agreements, and enforcement approach.
- [ ] IP in M&A context (if applicable) includes step-up benefit NPV calculation.
- [ ] Implementation roadmap includes phases, timeline, deliverables, dependencies, and regulatory filing checklist.
- [ ] Cross-references to related skills (valuation, tax-structure-advisory, transfer-pricing, tax-incentive-analysis) are included.
