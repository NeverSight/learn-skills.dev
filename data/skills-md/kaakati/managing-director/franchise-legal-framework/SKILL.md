---
name: franchise-legal-framework
description: >
  Comprehensive franchise legal and regulatory advisory engine. Generates FDD
  strategic guidance across all 23 Items, franchise agreement term sheets,
  territory rights structures, state and international registration mappings,
  and compliance calendars. Parameterized by {franchise_model}, {territory_scope},
  and {regulatory_domain}. USE THIS SKILL when preparing FDD strategy, drafting
  franchise agreement terms, analyzing Item 19 financial performance representations,
  mapping franchise registration requirements, structuring area development or
  master franchise agreements, or advising on franchise relationship laws.
---

# Franchise Legal Framework

## Core Variables

Identify these before execution — they drive every legal structure in this skill:

| Variable | Examples | Impact on Legal Framework |
|---|---|---|
| `{franchise_model}` | single-unit, multi-unit, area_development, master_franchise | Determines agreement type, fee structures, territory grants |
| `{territory_scope}` | local, national, international | Determines registration requirements, regulatory jurisdictions |
| `{regulatory_domain}` | data_privacy, food_safety, health_code, financial | Determines compliance overlay on FDD and agreements |
| `{business_model}` | SaaS, physical_retail, service, hybrid | Determines fee structures and operational obligations |
| `{product_type}` | software, food, education, healthcare, fitness | Determines sector-specific regulatory disclosures |
| `{revenue_model}` | subscription, transaction, licensing, retail | Determines royalty calculation methodology |
| `{target_franchisee}` | operator, investor, corporate, hybrid | Determines negotiation leverage and agreement flexibility |

## Required Inputs

- **Franchisor Entity**: Legal name, state of formation, corporate structure, years in operation.
- **Franchise System**: Number of units (franchised and company-owned), years franchising.
- **Fee Structure**: Initial franchise fee, ongoing royalty, advertising fund, technology fees.
- **Territory Definition**: How territories are defined (geography, population, zip codes, radius).
- **Franchise Model**: Single-unit, multi-unit, area development, or master franchise.
- **Geographic Scope**: States and/or countries where franchise will be offered/operating.
- **Litigation History**: Pending or resolved litigation, arbitration, bankruptcy filings.
- **Financial Statements**: Audited financials availability (3 years required for FDD).

## Execution Steps

### 1. FDD Structure — All 23 Items with Strategic Advisory

The Franchise Disclosure Document is the cornerstone legal instrument. Below is each Item with its purpose, strategic advisory notes, and risk flags by `{business_model}`.

