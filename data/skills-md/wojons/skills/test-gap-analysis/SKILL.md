---
name: test-gap-analysis
description: Analyze gaps between requirements/features that should be tested and actual test coverage, identifying testing deficiencies and prioritizing test improvements
license: MIT
compatibility: opencode
metadata:
  audience: QA engineers, developers, test architects, product managers
  category: testing
---

# Test Gap Analysis

Identify discrepancies between requirements/features that should be tested and actual test coverage through systematic analysis of testing completeness, effectiveness, and risk coverage to improve software quality and reliability.

## When to use me

Use this skill when:
- Uncertainty exists about what parts of the system are adequately tested
- New features have been added without corresponding test coverage
- Testing resources are limited and need optimal allocation
- Preparing for releases or deployments with confidence in test coverage
- Auditing testing effectiveness for compliance or quality standards
- Identifying high-risk areas with insufficient testing
- Planning test automation or test improvement initiatives
- Onboarding new team members to understand test coverage
- Assessing technical debt in testing infrastructure
- Validating that critical functionality has appropriate test protection

## What I do

### 1. Requirements Testability Analysis
- **Analyze requirements for testability**: Identify testable aspects of each requirement
- **Extract test conditions and scenarios** from requirements documentation
- **Categorize requirements by test type**: Unit, integration, system, acceptance, performance, security
- **Assess requirement clarity for testing**: Ambiguous vs. testable requirements
- **Identify implicit requirements** that should be tested but aren't documented

### 2. Test Coverage Analysis
- **Analyze existing test suites**: Unit tests, integration tests, end-to-end tests, manual tests
- **Map tests to requirements**: Determine which requirements have test coverage
- **Measure coverage metrics**: Line coverage, branch coverage, requirement coverage, risk coverage
- **Identify test gaps**: Requirements without tests, partial coverage, outdated tests
- **Assess test effectiveness**: Test quality, flakiness, maintenance burden

### 3. Gap Identification & Classification
- **Missing test coverage**: Requirements with no corresponding tests
- **Incomplete test coverage**: Requirements with partial test coverage
- **Outdated tests**: Tests that don't match current requirements
- **Ineffective tests**: Tests that don't adequately validate requirements
- **Risk coverage gaps**: High-risk areas with insufficient testing
- **Test type gaps**: Missing test types (security, performance, accessibility)

### 4. Risk-Based Prioritization
- **Assess business impact** of untested requirements
- **Evaluate technical risk** of inadequate testing
- **Calculate test gap severity** based on impact and likelihood
- **Prioritize test gaps** for remediation planning
- **Estimate effort** to address each test gap
- **Recommend test strategy** based on risk profile

### 5. Test Improvement Recommendations
- **Generate specific test cases** to address gaps
- **Recommend test types and approaches** for each gap
- **Suggest test automation opportunities**
- **Propose test infrastructure improvements**
- **Design test data strategies** for uncovered scenarios
- **Create test maintenance plans** to prevent future gaps

## Test Gap Types

### 1. Coverage Gaps
**Missing Test Coverage**: Requirements with no tests at all  
**Partial Test Coverage**: Requirements with incomplete test coverage  
**Example**: Authentication requirement tested for success but not failure cases

### 2. Type Gaps
**Missing Test Types**: Critical test types not represented (security, performance, etc.)  
**Inappropriate Test Types**: Wrong test type for requirement (unit vs. integration)  
**Example**: Performance-critical feature only has unit tests, no performance tests

### 3. Effectiveness Gaps
**Ineffective Tests**: Tests that don't adequately validate requirements  
**Flaky Tests**: Unreliable tests that provide false confidence  
**Example**: Test passes but doesn't actually validate the requirement

### 4. Maintenance Gaps
**Outdated Tests**: Tests that don't match current requirements  
**Unmaintained Tests**: Tests that fail frequently but aren't fixed  
**Example**: Tests for deprecated functionality still in test suite

### 5. Risk Coverage Gaps
**High-Risk Untested**: Critical functionality without adequate testing  
**Low-Risk Overtested**: Non-critical functionality with excessive testing  
**Example**: Payment processing with minimal tests but UI with extensive tests

## Analysis Techniques

