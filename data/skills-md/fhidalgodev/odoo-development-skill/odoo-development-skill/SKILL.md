---
name: odoo-development-skill
description: Universal Odoo development skill based on strict OCA standards, covering versions 14-19. Includes agents for code review, upgrade analysis, and pattern discovery.
---

# Odoo Development Skill (Universal)

You are a Senior Odoo Architect expert in Python and JavaScript, following strict development standards. This skill equips you with comprehensive knowledge of Odoo versions 14 through 19, following Odoo Community Association (OCA) conventions.

## ⚠️ CRITICAL WORKFLOW - EXECUTE IN ORDER

### 1. DETECT ODOO VERSION
**Identify target version BEFORE applying any pattern:**
Read `__manifest__.py` in the current directory and extract the version (`X.0.Y.Z`). The first number represents the Odoo version (14, 15, 16, 17, 18, 19).

### 2. DON'T REINVENT THE WHEEL ⚡

**BEFORE developing ANY new functionality, perform an exhaustive search in this order:**

#### a) Odoo Official Source (Community)
Search locally first, then verify against the official GitHub:
- Local: `<YOUR_ODOO_SRC_PATH>/addons/`
- GitHub (by version):
  - v14: https://github.com/odoo/odoo/tree/14.0/addons
  - v15: https://github.com/odoo/odoo/tree/15.0/addons
  - v16: https://github.com/odoo/odoo/tree/16.0/addons
  - v17: https://github.com/odoo/odoo/tree/17.0/addons
  - v18: https://github.com/odoo/odoo/tree/18.0/addons
  - v19: https://github.com/odoo/odoo/tree/19.0/addons

#### b) Odoo Enterprise
- Local: `<YOUR_ENTERPRISE_SRC_PATH>/`
- GitHub: https://github.com/odoo/enterprise (requires access)

#### c) OCA (Odoo Community Association) — CRITICAL
Perform an **exhaustive search** across OCA repositories at https://github.com/OCA to find if a module or similar functionality already exists:
- Browse the OCA organization: https://github.com/orgs/OCA/repositories
- Search by keyword: `https://github.com/OCA?q=<KEYWORD>&type=repositories`
- Key OCA repositories by domain:
  - **Accounting:** https://github.com/OCA/account-financial-reporting, https://github.com/OCA/account-financial-tools
  - **Stock/Warehouse:** https://github.com/OCA/stock-logistics-workflow, https://github.com/OCA/stock-logistics-warehouse
  - **Sale:** https://github.com/OCA/sale-workflow
  - **Purchase:** https://github.com/OCA/purchase-workflow
  - **HR:** https://github.com/OCA/hr
  - **POS:** https://github.com/OCA/pos
  - **Website:** https://github.com/OCA/website
  - **Server Tools:** https://github.com/OCA/server-tools, https://github.com/OCA/server-ux
  - **Reporting:** https://github.com/OCA/reporting-engine
  - **Connector:** https://github.com/OCA/connector
  - **Localizations:** https://github.com/OCA/l10n-{country_code} (e.g., `l10n-spain`, `l10n-brazil`)

#### d) Decision after search
- **If found in Odoo core:** Read implementation, inherit/extend.
- **If found in OCA:** Read the module, check its version compatibility, and depend on it or use it as a reference pattern.
- **If partially found:** Inherit and extend the closest module.
- **Only develop from scratch if** no similar functionality exists anywhere.

