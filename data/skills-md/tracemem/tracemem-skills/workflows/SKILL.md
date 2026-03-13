---
name: workflows
description: Complete workflow patterns for common TraceMem operations.
---

# Skill: TraceMem Complete Workflow Patterns

## ⚠️ CRITICAL RULE: Decision Envelope is MANDATORY

**The Decision Envelope is NOT optional.**

ALL TraceMem operations MUST happen within a decision envelope:

```
┌─────────────────────────────────────┐
│   DECISION ENVELOPE (decision_id)   │
│  ┌───────────────────────────────┐  │
│  │  ✓ decision_read              │  │
│  │  ✓ decision_write (CRUD)      │  │
│  │  ✓ decision_evaluate          │  │
│  │  ✓ decision_request_approval  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘

❌ CANNOT be called without decision_id
```

**Discovery tools** (do NOT require decision envelope):
- ✅ `products_list` - find available products
- ✅ `product_get` - get schema and purposes
- ✅ `capabilities_get` - get runtime capabilities

## Workflow 1: Read Single Record

**Use Case**: Get customer details for support ticket

### Complete Step-by-Step

```javascript
// Step 1: Create Decision Envelope (MANDATORY)
const createResult = await decision_create({
  intent: "customer.lookup.support",
  automation_mode: "autonomous"  // Must be: propose, approve, override, autonomous
});
const decisionId = createResult.decision_id;  // Save for all subsequent operations

// Step 2: Get Product Schema (Optional but recommended)
const productInfo = await product_get({
  product: "customers_v1"
});
// Returns: {
//   exposed_schema: [
//     {name: "customer_id", type: "integer"},
//     {name: "name", type: "string"},
//     {name: "email", type: "string"},
//     {name: "tier", type: "string"}
//   ],
//   allowed_purposes: ["support_context", "order_validation"]
// }

// Step 3: Read Data (REQUIRES decision_id)
const readResult = await decision_read({
  decision_id: decisionId,  // From Step 1
  product: "customers_v1",
  purpose: "support_context",  // Must be in allowed_purposes
  query: {customer_id: 1001},  // Use field names from schema
  allow_multiple: false
});
// Returns: {records: [{customer_id: 1001, name: "Acme Corp", ...}]}

// Step 4: Close Decision Envelope (MANDATORY)
await decision_close({
  decision_id: decisionId,
  action: "commit"  // or "abort" if cancelled
});
```

### Error Case: Missing Decision Envelope

```javascript
// ❌ WRONG - This will FAIL
const result = await decision_read({
  product: "customers_v1",
  purpose: "support_context",
  query: {customer_id: 1001}
  // Missing decision_id!
});
// Error: "decision_id is required"

// ✓ CORRECT - Create decision first
const createResult = await decision_create({...});
const result = await decision_read({
  decision_id: createResult.decision_id,
  ...
});
```

## Workflow 2: Insert New Record

**Use Case**: Create a new customer order

### Complete Step-by-Step

```javascript
// Step 1: Create Decision Envelope (MANDATORY)
const createResult = await decision_create({
  intent: "order.create.customer",
  automation_mode: "autonomous"
});
const decisionId = createResult.decision_id;

// Step 2: Get Product Schema to understand required fields
const productInfo = await product_get({
  product: "orders_v1"
});
// Check restrictions.write.insert_config.column_config for:
// - required fields
// - allowed fields
// - fields with auto-generation

// Step 3: Insert Data (REQUIRES decision_id)
const writeResult = await decision_write({
  decision_id: decisionId,  // From Step 1
  product: "orders_v1",
  purpose: "order_creation",
  mutation: {
    operation: "insert",
    records: [{
      customer_id: 1001,      // Required field
      total_amount: 99.99,    // Required field
      status: "pending"       // Required field
      // order_id omitted - auto-generated
    }]
  }
});
// Returns: {created_records: [{order_id: 12345, ...}]}

// Step 4: Close Decision Envelope (MANDATORY)
await decision_close({
  decision_id: decisionId,
  action: "commit"
});
```

## Workflow 3: Update Record

**Use Case**: Update order status to shipped

### Complete Step-by-Step

