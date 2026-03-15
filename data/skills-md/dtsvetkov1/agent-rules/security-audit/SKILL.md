---
name: security-audit
description: Scans code for security vulnerabilities, hardcoded secrets, and unsafe patterns in React Native and Expo applications. Use before merging sensitive changes or as part of a regular audit.
---

# Security Audit Skill

This skill focuses on making the application robust against common mobile security threats.

## Instructions

1. **Secret Scanning**: Check for API keys, passwords, or tokens in the codebase.
2. **Data Storage**: Ensure sensitive data is stored in `expo-secure-store` and not `AsyncStorage`.
3. **Network**: Verify that all API calls use HTTPS and that SSL pinning is considered for high-security apps.
4. **Input Validation**: Check for unsanitized inputs that could lead to XSS or injection.
5. **Permissions**: Review `app.json` for unnecessary permissions.

## Tools to Simulate/Use

- `bunx audit` (for dependencies)
- Custom grep patterns for secrets (e.g., `sk-`, `AIza`, `ghp_`)
- Checking for `dangerouslySetInnerHTML` in web-related components.

See [Mobile Security Checklist](references/CHECKLIST.md) for a comprehensive list.
