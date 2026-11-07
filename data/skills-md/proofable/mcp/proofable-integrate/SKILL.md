---
name: proofable-integrate
description: Add Proofable access control to a host app. Define a Gate Policy in code, drop in the gate widget, wire the server check, and test the flow. Use when a developer wants to gate content or add proof-based checks.
license: Apache-2.0
compatibility: Requires @proofable/sdk (npm).
metadata:
  author: Proofable
  version: "0.1.7"
  homepage: https://docs.proofable.me/use-cases/gate-access
---

# Integrate Proofable

Add proof-based access control in four steps. Define the policy in the app. A published `gateId` is optional.

## Ask once

Before writing code, ask the developer:

1. **What framework?** (Next.js, Vite/React, Express, other)
2. **What must already be proven?** Start with a verifier id such as `proof-of-human`. A dashboard listing is not required.

Do not ask about Proofable architecture, proof schemas, wallet setup, or credential choices.

## Install

```bash
npm install @proofable/sdk
```

If the app uses React, also ensure `react` and `react-dom` are installed (peer deps).

## Define the policy

```js
import { defineGate } from '@proofable/sdk';

const gate = defineGate([{ verifierId: 'proof-of-human' }]);
```

## Browser: gate the content

### React (Next.js, Vite, CRA)

```jsx
import { VerifyGate, ProofBadge } from '@proofable/sdk/widgets';

function ProtectedPage({ gate }) {
  return (
    <VerifyGate gate={gate} onVerified={grantAccess}>
      <ProtectedContent />
    </VerifyGate>
  );
}
```

`VerifyGate` checks for an existing proof, opens hosted sign-in on proofable.me when a new one is needed, then renders the children.

Optional: show proof status anywhere with `<ProofBadge qHash={proof.qHash} />`.

### Non-React (redirect flow)

```js
import { getHostedCheckoutUrl } from '@proofable/sdk';

window.location.assign(
  getHostedCheckoutUrl({
    verifiers: ['proof-of-human'],
    returnUrl: 'https://app.example.com/auth/callback',
  }),
);
```

Read the proof ID (`qHash`) from the callback URL query string, then store it.

## Server: confirm access

Before granting access, confirm the subject still satisfies the policy.

```js
import { ProofableClient } from '@proofable/sdk';

const client = new ProofableClient();
const result = await client.gateCheck({
  gate,
  subject: { accountId: user.accountAddress },
});

if (!result.satisfied) {
  // send the user back to VerifyGate or Proofable sign-in
}
```

For server-only apps or CI, use a server key: `new ProofableClient({ apiKey: 'npk_...' })`. Create keys at proofable.me → profile → Account → Access keys. Never paste keys into chat or committed files.

## Test

1. Run the app and navigate to the gated page.
2. Confirm `VerifyGate` opens the Proofable sign-in flow.
3. Complete sign-in (wallet, passkey, or OAuth all work).
4. Confirm the gated content renders.
5. Call `gateCheck` from the server. Confirm `satisfied` is `true`.

## Copy rules

User-visible strings in the app should use plain language:

- "gate" or "access", not "verifier" or "trust check"
- "proof", not "qHash" or "portable proof" in UI text
- "Sign in" or "Connect", not "mount" or "authenticate"
- "Your account", not "wallet" or "DID" unless the user specifically chose a wallet flow

Full copy guide: [references/quickstart.md](references/quickstart.md)

## When to stop

The integration is complete when:

1. `VerifyGate` renders on the gated page.
2. A visitor can sign in and see protected content.
3. The server `gateCheck` call returns `satisfied: true` for a verified visitor.
4. No Proofable jargon appears in user-visible strings.

Do not add extra Proofable concepts, tools, or surfaces unless the developer asks.

Docs: [Getting started](https://docs.proofable.me), [Gate access](https://docs.proofable.me/use-cases/gate-access)
