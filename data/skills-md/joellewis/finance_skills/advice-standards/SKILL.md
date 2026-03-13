---
name: advice-standards
description: "Determine when a product, platform, or communication crosses the regulatory line from education into investment advice requiring registration. Use when the user asks about the definition of investment advice under the Advisers Act, whether a fintech feature or AI chatbot constitutes advice, the publisher's exclusion for newsletters or model portfolios, broker-dealer solely incidental exclusion, what triggers a 'recommendation' under Reg BI, or DOL education vs advice safe harbors. Also trigger when users ask 'do I need to register as an investment adviser', 'does this app give investment advice', 'is this tool just education or advice', 'robo-adviser registration', or 'disclaimer language for financial content'."
---

# Investment Advice Standards & Regulatory Boundaries

## Purpose
This skill covers the critical regulatory distinctions between investment education, general information, recommendations, and investment advice under the Investment Advisers Act of 1940, Regulation Best Interest, and related federal and state frameworks. It provides the analytical tools to determine when a person, platform, or algorithm crosses the line from permissible education or information into regulated investment advice requiring registration, and the compliance consequences of getting that determination wrong.

## Layer
9 — Compliance & Regulatory Guidance

## Direction
prospective

## When to Use
- When evaluating whether a product, platform, tool, or AI application constitutes providing "investment advice" under the Advisers Act
- When designing fintech features that operate near the education/advice boundary
- When determining whether an individual or entity must register as an investment adviser
- When assessing whether broker-dealer communications constitute "recommendations" under Reg BI
- When building robo-advisory tools, AI chatbots, or digital platforms that discuss investments
- When analyzing whether content (newsletters, blogs, model portfolios, AI-generated text) qualifies for the publisher's exclusion
- When evaluating whether financial planning services cross into investment advice
- When assessing DOL education vs. advice safe harbors for ERISA retirement plans
- When a user asks "do I need to register as an investment adviser?"
- When a user asks "does this feature/tool/app constitute investment advice?"
- When reviewing disclaimers, disclosures, or terms of service for advice-boundary language

## Core Concepts

### The Statutory Definition: Investment Advisers Act Section 202(a)(11)
Under Section 202(a)(11) of the Investment Advisers Act of 1940 (15 U.S.C. Section 80b-2(a)(11)), an "investment adviser" is any person who, for compensation, engages in the business of advising others, either directly or through publications or writings, as to the value of securities or as to the advisability of investing in, purchasing, or selling securities. The SEC applies a three-prong test, all of which must be satisfied:

1. **Advice prong:** The person provides advice, counsel, analyses, or reports concerning securities. This is interpreted broadly. It includes recommendations about specific securities, asset classes, portfolio construction, and the advisability of investing in securities generally.

2. **Business prong:** The advice is provided as part of a regular business activity. This does not require that advising be the person's primary business — it need only be a regular, and not isolated, activity. The SEC has stated that even a single instance of advice can satisfy this prong if the person holds themselves out as providing advisory services. See SEC Release IA-1092 (1987).

3. **Compensation prong:** The person receives compensation for the advice. Compensation is construed broadly and need not be a separate, direct fee for advisory services. It can include commissions, transaction-based compensation, soft dollars, or any economic benefit received in connection with the advisory activity. Receiving compensation for a bundled service that includes advice satisfies this prong.

All three prongs must be met. However, the SEC applies each prong broadly, making the exclusions and safe harbors critically important in practice.

### The SEC's Functional Test: Substance Over Form
The SEC evaluates the advice question functionally, not formally. What matters is what a person or platform actually does, not how it labels its services. Calling a service "education," "information," or "tools" does not immunize it from being classified as investment advice if the substance of the communication is advisory in nature. See SEC v. Capital Gains Research Bureau, Inc., 375 U.S. 180 (1963) (establishing the broad, remedial purpose of the Advisers Act).

Key indicators the SEC considers:
- Whether the communication is tailored to the individual's specific financial situation
- Whether it includes a recommendation or suggestion to take specific action
- Whether a reasonable recipient would understand it as a call to action regarding a securities transaction
- Whether the provider exercises discretion or judgment on behalf of the client
- The degree of personalization involved

