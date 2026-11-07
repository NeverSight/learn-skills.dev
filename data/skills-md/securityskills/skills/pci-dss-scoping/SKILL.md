---
name: pci-dss-scoping
description: Scope a PCI DSS environment correctly — cardholder data flows, segmentation validation, and requirements mapping for compliance. Use when preparing for PCI DSS v4.0 assessments.
---

# PCI DSS Scoping

Correct scoping is 80% of PCI DSS. Get the data flows right first.

## 1. Find the Cardholder Data

- Trace the full payment path: capture → transmission → processing → storage → destruction
- PAN storage locations: databases, logs (log scrubbing!), backups, email/ticket systems, dev/test environments
- Verify truncation/masking everywhere PAN appears; confirm no SAD (sensitive auth data) persistence post-authorization

## 2. Define the CDE

- Cardholder Data Environment: all systems that store/process/transmit CHD, plus connected systems
- Identify connected-to systems: security-impacting (shared services like AD, DNS, NTP, monitoring) and security-impacting-or-not based on their ability to impact CDE security
- Everything with potential CDE connectivity is in scope until segmentation is proven

## 3. Segmentation (the scope killer)

- Document segmentation controls: firewalls, network access control, separate credentials/privileged accounts for CDE
- **Segmentation penetration test is mandatory** (v4.0): verify from out-of-scope zones that CDE boundaries hold, both directions
- If no segmentation: entire network is the CDE. Usually more expensive than segmenting.

## 4. Requirements Mapping (v4.0 highlights)

- Req 1/2: network controls, secure configurations (now with defined "defined approach" targets)
- Req 3: protect stored account data; cryptography inventory and key management (3.6/3.7 expanded)
- Req 4: strong cryptography in transit — **new in v4.0: PAN over open networks needs rendering unreadable (4.2.1)**
- Req 8: MFA for all access into CDE (8.4 expanded beyond admin)
- Req 10/11: logging + testing; **targeted risk analysis** for customizing frequencies (11.3.x)
- Req 12: policy, third-party/service provider management, customizes approaches documented

## 5. Evidence Preparation

- ASV scan reports, internal/external pentest reports, segmentation pen test
- Quarterly scans, configuration standards, key management records, training logs
- compensating controls worksheet for any "not applicable" requirements

## Output

Data-flow diagrams, scope document with in/out-of-scope justification, segmentation test plan, and a requirements evidence matrix.
