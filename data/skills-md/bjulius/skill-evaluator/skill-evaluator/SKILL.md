---
name: skill-evaluator
license: MIT
description: Comprehensive evaluation toolkit for analyzing Claude skills across security, quality, utility, and compliance dimensions. This skill should be used when users need to evaluate a skill before installation, review before publishing, or assess overall quality and safety. Performs 5-layer security analysis, validates structure and documentation, checks compliance with skill-creator guidelines, and generates markdown reports with scoring and recommendations.
---

# Skill Evaluator

Comprehensive evaluation toolkit for analyzing Claude skills before installation or publication.

## Purpose

Evaluate Claude skills across four critical dimensions:

1. **Security** - Identify vulnerabilities, injection risks, privilege escalation, and security weaknesses
2. **Quality** - Assess code quality, documentation clarity, structural organization, and functionality
3. **Utility** - Evaluate practical value, usability, scope appropriateness, and effectiveness
4. **Compliance** - Validate adherence to skill-creator guidelines and best practices

Generate detailed markdown reports with scores (0-100), risk assessments, and actionable recommendations.

## When to Use This Skill

Use this skill when:

- **Evaluating skills before installation** - Assess safety and quality of third-party skills
- **Pre-publication review** - Validate skills before distributing to others
- **Security auditing** - Check for vulnerabilities and security risks
- **Quality assessment** - Review code quality and documentation
- **Compliance validation** - Ensure skills follow skill-creator guidelines

## Evaluation Modes

### Mode 1: Full Evaluation (Default)

**Usage:** "Evaluate this skill at [path/to/skill]"

Comprehensive analysis across all four dimensions with detailed scoring and recommendations.

**Output:** Complete markdown report with overall score, security analysis, quality assessment, utility evaluation, compliance validation, and recommendations.

### Mode 2: Security-Focused Quick Check

**Usage:** "Is this skill safe to install?" or "Check the security of [skill-path]"

Deep security analysis with brief checks on other dimensions.

**Output:** Security-focused report emphasizing vulnerabilities, risk level, and installation safety.

### Mode 3: Pre-Publication Review

**Usage:** "Review my skill before I publish it" or "Help me improve [skill-path] for publication"

Full evaluation with detailed, actionable improvement guidance for skill authors.

**Output:** Comprehensive report with prioritized recommendations for improvement.

## How to Use

### Basic Usage

1. **Provide the skill path** (directory or .zip file):
   ```
   "Evaluate the skill at /path/to/my-skill"
   "Is /path/to/skill.zip safe to install?"
   ```

2. **Claude will execute evaluation scripts** to analyze the skill:
   - `scripts/evaluate_skill.py` - Main orchestrator
   - `scripts/security_scanner.py` - 5-layer security analysis
   - `scripts/quality_checker.py` - Quality assessment
   - `scripts/compliance_validator.py` - Compliance validation
   - `scripts/report_generator.py` - Report creation

3. **Receive a markdown report** with scores, findings, and recommendations

### Understanding the Report

#### Overall Score (0-100)

Weighted calculation:
- Security: 35% (highest weight due to critical importance)
- Quality: 25%
- Utility: 20%
- Compliance: 20%

**Score Ranges:**
- **90-100**: EXCELLENT - Highly recommended
- **75-89**: GOOD - Recommended
- **60-74**: FAIR - Use with caution
- **40-59**: POOR - Not recommended
- **0-39**: CRITICAL - Do not install

#### Security Analysis

Uses **5-layer defense-in-depth architecture**:

1. **Layer 1: Input Validation & Sanitization** - Command injection, path traversal, file validation
2. **Layer 2: Execution Environment Control** - Privilege escalation, sandboxing, environment manipulation
3. **Layer 3: Output Sanitization** - XSS prevention, information disclosure, data exposure
4. **Layer 4: Privilege Management** - Credential handling, weak cryptography, authentication
5. **Layer 5: Self-Protection** - DoS patterns, SSRF, resource exhaustion

**Vulnerability Severity:**
- **CRITICAL**: Command injection, arbitrary code execution, privilege escalation
- **HIGH**: Path traversal, insecure deserialization, SSRF
- **MEDIUM**: Information disclosure, weak crypto, XSS
- **LOW**: Minor issues, hardening opportunities

**Security Overrides:**
- Security score < 50 → ❌ DO NOT INSTALL (automatic)
- Any CRITICAL vulnerability → ❌ DO NOT INSTALL (automatic)

#### Quality Assessment

Four quality dimensions (25 points each):

1. **Code Quality** - Readability, error handling, modularity, dependencies, best practices
2. **Documentation** - Purpose clarity, usage instructions, resource references, writing quality, completeness
3. **Structure & Organization** - Directory structure, file naming, YAML frontmatter
4. **Functionality** - Practical value, appropriate tool usage, reusability, completeness

#### Utility Evaluation

Assesses practical value (100 points):
- **Problem-solving value** (25 pts) - Addresses real needs
- **Usability** (25 pts) - Clear and easy to use
- **Scope** (25 pts) - Appropriate complexity and boundaries
- **Effectiveness** (25 pts) - Works as described

#### Compliance Validation

Validates against skill-creator guidelines (100 points):
- SKILL.md structure (10 pts)
- YAML frontmatter (20 pts)
- Progressive disclosure (15 pts)
- Scripts/references/assets usage (30 pts total)
- Writing style (10 pts)
- Trigger description (10 pts)

**Critical Violations (Auto-Fail):**
- Missing SKILL.md
- Missing required YAML fields
- Invalid YAML syntax

## Bundled Resources

### Scripts (`scripts/`)