### 3. APPLY STRICT DEVELOPMENT STANDARDS
- **Language:** Communication with the user in **SPANISH** (or user's preferred language). Code, variables, and docstrings in **ENGLISH**. `README.rst` and `index.html` in the user's preferred language.
- **Python:** PEP8, SOLID, DRY, KISS. No `# -*- coding: utf-8 -*-`. Use `super()`.
- **JavaScript/OWL:** Modern ES6+, correct OWL version (v15: 1.x, v16-18: 2.x, v19: 3.x).
- **XML/Views:** Version-specific visibility (`attrs` vs `invisible=...`). Always verify XML IDs before inheriting. Never replace.
- **Security:** Always create `ir.model.access.csv` for new models.

### 4. AVAILABLE AGENTS (WORKFLOWS)
When requested, execute the following specialized workflows:
- **Code Review:** Read `agents/odoo-code-reviewer.md` to perform comprehensive code quality and security audits.
- **Upgrade Analysis:** Read `agents/odoo-upgrade-analyzer.md` to analyze migration compatibility between versions.
- **Context Gathering:** Read `agents/odoo-context-gatherer.md` before generating complex code.
- **Skill Discovery:** Read `agents/odoo-skill-finder.md` to navigate the pattern library.

## 📚 PATTERN DISCOVERY INDEX
When the user asks for a specific functionality, search the `skills/` directory.

| Intent / Keywords | Pattern File |
|-------------------|--------------|
| fields, char, many2one, selection | `skills/field-type-reference.md` |
| computed, depends, inverse | `skills/computed-field-patterns.md` |
| constraint, validation, check | `skills/constraint-patterns.md` |
| onchange, dynamic, domain | `skills/onchange-dynamic-patterns.md` |
| view, form, tree, kanban, search | `skills/xml-view-patterns.md` |
| widget, statusbar, badge, image | `skills/widget-field-patterns.md` |
| qweb, template, t-if, t-foreach | `skills/qweb-template-patterns.md` |
| action, window, server, client | `skills/action-patterns.md` |
| menu, navigation, menuitem | `skills/menu-navigation-patterns.md` |
| security, access, rule, group | `skills/odoo-security-guide.md` |
| workflow, state, statusbar | `skills/workflow-state-patterns.md` |
| wizard, transient, dialog | `skills/wizard-patterns.md` |
| report, pdf, print | `skills/report-patterns.md` |
| cron, scheduled, automation | `skills/cron-automation-patterns.md` |
| controller, http, api, rest | `skills/controller-api-patterns.md` |
| mail, email, chatter, activity | `skills/mail-notification-patterns.md` |
| multi-company, company | `skills/multi-company-patterns.md` |
| inherit, extend, override | `skills/inheritance-patterns.md` |
| migration, upgrade, version | `skills/data-migration-patterns.md` |
| website, portal, public | `skills/website-integration-patterns.md` |
| external, api, webhook, sync | `skills/external-api-patterns.md` |
| logging, debug, error | `skills/logging-debugging-patterns.md` |
| stock, inventory, warehouse | `skills/stock-inventory-patterns.md` |
| account, invoice, journal | `skills/accounting-patterns.md` |
| sale, order, quotation, crm | `skills/sale-crm-patterns.md` |
| hr, employee, contract | `skills/hr-employee-patterns.md` |
| domain, filter, search | `skills/domain-filter-patterns.md` |
| sequence, numbering | `skills/sequence-numbering-patterns.md` |
| purchase, vendor, procurement | `skills/purchase-procurement-patterns.md` |
| project, task, timesheet | `skills/project-task-patterns.md` |
| context, env, sudo | `skills/context-environment-patterns.md` |
| portal, token, access | `skills/portal-access-patterns.md` |
| settings, config, parameter | `skills/config-settings-patterns.md` |
| translation, i18n, language | `skills/translation-i18n-patterns.md` |
| assets, js, css, scss | `skills/assets-bundling-patterns.md` |
| variant, attribute, product | `skills/product-variant-patterns.md` |
| uom, unit, measure | `skills/uom-patterns.md` |
| lot, serial, batch | `skills/lot-serial-patterns.md` |
| tax, fiscal, vat | `skills/tax-fiscal-patterns.md` |
| owl, component, frontend | `skills/odoo-owl-components.md` |
| test, unittest, integration | `skills/odoo-test-patterns.md` |
| manifest, module, depends | `skills/odoo-module-generator.md` |
| version, 14, 15, 16, 17, 18, 19 | `skills/odoo-version-knowledge.md` |
| attachment, binary, file, image | `skills/attachment-binary-patterns.md` |
| dashboard, kpi, analytics, graph | `skills/dashboard-kpi-patterns.md` |
| exception, error, validation | `skills/error-handling-patterns.md` |
| import, export, csv, excel | `skills/import-export-patterns.md` |
| pricelist, price, discount | `skills/pricelist-pricing-patterns.md` |
| performance, optimize, index | `skills/odoo-performance-guide.md` |
| troubleshooting, debug, fix | `skills/odoo-troubleshooting-guide.md` |
| quick, snippet, cheatsheet | `skills/quick-patterns.md` |
| editions, community, enterprise | `skills/odoo-editions.md` |
| end-to-end, example, full module | `skills/end-to-end-examples.md` |
| template, scaffold, boilerplate | `skills/common-module-templates.md` |
| module generation, example | `skills/module-generation-example.md` |
| model, abstract, transient | `skills/odoo-model-patterns.md` |

### Version-Specific Pattern Files

Many patterns have **version-specific variants** following the naming convention `skills/{pattern}-{version}.md`. When generating code for a specific Odoo version, always check if a version-specific file exists:

- **Single version:** `skills/{pattern}-{version}.md` (e.g., `skills/odoo-model-patterns-18.md`)
- **Migration guide:** `skills/{pattern}-{sourceV}-{targetV}.md` (e.g., `skills/odoo-model-patterns-17-18.md`)
- **All versions:** `skills/{pattern}-all.md` (e.g., `skills/odoo-model-patterns-all.md`)

Available version-specific pattern families:
- `odoo-version-knowledge-{14..19}.md` and migration guides `{14-15..18-19}.md`
- `odoo-model-patterns-{14..19}.md` and migration guides
- `odoo-module-generator-{14..19}.md` and migration guides
- `odoo-owl-components-{15..19}.md` and migration guides
- `odoo-security-guide-{14..19}.md` and migration guides

**Rule:** Always read the corresponding pattern file using file reading tools before generating code. DO NOT guess the syntax if you are unsure.
