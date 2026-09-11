---
name: generate-rap-logic
description: Generate RAP determinations, validations, and custom action implementations for an existing behavior definition by reading the RAP stack and filling empty method stubs in the behavior pool. Use when asked to "implement RAP determinations", "fill in behavior pool methods", "add RAP validation logic", or "generate custom action code".
---

# Generate RAP Business Logic

Generate RAP determination, validation, and custom action implementations for an existing behavior definition. Reads the RAP stack, identifies empty method stubs (or missing handler signatures) in the behavior pool, and generates ABAP Cloud implementation code.

This skill replicates SAP Joule's "RAP Logic Prediction" capability by combining ARC-1 (SAP system access) with mcp-sap-docs (documentation & best practices).

## Smart Defaults (apply silently, do NOT ask)

| Setting | Default | Rationale |
|---|---|---|
| Entity access | `IN LOCAL MODE` always | Inside behavior pool, no auth check needed |
| Message style | Hardcoded text via `new_message_with_text()` | Simplest for prototyping; use MSAG for production (see Notes) |
| Scope | All empty methods | User can narrow after seeing the list |
| Error handling | `FAILED` + `REPORTED` structures | Standard RAP error propagation |

## Input

The user provides a behavior definition name (e.g., `ZI_TRAVEL`).

Only the **behavior definition name** is required. If the user provides just a BDEF name, apply Smart Defaults and proceed to read the stack and present available methods.

Optionally, the user may specify:
- **Specific determination/validation** (default: list all and let user choose)
- **Behavior description** — natural language description of desired logic (e.g., "calculate total price from line items", "validate status transitions")

## Step 1: Read the RAP Stack

Read the behavior definition, CDS view, and behavior pool to understand the complete RAP context.

### 1a. Read the behavior definition

```
SAPRead(type="BDEF", name="<bdef_name>")
```

⚠️ **FAIL-FAST GATE**: If the BDEF read fails with 404, the object may not exist — verify the name via `SAPSearch`. If it fails with 415, check `SAPManage(action="probe")` for system info and inform the user about the issue.

Parse the BDEF source to identify:
- **Scenario**: managed / unmanaged / abstract
- **Determinations**: `determination <Name> on (modify|save) { ... }`
- **Validations**: `validation <Name> on save { ... }`
- **Actions**: `action <Name> ...`
- **Draft status**: `with draft` present or not
- **Entity aliases**: `alias <Alias>`
- **Persistent table**: `persistent table <table_name>`
- **Behavior pool class**: `implementation in class <class_name> unique`

### 1b. Read the interface CDS view

```
SAPRead(type="DDLS", name="<interface_view>")
```

Understand the data model: field names, types, aliases, associations. This is needed to generate correct `READ ENTITIES` and `MODIFY ENTITIES` statements.

If access control exists, also read it to understand CDS-level authorization constraints:

```
SAPRead(type="DCLS", name="<interface_view>_DCL")
```

### 1c. Get dependency context

```
SAPContext(type="DDLS", name="<interface_view>", action="deps")
```

Understand underlying tables, associations, and related entities. Useful for cross-entity validations or determinations that read associated data.

### 1d. Read the behavior pool class

Find the behavior pool class name from the BDEF source (`implementation in class <name>`), then:

```
SAPRead(type="CLAS", name="<bp_class>", format="structured")
```

Use the structured read as the default because it returns metadata, includes, and existing test classes in one response. If you need a concise method catalog afterward, add:

```
SAPRead(type="CLAS", name="<bp_class>", method="*")
```

Identify which methods are empty stubs (body is just comments, `RETURN`, or blank) and which BDEF-declared handlers are missing entirely from the class signature.

### 1e. Optional history / documentation context

If this is an existing RAP BO that has already been modified by others, inspect recent changes and any attached documentation before overwriting logic:

```
SAPRead(type="VERSIONS", name="<bp_class>", objectType="CLAS")
SAPRead(type="SKTD", name="<bp_class>")
```

