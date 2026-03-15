---
name: prd
description: "Guidelines and templates for creating effective Product Requirement Documents (PRD), bridging the gap between business goals and technical implementation."
---

# Product Requirement Document (PRD) Skill

This skill helps you write well-structured and logically clear Product Requirement Documents (PRD). A PRD is the core blueprint of a product — it tells us *why* we are building this product and *what* features it should have.

## Why Do We Need a PRD?

*   **Align Goals**: Ensure developers, designers, and stakeholders share a common understanding of the product.
*   **Reduce Ambiguity**: Transform vague ideas into concrete requirements through clear text and diagrams.
*   **Serve as Test Baseline**: The Acceptance Criteria in the PRD serve as the basis for QA testing.

## PRD Core Components

A complete PRD typically contains the following sections:

1.  **Background & Goals**: Why are we doing this? What problem are we solving? What are the success metrics?
2.  **User Stories**: Who are the users? What do they want to do? What is their purpose?
3.  **Functional Requirements**: Specific descriptions of system behavior.
4.  **Non-Functional Requirements**: Performance, security, reliability constraints.
5.  **UI/UX Flow**: Page flow diagrams, wireframes, or mockup links.
6.  **Analytics**: What user behavior data needs to be tracked?
7.  **Out of Scope**: Clearly define what is *not* included to prevent scope creep.

## How to Use This Skill

When a user presents a vague idea (e.g., "I want a feature that allows users to share bookmarks"), follow these steps:

1.  **Initial Interview**: Ask the user key questions (Who, Why, What).
2.  **Drafting**: Use `template_comprehensive.md` (full version) or `template_simple.md` (simple version) to draft the PRD.
3.  **Review**: Have the user review the draft to confirm it meets expectations.
4.  **Finalize**: Once finalized, this PRD becomes the input for subsequent SA (System Analysis) and implementation phases.

## Tips & Best Practices

*   **Use Clear Language**: Avoid vague words like "might", "should"; use precise terms like "shall/must", "can".
*   **Use Diagrams**: Use flowcharts (Mermaid) to supplement text descriptions.
*   **Keep It Updated**: PRD is a Living Document — if requirements change, update the PRD accordingly.