```javascript
// Step 1: Create Decision Envelope (MANDATORY)
const createResult = await decision_create({
  intent: "order.status.update",
  automation_mode: "approve"  // Requires approval
});
const decisionId = createResult.decision_id;

// Step 2: Read current state (best practice)
const currentData = await decision_read({
  decision_id: decisionId,
  product: "orders_v1",
  purpose: "order_update",
  query: {order_id: 12345}
});
const currentStatus = currentData.records[0].status;

// Step 3: Evaluate policy (if required)
const policyResult = await decision_evaluate({
  decision_id: decisionId,
  policy_id: "order_status_change_v1",
  inputs: {
    current_status: currentStatus,
    new_status: "shipped"
  }
});
// Returns: {allowed: true, ...} or {allowed: false, requires_approval: true}

// Step 4: Update Data (REQUIRES decision_id, using NEW keys format)
const updateResult = await decision_write({
  decision_id: decisionId,
  product: "orders_v1",
  purpose: "order_update",
  operation: "update",  // Top-level operation
  keys: {order_id: 12345},  // NEW: Explicit key specification
  mutation: {
    fields: {  // NEW: Update fields separate from keys
      status: "shipped",
      shipped_at: new Date().toISOString()
    }
  }
});

// Step 5: Close Decision Envelope (MANDATORY)
await decision_close({
  decision_id: decisionId,
  action: "commit"
});
```

## Workflow 4: Delete Record

**Use Case**: Delete expired draft order

### Complete Step-by-Step

```javascript
// Step 1: Create Decision Envelope (MANDATORY)
const createResult = await decision_create({
  intent: "order.draft.cleanup",
  automation_mode: "autonomous"
});
const decisionId = createResult.decision_id;

// Step 2: Verify record before delete (best practice)
const verifyResult = await decision_read({
  decision_id: decisionId,
  product: "orders_v1",
  purpose: "data_cleanup",
  query: {
    order_id: 67890,
    status: "draft"
  }
});

if (verifyResult.records.length === 0) {
  // No record found - abort
  await decision_close({
    decision_id: decisionId,
    action: "abort",
    reason: "Record not found or not eligible for deletion"
  });
  return;
}

// Step 3: Delete Data (REQUIRES decision_id, using NEW keys format)
const deleteResult = await decision_write({
  decision_id: decisionId,
  product: "orders_v1",
  purpose: "data_cleanup",
  operation: "delete",  // Top-level operation
  keys: {order_id: 67890}  // NEW: Explicit key specification (no mutation needed for single delete)
});

// Step 4: Close Decision Envelope (MANDATORY)
await decision_close({
  decision_id: decisionId,
  action: "commit"
});
```

## Workflow 5: Approval Request

**Use Case**: Request approval for exceptional discount

### Complete Step-by-Step

```javascript
// Step 1: Create Decision Envelope (MANDATORY)
const createResult = await decision_create({
  intent: "discount.exception.request",
  automation_mode: "approve"  // Indicates approval needed
});
const decisionId = createResult.decision_id;

// Step 2: Evaluate policy to check if approval needed
const policyResult = await decision_evaluate({
  decision_id: decisionId,
  policy_id: "discount_cap_v1",
  inputs: {
    discount_percent: 30,
    customer_tier: "standard",
    order_value: 1000
  }
});

if (policyResult.requires_approval) {
  // Step 3: Request Approval (REQUIRES decision_id)
  const approvalResult = await decision_request_approval({
    decision_id: decisionId,
    title: "30% Discount Exception",
    message: "Customer requesting 30% discount on $1000 order. Standard tier typically limited to 15%."
  });
  
  // Step 4: Wait for approval (poll decision_get)
  let approved = false;
  for (let i = 0; i < 60; i++) {  // Poll for up to 5 minutes
    await sleep(5000);  // Wait 5 seconds
    
    const decisionStatus = await decision_get({
      decision_id: decisionId
    });
    
    if (decisionStatus.approval_status === "approved") {
      approved = true;
      break;
    } else if (decisionStatus.approval_status === "denied") {
      break;
    }
  }
  
  if (!approved) {
    // Step 5a: Close with abort if denied
    await decision_close({
      decision_id: decisionId,
      action: "abort",
      reason: "Approval denied or timed out"
    });
    return;
  }
}

// Step 5b: Apply the discount (if approved)
const writeResult = await decision_write({
  decision_id: decisionId,
  product: "discounts_v1",
  purpose: "discount_application",
  mutation: {
    operation: "insert",
    records: [{
      order_id: 12345,
      discount_percent: 30,
      reason: "exception_approved"
    }]
  }
});

// Step 6: Close Decision Envelope (MANDATORY)
await decision_close({
  decision_id: decisionId,
  action: "commit"
});
```