## Step 2: Identify Target Methods

Parse the BDEF for determination and validation declarations. Present a summary table:

```
Methods in behavior pool ZBP_I_TRAVEL:

| # | Type          | Name                  | Trigger            | Fields          | Status      |
|---|---------------|-----------------------|--------------------|-----------------|-------------|
| 1 | Determination | calculateTotalPrice   | on modify          | Price, Quantity | empty       |
| 2 | Determination | setDefaultStatus      | on modify          | %create         | empty       |
| 3 | Validation    | validateStatus        | on save            | Status          | implemented |
| 4 | Validation    | validateDates         | on save            | BeginDate       | empty       |
| 5 | Validation    | validateCustomer      | on save            | CustomerID      | empty       |
```

Ask the user: **"Which methods should I implement? (all empty / specific numbers / skip any?)"**

If the user provided a natural language description, map it to the appropriate method(s).

### 2b. Missing Handler Signature Recovery

If the BDEF declares action/determination/validation handlers that do not exist in the class definition:

1. Run `SAPWrite(action="scaffold_rap_handlers", type="CLAS", name="<bp_class>", bdefName="<bdef_name>")` to list missing signatures.
2. If signatures are missing, rerun with `autoApply=true` to inject declarations plus empty method stubs into class sections when possible.
3. If unresolved, try MCP quick-fix flow:
   - `SAPDiagnose(action="quickfix", ...)`
   - `SAPDiagnose(action="apply_quickfix", ...)`
4. If still unresolved, use ADT quick-fix to generate the missing `METHODS ... FOR ...` signature.
5. Re-read method list with `SAPRead(type="CLAS", name="<bp_class>", method="*")` before writing bodies.

## Step 3: Research RAP Patterns

Use mcp-sap-docs to fetch current RAP implementation patterns. Start with reference-style queries (`includeSamples=false`) and then fetch examples (`includeSamples=true`) only when you need executable patterns:

```
search(query="RAP validation implementation ABAP example", includeSamples=true, abapFlavor="<cloud|standard>")
```

```
search(query="RAP determination on save trigger", includeSamples=false, abapFlavor="<cloud|standard>")
```

For specific logic patterns:
```
search(query="RAP calculate total price determination", includeSamples=true, abapFlavor="<cloud|standard>")
```

```
search(query="RAP status validation transition", includeSamples=true, abapFlavor="<cloud|standard>")
```

For backend-driven UI behavior that frequently accompanies logic changes:

```
search(query="RAP feature control side effects authorization control", includeSamples=false, abapFlavor="<cloud|standard>")
```

Use documentation to inform correct ABAP Cloud patterns:
- `READ ENTITIES OF <entity> IN LOCAL MODE` for reading entity data
- `MODIFY ENTITIES OF <entity> IN LOCAL MODE` for updating entity data
- Proper `FAILED` / `REPORTED` structure handling
- Correct method signatures for determinations vs validations
- Feature control checks are **not** evaluated for EML with `IN LOCAL MODE`

## Step 4: Generate Method Implementation

For each selected method, generate ABAP Cloud implementation code.

### Determination Template

```abap
METHOD <determination_name>.
  " Read relevant fields of all affected entities
  READ ENTITIES OF <interface_view> IN LOCAL MODE
    ENTITY <alias>
      FIELDS ( <trigger_fields> )
      WITH CORRESPONDING #( keys )
    RESULT DATA(lt_entities).

  " Calculate derived values
  LOOP AT lt_entities ASSIGNING FIELD-SYMBOL(<entity>).
    " --- Business logic here ---
    " Example: <entity>-TotalPrice = <entity>-Price * <entity>-Quantity.
  ENDLOOP.

  " Write back modified fields
  MODIFY ENTITIES OF <interface_view> IN LOCAL MODE
    ENTITY <alias>
      UPDATE FIELDS ( <modified_fields> )
      WITH VALUE #( FOR entity IN lt_entities
        ( %tky = entity-%tky
          <field> = entity-<field> ) )
    REPORTED DATA(lt_update_reported).

  reported = CORRESPONDING #( DEEP lt_update_reported ).
ENDMETHOD.
```

