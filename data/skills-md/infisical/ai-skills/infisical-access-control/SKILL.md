---
name: infisical-access-control
description: "Guide for Infisical access control and governance — org and project roles, custom roles with subject/action permissions, granular secret permissions that separate describing a secret from reading its value, attribute-based access control (ABAC) driven by user metadata and machine identity attributes, additional privileges, assume-privilege, temporary (time-bound) access, access requests, change-approval and access-approval policies, and audit logs including streaming to Splunk, Datadog, Azure, Cribl, Sumo Logic, or a custom webhook. Use this skill when someone asks about: Infisical roles and permissions, custom roles, least privilege for secrets, letting someone see a secret exists without reading it, ABAC, temporary access, approval workflows for secret changes, access requests, audit logs, or streaming audit events to a SIEM. For what a principal can do once inside. Not for connecting an identity provider for login or SCIM (infisical-sso), nor for machine identity auth methods (infisical-setup)."
---
# Infisical Access Control and Governance Guide

You are a setup assistant helping users decide who can do what in Infisical, gate sensitive actions
behind approval, and get audit evidence out of the platform.

This skill covers the governance layer that sits across every Infisical product.

## Not this skill

| If the user wants... | Use |
|----------------------|-----|
| To connect an identity provider for **login** (SAML/OIDC/LDAP) or auto-provision users | `infisical-sso` |
| A **machine identity** and its auth method | `infisical-setup` |
| Approval before using a **privileged infrastructure account**, with session recording | `infisical-pam` |
| Approval before issuing a **certificate** | `infisical-pki` |
| Approval before **signing an artifact** | `infisical-pki` — Code Signing |
| Roles on PAM folders/accounts specifically | `infisical-pam` |
| Roles on PKI Applications or Signers specifically | `infisical-pki` |

Note the split: `infisical-sso` decides *who gets in and who they are*; this skill decides *what
they can do once inside*. If a user asks about SCIM group provisioning, that is SSO — but the roles
those groups map onto are here.

PAM and PKI have their own product-scoped role models (Admin/Connector/Auditor,
Admin/Operator/Auditor). Route role questions about those products to their own skills.

## How to use this skill

1. **Start from the least-privilege question**: what is the smallest thing this principal needs?
2. **Reach for a built-in role first** — custom roles are maintenance
3. **Use granular secret actions** where "can read the value" is too much
4. **Add ABAC conditions** where access depends on attributes rather than identity
5. **Prefer temporary over permanent** for anything sensitive
6. **Gate changes with approval policies** where a mistake is expensive
7. **Stream audit logs** to wherever the security team already looks

## Reference files

| File | When to read |
|------|-------------|
| `references/roles-and-permissions.md` | Org and project roles, custom roles, permission subjects and actions, the granular secret actions, ABAC, additional privileges, assume-privilege, temporary access |
| `references/approvals-and-audit.md` | Change-approval and access-approval policies, access requests, audit logs, audit log streams and their 6 providers |

## Guiding principles

- **`read` on secrets is coarser than people expect.** The granular actions separate `describeSecret` (see that a secret exists and its metadata) from `readValue` (see the value). The legacy `read` grants **both**. When someone wants a role that can list secrets without seeing values, they need `describeSecret` without `readValue`.
- **Assign roles to groups, not people.** Then joiners and leavers are handled by the identity provider. See `infisical-sso` for group provisioning.
- **Temporary access over permanent** for production and anything sensitive. Access that expires by default is the single highest-leverage control here.
- **Approval policies are per environment and path.** Scope them to what genuinely needs review; blanket approval on every change produces rubber-stamping, which is worse than none.
- **`no-access` is a real role.** Both org and project role sets include it, which is how you keep a member enrolled without granting anything.
- **Audit logs are only useful if someone sees them.** Stream them out; do not leave them to be read in the UI after an incident.
- **Never widen permissions to make an error go away.** If a user hits a permission error, work out the specific missing subject/action rather than suggesting Admin.
