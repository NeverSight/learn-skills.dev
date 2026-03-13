---
name: phone-agent
description: Use AI AutoGLM Phone Agent for automated mobile device control. Suitable for tasks requiring mobile phone automation, such as APP automated testing, data collection, UI interaction, etc. Supports controlling the mobile interface through natural language instructions to implement operations such as clicking, sliding, inputting, and screenshotting.
---

# AutoGLM Phone Agent Skill

This skill lets Codex drive an Android device through the AutoGLM Phone Agent SDK: tap, type, swipe, scroll, launch apps, take screenshots, and read UI text. It is aimed at automation tasks such as end-to-end testing, data collection, or reproducing user journeys.

## Prerequisites
- An Android device or emulator with developer mode and USB debugging enabled.
- `adb` available in the path and the device showing up in `adb devices`.
- AutoGLM Phone Agent SDK installed (see upstream docs: https://github.com/zai-org/Open-AutoGLM).
- A running Phone Agent backend (start the agent service provided by the SDK before using the skill).

## Setup
1) Connect the device and verify connectivity: `adb devices` should list at least one device as `device`.
2) Follow the SDK guide to start the Phone Agent service (typically binds to a host/port on your machine). Note the service URL.
3) Expose the service URL to the agent runtime, for example by setting `PHONE_AGENT_ENDPOINT=http://127.0.0.1:5000` (adapt to your actual host/port).
4) Grant the device the needed permissions (overlay/accessibility) when prompted by the SDK so that taps and text entry succeed.

## How to Use
- Describe high-level goals; the agent decomposes them into UI steps.
- Include app names or on-screen text to anchor actions (e.g., "open Settings, search for 'Wi‑Fi', toggle it off").
- Ask for confirmation screenshots when changes are risky.

Example prompts the skill handles well:
- "Open the Play Store, search for 'Signal', and share the first result link back."
- "In the Twitter app, open settings → Privacy and turn off location precision, then send me a screenshot of the toggle state."
- "Launch our test app, log in with the provided test account, and capture the purchase confirmation screen."

## Outputs
- Action logs (tap/swipe/type), screenshots, and structured observations returned by the SDK.
- Errors from the backend are surfaced directly so you can troubleshoot quickly.

## Troubleshooting
- If commands hang, confirm the Phone Agent service is reachable at `PHONE_AGENT_ENDPOINT` and that the port is not firewalled.
- If taps land in the wrong place, recalibrate the device resolution in the SDK or restart the accessibility service.
- If no device is detected, reconnect USB, ensure `adb` has permission, and rerun `adb devices`.

## Safety and Limits
- The skill executes real UI actions—use only on test devices or accounts when possible.
- Avoid tasks that require biometric auth; the SDK cannot bypass hardware prompts.
- Network-dependent steps may vary by region or app version; provide explicit fallbacks when reliability matters.

## Changelog
- 1.0.0: Initial publication with setup, usage guidance, and troubleshooting notes for the AutoGLM Phone Agent.
