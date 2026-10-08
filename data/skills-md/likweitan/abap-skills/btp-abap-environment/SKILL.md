---
name: btp-abap-environment
description: Help with SAP BTP ABAP Environment setup and development including service instance creation, ADT connectivity, communication arrangements, communication scenarios, inbound/outbound services, destination configuration, identity and access management, software components, and first-project scaffolding. Use when users ask about BTP ABAP Environment, SAP BTP ABAP, Steampunk, ABAP environment service instance, ADT connection to BTP, communication arrangement, communication scenario, communication system, outbound communication, inbound communication, destination service, software component, ABAP system on BTP, or cloud ABAP development setup. Triggers include "set up BTP ABAP", "connect ADT to BTP", "communication arrangement", "communication scenario", "create service instance", "ABAP on BTP", "outbound service", or "first ABAP project on BTP".
---

# SAP BTP ABAP Environment

Guide for setting up and developing in the SAP BTP ABAP Environment (Steampunk).

## Workflow

1. **Determine the user's goal**:
   - Setting up a new ABAP Environment instance
   - Connecting ADT to the BTP ABAP system
   - Configuring communication arrangements for integrations
   - Creating a first ABAP Cloud project
   - Managing software components and packages
   - Setting up outbound/inbound connectivity

2. **Identify the phase**:
   - Initial provisioning and setup
   - Developer onboarding
   - Integration configuration
   - Application development

3. **Guide implementation** step by step

## Setup Overview

### Prerequisites

| Requirement         | Description                                           |
| ------------------- | ----------------------------------------------------- |
| **SAP BTP Account** | Global account with entitlements for ABAP Environment |
| **Subaccount**      | Cloud Foundry-enabled subaccount                      |
| **ADT**             | Eclipse with ABAP Development Tools installed         |
| **User**            | Platform user with Space Developer role               |
| **Entitlements**    | `abap/standard` or `abap/saas_oem` service plan       |

### Service Instance Creation

1. Navigate to BTP Cockpit → Subaccount → Cloud Foundry → Spaces
2. Create service instance:
   - Service: **ABAP Environment**
   - Plan: **standard**
   - Instance name: e.g., `my-abap-instance`
3. Provide parameters (JSON):

```json
{
  "admin_email": "admin@example.com",
  "description": "Development ABAP System",
  "is_development_allowed": true,
  "sapsystemname": "DEV",
  "size_of_runtime": 1,
  "size_of_persistence": 4
}
```

4. Create a service key for ADT connectivity

### Connecting ADT to BTP ABAP

1. In Eclipse/ADT: **File → New → ABAP Cloud Project**
2. Select **SAP BTP ABAP Environment**
3. Enter the service key (JSON) or service instance URL
4. Authenticate via browser (SAP Identity Authentication)
5. Project is created — start developing

## System Architecture

```
SAP BTP Subaccount
└── Cloud Foundry Space
    └── ABAP Environment Service Instance
        ├── ABAP System (development/production)
        ├── Software Components (ZLOCAL, custom)
        ├── Communication Arrangements (integrations)
        └── Business Services (OData, RFC)
```

## Software Components

| Component | Description                                                                   |
| --------- | ----------------------------------------------------------------------------- |
| `ZLOCAL`  | Local development — not transportable (like `$TMP`)                           |
| Custom    | Transportable components — managed via gCTS or Manage Software Components app |

### Creating a Software Component

1. Open the **Manage Software Components** Fiori app
2. Click **Create** (or use the `+` button)
3. Enter:
   - Name: `Z_MY_COMPONENT`
   - Description: e.g., "My Custom Component"
   - Type: Development
4. **Clone** the component to make it available in ADT
5. Create packages within the component

### Package Structure

```
Z_MY_COMPONENT (Software Component)
└── Z_MY_APP (Structure Package)
    ├── Z_MY_APP_MODEL (Sub-package: CDS views, database tables)
    ├── Z_MY_APP_BIZ (Sub-package: business logic, RAP BOs)
    └── Z_MY_APP_SRV (Sub-package: service definitions, bindings)
```

## Communication Management

### Concepts

