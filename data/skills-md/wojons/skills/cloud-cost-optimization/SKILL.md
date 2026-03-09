---
name: cloud-cost-optimization
description: Use when you need to analyze and optimize cloud costs across multiple cloud providers (AWS, Azure, GCP)
license: MIT
compatibility: opencode
metadata:
  audience: devops, finops, engineers
  category: cloud
---

# Cloud Cost Optimization

Analyze and optimize cloud costs across multiple cloud providers including AWS, Azure, and Google Cloud Platform. This skill helps identify cost savings opportunities, optimize resource utilization, and implement cost management best practices.

## When to use me

Use this skill when:
- Your cloud costs are increasing unexpectedly
- You need to identify cost savings opportunities
- You're planning cloud migration or consolidation
- You want to optimize resource utilization
- You need to implement cost allocation and showback/chargeback
- You're preparing for budget planning or forecasting
- You need to compare costs across multiple cloud providers
- You want to implement FinOps practices and cloud financial management

## What I do

- **Multi-cloud cost analysis**: Analyze costs across AWS, Azure, GCP, and other cloud providers
- **Cost allocation and tagging**: Analyze resource tagging and cost allocation
- **Resource optimization**: Identify underutilized resources (idle instances, oversized resources)
- **Reserved instance analysis**: Analyze reserved instance purchases and savings plans
- **Storage optimization**: Identify unused storage, optimize storage classes
- **Network cost optimization**: Analyze data transfer costs and optimize network architecture
- **Database optimization**: Optimize database costs (instance sizing, storage, licensing)
- **Cost forecasting**: Forecast future costs based on usage patterns
- **Budget monitoring**: Monitor costs against budgets and set up alerts
- **FinOps practices**: Implement FinOps principles and cloud financial management

## Examples

```bash
# Analyze AWS costs
./scripts/analyze-cloud-costs.sh --provider aws --period monthly

# Compare costs across multiple providers
./scripts/analyze-cloud-costs.sh --multi-cloud --period quarterly

# Identify cost savings opportunities
./scripts/analyze-cloud-costs.sh --optimization --threshold 20

# Generate cost optimization report
./scripts/analyze-cloud-costs.sh --report --output cost-report.pdf

# Monitor costs against budget
./scripts/analyze-cloud-costs.sh --budget-monitoring --budget 10000
```

## Output format

