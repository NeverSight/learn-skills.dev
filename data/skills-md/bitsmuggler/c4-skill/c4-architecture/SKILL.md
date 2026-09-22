---
name: c4-architecture
description: >
  This skill should be used when the user asks to "create a C4 model",
  "generate architecture diagrams", "create a Structurizr workspace",
  "analyse the architecture", "model the system architecture",
  "create a system context diagram", "create a container diagram",
  "create a component diagram", "generate C4 diagrams",
  mentions C4, Structurizr, or architecture modelling,
  or needs to visualise software architecture.
version: 0.1.0
tools: Read, Glob, Grep, Bash, Write, Edit
---

# C4 Architecture Modelling with Structurizr DSL

Generate C4 architecture models using the Structurizr DSL and optionally render them as images.

## When To Use

- User wants to analyse and document software architecture
- User asks for C4 diagrams (System Context, Container, Component, Deployment)
- User wants to generate or update a Structurizr DSL workspace file
- User wants to render architecture diagrams as images

## Architecture Analysis Process

### Step 1: Discover the System

Analyse the codebase to identify architectural elements:

**Configuration & Build Files**
- `package.json`, `pom.xml`, `build.gradle`, `go.mod`, `Cargo.toml`, `requirements.txt`
- `docker-compose.yml`, `Dockerfile`, `kubernetes/*.yml`
- `.env`, configuration files, infrastructure-as-code

**Identify Elements**
- **People/Actors**: Who uses the system? (end users, admins, external services)
- **Software Systems**: The system being modelled + external systems it interacts with
- **Containers**: Deployable units (web apps, APIs, databases, message queues, file stores)
- **Components**: Logical groupings within containers (controllers, services, repositories)

**Map Relationships**
- API calls between services (REST, gRPC, GraphQL)
- Database connections and which containers access which stores
- Message queue producers/consumers
- External integrations (payment providers, email services, auth providers)
- User interactions with the system

### Step 2: Generate the Structurizr DSL

Write a `workspace.dsl` file following the Structurizr DSL syntax.

For the full DSL language reference, read: `references/structurizr-dsl-reference.md`
For a working example, read: `examples/example-workspace.dsl`

**Structure the workspace as follows:**

```
workspace "[System Name]" "[Brief description]" {
    model {
        // 1. Define people (actors)
        // 2. Define software systems
        //    - Nest containers inside the primary system
        //    - Nest components inside containers (if needed)
        // 3. Define relationships between elements
    }
    views {
        // 4. Create views at each required C4 level
        // 5. Apply styling via themes or element/relationship styles
    }
}
```

**Naming Conventions:**
- Use camelCase for identifiers: `webApp`, `apiGateway`, `userDb`
- Use descriptive display names: `"Web Application"`, `"API Gateway"`
- Include technology labels: `"Spring Boot REST API"`, `"PostgreSQL 15"`

**Relationship Guidelines:**
- Always include a description: `user -> webApp "Browses products using" "HTTPS"`
- Include technology where relevant: `"REST/JSON"`, `"JDBC"`, `"AMQP"`
- Direction matters: source -> destination (who initiates the interaction)

### Step 3: Create Views

Generate appropriate views based on the level of detail needed:

- **System Landscape**: Overview of all systems (`systemLandscape`)
- **System Context**: One system + its direct interactions (`systemContext`)
- **Container**: Internal structure of a system (`container`)
- **Component**: Internal structure of a container (`component`)
- **Deployment**: Infrastructure mapping (`deployment`)

Always use `autoLayout` unless the user provides explicit layout preferences.

### Step 4: Apply Styling

Use tags and styles to make diagrams readable:

```
styles {
    element "Person" {
        shape Person
        background #08427B
        color #ffffff
    }
    element "Software System" {
        background #1168BD
        color #ffffff
    }
    element "Container" {
        background #438DD5
        color #ffffff
    }
    element "Component" {
        background #85BBF0
        color #000000
    }
    element "Database" {
        shape Cylinder
    }
    element "External" {
        background #999999
        color #ffffff
    }
}
```

### Step 5: Export and Render Diagrams

All export and rendering is done via Docker. Requires Docker to be installed and running.

**Export DSL to C4-PlantUML:**

```bash
mkdir -p ./diagrams
docker run --rm -v $PWD:/usr/local/structurizr structurizr/structurizr \
    export -workspace /usr/local/structurizr/workspace.dsl -format plantuml/c4plantuml -output /usr/local/structurizr/diagrams
```

**Render PlantUML to PNG:**

```bash
docker run --rm -v $PWD/diagrams:/data plantuml/plantuml -tpng /data/*.puml
```

**Render PlantUML to SVG:**

```bash
docker run --rm -v $PWD/diagrams:/data plantuml/plantuml -tsvg /data/*.puml
```

Other supported export formats: `plantuml`, `mermaid`, `json`.

**Prerequisite:** Docker (`docker pull structurizr/structurizr && docker pull plantuml/plantuml`)

## Quality Checklist

Before presenting the workspace to the user, verify:

- [ ] All identified systems, containers, and components are modelled
- [ ] Every element has a description and technology label where appropriate
- [ ] Relationships have meaningful descriptions (not just "uses")
- [ ] External systems are clearly distinguished (tagged as "External")
- [ ] Database elements use the Cylinder shape
- [ ] Views exist for each appropriate C4 level
- [ ] `autoLayout` is applied to all views
- [ ] Styling is consistent and follows C4 colour conventions
