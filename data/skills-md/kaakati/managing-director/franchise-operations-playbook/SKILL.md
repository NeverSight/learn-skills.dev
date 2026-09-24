---
name: franchise-operations-playbook
description: >
  Generic parameterized franchise operations playbook engine for ANY business model
  and product type. Designs franchisee onboarding programs, customer/service delivery
  playbooks, tiered support models, quality assurance frameworks, and supply chain
  plans. Use when building franchise operations manuals, designing franchisee
  onboarding, creating customer delivery or implementation playbooks, setting up
  tiered support structures, establishing franchise quality and compliance audits,
  planning franchise supply chains, or generating operations SOPs for SaaS, retail,
  service, healthcare, fitness, food, education, or hybrid franchise systems.
---

# Franchise Operations Playbook (Parameterized)

A template engine that generates a complete franchise operations playbook tailored to
any business model, product type, and revenue model.

## Required Inputs

- **{business_model}**: One of `SaaS`, `physical_retail`, `service`, `hybrid`. Determines delivery workflow, support scope, supply chain, and milestone gates.
- **{product_type}**: Domain of the franchise offering — e.g., `software`, `food`, `education`, `healthcare`, `fitness`, `beauty`, `cleaning`, `automotive`. Drives terminology, training content, and compliance requirements.
- **{revenue_model}**: How revenue is generated — `subscription`, `transaction`, `licensing`, `retail`. Shapes sales enablement, pricing frameworks, and performance metrics.
- **Product/Service**: Capabilities, complexity, and delivery requirements of the franchise offering.
- **Franchise Model**: Territory structure, franchisee profile, support ratio.
- **Service Scope**: Responsibilities split between franchisee and franchisor.
- **Quality Standards**: Target SLAs, satisfaction targets, compliance requirements.

### Terminology Map

Resolve customer-facing language from `{business_model}` and `{product_type}`:

| business_model | Customer Term | Delivery Term | Location Term | Transaction Term |
|---|---|---|---|---|
| SaaS | client, account | implementation | territory | subscription |
| physical_retail | customer, guest | store experience | store, location | purchase, sale |
| service | client, patient, member | service delivery | service area | appointment, session |
| hybrid | client, customer | engagement | market, territory | contract, booking |

Use the resolved terms throughout all generated playbook sections.

## Execution Steps

### 1. Franchisee Onboarding Program (30/60/90 Day Ramp)

**Week 1-2: Foundation** (universal structure, {product_type}-adapted training)

- Business setup: entity formation, insurance, local business licenses.
- Platform/location access: admin portal credentials, tool provisioning, site access.
- Core training — adapts by `{product_type}`:
  - *software*: product knowledge certification, platform navigation, feature deep-dives.
  - *food*: food safety certification, recipe/menu mastery, equipment operation.
  - *healthcare*: clinical protocols, regulatory compliance (HIPAA/equivalents), equipment training.
  - *fitness*: program methodology certification, equipment safety, member assessment protocols.
  - *education*: curriculum mastery, pedagogy standards, student assessment tools.
  - *General*: product/service knowledge assessment (must pass >80%).
- Brand standards: visual identity, communication guidelines, co-branding rules.

**Week 3-4: Sales Enablement** (universal structure, {product_type}-specific ICP/demo)

- Sales playbook walkthrough: ICP definition (adapts to `{product_type}` target buyer), objection handling, demo/pitch script.
- CRM or POS setup and pipeline/funnel management training.
- Marketing toolkit: approved collateral, local marketing plan template.
- Pricing and quoting: contract/menu/rate templates, approval workflows.
- Shadow selling: ride-along with experienced franchisee or franchisor rep.

**Month 2: First Customers** (adapt "customer" per terminology map)

- Target: 2-3 prospects in pipeline, 1 signed/booked.
- First delivery: franchisor team leads, franchisee shadows.
  - *SaaS*: first client implementation.
  - *Retail*: soft-open operations under franchisor supervision.
  - *Service*: first client engagements with franchisor oversight.
- Support training: L1 ticketing/issue system, escalation procedures, SLA expectations.
- Weekly coaching calls with franchise development manager.

**Month 3: Independence**

- Target: 3-5 prospects in pipeline, 2-3 signed, 1 live/active.
- Franchisee leads delivery with franchisor oversight.
- Full responsibility for L1 support/issues in territory.
- First quality audit (baseline score, not graded).
- Graduation: formal sign-off that franchisee is operationally independent.

**Milestone Gates (Go/No-Go)** — adapt criteria by `{business_model}`:

| Gate | Timing | Universal Criteria | {business_model} Adaptation |
|---|---|---|---|
| Product/Service Certification | Day 14 | Pass knowledge assessment (>80%) | SaaS: platform demo cert. Retail: operations cert + food safety (if food). Service: methodology cert. |
| Sales Readiness | Day 30 | Complete pitch/demo certification, CRM/POS active | SaaS: live demo to mock client. Retail: POS proficiency test. Service: intake process walkthrough. |
| First Delivery | Day 60 | Successfully shadow 1 delivery cycle | SaaS: shadow implementation. Retail: supervised store shift. Service: supervised client engagement. |
| Operational Independence | Day 90 | 1+ active customer, L1 handling, audit baseline | SaaS: 1+ live account. Retail: store open, daily ops independent. Service: 1+ recurring client. |

**Consequence of Gate Failure** (universal): extend training period, delay territory activation, additional supervised practice, reassess at +7 days.

### 2. Customer/Service Delivery Playbook (Template Engine)

Generate the appropriate delivery playbook from `{business_model}`. All models follow a universal arc: **Intake → Setup → Delivery → Stabilization → Steady-State**.

---

**SaaS: Implementation Playbook**

| Phase | Timing | Activities | Owner |
|---|---|---|---|
| Discovery & Planning | Week 1-2 | Stakeholder mapping, requirements gathering, success criteria, implementation plan (RACI) | Franchisee + Client |
| Configuration & Migration | Week 3-6 | Platform config, data migration, integration setup, UAT | Franchisee (+ Franchisor if complex) |
| Training & Go-Live | Week 7-8 | Admin training, end-user training, go-live (parallel or cutover), hypercare (2 weeks) | Franchisee |
| Stabilization | Week 9-12 | Weekly check-ins, issue resolution, adoption tracking (DAU/MAU), success review, handoff to support | Franchisee |

---

**Physical Retail: Store Opening Playbook**

| Phase | Timing | Activities | Owner |
|---|---|---|---|
| Site Buildout | Week 1-6 | Construction/renovation, brand buildout, permits, inspections | Franchisee + Franchisor construction team |
| Equipment & Inventory | Week 7-8 | Equipment install, initial inventory receipt, POS setup, staff hiring/training | Franchisee |
| Soft Open | Week 9-10 | Friends & family events, operational dry-runs, process tuning | Franchisee + Franchisor ops |
| Grand Open | Week 11 | Marketing blitz, launch event, full operations | Franchisee |
| Stabilization | Week 12-16 | Daily ops review, staffing adjustments, inventory optimization, customer feedback loops | Franchisee |

---

**Service: Service Delivery Playbook**

| Phase | Timing | Activities | Owner |
|---|---|---|---|
| Client Intake | Day 1-3 | Initial consultation, needs assessment, qualification | Franchisee |
| Assessment & Planning | Day 4-7 | Detailed assessment, service plan creation, pricing/scope agreement | Franchisee |
| Service Delivery | Ongoing | Execute service plan, milestone check-ins, progress tracking | Franchisee |
| Follow-Up & Review | Post-delivery | Outcome review, satisfaction survey, maintenance/renewal plan | Franchisee |
| Retention | Ongoing | Regular check-ins, upsell opportunities, referral program | Franchisee |

---

**Hybrid: Blended Delivery Playbook**

Combine applicable phases from SaaS (digital component) and Retail or Service (physical component). Sequence: physical setup runs in parallel with digital configuration; unified go-live; single stabilization period covering both channels.

### 3. Tiered Support Model

Universal L1/L2/L3/Emergency structure with scope adapted by `{business_model}`:

| Tier | Owner | Universal Scope | SLA (Response / Resolution) |
|---|---|---|---|
| **L1: Basic** | Franchisee | Basic questions, how-to, simple issues, account/user management | 4 hrs / 24 hrs |
| **L2: Complex** | Franchisor support team | Complex issues, technical/operational problems, escalated complaints | 8 hrs / 48 hrs |
| **L3: Systemic** | Franchisor engineering/ops | Systemic issues, product/infrastructure bugs, architecture problems | 4 hrs (critical) / per severity |
| **Emergency** | Franchisor on-call | Outages, safety incidents, data breaches, regulatory emergencies | 15 min / immediate |

**Business-Model-Specific L1 Examples**

| Tier | SaaS | Retail | Service | Healthcare |
|---|---|---|---|---|
| L1 | Password resets, how-to, basic config | Register issues, product questions, simple returns | Scheduling, basic service questions | Appointment booking, portal access |
| L2 | Integration failures, data issues, complex config | Equipment malfunction, inventory system errors, vendor disputes | Complex service complaints, staff issues | Clinical system errors, compliance questions |
| L3 | Platform bugs, security, architecture | Supply chain failures, POS platform issues | Methodology/protocol issues, systemic quality | Regulatory violations, clinical system failures |
| Emergency | Platform outage, data breach | Safety incident, health code violation | Client safety incident, legal/liability | Patient safety, regulatory emergency |

**Escalation Matrix** (universal)

| Trigger | From | To | Notification |
|---|---|---|---|
| L1 unresolved > 24 hrs | Franchisee | Franchisor L2 | Automatic ticket escalation |
| Customer threatens churn/complaint | Franchisee | Franchise development manager | Immediate call + action plan |
| Safety/data incident suspected | Anyone | Franchisor security/safety team | Immediate + incident protocol |
| SLA breach | System detection | Franchisor operations | Automatic alert + root cause |
| Repeated L1 same issue (pattern) | Pattern detection | Franchisor product/ops team | Bug report or training gap analysis |

### 4. Quality Assurance & Compliance Audit Framework

**Quarterly Franchise Audit Scorecard** (universal structure, metrics adapt by `{business_model}`)

| Category | Weight | Universal Metrics | Pass Threshold |
|---|---|---|---|
| Customer Satisfaction | 25% | NPS, CSAT, retention rate | NPS > 40 |
| Delivery Quality | 20% | On-time delivery %, accuracy/defect rate, completion rate | > 85% on-time |
| Support Performance | 20% | L1 resolution rate, SLA compliance, escalation rate | > 90% SLA met |
| Sales Performance | 15% | Pipeline activity, conversion rate, revenue vs. target | > 70% of target |
| Compliance | 10% | Brand standards, regulatory, data/safety, contract compliance | 100% critical items |
| Operations | 10% | Reporting timeliness, system usage, training currency | > 90% compliance |

**Metric Customization by {business_model}**

- *SaaS*: Delivery Quality = on-time go-live %, data migration accuracy, adoption (DAU/MAU). Customer Satisfaction includes product NPS.
- *Retail*: Delivery Quality = mystery shop score, health/safety inspection pass rate, inventory accuracy. Add food safety or product quality metrics if applicable.
- *Service*: Delivery Quality = service outcome scores, client goal attainment %, on-time appointment rate. Customer Satisfaction includes service-specific CSAT.
- *Healthcare*: Add clinical quality metrics, regulatory compliance scores, patient outcome measures. Compliance weight increases to 20% (reduce Sales to 10%, Operations to 5%).

**Audit Process** (universal)

1. Self-assessment submitted by franchisee (monthly KPI reporting).
2. Franchisor remote audit (quarterly — dashboard review, ticket/record sampling).
3. Franchisor on-site audit (annually — full operational review).
4. Mystery shopping / secret client (semi-annually — test sales inquiry and support).

**Corrective Action Protocol** (universal)

