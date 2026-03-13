---
name: go-clean-architecture
description: A comprehensive guide to implementing Clean Architecture in software projects, based on the boot-backend-go-clean template.
license: MIT
metadata:
  author: Kirk Lin
  version: "1.0.0"
  source: Based on boot-backend-go-clean
---

# Clean Architecture

Clean Architecture is a software design philosophy that separates the elements of a design into ring levels. The main rule of Clean Architecture is the **Dependency Rule**, which states that source code dependencies can only point inwards. Nothing in an inner circle can know anything at all about something in an outer circle.

## Core Principles

1.  **Independent of Frameworks**: The architecture does not depend on the existence of some library of feature laden software. This allows you to use such frameworks as tools, rather than having to cram your system into their limited constraints.
2.  **Testable**: The business rules can be tested without the UI, Database, Web Server, or any other external element.
3.  **Independent of UI**: The UI can change easily, without changing the rest of the system. A Web UI could be replaced with a console UI, for example, without changing the business rules.
4.  **Independent of Database**: You can swap out Oracle or SQL Server, for Mongo, BigTable, CouchDB, or something else. Your business rules are not bound to the database.
5.  **Independent of any external agency**: In fact your business rules simply don't know anything at all about the outside world.

## The Dependency Rule

The concentric circles represent different areas of software. In general, the further in you go, the higher level the software becomes. The outer circles are mechanisms. The inner circles are policies.

**Source code dependencies must only point inward, towards higher-level policies.**

## Layers

### 1. Entities (Enterprise Logic)
Entities encapsulate enterprise-wide business rules. An entity can be an object with methods, or it can be a set of data structures and functions. It doesn't matter so long as the entities could be used by many different applications in the enterprise.

### 2. Use Cases (Application Logic)
The software in this layer contains application-specific business rules. It encapsulates and implements all of the use cases of the system. These use cases orchestrate the flow of data to and from the entities, and direct those entities to use their enterprise wide business rules to achieve the goals of the use case.

### 3. Interface Adapters (Controllers, Gateways, Presenters)
The software in this layer is a set of adapters that convert data from the format most convenient for the use cases and entities, to the format most convenient for some external agency such as the Database or the Web. It is this layer, for example, that will wholly contain the MVC architecture of a GUI.

### 4. Frameworks & Drivers (Web, DB, UI, External Interfaces)
The outermost layer is generally composed of frameworks and tools such as the Database, the Web Framework, etc. Generally you don’t write much code in this layer other than glue code that communicates to the next circle inwards.

## Implementation Structure Example

The project follows a standard Clean Architecture layout in Go, as demonstrated in `boot-backend-go-clean`.

```text
.
├── cmd/
│   └── app/                 # Application entry point (main.go)
├── internal/
│   ├── domain/              # Enterprise Logic (Entities) & Business Rules
│   │   ├── model/           # Core business objects
│   │   └── repository/      # Repository interfaces (ports)
│   ├── usecase/             # Application Logic (Use Cases)
│   │   └── [feature]/       # Feature-specific use cases
│   ├── interfaces/          # Interface Adapters
│   │   └── http/            # HTTP handlers/controllers
│   ├── infrastructure/      # Frameworks & Drivers
│   │   ├── database/        # Database implementations
│   │   └── config/          # Configuration handling
│   └── app/                 # Application bootstrap/wiring
```

### Reference Implementation
This structure is implemented in the [`boot-backend-go-clean`](../../sources/boot-backend-go-clean) template. Use this template as a starting point for new services.

-   **GitHub Repository**: [https://github.com/kirklin/boot-backend-go-clean](https://github.com/kirklin/boot-backend-go-clean)

## Benefits

-   **Flexibility**: Easy to swap out databases, frameworks, or UI.
-   **Maintainability**: Code is organized by feature and business capability, not technical concern.
-   **Testability**: Business logic is isolated and easily testable.

## Trade-offs

-   **Complexity**: Initial setup and boilerplate code can be higher.
-   **Learning Curve**: Conceptual shift from traditional layered architectures (like MVC).
-   **Indirection**: More layers can mean more jumping around in code to trace a request.