## Workflow 6: Read Multiple Records

**Use Case**: Get all premium customers for marketing

### Complete Step-by-Step

```javascript
// Step 1: Create Decision Envelope (MANDATORY)
const createResult = await decision_create({
  intent: "customer.list.marketing",
  automation_mode: "autonomous"
});
const decisionId = createResult.decision_id;

// Step 2: Read with allow_multiple (REQUIRES decision_id)
const readResult = await decision_read({
  decision_id: decisionId,
  product: "customers_v1",
  purpose: "marketing_campaign",
  query: {tier: "premium"},
  allow_multiple: true  // Allow multiple results
});

console.log(`Found ${readResult.records.length} premium customers`);

// Step 3: Close Decision Envelope (MANDATORY)
await decision_close({
  decision_id: decisionId,
  action: "commit"
});
```

## OpenCode Convenience Tools

When using OpenCode plugin, you can use convenience wrappers:

### tracemem_open (convenience wrapper for decision_create)

```javascript
// OpenCode convenience
const result = await tracemem_open({
  action: "db_change"  // Maps to intent: "data.change.apply"
});

// Is equivalent to:
const result = await decision_create({
  intent: "data.change.apply",
  automation_mode: "autonomous"
});
```

**Action Mappings**:
- `edit_files` → `code.change.apply`
- `refactor` → `code.refactor.execute`
- `run_command` → `ops.command.execute`
- `deploy` → `deploy.release.execute`
- `secrets` → `secrets.change.propose`
- `db_change` → `data.change.apply`
- `review` → `code.review.assist`

## Common Error Recovery

### Error: "decision_id is required"

```javascript
// Problem: Attempted operation without decision envelope
❌ await decision_read({product: "customers_v1", ...});

// Solution: Create decision first
✓ const {decision_id} = await decision_create({...});
✓ await decision_read({decision_id, ...});
```

### Error: "invalid automation_mode"

```javascript
// Problem: Used invalid automation mode
❌ await decision_create({
  intent: "order.create",
  automation_mode: "manual"  // Invalid!
});

// Solution: Use one of the 4 valid values
✓ await decision_create({
  intent: "order.create",
  automation_mode: "autonomous"  // Valid: propose, approve, override, autonomous
});
```

### Error: "Purpose 'X' is not allowed"

```javascript
// Problem: Used invalid purpose
❌ await decision_read({
  decision_id,
  product: "customers_v1",
  purpose: "random_purpose"  // Not in allowed_purposes
});

// Solution: Check product_get first
✓ const product = await product_get({product: "customers_v1"});
✓ console.log(product.allowed_purposes);  // ["support_context", "order_validation"]
✓ await decision_read({
  decision_id,
  product: "customers_v1",
  purpose: "support_context"  // Use valid purpose
});
```

### Error: "field X not found in schema"

```javascript
// Problem: Used wrong field name in query
❌ await decision_read({
  decision_id,
  product: "customers_v1",
  query: {customerId: 1001}  // Wrong field name
});

// Solution: Check schema first
✓ const product = await product_get({product: "customers_v1"});
✓ console.log(product.exposed_schema);  // [{name: "customer_id", ...}]
✓ await decision_read({
  decision_id,
  product: "customers_v1",
  query: {customer_id: 1001}  // Correct field name from schema
});
```

## Quick Reference: Operation Requirements

| Operation | Requires decision_id? | What It Returns | When to Use |
|-----------|----------------------|-----------------|-------------|
| `decision_create` | ❌ No (creates it) | decision_id | **FIRST STEP** - Always start here |
| `products_list` | ❌ No | List of product names | Discovery - find available products |
| `product_get` | ❌ No | **METADATA** about product (schema, purposes) | Discovery - understand product structure |
| `decision_read` | ✅ **YES** | **ACTUAL DATA** records from database | Read actual customer/order/etc records |
| `decision_write` | ✅ **YES** | Write confirmation | Insert/Update/Delete actual data |
| `decision_evaluate` | ✅ **YES** | Policy decision | Check if action is allowed |
| `decision_request_approval` | ✅ **YES** | Approval request ID | Request human approval |
| `decision_close` | ✅ **YES** | Closure confirmation | **FINAL STEP** - Always close |

