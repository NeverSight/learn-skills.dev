---
name: documentation-portfolio
description: Required architecture documents including current/future state diagrams, data models, flowcharts, state diagrams, mindmaps, and SWOT analysis
license: Apache-2.0
---

# Documentation Portfolio Skill

## Purpose
Defines the complete set of architecture documentation required for all Hack23 projects, ensuring comprehensive documentation supporting both current operations and future planning.

## Required Documentation Files

### Current State Documentation
- `ARCHITECTURE.md` — Complete C4 models (Context, Container, Component views)
- `DATA_MODEL.md` — Data structures, entities, and relationships
- `FLOWCHART.md` — Business process and data flows
- `STATEDIAGRAM.md` — System state transitions and lifecycles
- `MINDMAP.md` — System conceptual relationships
- `SWOT.md` — Strategic analysis and positioning

### Future State Planning
- `FUTURE_ARCHITECTURE.md` — Architectural evolution roadmap
- `FUTURE_DATA_MODEL.md` — Enhanced data architecture plans
- `FUTURE_FLOWCHART.md` — Improved process workflows
- `FUTURE_STATEDIAGRAM.md` — Advanced state management
- `FUTURE_MINDMAP.md` — Capability expansion plans
- `FUTURE_SWOT.md` — Future strategic opportunities

### Security Documentation
- `SECURITY_ARCHITECTURE.md` — Security controls and architecture
- `FUTURE_SECURITY_ARCHITECTURE.md` — Planned security improvements
- `THREAT_MODEL.md` — Threat analysis and mitigations

### Supplementary Documentation
- `README.md` — Project overview, getting started
- `.github/SECURITY.md` — Vulnerability reporting
- `CONTRIBUTING.md` — Contribution guidelines

## Documentation Standards

### MUST
- Write in Markdown format
- Use Mermaid for all diagrams
- Include table of contents for documents > 500 lines
- Add last updated date at top of document
- Link related documents
- Keep diagrams up-to-date with code

### MUST NOT
- Include sensitive information (secrets, credentials)
- Create stale documentation (update or delete)
- Duplicate information across documents (link instead)
- Use proprietary diagram formats (use Mermaid)

## Structure Requirements

### ARCHITECTURE.md
1. Overview — System purpose and scope
2. System Context Diagram — C4 Level 1
3. Container Diagram — C4 Level 2
4. Component Diagrams — C4 Level 3
5. Technology Stack
6. Deployment Architecture
7. Integration Points

### DATA_MODEL.md
1. Entity Relationship Diagram (Mermaid ER)
2. Entity Descriptions with attributes
3. Relationships with cardinality
4. Data Classification (sensitivity levels)
5. Data Retention policies

### FLOWCHART.md
1. Key Workflows (Mermaid flowcharts)
2. Decision Points explained
3. Error Handling flows
4. Performance Considerations

### SWOT.md
1. Strengths — Internal positive attributes
2. Weaknesses — Internal limitations
3. Opportunities — External favorable factors
4. Threats — External risks
5. Strategy Matrix
6. Action Items

## Related Policies
- [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)
