---
name: open-source-governance
description: Open source policy, license compliance, contribution guidelines, dependency management, and supply chain security
license: Apache-2.0
---

# Open Source Governance Skill

## Purpose
Defines governance for open source software use, contribution, and publication ensuring license compliance and supply chain security.

## License Compliance
### Approved Licenses
- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause
- ISC, CC-BY-4.0, Unlicense, 0BSD

### Restricted Licenses (Require Review)
- GPL-2.0, GPL-3.0, LGPL, AGPL
- SSPL, BSL, Commons Clause

### Prohibited
- No license specified (proprietary by default)
- Licenses incompatible with project license

## Dependency Management
- Pin dependencies to specific versions
- Use lock files (package-lock.json)
- Regular dependency updates via Dependabot
- Security scanning for known vulnerabilities
- SBOM generation for supply chain transparency

## Contribution Guidelines
- CONTRIBUTING.md required in all repos
- Code of Conduct (Contributor Covenant)
- Developer Certificate of Origin (DCO)
- PR review requirements
- CLA not required for Hack23 projects

## Supply Chain Security
- Pin GitHub Actions to SHA (not tags)
- Use step-security/harden-runner
- Enable Dependabot security updates
- Secret scanning with push protection
- SLSA provenance for releases

## ISO 27001 Mapping
- A.5.23 — Information security for use of cloud services
- A.8.28 — Secure coding

## Related Policies
- [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)
