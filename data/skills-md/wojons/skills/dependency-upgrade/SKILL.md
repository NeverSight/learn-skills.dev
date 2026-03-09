---
name: dependency-upgrade
description: Analyze and safely upgrade dependencies with breaking change detection, version compatibility checks, impact analysis, and migration planning
license: MIT
compatibility: opencode
metadata:
  audience: developers, devops engineers, security engineers, platform teams
  category: maintenance
---

# Dependency Upgrade

Analyze and safely upgrade software dependencies including OS packages and application libraries with comprehensive breaking change detection, version compatibility analysis, impact assessment on dependent code, and migration planning to maintain system stability and security.

## When to use me

Use this skill when:
- Security vulnerabilities require dependency updates
- New features require dependency version upgrades
- Maintaining compatibility across dependency versions
- Planning major version upgrades with breaking changes
- Pinning dependency versions for reproducibility
- Assessing impact of dependency changes on codebase
- Managing transitive dependency conflicts
- Automating dependency update workflows
- Evaluating dependency upgrade risks and benefits
- Creating migration plans for dependency upgrades

## What I do

### 1. Dependency Analysis
- **Inventory dependencies**: Identify all direct and transitive dependencies
- **Version analysis**: Analyze current versions vs. available versions
- **Dependency graph mapping**: Create dependency relationship graphs
- **Usage analysis**: Determine how dependencies are used in codebase
- **Version pinning assessment**: Evaluate current version pinning strategies

### 2. Breaking Change Detection
- **Changelog analysis**: Parse release notes and changelogs for breaking changes
- **API comparison**: Compare API surface between versions
- **Semantic versioning validation**: Verify version compatibility claims
- **Deprecation detection**: Identify deprecated APIs and features
- **Migration requirement identification**: Determine what needs to change

### 3. Impact Analysis
- **Code usage analysis**: Identify where dependencies are used in code
- **Affected code detection**: Determine which files/lines are impacted
- **Test coverage analysis**: Check if affected code has test coverage
- **Integration impact**: Assess impact on other systems and integrations
- **Performance impact**: Estimate performance implications of upgrades

### 4. Upgrade Planning
- **Upgrade path identification**: Determine optimal upgrade sequence
- **Risk assessment**: Evaluate risks associated with upgrades
- **Effort estimation**: Estimate implementation effort for upgrades
- **Rollback planning**: Create rollback strategies for failed upgrades
- **Staging strategy**: Plan phased rollout approaches

### 5. Safety Validation
- **Compatibility testing**: Verify compatibility with existing code
- **Integration testing**: Test integrations with upgraded dependencies
- **Performance testing**: Benchmark performance before/after
- **Security validation**: Verify security improvements and regressions
- **Regression testing**: Ensure no regressions in functionality

### 6. Automation & Tooling
- **Automated upgrade PR generation**: Create automated upgrade pull requests
- **CI/CD integration**: Integrate with CI/CD pipelines
- **Monitoring integration**: Monitor applications after upgrades
- **Tool recommendations**: Recommend appropriate upgrade tools
- **Workflow automation**: Automate dependency management workflows

## Dependency Types Covered

### Operating System Packages
- **Linux**: apt, yum, dnf, pacman, apk
- **macOS**: Homebrew, MacPorts
- **Windows**: Chocolatey, Winget, Scoop
- **Container**: Base image updates, security patches

### Application Dependencies
- **JavaScript/TypeScript**: npm, yarn, pnpm packages
- **Python**: pip, Poetry, Pipenv packages
- **Java**: Maven, Gradle dependencies
- **Go**: Go modules
- **Ruby**: RubyGems, Bundler
- **Rust**: Cargo crates
- **.NET**: NuGet packages
- **PHP**: Composer packages
- **Swift**: Swift Package Manager
- **Dart/Flutter**: Pub packages

### Infrastructure Dependencies
- **Container images**: Docker, OCI images
- **Terraform modules**: Provider and module versions
- **Kubernetes**: Helm charts, operator versions
- **Cloud services**: SDK and API versions