### The Solely Incidental Exclusion for Broker-Dealers: Section 202(a)(11)(C)
Broker-dealers are excluded from the definition of investment adviser under Section 202(a)(11)(C) if their advisory services are "solely incidental" to the conduct of their brokerage business and they receive no "special compensation" for the advice. Both conditions must be met.

**Solely incidental** means the advice is provided in connection with and reasonably related to the broker-dealer's primary business of effecting securities transactions. If a broker-dealer holds itself out as providing financial planning, investment advisory services, or asset management as a distinct service, the advice is likely not solely incidental.

**Special compensation** means separate, identifiable compensation for the advisory component, as distinguished from standard brokerage commissions. Asset-based fees, wrap fees, financial planning fees, and separate advisory charges all constitute special compensation.

**Interaction with Regulation Best Interest:** The adoption of Reg BI in 2019 (SEC Rule 15l-1, 17 CFR 240.15l-1) did not eliminate the solely incidental exclusion, but it significantly raised the standard of conduct for broker-dealer recommendations. Even where advice is solely incidental, broker-dealers must now satisfy Reg BI's Care Obligation, Disclosure Obligation, Conflict of Interest Obligation, and Compliance Obligation when making recommendations. The practical effect is that the solely incidental exclusion provides less regulatory shelter than it did under the prior suitability standard.

### The Publisher's Exclusion: Section 202(a)(11)(D)
Section 202(a)(11)(D) excludes from the investment adviser definition "the publisher of any bona fide newspaper, news magazine or business or financial publication of general and regular circulation." The SEC and courts have interpreted this exclusion through the Lowe v. SEC, 472 U.S. 181 (1985) framework:

- The publication must be of **general and regular circulation** — it is available to the public at large (or a broad subscriber base), not tailored to individual clients.
- The advice must be **impersonal** — it does not purport to tailor investment advice to the individual needs, objectives, or circumstances of specific recipients.
- The publication must be **bona fide** — it is not a sham publication used as a vehicle to provide personalized advisory services.

Model portfolios, newsletters, market commentary, and investment research published to a general audience without individual tailoring typically qualify. However, if the publisher also provides personalized follow-up advice, individual portfolio reviews, or tailored recommendations to specific subscribers, the exclusion is lost for those communications.

### The "Recommendation" Trigger Under Regulation Best Interest
Under Reg BI, a broker-dealer's obligations are triggered when it makes a "recommendation" to a retail customer. The SEC declined to define "recommendation" with a bright-line rule and instead applies a facts-and-circumstances test derived from prior FINRA guidance (particularly FINRA Regulatory Notice 11-02 and the legacy suitability rule framework).

A communication is a recommendation if, based on the content, context, and manner of presentation, a reasonable person in the customer's position would view it as a **suggested course of action** or a **call to action**. Factors include:
- Whether the communication is **reasonably individualized** to the customer rather than general in nature
- Whether it recommends a **specific security or investment strategy** involving securities
- Whether the communication is an **explicit or implicit suggestion** to buy, sell, hold, or adopt a particular strategy
- The **degree of tailoring** — more tailoring makes a recommendation more likely
- Whether the broker-dealer has **singled out** particular securities or strategies from a broader set

Communications that are purely educational, general market commentary, or responses to unsolicited orders generally do not constitute recommendations. However, even general communications can become recommendations depending on context — for example, if sent to a targeted subset of customers based on their account profiles.

### Financial Planning and the Advice Line
Financial planning — including retirement planning, estate planning, tax planning, and cash flow analysis — can cross into investment advice when it includes recommendations about investing in securities. The SEC has stated that a financial planner who recommends specific securities, asset allocations involving securities, or strategies for investing in securities is providing investment advice within the meaning of Section 202(a)(11). See SEC Release IA-1092.

The critical distinction:
- **Financial planning that does not involve securities advice** (e.g., budgeting, debt management, insurance analysis, tax return preparation) does not, by itself, require investment adviser registration.
- **Financial planning that includes recommendations about securities** — even if securities advice is a small component of a broader financial plan — triggers the Advisers Act definition.