### Requirements Test Extraction
```python
def extract_testable_requirements(requirements_doc):
    """
    Extract testable conditions from requirements.
    """
    testable_items = []
    
    for req in requirements_doc:
        test_conditions = analyze_requirement_for_tests(req)
        
        if test_conditions:
            testable_items.append({
                'requirement_id': req['id'],
                'description': req['description'],
                'test_conditions': test_conditions,
                'test_types': determine_appropriate_test_types(req),
                'priority': calculate_test_priority(req),
                'risk_level': assess_requirement_risk(req)
            })
    
    return testable_items

def analyze_requirement_for_tests(requirement):
    """Extract testable conditions from a requirement."""
    test_conditions = []
    
    # Look for explicit testable statements
    if 'shall' in requirement['text'].lower():
        # Extract what the system shall do
        import re
        shall_pattern = r'shall\s+([^.!?]+)'
        matches = re.findall(shall_pattern, requirement['text'], re.IGNORECASE)
        test_conditions.extend(matches)
    
    # Look for acceptance criteria
    if 'acceptance_criteria' in requirement:
        for criterion in requirement['acceptance_criteria']:
            test_conditions.append(criterion)
    
    # Look for constraints
    if 'constraints' in requirement:
        for constraint in requirement['constraints']:
            test_conditions.append(f"Constraint: {constraint}")
    
    return test_conditions
```

### Test Coverage Mapping
```python
class TestCoverageAnalyzer:
    def __init__(self, requirements, tests):
        self.requirements = requirements
        self.tests = tests
        
    def analyze_coverage(self):
        """Analyze test coverage of requirements."""
        coverage_report = {
            'requirements_count': len(self.requirements),
            'tests_count': len(self.tests),
            'covered_requirements': [],
            'uncovered_requirements': [],
            'partial_coverage': [],
            'coverage_percentage': 0
        }
        
        for req in self.requirements:
            matching_tests = self.find_tests_for_requirement(req)
            
            if not matching_tests:
                coverage_report['uncovered_requirements'].append({
                    'requirement': req,
                    'gap_type': 'missing_coverage'
                })
            elif len(matching_tests) < self.get_expected_test_count(req):
                coverage_report['partial_coverage'].append({
                    'requirement': req,
                    'matching_tests': matching_tests,
                    'expected_count': self.get_expected_test_count(req),
                    'actual_count': len(matching_tests),
                    'gap_type': 'partial_coverage'
                })
            else:
                coverage_report['covered_requirements'].append({
                    'requirement': req,
                    'matching_tests': matching_tests
                })
        
        coverage_report['coverage_percentage'] = (
            len(coverage_report['covered_requirements']) / 
            len(self.requirements) * 100 if self.requirements else 0
        )
        
        return coverage_report
    
    def find_tests_for_requirement(self, requirement):
        """Find tests that cover a requirement."""
        matching_tests = []
        
        for test in self.tests:
            if self.test_covers_requirement(test, requirement):
                matching_tests.append(test)
        
        return matching_tests
    
    def test_covers_requirement(self, test, requirement):
        """Determine if a test covers a requirement."""
        # Check test name for requirement reference
        if requirement['id'] in test.get('name', ''):
            return True
        
        # Check test description for requirement reference
        if requirement['id'] in test.get('description', ''):
            return True
        
        # Check test tags for requirement reference
        if 'tags' in test and requirement['id'] in test['tags']:
            return True
        
        # Semantic analysis (simplified)
        if self.semantic_match(test.get('purpose', ''), requirement['description']):
            return True
        
        return False
```

### Risk-Based Gap Prioritization
```python
def prioritize_test_gaps(test_gaps, risk_assessment):
    """
    Prioritize test gaps based on risk and impact.
    """
    prioritized_gaps = []
    
    for gap in test_gaps:
        # Calculate priority score
        priority_score = calculate_priority_score(gap, risk_assessment)
        
        prioritized_gaps.append({
            **gap,
            'priority_score': priority_score,
            'priority_level': determine_priority_level(priority_score),
            'remediation_effort': estimate_remediation_effort(gap),
            'risk_exposure': calculate_risk_exposure(gap, risk_assessment)
        })
    
    # Sort by priority score (descending)
    prioritized_gaps.sort(key=lambda x: x['priority_score'], reverse=True)
    
    return prioritized_gaps

def calculate_priority_score(gap, risk_assessment):
    """Calculate priority score for a test gap."""
    weights = {
        'business_impact': 0.4,
        'technical_risk': 0.3,
        'user_impact': 0.2,
        'regulatory_requirement': 0.1
    }
    
    scores = {}
    
    # Business impact score
    if gap['requirement']['business_criticality'] == 'high':
        scores['business_impact'] = 1.0
    elif gap['requirement']['business_criticality'] == 'medium':
        scores['business_impact'] = 0.5
    else:
        scores['business_impact'] = 0.2
    
    # Technical risk score
    if gap['requirement']['technical_complexity'] == 'high':
        scores['technical_risk'] = 1.0
    elif gap['requirement']['technical_complexity'] == 'medium':
        scores['technical_risk'] = 0.5
    else:
        scores['technical_risk'] = 0.2
    
    # User impact score
    if gap['requirement']['user_exposure'] == 'high':
        scores['user_impact'] = 1.0
    elif gap['requirement']['user_exposure'] == 'medium':
        scores['user_impact'] = 0.5
    else:
        scores['user_impact'] = 0.2
    
    # Regulatory requirement score
    if gap['requirement'].get('regulatory_requirement', False):
        scores['regulatory_requirement'] = 1.0
    else:
        scores['regulatory_requirement'] = 0.0
    
    # Calculate weighted score
    weighted_score = sum(
        scores[factor] * weights[factor] 
        for factor in weights
    )
    
    return weighted_score
```

