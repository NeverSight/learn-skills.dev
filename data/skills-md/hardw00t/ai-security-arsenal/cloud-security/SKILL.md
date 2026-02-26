---
name: cloud-security
description: "Multi-cloud security assessment skill for AWS, Azure, and GCP. This skill should be used when performing cloud security audits, scanning for misconfigurations, testing IAM policies, auditing storage permissions, and identifying privilege escalation paths. Triggers on requests to audit cloud security, scan AWS/Azure/GCP, check cloud misconfigurations, or perform cloud penetration testing."
---

# Cloud Security Assessment

This skill enables comprehensive security testing of AWS, Azure, and GCP cloud environments using industry-standard tools like ScoutSuite, Prowler, and CloudSploit. It covers misconfiguration scanning, IAM analysis, and privilege escalation testing.

## When to Use This Skill

This skill should be invoked when:
- Performing cloud security assessments
- Scanning for cloud misconfigurations
- Auditing IAM policies and permissions
- Testing storage bucket/blob permissions
- Identifying privilege escalation paths
- Checking CIS benchmark compliance
- Reviewing cloud security posture

### Trigger Phrases
- "audit AWS security"
- "scan Azure for misconfigurations"
- "check GCP security"
- "test cloud IAM"
- "find S3 bucket issues"
- "cloud penetration test"
- "CIS benchmark audit"

---

## Prerequisites

### Required Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| ScoutSuite | Multi-cloud security auditing | `pip install scoutsuite` |
| Prowler | AWS security assessment | `pip install prowler` |
| CloudSploit | Cloud security scanning | `npm install -g cloudsploit` |
| Steampipe | SQL for cloud APIs | steampipe.io download |
| Pacu | AWS exploitation framework | `pip install pacu` |
| enumerate-iam | IAM enumeration | GitHub |
| S3Scanner | S3 bucket scanner | `pip install s3scanner` |

### Authentication Setup

#### AWS
```bash
# Configure AWS CLI
aws configure
# Or use environment variables
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-east-1"

# Assume role for cross-account
aws sts assume-role --role-arn arn:aws:iam::ACCOUNT:role/ROLE --role-session-name audit
```

#### Azure
```bash
# Login with CLI
az login

# Service Principal
az login --service-principal -u CLIENT_ID -p SECRET --tenant TENANT_ID

# Set subscription
az account set --subscription "SUBSCRIPTION_ID"
```

#### GCP
```bash
# Application default credentials
gcloud auth application-default login

# Service account
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Set project
gcloud config set project PROJECT_ID
```

---

## Multi-Cloud Security Scanning

### ScoutSuite (All Clouds)

```bash
# AWS Assessment
scout aws --profile default --report-dir ./scout-aws

# Azure Assessment
scout azure --cli --report-dir ./scout-azure

# GCP Assessment
scout gcp --project-id PROJECT_ID --report-dir ./scout-gcp

# Key findings to review:
# - Danger (red): Critical misconfigurations
# - Warning (orange): High-risk issues
# - Info: Informational findings
```

### Quick Start Workflow

```markdown
1. **Credentials Setup**
   - Obtain read-only access credentials
   - Verify minimum required permissions

2. **Initial Scan**
   - Run ScoutSuite for comprehensive view
   - Run Prowler/CloudSploit for specific checks

3. **Deep Dive**
   - IAM policy analysis
   - Storage permissions review
   - Network security assessment
   - Logging/monitoring verification

4. **Exploitation Testing** (if authorized)
   - Privilege escalation attempts
   - Lateral movement testing
   - Data exfiltration simulation

5. **Reporting**
   - Document findings with evidence
   - Prioritize by risk and impact
   - Provide remediation guidance
```

---

## AWS Security Testing

### Prowler Assessment

```bash
# Full assessment
prowler aws

# Specific checks
prowler aws --checks check11,check12,check13

# CIS Benchmark
prowler aws --compliance cis_2.0_aws

# Output formats
prowler aws -M csv,html,json

# Check categories
prowler aws -g group1  # IAM
prowler aws -g group2  # Logging
prowler aws -g group3  # Monitoring
prowler aws -g group4  # Networking
```

### IAM Analysis

```bash
# Enumerate IAM permissions
enumerate-iam --access-key AKIA... --secret-key ...

# Check for privilege escalation
# Using Pacu
pacu
> import_keys --access-key AKIA... --secret-key ...
> run iam__enum_permissions
> run iam__privesc_scan

# Manual checks
aws iam list-users
aws iam list-roles
aws iam list-policies --scope Local
aws iam get-account-authorization-details
```

### S3 Security

```bash
# Scan for public buckets
s3scanner --bucket-file buckets.txt

# Check bucket policies
aws s3api get-bucket-policy --bucket BUCKET
aws s3api get-bucket-acl --bucket BUCKET
aws s3api get-public-access-block --bucket BUCKET

# Test bucket permissions
aws s3 ls s3://bucket-name --no-sign-request
aws s3 cp test.txt s3://bucket-name --no-sign-request
```

