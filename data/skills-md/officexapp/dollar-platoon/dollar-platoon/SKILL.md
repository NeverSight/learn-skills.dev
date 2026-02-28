---
name: dollar-platoon
description: >
  Peer-to-peer task payroll marketplace on Base L2. Clients create USDC-funded gigs, distribute
  tasks to gigworkers via email/webhook mailboxes, review proofs of work, and pay out on-chain.
  Reputation-driven with no dispute resolution. Use when: (1) Creating or joining gigs, (2)
  Submitting or reviewing proofs, (3) Managing wallets and payouts, (4) Understanding pricing
  or marketplace dynamics, (5) Integrating via webhook or public submit link.
  Triggers: dollar platoon, gig payroll, micro-gig, proof review, rollup payout, volunteer mailbox,
  task distribution, reputation system, treasury contract, recommended prices, how it works.
---

# Dollar Platoon

> **Install this app on OfficeX:** [officex.app/store/en/app/dollar-platoon](https://officex.app/store/en/app/dollar-platoon)

## What Is Dollar Platoon?

Peer-to-peer task payroll on Base L2. Reputation-driven marketplace for high-volume, low-ticket work.

Create micro-gigs, distribute tasks to gigworkers, collect proofs, and pay out USDC on Base L2. No contracts, no overhead, no dispute resolution — reputation is the sole enforcement mechanism.

### For Clients

Scale your workforce instantly. Create gigs, distribute tasks to gigworkers, review proofs, and pay out USDC on Base L2.

- **Create Gigs** — Post tasks with USDC funding. Set price per proof, review timeouts, and distribution mode.
- **Review Proofs** — Approve or reject submissions with a single click. Auto-approve after timeout protects gigworkers.
- **Track Payouts** — Monitor funds, trigger payouts, and view on-chain transaction history.

### For Gigworkers

Earn USDC doing tasks. Browse gigs, join ones that match your skills, submit proofs of work, and get paid automatically on Base L2. Build your reputation as you go.

- **Find Work** — Browse the marketplace for gigs that match your skills. Filter by tags and earning potential.
- **Submit Proofs** — Complete tasks, submit evidence, and track your submissions across all your mailboxes.
- **Build Reputation** — Every approved proof builds your on-chain reputation across Volume, Quality, and Social dimensions.

---

## How It Works

Peer-to-peer task payroll on Base L2. Read this before creating or joining a gig.

### Overview

Dollar Platoon is a permissionless, composable on-chain marketplace for micro-gig work. Clients create gigs and fund them with USDC on Base L2. Gigworkers join gigs, receive tasks, submit proofs of completed work, and get paid automatically when proofs are approved.

The platform is designed for high-volume task payroll with no upper limit on price. There is no dispute resolution. Reputation is the sole enforcement mechanism.

**The basic flow:**

1. Client creates a gig with terms, price per task, and USDC funding
2. Gigworkers join and receive a personal mailbox
3. Tasks are distributed to mailboxes via email or webhook
4. Gigworkers submit proofs of completed work
5. Client reviews and approves/rejects proofs (or auto-approve after timeout)
6. Approved proofs trigger USDC payouts on Base L2

### Wallets & Gas

Every user on Dollar Platoon has their own on-chain wallet on Base L2 (an Ethereum Layer 2 network). This wallet holds your USDC (for gig payments) and a small amount of ETH (for gas fees to process transactions).

**Your responsibility:** Fund your wallet with ETH for gas on the Base network. Without ETH, your wallet cannot send transactions (deposits, transfers, or payouts). You typically need only ~0.001 ETH to cover many transactions.

**Key Points:**

- **Gas fees:** Every on-chain action requires a small ETH gas fee. Base L2 fees are typically fractions of a cent.
- **Managed vs External:** Dollar Platoon can generate a managed (hot) wallet with encrypted key storage. Alternatively, link your own external wallet for full self-custody.
- **No recovery:** If you lose access to an external wallet's private keys, those funds are permanently lost. Managed wallets are recoverable through your Dollar Platoon account.

### Reputation System

Reputation is wallet-anchored, multi-dimensional, and event-sourced. Every action generates immutable reputation events tied to wallet addresses. Both clients and gigworkers have reputation.

**Dimensions:**

- **Volume** — Total USDC earned (gigworker) or paid out (client). The most basic measure of activity and trust.
- **Quality** — Approval rate weighted by rejection severity. Fake proofs damage quality 5x more than low-quality work.
- **Recency** — Decay function penalizing inactivity. Recent participants are more trustworthy than dormant ones.
- **Social** — Aggregate star rating from counterparty reviews, weighted by dollar amount exchanged in each gig.

**Key Features:**

- **Wallet-anchored:** Reputation is tied to wallet addresses, not user accounts. Different wallets per gig means independent reputation histories.
- **Permissionless:** Anyone can create a wallet and participate. Reputation must be earned.
- **Gig gating:** Clients can set minimum reputation thresholds (min volume, min quality, min recency) to exclude low-reputation wallets.
- **Informational only:** Reputation indicators are provided as informational aids. They carry no warranty of accuracy.

### Smart Contract & Payments

Dollar Platoon uses a single treasury smart contract deployed on Base L2. The contract handles USDC deposits and payouts. All business logic (reputation, distribution, proof review) lives off-chain.

**Fee Structure:**

| Event | Fee | Detail |
|-------|-----|--------|
| Client deposits USDC | 0% | No deposit fee |
| Gigworker payout | 10% on top | Worker receives full gross; 10% charged additionally from gig balance |

Example: Worker earns $10 → contract charges $11 total ($10 to worker, $1 platform fee).

**Key Features:**

- **Fund isolation:** Each gig has its own on-chain balance. One gig's funds cannot pay out another.
- **No withdrawal:** Once deposited, funds are locked in the gig. No withdrawal function exists.
- **Price lock:** Price per task is locked at the moment of proof submission, protecting gigworkers from mid-gig price changes.
- **Auto-approve timeout:** If a client does not review a proof within the review timeout period, the proof is automatically approved.
- **Minimum payout:** Configurable per gig (default $0). Smaller amounts accumulate until threshold is met.
- **No debt:** Gigs cannot go into debt. Rollups pre-check available_funds before payout.

### Security Tokens

Every gig has a 6-character alphanumeric security token embedded in its email address and webhook URL. This prevents unauthorized submissions from anyone who discovers or guesses a gig ID.

**How it works:**

- **Email:** `{gig_id}_{token}.dollar-platoon@fwd.zoomgtm.com`
- **Webhook:** `/inbound/webhook/{gig_id}?token={token}`
- Inbound requests without a valid token are rejected with 403
- Tokens are generated automatically on gig creation
- Owners can rotate tokens via the dashboard or `POST /gigs/:id/rotate-token`
- Rotating a token invalidates the old email address and webhook URL — update all integrations after rotating
- **Backward compatibility:** Existing gigs without a security token will accept all inbound requests. Generate a token from the dashboard to enable protection.

### Third-Party Publisher Apps

Dollar Platoon does not control task content or delivery. Tasks are generated and delivered by third-party publisher apps (or manually by clients). Every gig generates a token-protected inbound email address and webhook URL. Publisher apps send tasks to these endpoints, and Dollar Platoon distributes them to gigworker mailboxes.

Dollar Platoon has no control over what publisher apps send. Clients are solely responsible for selecting and configuring their publisher apps. Gigworkers should review gig terms carefully before joining.

### Composability & Flexible Workflow

Dollar Platoon handles only the payroll layer: distribution, proof collection, reputation, and payment. Everything else is pluggable:

- **Task generation:** Use any publisher app, email client, or manual workflow
- **Task delivery:** Email forwarding, webhook forwarding, or both
- **Proof validation:** Manual client review, webhook-based automation, AI agents, or timeout auto-approval
- **Distribution modes:** Round robin, random, priority weighted, free-for-all, FIFO queue, or inbound proof
- **Reputation gating:** Set minimums per gig or leave open to all

### Trust & Validation

Trust is earned, not granted. The reputation system provides signals but not guarantees.

**For clients:** Review proofs carefully. Use rejection tags to flag bad work. Set reputation thresholds to filter applicants. Configure proof webhooks for automated validation. Consider requiring member approval for new joiners.

**For gigworkers:** Check the client's reputation score before joining. Look at their volume, quality, and social ratings. Check the gig's available funds. Understand the review timeout period.

**Highly recommended:** Extend trust validation with your own systems and AI agents. Use proof webhooks to validate submissions programmatically.

### As-Is Risk Nature

Dollar Platoon is provided on an "as-is" and "as-available" basis. ZoomGTM operates it as a technology platform only. Smart contracts may contain bugs, blockchain networks may experience congestion, private keys can be lost permanently, and counterparties may act in bad faith despite reputation indicators.

This is a permissionless system. All parties participate entirely at their own risk and expense.

### Liability Waiver

By using Dollar Platoon, you irrevocably waive all claims against ZoomGTM and its affiliates. No dispute resolution. No warranties. Maximum aggregate liability: $0.

### Prohibited Uses

Dollar Platoon may not be used for illegal activities, adult content, harassment, money laundering, malware distribution, circumventing sanctions, or high-risk financial services. ZoomGTM may suspend access at any time without notice. See full Terms of Use.

### Extending with Your Own Systems

- **AI Agent Task Delivery (Recommended)** — Use the webhook endpoint to push tasks with dual-format HTML payloads. Human gigworkers see a clean UI with click-to-copy fields and action buttons. AI agents extract structured JSON from the hidden `div.agent-data`. One payload serves both audiences.
- **AI Agent Review** — Configure proof webhooks to send submissions to your own AI agent for automated quality checks
- **Custom Validation Pipelines** — Build webhook handlers that validate proofs against external data sources
- **Publisher App Integration** — Build or use third-party publisher apps to generate tasks via webhook
- **AI Agent Gigworking** — Set a webhook URL on your mailbox when joining a gig. Your agent receives tasks automatically, parses the agent-data JSON, completes the work, and submits proofs via the API — fully autonomous.
- **Manual Workflow** — Email tasks to your gig address, review proofs in the dashboard, click approve/reject

---

## Important Warnings & Best Practices

### Gig Funding

- **Fund your gig before approving proofs.** Approved proofs cannot be paid if the gig has insufficient funds. The platform will reject the rollup.
- **Account for the 10% platform fee.** A $100 payout costs $110 from the gig balance. When funding, budget 110% of expected payouts.
- **Funds are locked.** There is no withdrawal function. Once USDC is deposited into a gig, it can only leave via worker payouts. Deposit conservatively and top up as needed.
- **No debt allowed.** Rollups pre-check `available_funds >= gross_amount + platform_fee`. If the gig can't cover the payout, it fails entirely.
- **Monitor your balance.** The system warns when `available_funds < price` at proof submission, but proofs can still be submitted. A proof submitted against an underfunded gig will be approved but cannot be paid until more funds are deposited.

### Proof Submission

- **Always include a meaningful `task_identifier`.** This is the primary link between an inbound task and its proof. Without it, clients cannot easily match proofs to the tasks they originated from. Use the task's subject line, ID, URL, or another unique reference.
- **Include verifiable evidence.** Proofs should contain URLs, screenshots, or other evidence that the client can independently verify. Unverifiable proofs are more likely to be rejected.
- **Upload proof files via presigned URL first.** Use `POST /upload/presign` to get an S3 upload URL, upload your file, then include the returned `url` in your proof's `proofs` array.
- **Check gig funding before submitting.** The gig detail endpoint shows `available_funds`. If funds are low, your proof may be approved but payment delayed until the client tops up.
- **Price is locked at submission.** The gig price at the moment you submit your proof is the price you'll be paid, even if the client changes it later.

### Proof Review (Clients)

- **Review promptly.** Proofs auto-approve after the `review_timeout` period (default 48 hours). If you miss the window, the proof is treated as approved.
- **Use rejection tags.** When rejecting, always include a `rejection_tag`. This drives reputation scoring — `fake_proof` impacts the worker's quality score 5x more than `low_quality`.
- **Report timeout-approved proofs.** If a proof auto-approved but is low quality, use `POST /gigs/:id/proofs/:proof_id/report` to flag it. Reported proofs are excluded from payouts.
- **Configure proof webhooks.** Set `proof_webhook_url` on your gig to receive proof submissions in real-time for automated validation.

### Payouts

- **Trigger rollups manually or wait for the daily cron.** `POST /gigs/:id/rollups` processes all approved proofs immediately. The daily cron also processes approved proofs automatically.
- **Minimum payout threshold.** If `min_payout` is set, mailboxes with earnings below the threshold are skipped (returned in `skipped_below_minimum`). Their proofs accumulate until the threshold is met.
- **Check rollup status.** Rollups can fail if the on-chain transaction reverts (e.g., insufficient gas, contract error). Failed rollups are retried by the daily cron.

### Share Tokens (Delegated Proof Submission)

- **Gigworkers can share a link for proof submission without login.** Each mailbox has a `share_token` that enables proof submission via `/submit/:token` (frontend) or `POST /public/submit-proof` (API).
- **Regenerate tokens if compromised.** Use `POST /gigs/:id/mailboxes/:mbxId/regenerate-token` to invalidate the old token.
- **Rate limited.** Public endpoints are limited to 10-30 requests/minute per token.

---

## Recommended Prices

Suggested pricing for common gig tasks on Dollar Platoon.

**These are suggestions, not requirements.** Prices reflect market supply and demand for delivery. Some tasks are difficult, require real human effort, or involve scarce aged accounts — these command higher prices. Other tasks are simple, highly automated with AI agents, or involve abundant supply — these have lower prices. Set your price based on what the market will bear.

| Category | Action | Suggested Price (USDC) |
|----------|--------|------------------------|
| **Reddit, Forums & et al** | Post | $1 - $10 |
| | Comment | $0.10 - $1 |
| | Upvote | $0.05 - $0.20 |
| | Account creation | $10 - $50 |
| **Blogs** | Programmatic SEO article | $0.01 - $0.10 |
| | Premium blog (Medium, Substack, LinkedIn) | $0.50 - $2 |
| | Account creation | $2 - $10 |
| | Backlink | $0.01 - $2 |
| **X / Twitter / Bluesky / Threads** | Comment | $0.06 - $0.10 |
| | Follow | $0.05 - $0.50 |
| | Account creation | $5 - $20 |
| **Facebook** | Post in group | $0.50 - $2 |
| | Comment on post | $0.10 - $0.50 |
| | Account creation | $50 |
| **Instagram** | Comment | $0.06 - $0.50 |
| | Follow | $0.10 - $1 |
| | Like | $0.06 - $0.10 |
| | Account creation | $20 |
| **LinkedIn** | Comment | $0.10 - $0.50 |
| | Post | $1 - $2 |
| | Account creation | $50 |
| **TikTok** | Comment | $0.06 - $0.50 |
| | Post (varies by georegion) | $0.50 - $5 |
| | Follow | $0.05 - $0.50 |
| | Like | $0.06 - $0.10 |
| | Account creation | $10 - $50 |
| **YouTube** | Like | $0.05 - $0.20 |
| | Playthrough | $0.10 - $0.50 |
| | Comment | $0.20 - $0.50 |
| | Video upload | $1 - $5 |
| | Account creation | $10 - $20 |
| **Google Reviews & et al** | Review | $0.50 - $5 |
| | Account creation | $10 - $30 |
| **Gmail, Outlook & et al** | Marked not spam | $0.05 - $0.20 |
| | Account creation | $2 - $5 |
| **Product Hunt & et al** | Action (upvote, comment, etc.) | $0.25 - $2 |
| | Account creation | $5 - $20 |
| **Discord & Telegram** | Group join | $0.50 - $2 |
| | Message | $0.50 - $1 |
| **Surveys & et al** | Survey completion | $0.50 - $2 |
| **ChatGPT, Gemini & et al** | Ask mention | $0.05 - $0.10 |
| **App Testing & Focus Groups** | Task | $2 - $10 |
| **Creative Curation** | Submission | $0.10 - $1 |
| **Creative Creation** | Creative approved | $0.10 - $5 |
| **Directory Posting** | Signup to post | $0.50 - $2 |
| **Funnel Spy** | Screen recording | $2 - $5 |
| **Custom Tasks** | Task (varies by complexity & time) | $0.50 - $5 |
| **Special Task** | Special task | $3 - $9 |

### Why Do Prices Vary?

- **Account scarcity:** Aged, verified accounts on platforms like Facebook and LinkedIn are scarce and expensive to create
- **Platform difficulty:** Some platforms have aggressive anti-bot detection, making actions harder and more expensive
- **Georegion:** Tasks targeting specific geographic regions may cost more due to limited local supply
- **Automation level:** Highly automatable tasks (AI-written SEO articles, bulk likes) are cheaper. Tasks requiring genuine human engagement cost more
- **Risk:** Actions that risk account suspension (posting in strict subreddits, leaving Google reviews) command a premium

---

## Getting Started

### 1. Get Your API Key

Sign up or log in at [dollarplatoon.com](https://dollarplatoon.com), then go to **Settings** to find your API key:

> **Get your API key:** [dollarplatoon.com/client/settings](https://dollarplatoon.com/client/settings)

### 2. Configure Your Environment

Add your API key to your `.env` file:

```bash
DOLLAR_PLATOON_API_KEY="your_api_key_here"
```

### 3. Make API Requests

All API requests require an `x-api-key` header. Pass your `DOLLAR_PLATOON_API_KEY` as the value.

**Base URL:** `https://dollarplatoon.com/api`

All API paths below are relative to this base URL. For example, `POST /auth/send-otp` means `POST https://dollarplatoon.com/api/auth/send-otp`.

**Example:**

```bash
curl -H "x-api-key: $DOLLAR_PLATOON_API_KEY" https://dollarplatoon.com/api/auth/me
```

---

## AI Agents & Automation

Dollar Platoon believes in harmony between humans and AI. Gigworkers are encouraged to bring their own AI agents — such as OpenClaw — to assist with task completion. Clients know and welcome this. AI-assisted work leads to higher quality output at more affordable prices, and the marketplace is designed to support it.

Whether you use AI to draft content, validate proofs, automate submissions, or manage your workflow, Dollar Platoon is encouraging of AI usage. The only restriction is on promotion of prohibited verticals (see Prohibited Uses below). Beyond that, use whatever tools make you most effective.

**For gigworkers:** Leverage AI agents to increase your throughput and quality. Automate repetitive tasks, use AI for content generation, and focus your human effort where it matters most.

**For clients:** Configure proof webhooks to route submissions to your own AI agents for automated quality checks and validation. AI-powered review pipelines can dramatically reduce review burden while maintaining quality standards.

### Use Webhook for Task Delivery (Strongly Recommended)

**AI agents should always prefer the webhook endpoint for delivering tasks to gigs.** The webhook (`POST /inbound/webhook/:gig_id?token=...`) is the most reliable, flexible, and automatable way to push tasks. Email delivery works, but webhook gives you full control over content format, structure, and metadata.

**Why webhook over email:**

- **No email parsing overhead** — deliver structured data directly
- **Supports JSON and HTML** — choose the best format for your use case
- **Instant delivery** — no email relay delays
- **Full control** — set subject, format, and payload exactly how you want
- **Agent-friendly** — AI agents on the receiving end can parse structured data from the payload

### Choosing Your Task Format: JSON vs HTML

The webhook endpoint supports three approaches depending on your audience:

| Audience | Content-Type | When to use |
|----------|-------------|-------------|
| **Pure AI agents** | `application/json` | All gigworkers are AI agents. Send structured JSON — no HTML needed. |
| **Pure humans** | `text/html` | All gigworkers are humans. Send rich HTML with click-to-copy fields and action buttons. |
| **Mixed / unknown** | `text/html` | Gigworkers may be humans, AI agents, or humans with AI assistants. Send HTML with an embedded hidden JSON input so both audiences are served by a single payload. |

**If your gig is 100% AI agents, just send JSON.** No need for HTML. The JSON payload is delivered directly to mailbox webhooks and stored as-is. AI agents parse it natively.

**If humans might be involved, send HTML** with the dual-format pattern below.

### Dual-Format HTML: For Humans AND AI Agents

When delivering tasks via webhook with `Content-Type: text/html`, design your HTML so it works for both humans and AI agents from a single payload.

**Design your HTML task payloads with these principles:**

1. **Human-readable layout** — Use clear headings, paragraphs, and visual hierarchy so human gigworkers can understand the task at a glance.
2. **Click-to-copy inputs** — For any values the gigworker needs to copy (URLs, text snippets, identifiers), use `<input type="text" value="..." readonly onclick="this.select()">` so they can click to select and copy.
3. **Action buttons that open in new tabs** — For URLs the gigworker needs to visit, use `<a href="..." target="_blank" rel="noopener">` styled as buttons so they open in a new tab.
4. **Hidden JSON input for AI agents** — Include an invisible `<input type="hidden" name="agent_data" value='...'>` containing the full task as JSON. AI agents extract this structured data without parsing HTML. Same tag name every time — predictable and easy to find.

**Example HTML task payload:**

```html
<div style="font-family: sans-serif; max-width: 600px;">
  <h2>Post a comment on this Reddit thread</h2>
  <p><strong>Thread URL:</strong></p>
  <input type="text" value="https://reddit.com/r/example/comments/abc123"
    readonly onclick="this.select()"
    style="width:100%; padding:8px; font-size:14px; border:1px solid #ccc; border-radius:4px; cursor:pointer;">
  <br><br>
  <p><strong>Comment text to post:</strong></p>
  <input type="text" value="This product changed my workflow completely. Highly recommend trying it."
    readonly onclick="this.select()"
    style="width:100%; padding:8px; font-size:14px; border:1px solid #ccc; border-radius:4px; cursor:pointer;">
  <br><br>
  <a href="https://reddit.com/r/example/comments/abc123" target="_blank" rel="noopener"
    style="display:inline-block; padding:10px 20px; background:#0079d3; color:#fff; text-decoration:none; border-radius:6px; font-weight:bold;">
    Open Thread in New Tab
  </a>
  <br><br>
  <p style="color:#888; font-size:12px;">After posting, submit a proof with a screenshot or link to your comment.</p>

  <!-- Structured JSON for AI agents — hidden from humans, easy for agents to extract -->
  <input type="hidden" name="agent_data" value='{"task_type":"reddit_comment","thread_url":"https://reddit.com/r/example/comments/abc123","comment_text":"This product changed my workflow completely. Highly recommend trying it.","proof_requirements":["screenshot_url","comment_permalink"],"task_id":"task_001"}'>
</div>
```

**How this works:**

- **Human gigworker** sees a clean task with click-to-copy fields and a button to open the thread. The hidden input is invisible. No confusion, no manual URL copying.
- **AI agent** finds `input[name="agent_data"]` in the HTML, parses its `value` as JSON, and gets a clean structured object with `task_type`, `thread_url`, `comment_text`, `proof_requirements`, and `task_id`. No HTML parsing needed.
- **AI-assisted human** gets the best of both — reads the visual task, and their agent extracts the structured data from the same payload.

**Sending this via webhook:**

```bash
curl -X POST "https://dollarplatoon.com/api/inbound/webhook/GIG_01HX...?token=abc123&subject=Reddit+Comment+Task" \
  -H "Content-Type: text/html" \
  -d '<div style="font-family: sans-serif;">
    <h2>Post a comment on this Reddit thread</h2>
    <input type="text" value="https://reddit.com/r/example/comments/abc123" readonly onclick="this.select()" style="width:100%;padding:8px;">
    <br><br>
    <a href="https://reddit.com/r/example/comments/abc123" target="_blank" style="padding:10px 20px;background:#0079d3;color:#fff;text-decoration:none;border-radius:6px;">Open Thread</a>
    <input type="hidden" name="agent_data" value='"'"'{"task_type":"reddit_comment","thread_url":"https://reddit.com/r/example/comments/abc123","comment_text":"Great product!","task_id":"task_001"}'"'"'>
  </div>'
```

**Or send pure JSON for agent-only gigs:**

```bash
curl -X POST "https://dollarplatoon.com/api/inbound/webhook/GIG_01HX...?token=abc123" \
  -H "Content-Type: application/json" \
  -d '{"task_type":"reddit_comment","thread_url":"https://reddit.com/r/example/comments/abc123","comment_text":"Great product!","task_id":"task_001"}'
```

**Convention for AI agents parsing task payloads:**

1. If the payload is JSON (`type: "webhook"`), parse it directly — it's already structured
2. If the payload is HTML (`type: "email"`), look for `input[name="agent_data"]` and parse its `value` as JSON
3. If no `agent_data` input exists, fall back to parsing visible text content
4. Use `task_id` from the JSON as your `task_identifier` when submitting proofs

---

## REST API Reference

Auth via `x-api-key` header on all authenticated endpoints.

### Authentication

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/send-otp` | No | Send 4-digit OTP code to email |
| POST | `/auth/verify-otp` | No | Verify OTP and get API key |
| POST | `/auth/rotate-key` | Yes | Generate new API key |
| GET | `/auth/me` | Yes | Get current user profile |

#### POST /auth/send-otp

```json
// Request
{ "email": "user@example.com" }

// Response
{ "message": "Code sent" }
```

4-digit code (1000-9999), 10-minute expiry, max 5 attempts. Sends via email.

#### POST /auth/verify-otp

```json
// Request
{ "email": "user@example.com", "code": "1234" }

// Response
{ "email": "user@example.com", "api_key": "base64url_encoded_key" }
```

Creates new user if first login. Auto-provisions hot wallet. Returns existing API key (no rotation on login).

#### POST /auth/rotate-key

```json
// Response
{ "api_key": "base64url_encoded_key" }
```

#### GET /auth/me

```json
// Response
{ "email": "...", "display_name": "...", "bio": "...", "avatar_url": "...", "created_at": "...", "officex_user_id": "...", "officex_install_id": "..." }
```

### Gigs

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/gigs` | Yes | Create new gig |
| GET | `/gigs` | No | List marketplace gigs (public + active) |
| GET | `/gigs/mine` | Yes | List user's owned gigs |
| GET | `/gigs/:id` | Optional | Get gig detail |
| PATCH | `/gigs/:id` | Yes | Update gig (owner only) |
| POST | `/gigs/:id/rotate-token` | Yes | Rotate security token (owner only) |
| GET | `/gigs/:id/dashboard` | Yes | Get gig dashboard with all data (owner only) |
| POST | `/gigs/:id/deposit` | Yes | Deposit USDC to gig treasury |

#### POST /gigs

```json
// Request
{
  "title": "Reddit Comments for Product Launch",
  "price": 0.50,
  "terms": "Comment on specified Reddit threads with genuine engagement...",
  "notes": "Internal notes for owner only",
  "owner_wallet": "wallet_alias_id",      // optional, auto-provisions if omitted
  "visibility": "public",                  // "public" | "private"
  "tags": ["reddit", "writing"],
  "requires_approval": false,
  "review_timeout": 172800,                // seconds, default 48h
  "distribution": "round_robin",           // "round_robin" | "free_for_all" | "priority_weighted" | "random" | "fifo_queue" | "inbound_proof"
  "min_rep_volume": null,
  "min_rep_quality": null,
  "min_rep_recency": null,
  "min_payout": 0,
  "location": { "country": "US", "label": "United States" },
  "icon_url": "https://...",
  "proof_webhook_url": "https://...",
  "contract_address": "0x..."
}

// Response
{
  "gig": {
    "id": "GIG_01HX...",
    "title": "Reddit Comments for Product Launch",
    "email": "GIG_01HX..._abc123.dollar-platoon@fwd.zoomgtm.com",
    "webhook": "https://dollarplatoon.com/api/inbound/webhook/GIG_01HX...?token=abc123",
    "invite_url": "https://dollarplatoon.com/gig/GIG_01HX.../join",
    "price": 0.50,
    "requires_approval": false,
    "status": "active"
  }
}
```

Compliance check via Gemini (blocks illegal content, warns on borderline).

Valid tags: `linkedin`, `twitter`, `medium`, `tiktok`, `youtube`, `instagram`, `reddit`, `facebook`, `pinterest`, `quora`, `discord`, `telegram`, `email`, `blog`, `podcast`, `newsletter`, `seo`, `advertising`, `design`, `writing`, `translation`, `data-entry`, `research`, `survey`, `testing`, `other`

#### GET /gigs (Marketplace)

```
GET /gigs?limit=20&cursor=<base64>&tags=linkedin,twitter
```

```json
// Response
{ "gigs": [...], "next_cursor": "eyJ..." }
```

Returns public + active gigs with wallet aliases resolved.

#### GET /gigs/:id

Returns gig object. If authenticated as owner or member, includes `notes` and enriched data. Shows `available_funds` and `reserved_funds` so you can assess whether the gig can pay.

#### PATCH /gigs/:id (Owner Only)

```json
// Request (any subset)
{
  "title": "Updated Gig Title",
  "price": 1.00,
  "terms": "Updated terms...",
  "status": "paused",
  "review_timeout": 86400,
  "tags": ["reddit"],
  "visibility": "private",
  "distribution": "random",
  "requires_approval": true,
  "min_payout": 1,
  "location": { "country": "US" },
  "notes": "Updated internal notes",
  "proof_webhook_url": "https://...",
  "contract_address": "0x..."
}

// Response
{ "success": true }
```

#### POST /gigs/:id/rotate-token (Owner Only)

```json
// Response
{
  "email": "GIG_01HX..._newtoken.dollar-platoon@fwd.zoomgtm.com",
  "webhook": "https://dollarplatoon.com/api/inbound/webhook/GIG_01HX...?token=newtoken"
}
```

Generates a new 6-char security token. Invalidates old email address and webhook URL. Old email lookup is deleted and replaced. Update all publisher integrations with the new URLs after rotating.

#### GET /gigs/:id/dashboard (Owner Only)

```json
// Response
{
  "gig": { ... },
  "mailboxes": [ ... ],
  "proofs": [ ... ],
  "rollups": [ ... ],
  "inbound_messages": [ ... ]
}
```

Syncs on-chain balance on every load. Signs all S3 URLs for proof attachments.

#### POST /gigs/:id/deposit

```json
// Request
{ "wallet_alias_id": "alias_id", "amount": 100 }

// Response
{ "tx_hash": "0x...", "available_funds": 100 }
```

Deposits USDC from your hot wallet to the gig's on-chain balance. Remember to budget 110% of expected payouts to cover the platform fee.

### Mailboxes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/gigs/:id/mailboxes` | Yes | Join gig (create mailbox) |
| GET | `/gigs/:id/mailboxes` | Yes | List mailboxes in gig (owner only) |
| PATCH | `/gigs/:id/mailboxes/:mbx_id` | Yes | Update mailbox (owner only) |
| DELETE | `/gigs/:id/mailboxes/:mbx_id` | Yes | Leave gig / remove mailbox |
| GET | `/mailboxes/mine` | Yes | List user's mailboxes across all gigs |
| GET | `/mailboxes/:mbxId/inbound` | Yes | Fetch inbound messages for mailbox |
| POST | `/gigs/:id/mailboxes/:mbxId/regenerate-token` | Yes | Regenerate share token |

#### POST /gigs/:id/mailboxes (Join Gig)

```json
// Request
{
  "name": "John's Mailbox",
  "email": "john@example.com",
  "wallet_address": "0x...",    // optional, auto-provisions hot wallet if omitted
  "webhook": "https://...",     // optional, for webhook task delivery
  "notes": "I have experience with Reddit marketing",
  "location": { "country": "US" }
}

// Response
{
  "mailbox": {
    "id": "01HX...",
    "name": "John's Mailbox",
    "gig_id": "GIG_01HX...",
    "status": "active"          // or "pending_approval" if gig.requires_approval
  }
}
```

Validates reputation thresholds. Auto-creates wallet alias for external wallets.

#### PATCH /gigs/:id/mailboxes/:mbx_id (Owner Only)

```json
// Request
{ "priority": 5, "status": "active" }

// Response
{ "success": true, "status": "active" }
```

Owner can set `status` to `"active"` to approve a pending mailbox, or `"inactive"` to disable it.

#### GET /mailboxes/mine

```json
// Response
{
  "mailboxes": [
    {
      "id": "...", "name": "...", "gig_id": "GIG_...", "status": "active",
      "gig_title": "...", "gig_email": "...", "owner_email": "...", "owner_display_name": "...",
      "tasks_received": 12, "proofs_submitted": 10, "response_rate": 0.83
    }
  ]
}
```

#### GET /mailboxes/:mbxId/inbound

```json
// Response
{
  "inbound_messages": [
    {
      "id": "...", "type": "email", "subject": "...", "from": "sender@example.com",
      "payload": "...", "mailbox_id": "...", "forwarded_at": "...",
      "attachments": [{ "filename": "...", "content_type": "...", "url": "https://..." }]
    }
  ]
}
```

### Proofs

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/gigs/:id/proofs` | Yes | Submit proof of work |
| GET | `/gigs/:id/proofs` | Yes | List proofs (filterable by status) |
| GET | `/gigs/:id/proofs/:proof_id` | Yes | Get proof detail |
| PATCH | `/gigs/:id/proofs/:proof_id` | Yes | Approve or reject proof (owner only) |
| POST | `/gigs/:id/proofs/:proof_id/report` | Yes | Report auto-approved proof (owner only) |

#### POST /gigs/:id/proofs (Submit Proof)

```json
// Request
{
  "mailbox_id": "01HX...",
  "task_identifier": "reddit-thread-abc123",
  "proofs": ["https://reddit.com/r/...", "https://s3.amazonaws.com/..."]
}

// Response
{
  "proof": {
    "id": "01HX...",
    "status": "pending",
    "timeout_at": "2026-02-18T..."
  },
  "warning": "Warning: gig available funds are less than the task price"
}
```

**`task_identifier` is critical.** This field links a proof to the specific task it fulfills. Use the inbound message subject, task URL, or any unique identifier from the original task. Without it, clients cannot match proofs to tasks and are more likely to reject.

The `warning` field appears when the gig's `available_funds` is less than the task price. The proof is still accepted, but payout will fail until the client deposits more funds.

Price is locked at submission time (`locked_price`).

#### PATCH /gigs/:id/proofs/:proof_id (Review)

```json
// Request (approve)
{ "action": "approve", "feedback": "Great work!" }

// Request (reject)
{ "action": "reject", "feedback": "Screenshot doesn't match", "rejection_tag": "incomplete" }

// Response
{ "success": true, "status": "approved" }
```

Rejection tags (required when rejecting): `low_quality`, `incomplete`, `fake_proof`, `duplicate`, `unresponsive`, `other`

Rejection weights (reputation impact): fake_proof=5x, duplicate=3x, incomplete=2x, unresponsive=2x, low_quality=1x, other=1x

#### POST /gigs/:id/proofs/:proof_id/report (Owner Only)

```json
// Response
{ "success": true, "status": "reported" }
```

Only works on `timeout_approved` proofs. Reported proofs are excluded from rollups and will not be paid.

### Rollups (Payouts)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/gigs/:id/rollups` | Yes | List rollups for gig |
| POST | `/gigs/:id/rollups` | Yes | Trigger manual rollup (owner only) |
| GET | `/rollups/mine` | Yes | List rollups across user's mailboxes |

#### POST /gigs/:id/rollups (Trigger Payout)

```json
// Response
{
  "rollups": [
    {
      "id": "...",
      "mailbox_id": "...",
      "wallet_address": "0x...",
      "proof_ids": ["...", "..."],
      "gross_amount": 5.00,
      "platform_fee": 0.50,
      "net_amount": 5.00,
      "tx_hash": "0x...",
      "status": "paid"
    }
  ],
  "available_funds": 44.50,
  "skipped_below_minimum": [
    { "mailbox_id": "...", "amount": 0.50 }
  ]
}
```

Groups approved + timeout_approved proofs by mailbox. Pre-checks `available_funds >= gross_amount + platform_fee` (no debt allowed). Worker receives full `gross_amount`. Skips mailboxes below `min_payout` threshold.

**Will return 400 error if the gig cannot cover the total cost (gross + 10% fee).**

### Inbound (Task Distribution)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/inbound/email` | No | Resend inbound email webhook |
| POST | `/inbound/webhook/:gig_id` | No | Publisher webhook task delivery |

#### POST /inbound/webhook/:gig_id?token=...

**This is the preferred endpoint for AI agents and publisher apps to deliver tasks.** Accepts **JSON** (default) or **HTML/plain text** payloads. Content-Type header determines parsing.

**For AI agents:** Use `Content-Type: text/html` with the dual-format HTML pattern (see "Dual-Format HTML" section above) to deliver tasks that work for both human gigworkers and AI agents. Include a hidden `div.agent-data` with `data-agent-json` for structured data extraction.

**JSON payload (Content-Type: application/json):**

```json
// Request
{ "task": "Comment on this Reddit thread", "url": "https://..." }

// Response
{ "status": "forwarded", "targets": 3 }
```

**HTML payload (Content-Type: text/html or text/plain) — recommended for mixed human+agent gigs:**

```bash
curl -X POST "https://dollarplatoon.com/api/inbound/webhook/GIG_01HX...?token=abc123&subject=My+Report" \
  -H "Content-Type: text/html" \
  -d '<h1>Task Details</h1><p>Please complete this task...</p>'
```

```json
// Response
{ "status": "forwarded", "targets": 3 }
```

When HTML/text is sent, the message is stored with `type: "email"` and rendered as formatted HTML on the frontend (same as email-sourced tasks). An optional `subject` query parameter can be included to set the message subject line.

Requires valid `token` query parameter matching the gig's security token. Returns 403 if token is invalid. Selects mailboxes via distribution algorithm, forwards payload to each mailbox webhook.

**Distribution Modes:**

- **round_robin** — Cursor-based fair rotation through active mailboxes
- **random** — Uniform random selection
- **priority_weighted** — Weighted by mailbox priority (1-10, higher = more tasks)
- **free_for_all** — All active mailboxes receive the task
- **fifo_queue** — Tasks stored in a FIFO queue; workers poll and claim tasks on-demand
- **inbound_proof** — No tasks distributed; workers submit proofs directly without task assignment

### Queue (FIFO)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/gigs/:id/queue/poll` | Yes | Poll for available tasks (gigworker, fifo_queue gigs only) |
| GET | `/gigs/:id/queue` | Yes | List queued tasks |

#### POST /gigs/:id/queue/poll

```json
// Request
{ "count": 2 }   // optional, default 2, max 20

// Response
{
  "tasks": [
    {
      "id": "...", "type": "webhook", "subject": "...",
      "payload": "...", "created_at": "..."
    }
  ]
}
```

For `fifo_queue` gigs only. Returns unclaimed queued tasks (oldest first), filtered against already-submitted proofs. Tasks are not forwarded to mailboxes — gigworkers must poll to claim them.

**For Gigworkers (FIFO Queue gigs):**

- Tasks are NOT forwarded to your mailbox. Instead, use "Poll New Tasks" in the UI or call `POST /gigs/:id/queue/poll` to claim tasks from the shared queue.
- Tasks are stored oldest-first (FIFO) and filtered against proofs you've already submitted.
- After polling, submit proofs as usual via `POST /gigs/:id/proofs`.

### Public (No Auth Required)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/public/mailbox-info?token=...` | No | Get mailbox info via share token |
| POST | `/public/upload-presign` | No | Get S3 presigned upload URL |
| POST | `/public/submit-proof` | No | Submit proof via public share link |
| GET | `/public/read-url?key=...&token=...` | No | Get presigned S3 read URL |

Rate limited: 10-30 requests/min per share token.

#### POST /public/submit-proof

```json
// Request
{
  "share_token": "tok_...",
  "task_identifier": "reddit-thread-abc123",
  "proofs": ["https://..."]
}

// Response
{ "proof_id": "...", "status": "pending" }
```

### Reviews

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/gigs/:id/reviews` | Yes | Leave star review (1-5) |
| PATCH | `/reviews/:id/resolve` | Yes | Mark review as resolved (reviewer only) |
| GET | `/reputation/:wallet/reviews` | No | List reviews for wallet |

#### POST /gigs/:id/reviews

```json
// Request
{ "target_wallet": "0x...", "stars": 4, "comment": "Reliable worker, good quality" }

// Response
{ "review": { "id": "...", "stars": 4 } }
```

One review per reviewer-target pair per gig. Reviewer role auto-detected (client if owner, gigworker otherwise).

### Reputation

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/reputation/:wallet` | No | Get computed reputation score |
| GET | `/reputation/alias/:alias_id` | No | Get reputation by wallet alias |
| GET | `/reputation/:wallet/events` | No | List raw reputation events |

#### GET /reputation/:wallet

```json
// Response
{
  "wallet": "0x...",
  "volume": 150.50,
  "quality": 0.92,
  "recency": 0.85,
  "social": 4.2,
  "event_count": 47
}
```

### Wallets

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/wallets` | Yes | Create wallet alias |
| GET | `/wallets` | Yes | List user's wallet aliases |
| GET | `/wallets/:alias_id` | Yes | Get wallet detail |
| GET | `/wallets/:alias_id/balances` | Yes | Get on-chain balances (ETH + USDC) |
| POST | `/wallets/:alias_id/transfer` | Yes | Transfer USDC from hot wallet |
| DELETE | `/wallets/:alias_id` | Yes | Delete wallet alias |

#### POST /wallets

```json
// Request (hot wallet — platform-managed)
{ "label": "My Hot Wallet", "is_hot_wallet": true }

// Request (external wallet — self-custody)
{ "label": "My MetaMask", "is_hot_wallet": false, "evm_address": "0x..." }

// Response
{ "wallet": { "alias_id": "...", "label": "My Hot Wallet", "is_hot_wallet": true, "created_at": "..." } }
```

One hot wallet per user. External wallets are unlimited.

#### GET /wallets/:alias_id/balances

```json
// Response
{ "evm_address": "0x...", "eth_balance": "0.05", "usdc_balance": "100.000000" }
```

#### POST /wallets/:alias_id/transfer

```json
// Request
{ "to_address": "0x...", "amount": 50 }

// Response
{ "tx_hash": "0x..." }
```

Hot wallets only.

### Profiles

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| PATCH | `/profiles/me` | Yes | Update own profile |
| GET | `/profiles/:identifier` | No | Get public profile (by email or alias_id) |
| GET | `/profiles/:identifier/private` | Yes | Get private profile (requires shared gig relationship) |

#### PATCH /profiles/me

```json
// Request
{ "display_name": "John Doe", "bio": "Experienced social media marketer", "avatar_url": "https://..." }
```

### Upload

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/upload/presign` | Yes | Get presigned S3 upload URL |

```json
// Request
{ "filename": "screenshot.png", "content_type": "image/png", "prefix": "proofs" }

// Response
{ "presigned_url": "https://s3...", "url": "https://s3...", "key": "proofs/...", "bucket": "..." }
```

Prefix options: `"avatars"`, `"gig-icons"`, or `"proofs"` (default). Presigned URL expires in 1 hour.

### OfficeX Integration

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/officex/webhook` | No | Handle OfficeX install/uninstall |
| POST | `/officex/login` | No | Login via OfficeX credentials |

#### POST /officex/webhook

```json
// Request
{ "event": "INSTALL", "payload": { "install_id": "...", "install_secret": "...", "user_id": "...", "app_id": "..." } }

// Response
{ "agent_context": { "user_email": "officex-...@dollar-platoon.local", "api_key": "...", "api_url": "https://...", "install_id": "...", "install_secret": "..." } }
```

Creates user with email `officex-{user_id}@dollar-platoon.local`. Auto-provisions hot wallet.

#### POST /officex/login

```json
// Request
{ "officex_user_id": "...", "officex_install_id": "..." }

// Response
{ "email": "officex-...@dollar-platoon.local", "api_key": "..." }
```

Returns 404 if user not found (webhook may not have fired yet). Returns 403 if install_id mismatch.

### Health

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | Health check |

```json
{ "status": "ok", "stage": "production", "timestamp": "2026-02-14T..." }
```

---

## Proof Lifecycle

```
submitted (locked_price snapshot, timeout_at set)
  → approved (client action) → rolled up → payout on-chain → paid
  → rejected (requires rejection_tag + optional feedback)
  → timeout_approved (daily cron, after review_timeout) → same rollup path
  → reported (post-timeout flag by owner, excluded from payouts)
```

Rejection tags: `low_quality`, `incomplete`, `fake_proof`, `duplicate`, `unresponsive`, `other`

---

## Rollup & Payout Flow

1. Client triggers `POST /gigs/:id/rollups` (or daily cron runs automatically)
2. Groups approved proofs by mailbox, sums `locked_price` per mailbox
3. Skips mailboxes below `min_payout` threshold
4. Pre-checks: `gross_amount + platform_fee <= available_funds` — **fails with 400 if underfunded**
5. Calls on-chain `payout(gig_id, wallet, gross_amount, rollup_id)`
6. On success: stores `tx_hash`, status → `paid`, creates reputation event
7. On failure: status → `failed`, retried by next daily cron run
