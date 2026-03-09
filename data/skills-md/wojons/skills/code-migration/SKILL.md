---
name: code-migration
description: Guide framework and library migrations with incremental strategies, breaking change analysis, compatibility testing, and automated migration tools
license: MIT
compatibility: opencode
metadata:
  audience: developers, platform engineers, migration teams, architects
  category: maintenance
---

# Code Migration

Guide framework and library migrations with incremental strategies, breaking change analysis, compatibility testing, and automated migration tools to safely transition codebases between versions, frameworks, and architectures while minimizing risk and maintaining functionality.

## When to use me

Use this skill when:
- Upgrading between major framework versions (React, Angular, .NET, etc.)
- Migrating between frameworks (Angular to React, jQuery to Vue, etc.)
- Transitioning between architectural patterns (monolith to microservices)
- Adopting new language versions or runtime environments
- Replacing deprecated libraries with modern alternatives
- Consolidating multiple codebases or technology stacks
- Preparing for end-of-life technology deprecation
- Implementing incremental migration strategies
- Automating repetitive migration patterns
- Validating migration correctness and completeness

## What I do

### 1. Migration Planning
- **Migration strategy selection**: Choose appropriate migration approach (big bang, incremental, parallel, strangler pattern)
- **Dependency analysis**: Map all dependencies and compatibility constraints
- **Risk assessment**: Evaluate technical and business risks of migration
- **Effort estimation**: Calculate time, resources, and complexity of migration
- **Staging plan creation**: Define phased rollout and validation steps

### 2. Breaking Change Analysis
- **API surface comparison**: Analyze differences between source and target APIs
- **Behavior change detection**: Identify functional and behavioral changes
- **Deprecation mapping**: Track deprecated features and their replacements
- **Compatibility matrix creation**: Build comprehensive compatibility reference
- **Migration requirement identification**: Determine what needs to change

### 3. Incremental Migration Support
- **Parallel run capability**: Support running old and new versions simultaneously
- **Feature flag integration**: Implement feature toggles for gradual rollout
- **Data migration planning**: Plan database and data structure migrations
- **Integration bridge creation**: Build compatibility layers and adapters
- **Rollback strategy development**: Create safe rollback procedures

### 4. Automated Migration Tools
- **Code transformation generation**: Create automated code modification scripts
- **Test migration automation**: Migrate and update test suites
- **Configuration migration**: Automate configuration file updates
- **Build system migration**: Update build tools and pipelines
- **Deployment automation**: Automate deployment process changes

### 5. Testing & Validation
- **Compatibility testing**: Verify functionality preservation
- **Performance comparison**: Compare performance before/after migration
- **Integration testing**: Test interfaces with other systems
- **Regression testing**: Ensure no regressions in existing functionality
- **Acceptance validation**: Validate migration meets business requirements

### 6. Documentation & Training
- **Migration guide creation**: Develop comprehensive migration documentation
- **Team training materials**: Create training for new technologies
- **Knowledge transfer planning**: Plan knowledge sharing sessions
- **Support documentation**: Update support and operational documentation
- **Lessons learned capture**: Document migration insights and best practices

## Migration Types Covered

### Framework Version Upgrades
- **Frontend**: React 16 → 18, Angular 12 → 16, Vue 2 → 3
- **Backend**: .NET Framework → .NET Core/5/6/7/8, Spring Boot major versions
- **Mobile**: React Native version upgrades, Flutter SDK upgrades
- **Database**: MySQL 5.7 → 8.0, PostgreSQL 11 → 16, MongoDB 3.6 → 7.0

### Framework-to-Framework Migrations
- **Frontend**: Angular → React, jQuery → Vue, Backbone → React
- **Backend**: PHP → Node.js, Ruby on Rails → Django, .NET → Go
- **Mobile**: Native iOS/Android → React Native/Flutter
- **Database**: MySQL → PostgreSQL, SQL Server → MySQL, Oracle → PostgreSQL

### Architectural Migrations
- **Monolith to Microservices**: Decompose monolithic applications
- **Server-side to Client-side**: Transition from server-rendered to SPA
- **On-premise to Cloud**: Migrate to cloud-native architectures
- **Synchronous to Async**: Move from synchronous to event-driven architectures

### Language Migrations
- **JavaScript to TypeScript**: Add type safety to JavaScript codebases
- **Python 2 to Python 3**: Upgrade Python versions
- **Java 8 to Java 17+**: Modernize Java codebases
- **PHP 5 to PHP 8**: Upgrade PHP applications

## Analysis Techniques

