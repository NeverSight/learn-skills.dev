---
name: salesforce-developer
description: >
  Generates, reviews, and debugs Salesforce platform code including Apex classes,
  triggers, SOQL/SOSL queries, LWC/Aura components, Flows, validation rules, formulas,
  REST/Bulk/SOAP API integrations, and Agentforce agent actions. Use when the user asks
  about Salesforce development, Lightning Platform, Apex, LWC, SOQL, Flows, deployment,
  scratch orgs, Agentforce, platform events, or any .cls, .trigger, .js-meta.xml files.
license: MIT
metadata:
  author: salesforce-dev-team
  version: "2.0"
compatibility: Designed for VS Code, Claude Code, Cursor, and GitHub Copilot coding agent
---

# Salesforce Developer Skill

## How to Use This Skill

Read the appropriate reference file(s) **AND** the corresponding coding ruleset before generating code:

### Step 1: Read the Coding Rulesets (MANDATORY for all code generation)

| Code Type | Ruleset File |
|---|---|
| Apex (classes, triggers, tests, async, integrations) | [../../Blogs/salesforce-apex-coding-rules.md](../../Blogs/salesforce-apex-coding-rules.md) |
| LWC (components, templates, JS, events, Jest tests) | [../../Blogs/salesforce-lwc-coding-rules.md](../../Blogs/salesforce-lwc-coding-rules.md) |

These rulesets contain comprehensive coding standards, anti-patterns, PMD/ESLint rules, and code examples. **Always** apply these rules to all generated code.

### Step 2: Read the Appropriate Reference File(s)

| User's Task | Reference File |
|---|---|
| Apex classes, triggers, testing, DML, async, dynamic Apex, JSON, wrappers, interfaces, debugging | [references/apex-patterns.md](references/apex-patterns.md) |
| SOQL/SOSL, query optimization, dynamic SOQL, Big Objects, LDV, cursors | [references/soql-optimization.md](references/soql-optimization.md) |
| LWC, Aura, dynamic components, lazy loading | [references/lwc-guide.md](references/lwc-guide.md) |
| REST/Bulk/SOAP API, integrations, OAuth, Named Credentials | [references/api-integration.md](references/api-integration.md) |
| Formulas, validation rules | [references/formulas-validation.md](references/formulas-validation.md) |
| Flows, screen flows, record-triggered flows, process automation | [references/flows-automation.md](references/flows-automation.md) |
| Security, sharing, CRUD/FLS, permissions, encryption | [references/security-sharing.md](references/security-sharing.md) |
| Deployment, sf CLI, scratch orgs, CI/CD, packaging | [references/deployment-devops.md](references/deployment-devops.md) |
| Agentforce, AI agents, Prompt Builder, platform events, CDC | [references/agentforce-ai.md](references/agentforce-ai.md) |

### Step 3: Cross-Reference the Architect Skill (for design questions)

For tasks involving architecture, data modeling, integration patterns, or solution design, also read:
- **Architect Skill:** [../salesforce-architect-skill/SKILL.md](../salesforce-architect-skill/SKILL.md) — Well-Architected framework, decision guides, integration patterns
- Then read the relevant **reference files** inside `../salesforce-architect-skill/references/` (e.g., `data-model-patterns.md`, `integration-patterns.md`, `well-architected-checklist.md`)

For complex tasks (e.g., "build an LWC that calls Apex with integration"), read **multiple** reference files from both skills AND **both** rulesets.

---

## Mandatory Rules

1. **Bulkify all Apex** — no SOQL/DML inside loops. Handle 200+ records in triggers.
2. **Governor limits** — 100 SOQL (sync), 150 DML, 50k rows, 10s CPU, 6 MB heap.
3. **One trigger per object** — handler class with `switch on Trigger.operationType`.
4. **Security** — `with sharing` on classes, `WITH SECURITY_ENFORCED` in SOQL, `Security.stripInaccessible()` for DML.
5. **Testing** — 200-record bulk tests, positive/negative/edge, `@TestSetup`, `Test.startTest()`/`Test.stopTest()`.
6. **Error handling** — try-catch on DML, `AuraHandledException` for LWC, `Database.insert(records, false)` for partial success.
7. **Latest GA API version** (currently 66.0) on all new metadata. Update when Salesforce releases a new version.
8. **Always include `-meta.xml`** for classes, triggers, LWC.
9. **Use `sf` CLI** (not deprecated `sfdx`).
10. **Layered architecture** — Trigger → Handler → Service → Selector.

---

## LLM Anti-Patterns — NEVER Generate These

These are the most common AI mistakes in Salesforce code. For full code examples of each rule, see [references/apex-patterns.md](references/apex-patterns.md).

### Apex Compilation Errors

