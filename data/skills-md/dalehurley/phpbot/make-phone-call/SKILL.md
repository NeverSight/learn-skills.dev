---
name: make-phone-call
description: "Initiate phone calls with text-to-speech messages using the Twilio API. Use this skill when the user asks to make a phone call, call someone, initiate a call, or send a voice message to a phone number. Supports custom message content and any recipient number in E.164 format."
tags: [communication, twilio, voice, automation, telephony, auto-generated]
version: 0.1.0
---

# Skill: make-phone-call

## Overview

This skill uses the Twilio API to programmatically initiate outbound phone calls with text-to-speech messages. The call is queued immediately and the recipient will hear the message read aloud when they answer.

## When to Use

Use this skill when the user asks to:
- Make a phone call
- Call someone
- Initiate an outbound call
- Send a voice message
- Notify someone via phone call
- Leave a voice message

## Required Credentials

Retrieve these via the `get_keys` tool before executing:

| Key Store Key | Environment Variable | Description |
|---------------|---------------------|-------------|
| `twilio_account_sid` | `TWILIO_ACCOUNT_SID` | Your Twilio Account SID for API authentication |
| `twilio_auth_token` | `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token for API authentication |
| `twilio_phone_number` | `TWILIO_PHONE_NUMBER` | Your Twilio phone number to send calls from |

### Twilio Setup

1. Create a Twilio account at twilio.com
2. Verify your identity and get your Account SID and Auth Token from the Console dashboard
3. Purchase or verify a phone number for making outbound calls
4. Store credentials in the key store: twilio_account_sid, twilio_auth_token, twilio_phone_number

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `recipient_phone_number` | Yes | The phone number to call in E.164 format | {{PHONE_NUMBER}} |
| `message_text` | Yes | The message to be read aloud via text-to-speech | hey buddy |

## Procedure

1. Retrieve Twilio credentials using `get_keys` with keys `[twilio_account_sid, twilio_auth_token, twilio_phone_number]`
2. Get the recipient phone number and message content from the user if not provided (use `ask_user`)
3. Validate phone numbers are in E.164 format (e.g., {{PHONE_NUMBER}})
4. Install Twilio Node.js package if not already present: `npm install twilio`
5. Create and execute the call script using bundled `make_call.js` with recipient number and message text
6. Verify the response contains a Call SID indicating successful queue
7. Report call status and SID to the user

## Output

A confirmation message containing the Call SID, recipient number, sender number, message text, and call status (queued).

## Bundled Scripts

| Script | Type | Description |
|--------|------|-------------|
| `scripts/make_call.js` | JS | Auto-captured from task execution |

Credentials in scripts use environment variables. Set them via `get_keys` before running.

## Reference Commands

Commands for executing this skill (adapt to actual inputs):

```bash
npm install twilio
node make_call.js {{RECIPIENT_PHONE}} {{MESSAGE_TEXT}}
```

Replace `{{PLACEHOLDER}}` values with actual credentials from the key store.

## Example

Example requests that trigger this skill:

```
make a phone call to confirm the appointment
```

## Notes

- Phone numbers must be in E.164 format (e.g., {{PHONE_NUMBER}} for US numbers)
- Twilio trial accounts can only call verified phone numbers
- The call is queued immediately; actual connection may take a few seconds
- Text-to-speech voice is set to 'alice' by default
- Ensure the Twilio phone number has outbound calling permissions enabled


## Keywords

call, phone, voice, twilio, outbound, text-to-speech, tts, notify
