---
name: test-viewpoint-analyst
description: Generates and reviews test scenarios based on IPA non-functional grade standards. Analyzes system requirements to identify critical test viewpoints for performance, security, and availability.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
  - qa
  - security
---

# Test Viewpoint Analyst (IPA-Standard)

This skill specializes in deriving and auditing test cases based on the IPA Non-Functional Requirements Grade 2018. It ensures that system verification covers all critical non-functional aspects.

## Capabilities

### 1. Test Scenario Generation

Translate system requirements into specific test viewpoints and scenarios.

- **Functional**: Validation (TIS-standard), DB access patterns, Web/Mobile/Batch specific behaviors.
- **Availability**: Disaster recovery drills, failover tests, backup verification (IPA-standard).
- **Performance**: Load testing, stress testing, endurance testing.
- **Security**: Penetration testing (scoping), log analysis verification, compliance checks.

### 2. Test Plan Review

Audit existing test plans against the standards to identify missing viewpoints.

- Check for "Overcommitment" impacts in virtualized environments.
- Verify "Global Compliance" requirements (e.g., GDPR).
- Ensure "Incident Response" drills are included.

## Knowledge Base

- **Standard Viewpoints (Non-Functional)**: `knowledge/nonfunctional/test-viewpoints/ipa_grade_2018.md`
- **Standard Viewpoints (Functional/General)**: `knowledge/testing/viewpoint-catalogs/tis_catalog_v1_6.md`
- Always refer to these documents for the latest aligned test criteria.

## Usage Examples

- "Generate a performance test plan for a system with the response time requirements in `work/rd.md`."
- "Review my security test viewpoints in `tests/security.md` against the IPA 2018 standards."
- "What are the essential test points for a virtualized DB server according to the IPA guide?"

## Workflow Focus

1.  **Extract**: Identify non-functional requirements from input documents.
2.  **Map**: Align requirements with the IPA Test Viewpoint Catalog.
3.  **Synthesize**: Produce actionable test scenarios or improvement recommendations.

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
