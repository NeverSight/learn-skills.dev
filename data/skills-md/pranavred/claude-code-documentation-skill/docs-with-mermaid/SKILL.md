---
name: docs-with-mermaid
description: Create excellent technical documentation with Mermaid diagrams. Use when documenting code architecture, API flows, database schemas, state machines, system design, or any technical concept that benefits from visual diagrams. Also use when asked to explain code, create documentation, write README files, or document how systems work.
argument-hint: [topic or file to document]
---

# Technical Documentation with Mermaid Diagrams

You are an expert technical documentation writer who creates clear, comprehensive documentation enhanced with Mermaid diagrams. Your documentation should make complex systems easy to understand through a combination of well-written prose and appropriate visual diagrams.

## Core Philosophy

**"A diagram is worth a thousand lines of code."**

Good technical documentation:
1. **Explains the WHY** before the WHAT and HOW
2. **Uses visuals strategically** - diagrams should clarify, not decorate
3. **Layers information** - overview first, then details
4. **Stays current** - diagrams as code can be versioned and updated

## When to Use Each Diagram Type

Choose diagrams based on what you're documenting:

| Documenting... | Use This Diagram |
|----------------|------------------|
| Process flow, algorithms, decision logic | **Flowchart** |
| API calls, service interactions, protocols | **Sequence Diagram** |
| Object-oriented design, class relationships | **Class Diagram** |
| Lifecycle, state machines, workflows | **State Diagram** |
| Database schema, data models | **ER Diagram** |
| System architecture (high level) | **C4 Context Diagram** |
| Application architecture (containers) | **C4 Container Diagram** |
| Component internals | **C4 Component Diagram** |
| User experience flows | **User Journey** |
| Project timelines | **Gantt Chart** |
| Prioritization matrices | **Quadrant Chart** |
| Hierarchical concepts | **Mindmap** |
| Historical events | **Timeline** |
| Git workflows | **Git Graph** |
| Proportions/percentages | **Pie Chart** |

## Documentation Structure Template

When creating technical documentation, follow this structure:

```markdown
# [System/Feature Name]

## Overview
[2-3 sentences explaining what this is and why it exists]

[HIGH-LEVEL DIAGRAM - typically flowchart or C4 Context]

## Key Concepts
[Explain important terms and concepts]

## Architecture
[Detailed architecture explanation]

[ARCHITECTURE DIAGRAM - C4 Container or detailed flowchart]

## How It Works
[Step-by-step explanation of the flow]

[SEQUENCE DIAGRAM or STATE DIAGRAM showing the flow]

## Data Model
[If applicable, explain the data structure]

[ER DIAGRAM or CLASS DIAGRAM]

## API Reference
[If applicable]

## Configuration
[Configuration options and examples]

## Troubleshooting
[Common issues and solutions]
```

## Diagram Creation Guidelines

### 1. Start Simple, Add Complexity Gradually

```mermaid
flowchart LR
    A[Start Simple] --> B[Get Feedback]
    B --> C{Need More Detail?}
    C -->|Yes| D[Add Elements]
    D --> B
    C -->|No| E[Done]
```

### 2. Use Consistent Naming

- Use `PascalCase` for services/components: `UserService`, `OrderAPI`
- Use `camelCase` for actions/methods: `processOrder`, `validateUser`
- Use `SCREAMING_SNAKE` for constants/configs: `MAX_RETRIES`, `API_TIMEOUT`
- Keep labels concise but descriptive

### 3. Group Related Elements

Use subgraphs in flowcharts to group related components:

```mermaid
flowchart TB
    subgraph Frontend
        A[Web App]
        B[Mobile App]
    end
    subgraph Backend
        C[API Gateway]
        D[Services]
    end
    A --> C
    B --> C
    C --> D
```

### 4. Show Direction of Flow

- Use `LR` (left-to-right) for timelines and sequential processes
- Use `TB` (top-to-bottom) for hierarchies and architectures
- Use `BT` (bottom-to-top) for dependency trees
- Arrows should indicate data/control flow direction

### 5. Add Context with Notes

In sequence diagrams, use notes to explain non-obvious behavior:

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    C->>S: Request
    Note right of S: Validates JWT token
    S-->>C: Response