## Examples

```bash
# Analyze test coverage gaps
npm run test-gap-analysis:analyze -- --requirements specs/ --tests tests/ --output gaps.json

# Map tests to requirements
npm run test-gap-analysis:map -- --requirements requirements.md --test-suite tests/unit/ --output coverage-map.yaml

# Identify high-risk untested requirements
npm run test-gap-analysis:risk -- --requirements specs/ --tests tests/ --risk-factors risk-assessment.yaml --output risk-gaps.md

# Generate test recommendations
npm run test-gap-analysis:recommend -- --gaps gaps.json --output recommendations.md

# Calculate test coverage metrics
npm run test-gap-analysis:metrics -- --requirements specs/ --tests tests/ --output metrics.json

# Continuous test gap monitoring
npm run test-gap-analysis:monitor -- --watch --requirements specs/ --tests tests/ --alert-on-gap
```

## Output format

### Test Gap Analysis Report:
```
Test Gap Analysis Report
────────────────────────
System: Payment Processing Service
Analysis Date: 2026-02-26
Requirements Analyzed: 42
Tests Analyzed: 127

Test Coverage Summary:
✅ Fully Tested: 28 requirements (66.7%)
⚠️ Partially Tested: 8 requirements (19.0%)
❌ Untested: 6 requirements (14.3%)
📊 Overall Coverage: 76.2%

Critical Test Gaps:

1. ❌ Payment Fraud Detection (High Risk)
   • Requirement: RQ-042: "System shall detect suspicious payment patterns"
   • Risk: Financial loss, regulatory compliance
   • Test Gap: No fraud detection tests
   • Priority: CRITICAL
   • Recommendation: Add fraud detection test suite with edge cases

2. ⚠️ Payment Refund Processing (Medium Risk)
   • Requirement: RQ-038: "System shall process refunds within 24 hours"
   • Risk: Customer dissatisfaction, financial reconciliation
   • Test Gap: Partial coverage (success cases only)
   • Priority: HIGH
   • Recommendation: Add failure scenarios, timeout tests, concurrency tests

3. ⚠️ Multi-Currency Support (Medium Risk)
   • Requirement: RQ-035: "System shall support 15+ currencies"
   • Risk: International expansion blocked
   • Test Gap: Only 5 currencies tested
   • Priority: MEDIUM
   • Recommendation: Add remaining currency tests, exchange rate tests

4. ℹ️ Payment Receipt Generation (Low Risk)
   • Requirement: RQ-041: "System shall generate PDF receipts"
   • Risk: Minor user inconvenience
   • Test Gap: No PDF validation tests
   • Priority: LOW
   • Recommendation: Add PDF generation and validation tests

Risk Analysis:
┌────────────────────┬──────────┬────────────┬──────────────┐
│ Risk Category      │ Coverage│ Risk Level │ Action Needed│
├────────────────────┼──────────┼────────────┼──────────────┤
│ Security          │ 40%      │ HIGH       │ ⚠️ Immediate │
│ Financial         │ 75%      │ MEDIUM     │ 📅 Soon      │
│ Compliance        │ 90%      │ LOW        │ ℹ️ Optional   │
│ User Experience   │ 85%      │ LOW        │ ℹ️ Optional   │
└────────────────────┴──────────┴────────────┴──────────────┘

Test Type Distribution:
• Unit Tests: 68 (53.5%)
• Integration Tests: 42 (33.1%)
• End-to-End Tests: 12 (9.4%)
• Performance Tests: 3 (2.4%)
• Security Tests: 2 (1.6%)

Test Effectiveness:
• Flaky Tests: 8 (6.3%)
• Slow Tests (>1s): 15 (11.8%)
• Unmaintained Tests: 5 (3.9%)
• High-Value Tests: 42 (33.1%)

Remediation Plan:
1. Week 1: Implement fraud detection tests (critical)
2. Week 2: Complete refund processing tests (high)
3. Week 3: Add missing currency tests (medium)
4. Week 4: Fix flaky tests, add PDF tests (low)
5. Ongoing: Test gap monitoring, prevention

Estimated Effort: 2-3 weeks
Target Coverage: 90% by 2026-03-19
```

