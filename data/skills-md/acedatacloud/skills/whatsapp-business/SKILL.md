---
name: whatsapp-business
description: Inspect approved WhatsApp Business templates and send an opted-in template through Meta's official Cloud API. Use for a specific customer follow-up, never cold outreach or list blasting.
when_to_use: |
  Use for a connected WhatsApp Business Account when the user identifies the
  recipient, an approved template, and the recipient's opt-in record. This
  connector does not read inbound chats or discover new leads.
connections: [whatsappbusiness]
allowed_tools: [Bash]
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
---

# WhatsApp Business Cloud API

The connector injects `$WHATSAPPBUSINESS_ACCESS_TOKEN`,
`$WHATSAPPBUSINESS_PHONE_NUMBER_ID`, and `$WHATSAPPBUSINESS_WABA_ID`. Never
print or place the access token in a URL. This skill uses Meta's official
Cloud API, not personal WhatsApp automation.

```bash
SCRIPT="$SKILL_DIR/scripts/whatsapp_business.py"
python3 "$SCRIPT" templates
python3 "$SCRIPT" send-template --to +919876543210 --template welcome_followup \
  --language en_US --opt-in-reference CRM-12345
# Show recipient, template, variables, and opt-in evidence before the write:
python3 "$SCRIPT" send-template --to +919876543210 --template welcome_followup \
  --language en_US --opt-in-reference CRM-12345 --confirm
```

For a template with variables, pass `--components-file components.json` using
Meta's `components` array shape. The send command defaults to a dry run;
`--confirm` sends exactly one message. A response message ID means Meta
accepted the request, **not** that the customer received it. Delivery requires
a configured webhook or later provider readback; this connector does not claim
delivery. Never send to a batch, guess an opt-in reference, or use the token to
message people who have not opted in.

Official reference: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages .
