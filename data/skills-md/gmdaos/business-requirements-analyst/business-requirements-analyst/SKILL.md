---
name: business-requirements-analyst
description: Complete methodology for software and business requirements gathering. Use when you need to document a new project, validate a business idea, create technical specifications, or generate complete documentation covering business vision, stakeholders, processes, functional and non-functional requirements, data model, integrations, risks, and roadmap. Ideal for projects requiring quoting, development, delegation, or presentation to investors.
license: MIT
metadata:
  author: github.com/gmdaos
  version: '2.0.0'
---

# Requirements Gathering

This Skill provides a professional and complete methodology for conducting requirements gathering that covers all business layers, not just "the app" or "the system."

## Fundamental Principle

**Requirements gathering is NOT just a list of functionalities.**

Good requirements gathering covers all business layers:

- 🧠 Idea and objective
- 👥 Users
- 💼 Operation
- 💰 Money
- ⚙️ Technology
- ⚠️ Risks
- 📈 Growth
- 🔗 **Traceability** (from Business to Code)
- ⚖️ **Quality Gates** (Validation standards)

## Available Methodologies

### 1. Design Thinking (for new ideas)

**Ideal when:**

- The idea is still being validated
- Not everything is clear
- You want to truly understand the user

**Phases:**

1. **Empathize** - Understand users
2. **Define** - Identify key problems
3. **Ideate** - Generate solutions
4. **Prototype** - Create early versions
5. **Test** - Validate with real users

**Note:** Used to discover what to build, not to document everything.

### 2. Business Analysis (BABOK)

**The most complete and professional.**

**Covers:**

- Business requirements
- Functional requirements
- Non-functional requirements
- Business rules
- Stakeholders
- Processes

**Note:** This is what's used to create formal documents.

### 3. Lean / Startup Canvas (quick vision)

**Useful for:**

- Organizing the idea
- Seeing if the business makes sense

**⚠️ Important:** DOES NOT replace complete requirements gathering.

## Recommended Approach

Combine 3 key elements:

1. **Business vision**
2. **Processes**
3. **System / product**
4. **Traceability & Validation** (Ensure everything is connected and meets quality standards)

And document everything in a **single master artifact** or a structured layer system.

## Structure of the Complete Requirements Document

### 📌 1. Business Vision

Include:

- **Problem solved** - What pain or need does it address?
- **Value proposition** - Why is it better than alternatives?
- **Business objective** - Clear and measurable goals
- **Main KPIs** - Success metrics
- **Scope** - What IS and what is NOT included

**Format example:**

```markdown
## Business Vision

### Problem

[Description of the problem being solved]

### Value Proposition

[What makes this product/service unique]

### Objectives

- Objective 1: [Description]
- Objective 2: [Description]

### KPIs

- KPI 1: [Specific metric]
- KPI 2: [Specific metric]

### Scope

**Includes:**

- [Element 1]
- [Element 2]

**Does not include:**

- [Element 1]
- [Element 2]
```

### 📌 2. Stakeholders

Identify all involved actors:

- **Business owners** - Who makes decisions
- **End users** - Who will use the system
- **Administrators** - Who will manage the system
- **Suppliers** - External services or products
- **Third parties** - Payments, logistics, integrations, etc.

**Suggested format:**

```markdown
## Stakeholders

| Type  | Name/Role | Interest          | Influence         |
| ----- | --------- | ----------------- | ----------------- |
| Owner | [Name]    | [High/Medium/Low] | [High/Medium/Low] |
| User  | [Type]    | [High/Medium/Low] | [High/Medium/Low] |
```

### 📌 3. User Types (Personas)

For each user type, document:

- **What they need** - Key functionalities
- **What pain they have** - Current problems
- **What they expect from the system** - Expectations

**Example:**

```markdown
## Personas

### End Customer

- **Needs:** Make fast and secure purchases
- **Pain:** Complicated checkout processes
- **Expectation:** Checkout in less than 3 clicks

### Administrator

- **Needs:** Manage inventory and orders
- **Pain:** Lack of real-time visibility
- **Expectation:** Dashboard with updated metrics
```

### 📌 4. Business Processes

**⚠️ VERY IMPORTANT - This is where many fail.**

Document complete flows:

- How a customer enters
- How a sale is generated
- How payment is collected
- What happens if the payment fails
- How a claim is handled

**Express as step-by-step flows:**

