---
name: dogfooding
description: Use when you need to test and validate the skills repository using the skills system itself, practicing "eating your own dog food"
license: MIT
compatibility: opencode
metadata:
  audience: skill-maintainers, quality-assurance
  category: quality
---

# Dogfooding

Test and validate the skills repository using the skills system itself, practicing "eating your own dog food". This skill orchestrates other skills to validate that all skills work correctly, follow specifications, and provide value.

## When to use me

Use this skill when:
- You want to validate that the skills repository actually works with the skills CLI
- You need to ensure all 60 skills follow Agent Skills specification
- You want to run automated validation of skill quality
- You need to demonstrate the power of the skills system by using it to test itself
- You're preparing for a release and need comprehensive validation
- You want to establish continuous dogfooding practices for the repository

## What I do

- **Skill validation**: Test skills using the skills CLI (`npx skills add . --skill <name>`)
- **Structure verification**: Validate skill structure against Agent Skills specification
- **Script execution**: Run skill scripts to ensure they work correctly
- **Dependency checking**: Check skill dependencies and compatibility
- **Cross-referencing**: Use existing skills to validate other skills (skill-builder validates structure, testing-ecosystem validates testing approach)
- **Report generation**: Generate dogfooding reports showing which skills pass/fail self-testing
- **Continuous validation**: Establish patterns for ongoing dogfooding practice

## Related Skills for Comprehensive Dogfooding

This skill **references and builds upon** these existing skills rather than duplicating functionality:

### Skill Creation & Validation
- **`skill-builder`**: Build basic to intermediate Agent Skills using structured templates
- **`hypercognitive-skill-compiler`**: Transform complex skill requirements into complete Agent Skills
- **`best-practice-guide`**: Create best practice guides for skill development

### Testing & Quality
- **`testing-ecosystem`**: Understand complete testing ecosystem and relationships
- **`test-coverage`**: Measure and report test coverage across all test types
- **`test-gap-analysis`**: Analyze gaps between requirements/features that should be tested and actual test coverage
- **`trust-but-verify`**: Verify system claims and test results through independent validation
- **`gap-analysis`**: Identify discrepancies between documentation and implementation
- **`spec-gap-analysis`**: Analyze gaps between specifications and actual implementation

### Workflow Automation
- **`workflow-orchestrator`**: Build AI-driven development workflows that iterate until success
- **`index`**: Maintain directory organization with index files and consistency prompts

### Adversarial Thinking
- **`adversarial-thinking`**: Apply systematic adversarial thinking patterns
- **`devils-advocate`**: Challenge ideas, assumptions, and decisions
- **`assumption-buster`**: Aggressively challenge and attempt to disprove assumptions
- **`reality-validation`**: Compare system behavior against real-world expectations

## Dogfooding Methodology

### Phase 1: Skill Installation Validation
1. **Install each skill** using the skills CLI
2. **Verify discovery** by OpenCode and other agents
3. **Check dependencies** and compatibility requirements
4. **Validate frontmatter** (name, description, compatibility fields)

### Phase 2: Skill Functionality Testing
1. **Run skill scripts** to ensure they execute without errors
2. **Test example commands** provided in SKILL.md
3. **Validate output formats** match documented examples
4. **Check error handling** for edge cases and invalid inputs

### Phase 3: Cross-Skill Validation
1. **Use skill-builder** to validate skill structure
2. **Apply testing-ecosystem** to evaluate testing completeness
3. **Run trust-but-verify** on skill claims and outputs
4. **Use gap-analysis** to identify documentation-implementation gaps

### Phase 4: Ecosystem Integration Testing
1. **Test skill dependencies** and relationships
2. **Validate cross-skill references** (this skill references others)
3. **Check repository structure** using index skill
4. **Validate workflow patterns** using workflow-orchestrator

## Examples

```bash
# Run comprehensive dogfooding validation
./scripts/validate-dogfooding.sh --scope all --output dogfooding-report.json

# Validate specific skill categories
./scripts/validate-dogfooding.sh --category core --output core-validation.json

# Test skill installation and discovery
./scripts/test-skill-installation.sh --skill git-release --verbose

# Generate dogfooding report using cross-skill references
./scripts/generate-dogfooding-report.sh --reference skill-builder --reference testing-ecosystem

# Continuous dogfooding setup
./scripts/setup-continuous-dogfooding.sh --cron "0 */6 * * *"
```

## Output format

