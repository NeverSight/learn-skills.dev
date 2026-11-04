---
name: business-analyst
description: |
  Run a structured business analysis workflow: requirements elicitation with stakeholder
  interviews and MoSCoW prioritization, as-is/to-be process mapping with BPMN notation,
  data-driven analysis (CBA, SWOT, root cause), and production-ready documentation
  (BRD, FRD, user stories with INVEST acceptance criteria).
  Triggers on "gather requirements", "write user stories", "map business process", "BRD",
  "FRD", "gap analysis", "cost-benefit analysis", "facilitate workshop", "business requirements",
  "process mapping", "as-is to-be", "stakeholder interview", or "business analyst".
  For management consulting (issue trees, steerCo business cases, operating model), use
  business-consultant—not business-analyst. For business model canvas, market sizing, and unit
  economics research, use business-model-researcher. Human data / labeling platform PRDs:
  product-management-human-data-platform. Monetization PRDs and packaging:
  product-management-monetization.
---

# Business Analyst

## Overview

Run a structured business analysis workflow for requirements elicitation, process modeling,
stakeholder alignment, and solution validation. This skill covers BRD/FRD creation, user stories,
acceptance criteria, BPMN diagrams, gap analysis, and change impact assessment.

## Features

- Requirements elicitation techniques (interviews, workshops, observation, document analysis)
- BRD and FRD document templates with section-by-section guidance
- User story writing with INVEST criteria and acceptance criteria patterns
- BPMN process modeling with swimlane diagrams
- Gap analysis framework and change impact assessment templates

## Usage

1. Identify the user's BA need (requirements, process modeling, user stories, or solution validation)
2. Follow the corresponding workflow below
3. Produce structured outputs: BRD/FRD documents, user stories, BPMN diagrams, or gap analysis reports

## Examples

- **User**: "Gather requirements for a new feature"
  **Agent**: Runs Requirements Elicitation workflow, conducts stakeholder interviews, produces BRD with functional and non-functional requirements

- **User**: "Map our order fulfillment process"
  **Agent**: Runs Process Modeling workflow, creates BPMN diagram with swimlanes, identifies bottlenecks and handoff points

- **User**: "Write user stories for login"
  **Agent**: Runs User Story Writing workflow, produces stories with INVEST criteria and Given/When/Then acceptance criteria

## When to Use

- Elicit and document business requirements (BRD, FRD, user stories)
- Map as-is/to-be processes and run gap or impact analysis
- Facilitate workshops and translate between business and technical teams
- Produce cost-benefit, SWOT, or root-cause analysis for business decisions

## Workflow Selection

- User wants to gather or document requirements → **Workflow 1: Requirements Elicitation**
- User wants to map or improve a process → **Workflow 2: Business Process Analysis**
- User wants to evaluate a business decision → **Workflow 3: Data-Driven Business Analysis**
- User wants to produce documentation → **Workflow 4: Documentation & Communication**

## When NOT to Use

- Dashboard design, metric catalogs, or analytical SQL → use `bi-analyst`
- Data platform or enterprise architecture decisions → use `data-architect`
- Cross-service system design, ADRs, architecture review → use `senior-system-architecture`
- Customer support SLAs, billing ops, or CS health scoring → use `customer-ops-specialist`
- Revenue recognition, month-end close, or ASC 606 contract analysis → use `senior-revenue-accountant`
- UX flows, wireframes, and design handoff → use `product-designer`
- Labeling/RLHF platform product roadmap and quality systems → use `product-management-human-data-platform`
- Cross-team program execution, RAID, exec status → use `technical-program-manager`
- MSA, SaaS, vendor/customer contract redlines → use `commercial-counsel`
- HR operational processes and employee lifecycle checklists → use `people-operations-specialist`
- Strategy, issue trees, steerCo business cases → use `business-consultant`
- Business model research, TAM, competitor monetization → use `business-model-researcher`

## Core Workflows

### 1. Requirements Elicitation

**Step-by-step process:**

1. **Prepare**
   - Review existing documentation, systems, and pain points
   - Identify stakeholders (sponsors, users, implementers)
   - Define scope boundaries (in-scope, out-of-scope)

2. **Elicit**
   - Interview key stakeholders using open-ended questions
   - Observe users in their current workflow (shadowing)
   - Review existing reports, data, and system outputs
   - Run workshops for complex or cross-functional needs

3. **Analyze & consolidate**
   - Group requirements by theme (functional, non-functional, technical)
   - Resolve conflicts between stakeholders
   - Prioritize using MoSCoW or weighted scoring

4. **Validate**
   - Walk through requirements with stakeholders
   - Confirm understanding with prototypes or examples
   - Get formal sign-off before proceeding

### 2. Business Process Analysis

**Analysis workflow:**

1. **Map the current state (as-is)**
   - Identify actors, steps, decisions, and handoffs
   - Note time spent, pain points, and error rates
   - Document data inputs and outputs at each step

2. **Identify gaps and inefficiencies**
   - Redundancies, manual workarounds, bottlenecks
   - Missing integrations, duplicate data entry
   - Compliance risks or audit gaps

3. **Design the future state (to-be)**
   - Streamline or automate steps
   - Eliminate non-value-add activities
   - Define new roles, systems, and data flows

4. **Plan the transition**
   - Phased rollout vs big-bang
   - Change impact assessment
   - Training and communication plan

### 3. Data-Driven Business Analysis

**Analytical techniques:**

| Technique | When to Use | Output |
|---|---|---|
| Cost-benefit analysis | Evaluate initiatives | ROI, payback period, NPV |
| SWOT analysis | Strategic planning | Strengths, weaknesses, opportunities, threats |
| Root cause analysis | Problem diagnosis | 5 Whys, fishbone diagram |
| Process mining | Understand actual vs documented process | Bottleneck map, variant analysis |
| Benchmarking | Compare performance | Gap vs industry leaders |

### 4. Documentation & Communication

**Key documents:**

| Document | Purpose | Audience |
|---|---|---|
| Business Requirements Document (BRD) | What the business needs and why | Business stakeholders, project sponsor |
| Functional Requirements Document (FRD) | How the system should behave | Developers, QA, solution architects |
| User Stories | Feature from user perspective | Agile team, product owner |
| Process Flow | Visual step-by-step workflow | All stakeholders |
| Data Dictionary | Definitions of fields and terms | Technical team, data consumers |
