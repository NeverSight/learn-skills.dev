---
name: cds-view-entities
description: Help with CDS (Core Data Services) view entity development including data modeling, annotations, associations, compositions, access controls, aggregate expressions, built-in functions, and input parameters. Use when users ask about CDS views, CDS view entities, CDS annotations, CDS associations, CDS compositions, CDS access control, CDS metadata extensions, data modeling in ABAP, define view entity, define root view entity, semantic annotations, UI annotations, or building CDS data models for RAP or analytical scenarios. Triggers include "create a CDS view", "define view entity", "add an association", "CDS annotation", "access control", "composition", "CDS hierarchy", "CDS aggregate", "CDS functions", or "data model".
---

# CDS View Entities

Guide for building semantic data models using ABAP CDS (Core Data Services) view entities in ABAP Cloud.

> **Clean core context**: selecting from a **released** SAP CDS view (`I_*`) is **Level A**. Direct **read** access to an SAP database table is **Level C** (ATC priority 2); direct **write** access is **Level D** (ATC priority 1). Where no released CDS view exists, build a wrapper CDS view on top of the non-released SAP view or table and release it for ABAP Cloud — the wrapper is Level B if the wrapped object is a classic API, otherwise Level C. Use **CDS extends** and **CDS metadata extensions** rather than modifying SAP CDS views. See the `abap-cloud` skill for level details.

## Workflow

1. **Determine the user's goal**:
   - Creating a new data model (standalone or for RAP)
   - Defining relationships between entities (associations, compositions)
   - Adding annotations for UI, semantics, or analytics
   - Implementing access controls
   - Using expressions, functions, or parameters in CDS

2. **Identify the context**:
   - Standalone CDS view vs. RAP BO data model
   - Root entity vs. child entity vs. projection view
   - Transactional (RAP) vs. analytical vs. read-only consumption

3. **Apply best practices**:
   - Use CDS view entities (v2 syntax `define view entity`) — not legacy CDS views (`define view`)
   - Follow naming conventions (e.g., `ZR_*` for interface/BO views, `ZC_*` for consumption/projection views, `ZI_*` for reuse views)
   - Add appropriate annotations for metadata consumers (UI, OData, analytics)

## CDS View Entity Syntax

### Basic View Entity

```cds
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Sales Order'
define view entity ZI_SalesOrder
  as select from zsalesorder
{
  key order_id       as OrderId,
      customer_id    as CustomerId,
      order_date     as OrderDate,
      net_amount     as NetAmount,
      currency_code  as CurrencyCode,
      status         as Status,
      created_by     as CreatedBy,
      created_at     as CreatedAt,
      last_changed_at as LastChangedAt
}
```

### Root View Entity (for RAP)

```cds
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Sales Order Root'
define root view entity ZR_SalesOrder
  as select from zsalesorder
  composition [0..*] of ZR_SalesOrderItem as _Item
{
  key order_uuid         as OrderUUID,
      order_id           as OrderId,
      customer_id        as CustomerId,
      order_date         as OrderDate,
      @Semantics.amount.currencyCode: 'CurrencyCode'
      net_amount         as NetAmount,
      currency_code      as CurrencyCode,
      status             as Status,

      @Semantics.user.createdBy: true
      created_by         as CreatedBy,
      @Semantics.systemDateTime.createdAt: true
      created_at         as CreatedAt,
      @Semantics.user.localInstanceLastChangedBy: true
      last_changed_by    as LastChangedBy,
      @Semantics.systemDateTime.localInstanceLastChangedAt: true
      last_changed_at    as LastChangedAt,
      @Semantics.systemDateTime.lastChangedAt: true
      last_changed_at    as LastChangedAt,

      _Item
}
```

### Child View Entity

```cds
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Sales Order Item'
define view entity ZR_SalesOrderItem
  as select from zsalesorder_item
  association to parent ZR_SalesOrder as _Order
    on $projection.OrderUUID = _Order.OrderUUID
{
  key item_uuid       as ItemUUID,
      order_uuid      as OrderUUID,
      product_id      as ProductId,
      quantity         as Quantity,
      @Semantics.amount.currencyCode: 'CurrencyCode'
      unit_price       as UnitPrice,
      currency_code    as CurrencyCode,

      @Semantics.user.createdBy: true
      created_by       as CreatedBy,
      @Semantics.systemDateTime.localInstanceLastChangedAt: true
      last_changed_at  as LastChangedAt,

      _Order
}
```

