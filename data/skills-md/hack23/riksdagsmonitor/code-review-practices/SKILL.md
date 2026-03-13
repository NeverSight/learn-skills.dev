---
name: code-review-practices
description: Code review best practices, quality gates, security checks, and constructive feedback guidelines for collaborative development
license: Apache-2.0
---

# Code Review Practices Skill

## Purpose
Establishes effective code review practices that improve code quality, catch bugs early, and maintain security standards while fostering collaborative development.

## Review Checklist

### MUST CHECK
1. **Functionality** — Code solves the stated problem, edge cases handled
2. **Design** — Follows project patterns, appropriate abstraction
3. **Code Quality** — Readable, maintainable, DRY, proper naming
4. **Testing** — Unit tests included, coverage adequate, edge cases tested
5. **Security** — No hardcoded secrets, input validation, XSS/injection prevention
6. **Performance** — No obvious inefficiencies, queries optimized
7. **Documentation** — README updated, complex logic explained

## PR Size Guidelines
- Small: < 200 lines (ideal)
- Medium: 200-500 lines (acceptable)
- Large: 500-1000 lines (split if possible)
- XL: > 1000 lines (must split)

## Feedback Guidelines

### Effective Comments
- Focus on code, not the person
- Provide constructive suggestions with examples
- Use labels: `MUST FIX`, `SHOULD FIX`, `NIT`, `QUESTION`, `SUGGESTION`, `PRAISE`

### Security-Focused Review
- Authentication/authorization checks
- Input validation and sanitization
- No secrets in code, secure logging
- Dependencies from trusted sources
- Lock files updated

## Approval Criteria
- ✅ APPROVE: All MUST FIX resolved, tests passing, security checks pass
- 💬 COMMENT: Clarification needed, non-blocking suggestions
- 🔄 REQUEST CHANGES: Critical bugs, security vulnerabilities, missing tests

## Related Policies
- [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)