### Migration Strategy Selection Algorithm
```python
def select_migration_strategy(project_characteristics):
    """
    Select appropriate migration strategy based on project characteristics.
    """
    strategies = {
        'big_bang': {
            'score': 0,
            'conditions': ['small_codebase', 'low_complexity', 'minimal_dependencies']
        },
        'incremental': {
            'score': 0,
            'conditions': ['large_codebase', 'high_complexity', 'many_dependencies']
        },
        'parallel_run': {
            'score': 0,
            'conditions': ['business_critical', 'zero_downtime', 'high_availability']
        },
        'strangler_pattern': {
            'score': 0,
            'conditions': ['monolithic', 'legacy_system', 'gradual_replacement']
        }
    }
    
    # Score each strategy based on project characteristics
    for characteristic in project_characteristics:
        for strategy_name, strategy_info in strategies.items():
            if characteristic in strategy_info['conditions']:
                strategy_info['score'] += 1
    
    # Select highest scoring strategy
    selected_strategy = max(strategies.items(), key=lambda x: x[1]['score'])
    
    return {
        'strategy': selected_strategy[0],
        'score': selected_strategy[1]['score'],
        'rationale': generate_strategy_rationale(selected_strategy[0], project_characteristics)
    }

def generate_strategy_rationale(strategy, characteristics):
    """Generate rationale for selected migration strategy."""
    rationales = {
        'big_bang': "Complete migration in single phase suitable for small, simple codebases",
        'incremental': "Gradual migration reducing risk for large, complex systems",
        'parallel_run': "Maintain both old and new systems during transition for critical systems",
        'strangler_pattern': "Gradually replace legacy system components while maintaining functionality"
    }
    
    return rationales.get(strategy, "Standard migration approach")
```

### Breaking Change Analysis
```python
class BreakingChangeAnalyzer:
    def __init__(self, source_api, target_api):
        self.source_api = source_api
        self.target_api = target_api
        
    def analyze_breaking_changes(self):
        """Comprehensive breaking change analysis."""
        analysis = {
            'api_removals': self.find_removed_apis(),
            'signature_changes': self.find_signature_changes(),
            'behavior_changes': self.find_behavior_changes(),
            'deprecations': self.find_deprecations(),
            'new_requirements': self.find_new_requirements()
        }
        
        # Calculate migration complexity score
        analysis['complexity_score'] = self.calculate_complexity_score(analysis)
        analysis['migration_effort'] = self.estimate_migration_effort(analysis)
        
        return analysis
    
    def find_removed_apis(self):
        """Find APIs removed in target version."""
        removed = []
        
        for api in self.source_api:
            if api not in self.target_api:
                removed.append({
                    'api': api,
                    'type': 'removed',
                    'impact': 'high',
                    'migration_action': 'find_replacement_or_rewrite'
                })
        
        return removed
    
    def find_signature_changes(self):
        """Find APIs with changed signatures."""
        changed = []
        
        for api in self.source_api:
            if api in self.target_api:
                source_sig = self.source_api[api]['signature']
                target_sig = self.target_api[api]['signature']
                
                if source_sig != target_sig:
                    changed.append({
                        'api': api,
                        'type': 'signature_change',
                        'source_signature': source_sig,
                        'target_signature': target_sig,
                        'impact': 'medium',
                        'migration_action': 'update_calls'
                    })
        
        return changed
```

### Incremental Migration Planner
```python
def create_incremental_migration_plan(codebase, migration_strategy):
    """
    Create incremental migration plan with phases.
    """
    phases = []
    
    # Phase 1: Preparation
    phases.append({
        'phase': 1,
        'name': 'Preparation & Setup',
        'tasks': [
            'Set up new framework/project structure',
            'Configure build and deployment pipelines',
            'Implement feature flags for migration control',
            'Create compatibility layer/adapters',
            'Set up monitoring and observability'
        ],
        'success_criteria': [
            'New project builds successfully',
            'Feature flags operational',
            'Monitoring configured',
            'Rollback procedures tested'
        ]
    })
    
    # Phase 2: Dependency Migration
    phases.append({
        'phase': 2,
        'name': 'Dependency Migration',
        'tasks': [
            'Migrate shared libraries and utilities',
            'Update build dependencies',
            'Create shared interfaces and contracts',
            'Test library compatibility'
        ],
        'success_criteria': [
            'All dependencies compatible with both versions',
            'Shared libraries functioning',
            'Build system supports both versions'
        ]
    })
    
    # Phase 3: Component Migration
    components = identify_migration_components(codebase)
    for i, component_group in enumerate(chunk_components(components, 5), 3):
        phases.append({
            'phase': i,
            'name': f'Component Migration Group {i-2}',
            'components': component_group,
            'tasks': [
                f'Migrate {len(component_group)} components',
                'Update integration tests',
                'Perform component-level testing',
                'Enable via feature flags'
            ],
            'success_criteria': [
                'All components migrated successfully',
                'Integration tests passing',
                'Feature flags controlling migration',
                'No performance regressions'
            ]
        })
    
    # Final Phase: Cleanup
    phases.append({
        'phase': len(phases) + 1,
        'name': 'Cleanup & Optimization',
        'tasks': [
            'Remove old code and dependencies',
            'Clean up feature flags',
            'Optimize new implementation',
            'Update documentation',
            'Train team on new system'
        ],
        'success_criteria': [
            'Old code completely removed',
            'Performance meets targets',
            'Documentation updated',
            'Team trained and proficient'
        ]
    })
    
    return {
        'total_phases': len(phases),
        'estimated_duration': calculate_duration(phases),
        'phases': phases,
        'risk_mitigation': create_risk_mitigation_plan(phases)
    }
```

