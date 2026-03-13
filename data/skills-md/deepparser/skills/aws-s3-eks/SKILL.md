---
name: aws-s3-eks
description: "Create and manage Amazon S3 buckets with EKS Pod Identity authentication. Use when: (1) Creating S3 buckets for any service running on EKS, (2) Setting up EKS Pod Identity so pods can access S3 without static credentials, (3) Configuring IAM roles/policies for S3 access, (4) Connecting Kubernetes services to S3 storage on EKS, (5) Troubleshooting S3 access from Kubernetes pods. Requires: aws CLI v2, kubectl, eksctl."
---

# AWS S3 + EKS Pod Identity

Provision S3 buckets and configure EKS Pod Identity so services running on EKS can access S3 without static AWS credentials.

## Prerequisites

Verify tools are installed before proceeding:

```bash
aws --version        # AWS CLI v2
kubectl version      # kubectl
eksctl version       # eksctl (for pod identity association)
```

## Quick Start

For a complete setup (bucket + IAM role + pod identity), run the bundled script:

```bash
scripts/create-s3-bucket.sh \
  --bucket my-app-uploads \
  --region us-east-1 \
  --cluster my-cluster \
  --namespace my-app \
  --service-account my-app-api
```

This single command:
1. Creates the S3 bucket with encryption + versioning
2. Creates an IAM role with a trust policy for `pods.eks.amazonaws.com`
3. Attaches an S3 access policy to the role
4. Creates/annotates the Kubernetes ServiceAccount
5. Creates the EKS Pod Identity Association

## Workflow

### Step 1: Create S3 Bucket

```bash
scripts/create-s3-bucket.sh \
  --bucket <BUCKET_NAME> \
  --region <REGION>
```

Pass `--bucket-only` to skip IAM/pod identity setup.

Options:
- `--versioning` — Enable versioning (default: enabled)
- `--lifecycle-days N` — Add lifecycle rule to expire objects after N days
- `--public-read` — Apply a public-read policy (for serving file URLs directly)
- `--cors-origins "https://example.com"` — Configure CORS allowed origins

### Step 2: Set Up EKS Pod Identity

```bash
scripts/setup-pod-identity.sh \
  --cluster <CLUSTER_NAME> \
  --namespace <NAMESPACE> \
  --service-account <SA_NAME> \
  --bucket <BUCKET_NAME> \
  --region <REGION>
```

Options:
- `--role-name` — Custom IAM role name (default: `<cluster>-<namespace>-<sa>-s3-role`)
- `--read-only` — Grant only s3:GetObject/s3:ListBucket (no write)
- `--prefix "uploads/"` — Restrict access to a key prefix

### Step 3: Verify Access

After pod identity is configured, verify from within a pod:

```bash
kubectl run s3-test --rm -it \
  --image=amazon/aws-cli \
  --serviceaccount=<SA_NAME> \
  --namespace=<NAMESPACE> \
  -- s3 ls s3://<BUCKET_NAME>/
```

If it lists objects (or shows empty), pod identity is working. The AWS SDK credential chain automatically picks up the injected `AWS_CONTAINER_CREDENTIALS_FULL_URI` env var.

### Step 4: Configure Your Service

Set the bucket name and region in your application's environment variables:

```yaml
S3_BUCKET: "my-app-uploads"
S3_REGION: "us-east-1"
# No access key / secret key needed — Pod Identity handles credentials
```

The AWS SDK default credential chain (boto3, aioboto3, aws-sdk-js, etc.) picks up credentials automatically via the injected `AWS_CONTAINER_CREDENTIALS_FULL_URI` env var.

## How EKS Pod Identity Works

Unlike IRSA (which requires an OIDC provider), Pod Identity uses the EKS Pod Identity Agent DaemonSet:

1. IAM role trusts `pods.eks.amazonaws.com` service principal
2. `CreatePodIdentityAssociation` links the role to a K8s ServiceAccount
3. Pod Identity Agent (link-local `169.254.170.23:80`) injects STS credentials
4. AWS SDKs detect `AWS_CONTAINER_CREDENTIALS_FULL_URI` and use those credentials

No OIDC provider, no annotation-based IRSA. Works on EKS 1.24+.

## Reference Files

- **IAM policies**: See [references/iam-policies.md](references/iam-policies.md) for full IAM policy JSON templates (read-only, read-write, prefix-scoped)
- **K8s manifests**: See [references/k8s-manifests.md](references/k8s-manifests.md) for ServiceAccount, Deployment patches, and ConfigMap examples
- **S3 API spec**: See [references/openapi.yaml](references/openapi.yaml) for the full S3 OpenAPI 3.2.0 spec

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `NoCredentialProviders` | Pod Identity Agent not installed | `eksctl create addon --name eks-pod-identity-agent --cluster <cluster>` |
| `AccessDenied` on S3 call | IAM policy missing or wrong bucket | Check `aws iam get-role-policy` and verify bucket ARN |
| `403 Forbidden` | Pod Identity Association not created | `aws eks list-pod-identity-associations --cluster <cluster>` |
| Credentials work in test pod but not app | ServiceAccount name mismatch | Verify `spec.serviceAccountName` in Deployment matches the association |
| `ExpiredTokenException` | Stale cached credentials | Restart the pod — agent injects fresh credentials on start |
