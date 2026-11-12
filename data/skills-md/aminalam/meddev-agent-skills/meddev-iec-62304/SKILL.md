---
name: meddev-iec-62304
description: Provide actionable guidance to implement IEC 62304:2006+A1:2015 lifecycle processes—development, maintenance, software risk management, configuration management, and problem resolution—with rigor scaled by safety class (A/B/C). This hub skill indexes clause obligations; load child skills for depth. Use when working on iec 62304 in medical device software.
license: MIT
metadata:
  skill_id: REG-IEC62304
  version: 1.1.0
  last_updated: '2026-05-21'
  applies_to: Class A, Class B, Class C
  jurisdiction: FDA, EU MDR, Canada, UK
  prerequisites: REG-ISO14971
  category: regulatory
---

# IEC 62304 Medical Device Software Lifecycle

## Purpose
Provide actionable guidance to implement IEC 62304:2006+A1:2015 lifecycle processes—development, maintenance, software risk management, configuration management, and problem resolution—with rigor scaled by safety class (A/B/C). This hub skill indexes clause obligations; load child skills for depth.

## When to Apply
- Code or design changes in regulated medical device software.
- Creating or updating lifecycle deliverables (plans, requirements, architecture, tests, release records).
- Introducing SOUP or third-party libraries; changing build tools or CI.
- Release preparation, field corrections, or legacy software assessments.
- Any change affecting traceability across requirements, design, code, and tests.

## Requirements (testable)

### Clause 4 — General
1. QMS [Class A, B, C]: Operate under a quality management system appropriate to medical device software (e.g. ISO 13485); software activities align with QMS procedures. Rationale: 4.1. See manufacturer QMS—not duplicated here.
2. Device Risk Management [Class A, B, C]: Apply ISO 14971 risk management; link outputs to software processes. Rationale: 4.2. Skill: `REG-ISO14971`.
3. Safety Classification [Class A, B, C]: Assign class A/B/C per system hazard analysis; document in risk file; decompose items with segregation rationale when classes differ; until classified, apply Class C controls. Rationale: 4.3. Skills: `ARCH-SAFETY-CLASS`, `REG-IEC62304-SWRM` (controls in software).
4. Legacy Software [Class A, B, C]: When 4.4 applies, use legacy pathway (gap analysis, continued-use rationale) instead of assuming full Clause 5–9 history exists. Rationale: 4.4. Skill: `REG-IEC62304-LEGACY`.

### Clause 5 — Software development
5. Development Planning [Class A, B, C]: Maintain a software development plan (SDP) with life-cycle model, deliverables, traceability to system needs and risk controls, CM and problem-resolution hooks, and coordination with system development. Rationale: 5.1.1–5.1.3, 5.1.6–5.1.9.
6. Integration Planning [Class B, C]: Plan integration of software items including SOUP and integration testing. Rationale: 5.1.5.
7. Class C Planning [Class C]: Plan standards, methods, and tools for Class C items. Rationale: 5.1.4.
8. Development Tools [Class B, C]: Control compilers, build tools, and environment settings that could affect the software; place items under CM before verification. Rationale: 5.1.10–5.1.11. Skill: `CICD-PIPELINE`, `DOC-SCM`.
9. Technology Defect Review [Class B, C]: Identify defect categories relevant to chosen programming technology and document evidence they do not create unacceptable risk. Rationale: 5.1.12.
10. Software Requirements [Class A, B, C]: Define, verify, and maintain software requirements per 5.2. Skill: `DOC-SW-REQ`.
11. Architecture [Class B, C]: Document architecture, interfaces, SOUP needs, segregation for risk control (Class C), and verify against requirements. Rationale: 5.3. Skill: `DOC-DESIGN-DOCS`.
12. Detailed Design [Class C]: Subdivide to units; document unit and interface design sufficient for correct implementation; verify against architecture. Rationale: 5.4. Skill: `DOC-DESIGN-DOCS`.
13. Unit Implementation and Verification [Class A, B, C]: Implement units; Class B/C verify with procedures, acceptance criteria, and records; Class C add enhanced acceptance topics (timing, resources, faults, memory). Rationale: 5.5. Skills: `TEST-UNIT`, `TEST-COVERAGE`.
14. Integration [Class B, C]: Integrate per plan; verify integration; test behaviour including risk controls and interfaces; regression test; record results; feed anomalies to problem process. Rationale: 5.6. Skill: `TEST-INTEGRATION`, `DOC-PROBLEM-RES`.
15. System Testing [Class A, B, C]: Test all software requirements with defined procedures; evaluate strategies; record repeatable test evidence; retest after changes with risk analysis. Rationale: 5.7. Skills: `DOC-TEST-DOCS`, `REG-IEC62304-SWRM` (7.4 on retest).
16. Release [Class A, B, C]: Complete verification before release; document residual anomalies and evaluate risk (B/C); document version and build procedure; complete plan activities; archive software and docs; ensure reliable delivery. Rationale: 5.8. Skill: `CICD-RELEASE`.

