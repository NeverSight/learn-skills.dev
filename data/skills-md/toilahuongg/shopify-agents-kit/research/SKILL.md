---
name: research
description: Guide for conducting thorough and synthesized research, focusing on verification, multi-source analysis, and RAG patterns.
---

# Research Skill

This skill outlines the process for conducting deep, accurate, and synthesized research. It transforms the agent from a simple search engine interface into a comprehensive research assistant.

## 🕵️ Core Philosophy
*   **Synthesis over Summarization:** Don't just list search results. Combine information to answer the "So What?".
*   **Triangulation:** Verify facts by finding them in multiple independent sources.
*   **Citation is Mandatory:** Every specific claim must be backed by a source.

## 🛠️ The Research Framework

### 1. Planning (The "Research Agent" Mode)
Before searching, define the scope.
*   **Clarify Objectives:** What is the exact question?
*   **Identify Domains:** Where does this information live? (Academic papers, technical docs, news, forums?)
*   **Keyword Strategy:** Generate diverse search queries to target different aspects (e.g., broad vs. specific, technical vs. layman).

### 2. Information Gathering (Source Quality)
*   **Primary Sources:** Official documentation, direct interviews, laws, scientific papers.
*   **Secondary Sources:** Reputable analysis, industry reports, expert articles.
*   **Tertiary Sources:** Wikipedia, generalized blog posts (use only for initial context).

> **Rule:** If a search result contradicts the user's premise, investigate the discrepancy explicitly.

### 3. Synthesis & Analysis (RAG Pattern)
When presenting findings:
1.  **The Executive Summary:** Answer the question directly in 1-2 paragraphs.
2.  **Key Findings:** Group facts by *theme*, not by source.
    *   *Bad:* "Source A says X. Source B says Y."
    *   *Good:* "The consensus on Topic X is [...], although some experts disagree regarding [...] (Source B)."
3.  **Evidence Table:** If comparing options, always use a table.

### 4. Verification & Fact-Checking
*   **Check Dates:** Is this info outdated? (Critical for tech/laws).
*   **Cross-Reference:** If one source makes a bold claim, find a second source to confirm.
*   **Identify Bias:** Note if a source has a conflict of interest (e.g., a vendor review).

## 🚀 Execution Patterns

**for "Deep Dive" Requests:**
1.  Search for the core concept.
2.  Read the top results to understand the vocabulary.
3.  Refine search with specific technical terms found in step 2.
4.  Synthesize findings into a structured report.

**for "Tech Stack Comparison":**
1.  Identify criteria (e.g., Performance, Cost, DX).
2.  Search for specific comparisons (e.g., "Mongoose vs Prisma performance").
3.  Create a comparison matrix.
4.  Provide a recommendation based on specific use cases.
