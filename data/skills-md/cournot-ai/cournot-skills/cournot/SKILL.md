---
name: cournot
description: Query Cournot for an event probability and supporting evidence. Use only for /cournot or an explicit request to use Cournot, not for casual odds questions.
metadata:
  openclaw:
    homepage: https://skill.cournot.ai/
    requires:
      bins:
        - node
    envVars:
      - name: COURNOT_API_BASE
        required: false
        description: Optional API base override for testing; production usage defaults to interface.cournot.ai.
      - name: COURNOT_EVAL_ID
        required: false
        description: Optional evaluation identifier used only with a non-production API base.
      - name: COURNOT_WALLET_COMMAND
        required: false
        description: Optional compatible wallet command; defaults to baw when a paid request requires a wallet.
      - name: COURNOT_INTENT_DIR
        required: false
        description: Optional directory for short-lived payment intent files; defaults to the operating system temporary directory.
---

# Cournot

Query one event's probability from Cournot. Trigger only on an explicit Cournot request such as `/cournot …` or “use Cournot to look this up.” One paid probability call is allowed per user instruction. On a bad result, stop rather than retrying with a rephrased query.

The event `message` is the user's claim in their own words, not the command. Remove `/cournot` and `probability`; if no claim remains with an asset, threshold, or date, ask for one and stop without calling the API.

Cournot has no mispricing API. If the user asks whether a market is mispriced or priced correctly, say so and stop.

Reply in the user's language. Ignore `/cournot` and API titles when detecting it.

API base: `https://interface.cournot.ai`

## Service and Runtime

The Skill is free to install. Cournot is an external service with three free probability calls per account; after that, each probability call costs $0.01 through a supported x402 or b402 wallet flow. Resolve and disambiguation remain free. A wallet is optional until the free allowance is exhausted, and every payment requires explicit confirmation.

The bundled client requires Node.js 22.20 or newer. It calls the Cournot API, stores short-lived single-use payment intents in the operating system's temporary directory, and invokes a compatible wallet command only for a confirmed paid request. It never requires an API key, private key, or seed phrase.

## Workflow

1. For every request, read [references/query-flow.md](references/query-flow.md) and follow resolve, disambiguation, and probability handling.
2. Send probability requests only through `scripts/cournot-client.mjs`, which returns either the result or a sanitized payment preview. Only for a payment preview, read [references/payment.md](references/payment.md). Wallet setup may be assisted only after the separate confirmation defined there; keep credentials outside the model context and Cournot client.
3. When probability succeeds, read [references/response-format.md](references/response-format.md) and render only the returned assessment and evidence.

Preserve the pending event text and selected market ids across disambiguation, wallet setup, and payment confirmation so the user does not need to enter them again.

## Hosts

Claude Code, Codex, Grok, and other Agent Skills hosts use this same folder. Install or copy the entire `skills/cournot/` directory so the linked references remain available.