```
Dogfooding Validation Report
─────────────────────────────────────
Validation Date: 2025-01-15T10:30:00Z
Repository: skills
Total Skills: 60
Validation Duration: 12 minutes 45 seconds

SKILL INSTALLATION VALIDATION:
──────────────────────────────
✅ Passed: 58 skills (96.7%)
❌ Failed: 2 skills (3.3%)

Installation Failures:
• skill-builder: Dependency conflict with hypercognitive-skill-compiler
• testing-chaos: Missing dependency 'chaos-mesh' not documented

SKILL FUNCTIONALITY TESTING:
────────────────────────────
✅ Script Execution: 55 skills (91.7%)
✅ Example Commands: 52 skills (86.7%)
✅ Output Format: 57 skills (95.0%)
✅ Error Handling: 48 skills (80.0%)

Functionality Issues:
• 5 skills have non-executable scripts (chmod +x needed)
• 8 skills have example commands that don't match actual behavior
• 3 skills produce unexpected output formats
• 12 skills lack proper error handling for invalid inputs

CROSS-SKILL VALALIDATION RESULTS:
─────────────────────────────────
Using skill-builder to validate structure:
• 58 skills pass structure validation
• 2 skills fail: missing required frontmatter fields

Using testing-ecosystem to evaluate testing:
• Core skills: 9/9 have adequate testing documentation
• Testing ecosystem skills: 27/27 self-referential (expected)
• Development tools: 2/2 need more example test cases
• Performance optimization: 1/1 well-tested
• Security & compliance: 1/1 comprehensive
• Documentation: 1/1 excellent examples
• Cloud management: 1/1 realistic scenarios
• Data management: 1/1 thorough validation
• Database optimization: 1/1 detailed examples
• Operations: 2/2 practical workflows

Using trust-but-verify on skill claims:
• Verified: 42 skills have claims that match implementation
• Questionable: 12 skills have exaggerated capabilities
• Unverified: 6 skills make claims that can't be tested automatically

Using gap-analysis on documentation:
• Complete: 38 skills have documentation matching implementation
• Partial gaps: 18 skills have minor documentation discrepancies
• Significant gaps: 4 skills have major documentation-implementation mismatches

ECOSYSTEM INTEGRATION TESTING:
──────────────────────────────
Skill Dependencies:
• Circular dependencies detected: skill-builder ↔ hypercognitive-skill-compiler
• Missing dependencies: 3 skills reference non-existent skills
• Version conflicts: 2 skills have incompatible dependency versions

Cross-Skill References:
• This skill (dogfooding) references 15 other skills ✓
• skill-builder references hypercognitive-skill-compiler ✓
• testing-ecosystem references all testing skills ✓
• workflow-orchestrator references no specific skills (general)

Repository Structure:
• All skills follow kebab-case naming ✓
• Directory structure consistent across skills ✓
• Symlinks properly maintained in .opencode/skills/ ✓
• README.md and AGENTS.md up to date ✓

DOGFOODING QUALITY METRICS:
───────────────────────────
Overall Dogfooding Score: 84/100
• Installation: 97/100 (96.7% success)
• Functionality: 88/100 (average across 4 categories)
• Cross-validation: 79/100 (skill interdependence quality)
• Ecosystem: 91/100 (integration and structure)

Critical Issues Found:
1. Circular dependency between skill builders
2. Missing error handling in 12 skills
3. Exaggerated claims in 12 skills
4. Documentation gaps in 22 skills

RECOMMENDATIONS:
────────────────
1. HIGH PRIORITY:
   • Fix circular dependency: skill-builder vs hypercognitive-skill-compiler
   • Add error handling to 12 skills missing it
   • Verify claims in 12 skills with exaggerated capabilities

2. MEDIUM PRIORITY:
   • Update documentation for 22 skills with gaps
   • Add missing dependencies for 3 skills
   • Fix example commands in 8 skills
   • Make scripts executable for 5 skills

3. LOW PRIORITY:
   • Improve output format consistency for 3 skills
   • Add more test cases for development tools (2 skills)
   • Enhance cross-skill referencing across ecosystem

DOGFOODING PATTERNS ESTABLISHED:
─────────────────────────────────
✅ Self-validation: This skill validates itself through recursive dogfooding
✅ Cross-referencing: Uses 15 existing skills to validate others
✅ Continuous practice: Setup scripts for ongoing validation
✅ Documentation: This report generated by dogfooding process

CONTINUOUS DOGFOODING SETUP:
─────────────────────────────
• Cron job: Every 6 hours
• Notification: Slack/webhook on validation failures
• Reporting: Weekly dogfooding quality metrics
• Escalation: Critical issues → immediate maintainer notification

NEXT VALIDATION SCHEDULED: 2025-01-15T16:30:00Z
```

## Notes

- Dogfooding is most valuable when done continuously, not just before releases
- This skill intentionally references other skills to demonstrate cross-skill integration
- The validation process should itself be validated (dogfooding the dogfooding)
- Focus on practical validation that skills actually work, not just structural compliance
- Use adversarial thinking skills to challenge dogfooding assumptions
- Document dogfooding findings to improve skill quality over time
- Balance automation with manual spot-checking for comprehensive validation
- Share dogfooding results to build trust in the skills ecosystem
- Update dogfooding methodology as new skills are added to the repository