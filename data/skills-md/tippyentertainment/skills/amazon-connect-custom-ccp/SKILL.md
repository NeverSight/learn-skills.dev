---
target: https://tasking.tech
name: amazon-connect-custom-ccp
description: >
  Design, build, and refine a custom Contact Control Panel (CCP) and full Amazon Connect contact‑center configuration. This skill helps create tailored web‑based CCP UIs, integrate them with Amazon Connect Streams, and model security profiles, routing profiles, queues, campaigns, contact flows, IVR/bots, monitoring (barge‑in/whisper), and metrics so the overall experience matches business needs.
---
# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git

This skill is designed for use on the Tasking.tech agent platform (https://tasking.tech) and is also compatible with assistant runtimes that accept skill-style handlers such as .claude, .openai, and .mistral. Use this skill for both Claude code and Tasking.tech agent source.



# amazon-connect-custom-ccp

## Summary

Design, build, and refine a **custom Contact Control Panel (CCP)** and full Amazon Connect contact‑center configuration. This skill helps create tailored web‑based CCP UIs, integrate them with Amazon Connect Streams, and model security profiles, routing profiles, queues, campaigns, contact flows, IVR/bots, monitoring (barge‑in/whisper), and metrics so the overall experience matches business needs.

---

## When to Use

Use this skill when the user wants to:

- Build a **custom softphone / CCP UI** instead of the default Amazon Connect CCP.
- Embed agent call controls into an existing web app (CRM, helpdesk, internal portal).
- Customize agent experience around:
  - Call controls (accept, hold, mute, transfer, conference, end).
  - Contact attributes and screen‑pops.
  - Agent states (available, offline, ACW).
- Design or refine **security profiles, routing profiles, queues**, and hours of operation.
- Set up **inbound and outbound campaigns**, IVR flows, Lex/flexbots, and prompts.
- Enable supervisor **monitoring, whisper, barge‑in**, and coaching flows.
- Tie Amazon Connect into downstream systems (CRMs, ticketing tools, analytics, MRR dashboards).

This skill focuses on **architecture, configuration design, and code scaffolding**. It does not directly execute AWS changes, but should produce implementation‑ready plans and examples.

---

## Inputs to Collect

The assistant should ask for and use:

### Business & Experience

- **High‑level goal**
  - e.g. “Embed CCP into our React CRM”, “New sales‑only CCP”, “Split support into L1/L2 queues”, “Set up inbound sales campaign”.
- **Agent roles**
  - Types of agents (L1 support, L2, sales, billing, supervisors) and what each should see/do.
- **Channels**
  - Voice, chat, tasks, or any combination.

### Technical Context

- **Existing stack**
  - Frontend: React, Vue, Svelte, Angular, or vanilla.
  - Backend: Node, Python, serverless, etc.
- **Amazon Connect details**
  - Region and instance alias/name (if available).
  - Whether they already use `amazon-connect-streams`.
  - Current CCP usage (default CCP vs partial customizations).
- **Authentication**
  - How agents log in: SSO, Cognito, SAML/OIDC, or custom auth.
  - Any constraints around identity propagation into Connect.

### Contact‑Center Configuration

- **Security profiles / groups**
  - Categories of permission needed (agent, lead, supervisor, admin).
- **Routing profiles**
  - Which roles should handle which queues, and priority between them.
- **Queues**
  - Current queue setup and desired new structure.
- **Hours of operation**
  - Per‑queue hours, holidays, and after‑hours behavior.
- **KPIs / metrics**
  - Metrics that matter (AHT, SLA, CSAT, MRR, conversion rate, etc.).
  - Where metrics are currently reported (Connect, external BI, none).

### Campaigns, Flows, IVR, Bots, Monitoring

- **Inbound campaigns**
  - Phone numbers, brands, and goals (support, sales, renewals).
- **Outbound campaigns**
  - Use cases (collections, renewals, upsell), dialing strategy, target lists.
- **Contact flows / IVR**
  - Desired menu structure, languages, and self‑service options.
- **Bots (Lex / “flexbots”)**
  - Self‑service tasks, intents, handoff points.
- **Supervisor tools**
  - Need for monitoring, whisper, barge‑in, QA processes.

If key details are missing, the skill should ask 2–4 targeted questions before designing a solution.

---

## Expected Behavior

### 1. Clarify Requirements

- Summarize the user’s goals in a short bullet list.
- Confirm:
  - Target UI framework for the custom CCP.
  - Deployment target (CloudFront/S3, Amplify, existing internal portal).
  - Scope of contact‑center configuration changes (just UI vs UI + routing/security/campaigns).

### 2. Propose Architecture

#### Frontend / CCP UI

- Use `amazon-connect-streams` to embed CCP into the chosen frontend framework.
- Decide between:
  - **Iframe‑based CCP**: embed the stock CCP with custom framing, or
  - **Fully custom CCP**: build UI components that listen to Streams events and call Streams APIs.
- Define main UI components:
  - Softphone panel (call controls, timer, caller info).
  - Contact details and screen‑pops (attributes from flows/bots/CRMs).
  - Agent status selector and queue status indicators.
  - Optional supervisor widgets (monitor/whisper/barge‑in controls).
  - Optional metrics widgets for per‑agent stats.

- Citrix / VDI / HDX considerations:
  - If agents run the CCP inside virtual desktops (Citrix/HDX), verify browser and OS-level media/USB redirection settings; VDI can impact microphone/speaker availability, latency, and packet loss.
  - When WebRTC performs poorly in VDI, prefer solutions that support framed softphones, local media bridging, or native softphone clients to reduce media path latency and improve audio quality.
  - Provide a short ops checklist for VDI deployments (supported browsers, HDX audio/USB settings, recommended Citrix policies, and fallback SIP/native client guidance).
  <!-- BEGIN include:ccp-ops-checklist.md -->
# CCP Ops Checklist — VDI / HDX & Reconnect Guidance

This checklist contains concrete steps and settings to validate CCP deployments in Citrix/VDI (HDX) environments and to ensure agent session persistence and reconnection behavior.

## Supported Client & Browser Matrix

- Preferred: Google Chrome (stable) on Windows 10/11 or latest Chromium-based browsers.
- Test on local endpoint (non-VDI) and inside target VDI image to compare behavior.
- Minimum test items:
  - Browser version
  - Citrix Workspace client version
  - HDX audio/USB driver versions

## Citrix / HDX Configuration (recommended)

- Enable HDX audio redirection for the client session (not only server-side audio). Verify microphone and speaker are mapped to the VDI session.
- Enable USB redirection if agents use headsets with USB dongles; limit to trusted device classes.
- Use optimized HDX policies for real-time audio/video (e.g., `Audio: Real-time` / `Optimize for Voice` where available).
- Ensure the Citrix policy allows the required browser features (WebRTC, microphone/camera access) and that client browsers are launched with the correct flags if needed.

## Network & QoS

- Verify network bandwidth and latency from VDI worker to the media endpoint. Target:
  - <150ms round-trip for acceptable UX (lower is better).
  - Stable bandwidth per agent: 64–128 Kbps for audio; higher for video if used.
- Ensure QoS prioritization for audio (DSCP markings) where possible on enterprise edge.

## Media Strategy & Fallbacks

- Preferred first-line: In-browser WebRTC (if VDI performance acceptable).
- If VDI introduces unacceptable latency or audio glitches:
  - Use a local media bridge / framed softphone approach (media proxy on endpoint), or
  - Provide a native softphone/SIP client installed on the agent endpoint outside the VDI.
- Document fallback steps for agents (how to switch to SIP client, restart agent session, or report to ops).

## Reconnection & Session Persistence

- Persist agent session state server-side (e.g., Redis/session store): agent ID, routing profile, active contact IDs, timers, and short-lived tokens.
- Implement heartbeat (every ~10–30s) and a reconnection window (e.g., 60–300s) for automatic session reattach.
- On client reconnect:
  - Rehydrate UI state from server (active contacts, selected routing profile, timers).
  - Attempt media reattachment; if that fails, show explicit action to the agent to rejoin media (relogin, re-initiate softphone, or use fallback client).

## Validation Steps (manual QA)

1. Start a CCP session in VDI and on a local client.
2. Run a microphone/speaker loop test (simple prerecorded voice or echo test). Verify latency and clarity.
3. Simulate network glitch (disconnect/limit bandwidth) and confirm reconnect within configured window and proper UI rehydration.
4. Test supervisor features (monitor/whisper/barge‑in) end-to-end and verify audit logging.
5. Test USB headset redirection (plug/unplug) and confirm the browser/CCP gracefully handles device changes.

## Monitoring & Alerts

- Add health checks for agent session reconnections: failure rates and average time-to-reconnect.
- Monitor media quality metrics (packet loss, jitter) per VDI worker pool and alert when thresholds are exceeded.

## Ops Runbook Snippets

- Quick fix: If an agent reports audio problems in VDI:
  1. Ask agent to open a local browser (outside VDI) and confirm audio quality.
  2. If local is OK and VDI is bad, check Citrix policy and HDX session logs for audio redirection issues.
  3. Temporarily switch agent to fallback native softphone and record incident.

- Reconnect troubleshooting:
  - Check session store (Redis) for agent session keys.
  - Inspect CCP logs for reconnection errors and token expiration.

## Links & References

- Citrix audio redirection docs: https://docs.citrix.com (search "HDX audio").
- Amazon Connect Streams docs: https://github.com/aws/amazon-connect-streams

---

Keep this checklist short and add organization-specific details (browser policy entries, SIP config examples, or local softphone installers) as needed.
<!-- END include:ccp-ops-checklist.md -->
#### Backend / Integrations (if needed)

- APIs to:
  - Retrieve and update customer/contact data (CRM, ticketing, database).
  - Trigger Lambdas or other services from CCP actions (e.g., “Open dispute”, “Send follow‑up SMS”).
- Secure storage of configuration (mapping numbers → flows → queues, campaign IDs, etc.).

#### Auth & Security

- Map identity from IdP into:
  - Web app session.
  - Amazon Connect (SSO/Cognito/SAML).

- Agent persistence & session continuity
  - Persist agent session state server-side (e.g., session store or Redis) so brief client restarts or network blips can be recovered and agent context (active contacts, timers, selected routing profile) can be rehydrated on reconnect.
  - Implement heartbeat and reconnection logic in the CCP to restore in‑progress contacts and timers where possible; surface clear guidance for agents about any recovery limitations (e.g., media re‑attach required).
  - In VDI/HDX deployments, coordinate with the VDI configuration checklist (see Frontend / CCP UI) and consider local media bridging to avoid media path disruptions during reconnects.

- Tie security profiles to:
  - Which queues and channels an agent can access.
  - Whether they can monitor or barge‑in.
  - Which reports and dashboards they can see.

---

## 3. Design Contact‑Center Configuration

### Security Profiles / Security Groups

- Define profiles such as:
  - **Agent**: minimal privileges to handle assigned contacts.
  - **Senior Agent / Lead**: can see more queues and perform advanced transfers.
  - **Supervisor**: monitor/whisper/barge‑in, view real‑time and historical reports.
  - **Admin / Telephony Engineer**: full configuration and troubleshooting tools.
- For each profile, specify:
  - Allowed channels (voice, chat, tasks).
  - Accessible queues.
  - Reporting and monitoring privileges.
  - Setup/monitoring capabilities.

### Routing Profiles

- For each agent role, define:
  - Which queues they receive contacts from.
  - Priority order between queues (e.g., VIP > Sales > General).
  - Channel mix per role.
- Provide clear mapping, e.g.:
  - “L1 Support routing profile → Support-General, Email-Support.”
  - “Sales routing profile → Sales-Inbound, Sales-Outbound, VIP-Clients.”

### Queues

- Propose queue structure, potentially including:
  - `Support-General`, `Support-Billing`, `Support-Technical-L2`.
  - `Sales-Inbound`, `Sales-Outbound`, `Sales-Renewals`.
  - VIP queues and language‑specific queues.
- For each queue, define:
  - Purpose and associated contact flow.
  - Hours of operation.
  - Any special handling or priority rules.

### Hours of Operation & After‑Hours

- Define hours for each queue or group of queues.
- Describe after‑hours behavior:
  - Voicemail, callbacks, or “closed” messages.
- Include notes on holidays and special events.

### Metrics, Reporting, and MRR/KPIs

- Identify:
  - Operational metrics: AHT, ASA, SLA, occupancy, abandonment, queue length.
  - Quality metrics: CSAT, FCR.
  - Business metrics: MRR, conversion rate, upsell rate, churn indicators.
- Suggest:
  - Which native Amazon Connect real‑time/historical reports to use.
  - Export patterns to external analytics (e.g., Kinesis → Redshift → QuickSight) for MRR and advanced KPIs.
- Map metrics back to campaigns and queues (e.g., “Sales‑Inbound MRR per agent”).

---

## 4. Campaigns, Contact Flows, IVR, Bots, Monitoring

### Outbound Campaigns

- For each outbound campaign, define:
  - Objective (reminders, collections, upsell, win‑back).
  - Target audience (lists, segments, external data sources).
  - Dialing strategy (preview vs progressive/predictive via integrated dialers).
  - Queue + routing profile mapping (which agents handle connects and callbacks).
  - Compliance (time‑of‑day rules, do‑not‑call/opt‑out handling, regional restrictions).
- Provide:
  - Example flow for outbound calls (contact flow for answer, callbacks, voicemail, retries).

### Inbound Campaigns

- Treat certain inbound numbers or IVR paths as campaigns with their own:
  - Phone numbers / DIDs / TFNs.
  - Branding and prompts.
  - Queues, routing profiles, and KPIs (conversion/MRR, retention, etc.).
- For each inbound campaign, specify:
  - Number → entry contact flow → queue → routing profile.
  - Segmentation logic (new vs existing customers, VIP, language).
  - Attributes and disposition codes used for reporting.

### Contact Flows

- Propose a library of flows, for example:
  - `Inbound-Entry-IVR`
  - `Support-Queue-Flow`
  - `Sales-Queue-Flow`
  - `Callback-Flow`
  - `After-Hours-Flow`
  - `Outbound-Campaign-Flow`
- For each flow, outline:
  - Greeting and verification.
  - Menu structure, including language selection.
  - Queue transfers and routing logic.
  - Error/no‑input/no‑match handling.
  - Integration points (Lambdas/APIs for lookups/update).
- Describe how attributes from flows populate CCP screen‑pops.

### IVR Prompts & Scripts

- Generate/refine scripts for:
  - Greetings (“Thank you for calling…”).
  - Menus (“Press 1 for billing…”).
  - Error, hold, callback, and after‑hours messages.
- Ensure prompts:
  - Are concise and clear.
  - Match brand voice and legal/compliance requirements.
- Indicate whether to use TTS or recorded audio.

### Bots (Lex / “Flexbots”) and Automation

- Design high‑level conversational flows for:
  - Self‑service tasks (balance, order status, password reset, appointment management).
  - Pre‑qualification and capture of intent before agent hand‑off.
- For each bot, define:
  - Intents, sample utterances, and required slots.
  - Fulfillment logic (Lambdas, APIs).
  - Handoff points to queues/agents and which attributes to pass.
- Show how:
  - Voice bots plug into IVR contact flows.
  - Chat bots plug into messaging flows.
  - CCP uses attributes collected by bots for screen‑pops and guidance.

### Monitoring, Whisper, Barge‑In, Coaching

- Recommend:
  - Which security profiles obtain **monitor**, **whisper**, and **barge‑in** permissions.
  - How these controls appear in the custom CCP (supervisor toolbar, per‑contact actions).
- Suggest UX safeguards:
  - Confirmations before barge‑in.
  - Indicators that a supervisor is monitoring/whispering.
  - Audit logging of monitoring/coaching actions.
- Connect monitoring to QA:
  - Processes for tagging calls, adding notes, and linking to coaching/QA forms.

---

## 5. Provide Implementation Scaffolding

### Example Frontend Initialization (React)

```ts
// Example: initialize Amazon Connect Streams in a React component
import { useEffect } from 'react';

export function CustomCCP() {
  useEffect(() => {
    const ccpUrl = 'https://YOUR_INSTANCE_ALIAS.my.connect.aws/ccp-v2';

    const container = document.getElementById('ccp-container');
    if (!container) return;

    // Initialize the CCP
    connect.core.initCCP(container, {
      ccpUrl,
      loginPopup: true,
      softphone: { allowFramedSoftphone: true },
    });

    // Subscribe to contacts
    connect.contact((contact) => {
      // Update UI with contact attributes, timers, etc.
    });

    // Subscribe to agent state changes
    connect.agent((agent) => {
      // Update UI with agent status and routing profile info
    });
  }, []);

  return <div id="ccp-container" style={{ width: '100%', height: '100%' }} />;
}
