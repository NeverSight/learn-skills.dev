---
name: uml-modeling
description: UML diagram generation including class, sequence, activity, use case, and state diagrams
allowed-tools: Read, Glob, Grep, Write, Edit
---

# UML Modeling Skill

## When to Use This Skill

Use this skill when:

- **Uml Modeling tasks** - Working on uml diagram generation including class, sequence, activity, use case, and state diagrams
- **Planning or design** - Need guidance on Uml Modeling approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Create UML diagrams using PlantUML and Mermaid notation for software design documentation.

## MANDATORY: Documentation-First Approach

Before creating UML diagrams:

1. **Invoke `docs-management` skill** for UML standards guidance
2. **Verify diagram syntax** using appropriate notation (PlantUML/Mermaid)
3. **Base all guidance on UML 2.5 specification**

## UML Diagram Types

### Structural Diagrams

| Diagram | Purpose | When to Use |
|---------|---------|-------------|
| Class | Show classes, attributes, methods, relationships | Domain modeling, design |
| Component | Show components and dependencies | Architecture documentation |
| Deployment | Show physical deployment | Infrastructure planning |
| Object | Show object instances | Specific scenarios |
| Package | Show namespaces/modules | Code organization |

### Behavioral Diagrams

| Diagram | Purpose | When to Use |
|---------|---------|-------------|
| Use Case | Show actor-system interactions | Requirements |
| Sequence | Show message flow over time | API design, protocols |
| Activity | Show workflows and processes | Business processes |
| State Machine | Show state transitions | Lifecycle modeling |
| Communication | Show object interactions | Design patterns |

## Class Diagram

### PlantUML Syntax

```plantuml
@startuml
skinparam classAttributeIconSize 0

abstract class Entity {
  +Id: Guid
  +CreatedAt: DateTimeOffset
  +UpdatedAt: DateTimeOffset
}

class Order extends Entity {
  -_lineItems: List<LineItem>
  +CustomerId: Guid
  +Status: OrderStatus
  +Total: Money
  --
  +AddItem(product: Product, quantity: int): Result<LineItem>
  +RemoveItem(lineItemId: Guid): Result
  +Submit(): Result
  +Cancel(): Result
}

class LineItem extends Entity {
  +ProductId: Guid
  +ProductName: string
  +Quantity: int
  +UnitPrice: Money
  +LineTotal: Money
}

enum OrderStatus {
  Draft
  Submitted
  Paid
  Shipped
  Delivered
  Cancelled
}

class Money <<value object>> {
  +Amount: decimal
  +Currency: string
  +{static} Zero: Money
  +Add(other: Money): Money
  +Multiply(factor: decimal): Money
}

Order "1" *-- "0..*" LineItem : contains
Order --> OrderStatus
Order --> Money
LineItem --> Money

@enduml
```

### Mermaid Class Diagram

```mermaid
classDiagram
    class Entity {
        <<abstract>>
        +Guid Id
        +DateTimeOffset CreatedAt
        +DateTimeOffset UpdatedAt
    }

    class Order {
        -List~LineItem~ _lineItems
        +Guid CustomerId
        +OrderStatus Status
        +Money Total
        +AddItem(Product, int) Result~LineItem~
        +RemoveItem(Guid) Result
        +Submit() Result
        +Cancel() Result
    }

    class LineItem {
        +Guid ProductId
        +string ProductName
        +int Quantity
        +Money UnitPrice
        +Money LineTotal
    }

    class OrderStatus {
        <<enumeration>>
        Draft
        Submitted
        Paid
        Shipped
        Delivered
        Cancelled
    }

    Entity <|-- Order
    Entity <|-- LineItem
    Order "1" *-- "0..*" LineItem : contains
    Order --> OrderStatus
```

### Relationship Types

```csharp
// UML Relationship Reference
public static class UMLRelationships
{
    // Association: uses, knows about
    // Customer --> Order (Customer uses Order)

    // Aggregation: has-a (shared ownership)
    // Team o-- Player (Team has Players, Players can exist independently)

    // Composition: contains (exclusive ownership)
    // Order *-- LineItem (Order contains LineItems, LineItems cannot exist without Order)

    // Inheritance: is-a
    // Dog --|> Animal (Dog extends Animal)

    // Implementation: implements
    // UserService ..|> IUserService (UserService implements IUserService)

    // Dependency: depends on
    // Controller ..> Service (Controller depends on Service)
}
```

## Sequence Diagram

### PlantUML Syntax

```plantuml
@startuml
title Order Submission Flow

actor Customer
participant "API Gateway" as API
participant "Order Service" as Orders
participant "Payment Service" as Payment
participant "Notification Service" as Notify
database "Order DB" as DB
queue "Message Bus" as Bus

Customer -> API: POST /orders/{id}/submit
activate API

API -> Orders: SubmitOrder(orderId)
activate Orders

Orders -> DB: GetOrder(orderId)
activate DB
DB --> Orders: Order
deactivate DB

alt Order is valid
    Orders -> Payment: ProcessPayment(order)
    activate Payment

    Payment --> Orders: PaymentResult
    deactivate Payment

    alt Payment successful
        Orders -> DB: UpdateStatus(Paid)
        Orders -> Bus: Publish(OrderSubmitted)
        Bus -> Notify: OrderSubmitted
        activate Notify
        Notify -> Notify: SendConfirmation()
        deactivate Notify

        Orders --> API: Success
        API --> Customer: 200 OK
    else Payment failed
        Orders --> API: PaymentFailed
        API --> Customer: 402 Payment Required
    end
else Order invalid
    Orders --> API: ValidationError
    API --> Customer: 400 Bad Request
end

deactivate Orders
deactivate API

@enduml
```