### Validation Template

```abap
METHOD <validation_name>.
  " Read relevant fields of all affected entities
  READ ENTITIES OF <interface_view> IN LOCAL MODE
    ENTITY <alias>
      FIELDS ( <validated_fields> )
      WITH CORRESPONDING #( keys )
    RESULT DATA(lt_entities).

  LOOP AT lt_entities ASSIGNING FIELD-SYMBOL(<entity>).
    " --- Validation logic here ---
    " Example: check field is not initial
    IF <entity>-<Field> IS INITIAL.
      APPEND VALUE #( %tky = <entity>-%tky ) TO failed-<alias>.
      APPEND VALUE #(
        %tky     = <entity>-%tky
        %msg     = new_message_with_text(
                     severity = if_abap_behv_message=>severity-error
                     text     = '<Error message>' )
        %element-<Field> = if_abap_behv=>mk-on
      ) TO reported-<alias>.
    ENDIF.
  ENDLOOP.
ENDMETHOD.
```

### Action Template

```abap
METHOD <action_name>.
  READ ENTITIES OF <interface_view> IN LOCAL MODE
    ENTITY <alias>
      FIELDS ( <action_input_fields> )
      WITH CORRESPONDING #( keys )
    RESULT DATA(lt_entities).

  LOOP AT lt_entities ASSIGNING FIELD-SYMBOL(<entity>).
    " --- Action logic here ---
  ENDLOOP.

  MODIFY ENTITIES OF <interface_view> IN LOCAL MODE
    ENTITY <alias>
      UPDATE FIELDS ( <action_output_fields> )
      WITH VALUE #( FOR entity IN lt_entities
        ( %tky = entity-%tky
          <field> = entity-<field> ) )
    REPORTED DATA(lt_reported)
    FAILED DATA(lt_failed).

  reported = CORRESPONDING #( DEEP lt_reported ).
  failed   = CORRESPONDING #( DEEP lt_failed ).
ENDMETHOD.
```

### Output to User

Show the generated code for each method and ask:

**"Here's the generated implementation. Should I write it to the SAP system? (yes / edit first / cancel)"**

If the user wants edits, incorporate them before proceeding.

## Step 5: Write and Validate

Before writing, optionally lint-check the generated code to catch issues before acquiring SAP locks:

```
SAPLint(action="lint", source="<generated_method_code>", name="<bp_class>")
```

If you want the generated method body to follow SAP's formatter settings before it is written back:

```
SAPLint(action="format", source="<generated_method_code>", name="<bp_class>")
```

Before calling `edit_method`, confirm the target method exists in `SAPRead(..., method="*")`. If it does not exist yet, run `scaffold_rap_handlers` first, then quick-fix flow (`quickfix` + `apply_quickfix`) or ADT quick-fix fallback.

Write each method implementation using method-level surgery:

```
SAPWrite(action="edit_method", type="CLAS", name="<bp_class>", method="<method_name>", source="<generated_code>", transport="<transport>")
```

**Note:** The `transport` parameter is recommended but not always required for edit_method. ARC-1 auto-propagates the lock-provided `corrNr` when no explicit transport is supplied. Pre-write lint validation runs automatically when enabled (default: on). Prefer `edit_method` over full-class rewrites for behavior pools.

After writing all methods, run a syntax check:

```
SAPDiagnose(action="syntax", type="CLAS", name="<bp_class>")
```

If syntax errors occur, try SAP quickfix proposals first before manual edits:

```
SAPDiagnose(action="quickfix", type="CLAS", name="<bp_class>", source="<current_source>", line=<error_line>, column=<error_col>)
```

