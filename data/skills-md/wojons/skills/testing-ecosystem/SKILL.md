---
name: testing-ecosystem
description: Understand the complete testing ecosystem and relationships between test types
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Testing Ecosystem

Understand the complete testing ecosystem, including all test types, their relationships, purposes, and appropriate usage contexts.

## When to use me

Use this skill when:
- Learning about software testing approaches
- Designing comprehensive testing strategies
- Understanding how different test types complement each other
- Troubleshooting testing gaps or inefficiencies
- Onboarding team members to testing practices
- Evaluating testing tools and frameworks
- Planning test automation and infrastructure
- Communicating testing approach to stakeholders

## What I do

- **Comprehensive test type catalog**:
  - Document all test types and their characteristics
  - Map test types to quality attributes and objectives
  - Provide usage guidelines and best practices
  - Show relationships and dependencies between test types

- **Ecosystem mapping**:
  - Create test type relationship networks
  - Map test types to development lifecycle stages
  - Show test type evolution across project maturity
  - Illustrate test type complementarity and overlap

- **Contextual guidance**:
  - Recommend test types based on project context
  - Suggest test type sequencing and orchestration
  - Provide anti-patterns and common mistakes
  - Offer optimization strategies for testing ecosystems

- **Integration knowledge**:
  - How test types work together in CI/CD pipelines
  - Test type dependencies and execution constraints
  - Resource allocation across test types
  - Monitoring and measurement approaches

## Testing Ecosystem Components

### Core Functional Testing Types
- **Unit Testing**: Isolated component validation
- **Integration Testing**: Component interaction validation
- **End-to-End Testing**: Complete user workflow validation
- **API Testing**: Interface and contract validation
- **Database Testing**: Data persistence and integrity validation
- **Regression Testing**: Existing functionality preservation

### Non-Functional Testing Types
- **Performance Testing**: Speed, scalability, stability
- **Security Testing**: Vulnerability and threat protection
- **Accessibility Testing**: Inclusive design compliance
- **Compatibility Testing**: Cross-environment functionality
- **Usability Testing**: User experience and interaction design

### Specialized Testing Types
- **Smoke/Sanity Testing**: Basic functionality verification
- **Chaos Testing**: Resilience and failure recovery
- **Contract Testing**: API consumer-provider agreements
- **Mutation Testing**: Test suite effectiveness validation
- **Visual Testing**: UI appearance and layout consistency

### Coordination & Management
- **Test Orchestration**: Execution order and dependency management
- **Test Planning**: Strategy, resource, and schedule management
- **Test Coverage**: Measurement and gap analysis
- **Dependency Mapping**: Relationship and constraint analysis

## Ecosystem Relationships

```
Testing Ecosystem Map:
──────────────────────────────
Development Stage → Test Types:
  - Coding → Unit, Mutation, Static Analysis
  - Integration → Integration, Contract, API
  - System → E2E, Smoke, Regression
  - Release → Performance, Security, Compatibility
  - Production → Chaos, Monitoring, Canary

Quality Attribute → Test Types:
  - Functionality → Unit, Integration, E2E, Regression
  - Performance → Load, Stress, Endurance, Spike
  - Security → Vulnerability, Penetration, Audit
  - Usability → User Testing, UX Evaluation
  - Reliability → Chaos, Failover, Recovery
  - Compatibility → Cross-browser, Cross-platform

Test Type Dependencies:
  Smoke → [Unit, Integration, E2E, Performance, Security]
  Unit → [Integration, E2E, Regression]
  Integration → [E2E, Performance, Security]
  E2E → [Performance, Compatibility, Usability]
  Security → [Penetration, Vulnerability, Compliance]
```

## Examples