```markdown
## Process: Product Purchase

1. User browses catalog
2. User adds products to cart
3. User proceeds to checkout
4. System validates availability
5. User enters payment details
6. System processes payment
   - **If success:** Confirms order and sends email
   - **If failure:** Shows error and allows retry
7. System generates shipping order
8. User receives confirmation
```

For complex processes, see [references/process-mapping.md](references/process-mapping.md).

### 📌 5. Functional Requirements

Standard format:

- **FR-01:** The system must allow...
- **FR-02:** The user will be able to...

**Common categories:**

- User registration
- Order management
- Payments
- Notifications
- Reports

**Example:**

```markdown
## Functional Requirements

### Authentication

- **FR-01:** The system must allow registration with email and password
- **FR-02:** The system must send a verification email
- **FR-03:** The user will be able to recover a forgotten password

### Order Management

- **FR-04:** The user will be able to view order history
- **FR-05:** The system must allow canceling orders in "pending" status
```

### 📌 6. Non-Functional Requirements

**This separates the amateur from the professional.**

Key areas:

- **Security** - Authentication, authorization, encryption
- **Performance** - Response times, capacity
- **Scalability** - Expected growth
- **Availability** - Uptime, redundancy
- **Legal compliance** - GDPR, data protection
- **UX / Usability** - Accessibility, responsive

**Example:**

```markdown
## Non-Functional Requirements

### Performance

- **NFR-01:** The system must respond in < 2 seconds for 95% of requests
- **NFR-02:** The system must support 1000 concurrent users

### Security

- **NFR-03:** All passwords must be hashed with bcrypt
- **NFR-04:** Communications must use HTTPS/TLS 1.3

### Compliance

- **NFR-05:** The system must comply with GDPR for European user data
```

### 📌 7. Business Rules

Domain-specific logic:

**Examples:**

```markdown
## Business Rules

- **BR-01:** An order cannot be canceled after 30 minutes of creation
- **BR-02:** A user can only have one active plan at a time
- **BR-03:** Commissions are calculated as 5% of the total amount
- **BR-04:** Taxes are applied according to the buyer's region
```

### 📌 8. Data Model (High Level)

**Conceptual, not SQL yet.**

Document:

- **Primary entities** - User, Order, Product, etc.
- **Relationships** - One to many, many to many
- **Critical data** - Essential fields

**Example:**

```markdown
## Data Model

### Primary Entities

**User**

- id (PK)
- email (unique)
- name
- registration_date

**Order**

- id (PK)
- user_id (FK)
- status
- total
- creation_date

**Product**

- id (PK)
- name
- price
- stock

### Relationships

- A User can have many Orders (1:N)
- An Order can contain many Products (N:M)
```

For complex models, see [references/data-modeling.md](references/data-modeling.md).

### 📌 9. Integrations

Necessary external services:

- **Payment gateways** - Stripe, PayPal, etc.
- **External APIs** - Third-party services
- **Third-party services** - Email, SMS, analytics

**Example:**

```markdown
## Integrations

### Payment Gateway

- **Provider:** Stripe
- **Functionality:** Credit card processing
- **Data exchanged:** Amount, currency, card token

### Email Service

- **Provider:** SendGrid
- **Functionality:** Sending notifications
- **Data exchanged:** Recipient, subject, HTML body
```

### 📌 10. Risks and Assumptions

Identify potential problems:

- **Technical risks** - Dependencies, scalability
- **Legal risks** - Compliance, privacy
- **Business assumptions** - Assumptions that must be validated

**Example:**

```markdown
## Risks

### Technical

- **R-01:** Dependency on external API may cause downtime
  - _Mitigation:_ Implement caching and fallback system

### Legal

- **R-02:** Changes in data protection regulation
  - _Mitigation:_ Modular design for rapid adaptation

## Assumptions

- **S-01:** Users have stable internet access
- **S-02:** Initial volume will not exceed 10,000 users
```

### 📌 11. Roadmap / Phases

Divide into manageable stages:

**Example:**

```markdown
## Roadmap

### MVP (Phase 1) - 3 months

- Registration and authentication
- Product catalog
- Shopping cart
- Basic payment with Stripe

### Phase 2 - 2 months

- Notifications system
- Order history
- Basic administration panel

### Phase 3 - 3 months

- Advanced reports
- Logistics integration
- Recommendations system
```

### 📌 12. Architecture Decision Records (ADR)

