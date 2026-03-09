---
name: gap-analysis
description: Identify discrepancies between documented requirements and actual implementation through systematic comparison and analysis
license: MIT
compatibility: opencode
metadata:
  audience: developers, product managers, QA engineers, technical writers
  category: analysis
---

# Gap Analysis

Systematically identify discrepancies between documented requirements, specifications, and actual implementation through comprehensive comparison, analysis, and gap identification to improve system completeness and accuracy.

## When to use me

Use this skill when:
- Requirements documentation exists but implementation status is unclear
- Specifications have evolved but documentation hasn't been updated
- Code changes have been made without corresponding documentation updates
- Preparing for audits, compliance checks, or quality assessments
- Onboarding new team members who need accurate system understanding
- Planning refactoring or modernization efforts
- Validating that implementation matches design intentions
- Identifying technical debt in undocumented features
- Assessing risk from undocumented behavior

## What I do

### 1. Documentation Analysis
- **Parse various documentation formats** (Markdown, YAML, JSON, Confluence, Google Docs exports)
- **Extract requirements and specifications** from structured and unstructured text
- **Identify documented features, constraints, and behaviors**
- **Categorize requirements** by type (functional, non-functional, business, technical)
- **Assess documentation quality** (completeness, clarity, consistency, currency)

### 2. Implementation Analysis
- **Analyze source code** to identify implemented features and behaviors
- **Examine API contracts and interfaces** for exposed capabilities
- **Review database schemas and data models** for persistent structures
- **Inspect configuration files** for system behavior settings
- **Analyze deployment artifacts** for runtime characteristics

### 3. Gap Identification
- **Compare documented vs. implemented features** to identify mismatches
- **Detect undocumented implementations** (features without documentation)
- **Identify unimplemented documentation** (documented but not built)
- **Spot behavioral discrepancies** (documented behavior vs. actual behavior)
- **Find specification drift** where implementation diverged from original specs

### 4. Gap Classification & Prioritization
- **Categorize gaps** by type (missing, incomplete, incorrect, outdated)
- **Assess gap severity** (critical, high, medium, low)
- **Estimate effort** to address each gap
- **Prioritize gaps** based on impact, risk, and effort
- **Group related gaps** for efficient resolution

### 5. Recommendations & Remediation Planning
- **Generate gap resolution recommendations** for each identified discrepancy
- **Create remediation plans** with actionable steps
- **Suggest documentation updates** to align with implementation
- **Propose implementation changes** to match documentation
- **Design verification strategies** to confirm gap closure

## Analysis Techniques

### Document Parsing Patterns
```yaml
document_sources:
  requirements:
    patterns:
      - "As a [role], I want [feature] so that [benefit]"
      - "The system shall [requirement]"
      - "Must support [capability]"
      - "Should be able to [action]"
  
  specifications:
    patterns:
      - "### Feature: [name]"
      - "**Specification:** [details]"
      - "| Parameter | Type | Required | Description |"
      - "API endpoint: [method] [path]"
  
  architecture:
    patterns:
      - "Component: [name]"
      - "Responsibility: [description]"
      - "Interfaces: [list]"
      - "Data flow: [description]"
```

### Code Analysis Approaches
```python
def analyze_implementation(codebase_path):
    """
    Analyze code implementation for features and behaviors.
    """
    features = extract_features_from_code(codebase_path)
    apis = extract_api_endpoints(codebase_path)
    data_models = extract_data_models(codebase_path)
    configs = parse_configuration_files(codebase_path)
    
    return {
        'implemented_features': features,
        'api_endpoints': apis,
        'data_models': data_models,
        'configurations': configs,
        'behavioral_patterns': extract_behavioral_patterns(codebase_path)
    }
```

### Gap Detection Algorithms
```python
class GapAnalyzer:
    def detect_gaps(self, documented, implemented):
        """
        Detect gaps between documented and implemented items.
        """
        gaps = {
            'undocumented_implementations': [],
            'unimplemented_documentation': [],
            'behavioral_mismatches': [],
            'specification_drift': []
        }
        
        # Find undocumented implementations
        for impl_item in implemented:
            if not self.is_documented(impl_item, documented):
                gaps['undocumented_implementations'].append(impl_item)
        
        # Find unimplemented documentation
        for doc_item in documented:
            if not self.is_implemented(doc_item, implemented):
                gaps['unimplemented_documentation'].append(doc_item)
        
        # Find behavioral mismatches
        for doc_item in documented:
            impl_item = self.find_matching_implementation(doc_item, implemented)
            if impl_item and not self.behaviors_match(doc_item, impl_item):
                gaps['behavioral_mismatches'].append({
                    'documented': doc_item,
                    'implemented': impl_item,
                    'differences': self.find_differences(doc_item, impl_item)
                })
        
        return gaps
```