### Clause 6 — Maintenance
17. Maintenance Process [Class A, B, C]: After release, follow maintenance plan—feedback, problems, changes, SOUP updates, re-apply Clause 5 as needed, re-release per 5.8. Rationale: Clause 6. Skills: `DOC-SW-MAINT`, `REG-POSTMKT-LABEL`.

### Clause 7 — Software risk management
18. Software Risk Process [Class B, C]: Perform Clause 7 activities (causes, controls, verification, change impact); Class A still performs 7.4.1 on changes. Rationale: Clause 7. Skill: `REG-IEC62304-SWRM`.

### Clause 8 — Configuration management
19. Configuration Management [Class A, B, C]: Identify items and SOUP; control changes; status accounting. Rationale: Clause 8. Skills: `DOC-SCM`, `DOC-CHANGE-CONTROL`.

### Clause 9 — Problem resolution
20. Problem Resolution [Class A, B, C]: Report, investigate, trend, verify fixes, and link to change control and test records. Rationale: Clause 9. Skill: `DOC-PROBLEM-RES`.

### Cross-cutting
21. Traceability [Class A, B, C]: Maintain bidirectional links across system/software requirements, architecture, risk controls, code, and tests. Rationale: 5.1.1 c, 7.3.3. Skill: `DOC-TRACEABILITY`.
22. Class Re-assessment [Class A, B, C]: Re-evaluate safety class when problems or changes indicate misclassification or new hazards. Rationale: 4.3, 6.2.2 (interpretation).

## Recommended Practices
- Keep a class-specific activity checklist; gate merges on checklist completion for the affected class.
- Use requirement IDs (`REQ-62304-###`) and hazard IDs (`HZ-###`) in code comments and tests.
- Maintain SBOM entries for SOUP with CVE monitoring.
- Automate traceability matrix generation from annotations and test metadata.
- Load child skills by process: planning/requirements (`DOC-SW-REQ`), design (`DOC-DESIGN-DOCS`), test (`DOC-TEST-DOCS`, `TEST-*`), release (`CICD-RELEASE`), post-release (`DOC-SW-MAINT`, `DOC-PROBLEM-RES`).
- Pin skill versions in change records when using AI-assisted development (`DOC-AI-GOV`).

## Patterns
Requirement/code/test traceability:
```c
// REQ-62304-102: Pump shall stop within 50 ms on door open (Class C)
// HZ-12, RISK-CTRL-33
bool pump_stop_on_door_open(void) {
    if (is_door_open()) {
        stop_motor(); // TEST-201 covers timing @ 50 ms
        return true;
    }
    return false;
}
```

SOUP documentation snippet (YAML):
```yaml
soup:
  - name: tiny-rtos
    version: 1.4.2
    function: scheduler, mutex, queues
    known_anomalies:
      - id: TR-77
        desc: priority inheritance bug on nested mutex
        mitigation: disabled nesting; wrapper enforces single-level
        verification: test/rtos_mutex_single_level.c
    provenance: https://example.com/releases/tiny-rtos-1.4.2.tar.gz
    classification_impact: Class C items use it for comms tasks
```

## Anti-Patterns (risks)
- Missing class rationale -> risk: incorrect activity tailoring; audit finding.
- Untracked SOUP versions -> risk: unmitigated vulnerabilities/bugs.
- Requirements only in code comments -> risk: loss of traceability.
- Untested interface changes (Class B/C) -> risk: integration defects.
- No linkage between defects and requirements/tests -> risk: weak CAPA and verification.
- Ignoring legacy 4.4 when evidence is incomplete -> risk: false claim of full lifecycle compliance.

