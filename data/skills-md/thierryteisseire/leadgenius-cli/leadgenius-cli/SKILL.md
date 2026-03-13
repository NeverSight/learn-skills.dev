---
name: leadgenius-cli
description: Comprehensive skill for operating the LeadGenius Pro Automation API and lgp CLI. Covers ICP management, FSD pipeline automation, lead generation/enrichment/scoring, user provisioning, territory analysis, webhook management, and email platform integration.
---

# LeadGenius Pro — CLI & Automation API Skill

This skill teaches AI agents how to operate the **LeadGenius Pro Automation API** and the **`lgp` CLI tool**. It covers the full lifecycle of B2B lead management — from ICP (Ideal Customer Profile) definition and automated lead generation through enrichment, scoring, qualification, and email delivery via the FSD (Full-Stack Demand) pipeline.

## Base URL

```
https://api.leadgenius.app
```

All API endpoints live under `/api/automation/`.

## Authentication

Every request must include an API key in the `X-API-Key` header:

```
X-API-Key: lgp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- Keys are prefixed with `lgp_` and tied to a specific company.
- The key determines `company_id`, `owner` identity, and rate limits.
- Keys are created via `POST /api/automation/users/provision` — the plain-text key is returned only once at creation time.
- Test your key with `GET /api/automation/auth/test`.

### Rate Limits

| Window     | Default Limit    |
|------------|------------------|
| Per minute | 60 requests      |
| Per hour   | 1,000 requests   |
| Per day    | 10,000 requests  |

---

## Prerequisites Checklist

Before running enrichment, copyright, scoring, or FSD pipelines, the following configuration records must exist. Create them via the Tables API (`POST /api/automation/tables/{tableName}`).

### UrlSettings (required for enrichment)

| Field                | Description                              |
|----------------------|------------------------------------------|
| `companyUrl`         | Company URL lookup service endpoint      |
| `companyUrl_Apikey`  | API key for company URL service          |
| `emailFinder`        | Email finder service endpoint            |
| `emailFinder_Apikey` | API key for email finder service         |
| `enrichment1`–`enrichment10` | Enrichment service endpoints (up to 10) |
| `enrichment1_Apikey`–`enrichment10_Apikey` | Corresponding API keys |

### AgentSettings (required for copyright / AI content generation)

| Field                          | Description                                |
|--------------------------------|--------------------------------------------|
| `projectId`                    | EpsimoAI project ID                        |
| `enrichment1AgentId`–`enrichment10AgentId` | EpsimoAI agent IDs for each copyright process |

### SdrAiSettings (required for SDR AI scoring)

| Field                          | Description                                |
|--------------------------------|--------------------------------------------|
| `projectId`                    | EpsimoAI project ID                        |
| `aiLeadScoreAgentId`          | Agent for lead scoring                     |
| `aiQualificationAgentId`      | Agent for qualification assessment         |
| `aiNextActionAgentId`         | Agent for next-action recommendation       |
| `aiColdEmailAgentId`          | Agent for cold email generation            |
| `aiInterestAgentId`           | Agent for interest analysis                |
| `aiLinkedinConnectAgentId`    | Agent for LinkedIn connect messages        |
| `aiCompetitorAnalysisAgentId` | Agent for competitor analysis              |
| `aiEngagementLevelAgentId`    | Agent for engagement level assessment      |
| `aiPurchaseWindowAgentId`     | Agent for purchase window estimation       |
| `aiDecisionMakerRoleAgentId`  | Agent for decision-maker role detection    |
| `aiSentimentAgentId`          | Agent for sentiment analysis               |
| `aiSocialEngagementAgentId`   | Agent for social engagement scoring        |
| `aiNurturingStageAgentId`     | Agent for nurturing stage classification   |
| `aiBudgetEstimationAgentId`   | Agent for budget estimation                |
| `aiRiskScoreAgentId`          | Agent for risk scoring                     |
| `aiProductFitScoreAgentId`    | Agent for product-fit scoring              |

### ICP with Apify Config (required for lead generation)

| Field             | Description                                      |
|-------------------|--------------------------------------------------|
| `name`            | ICP display name                                 |
| `apifyActorId`    | Apify actor ID for lead scraping (required)      |
| `apifyInput`      | JSON string of actor input configuration         |
| `apifySettings`   | JSON string of additional Apify settings         |
| `maxLeads`        | Max leads per generation run (default 100)       |
| `industries`      | JSON array of target industries                  |
| `companySizes`    | JSON array of size ranges ("1-10", "51-200")     |
| `geographies`     | JSON array of countries/regions                  |
| `jobTitles`       | JSON array of target job titles                  |
| `seniority`       | JSON array of seniority levels                   |
| `client_id`       | Client partition for data isolation              |

### Client (required for data isolation)

| Field         | Description                          |
|---------------|--------------------------------------|
| `clientName`  | Display name for the client          |
| `companyURL`  | Company website URL                  |
| `description` | Client description                   |

### EmailPlatformSettings (required for email delivery)

| Field        | Description                              |
|--------------|------------------------------------------|
| `platform`   | Email platform name (e.g., "woodpecker") |
| `apiKey`     | Platform API key                         |
| `campaignId` | Default campaign ID on the platform      |

---

## Quick-Reference: Endpoint Map

| API Section         | Reference                                                        |
|---------------------|------------------------------------------------------------------|
| Auth                | [references/api_endpoints.md#authentication](references/api_endpoints.md#authentication) |
| Leads               | [references/api_endpoints.md#leads](references/api_endpoints.md#leads) |
| Tasks               | [references/api_endpoints.md#tasks](references/api_endpoints.md#tasks) |
| Territory           | [references/api_endpoints.md#territory-companies](references/api_endpoints.md#territory-companies) |
| Webhooks            | [references/api_endpoints.md#webhook-events](references/api_endpoints.md#webhook-events) |
| Users               | [references/api_endpoints.md#users](references/api_endpoints.md#users) |
| Organizations       | [references/api_endpoints.md#organizations](references/api_endpoints.md#organizations) |
| Tables / ICP        | [references/api_endpoints.md#tables-generic-crud-with-icp-focus](references/api_endpoints.md#tables-generic-crud-with-icp-focus) |
| Email Platforms     | [references/api_endpoints.md#email-platforms](references/api_endpoints.md#email-platforms) |
| FSD Pipeline        | [references/api_endpoints.md#fsd-pipeline](references/api_endpoints.md#fsd-pipeline) |
| Error Codes         | [references/api_endpoints.md#error-codes](references/api_endpoints.md#error-codes) |

## Quick-Reference: CLI Map

| Command Group      | Reference                                                          |
|--------------------|--------------------------------------------------------------------|
| `auth`             | [references/cli_reference.md#auth](references/cli_reference.md#auth) |
| `leads`            | [references/cli_reference.md#leads](references/cli_reference.md#leads) |
| `tasks`            | [references/cli_reference.md#tasks](references/cli_reference.md#tasks) |
| `companies`        | [references/cli_reference.md#companies](references/cli_reference.md#companies) |
| `webhooks`         | [references/cli_reference.md#webhooks](references/cli_reference.md#webhooks) |
| `tables`           | [references/cli_reference.md#tables](references/cli_reference.md#tables) |
| `email-platforms`  | [references/cli_reference.md#email-platforms](references/cli_reference.md#email-platforms) |
| `users`            | [references/cli_reference.md#users](references/cli_reference.md#users) |
| `cognito`          | [references/cli_reference.md#cognito](references/cli_reference.md#cognito) |
| `org`              | [references/cli_reference.md#org](references/cli_reference.md#org) |
| `fsd`              | [references/cli_reference.md#fsd](references/cli_reference.md#fsd) |