## Best Practices

1. **Always create decision first**: No exceptions. All operations require a decision envelope.

2. **Understand product structure first**: Call `product_get` to get METADATA (schema, purposes). This tells you HOW to query, not the data itself. Then use `decision_read` to get ACTUAL DATA.

3. **Choose correct write operation**:
   - **INSERT**: Creating NEW records → `operation: "insert", mutation: {records: [...]}`
   - **UPDATE**: Modifying EXISTING records → `operation: "update", keys: {...}, mutation: {fields: {...}}`
   - **DELETE**: Removing records → `operation: "delete", keys: {...}`

4. **Close every decision**: Use try/finally to ensure decisions are closed even on errors.

4. **Use meaningful intents**: Follow pattern `domain.entity.action` (e.g., `customer.order.create`).

5. **Only 4 automation modes**: `propose`, `approve`, `override`, `autonomous` - no others are valid.

6. **Read before update/delete**: For updates/deletes, always read current state first to verify the record exists.

7. **Handle errors gracefully**: Close with "abort" if operation fails or is cancelled.

## Understanding decision_read vs product_get

**Critical distinction**:

```javascript
// product_get → Returns METADATA about the product
const metadata = await product_get({product: "customers_v1"});
// Returns: {
//   exposed_schema: [{name: "customer_id", type: "integer"}, ...],
//   allowed_purposes: ["support_context", ...],
//   example_queries: [...]
// }
// This tells you HOW the product works, not the actual data

// decision_read → Returns ACTUAL DATA from the product
const data = await decision_read({
  decision_id,
  product: "customers_v1",
  purpose: "support_context",
  query: {customer_id: 1001}
});
// Returns: {
//   records: [{customer_id: 1001, name: "Acme Corp", email: "contact@acme.com"}]
// }
// This gives you the actual customer record
```

**Think of it like a library**:
- `product_get` = Reading the card catalog to understand what's available
- `decision_read` = Actually checking out and reading a book

## Choosing the Right Write Operation

When using `decision_write`, provide the `operation` as a top-level parameter:

### INSERT - Creating New Records
Use when: You want to add a NEW record that doesn't exist yet

```javascript
// Top-level operation parameter (NEW)
operation: "insert",
mutation: {
  records: [{
    customer_id: 1001,     // Required fields from schema
    name: "Acme Corp",
    email: "contact@acme.com"
    // order_id omitted if auto-generated
  }]
}
```

### UPDATE - Modifying Existing Records  
Use when: You want to CHANGE specific fields in records that already exist

```javascript
// NEW recommended format: keys object (single record)
operation: "update",
keys: {order_id: 12345},  // Explicit key specification
mutation: {
  fields: {  // Update fields separate from keys
    status: "shipped",
    shipped_at: "2026-02-03T10:00:00Z"
  }
}

// OR batch format with keys array
operation: "update",
keys: ["order_id"],  // Declare key field names
mutation: {
  records: [{
    order_id: 12345,
    status: "shipped",
    shipped_at: "2026-02-03T10:00:00Z"
  }]
}
```

### DELETE - Removing Records
Use when: You want to REMOVE records entirely

```javascript
// NEW recommended format: keys object (simplest for single delete)
operation: "delete",
keys: {order_id: 67890}  // Explicit key specification

// OR batch format with keys array
operation: "delete",
keys: ["order_id"],
mutation: {
  records: [{
    order_id: 67890
  }, {
    order_id: 67891
  }]
}
```

**Note**: The new `keys` parameter makes update/delete requests self-documenting and clear. For backward compatibility, the old format (keys mixed with fields) still works but is deprecated. Always use explicit key specification for better clarity and maintainability.

**Rule of thumb**: 
- Creating something new? → **INSERT**
- Changing existing data? → **UPDATE** (provide identifiers + changed fields)
- Removing data? → **DELETE** (provide identifiers only)
