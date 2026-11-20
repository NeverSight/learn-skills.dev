---
name: infisical-pam
description: "Guide for Infisical Privileged Access Manager (PAM) — brokering human and AI-agent access to databases, servers, Kubernetes clusters, and cloud accounts without the connecting party ever seeing a credential, with full session recording and audit. Covers all 13 account types (SSH, PostgreSQL, MySQL, MSSQL, OracleDB, MongoDB, Redis, Kubernetes, AWS IAM, GCP service account, Azure CLI, Windows, Windows AD), the accounts/folders/templates/memberships model, Admin/Connector/Auditor roles, session lifecycle and recording, just-in-time access requests with approvals, account credential rotation, discovery, dependencies, web and CLI access, and agentic access for AI agents via `infisical pam agentic access`. Use this skill when someone asks about: Infisical PAM, privileged access, session recording, just-in-time database access, brokered SSH access, giving an AI agent database access safely, access requests and approvals for infrastructure, or 'how do I let someone into production without giving them the password'. For humans and AI agents reaching infrastructure without ever holding a credential. Not for applications fetching a credential themselves (infisical-dynamic-secrets)."
---
# Infisical Privileged Access Manager (PAM) Guide

You are a setup assistant helping users broker privileged access to infrastructure through
Infisical PAM.

The core property: **the connecting party never sees the credential.** A person or an AI agent
connects through Infisical, Infisical holds the real credential and proxies the connection, and
every query or command is recorded.

PAM is a **separate Infisical product** with its own project type (`pam`). Enterprise feature.

## Not this skill

The boundary is *who or what is connecting, and whether they see a credential*:

| If the user wants... | Use |
|----------------------|-----|
| A **person or agent** to reach a database/server without holding a credential, with recording | **this skill** |
| An **application** to fetch a credential and connect itself | `infisical-dynamic-secrets` or `infisical-setup` |
| An ephemeral credential handed to a workload | `infisical-dynamic-secrets` |
| An existing credential rotated on a schedule into secrets | `infisical-secret-rotation` |
| Approval workflows for **secrets**, not infrastructure | `infisical-access-control` |
| To deploy the Gateway that PAM proxies through | `infisical-gateway` |

The sharpest distinction is PAM versus dynamic secrets. Both give time-bound access, but:

- **Dynamic secrets** hand a real credential to the consumer. Good for applications and CI, which need to connect themselves.
- **PAM** never hands over a credential. Infisical proxies the session. Good for humans and AI agents, where you want recording and the ability to terminate mid-session.

If the user says "I want engineers to query production without knowing the password," that is PAM.
If they say "my service needs a database credential," that is dynamic secrets.

## The four components

Get this model right and the rest follows:

| Component | What it is |
|-----------|-----------|
| **Account** | One database, server, cluster, or cloud account. Holds connection details and credentials |
| **Folder** | A grouping of accounts **by who needs access**. Permissions are set here |
| **Account Template** | The policy applied when connecting: max session duration, reason required, MFA required. Type-specific |
| **Membership** | Assigns a user, group, or machine identity a role on a folder or account |

The rule to remember: **templates define rules, folders define access.**

- Accounts in the same folder can use different templates — same team, different rules
- Accounts in different folders can share a template — same rules, different teams
- Folder memberships **cascade** to every account inside; assign directly on an account only for exceptions

Organize folders by *who needs access*, not by technology. `backend-team` is a better folder than
`postgres-databases`, because permissions live at the folder level.

## Roles

| Role | Capabilities |
|------|-------------|
| **Admin** | Full control — accounts, folders, sessions, memberships |
| **Connector** | Launch sessions and connect to accounts |
| **Auditor** | View audit logs and session recordings |

Machine identities hold these same roles. **Connector** is the usual choice for an unattended AI
agent.

There is also a product-level role split (`admin`, `member`) governing who can create Accounts and
Folders at all.

## How to use this skill

1. **Confirm PAM is right** — the connecting party must not hold a credential (see the table above)
2. **Check the Gateway story** — PAM proxies through a Gateway; internal targets need one
3. **Model folders around teams**, not technologies
4. **Create accounts** with connection details and credentials
5. **Pick or create templates** for session policy
6. **Assign memberships** at the folder level
7. **Decide on just-in-time access** — standing Connector access, or access requests with approval
8. **Confirm recording and auditing** meet the requirement

## Reference files

| File | When to read |
|------|-------------|
| `references/accounts-and-access.md` | All 13 account types, per-type auth options, folders, templates, memberships, access requests, discovery, dependencies |
| `references/sessions-and-agents.md` | Session lifecycle and states, recording, termination, web vs CLI access, agentic access for AI agents |

## Guiding principles

- **Never route a credential to the user.** The whole value of PAM is that they do not get one. If a user asks how to retrieve the underlying password, explain that PAM deliberately does not expose it.
- **PAM needs a Gateway for anything internal.** Connections are proxied. See `infisical-gateway`.
- **Folders are the permission boundary.** Someone with access to a folder reaches every account in it. That makes folder design a security decision, not an organizational nicety.
- **Recording is real-time.** Recordings can be reviewed while a session is still active, and an admin can terminate mid-session. Mention this for incident-response scenarios.
- **Require a reason and MFA on production templates.** They are template settings, cheap to enable, and they are what makes the audit trail meaningful after the fact.
- **Agentic access is the right answer for AI agents.** `infisical pam agentic access -- <agent>` sandboxes the agent and brokers its access; do not suggest putting a connection string in an agent's environment.
- **Session TTLs are ceilings, not targets.** Set the maximum session duration to the shortest thing that lets real work finish.
