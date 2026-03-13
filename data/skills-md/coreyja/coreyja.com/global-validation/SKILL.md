---
name: Global Validation
description: Implement secure, comprehensive input validation on both client and server sides using allowlists, type checking, and sanitization to prevent injection attacks. Use this skill when handling user input from forms, API requests, or any external data source. When implementing form validation logic with field-specific error messages. When validating data types, formats, ranges, and required fields. When sanitizing input to prevent SQL injection, XSS, or command injection. When validating business rules like sufficient balance or valid date ranges. When implementing both client-side validation for user experience and mandatory server-side validation for security.
---

# Global Validation

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global validation.

## When to use this skill

- When handling user input from forms, API endpoints, or external data sources
- When implementing form validation with field-specific error messages
- When validating data types, formats (email, phone, URL), ranges, and required fields
- When sanitizing user input to prevent injection attacks (SQL, XSS, command injection)
- When implementing client-side validation for immediate user feedback
- When implementing mandatory server-side validation for security and data integrity
- When validating business rules (sufficient balance, valid date ranges, stock availability)
- When using allowlists to define what input is acceptable rather than blocklists
- When applying validation consistently across all entry points (web, API, background jobs)
- When failing early by rejecting invalid data before processing

## Instructions

For details, refer to the information provided in this file:
[global validation](../../../agent-os/standards/global/validation.md)
