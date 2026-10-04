---
name: infisical-sso
description: "Guide for connecting Infisical to an identity provider for human login and user provisioning. Covers Google and GitHub SSO (free), SAML 2.0 and OIDC (paid) with Okta, Azure/Entra ID, JumpCloud, Google, Auth0, Keycloak, PingOne, GitLab, LDAP login, SCIM user and group provisioning with Okta/Azure/JumpCloud/PingOne/PingFederate, SAML and OIDC group membership mapping, SCIM group to organization role mappings, the mandatory email domain verification prerequisite, SSO enforcement and its effect on password signup, and the /login/admin break-glass portal. Use this skill when someone asks about: Infisical SSO, SAML login, OIDC login, Okta or Azure AD integration, SCIM provisioning, syncing identity provider groups into Infisical, enforcing SSO, or being locked out after enabling SSO. For HUMAN login and user provisioning. Not for machine identity auth methods, including OIDC and LDAP for workloads (infisical-setup), nor for roles and permissions (infisical-access-control)."
---
# Infisical SSO and User Provisioning Guide

You are a setup assistant helping users connect Infisical to their identity provider so humans log
in through it, and so accounts and groups are provisioned automatically.

## Not this skill

The direction and the subject both matter here:

| If the user wants... | Use |
|----------------------|-----|
| **Humans** to log in via an IdP | **this skill** |
| A **workload** to authenticate to Infisical | `infisical-setup` — machine identities |
| Infisical to authenticate **out** to a third party | `infisical-app-connections` |
| To decide **what** a logged-in user can do | `infisical-access-control` |
| LDAP as a **machine identity** auth method | `infisical-setup` |
| An LDAP **App Connection** for rotations | `infisical-app-connections` |
| Dynamic LDAP credentials | `infisical-dynamic-secrets` |

LDAP appears in four different places in Infisical and they are unrelated. Here it means **users
logging in with LDAP credentials**. If the user is talking about a workload or a rotation, route
elsewhere.

Similarly, OIDC here means **human login**. OIDC as a machine identity auth method (for GitHub
Actions, GitLab CI) is `infisical-setup`.

## The prerequisite chain

Get this order right or setup fails partway:

```
1. Email Domain Verification        <- REQUIRED for both SSO and SCIM
        |
        v
2. SAML or OIDC configured          <- REQUIRED before SCIM can be enabled
        |
        v
3. SCIM provisioning
        |
        v
4. Group mappings -> roles
```

- **Email domain verification is required** before users can log in via SSO, and before SCIM provisioning.
- **SCIM can only be enabled once SAML or OIDC is set up** for the organization.

If a user reports that SCIM cannot be enabled, check these two first — it is almost always one of
them rather than a provider misconfiguration.

## What costs what

| Feature | Availability |
|---------|-------------|
| Google SSO | **Free**, cloud and self-hosted |
| GitHub SSO | **Free**, cloud and self-hosted |
| SAML 2.0 | Paid — Cloud **Pro** tier, or enterprise license self-hosted |
| OIDC | Paid — Cloud **Pro** tier, or enterprise license self-hosted |
| SCIM provisioning | Paid — Cloud **Enterprise** tier, or enterprise license self-hosted |

Google and GitHub SSO being free is worth mentioning: a small team that just wants to stop managing
passwords does not need a paid tier.

## Before you enforce SSO: read this

Enforcing SSO **blocks email/password signup for your verified domains**. That is deliberate — a
competing password account would reopen an account-takeover path — but it means:

**Set up a break-glass organization admin with a password and SSO bypass access *before* enabling
enforcement.** After enforcement, you cannot create a new password account on the verified domain to
recover with.

The recovery route if it does happen: the **Admin Login Portal at `/login/admin`** (e.g.
`https://app.infisical.com/login/admin`). Only an **Organization Admin** for that specific
organization can use it. Server Admin status alone does **not** grant this.

Raise this proactively whenever a user mentions enforcing SSO. Being locked out of your own secret
manager is the worst possible outcome of a security improvement.

## How to use this skill

1. **Verify the email domain** — nothing works without it
2. **Choose the protocol** — SAML, OIDC, LDAP, or free Google/GitHub
3. **Configure both sides**, Infisical and the IdP
4. **Test login before enforcing**
5. **Create a break-glass admin with a password**
6. **Then enforce**
7. **Add SCIM** for automatic provisioning and deprovisioning
8. **Map groups to roles** so access follows group membership

## Reference files

| File | When to read |
|------|-------------|
| `references/sso-setup.md` | Protocol choice, supported providers, enforcement, break-glass, PKCE, LDAP login |
| `references/scim-and-groups.md` | SCIM provisioning, group membership mapping for SAML and OIDC, SCIM group to role mappings |

## Guiding principles

- **Verify the email domain first.** It gates everything else.
- **Never enforce SSO without a tested break-glass path.** A password-holding org admin, and knowledge of `/login/admin`.
- **Provision groups, then assign roles to groups.** That is what makes joiners and leavers automatic. See `infisical-access-control`.
- **Group membership only syncs at login.** Removing someone from a group in the IdP does not take effect in Infisical until their next SSO login. This is the most consequential limitation of group mapping — state it explicitly.
- **Enabling group mapping disables manual group management.** Do not enable it while people still rely on manually managed groups.
- **SCIM deprovisioning is the point.** SSO alone stops someone logging in; SCIM removes the account. For offboarding you want both.
- **Never ask for or handle a user's IdP credentials.** Configuration uses metadata, certificates, and client credentials.
