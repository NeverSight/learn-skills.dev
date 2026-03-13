---
name: deep-research
description: Comprehensive research on a topic using multiple sources and approaches. Spawns parallel research threads.
context: fork
agent: researcher
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
---

# Deep Research

Thoroughly research: $ARGUMENTS

## Methodology
1. **Codebase analysis**: Search the local codebase for related code, patterns, and documentation
2. **Web research**: Use available web tools to find current best practices and documentation
3. **Cross-reference**: Compare findings from multiple sources
4. **Synthesize**: Create a comprehensive summary with actionable insights

## Output
Provide a structured research report:
- Executive summary (2-3 sentences)
- Detailed findings organized by topic
- Code examples where relevant
- Specific recommendations for this project
- Links to key resources
