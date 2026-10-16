---
name: skill-router
description: "MASTER SKILL ROUTER - Automatic intent detection and skill routing for the entire Talosix skill library (92 skills). This skill is loaded as background knowledge so Claude can automatically detect what the user is trying to accomplish and invoke the correct skill(s) without the user needing to know skill names. Covers: product management, engineering, QA, testing, sales, marketing, content creation, lead generation, outreach, regulatory, compliance, deployment, release, operations, design, finance, HR, PRDs, code review, test cases, demos, RFPs, competitive analysis, UI design, deployments, FDA audits, marketing campaigns, lead research, outreach emails, wireframes, one-pagers, social media, test strategy, user interviews, incident response, SOPs, compliance checks, and much more@"
user-invocable: false
---

# Talosix Skill Router - Master Catalog & Intent Routing

You have access to 92 specialized skills across 13 departments. Your job is to AUTOMATICALLY detect what the user wants and invoke the right skill(s). The user should NEVER need to memorize skill names.

---

## COMPLETE SKILL CATALOG

### Product Management (12 skills)

| Skill                       | Invoke With                    | What It Does                                                                         |
| --------------------------- | ------------------------------ | ------------------------------------------------------------------------------------ |
| product-prd                 | `/product-prd`                 | Writes a full Product Requirements Document from a feature idea or brief             |
| user-interview-analysis     | `/user-interview-analysis`     | Analyzes user interview transcripts to extract themes, pain points, and insights     |
| roadmap-planning            | `/roadmap-planning`            | Creates quarterly/annual product roadmaps with prioritization and dependencies       |
| business-case               | `/business-case`               | Builds a business case with ROI analysis, market sizing, and financial justification |
| feature-scoring             | `/feature-scoring`             | Scores and prioritizes features using RICE, MoSCoW, or weighted frameworks           |
| stakeholder-alignment       | `/stakeholder-alignment`       | Creates stakeholder maps, RACI charts, and alignment documents                       |
| competitor-analysis         | `/competitor-analysis`         | Deep-dive competitor analysis with feature comparison and positioning                |
| customer-feedback-synthesis | `/customer-feedback-synthesis` | Synthesizes customer feedback from multiple sources into actionable themes           |
| sprint-planning             | `/sprint-planning`             | Facilitates sprint planning with capacity, velocity, and commitment                  |
| backlog-grooming            | `/backlog-grooming`            | Refines and prioritizes the product backlog with estimation                          |
| release-notes               | `/release-notes`               | Generates user-facing release notes from tickets, PRs, or changelogs                 |
| acceptance-criteria         | `/acceptance-criteria`         | Writes detailed acceptance criteria in Given/When/Then format for user stories       |

### Engineering (14 skills)

| Skill                    | Invoke With                 | What It Does                                                                      |
| ------------------------ | --------------------------- | --------------------------------------------------------------------------------- |
| code-review              | `/code-review`              | Reviews code for quality, bugs, security, performance, and best practices         |
| refactoring-guide        | `/refactoring-guide`        | Guides systematic refactoring with patterns and safe transformation steps         |
| technical-design         | `/technical-design`         | Creates technical design documents with architecture, data models, and trade-offs |
| api-design               | `/api-design`               | Designs RESTful or GraphQL APIs with schemas, endpoints, and documentation        |
| database-migration       | `/database-migration`       | Plans and generates database migration scripts with rollback strategies           |
| technical-debt-tracking  | `/technical-debt-tracking`  | Catalogs, prioritizes, and plans remediation of technical debt                    |
| performance-optimization | `/performance-optimization` | Analyzes and optimizes application performance with profiling and recommendations |
| security-audit           | `/security-audit`           | Performs security audits covering OWASP Top 10, auth, data protection             |
| cicd-pipeline            | `/cicd-pipeline`            | Designs and configures CI/CD pipelines for build, test, and deploy                |
| documentation-generation | `/documentation-generation` | Auto-generates technical documentation from code, APIs, or architecture           |
| dependency-upgrade       | `/dependency-upgrade`       | Plans and executes dependency upgrades with compatibility checks                  |
| error-handling-strategy  | `/error-handling-strategy`  | Designs error handling, logging, and alerting strategies                          |
| debugging-guide          | `/debugging-guide`          | Systematic debugging methodology for reproducing and resolving issues             |
| load-testing             | `/load-testing`             | Designs and runs load/stress testing plans with performance benchmarks            |

