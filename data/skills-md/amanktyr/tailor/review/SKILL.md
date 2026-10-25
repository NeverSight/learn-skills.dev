---
name: review
description: Guides comprehensive code and architecture reviews (/review or tailor review), evaluating duplication, security risks, performance bottlenecks, and convention adherence.
---

# Code & Architecture Review Skill

Activate this skill when reviewing code changes, evaluating pull requests, or conducting a project-wide health review (`/review` or `tailor review`).

> **Review Directive:** *Provide actionable, prioritized feedback focusing on architecture, security, code reuse, and long-term maintainability.*

---

## 1. Multi-Dimensional Review Rubric

Evaluate code changes across 5 core dimensions:

1. **Architecture & Boundaries:** Does the implementation violate established ADRs in `.ai/DECISIONS.md` or cross layer boundaries illegally?
2. **Reuse & Duplication:** Could this code have reused existing components, utilities, or abstractions instead of introducing duplicates?
3. **Dependency Governance:** Were unnecessary external packages added when standard library primitives or native APIs suffice?
4. **Security & Validation:** Are user inputs sanitized? Are database queries parameterized? Are secrets kept out of source code?
5. **Testing & Quality:** Are there targeted tests covering happy paths, error handling, and edge cases?

---

## 2. Standardized Actionable Finding Schema

Structure all review feedback using this concise format:

```markdown
### [SEVERITY] REV-00X: [Clear Issue Summary]
- **Severity Level:** CRITICAL | HIGH | MEDIUM | LOW | INFO
- **File Location:** `src/features/auth/login.ts:28`
- **Problem Statement:** Concise explanation of the flaw or anti-pattern.
- **Impact & Risk:** Why this matters (security compromise, memory leak, code duplication).
- **Remediation Code:**
  ```ts
  // Replace the insecure/duplicate block with this implementation
  ```
```

---

## 3. Pull Request Review Checklist

- [ ] Zero unvalidated user inputs reaching database or shell execution.
- [ ] Zero hardcoded credentials, API keys, or JWT secrets.
- [ ] Existing UI components and helpers reused where applicable.
- [ ] No new micro-packages introduced without justification.
- [ ] All automated tests pass with exit code 0.
- [ ] Updated project memory documentation in `.ai/` if architecture or schemas changed.