SAP quickfixes can automatically resolve common issues like missing declarations or straightforward syntax corrections.

If syntax errors occur:
1. Read the error message carefully
2. Common issues: wrong entity name in `READ ENTITIES`, incorrect field alias, missing `IN LOCAL MODE`
3. Fix the method and re-write
4. Re-check syntax

## Step 6: Activate and Verify

Activate the behavior pool and behavior definition together:

```
SAPActivate(objects=[{type:"BDEF", name:"<bdef>"}, {type:"CLAS", name:"<bp_class>"}])
```

**Note:** Activation returns structured responses with detailed error/warning messages including line numbers and URIs. Use this to pinpoint exact issues rather than re-reading full source.

Optionally, if a test class exists, run the unit tests:

```
SAPDiagnose(action="unittest", type="CLAS", name="<bp_class>")
```

If ATC is available and the change is non-trivial, run it too:

```
SAPDiagnose(action="atc", type="CLAS", name="<bp_class>")
```

Present a summary:

```
RAP Logic Generation Complete!

Implemented methods:
  [x] Determination: calculateTotalPrice — calculates total from price * quantity
  [x] Determination: setDefaultStatus — sets status to 'N' (New) on create
  [x] Validation: validateDates — ensures begin_date < end_date
  [x] Validation: validateCustomer — checks customer_id is not empty
  [ ] Validation: validateStatus — already implemented, skipped

Next steps:
  - Test the logic via the Fiori Elements preview
  - Add unit tests (use generate-abap-unit-test skill)
  - Add more validations/determinations to the BDEF as needed
```

## Common RAP Logic Patterns

### Field Calculation Determination

Calculate a derived field from other fields (e.g., total price = price * quantity):

```abap
METHOD calculateTotalPrice.
  READ ENTITIES OF zi_order IN LOCAL MODE
    ENTITY Order
      FIELDS ( Price Quantity )
      WITH CORRESPONDING #( keys )
    RESULT DATA(lt_orders).

  LOOP AT lt_orders ASSIGNING FIELD-SYMBOL(<order>).
    <order>-TotalPrice = <order>-Price * <order>-Quantity.
  ENDLOOP.

  MODIFY ENTITIES OF zi_order IN LOCAL MODE
    ENTITY Order
      UPDATE FIELDS ( TotalPrice )
      WITH VALUE #( FOR order IN lt_orders
        ( %tky = order-%tky
          TotalPrice = order-TotalPrice ) )
    REPORTED DATA(lt_reported).

  reported = CORRESPONDING #( DEEP lt_reported ).
ENDMETHOD.
```

### Default Value Determination

Set default values when an entity is created:

```abap
METHOD setDefaultStatus.
  READ ENTITIES OF zi_travel IN LOCAL MODE
    ENTITY Travel
      FIELDS ( Status )
      WITH CORRESPONDING #( keys )
    RESULT DATA(lt_travels).

  MODIFY ENTITIES OF zi_travel IN LOCAL MODE
    ENTITY Travel
      UPDATE FIELDS ( Status )
      WITH VALUE #( FOR travel IN lt_travels
                    WHERE ( Status IS INITIAL )
        ( %tky = travel-%tky
          Status = 'N' ) )
    REPORTED DATA(lt_reported).

  reported = CORRESPONDING #( DEEP lt_reported ).
ENDMETHOD.
```

### Mandatory Field Validation

Check that a required field is not empty:

```abap
METHOD validateCustomer.
  READ ENTITIES OF zi_travel IN LOCAL MODE
    ENTITY Travel
      FIELDS ( CustomerID )
      WITH CORRESPONDING #( keys )
    RESULT DATA(lt_travels).

  LOOP AT lt_travels ASSIGNING FIELD-SYMBOL(<travel>).
    IF <travel>-CustomerID IS INITIAL.
      APPEND VALUE #( %tky = <travel>-%tky ) TO failed-travel.
      APPEND VALUE #(
        %tky     = <travel>-%tky
        %msg     = new_message_with_text(
                     severity = if_abap_behv_message=>severity-error
                     text     = 'Customer must be specified' )
        %element-CustomerID = if_abap_behv=>mk-on
      ) TO reported-travel.
    ENDIF.
  ENDLOOP.
ENDMETHOD.
```

