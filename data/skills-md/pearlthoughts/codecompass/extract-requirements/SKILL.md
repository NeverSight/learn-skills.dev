---
name: "extract-requirements"
description: "Use this when user needs to document business requirements from undocumented legacy code. Provides systematic 6-phase extraction: automated analysis, validation rules, use cases, business rules, data models, and workflow mapping. Apply for legacy system documentation, migration planning, compliance audits, or M&A due diligence"
categories: ["workflow", "requirements", "documentation"]
tags: ["requirements", "business-rules", "documentation", "reverse-engineering"]
version: "1.0.0"
---

# Extract Requirements Workflow

## Purpose

Systematic process for extracting business requirements from undocumented or poorly documented codebases.

## When to Use

- ✅ Legacy system with no documentation
- ✅ Planning migration (need requirements baseline)
- ✅ M&A due diligence (understand acquired system)
- ✅ Compliance audit (document what system does)
- ✅ Knowledge transfer (developers leaving)

## Prerequisites

### Codebase Indexed
```bash
codecompass batch:index <path>
```

### Infrastructure Running
```bash
codecompass health
```

## Extraction Workflow

### Phase 1: Automated Extraction

**Step 1.1: Run Requirements Extractor**
```bash
codecompass requirements:extract --project-id <id> --output requirements.md
```

**What this extracts**:
1. **Validation Rules** → Business constraints
2. **Controller Actions** → Use cases
3. **Database Constraints** → Data integrity rules
4. **RBAC/Authorization** → Access requirements
5. **Business Logic** → Domain rules

**Step 1.2: Review Output**
Check generated `requirements.md`:
- Completeness (coverage of major features)
- Accuracy (rules match actual behavior)
- Gaps (missing business logic)

### Phase 2: Validation Rule Analysis

**From Models/Entities**:
```php
// Yii2 Model example
public function rules() {
  return [
    [['email', 'password'], 'required'],
    ['email', 'email'],
    ['password', 'string', 'min' => 8],
    ['age', 'integer', 'min' => 18],
  ];
}
```

**Extracted Requirements**:
```markdown
### User Registration Requirements
- REQ-001: Email address is mandatory
- REQ-002: Email must be valid format
- REQ-003: Password is mandatory
- REQ-004: Password minimum length: 8 characters
- REQ-005: User must be at least 18 years old
```

### Phase 3: Use Case Extraction

**From Controllers**:
```php
// Controller actions → Use cases
public function actionCreate() {
  // Use Case: Create New Order
}

public function actionApprove($id) {
  // Use Case: Approve Order (with authorization check)
}

public function actionCancel($id) {
  // Use Case: Cancel Order (business rules apply)
}
```

**Extracted Use Cases**:
```markdown
## Order Management Use Cases

### UC-001: Create New Order
**Actor**: Customer
**Preconditions**: User authenticated
**Steps**:
1. User selects products
2. System validates inventory
3. User provides shipping address
4. System calculates total
5. Order created in pending status

### UC-002: Approve Order
**Actor**: Manager
**Preconditions**:
- Order in pending status
- User has 'manager' role
**Steps**:
1. Manager reviews order details
2. System validates business rules
3. Order status changed to approved
4. Notification sent to customer
```

### Phase 4: Business Rule Discovery

**Semantic Search for Rules**:
```bash
codecompass search:semantic "business validation rules for order approval"
codecompass search:semantic "conditions for discount calculation"
codecompass search:semantic "authorization checks for admin actions"
```

**Common Patterns to Find**:
1. **Conditional Logic** → Business rules
2. **Status Transitions** → Workflow states
3. **Calculations** → Business formulas
4. **Validations** → Constraints
5. **Authorization Checks** → Access rules

### Phase 5: Data Model Requirements

**From Database Schema**:
```sql
CREATE TABLE orders (
  id INT PRIMARY KEY,
  status ENUM('pending', 'approved', 'shipped', 'cancelled'),
  total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
  customer_id INT NOT NULL FOREIGN KEY REFERENCES customers(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Extracted Requirements**:
```markdown
### Data Requirements
- REQ-010: Order must have unique identifier
- REQ-011: Order status: pending, approved, shipped, or cancelled
- REQ-012: Order total must be non-negative
- REQ-013: Order must be associated with a customer
- REQ-014: Order creation timestamp must be recorded
```

### Phase 6: Workflow Mapping

**Identify State Machines**:
```
Order Status Flow:
pending → approved → shipped → delivered
         ↓
         cancelled
```

**Extract Transitions**:
```markdown
### Order Workflow
**States**: pending, approved, shipped, cancelled, delivered

**Transitions**:
- pending → approved (requires: manager approval)
- approved → shipped (requires: items in stock)
- shipped → delivered (requires: delivery confirmation)
- pending|approved → cancelled (requires: cancellation reason)

