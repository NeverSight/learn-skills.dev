---
name: happy-servicenow-skills
version: 1.0.0
author: Happy Technologies LLC
description: Platform-agnostic AI skills library for ServiceNow - 47 comprehensive skills for ITSM, CMDB, Catalog, Security, Reporting, and Development
tags:
  - servicenow
  - itsm
  - itil
  - cmdb
  - incident-management
  - change-management
  - development
  - enterprise
---

# Happy ServiceNow AI Skills

A comprehensive library of platform-agnostic AI skills for ServiceNow development and administration. Works with Claude Code, Claude Desktop, ChatGPT, Cursor, and any agentic AI system.

## When to use this skill

Use these skills when you need to:
- "help me triage ServiceNow incidents"
- "create a change request in ServiceNow"
- "write a business rule for incident assignment"
- "set up a catalog item with approval workflow"
- "query CMDB relationships"
- "debug a client script"
- "manage update sets and deployments"

## Available Skill Categories

### ITSM (7 skills)
- **incident-triage** - Automated incident classification and prioritization
- **incident-lifecycle** - End-to-end incident management workflow
- **major-incident** - P1/Major incident coordination
- **problem-analysis** - Root cause analysis and known error management
- **change-management** - RFC creation, CAB, implementation, PIR
- **natural-language-queries** - Plain English ServiceNow searches
- **quick-reference** - Common operations cheat sheet

### Development (12 skills)
- **business-rules** - Server-side automation scripts
- **client-scripts** - Form manipulation and validation
- **script-includes** - Reusable server-side libraries
- **glide-api-reference** - GlideRecord, GlideAggregate, GlideDateTime
- **debugging-techniques** - Script debugger, logging, troubleshooting
- **notifications** - Email notifications, events, templates
- **ui-actions** - Buttons, context menus, client/server actions
- **scheduled-jobs** - Automated recurring tasks
- **data-import** - Import sets and transform maps
- **scripted-rest-apis** - Custom REST endpoints
- **automated-testing** - ATF and script testing
- **performance-optimization** - Script optimization techniques

### Administration (12 skills)
- **update-set-management** - Configuration tracking and deployment
- **deployment-workflow** - Instance-to-instance migration
- **batch-operations** - Bulk record operations
- **script-execution** - Background script patterns
- **script-sync** - Local development workflow
- **user-provisioning** - User lifecycle management
- **workflow-creation** - Programmatic workflow building
- **schema-discovery** - Table and field exploration
- **instance-management** - Multi-instance operations
- **application-scope** - Scoped app development
- **configuration-validation** - Catalog item validation
- **generic-crud-operations** - Universal table operations

### Service Catalog (5 skills)
- **request-fulfillment** - End-to-end request processing
- **item-creation** - Catalog item setup
- **approval-workflows** - Approval configuration
- **variable-management** - Form variables and options
- **ui-policies** - Dynamic form behavior

### CMDB (4 skills)
- **ci-discovery** - Configuration item management
- **relationship-mapping** - CI relationships and dependencies
- **impact-analysis** - Service impact assessment
- **data-quality** - CMDB health and validation

### Security (4 skills)
- **incident-response** - Security incident handling
- **acl-management** - Access control configuration
- **audit-compliance** - Compliance monitoring
- **data-classification** - Data sensitivity management

### Reporting (3 skills)
- **sla-analysis** - SLA performance metrics
- **executive-dashboard** - KPI dashboards
- **trend-analysis** - Historical trend reporting

## Installation

```bash
# Install all skills
npx skills add Happy-Technologies-LLC/happy-servicenow-skills --all

# Install specific category
npx skills add Happy-Technologies-LLC/happy-servicenow-skills -s "itsm/*"

# Install single skill
npx skills add Happy-Technologies-LLC/happy-servicenow-skills -s "development/business-rules"
```

## Usage with npm

```bash
# Install globally
npm install -g happy-servicenow-skills

# Search skills
npx sn-skills search "incident"

# Load skill content
npx sn-skills load itsm/incident-triage

# Validate skills
npx sn-skills validate
```

## Skill Format

Each skill includes:
- **Overview** - What the skill does and when to use it
- **Prerequisites** - Required roles and knowledge
- **Procedure** - Step-by-step instructions with MCP tool examples
- **Best Practices** - ITIL-aligned recommendations
- **Troubleshooting** - Common issues and solutions
- **Related Skills** - Cross-references to related content

## MCP Tool Coverage

These skills provide full parity with the ServiceNow MCP Server tools:
- Query and CRUD operations (SN-Query-Table, SN-Create-Record, etc.)
- Update set management (SN-Set-Update-Set, SN-Clone-Update-Set)
- Script execution (SN-Execute-Background-Script)
- Natural language interface (SN-NL-Search, SN-NL-Query-Builder)
- Batch operations (SN-Batch-Create, SN-Batch-Update)
- Workflow creation (SN-Create-Workflow, SN-Create-Activity)
- And 35+ more tools

## Contributing

See [CREATING_SKILLS.md](docs/CREATING_SKILLS.md) for contribution guidelines.

## License

MIT - Happy Technologies LLC
