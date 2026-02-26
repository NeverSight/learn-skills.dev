---
name: ai-vendor-evaluation
description: Comprehensive framework for evaluating AI vendors and solutions to avoid costly mistakes. Use this skill when assessing AI vendor proposals, conducting due diligence, evaluating contracts, comparing vendors, or making build-vs-buy decisions. Helps identify red flags, assess pricing models, evaluate technical capabilities, and conduct structured vendor comparisons.
---

# AI Vendor Evaluation

**Version 1.0** | October 2025 | Based on $1.2M average AI spend analysis

---

## Overview

This skill provides a systematic framework for evaluating AI vendors and solutions to avoid the costly mistakes that plague 95% of AI projects. Use when conducting vendor due diligence, evaluating proposals, negotiating contracts, or making strategic AI purchasing decisions.

**Key capabilities:**
- Structured evaluation criteria for AI vendors
- Red flag identification in proposals and demos
- Pricing model analysis and fair market rates
- Technical capability assessment
- Contract term evaluation
- Build vs buy decision framework

---

## Quick Decision Tree

**Start here to determine which references to read:**

```
What stage are you in?

├─ Early exploration (multiple vendors being considered)
│  └─ Read: evaluation-criteria.md, use-case-fit.md
│     Use: scorecard-template.xlsx
│
├─ Evaluating specific proposal or demo
│  └─ Read: red-flags.md, technical-assessment.md
│     Check: pricing-models.md for pricing reasonableness
│
├─ Contract negotiation
│  └─ Read: contract-checklist.md, pricing-models.md
│     Reference: red-flags.md for problematic terms
│
├─ Build vs Buy decision
│  └─ Read: build-vs-buy.md, use-case-fit.md
│     Consider: Total cost of ownership from pricing-models.md
│
└─ Post-purchase review or audit
   └─ Read: evaluation-criteria.md, technical-assessment.md
      Assess: Whether vendor is delivering on promises
```

---

## When to Use This Skill

**Trigger scenarios:**
- "Help me evaluate this AI vendor proposal"
- "What should I look for in AI vendor demos?"
- "Is this pricing reasonable for an AI solution?"
- "Should we build or buy this AI capability?"
- "What questions should I ask this AI vendor?"
- "Help me compare these AI vendors"
- "Review this AI contract for red flags"
- "Conduct due diligence on this AI company"

---

## Core Evaluation Framework

### Phase 1: Initial Screening
**Goal**: Eliminate obviously problematic vendors before deep evaluation

**Key questions:**
- Does the vendor have relevant domain experience?
- Are there verifiable customer references?
- Is the technology approach sound?
- Are pricing and terms transparent?

**Read**: `references/red-flags.md` for disqualifying signals  
**Read**: `references/use-case-fit.md` for domain fit assessment

---

### Phase 2: Deep Evaluation
**Goal**: Assess vendor capabilities systematically across all dimensions

**Evaluation dimensions:**
1. **Technical capability** - Can they actually deliver?
2. **Business viability** - Will they still exist in 2 years?
3. **Pricing fairness** - Are costs reasonable for value delivered?
4. **Implementation risk** - How likely is successful deployment?
5. **Contract terms** - Are legal terms acceptable?

**Read**: `references/evaluation-criteria.md` for comprehensive framework  
**Read**: `references/technical-assessment.md` for technical evaluation  
**Read**: `references/pricing-models.md` for pricing analysis  
**Use**: `assets/scorecard-template.xlsx` to score vendors systematically

---

### Phase 3: Contract Negotiation
**Goal**: Secure favorable terms and avoid costly traps

**Critical areas:**
- Performance guarantees and SLAs
- Data ownership and usage rights
- Pricing structure and escalation terms
- Exit clauses and data portability
- Liability and indemnification

**Read**: `references/contract-checklist.md` for essential terms  
**Reference**: `references/red-flags.md` for problematic contract patterns

---

