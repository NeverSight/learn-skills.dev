---
name: eks-cluster
description: "Create and manage Amazon EKS clusters, managed node groups, and EC2 instances. Use when: (1) Provisioning a new EKS cluster from scratch, (2) Adding or modifying managed node groups, (3) Choosing EC2 instance types for workloads, (4) Installing EKS addons (CoreDNS, kube-proxy, VPC CNI, EBS CSI, Pod Identity Agent), (5) Setting up VPC networking for EKS, (6) Configuring cluster autoscaling with Karpenter or Cluster Autoscaler, (7) Deploying services to EKS, (8) Troubleshooting EKS node or cluster issues. Requires: aws CLI v2, eksctl, kubectl."
---

# EKS Cluster + Node Group + EC2 Setup

Provision EKS clusters with managed node groups for running services on AWS.

## Prerequisites

```bash
aws --version        # AWS CLI v2
eksctl version       # eksctl 0.175+
kubectl version      # kubectl
```

Ensure your AWS credentials have permissions for EKS, EC2, VPC, IAM, and CloudFormation.

## Quick Start

Create a production-ready cluster with a single command:

```bash
scripts/create-eks-cluster.sh \
  --name my-cluster \
  --region us-east-1 \
  --version 1.31 \
  --node-type m6i.xlarge \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 8
```

This creates:
1. VPC with public + private subnets across 3 AZs
2. EKS cluster with specified Kubernetes version
3. Managed node group with autoscaling
4. Essential addons (VPC CNI, CoreDNS, kube-proxy, EBS CSI, Pod Identity Agent)
5. NGINX Ingress Controller

## Workflow

### Step 1: Create EKS Cluster

For a new cluster with default VPC:

```bash
scripts/create-eks-cluster.sh \
  --name <CLUSTER_NAME> \
  --region <REGION> \
  --version <K8S_VERSION>
```

Options:
- `--version` — Kubernetes version (default: 1.31)
- `--vpc-cidr` — VPC CIDR block (default: 10.0.0.0/16)
- `--node-type` — EC2 instance type (default: m6i.xlarge)
- `--nodes` — Desired node count (default: 3)
- `--nodes-min` — Minimum nodes for autoscaling (default: 2)
- `--nodes-max` — Maximum nodes for autoscaling (default: 8)
- `--node-volume-size` — EBS volume size in GB (default: 80)
- `--ssh-key` — EC2 key pair name for SSH access
- `--existing-vpc` — Use an existing VPC ID instead of creating a new one
- `--private-subnets` — Comma-separated private subnet IDs (with --existing-vpc)
- `--public-subnets` — Comma-separated public subnet IDs (with --existing-vpc)
- `--spot` — Use Spot instances for the node group
- `--dry-run` — Generate eksctl config without creating resources

For an eksctl config file approach (more control):

```bash
scripts/create-eks-cluster.sh --name my-cluster --config-only
# Generates eksctl-config.yaml — edit it, then:
eksctl create cluster -f eksctl-config.yaml
```

### Step 2: Add Node Groups

Add specialized node groups for different workload types:

```bash
# General workloads
scripts/create-node-group.sh \
  --cluster my-cluster \
  --name general \
  --type m6i.xlarge \
  --nodes 3

# GPU / ML workloads
scripts/create-node-group.sh \
  --cluster my-cluster \
  --name gpu \
  --type g5.xlarge \
  --nodes 1 \
  --nodes-max 4 \
  --taint "nvidia.com/gpu=true:NoSchedule" \
  --label workload-type=gpu

# Spot instances for batch / non-critical workloads
scripts/create-node-group.sh \
  --cluster my-cluster \
  --name spot-workers \
  --type m6i.xlarge,m5.xlarge,m5a.xlarge \
  --spot \
  --nodes 2 \
  --nodes-max 10 \
  --label workload-type=spot
```

Options:
- `--type` — Instance type(s), comma-separated for mixed (default: m6i.xlarge)
- `--nodes` / `--nodes-min` / `--nodes-max` — Autoscaling range
- `--spot` — Use Spot instances
- `--taint` — Apply taint (key=value:effect)
- `--label` — Apply label (key=value), repeatable
- `--volume-size` — EBS volume in GB (default: 80)
- `--ami-family` — AMI family: AmazonLinux2023, Bottlerocket (default: AmazonLinux2023)
- `--ssh-key` — EC2 key pair for SSH access

### Step 3: Install Addons

The cluster script installs essential addons automatically. To manage them separately:

```bash
# Pod Identity Agent (required for aws-s3-eks skill)
eksctl create addon --cluster my-cluster --name eks-pod-identity-agent

# EBS CSI Driver (for PersistentVolumeClaims)
eksctl create addon --cluster my-cluster --name aws-ebs-csi-driver \
  --service-account-role-arn arn:aws:iam::ACCOUNT:role/ebs-csi-role

# EFS CSI Driver (for ReadWriteMany PVCs)
eksctl create addon --cluster my-cluster --name aws-efs-csi-driver

# AWS Load Balancer Controller (alternative to NGINX Ingress)
eksctl create addon --cluster my-cluster --name aws-load-balancer-controller
```

See [references/addons.md](references/addons.md) for full addon details and IAM role setup.

### Step 4: Deploy Your Services

After the cluster is ready, deploy your services:

```bash
# Create a namespace
kubectl create namespace my-app

# Deploy via manifests
kubectl apply -f k8s/

# Deploy via Helm
helm upgrade --install my-app ./helm/ -n my-app --create-namespace
```

### Step 5: Verify

```bash
# Cluster health
kubectl get nodes -o wide
kubectl get pods -A

# Service endpoints
kubectl get ingress -A
kubectl get svc -A
```

## Workload → Instance Type Mapping

| Workload Profile | Recommended Instance | Min Nodes |
|-----------------|---------------------|-----------|
| Low CPU, low memory (auth, proxies) | t3.medium or m6i.large | 1 |
| Medium CPU, medium memory (APIs, agents) | m6i.xlarge | 2 |
| High CPU, medium memory (request routing) | c6i.xlarge or m6i.xlarge | 2 |
| Memory-optimized (databases, caches) | r6i.xlarge | 2 |
| GPU inference | g5.xlarge / g5.2xlarge | 1 |

See [references/ec2-instance-types.md](references/ec2-instance-types.md) for detailed sizing guidance.

## Reference Files

- **eksctl configs**: See [references/eksctl-configs.md](references/eksctl-configs.md) for full ClusterConfig YAML templates (dev, staging, production)
- **Instance types**: See [references/ec2-instance-types.md](references/ec2-instance-types.md) for EC2 sizing by workload with pricing
- **Addons**: See [references/addons.md](references/addons.md) for EKS addon installation, IAM roles, and configuration

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `eksctl create cluster` hangs | CloudFormation stack stuck | Check AWS Console > CloudFormation for failed events |
| Nodes `NotReady` | VPC CNI or kubelet issue | `kubectl describe node <name>` — check conditions |
| Pods `Pending` | No capacity / taint mismatch | `kubectl describe pod <name>` — check Events |
| `CreateContainerConfigError` | Missing ConfigMap/Secret | Verify configmaps and secrets exist in the namespace |
| `ImagePullBackOff` | ECR auth or image not found | Check `aws ecr get-login-password` and image URI |
| Node group create fails | Instance type unavailable in AZ | Try different AZs or instance types |
| `InsufficientFreeAddressesInSubnet` | VPC subnet exhausted | Check subnet CIDR size or use `--vpc-cidr` with larger range |
