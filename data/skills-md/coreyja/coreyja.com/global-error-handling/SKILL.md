---
name: Global Error Handling
description: Implement robust error handling with user-friendly messages, specific exception types, centralized error boundaries, and graceful degradation strategies. Use this skill when implementing error handling logic in any part of the application. When writing try-catch blocks, error boundaries, or exception handlers. When validating input and failing fast with clear error messages. When handling API errors, network failures, or external service timeouts. When implementing retry strategies with exponential backoff. When ensuring resources are properly cleaned up in finally blocks. When displaying error messages to users without exposing technical details. This skill applies to all error handling across frontend and backend code.
---

# Global Error Handling

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global error handling.

## When to use this skill

- When implementing error handling logic in any application code
- When writing try-catch blocks or error boundaries in components
- When handling API errors, network failures, or timeout scenarios
- When validating input and failing fast with explicit error messages
- When implementing retry strategies with exponential backoff for transient failures
- When cleaning up resources (file handles, connections, locks) in finally blocks
- When using specific exception types rather than generic error classes
- When designing systems with graceful degradation for non-critical service failures
- When centralizing error handling at controller, API, or component boundaries
- When displaying user-friendly error messages without exposing security information

## Instructions

For details, refer to the information provided in this file:
[global error handling](../../../agent-os/standards/global/error-handling.md)