| Artifact                      | Purpose                                                      |
| ----------------------------- | ------------------------------------------------------------ |
| **Communication Scenario**    | Template defining inbound/outbound services and auth methods |
| **Communication System**      | Represents the external system (host, port, credentials)     |
| **Communication Arrangement** | Binds scenario + system + user, activating the integration   |
| **Communication User**        | Technical user for inbound communication                     |

### Creating a Communication Scenario

```abap
"Defined via ADT: New → Other → Communication Scenario
"Name: Z_MY_COMM_SCENARIO
```

Communication scenario definition (in ADT):

| Property                 | Value                          |
| ------------------------ | ------------------------------ |
| **Scenario ID**          | `Z_MY_COMM_SCENARIO`           |
| **Scenario Type**        | Managed by Customer            |
| **Inbound Services**     | List of inbound OData services |
| **Outbound Services**    | List of outbound HTTP services |
| **Allowed Auth Methods** | Basic, OAuth 2.0, x.509        |

### Outbound Communication (Calling External Services)

```abap
"Get HTTP destination from communication arrangement
DATA(lo_dest) = cl_http_destination_provider=>create_by_comm_arrangement(
  comm_scenario  = 'Z_MY_COMM_SCENARIO'
  service_id     = 'Z_MY_OUTBOUND_SERVICE' ).

"Create HTTP client
DATA(lo_client) = cl_web_http_client_manager=>create_by_http_destination( lo_dest ).

"Execute request
DATA(lo_request) = lo_client->get_http_request( ).
lo_request->set_uri_path( '/api/resource' ).
lo_request->set_header_field( i_name = 'Content-Type' i_value = 'application/json' ).

DATA(lo_response) = lo_client->execute( if_web_http_client=>get ).
DATA(lv_status) = lo_response->get_status( ).
DATA(lv_body) = lo_response->get_text( ).

lo_client->close( ).
```

### Inbound Communication (Exposing Services)

1. Create an OData service (RAP-based)
2. Add the service binding to a communication scenario as inbound service
3. Create communication arrangement in Fiori app:
   - Select scenario
   - Create or assign communication system
   - Create communication user (for Basic auth) or configure OAuth
4. External systems can now call the service

## Identity and Access Management

### Business Roles and Catalogs

```
IAM App → Business Catalog → Business Role → Business User
```

1. **Create IAM App** in ADT (for your service binding)
2. **Create Business Catalog** containing the IAM App
3. **Create Business Role** in Fiori including the catalog
4. **Assign Business Role** to users

### Creating an IAM App

```
ADT: New → Other → IAM App
Name: Z_MY_APP_IAM
Service Binding: Z_MY_SERVICE_BINDING
```

## First Project Scaffolding

Quick steps to create a minimal RAP-based Fiori app:

1. **Create database table**
2. **Create CDS root view entity** on the table
3. **Create CDS projection view** (consumption view)
4. **Create behavior definition** (managed, with draft)
5. **Create behavior implementation** class
6. **Create service definition** exposing projection
7. **Create service binding** (OData V4 - UI)
8. **Publish** and **Preview** in Fiori Elements

## Useful Fiori Apps

| App                                | Purpose                                 |
| ---------------------------------- | --------------------------------------- |
| **Manage Software Components**     | Create, clone, pull software components |
| **Communication Arrangements**     | Configure inbound/outbound integrations |
| **Communication Systems**          | Register external systems               |
| **Maintain Business Roles**        | Create and assign roles                 |
| **Application Jobs**               | Schedule and monitor background jobs    |
| **Custom Business Configurations** | Maintain configuration tables           |

## Output Format

When helping with BTP ABAP Environment topics, structure responses as:

```markdown
## BTP ABAP Environment Guidance

### Phase

- [Setup / Development / Integration / Deployment]

### Steps

[Step-by-step instructions]

### Configuration

[Relevant settings or code]
```

## References

- SAP BTP ABAP Environment: https://help.sap.com/docs/btp/sap-business-technology-platform/abap-environment
- Communication Management: https://help.sap.com/docs/btp/sap-business-technology-platform/communication-management
- Getting Started Tutorial: https://developers.sap.com/group.abap-env-get-started.html

## Related Skills

- **abap-cloud**: Use for ABAP Cloud development concepts and restrictions
- **authorization-iam**: Use for setting up IAM apps and business roles
- **rap**: Use for building RAP business objects in BTP ABAP Environment
- **abapgit**: Use for version control in BTP ABAP Environment