## Gap Types

### 1. Missing Documentation
**Symptoms**: Feature exists in code but has no documentation
**Impact**: Knowledge silos, difficult maintenance, increased onboarding time
**Example**: API endpoint implemented but not documented in API docs

### 2. Missing Implementation
**Symptoms**: Documented feature not found in code
**Impact**: Unmet expectations, broken promises, customer dissatisfaction
**Example**: "Export to PDF" documented but not implemented

### 3. Behavioral Mismatch
**Symptoms**: Documentation describes different behavior than implementation
**Impact**: Bugs, integration issues, unexpected behavior
**Example**: Documentation says "case-insensitive search" but implementation is case-sensitive

### 4. Outdated Documentation
**Symptoms**: Documentation references deprecated features or old interfaces
**Impact**: Confusion, incorrect usage, wasted development time
**Example**: Documentation shows old API version 1.0 but implementation is 2.0

### 5. Incomplete Documentation
**Symptoms**: Documentation exists but lacks important details
**Impact**: Partial understanding, guesswork, implementation errors
**Example**: API documented but missing error responses or rate limits

### 6. Over-specified Documentation
**Symptoms**: Documentation specifies details not reflected in implementation
**Impact**: Implementation flexibility reduced, maintenance burden increased
**Example**: Documentation specifies exact algorithm but implementation uses different approach

## Examples

```bash
# Analyze gaps between requirements docs and implementation
npm run gap-analysis:analyze -- --requirements requirements.md --code src/ --output gaps.json

# Compare API documentation with actual implementation
npm run gap-analysis:compare -- --api-docs api.md --code src/api/ --output api-gaps.yaml

# Identify undocumented features
npm run gap-analysis:undocumented -- --code src/ --docs docs/ --output undocumented-features.md

# Check for unimplemented requirements
npm run gap-analysis:unimplemented -- --requirements specs/ --code src/ --output missing-features.json

# Generate remediation plan
npm run gap-analysis:remediate -- --gaps gaps.json --output remediation-plan.md

# Continuous gap monitoring
npm run gap-analysis:monitor -- --watch --requirements docs/ --code src/ --alert-on-gap
```

## Output format

### Gap Analysis Report:
```
Gap Analysis Report
───────────────────
System: User Management Service
Analysis Date: 2026-02-26
Documents Analyzed: 3 (requirements.md, api-spec.yaml, architecture.md)
Code Analyzed: 42 files, 8,567 lines

Summary:
✅ Documented & Implemented: 28 features (70%)
⚠️  Documented but Not Implemented: 6 features (15%)
⚠️  Implemented but Not Documented: 4 features (10%)
❌ Behavioral Mismatches: 2 features (5%)

Gap Details:

1. CRITICAL: Missing Implementation
   • Feature: "User password reset via email"
   • Location: requirements.md:45
   • Impact: Security feature missing
   • Effort: Medium (3-5 days)
   • Recommendation: Implement password reset flow

2. HIGH: Missing Documentation
   • Feature: "User session invalidation on role change"
   • Location: src/auth/session.js:123
   • Impact: Undocumented security behavior
   • Effort: Low (2 hours)
   • Recommendation: Document in security.md

3. MEDIUM: Behavioral Mismatch
   • Documented: "Search returns max 100 results"
   • Implemented: "Search returns max 50 results"
   • Location: api.md:89 vs src/search.js:45
   • Impact: Performance vs functionality tradeoff
   • Effort: Low (configuration change)
   • Recommendation: Align implementation with docs or update docs

4. LOW: Outdated Documentation
   • Documented: "API version 1.2"
   • Implemented: "API version 2.0"
   • Location: api.md:1 (header)
   • Impact: Confusion for API consumers
   • Effort: Low (documentation update)
   • Recommendation: Update API documentation

Priority Matrix:
┌─────────────┬─────────┬─────────┬──────────────┐
│ Priority    │ Count   │ Effort  │ Risk         │
├─────────────┼─────────┼─────────┼──────────────┤
│ Critical    │ 1       │ 3-5 days│ Security     │
│ High        │ 2       │ 1 day   │ Compliance   │
│ Medium      │ 3       │ 2 days  │ User Experience│
│ Low         │ 6       │ 3 days  │ Maintenance  │
└─────────────┴─────────┴─────────┴──────────────┘

Remediation Plan:
1. Week 1: Address critical security gap (password reset)
2. Week 2: Document undocumented security features
3. Week 3: Align behavioral mismatches
4. Week 4: Update outdated documentation
5. Ongoing: Implement gap monitoring to prevent recurrence
```