### QA & Testing (6 skills)

| Skill                      | Invoke With                   | What It Does                                                            |
| -------------------------- | ----------------------------- | ----------------------------------------------------------------------- |
| test-case-generation       | `/test-case-generation`       | Generates comprehensive test cases from requirements or user stories    |
| uat-test-generation        | `/uat-test-generation`        | Creates User Acceptance Testing scripts for business stakeholders       |
| playwright-test-generation | `/playwright-test-generation` | Generates Playwright end-to-end test automation code                    |
| test-strategy              | `/test-strategy`              | Creates a comprehensive test strategy document for a project or release |
| test-planning              | `/test-planning`              | Builds detailed test plans with scope, schedule, resources, and risk    |
| zephyr-test-sync           | `/zephyr-test-sync`           | Syncs test cases and results with Zephyr test management                |

### Sales (10 skills)

| Skill                  | Invoke With               | What It Does                                                                          |
| ---------------------- | ------------------------- | ------------------------------------------------------------------------------------- |
| sales-rfp-response     | `/sales-rfp-response`     | Drafts comprehensive RFP/RFI responses with win themes and compliance mapping         |
| demo-script            | `/demo-script`            | Creates structured demo scripts with talk tracks, objection handling, and transitions |
| sales-proposal         | `/sales-proposal`         | Builds sales proposals with executive summary, solution design, and pricing           |
| competitive-battlecard | `/competitive-battlecard` | Creates competitive battlecards with objection handling and win strategies            |
| discovery-call-prep    | `/discovery-call-prep`    | Prepares discovery call guides with questions, personas, and qualification criteria   |
| deal-risk-assessment   | `/deal-risk-assessment`   | Assesses deal risk and recommends mitigation strategies                               |
| roi-calculator         | `/roi-calculator`         | Builds ROI/TCO calculators and value justification documents                          |
| contract-review        | `/contract-review`        | Reviews contracts for risk, terms, and negotiation opportunities                      |
| reference-matching     | `/reference-matching`     | Matches customer references to prospect industry, size, and use case                  |
| sales-forecast         | `/sales-forecast`         | Analyzes pipeline and generates sales forecasts with confidence levels                |

### Marketing - Content Engine (8 skills)

| Skill                    | Invoke With                 | What It Does                                                               |
| ------------------------ | --------------------------- | -------------------------------------------------------------------------- |
| marketing-orchestrator   | `/marketing-orchestrator`   | MASTER marketing skill that chains sub-skills for complete campaigns       |
| brand-voice              | `/brand-voice`              | Ensures all content matches Talosix brand voice, tone, and guidelines      |
| content-atomizer         | `/content-atomizer`         | Breaks long-form content into social posts, snippets, and micro-content    |
| one-pager-generator      | `/one-pager-generator`      | Creates product/feature one-pagers for sales enablement                    |
| social-media-transformer | `/social-media-transformer` | Transforms content for specific social platforms (LinkedIn, Twitter, etc.) |
| blog-post-engine         | `/blog-post-engine`         | Writes SEO-optimized blog posts with research, structure, and CTAs         |
| direct-response-copy     | `/direct-response-copy`     | Writes direct-response copywriting for ads, emails, and landing pages      |
| lead-magnet-creator      | `/lead-magnet-creator`      | Creates lead magnets (ebooks, checklists, templates, guides)               |

### Marketing - Original (10 skills)

| Skill               | Invoke With            | What It Does                                                                  |
| ------------------- | ---------------------- | ----------------------------------------------------------------------------- |
| marketing-content   | `/marketing-content`   | General marketing content creation across formats                             |
| case-study-creation | `/case-study-creation` | Writes customer case studies with problem/solution/results structure          |
| email-campaign      | `/email-campaign`      | Designs multi-touch email campaigns with sequences and A/B variants           |
| landing-page-copy   | `/landing-page-copy`   | Writes conversion-optimized landing page copy with hero, benefits, CTAs       |
| webinar-planning    | `/webinar-planning`    | Plans webinars end-to-end: topic, speakers, promotion, follow-up              |
| seo-content         | `/seo-content`         | Creates SEO-optimized content with keyword research and on-page optimization  |
| white-paper         | `/white-paper`         | Writes authoritative white papers with research, data, and thought leadership |
| press-release       | `/press-release`       | Drafts press releases following AP style with quotes and boilerplate          |
| ad-copy             | `/ad-copy`             | Creates ad copy for Google, LinkedIn, Facebook, and display campaigns         |
| content-calendar    | `/content-calendar`    | Plans content calendars with themes, channels, cadence, and assignments       |

