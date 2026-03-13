---
name: skill-hunter
description: Discover, extract, and analyze Claude SKILL.md files from GitHub repositories to understand ecosystem patterns and best practices.
---

# Skill Hunter

## Overview

Skill Hunter is a comprehensive tool for discovering and analyzing Claude skill documentation across GitHub. It automates the process of finding SKILL.md files, extracting their content, analyzing patterns, and generating insights about the skill ecosystem.

**Use this skill when you need to:**
- Find example SKILL.md files from real projects
- Understand ecosystem patterns and best practices
- Analyze skill documentation quality and structure
- Discover well-implemented skills to learn from
- Research how different developers approach skill design

---

## What It Does

Skill Hunter performs five core operations:

### 1. Discovery Phase
Searches GitHub for all SKILL.md files using the GitHub API. Returns metadata about discovered skills including:
- Repository name and owner
- File location within repository
- Direct GitHub links
- Raw content URLs

**Result:** 270+ SKILL.md file instances across 193+ repositories

### 2. Extraction Phase
Retrieves the complete content of selected SKILL.md files directly from GitHub. Handles:
- Base64 decoding of GitHub API responses
- Multiple file naming conventions (SKILL.md, skill.md, Skill.md, etc.)
- Nested directory structures
- Rate limit optimization with authentication

**Result:** 100+ complete, extracted SKILL.md files ready for analysis

### 3. Analysis Phase
Parses and analyzes extracted skills to identify:
- YAML frontmatter structure and metadata
- Section organization and hierarchy
- Code blocks and examples
- Documentation completeness
- Quality metrics and patterns

**Result:** Structured analysis of each skill's composition

### 4. Pattern Recognition
Identifies ecosystem-wide patterns including:
- Naming convention trends
- File size distribution
- Documentation best practices
- Quality standards across official vs. community skills
- Common section structures

**Result:** 10+ key insights about skill design patterns

### 5. Categorization
Organizes discovered skills into meaningful categories:
- **Official Anthropic skills** — Canonical implementations
- **Production community skills** — Battle-tested, well-maintained
- **Experimental community skills** — Emerging patterns
- **Individual ecosystem skills** — Diverse implementations

**Result:** Structured skill directory organized by source and quality

---

## How to Use This Skill

### Scenario 1: Find Example Skills in a Domain

**Request:** "I want to build a skill for code review. Show me well-documented examples."

**Skill Hunter will:**
1. Search the skill ecosystem for code review-related skills
2. Extract the top-quality examples
3. Analyze their structure and patterns
4. Show you how professional skills approach this domain

**Output:** Links to real SKILL.md files you can study

---

### Scenario 2: Understand Skill Documentation Best Practices

**Request:** "What makes a well-documented skill? Show me examples."

**Skill Hunter will:**
1. Identify skills with high documentation quality
2. Show the structure of top-rated skills
3. Explain what patterns they follow
4. Provide excerpts you can learn from

**Output:** Best practice examples with explanations

---

### Scenario 3: Analyze Ecosystem Trends

**Request:** "What's trending in skill design? How are developers evolving their approach?"

**Skill Hunter will:**
1. Analyze recent skills and updates
2. Identify emerging patterns
3. Compare with historical baselines
4. Highlight innovation areas

**Output:** Trend analysis and insights

---

### Scenario 4: Research Specific Skill Types

**Request:** "Show me methodology skills (like TDD, debugging). How do they work?"

**Skill Hunter will:**
1. Filter for methodology vs. tool-based skills
2. Extract those specific types
3. Analyze what makes them effective
4. Provide side-by-side comparisons

**Output:** Filtered analysis by skill category

---

### Scenario 5: Get Started Building Your Own Skill

**Request:** "I want to build a skill. What should I know? Show me the learning path."

**Skill Hunter will:**
1. Recommend official Anthropic examples to study
2. Show production-quality community skills
3. Explain common patterns you'll see
4. Provide a learning progression

**Output:** Structured learning path with real examples

---

## Technical Details

### Required Inputs

- **GitHub Token** (optional but recommended)
  - Increases rate limits from 60/hour to 5,000/hour
  - Set via `GITHUB_TOKEN` environment variable

### Outputs Provided

**Discovery Results:**
- JSON file with all 270+ discovered skills and metadata
- Searchable, filterable, analyzable

**Extracted Skills:**
- 100+ complete SKILL.md files
- Raw markdown content
- Organized by repository

**Analysis Reports:**
- Quality rankings and metrics
- Pattern summaries
- Best practice documentation
- Ecosystem health assessment

### Architecture

```
GitHub Search API
        ↓
Discovery (find all SKILL.md files)
        ↓
GitHub Contents API
        ↓
Extraction (get complete files)
        ↓
Analysis Engine
        ↓
Pattern Recognition
        ↓
Reports & Recommendations
```

### Performance

- **Discovery:** 270+ files in 20 seconds
- **Extraction:** 100 files in 2 minutes
- **Analysis:** Patterns identified in 1 minute
- **Total:** Complete ecosystem analysis in ~5 minutes

---

## Key Insights It Reveals

After running Skill Hunter, you'll understand:

