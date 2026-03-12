---
name: healthcare-ui-design
description: Design clinical and patient-facing healthcare web UIs that prioritize safety, clarity, and regulatory compliance while integrating all backend actions strictly through APIs.
---

# Healthcare UI Design Skill

## Overview

Design healthcare user interfaces for clinical workflows, patient portals, and medical record systems. Prioritize patient safety, regulatory compliance (HIPAA, FDA 21 CFR Part 11), and clarity under high-stress conditions. Ensure all backend activity is API-driven.

## When to Use

- Designing clinical dashboards, patient intake forms, or electronic health record (EHR) screens.
- Creating patient-facing portals for appointment scheduling, lab results, or medication management.
- Reviewing existing healthcare UIs for compliance, accessibility, and usability.
- Defining API-first UI workflows for clinical data entry and retrieval.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Domain**  | Healthcare, clinical, patient-facing |
| **Standards** | HIPAA, FDA 21 CFR Part 11, WCAG 2.1 AA, ISO 62366-1 (Usability Engineering) |
| **Tone**    | Safety-critical, precise, compliant |

## Core Instructions

### 1) Patient Safety First

- Display critical information (allergies, drug interactions, alerts) prominently and persistently.
- Use color coding with redundant text/icon indicators (never color alone per WCAG 2.1).
- Require explicit confirmation for high-risk actions (medication orders, dosage changes).

### 2) Regulatory Compliance

- Implement audit trails for all data modifications (who, what, when).
- Support electronic signatures per FDA 21 CFR Part 11 where applicable.
- Enforce session timeouts and re-authentication for sensitive operations (HIPAA).
- Display patient identifiers consistently (minimum two identifiers per ISO 62366-1).

### 3) Clinical Workflow Efficiency

- Minimize clicks for high-frequency tasks (vitals entry, medication administration).
- Support barcode scanning for patient wristbands and medication verification.
- Provide keyboard shortcuts for power users in clinical settings.
- Design for interruption recovery (clinicians are frequently interrupted mid-task).

### 4) API-First Rule

All backend activity must go through APIs. Never assume direct database access. Keep UI optimistic where safe and reconcile with API responses. Apply strict error handling for clinical data integrity.

## Cognitive UX Evaluation

For cognitive science-based evaluation of clinical UI designs -- particularly the Attention Mind (reducing cognitive load in high-stress clinical environments), Language Mind (clear medical terminology and error messages), and Emotion Mind (trust signals for patient-facing interfaces) -- reference `skills/cognitive-ux-framework/`.

## Accessibility

- WCAG 2.1 AA minimum; AAA for patient-facing interfaces.
- Large touch targets (minimum 48x48px) for tablet-based clinical entry.
- High contrast mode for bright clinical environments.
- Screen reader compatibility for visually impaired patients.

## Common Pitfalls

- Displaying too much information simultaneously (cognitive overload in clinical settings).
- Relying on color alone to indicate alert severity.
- Missing confirmation dialogs on irreversible clinical actions.
- Inadequate session timeout policies for shared clinical workstations.
- Not designing for interruption recovery in clinical workflows.

## Cognitive UX Evaluation

For cognitive science-based evaluation of clinical UI designs — particularly the Attention Mind (reducing cognitive load in high-stress clinical environments), Language Mind (clear medical terminology and error messages), and Emotion Mind (trust signals for patient-facing interfaces) — reference `skills/cognitive-ux-framework/`.
