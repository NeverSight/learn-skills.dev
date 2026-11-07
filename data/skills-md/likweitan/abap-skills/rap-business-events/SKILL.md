---
name: rap-business-events
description: Help with RAP business events and enterprise eventing including event definitions in behavior definitions, raising events from RAP handler methods, event bindings, SAP Event Mesh integration, event consumption, and event-driven architecture patterns in ABAP Cloud. Use when users ask about RAP business events, enterprise events, event mesh, eventing, raising events, event binding, event definition, event consumption, event-driven, asynchronous processing, event topics, or publish-subscribe in ABAP. Triggers include "RAP event", "business event", "raise event", "event mesh", "event binding", "enterprise eventing", "event-driven", "publish event", "consume event", or "asynchronous event".
---

# RAP Business Events & Enterprise Eventing

Guide for implementing event-driven patterns using RAP business events and SAP Event Mesh in ABAP Cloud.

## Workflow

1. **Determine the user's goal**:
   - Defining business events in a RAP BO
   - Raising events from RAP handler methods
   - Binding events for consumption
   - Consuming events from external systems
   - Integrating with SAP Event Mesh
   - Understanding event-driven architecture in ABAP

2. **Identify the scenario**:
   - Local event (within the same ABAP system)
   - Enterprise event (cross-system via Event Mesh)
   - Event producer vs. event consumer

3. **Guide implementation** following RAP eventing patterns

## Business Events Overview

| Concept               | Description                                                       |
| --------------------- | ----------------------------------------------------------------- |
| **Business Event**    | Declared in BDEF; raised when something significant happens       |
| **Event Definition**  | Formal declaration with parameters in the behavior definition     |
| **Event Raising**     | Triggered in handler/saver methods via `RAISE ENTITY EVENT`       |
| **Event Binding**     | Maps RAP event to an enterprise event topic for external delivery |
| **Event Consumption** | External systems subscribe and react to published events          |

## Defining Business Events

### In the Behavior Definition (BDL)

```
managed implementation in class zbp_r_travel unique;
strict ( 2 );

define behavior for ZR_Travel alias Travel
persistent table ztravel_tab
lock master
authorization master ( instance )
etag master LocalLastChangedAt
{
  create;
  update;
  delete;

  "Define business events
  event travel_created parameter ZD_TravelCreatedEvt;
  event travel_accepted;
  event travel_rejected;
}
```

### Event Parameter Structure

Define a CDS abstract entity for the event payload:

```cds
@EndUserText.label: 'Travel Created Event'
define abstract entity ZD_TravelCreatedEvt
{
  travel_id   : /dmo/travel_id;
  agency_id   : /dmo/agency_id;
  customer_id : /dmo/customer_id;
  description : /dmo/description;
  total_price : /dmo/total_price;
  currency    : /dmo/currency_code;
}
```

Events without the `parameter` addition have no payload.

## Raising Business Events

### In Handler Methods

```abap
METHOD on_travel_accept.
  "Read travel data
  READ ENTITIES OF zr_travel IN LOCAL MODE
    ENTITY Travel
    ALL FIELDS
    WITH CORRESPONDING #( keys )
    RESULT DATA(lt_travels).

  "Update status
  MODIFY ENTITIES OF zr_travel IN LOCAL MODE
    ENTITY Travel
    UPDATE FIELDS ( status )
    WITH VALUE #( FOR travel IN lt_travels
      ( %tky   = travel-%tky
        status = 'A' ) )
    REPORTED DATA(lt_reported).

  "Raise event for each accepted travel
  RAISE ENTITY EVENT zr_travel~travel_accepted
    FROM VALUE #( FOR travel IN lt_travels
      ( %key = travel-%key ) ).
ENDMETHOD.
```

### With Event Parameters

```abap
METHOD on_travel_create.
  "After successful creation
  RAISE ENTITY EVENT zr_travel~travel_created
    FROM VALUE #( FOR travel IN lt_created_travels
      ( %key = travel-%key
        %param = VALUE #(
          travel_id   = travel-travel_id
          agency_id   = travel-agency_id
          customer_id = travel-customer_id
          description = travel-description
          total_price = travel-total_price
          currency    = travel-currency_code ) ) ).
ENDMETHOD.
```

### In Saver Methods (Additional Save)

```abap
METHOD save_modified.
  "Raise events in the save phase for committed data
  IF create-travel IS NOT INITIAL.
    RAISE ENTITY EVENT zr_travel~travel_created
      FROM VALUE #( FOR travel IN create-travel
        ( %key = travel-%key
          %param = VALUE #(
            travel_id = travel-travel_id ) ) ).
  ENDIF.
ENDMETHOD.
```

## Event Processing Flow

```
1. User action triggers RAP operation
2. Handler method executes business logic
3. RAISE ENTITY EVENT queues the event
4. RAP framework commits the transaction
5. After successful COMMIT:
   a. Local event handlers are called
   b. Enterprise events are published to Event Mesh
```

## Enterprise Event Enablement

### Event Binding

To publish RAP events externally, create an event binding:

```
ADT: New → Other → Event Binding
Name: Z_EVT_BIND_TRAVEL
```

Event binding maps RAP events to enterprise event topics:

| Property            | Value                            |
| ------------------- | -------------------------------- |
| **Namespace**       | `sap.s4.beh` or custom namespace |
| **Business Object** | `ZR_Travel`                      |
| **Event**           | `travel_created`                 |
| **Topic**           | `sap/s4/beh/travel/created/v1`   |

### Event Topic Structure

```
<namespace>/<business-object>/<event-name>/<version>
Example: z.custom/travel/created/v1
```

### Channel Binding for SAP Event Mesh

1. Create a **Communication Arrangement** for scenario `SAP_COM_0092` (Enterprise Event Enablement)
2. Configure the Event Mesh service instance in BTP
3. Maintain the channel in the **Enterprise Event Enablement** Fiori app
4. Activate the event topic

## Consuming Events

### Local Event Consumption (Same System)

Register an event handler class:

```abap
CLASS zcl_travel_event_handler DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    "Event handler method
    METHODS on_travel_created
      FOR ENTITY EVENT
      travel_created FOR Travel~travel_created.
ENDCLASS.

CLASS zcl_travel_event_handler IMPLEMENTATION.
  METHOD on_travel_created.
    "React to travel creation
    LOOP AT travel_created INTO DATA(ls_event).
      "Process event data
      DATA(lv_travel_id) = ls_event-travel_id.
      "e.g., send notification, update related records
    ENDLOOP.
  ENDMETHOD.
ENDCLASS.
```

### External Event Consumption (via Event Mesh)

External systems subscribe to topics via:

- SAP Event Mesh webhooks
- SAP Integration Suite
- Custom applications using AMQP or REST APIs

### Consuming Events from External Systems in ABAP

```abap
"Using the event consumption model
"1. Create event consumption model in ADT
"   (imports AsyncAPI spec or defines events manually)

"2. Implement the event handler
CLASS zcl_ext_event_handler DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_event_handler.
ENDCLASS.

CLASS zcl_ext_event_handler IMPLEMENTATION.
  METHOD if_event_handler~handle.
    "Parse event payload
    DATA(lv_payload) = io_event->get_text( ).
    "Process the event
  ENDMETHOD.
ENDCLASS.
```

## Event Patterns

### Fire and Forget

```
Producer raises event → Event Mesh delivers → Consumer processes independently
```

- No response expected
- Loose coupling between systems
- Best for notifications, audit logging, data replication triggers

### Event-Carried State Transfer

Include full entity data in event payload so consumers don't need to call back:

```abap
RAISE ENTITY EVENT zr_travel~travel_created
  FROM VALUE #( ( %key = ls_travel-%key
                  %param = CORRESPONDING #( ls_travel ) ) ).
```

### Event Sourcing

Record every state change as an event for full audit trail.

## Best Practices

1. **Define events for business-meaningful state changes**, not technical operations
2. **Include sufficient data in event parameters** to avoid consumer callbacks
3. **Use CDS abstract entities** for event parameter types (clear contract)
4. **Raise events after validation** — only raise when the operation will succeed
5. **Handle event processing failures** — consumers should be idempotent
6. **Use meaningful topic naming** following SAP conventions
7. **Version event topics** for backward compatibility (`/v1`, `/v2`)

## Output Format

When helping with eventing topics, structure responses as:

```markdown
## RAP Business Event Guidance

### Scenario

- Type: [Local event / Enterprise event]
- Role: [Producer / Consumer]

### Implementation

[Event definition, raising, and consumption code]

### Configuration

[Event binding and communication arrangement setup]
```

## References

- RAP Business Events Cheat Sheet: https://github.com/SAP-samples/abap-cheat-sheets/blob/main/08_RAP_Business_Events.md
- Enterprise Event Enablement: https://help.sap.com/docs/abap-cloud/abap-rap/enterprise-event-enablement
- SAP Event Mesh: https://help.sap.com/docs/event-mesh

## Related Skills

- **rap**: Use for building RAP business objects that can raise events
- **btp-abap-environment**: Use for setting up Event Mesh integration via communication arrangements
- **authorization-iam**: Use for securing event handling and access control
