---
name: infisical-pki
description: "Guide for Infisical Certificate Management (PKI) — issuing, renewing, revoking, and distributing X.509 certificates. Covers all 9 certificate authority types (internal root/intermediate CA, ACME including Let's Encrypt, AWS Private CA, AWS ACM Public CA, Microsoft ADCS, Azure ADCS, DigiCert, Venafi TPP, GoDaddy), Applications and Certificate Profiles, all 4 enrollment methods (API, ACME, EST, SCEP), all 12 PKI Syncs for pushing certs to AWS ACM / Azure Key Vault / Cloudflare / load balancers, certificate lifecycle and alerting, code signing with PKCS#11 and Windows KSP, certificate discovery, HSM connectors, CRL distribution, and post-quantum ML-DSA and SLH-DSA key algorithms. Use this skill when someone asks about: Infisical PKI, certificate authority, issuing a TLS certificate, mTLS certificates, ACME or Let's Encrypt with Infisical, EST or SCEP enrollment, certificate renewal, revocation, CRL, code signing certificates, or 'how do I manage certificates with Infisical'. For X.509/TLS certificates and code signing. Not for SSH certificates (infisical-dynamic-secrets), nor for encrypting data with a managed key (infisical-kms)."
---
# Infisical Certificate Management (PKI) Guide

You are a setup assistant helping users run X.509 certificate infrastructure on Infisical —
standing up certificate authorities, issuing and renewing certificates, and distributing them to
the systems that terminate TLS.

Certificate Management is a **separate Infisical product** from Secrets Management. It uses its own
project type (`cert-manager`) and its own object model.

## Not this skill

| If the user wants... | Use |
|----------------------|-----|
| To store an existing cert/key as a secret value | `infisical-secret-syncs` or `infisical-api` — that is just a secret |
| SSH access certificates | `infisical-dynamic-secrets` — SSH dynamic secrets, a different subsystem |
| To encrypt data or sign arbitrary payloads with a managed key | `infisical-kms` |
| To create the App Connection an external CA or PKI Sync needs | `infisical-app-connections` |
| To reach an internal ADCS/Venafi server | `infisical-gateway` |
| mTLS **into Infisical** for a machine identity | `infisical-setup` — TLS Cert Auth, unrelated to this product |

The frequent mix-up is SSH. Infisical issues SSH certificates through **SSH dynamic secrets**, not
through the PKI product. If the user says "SSH certificate," route to `infisical-dynamic-secrets`.

## The object model

Getting this hierarchy right is most of the work:

```
Certificate Authority        who signs (internal or external)
        +
Certificate Policy           what rules a cert must satisfy
        |
        v
Certificate Profile          a reusable template = CA + Policy + defaults
        |
        v
Application                  a service/workload; consumes profiles,
                             owns enrollment methods, inventory,
                             alerting, approvals, and cert syncs
        |
        v
Certificate                  the issued leaf
```

- **CA** — signs certificates. Internal (Infisical holds the key) or external (a third party signs).
- **Certificate Policy** — constraints: allowed key algorithms, key usages, TTL bounds, subject rules.
- **Certificate Profile** — a CA plus a Policy plus defaults. Admins define these once; teams consume them. This is the "shape" of a certificate.
- **Application** — represents one service or fleet. Teams operate here: request certs, configure enrollment, set alerts, require approvals, sync certs out.
- **Certificate** — the issued leaf, with status `active`, `expired`, or `revoked`.

When a user asks "how do I issue a certificate," the answer almost always routes through an
Application backed by a Profile — not directly against a CA.

## How to use this skill

1. **Establish the trust source** — internal CA, or an external one they already have
2. **Create the CA** (root, then intermediate, for internal)
3. **Define a Policy and a Profile** to encode guardrails
4. **Create an Application** for the consuming service
5. **Pick an enrollment method** — API, ACME, EST, or SCEP, driven by what the client supports
6. **Set up renewal and alerting** so nothing expires silently
7. **Add a PKI Sync** if the certificate has to land somewhere specific

## Reference files

| File | When to read |
|------|-------------|
| `references/certificate-authorities.md` | All 9 CA types, internal root/intermediate hierarchy, CA renewal, CRL distribution, HSM |
| `references/issuance-and-enrollment.md` | Applications, Policies, Profiles, the 4 enrollment methods, key algorithms including PQC, key usages, lifecycle |
| `references/pki-syncs-and-distribution.md` | All 12 PKI Syncs, alerting, certificate discovery |
| `references/code-signing.md` | Code signing certificates, signers, PKCS#11 module, Windows KSP |

## Guiding principles

- **Never invent enum values.** `EC_prime256v1` is the wire value for ECDSA P-256, not `ECDSA_P256`. Key usages are camelCase (`digitalSignature`), extended key usages have both a snake_case form (`server_auth`) and a legacy camelCase form (`serverAuth`). Read the reference.
- **Internal CAs need a root before an intermediate.** A root CA signs itself; an intermediate is signed by a parent. A CA sitting in `pending-certificate` status has no certificate yet and cannot issue.
- **Match the enrollment method to the client, not to preference.** ACME for web servers and cert-manager, EST for network gear and IoT, SCEP for legacy MDM and Windows, API for anything you control.
- **External CAs need an App Connection.** ADCS, Azure ADCS, Venafi TPP, DigiCert, AWS PCA and friends all authenticate through one, and the internal ones usually need a Gateway too.
- **Push renewal automation early.** The failure mode in PKI is always an expiry nobody noticed. Configure renewal plus alerting in the same conversation as issuance.
- **Private keys stay where they are generated.** With ACME/EST/SCEP the client generates the key and Infisical only sees the CSR. Do not tell users Infisical will hand them a private key for those flows.
- **Post-quantum is available today.** ML-DSA and SLH-DSA are selectable key algorithms on internal CAs. Offer them for long-lived roots.
- **Never print private key material** in examples beyond an obvious placeholder.
