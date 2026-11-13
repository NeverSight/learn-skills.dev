---
name: devsecops-free-discovery
description: "Orchestrates discovery of free DevSecOps infrastructure from ripienaar/free-for-dev and other sources"
---

# Skill: DevSecOps Free Discovery

## Goal
Orchestrate systematic discovery of free DevSecOps infrastructure by walking agents through the free-for-dev catalog and related resources.

## Use This Skill When
- Starting a DevSecOps infrastructure discovery workflow
- Building a free tier infrastructure plan
- Identifying cost-effective alternatives for paid services

## Do Not Use This Skill When
- Looking for paid enterprise solutions
- Needing SLA-backed production services

## Inputs
- Project requirements (compute, storage, CI/CD, monitoring needs)
- Budget constraints (zero-cost preferred)
- Infrastructure category focus (optional)

## Steps

1. **Identify Infrastructure Categories**
   - Major Cloud Providers (GCP, AWS, Azure, Oracle, IBM)
   - CI/CD and Build Systems
   - Security and PKI
   - Monitoring and Logging
   - DNS and CDN
   - Source Code Repos
   - Authentication and Authorization
   - Storage and Media Processing
   - Container/Container Registry

2. **Fetch the Catalog**
   - Primary: https://github.com/ripienaar/free-for-dev
   - Use `webfetch` tool on https://raw.githubusercontent.com/ripienaar/free-for-dev/master/README.md
   - Parse the table of contents for relevant sections

3. **Categorize by DevSecOps Domain**
   - Use sub-skills for domain-specific discovery:
     - `devsecops-free-cloud` - IaaS/PaaS compute resources
     - `devsecops-free-cicd` - CI/CD pipelines, build systems
     - `devsecops-free-security` - Security, PKI, scanning
     - `devsecops-free-monitoring` - Monitoring, logging, APM
     - `devsecops-free-dns` - DNS, CDN, SSL/TLS
     - `devsecops-free-auth` - Authentication, authorization
     - `devsecops-free-storage` - Object storage, databases

4. **Match Requirements to Offerings**
   - Compare project needs against free tier limits
   - Document limitations (bandwidth, storage, compute hours)
   - Flag services requiring credit card for signup

5. **Create Comparison Matrix**
   - Service name, provider, free tier limits
   - Region availability
   - Credit card requirement
   - SSL/TLS availability
   - SSO restrictions

## Output
- Structured inventory of free DevSecOps infrastructure
- Recommendations matched to project requirements
- Limitations and gotchas document

## Reference
Primary catalog: https://github.com/ripienaar/free-for-dev