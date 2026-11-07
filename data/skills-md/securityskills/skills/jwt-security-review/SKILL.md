---
name: jwt-security-review
description: Audit JSON Web Token implementations for algorithm confusion, weak secrets, missing validation, and token lifecycle flaws. Use when a codebase or API uses JWTs for auth.
---

# JWT Security Review

Review JWT-based authentication end to end.

## Review Areas

### Algorithm Handling
- Pin the expected algorithm server-side; reject `alg: none` outright
- **RS256→HS256 confusion**: if the server verifies HMAC using the public key as the secret, an attacker can forge tokens. Confirm verification uses the correct key type per algorithm
- Watch for `jku`/`x5u` header injection where the server fetches keys from an attacker-controllable URL
- `kid` injection: path traversal or SQL/Command injection in key lookup

### Key and Secret Strength
- HS256 secrets: ≥32 bytes of entropy, not from wordlists (`jwt-tools` crack mode)
- Keys rotated; old keys revoked rather than just unused

### Claims Validation
- `exp` and `nbf` enforced, clock skew bounded
- `iss` and `aud` validated against expected values
- Reject tokens with unexpected/extra privileged claims (e.g., `admin: true`) — parse then validate allowlist
- Don't trust client-controlled `role`/`uid` claims if a server-side lookup exists

### Token Lifecycle
- Refresh tokens: rotation with reuse detection; stored hashed server-side
- Revocation path exists for logout/password change/admin force-logout
- Access tokens short-lived (≤15 min); no long-lived bearer tokens
- Tokens not persisted in localStorage if XSS surface exists; prefer httpOnly cookies with CSRF protection
- `sub` is stable and unambiguous (user ID, not email that can change)

### Common Code Smells

```
jwt.decode(token)            // decode ≠ verify: signature never checked
jwt.verify(token, key)       // no algorithms option pinned
jwt.verify(token, key, { algorithms: ['*'] })
```

## Test Cases

1. Remove the signature; send `alg: none` token
2. Flip `alg` to HS256 signed with the public key
3. Expired/missing `exp`, wrong `iss`/`aud`
4. Tampered claims with valid signature (e.g., escalate role)
5. Replay a rotated refresh token — should invalidate the family

## Output

Findings with token samples (redacted), affected code paths, and remediation per issue.