### Projection View (Consumption Layer)

```cds
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Sales Order Projection'
@Metadata.allowExtensions: true
define view entity ZC_SalesOrder
  as projection on ZR_SalesOrder
{
  key OrderUUID,
      OrderId,
      CustomerId,
      OrderDate,
      NetAmount,
      CurrencyCode,
      Status,
      CreatedBy,
      CreatedAt,
      LastChangedBy,
      LastChangedAt,

      _Item : redirected to composition child ZC_SalesOrderItem
}
```

## Associations & Compositions

### Association Types

| Type                      | Syntax                                                  | Use Case                                              |
| ------------------------- | ------------------------------------------------------- | ----------------------------------------------------- |
| **Regular association**   | `association [0..1] to ZI_Customer as _Customer on ...` | Independent entities (e.g., master data lookup)       |
| **Composition**           | `composition [0..*] of ZR_Child as _Child`              | Parent-child with lifecycle dependency (RAP BO trees) |
| **To-parent association** | `association to parent ZR_Parent as _Parent on ...`     | Child → parent back-reference in compositions         |

### Association Syntax

```cds
define view entity ZI_SalesOrder
  as select from zsalesorder
  association [0..1] to ZI_Customer as _Customer
    on $projection.CustomerId = _Customer.CustomerId
  association [0..*] to ZI_SalesOrderItem as _Item
    on $projection.OrderId = _Item.OrderId
{
  key order_id    as OrderId,
      customer_id as CustomerId,

      // Expose associations — required for consumption via ABAP SQL or OData
      _Customer,
      _Item
}
```

### Using Associations in ABAP SQL

```abap
" Path expression — triggers LEFT OUTER JOIN by default
SELECT FROM zi_salesorder
  FIELDS OrderId,
         \_Customer-CustomerName,
         \_Item-ProductId
  WHERE OrderId = @lv_order_id
  INTO TABLE @DATA(lt_result).

" Filtering associations
SELECT FROM zi_salesorder
  FIELDS OrderId, \_Item[ ProductId = 'PROD01' ]-Quantity
  WHERE OrderId = @lv_order_id
  INTO TABLE @DATA(lt_filtered).
```

## Expressions & Built-in Functions

### Cast Expressions

```cds
cast( amount as abap.dec(15,2) ) as ConvertedAmount,
cast( status as abap.char(10) )  as StatusText,
```

### Case Expressions

```cds
// Simple CASE
case status
  when 'N' then 'New'
  when 'A' then 'Approved'
  when 'R' then 'Rejected'
  else 'Unknown'
end as StatusText,

// Searched CASE
case when net_amount > 10000 then 'High'
     when net_amount > 1000  then 'Medium'
     else 'Low'
end as PriorityCategory,
```

### Arithmetic Expressions

```cds
quantity * unit_price as TotalPrice,
net_amount + tax_amount as GrossAmount,
```

### String Functions

```cds
concat( first_name, concat( ' ', last_name ) ) as FullName,
substring( postal_code, 1, 2 )                 as Region,
length( description )                          as DescLength,
upper( country_code )                          as CountryUpper,
```

### Date & Time Functions

```cds
dats_days_between( start_date, end_date ) as DurationDays,
dats_add_days( order_date, 30 )           as DueDate,
tstmp_current_utctimestamp()              as CurrentTimestamp,
```

### Aggregate Expressions

```cds
define view entity ZI_OrderSummary
  as select from zsalesorder
{
  key customer_id as CustomerId,
      count(*)                      as OrderCount,
      sum( net_amount )             as TotalAmount,
      avg( net_amount as abap.dec(15,2) ) as AvgAmount,
      min( order_date )             as FirstOrderDate,
      max( order_date )             as LastOrderDate
}
group by customer_id
```

### Input Parameters

```cds
define view entity ZI_SalesOrderByDate
  with parameters
    p_date : abap.dats
  as select from zsalesorder
{
  key order_id   as OrderId,
      order_date as OrderDate,
      net_amount as NetAmount
}
where order_date >= $parameters.p_date
```

Using in ABAP SQL:

```abap
SELECT FROM zi_salesorderbydate( p_date = @lv_date )
  FIELDS OrderId, OrderDate, NetAmount
  INTO TABLE @DATA(lt_orders).
```

### Session Variables

```cds
$session.user           as CurrentUser,
$session.client         as CurrentClient,
$session.system_date    as SystemDate,
$session.system_language as SystemLanguage,
```

## Joins