### Lead Gen & Outreach (6 skills)

| Skill                            | Invoke With                         | What It Does                                                              |
| -------------------------------- | ----------------------------------- | ------------------------------------------------------------------------- |
| linkedin-prospect-research       | `/linkedin-prospect-research`       | Researches LinkedIn prospects with company intel and talking points       |
| outreach-sequence-generator      | `/outreach-sequence-generator`      | Creates multi-step outreach email/call sequences with personalization     |
| abm-account-research             | `/abm-account-research`             | Deep account research for Account-Based Marketing campaigns               |
| competitive-intelligence-scraper | `/competitive-intelligence-scraper` | Gathers competitive intelligence from public sources                      |
| seo-audit                        | `/seo-audit`                        | Performs technical and content SEO audits with actionable recommendations |
| lead-research-assistant          | `/lead-research-assistant`          | Researches and qualifies leads with company and contact intelligence      |

### Regulatory & Compliance (8 skills)

| Skill               | Invoke With            | What It Does                                                                 |
| ------------------- | ---------------------- | ---------------------------------------------------------------------------- |
| validation-protocol | `/validation-protocol` | Creates IQ/OQ/PQ validation protocols for regulated environments (FDA, ISO)  |
| change-control      | `/change-control`      | Manages change control documentation and impact assessment                   |
| risk-assessment     | `/risk-assessment`     | Performs risk assessments (FMEA, hazard analysis) for products and processes |
| traceability-matrix | `/traceability-matrix` | Builds requirements traceability matrices linking requirements to tests      |
| regulatory-research | `/regulatory-research` | Researches regulatory requirements (FDA, EU MDR, ISO, HIPAA)                 |
| sop-generation      | `/sop-generation`      | Generates Standard Operating Procedures with proper formatting and controls  |
| audit-preparation   | `/audit-preparation`   | Prepares for regulatory audits with gap analysis and documentation review    |
| deploy-plan         | `/deploy-plan`         | Creates deployment plans with validation steps for regulated environments    |

### Release & Deployment (4 skills)

| Skill              | Invoke With           | What It Does                                                     |
| ------------------ | --------------------- | ---------------------------------------------------------------- |
| deploy-checklist   | `/deploy-checklist`   | Generates pre/during/post deployment checklists                  |
| rollback-plan      | `/rollback-plan`      | Creates rollback plans with triggers, steps, and verification    |
| release-monitoring | `/release-monitoring` | Sets up release monitoring dashboards, alerts, and health checks |
| hotfix-procedure   | `/hotfix-procedure`   | Documents hotfix procedures with expedited review and deployment |

### Operations (3 skills)

| Skill             | Invoke With          | What It Does                                                             |
| ----------------- | -------------------- | ------------------------------------------------------------------------ |
| incident-response | `/incident-response` | Guides incident response with severity classification, comms, and RCA    |
| retrospective     | `/retrospective`     | Facilitates team retrospectives with structured formats and action items |
| meeting-agent     | `/meeting-agent`     | Manages meeting agendas, notes, action items, and follow-ups             |

### Design (7 skills)

| Skill                     | Invoke With                  | What It Does                                                                 |
| ------------------------- | ---------------------------- | ---------------------------------------------------------------------------- |
| talosix-design-system     | `/talosix-design-system`     | Applies the Talosix design system (colors, typography, components, spacing)  |
| prd-to-wireframe          | `/prd-to-wireframe`          | Converts PRDs into wireframe specifications and layout descriptions          |
| figma-to-code             | `/figma-to-code`             | Converts Figma designs into production-ready frontend code                   |
| user-flow-generator       | `/user-flow-generator`       | Creates user flow diagrams and journey maps from requirements                |
| design-qa                 | `/design-qa`                 | QA checks designs against specs, accessibility, and design system compliance |
| figma-component-generator | `/figma-component-generator` | Generates Figma component specifications and documentation                   |
| design-sprint-prototype   | `/design-sprint-prototype`   | Facilitates design sprints and creates rapid prototypes                      |

