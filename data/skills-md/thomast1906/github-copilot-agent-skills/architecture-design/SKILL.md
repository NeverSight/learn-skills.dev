---
name: architecture-design
description: Design Azure cloud architectures from requirements and generate High-Level Design (HLD) documentation with service selection, patterns, cost estimates, and WAF alignment. Use this when asked to design or architect Azure solutions.
---

# Architecture Design Skill

Design comprehensive Azure architectures and produce HLD documentation following Well-Architected Framework and Cloud Adoption Framework best practices.

## When to Use

- Design new Azure solutions from requirements
- Create High-Level Design (HLD) documentation
- Select Azure services and architectural patterns
- Plan cloud migrations or modernization
- Produce architecture decision records

## Design Process

### 1. Gather Requirements

Ask clarifying questions about:
- **Workload type**: Web app, API, data processing, IoT, AI/ML
- **Scale**: User count, data volume, geographic distribution
- **Performance**: Response time, throughput, latency SLAs
- **Availability**: Uptime requirements (e.g., 99.9%, 99.99%)
- **Security**: Data classification, compliance (HIPAA, GDPR, PCI-DSS)
- **Budget**: Monthly/annual cost constraints
- **Timeline**: Deployment deadlines, phasing needs

### 2. Select Azure Services

**Service Selection Priority:** PaaS > Containers > IaaS

Refer to [references.md](./references.md) for detailed guidance on:
- Compute options (App Service, Functions, AKS, Container Apps, VMs)
- Data storage (Azure SQL, Cosmos DB, PostgreSQL, Blob Storage)
- Messaging (Service Bus, Event Hubs, Event Grid, Storage Queues)
- Networking (Front Door, Application Gateway, Load Balancer)

**Key Decision Criteria:**
- Match service capabilities to requirements
- Consider team expertise and operational overhead
- Evaluate cost vs. feature trade-offs
- Prioritize managed services to reduce operations

### 3. Design Architecture

Apply patterns based on requirements:

**N-Tier (Traditional):**
- **When**: Standard web apps, proven patterns, team familiarity
- **Structure**: Frontend → Load Balancer → App Tier → Database
- **Services**: App Service, Azure SQL, Application Gateway, Redis Cache

**Microservices:**
- **When**: Loosely coupled services, independent scaling, polyglot needs
- **Structure**: API Gateway → Services → Message Bus → Databases
- **Services**: API Management, AKS/Container Apps, Service Bus, Cosmos DB

**Event-Driven:**
- **When**: Asynchronous processing, reactive systems, decoupled components
- **Structure**: Event Sources → Event Hub/Grid → Functions/Logic Apps → Storage
- **Services**: Event Hubs, Azure Functions, Cosmos DB, Service Bus

**Serverless:**
- **When**: Sporadic workloads, event processing, cost-sensitive scenarios
- **Structure**: HTTP/Timer/Queue Triggers → Functions → Storage/Database
- **Services**: Azure Functions, Logic Apps, Cosmos DB, Blob Storage

### 4. Apply Well-Architected Framework

Address all five pillars (detailed checklists in [waf-assessment skill](../waf-assessment/)):

**Reliability:**
- Availability Zones for production
- Multi-region for mission-critical (99.99%+)
- Health checks and auto-healing
- Backup strategy with RPO/RTO defined

**Security:**
- Managed identities (no credentials in code)
- Private endpoints for PaaS services
- HTTPS only with TLS 1.2+
- Network security groups (least privilege)
- Azure Key Vault for secrets
- Azure AD authentication and RBAC

**Cost Optimization:**
- Right-size resources (start small, scale up)
- Auto-scaling policies
- Reserved instances for predictable workloads
- Storage tiers (Hot/Cool/Archive)
- Cost monitoring and alerts

**Operational Excellence:**
- Infrastructure as Code (Bicep or Terraform)
- CI/CD pipelines
- Application Insights + Log Analytics
- Alerts for critical scenarios
- Automated deployment and rollback

**Performance Efficiency:**
- CDN for static content
- Caching strategy (Redis, CDN)
- Asynchronous processing
- Appropriate compute SKUs
- Auto-scaling rules

### 5. Create Naming Convention

Follow Cloud Adoption Framework:
```
{resource-type}-{workload}-{environment}-{region}-{instance}

Examples:
- rg-ecommerce-prod-eastus-001
- app-ecommerce-prod-eastus-001
- sql-ecommerce-prod-eastus-001
- kv-ecommerce-prod-eastus
- func-orderproc-prod-eastus-001
```

**Standard Tags:**
```
Environment: Production | Staging | Development | Test
Owner: teamname@company.com
CostCenter: IT-12345
Project: ProjectName
BusinessUnit: Sales | Marketing | Engineering
Criticality: Critical | High | Medium | Low
DataClassification: Public | Internal | Confidential | Restricted
```

### 6. Estimate Costs

Provide monthly cost breakdown by service category:
- Compute (App Service, Functions, VMs)
- Data (SQL, Cosmos DB, Storage)
- Networking (Front Door, App Gateway, Bandwidth)
- Monitoring (Application Insights, Log Analytics)

