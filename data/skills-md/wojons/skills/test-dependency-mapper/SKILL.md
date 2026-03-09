---
name: test-dependency-mapper
description: Map dependencies and relationships between different test types
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Test Dependency Mapper

Map dependencies, relationships, and execution constraints between different test types to optimize test orchestration and identify bottlenecks.

## When to use me

Use this skill when:
- Understanding how different test types depend on each other
- Optimizing test execution order in CI/CD pipelines
- Identifying test bottlenecks and dependencies
- Planning test infrastructure and environment requirements
- Troubleshooting test execution failures
- Designing comprehensive test strategies
- Onboarding new team members to testing practices

## What I do

- **Dependency analysis**:
  - Map prerequisite relationships between test types
  - Identify execution order constraints
  - Detect circular dependencies
  - Analyze resource dependencies (environments, data, services)

- **Relationship mapping**:
  - Create dependency graphs for test execution
  - Map test types to quality attributes
  - Identify overlapping test coverage areas
  - Analyze test type complementarity

- **Constraint identification**:
  - Environmental constraints (prod vs staging vs local)
  - Data dependencies (test data, fixtures, seeds)
  - Service dependencies (databases, APIs, third-party)
  - Temporal constraints (execution time, scheduling)

- **Optimization recommendations**:
  - Suggest parallel execution opportunities
  - Identify serial execution requirements
  - Recommend dependency reduction strategies
  - Propose test environment optimizations

## Test Dependency Types

1. **Execution Dependencies**: Test B requires Test A to pass first
2. **Environmental Dependencies**: Tests require specific environments
3. **Data Dependencies**: Tests require specific test data
4. **Resource Dependencies**: Tests compete for resources
5. **Temporal Dependencies**: Tests have timing constraints

## Examples

```bash
# Generate dependency map
npm run test:dependencies:map      # Create dependency graph
npm run test:dependencies:analyze  # Analyze dependencies
npm run test:dependencies:visualize # Visualize relationships

# Specific dependency analysis
npm run test:dependencies -- --type execution   # Execution dependencies
npm run test:dependencies -- --type environment # Environment dependencies
npm run test:dependencies -- --type data        # Data dependencies
npm run test:dependencies -- --type resource    # Resource dependencies

# Integration with other tools
npm run test:dependencies -- --format json      # JSON output for automation
npm run test:dependencies -- --format graphviz  # Graphviz for visualization
npm run test:dependencies -- --format mermaid   # Mermaid diagram format

# Dependency optimization
npm run test:dependencies:optimize  # Suggest optimization strategies
npm run test:dependencies:validate  # Validate dependency graph
```

## Output format

```
Test Dependency Mapping Report:
──────────────────────────────
Analysis Scope: Complete testing ecosystem
Test Types Analyzed: 12
Dependencies Identified: 47

Dependency Graph Summary:
  - Nodes: 12 test types
  - Edges: 47 dependencies
  - Circular Dependencies: 0
  - Critical Path: 8 steps

Execution Dependencies:
  smoke → unit (prerequisite)
  smoke → integration (prerequisite)
  unit → e2e (coverage prerequisite)
  integration → e2e (integration prerequisite)
  e2e → performance (environment stability)
  e2e → security (deployed application)
  performance → chaos (baseline established)

Environmental Dependencies:
  Local Environment: unit, integration (lightweight)
  CI Environment: smoke, unit, integration, security
  Staging Environment: e2e, performance, compatibility
  Production-like: chaos, disaster recovery

Data Dependencies:
  Unit Tests: Mock data, no external dependencies
  Integration Tests: Test database with seeded data
  E2E Tests: Realistic user scenarios, test accounts
  Performance Tests: Volume data, load patterns
  Security Tests: Test credentials, vulnerability data

Resource Constraints:
  CPU Intensive: performance, chaos
  Memory Intensive: e2e (browsers), performance
  Network Intensive: compatibility, chaos
  Storage Intensive: database tests, backup tests

Critical Path Analysis:
  1. smoke (1min) → unit (3min) → integration (5min)
  2. → e2e (10min) → performance (8min) → security (3min)
  3. → final validation (1min)
  Total: 31 minutes minimum

Parallelization Opportunities:
  - unit and integration can run in parallel after smoke
  - security can run parallel with e2e (different resources)
  - compatibility testing can run parallel with performance
  - accessibility testing independent after e2e

Optimization Recommendations:
  1. Reduce e2e dependency on integration completion
  2. Parallelize security scanning earlier in pipeline
  3. Implement test data caching to reduce setup time
  4. Use test stubs for external service dependencies

Visualization:
  [Dependency Graph]
  smoke → unit ───┐
  smoke → integration ─┐
        unit → e2e ────┤
  integration → e2e ───┼→ performance → security → final
                 e2e → compatibility ─┘
        unit → accessibility
  integration → api-contract

Impact Analysis:
  - Most critical: smoke tests (blocks everything)
  - Longest path: e2e tests (bottleneck)
  - Most dependencies: e2e tests (depends on 4 other test types)
  - Least dependent: unit tests (only depends on smoke)
```

## Notes

- Dependency mapping should be automated and version controlled
- Update dependency maps when test strategies change
- Consider both technical and organizational dependencies
- Document assumptions and constraints explicitly
- Use dependency analysis for capacity planning
- Validate dependency maps against actual execution
- Consider failure mode dependencies (what fails if X fails)
- Share dependency maps across teams for alignment
- Use dependency analysis for test environment design
- Continuously refine dependencies based on learnings
