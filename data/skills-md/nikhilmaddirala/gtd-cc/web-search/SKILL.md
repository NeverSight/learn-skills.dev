---
name: web-search
description: General web search patterns and techniques including Gemini CLI coordination. Use this skill when you need to perform web searches, find current information, or research topics online. Covers both Gemini CLI and built-in WebSearch tool usage with precise instruction crafting.
version: 0.1.0
last_updated: 2025-01-26
---

# Web Search Techniques & Coordination

## Overview

This skill provides patterns for web searching using Gemini CLI coordination or Claude's built-in WebSearch tool. It enables finding current information beyond knowledge cutoffs through precise instruction crafting.


## Context

User needs to find current information, verify facts, or research topics online. This skill is appropriate when:
- Searching for recent developments or current events
- Verifying claims or checking facts
- Researching technical topics with up-to-date information
- Finding domain-specific information from particular websites


## Process

1. Analyze user's web search requirements
2. Craft precise instructions for Gemini CLI or WebSearch tool
3. Execute the search with appropriate constraints
4. Process and validate the returned results
5. Present information with proper source attribution
6. Verification: Confirm sources are current and reliable


## Agent Coordination Model

This skill operates on a two-agent model:

**Your Role (Calling Agent):**
- Analyzes user's web search requirements
- Crafts precise instructions for Gemini CLI
- Executes `gemini -p` commands with properly formatted prompts
- Processes and presents Gemini CLI's responses to users

**Gemini CLI (Web Research Agent):**
- A general-purpose agent restricted to web research operations only
- Accesses current information beyond knowledge cutoffs when asked to do web search
- Formats responses with source citations when requested
- Returns structured results based on received instructions
- Does NOT edit files, write code, execute commands, or perform any non-research actions

## Core Principle
You do NOT perform web searches directly. Instead, you act as an intelligent prompt coordinator that crafts optimal instructions for Gemini CLI to execute web searches effectively.

## Scope Limitations
Gemini CLI has the following tools:
  - Codebase Investigator Agent
    (codebase_investigator)
  - Edit (replace)
  - FindFiles (glob)
  - GoogleSearch (google_web_search)
  - ReadFile (read_file)
  - ReadFolder (list_directory)
  - SaveMemory (save_memory)
  - SearchText (search_file_content)
  - Shell (run_shell_command)
  - WebFetch (web_fetch)
  - WriteFile (write_file)
  - WriteTodos (write_todos)

But in this skill, we want to restrict Gemini CLI to web research operations ONLY. When crafting instructions, always include this constraint:

```
IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

This ensures Gemini CLI operates purely as a web research tool without attempting general-purpose coding or file manipulation tasks.


## Crafting Instructions for Gemini CLI

### Basic Web Search Instructions

When users need simple web searches, craft these prompts for Gemini CLI:

**Template for current information:**
```
Do a web search to find the latest information about [TOPIC]. Focus on recent developments, current status, and up-to-date data. Include sources with publication dates and provide comprehensive coverage of recent changes.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

**Template for fact-checking:**
```
Search the web to verify the accuracy of [CLAIM]. Look for authoritative sources, fact-checking websites, and recent coverage. Provide evidence for or against the claim with proper source attribution.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

**Template for recent developments:**
```
Conduct web research to answer: [QUESTION]. Focus on information from the past 6-12 months, recent news, and current developments. Prioritize recent sources and provide timeline context.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

### Domain-Specific Search Instructions

**Site-specific research:**
```
Do web search on site:github.com for [QUERY]. Look for repositories, documentation, discussions, and issues related to [TOPIC]. Include repository stats, recent activity, and community feedback.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

**Multiple domain restriction:**
```
Search the web on site:stackoverflow.com OR site:docs.microsoft.com OR site:medium.com for [TECHNICAL QUESTION]. Focus on recent solutions, best practices, and current documentation.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

**News and industry sources:**
```
Conduct web research on site:techcrunch.com OR site:theverge.com OR site:arstechnica.com about [TOPIC]. Focus on recent coverage, industry analysis, and expert opinions from the past year.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

### Advanced Research Instructions

**Competitive analysis:**
```
Do comprehensive web research to compare [PRODUCT A] vs [PRODUCT B]. Include recent reviews, pricing information, feature comparisons, user feedback, and market position. Look for sources from the past 6 months and provide balanced analysis with specific examples.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

**Industry trends and statistics:**
```
Search the web for current trends and statistics about [INDUSTRY OR MARKET]. Focus on recent reports, market research, expert analysis, and quantitative data from the past 12 months. Include sources like industry reports, research firms, and reputable business publications.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

**Technical documentation and examples:**
```
Do web search for latest best practices, documentation, and examples about [TECHNOLOGY]. Focus on official documentation, recent tutorials, community discussions, and current conventions. Include code examples and practical implementation guidance from 2024-2025.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