### Finance (1 skill)

| Skill              | Invoke With           | What It Does                                                           |
| ------------------ | --------------------- | ---------------------------------------------------------------------- |
| reconcile-payments | `/reconcile-payments` | Reconciles payment records across systems and identifies discrepancies |

### HR (3 skills)

| Skill                | Invoke With             | What It Does                                                                     |
| -------------------- | ----------------------- | -------------------------------------------------------------------------------- |
| job-description      | `/job-description`      | Creates compelling, inclusive job descriptions with requirements and culture fit |
| onboarding-checklist | `/onboarding-checklist` | Generates comprehensive onboarding checklists for new hires                      |
| policy-document      | `/policy-document`      | Drafts HR policy documents with legal compliance and best practices              |

---

## INTENT DETECTION & ROUTING RULES

When a user makes a request, match their intent to the appropriate skill(s) using these rules. You do NOT need to announce routing -- just invoke the skill. If the user's request clearly maps to a skill, use it. If it maps to multiple skills, chain them.

### Single-Skill Intent Mappings

**Product & Strategy**

- "Write a PRD" / "I need a product requirements document" / "Define this feature" -> `/product-prd`
- "Analyze these interviews" / "What did users say" / "User research synthesis" -> `/user-interview-analysis`
- "Plan the roadmap" / "What should we build next quarter" -> `/roadmap-planning`
- "Build a business case" / "Justify this investment" / "ROI for this project" -> `/business-case`
- "Prioritize these features" / "Score these ideas" / "Which feature first" -> `/feature-scoring`
- "Get stakeholders aligned" / "RACI chart" / "Who owns what" -> `/stakeholder-alignment`
- "What are competitors doing" / "Competitor deep-dive" -> `/competitor-analysis`
- "Synthesize this feedback" / "What are customers saying" -> `/customer-feedback-synthesis`
- "Plan the sprint" / "Sprint planning" -> `/sprint-planning`
- "Groom the backlog" / "Refine stories" / "Prioritize tickets" -> `/backlog-grooming`
- "Write release notes" / "What shipped this release" -> `/release-notes`
- "Write acceptance criteria" / "Define done for this story" -> `/acceptance-criteria`

**Engineering**

- "Review this code" / "Code review" / "Check this PR" -> `/code-review`
- "Refactor this" / "Clean up this code" / "Improve code structure" -> `/refactoring-guide`
- "Technical design" / "Architecture for" / "System design" -> `/technical-design`
- "Design an API" / "API endpoints for" / "REST API for" -> `/api-design`
- "Database migration" / "Schema change" / "Add a column" -> `/database-migration`
- "Technical debt" / "Track tech debt" / "Debt remediation" -> `/technical-debt-tracking`
- "Optimize performance" / "It's slow" / "Speed up" -> `/performance-optimization`
- "Security audit" / "Check for vulnerabilities" / "OWASP" -> `/security-audit`
- "Set up CI/CD" / "Pipeline configuration" / "Automate builds" -> `/cicd-pipeline`
- "Generate docs" / "Document this code" / "API documentation" -> `/documentation-generation`
- "Upgrade dependencies" / "Update packages" / "Library versions" -> `/dependency-upgrade`
- "Error handling" / "How should we handle errors" / "Logging strategy" -> `/error-handling-strategy`
- "Debug this" / "Why is this failing" / "Troubleshoot" -> `/debugging-guide`
- "Load test" / "Stress test" / "Performance benchmarks" -> `/load-testing`

**QA & Testing**

- "Write test cases" / "Test cases for this story" / "QA tests" -> `/test-case-generation`
- "UAT tests" / "User acceptance tests" / "Business testing" -> `/uat-test-generation`
- "Playwright tests" / "E2E tests" / "Automated browser tests" -> `/playwright-test-generation`
- "Test strategy" / "Overall testing approach" / "How should we test" -> `/test-strategy`
- "Test plan" / "Testing schedule" / "QA plan" -> `/test-planning`
- "Sync with Zephyr" / "Upload test cases to Zephyr" -> `/zephyr-test-sync`

