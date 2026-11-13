---
name: skill-code-review
description: Perform thorough, constructive code reviews focusing on correctness, security, maintainability, and best practices
---

# skill-code-review


# Code Review Skill Instructions

## Purpose
Conduct comprehensive code reviews that improve code quality, catch bugs early, ensure security, and promote team learning through constructive feedback.

## When to Use
- Pull request reviews
- Pre-merge code inspections
- Security audits
- Refactoring validation
- New feature implementation reviews

---

## Review Process

### 1. Understand Context First
- Read the PR/change description and linked issues
- Understand the **intent** and **scope** of the change
- Check if tests and documentation are included
- Review the overall architecture impact

### 2. Review Checklist

#### ✅ Correctness
- [ ] Does the code do what it's supposed to do?
- [ ] Are edge cases handled properly?
- [ ] Is the logic correct and complete?
- [ ] Are there any off-by-one errors, null pointer issues, or race conditions?

#### 🔒 Security
- [ ] Input validation and sanitization
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] Proper authentication and authorization checks
- [ ] SQL injection, XSS, CSRF protection
- [ ] Secure handling of sensitive data
- [ ] Dependencies free of known vulnerabilities

#### 🏗️ Architecture & Design
- [ ] Follows SOLID principles
- [ ] Appropriate separation of concerns
- [ ] No unnecessary coupling between components
- [ ] Consistent with existing patterns in the codebase
- [ ] Scalability considerations addressed

#### 📖 Readability & Maintainability
- [ ] Clear, descriptive naming (variables, functions, classes)
- [ ] Functions are small and do one thing well
- [ ] No magic numbers or strings (use constants)
- [ ] Complex logic is commented or self-documenting
- [ ] No dead code or commented-out code blocks

#### ⚡ Performance
- [ ] No N+1 queries or unnecessary database calls
- [ ] Efficient algorithms and data structures
- [ ] Proper caching where appropriate
- [ ] No memory leaks or resource exhaustion risks
- [ ] Async operations used correctly

#### 🧪 Testing
- [ ] Unit tests cover new functionality
- [ ] Edge cases and error paths tested
- [ ] Tests are readable and maintainable
- [ ] No flaky or brittle tests
- [ ] Integration tests where appropriate

#### 📝 Documentation
- [ ] Public APIs documented
- [ ] Complex business logic explained
- [ ] README updated if needed
- [ ] Breaking changes documented

---

## Feedback Guidelines

### Be Constructive
```
❌ "This code is bad"
✅ "Consider extracting this into a separate function for better testability"
```

### Be Specific
```
❌ "Fix the naming"
✅ "Rename `data` to `userProfile` to clarify its purpose"
```

### Explain the Why
```
❌ "Don't use var"
✅ "Use `const` instead of `var` to prevent accidental reassignment and improve code clarity"
```

### Categorize Feedback Severity

| Prefix | Meaning | Action Required |
|--------|---------|-----------------|
| 🚨 **BLOCKER** | Critical issue, must fix | Cannot merge |
| ⚠️ **WARNING** | Should fix, potential problem | Strongly recommended |
| 💡 **SUGGESTION** | Improvement opportunity | Optional |
| ❓ **QUESTION** | Clarification needed | Please explain |
| 👍 **PRAISE** | Great work! | Keep it up |

---

## Comment Templates

### Security Issue
```
🚨 **BLOCKER - Security**: User input is not sanitized before being used in the SQL query. 
This creates a SQL injection vulnerability.

**Suggestion**: Use parameterized queries or an ORM to safely handle user input.
```

### Performance Concern
```
⚠️ **WARNING - Performance**: This loop makes a database call on each iteration, 
resulting in N+1 queries.

**Suggestion**: Batch the queries or use eager loading to fetch all data upfront.
```

### Code Quality Suggestion
```
💡 **SUGGESTION**: This function is 80 lines long with multiple responsibilities.

Consider splitting into:
- `validateInput()` - Input validation
- `processData()` - Core business logic  
- `formatResponse()` - Response formatting
```

### Positive Feedback
```
👍 **PRAISE**: Excellent error handling here! The fallback mechanism and 
detailed logging will make debugging much easier.
```

---

## Review Output Format

Structure your review as follows:

```markdown
## Code Review Summary

**Overall Assessment**: ✅ Approved | ⚠️ Needs Changes | 🚨 Request Changes

### Overview
Brief summary of what was reviewed and overall impressions.

### Critical Issues (Must Fix)
- Issue 1 with location and fix suggestion
- Issue 2 with location and fix suggestion

### Recommendations (Should Fix)
- Recommendation 1
- Recommendation 2

### Suggestions (Nice to Have)
- Suggestion 1
- Suggestion 2

### Positive Highlights
- What was done well

### Questions
- Any clarifications needed
```

---

## Best Practices

1. **Review in small batches** - Keep PRs small (<400 lines) for effective review
2. **Take your time** - Don't rush; bugs missed in review are expensive later
3. **Be respectful** - Review the code, not the person
4. **Assume good intent** - Authors did their best with available information
5. **Offer alternatives** - Don't just criticize; provide solutions
6. **Learn together** - Reviews are learning opportunities for everyone
7. **Follow up** - Verify fixes address the concerns raised

---

## Anti-Patterns to Avoid

- ❌ Nitpicking style issues (use linters instead)
- ❌ Rewriting someone's code in your style
- ❌ Blocking PRs for subjective preferences
- ❌ Reviewing without understanding context
- ❌ Being vague or unconstructive
- ❌ Ignoring positive aspects of the code