Execute these for evaluation:

- **`evaluate_skill.py`** - Main orchestrator coordinating all analyses
- **`security_scanner.py`** - 5-layer security architecture with pattern detection
- **`quality_checker.py`** - Code quality, documentation, and structure assessment
- **`compliance_validator.py`** - Guideline adherence and compliance checking
- **`report_generator.py`** - Markdown report generation from results

### References (`references/`)

Load these for detailed evaluation criteria:

- **`security_patterns.md`** - Vulnerability pattern database with detection criteria and secure examples
- **`quality_criteria.md`** - Quality assessment rubrics and scoring guidelines
- **`compliance_checklist.md`** - skill-creator guideline requirements
- **`evaluation_methodology.md`** - Evaluation process, scoring formulas, and report structure

### Assets (`assets/`)

- **`report_template.md`** - Markdown report template with structured sections

## Evaluation Workflow

### Step 1: Skill Discovery

Accept skill input (directory or .zip), extract if needed, identify SKILL.md and bundled resources.

### Step 2: Run Analyses

Execute evaluations: Security Scanner → Quality Checker → Compliance Validator → Utility Evaluator

### Step 3: Calculate Scores

Apply weighted formula and override rules:
```
Overall = (Security × 0.35) + (Quality × 0.25) + (Utility × 0.20) + (Compliance × 0.20)
```

### Step 4: Generate Report

Create markdown report using template with executive summary, detailed analyses, and recommendations.

### Step 5: Save Report

Write report to `{skill_name}_evaluation_report.md` and present to user.

## Installation Recommendations

- **✅ HIGHLY RECOMMENDED** (90-100) - Excellent quality, safe to install
- **✅ RECOMMENDED** (75-89) - Good quality, safe to install
- **⚠️ USE WITH CAUTION** (60-74) - Review findings before installing
- **⚠️ NOT RECOMMENDED** (40-59) - Major improvements needed
- **❌ DO NOT INSTALL** (0-39 or security override) - Critical issues, unsafe

## Limitations

### Can Assess
- ✅ Static code analysis
- ✅ Pattern-based vulnerability detection
- ✅ Structure and compliance
- ✅ Documentation quality

### Cannot Assess
- ❌ Runtime behavior
- ❌ Performance at scale
- ❌ Novel attack vectors
- ❌ Subjective satisfaction

## ⚠️ Important Disclaimers

**READ CAREFULLY BEFORE USING THIS SKILL**

### No Guarantee of Safety

**This evaluation CANNOT determine with certainty that a skill is safe.** Like all security analysis tools:

- **Cannot prove absence of vulnerabilities** - Only detect known patterns; novel or obfuscated attacks may go undetected
- **Static analysis limitations** - Cannot assess runtime behavior, dynamic code execution, or context-dependent risks
- **False negatives possible** - Sophisticated malicious code may evade pattern-based detection
- **Time-bound assessment** - New vulnerabilities may be discovered after evaluation

### Use as ONE Input Only

**This evaluation should be used as ONE input into your security decision, not the sole determining factor.**

You are responsible for:

1. **Manual code review** - Read and understand the skill's code yourself
2. **Test in isolated environment** - Run skills in sandboxed/test environments first
3. **Organizational policies** - Always follow your organization's security policies and approval processes
4. **Risk assessment** - Consider your specific threat model and risk tolerance
5. **Ongoing monitoring** - Continue to monitor skill behavior after installation

### Your Responsibility

- **YOU are responsible for skills you install** - Not the evaluator, not the skill author
- **Follow organizational policies** - Security policies override any evaluation recommendation
- **Trust but verify** - Even "HIGHLY RECOMMENDED" skills should be reviewed
- **When in doubt, don't install** - If unsure about a skill's safety, consult security experts

### Limitations of Automated Analysis

This tool performs **pattern-based static analysis**, which means:

- ✅ Good at: Detecting common vulnerability patterns, structural issues, compliance violations
- ❌ Cannot detect: Zero-day exploits, logic bombs, social engineering, supply chain attacks
- ❌ Cannot assess: Author trustworthiness, long-term maintenance, backdoor triggers
- ❌ Cannot guarantee: Complete security, absence of malicious intent, future safety

### Legal Disclaimer

**NO WARRANTIES**: This evaluation tool is provided "as-is" without warranties of any kind. The authors and contributors assume no liability for damages resulting from use of this tool or skills evaluated by it.

**USE AT YOUR OWN RISK**: You accept all risks associated with installing and using evaluated skills.

## Examples

### Example 1: Security Check

**User:** "Is /downloads/data-analyzer.zip safe?"

**Output:** Security report with vulnerabilities, risk level, and installation recommendation.

### Example 2: Pre-Publication

**User:** "Review my skill: /my-projects/excel-parser/"

**Output:** Full evaluation with priority improvements and publication readiness assessment.

### Example 3: Full Evaluation

**User:** "Evaluate /skills/api-connector/"

**Output:** Complete report with all dimensions, scores, and recommendations.

## Best Practices for Skill Authors

### Security
- Never use subprocess with shell=True
- Validate and sanitize inputs
- Use Path.resolve() for paths
- Avoid hardcoded credentials
- Implement error handling

### Quality
- Write clean, readable code
- Add type hints and docstrings
- Remove TODO placeholders
- Provide comprehensive documentation

### Compliance
- Use imperative/infinitive form
- Write clear, specific descriptions
- Follow progressive disclosure
- Organize files correctly
- Use lowercase-with-hyphens naming

### Utility
- Solve real problems
- Provide clear instructions
- Include practical examples
- Ensure appropriate scope
