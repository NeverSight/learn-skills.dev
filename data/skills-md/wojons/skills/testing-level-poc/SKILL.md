---
name: testing-level-poc
description: Testing strategy for Proof of Concept projects
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# POC Testing Strategy

Minimal testing approach for Proof of Concept projects focused on validating technical feasibility.

## When to use me

Use this skill when:
- Building a proof of concept to validate technology choices
- Testing architectural approaches or algorithms
- Demonstrating feasibility to stakeholders
- Exploring new technologies with minimal investment
- Rapid prototyping without production concerns

## What I do

**Core Philosophy**: Maximum learning, minimal quality assurance. Focus on answering "Can we build this?" not "Is this production-ready?"

**Recommended Testing Approach**:

1. **Manual Testing (Primary)**
   - Ad-hoc testing by developers
   - Quick validation of core hypotheses
   - No formal test documentation
   - Exploratory testing of key technical challenges

2. **Minimal Unit Testing**
   - Test only critical algorithms or complex logic
   - Skip business logic and edge cases
   - No coverage requirements
   - Focus on technical risk areas

3. **No Formal Test Types**
   - Skip integration, E2E, performance, security testing
   - No test automation setup
   - No CI/CD pipeline for testing
   - No formal test reporting

**Project-Specific Adjustments**:

- **Hobby POC**: Pure manual testing, focus on fun/learning
- **Enterprise POC**: Some unit testing for credibility, demo scenarios
- **Technical Spike**: Targeted testing of specific technical risks only

## Examples

```bash
# POC testing is minimal and manual
# Example manual validation commands:

# Test core algorithm
node test-algorithm.js
python validate-hypothesis.py

# Quick API test
curl -X POST http://localhost:3000/api/test

# Database connection test
node test-db-connection.js

# No formal test suites needed
```

## Output format

```
POC Testing Summary:
──────────────────────────────
Technical Feasibility Assessment:

✅ Core Algorithm Works:
  - Processes 10k records in < 2 seconds
  - Accuracy: 98.7% (meets 95% target)
  - Memory usage: Acceptable (max 512MB)

⚠️ Integration Challenges:
  - API rate limiting may be issue at scale
  - Database schema needs optimization

❌ Showstopper Found:
  - Third-party service has 5-second latency
  - May not meet performance requirements

Recommendation:
  - Technical concept is feasible
  - Address API latency concern before proceeding
  - Proceed to MVP with risk mitigation plan

Testing Effort: 4 hours manual testing
No formal test infrastructure needed
```

## Notes

- POC testing should be time-boxed (days, not weeks)
- Document findings and limitations clearly
- Focus on answering specific technical questions
- Don't build test infrastructure that won't be used later
- Be clear with stakeholders about POC limitations
- POC code is often thrown away or significantly refactored
- Consider spike solutions for specific technical risks
- Balance speed with enough testing to validate feasibility