## Examples

```bash
# Analyze migration from Angular 12 to 16
npm run code-migration:analyze -- --source angular --source-version 12 --target angular --target-version 16 --codebase src/

# Create incremental migration plan
npm run code-migration:plan -- --strategy incremental --framework react --from 16 --to 18 --output migration-plan.json

# Generate automated migration scripts
npm run code-migration:generate -- --framework .net --from 4.8 --to 8.0 --codebase . --output migration-scripts/

# Test migration compatibility
npm run code-migration:test -- --source-code src/ --target-framework vue-3 --tests tests/ --output compatibility-report.json

# Execute phased migration
npm run code-migration:execute -- --plan migration-plan.json --phase 2 --dry-run

# Monitor migration progress
npm run code-migration:monitor -- --plan migration-plan.json --metrics coverage,performance,errors --dashboard

# Validate migration completeness
npm run code-migration:validate -- --source src/ --target dist/ --validation-tests tests/validation/

# Create rollback plan
npm run code-migration:rollback -- --plan migration-plan.json --trigger error-rate --threshold 1%

# Generate migration documentation
npm run code-migration:docs -- --plan migration-plan.json --template comprehensive --output docs/migration-guide.md

# Train team on migrated codebase
npm run code-migration:train -- --new-framework react-18 --training-modules all --output training-materials/
```

## Output format