### Mermaid Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Customer
    participant A as API Gateway
    participant O as Order Service
    participant P as Payment Service
    participant D as Database

    C->>A: POST /orders/{id}/submit
    activate A
    A->>O: SubmitOrder(orderId)
    activate O
    O->>D: GetOrder(orderId)
    D-->>O: Order

    alt Order valid
        O->>P: ProcessPayment(order)
        P-->>O: PaymentResult

        alt Payment successful
            O->>D: UpdateStatus(Paid)
            O-->>A: Success
            A-->>C: 200 OK
        else Payment failed
            O-->>A: PaymentFailed
            A-->>C: 402 Payment Required
        end
    else Order invalid
        O-->>A: ValidationError
        A-->>C: 400 Bad Request
    end

    deactivate O
    deactivate A
```

## Activity Diagram

### PlantUML Syntax

```plantuml
@startuml
title Order Processing Workflow

start

:Customer submits order;

:Validate order;

if (Order valid?) then (yes)
  :Calculate totals;
  :Reserve inventory;

  fork
    :Process payment;
  fork again
    :Send confirmation email;
  end fork

  if (Payment successful?) then (yes)
    :Confirm inventory;
    :Create shipment;
    :Update order status;
    stop
  else (no)
    :Release inventory;
    :Notify customer;
    stop
  endif
else (no)
  :Return validation errors;
  stop
endif

@enduml
```

## Use Case Diagram

### PlantUML Syntax

```plantuml
@startuml
left to right direction

actor Customer
actor "Warehouse Staff" as Warehouse
actor Admin

rectangle "E-Commerce System" {
  usecase "Browse Products" as UC1
  usecase "Add to Cart" as UC2
  usecase "Checkout" as UC3
  usecase "Track Order" as UC4
  usecase "Process Refund" as UC5
  usecase "Manage Inventory" as UC6
  usecase "Fulfill Order" as UC7
  usecase "Generate Reports" as UC8

  Customer --> UC1
  Customer --> UC2
  Customer --> UC3
  Customer --> UC4
  Customer --> UC5

  Warehouse --> UC6
  Warehouse --> UC7

  Admin --> UC6
  Admin --> UC8

  UC3 ..> UC2 : <<include>>
  UC5 ..> UC4 : <<extend>>
}

@enduml
```

## State Machine Diagram

### PlantUML Syntax

```plantuml
@startuml
title Order State Machine

[*] --> Draft : Create

Draft --> Submitted : Submit
Draft --> Cancelled : Cancel

Submitted --> Paid : PaymentReceived
Submitted --> Cancelled : Cancel
Submitted --> Draft : RequiresChanges

Paid --> Shipped : Ship
Paid --> Refunded : Refund

Shipped --> Delivered : Deliver
Shipped --> Returned : Return

Delivered --> Completed : Finalize
Delivered --> Returned : Return

Returned --> Refunded : ProcessReturn

Completed --> [*]
Refunded --> [*]
Cancelled --> [*]

@enduml
```

### Mermaid State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft : Create

    Draft --> Submitted : Submit
    Draft --> Cancelled : Cancel

    Submitted --> Paid : PaymentReceived
    Submitted --> Cancelled : Cancel
    Submitted --> Draft : RequiresChanges

    Paid --> Shipped : Ship
    Paid --> Refunded : Refund

    Shipped --> Delivered : Deliver
    Shipped --> Returned : Return

    Delivered --> Completed : Finalize
    Delivered --> Returned : Return

    Returned --> Refunded : ProcessReturn

    Completed --> [*]
    Refunded --> [*]
    Cancelled --> [*]
```

## Component Diagram

### PlantUML Syntax

```plantuml
@startuml
title System Components

package "Presentation Layer" {
  [Web Application] as Web
  [Mobile App] as Mobile
}

package "API Layer" {
  [API Gateway] as Gateway
  [GraphQL Server] as GraphQL
}

package "Business Layer" {
  [Order Service] as Orders
  [Payment Service] as Payment
  [Notification Service] as Notify
  [User Service] as Users
}

package "Data Layer" {
  database "Order DB" as OrderDB
  database "User DB" as UserDB
  queue "Message Bus" as Bus
}

package "External" {
  [Payment Provider] as PaymentExt
  [Email Service] as EmailExt
}

Web --> Gateway
Mobile --> Gateway
Gateway --> GraphQL
Gateway --> Orders
Gateway --> Users

Orders --> OrderDB
Orders --> Bus
Users --> UserDB

Payment --> PaymentExt
Notify --> EmailExt
Notify --> Bus

@enduml
```

## Best Practices

### General Guidelines

1. **Keep diagrams focused**: One concept per diagram
2. **Use consistent notation**: Choose PlantUML or Mermaid per project
3. **Add meaningful names**: Clear, descriptive labels
4. **Include legends**: For complex diagrams
5. **Version control**: Store in repository with code

### Diagram Selection Guide

| Need | Diagram Type |
|------|--------------|
| Data structures, domain model | Class Diagram |
| API flow, protocols | Sequence Diagram |
| Business processes | Activity Diagram |
| Actor interactions | Use Case Diagram |
| Lifecycle, state transitions | State Machine |
| System structure | Component Diagram |
| Infrastructure | Deployment Diagram |

## Workflow

When creating UML diagrams:

1. **Identify purpose**: What question does the diagram answer?
2. **Select diagram type**: Choose most appropriate type
3. **Draft in text**: Use PlantUML or Mermaid notation
4. **Review for accuracy**: Verify against code/requirements
5. **Add context**: Title, notes, legend as needed
6. **Render and verify**: Ensure diagram renders correctly

## References

For detailed notation guides:

---

**Last Updated:** 2025-12-26
