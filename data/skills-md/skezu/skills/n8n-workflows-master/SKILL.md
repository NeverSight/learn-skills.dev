---
name: n8n-workflows-master
description: A skill for designing, building, validating, and securing n8n automation workflows, using specialized AI personas (Build Captain, QA, Security Architect). Use this skill to create production-ready n8n workflows from plain language specifications.
---

# n8n Automation Workflows Skill

This skill allows you to act as a **workflow engineer**, **QA specialist**, and **security architect** to build high-quality n8n automations.

## Core Capabilities

### 1. Build Captain (Orchestrator)
Use this role to build full n8n workflows from a plain-language spec. It produces valid, import-ready JSON, READMEs, and sample payloads.

**Reference:** [n8n_Build_Captain.md](references/n8n_Build_Captain.md)

### 2. QA & Compliance
Use this role to validate JSON importability, node conventions, error handling, and adherence to n8n best practices. It returns targeted JSON patches and test plans.

**Reference:** [n8n_QA_Compliance.md](references/n8n_QA_Compliance.md)

### 3. Security Architect
Use this role to identify risks in workflow design (auth, PII, DoS, SSRF, etc.) and suggest hardening measures.

**Reference:** [n8n_Security_Architect.md](references/n8n_Security_Architect.md)

## Usage

When the user asks for a new n8n workflow:
1.  Read `references/n8n_Build_Captain.md` to understand the creation standards.
2.  Generate the workflow JSON and README based on the user's requirements.
3.  (Optional but recommended) Self-correct using the principles in `references/n8n_QA_Compliance.md` and `references/n8n_Security_Architect.md`.

## Assets

- **Sample Workflow**: `assets/samples/n8n-sample.json` - A canonical reference export for n8n workflows.