### Common AWS Misconfigurations

```markdown
### Critical
- [ ] Public S3 buckets with sensitive data
- [ ] IAM users with admin access
- [ ] Root account used for daily operations
- [ ] No MFA on root or privileged accounts
- [ ] Hardcoded credentials in Lambda/EC2

### High
- [ ] Security groups with 0.0.0.0/0 ingress
- [ ] RDS instances publicly accessible
- [ ] CloudTrail not enabled
- [ ] Default VPC in use
- [ ] IAM policies with * resources

### Medium
- [ ] S3 buckets without versioning
- [ ] EBS volumes unencrypted
- [ ] Access keys not rotated
- [ ] VPC flow logs disabled
- [ ] GuardDuty not enabled
```

### AWS Privilege Escalation

```markdown
## Common Paths

1. **iam:CreatePolicyVersion**
   - Create new policy version with admin access
   - aws iam create-policy-version --policy-arn ARN --policy-document file://admin.json --set-as-default

2. **iam:SetDefaultPolicyVersion**
   - Switch to overly permissive version

3. **iam:AttachUserPolicy/AttachRolePolicy**
   - Attach AdministratorAccess

4. **iam:CreateAccessKey**
   - Create keys for other users

5. **iam:PassRole + Lambda/EC2**
   - Create Lambda with powerful role
   - Launch EC2 with powerful role

6. **sts:AssumeRole**
   - Assume more privileged role

7. **lambda:UpdateFunctionCode**
   - Modify Lambda to exfiltrate credentials

## Detection
- CloudTrail logs
- IAM Access Analyzer
- GuardDuty findings
```

---

## Azure Security Testing

### Azure Security Assessment

```bash
# Using ScoutSuite
scout azure --cli

# Azure native tools
az security assessment list
az security alert list

# Storage account checks
az storage account list
az storage account show --name ACCOUNT --query allowBlobPublicAccess
```

### Azure Misconfigurations

```markdown
### Critical
- [ ] Storage accounts with public access
- [ ] Key Vault access policies too permissive
- [ ] No MFA for privileged accounts
- [ ] Service Principal with Owner role
- [ ] Exposed management ports (RDP/SSH)

### High
- [ ] Network Security Groups too open
- [ ] Azure AD users with Global Admin
- [ ] Defender for Cloud disabled
- [ ] Diagnostic logs not configured
- [ ] Azure Policy not enforced

### Medium
- [ ] Managed disk encryption disabled
- [ ] Activity logs retention < 90 days
- [ ] Resource locks not applied
- [ ] Azure Bastion not used
- [ ] Just-in-time VM access disabled
```

### Azure AD / Entra ID Testing

```bash
# Using Azure CLI
az ad user list
az ad group list
az ad app list
az role assignment list

# Check privileged roles
az role assignment list --role "Owner"
az role assignment list --role "Contributor"
az role assignment list --role "User Access Administrator"

# Service Principal enumeration
az ad sp list --all
```

### Azure Privilege Escalation

```markdown
## Common Paths

1. **Automation Account RunAs**
   - Runbooks often have high privileges
   - Check for stored credentials

2. **Key Vault Access**
   - Extract secrets/certificates
   - Impersonate service principals

3. **Managed Identity Abuse**
   - IMDS endpoint token theft
   - curl http://169.254.169.254/metadata/identity/oauth2/token

4. **Resource Group Permissions**
   - Contributor can reset VM passwords
   - Can add new users to VMs

5. **Azure AD Roles**
   - Global Admin = full control
   - Application Admin can create apps with high privileges

6. **Subscription Permissions**
   - User Access Administrator can grant roles
```

---

## GCP Security Testing

### GCP Assessment

```bash
# Using ScoutSuite
scout gcp --project-id PROJECT_ID

# Using gcloud
gcloud projects get-iam-policy PROJECT_ID
gcloud compute instances list
gcloud storage buckets list
```

### GCP Misconfigurations

```markdown
### Critical
- [ ] Public Cloud Storage buckets
- [ ] Service accounts with Owner role
- [ ] Default service account in use
- [ ] Public GCE instances
- [ ] No organization policies

### High
- [ ] Firewall rules too permissive
- [ ] Cloud Logging disabled
- [ ] No VPC Service Controls
- [ ] Compute Engine default encryption
- [ ] IAM binding with allUsers

### Medium
- [ ] Uniform bucket access not enforced
- [ ] Cloud Armor not configured
- [ ] Binary Authorization disabled
- [ ] Container Registry public
- [ ] Access Transparency not enabled
```

### GCP IAM Analysis