**Sales**

- "Respond to this RFP" / "RFP response" / "RFI answer" -> `/sales-rfp-response`
- "Create a demo script" / "Prepare for demo" / "Demo talk track" -> `/demo-script`
- "Write a proposal" / "Sales proposal for" -> `/sales-proposal`
- "Competitive battlecard" / "How to sell against X" / "Win against competitor" -> `/competitive-battlecard`
- "Prepare for discovery call" / "Discovery questions" -> `/discovery-call-prep`
- "Assess this deal" / "Deal risk" / "Is this deal at risk" -> `/deal-risk-assessment`
- "ROI calculator" / "Show the value" / "TCO analysis" -> `/roi-calculator`
- "Review this contract" / "Contract terms" / "Redline this" -> `/contract-review`
- "Find a reference" / "Customer reference for" -> `/reference-matching`
- "Sales forecast" / "Pipeline analysis" / "Revenue projection" -> `/sales-forecast`

**Marketing & Content**

- "Create a marketing campaign" / "Full campaign for" / "Launch marketing for" -> `/marketing-orchestrator`
- "Check brand voice" / "Does this sound like us" / "Brand consistency" -> `/brand-voice`
- "Break this into social posts" / "Atomize this content" / "Repurpose this" -> `/content-atomizer`
- "Create a one-pager" / "Product one-pager" / "Sales sheet" -> `/one-pager-generator`
- "Social media posts" / "LinkedIn post" / "Tweet this" -> `/social-media-transformer`
- "Write a blog post" / "Blog about" / "Article on" -> `/blog-post-engine`
- "Direct response copy" / "Sales copy" / "Conversion copy" -> `/direct-response-copy`
- "Create a lead magnet" / "Ebook" / "Downloadable guide" -> `/lead-magnet-creator`
- "Marketing content" / "Collateral for" -> `/marketing-content`
- "Write a case study" / "Customer success story" -> `/case-study-creation`
- "Email campaign" / "Drip sequence" / "Nurture emails" -> `/email-campaign`
- "Landing page" / "Landing page copy" -> `/landing-page-copy`
- "Plan a webinar" / "Webinar on" -> `/webinar-planning`
- "SEO content" / "Rank for keyword" / "SEO article" -> `/seo-content`
- "Write a white paper" / "Thought leadership piece" -> `/white-paper`
- "Press release" / "Announce this" / "Media announcement" -> `/press-release`
- "Ad copy" / "Google ads" / "LinkedIn ads" / "Facebook ads" -> `/ad-copy`
- "Content calendar" / "Publishing schedule" / "Plan content for the month" -> `/content-calendar`

**Lead Gen & Outreach**

- "Research this prospect" / "LinkedIn research on" -> `/linkedin-prospect-research`
- "Write outreach emails" / "Cold email sequence" / "Follow-up sequence" -> `/outreach-sequence-generator`
- "ABM research" / "Account research for" / "Target account intel" -> `/abm-account-research`
- "Competitive intelligence" / "What's the competition doing" / "Monitor competitors" -> `/competitive-intelligence-scraper`
- "SEO audit" / "Check our SEO" / "Technical SEO" -> `/seo-audit`
- "Find leads" / "Research leads" / "Qualify this lead" -> `/lead-research-assistant`

**Regulatory & Compliance**

- "Validation protocol" / "IQ/OQ/PQ" / "FDA validation" -> `/validation-protocol`
- "Change control" / "Document this change" / "Impact assessment" -> `/change-control`
- "Risk assessment" / "FMEA" / "Hazard analysis" -> `/risk-assessment`
- "Traceability matrix" / "RTM" / "Trace requirements to tests" -> `/traceability-matrix`
- "Regulatory requirements" / "FDA rules for" / "What does ISO say" / "HIPAA requirements" -> `/regulatory-research`
- "Write an SOP" / "Standard operating procedure" / "Process document" -> `/sop-generation`
- "Prepare for audit" / "Audit prep" / "FDA audit" / "ISO audit" -> `/audit-preparation`
- "Deploy plan" / "Deployment plan for regulated" -> `/deploy-plan`

