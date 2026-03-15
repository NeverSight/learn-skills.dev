---
name: 04-audit-and-release
description: Audit, harden, and package Antonella plugins for production release. Use as the final QA and deployment gate before generating the distributable ZIP.
---

# Skill: 04-audit-and-release (Sentinel & Packaging)

## 📜 Source of Truth
> **All Standards**: `../../normative/` (Security, Architecture, Database, Deployment, OOP)

## 🎯 Purpose
Act as the ultimate gatekeeper of quality and prepare the plugin for the real world. This skill performs a rigorous audit of the codebase to identify security vulnerabilities, then optimizes and packages the final ZIP for distribution. **You act as a QA auditor and DevOps engineer.**

---

## 🗣️ Agent Interaction Protocol — The QA Phase

> [!CAUTION]
> **DO NOT build the final ZIP until you have performed the audit and received user confirmation to proceed.**

**First Action:** Run a comprehensive code review against the normative standards. Present the findings to the user:

"I have completed the security and architecture audit of the plugin. Here are my findings:"

*(Present a brief Markdown summary of identified issues: High/Medium/Low risk. Example check items: missing Nonces, raw SQL in controllers, `ABSPATH` checks).*

Then, present options:

**Option A: Auto-Fix and Release**
I will attempt to fix all identified issues automatically, clean the dev files, and build the final ZIP.

**Option B: Review Fixes Step-by-Step**
I will propose fixes for the issues one by one for your approval before building.

**Option C: Ignore warnings and Build NOW**
Skip the fixes, clean development files, and immediately package the plugin as-is.

*Wait for the user's response to proceed.*

---

## 🔄 Execution Protocol

### 🧭 Phase 1: Guided Remediation (If Option A or B)
Apply fixes to the codebase to achieve 100% compliance with `architecture_standards.md` and `security_standards.md`.

### 🧭 Phase 2: Environment Sanitization
Remove dev-only files before packaging. Ensure `.git`, `tests/`, `docker/`, `.env`, local logs, and development configuration files are fully removed or excluded.

### 🧭 Phase 3: Build Optimization
Run the production engine to optimize the Autoloader and build the app:
```bash
php antonella makeup
```
*(This internal command handles `composer install --no-dev -o` and packages the plugin automatically into a `.zip` file).*

### 🧭 Phase 4: Delivery
Verify the generated `.zip` file exists. Confirm to the user that the plugin is packaged and ready for deployment.

---

## 🏁 Quality Gates
- ✅ Agent presented the audit report and asked for confirmation before packaging.
- ✅ Identified "High" risk security vulnerabilities were addressed (unless Option C was chosen).
- ✅ Final ZIP contains 0 development dependencies.
- ✅ Autoloader is optimized for production.
