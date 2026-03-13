---
name: paystack-disputes
description: >-
  Paystack Disputes API — manage transaction disputes (chargebacks) on your integration.
  List, fetch, update, resolve, and export disputes. Provide evidence, upload supporting
  documents, and handle resolution workflows. Use this skill whenever dealing with
  chargebacks, dispute management, fraud claims, refund disputes, providing evidence for
  contested transactions, or monitoring dispute status. Also use when you see references
  to /dispute endpoint, dispute statuses (awaiting-merchant-feedback, pending, resolved),
  or need to upload dispute evidence files.
---

# Paystack Disputes

The Disputes API lets you manage chargebacks and disputes on your integration.

> Depends on: **paystack-setup** for the `paystackRequest` helper.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/dispute` | List disputes |
| GET | `/dispute/:id` | Fetch a dispute |
| GET | `/dispute/transaction/:id` | List disputes for a transaction |
| PUT | `/dispute/:id` | Update a dispute |
| POST | `/dispute/:id/evidence` | Add evidence |
| GET | `/dispute/:id/upload_url` | Get upload URL for attachment |
| PUT | `/dispute/:id/resolve` | Resolve a dispute |
| GET | `/dispute/export` | Export disputes |

## Dispute Statuses

| Status | Description |
| --- | --- |
| `awaiting-merchant-feedback` | Paystack is waiting for your response |
| `awaiting-bank-feedback` | Bank is reviewing evidence |
| `pending` | Dispute is being processed |
| `resolved` | Dispute has been resolved |

## List Disputes

```typescript
const disputes = await paystackRequest(
  "/dispute?from=2024-01-01&to=2024-12-31&status=awaiting-merchant-feedback"
);
```

## Fetch Dispute

```typescript
const dispute = await paystackRequest(`/dispute/${disputeId}`);
```

## List Disputes for a Transaction

```typescript
const txDisputes = await paystackRequest(`/dispute/transaction/${transactionId}`);
// Returns { history: [...], messages: [...] }
```

## Update Dispute

Accept a dispute and set refund amount:

```typescript
await paystackRequest(`/dispute/${disputeId}`, {
  method: "PUT",
  body: JSON.stringify({
    refund_amount: 1002, // Amount in subunits
    uploaded_filename: "qesp8a4df1xejihd9x5q", // From upload URL
  }),
});
```

## Add Evidence

```typescript
await paystackRequest(`/dispute/${disputeId}/evidence`, {
  method: "POST",
  body: JSON.stringify({
    customer_email: "customer@email.com",
    customer_name: "John Doe",
    customer_phone: "0802345167",
    service_details: "Customer purchased premium plan on Jan 5",
    delivery_address: "123 Main Street, Lagos",
    delivery_date: "2024-01-06",
  }),
});
```

## Get Upload URL

```typescript
const upload = await paystackRequest(
  `/dispute/${disputeId}/upload_url?upload_filename=receipt.pdf`
);
// upload.data.signedUrl → Use PUT to upload file to this S3 URL
// upload.data.fileName → Reference this in update/resolve calls
```

## Resolve Dispute

```typescript
await paystackRequest(`/dispute/${disputeId}/resolve`, {
  method: "PUT",
  body: JSON.stringify({
    resolution: "merchant-accepted", // or "declined"
    message: "Customer refund approved",
    refund_amount: 500000,
    uploaded_filename: "uploaded_file_ref",
    evidence: 21, // Evidence ID (optional, for fraud claims)
  }),
});
```

## Export Disputes

```typescript
const exported = await paystackRequest(
  "/dispute/export?from=2024-01-01&to=2024-12-31"
);
// exported.data.path → CSV download URL
```

## Full Dispute Handling Flow

```typescript
// 1. List pending disputes
const disputes = await paystackRequest(
  "/dispute?status=awaiting-merchant-feedback"
);

for (const dispute of disputes.data) {
  // 2. Get upload URL for evidence
  const upload = await paystackRequest(
    `/dispute/${dispute.id}/upload_url?upload_filename=evidence.pdf`
  );

  // 3. Upload file to signed URL (use your preferred HTTP client)
  // await uploadToS3(upload.data.signedUrl, fileBuffer);

  // 4. Add evidence
  await paystackRequest(`/dispute/${dispute.id}/evidence`, {
    method: "POST",
    body: JSON.stringify({
      customer_email: "customer@email.com",
      customer_name: "Customer Name",
      customer_phone: "08012345678",
      service_details: "Service was delivered successfully",
    }),
  });

  // 5. Resolve — decline the chargeback
  await paystackRequest(`/dispute/${dispute.id}/resolve`, {
    method: "PUT",
    body: JSON.stringify({
      resolution: "declined",
      message: "Service was delivered. Evidence attached.",
      refund_amount: 0,
      uploaded_filename: upload.data.fileName,
    }),
  });
}
```