Many states require financial planners to register as investment advisers if they hold themselves out as providing financial planning services, even absent specific securities recommendations, on the theory that the public reasonably expects financial planners to advise on securities.

### Robo-Advice and Digital Tools
The SEC has addressed digital investment advisory programs in several releases, most notably the February 2017 guidance update "Robo-Advisers" (IM Guidance Update No. 2017-02). Key principles:

- **Algorithmic portfolio construction and management constitutes investment advice.** If a digital tool collects information about an investor's financial situation, goals, and risk tolerance, and then provides a recommended portfolio allocation or specific securities recommendations, it is providing investment advice under Section 202(a)(11). The fact that the advice is generated by an algorithm rather than a human does not change the analysis.

- **Registration required.** Robo-advisers must register as investment advisers (or operate under the umbrella of a registered investment adviser) and comply with all fiduciary obligations of the Advisers Act.

- **Disclosure obligations.** Robo-advisers must clearly disclose the limitations of their algorithms, the scope of their advisory services, conflicts of interest (e.g., proprietary funds, revenue sharing), and the fact that the advice is algorithmically generated.

- **Suitability of algorithms.** The adviser must ensure its algorithm produces advice that is suitable and in the best interest of the client, and must conduct ongoing oversight of the algorithm's performance and outputs.

- **Mere tools vs. advisory services:** A tool that provides general educational content — such as a retirement savings calculator, a compound interest illustrator, or a general asset allocation questionnaire that does not recommend specific securities — may not constitute investment advice. But once the tool generates personalized recommendations tied to the user's inputs, it likely crosses the line.

### Education vs. Advice Safe Harbors (DOL Interpretive Bulletin 96-1)
Department of Labor Interpretive Bulletin 96-1 (29 CFR 2509.96-1) provides safe harbors for investment education in the ERISA retirement plan context. Although this bulletin applies to ERISA fiduciary status rather than the Advisers Act, its framework is widely referenced and influential. The bulletin identifies four categories of education that do not constitute "investment advice" under ERISA Section 3(21)(A)(ii):

1. **Plan information:** General information about the plan, its investment options, benefits of participation, and the effects of contribution changes.

2. **General financial and investment concepts:** Information about general investment principles such as risk and return, diversification, dollar cost averaging, compound interest, and tax-deferred investing. This education does not constitute advice as long as it is not tied to specific investment alternatives available under the plan.

3. **Asset allocation models:** Hypothetical asset allocation models — including pie charts and model portfolios based on assumptions about risk tolerance, time horizon, and investment objectives — that are presented as educational examples and not as individualized recommendations. The models must be accompanied by disclosures that they are hypothetical, that participants should consider their individual circumstances, and that other investment options are available.

4. **Interactive investment materials:** Questionnaires, worksheets, software, and similar tools that allow participants to estimate future retirement income, assess risk tolerance, or model hypothetical investment scenarios, provided the materials are based on generally accepted investment theories and do not recommend specific plan investment options.

The critical boundary: once a communication moves from general education to a **specific recommendation for a specific individual** based on their particular circumstances, it becomes advice.

### Impersonal vs. Personal Advice
Several regulatory frameworks distinguish between impersonal advice (advice not tailored to individual circumstances) and personal advice (advice tailored to a specific individual):

- **Federal:** The publisher's exclusion under Section 202(a)(11)(D) is the primary federal carve-out for impersonal advice. Additionally, Section 203A(b) and related rules provide that certain advisers providing impersonal advice through publications may be exempt from state registration requirements.

- **State:** Many states have carve-outs or reduced regulatory burdens for impersonal advice. For example, some states exempt from registration persons whose advice is limited to impersonal advice delivered through publications of general circulation, provided they have no individual client relationships.

- **Model portfolios and newsletters:** A model portfolio published to all subscribers without individual tailoring is generally impersonal advice. But a model portfolio that is adjusted for a specific subscriber's risk tolerance, tax situation, or financial goals becomes personal advice.

