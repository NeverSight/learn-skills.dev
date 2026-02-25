---
name: lotus-analyze-reference-dependencies
description: |
  Identifies and maps Lotus Notes reference database dependencies, lookups, and cross-database relationships.
  Use when analyzing how applications depend on shared reference databases (suppliers, catalogs, employees),
  tracking bidirectional relationships, handling orphaned references, or planning database synchronization.
allowed-tools:
  - Read
  - Bash
  - Grep
---

Works with reference field mapping, dependency graphs, circular reference detection, and orphan handling.
# Analyze Lotus Notes Reference Database Dependencies

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#examples)

**How to Implement** → [Step-by-Step](#instructions) | [Expected Outcomes](#quick-start)

**Reference** → [Requirements](#requirements) | [Related Skills](#see-also)

## Purpose

Lotus Notes applications frequently depend on shared reference databases—master lists like Suppliers, Catalogs, Employees, Locations, etc. These reference databases are typically read-only lookups that multiple applications depend on. Understanding these dependencies is critical for migration planning: you must migrate reference databases first and handle orphaned references. This skill guides you through mapping these complex dependency relationships.

## When to Use

Use this skill when you need to:

- **Analyze shared reference databases** - Identify master lists (suppliers, catalogs, employees) used by multiple applications
- **Track bidirectional relationships** - Map how applications reference each other and detect circular dependencies
- **Handle orphaned references** - Find and remediate broken references before or during migration
- **Plan database synchronization** - Design proper migration sequencing to avoid breaking dependencies
- **Map cross-database relationships** - Document lookup patterns, reference fields, and data dependencies
- **Validate reference integrity** - Detect missing references and assess data quality

This skill is critical for determining migration order and preventing broken references during Lotus Notes migrations.

## Quick Start

To analyze reference database dependencies:

1. Create inventory of all reference databases in your ecosystem
2. Identify all applications that reference them
3. Map specific reference fields in each application
4. Document reference integrity constraints and orphan handling
5. Create dependency graph showing which applications depend on what references
6. Plan migration order based on dependency chains
7. Design orphan handling and fallback strategies

## Instructions

### Step 1: Identify Reference Databases

Locate all shared reference databases in your Lotus Notes environment:

**Search for databases with patterns:**
- Names like "Lookup", "Master", "Catalog", "Configuration"
- Read-only databases accessed by multiple applications
- Databases replicated across multiple servers
- Domino Directory (Notes.nsf)—the system reference database
- Custom reference databases specific to your organization

**For each reference database, document:**
- Database name and title
- Physical file location(s) and replicas
- Primary documents forms (Supplier, Product, Employee, etc.)
- Which applications reference it
- Update frequency (static vs. regularly updated)
- Access restrictions and who can modify it

Example inventory:

```
Reference Database: Supplier Master
  File: suppliers.nsf
  Location: Domino Server, also replicated to local workstations
  Forms:
    - Supplier (main form)
    - SupplierCategory
    - SupplierContact
  Applications that use it:
    - Order Management (B&O system)
    - Purchasing
    - Finance/Billing
  Update frequency: Weekly (Monday 2 PM)
  Access: Everyone can read, only procurement team can edit

Reference Database: Employee Directory
  File: employees.nsf
  Location: Domino Server (HR maintains)
  Forms:
    - Employee (main form)
    - Department
    - Manager
  Applications that use it:
    - Order Management
    - Project Tracking
    - Expense Reports
  Update frequency: Daily (automatic sync from HR system)
  Access: Everyone can read, HR team can edit
```

### Step 2: Map Reference Fields in Applications

Identify all fields that reference external databases:

**For each application, document:**

1. **Which forms use references:**
   ```
   Form: Order
     Field: Supplier
       Type: Reference
       Points to: Supplier Master.nsf, Supplier form
       Is multi-value: No
       Key field: SupplierID
       Display field: SupplierName

     Field: Approvers
       Type: Reference
       Points to: Employee Directory.nsf, Employee form
       Is multi-value: Yes (can select multiple)
       Key field: EmployeeID
       Display field: EmployeeName
   ```

2. **How are references used:**
   - In views (filtering by supplier name)
   - In computed fields (pulling supplier information)
   - In validation (ensuring supplier exists)
   - In lookups (formula looking up supplier data)

3. **What happens when reference is missing:**
   - Does the document fail to save?
   - Is there a fallback value?
   - Is there a validation formula that enforces it?

Example complete mapping:

```
Application: Order Management (B&O System)

Form: Order
  Reference Fields:
    1. Supplier
       Points to: Supplier Master.nsf → Supplier form
       Key: SupplierID
       Display: SupplierName
       Required: Yes
       Multi-value: No
       Used in: View filtering, computed field for discount lookup

    2. Items (embedded table)
       Contains: Product (reference)
       Points to: Catalog.nsf → Product form
       Key: ProductCode
       Display: ProductName
       Required: Yes (per row)
       Multi-value: No
       Used in: Price lookup, inventory check

    3. Approvers
       Points to: Employee Directory.nsf → Employee form
       Key: EmployeeID
       Display: EmployeeName
       Required: No
       Multi-value: Yes
       Used in: Approval workflow routing

View: "Orders by Supplier"
  Uses field: Supplier (grouping)
  Filter: Shows only documents with valid Supplier reference

Computed Fields:
  SupplierDiscount
    Formula: @DbLookup("NotesSQL"; ""; "suppliers.nsf"; Supplier; "DiscountRate")
    Depends on: Supplier field, Supplier Master database
    Fallback: 0 if lookup fails
```

### Step 3: Create Dependency Graph

Visualize how databases and applications relate:

**Text representation of dependency graph:**

```
Reference Databases (bottom tier - depended upon):
  ├─ Employee Directory (employees.nsf)
  ├─ Supplier Master (suppliers.nsf)
  └─ Catalog (products.nsf)

Applications (top tier - depend on references):
  ├─ Order Management
  │   └─ Depends on: Suppliers, Products, Employees
  ├─ Purchasing
  │   └─ Depends on: Suppliers, Employees
  ├─ Finance/Billing
  │   └─ Depends on: Suppliers
  └─ Project Tracking
      └─ Depends on: Employees
```

**Example with cardinality:**

```
Order Management
    ├─ Supplier reference (many-to-one)
    │   Points to: Supplier Master.nsf
    │   ~100K orders reference ~500 suppliers
    │   Risk: HighHigh (missing supplier breaks entire order)
    │
    ├─ Product reference (many-to-many via embedded table)
    │   Points to: Catalog.nsf
    │   ~100K orders × ~15 items avg = ~1.5M item references
    │   Risk: High (missing product breaks line item)
    │
    └─ Approver reference (many-to-one or one-to-many)
        Points to: Employee Directory.nsf
        ~100K orders with ~1-3 approvers each
        Risk: Medium (missing approver affects approval workflow, not order)
```

### Step 4: Analyze Reference Integrity

Assess how well references are maintained:

**For each reference field, investigate:**

1. **Is reference validation enforced?**
   ```
   Supplier field in Order form
     Validation formula: @NotEmpty(Supplier)
     Valid values: @DbCommand("NotesSQL"; ... list from Supplier Master)
     Result: ENFORCED - can't save order without valid supplier
   ```

2. **What happens with obsolete references?**
   - If a Supplier is marked inactive, can orders still reference it?
   - Can you change a Supplier's key field (SupplierID)?
   - Are there any historical orders that reference deleted suppliers?

3. **Orphan references:**
   - Count documents with broken/missing references
   - Document why references might be orphaned:
     ```
     Order with orphaned Supplier reference because:
       - Supplier was deleted from Supplier Master
       - OR Supplier replica is out of sync
       - OR Network issue when loading reference
     ```

4. **Circular dependencies:**
   - Does Supplier Master reference Employee Directory?
   - Does Employee Directory reference anything?
   - Map any circular references (rare but problematic)

**Detection query (pseudo-code):**

```sql
-- Find orders with orphaned supplier references
SELECT Count(*) as OrphanCount
FROM "orders.nsf"
WHERE Supplier IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM "suppliers.nsf"
    WHERE SupplierID = Order.Supplier
  )

-- Result: ~250 orphaned references out of 100,000 orders
-- Action required: Investigate root cause, decide on remediation
```

### Step 5: Document Lookup Patterns

Identify how data is looked up from reference databases:

**Pattern 1: Direct reference lookup (UI-driven)**

```
User selects supplier from dropdown in Order form
  Behind scenes: Notes client queries Supplier Master database
  Display: Shows SupplierName alongside SupplierID
  Performance: Fast if database is replicated locally
```

**Pattern 2: Formula-based lookup (computed fields)**

```
SupplierDiscount field in Order form
  Formula: @DbLookup("NotesSQL"; ""; "suppliers.nsf"; Supplier; "DiscountRate")
  Triggers: Whenever Supplier field changes
  Performance: Slow if supplier database is remote (can add 5-10s per save)
  Caching: Cached in document (requires recalc if supplier changes)
```

**Pattern 3: View-based filtering**

```
View: "High-Value Suppliers"
  Selection formula: @DbLookup("NotesSQL"; ""; "suppliers.nsf";
                               @ThisValue; "IsHighValue") = "Yes"
  Rebuilds: When supplier master changes
  Performance: View index must be rebuilt, can take minutes for large databases
```

**Document all lookup patterns used:**

```
Application: Order Management

Lookup Patterns:
  1. Direct reference (dropdowns)
     Where used: Supplier, Approver fields
     Performance impact: Low (client-side)
     Depends on: Local replica or good network

  2. @DbLookup formulas
     Where used: CalculateDiscount, LookupTax
     Performance impact: High (server round-trip per lookup)
     Count: ~500 documents per day, ~3 lookups each = 1,500 lookups/day

  3. View-based filters
     Where used: OrdersBySupplier, ApprovalPending views
     Performance impact: Medium (view rebuild required)
     Frequency: Suppliers update weekly, so view rebuild weekly
```

### Step 6: Plan Migration Order

Determine the correct sequence for migrating dependent databases:

**Migration dependency order:**

```
Phase 1: Reference Databases (FIRST)
  1. Migrate Employee Directory
  2. Migrate Supplier Master
  3. Migrate Catalog/Products
  (All applications depend on these)

Phase 2: Primary Applications (SECOND)
  1. Migrate Order Management
     (depends on Suppliers, Products, Employees)
  2. Migrate Purchasing
     (depends on Suppliers, Employees)
  3. Migrate Finance/Billing
     (depends on Suppliers)

Phase 3: Secondary Applications (THIRD)
  1. Migrate Project Tracking
     (depends on Employees)

Critical: Don't migrate Order Management before Supplier Master!
```

**Parallel migration planning:**

```
Timeline:
  Week 1: Migrate reference databases (Employee Dir + Suppliers)
    └─ Validate all reference lookups work in new system

  Weeks 2-3: Migrate primary applications in parallel
    ├─ Team A: Order Management → new system
    ├─ Team B: Purchasing → new system
    └─ Both teams rely on reference databases migrated in Week 1

  Weeks 4-5: Migrate secondary applications
```

### Step 7: Handle Orphaned References and Migration Strategy

Design how to handle references that may be broken:

**Strategy 1: Strict validation (reject invalid references)**

```
During migration:
  For each Order document:
    Check if Supplier reference exists in new Supplier Master
    IF NOT EXISTS:
      → Reject migration (flag for manual review)
      → Record which orders have orphaned references
      → Users must manually select valid supplier before migrating

  Post-migration:
    Run validation report
    Result: 250 orders have missing suppliers
    Action: Procurement team manually assigns suppliers
```

**Strategy 2: Lenient mapping (try to resolve references)**

```
Before migration:
  Build mapping: OldSupplierID → NewSupplierID

During migration:
  For each Order document:
    Supplier = mapping[OldSupplierID]
    IF mapping entry not found:
      → Use fallback supplier (e.g., "Unknown")
      → Log which orders used fallback
      → Flag for review

  Example mapping:
    "SUP-OLD-123" → "SUP-NEW-456"
    "SUP-OLD-999" → null (no mapping, use fallback)
```

**Strategy 3: Deactivate without deletion (preserve history)**

```
In reference database, don't DELETE old suppliers.
Instead, mark as inactive:
  Supplier record:
    SupplierID: "SUP-123"
    Status: "Inactive"  (was "Active")
    InactiveDate: "2025-11-03"
    Reason: "Migrated to new system"

Benefits:
  - Old orders can still reference the supplier
  - Historical data remains intact
  - No orphaned references
  - Can query "when did we last order from this supplier?"
```

**Choose your strategy and document:**

```
Reference Integrity Strategy
────────────────────────────

For Supplier references in Orders:
  Approach: Lenient mapping with fallback

  Migration process:
    1. Build mapping of old→new supplier IDs
    2. For each order, map supplier ID using table
    3. If no mapping found, set supplier="UNKNOWN" and flag order
    4. Post-migration: 30-day grace period for manual review
    5. After 30 days, orders with UNKNOWN supplier auto-archived

  Validation:
    - ~100K orders checked
    - ~250 orders (0.25%) mapped to UNKNOWN
    - Procurement team reviews flagged orders
    - Historical data preserved via AuditLog

For Product references in Order Items:
  Approach: Strict validation (reject incomplete migrations)

  Migration process:
    1. Build complete mapping of old→new product codes
    2. For each order item, validate product exists in new catalog
    3. If product not found, REJECT entire order (don't migrate)
    4. Migration report lists rejected orders

  Action:
    - ~100K orders processed
    - ~5K orders (5%) have obsolete products
    - Procurement reviews with finance
    - Decide: delete from history OR update product references
```

## Examples

### Example 1: Simple Reference Dependency

**Scenario: Employee Allocation System**

```
Reference Database: Employees (employees.nsf)
  Form: Employee
  Fields: EmployeeID, Name, Department, Email, Manager

Application: Time Tracking (timetracking.nsf)
  Form: TimeEntry
  Fields:
    - Employee (reference → employees.nsf → Employee)
      Required: Yes
      Validation: Must be active employee
    - Date, Hours, Project, Comments

Dependency:
  100K time entries → ~500 active employees
  Risk: MEDIUM (invalid employee blocks time entry saving)

Migration:
  1. First: Migrate Employee database → new system
  2. Validate all employees loaded correctly
  3. Then: Migrate time entries
  4. Validation: All 100K entries have valid employee reference
```

### Example 2: Complex Multi-Reference Dependency

**Scenario: Order Management with Multiple References**

```
Reference Databases:
  1. Suppliers (suppliers.nsf)
     Primary form: Supplier
     Key field: SupplierID

  2. Catalog (products.nsf)
     Primary form: Product
     Key field: ProductCode

  3. Employees (employees.nsf)
     Primary form: Employee
     Key field: EmployeeID

Application: Order Management (orders.nsf)
  Form: Order
  Reference fields:
    1. Supplier (many-to-one)
       → suppliers.nsf → SupplierID
    2. BillingContact (many-to-one)
       → employees.nsf → EmployeeID
    3. ShippingAddress (computed from Supplier)
       → Lookup: @DbLookup to suppliers.nsf

  Form: OrderLineItem (embedded in Order)
  Reference fields:
    1. Product (many-to-one)
       → products.nsf → ProductCode
    2. Quantity, Price

Dependency Graph:
  Order depends on:
    ├─ Supplier Master (1:many) [CRITICAL]
    ├─ Employee Directory (1:1) [REQUIRED for approval]
    └─ Catalog (1:many via items) [CRITICAL]

Migration Order:
  1. Suppliers database → new system
  2. Catalog database → new system
  3. Employee directory → new system
  4. Order management → new system (all dependencies now ready)

Reference Integrity:
  Current state:
    - 150K orders
    - ~50 reference integrity issues

  Issues found:
    - 25 orders reference deleted suppliers
    - 15 orders reference inactive employees
    - 10 order items reference obsolete products

  Resolution:
    - Suppliers: Deactivate instead of delete (preserve history)
    - Employees: Remap to new employee IDs
    - Products: Remap to current product codes or flag for review
```

### Example 3: Detecting Circular Dependencies

**Scenario: Complex Reference Network**

```
Databases in system:
  A. Suppliers (suppliers.nsf)
  B. Employees (employees.nsf)
  C. Contracts (contracts.nsf)
  D. Budget (budget.nsf)

Dependencies found:
  Suppliers
    └─ references: Employee (SupplierContact)

  Employees
    └─ references: none

  Contracts
    └─ references: Supplier, Employee

  Budget
    └─ references: Supplier, Employee, Contract

Dependency analysis:
  ✓ No circular dependencies (good)

  Migration order:
    1. Employees (depended on by others, depends on nothing)
    2. Suppliers (depends on Employees only)
    3. Contracts (depends on Employees + Suppliers)
    4. Budget (depends on all others - migrate last)
```

## Requirements

- **Database access**: Ability to inspect forms and fields in NSF databases
  - Lotus Notes Designer
  - Domino HTTP API with proper authentication
  - NSF export tools

- **Documentation**: Access to existing reference database documentation
  - Form specifications
  - Field definitions
  - Lookup formula documentation
  - Known reference integrity issues

- **Analysis tools**: Optional but helpful
  - Database dependency graphing tools
  - SQL query tools for NSF analysis
  - Graph visualization software (draw.io, Graphviz)

- **Data export capability**: To create migration mappings
  - Ability to export reference database contents
  - Ability to create mapping tables (old ID → new ID)

## See Also

- [lotus-analyze-nsf-structure](../lotus-analyze-nsf-structure/SKILL.md) - Understanding NSF database forms and fields
- [lotus-migration](../lotus-migration/SKILL.md) - Overall migration planning
- [lotus-replace-odbc-direct-writes](../lotus-replace-odbc-direct-writes/SKILL.md) - Replacing direct database access with APIs