## Analysis Techniques

### Static Code Analysis
```python
def analyze_dependency_usage(codebase, dependency_name):
    """
    Analyze how a dependency is used in the codebase.
    """
    usage_patterns = {
        'imports': [],
        'function_calls': [],
        'class_instantiations': [],
        'configuration_usage': [],
        'api_calls': []
    }
    
    # Parse source code for dependency usage
    for file_path in codebase.source_files:
        ast = parse_file(file_path)
        
        # Find imports of the dependency
        imports = find_imports(ast, dependency_name)
        if imports:
            usage_patterns['imports'].extend(imports)
        
        # Find usage of dependency APIs
        api_calls = find_api_calls(ast, dependency_name)
        if api_calls:
            usage_patterns['api_calls'].extend(api_calls)
    
    return usage_patterns
```

### Breaking Change Detection
```python
class BreakingChangeAnalyzer:
    def __init__(self, old_version, new_version):
        self.old_version = old_version
        self.new_version = new_version
        
    def analyze_breaking_changes(self):
        """Analyze breaking changes between versions."""
        changes = {
            'api_changes': self.analyze_api_changes(),
            'behavior_changes': self.analyze_behavior_changes(),
            'deprecations': self.analyze_deprecations(),
            'removals': self.analyze_removals(),
            'security_changes': self.analyze_security_changes()
        }
        
        # Calculate impact score
        changes['impact_score'] = self.calculate_impact_score(changes)
        
        return changes
    
    def analyze_api_changes(self):
        """Analyze API surface changes."""
        api_changes = []
        
        # Compare public APIs
        old_apis = extract_public_apis(self.old_version)
        new_apis = extract_public_apis(self.new_version)
        
        # Find removed APIs
        removed = old_apis - new_apis
        if removed:
            api_changes.append({
                'type': 'removed',
                'apis': list(removed),
                'impact': 'high'
            })
        
        # Find changed signatures
        changed = find_changed_signatures(old_apis, new_apis)
        if changed:
            api_changes.append({
                'type': 'signature_change',
                'apis': changed,
                'impact': 'medium'
            })
        
        return api_changes
```

### Impact Analysis Algorithm
```python
def calculate_upgrade_impact(dependency_changes, codebase_usage):
    """
    Calculate the impact of dependency changes on codebase.
    """
    impact_report = {
        'files_affected': [],
        'lines_affected': [],
        'tests_affected': [],
        'risk_level': 'low',
        'estimated_effort': 0
    }
    
    # Map changes to code usage
    for change in dependency_changes:
        affected_code = map_change_to_code(change, codebase_usage)
        
        if affected_code:
            impact_report['files_affected'].extend(affected_code['files'])
            impact_report['lines_affected'].extend(affected_code['lines'])
            
            # Update risk level based on change severity
            if change['impact'] == 'high':
                impact_report['risk_level'] = 'high'
            elif change['impact'] == 'medium' and impact_report['risk_level'] != 'high':
                impact_report['risk_level'] = 'medium'
    
    # Calculate estimated effort
    impact_report['estimated_effort'] = estimate_effort(
        len(impact_report['files_affected']),
        impact_report['risk_level']
    )
    
    return impact_report
```

## Examples

```bash
# Analyze dependency upgrade impact
npm run dependency-upgrade:analyze -- --package react --from 17.0.0 --to 18.0.0 --codebase src/

# Generate upgrade plan
npm run dependency-upgrade:plan -- --dependencies package.json --output upgrade-plan.json

# Check for breaking changes
npm run dependency-upgrade:breaking -- --package lodash --from 4.17.20 --to 4.17.21

# Analyze OS package upgrades
npm run dependency-upgrade:os -- --system ubuntu --packages "nginx,nodejs,postgresql"

# Create automated upgrade PR
npm run dependency-upgrade:pr -- --package axios --to latest --create-pr

# Test upgrade compatibility
npm run dependency-upgrade:test -- --package express --from 4.18.0 --to 5.0.0 --test-suite tests/

# Generate migration code
npm run dependency-upgrade:migrate -- --package moment --to luxon --output migration-guide.md

# Monitor dependency security
npm run dependency-upgrade:security -- --monitor --alert-on-cve

# Batch upgrade analysis
npm run dependency-upgrade:batch -- --file dependencies.json --strategy conservative

# Dependency graph visualization
npm run dependency-upgrade:graph -- --format mermaid --output dependency-graph.md
```