```cds
define view entity ZI_OrderWithCustomer
  as select from zsalesorder as so
  inner join zcustomer as cust
    on so.customer_id = cust.customer_id
{
  key so.order_id      as OrderId,
      cust.customer_name as CustomerName,
      so.net_amount     as NetAmount
}
```

| Join Type   | Keyword            | Behavior                       |
| ----------- | ------------------ | ------------------------------ |
| Inner       | `inner join`       | Only matching rows             |
| Left Outer  | `left outer join`  | All from left + matching right |
| Right Outer | `right outer join` | All from right + matching left |
| Cross       | `cross join`       | Cartesian product              |

> **Note**: Prefer associations over joins when possible — associations are lazily resolved and support path expressions.

## Key Annotations

### Semantics Annotations (for managed fields in RAP)

```cds
@Semantics.user.createdBy: true
created_by as CreatedBy,

@Semantics.systemDateTime.createdAt: true
created_at as CreatedAt,

@Semantics.user.localInstanceLastChangedBy: true
last_changed_by as LastChangedBy,

@Semantics.systemDateTime.localInstanceLastChangedAt: true
local_last_changed_at as LocalLastChangedAt,

@Semantics.systemDateTime.lastChangedAt: true
last_changed_at as LastChangedAt,
```

### Amount & Currency / Quantity & Unit

```cds
@Semantics.amount.currencyCode: 'CurrencyCode'
net_amount as NetAmount,

currency_code as CurrencyCode,

@Semantics.quantity.unitOfMeasure: 'QuantityUnit'
quantity as Quantity,

quantity_unit as QuantityUnit,
```

### UI Annotations (in CDS or Metadata Extensions)

```cds
@UI.headerInfo: {
  typeName: 'Sales Order',
  typeNamePlural: 'Sales Orders',
  title: { type: #STANDARD, value: 'OrderId' }
}

@UI.lineItem: [{ position: 10 }]
@UI.identification: [{ position: 10 }]
@UI.selectionField: [{ position: 10 }]
order_id as OrderId,
```

### Metadata Extensions (recommended for UI annotations)

```cds
@Metadata.layer: #CUSTOMER
annotate view ZC_SalesOrder with
{
  @UI.facet: [{
    id: 'GeneralInfo',
    type: #IDENTIFICATION_REFERENCE,
    label: 'General Information',
    position: 10
  }]

  @UI.lineItem: [{ position: 10, importance: #HIGH }]
  @UI.identification: [{ position: 10 }]
  OrderId;

  @UI.lineItem: [{ position: 20 }]
  @UI.identification: [{ position: 20 }]
  @UI.selectionField: [{ position: 10 }]
  CustomerId;

  @UI.lineItem: [{ position: 30 }]
  @UI.identification: [{ position: 30 }]
  NetAmount;
}
```

## CDS Access Control

```cds
@EndUserText.label: 'Access Control for Sales Order'
@MappingRole: true
define role ZR_SalesOrder
{
  grant select on ZR_SalesOrder
  where ( CustomerId ) = aspect pfcg_auth ( Z_SO_AUTH, CUSTOMER_ID, ACTVT = '03' );
}
```

### Access Control Patterns

| Pattern          | Description                                 |
| ---------------- | ------------------------------------------- |
| `pfcg_auth`      | Standard authorization object check         |
| `inherit`        | Inherit restrictions from associated entity |
| `aspect user`    | Restrict by current user                    |
| `true` / `false` | Unrestricted / no access                    |

```cds
// Inherit from parent entity
define role ZR_SalesOrderItem {
  grant select on ZR_SalesOrderItem
  where inheriting conditions from entity ZR_SalesOrder
    association _Order;
}

// User-based restriction
define role ZR_MyOrders {
  grant select on ZR_SalesOrder
  where CreatedBy = aspect user;
}
```

## CDS Table Entities

```cds
define table entity ztab_salesorder {
  key client    : abap.clnt;
  key order_uuid: sysuuid_x16;
      order_id  : abap.numc(10);
      customer  : abap.char(10);
      amount    : abap.dec(15,2);
      currency  : abap.cuky(5);
}
```

> CDS table entities can serve as alternatives to classic DDIC database tables and can be used as `persistent table` in RAP BDEFs.

## Data Model Patterns for RAP

### Typical Composition Tree

