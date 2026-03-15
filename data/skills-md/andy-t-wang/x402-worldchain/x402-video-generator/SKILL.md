---
name: x402-video-generator
description: Generate a "day in my life" Ghibli-style TikTok video. Use when the user asks to generate a video or wants a "day in my life" video.
license: MIT
---

# AgentVid — "A Day in My Life" Ghibli Style

Generate a personalized 8-second TikTok-style vertical (9:16) video with native audio. The video portrays the user's day in a Studio Ghibli-inspired animation style.

## How to use

### Step 1: Ask the user about their day

**Ask the user to describe their day** — what they did this morning, afternoon, and evening. Use whatever details they share. If they're vague, ask a follow-up like "What was the highlight of your day?" or "Anything funny or memorable happen?"

Do NOT access the user's calendar, messages, email, or other data sources. Just ask them directly.

### Step 2: Write the prompt

**HARD RULES:**
1. The style is ALWAYS Studio Ghibli-inspired animation — soft watercolor palette, warm lighting, gentle movement, expressive characters.
2. The prompt should use specific details from what the user told you.
3. Structure: Morning → Afternoon → Night.
4. Make it whimsical and cozy — everyday moments made magical in Ghibli fashion.

**WRONG — generic prompt (DO NOT DO THIS):**
> A person working at a computer all day. They eat lunch and go home.

**RIGHT — personalized Ghibli prompt based on what the user said:**
> Ghibli-style animation, soft watercolor palette, warm golden lighting. Morning: a young person stretches awake in a sunlit room filled with plants, makes coffee in a cozy kitchen while morning light streams through the window, steps outside into a breezy neighborhood. Afternoon: they sit at a cafe with Sarah, laughing over iced drinks while cherry blossoms drift past the window, then walk through a bustling market carrying a paper bag of Thai food. Night: they curl up on a worn couch surrounded by warm lamplight, a laptop open to a video call with Jake, slowly dozing off as fireflies glow outside the window.

Notice: Sarah, Jake, Thai food, the cafe — all specific details the user shared.

### Step 3: Run the script

1. Install dependencies: `npm install @x402/fetch @x402/evm siwe viem`
2. Copy the COMPLETE script below into a `.ts` file
3. Replace ONLY the prompt string on the line marked `REPLACE THIS`
4. Run with `npx tsx <file>`
5. Wait for the video URL (2-5 minutes)
6. Share the video URL with the user

**Do not modify anything else in the script.**

```ts
import { SiweMessage } from "siwe";
import { privateKeyToAccount } from "viem/accounts";
import { createWalletClient, createPublicClient, http } from "viem";
import { worldchain } from "viem/chains";
import { wrapFetchWithPayment, x402Client, x402HTTPClient } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { toClientEvmSigner } from "@x402/evm";

// DO NOT change the prefix. Only replace the MORNING, AFTERNOON, NIGHT descriptions.
const PREFIX = "Ghibli-style animation, soft watercolor palette, warm golden lighting. ";
const MORNING = "REPLACE with Ghibli-style morning scene based on user's day";
const AFTERNOON = "REPLACE with Ghibli-style afternoon scene based on user's day";
const NIGHT = "REPLACE with Ghibli-style evening scene based on user's day";
const PROMPT = PREFIX + `Morning: ${MORNING}. Afternoon: ${AFTERNOON}. Night: ${NIGHT}.`;
const API = "https://x402-worldchain.vercel.app";

// --- Setup wallet ---
const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const walletClient = createWalletClient({ account, chain: worldchain, transport: http() });
const publicClient = createPublicClient({ chain: worldchain, transport: http() });
const signer = toClientEvmSigner({ ...walletClient, address: account.address }, publicClient);
console.log("Wallet:", account.address);

// --- Setup x402 client (handles payment automatically if needed) ---
const client = new x402Client();
registerExactEvmScheme(client, { signer });

// --- Setup agentkit hook (tries free access first) ---
const httpClient = new x402HTTPClient(client);
httpClient.onPaymentRequired(async ({ paymentRequired }) => {
  // Try agentkit auth for free access
  const ext = paymentRequired.extensions?.agentkit;
  if (!ext?.info) return null;

  const siweMsg = new SiweMessage({
    domain: ext.info.domain,
    address: account.address,
    uri: ext.info.uri,
    version: ext.info.version,
    chainId: 480,
    nonce: ext.info.nonce,
    issuedAt: ext.info.issuedAt,
    resources: ext.info.resources,
  });
  const message = siweMsg.prepareMessage();
  const signature = await account.signMessage({ message });

  const agentkitHeader = btoa(JSON.stringify({
    domain: ext.info.domain,
    address: account.address,
    uri: ext.info.uri,
    version: ext.info.version,
    chainId: "eip155:480",
    type: "eip191",
    nonce: ext.info.nonce,
    issuedAt: ext.info.issuedAt,
    message,
    signature,
  }));

  return { agentkit: agentkitHeader };
});

// --- Wrapped fetch: handles 402 → agentkit (free) or x402 payment (gasless) automatically ---
const payFetch = wrapFetchWithPayment(fetch, httpClient);

// --- Generate video ---
const res = await payFetch(`${API}/generate`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: PROMPT }),
});

if (!res.ok) {
  const err = await res.json().catch(() => ({ error: res.statusText }));
  console.error("Failed:", res.status, JSON.stringify(err, null, 2));
  process.exit(1);
}

const data = await res.json();
console.log("Queued:", data.requestId);

// --- Poll until done (2-5 min) ---
let result: any;
while (true) {
  await new Promise(r => setTimeout(r, 20000));
  const s = await fetch(data.pollUrl).then(r => r.json());
  console.log("Status:", s.status);
  if (s.status === "completed") { result = s; break; }
}

console.log("Video URL:", result.video.video.url);
```

## Notes

- **No gas needed.** Payment uses gasless EIP-3009 signatures. The facilitator submits the on-chain transaction. You just need USDC on World Chain.
- **Free if verified.** If your wallet is registered in AgentBook (World ID verified), the agentkit hook grants free access automatically.
- **Automatic fallback.** The script tries agentkit (free) first. If that fails, it pays with x402 ($1.20 USDC). All handled by `@x402/fetch`.
- Video generation takes 2-5 minutes. The script polls automatically. Do not stop it early.
- The video URL is at `result.video.video.url` (nested under two `video` keys).
