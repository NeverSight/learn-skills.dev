---
name: architecture-documentation
description: Generate architecture documents using templates with diagram integration. Use for creating C4 diagrams, viewpoint documents, and technical overviews.
allowed-tools: Read, Write, Glob, Grep, Skill, Task
---

# Architecture Documentation

## When to Use This Skill

Use this skill when you need to:

- Generate architecture documentation for a system
- Create C4 diagrams (Context, Container, Component)
- Document architecture for different stakeholder viewpoints
- Produce technical overviews or executive summaries

**Keywords:** document, c4, container, context, component, viewpoint, architecture description, technical overview, executive summary

## Document Types

| Type | Audience | Content |
| --- | --- | --- |
| Context | All stakeholders | System boundaries, external interactions |
| Container | Technical leads | Services, databases, major components |
| Component | Developers | Internal structure of containers |
| Deployment | Operations | Infrastructure, environments |
| Data | Data architects | Data flows, storage, schemas |
| Executive Summary | Leadership | Business value, key decisions |

## Document Generation Workflow

### 1. Analyze the Codebase

Before generating documentation:

1. Identify the scope (single service, multiple services, entire system)
2. Find existing documentation to incorporate
3. Locate key architectural files (configs, deployment specs)

### 2. Select Document Type

Choose based on:

- **Audience**: Who will read this?
- **Purpose**: Decision support, onboarding, compliance?
- **Scope**: Component, service, or system level?

### 3. Generate Documentation

Each document type has a standard structure:

#### Context Document

```markdown
# System Context: [System Name]

## Overview
[1-2 paragraph description]

## Context Diagram
[C4 Context diagram - via visualization plugin]

## External Systems
| System | Description | Integration |
| --- | --- | --- |
| ... | ... | ... |

## Users/Actors
| Actor | Description | Interactions |
| --- | --- | --- |
| ... | ... | ... |
```

#### Container Document

```markdown
# Container Architecture: [System Name]

## Overview
[Architecture summary]

## Container Diagram
[C4 Container diagram - via visualization plugin]

## Containers
### [Container Name]
- **Technology**: [Stack]
- **Purpose**: [Description]
- **Responsibilities**: [List]
- **Dependencies**: [List]
```

#### Component Document

```markdown
# Component Architecture: [Container Name]

## Overview
[Component structure summary]

## Component Diagram
[C4 Component diagram - via visualization plugin]

## Components
### [Component Name]
- **Type**: [Service/Repository/Controller/etc.]
- **Responsibilities**: [List]
- **Interfaces**: [Public APIs]
```

### 4. Integrate Diagrams

If the visualization plugin is available:

1. Invoke `visualization:diagram-generator` agent
2. Request appropriate C4 diagram type
3. Embed generated Mermaid/PlantUML code in document

**Fallback**: If visualization plugin unavailable, create text-based architecture description and note that diagrams can be added with the visualization plugin.

## Template Structure

All architecture documents should include:

1. **Header**: Title, version, date, authors
2. **Overview**: 1-2 paragraph summary
3. **Diagram**: Visual representation
4. **Details**: Structured information about components
5. **Decisions**: Link to relevant ADRs
6. **References**: Links to related documentation

## Completeness Checklist

Before finalizing documentation, verify:

- [ ] Scope is clearly defined
- [ ] All major components identified
- [ ] External dependencies documented
- [ ] Key decisions linked to ADRs
- [ ] Diagram matches text description
- [ ] Audience-appropriate language used
- [ ] Version and date included

## Repository Location

Generated documentation should be placed in:

```text
/architecture/
  /viewpoints/
    context.md
    containers.md
    components/
      [container-name].md
    executive-summary.md
```

## Integration with Other Skills

- **adr-management**: Link to relevant ADRs in documentation
- **togaf-guidance**: Align with current ADM phase
- **zachman-analysis**: Ensure appropriate viewpoint coverage

## Version History

- **v1.0.0** (2025-12-05): Initial release
  - Document generation workflow for C4 diagrams
  - Six document types (context, container, component, deployment, data, executive summary)
  - Visualization plugin integration
  - Completeness checklist

---

## Last Updated

**Date:** 2025-12-05
**Model:** claude-opus-4-5-20251101
