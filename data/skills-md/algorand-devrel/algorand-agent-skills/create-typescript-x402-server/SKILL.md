---
name: create-typescript-x402-server
description: Create x402 payment-protected servers with Express.js and Hono. Use when building a resource server that returns 402 Payment Required, setting up payment middleware, configuring protected routes, implementing multi-network support (AVM+EVM+SVM), integrating paywall UI, building facilitator servers, or implementing dynamic pricing. Strong triggers include "create an x402 server", "add payment middleware to Express", "protect routes with x402", "set up payment-gated API", "hono payment middleware", "402 payment required server", "x402 express server", "x402 hono server", "build a facilitator server", "fee abstraction server".
---

# Creating x402 Payment-Protected Servers

Build TypeScript servers that gate API endpoints behind Algorand (AVM) payments using Express.js or Hono middleware.

## Prerequisites

Before creating a payment-protected server:

1. **Node.js 18+** installed
2. **An Algorand address** to receive payments (58-character address)
3. **A facilitator** -- either run your own or use `https://facilitator.goplausible.xyz`
4. **TypeScript project** initialized with `tsconfig.json`

## Core Workflow: Middleware-Based Payment Gating

The server middleware intercepts requests to protected routes, checks for a valid `X-PAYMENT` header, and either returns 402 (pay first) or passes through to the route handler (payment verified).

```
Request → Middleware checks X-PAYMENT header
  ├── No header → Return 402 with PaymentRequirements
  ├── Has header → Forward to facilitator
  │     ├── verify() fails → Return 402
  │     └── verify() passes → settle() → Pass to route handler
  └── Route not protected → Pass through
```

## How to Proceed

### Step 1: Install Dependencies

**Express.js:**
```bash
npm install @x402-avm/express @x402-avm/avm @x402-avm/core express
npm install -D @types/express typescript
```

**Hono:**
```bash
npm install @x402-avm/hono @x402-avm/avm @x402-avm/core hono
npm install -D typescript
```

**Hono with Node.js server:**
```bash
npm install @x402-avm/hono @x402-avm/avm @x402-avm/core hono @hono/node-server
```

**With paywall UI (optional):**
```bash
npm install @x402-avm/paywall
```

### Step 2: Choose a Middleware Variant

There are three middleware variants, from simplest to most configurable:

| Variant | Use Case | What It Creates |
|---------|----------|-----------------|
| `paymentMiddlewareFromConfig` | Quick start, simple apps | Creates x402ResourceServer internally |
| `paymentMiddleware` | Need custom server config | Uses your x402ResourceServer instance |
| `paymentMiddlewareFromHTTPServer` | Need hooks (API key bypass, logging) | Uses x402HTTPResourceServer with hooks |

### Step 3: Define Routes

Routes map HTTP method + path patterns to payment configuration:

```typescript
import { ALGORAND_TESTNET_CAIP2 } from "@x402-avm/avm";

const routes = {
  "GET /api/weather": {
    accepts: {
      scheme: "exact",
      network: ALGORAND_TESTNET_CAIP2,
      payTo: "YOUR_ALGORAND_ADDRESS",
      price: "$0.01",
    },
    description: "Weather data",
  },
  "GET /api/premium/*": {
    accepts: {
      scheme: "exact",
      network: ALGORAND_TESTNET_CAIP2,
      payTo: "YOUR_ALGORAND_ADDRESS",
      price: "$0.10",
    },
    description: "Premium API endpoints",
  },
};
```

### Step 4: Apply Middleware (Express)

```typescript
import express from "express";
import { paymentMiddleware, x402ResourceServer } from "@x402-avm/express";
import { registerExactAvmScheme } from "@x402-avm/avm/exact/server";
import { HTTPFacilitatorClient } from "@x402-avm/core/server";

const app = express();

const facilitatorClient = new HTTPFacilitatorClient({
  url: process.env.FACILITATOR_URL || "https://facilitator.goplausible.xyz",
});
const server = new x402ResourceServer(facilitatorClient);
registerExactAvmScheme(server);

app.use(paymentMiddleware(routes, server));

app.get("/api/weather", (req, res) => {
  res.json({ temperature: 72, condition: "sunny" });
});

app.listen(4021);
```

### Step 4 (Alternative): Apply Middleware (Hono)