**Release & Deployment**

- "Deploy checklist" / "Pre-deploy checks" / "Deployment steps" -> `/deploy-checklist`
- "Rollback plan" / "What if deploy fails" / "How to roll back" -> `/rollback-plan`
- "Release monitoring" / "Post-deploy monitoring" / "Watch the release" -> `/release-monitoring`
- "Hotfix procedure" / "Emergency fix" / "Critical patch" -> `/hotfix-procedure`

**Operations**

- "Incident response" / "We have an outage" / "Production issue" / "System is down" -> `/incident-response`
- "Run a retro" / "Retrospective" / "What went well" -> `/retrospective`
- "Meeting agenda" / "Meeting notes" / "Action items from meeting" -> `/meeting-agent`

**Design**

- "Design system" / "Brand colors" / "Component specs" / "Talosix design" -> `/talosix-design-system`
- "Generate wireframes" / "Wireframe for" / "Layout for this feature" -> `/prd-to-wireframe`
- "Convert Figma to code" / "Implement this design" / "Code from Figma" -> `/figma-to-code`
- "User flow" / "Journey map" / "How does the user get from A to B" -> `/user-flow-generator`
- "Design QA" / "Check design against spec" / "Pixel perfect review" -> `/design-qa`
- "Figma component" / "Create a component in Figma" -> `/figma-component-generator`
- "Design sprint" / "Rapid prototype" / "Quick prototype" -> `/design-sprint-prototype`

**Finance**

- "Reconcile payments" / "Payment discrepancies" / "Match transactions" -> `/reconcile-payments`

**HR**

- "Write a job description" / "Job posting for" / "We're hiring a" -> `/job-description`
- "Onboarding checklist" / "New hire onboarding" / "Onboard someone" -> `/onboarding-checklist`
- "Write a policy" / "HR policy" / "Employee policy" -> `/policy-document`

---

## SKILL CHAINING RULES

Many tasks require multiple skills working together. When you detect these compound intents, invoke the skills in the specified order.

### Content Creation Chains

- **Blog post with SEO**: `/blog-post-engine` -> `/seo-content` -> `/brand-voice` (review)
- **Full content campaign**: `/marketing-orchestrator` (this skill handles chaining internally)
- **Content repurposing**: `/content-atomizer` -> `/social-media-transformer`
- **One-pager with brand**: `/one-pager-generator` -> `/brand-voice` (review)
- **Thought leadership**: `/white-paper` -> `/blog-post-engine` (summary post) -> `/content-atomizer`
- **Social media planning**: `/content-calendar` -> `/social-media-transformer`

### Product-to-Engineering Chains

- **Feature end-to-end**: `/product-prd` -> `/acceptance-criteria` -> `/technical-design` -> `/test-case-generation`
- **Design from PRD**: `/product-prd` -> `/prd-to-wireframe` -> `/talosix-design-system`
- **PRD to tests**: `/product-prd` -> `/acceptance-criteria` -> `/test-case-generation`
- **Sprint readiness**: `/backlog-grooming` -> `/sprint-planning` -> `/acceptance-criteria`

### Sales Chains

- **Full RFP response**: `/sales-rfp-response` -> `/competitive-battlecard` -> `/roi-calculator`
- **Demo preparation**: `/demo-script` -> `/competitive-battlecard` -> `/discovery-call-prep`
- **Proposal with ROI**: `/sales-proposal` -> `/roi-calculator` -> `/reference-matching`
- **Lead to outreach**: `/lead-research-assistant` -> `/linkedin-prospect-research` -> `/outreach-sequence-generator`
- **Find and engage leads**: `/lead-research-assistant` -> `/linkedin-prospect-research` -> `/outreach-sequence-generator`

### Deployment Chains

- **Full deployment**: `/deploy-plan` -> `/deploy-checklist` -> `/rollback-plan` -> `/release-monitoring`
- **Regulated deployment**: `/deploy-plan` -> `/validation-protocol` -> `/deploy-checklist` -> `/rollback-plan`
- **Emergency fix**: `/hotfix-procedure` -> `/deploy-checklist` -> `/rollback-plan`

### Regulatory Chains