```bash
# List IAM bindings
gcloud projects get-iam-policy PROJECT_ID --flatten="bindings[].members" \
  --format="table(bindings.role, bindings.members)"

# Service accounts
gcloud iam service-accounts list
gcloud iam service-accounts get-iam-policy SA_EMAIL

# Check for wide permissions
gcloud asset search-all-iam-policies --scope=projects/PROJECT_ID \
  --query="resource:*" --flatten="policy.bindings[].members"
```

### GCP Privilege Escalation

```markdown
## Common Paths

1. **Service Account Key Creation**
   - iam.serviceAccountKeys.create
   - Create key for privileged SA

2. **Service Account Impersonation**
   - iam.serviceAccounts.getAccessToken
   - Act as another service account

3. **Compute Instance Access**
   - SSH to instance with service account
   - Metadata token extraction

4. **Cloud Functions**
   - cloudfunctions.functions.update
   - Modify function code to exfil credentials

5. **GKE/Kubernetes**
   - Access workload identity
   - Container escape to node

6. **IAM Policy Modification**
   - resourcemanager.projects.setIamPolicy
   - Grant self Owner role

## Metadata Exploitation
curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
```

---

## Steampipe Queries

### Installation

```bash
# Install Steampipe
brew install turbot/tap/steampipe

# Install plugins
steampipe plugin install aws
steampipe plugin install azure
steampipe plugin install gcp
```

### Security Queries

```sql
-- AWS: Public S3 buckets
SELECT name, acl, policy
FROM aws_s3_bucket
WHERE bucket_policy_is_public = true;

-- AWS: Security groups with 0.0.0.0/0
SELECT group_id, group_name, ip_permissions
FROM aws_vpc_security_group_rule
WHERE cidr_ipv4 = '0.0.0.0/0';

-- AWS: IAM users without MFA
SELECT name, mfa_enabled
FROM aws_iam_user
WHERE mfa_enabled = false;

-- Azure: Storage accounts with public access
SELECT name, allow_blob_public_access
FROM azure_storage_account
WHERE allow_blob_public_access = true;

-- GCP: Service accounts with Owner
SELECT distinct member
FROM gcp_iam_policy_binding
WHERE role = 'roles/owner'
AND member LIKE 'serviceAccount:%';
```

---

## CIS Benchmark Compliance

### AWS CIS Checks

```bash
# Using Prowler for CIS
prowler aws --compliance cis_2.0_aws

# Key CIS controls:
# 1.x - Identity and Access Management
# 2.x - Storage
# 3.x - Logging
# 4.x - Monitoring
# 5.x - Networking
```

### Compliance Frameworks

| Framework | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| CIS Benchmark | v2.0 | v2.0 | v2.0 |
| SOC 2 | Prowler | Defender | SCC |
| PCI DSS | Config Rules | Policy | SCC |
| HIPAA | Config Rules | Policy | SCC |
| GDPR | Artifact | Compliance | SCC |

---

## Cloud Metadata Services

### SSRF to Cloud Credentials

```markdown
## AWS IMDS
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME
http://169.254.169.254/latest/user-data/

## Azure IMDS (requires header: Metadata: true)
http://169.254.169.254/metadata/instance?api-version=2021-02-01
http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/

## GCP (requires header: Metadata-Flavor: Google)
http://metadata.google.internal/computeMetadata/v1/
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

## Bypass techniques for SSRF filters
http://[::ffff:169.254.169.254]
http://169.254.169.254.nip.io
http://0xA9FEA9FE  # Decimal encoding
```

---

## Reporting Template

```markdown
# Cloud Security Assessment Report

## Executive Summary
- Cloud provider(s) assessed
- Assessment period
- Critical findings count
- Overall risk rating

## Scope
- Accounts/subscriptions/projects
- Services in scope
- Testing methodology

## Findings

### [CRITICAL] Finding Title

**Cloud**: AWS/Azure/GCP
**Service**: S3/IAM/Storage
**CIS Control**: 2.1.1

**Description**
Detailed description of the misconfiguration.

**Evidence**
- Screenshots
- CLI output
- Policy documents

**Impact**
- Data exposure risk
- Compliance violation
- Attack scenarios

**Remediation**
1. Immediate steps
2. Long-term fixes
3. Monitoring recommendations

**References**
- CIS Benchmark
- Cloud documentation
```

---

## Bundled Resources

### scripts/
- `aws_enum.py` - AWS enumeration automation
- `azure_enum.py` - Azure enumeration automation
- `gcp_enum.py` - GCP enumeration automation
- `cloud_privesc.py` - Privilege escalation checker
- `bucket_scanner.py` - Multi-cloud storage scanner

### references/
- `aws_security.md` - AWS security best practices
- `azure_security.md` - Azure security best practices
- `gcp_security.md` - GCP security best practices
- `cis_controls.md` - CIS benchmark mappings

### checklists/
- `aws_audit.md` - AWS security audit checklist
- `azure_audit.md` - Azure security audit checklist
- `gcp_audit.md` - GCP security audit checklist
