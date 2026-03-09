---
name: silent-degradation-audit
description: |
  Production-ready skill for detecting silent degradation across codebases.
  Uses multi-wave audit system with 6 specialized category agents, multi-agent
  validation panel, and convergence detection.
---

# Silent Degradation Audit Skill

## Overview

Production-ready skill for detecting silent degradation across codebases. Uses multi-wave audit system with 6 specialized category agents, multi-agent validation panel, and convergence detection. Battle-tested on CyberGym codebase (~250 bugs found).

## When to Use This Skill

**Use this skill when:**

- Code has reliability issues but unclear where
- Systems fail silently without operator visibility
- Error handling exists but effectiveness unknown
- Need comprehensive audit across multiple failure modes
- Preparing for production deployment
- Post-mortem analysis after silent failures

**Don't use for:**

- Code style or formatting issues (use linters)
- Performance optimization (use profilers)
- Security vulnerabilities (use security scanners)
- Simple one-off code reviews (use /analyze)

## Key Features

### Multi-Wave Progressive Audit

- **Wave 1**: Broad scan, finds obvious issues (40-50% of total)
- **Wave 2-3**: Deeper analysis, finds hidden issues (30-40%)
- **Wave 4-6**: Edge cases and subtleties (10-20%)
- **Convergence**: Stops when < 10 new findings or < 5% of Wave 1

### 6 Category Agents

1. **Dependency Failures** (Category A): "What happens when X is down?"
2. **Config Errors** (Category B): "What happens when config is wrong?"
3. **Background Work** (Category C): "What happens when background work fails?"
4. **Test Effectiveness** (Category D): "Do tests actually detect failures?"
5. **Operator Visibility** (Category E): "Is the error visible to operators?"
6. **Functional Stubs** (Category F): "Does this code actually do what its name says?"

### Multi-Agent Validation Panel

- 3 agents review findings: Security, Architect, Builder
- 2/3 consensus required to validate finding
- Prevents false positives and unnecessary changes
- Tracks strong vs weak consensus

### Language-Agnostic

Supports 9 languages with language-specific patterns:

- Python, JavaScript, TypeScript
- Rust, Go, Java, C#
- Ruby, PHP

## Integration Modes

### Standalone Invocation

Direct skill invocation for focused audit:

```
/silent-degradation-audit path/to/codebase
```

### Sub-Loop in Quality Audit Workflow

Integrated as Phase 2 of quality-audit-workflow:

```
quality-audit-workflow calls silent-degradation-audit
→ Returns findings to quality workflow
→ Quality workflow applies fixes
→ Continues to next phase
```

## Usage

### Basic Usage

```bash
# Audit entire codebase
/silent-degradation-audit .

# Audit specific directory
/silent-degradation-audit ./src

# With custom exclusions
/silent-degradation-audit . --exclusions .my-exclusions.json
```

### Configuration

Create `.silent-degradation-config.json` in codebase root:

```json
{
  "convergence": {
    "absolute_threshold": 10,
    "relative_threshold": 0.05
  },
  "max_waves": 6,
  "exclusions": {
    "patterns": ["*.test.js", "test_*.py", "**/__tests__/**"]
  },
  "categories": {
    "enabled": [
      "dependency-failures",
      "config-errors",
      "background-work",
      "test-effectiveness",
      "operator-visibility",
      "functional-stubs"
    ]
  }
}
```

### Exclusion Lists

#### Global Exclusions

Edit `~/.amplihack/.claude/skills/silent-degradation-audit/exclusions-global.json`:

```json
[
  {
    "pattern": "*.test.*",
    "reason": "Test files excluded from production audits",
    "category": "*"
  },
  {
    "pattern": "**/vendor/**",
    "reason": "Third-party code",
    "category": "*"
  }
]
```

#### Repository-Specific Exclusions

Create `.silent-degradation-exclusions.json` in repository root:

```json
[
  {
    "pattern": "src/legacy/*.py",
    "reason": "Legacy code being replaced",
    "category": "*",
    "wave": 1
  },
  {
    "pattern": "api/endpoints.py:42",
    "reason": "Empty dict is valid API response",
    "category": "functional-stubs",
    "type": "exact"
  }
]
```

## Output

### Report Format

Generates `.silent-degradation-report.md`:

```markdown
# Silent Degradation Audit Report

## Summary

- **Total Waves**: 4
- **Total Findings**: 137
- **Converged**: Yes
- **Convergence Ratio**: 4.2%

## Convergence Progress

Wave 1: ██████████████████████████████████████████████████ 120
Wave 2: ███████████████████████████ 65 (54.2% of Wave 1)
Wave 3: ████████ 18 (15.0% of Wave 1)
Wave 4: ██ 5 (4.2% of Wave 1)

Status: ✓ CONVERGED
Reason: Relative threshold met: 4.2% < 5.0%

## Findings by Category

### dependency-failures (42 findings)

- High: 15
- Medium: 20
- Low: 7

[... continues for all 6 categories ...]
```