```
Cloud Cost Optimization Analysis
─────────────────────────────────────
Analysis Period: January 2025
Total Cloud Spend: $47,850.25
Potential Savings Identified: $12,450.75 (26%)

COST BREAKDOWN BY PROVIDER:
───────────────────────────
AWS: $28,450.50 (59%)
  • EC2 Instances: $14,200.75 (50%)
  • S3 Storage: $3,850.25 (14%)
  • RDS Databases: $5,400.50 (19%)
  • Data Transfer: $2,150.75 (8%)
  • Other Services: $2,848.25 (10%)

Azure: $12,850.75 (27%)
  • Virtual Machines: $6,425.38 (50%)
  • Blob Storage: $1,542.09 (12%)
  • SQL Database: $3,085.18 (24%)
  • Bandwidth: $1,028.06 (8%)
  • Other Services: $770.04 (6%)

GCP: $6,549.00 (14%)
  • Compute Engine: $3,274.50 (50%)
  • Cloud Storage: $982.35 (15%)
  • Cloud SQL: $1,309.80 (20%)
  • Network Egress: $654.90 (10%)
  • Other Services: $327.45 (5%)

COST SAVINGS OPPORTUNITIES:
───────────────────────────
🔍 HIGH IMPACT SAVINGS (Estimated: $8,250.50):
   • 42 idle EC2 instances (running <10% CPU): $3,150.75
   • Oversized RDS instances (80% memory unused): $2,100.25
   • Unused EBS volumes (1.2TB): $1,250.50
   • S3 storage not transitioned to Glacier: $1,749.00

🔍 MEDIUM IMPACT SAVINGS (Estimated: $3,450.25):
   • Reserved Instance optimization: $1,850.75
   • Storage class optimization: $850.25
   • Network cost optimization (cross-AZ traffic): $749.25

🔍 LOW IMPACT SAVINGS (Estimated: $750.00):
   • Unused Elastic IP addresses: $250.00
   • Old snapshots not deleted: $350.00
   • Unused load balancers: $150.00

RESOURCE UTILIZATION ANALYSIS:
──────────────────────────────
• CPU Utilization: Average 24% (48% of instances below 20%)
• Memory Utilization: Average 32% (42% of instances below 25%)
• Storage Utilization: Average 45% (38% of volumes below 20%)
• Network Utilization: Average 18% (low optimization potential)

RESERVED INSTANCE ANALYSIS:
───────────────────────────
• AWS Reserved Instances: 65% coverage, 22% unused reservations
• Azure Reserved VM Instances: 58% coverage, 18% unused reservations
• GCP Committed Use Discounts: 42% coverage, 12% unused commitments
• Potential additional savings with better RI planning: $2,850.75

STORAGE OPTIMIZATION:
─────────────────────
• S3 Standard storage with infrequent access pattern: 2.8TB
• Unused EBS snapshots older than 90 days: 450
• Azure Blob hot tier with cold access pattern: 1.5TB
• GCP Cloud Standard storage with nearline pattern: 850GB
• Potential storage savings: $1,450.25

DATABASE OPTIMIZATION:
──────────────────────
• Over-provisioned RDS instances: 18 instances
• Unused Azure SQL databases: 7 instances
• GCP Cloud SQL with low utilization: 12 instances
• Database licensing optimization: Potential $2,150.75 savings

NETWORK COST ANALYSIS:
──────────────────────
• Cross-AZ data transfer costs: $1,250.75/month
• Internet egress costs: $850.25/month
• Inter-region transfer costs: $450.50/month
• CDN optimization potential: $350.25/month savings

COST FORECASTING:
─────────────────
• Current monthly run rate: $47,850.25
• Forecast next month: $49,250.75 (+2.9%)
• Forecast next quarter: $145,850.50 (+2.1% monthly growth)
• Forecast next year: $585,450.25 (assuming 2% monthly growth)

RECOMMENDATIONS:
────────────────
1. IMMEDIATE ACTION (1-7 days):
   • Terminate 42 idle EC2 instances: Save $3,150.75/month
   • Right-size 18 over-provisioned RDS instances: Save $2,100.25/month
   • Delete unused EBS volumes: Save $1,250.50/month

2. SHORT TERM (1-4 weeks):
   • Optimize Reserved Instance purchases: Save $1,850.75/month
   • Implement S3 lifecycle policies: Save $1,749.00/month
   • Optimize storage classes: Save $850.25/month

3. MEDIUM TERM (1-3 months):
   • Implement auto-scaling policies
   • Deploy cost monitoring and alerting
   • Establish FinOps practices and cost accountability

4. LONG TERM (3-12 months):
   • Multi-cloud cost optimization strategy
   • Architecture review for cost efficiency
   • Cost-aware development practices

IMPLEMENTATION PLAN:
────────────────────
• Week 1-2: Identify and terminate idle resources
• Week 3-4: Implement storage optimization
• Month 2: Optimize database resources
• Month 3: Implement cost monitoring and alerting
• Ongoing: Regular cost optimization reviews
```

## Notes

- Cloud cost optimization is an ongoing process, not a one-time activity
- Consider performance and availability requirements when optimizing costs
- Implement tagging for accurate cost allocation and showback/chargeback
- Use cloud provider cost management tools (AWS Cost Explorer, Azure Cost Management, GCP Billing)
- Consider third-party cloud cost management tools for multi-cloud environments
- Establish FinOps practices for cloud financial management
- Monitor cost optimization impact on performance and reliability
- Regular cost reviews help maintain cost efficiency over time