---
name: rap
description: Help with RAP (RESTful ABAP Programming Model) development including behavior definitions, EML statements, managed and unmanaged BOs, draft handling, actions, validations, determinations, side effects, and business events. Use when users ask about RAP, BDEF, BDL, EML, behavior definitions, behavior pools, managed BO, unmanaged BO, draft-enabled BO, RAP actions, RAP validations, RAP determinations, RAP side effects, RAP business events, create/read/update/delete in RAP, or building transactional Fiori apps with ABAP Cloud. Triggers include "create a RAP BO", "write a behavior definition", "EML syntax", "managed vs unmanaged", "enable draft", "add an action", "add a validation", "RAP handler method", or "RAP saver class".
---

# RAP (RESTful ABAP Programming Model)

Guide for building transactional applications using the ABAP RESTful Application Programming Model (RAP) in ABAP Cloud.

> **Clean core context**: RAP is the leading programming model for ABAP Cloud development, which is **clean core Level A**. A custom RAP-based Fiori app for the core SAP Cloud ERP scope is Level A; extending a RAP-based SAP Fiori app via released extension points is also Level A. By contrast, SEGW/BOPF/UI5-based apps and their extensions are Level B. Keep RAP handler code restricted to released APIs to stay at Level A — a single internal object call demotes the whole application to Level C. See the `abap-cloud` skill for level details.

## Workflow

1. **Determine the user's goal**:
   - Creating a new RAP BO from scratch
   - Adding behavior (actions, validations, determinations) to an existing BO
   - Writing EML statements to consume a RAP BO
   - Troubleshooting RAP-related issues
   - Understanding RAP concepts

2. **Identify the scenario**:
   - Managed (greenfield) vs. unmanaged (brownfield)
   - Draft-enabled or not
   - Numbering concept: early/late, internal/external/managed
   - Single entity or composition tree (root + children)

3. **Guide implementation** following the RAP layered architecture:
   - Data modeling (database tables → CDS view entities)
   - Behavior definition (BDEF using BDL)
   - Behavior implementation (ABAP behavior pool)
   - Business service exposure (service definition → service binding)

4. **Provide code examples** using correct BDL and EML syntax

## RAP Architecture Layers

| Layer                       | Artifacts                                     | Purpose                                                                 |
| --------------------------- | --------------------------------------------- | ----------------------------------------------------------------------- |
| **Data Modeling**           | Database tables, CDS root/child view entities | Data persistence and semantic data model                                |
| **Behavior Definition**     | BDEF (`.bdef`)                                | Declares transactional behavior (operations, characteristics) using BDL |
| **Behavior Implementation** | ABAP behavior pool (`BP_*`)                   | Implements business logic in handler/saver classes                      |
| **Projection**              | CDS projection views, projection BDEF         | Adapts BO for specific service consumers                                |
| **Business Service**        | Service definition, service binding           | Exposes BO as OData service                                             |

## Implementation Types

### Managed (Greenfield)

- Framework handles transactional buffer and standard CRUD operations automatically
- Only need custom code for non-standard operations (actions, validations, determinations)
- Automatic save handling (can be enhanced with `additional save` or replaced with `unmanaged save`)

```
managed implementation in class zbp_r_entity unique;
strict ( 2 );
```

### Unmanaged (Brownfield)

- Developer provides transactional buffer and implements all operations
- Used when existing business logic needs to be embedded in RAP

```
unmanaged implementation in class zbp_r_entity unique;
strict ( 2 );
```

## Behavior Definition (BDL) Quick Reference

### Complete BDEF Structure