The line shifts when there is **any individualization** — responding to an individual's specific question about their portfolio, tailoring a model to their circumstances, or providing follow-up guidance based on their financial situation.

### AI-Generated Content and the Advice Boundary
The SEC and FINRA have increasingly focused on AI-generated content in the financial services context:

- **SEC AI risk alerts and statements (2023-2025):** The SEC has warned that AI tools providing personalized investment suggestions to retail investors may constitute investment advice, regardless of disclaimers. The SEC's Division of Examinations has identified AI-driven advice as an examination priority. Disclaimers stating "this is not investment advice" do not override the functional test — if the content is functionally advisory, it is advisory.

- **FINRA Regulatory Notice 24-09 (2024):** FINRA addressed the use of AI in broker-dealer communications, noting that AI-generated content distributed to customers is subject to the same supervisory and compliance requirements as human-generated content. If an AI tool generates a communication that constitutes a recommendation, the firm must ensure Reg BI compliance.

- **Conduct over disclaimers:** Both the SEC and FINRA have emphasized that disclaimers do not determine regulatory status. If an AI chatbot analyzes a user's financial situation and suggests specific investment actions, stating "this is for informational purposes only" does not prevent the communication from being classified as advice or a recommendation. The functional test governs.

- **Supervisory obligations:** Firms using AI tools must have supervisory systems reasonably designed to ensure that AI-generated outputs comply with applicable securities laws, including the Advisers Act and Reg BI. Firms cannot delegate compliance obligations to an algorithm.

### State Registration Triggers
Investment adviser registration operates at both the federal and state level:

- **Federal registration:** Required for advisers with $100 million or more in regulatory assets under management (AUM), or advisers to registered investment companies, among other categories. See Section 203A of the Advisers Act and SEC Rule 203A-1.

- **State registration:** Required for advisers with less than $100 million in AUM who do not qualify for federal registration. State registration is governed by individual state securities statutes (often modeled on the Uniform Securities Act).

- **De minimis exemptions:** Section 203(b)(3) of the Advisers Act provides an exemption from registration for advisers who (i) have fewer than 15 clients in a 12-month period, (ii) do not hold themselves out as investment advisers, and (iii) do not advise registered investment companies. Many states have analogous de minimis exemptions, but thresholds vary.

- **The "place of business" test:** Under NASAA and most state laws, an adviser's registration obligations are determined by where it has a "place of business" and where its clients are located. An adviser with a place of business in a state generally must register in that state. An adviser without a place of business in a state may be exempt under the state's de minimis rules if it has fewer than a specified number of clients in that state (commonly 5 or 6 within a 12-month period).

- **Internet and digital presence:** The SEC's internet investment adviser no-action letters (e.g., the 2002 SEC staff letter to NASAA) provide some guidance on when a website or digital tool creates a "place of business" in a state, but this area remains unsettled, particularly for AI-driven tools that may interact with users in all 50 states.

## Worked Examples

### Example 1: Fintech App Providing Personalized Portfolio Suggestions Without IA Registration
**Scenario:** A fintech startup launches a mobile app called "InvestSmart." Users complete a questionnaire about their age, income, risk tolerance, investment goals, and existing portfolio. The app's algorithm then generates a specific recommended portfolio allocation — for example, "Based on your profile, we recommend 60% U.S. equity index funds, 25% investment-grade bonds, 10% international equity, and 5% alternatives" — along with specific fund tickers (e.g., VTI, BND, VXUS). The app does not charge an advisory fee but monetizes through payment for order flow and revenue sharing with fund companies. The app's terms of service state: "InvestSmart does not provide investment advice."

**Compliance Issues:**
1. **Advice prong — met.** The app provides personalized recommendations about specific securities (index funds identified by ticker) tailored to the individual's financial situation, goals, and risk tolerance. This is advice about the "advisability of investing in securities" under Section 202(a)(11).
2. **Business prong — met.** The app is offered as a regular, ongoing service to the public. This is not an isolated instance.
3. **Compensation prong — met.** Although the app does not charge a direct advisory fee, it receives economic benefits (payment for order flow, revenue sharing) in connection with the advisory activity. The compensation prong is satisfied.
4. **Disclaimer irrelevant.** The terms of service disclaimer does not override the functional analysis. The SEC applies a substance-over-form test.
5. **Publisher's exclusion — not available.** The advice is personalized to each user, not impersonal advice of general circulation.