| Item | Title | Strategic Advisory | Key Risk Flags |
|---|---|---|---|
| 1 | The Franchisor and Parents/Predecessors/Affiliates | Disclose complete corporate family tree. Affiliates offering competing products require explicit disclosure. | Undisclosed affiliates competing in same sector. |
| 2 | Business Experience | 5-year biographical data for all officers/directors. Turnover signals instability. | High executive turnover, lack of franchise experience in leadership. |
| 3 | Litigation | ALL pending/settled litigation in 10-year lookback. Pattern litigation signals systemic issues. | Patterns of franchisee-initiated suits, SPA violations, fraud allegations. |
| 4 | Bankruptcy | 15-year lookback for principals. Bankruptcy does not bar franchising but must be disclosed. | Recent bankruptcy by key officers, serial bankruptcy filings. |
| 5 | Initial Fees | All fees paid before opening. Includes franchise fee, training fees, technology fees, build-out deposits. | Excessive front-loaded fees, non-refundable deposits without milestones. |
| 6 | Other Fees | Ongoing fees table — royalties, advertising, technology, transfer, renewal, audit, late fees. | Hidden fees, uncapped advertising fund, technology fees escalating without cap. |
| 7 | Estimated Initial Investment | Full investment range from signing through 3 months of operation. Must be reasonable and verifiable. | Unrealistically low estimates, missing categories, no range (single-point). |
| 8 | Restrictions on Sources | Required and approved suppliers. Franchisor rebate/revenue from suppliers must be disclosed. | Exclusive sourcing with franchisor markup, undisclosed supplier rebates. |
| 9 | Franchisee's Obligations | Cross-reference table pointing to agreement provisions and FDD items for each obligation. | Vague obligation descriptions, obligations not cross-referenced to agreement. |
| 10 | Financing | Franchisor-offered or arranged financing terms. | Predatory financing terms, mandatory franchisor financing. |
| 11 | Franchisor's Assistance | Pre-opening and post-opening obligations of the franchisor. This is the franchisor's performance commitment. | Vague support commitments, no defined timelines, "may" vs. "will" language. |
| 12 | Territory | Exclusive, protected, or open territory. Impact of e-commerce, delivery, and alternative channels. | Lack of exclusivity, reservation of all alternative channels, internet sales carve-outs. |
| 13 | Trademarks | Registration status, principal marks, known infringement disputes. | Unregistered marks, pending oppositions, ITU applications not converted. |
| 14 | Patents/Copyrights/Proprietary Information | IP protections for systems, software, methods, content. Critical for SaaS and education models. | Weak IP protection, trade secret reliance without NDA framework. |
| 15 | Obligation to Participate | Whether franchisee must be hands-on or can hire a manager. Drives `{target_franchisee}` fit. | Mandatory operator requirement conflicts with investor franchisee model. |
| 16 | Restrictions on Goods/Services | Limitations on what franchisee can sell. Approved products/services only. | Overly restrictive product limitations, no innovation path. |
| 17 | Renewal, Termination, Transfer, Dispute Resolution | Summary table of 23 relationship provisions. Most negotiated section. | One-sided termination rights, unreasonable non-compete, transfer restrictions. |
| 18 | Public Figures | Celebrity endorsements or spokesperson arrangements with compensation disclosure. | Undisclosed compensation, expired endorsement agreements still referenced. |
| 19 | Financial Performance Representations | Optional but increasingly expected. Historical or projected unit-level financial performance. | Cherry-picked data, non-representative sample, missing expense data, no basis statement. |
| 20 | Outlets and Franchisee Information | Unit count tables — openings, closings, transfers, reacquisitions over 3 years. Contact list of all franchisees. | High closure rates (>10%), declining net growth, large number of ceased operations. |
| 21 | Financial Statements | Audited financial statements for 3 fiscal years. Audit must follow US GAAP by independent CPA. | Qualified audit opinions, going-concern notes, negative net worth, thin capitalization. |
| 22 | Contracts | All agreements franchisee will sign — franchise agreement, lease, supply, technology, NDA. | Undisclosed side agreements, inconsistency between FDD and agreement terms. |
| 23 | Receipts | Acknowledgment that prospect received the FDD. Starts the 14-day waiting period (FTC Rule). | Failure to document receipt date, compressed waiting periods. |

### 2. Key FDD Items Deep-Dive

**Item 5 — Initial Fees by `{business_model}`**

| Fee Component | SaaS | Physical Retail | Service | Hybrid |
|---|---|---|---|---|
| Initial franchise fee | $15K-$50K | $25K-$50K | $20K-$45K | $25K-$50K |
| Technology setup fee | $5K-$25K | $2K-$10K | $2K-$10K | $5K-$20K |
| Training fee | $2K-$10K | $3K-$15K | $3K-$10K | $3K-$15K |
| Territory activation | $0-$10K | N/A | $0-$5K | $0-$10K |
| Build-out deposit | N/A | $10K-$50K | $0-$10K | $5K-$25K |
| Grand opening marketing | $2K-$10K | $5K-$25K | $2K-$10K | $5K-$20K |

**Item 6 — Ongoing Fee Structure**

| Fee Type | Typical Range | Calculation Basis | Cap/Floor |
|---|---|---|---|
| Royalty | 4-12% | Gross revenue (define clearly) | Minimum monthly royalty common |
| Advertising/brand fund | 1-3% | Gross revenue | Usually no cap — requires disclosure of spend |
| Technology/platform fee | $200-$2,000/mo or 1-3% | Flat fee or percentage | Annual CPI escalator common |
| Reporting/audit fee | $0-$500/mo | Flat fee | Triggered by late reporting |
| Transfer fee | $5K-$25K or 25-50% of then-current franchise fee | Per transfer event | Waiver for intra-family common |
| Renewal fee | $2K-$15K or 25-50% of then-current franchise fee | Per renewal event | Often negotiable |
| Late fee | 1.5%/mo or $50-$500 | On overdue amounts | State usury limits apply |

**Item 7 — Estimated Initial Investment Template**

