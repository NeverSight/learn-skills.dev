---
name: social-engineering-audit
description: Assess social engineering attack surface in applications and organizations. Identifies pretexting vectors, OSINT exposure, phishing susceptibility in authentication flows, and human-factor vulnerabilities in security architecture. Use when auditing auth flows, help desk procedures, password reset mechanisms, or organizational security posture.
---

# Social Engineering Audit

## When to Use

Invoke this skill when assessing:

- Authentication and authorization flows (login, MFA, password reset, account recovery)
- Help desk and customer support procedures
- Identity verification and onboarding processes
- Organizational security posture against targeted attacks
- Account takeover risk via non-technical channels
- Physical access control and personnel security

This is not a penetration test. This is a structured assessment of the human-factor
attack surface -- the seams where process, trust, and technology meet.

## Attack Surface Taxonomy

### 1. Pretexting Vectors

- **Support channels**: phone, email, chat, social media DMs. Each is an identity
  verification boundary. Map them all. Determine what each channel can do
  (password reset, account unlock, PII disclosure, plan changes).
- **Internal help desk**: IT support desks are high-value targets. Assess what
  credentials or verification they require before acting on requests.
- **Vendor/contractor impersonation**: third-party relationships create implicit
  trust. Identify which vendors have elevated access or bypass normal auth.
- **Authority exploitation**: executive impersonation, "urgent" escalation paths,
  out-of-band requests that skip normal verification.

### 2. Authentication Bypass via Social Channels

- **Password reset**: Does the reset flow rely on email alone? Is there a
  fallback path through support? Can support override MFA?
- **Account recovery**: What happens when a user "loses everything"? The recovery
  path is the weakest authentication path.
- **SIM swap / number porting**: If SMS is used for 2FA or recovery, the phone
  carrier is part of your authentication chain.
- **Session hijacking via support**: Can support generate magic links, session
  tokens, or bypass codes? Under what verification?

### 3. OSINT Exposure

- **Breached credentials**: Check paste sites, breach databases. Credential
  reuse is the simplest attack.
- **Social media**: Employee roles, org charts, technology stack, office photos
  (badges, screens, whiteboards).
- **Public records**: Domain registrations, DNS records, job postings (reveal
  internal tooling), SEC filings, patent applications.
- **Code repositories**: Leaked secrets, internal URLs, employee emails in
  commit history, CI/CD configurations.
- **Metadata**: Document metadata (author names, software versions, internal
  paths) in public PDFs, images, office documents.

### 4. Phishing Surface

- **Email authentication**: Check SPF, DKIM, DMARC records. A missing or
  permissive DMARC policy (p=none) means anyone can spoof the domain.
- **Lookalike domains**: Check for registered typosquats and homoglyph domains.
  Use dnstwist or similar.
- **Link handling**: How does the application handle links in emails, chat,
  notifications? Are URLs previewed, sandboxed, or blindly followed?
- **OAuth consent phishing**: Can an attacker register an OAuth app with a
  deceptive name and request broad scopes?

### 5. Physical Social Engineering

- **Tailgating**: Badge-controlled entrances without mantraps or visual
  verification.
- **Badge cloning**: Proximity card technology (125kHz HID is trivially cloned).
- **Impersonation**: Delivery, maintenance, IT support pretexts for physical
  access.
- **Dumpster diving**: Document disposal procedures, shredding policy.

## Audit Methodology

Execute in order. Each step informs the next.

**Step 1: Map human-mediated authentication paths.**
Enumerate every path where a human (support agent, IT admin, manager) can
override, bypass, or supplement automated authentication. Document what each
path can do and what verification it requires.

**Step 2: Identify identity verification procedures.**
For each human-mediated path: what questions are asked? What constitutes
"sufficient" proof of identity? Is it documented or ad hoc? Can the answers
be obtained via OSINT?

**Step 3: Assess OSINT exposure.**
Gather publicly available information that could be used to answer verification
questions or craft targeted pretexts. Focus on: employee names and roles,
email formats, technology stack, org structure, breached credentials.

**Step 4: Evaluate phishing controls.**
Check email authentication records (SPF/DKIM/DMARC). Enumerate registered
lookalike domains. Review whether the organization has phishing-resistant
MFA (WebAuthn/FIDO2) or phishable MFA (TOTP/SMS).

**Step 5: Review account recovery flows.**
Walk through every account recovery path as an attacker who controls only
public information. Identify which paths leak user existence, accept
guessable answers, or defer to a human who can be pretexted.

**Step 6: Test help desk resistance.**
Design pretext scenarios based on Steps 2-3. Assess (or recommend testing)
whether support staff follow verification procedures under pressure,
urgency, or authority cues.

## Code Review Patterns

When reviewing application source, flag these patterns:

### User Enumeration

```
# BAD: Different responses for valid vs invalid users
if not user_exists(email):
    return "No account found"     # Leaks existence
return "Reset link sent"
```

Fix: Return the same response regardless. Send email only if account exists.

### Security Questions for Recovery

Any use of security questions (mother's maiden name, first pet, etc.) is a
finding. These are OSINT-retrievable and not secrets.

### Support Tooling Without Verification Audit Trail

```
# BAD: Support action with no identity verification logged
@admin_required
def reset_user_password(user_id):
    user.set_random_password()    # No record of what verification was performed
```

Fix: Require and log the verification method used before any support action.

### OAuth/SSO Misconfigurations

- Open redirect in OAuth callback URLs (enables token theft)
- Wildcard or overly broad redirect URI matching
- Missing `state` parameter validation (CSRF in OAuth flow)
- Auto-approval of OAuth consent for internal apps (can be abused if app
  registration is open)

### Rate Limiting Gaps

```
# BAD: No rate limit on verification code endpoint
@app.route("/verify-code", methods=["POST"])
def verify_code():
    if request.form["code"] == stored_code:
        grant_access()
```

Fix: Rate limit by IP and account. Lock after N failures. Use longer codes.

### MFA Bypass in Recovery

Look for code paths where MFA is enforced at login but skipped during
account recovery, password reset, or support-initiated access.

## Output Format

Structure findings as:

```
### [SE-001] Finding Title

Severity: Critical / High / Medium / Low / Informational
Category: Pretexting | Auth Bypass | OSINT Exposure | Phishing | Physical
Attack Scenario: Concrete, step-by-step description of how an attacker
  exploits this. Name the pretext. Name the channel. Name what they obtain.
Evidence: What was observed (code path, policy gap, DNS record, etc.)
Remediation: Specific, actionable fix. Not "improve training."
References: Relevant standards (NIST 800-63B, OWASP, etc.)
```

Severity calibration:
- **Critical**: Direct account takeover via social channel, no technical skill required.
- **High**: Account takeover possible with moderate OSINT gathering.
- **Medium**: Information disclosure that enables targeted attacks.
- **Low**: Weak controls that increase attack surface but require chaining.
- **Informational**: Observations that inform security posture but lack direct exploit path.

## Related Skills

- `entry-point-analyzer` -- map technical entry points before assessing human ones
- `webapp-testing` -- complement social engineering audit with technical testing
- `audit-context-building` -- establish organizational context and threat model