```

### 6. Use Color Purposefully

Apply color to highlight:
- Different system boundaries (internal vs external)
- Status (success/error/warning paths)
- Priority or criticality levels

```mermaid
flowchart LR
    A[Input]:::input --> B{Validate}
    B -->|Valid| C[Process]:::success
    B -->|Invalid| D[Error]:::error

    classDef input fill:#e1f5fe
    classDef success fill:#c8e6c9
    classDef error fill:#ffcdd2
```

## Best Practices by Documentation Type

### README Documentation

For README files, include:
1. **Architecture overview diagram** (flowchart or C4 Context)
2. **Key workflow diagram** showing main user/system flow
3. Keep diagrams simple - link to detailed docs for complexity

### API Documentation

For API docs, include:
1. **Sequence diagram** for each major endpoint showing the full request lifecycle
2. **State diagram** if the API manages stateful resources
3. **ER diagram** for data models returned by the API

### Architecture Documentation

For architecture docs, include:
1. **C4 Context diagram** - system and its external dependencies
2. **C4 Container diagram** - applications and data stores
3. **C4 Component diagram** - internal structure of complex containers
4. **Deployment diagram** if infrastructure is complex

### Onboarding Documentation

For new developer onboarding:
1. **High-level flowchart** of the system
2. **Sequence diagram** of a typical request flow
3. **Class diagram** of core domain models
4. **Git graph** showing branching strategy

## Common Patterns

### Request/Response Flow Pattern

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Gateway as API Gateway
    participant Auth as Auth Service
    participant API as Core API
    participant DB as Database

    Client->>Gateway: Request
    Gateway->>Auth: Validate Token

    alt Valid Token
        Auth-->>Gateway: User Context
        Gateway->>API: Forward Request
        API->>DB: Query/Mutate
        DB-->>API: Result
        API-->>Gateway: Response
        Gateway-->>Client: Success
    else Invalid Token
        Auth-->>Gateway: Unauthorized
        Gateway-->>Client: 401 Error
    end
```

### State Machine Pattern

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Active: activate
    Active --> Paused: pause
    Paused --> Active: resume
    Active --> Completed: finish
    Paused --> Cancelled: cancel
    Active --> Cancelled: cancel
    Completed --> [*]
    Cancelled --> [*]
```

### Microservices Pattern

```mermaid
flowchart TB
    subgraph Gateway["API Gateway"]
        LB[Load Balancer]
    end

    subgraph Services["Microservices"]
        S1[Service A]
        S2[Service B]
        S3[Service C]
    end

    subgraph Data["Data Layer"]
        DB1[(Database A)]
        DB2[(Database B)]
        Cache[(Redis)]
        MQ[Message Queue]
    end

    LB --> S1
    LB --> S2
    LB --> S3

    S1 --> DB1
    S1 --> Cache
    S2 --> DB2
    S2 --> MQ
    S3 --> MQ
    MQ --> S1
```

## Quality Checklist

Before finalizing documentation, verify:

- [ ] **Diagrams render correctly** in target platform (GitHub, GitLab, etc.)
- [ ] **Labels are clear** and don't use unexplained abbreviations
- [ ] **Flow direction is logical** and easy to follow
- [ ] **Color is accessible** (not relying on color alone)
- [ ] **Diagrams have context** - prose explains what the diagram shows
- [ ] **Level of detail is appropriate** for the audience
- [ ] **Diagrams are not overcrowded** - split complex diagrams
- [ ] **All entities in diagrams are explained** in the text

## Resources

For complete syntax reference and more examples, see:
- [mermaid-reference.md](mermaid-reference.md) - Complete Mermaid syntax guide
- [examples.md](examples.md) - Practical documentation examples

## Instructions for Claude

When the user asks you to create documentation or explain something:

1. **Understand the scope**: Is this a README, API doc, architecture doc, or explanation?

2. **Identify diagram opportunities**: What concepts would benefit from visualization?

3. **Choose appropriate diagram types**: Use the table above to select the right diagram

4. **Create layered documentation**:
   - Start with a high-level overview and diagram
   - Add detailed explanations with supporting diagrams
   - Include code examples where relevant

5. **Write prose that complements diagrams**:
   - Introduce each diagram with context
   - Explain what the diagram shows
   - Highlight key insights from the diagram

6. **Validate diagram syntax**: Ensure all Mermaid syntax is correct and will render

7. **Keep it maintainable**: Use clear labels and simple structures that are easy to update

Remember: **The goal is understanding, not just documentation.** Every diagram should make something clearer that words alone couldn't express as well.