| Category | Low Estimate | High Estimate | Notes |
|---|---|---|---|
| Initial franchise fee | $ | $ | As disclosed in Item 5 |
| Real estate / lease deposits | $ | $ | Physical retail: highest category |
| Build-out / construction | $ | $ | Per brand standards specifications |
| Equipment and fixtures | $ | $ | Approved vendor pricing |
| Technology systems | $ | $ | POS, CRM, franchise platform |
| Initial inventory / supplies | $ | $ | First 30-90 days |
| Insurance premiums | $ | $ | 3-month prepayment |
| Training expenses (travel) | $ | $ | Travel, lodging, meals for initial training |
| Professional fees | $ | $ | Attorney, accountant, entity formation |
| Permits and licenses | $ | $ | `{regulatory_domain}`-specific |
| Grand opening marketing | $ | $ | Per required marketing plan |
| Additional funds (3 months) | $ | $ | Working capital for first 90 days |
| **TOTAL** | **$** | **$** | |

**Item 19 — Financial Performance Representations**

Structure options for Item 19 disclosure:

| Approach | Description | Pros | Cons |
|---|---|---|---|
| No Item 19 | State "We do not make financial performance representations" | Zero liability | Competitive disadvantage; prospects demand data |
| Historic — All Units | Report actual results of all units over defined period | Credible, comprehensive | Weak units drag averages; requires extensive data |
| Historic — Subset | Report results of defined subset (e.g., units open 12+ months) | Shows mature performance | Must disclose selection criteria and percentage represented |
| Projected (with basis) | Forward-looking projections with reasonable basis statement | Persuasive sales tool | Higher legal risk if projections not achieved |
| Gross Revenue Only | Disclose only top-line revenue, not expenses or profit | Lower risk, some data | Franchisees cannot assess profitability |
| Full P&L | Disclose revenue, COGS, operating expenses, net income | Most helpful to prospects | Highest exposure if results vary widely |

**Item 19 Substantiation Requirements:**
- Written basis for the representation (data sources, methodology, assumptions).
- Statement of whether the representation relates to historic or projected results.
- If historic: the percentage of units that met or exceeded the stated results.
- Material assumptions underlying the representation.
- Cautionary language per FTC guidance.

**Item 20 — Outlets Table Analysis**

| Metric | Red Flag | Healthy | Best-in-Class |
|---|---|---|---|
| Net unit growth (annual) | Negative or flat | 5-15% growth | >15% sustained growth |
| Closure/termination rate | >10% annually | 3-5% | <2% |
| Transfer rate | >15% (distress signal) | 5-10% | <5% |
| Reacquisition rate | >5% (franchisor buying back) | <2% | 0% (strong network) |
| Ceased operations — reason | Termination-heavy | Mutual / market exit | Rare, with waitlist for territory |

### 3. Franchise Agreement Term Sheet — 10 Most Negotiated Provisions

| Provision | Franchisor Starting Position | Common Negotiation | Franchisee Ideal | Notes |
|---|---|---|---|---|
| **1. Term length** | 10 years | 10-15 years, align with lease | 15-20 years with renewal options | Must amortize initial investment |
| **2. Territory exclusivity** | Protected (not exclusive) | Exclusive with performance requirements | Exclusive, no performance triggers | See Territory Rights section below |
| **3. Royalty rate** | Published rate, no reduction | Tiered by revenue or unit count | Reduced rate, performance bonuses | Multi-unit operators negotiate hardest |
| **4. Advertising fund control** | Franchisor sole discretion | Advisory council input, spend reporting | Franchisee approval for local spend | Most contentious ongoing issue |
| **5. Transfer rights** | ROFR + transfer fee + buyer approval | Reasonable approval standard | Free transfer to qualified buyers | Intra-entity and family transfers exempt |
| **6. Renewal terms** | Sign then-current agreement | Renewal on original terms or hybrid | Same terms with fee inflation cap | "Then-current agreement" is the key battle |
| **7. Non-compete scope** | 2 years / 25 miles or territory | 1 year / 10-15 miles | 6 months / immediate territory only | Enforceability varies dramatically by state |
| **8. Termination rights** | Extensive cure and no-cure defaults | Reasonable cure periods, limited no-cure | Only material breach, mandatory mediation first | Franchise relationship laws override in some states |
| **9. Sourcing restrictions** | Designated suppliers only | Approved supplier process with alternatives | Freedom to source with quality standards | Supplier rebate disclosure required |
| **10. Dispute resolution** | Binding arbitration, franchisor's home state | Arbitration, neutral venue | Litigation option, franchisee's state | State franchise laws may override venue selection |