## Common Vendor Patterns

### The Overpromiser
**Characteristics**: Claims to solve everything, vague on technical details, aggressive sales tactics  
**Red flag**: "Our AI can handle any use case"  
**Response**: Demand specific technical explanations and verifiable references

### The Feature Dumper
**Characteristics**: Long feature lists, complex pricing, unclear core value proposition  
**Red flag**: Can't explain what problem they actually solve  
**Response**: Force clarity on primary use case and success metrics

### The Consultant in Disguise
**Characteristics**: Software license + mandatory professional services  
**Red flag**: Professional services cost more than software  
**Response**: Assess true cost of ownership, consider if you're buying software or consulting

### The Model Wrapper
**Characteristics**: Thin layer over OpenAI/Anthropic APIs with high markup  
**Red flag**: No proprietary technology, just API access + UI  
**Response**: Calculate cost of building similar solution in-house

**Full pattern library**: See `references/red-flags.md`

---

## Build vs Buy Decision Framework

**When to read this section**: Before committing to vendor evaluation, determine if building in-house is better option.

**Key factors:**
1. **Capability availability** - Does suitable vendor solution exist?
2. **Time to value** - Buy: weeks-months, Build: months-years
3. **Total cost** - Consider 3-year TCO for both options
4. **Strategic importance** - Core competency? Build. Commodity? Buy.
5. **Team capability** - Do you have talent to build and maintain?

**Read**: `references/build-vs-buy.md` for detailed decision framework

---

## Using the Scorecard Template

The vendor scorecard enables structured comparison across vendors.

**To use**:
1. Open `assets/scorecard-template.xlsx`
2. List vendors to compare (up to 5)
3. Score each vendor on evaluation criteria (1-5 scale)
4. Review weighted scores and vendor comparison chart
5. Document decision rationale

**Customization**: Adjust weights based on priorities for your specific use case.

---

## Reference Documents

### references/evaluation-criteria.md
Comprehensive scoring framework across all vendor evaluation dimensions. Includes specific questions to ask, what constitutes good/bad answers, and how to weight criteria for different use cases.

**Use when**: Conducting systematic vendor evaluation

---

### references/red-flags.md
Catalog of warning signs indicating problematic vendors. Organized by category: technical red flags, business red flags, pricing red flags, contract red flags, and behavioral red flags.

**Use when**: Initial vendor screening or reviewing proposals

---

### references/pricing-models.md
Guide to AI vendor pricing models (per-seat, usage-based, platform fees, etc.), fair market rates, what drives costs, and how to negotiate. Includes pricing red flags and total cost of ownership analysis.

**Use when**: Evaluating vendor pricing or negotiating contracts

---

### references/technical-assessment.md
Framework for assessing technical capabilities: architecture review, model evaluation, integration complexity, scalability, security, and data handling. Includes specific technical questions to ask.

**Use when**: Deep technical evaluation of vendor capabilities

---

### references/contract-checklist.md
Essential contract terms for AI vendor agreements: performance guarantees, data rights, pricing protection, exit terms, liability, and support commitments. Includes negotiation guidance.

**Use when**: Contract review or negotiation

---

### references/use-case-fit.md
Framework for assessing whether vendor solution actually fits your use case. Includes questions to ask yourself, questions to ask vendor, and warning signs of poor fit.

**Use when**: Initial vendor screening or use case definition

---

### references/build-vs-buy.md
Decision framework for whether to build AI capability in-house vs purchasing vendor solution. Includes total cost analysis, capability assessment, and strategic considerations.

**Use when**: Before committing to vendor evaluation process

---

## Assets

### assets/scorecard-template.xlsx
Structured spreadsheet for vendor comparison with:
- Evaluation criteria organized by category
- Scoring system (1-5 scale) with descriptions
- Weighted scoring based on priorities
- Vendor comparison charts
- Decision documentation section

**Customize**: Adjust criteria weights and add company-specific requirements
