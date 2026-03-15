---
name: send-sms
description: "Send SMS text messages to any phone number using the Twilio API. Use this skill when the user asks to send a text, SMS, text message, or notify someone via phone. Supports custom message content and any recipient number in E.164 format."
tags: [auto-generated, sms, twilio, messaging]
version: 0.2.0
---

# Skill: send-sms

## When to Use

Use this skill when the user asks to:

- Send an SMS or text message
- Text someone a message
- Notify someone via SMS
- Send a message to a phone number
- Use Twilio to message someone

## Required Credentials

Retrieve these via the `get_keys` tool before executing:

| Key Store Key         | Environment Variable | Description                         |
| --------------------- | -------------------- | ----------------------------------- |
| `twilio_account_sid`  | `TWILIO_ACCOUNT_SID` | Twilio Account SID (starts with AC) |
| `twilio_auth_token`   | `TWILIO_AUTH_TOKEN`  | Twilio Auth Token                   |
| `twilio_phone_number` | `FROM_PHONE_NUMBER`  | Twilio phone number (sender)        |

## Input Parameters

| Parameter      | Required | Description                            | Example     |
| -------------- | -------- | -------------------------------------- | ----------- |
| `to_phone`     | Yes      | Recipient phone number in E.164 format | +1234567890 |
| `message_body` | Yes      | The text message content to send       | Hello!      |

## Procedure

1. Retrieve Twilio credentials: use `get_keys` with keys `[twilio_account_sid, twilio_auth_token, twilio_phone_number]`
2. If recipient phone number or message content not provided, ask the user via `ask_user`
3. Send SMS using bundled script: `bash scripts/run.sh <to_phone> <message_body>`
   Or via curl: `curl -X POST "https://api.twilio.com/2010-04-01/Accounts/{{TWILIO_ACCOUNT_SID}}/Messages.json" --data-urlencode "From={{FROM_PHONE_NUMBER}}" --data-urlencode "To={{TO_PHONE_NUMBER}}" --data-urlencode "Body={{MESSAGE_BODY}}" -u "{{TWILIO_ACCOUNT_SID}}:{{TWILIO_AUTH_TOKEN}}"`
4. Verify the JSON response contains a `sid` field indicating the message was queued
5. Report delivery status and message SID to the user

## Bundled Scripts

| Script           | Type | Description             |
| ---------------- | ---- | ----------------------- |
| `scripts/run.sh` | SH   | Send SMS via Twilio API |

### Script Usage

```bash
# Set credentials as environment variables (from get_keys), then:
bash scripts/run.sh <to_phone> <message_body>
```

Credentials in scripts use environment variables. Set them via `get_keys` before running.

## Example

Example requests that trigger this skill:

```
send an sms saying "hello world"
text +1234567890 saying "meeting at 3pm"
send a text message to mom
```