```
managed implementation in class zbp_r_root unique;
strict ( 2 );
with draft;

define behavior for ZR_Root alias Root
persistent table zroot_tab
draft table zroot_d
etag master LocalLastChangedAt
lock master
total etag LastChangedAt
authorization master ( global )
late numbering
{
  // Field characteristics
  field ( readonly ) RootUUID, CreatedBy, CreatedAt, LastChangedBy, LastChangedAt;
  field ( mandatory ) Description;
  field ( numbering : managed ) RootUUID;

  // Standard operations
  create;
  update;
  delete;

  // Association to child entity
  association _Child { create; }

  // Actions
  action doSomething result [1] $self;
  static action createFromTemplate parameter ZD_CreateParam result [1] $self;
  internal action recalculate;

  // Validations
  validation validateDescription on save { create; field Description; }

  // Determinations
  determination setDefaults on modify { create; }
  determination calcTotal on modify { field Quantity, Price; }

  // Draft actions
  draft action Resume;
  draft action Edit;
  draft action Activate optimized;
  draft action Discard;
  draft determine action Prepare
  {
    validation validateDescription;
  }

  // Side effects
  side effects
  {
    field Quantity affects field TotalAmount;
    field Price affects field TotalAmount;
    determine action Prepare executed on field Description affects messages;
  }

  // Events
  event created;
  event deleted parameter ZD_DeletedEvent;

  // Mapping
  mapping for zroot_tab corresponding
  {
    RootUUID = root_uuid;
    Description = description;
  }
}

define behavior for ZR_Child alias Child
persistent table zchild_tab
draft table zchild_d
etag master LocalLastChangedAt
lock dependent by _Root
authorization dependent by _Root
{
  field ( readonly ) ChildUUID, RootUUID;
  field ( numbering : managed ) ChildUUID;

  update;
  delete;

  association _Root;

  mapping for zchild_tab corresponding
  {
    ChildUUID = child_uuid;
    RootUUID = root_uuid;
  }
}
```

### Projection BDEF

```
projection;
strict ( 2 );
use draft;

define behavior for ZC_Root alias Root
{
  use create;
  use update;
  use delete;

  use action doSomething;

  use association _Child { create; }
}

define behavior for ZC_Child alias Child
{
  use update;
  use delete;

  use association _Root;
}
```

### Key BDL Elements

| Element                 | Syntax                                    | Purpose                                                                |
| ----------------------- | ----------------------------------------- | ---------------------------------------------------------------------- |
| **Managed numbering**   | `field ( numbering : managed ) KeyField;` | Framework assigns UUID keys automatically                              |
| **Early numbering**     | `early numbering`                         | Custom key assignment in interaction phase via `FOR NUMBERING` handler |
| **Late numbering**      | `late numbering`                          | Key assignment in save sequence via `adjust_numbers` saver method      |
| **Lock master**         | `lock master`                             | Root entity controls pessimistic locking                               |
| **Lock dependent**      | `lock dependent by _Assoc`                | Child entity delegates locking to parent                               |
| **ETag**                | `etag master FieldName`                   | Optimistic concurrency control                                         |
| **Total ETag**          | `total etag FieldName`                    | Required for draft-enabled BOs                                         |
| **Draft**               | `with draft;`                             | Enables draft handling for entire BO                                   |
| **Collaborative draft** | `with collaborative draft;`               | Multi-user draft editing                                               |
| **Strict mode**         | `strict ( 2 );`                           | Enables additional BDL syntax checks (use latest version)              |

## ABAP Behavior Pool (ABP)

### Handler Class

```abap
CLASS lhc_root DEFINITION INHERITING FROM cl_abap_behavior_handler.
  PRIVATE SECTION.

    " Standard operations (unmanaged only)
    METHODS create FOR MODIFY
      IMPORTING entities FOR CREATE Root.

    " Action implementation
    METHODS doSomething FOR MODIFY
      IMPORTING keys FOR ACTION Root~doSomething RESULT result.

    " Validation
    METHODS validateDescription FOR VALIDATE ON SAVE
      IMPORTING keys FOR Root~validateDescription.

    " Determination
    METHODS setDefaults FOR DETERMINE ON MODIFY
      IMPORTING keys FOR Root~setDefaults.

    " Instance feature control
    METHODS get_instance_features FOR INSTANCE FEATURES
      IMPORTING keys REQUEST requested_features FOR Root RESULT result.

    " Instance authorization
    METHODS get_instance_authorizations FOR INSTANCE AUTHORIZATION
      IMPORTING keys REQUEST requested_authorizations FOR Root RESULT result.

ENDCLASS.

CLASS lhc_root IMPLEMENTATION.

  METHOD doSomething.
    " Read current instance data
    READ ENTITIES OF zr_root IN LOCAL MODE
      ENTITY Root
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(entities)
      FAILED failed.

    " Modify instances
    MODIFY ENTITIES OF zr_root IN LOCAL MODE
      ENTITY Root
      UPDATE FIELDS ( Status )
      WITH VALUE #( FOR entity IN entities
        ( %tky = entity-%tky
          Status = 'DONE'
          %control-Status = if_abap_behv=>mk-on ) )
      FAILED failed
      REPORTED reported.

    " Fill result
    result = VALUE #( FOR entity IN entities
      ( %tky = entity-%tky
        %param = entity ) ).
  ENDMETHOD.

  METHOD validateDescription.
    READ ENTITIES OF zr_root IN LOCAL MODE
      ENTITY Root
      FIELDS ( Description ) WITH CORRESPONDING #( keys )
      RESULT DATA(entities).

    LOOP AT entities INTO DATA(entity).
      IF entity-Description IS INITIAL.
        APPEND VALUE #( %tky = entity-%tky ) TO failed-root.
        APPEND VALUE #( %tky = entity-%tky
          %msg = new_message_with_text(
            severity = if_abap_behv_message=>severity-error
            text = 'Description must not be empty' )
          %element-Description = if_abap_behv=>mk-on
        ) TO reported-root.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  METHOD setDefaults.
    READ ENTITIES OF zr_root IN LOCAL MODE
      ENTITY Root
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(entities).

    MODIFY ENTITIES OF zr_root IN LOCAL MODE
      ENTITY Root
      UPDATE FIELDS ( Status CreatedAt )
      WITH VALUE #( FOR entity IN entities
        ( %tky = entity-%tky
          Status = 'NEW'
          %control-Status = if_abap_behv=>mk-on ) )
      REPORTED reported.
  ENDMETHOD.

ENDCLASS.
```

### Saver Class

```abap
CLASS lsc_root DEFINITION INHERITING FROM cl_abap_behavior_saver.
  PROTECTED SECTION.
    METHODS finalize REDEFINITION.
    METHODS check_before_save REDEFINITION.
    METHODS save_modified REDEFINITION.
    METHODS cleanup REDEFINITION.
    METHODS cleanup_finalize REDEFINITION.
ENDCLASS.

CLASS lsc_root IMPLEMENTATION.
  METHOD finalize.
    " Final calculations before save
  ENDMETHOD.

  METHOD check_before_save.
    " Final consistency checks
  ENDMETHOD.

  METHOD save_modified.
    " Only needed for 'with additional save' or 'with unmanaged save'
    " Raise business events here
    IF create-root IS NOT INITIAL.
      RAISE ENTITY EVENT zr_root~created
        FROM VALUE #( FOR <cr> IN create-root
          ( %key = VALUE #( RootUUID = <cr>-RootUUID ) ) ).
    ENDIF.
  ENDMETHOD.

  METHOD cleanup.
    " Clear transactional buffer
  ENDMETHOD.

  METHOD cleanup_finalize.
    " Rollback finalize changes on failure
  ENDMETHOD.
ENDCLASS.
```

## EML (Entity Manipulation Language) Quick Reference

EML is the ABAP language for programmatically interacting with RAP BOs. Key operations: `MODIFY ENTITY` (create/update/delete/execute action), `READ ENTITIES`, `COMMIT ENTITIES`, `ROLLBACK ENTITIES`.

- **Create**: `MODIFY ENTITY ... CREATE FIELDS ( ... ) WITH VALUE #( ( %cid = '...' ... ) )`
- **Read**: `READ ENTITIES OF ... ALL FIELDS WITH VALUE #( ( key = val ) ) RESULT DATA(result)`
- **Update**: `MODIFY ENTITY ... UPDATE FIELDS ( ... ) WITH VALUE #( ( %tky = ... ) )`
- **Delete**: `MODIFY ENTITY ... DELETE FROM VALUE #( ( %tky = ... ) )`
- **Execute Action**: `MODIFY ENTITY ... EXECUTE actionName FROM VALUE #( ( %tky = ... ) )`
- **Deep Create**: Use `CREATE BY \_Assoc` with `%cid_ref` and `%target`

> For full EML syntax with code examples, read [references/eml-quick-reference.md](references/eml-quick-reference.md).

## Draft Handling

- Enabled via `with draft;` in BDEF header
- Requires separate `draft table` for each entity
- Draft table must include `"%admin": include sych_bdl_draft_admin_inc;`
- Draft actions (`Edit`, `Activate`, `Discard`, `Resume`, `Prepare`) are implicitly provided
- Use `%is_draft` component (or `%tky` which includes it) to distinguish draft vs. active instances

## RAP Save Sequence

