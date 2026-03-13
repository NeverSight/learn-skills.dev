---
name: cost-optimization
description: Analyze Azure architectures for cost optimization opportunities, provide savings recommendations, and calculate ROI for improvements.
---

# Cost Optimization Skill

Analyze Azure costs and identify optimization opportunities across compute, storage, networking, and data services. Provide actionable recommendations with savings estimates.

## When to Use

- Review architecture costs and identify waste
- Optimize existing Azure deployments
- Right-size over-provisioned resources
- Implement reserved instances and savings plans
- Set up cost monitoring and alerts
- Reduce monthly Azure bills

## Cost Optimization Categories

### 1. Right-Sizing
Adjust resource SKUs to match actual usage patterns.

**Target Resources:**
- Virtual Machines
- App Service Plans
- SQL Databases
- Cosmos DB throughput
- Azure Cache for Redis

**Analysis Method:**
1. Review 30-day metrics (CPU, memory, DTU utilization)
2. Identify resources with < 40% average utilization
3. Recommend smaller SKU or scaling adjustments

**Typical Savings:** 30-50%

### 2. Reserved Instances & Savings Plans
Commit to 1-year or 3-year terms for predictable workloads.

**Eligible Services:**
- Virtual Machines
- App Service Plans
- Azure SQL Database
- Cosmos DB
- Azure Cache for Redis

**Savings:**
- 1-year: 20-40%
- 3-year: 40-72%

**When to Use:** Workloads with consistent, predictable usage

### 3. Auto-Scaling
Scale resources based on demand instead of static provisioning.

**Applicable Services:**
- App Service
- Virtual Machine Scale Sets
- Container Apps
- AKS node pools
- Cosmos DB autoscale

**Typical Savings:** 20-40% (eliminates idle capacity during off-peak)

### 4. Storage Tiering
Move infrequently accessed data to cheaper storage tiers.

**Blob Storage Tiers:**
- **Hot**: Frequent access (< 30 days old)
- **Cool**: Infrequent access (30-90 days), 50% cheaper
- **Archive**: Rare access (> 90 days), 90% cheaper

**Implementation:** Lifecycle management policies

**Typical Savings:** 50-90% on archived data

### 5. Eliminate Waste
Identify and remove unused resources.

**Common Waste:**
- Unattached disks
- Stopped (but not deallocated) VMs
- Orphaned public IPs
- Unused App Service Plans
- Old snapshots and backups
- Idle Load Balancers

**Typical Savings:** $200-2,000/month per environment

## Cost Analysis Process

### Step 1: Gather Current Costs

Extract cost data from Azure Cost Management:
- Last 30-60 days of spending by resource
- Group by resource type and resource group
- Identify top 10 cost contributors

### Step 2: Analyze Resource Utilization

For each major resource:
- **Compute**: Average CPU, memory utilization
- **Database**: DTU/vCore usage, storage growth
- **Storage**: Access patterns, growth rate
- **Networking**: Bandwidth usage, idle resources

### Step 3: Identify Opportunities

Categorize findings:
- **Quick Wins**: < 1 hour, immediate savings (delete unused resources)
- **Right-Sizing**: < 1 day, 30-50% savings
- **Reserved Instances**: < 1 hour setup, 1-3 year commitment
- **Architecture Changes**: > 1 week, significant redesign

### Step 4: Calculate ROI

For each recommendation:
- Current monthly cost
- Optimized monthly cost
- Monthly savings
- Implementation effort (hours)
- Break-even time

## Output Format