```
ZR_Root (define root view entity)
├── composition [0..*] of ZR_Child1 as _Child1
└── composition [0..*] of ZR_Child2 as _Child2
    └── composition [0..*] of ZR_GrandChild as _GrandChild

ZR_Child1 (association to parent ZR_Root as _Root)
ZR_Child2 (association to parent ZR_Root as _Root)
  └── composition [0..*] of ZR_GrandChild as _GrandChild
ZR_GrandChild (association to parent ZR_Child2 as _Parent)
```

### Admin Field Pattern (Managed RAP BO)

Every entity in a managed RAP BO should include admin fields:

| Field                | Type      | Annotation                                                   | Purpose                         |
| -------------------- | --------- | ------------------------------------------------------------ | ------------------------------- |
| `CreatedBy`          | `syuname` | `@Semantics.user.createdBy: true`                            | Who created                     |
| `CreatedAt`          | `utclong` | `@Semantics.systemDateTime.createdAt: true`                  | When created                    |
| `LastChangedBy`      | `syuname` | `@Semantics.user.localInstanceLastChangedBy: true`           | Who last changed                |
| `LocalLastChangedAt` | `utclong` | `@Semantics.systemDateTime.localInstanceLastChangedAt: true` | ETag for optimistic concurrency |
| `LastChangedAt`      | `utclong` | `@Semantics.systemDateTime.lastChangedAt: true`              | Total ETag for draft            |

## Output Format

- Provide complete CDS source code when creating new views
- Include all relevant annotations
- Follow naming conventions (`ZR_*` for interface, `ZC_*` for consumption, `ZI_*` for reuse)
- Always expose associations used in consumption
- Include access control definitions when security is relevant

## References

- [SAP ABAP Cheat Sheets — CDS View Entities](https://github.com/SAP-samples/abap-cheat-sheets/blob/main/15_CDS_View_Entities.md)
- [SAP Help — ABAP Data Models Guide](https://help.sap.com/docs/abap-cloud/abap-data-models/abap-data-models)
- [SAP Help — ABAP CDS Reference](https://help.sap.com/doc/abapdocu_cp_index_htm/CLOUD/en-US/index.htm?file=abencds.htm)
- [SAP Help — CDS Annotations](https://help.sap.com/doc/abapdocu_cp_index_htm/CLOUD/en-US/ABENCDS_ANNOTATIONS.html)
- [CDS Feature Matrix Blog](https://blogs.sap.com/2022/10/24/feature-matrix-data-modeling-with-abap-core-data-services/)

## Clean Core Level Notes for CDS

| Scenario                                                          | Level | Notes                                                         |
| ----------------------------------------------------------------- | ----- | ------------------------------------------------------------- |
| `SELECT` from a released SAP CDS view (`I_*`)                      | **A** | Target state                                                  |
| Custom CDS view over your own tables                              | **A** | Allowed within the same software component                    |
| `SELECT` from a classic (nominated) SAP CDS view                  | **B** | Acceptable in classic ABAP development                        |
| Wrapper CDS view over a non-released SAP CDS view                 | **B/C** | B if the wrapped view is a classic API, otherwise C         |
| Direct **read** access to an SAP database table                   | **C** | ATC priority 2 — use a released CDS view or classic API       |
| Direct **write** access to an SAP database table                  | **D** | ATC priority 1 — use released or classic APIs                 |
| `CDS extend` / metadata extension on an SAP CDS view              | **A/B** | Preferred over modification                                 |
| Custom field via a **released** extension include                 | **A** | Preferred technique                                           |
| Custom field via a **non-released** extension include             | **B** | Monitor for a released include                                |
| Custom field via a classic append                                 | **C** | Monitor when an extension include becomes available           |

### Wrapper CDS view guidance

- If a suitable SAP CDS view exists but is not released, create a custom CDS view on top of it and release it for ABAP Cloud development
- CDS views referenced by the SAP view (association targets, value help views) may need their own wrappers
- If no suitable SAP CDS view exists at all, create the custom CDS view directly on the database table
- Retire the wrapper once SAP releases an equivalent CDS view

CDS views are classified in the Cloudification Repository under object type `STOB`.

## Related Skills

- **abap-sql-amdp**: Use for advanced ABAP SQL queries and AMDP procedures
- **rap**: Use for building RAP business objects based on CDS data models
- **authorization-iam**: Use for implementing CDS access control (DCL)
- **odata**: Use for exposing CDS views as OData services
- **abap-cloud**: Use for clean core level classification and wrapper CDS view patterns
- **abap-cloud-migration**: Use for replacing direct table access with released CDS views
