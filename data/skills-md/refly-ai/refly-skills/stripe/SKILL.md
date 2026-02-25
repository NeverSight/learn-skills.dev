---
name: stripe
description: "Integrate with Stripe for payment processing. Use when you need to: (1) manage customers and payments, (2) create invoices and subscriptions, or (3) automate billing workflows."
version: 1.0.0
skillId: skp-mfyz61qqatnfv05xj9nruiom
workflowId: c-ng1d926qh9pder6anqky106c
installationId: skpi-tunc82wqp4miz5uo8bqes7ls
category: action
---

# Stripe

Integrate with Stripe for payment processing. Use when you need to: (1) manage customers and payments, (2) create invoices and subscriptions, or (3) automate billing workflows.

## Input

Provide input as JSON:

```json
{
  "customer_email": "Email address of the customer to manage",
  "customer_name": "Full name of the customer",
  "payment_amount": "Payment amount in cents (e.g., 5000 for $50.00)",
  "currency": "Currency code (e.g., usd, eur, gbp)",
  "invoice_description": "Description for the invoice"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-tunc82wqp4miz5uo8bqes7ls --input '{
  "amount": "2000",
  "currency": "usd",
  "customer_email": "customer@example.com"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-ng1d926qh9pder6anqky106c"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm payment processed
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON payment data (payment ID, status)
- **Action**: Confirm payment processed successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