```bash
# Explore testing ecosystem
npm run test:ecosystem:explore      # Interactive ecosystem exploration
npm run test:ecosystem:map          # Generate ecosystem map
npm run test:ecosystem:relationships # Show test type relationships

# Get guidance for specific contexts
npm run test:ecosystem:guidance -- --context web-application
npm run test:ecosystem:guidance -- --context mobile-app
npm run test:ecosystem:guidance -- --context api-service
npm run test:ecosystem:guidance -- --context enterprise-system

# Analyze current testing ecosystem
npm run test:ecosystem:analyze      # Analyze current test coverage
npm run test:ecosystem:gaps        # Identify ecosystem gaps
npm run test:ecosystem:optimize    # Suggest ecosystem optimization

# Learning and documentation
npm run test:ecosystem:learn       # Learning resources
npm run test:ecosystem:glossary    # Testing terminology
npm run test:ecosystem:patterns    # Testing patterns and anti-patterns
```

## Output format

```
Testing Ecosystem Analysis
──────────────────────────────
Project Context: SaaS Web Application
Stage: Production (2 years in market)
Team Size: 15 developers, 4 QA, 2 DevOps

Current Ecosystem Assessment:
  ✅ Strong Foundation:
    - Unit testing: 85% coverage, mature practices
    - Integration testing: Good API and database coverage
    - E2E testing: Critical paths automated
  
  ⚠️ Moderate Coverage:
    - Performance testing: Basic load testing only
    - Security testing: Vulnerability scanning, no penetration tests
    - Accessibility testing: Partial WCAG compliance
  
  ❌ Weak Areas:
    - Chaos engineering: No resilience testing
    - Contract testing: No API consumer contracts
    - Visual testing: Manual only, no automation

Ecosystem Relationships Analysis:
  Healthy Dependencies:
    - Unit → Integration → E2E flow well established
    - Smoke tests gate deployment effectively
    - Regression testing comprehensive
  
  Missing Dependencies:
    - No performance → chaos dependency (resilience untested)
    - Security tests not integrated with deployment pipeline
    - Accessibility not part of CI workflow

Ecosystem Maturity Score: 7.2/10
  - Foundation: 9/10 (strong functional testing)
  - Non-functional: 6/10 (moderate coverage)
  - Advanced: 4/10 (limited specialized testing)
  - Integration: 8/10 (good pipeline integration)

Recommended Ecosystem Evolution:
  Phase 1 (Next 3 months):
    - Implement visual regression testing
    - Add performance testing to CI pipeline
    - Basic chaos experiments for critical services
  
  Phase 2 (3-6 months):
    - Contract testing for public APIs
    - Penetration testing program
    - Enhanced accessibility automation
  
  Phase 3 (6-12 months):
    - Comprehensive chaos engineering
    - Advanced performance testing (stress, endurance)
    - Production canary testing and feature flags

Test Type Interdependencies to Establish:
  1. Performance tests should run after successful E2E tests
  2. Security scans should gate production deployments
  3. Accessibility tests should be part of PR validation
  4. Chaos experiments should validate monitoring alerts

Ecosystem Anti-Patterns Identified:
  - E2E tests used for unit-level validation (expensive)
  - Performance testing only before major releases (infrequent)
  - Security testing as afterthought, not integrated
  - No test environment for compatibility testing

Resource Allocation Analysis:
  - Current: 70% functional, 20% non-functional, 10% specialized
  - Recommended: 50% functional, 30% non-functional, 20% specialized
  - Justification: Mature product needs more resilience and quality focus

Ecosystem Health Metrics:
  - Test feedback time: 45 minutes (target: < 30 minutes)
  - Defect escape rate: 2.1% (target: < 1%)
  - Test maintenance cost: 15% of development time (target: < 10%)
  - Test flakiness rate: 3.5% (target: < 1%)

Ecosystem Integration Status:
  - CI/CD Integration: 8/10 test types integrated
  - Monitoring Integration: 4/10 test types feeding metrics
  - Alerting Integration: 3/10 test types triggering alerts
  - Reporting Integration: 7/10 test types in reports
```

## Notes

- Testing ecosystems evolve with product maturity
- Balance ecosystem complexity with team capacity
- Different projects need different ecosystem configurations
- Monitor ecosystem health metrics regularly
- Plan ecosystem evolution as part of product roadmap
- Consider ecosystem dependencies when making changes
- Document ecosystem decisions and rationales
- Share ecosystem knowledge across the organization
- Continuously learn from ecosystem performance
- Adapt ecosystem based on changing requirements and context
