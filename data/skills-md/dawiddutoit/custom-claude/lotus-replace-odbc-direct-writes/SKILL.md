---
name: lotus-replace-odbc-direct-writes
description: |
  Replaces direct ODBC database writes and backend connections with proper API-based integration patterns.
  Use when migrating code that directly modifies Lotus Notes databases via ODBC, converting backend
  connections to HTTP APIs, implementing proper request/response patterns, or establishing secure
  data synchronization.
allowed-tools:
  - Read
  - Bash
  - Grep
---

Works with ODBC query migration, connection string updates, transaction handling, and error recovery patterns.
# Replace Lotus ODBC Direct Writes with API Patterns

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#examples)

**How to Implement** → [Step-by-Step](#instructions) | [Expected Outcomes](#quick-start)

**Reference** → [Requirements](#requirements) | [Related Skills](#see-also)

## Purpose

Legacy Lotus Notes systems often use ODBC (Open Database Connectivity) for direct database manipulation—bypassing the Notes client and directly modifying NSF files. This approach is problematic for migration because it creates hidden dependencies, lacks proper transaction handling, and breaks encapsulation. This skill guides you through replacing ODBC direct writes with clean, API-based patterns that work in modern architectures.

## When to Use

Use this skill when you need to:

- **Migrate direct ODBC writes** - Replace code that directly modifies Lotus Notes databases via ODBC
- **Convert backend connections** - Transform ODBC connections to HTTP API calls
- **Implement proper request/response patterns** - Design clean API contracts with validation and error handling
- **Establish secure data synchronization** - Replace direct database access with authenticated API calls
- **Update transaction handling** - Migrate ODBC transactions to API-based transaction semantics
- **Improve error recovery** - Add retry logic, idempotency, and proper error propagation

This skill is essential for modernizing tightly-coupled Lotus Notes integrations that bypass proper application boundaries.

## Quick Start

To migrate from ODBC direct writes to APIs:

1. Identify all ODBC connection strings and database access patterns
2. Map direct writes to business operations (what data changes are intended?)
3. Design API endpoints that encapsulate these operations
4. Implement request/response contracts with validation
5. Update calling code to use HTTP APIs instead of ODBC
6. Add retry logic, error handling, and logging
7. Test transaction behavior and rollback scenarios

## Instructions

### Step 1: Identify ODBC Direct Writes

Locate all direct ODBC database access in the codebase:

**Search for patterns:**
- ODBC connection strings or DSN references
- Direct SQL UPDATE/INSERT/DELETE statements to NSF databases
- Lotus Notes backend agent scripts that modify databases
- VB, Java, or scripting code that writes directly to Notes databases

**Document each occurrence with:**
- Source code location (file, function, line)
- ODBC connection details (database path, credentials)
- SQL statement being executed
- What business operation does this represent?
- Who calls this code and how often?
- What data validation is currently in place?

Example:

```
File: OrderProcessing.cls
Function: ApproveOrder(OrderID)
  Line 45: conn.Execute("UPDATE Orders SET Status='Approved' WHERE OrderID='" & OrderID & "'")
  Issue: Direct write with no validation or transaction handling
  Business operation: Mark order as approved
```

### Step 2: Understand Current Transaction Semantics

Analyze the ODBC access patterns to understand what transactions are needed:

**For each write operation, document:**
- Is this a single update or are multiple tables modified?
- What validation must happen before the write?
- What happens if the write fails? (rollback other changes?)
- Are there dependent operations that must follow?
- Does this operation trigger external side effects (emails, notifications)?

Example structure:

```
Operation: ApproveOrder(OrderID)
  Preconditions:
    - Order exists and Status='Draft'
    - User has 'Approver' role
    - Order total < budget limit for supplier
  Changes:
    - Update Order.Status = 'Approved'
    - Update Order.ApprovedDate = Now()
    - Create AuditLog entry
  Side effects:
    - Send email to Supplier
    - Update Dashboard cache
  Rollback behavior:
    - If email fails, should approval be rolled back?
```

### Step 3: Design API Endpoints

Create API endpoint definitions that replace the ODBC operations:

**For each operation, design:**

```
POST /api/orders/{orderId}/approve
  Description: Approve a pending order

  Request:
    {
      "approvalReason": "Budget approved",
      "approverNotes": "..."
    }

  Response (Success - 200):
    {
      "id": "ORDER-123",
      "status": "Approved",
      "approvedDate": "2025-11-03T10:30:00Z",
      "approvedBy": "user@example.com"
    }

  Response (Validation Error - 400):
    {
      "error": "ORDER_NOT_DRAFT",
      "message": "Order must be in Draft status to approve"
    }

  Response (Permission Error - 403):
    {
      "error": "INSUFFICIENT_PERMISSIONS",
      "message": "User does not have approval role"
    }

  Response (Server Error - 500):
    {
      "error": "APPROVAL_FAILED",
      "message": "Failed to send approval notification"
    }
```

**Design principles:**

- **Validation at API boundary**: All input validation before any database changes
- **Clear error responses**: Distinguish between user errors (4xx) and system errors (5xx)
- **Transaction clarity**: Make it clear what will and won't be rolled back
- **Idempotency**: Consider if calling the same operation twice should be safe
- **Audit trail**: Ensure who, what, when is captured

### Step 4: Implement API Endpoints

Create backend API endpoints with proper structure:

**Example Python implementation pattern:**

```python
from flask import Flask, request, jsonify
from typing import Dict, Tuple

class OrderService:
    def approve_order(self, order_id: str, approver_id: str, reason: str) -> Dict:
        """
        Approve a pending order with full validation and transaction handling.

        Args:
            order_id: The order to approve
            approver_id: User ID of approver
            reason: Reason for approval

        Returns:
            Approved order details

        Raises:
            OrderNotFound: Order doesn't exist
            OrderNotPending: Order is not in Draft status
            InsufficientPermissions: User can't approve
            ApprovalFailed: Underlying operation failed
        """
        # Step 1: Validate inputs
        if not order_id or not approver_id:
            raise ValueError("order_id and approver_id required")

        # Step 2: Check preconditions
        order = self.db.orders.get(order_id)
        if not order:
            raise OrderNotFound(f"Order {order_id} not found")

        if order['status'] != 'Draft':
            raise OrderNotPending(f"Order status is {order['status']}, expected Draft")

        if not self._user_can_approve(approver_id, order):
            raise InsufficientPermissions(f"User {approver_id} cannot approve")

        # Step 3: Execute transaction
        try:
            with self.db.transaction() as txn:
                # Update order
                self.db.orders.update(order_id, {
                    'status': 'Approved',
                    'approved_date': datetime.now(),
                    'approved_by': approver_id,
                    'approval_reason': reason
                })

                # Create audit entry
                self.db.audit_log.create({
                    'order_id': order_id,
                    'action': 'APPROVE',
                    'user': approver_id,
                    'timestamp': datetime.now(),
                    'details': reason
                })

                txn.commit()
        except Exception as e:
            raise ApprovalFailed(f"Failed to approve order: {str(e)}")

        # Step 4: Handle side effects (outside transaction)
        try:
            self._send_approval_notification(order_id)
        except Exception as e:
            # Log but don't fail—approval is already committed
            logger.error(f"Failed to send notification for {order_id}: {e}")

        # Step 5: Return updated order
        return self.db.orders.get(order_id)

@app.route('/api/orders/<order_id>/approve', methods=['POST'])
def approve_order(order_id: str) -> Tuple[Dict, int]:
    """HTTP endpoint for order approval."""

    data = request.get_json()
    approver_id = get_current_user_id()

    try:
        approved_order = OrderService().approve_order(
            order_id=order_id,
            approver_id=approver_id,
            reason=data.get('reason', '')
        )
        return jsonify(approved_order), 200

    except OrderNotFound as e:
        return jsonify({'error': 'ORDER_NOT_FOUND', 'message': str(e)}), 404

    except OrderNotPending as e:
        return jsonify({'error': 'ORDER_NOT_DRAFT', 'message': str(e)}), 400

    except InsufficientPermissions as e:
        return jsonify({'error': 'INSUFFICIENT_PERMISSIONS', 'message': str(e)}), 403

    except ApprovalFailed as e:
        return jsonify({'error': 'APPROVAL_FAILED', 'message': str(e)}), 500
```

### Step 5: Update Calling Code

Replace ODBC calls with HTTP API calls:

**Before (ODBC direct write):**

```vb
' Legacy Lotus Notes backend agent
Dim session As New NotesSession
Dim db As NotesDatabase
Set db = session.GetDatabase("", "Orders.nsf")

' Direct database modification via ODBC
Set con = CreateObject("ADODB.Connection")
con.Open "Driver={Lotus Notes ODBC Driver};..."
con.Execute("UPDATE Orders SET Status='Approved' WHERE OrderID=" & orderID)
```

**After (API call):**

```vb
' Use HTTP client library (e.g., HTTP.sys, curl)
Function ApproveOrder(orderID As String) As Boolean
    Dim client As Object
    Dim response As Object
    Dim url As String
    Dim payload As String

    url = "https://api.example.com/api/orders/" & orderID & "/approve"

    Set client = CreateObject("MSXML2.XMLHTTP")
    client.Open "POST", url, False
    client.SetRequestHeader "Content-Type", "application/json"
    client.SetRequestHeader "Authorization", "Bearer " & GetAuthToken()

    payload = "{""reason"": ""Manager approved""}"
    client.Send payload

    If client.Status = 200 Then
        ApproveOrder = True
    Else
        MsgBox "Approval failed: " & client.ResponseText
        ApproveOrder = False
    End If
End Function
```

**In Python:**

```python
import requests
from requests.auth import BearerTokenAuth

def approve_order(order_id: str) -> bool:
    """Call API to approve an order."""

    url = f"https://api.example.com/api/orders/{order_id}/approve"
    headers = {
        "Authorization": f"Bearer {get_auth_token()}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json={"reason": "Manager approved"},
        timeout=30
    )

    if response.status_code == 200:
        print(f"Order {order_id} approved")
        return True
    else:
        print(f"Approval failed: {response.text}")
        return False
```

### Step 6: Implement Retry and Error Handling

Add robust error handling for distributed calls:

```python
import time
from typing import Callable, Any

def retry_api_call(
    fn: Callable,
    max_retries: int = 3,
    backoff_seconds: float = 1.0
) -> Any:
    """
    Retry a function call with exponential backoff.

    Args:
        fn: Callable that makes the API request
        max_retries: Number of times to retry on failure
        backoff_seconds: Initial backoff interval
    """

    for attempt in range(max_retries):
        try:
            return fn()
        except requests.ConnectionError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = backoff_seconds * (2 ** attempt)
            logger.warning(f"Request failed, retrying in {wait_time}s: {e}")
            time.sleep(wait_time)
        except requests.Timeout:
            raise  # Don't retry timeouts—likely indicates slow API
```

### Step 7: Test Transaction Behavior

Validate that your API handles edge cases:

- **Idempotency**: Calling approve twice shouldn't double-approve
- **Concurrent updates**: What if two people try to approve simultaneously?
- **Partial failures**: If side effects fail, is the core operation still committed?
- **Validation enforcement**: Invalid data is rejected before any changes

## Examples

### Example 1: Simple Update Migration

**ODBC Direct Write:**

```
UPDATE Suppliers SET Status='Active' WHERE SupplierID='SUP-123'
```

**API Endpoint:**

```
PUT /api/suppliers/SUP-123
{
  "status": "Active"
}
```

**Implementation:**

```python
@app.route('/api/suppliers/<supplier_id>', methods=['PUT'])
def update_supplier(supplier_id: str):
    data = request.get_json()
    supplier = SupplierService().update(supplier_id, data)
    return jsonify(supplier), 200
```

### Example 2: Multi-Table Transaction

**ODBC Multiple Statements:**

```
UPDATE Orders SET Status='Shipped' WHERE OrderID=123
INSERT INTO ShipmentLog VALUES (123, NOW(), 'USER123')
UPDATE Suppliers SET LastShipmentDate=NOW() WHERE SupplierID=123
```

**API Endpoint:**

```
POST /api/orders/123/ship
{}
```

**Implementation:**

```python
def ship_order(order_id: str, user_id: str):
    with db.transaction():
        db.orders.update(order_id, {'status': 'Shipped'})
        db.shipment_log.create({
            'order_id': order_id,
            'timestamp': datetime.now(),
            'user': user_id
        })
        # Update supplier last shipment date
        order = db.orders.get(order_id)
        db.suppliers.update(order['supplier_id'], {
            'last_shipment_date': datetime.now()
        })
```

## Requirements

- **API Framework**: Choose one for your target platform
  - Python: Flask, FastAPI, Django
  - Node.js: Express, NestJS
  - Java: Spring Boot

- **Database Driver**: For target system
  - PostgreSQL, MySQL, SQL Server client libraries
  - MongoDB drivers, etc.

- **HTTP Client Libraries**: For calling code migration
  - Python: `requests` library
  - Node.js: `axios`, `node-fetch`
  - VB/VBScript: `MSXML2.XMLHTTP`, WinHTTP
  - Java: `HttpClient`, Spring `RestTemplate`

- **Authentication**: Decide on auth mechanism
  - OAuth 2.0 / Bearer tokens
  - API keys
  - mTLS certificates

## See Also

- [lotus-analyze-nsf-structure](../lotus-analyze-nsf-structure/SKILL.md) - Understanding NSF database structures before replacement
- [lotus-migration](../lotus-migration/SKILL.md) - Comprehensive migration approach
- [lotus-convert-rich-text-fields](../lotus-convert-rich-text-fields/SKILL.md) - Converting formatted data fields