### Cross-Field Validation

Validate that related fields are consistent (e.g., begin date before end date):

```abap
METHOD validateDates.
  READ ENTITIES OF zi_travel IN LOCAL MODE
    ENTITY Travel
      FIELDS ( BeginDate EndDate )
      WITH CORRESPONDING #( keys )
    RESULT DATA(lt_travels).

  LOOP AT lt_travels ASSIGNING FIELD-SYMBOL(<travel>).
    IF <travel>-BeginDate IS NOT INITIAL
   AND <travel>-EndDate IS NOT INITIAL
   AND <travel>-BeginDate > <travel>-EndDate.
      APPEND VALUE #( %tky = <travel>-%tky ) TO failed-travel.
      APPEND VALUE #(
        %tky     = <travel>-%tky
        %msg     = new_message_with_text(
                     severity = if_abap_behv_message=>severity-error
                     text     = 'Begin date must be before end date' )
        %element-BeginDate = if_abap_behv=>mk-on
        %element-EndDate   = if_abap_behv=>mk-on
      ) TO reported-travel.
    ENDIF.
  ENDLOOP.
ENDMETHOD.
```

### Status Transition Validation

Validate that status changes follow allowed transitions:

```abap
METHOD validateStatus.
  READ ENTITIES OF zi_travel IN LOCAL MODE
    ENTITY Travel
      FIELDS ( Status )
      WITH CORRESPONDING #( keys )
    RESULT DATA(lt_travels).

  LOOP AT lt_travels ASSIGNING FIELD-SYMBOL(<travel>).
    CASE <travel>-Status.
      WHEN 'N' OR 'O' OR 'A' OR 'X'.
        " Valid statuses: New, Open, Accepted, Cancelled
      WHEN OTHERS.
        APPEND VALUE #( %tky = <travel>-%tky ) TO failed-travel.
        APPEND VALUE #(
          %tky     = <travel>-%tky
          %msg     = new_message_with_text(
                       severity = if_abap_behv_message=>severity-error
                       text     = |Invalid status: { <travel>-Status }| )
          %element-Status = if_abap_behv=>mk-on
        ) TO reported-travel.
    ENDCASE.
  ENDLOOP.
ENDMETHOD.
```

### Number Range Determination

Assign sequential numbers for non-UUID key scenarios:

```abap
METHOD setTravelID.
  READ ENTITIES OF zi_travel IN LOCAL MODE
    ENTITY Travel
      FIELDS ( TravelID )
      WITH CORRESPONDING #( keys )
    RESULT DATA(lt_travels).

  " Get next number from number range or max+1
  SELECT MAX( travel_id ) FROM ztravel_d INTO @DATA(lv_max_id).
  DATA(lv_next_id) = lv_max_id + 1.

  LOOP AT lt_travels ASSIGNING FIELD-SYMBOL(<travel>)
    WHERE TravelID IS INITIAL.
    <travel>-TravelID = lv_next_id.
    lv_next_id += 1.
  ENDLOOP.

  MODIFY ENTITIES OF zi_travel IN LOCAL MODE
    ENTITY Travel
      UPDATE FIELDS ( TravelID )
      WITH VALUE #( FOR travel IN lt_travels
                    WHERE ( TravelID IS NOT INITIAL )
        ( %tky = travel-%tky
          TravelID = travel-TravelID ) )
    REPORTED DATA(lt_reported).

  reported = CORRESPONDING #( DEEP lt_reported ).
ENDMETHOD.
```

## Error Handling

### Common Issues and Fixes