- **Audit preparation**: `/audit-preparation` -> `/traceability-matrix` -> `/validation-protocol`
- **Compliance check**: `/regulatory-research` -> `/validation-protocol` -> `/risk-assessment`
- **Change with compliance**: `/change-control` -> `/risk-assessment` -> `/traceability-matrix`
- **Full regulatory package**: `/regulatory-research` -> `/sop-generation` -> `/validation-protocol` -> `/traceability-matrix` -> `/audit-preparation`

### QA Chains

- **Test strategy to execution**: `/test-strategy` -> `/test-planning` -> `/test-case-generation`
- **Automated testing**: `/test-case-generation` -> `/playwright-test-generation` -> `/zephyr-test-sync`
- **UAT preparation**: `/acceptance-criteria` -> `/uat-test-generation`

### Design Chains

- **Design a feature**: `/prd-to-wireframe` -> `/talosix-design-system` -> `/user-flow-generator`
- **Design to code**: `/prd-to-wireframe` -> `/figma-component-generator` -> `/figma-to-code`
- **Design validation**: `/design-qa` -> `/talosix-design-system`

### Marketing + Sales Alignment

- **Case study to campaign**: `/case-study-creation` -> `/content-atomizer` -> `/email-campaign`
- **Product launch**: `/marketing-orchestrator` -> `/press-release` -> `/landing-page-copy` -> `/email-campaign` -> `/ad-copy` -> `/social-media-transformer`
- **ABM campaign**: `/abm-account-research` -> `/one-pager-generator` -> `/outreach-sequence-generator`

---

## COMPOUND INTENT DETECTION

When the user's request touches multiple areas, use these heuristics:

1. **"Create marketing content for..."** -> Start with `/marketing-orchestrator` which handles sub-skill chaining
2. **"We're launching a new feature"** -> `/product-prd` -> `/prd-to-wireframe` -> `/release-notes` -> `/marketing-content`
3. **"We're deploying tomorrow"** -> `/deploy-plan` -> `/deploy-checklist` -> `/rollback-plan`
4. **"Prepare for the FDA audit"** -> `/audit-preparation` -> `/traceability-matrix` -> `/validation-protocol`
5. **"Find leads and reach out"** -> `/lead-research-assistant` -> `/linkedin-prospect-research` -> `/outreach-sequence-generator`
6. **"Design the UI for..."** -> `/prd-to-wireframe` -> `/talosix-design-system`
7. **"Plan our social media"** -> `/content-calendar` -> `/social-media-transformer`
8. **"We need a test strategy"** -> `/test-strategy` -> `/test-planning`
9. **"Check compliance"** -> `/validation-protocol` -> `/regulatory-research`
10. **"I need to respond to this RFP"** -> `/sales-rfp-response` (may chain `/competitive-battlecard` and `/roi-calculator`)
11. **"Create a blog post about..."** -> `/blog-post-engine` -> `/brand-voice` -> `/seo-content`
12. **"Generate wireframes"** -> `/prd-to-wireframe` -> `/talosix-design-system`
13. **"Write outreach emails"** -> `/outreach-sequence-generator`
14. **"Onboard a new hire"** -> `/onboarding-checklist`
15. **"Create a job posting"** -> `/job-description`
16. **"Help me prepare for this demo"** -> `/demo-script`
17. **"What's our competition doing?"** -> `/competitive-intelligence-scraper` or `/competitor-analysis`

---

## ROUTING BEHAVIOR

1. **Be proactive**: If the user's request maps to a skill, just use it. Do not ask "would you like me to use the X skill?" -- just invoke it.
2. **Chain when appropriate**: If a task naturally requires multiple skills, invoke them in sequence.
3. **Suggest related skills**: After completing a task, briefly mention related skills that could add value. For example, after writing a PRD, mention that `/acceptance-criteria` and `/test-case-generation` can follow.
4. **Ambiguity resolution**: If a request could map to multiple unrelated skills, briefly ask which direction the user wants. For example, "competitive" could mean `/competitor-analysis` (product) or `/competitive-battlecard` (sales) or `/competitive-intelligence-scraper` (lead gen).
5. **Partial matches**: If the user's request partially matches a skill, use it and adapt. Skills are templates -- they can be flexed to fit the specific need.
6. **Unknown requests**: If no skill matches, handle the request with general capability. Not everything needs a skill.