### 4. Territory Rights by `{franchise_model}`

| Territory Type | Definition | Best For | Risk |
|---|---|---|---|
| **Exclusive** | No other franchisees or company units in defined area | Single-unit operators, mature systems | Limits franchisor flexibility, requires performance obligations |
| **Protected** | No other franchisees, but franchisor reserves alternative channels | Most franchise systems | Internet/delivery channel conflicts, definition ambiguity |
| **Open** | No territory protection — first-come, first-served | High-density retail concepts | Cannibalization, franchisee conflict |

**Territory Grant by `{franchise_model}`:**

| Model | Typical Territory | Performance Requirement | Modification Rights |
|---|---|---|---|
| Single-unit | Defined geography (zip codes, radius, population) | Minimum revenue or customer targets | Reduction only for sustained underperformance |
| Multi-unit | Multiple defined territories within a market | Per-unit performance + aggregate | Territories revert individually upon unit failure |
| Area development | Exclusive development area for defined unit count | Development schedule: X units by Y date | Entire area reverts on missed development milestones |
| Master franchise | Country or large region | Sub-franchise development schedule + unit performance | Phased territory grant common, earn additional regions |

### 5. Non-Compete and Post-Term Covenants

**During-term non-compete:**
- Franchisee may not operate or invest in a competing business during the franchise term.
- Scope: define "competing business" precisely by `{product_type}` sector.
- Geographic scope: typically unlimited during term (franchise territory is irrelevant — it is about diversion of effort).

**Post-term non-compete by enforceability tier:**

| Enforceability | States / Jurisdictions | Recommended Scope |
|---|---|---|
| Generally enforceable | TX, FL, GA, OH, PA, most states | 1-2 years, 10-25 mile radius or defined territory |
| Limited enforcement | CA (largely unenforceable), OK, ND, MN | Narrow scope, consider alternatives (non-solicitation) |
| Moderate scrutiny | NY, IL, WA, MA | Reasonable in time and geography, tied to legitimate interest |
| International variance | UK (reasonable restraints), EU (1 year max per block exemption), Australia (cascading clauses) | Consult local counsel, use cascading enforceability clauses |