## Output format

### Dependency Upgrade Analysis Report:
```
Dependency Upgrade Analysis Report
──────────────────────────────────
Package: react
Current Version: 17.0.2
Target Version: 18.2.0
Analysis Date: 2026-02-26

Version Analysis:
✅ Security patches: 4 available
⚠️ Minor features: 12 new features
⚠️ Breaking changes: 3 identified
📊 Compatibility: 85% compatible

Breaking Changes Identified:
1. ❌ ReactDOM.render deprecated (High Impact)
   • Current usage: 15 files, 42 calls
   • Replacement: createRoot API
   • Migration effort: 8 hours
   • Risk: High (affects entry points)

2. ⚠️ Automatic batching changes (Medium Impact)
   • Current usage: 8 files, 23 state updates
   • Behavior change: Batched updates timing
   • Testing required: State update tests
   • Risk: Medium (potential UI glitches)

3. ℹ️ New JSX transform required (Low Impact)
   • Current usage: All JSX files
   • Tooling update: Babel/TypeScript config
   • Migration effort: 2 hours
   • Risk: Low (tooling only)

Impact Analysis:
• Files affected: 47 files (15.3% of codebase)
• Lines affected: 328 lines (2.1% of codebase)
• Tests affected: 23 test files (18.4% of tests)
• Estimated effort: 12-16 hours
• Risk level: MEDIUM

Code Usage Patterns:
• Component lifecycle: 85% compatible
• Hooks usage: 95% compatible  
• Context API: 100% compatible
• Error boundaries: 100% compatible

Security Assessment:
• CVEs fixed: 2 critical, 1 high
• Security improvements: 5
• Audit required: No
• Security risk: LOW

Test Coverage:
• Affected code coverage: 78%
• Missing tests: 72 lines (22%)
• Test updates needed: 15 test files

Upgrade Recommendations:
1. Immediate: Update to 17.2.0 (security fixes)
2. Short-term: Migrate to createRoot API
3. Medium-term: Update JSX transform
4. Long-term: Full migration to React 18

Migration Plan:
Phase 1: Security updates (2 hours)
  • Update to 17.2.0
  • Verify security fixes
  • Run security tests

Phase 2: createRoot migration (6 hours)
  • Update entry points (5 files)
  • Update SSR rendering (3 files)
  • Update test utilities (7 files)

Phase 3: Automatic batching (4 hours)
  • Update state management tests
  • Add batching verification
  • Performance testing

Phase 4: JSX transform (2 hours)
  • Update Babel config
  • Update TypeScript config
  • Verify build outputs

Rollback Strategy:
• Feature flag: createRoot usage
• A/B testing: New vs old render
• Monitoring: Error rates, performance
• Rollback trigger: >0.1% error increase

Success Criteria:
• Zero breaking changes in production
• Performance within 5% of baseline
• All tests passing
• Security scans clean
• Monitoring alerts nominal
```

