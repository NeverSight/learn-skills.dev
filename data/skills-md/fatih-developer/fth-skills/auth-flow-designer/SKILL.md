---
name: auth-flow-designer
description: Determines whether to use API keys, JWT, OAuth2, or mTLS. Designs token lifespans, refresh token strategies, and secure session management.
---

# Auth Flow Designer Protocol

This skill designs the authentication and authorization strategy for an API. It prevents developers from defaulting to "Just use JWTs for everything," ensuring the right security model is applied based on the consumers and the data sensitivity.

**Core assumption:** A leaked token is inevitable. The architecture must minimize the damage through short lifespans, refresh flows, and tight scopes.

---

## 1. Flow Selection (Static)

Analyze the consumer type to pick the right strategy:
- **Server-to-Server (Internal):** `mTLS` (Mutual TLS) or service-specific short-lived `JWT` signed by an internal KMS.
- **Server-to-Server (B2B/External):** `API Keys` with IP whitelisting, or `OAuth2 Client Credentials` flow.
- **Single Page App (SPA) / Frontend:** `HttpOnly Cookies` holding the session ID or a short-lived `JWT`. NEVER store JWTs in `localStorage`.
- **Mobile App:** `OAuth2 Authorization Code Flow with PKCE`. Use a refresh token rotation strategy.

## 2. Token Lifecycle & Strategy
Define the rules of engagement:
- **Access Token:** Very short lifespan (e.g., 5-15 minutes). Contains minimal claims (`user_id`, `role`).
- **Refresh Token:** Longer lifespan (e.g., 7-30 days). Opacity is preferred (random string in DB, not a JWT).
- **Rotation:** Every time a refresh token is used, it is invalidated and a new one is issued (Refresh Token Rotation).

## 3. Scope Design (RBAC vs ABAC)
Define how permissions are enforced:
- **RBAC (Role-Based):** Standard roles (`admin`, `user`).
- **Scopes (Capability-Based):** `read:orders`, `write:profile`. Ensure scopes are attached to the token payload so the API Gateway can reject requests before they hit the microservice.

## 4. Output Generation

**Required Outputs (Must write BOTH to `docs/api-report/`):**

1. **Human-Readable Markdown (`docs/api-report/auth-flow-report.md`)**
```markdown
### 🔐 Authentication Architecture Plan
- **Primary Consumer:** React Native Mobile App
- **Selected Flow:** OAuth2 Authorization Code Flow (PKCE)
- **Token Strategy:** JWT Access Token + Opaque Refresh Token (Rotated)

#### 🚦 Token Configurations
- **Access Token (JWT):** Lifespan: 15 minutes. Claims: `sub` (UUID), `roles` (Array).
- **Refresh Token (Opaque):** Lifespan: 30 days. Action: Rotated on every use. Stored securely on the device encrypted enclave.

#### 🛡️ API Gateway Enforcement
The API Gateway must validate the JWT Signature and ensure `Scope: read:orders` exists before forwarding to the upstream service.
```

2. **Machine-Readable JSON (`docs/api-report/auth-flow-output.json`)**
```json
{
  "skill": "auth-flow-designer",
  "flow": "oauth2_pkce",
  "client_type": "mobile",
  "access_token": {"type": "JWT", "lifespan_min": 15},
  "refresh_token": {"type": "Opaque", "lifespan_days": 30, "rotation": true},
  "required_scopes": ["read:orders", "write:profile"]
}
```

---

## Guardrails
- **JWT in LocalStorage:** Strictly forbid and flag this practice. Push towards `HttpOnly` cookies for web clients.
- **Revocation:** Point out that stateless JWTs cannot be instantly revoked without a blocklist check. If instant revocation is required, suggest opaque Session IDs or a Redis-backed blocklist.
