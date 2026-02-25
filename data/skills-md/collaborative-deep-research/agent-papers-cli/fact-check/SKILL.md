---
name: fact-check
description: Verify a specific claim by searching for evidence across web and academic sources. Use when the user asks to verify, fact-check, or confirm a statement.
argument-hint: [claim to verify]
allowed-tools: Bash, Read, Glob, Grep, Write
---

Fact-check the following claim: "$ARGUMENTS"

## 1. Decompose

Break the claim into specific, verifiable sub-claims. List them explicitly before searching.

## 2. Search for Evidence

For each sub-claim:
```
paper-search google web "<sub-claim as question>"
paper-search semanticscholar snippets "<sub-claim keywords>"
paper-search semanticscholar papers "<sub-claim keywords>" --limit 5
```

## 3. Verify Sources

For each promising source:
```
paper read <arxiv_id> <relevant section>   # for academic papers
paper-search browse <url>                   # for web pages
```

Prefer primary sources (original papers, official data) over secondary reports.

## 4. Assess

For each sub-claim, assign a verdict:
- **Supported**: strong evidence from multiple reliable sources
- **Partially supported**: some evidence, with caveats
- **Unsupported**: no evidence found, or evidence contradicts the claim
- **Uncertain**: insufficient evidence to judge

## 5. Report

Present:
- The original claim
- Each sub-claim with its verdict and supporting evidence
- An overall assessment
- All sources cited with URLs

## Guidelines

- Always cite specific sources — never state a verdict without evidence.
- Distinguish between "no evidence found" and "evidence contradicts."
- Note the quality and recency of sources.
- If a claim is about a specific paper, read that paper directly rather than relying on summaries.