### JSON Output Format:
```json
{
  "analysis": {
    "package": "react",
    "current_version": "17.0.2",
    "target_version": "18.2.0",
    "analysis_date": "2026-02-26",
    "compatibility_score": 85
  },
  "breaking_changes": [
    {
      "id": "bc-react-001",
      "description": "ReactDOM.render deprecated",
      "type": "deprecation",
      "impact": "high",
      "affected_files": 15,
      "affected_lines": 42,
      "replacement": "createRoot API",
      "migration_effort_hours": 8,
      "risk": "high",
      "testing_required": true
    },
    {
      "id": "bc-react-002",
      "description": "Automatic batching changes",
      "type": "behavior_change",
      "impact": "medium",
      "affected_files": 8,
      "affected_lines": 23,
      "migration_effort_hours": 4,
      "risk": "medium",
      "testing_required": true
    }
  ],
  "security_analysis": {
    "cves_fixed": [
      {
        "id": "CVE-2023-12345",
        "severity": "critical",
        "fixed_in": "18.0.0"
      },
      {
        "id": "CVE-2023-12346",
        "severity": "high",
        "fixed_in": "18.1.0"
      }
    ],
    "security_improvements": 5,
    "audit_required": false,
    "overall_risk": "low"
  },
  "impact_summary": {
    "files_affected": 47,
    "lines_affected": 328,
    "tests_affected": 23,
    "estimated_effort_hours": 16,
    "risk_level": "medium",
    "compatibility_percentage": 85
  },
  "upgrade_recommendations": {
    "immediate": "Update to 17.2.0 for security fixes",
    "short_term": "Migrate to createRoot API",
    "medium_term": "Update JSX transform",
    "long_term": "Full migration to React 18"
  },
  "migration_plan": {
    "phases": [
      {
        "phase": 1,
        "name": "Security updates",
        "duration_hours": 2,
        "tasks": [
          "Update to 17.2.0",
          "Verify security fixes",
          "Run security tests"
        ]
      },
      {
        "phase": 2,
        "name": "createRoot migration",
        "duration_hours": 6,
        "tasks": [
          "Update entry points",
          "Update SSR rendering",
          "Update test utilities"
        ]
      }
    ],
    "total_effort_hours": 16,
    "rollback_strategy": "Feature-flagged deployment",
    "success_criteria": [
      "Zero breaking changes",
      "Performance within 5%",
      "All tests passing"
    ]
  }
}
```

### Upgrade Impact Dashboard:
```
Dependency Upgrade Dashboard
───────────────────────────
Status: ANALYSIS_COMPLETE
Last Updated: 2026-02-26 19:45:00

Upgrade Progress:
┌──────────────────────┬──────────┬────────────┐
│ Package             │ Current  │ Target     │
├──────────────────────┼──────────┼────────────┤
│ react               │ 17.0.2   │ 18.2.0     │
│ react-dom           │ 17.0.2   │ 18.2.0     │
│ @types/react        │ 17.0.0   │ 18.0.0     │
│ react-test-renderer │ 17.0.2   │ 18.2.0     │
└──────────────────────┴──────────┴────────────┘

Risk Assessment:
• High Risk: 1 package (react)
• Medium Risk: 2 packages
• Low Risk: 1 package
• Overall Risk: MEDIUM

Security Status:
✅ 2 CVEs fixed
✅ Security improvements: 5
⚠️  Audit recommended: No
✅ Security risk: LOW

Estimated Timeline:
• Analysis: COMPLETE
• Planning: IN_PROGRESS
• Implementation: PENDING
• Testing: PENDING
• Deployment: PENDING

Total Effort: 16 hours (2-3 days)
Target Completion: 2026-03-01

Next Actions:
1. Review breaking changes analysis
2. Approve migration plan
3. Allocate development resources
4. Schedule upgrade window

Monitoring Metrics:
• Error rate: < 0.1% target
• Performance: < 5% degradation
• Test coverage: > 80% target
• Security scan: Clean required
```

## Notes

- **Dependency upgrades require careful planning** - never upgrade dependencies blindly
- **Always test in staging** before deploying to production
- **Monitor applications closely** after dependency upgrades
- **Have rollback plans ready** for unexpected issues
- **Consider transitive dependencies** when upgrading direct dependencies
- **Security updates should be prioritized** over feature updates
- **Version pinning improves reproducibility** but requires regular updates
- **Automated dependency management** reduces manual effort and human error
- **Document upgrade decisions and rationales** for future reference
- **Regular dependency audits** prevent technical debt accumulation