### Gap Analysis JSON Output:
```json
{
  "analysis": {
    "system": "user-management",
    "timestamp": "2026-02-26T19:00:00Z",
    "documents_analyzed": ["requirements.md", "api-spec.yaml"],
    "code_analyzed": ["src/", "lib/"],
    "summary": {
      "total_features": 40,
      "documented_and_implemented": 28,
      "documented_not_implemented": 6,
      "implemented_not_documented": 4,
      "behavioral_mismatches": 2,
      "gap_percentage": 30
    }
  },
  "gaps": [
    {
      "id": "gap-001",
      "type": "missing_implementation",
      "severity": "critical",
      "description": "User password reset via email not implemented",
      "document_reference": "requirements.md:45",
      "code_reference": null,
      "impact": "Security feature missing, violates compliance requirements",
      "effort_estimate": "3-5 days",
      "recommendation": "Implement password reset flow with email verification",
      "owner": "security-team",
      "due_date": "2026-03-05"
    },
    {
      "id": "gap-002",
      "type": "missing_documentation",
      "severity": "high",
      "description": "User session invalidation on role change not documented",
      "document_reference": null,
      "code_reference": "src/auth/session.js:123",
      "impact": "Undocumented security behavior, audit finding risk",
      "effort_estimate": "2 hours",
      "recommendation": "Add to security documentation and API docs",
      "owner": "documentation-team",
      "due_date": "2026-03-01"
    }
  ],
  "remediation_plan": {
    "phases": [
      {
        "phase": 1,
        "name": "Critical Security Gaps",
        "duration": "1 week",
        "gaps": ["gap-001"],
        "deliverables": ["Password reset implementation", "Security review"]
      },
      {
        "phase": 2,
        "name": "Documentation Cleanup",
        "duration": "1 week",
        "gaps": ["gap-002"],
        "deliverables": ["Updated security docs", "API documentation"]
      }
    ],
    "total_effort": "2 weeks",
    "priority_order": ["gap-001", "gap-002"],
    "success_criteria": ["All critical gaps closed", "Documentation coverage > 90%"]
  }
}
```

### Gap Monitoring Dashboard:
```
Gap Monitoring Dashboard
────────────────────────
Status: ACTIVE
Last Analysis: 2026-02-26 19:00:00
Next Analysis: 2026-02-27 07:00:00

Trends:
┌──────────────────────────────────────┐
│ Gap Trend (Last 30 Days)            │
│                                      │
│ 40 ┤                                │
│    │                                │
│ 30 ┤                █               │
│    │               █ █              │
│ 20 ┤              █   █             │
│    │             █     █            │
│ 10 ┤           █       █           │
│    │          █         █          │
│  0 ┼───────────█─────────█─────────│
│     1   5   10   15   20   25   30 │
│              Days                  │
└──────────────────────────────────────┘

Current Gaps by Type:
• Missing Documentation: 4 (33%)
• Missing Implementation: 3 (25%)
• Behavioral Mismatch: 3 (25%)
• Outdated Documentation: 2 (17%)

Gap Age Distribution:
• < 1 week: 6 gaps
• 1-4 weeks: 4 gaps
• 1-3 months: 2 gaps
• > 3 months: 0 gaps

Alert Status:
✅ No critical gaps
⚠️  2 high-priority gaps aging > 2 weeks
✅ Documentation coverage: 85%
✅ Implementation coverage: 90%

Recommended Actions:
1. Address 2 high-priority gaps aging > 2 weeks
2. Improve documentation for 4 undocumented features
3. Schedule review for 3 behavioral mismatches
```

## Notes

- **Gap analysis is not a blame exercise** - focus on improving the system, not assigning fault
- **Regular gap analysis prevents accumulation** - small, frequent analyses are better than large, infrequent ones
- **Automate where possible** - continuous gap detection catches issues early
- **Involve stakeholders** - developers, product managers, and technical writers should collaborate on gap resolution
- **Prioritize based on impact** - not all gaps are equally important
- **Track gap closure** - measure progress in reducing gaps over time
- **Use gap analysis proactively** - not just for problem detection but for quality improvement
- **Integrate with development workflow** - gap analysis should inform planning and prioritization
- **Document the analysis process** - so it can be repeated and improved
- **Celebrate gap reduction** - recognize improvements in system completeness and accuracy