```markdown
# Cost Optimization Analysis
**Architecture**: [Name]
**Current Monthly Cost**: $X,XXX
**Optimized Monthly Cost**: $X,XXX
**Potential Savings**: $XXX/month (XX%)
**Annual Savings**: $X,XXX

---

## Executive Summary
[2-3 sentences on current spending, biggest opportunities, recommended priorities]

---

## Current Cost Breakdown

| Category | Monthly Cost | % of Total |
|----------|-------------|------------|
| Compute | $1,200 | 45% |
| Database | $800 | 30% |
| Storage | $300 | 11% |
| Networking | $250 | 9% |
| Monitoring | $150 | 5% |
| **Total** | **$2,700** | **100%** |

---

## Optimization Opportunities

### Priority 1: Quick Wins (< 1 day effort)

#### Opportunity #1: Delete Unattached Disks
**Current Cost**: $80/month
**Savings**: $80/month (100%)
**Effort**: 30 minutes
**Risk**: Low (verify not needed)
**Action**: 
1. Identify unattached disks: `az disk list --query "[?diskState=='Unattached']"`
2. Verify with team (ensure not needed)
3. Delete: `az disk delete --ids <disk-id>`

#### Opportunity #2: Stop Unused Dev/Test VMs After Hours
**Current Cost**: $500/month (VM running 24/7)
**Savings**: $300/month (60%)
**Effort**: 2 hours (automation script)
**Risk**: Low (dev environment)
**Action**: Auto-shutdown policy: 7 PM - 7 AM weekdays, all day weekends

---

### Priority 2: Right-Sizing (< 1 week effort)

#### Opportunity #3: Downsize App Service Plan
**Current**: P2v3 (2 cores, 8GB RAM) - Avg CPU: 20%, RAM: 35%
**Current Cost**: $292/month
**Recommended**: P1v3 (2 cores, 4GB RAM)
**Optimized Cost**: $146/month
**Savings**: $146/month (50%)
**Effort**: 4 hours (testing + validation)
**Risk**: Medium (test performance after change)
**Action**:
1. Validate scaling limits in lower SKU
2. Scale down during low-traffic window
3. Monitor performance for 48 hours
4. Rollback if issues detected

#### Opportunity #4: SQL Database DTU Optimization
**Current**: S3 (100 DTU) - Avg DTU: 35%
**Current Cost**: $300/month
**Recommended**: S1 (20 DTU) with auto-scaling to S2
**Optimized Cost**: $120/month (avg)
**Savings**: $180/month (60%)
**Effort**: 1 day (testing + validation)
**Risk**: Medium (requires performance testing)

---

### Priority 3: Commitment Savings (< 1 hour setup)

#### Opportunity #5: Reserved Instances for Production VMs
**Current**: 2x Standard_D4s_v3 VMs (pay-as-you-go)
**Current Cost**: $280/month per VM = $560/month
**Recommended**: 1-year reserved instance
**Optimized Cost**: $392/month (2 VMs)
**Savings**: $168/month (30%)
**Effort**: 30 minutes (purchase reservation)
**Risk**: Low (production VMs run continuously)
**Commitment**: 1 year

#### Opportunity #6: Azure SQL Reserved Capacity
**Current**: Pay-as-you-go
**Current Cost**: $300/month
**Recommended**: 1-year reserved capacity
**Optimized Cost**: $210/month
**Savings**: $90/month (30%)
**Effort**: 15 minutes
**Commitment**: 1 year

---

### Priority 4: Architecture Optimization (> 1 week)

#### Opportunity #7: Migrate to Serverless Cosmos DB
**Current**: Provisioned 1000 RU/s (24/7)
**Current Cost**: $58/month
**Recommended**: Serverless (pay-per-request)
**Optimized Cost**: $20/month (estimated based on usage patterns)
**Savings**: $38/month (65%)
**Effort**: 1 week (code changes + testing)
**Risk**: Medium (requires application changes)

#### Opportunity #8: Implement Storage Lifecycle Policies
**Current**: 2TB in Hot tier
**Current Cost**: $40/month
**Recommended**: Hot (30 days) → Cool (90 days) → Archive
**Optimized Cost**: $22/month
**Savings**: $18/month (45%)
**Effort**: 4 hours (policy setup)
**Risk**: Low (automated)

---

## Implementation Roadmap

### Month 1: Quick Wins
- Delete unattached disks [$80/month]
- Configure auto-shutdown for dev VMs [$300/month]
- **Month 1 Savings**: $380

### Month 2: Right-Sizing
- Downsize App Service Plan [$146/month]
- Optimize SQL Database DTU [$180/month]
- **Month 2 Savings**: $326

### Month 3: Commitment Savings
- Purchase VM Reserved Instances [$168/month]
- Purchase SQL Reserved Capacity [$90/month]
- **Month 3 Savings**: $258

### Months 4-6: Architecture Changes
- Migrate to Serverless Cosmos DB [$38/month]
- Implement Storage Lifecycle [$18/month]
- **Months 4-6 Savings**: $56

---

## Total Savings Summary

| Timeframe | Cumulative Monthly Savings | Annual Savings |
|-----------|---------------------------|----------------|
| Month 1 | $380 | $4,560 |
| Month 2 | $706 | $8,472 |
| Month 3 | $964 | $11,568 |
| Months 4-6 | $1,020/month | $12,240 |

**Final Optimized Cost**: $1,680/month (from $2,700)
**Total Annual Savings**: $12,240 (38% reduction)

---

## Cost Governance Recommendations

### 1. Set Up Budgets & Alerts
- Monthly budget: $1,800 (10% buffer)
- Alert at 50%, 80%, 90%, 100%
- Auto-notification to team leads

### 2. Tag Resources for Cost Allocation
```
Environment: Production | Staging | Development
CostCenter: IT-12345
Project: ProjectName
Owner: teamname@company.com
```

### 3. Regular Reviews
- Weekly: Review anomalies (via Cost Management)
- Monthly: Cost optimization review
- Quarterly: Reserved instance optimization

### 4. Enable Azure Advisor Recommendations
- Automatically flags optimization opportunities
- Cost, security, reliability, performance recommendations

---

## Conclusion
[Summary with total savings, timeline, and priorities]
```

## Cost Optimization Best Practices

**Start with Quick Wins**: Delete unused resources first
**Monitor Before Changing**: 30-day metrics for right-sizing decisions
**Test Performance**: Validate after SKU changes
**Use Automation**: Auto-shutdown, lifecycle policies, auto-scaling
**Set Budgets**: Prevent surprise bills
**Tag Everything**: Enable cost allocation and tracking
**Review Regularly**: Monthly cost reviews catch drift
**Document Decisions**: Why resources are sized as they are

**Avoid**: Blind right-sizing, skipping performance validation, ignoring monitoring, missing reservations