| Error | Cause | Fix |
|---|---|---|
| 415 Unsupported Media Type on DDLS/BDEF | RAP/CDS endpoint not responding as expected | Check `SAPManage(action="probe")` for system info. Verify ICF service activation. Try creating the object in ADT to confirm system capability. |
| Method not found in behavior pool | Class name in BDEF doesn't match actual class | Check `implementation in class` in BDEF source, verify class exists |
| Missing `METHODS ... FOR ...` handler signature | BDEF declaration exists but class signature not generated yet | Run `SAPWrite(action="scaffold_rap_handlers", ...)` first (optionally `autoApply=true`), then `SAPDiagnose(action="quickfix")` + `apply_quickfix` or ADT quick-fix, then retry `edit_method` |
| Syntax error: `<entity>` unknown in `READ ENTITIES` | Wrong entity name or alias | Use the exact alias from the BDEF `define behavior for ... alias <Alias>` |
| Syntax error: field `<Field>` unknown | Field alias doesn't match CDS view | Check CDS view field aliases — BDEF uses CDS aliases, not table field names |
| Activation fails | BDEF and class are incompatible | Activate BDEF and class together: `SAPActivate(objects=[...])` |
| `FAILED` / `REPORTED` structure mismatch | Wrong alias used in `failed-<alias>` or `reported-<alias>` | Use the lowercase entity alias from BDEF (e.g., `failed-travel`, not `failed-Travel`) |
| `IN LOCAL MODE` missing | Missing clause causes authorization check | Always use `IN LOCAL MODE` for internal reads/writes within the behavior pool |
| `%tky` not available | Method signature doesn't provide transactional key | Check method signature — determinations use `keys`, validations use `keys` |
| Runtime error on `MODIFY ENTITIES` | Trying to modify read-only fields | Don't modify fields marked `field ( readonly )` in BDEF |
| Generic save error `[?/011]` on full class write | Behavior-pool full-class update path is unstable on some systems | Use `scaffold_rap_handlers` + quickfix path for signatures, then patch method bodies via `edit_method` only |

## Notes

### BTP vs On-Prem Differences

- **BTP**: ABAP Cloud syntax strictly enforced. Only `READ ENTITIES` / `MODIFY ENTITIES` — no `SELECT` from database tables directly. All APIs must be released. `strict ( 2 )` in BDEF.
- **On-Prem**: More flexible — classic ABAP can be used in the behavior pool (e.g., `SELECT` directly), but `READ ENTITIES` / `MODIFY ENTITIES` is strongly recommended for consistency and future compatibility.
- **Authorization layering**: `DCLS` enforces CDS row-level access, while BDEF authorization (`authorization master`) governs behavior operations. Consider both when debugging authorization-related logic.

### What This Skill Does NOT Do

- **Automatic BDEF declaration authoring**: This skill assumes declarations exist in BDEF; it does not redesign BDEF contracts for you.
- **Side effects**: No end-to-end `side effects` implementation (UI refresh triggers). Add manually if needed.
- **Feature control**: No end-to-end dynamic feature control (`instance_features` / `global_features`). Add manually, especially when the UI should disable actions or updates.
- **Authorization**: No `authorization master` implementation. Add authorization checks manually.
- **Cross-BO logic**: No inter-business-object operations. Each determination/validation operates within its own BO.
- **Message class creation**: Uses hardcoded text for messages. For production services, create a message class afterward: `SAPWrite(action="create", type="MSAG", name="Z<MSG_CLASS>", ...)` and replace `new_message_with_text()` with `new_message()` referencing the message class.

### When to Use This Skill

- After creating a RAP service (use generate-rap-service first)
- When the BDEF has determination/validation declarations but empty method stubs
- When adding new business logic to an existing RAP service
- When the user describes desired behavior in natural language (e.g., "validate that the end date is after the begin date")
- NOT for creating the RAP service from scratch (use generate-rap-service)
- NOT for CDS unit tests (use generate-cds-unit-test or generate-abap-unit-test)
