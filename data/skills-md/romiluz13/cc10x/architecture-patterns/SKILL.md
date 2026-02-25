---
name: architecture-patterns
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Grep, Glob, LSP
---

# Architecture Patterns

## Overview

Architecture exists to support functionality. Every architectural decision should trace back to a functionality requirement.

**Core principle:** Design architecture FROM functionality, not TO functionality.

## Focus Areas (Reference Pattern)

- **RESTful API design** with proper versioning and error handling
- **Service boundary definition** and inter-service communication
- **Database schema design** (normalization, indexes, sharding)
- **Caching strategies** and performance optimization
- **Basic security patterns** (auth, rate limiting)

## The Iron Law

```
NO ARCHITECTURE DESIGN BEFORE FUNCTIONALITY FLOWS ARE MAPPED
```

If you haven't documented user flows, admin flows, and system flows, you cannot design architecture.

## Intake Routing

**First, determine what kind of architectural work is needed:**

| Request Type | Route To |
|--------------|----------|
| "Design API endpoints" | API Design section |
| "Plan system architecture" | Full Architecture Design |
| "Design data models" | Data Model section |
| "Plan integrations" | Integration Patterns section |
| "Make decisions" | Decision Framework section |

## Universal Questions (Answer First)

**ALWAYS answer before designing:**

1. **What functionality are we building?** - User stories, not technical features
2. **Who are the actors?** - Users, admins, external systems
3. **What are the user flows?** - Step-by-step user actions
4. **What are the system flows?** - Internal processing steps
5. **What integrations exist?** - External dependencies
6. **What are the constraints?** - Performance, security, compliance
7. **What observability is needed?** - Logging, metrics, monitoring, alerting

## Functionality-First Design Process

### Phase 1: Map Functionality Flows

**Before any architecture:**

```
User Flow (example):
1. User opens upload page
2. User selects file
3. System validates file type/size
4. System uploads to storage
5. System shows success message

Admin Flow (example):
1. Admin opens dashboard
2. Admin views all uploads
3. Admin can delete uploads
4. System logs admin action

System Flow (example):
1. Request received at API
2. Auth middleware validates token
3. Service processes request
4. Database stores data
5. Response returned
```

### Phase 2: Map to Architecture

**Each flow maps to components:**

| Flow Step | Architecture Component |
|-----------|----------------------|
| User opens page | Frontend route + component |
| User submits data | API endpoint |
| System validates | Validation service |
| System processes | Business logic service |
| System stores | Database + repository |
| System integrates | External client/adapter |

### Phase 3: Design Components

**For each component, define:**

- **Purpose**: What functionality it supports
- **Inputs**: What data it receives
- **Outputs**: What data it returns
- **Dependencies**: What it needs
- **Error handling**: What can fail

## Architecture Views

### System Context (C4 Level 1)
```
┌─────────────────────────────────────────────┐
│                 SYSTEM                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │   Web   │  │   API   │  │Database │     │
│  │   App   │──│ Service │──│         │     │
│  └─────────┘  └─────────┘  └─────────┘     │
└─────────────────────────────────────────────┘
       │              │              │
    ┌──┴──┐        ┌──┴──┐        ┌──┴──┐
    │User │        │Admin│        │ Ext │
    └─────┘        └─────┘        └─────┘
```

### Container View (C4 Level 2)
- **Web App**: React/Vue/Angular frontend
- **API Service**: REST/GraphQL backend
- **Database**: PostgreSQL/MongoDB/etc
- **Cache**: Redis/Memcached
- **Queue**: RabbitMQ/SQS for async

### Component View (C4 Level 3)
- **Controllers**: Handle HTTP requests
- **Services**: Business logic
- **Repositories**: Data access
- **Clients**: External integrations
- **Models**: Data structures

## LSP-Powered Architecture Analysis

**Use LSP to map actual code dependencies:**

| Architecture Task | LSP Tool | Output |
|-------------------|----------|--------|
| Map component dependencies | `lspCallHierarchy(outgoing)` | What each component uses |
| Find all consumers of a service | `lspCallHierarchy(incoming)` | Impact analysis |
| Verify interface implementations | `lspFindReferences` | All implementers |
| Trace data flow | Chain `lspCallHierarchy` calls | Full flow map |

**Mapping Actual Architecture:**
```
1. localSearchCode("ServiceName") → find entry points
2. lspCallHierarchy(outgoing) → map dependencies
3. For each dependency: repeat step 2
4. Build dependency graph from results
```

**Use LSP BEFORE drawing architecture diagrams** - verify assumptions with code.

**CRITICAL:** Always get lineHint from localSearchCode first. Never guess line numbers.

## API Design (Functionality-Aligned)

**Map user flows to endpoints:**