**Post-term obligations checklist:**
- De-identification (remove all marks, signage, branded materials).
- Customer transition (franchisor option to communicate with franchisee's customers).
- Non-solicitation of employees (typically 1-2 years).
- Return of confidential information and operations manuals.
- Assignment of local phone numbers, domains, social media handles.

### 6. Renewal, Transfer, and Termination Provisions

**Renewal Framework:**

| Element | Market Standard | Pro-Franchisor | Pro-Franchisee |
|---|---|---|---|
| Renewal right | Conditional — good standing | Right to not renew at discretion | Automatic renewal unless breach |
| Agreement version | Then-current form | Then-current, no negotiation | Original terms with CPI adjustments |
| Renewal fee | 25-50% of then-current initial fee | Full initial fee | Nominal or zero fee |
| Facility upgrade | Refurbishment to current standards | Full rebuild to new unit standards | Reasonable updates only |
| Notice period | 6-12 months before expiration | 12+ months | 6 months |

**Transfer Provisions:**

| Element | Standard | Key Negotiation Points |
|---|---|---|
| Franchisor consent | Required, not to be unreasonably withheld | Define "reasonable" — financial and operational criteria |
| Right of first refusal (ROFR) | 30-60 day matching period | Limit to exact terms, time-bound |
| Transfer fee | 25-50% of then-current franchise fee | Cap at $X or flat fee |
| Buyer qualifications | Meet current franchisee criteria | Same criteria, streamlined process |
| Seller obligations | Complete term obligations, cure all defaults | Reasonable wind-down period |
| Training requirement | Buyer completes full initial training | Abbreviated training if experienced operator |

**Termination — Cure vs. No-Cure Defaults:**

| Default Type | Cure Period | Examples |
|---|---|---|
| No-cure (immediate) | None — termination upon notice | Bankruptcy, criminal conviction, abandonment, material misrepresentation, health/safety violation |
| Curable (with notice) | 30-60 days | Failure to pay royalties, operational standard violations, reporting failures, unauthorized transfer |
| Repeated default | Shorter cure or no cure on third occurrence | Pattern of late payments, recurring audit failures |

### 7. State Franchise Registration Requirements

**Registration States** (must file and register FDD before offering):

| State | Registration | Relationship Law | Renewal Required | Key Nuance |
|---|---|---|---|---|
| California | Yes — DFPI | Yes — Franchise Relations Act | Annual | Most comprehensive requirements |
| New York | Yes — AG | Yes | Annual | Detailed advertising review |
| Illinois | Yes — AG | Yes — Franchise Disclosure Act | Annual | Relationship law protections |
| Maryland | Yes — AG | Yes | Annual | Broad relationship protections |
| Minnesota | Yes — Commerce | Yes | Annual | Cannot waive jury trial |
| Virginia | Yes — SCC | No | Annual | Review-intensive process |
| Washington | Yes — DFI | Yes — Franchise Investment Protection Act | Annual | Strong termination protections |
| Wisconsin | Yes — Securities | Yes — Fair Dealership Law | Annual | Broadest dealership protections |
| Indiana | Yes — Securities | Yes — Deceptive Franchise Practices Act | Annual | Venue/choice-of-law restrictions |
| Hawaii | Yes — Commerce | Yes | Annual | Pre-sale escrow may be required |
| Rhode Island | Yes | Yes | Annual | |
| South Dakota | Yes — Securities | No | Annual | |
| North Dakota | Yes — Securities | Yes | Annual | Strong franchisee protections |

**Filing States** (file FDD, no substantive review):

| State | Filing Type | Notes |
|---|---|---|
| Connecticut | Notice filing | AG office |
| Florida | Annual filing | DBPR — advertising filing required |
| Kentucky | Filing — no review | AG office |
| Nebraska | Filing | Securities bureau |
| Texas | Filing with exemptions | Business opportunity act — analyze if franchise or biz opp |
| Utah | Filing | Commerce |
| Oregon | Filing | Securities |
| Michigan | Notice filing | AG — relationship law also |

**No Registration States**: All other states (AL, AK, AZ, AR, CO, DE, GA, ID, IA, KS, LA, ME, MA, MS, MO, MT, NV, NH, NJ, NM, NC, OH, OK, PA, SC, TN, VT, WV, WY, DC).

### 8. International Franchise Regulation Mapping

| Jurisdiction | Disclosure Required | Registration Required | Relationship Law | Key Regulation | Typical Timeline |
|---|---|---|---|---|---|
| **United States** | Yes — FDD (FTC Rule 436) | State-by-state (see above) | State-by-state | FTC Franchise Rule 16 CFR 436 | 14-day waiting period |
| **Canada — Alberta** | Yes | Yes — Fair Trading Act | Yes | Franchises Act (Alberta) | 14-day waiting period |
| **Canada — Ontario** | Yes | No registration | Yes — right of rescission | Arthur Wishart Act | 14-day cooling off |
| **Canada — Other provinces** | AB, BC, MB, NB, ON, PEI have franchise laws | Varies by province | Yes in regulated provinces | Provincial franchise statutes | Province-specific |
| **United Kingdom** | No mandatory FDD | No | Limited — contract law | BFA (self-regulation), Competition Act | No mandated waiting period |
| **European Union** | Varies by member state | Generally no | EU Competition rules apply | EU Block Exemption Regulation (vertical) | Pre-contractual disclosure varies |
| **France** | Yes — Loi Doubin | No | Yes | Code de Commerce Art. L330-3 | 20-day waiting period |
| **Australia** | Yes — Disclosure Document | No | Yes — Franchising Code of Conduct | Competition and Consumer Act 2010 | 14-day waiting period |
| **China** | Yes | Yes — MOFCOM | Yes | Commercial Franchise Admin Regulations | 20-day waiting period, 2+ units required |
| **Japan** | Yes — for retail/service | No | Limited | Medium and Small Retail Commerce Act | Disclosure before signing |
| **South Korea** | Yes | Yes — KFTC | Yes | Fair Transactions in Franchise Business Act | 14-day waiting period |
| **UAE / Middle East** | Varies (UAE has no franchise law; Saudi, Bahrain emerging) | No (generally) | Limited — contract law | Civil/commercial code; agency law may apply | Agency law can create irrevocable rights |
| **India** | No franchise-specific law | No | Contract law applies | Indian Contract Act, IP registration | Brand registration essential |
| **Brazil** | Yes — Circular de Oferta de Franquia | No | Yes | Lei de Franquias (Law 13.966/2019) | 10-day waiting period |
| **Mexico** | Yes | Yes — NOM-information standard | Yes | Industrial Property Law, NOM-ROC | 30 days before signing |

### 9. Franchise Relationship Laws

**State-by-state franchise relationship law provisions:**

| Protection | States Providing | Impact |
|---|---|---|
| Good faith and fair dealing | CA, CT, HI, IL, IN, IA, MI, MN, MS, MO, NE, NJ, WA, WI | Cannot act arbitrarily in exercising discretion |
| Termination only for good cause | AR, CA, CT, DC, HI, IL, IN, IA, MI, MN, MS, MO, NE, NJ, VA, WA, WI | Must demonstrate material breach or other statutory cause |
| Mandatory cure period before termination | Most relationship law states | 30-60 day cure for curable defaults |
| Non-renewal restrictions | CA, CT, HI, IL, IN, MN, NJ, WA, WI | Must provide notice and often good cause for non-renewal |
| Venue / choice-of-law restrictions | CA, IL, IN, MI, MN, RI, WA, WI | Cannot require out-of-state litigation; local law may apply regardless of choice |
| Prohibition on waiver of jury trial | MN, WI | Arbitration clauses may be unenforceable |
| Encroachment restrictions | HI, IL, WA | Cannot place competing unit unreasonably close |
| Sourcing restrictions | Several states | Cannot mandate suppliers without competitive justification |

### 10. Area Development Agreement Framework

**Key provisions for `{franchise_model}` = area_development:**

| Provision | Standard Terms | Negotiation Range |
|---|---|---|
| Development area | Defined geographic region | Larger area with phased access based on performance |
| Development schedule | X units open by specific dates | Flexibility: +/- 6 months per milestone |
| Development fee | 25-75% of aggregate franchise fees for committed units | Credited against individual franchise fees upon unit opening |
| Individual franchise agreements | Signed per unit at each opening | Pre-negotiated form locked at ADA signing |
| Performance requirements | Meet schedule + each unit meets minimum performance | Grace period for market disruption (e.g., pandemic clause) |
| Default and cure | Missed milestone = loss of remaining development rights | Right to cure by accelerating next unit opening |
| Reduced royalty/fees | Tiered reduction for volume commitment | 0.5-2% royalty reduction for 5+ unit commitment |
| ROFR on adjacent territory | Franchisor may grant | Developer earns ROFR after proving performance |

### 11. Master Franchise Agreement Framework

**Key provisions for `{franchise_model}` = master_franchise:**

| Provision | Standard Terms | Key Considerations |
|---|---|---|
| Territory grant | Country or major region | Phased: earn additional regions via performance |
| Sub-franchising rights | Master franchisee recruits and manages sub-franchisees | Sub-franchise agreement must mirror franchisor standards |
| Revenue sharing | Master franchisee collects royalties, remits portion to franchisor | Typical split: 50/50 on royalties, master keeps sub-franchise fees |
| Initial master franchise fee | $50K-$500K+ depending on territory | Covers territory exclusivity and training of master organization |
| Development schedule | Minimum units over defined timeline | Country-specific market analysis drives realistic targets |
| Quality control | Master franchisee conducts local audits per franchisor standards | Franchisor retains override audit rights |
| Training obligations | Master franchisee trains sub-franchisees | Franchisor trains master; master trains subs (train-the-trainer) |
| Term | 10-20 years (longer due to investment scale) | Renewal tied to development schedule compliance |
| Local adaptation | Right to adapt operations manual for local market | Approval process for material modifications |
| Regulatory compliance | Master franchisee handles local franchise law compliance | Including local FDD equivalent where required |

### 12. Compliance Calendar

| Task | Frequency | Deadline | Notes |
|---|---|---|---|
| FDD annual renewal | Annual | 120 days after fiscal year end | Update all 23 Items, new audited financials |
| State registration amendments | Annual per state | Varies by state (30-60 days after FDD renewal) | Registration states require re-filing |
| State registration renewals | Annual | Per state deadlines | Track each state's renewal date separately |
| Audited financial statements | Annual | Included in FDD renewal | Must be US GAAP, independent CPA |
| Item 20 outlet data update | Annual | Part of FDD renewal | Verify with franchisee records |
| Material change amendments | As needed | Filed before use (some states require pre-approval) | Changes to fees, territory, key personnel, litigation |
| Franchise agreement updates | As needed | Effective with next FDD renewal cycle | Material changes require FDD amendment |
| Advertising fund financial report | Annual | Per franchise agreement terms | Many states require separate accounting |
| Franchisee contact list update | Annual | Part of Item 20 | Include all current and former (within 1 year) franchisees |
| Trademark renewal | Per mark | Per USPTO schedule (Section 8/9 at years 5-6, then every 10) | International marks per local schedule |
| State business opportunity compliance | Annual | Per state | Some states classify certain franchises as business opportunities |
| International disclosure updates | Annual per jurisdiction | Per local law requirements | Each country has its own timing |

## Output Template

```markdown
## Franchise Legal Framework: [Franchise System Name]

### Engagement Parameters
| Variable | Value |
|---|---|
| Franchise Model | {franchise_model} |
| Territory Scope | {territory_scope} |
| Regulatory Domain | {regulatory_domain} |
| Business Model | {business_model} |
| Product Type | {product_type} |
| Revenue Model | {revenue_model} |
| Target Franchisee | {target_franchisee} |

### Executive Summary
[1-2 paragraphs summarizing legal readiness, key risks, and priority actions]

### FDD Readiness Assessment
| Item | Status | Priority Issues | Recommended Action |
|---|---|---|---|
| Item 1: Franchisor | [Ready/Needs Work/Not Started] | | |
| Item 2: Business Experience | | | |
| [Continue for all 23 Items] | | | |

### FDD Key Items Analysis
#### Item 5: Initial Fees
[Fee structure table tailored to {business_model}]

#### Item 7: Estimated Initial Investment
[Completed investment table with ranges]

#### Item 19: Financial Performance Representations
[Recommended approach with rationale]

#### Item 20: Outlet Analysis
[Unit growth/closure analysis with health assessment]

### Franchise Agreement Term Sheet
| Provision | Recommended Position | Rationale |
|---|---|---|
| Term length | | |
| Territory | | |
| Royalty | | |
| [Continue for all 10 provisions] | | |

### Territory Rights Structure
[Territory type recommendation with map/definition methodology for {franchise_model}]

### Non-Compete and Post-Term Covenants
[Recommended scope calibrated to target jurisdictions and enforceability]

### Registration Requirements
#### US State Requirements
[Table of required registrations/filings based on {territory_scope}]

#### International Requirements
[Applicable international jurisdictions with compliance requirements]

### Franchise Relationship Law Impact
[Analysis of relationship law implications for target states]

### Agreement Framework
[Area Development or Master Franchise framework if applicable to {franchise_model}]

### Compliance Calendar
[12-month calendar with all filing deadlines]

### Key Legal Risks and Mitigations
| Risk | Severity | Mitigation |
|---|---|---|
| [Risk 1] | High/Medium/Low | [Specific action] |

### Recommended Next Steps
1. [Immediate actions — 30 days]
2. [Short-term actions — 60-90 days]
3. [Ongoing compliance actions]

> **Disclaimer:** This analysis provides a strategic framework for franchise
> planning and operations. It does not constitute legal advice or a Franchise
> Disclosure Document. Franchise offerings require compliance with FTC Rule 436
> (US) and applicable state/country franchise laws. Implementation requires
> review by qualified franchise counsel.
```

## Quality Checks

- [ ] All 23 FDD Items addressed with status assessment and strategic advisory.
- [ ] Fee structures (Items 5, 6, 7) tailored to `{business_model}` with realistic ranges.
- [ ] Item 19 recommendation includes approach rationale and substantiation requirements.
- [ ] Item 20 outlet analysis includes red flag / healthy / best-in-class benchmarking.
- [ ] All 10 most-negotiated franchise agreement provisions analyzed with negotiation range.
- [ ] Territory rights structure matches `{franchise_model}` (not generic).
- [ ] Non-compete scope calibrated to target state enforceability.
- [ ] State registration map covers all registration, filing, and no-registration states.
- [ ] International regulation mapping covers jurisdictions relevant to `{territory_scope}`.
- [ ] Franchise relationship law analysis specific to target states.
- [ ] Area development or master franchise framework included when applicable to `{franchise_model}`.
- [ ] Compliance calendar includes all recurring deadlines with specific timing.
- [ ] Disclaimer included in output.
- [ ] No unresolved `{variable}` placeholders in final output — all parameters substituted.
