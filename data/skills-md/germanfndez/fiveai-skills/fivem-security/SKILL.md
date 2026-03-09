---
name: fivem-security
description: Best practices and rules for securing FiveM resources against cheaters and exploits. Use this skill when writing or reviewing server-side and client-side code to ensure malicious events, unauthorized entity creations, and client trust issues are prevented. Focuses on strict server authority and safe event handling.
---

# 🛡️ FiveM Security & Anti-Exploit Principles

This skill provides architectural guidance for securing FiveM resources against common cheats, unauthorized event triggers, and malicious data manipulation.

**Core Philosophy:** NEVER TRUST THE CLIENT. 

The client is in the hands of the user, which means it can be fully compromised. Every action that affects the game state, economy, or other players MUST be validated on the server.

## 📂 Core Concepts & Rules

Detailed rules are broken down into specific topics within the `rules/` directory:

- **[events.md](rules/events.md)**: How to properly structure and validate `RegisterNetEvent` / `TriggerServerEvent` to prevent unauthorized execution.

## ⚠️ The Golden Rules of FiveM Security

1. **Server Authority**: The server dictates the truth. The client only requests actions.
2. **Never Trust Parameters**: Always validate arguments sent from the client (e.g., if a client says "give me $50", the server must check if the client *earned* it, not just blindly accept the amount).
3. **Distance Checks**: Always check the distance on the server side before allowing an interaction (e.g., looting, selling, entering a zone).
4. **Rate Limiting**: Prevent event spamming by implementing server-side cooldowns or debouncing for critical actions.