| Phase          | Methods Called                                                      | Purpose                  |
| -------------- | ------------------------------------------------------------------- | ------------------------ |
| **Early Save** | `finalize` → `check_before_save` → (on failure: `cleanup_finalize`) | Ensure data consistency  |
| **Late Save**  | `adjust_numbers` → `save` / `save_modified` → `cleanup`             | Persist data to database |

- Early save failures (sy-subrc = 4) return to interaction phase
- Late save is point of no return — either commit succeeds or runtime error

## Key BDEF Derived Type Components

| Component   | Purpose                                                             |
| ----------- | ------------------------------------------------------------------- |
| `%cid`      | Content ID — unique preliminary identifier for new instances        |
| `%cid_ref`  | Reference to a `%cid` in the same EML request                       |
| `%key`      | Primary key fields                                                  |
| `%tky`      | Transactional key (`%key` + `%is_draft` + `%pid`) — **recommended** |
| `%data`     | All key and data fields                                             |
| `%control`  | Flags indicating which fields are provided/requested                |
| `%is_draft` | Draft indicator (draft-enabled BOs only)                            |
| `%pid`      | Preliminary ID (late numbering only)                                |
| `%target`   | Target instances for create-by-association                          |
| `%param`    | Action/function parameter values                                    |

## Best Practices

- Always use `strict ( 2 );` for new BOs
- Prefer `%tky` over `%key` for future-proof code (handles draft/late numbering transitions)
- Always fill `%cid` in create operations even if not referenced later
- Use `IN LOCAL MODE` in handler methods to bypass feature controls and authorization checks
- Implement validations for data consistency checks, determinations for calculated fields
- Keep handler methods focused; use ABP auxiliary classes for shared logic
- For managed BOs, only implement handler methods for non-standard operations

## References

- [SAP ABAP Cheat Sheets — RAP BDL](https://github.com/SAP-samples/abap-cheat-sheets/blob/main/36_RAP_Behavior_Definition_Language.md)
- [SAP ABAP Cheat Sheets — EML](https://github.com/SAP-samples/abap-cheat-sheets/blob/main/08_EML_ABAP_for_RAP.md)
- [SAP Help — RAP Development Guide](https://help.sap.com/docs/abap-cloud/abap-rap/abap-restful-application-programming-model)
- [SAP Help — BDL Reference](https://help.sap.com/doc/abapdocu_cp_index_htm/CLOUD/en-US/ABENBDL.html)
- [ABAP Flight Reference Scenario](https://github.com/SAP-samples/abap-platform-refscen-flight)

## Clean Core Level Notes for RAP

| Scenario                                                        | Level | Notes                                                        |
| --------------------------------------------------------------- | ----- | ------------------------------------------------------------ |
| Custom RAP-based Fiori app for the core scope                   | **A** | Target state for new applications                            |
| Extension of a RAP-based SAP Fiori app via released extension points | **A** | Preferred extension approach                            |
| RAP BO consuming only released CDS views and released APIs      | **A** | Keep handler/saver code restricted to released APIs          |
| RAP BO consuming a classic API (`transactional-consistent`)     | **B** | Only classic APIs labelled `transactional-consistent` are safe inside RAP |
| RAP BO consuming an internal object or direct table read        | **C** | Wrap the object and create a single ATC exemption            |
| Custom SEGW / BOPF / UI5 app                                    | **B** | Prefer RAP; exceptions could be know-how or reuse            |
| Extension of an SEGW / BOPF / UI5 Fiori app                     | **B** | Migrate to the delivered RAP app when available              |
| `SE54`-based BC UI                                              | **B** | Prefer a RAP-based Business Configuration app                |

**Key rule**: a classic API may only be used inside a RAP application if it carries the `transactional-consistent` label in the Cloudification Repository. Other classic APIs may break RAP's transactional model.

## Related Skills

- **cds-view-entities**: Use for data modeling that forms the foundation of RAP business objects
- **abap-sql-amdp**: Use for implementing complex database operations in RAP
- **authorization-iam**: Use for implementing RAP authorization checks
- **odata**: Use for exposing RAP business objects as OData services
- **rap-business-events**: Use for implementing event-driven patterns in RAP
- **abap-cloud**: Use for clean core level classification and the wrapper pattern
- **badi-enhancement**: Use for implementing released RAP BAdIs to extend standard RAP BOs