## Execution Commands

### Basic Command Structure

```bash
# Direct web search with crafted instruction
gemini -p "[CRAFTED_INSTRUCTION_FOR_TOPIC]"

# Pipe content to Gemini with analysis instruction
cat [FILE] | gemini -p "Analyze this content and do web search for [RESEARCH_TOPIC]"
```

### JSON Output for Structured Data

```bash
# Get structured JSON response
gemini -p "[INSTRUCTION]" --output-format json | jq '.response'

# Extract sources from JSON response
gemini -p "[INSTRUCTION]" --output-format json | jq '.sources[]'

# Process streaming responses for long content
gemini -p "[COMPREHENSIVE_INSTRUCTION]" --output-format stream-json
```

## Response Processing

### Handling Gemini CLI Responses

After executing `gemini -p`, process the returned information:

**For standard text responses:**
- Extract main content and source citations
- Verify that sources are properly formatted with URLs
- Check for publication dates and source authority
- Present information in user-friendly format

**For JSON responses:**
```bash
# Extract main response content
gemini -p "[INSTRUCTION]" --output-format json | jq -r '.response'

# Extract structured sources
gemini -p "[INSTRUCTION]" --output-format json | jq '.sources[] | "\(.title): \(.url)"'

# Get metadata about search quality
gemini -p "[INSTRUCTION]" --output-format json | jq '.metadata'
```

### Quality Validation Guidelines

When processing Gemini CLI responses, verify:

1. **Source currency** - Check if information reflects recent developments
2. **Source reliability** - Assess credibility of cited sources
3. **Information completeness** - Ensure user's question is fully addressed
4. **Source accessibility** - Verify URLs are accessible and relevant

### Error Handling Strategies

If Gemini CLI returns inadequate results:

1. **Refine the instruction** with more specific requirements:
    ```
    Do web search for [TOPIC]. Focus on sources from 2024-2025, look for official documentation, and include specific examples and data points.

    IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
    ```

2. **Add domain constraints** for better source quality:
    ```
    Search the web on site:official-docs.com OR site:reputable-news.com about [TOPIC]. Focus on recent coverage and expert analysis.

    IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
    ```

3. **Request specific source types**:
    ```
    Do web research about [TOPIC]. Look for academic papers, industry reports, and government statistics from the past 12 months.

    IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
    ```

## Common Usage Scenarios

### Replacing Claude Code's WebSearch

**When user asks:** "What are the latest developments in AI?"

**Claude Code action:**
```bash
gemini -p "Do web search for latest developments in AI and machine learning. Focus on breakthrough technologies, recent product launches, and research advances from 2024-2025. Include specific examples, company announcements, and expert analysis with proper source attribution.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations."
```

### Technical Research

**When user asks:** "How do I implement authentication in React?"

**Claude Code action:**
```bash
gemini -p "Search the web for current best practices and examples of implementing authentication in React applications. Focus on modern libraries like Auth0, Firebase Auth, and Next.js auth from 2024-2025. Include code examples, security considerations, and official documentation sources.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations."
```

### Current Events Verification

**When user asks:** "Is [company] still in business?"

**Claude Code action:**
```bash
gemini -p "Search the web to verify the current business status of [COMPANY]. Look for recent news, official company announcements, financial reports, and reliable business sources from the past 6 months. Provide evidence of current operational status or changes.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations."
```

## Integration with Local Content

### Code Analysis with Current Context

```bash
# Analyze codebase with current best practices
cat codebase.txt | gemini -p "Analyze this code structure and do web search for current best practices, security vulnerabilities, and modern alternatives for [TECHNOLOGY] as of 2024-2025. Focus on recent documentation and community recommendations.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations."

# Update outdated patterns
README.md | gemini -p "Review this documentation and do web search for current project standards, formatting conventions, and comprehensive examples for [TOPIC]. Focus on recent guidelines and community best practices.

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations."
```

## Guidelines

- Always include the "web research ONLY" constraint when using Gemini CLI to prevent unintended actions
- Validate source currency - check publication dates before presenting information
- Use domain constraints (site:) for authoritative sources in specific fields
- For technical searches, always request sources from 2024-2025
- Process JSON output when structured data is needed
- Refine instructions if initial results are inadequate


## Resources

- [Google Gemini CLI](https://github.com/google-gemini/gemini-cli) - Tool you're coordinating with
- [Headless Mode Guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md) - Execution patterns
- [JSON Output Documentation](https://github.com/google-gemini/gemini-cli/docs) - Response processing
- [Search Operators Reference](https://developers.google.com/search/docs/essentials/search_operators) - Instruction crafting