### Code Migration Analysis Report:
```
Code Migration Analysis Report
──────────────────────────────
Source: Angular 12 Application
Target: Angular 16
Analysis Date: 2026-02-26
Codebase Size: 45,328 lines, 247 files

Migration Strategy Recommendation: INCREMENTAL MIGRATION
Rationale: Large codebase with complex dependencies and business-critical functionality

Breaking Changes Analysis:
❌ Critical Changes: 12
⚠️ Medium Changes: 28
ℹ️ Minor Changes: 45
✅ Compatible: 320 APIs

Critical Breaking Changes:
1. ❌ Ivy Compiler Required (Impact: High)
   • Current: View Engine compiler
   • Required: Ivy compiler (Angular 13+)
   • Migration: Update angular.json and tsconfig.json
   • Effort: 8 hours

2. ❌ RxJS 7 Required (Impact: High)
   • Current: RxJS 6.6.7
   • Required: RxJS 7.8.0+
   • Breaking Changes: Operator function changes, observable creation
   • Effort: 16 hours

3. ❌ TypeScript 4.7+ Required (Impact: High)
   • Current: TypeScript 4.2.4
   • Required: TypeScript 4.7.2+
   • Migration: Update tsconfig.json, fix type errors
   • Effort: 12 hours

Dependency Analysis:
┌──────────────────────┬────────────┬────────────┬────────────┐
│ Dependency          │ Current    │ Required   │ Status     │
├──────────────────────┼────────────┼────────────┼────────────┤
│ @angular/core       │ 12.2.16    │ 16.2.0     ❌ Upgrade    │
│ @angular/cli        │ 12.2.18    │ 16.2.0     ❌ Upgrade    │
│ rxjs                │ 6.6.7      │ 7.8.0      ❌ Upgrade    │
│ typescript          │ 4.2.4      │ 4.7.2      ❌ Upgrade    │
│ zone.js             │ 0.11.4     │ 0.13.0     ⚠️ Compatible │
│ @angular/material   │ 12.2.13    │ 16.2.0     ❌ Upgrade    │
└──────────────────────┴────────────┴────────────┴────────────┘

Code Impact Assessment:
• Components affected: 142 (57% of total)
• Services affected: 45 (92% of total)
• Directives affected: 18 (75% of total)
• Pipes affected: 12 (100% of total)
• Tests affected: 245 (98% of total)

Migration Complexity Score: 78/100 (High Complexity)
Estimated Effort: 120-160 hours (3-4 weeks)

Incremental Migration Plan:
Phase 1: Foundation (1 week)
  • Update build system and dependencies
  • Configure Ivy compiler
  • Set up feature flags for migration

Phase 2: Core Libraries (1 week)
  • Migrate RxJS to version 7
  • Update TypeScript to 4.7+
  • Update zone.js compatibility

Phase 3: Angular Core (2 weeks)
  • Update @angular/core to v16
  • Migrate @angular/cli
  • Update component lifecycle methods

Phase 4: UI Libraries (1 week)
  • Update @angular/material
  • Migrate custom UI components
  • Update CSS and theming

Phase 5: Testing & Validation (1 week)
  • Update test utilities
  • Run comprehensive tests
  • Performance benchmarking

Risk Assessment:
• Technical Risk: HIGH (multiple breaking changes)
• Business Risk: MEDIUM (downtime during migration)
• Schedule Risk: MEDIUM (complex dependency chain)
• Team Risk: LOW (Angular expertise available)

Risk Mitigation Strategies:
1. Implement feature flags for gradual rollout
2. Maintain parallel branches during migration
3. Extensive automated testing
4. Regular stakeholder updates
5. Rollback procedures defined

Testing Strategy:
• Unit Tests: Update all 245 test files
• Integration Tests: Test component interactions
• E2E Tests: Verify user workflows
• Performance Tests: Compare before/after metrics
• Compatibility Tests: Verify browser support

Success Criteria:
1. All tests passing in new environment
2. Performance within 10% of baseline
3. Zero breaking changes in production
4. Team proficient with Angular 16 features
5. Documentation updated and complete

Tooling Recommendations:
1. Angular Update Guide (ng update)
2. RxJS upgrade helper
3. TypeScript migration scripts
4. Automated test migration tools
5. Performance monitoring setup

Next Steps:
1. Approve migration plan and timeline
2. Allocate development resources
3. Schedule migration window
4. Set up monitoring and alerting
5. Begin Phase 1 implementation

Migration Dashboard:
Status: PLANNING_COMPLETE
Current Phase: Preparation
Progress: 0%
Estimated Completion: 2026-03-26
Risks: 3 high, 2 medium, 1 low
```

### JSON Output Format:
```json
{
  "analysis": {
    "source": "Angular 12 Application",
    "target": "Angular 16",
    "analysis_date": "2026-02-26",
    "codebase_size": {
      "lines": 45328,
      "files": 247,
      "components": 250,
      "services": 49,
      "directives": 24,
      "pipes": 12
    },
    "recommended_strategy": "incremental",
    "complexity_score": 78,
    "estimated_effort_hours": 140
  },
  "breaking_changes": {
    "critical": [
      {
        "id": "bc-angular-001",
        "description": "Ivy Compiler Required",
        "type": "compiler_change",
        "impact": "high",
        "current": "View Engine compiler",
        "required": "Ivy compiler (Angular 13+)",
        "migration_action": "Update angular.json and tsconfig.json",
        "estimated_effort_hours": 8
      },
      {
        "id": "bc-angular-002",
        "description": "RxJS 7 Required",
        "type": "dependency_change",
        "impact": "high",
        "current": "RxJS 6.6.7",
        "required": "RxJS 7.8.0+",
        "breaking_changes": "Operator function changes, observable creation",
        "estimated_effort_hours": 16
      }
    ],
    "medium": 28,
    "minor": 45,
    "compatible": 320
  },
  "dependencies": [
    {
      "name": "@angular/core",
      "current": "12.2.16",
      "required": "16.2.0",
      "status": "upgrade_required",
      "impact": "high"
    },
    {
      "name": "@angular/cli",
      "current": "12.2.18",
      "required": "16.2.0",
      "status": "upgrade_required",
      "impact": "high"
    }
  ],
  "impact_assessment": {
    "components_affected": 142,
    "components_percentage": 57,
    "services_affected": 45,
    "services_percentage": 92,
    "directives_affected": 18,
    "directives_percentage": 75,
    "pipes_affected": 12,
    "pipes_percentage": 100,
    "tests_affected": 245,
    "tests_percentage": 98
  },
  "migration_plan": {
    "phases": [
      {
        "phase": 1,
        "name": "Foundation",
        "duration_weeks": 1,
        "tasks": [
          "Update build system and dependencies",
          "Configure Ivy compiler",
          "Set up feature flags for migration"
        ],
        "success_criteria": [
          "New project builds successfully",
          "Feature flags operational",
          "Monitoring configured"
        ]
      },
      {
        "phase": 2,
        "name": "Core Libraries",
        "duration_weeks": 1,
        "tasks": [
          "Migrate RxJS to version 7",
          "Update TypeScript to 4.7+",
          "Update zone.js compatibility"
        ],
        "success_criteria": [
          "RxJS migration complete",
          "TypeScript compilation successful",
          "Zone.js compatibility verified"
        ]
      }
    ],
    "total_phases": 5,
    "total_duration_weeks": 6,
    "estimated_completion_date": "2026-03-26"
  },
  "risk_assessment": {
    "technical_risk": "high",
    "business_risk": "medium",
    "schedule_risk": "medium",
    "team_risk": "low",
    "mitigation_strategies": [
      "Implement feature flags for gradual rollout",
      "Maintain parallel branches during migration",
      "Extensive automated testing",
      "Regular stakeholder updates",
      "Rollback procedures defined"
    ]
  },
  "testing_strategy": {
    "unit_tests": {
      "count": 245,
      "action": "update_all"
    },
    "integration_tests": {
      "focus": "component interactions",
      "coverage": "high"
    },
    "e2e_tests": {
      "focus": "user workflows",
      "automation": "full"
    },
    "performance_tests": {
      "metrics": ["response_time", "memory_usage", "bundle_size"],
      "comparison": "before_after"
    }
  },
  "tooling_recommendations": [
    "Angular Update Guide (ng update)",
    "RxJS upgrade helper",
    "TypeScript migration scripts",
    "Automated test migration tools",
    "Performance monitoring setup"
  ],
  "next_steps": [
    "Approve migration plan and timeline",
    "Allocate development resources",
    "Schedule migration window",
    "Set up monitoring and alerting",
    "Begin Phase 1 implementation"
  ]
}
```