```typescript
import { Hono } from "hono";
import { paymentMiddleware, x402ResourceServer } from "@x402-avm/hono";
import { registerExactAvmScheme } from "@x402-avm/avm/exact/server";
import { HTTPFacilitatorClient } from "@x402-avm/core/server";

const app = new Hono();

const facilitatorClient = new HTTPFacilitatorClient({
  url: process.env.FACILITATOR_URL || "https://facilitator.goplausible.xyz",
});
const server = new x402ResourceServer(facilitatorClient);
registerExactAvmScheme(server);

app.use(paymentMiddleware(routes, server));

app.get("/api/weather", (c) => {
  return c.json({ temperature: 72, condition: "sunny" });
});

export default app;
```

### Step 5: Add a Facilitator Server (Optional)

If you need your own facilitator instead of the public one:

```typescript
import express from "express";
import { x402Facilitator } from "@x402-avm/core/facilitator";
import { registerExactAvmScheme } from "@x402-avm/avm/exact/facilitator";
import { ALGORAND_TESTNET_CAIP2 } from "@x402-avm/avm";
import algosdk from "algosdk";

const secretKey = Buffer.from(process.env.AVM_PRIVATE_KEY!, "base64");
const address = algosdk.encodeAddress(secretKey.slice(32));
const algodClient = new algosdk.Algodv2("", "https://testnet-api.algonode.cloud", "");

// Create signer implementing FacilitatorAvmSigner interface
const signer = { /* ... see EXAMPLES.md for full implementation ... */ };

const facilitator = new x402Facilitator();
registerExactAvmScheme(facilitator, { signer, networks: ALGORAND_TESTNET_CAIP2 });

const app = express();
app.use(express.json());
app.post("/verify", async (req, res) => { /* ... */ });
app.post("/settle", async (req, res) => { /* ... */ });
app.get("/supported", (req, res) => { /* ... */ });
app.listen(4020);
```

### Step 6: Set Environment Variables

```bash
# Resource Server
AVM_ADDRESS=YOUR_ALGORAND_ADDRESS_HERE
FACILITATOR_URL=https://facilitator.goplausible.xyz
PORT=4021

# Facilitator (if running your own)
AVM_PRIVATE_KEY=<base64-encoded-64-byte-key>
ALGOD_SERVER=https://testnet-api.algonode.cloud
ALGOD_TOKEN=
FACILITATOR_PORT=4020
```

## Important Rules / Guidelines

1. **Register AVM scheme unconditionally** -- always call `registerExactAvmScheme(server)` without environment variable guards
2. **Public routes are unaffected** -- only routes listed in the `routes` config object are protected
3. **Route patterns support wildcards** -- `"GET /api/premium/*"` matches all sub-paths
4. **Method prefix is optional** -- `"/api/resource"` matches all HTTP methods
5. **Multi-network routes use arrays** -- pass an array to `accepts` for cross-chain support
6. **Facilitator URL is required** -- the resource server must be able to reach a facilitator
7. **Price strings use USD notation** -- `"$0.01"` is resolved to the appropriate asset amount

## Common Errors / Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| All routes return 402 | Route patterns too broad | Check route patterns match intended paths |
| 402 but no `accepts` array | AVM scheme not registered on server | Call `registerExactAvmScheme(server)` |
| Facilitator unreachable | Wrong URL or facilitator not running | Check `FACILITATOR_URL` and facilitator status |
| `paymentMiddleware is not a function` | Wrong import | Import from `@x402-avm/express` or `@x402-avm/hono` |
| CORS errors in browser | Missing CORS middleware | Add `cors()` middleware before payment middleware |
| Paywall not showing | Missing `mimeType: "text/html"` | Set `mimeType` in route config for browser routes |
| Dynamic price error | Price function throws | Ensure price function handles all edge cases |
| 500 on verify/settle | Facilitator signer error | Check facilitator logs, verify private key |

## References / Further Reading

- [REFERENCE.md](./references/REFERENCE.md) - Detailed middleware API reference
- [EXAMPLES.md](./references/EXAMPLES.md) - Complete server code examples
- [@x402-avm/express on npm](https://www.npmjs.com/package/@x402-avm/express)
- [@x402-avm/hono on npm](https://www.npmjs.com/package/@x402-avm/hono)
- [GoPlausible x402-avm Examples](https://github.com/GoPlausible/x402-avm/tree/branch-v2-algorand-publish/examples/)
- [GoPlausible x402-avm Documentation](https://github.com/GoPlausible/.github/blob/main/profile/algorand-x402-documentation/)