```
User Flow: Upload file
→ POST /api/files
  Request: { file: binary, metadata: {...} }
  Response: { id: string, url: string }
  Errors: 400 (invalid), 413 (too large), 500 (storage failed)

User Flow: View file
→ GET /api/files/:id
  Response: { id, url, metadata, createdAt }
  Errors: 404 (not found), 403 (not authorized)

Admin Flow: Delete file
→ DELETE /api/files/:id
  Response: { success: true }
  Errors: 404, 403
```

**API Design Checklist:**
- [ ] Each endpoint maps to a user/admin flow
- [ ] Request schema matches flow inputs
- [ ] Response schema matches flow outputs
- [ ] Errors cover all failure modes
- [ ] Auth/authz requirements documented

## Integration Patterns

**Map integration requirements to patterns:**

| Requirement | Pattern |
|-------------|---------|
| Flaky external service | Retry with exponential backoff |
| Slow external service | Circuit breaker + timeout |
| Async processing needed | Message queue |
| Real-time updates needed | WebSocket/SSE |
| Data sync needed | Event sourcing |

**For each integration:**
```markdown
### [Integration Name]

**Functionality**: What user flow depends on this?
**Pattern**: [Retry/Circuit breaker/Queue/etc]
**Error handling**: What happens when it fails?
**Fallback**: What's the degraded experience?
```

## Observability Design

**For each component, define:**

| Aspect | Questions |
|--------|-----------|
| **Logging** | What events? What level? Structured format? |
| **Metrics** | What to measure? Counters, gauges, histograms? |
| **Alerts** | What thresholds? Who gets notified? |
| **Tracing** | Span boundaries? Correlation IDs? |

**Minimum observability:**
- Request/response logging at boundaries
- Error rates and latencies
- Health check endpoint
- Correlation ID propagation

## Decision Framework

**For each architectural decision:**

```markdown
### Decision: [Title]

**Context**: What functionality requirement drives this?

**Options**:
1. [Option A] - [Brief description]
2. [Option B] - [Brief description]
3. [Option C] - [Brief description]

**Trade-offs**:
| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Performance | Good | Better | Best |
| Complexity | Low | Medium | High |
| Cost | Low | Medium | High |

**Decision**: [Option chosen]

**Rationale**: [Why this option best supports functionality]
```

## Red Flags - STOP and Redesign

If you find yourself:

- Designing architecture before mapping flows
- Adding components without clear functionality
- Choosing patterns because "it's best practice"
- Over-engineering for hypothetical scale
- Ignoring existing architecture patterns
- Making decisions without documenting trade-offs

**STOP. Go back to functionality flows.**

## Keep It Simple (Reference Pattern)

**Approach for backend architecture:**

1. Start with clear service boundaries
2. Design APIs contract-first
3. Consider data consistency requirements
4. Plan for horizontal scaling from day one
5. **Keep it simple - avoid premature optimization**

**Architecture Output Checklist:**

- [ ] API endpoint definitions with example requests/responses
- [ ] Service architecture diagram (mermaid or ASCII)
- [ ] Database schema with key relationships
- [ ] Technology recommendations with brief rationale
- [ ] Potential bottlenecks and scaling considerations

**Always provide concrete examples. Focus on practical implementation over theory.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This pattern is industry standard" | Does it support THIS functionality? |
| "We might need it later" | YAGNI. Design for now. |
| "Microservices are better" | For this functionality? Justify it. |
| "Everyone uses this" | That's not a trade-off analysis. |
| "It's more flexible" | Flexibility without need = complexity. |

## Output Format

```markdown
# Architecture Design: [Feature/System Name]

## Functionality Summary
[What this architecture supports - trace to user value]

## Flows Mapped

### User Flows
1. [Flow 1 steps]
2. [Flow 2 steps]

### System Flows
1. [Flow 1 steps]
2. [Flow 2 steps]

## Architecture

### System Context
[Diagram or description of actors and system boundaries]

### Components
| Component | Purpose (Functionality) | Dependencies |
|-----------|------------------------|--------------|
| [Name] | [What flow it supports] | [What it needs] |

### API Endpoints
| Endpoint | Flow | Request | Response |
|----------|------|---------|----------|
| POST /api/x | User uploads | {...} | {...} |

## Key Decisions

### Decision 1: [Title]
- Context: [Functionality driver]
- Options: [List]
- Trade-offs: [Table]
- Decision: [Choice]
- Rationale: [Why]

## Implementation Roadmap

### Critical (Must have for core flow)
1. [Component/feature]

### Important (Completes flows)
1. [Component/feature]

### Enhancement (Improves experience)
1. [Component/feature]
```

## Final Check

Before completing architecture design:

- [ ] All user flows mapped
- [ ] All system flows mapped
- [ ] Each component traces to functionality
- [ ] Each API endpoint traces to flow
- [ ] Decisions documented with trade-offs
- [ ] Implementation roadmap prioritized
