---
name: c4-architecture-documentation
description: C4 architecture model for documenting static HTML/CSS websites with MCP server integrations
license: Apache-2.0
---

# C4 Architecture Documentation

## Purpose

Document Riksdagsmonitor architecture using C4 model (Context, Container, Component, Code).

## C4 Model Levels

### Level 1: Context Diagram
Shows system in environment with users and external systems.

```mermaid
C4Context
  title System Context - Riksdagsmonitor

  Person(citizen, "Citizen", "Seeks political transparency")
  
  System(riksdag, "Riksdagsmonitor", "Static HTML/CSS website for Swedish Parliament monitoring")
  
  System_Ext(github_pages, "GitHub Pages", "Static site hosting with CDN")
  System_Ext(riksdag_api, "Riksdag-Regering MCP", "Swedish political data API (32 tools)")
  System_Ext(cia, "CIA Platform", "Political intelligence backend")
  
  Rel(citizen, riksdag, "Views political data", "HTTPS")
  Rel(riksdag, github_pages, "Hosted on", "HTTPS, TLS 1.3")
  Rel(riksdag, riksdag_api, "Fetches data via", "HTTP MCP")
  Rel(riksdag, cia, "Links to", "HTTPS")
```

### Level 2: Container Diagram
Shows high-level technology choices.

```mermaid
C4Container
  title Container Diagram - Riksdagsmonitor

  Person(citizen, "Citizen")
  
  Container(web, "Web Application", "HTML5/CSS3", "Static website with 14 languages")
  Container(mcp, "MCP Servers", "Node.js", "riksdag-regering, filesystem, memory, git")
  Container(gh_actions, "GitHub Actions", "CI/CD", "Quality checks, deployment")
  
  ContainerDb(git_repo, "Git Repository", "GitHub", "Version control, content storage")
  
  System_Ext(github_pages, "GitHub Pages")
  System_Ext(riksdag_api, "Riksdagen API")
  
  Rel(citizen, web, "Views", "HTTPS")
  Rel(web, github_pages, "Hosted on")
  Rel(mcp, riksdag_api, "Fetches data")
  Rel(gh_actions, git_repo, "Deploys from")
  Rel(gh_actions, github_pages, "Publishes to")
```

### Level 3: Component Diagram
Shows internal structure.

## Documentation Structure

**ARCHITECTURE.md Template:**
```markdown
# Architecture

## Executive Summary
## System Context (C4 Level 1)
## Container View (C4 Level 2)
## Component View (C4 Level 3)
## Technology Stack
## Security Architecture
## Deployment Pipeline
## References
```

## References

- **C4 Model**: https://c4model.com
- **ARCHITECTURE.md**: Complete C4 models
- **Mermaid Docs**: https://mermaid.js.org/
