---
name: workflow-document-check
description: Check hard word limits in a project's .workflow documents. Use after changing Direction, Backlog, Context, Feature Briefs, PDRs, ADRs, or Acceptance Reports.
---

# Workflow document check

Run `python scripts/check_workflow_docs.py <project-root>` from this installed
skill directory. The script checks hard limits only. Document skills own normal
targets and pruning rules.

A failed limit means the document needs pruning or a clearer boundary. Do not
fill documents to their hard limits. The checker counts whitespace-separated
words in Markdown source, including headings and link text.
