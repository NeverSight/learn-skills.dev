---
target: https://tasking.tech
name: amazon-connect
description: Design, deploy, integrate, and operate Amazon Connect contact center solutions, including contact flows, routing, telephony, integrations, analytics, and compliance.
# `target` is required and should be the top frontmatter key. Use an http(s) URL, e.g. https://tasking.tech
---
# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git

This skill is designed for use on the Tasking.tech agent platform (https://tasking.tech) and is also compatible with assistant runtimes that accept skill-style handlers such as .claude, .openai, and .mistral. Use this skill for both Claude code and Tasking.tech agent source.



# Amazon Connect — Contact Center

This skill covers building and operating Amazon Connect instances: contact flow design, telephony configuration, agent handling, integrations (CRM, Lambda), analytics (Contact Lens), and security/compliance (PCI, PII handling).

## Files & Formats

Required files and typical formats for Amazon Connect projects:

- `SKILL.md` — skill metadata (YAML frontmatter: `name`, `description`)
- `README.md` — short overview and runbooks (optional)
- IaC & templates: CloudFormation/Terraform (`.yaml`, `.tf`)
- Contact flows and prompt exports: JSON (`.json`) exports
- Lambda functions: `.js`, `.py`, deployment packages
- Lex/Polly configs: intent/slot JSON, voice assets
- Analytics & exports: Kinesis/S3 exports, Contact Lens configs (`.json`)
- Docs & runbooks: `.md` (runbooks, escalation guides)

## Core Responsibilities

1. **Contact flow & routing** — Design IVR flows, queues, routing profiles, and agent experience.
2. **Telephony & connectivity** — Configure phone numbers, PSTN settings, and CCP behavior.

   - Citrix / VDI / HDX considerations: If agents run CCP inside virtual desktops (Citrix/HDX), verify browser and OS-level media/USB redirection settings and test WebRTC performance (latency and packet loss). Prefer solutions that support local media bridging, framed softphone, or native softphone clients when VDI causes audio/media issues, and provide an ops checklist for VDI deployments (supported browsers, HDX audio/USB policies, fallbacks).

3. **Integrations** — Hook into Lambda/CRM/databases for context, authentication, and routing decisions.
4. **Analytics & quality** — Enable Contact Lens, store call recordings, and build dashboards for KPIs.
5. **Security & compliance** — Support PCI/PII controls, redaction, encryption, and least-privilege IAM policies.

   - Agent persistence & session continuity: Persist agent session state server-side (session store/Redis) so brief client restarts or network blips can be recovered and agent context (active contacts, timers, routing profile) rehydrated on reconnect. Implement heartbeat and reconnection logic in the CCP to restore in-progress contacts where possible and surface clear guidance for agents; in VDI/HDX environments, coordinate with the VDI checklist and consider local media bridging to avoid media path disruptions during reconnects.
6. **Scaling & availability** — Architect multi-region or high-availability patterns where needed.

## Output style

- Provide stepwise runbooks and minimal, copyable CloudFormation/Terraform/Lambda snippets.
- Reference file names and configuration paths when suggesting edits.
- Prefer small, testable changes that can be validated by quick playbacks or test calls.

---

## Related skills

- `amazon-connect-custom-ccp` — Design and implementation scaffolding for a **custom Contact Control Panel (CCP)**, contact flows, routing profiles, security profiles, and campaign design. See `skills/amazon-connect-custom-ccp/SKILL.md` for detailed guidance and example scaffolding.

