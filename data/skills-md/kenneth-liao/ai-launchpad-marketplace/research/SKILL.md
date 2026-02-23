---
name: research
description: Conduct topic and competitor research for any content type. Analyzes existing content landscape, identifies gaps, and produces actionable insights. This is a generalized research skill — platform-specific tools and output locations are provided by orchestrator skills.
---

# Content Research

## Overview

This skill conducts topic and competitor research for any content type. Execute all steps to produce actionable insights that identify content gaps and analyze competitors. This skill focuses ONLY on research — it does not generate titles, hooks, or other creative assets.

**Core Principle**: Focus on insights and big levers, not data dumping. Research should be comprehensive yet concise, backed by data, and designed to inform strategic decisions.

## When to Use

Use this skill when:
- You need to research a topic before creating content
- The user asks to research a content idea or topic
- You want to understand the competitive landscape for a topic
- You need to identify content gaps and opportunities
- Preparing for title generation, hook creation, or full content planning

## Platform-Specific Research Tools

This skill is designed to work across platforms. Orchestrator skills may provide platform-specific tools for research:

| Platform | Tools Provided By Orchestrator | Fallback |
|---|---|---|
| YouTube | YouTube Analytics MCP (search, video details, channel details) | Web search |
| Newsletter/Blog | Content analytics, email platform data | Web search |
| Social Media | Platform analytics, engagement data | Web search |
| General | N/A | Web search (default) |

When no platform-specific tools are available, use web search as a general-purpose research tool to find existing content, competitor analysis, and trending topics.

## Research Subagents

You can invoke research subagents using the `Task` tool to conduct specific, focused research tasks in parallel. Each `Task` prompt should be focused and specific, with a clear objective.

Bias towards using the `Task` tool rather than executing all research sequentially. Parallel research greatly improves performance.

## Research Workflow

Execute all steps below to complete the research.

### Step 0: Initialize Research Document

Create a research document at the location specified by the orchestrator or the user. If no location is specified, ask the user where to save the output.

All research **MUST** be written to this file. If the file already exists, read it to understand what research has been done so far and continue from there.

### Step 1: Understand the Topic

Analyze and document:
- What problem does this content solve?
- Why would someone engage with this content?
- What makes this topic relevant now?
- Who is the target audience?

### Step 2: Research Existing Content

Execute these actions using available tools (platform-specific MCP tools if provided, otherwise web search):

1. Find the user's related existing content on the topic
2. Gather performance metrics where available
3. Identify what has already been covered and how to differentiate

Document in research file:
- Related existing content (title, link, key metrics if available)
- Performance insights (what worked, what did not)
- Differentiation strategy for new content

### Step 3: Competitor Research

Execute these actions:
1. Find 5-8 top-performing pieces of content on the topic
2. Filter for recent content with high engagement
3. Gather details and metrics for each
4. Analyze patterns in successful content

Document for each competitor:
- Title, creator/publication, link
- Key metrics (views, engagement, shares — whatever is available)
- Focus/angle and what makes it successful

Synthesize key insights: Identify common patterns and different approaches across competitors.

### Step 4: Content Gap Analysis

Analyze and identify:
- What subtopics or angles are saturated?
- What is missing or underexplored?
- Where can the user add unique value?

Document in research file:
- **What's Already Well-Covered**: 3-5 saturated topics/approaches
- **Content Gaps (Opportunities)**: Specific opportunities rated by potential
  - Rating: *** (high), ** (medium), * (low)
- **Recommended Focus**: The specific angle and unique value proposition

**Rating Criteria**:
- *** High: Significant gap, strong demand, clear differentiation possible
- ** Medium: Moderate gap, some competition, good potential
- * Low: Minor gap, heavily competed, incremental value

### Step 5: Recommended Angle

Based on the gap analysis, define:
- The specific angle to take
- The unique value proposition
- Why this angle is better than what already exists
- What makes the user uniquely qualified to cover this

## Output Structure

Use this template structure for the research document:

```markdown
# [Topic] - Research

## Content Overview
**Topic**: [Brief description]
**Target Audience**: [Who this is for]
**Content Type**: [YouTube video, newsletter, social post, etc.]
**Goal**: [What the audience will learn/gain]

## Research Notes
### Key Concepts to Cover
[High-level list]

## Existing Content Landscape
### User's Related Content
[Analysis of user's previous content on this topic]

### Top Competing Content
[5-8 pieces with analysis]

### Key Insights
[Patterns and findings across competitors]

## Content Gap Analysis
### What's Already Well-Covered
[List of saturated angles]

### Content Gaps (Opportunities)
[Rated list of specific gaps]

### Recommended Focus
[Specific angle and unique value proposition]

## Production Notes
**Status**: Research Complete
**Created**: [Date]
**Updated**: [Date]
```

## Voice Application

Before finalizing any written output, invoke the `writing:voice` skill to apply voice rules. Research documents should reflect the user's authentic voice, not generic analyst language.

## Brand Compliance

When creating assets for The AI Launchpad, invoke `branding-kit:brand-guidelines` to resolve the correct design system and check anti-patterns.

## Execution Guidelines

### Focus on Insights, Not Data

Execute research with these principles:
- Synthesize patterns from research
- Identify 3-5 key insights with supporting data
- Explain WHY approaches work
- Limit competitor research to 5-8 pieces of content

### Prioritize Big Levers

Focus research on these impact areas in order:
1. Content Gaps (unique value)
2. Competitor Patterns
3. Audience Needs
4. Technical/Format Requirements

### Back Recommendations with Data

When documenting findings:
- Bad: "Write about AI agents"
- Good: "Focus on AI agent memory systems (*** gap) — competitors get high engagement but none cover persistent memory"

## Quality Checklist

Verify completion before finalizing research:
- [ ] Topic clearly understood with audience and goal defined
- [ ] User's existing related content reviewed
- [ ] 5-8 competitors documented with analysis
- [ ] Content gaps identified with star ratings
- [ ] Research is concise yet comprehensive (not data dumping)
- [ ] All recommendations backed by data
- [ ] Unique value proposition clearly stated
- [ ] Voice skill applied to final output

## Common Pitfalls to Avoid

1. **Data Dumping**: Listing every piece of content found without synthesis. Limit to 5-8 top competitors, focus on patterns.
2. **Vague Content Gaps**: "Not much content on this topic." Identify specific angles that are missing.
3. **Over-Researching Technical Details**: Deep implementation research when high-level coverage suffices. Keep focused on what to cover, not how.
4. **Long Reports**: 800+ line documents with low signal. Focus on insights and big levers.
5. **Platform Assumptions**: Assuming YouTube tools are available when they may not be. Check what tools the orchestrator has provided.

## Example Execution

**Scenario**: User requests research for content about "Building AI agents with memory"

Execute workflow:
1. Understand topic: Practical guide to AI agent memory, targeting developers
2. Find related content: Search user's existing content, find related pieces on personal assistants
3. Competitor research: Search and analyze 8 top pieces, identify they cover theory not implementation
4. Gap analysis: Document *** opportunity for practical memory implementation tutorial
5. Save research: Write to user-specified location

**Result**: Comprehensive research document ready for review or to proceed to title/hook generation.

**Next Step**: If the user has asked to plan content, invoke `content-strategy:title` to generate title options based on this research.