### Migration Dashboard:
```
Code Migration Dashboard
───────────────────────
Project: E-commerce Platform
Migration: Angular 12 → 16
Status: IN_PROGRESS
Current Phase: 3/5 (Angular Core Migration)

Progress Summary:
┌──────────────────────┬──────────┬────────────┬────────────┐
│ Phase                │ Status   │ Progress   │ Timeline   │
├──────────────────────┼──────────┼────────────┼────────────┤
│ 1. Foundation        │ ✅ Done  │ 100%       │ Feb 19-26  │
│ 2. Core Libraries    │ ✅ Done  │ 100%       │ Feb 26-Mar 5│
│ 3. Angular Core      │ 🔄 Active│ 65%        │ Mar 5-19   │
│ 4. UI Libraries      │ ⏳ Pending│ 0%        │ Mar 19-26  │
│ 5. Testing & Validation│ ⏳ Pending│ 0%        │ Mar 26-Apr 2│
└──────────────────────┴──────────┴────────────┴────────────┘

Current Phase Details:
• Components migrated: 92/142 (65%)
• Services migrated: 28/45 (62%)
• Tests passing: 78% (191/245)
• Performance: Within 5% of baseline
• Issues: 12 open (3 critical, 5 medium, 4 low)

Recent Activity:
• Mar 12: Migrated checkout component (critical path)
• Mar 11: Fixed RxJS operator compatibility issue
• Mar 10: Updated authentication service
• Mar 9: Performance regression detected and fixed

Upcoming Tasks:
1. Migrate product catalog component (priority: high)
2. Update shopping cart service (priority: high)
3. Fix remaining TypeScript errors (priority: medium)
4. Update remaining unit tests (priority: medium)

Risks & Issues:
• ⚠️ Critical: Product image component migration delayed
• ⚠️ Medium: CSS theming inconsistencies
• ✅ Resolved: RxJS migration completed successfully
• ✅ Resolved: Build system configuration fixed

Metrics:
• Code Coverage: 78% (target: 85%)
• Performance: 95% of baseline (target: 90%+)
• Test Pass Rate: 92% (target: 95%+)
• Migration Velocity: 12 components/week

Next Milestone: Complete Phase 3 by Mar 19
Overall Progress: 42%
Estimated Completion: Apr 2, 2026
```

## Notes

- **Start with comprehensive analysis** before beginning migration
- **Choose migration strategy based on risk tolerance and complexity**
- **Implement incremental migration for large, complex systems**
- **Maintain parallel run capability for business-critical systems**
- **Extensive testing is crucial for migration success**
- **Document all migration decisions and rationales**
- **Plan for knowledge transfer and team training**
- **Monitor performance closely during and after migration**
- **Have rollback procedures ready for unexpected issues**
- **Celebrate milestones to maintain team morale during long migrations