### Findings Format

Generates `.silent-degradation-findings.json`:

```json
[
  {
    "id": "dep-001",
    "category": "dependency-failures",
    "severity": "high",
    "file": "src/payments.py",
    "line": 89,
    "description": "Payment API failure silently falls back to mock",
    "impact": "Production system using mock payments, no real charges",
    "visibility": "None - no logs or metrics",
    "recommendation": "Add explicit failure logging and metric, or fail fast",
    "wave": 1,
    "validation": {
      "result": "VALIDATED",
      "consensus": "strong",
      "votes": {
        "security": "APPROVE",
        "architect": "APPROVE",
        "builder": "APPROVE"
      }
    }
  },
  ...
]
```

## Workflow Details

### Phase 1: Initialization

1. Create convergence tracker with thresholds
2. Initialize exclusion manager
3. Set up audit state

### Phase 2: Language Detection

1. Scan codebase for file extensions
2. Identify languages (> 5 files or > 5% threshold)
3. Load language-specific patterns

### Phase 3: Load Exclusions

1. Load global exclusions from skill directory
2. Load repository-specific exclusions
3. Merge into single exclusion list

### Phase 4: Wave Loop

For each wave (until convergence):

1. **Category Analysis** (6 agents in parallel)
   - Each agent scans for category-specific issues
   - Uses language-specific patterns
   - Excludes previous findings

2. **Validation Panel** (3 agents in parallel)
   - Security agent reviews security implications
   - Architect agent reviews design impact
   - Builder agent reviews implementation feasibility

3. **Vote Tallying**
   - Require 2/3 consensus (APPROVE)
   - Track strong vs weak consensus
   - Flag inconclusive for human review

4. **Exclusion Filtering**
   - Apply global and repo-specific exclusions
   - Filter out duplicates

5. **State Update**
   - Add new findings to total
   - Record wave metrics

6. **Convergence Check**
   - Absolute: < 10 new findings
   - Relative: < 5% of Wave 1 findings
   - Break if converged

### Phase 5: Report Generation

1. Generate convergence plot
2. Calculate metrics summary
3. Categorize findings by type and severity
4. Write markdown report
5. Write JSON findings

## Architecture

### Directory Structure

```
.claude/skills/silent-degradation-audit/
├── SKILL.md                    # This file
├── reference.md                # Detailed patterns and examples
├── examples.md                 # Usage examples
├── patterns.md                 # Language-specific patterns
├── README.md                   # Quick start
├── category_agents/            # 6 category agent definitions
│   ├── dependency-failures.md
│   ├── config-errors.md
│   ├── background-work.md
│   ├── test-effectiveness.md
│   ├── operator-visibility.md
│   └── functional-stubs.md
├── validation_panel/           # Validation panel specs
│   ├── panel-spec.md
│   └── voting-rules.md
├── recipe/                     # Recipe-based workflow
│   └── audit-workflow.yaml
└── tools/                      # Python utilities
    ├── exclusion_manager.py
    ├── language_detector.py
    ├── convergence_tracker.py
    └── __init__.py
```

### Component Responsibilities

**Category Agents**:

- Scan codebase for category-specific issues
- Use language-specific patterns
- Produce findings with severity, impact, recommendation

**Validation Panel**:

- Review findings from multiple perspectives
- Vote APPROVE/REJECT/ABSTAIN
- Require 2/3 consensus

**Convergence Tracker**:

- Track findings per wave
- Calculate convergence metrics
- Determine when to stop

**Exclusion Manager**:

- Load and merge exclusion lists
- Filter findings against patterns
- Add new exclusions

**Language Detector**:

- Identify languages in codebase
- Load language-specific patterns
- Support 9 languages

## Best Practices

### Running First Audit

1. **Start with small scope**: Audit single service/module first
2. **Review Wave 1 carefully**: Establishes baseline
3. **Tune exclusions**: Add false positives to exclusion list
4. **Verify fixes**: Test fixes before applying broadly

### Exclusion Management

**When to add exclusions:**

