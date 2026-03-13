---
name: paystack-terminal
description: >-
  Paystack Terminal API — build in-person payment experiences with Paystack POS terminals.
  Send events (invoice/transaction), check terminal status, commission/decommission
  devices, and manage terminal details. Use this skill whenever integrating Paystack POS
  terminals, sending payment events to terminals, processing in-person payments, checking
  terminal availability, activating or deactivating terminal devices, or managing a fleet
  of POS terminals. Also use when you see references to /terminal endpoint, terminal_id,
  serial numbers, or event-based terminal communication.
---

# Paystack Terminal

The Terminal API lets you build in-person payment experiences with Paystack POS terminals.

> Depends on: **paystack-setup** for the `paystackRequest` helper.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/terminal/:terminal_id/event` | Send event to terminal |
| GET | `/terminal/:terminal_id/event/:event_id` | Check event delivery status |
| GET | `/terminal/:terminal_id/presence` | Check terminal availability |
| GET | `/terminal` | List terminals |
| GET | `/terminal/:terminal_id` | Fetch terminal details |
| PUT | `/terminal/:terminal_id` | Update terminal |
| POST | `/terminal/commission_device` | Commission (activate) terminal |
| POST | `/terminal/decommission_device` | Decommission (deactivate) terminal |

## Send Event to Terminal

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | Yes | `invoice` or `transaction` |
| `action` | string | Yes | For invoice: `process` or `view`. For transaction: `process` or `print` |
| `data` | object | Yes | Event data (see examples) |

```typescript
// Send invoice to terminal for processing
const event = await paystackRequest<{ id: string }>(
  `/terminal/${terminalId}/event`,
  {
    method: "POST",
    body: JSON.stringify({
      type: "invoice",
      action: "process",
      data: {
        id: 7895939,           // Invoice ID
        reference: 4634337895939, // Offline reference
      },
    }),
  }
);
// event.data.id → "616d721e8c5cd40a0cdd54a6"

// Print a transaction receipt
await paystackRequest(`/terminal/${terminalId}/event`, {
  method: "POST",
  body: JSON.stringify({
    type: "transaction",
    action: "print",
    data: { id: transactionId },
  }),
});
```

## Check Event Status

```typescript
const status = await paystackRequest<{ delivered: boolean }>(
  `/terminal/${terminalId}/event/${eventId}`
);
// status.data.delivered → true
```

## Check Terminal Availability

Always check before sending events:

```typescript
const presence = await paystackRequest<{
  online: boolean;
  available: boolean;
}>(`/terminal/${terminalId}/presence`);

if (presence.data.online && presence.data.available) {
  // Send event to terminal
}
```

## List Terminals

Uses cursor pagination:

```typescript
const terminals = await paystackRequest("/terminal?perPage=50");
// terminals.meta.next → cursor for next page
// terminals.meta.previous → cursor for previous page
```

## Fetch Terminal

```typescript
const terminal = await paystackRequest(`/terminal/${terminalId}`);
// terminal.data: { id, serial_number, terminal_id, name, address, status }
```

## Update Terminal

```typescript
await paystackRequest(`/terminal/${terminalId}`, {
  method: "PUT",
  body: JSON.stringify({
    name: "Front Desk Terminal",
    address: "123 Main Street, Lagos",
  }),
});
```

## Commission / Decommission

```typescript
// Activate a new terminal
await paystackRequest("/terminal/commission_device", {
  method: "POST",
  body: JSON.stringify({ serial_number: "1111150412230003899" }),
});

// Deactivate a terminal
await paystackRequest("/terminal/decommission_device", {
  method: "POST",
  body: JSON.stringify({ serial_number: "1111150412230003899" }),
});
```