**Analysis:** InvestSmart is operating as an unregistered investment adviser in violation of Section 203(a) of the Advisers Act. The app must register as an investment adviser (or affiliate with a registered adviser), adopt compliance policies under Rule 206(4)-7, deliver Form ADV to users, satisfy fiduciary duties, and disclose its conflicts of interest (particularly the payment-for-order-flow and revenue-sharing arrangements that create incentives to recommend certain funds over others). The company also faces potential state registration requirements in every state where its users are located.

### Example 2: Content Platform Crossing From Education Into Advice
**Scenario:** A financial education website, "MoneyLearn," publishes articles, videos, and courses about investing concepts — diversification, compound interest, how to read financial statements, and general explanations of different asset classes. The content is available to all users without personalization. Over time, MoneyLearn adds a "Portfolio Checkup" feature: users can input their current holdings, and the platform provides a personalized analysis identifying "gaps" in their allocation and suggesting specific asset classes or funds to add. MoneyLearn also launches a premium tier where subscribers can submit questions and receive individualized responses from the editorial team about their specific portfolios.

**Compliance Issues:**
1. **Original educational content — not advice.** General articles and courses about investing concepts, available to all users, constitute financial education. They are impersonal, not tailored, and fall within both the publisher's exclusion and the DOL IB 96-1 safe harbors for general financial and investment concepts.
2. **Portfolio Checkup feature — likely advice.** The feature collects individualized information (the user's holdings) and provides personalized recommendations (specific gaps to fill, specific funds to consider). This is functionally identical to what a human investment adviser does and satisfies all three prongs of the Section 202(a)(11) test if MoneyLearn receives any form of compensation (e.g., subscription fees, advertising revenue, affiliate commissions for fund recommendations).
3. **Premium Q&A — advice.** Individualized responses to specific questions about a subscriber's portfolio are paradigmatic investment advice. This cannot qualify for the publisher's exclusion because it is personal, not impersonal.

**Analysis:** MoneyLearn crossed the line from education to advice when it introduced the Portfolio Checkup and premium Q&A features. The company should either (a) register as an investment adviser and comply with the Advisers Act, (b) restructure the features to remove individualization (e.g., provide only general asset allocation models with appropriate disclaimers per DOL IB 96-1 safe harbor), or (c) partner with a registered investment adviser that assumes the advisory function and fiduciary obligations. The educational content can continue without registration, but it must be clearly separated from the advisory features.

### Example 3: Broker-Dealer Using AI-Generated Talking Points That Constitute Recommendations
**Scenario:** A registered broker-dealer deploys an internal AI tool that generates client-facing "conversation starters" for its registered representatives. Before a client meeting, the representative inputs the client's account profile (holdings, risk score, recent activity, stated goals). The AI tool produces a set of tailored talking points, such as: "Given the client's moderate risk tolerance and approaching retirement date, consider discussing a shift from growth equities to dividend-paying stocks and investment-grade bond funds. Specific options: DVY, SCHD, AGG." The firm's compliance department has reviewed the AI tool's general methodology but does not pre-review individual outputs. The firm classifies the tool as a "productivity aid" rather than a recommendation engine.

**Compliance Issues:**
1. **Recommendation under Reg BI — yes.** The AI-generated talking points are tailored to the individual client's profile and suggest specific securities. If the registered representative communicates these suggestions to the client, the communication constitutes a recommendation under Reg BI's facts-and-circumstances test. A reasonable person in the client's position would view "consider shifting to DVY, SCHD, AGG" as a call to action.
2. **Firm classification irrelevant.** Calling the tool a "productivity aid" does not change the regulatory analysis. The SEC applies a functional test. If the tool's output is a recommendation, it is subject to Reg BI.
3. **Supervisory failure.** Under Reg BI's Compliance Obligation and FINRA Rules 3110 and 3120, the firm must establish and maintain a supervisory system reasonably designed to ensure compliance. Not pre-reviewing AI-generated outputs that are used in client communications is a supervisory deficiency. The firm is responsible for the content of the AI's outputs just as it would be for a human analyst's recommendations.
4. **Care Obligation.** Under Reg BI's Care Obligation, the firm and its representatives must have a reasonable basis for the recommendation, consider the client's investment profile, and ensure the recommendation is in the client's best interest. The firm must validate that the AI's recommendations meet this standard, which requires substantive review of the algorithm's logic and outputs.
5. **Conflict of Interest Obligation.** If the AI tool is more likely to recommend proprietary products, revenue-sharing partners, or higher-commission products, the firm has a conflict of interest that must be identified, disclosed, and mitigated or eliminated under Reg BI.

**Analysis:** The firm must treat the AI tool's outputs as recommendations subject to the full requirements of Reg BI. This means: (a) implementing pre-use or concurrent supervisory review of AI-generated talking points before they reach clients, (b) validating the AI algorithm against the Care Obligation's reasonable-basis, customer-specific, and quantitative standards, (c) identifying and addressing any conflicts embedded in the algorithm's design, (d) training registered representatives that AI-generated suggestions are recommendations requiring Reg BI compliance, and (e) maintaining records of AI outputs and the supervisory review process consistent with SEC Rule 17a-4 and FINRA recordkeeping requirements.

## Common Pitfalls
- **Relying on disclaimers to avoid adviser status.** "This is not investment advice" does not override the functional test. If the substance is advisory, the disclaimer is meaningless for regulatory purposes.
- **Assuming "free" means no compensation.** The compensation prong is satisfied by any economic benefit, including indirect compensation such as advertising revenue, affiliate fees, payment for order flow, data monetization, or commission-based revenue.
- **Treating algorithmic advice differently from human advice.** The SEC has made clear that the medium of delivery (human vs. algorithm vs. AI) does not change the analysis. If a machine provides personalized securities recommendations, it is investment advice.
- **Confusing education with advice.** Education becomes advice the moment it is individualized — when it moves from "here are general principles of diversification" to "based on your situation, you should hold more bonds."
- **Ignoring state registration.** Federal registration does not preempt state notice filing requirements, and advisers below the federal AUM threshold must register at the state level. Digital platforms that serve users nationwide may trigger registration in multiple states.
- **Assuming the solely incidental exclusion is a blanket exemption for broker-dealers.** The exclusion requires both that the advice be solely incidental to brokerage AND that there be no special compensation. Broker-dealers offering financial planning, advisory accounts, or wrap programs typically do not qualify.
- **Failing to supervise AI outputs.** Firms cannot deploy AI tools that generate client-facing content without supervisory review procedures. Regulatory responsibility does not transfer to the algorithm.
- **Overlooking the "holding out" standard.** Even if a person has not yet provided advice, holding themselves out as an investment adviser (through marketing, titles, or descriptions of services) can trigger registration requirements and the business prong.
- **Conflating ERISA education safe harbors with Advisers Act analysis.** DOL Interpretive Bulletin 96-1 governs ERISA fiduciary status, not Advisers Act registration. The frameworks overlap conceptually but are legally distinct.
- **Treating model portfolios as always safe.** Model portfolios published to a general audience may qualify for the publisher's exclusion, but model portfolios tailored to individual clients or adjusted based on client-specific inputs are personal advice.

## Cross-References
- **fiduciary-standards** (compliance plugin, Layer 9): Fiduciary duties that attach once adviser status is established
- **reg-bi** (compliance plugin, Layer 9): Regulation Best Interest obligations for broker-dealer recommendations
- **investment-suitability** (compliance plugin, Layer 9): Suitability analysis framework underlying both advice and recommendations
- **advertising-compliance** (compliance plugin, Layer 9): Rules governing how advisory and brokerage services are marketed
- **conflicts-of-interest** (compliance plugin, Layer 9): Identification and management of conflicts that arise in advisory and brokerage relationships
