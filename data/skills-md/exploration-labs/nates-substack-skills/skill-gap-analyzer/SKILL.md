---
name: skill-gap-analyzer
description: Analyzes the user's skill library to identify coverage gaps, redundant overlaps, and optimization opportunities. Use when users want to understand their skill ecosystem, optimize their skill collection, find missing capabilities for common workflows, or reduce redundant coverage. Triggered by requests like "analyze my skills," "what skills am I missing," "are any of my skills redundant," or "optimize my skill library."
---

# Skill Gap Analyzer

## Overview

This skill performs systematic analysis of a user's skill library to identify gaps in capability coverage, redundant overlaps between skills, and opportunities for optimization. It compares existing skills against common workflow patterns to surface actionable recommendations for improving the skill ecosystem.

## Analysis Workflow

The skill gap analysis follows these steps:

1. Inventory current skills
2. Map coverage patterns and capabilities
3. Identify gaps against common workflows
4. Detect redundancies and overlaps
5. Generate prioritized recommendations

## Step 1: Inventory Current Skills

Begin by reviewing the complete list of available skills. Examine each skill's name and description to understand:

- Primary purpose and capabilities
- Domains or file types covered
- Workflows supported
- Trigger patterns and use cases

Create a structured inventory that captures:
- Skill name
- Core capabilities (what it does)
- Primary domains (e.g., documents, presentations, data analysis)
- File type associations (e.g., .docx, .pdf, .xlsx)
- Key workflows (e.g., creation, editing, analysis)

## Step 2: Map Coverage Patterns

Analyze the inventory to identify coverage patterns across multiple dimensions:

**By domain:**
- Document processing (word docs, PDFs, presentations)
- Data and analytics (spreadsheets, databases, visualization)
- Development (coding, debugging, testing)
- Creative (design, content creation, media)
- Communication (writing, presentations, reporting)
- Research (information gathering, analysis, synthesis)
- Business (strategy, planning, operations)

**By workflow stage:**
- Creation (new artifacts from scratch)
- Editing/modification (improving existing work)
- Analysis (extracting insights, understanding)
- Conversion (format transformation)
- Automation (scripting, batch processing)
- Quality assurance (validation, review, testing)

**By file type:**
- Office formats (.docx, .xlsx, .pptx)
- PDFs
- Code files (various languages)
- Media (images, video, audio)
- Data formats (CSV, JSON, databases)
- Web (HTML, React artifacts)

## Step 3: Identify Gaps

Compare the coverage map against common workflows to identify gaps. Consider these high-value workflow categories:

**Document workflows:**
- Creating, editing, analyzing text documents
- Working with forms and templates
- PDF manipulation and form-filling
- Presentation creation and design
- Multi-format document conversion

**Data workflows:**
- Spreadsheet creation with formulas and formatting
- Data analysis and visualization
- Database querying and management
- Report generation and dashboards
- Financial modeling

**Development workflows:**
- Code writing and debugging
- Testing and quality assurance
- Documentation generation
- Package and dependency management
- Deployment and DevOps

**Research workflows:**
- Information gathering and synthesis
- Academic paper analysis
- Competitive research
- Market analysis
- Literature reviews

**Business workflows:**
- Strategic planning documents
- Project management artifacts
- Stakeholder communication
- Performance analysis
- Process documentation

**Creative workflows:**
- Visual design and graphics
- Content writing and editing
- Brand asset creation
- Marketing materials
- Media editing

For each gap identified, assess:
- **Impact**: How frequently would this capability be used?
- **Availability**: Could existing skills partially address this with modification?
- **Complexity**: How difficult would it be to create a skill for this gap?
- **Priority**: High (frequently needed), Medium (occasionally useful), Low (rarely needed)

## Step 4: Detect Redundancies

Identify overlapping capabilities across multiple skills that may indicate redundancy:

**Look for:**
- Multiple skills covering the same file types with similar workflows
- Overlapping domain coverage without clear differentiation
- Similar trigger patterns that might cause confusion
- Duplicated functionality that could be consolidated

**Evaluate each overlap:**
- **Complementary**: Different skills handle different aspects well (keep both)
- **Redundant**: Significant overlap with minimal differentiation (consider consolidating)
- **Partially redundant**: Some overlap but each skill has unique value (clarify boundaries or merge strategically)

**Assessment criteria:**
- Do the skills serve distinctly different use cases?
- Is there clear guidance on when to use each skill?
- Would consolidation improve usability or create confusion?
- Is the redundancy justified by specialization or different approaches?

## Step 5: Generate Recommendations

Synthesize findings into actionable recommendations structured in these categories:

### Critical Gaps (High Priority)
Skills that would address frequently-needed workflows currently not covered. Include:
- Specific workflow or use case not currently supported
- Expected frequency of use
- Potential impact on productivity
- Suggested skill name and core capabilities

### Enhancement Opportunities (Medium Priority)
Areas where existing skills could be extended or improved:
- Existing skill that could be enhanced
- Specific capability additions
- Workflows that would be better supported

### Consolidation Candidates (Redundancy Reduction)
Skills with significant overlap that could be merged or clarified:
- Skills involved in redundancy
- Nature of overlap
- Recommendation to consolidate, differentiate, or maintain status quo
- Trade-offs to consider

### Low-Priority Additions
Nice-to-have capabilities for specialized workflows:
- Workflow or use case
- Why it's lower priority (infrequent use, narrow applicability)
- Potential value if implemented

### Configuration Recommendations
Suggestions for optimizing existing skills:
- Description clarifications for better triggering
- Boundary adjustments between overlapping skills
- Documentation improvements
- Cross-references between related skills

## Output Format

Present analysis in a clear, scannable format:

1. **Executive Summary**: 2-3 sentence overview of findings
2. **Coverage Heatmap**: Visual or structured representation of where skills are concentrated vs. sparse
3. **Critical Gaps**: Prioritized list with justification
4. **Redundancy Analysis**: Specific overlaps with recommendations
5. **Action Items**: Concrete next steps prioritized by impact

Keep recommendations specific and actionable. Avoid vague suggestions—each recommendation should enable the user to immediately understand what to build or change and why it matters.

## Usage Notes

**Trigger this skill when users ask about:**
- "What skills am I missing?"
- "Are my skills redundant?"
- "How can I optimize my skill library?"
- "What workflows aren't covered by my skills?"
- "Analyze my skill ecosystem"
- "Should I consolidate any skills?"

**Don't overthink:**
- Perfect coverage isn't the goal—focus on high-impact gaps
- Some redundancy may be intentional and valuable
- User-specific workflows matter more than theoretical completeness

**Context matters:**
- Consider the user's actual work patterns when assessing gaps
- Ask clarifying questions about workflows they frequently perform
- Prioritize based on their stated needs, not generic best practices