1. **Naming Conventions**
   - 45% use SKILL.md (formal, uppercase)
   - 35% use skill.md (modern, lowercase)
   - 20% use variants (Skill.md, etc.)
   - Recommendation: Lowercase is trending

2. **Documentation Size**
   - Sweet spot: 5-15 KB
   - Completeness matters more than length
   - Average across ecosystem: ~5.5 KB

3. **Quality Distribution**
   - 28% excellent (80+/100)
   - 20% good (60-79/100)
   - 35% need improvement (<40/100)
   - Official Anthropic skills: canonical quality

4. **Structure Patterns**
   - YAML frontmatter is critical (controls auto-triggering)
   - Progressive disclosure works (structure > length)
   - Examples are valued (present in 63% of skills)
   - Most successful skills solve one problem well

5. **Ecosystem Health**
   - Growing (increasing number of new skills)
   - Maturing (standards forming naturally)
   - Diverse (spans many domains and industries)
   - Accessible (you don't need to be perfect to publish)

---

## When NOT to Use This Skill

- **Real-time data needed:** This captures a point-in-time snapshot
- **Private repositories:** Only searches public GitHub
- **Incomplete searches:** GitHub API search limitations may affect results
- **Specific version history:** This skill does not track historical versions

---

## Examples

### Example 1: Find Skills Similar to What You're Building

```
"I'm building a skill for systematic debugging.
Show me how the obra/superpowers debugging skill is structured."

Result:
- Extract of obra/superpowers systematic-debugging SKILL.md
- Analysis of its structure and patterns
- Explanation of why it's well-designed
- Links to the original repository
```

### Example 2: Understand Official Standards

```
"What do official Anthropic skills look like?
Show me examples of excellent skill design."

Result:
- Links to all 16 official Anthropic skills
- Categorization by type (tool, methodology, reference)
- Quality analysis of official implementations
- Common patterns across official skills
```

### Example 3: Analyze Ecosystem Maturity

```
"Is skill building mature enough for production use?
What does the data show?"

Result:
- Statistics on ecosystem size and growth
- Quality distribution analysis
- Comparison of official vs. community standards
- Recommendations for production readiness
```

### Example 4: Get Learning Resources

```
"Help me learn how to build skills.
Where should I start?"

Result:
- Recommended official examples to study
- Community production-quality references
- Learning progression from simple to complex
- Best practices checklist
```

---

## Resources

### Official Anthropic Documentation
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### Reference Implementations
- [Official Skills Repository](https://github.com/anthropics/skills)
- [Production Community Skills (obra/superpowers)](https://github.com/obra/superpowers)
- [Experimental Skills (obra/superpowers-lab)](https://github.com/obra/superpowers-lab)

### Skill Hunter Resources
- [Source Code & Data](https://github.com/jdluther2020/ai-claude-code-talk/tree/main/skills/skill-hunter)
- [Blog Series](https://medium.com/@jdluther2020) — Deep dive into findings

---

## Implementation Details

### Code
- **Main Script:** `discovery_phase_1_v3.py`
- **Language:** Python 3
- **Dependencies:** requests, python-dotenv
- **Setup:** Requires `GITHUB_TOKEN` in `.env` file

### Data Files
- **Search Results:** `GITHUB_SEARCH_RESULTS_V3.json` (270 discovered skills)
- **Extracted Content:** `extracted_skills/` folder (100 complete SKILL.md files)
- **Analysis Results:** `EXTRACTED_SKILLS_SAMPLE_V3.json` (metadata)

### Methodology
- Official APIs over web scraping (more reliable, future-proof)
- Base64 content decoding from GitHub API responses
- Comprehensive error handling and retry logic
- Progress tracking and reporting

---

## Tips for Best Results

1. **Provide context** — Tell me what you're trying to build
2. **Be specific** — Domain, use case, skill type helps narrow results
3. **Start with examples** — "Show me a well-made skill for X"
4. **Then learn patterns** — "What makes this one well-designed?"
5. **Finally, build** — Use patterns to create your own

---

## What Makes This Skill Useful

This skill is valuable because it:

- ✅ **Saves time** — No manual GitHub searching needed
- ✅ **Provides context** — Explains patterns and best practices
- ✅ **Shows examples** — Real code from real projects
- ✅ **Reveals standards** — Official vs. community quality baselines
- ✅ **Enables learning** — See how others solve problems
- ✅ **Guides building** — Understand what works before you build

---

## The Meta Part

This skill is self-referential in the best way. It's a skill about skills. You can use it to:

1. Learn how skills work (by studying SKILL.md files)
2. Understand how others structure skills (by analyzing examples)
3. Get better at building skills (by learning from excellence)
4. Teach others about skills (by providing evidence-based insights)

That's the recursive value: using skill-hunter helps you understand and build better skills, including improving skill-hunter itself.

---

## Feedback & Contributions

Found a pattern we missed? Want to extend the analysis? Suggestions for improvement?

The skill-hunter project is open source. All code, data, and analysis are on GitHub.

---

**Last Updated:** February 26, 2026
**Status:** Production ready
**Ecosystem Coverage:** 270+ discovered skills, 100+ analyzed, 34 verified reference skills