- False positives (finding not actually an issue)
- Intentional design (behavior is correct as-is)
- Legacy code (not worth fixing right now)
- Third-party code (can't modify)

**When NOT to add exclusions:**

- Real issues you don't want to fix
- Issues without time to fix now
- Issues that seem hard

Better approach: Fix real issues, prioritize by severity.

### Validation Tuning

**If too many false positives:**

- Review validation panel prompts
- Increase consensus threshold (require unanimous)
- Add category-specific validation rules

**If missing real issues:**

- Review category agent patterns
- Add language-specific patterns
- Decrease consensus threshold (1/3 approval)

### Wave Management

**Typical wave characteristics:**

- Wave 1: 40-50% of findings (obvious issues)
- Wave 2: 25-30% (deeper issues)
- Wave 3: 15-20% (subtle issues)
- Wave 4+: < 10% each (edge cases)

**If waves not converging:**

- Check for duplicate findings (exclusion not working)
- Review category agent overlap (agents finding same things)
- Consider lowering convergence threshold

## Metrics and Monitoring

### Success Metrics

Track these over time:

```
Audit Success:
- Convergence reached: Yes/No
- Waves to convergence: 4 (target: 3-5)
- Total findings: 137 (varies by codebase)
- Validation rate: 75% (target: 60-80%)

Finding Distribution:
- High severity: 15% (target: < 20%)
- Medium severity: 45% (target: 40-60%)
- Low severity: 40% (target: 30-50%)

Panel Effectiveness:
- Strong consensus: 60% (target: > 50%)
- Weak consensus: 30% (target: 20-40%)
- Inconclusive: 10% (target: < 10%)
- Abstention rate: 5% (target: < 10%)
```

### Quality Indicators

**Healthy audit:**

- Converges in 3-5 waves
- Validation rate 60-80%
- Strong consensus > 50%
- Abstention rate < 10%

**Warning signs:**

- Doesn't converge after 6 waves (agents finding same things)
- Validation rate > 95% (rubber stamping)
- Validation rate < 40% (too strict)
- Inconclusive rate > 20% (poor context)

## Troubleshooting

### "Audit not converging"

**Symptoms**: Reaches max waves without convergence

**Causes**:

- Category agents finding duplicate issues
- Exclusion filtering not working
- Convergence threshold too tight

**Solutions**:

1. Review findings for duplicates
2. Check exclusion patterns are matching
3. Increase relative threshold to 10%
4. Reduce max waves to 5

### "Too many false positives"

**Symptoms**: Validation rate > 95%, many non-issues

**Causes**:

- Category agents too aggressive
- Validation panel too permissive
- Patterns not tuned for codebase

**Solutions**:

1. Review category agent patterns
2. Add exclusions for false positive patterns
3. Require unanimous validation (3/3)
4. Tune language-specific patterns

### "Missing real issues"

**Symptoms**: Known issues not in findings

**Causes**:

- Category agent gaps
- Exclusion too broad
- Validation panel too strict

**Solutions**:

1. Check if issue matches any category
2. Review exclusion list for overly broad patterns
3. Lower consensus threshold to 1/3
4. Add specific patterns for missed issues

### "Validation panel abstaining"

**Symptoms**: High abstention rate (> 20%)

**Causes**:

- Insufficient context in findings
- Agent prompts unclear
- Findings outside agent expertise

**Solutions**:

1. Include more code context in findings
2. Review and improve agent prompts
3. Add fourth "generalist" agent
4. Improve finding descriptions

## Advanced Configuration

### Custom Category Agents

Create custom category agent in `category_agents/custom.md`:

```markdown
# Category Custom: My Special Cases

## Core Question

"What happens when [specific scenario]?"

## Detection Focus

[Patterns to detect...]

## Language-Specific Patterns

[Language examples...]
```

Then enable in config:

```json
{
  "categories": {
    "enabled": [
      "dependency-failures",
      "config-errors",
      "background-work",
      "test-effectiveness",
      "operator-visibility",
      "functional-stubs",
      "custom"
    ]
  }
}
```

### Custom Validation Panel

Override validation panel with different agents:

```yaml
# In recipe/audit-workflow.yaml
validation_panel:
  agents:
    - security
    - architect
    - builder
    - domain-expert # Add domain-specific agent

  consensus:
    required: 0.75 # Require 3/4 approval
```

### Staged Rollout

Audit codebase incrementally:

```bash
# Phase 1: Critical services only
/silent-degradation-audit ./services/payments ./services/auth

# Phase 2: All services
/silent-degradation-audit ./services

# Phase 3: Full codebase
/silent-degradation-audit .
```

## See Also

- `reference.md` - Detailed technical reference
- `examples.md` - Real-world usage examples
- `patterns.md` - Language-specific degradation patterns
- `README.md` - Quick start guide
- `category_agents/` - Individual category agent documentation
- `validation_panel/` - Validation panel specifications

## Changelog

### Version 1.0.0 (2025-02-24)

- Initial release
- 6 category agents (A-F)
- Multi-agent validation panel (2/3 consensus)
- Convergence detection (dual thresholds)
- Language-agnostic (9 languages)
- Battle-tested on CyberGym (~250 bugs)
- Integration modes: standalone + sub-loop