**Business Rules**:
- Cannot cancel after shipped
- Cannot approve if out of stock
- Refund required if cancelled after payment
```

## Extraction Techniques

### Technique 1: Code Reading Patterns

**Look for**:
- `if` statements → Business conditions
- `switch/case` → State transitions
- Loops → Bulk operations
- Exceptions → Error handling requirements
- Comments → Intent (when present)

### Technique 2: Test Analysis

**Tests reveal**:
- Expected behavior (what should happen)
- Edge cases (what shouldn't happen)
- Valid input ranges
- Error scenarios

```bash
codecompass search:semantic "test cases for order validation"
```

### Technique 3: Configuration Analysis

**Config files contain**:
- Feature flags → Optional requirements
- Limits/thresholds → Business constraints
- Integration settings → External dependencies

### Technique 4: Semantic Clustering

**Find related code**:
```bash
# Find all code related to "discount calculation"
codecompass search:semantic "discount calculation logic"

# Find all code related to "inventory management"
codecompass search:semantic "inventory stock management"
```

Group results by business capability

## Output Formats

### Format 1: Requirements Document (Markdown)

```markdown
# Business Requirements - [System Name]

## Functional Requirements

### FR-001: User Authentication
**Priority**: High
**Description**: System must authenticate users via email and password
**Acceptance Criteria**:
- Email validation follows RFC 5322
- Password minimum 8 characters
- Account locked after 5 failed attempts
**Source**: UserController::actionLogin(), User::validatePassword()

### FR-002: Order Approval Workflow
...
```

### Format 2: Capability Map (Structured)

```json
{
  "capabilities": {
    "user_management": {
      "features": ["register", "login", "reset_password"],
      "rules": ["email_unique", "password_complexity"],
      "roles": ["user", "admin"]
    },
    "order_processing": {
      "features": ["create", "approve", "cancel", "ship"],
      "rules": ["approval_required", "inventory_check"],
      "workflow": "pending→approved→shipped→delivered"
    }
  }
}
```

### Format 3: Use Case Catalog

```markdown
| UC ID | Use Case Name | Actor | Complexity |
|-------|---------------|-------|------------|
| UC-001 | Create Order | Customer | Medium |
| UC-002 | Approve Order | Manager | Low |
| UC-003 | Cancel Order | Customer/Manager | High |
```

## Validation Steps

### Step 1: Cross-Check with Tests
Compare extracted requirements with test cases:
- Tests validate requirements
- Missing tests → Undocumented behavior
- Failing tests → Requirements changed

### Step 2: Semantic Verification
```bash
# For each requirement, verify in code
codecompass search:semantic "password must be at least 8 characters"
```

Should find validator implementation

### Step 3: Interview Stakeholders (if available)
- Validate extracted requirements
- Fill gaps in documentation
- Clarify ambiguous logic

### Step 4: Traceability Matrix
Map requirements to code:
```markdown
| Requirement | Source Files | Tests |
|-------------|--------------|-------|
| REQ-001 | User.php:45, UserController.php:102 | UserTest.php:23 |
| REQ-002 | Order.php:78 | OrderTest.php:56 |
```

## Common Patterns

### Pattern 1: Implicit Requirements
**Code**:
```php
if ($order->total < 1000) {
  // No approval needed
}
```

**Requirement**:
```markdown
REQ: Orders under $1000 do not require manager approval
```

### Pattern 2: Embedded Business Logic
**Code**:
```php
$discount = ($customer->vip) ? 0.20 : 0.10;
```

**Requirement**:
```markdown
REQ: VIP customers receive 20% discount, regular customers 10%
```

### Pattern 3: Temporal Constraints
**Code**:
```php
if (strtotime($order->created_at) > strtotime('-30 days')) {
  // Can cancel
}
```

**Requirement**:
```markdown
REQ: Orders can only be cancelled within 30 days of creation
```

## Best Practices

### ✅ Do
- Extract from multiple sources (code, tests, configs)
- Use semantic search for concept discovery
- Validate with tests
- Document sources for traceability
- Prioritize by business impact
- Include non-functional requirements (performance, security)

### ❌ Don't
- Rely solely on comments (often outdated)
- Assume standard behavior without verification
- Skip edge cases
- Ignore error handling logic
- Document technical implementation instead of business requirements

## Related Skills

- `0-discover-capabilities.md` - Find relevant modules
- `semantic-search.md` - Search for business logic
- `analyze-yii2-project.md` - Framework-specific extraction

## Related Modules

From `.ai/capabilities.json`:
- `requirements` - RequirementsExtractionService
- `business-analyzer` - CapabilityCatalogService
- `search` - Semantic code search
- `analyzers` - Code analysis for extraction

---

**Remember**: Requirements are **what** the system must do, not **how** it does it. Focus on business value, not technical implementation.
