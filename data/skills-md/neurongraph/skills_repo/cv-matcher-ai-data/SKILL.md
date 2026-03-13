---
name: cv-matcher-ai-data
description: Analyzes CVs to extract skills and experience, maps candidates to specific roles (ML Engineer, GenAI Engineer, AI Architect, Data Engineer), and matches them against open demands. Use when processing multiple CVs for role classification, skill assessment, or resource allocation to client accounts.
---

# CV Matcher for AI and Data Roles

## Instructions

1. Read CVs from the specified directory, defaulting to current directory if unspecified. Look for .pdf or .docx files only
2. Extract experience, projects, and technologies from each CV
3. Map candidates to roles based on criteria below
4. Generate Output1 (role-based analysis with rankings)
5. Request open demands from user (Account, Role, Number of resources)
6. Generate Output2 (candidate-to-demand matching)

## Role Classification Criteria

**ML Engineer**: Machine Learning experience, data analysis, ML-related Python packages

**GenAI Engineer**: Python, LLMs, prompt engineering, GenAI packages. Agents/agentic frameworks preferred

**AI Architect**: ML/Data Platform/Application Architecture background with Architect or Solution Designer role. Python, LLMs, prompt engineering, GenAI packages, agents/agentic frameworks preferred

**Data Engineer**: ETL experience using Python or SQL frameworks (PySpark, PySQL, dbt, Databricks, AWS Glue)

## Output Specifications

### Output1: Role Analysis
Markdown tables by role, ranking candidates by skill match with short justifications. Include summary table showing each candidate's best-matched roles.

### Output2: Demand Matching
Match candidates to open demands by role. If demand > supply, fill minimum one role per account. If supply > demand, assign more candidates than requested based on role match. Output markdown table with assignments and justifications.