Document critical technical decisions to preserve context.

**Example:**

- **ADR-001:** Use PostgreSQL for relational data integrity.
- **ADR-002:** Implement Redis for real-time notification caching.

See [references/adr-template.md](references/adr-template.md) for details.

### 📌 13. Traceability Matrix & Tags

Embed cumulative tags to bridge the gap between requirements and implementation.

**Format:** `@brd: BRD.01.01 @req: REQ-001`

See [references/traceability-guide.md](references/traceability-guide.md).

### 📌 14. Quality Gates & Score

Evaluate the maturity of the documentation before proceeding.

- **Maturity Level:** [0-100%]
- **Status:** [Draft | Ready for Dev | Approved]
- **Missing Items:** List of gaps to be filled.

## Gathering Process (Step by Step)

### 0. Process Kickoff & Roadmap

**Instruction:** At the very beginning of the interaction, you MUST:

1.  **Introduce yourself:** Briefly explain you are a Business Requirements Analyst using a professional methodology.
2.  **Present the Roadmap:** Explain the 6 phases you will follow (Discovery → Vision → Processes → Functional/Non-Functional → Data Model → Roadmap) so the user knows what to expect.
3.  **Acknowledge Documentation:** If the user has provided files or previous context, state that you will analyze them first to avoid asking for information already provided.

### 1. Discovery & Context Analysis (Smart Discovery)

**Instruction:**

- **Analyze First:** Before asking any questions, scan all provided files (images, text, documents).
- **Find Gaps:** Extract all possible information (Stakeholders, Problem, Goals) from the context.
- **Zero Redundancy Rule:** Never ask "What is the problem?" if it's already in the documents. Instead, validate: "I've analyzed the documents and understood the problem as [X]. Is that correct?".

### 2. Interviews & Deep Dive

**Instruction:** Focus only on the gaps. **Even if you are the stakeholder yourself**, perform the exercise of answering:

- What problem does this solve?
- Who will use it?
- How will they use it?
- What alternatives exist?
- Why is this better?

### 2. Uncomfortable Questions

**Fundamental for discovering edge cases:**

- What happens if the payment fails?
- What happens if the user loses connection?
- What happens if there is duplicate data?
- What happens if the external service is down?

### 3. Diagram Flows

Create visual diagrams of:

- User flows
- Business processes
- System architecture

### 4. Write → Validate → Adjust

**Iterative process:**

1. Write the first version of the document
2. Review with stakeholders
3. Identify gaps and ambiguities
4. Adjust and refine
5. Repeat until consensus is reached

### 5. Entity & Data Model Synthesis (Auto-ERD)

**Instruction:**

- **Active Extraction:** Throughout the entire process, identify all key entities mentioned (e.g., Orders, Users, inventory items).
- **Auto-Generation:** At the end of the analysis, if entities were detected, generate the Data Model section automatically.
- **Visual Diagram:** You MUST include a visual Entity-Relationship Diagram using **Mermaid.js** syntax for better clarity.

### 6. Living Document

**Keep it updated:**

- Use Markdown format for versioning
- Tools: Notion, Confluence, GitHub Wiki
- Update when requirements change

## Complete Template

For a ready-to-use template, see [assets/requirements-template.md](assets/requirements-template.md).

## Final Result

When you finish the complete gathering, you have:

- ✅ **Document for development** - Clear specifications
- ✅ **Basis for quoting** - Defined scope
- ✅ **Guide for delegating** - Complete instructions
- ✅ **Material to present** - To partners or investors

## Important Tips

1. **Don't start by writing requirements** - Start by understanding the business as if it already existed
2. **Be specific** - "Fast" is not a requirement, "< 2 seconds" is
3. **Include the "why"** - Not just the "what," but the reason behind it
4. **Document decisions** - Why a certain technology or approach was chosen
5. **Keep updated** - An outdated document is worse than no document at all

## Additional References

For advanced techniques and specific examples:

- **Complex process mapping:** [references/process-mapping.md](references/process-mapping.md)
- **Advanced data modeling:** [references/data-modeling.md](references/data-modeling.md)
- **Detailed use cases:** [references/use-cases.md](references/use-cases.md)
- **EARS Methodology:** [references/ears-methodology.md](references/ears-methodology.md)
- **ADR Templates:** [references/adr-template.md](references/adr-template.md)
- **Traceability Guide:** [references/traceability-guide.md](references/traceability-guide.md)