## Verification Checklist

### All classes (A, B, C)
- [ ] SDP current; coordinates with system development and risk management.
- [ ] Safety class documented and linked to hazard analysis (`ARCH-SAFETY-CLASS`).
- [ ] Software requirements defined and verified (`DOC-SW-REQ`).
- [ ] System tests cover software requirements with recorded evidence (`DOC-TEST-DOCS`).
- [ ] Configuration items identified; changes approved (`DOC-SCM`, `DOC-CHANGE-CONTROL`).
- [ ] Problems tracked through resolution process (`DOC-PROBLEM-RES`).
- [ ] Maintenance plan exists for released software (`DOC-SW-MAINT`).
- [ ] Release criteria met; version documented; archive and delivery controls (`CICD-RELEASE`).
- [ ] Traceability matrix available for the release baseline.

### Class B and C additionally
- [ ] Architecture and SOUP specifications current (`DOC-DESIGN-DOCS`).
- [ ] Integration planned, executed, regression tested; anomalies in problem process.
- [ ] Unit verification with procedures and results (`TEST-UNIT`).
- [ ] Software risk process records for hazardous situations (`REG-IEC62304-SWRM`).
- [ ] Residual release anomalies evaluated for risk (5.8.3).
- [ ] Build procedure and development tools controlled (`CICD-PIPELINE`, `DOC-SCM`).

### Class C additionally
- [ ] Standards/methods/tools planned for Class C items (5.1.4).
- [ ] Detailed design documented and verified against architecture (5.4).
- [ ] Enhanced unit acceptance criteria addressed (5.5.4).
- [ ] Architecture segregation for risk control documented (5.3.5).
- [ ] Programming-technology defect review documented (5.1.12).

### Legacy (when 4.4 applies)
- [ ] Gap analysis and continued-use rationale per `REG-IEC62304-LEGACY`.

## Traceability
- Use stable IDs: requirements (`REQ-62304-###`), hazards (`HZ-###`), risks (`RISK-###`), controls (`RISK-CTRL-###`), tests (`TEST-###`), design elements (`DES-###`), problems (`PR-###`), changes (`CR-###`).
- Embed IDs in code comments and test names; source-of-truth in managed requirements tool or `requirements.yaml`.
- Generate matrices (REQ↔DES↔CODE↔TEST) per release; include software hazard chain per `DOC-TRACEABILITY` and `REG-IEC62304-SWRM`.

## References
- IEC 62304:2006+A1:2015, Clauses 4–9 (informative class summary: Annex A Table A.1 — cite clause IDs only).
- Child skills: `REG-IEC62304-SWRM` (7), `REG-IEC62304-LEGACY` (4.4), `DOC-SW-REQ` (5.2), `DOC-DESIGN-DOCS` (5.3–5.4), `DOC-SCM` (8), `DOC-CHANGE-CONTROL`, `DOC-PROBLEM-RES` (9), `DOC-SW-MAINT` (6), `DOC-TEST-DOCS`, `ARCH-SAFETY-CLASS` (4.3).
- IEC TR 80002-1:2019 (informative).
- FDA Guidance (2023): device software functions; cybersecurity (documentation expectations).
- ISO 14971:2019 (`REG-ISO14971`).

**Note**: IEC 62304:2024 (Edition 2) may supersede IEC 62304:2006+A1:2015 when adopted; verify applicable edition with QA/RA.

## Changelog
- 1.1.0 (2026-05-21): Process-indexed requirements (Clauses 4–9); class-tagged checklist; child skill pointers; legacy 4.4; Table A.1-aligned class labels (interpretation).
- 1.0.2 (2026-03-20): Corrected Clause 8 vs 5.8 mapping; SOUP under 5.3+.
- 1.0.1 (2026-01-04): Audit corrections (Section 9, 5.7, Section 6, TR 80002-1, FDA 2023).
- 1.0.0 (2026-01-04): Initial comprehensive lifecycle skill.

## Audit History
- **2026-05-21**: IEC 62304 alignment pass—modular child skills, class-aware checklist, 4.4 legacy pointer.
- **2026-03-20**: Clause mapping audit (5.8 release vs Clause 8 CM).
- **2026-01-04**: Regulatory audit—Section 9, 5.7, maintenance, references corrected.
