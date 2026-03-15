---
name: change-management
description: Change management processes, impact assessment, approval workflows, and rollback procedures following ITIL and ISO 27001
license: Apache-2.0
---

# Change Management Skill

## Purpose
Defines change management processes ensuring controlled, documented changes with proper impact assessment and rollback capabilities.

## Change Categories
| Category | Description | Approval |
|----------|-------------|----------|
| Standard | Pre-approved, low risk | Automated |
| Normal | Requires assessment | PR review |
| Emergency | Critical fix needed | Post-approval |

## Change Process
1. **Request** — Document change and rationale
2. **Assess** — Impact analysis, risk assessment
3. **Approve** — Required reviewers sign off
4. **Implement** — Execute change with monitoring
5. **Review** — Verify change is effective
6. **Close** — Document results and lessons learned

## For Static Sites
- All changes via Pull Requests
- CI/CD validates before merge
- Automated rollback via git revert
- Feature flags for gradual rollout
- Monitoring after deployment

## Impact Assessment
- Which pages/languages affected?
- Performance impact (Lighthouse check)
- Accessibility impact (WCAG validation)
- SEO impact (structured data, meta tags)
- Security impact (headers, CSP)

## Rollback Procedures
- Git revert for code changes
- Previous deployment artifacts cached
- DNS rollback for infrastructure changes
- Communication plan for user-facing changes

## ISO 27001 Mapping
- A.8.32 — Change management
- A.8.9 — Configuration management

## Related Policies
- [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)