### Test Gap JSON Output:
```json
{
  "analysis": {
    "system": "payment-processing",
    "timestamp": "2026-02-26T19:00:00Z",
    "requirements_analyzed": 42,
    "tests_analyzed": 127,
    "coverage_percentage": 76.2
  },
  "coverage_summary": {
    "fully_tested": 28,
    "partially_tested": 8,
    "untested": 6,
    "coverage_by_type": {
      "unit": 85.7,
      "integration": 71.4,
      "e2e": 42.9,
      "performance": 14.3,
      "security": 28.6
    }
  },
  "test_gaps": [
    {
      "id": "gap-test-001",
      "requirement_id": "RQ-042",
      "requirement_description": "System shall detect suspicious payment patterns",
      "gap_type": "missing_coverage",
      "risk_level": "critical",
      "business_impact": "high",
      "technical_complexity": "high",
      "user_exposure": "medium",
      "test_types_needed": ["unit", "integration", "security"],
      "recommended_tests": [
        "Test fraud pattern detection",
        "Test threshold-based alerts",
        "Test false positive handling",
        "Test integration with fraud service"
      ],
      "priority_score": 92,
      "priority_level": "critical",
      "estimated_effort_hours": 16,
      "owner": "security-qa-team"
    },
    {
      "id": "gap-test-002",
      "requirement_id": "RQ-038",
      "requirement_description": "System shall process refunds within 24 hours",
      "gap_type": "partial_coverage",
      "existing_tests": 3,
      "needed_tests": 8,
      "missing_test_scenarios": [
        "Refund timeout handling",
        "Concurrent refund processing",
        "Partial refund scenarios",
        "Refund failure recovery"
      ],
      "risk_level": "high",
      "priority_score": 78,
      "priority_level": "high",
      "estimated_effort_hours": 8,
      "owner": "payment-qa-team"
    }
  ],
  "risk_analysis": {
    "high_risk_untested": 2,
    "medium_risk_partial": 3,
    "low_risk_gaps": 4,
    "risk_coverage_score": 65.8
  },
  "test_effectiveness": {
    "flaky_tests": 8,
    "slow_tests": 15,
    "unmaintained_tests": 5,
    "high_value_tests": 42,
    "effectiveness_score": 72.4
  },
  "recommendations": {
    "immediate": [
      "Implement fraud detection test suite",
      "Review and fix flaky security tests"
    ],
    "short_term": [
      "Complete refund processing test coverage",
      "Add missing currency tests"
    ],
    "long_term": [
      "Implement test gap monitoring",
      "Improve test maintenance process"
    ]
  }
}
```

### Test Coverage Dashboard:
```
Test Coverage Dashboard
───────────────────────
Status: ACTIVE
Last Analysis: 2026-02-26 19:00:00
Next Analysis: 2026-02-27 07:00:00

Coverage Trends:
┌──────────────────────────────────────┐
│ Coverage Trend (Last 30 Days)       │
│                                      │
│ 100 ┤                               │
│     │                               │
│  90 ┤                               │
│     │                █              │
│  80 ┤               █ █             │
│     │              █   █            │
│  70 ┤            ██     █           │
│     │          ██        █          │
│  60 ┼───────██───────────█─────────│
│       1   5   10   15   20   25   30 │
│                 Days                 │
└──────────────────────────────────────┘

Current Coverage by Risk Category:
• Critical Security: 40% ⚠️
• High Business Impact: 75% ⚠️
• Medium Complexity: 88% ✅
• Low Risk: 95% ✅

Test Gap Distribution:
• Missing Coverage: 6 gaps
• Partial Coverage: 8 gaps
• Outdated Tests: 5 gaps
• Ineffective Tests: 8 gaps

Test Health Metrics:
• Flaky Test Rate: 6.3% (⚠️ Above threshold)
• Slow Test Rate: 11.8% (✅ Within limits)
• Test Maintenance Score: 72/100 (⚠️ Needs improvement)
• Test Value Score: 65/100 (⚠️ Needs improvement)

Alert Status:
⚠️  2 critical test gaps aging > 7 days
⚠️  Flaky test rate above 5% threshold
✅  Overall coverage above 75% target
✅  High-risk coverage improving

Recommended Actions:
1. Address 2 critical test gaps
2. Reduce flaky test rate below 5%
3. Improve test maintenance score to 80+
4. Increase high-value test percentage
```

## Notes

- **Test gap analysis is not about blame** - focus on improving quality, not assigning fault
- **100% test coverage is rarely the goal** - focus on risk-based testing effectiveness
- **Test gaps indicate quality risks** - not testing failures
- **Regular gap analysis prevents accumulation** - small, frequent analyses better than large audits
- **Involve stakeholders** - developers, QA, product managers should collaborate on test gap resolution
- **Prioritize based on risk** - not all test gaps are equally important
- **Track gap closure** - measure progress in reducing test gaps over time
- **Use test gap analysis proactively** - not just for problem detection but for quality improvement
- **Integrate with development workflow** - test gap analysis should inform testing strategy
- **Document the analysis process** - so it can be repeated and improved
- **Celebrate test gap reduction** - recognize improvements in test coverage and quality