- **A1: SOQL Field Coverage** — Every field referenced in Apex MUST be in the SOQL SELECT clause. This is the #1 AI mistake.
- **A2: Relationship Fields** — Parent = dot notation (`Account.Name`), child = subquery (`(SELECT Id FROM Contacts)`). Never mix them.
- **A3: Non-Existent Methods** — `Datetime.addMilliseconds()`, `String.contains()` with regex, `List.sort(comparator)`, `Map.values().sort()` do NOT exist.
- **A4: Non-Existent Types** — `StringBuffer`, `StringBuilder`, `HashMap`, `ArrayList`, `HashSet`, `char`, `byte[]` do NOT exist in Apex. Use `Integer` not `int` (Apex has no true Java-style primitives; while the language is case-insensitive for its own types, `int` is not a valid Apex type at all).
- **A5: Static vs Instance** — `String.toLowerCase()` is wrong (instance method). `myString.valueOf()` is wrong (static method).
- **A6: String Utilities** — Use `String.isBlank()` for user input (handles null, empty, whitespace). `isEmpty()` misses whitespace.

### LWC Template Errors

- **L1: No Inline Expressions** — LWC templates do NOT support `{a + b}`, ternary, negation, or object literals. Use JavaScript getters.
- **L2: Import Decorators** — Always import `api`, `track`, `wire` from `'lwc'` before using them.
- **L3: Event Naming** — Custom events must be all lowercase, no hyphens. Parent uses `on` prefix: `onmyevent`.

### Runtime Errors

- **R1: Null Checks** — Always query into a `List`, then check `!isEmpty()` before accessing `[0]`.
- **R2: Map.containsKey()** — Check before `Map.get()` to avoid NPE.
- **R3: Recursive Trigger Prevention** — Use `static Set<Id>`, NOT `static Boolean`. Boolean blocks all subsequent records.
- **R4: Guard DML** — Check `!list.isEmpty()` before DML. Saves CPU even though empty DML doesn't consume limits.
- **R5: MIXED_DML** — Cannot DML setup objects (User, Profile) and non-setup objects in same transaction. Use `@future` or Queueable.

### Deployment Errors

- **D1: Permission Set Fields** — Only include FLS for fields on the correct object. Skip standard non-FLS fields (`Name`, `Id`, `CreatedDate`).
- **D2: Permission Set Apex Access** — Include `classAccesses` for Apex classes used by LWC via `@AuraEnabled`.
- **D3: package.xml Order** — CustomObject → CustomField → ApexClass → ApexTrigger → Layout → PermissionSet → Profile.

### Integration Errors

- **I1: Same-Org Endpoints** — Use org's instance URL, not `api.salesforce.com`.
- **I2: Callout After DML** — Cannot make HTTP callout after DML in same transaction. Callout first, or use `@future(callout=true)`.

### Agentforce & Flow Errors

- **AF1: @AuraEnabled** — Must be `public static`. With `@wire`, must have `cacheable=true`. Class must be `with sharing`.
- **AF2: @InvocableVariable Types** — Primitives, `List<String>`, `List<Id>`, `SObject`, `List<SObject>`, Apex-defined types. NO Maps.
- **AF3: @JsonAccess** — Custom return types for Agentforce actions need `@JsonAccess(serializable='always')`.

---

## Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Classes | PascalCase + suffix | `AccountTriggerHandler`, `OrderService`, `ContactSelector` |
| Test Classes | PascalCase + `Test` | `AccountServiceTest` |
| Methods | camelCase, verb-first | `getAccountsByIds()`, `calculateTotal()` |
| Variables | camelCase | `accountList`, `totalRevenue` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE` |
| Triggers | `{Object}Trigger` | `AccountTrigger` |
| LWC | camelCase folder, kebab-case markup | `accountList` → `<c-account-list>` |
| Custom Objects | PascalCase + `__c` | `Invoice_Line_Item__c` |
| Custom Fields | PascalCase + `__c` | `Total_Amount__c` |
| Platform Events | PascalCase + `__e` | `Order_Placed__e` |
| Custom Metadata | PascalCase + `__mdt` | `Integration_Config__mdt` |

---

## Governor Limits Quick Reference

| Resource | Sync Limit | Async Limit |
|---|---|---|
| SOQL queries | 100 | 200 |
| SOQL rows | 50,000 | 50,000 |
| DML statements | 150 | 150 |
| DML rows | 10,000 | 10,000 |
| CPU time | 10,000 ms | 60,000 ms |
| Heap size | 6 MB | 12 MB |
| Callouts | 100 | 100 |
| Future calls | 50 | 0 (in future) |
| Queueable jobs | 50 | 1 |

---

## Async Apex Decision Guide

| Pattern | Use When | Key Notes |
|---|---|---|
| `@future` | Fire-and-forget, callouts | Primitives only, max 50/txn, can't chain |
| `Queueable` | Chaining, complex types, job ID | 50/txn sync, 1 child async, Transaction Finalizers |
| `Batch Apex` | 50k+ records | 200/execute, QueryLocator up to 50M rows |
| `Schedulable` | Recurring CRON jobs | 100 scheduled jobs/org |
| Platform Events | Event-driven, decoupled | `EventBus.publish()`, `RetryableException` for retry |

For full async patterns, see [references/apex-patterns.md](references/apex-patterns.md).

---

## Order of Execution

1. Load original record / initialize for insert
2. Overwrite with new field values
3. System validation (required fields, formats)
4. **Before-save record-triggered flows**
5. **Before triggers**
6. System validation + custom validation rules
7. Duplicate rules
8. Record saved to DB (not yet committed)
9. **After triggers**
10. Assignment/auto-response rules
11. Workflow rules (field updates re-fire triggers ONCE)
12. Process Builder / flow trigger workflow actions
13. **After-save record-triggered flows**
14. Roll-up summary calculations
15. Criteria-based sharing evaluation
16. **DML committed**
17. Post-commit: email, async Apex, async flow paths

**Key:** Before triggers can modify `Trigger.new` without DML. After triggers CANNOT.

---

## Code Generation Checklist

1. Every field referenced in code MUST be in the SOQL SELECT clause (Rule A1)
2. Include `-meta.xml` for all new classes, triggers, LWC
3. Latest GA API version (currently 66.0) on all metadata
4. Include JSDoc in LWC JavaScript and ApexDoc in Apex
5. Wrap DML in try-catch, use `AuraHandledException` for LWC
6. Use `WITH SECURITY_ENFORCED` in SOQL
7. Use `Database.insert(records, false)` for partial success
8. Null-check query results, `Map.get()` returns, parent relationship fields
9. Guard DML with `!list.isEmpty()`
10. Use `with sharing` on user-facing classes, `inherited sharing` on utilities
11. Use `switch on Trigger.operationType` in handlers
12. Never hardcode IDs — use `Schema.describe`, Custom Metadata, or Custom Labels
13. Prefer `Assert.areEqual()` (modern Assert class) over `System.assertEquals()` for new code
14. Test methods use Arrange-Act-Assert with descriptive names

---

## Common Error Solutions

| Error | Fix |
|---|---|
| `Too many SOQL queries: 101` | Move query outside loop, use Maps |
| `MIXED_DML_OPERATION` | Use `@future` or Queueable for setup object DML |
| `Non-selective query` | Add indexed filter, request custom index |
| `You have uncommitted work` | Move callout before DML or use `@future(callout=true)` |
| `NullPointerException` | Add null checks; query into List + `isEmpty()` |
| `SObject row was retrieved via SOQL without querying the requested field` | Add field to SOQL SELECT (Rule A1) |
| `Too many DML statements: 151` | Collect records in lists, single DML outside loop |
| `UNABLE_TO_LOCK_ROW` | Use `FOR UPDATE` or implement retry |
| `Apex CPU time limit exceeded` | Optimize loops, use async Apex |

For full error patterns and JSON/debugging details, see [references/apex-patterns.md](references/apex-patterns.md).

---

## Metadata XML Templates

### Apex Class
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>66.0</apiVersion>
    <status>Active</status>
</ApexClass>
```

### Apex Trigger
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ApexTrigger xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>66.0</apiVersion>
    <status>Active</status>
</ApexTrigger>
```

### LWC Component
```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>66.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__RecordPage</target>
        <target>lightning__AppPage</target>
        <target>lightning__HomePage</target>
    </targets>
</LightningComponentBundle>
```

---

## Project Structure

```
force-app/main/default/
├── classes/         # Handler, Service, Selector, Controller, Test classes + -meta.xml
├── triggers/        # One trigger per object + -meta.xml
├── lwc/             # camelCase folders with html/js/css/js-meta.xml + __tests__/
├── objects/         # fields/, validationRules/, listViews/
├── permissionsets/
├── customMetadata/
└── labels/
```

**Architecture:** Trigger (thin) → Handler (routing, recursion guard) → Service (business logic, DML) → Selector (SOQL, `with sharing`)

---

## Quick Reference Pointers

- **Apex coding rules (full ruleset)** → [../../Blogs/salesforce-apex-coding-rules.md](../../Blogs/salesforce-apex-coding-rules.md)
- **LWC coding rules (full ruleset)** → [../../Blogs/salesforce-lwc-coding-rules.md](../../Blogs/salesforce-lwc-coding-rules.md)
- **Architecture & solution design** → [../salesforce-architect-skill/SKILL.md](../salesforce-architect-skill/SKILL.md)
- **Security & sharing rules** → [references/security-sharing.md](references/security-sharing.md)
- **Agentforce, platform events, CDC** → [references/agentforce-ai.md](references/agentforce-ai.md)
- **OAuth, Named Credentials, Connected Apps** → [references/api-integration.md](references/api-integration.md)
- **LDV, custom indexes, data skew, Big Objects** → [references/soql-optimization.md](references/soql-optimization.md)
- **Dynamic LWC, lazy loading** → [references/lwc-guide.md](references/lwc-guide.md)
- **sf CLI commands, CI/CD pipelines** → [references/deployment-devops.md](references/deployment-devops.md)
- **Flow decision guide, invocable Apex** → [references/flows-automation.md](references/flows-automation.md)