Include cost optimization opportunities and reserved instance recommendations.

## High-Level Design Output Format

Generate comprehensive HLD documents with these sections:

### 1. Executive Summary
- Solution overview (2-3 paragraphs)
- Key benefits and business value
- High-level cost estimate
- Timeline and deployment approach

### 2. Requirements Summary
- Functional requirements (bullet points)
- Non-functional requirements (performance, availability, security)
- Constraints and assumptions

### 3. Architecture Overview
- Architecture diagram description (components and connections)
- Design pattern used (N-tier, microservices, event-driven, serverless)
- Rationale for architectural approach

### 4. Component Design

For each component:
- **Service Name**: Azure service selected
- **SKU/Tier**: Specific pricing tier (e.g., App Service P2v3, Azure SQL S2)
- **Purpose**: Role in the architecture
- **Configuration**: Key settings (regions, zones, instances, capacity)
- **Naming**: Following CAF convention (rg-app-prod-eastus-001)

### 5. Networking Design
- Virtual Network configuration (address spaces)
- Subnets and network security groups
- Private endpoints and service endpoints
- Ingress/egress patterns (load balancers, gateways)
- DNS configuration

### 6. Security Design
- Authentication and authorization (Azure AD, Managed Identity)
- Secrets management (Key Vault)
- Encryption (at-rest and in-transit)
- Network security (NSGs, firewalls, WAF)
- Compliance requirements

### 7. Data Design
- Database schema approach
- Data flow between components
- Backup and recovery strategy (RPO/RTO)
- Data retention policies
- Disaster recovery approach

### 8. Monitoring and Operations
- Application Insights configuration
- Log Analytics workspace
- Key metrics to monitor
- Alert definitions and thresholds
- Dashboard recommendations

### 9. Deployment Strategy
- Infrastructure as Code approach (Bicep or Terraform)
- CI/CD pipeline design
- Environment strategy (dev, staging, prod)
- Deployment sequence and dependencies
- Rollback procedure

### 10. Cost Breakdown
- Monthly cost estimate by service
- Annual projection
- Cost optimization recommendations
- Reserved instance opportunities

### 11. Well-Architected Assessment
- Brief evaluation against each WAF pillar
- Key strengths of the design
- Areas for future improvement

### 12. Risks and Mitigations
- Identified technical risks
- Mitigation strategies
- Dependencies and assumptions

### 13. Next Steps
- Immediate actions (Phase 1)
- Short-term improvements (Phase 2)
- Long-term roadmap (Phase 3)

## Example HLD Snippet

```markdown
# High-Level Design: E-Commerce Web Platform

## 1. Executive Summary

This HLD describes a scalable e-commerce platform on Azure supporting up to 100K concurrent users
with 99.95% availability. The solution uses proven PaaS services with multi-region capabilities,
comprehensive security controls, and cost-optimized infrastructure.

**Key Benefits:**
- Global reach with Azure Front Door CDN
- Auto-scaling for traffic spikes (Black Friday, holidays)
- PCI-DSS compliant payment processing
- Estimated cost: $2,850/month (Production)

**Timeline:** 8-week implementation with phased rollout

## 3. Architecture Overview

**Pattern:** N-Tier with asynchronous order processing

**Components:**
```
Azure Front Door (Global CDN + WAF)
└─ Application Gateway (Regional WAF + LB)
   ├─ App Service (Web Frontend - 3 instances, P2v3)
   ├─ App Service (API Backend - 3 instances, P2v3)
   ├─ Azure Functions (Order Processor, Premium)
   ├─ Azure SQL Database (S2 DTU, 50GB)
   ├─ Redis Cache (Basic C1, 1GB)
   └─ Blob Storage (Hot tier, product images)
```

**Rationale:** N-tier provides proven scalability, PaaS reduces operational overhead,
Functions handle asynchronous order processing, Azure SQL provides ACID guarantees.

## 4. Component Design

**Frontend Web App**
- Service: Azure App Service (Linux)
- SKU: P2v3 (2 vCores, 8GB RAM)
- Instances: 3 (Availability Zones 1, 2, 3)
- Auto-scale: 3-10 instances based on CPU > 70%
- Naming: app-ecommerce-web-prod-eastus-001
- Purpose: Serves customer-facing website

[Continue with all components...]
```

## Tips for Great HLDs

**Be Specific:** Use exact service names and SKUs (not "database" but "Azure SQL Database S2 DTU")
**Show Trade-offs:** Explain why you chose service X over Y
**Include Diagrams:** Describe architecture visually with clear component relationships
**Cost-Aware:** Always provide cost estimates and optimization opportunities
**Security First:** Address authentication, authorization, encryption, network security
**WAF Alignment:** Reference specific WAF principles in design decisions
**Naming Standards:** Use CAF conventions consistently
**Implementation-Ready:** Provide enough detail for IaC generation

**Avoid:** Vague terms, missing costs, ignoring security, skipping WAF, incomplete components, no rationale