| Score | Status | Action | Timeline |
|---|---|---|---|
| 90-100% | Exemplary | Recognition, case study opportunity | N/A |
| 75-89% | Satisfactory | Improvement plan for weak areas | 90 days |
| 60-74% | At Risk | Mandatory improvement plan, increased monitoring | 60 days |
| < 60% | Critical | Performance remediation, potential default notice | 30 days |

### 5. Supply Chain & Materials Matrix

Generate the materials/supply plan from `{business_model}`:

**SaaS**

| Item | Purpose | Sourcing | Inventory Model |
|---|---|---|---|
| Training kits | Franchisee onboarding | Centrally produced | Ship on franchise signing |
| Branded collateral | Client presentations, events | Approved print vendors | Order on demand |
| Demo devices | Product demonstrations | Centrally procured | 2 per franchise unit |
| Event materials | Trade shows, conferences | Central design, local print | Seasonal ordering |
| Welcome packages | New client onboarding | Centrally produced | Ship per implementation |

**Physical Retail**

| Item | Purpose | Sourcing | Inventory Model |
|---|---|---|---|
| Raw materials / ingredients | Product production | Approved supplier network | Par-level replenishment |
| Packaging | Product packaging, bags | Centrally designed, bulk order | Monthly shipment |
| POS equipment | Transaction processing | Centrally procured | Ship on store opening |
| Uniforms | Staff branding | Approved vendor | Order per hire |
| Signage & fixtures | Store branding | Centrally produced | Ship on buildout |
| Consumables | Daily operations | Approved suppliers | Weekly/bi-weekly reorder |

**Service**

| Item | Purpose | Sourcing | Inventory Model |
|---|---|---|---|
| Tools / equipment | Service delivery | Approved vendors or central procurement | Ship on franchise signing |
| Branded materials | Client-facing collateral, forms | Central design, local print | Order on demand |
| Uniforms | Staff branding | Approved vendor | Order per hire |
| Consumables | Service delivery (cleaning supplies, medical supplies, etc.) | Approved suppliers | Par-level replenishment |
| Client welcome kits | New client onboarding | Centrally produced | Ship per engagement |

**Hybrid**: Combine SaaS digital materials with the applicable physical model above. Ensure a unified ordering portal or system that covers both digital provisioning and physical procurement.

## Output Template

```markdown
## Franchise Operations Playbook: [Product/Brand Name]
### Parameters: {business_model} | {product_type} | {revenue_model}

### 1. Franchisee Onboarding Program
[30/60/90 day plan with milestone gates adapted to {business_model}]

### 2. [Customer Term] Delivery Playbook
[Delivery phases generated from {business_model} template — include timeline and RACI]

### 3. Tiered Support Model
[L1/L2/L3/Emergency with SLAs and escalation matrix, scoped to {business_model}]

### 4. Quality Assurance Framework
[Audit scorecard with {business_model}-specific metrics, audit process, corrective actions]

### 5. Supply Chain & Materials Plan
[Materials matrix generated from {business_model}]

### Appendices
- A: Franchisee onboarding checklist (adapted to {product_type})
- B: [Customer term] delivery checklist (generated from {business_model})
- C: L1 support knowledge base structure
- D: Audit self-assessment template
```

## Quality Checks

- All `{business_model}`, `{product_type}`, and `{revenue_model}` parameters are resolved — no unresolved placeholders in final output.
- Customer-facing terminology is consistent with the terminology map throughout.
- 30/60/90 onboarding includes measurable milestone gates with {business_model}-specific criteria and consequences.
- Delivery playbook matches the selected {business_model} template (not a generic fallback).
- Support model defines specific SLAs in hours (not vague terms like "timely").
- Escalation matrix covers both operational and crisis/safety scenarios.
- Audit scorecard metrics are customized to {business_model} — not generic placeholders.
- Corrective action protocol has defined score thresholds and remediation timelines.
- Supply chain matrix matches {business_model} — SaaS does not list raw materials; retail does not list demo devices.
- Compliance section accounts for {product_type}-specific regulations (HIPAA, food safety, etc.).
