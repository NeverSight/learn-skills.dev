---
name: best-practice-guide
description: Analyze project documentation to identify missing context, then generate and store best practice guides using web search when available
license: MIT
compatibility: opencode
metadata:
  audience: developers, AI agents, project maintainers
  category: documentation
---

# Best Practice Guide Generator

Analyze project documentation (AGENTS.md, CLAUDE.md, specifications) to identify missing context, critical problems, and knowledge gaps. Use web search when available to find authoritative best practices, then generate and store guides as either documentation links or standalone skills for easy agent discovery.

## When to use me

Use this skill when:
- Starting work on a new project with incomplete documentation
- Notice repeated questions or confusion about specific topics
- Preparing for complex tasks requiring specialized knowledge
- Building comprehensive project onboarding materials
- Identifying areas where agents lack sufficient context
- Creating reusable knowledge assets for future agent sessions
- Validating project practices against industry standards

## What I do

### 1. Documentation Analysis & Gap Detection
- **Scan project files** for key documentation (AGENTS.md, CLAUDE.md, README.md, SPECS.md, etc.)
- **Identify knowledge gaps** by analyzing:
  - Missing or incomplete explanations
  - Undocumented assumptions and conventions
  - Areas requiring specialized domain knowledge
  - Security, performance, or compliance considerations not addressed
  - Tool-specific configurations not documented
- **Map dependencies** between documented and undocumented areas
- **Prioritize gaps** by impact on agent effectiveness and project success

### 2. Research-Driven Best Practice Discovery
- **Use available search tools** (`searxng_searxng_web_search`, `searxng_web_url_read`) when possible
- **Find authoritative sources** for identified gaps:
  - Official documentation and style guides
  - Industry best practice articles and whitepapers
  - Framework/library-specific recommendations
  - Security compliance requirements
  - Performance optimization patterns
- **Cross-reference multiple sources** to validate information
- **Document sources** for traceability and credibility

### 3. Guide Generation & Storage
- **Create comprehensive guides** addressing identified gaps
- **Structure guides for easy consumption** by both agents and humans
- **Generate multiple output formats**:
  - **Documentation links**: Add to AGENTS.md/CLAUDE.md with clear sections
  - **Standalone skills**: Create new skills in the skills directory for agent discovery
  - **Reference files**: Store in `references/` or `guides/` directories
- **Include practical examples** and implementation patterns
- **Add verification steps** to confirm guide effectiveness

### 4. Integration & Maintenance
- **Update project documentation** with guide references
- **Create skill metadata** for easy agent discovery
- **Establish maintenance procedures** for keeping guides current
- **Set up validation checks** to ensure guide accuracy over time
- **Document guide creation process** for future updates

## Output Strategy

### Option 1: Documentation Integration (When guides are project-specific)
- **Add to AGENTS.md**: New sections with clear headings and references
- **Update CLAUDE.md**: Context-specific guidance for Claude Code
- **Create `docs/guides/` directory**: Organized by topic
- **Link from existing documentation**: Cross-references between related topics

### Option 2: Skill Creation (When guides are reusable across projects)
- **Create new skill directory** in `skills/<topic>-guide/`
- **Include SKILL.md** with guide content and usage instructions
- **Add references/README.md** with detailed explanations
- **Create scripts/** for practical implementation
- **Register in skills catalog** for agent discovery

### Option 3: Hybrid Approach
- **Core best practices** as reusable skills
- **Project-specific adaptations** in project documentation
- **Cross-references** between skills and project docs

## Examples

```bash
# Analyze current project documentation for gaps
npm run best-practice:analyze -- --project-dir . --output gaps.json

# Generate guide for identified React performance gaps
npm run best-practice:generate -- --topic "react-performance" --format skill --search true

# Create documentation links for identified security gaps
npm run best-practice:integrate -- --gaps gaps.json --target AGENTS.md --format documentation

# Comprehensive analysis and guide generation
npm run best-practice:full -- --project-dir . --search true --output-formats "skill,documentation"
```

## Output format

### Gap Analysis Report:
```yaml
project: example-project
analysis_date: 2026-02-26
documents_analyzed:
  - AGENTS.md
  - CLAUDE.md
  - README.md
  - package.json
critical_gaps:
  - topic: "database-migration-best-practices"
    impact: "High (data loss risk)"
    evidence: "No documentation on migration procedures"
    sources_needed: ["Official framework docs", "Industry patterns"]
  - topic: "authentication-security-considerations"
    impact: "Critical (security risk)"
    evidence: "Authentication mentioned but no security guidelines"
    sources_needed: ["OWASP guidelines", "Framework security docs"]
  - topic: "performance-monitoring-setup"
    impact: "Medium (operational visibility)"
    evidence: "Monitoring mentioned but no implementation details"
    sources_needed: ["Monitoring tool docs", "SRE practices"]
research_required: 3 topics
search_tools_available: true
```

### Generated Guide (as Skill):
```
skills/database-migration-guide/
├── SKILL.md
├── references/
│   └── README.md (with detailed migration patterns)
└── scripts/
    └── safe-migration.sh
```

### Documentation Integration:
```markdown
## Database Migration Best Practices

[See skills/database-migration-guide/ for comprehensive guidance]

Key principles:
1. Always backup before migration
2. Use transactional migrations where possible
3. Test migrations in staging environment
4. Monitor performance during migration

*Generated by best-practice-guide skill - Last updated: 2026-02-26*
```

## Notes

- **Research is critical**: Always use available search tools to find authoritative sources
- **Balance specificity and reusability**: Create guides that are useful for current project but potentially reusable
- **Document sources**: Always cite sources for credibility and future reference
- **Prioritize by impact**: Focus on high-impact gaps first (security, data integrity, critical functionality)
- **Validate generated content**: Test guides for clarity and usefulness
- **Maintain over time**: Schedule periodic review and updates of generated guides
- **Respect intellectual property**: Properly attribute sources and follow licensing requirements
- **Adapt to project maturity**: Different guidance needed for POC vs production projects
- **Consider agent capabilities**: Create guides that work within agent context limits