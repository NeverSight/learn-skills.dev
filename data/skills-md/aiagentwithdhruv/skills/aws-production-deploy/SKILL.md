---
name: aws-production-deploy
description: Deploy any full-stack app (Next.js + FastAPI or similar) to AWS production with Docker, ECR, ECS Fargate, ALB, ElastiCache, CloudWatch, and Grafana. Use when deploying to AWS, setting up CI/CD, configuring production infrastructure, or shipping any app to production.
---

# AWS Production Deployment Stack

## Goal
Ship any full-stack application to production on AWS with proper CI/CD, monitoring, caching, and load balancing. Zero manual deployments after setup.

---

## When to Use This Skill

- Deploying Next.js + FastAPI (or any frontend + backend) to production
- Setting up Docker → ECR → ECS Fargate pipeline
- Configuring GitHub Actions CI/CD for AWS
- Adding CloudWatch logging + Grafana dashboards
- Setting up ElastiCache (Redis) for caching/sessions
- Configuring Application Load Balancer with SSL
- ANY project that needs production-grade AWS hosting

---

## Architecture Pattern

```
git push → GitHub Actions → Docker Build → ECR Push → ECS Fargate Deploy
                                                          ↓
                                              ALB (HTTPS + SSL)
                                                          ↓
                                              ECS Tasks (Containers)
                                                ↓         ↓         ↓
                                           Database   ElastiCache  CloudWatch
                                                                      ↓
                                                                   Grafana
```

---

## Step-by-Step AWS CLI Setup

### Prerequisites
```bash
# Install AWS CLI (macOS)
brew install awscli

# Configure credentials
aws configure
# AWS Access Key ID: <from IAM>
# AWS Secret Access Key: <from IAM>
# Default region: ap-south-1 (or your region)
# Default output: json

# Verify
aws sts get-caller-identity
```

### Step 1: Create ECR Repositories
```bash
# Create repos for frontend and backend images
aws ecr create-repository --repository-name <app>-frontend --image-scanning-configuration scanOnPush=true
aws ecr create-repository --repository-name <app>-backend --image-scanning-configuration scanOnPush=true

# Login to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

### Step 2: Create VPC & Networking
```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=<app>-vpc}]'

# Create public subnets (for ALB) — need 2 AZs minimum
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.1.0/24 --availability-zone <region>a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=<app>-public-1}]'
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.2.0/24 --availability-zone <region>b --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=<app>-public-2}]'

# Create private subnets (for ECS + ElastiCache)
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.3.0/24 --availability-zone <region>a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=<app>-private-1}]'
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.4.0/24 --availability-zone <region>b --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=<app>-private-2}]'

# Create Internet Gateway (for ALB)
aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=<app>-igw}]'
aws ec2 attach-internet-gateway --internet-gateway-id <igw-id> --vpc-id <vpc-id>

# Create NAT Gateway (for ECS Fargate to pull images + reach internet)
aws ec2 allocate-address --domain vpc  # Get Elastic IP
aws ec2 create-nat-gateway --subnet-id <public-subnet-1-id> --allocation-id <eip-alloc-id>

# Route tables — public subnets → IGW, private subnets → NAT
aws ec2 create-route-table --vpc-id <vpc-id>  # Public RT
aws ec2 create-route --route-table-id <public-rt-id> --destination-cidr-block 0.0.0.0/0 --gateway-id <igw-id>
aws ec2 associate-route-table --route-table-id <public-rt-id> --subnet-id <public-subnet-1-id>
aws ec2 associate-route-table --route-table-id <public-rt-id> --subnet-id <public-subnet-2-id>

aws ec2 create-route-table --vpc-id <vpc-id>  # Private RT
aws ec2 create-route --route-table-id <private-rt-id> --destination-cidr-block 0.0.0.0/0 --nat-gateway-id <nat-gw-id>
aws ec2 associate-route-table --route-table-id <private-rt-id> --subnet-id <private-subnet-1-id>
aws ec2 associate-route-table --route-table-id <private-rt-id> --subnet-id <private-subnet-2-id>
```

### Step 3: Security Groups
```bash
# ALB security group — allow HTTPS from internet
aws ec2 create-security-group --group-name <app>-alb-sg --description "ALB SG" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <alb-sg-id> --protocol tcp --port 443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id <alb-sg-id> --protocol tcp --port 80 --cidr 0.0.0.0/0

# ECS security group — allow from ALB only
aws ec2 create-security-group --group-name <app>-ecs-sg --description "ECS SG" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <ecs-sg-id> --protocol tcp --port 3000 --source-group <alb-sg-id>
aws ec2 authorize-security-group-ingress --group-id <ecs-sg-id> --protocol tcp --port 8000 --source-group <alb-sg-id>

# ElastiCache security group — allow from ECS only
aws ec2 create-security-group --group-name <app>-redis-sg --description "Redis SG" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <redis-sg-id> --protocol tcp --port 6379 --source-group <ecs-sg-id>
```

### Step 4: ElastiCache (Redis)
```bash
# Create subnet group
aws elasticache create-cache-subnet-group \
  --cache-subnet-group-name <app>-redis-subnet \
  --cache-subnet-group-description "Redis subnets" \
  --subnet-ids <private-subnet-1-id> <private-subnet-2-id>

# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id <app>-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1 \
  --cache-subnet-group-name <app>-redis-subnet \
  --security-group-ids <redis-sg-id>
```

### Step 5: Application Load Balancer
```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name <app>-alb \
  --subnets <public-subnet-1-id> <public-subnet-2-id> \
  --security-groups <alb-sg-id> \
  --scheme internet-facing \
  --type application

# Create target groups
aws elbv2 create-target-group --name <app>-frontend-tg --protocol HTTP --port 3000 --vpc-id <vpc-id> --target-type ip --health-check-path /
aws elbv2 create-target-group --name <app>-backend-tg --protocol HTTP --port 8000 --vpc-id <vpc-id> --target-type ip --health-check-path /health

# SSL Certificate (via ACM)
aws acm request-certificate --domain-name <yourdomain.com> --validation-method DNS --subject-alternative-names "*.<yourdomain.com>"
# → Validate DNS via Route53 or your DNS provider

# HTTPS Listener with path-based routing
aws elbv2 create-listener \
  --load-balancer-arn <alb-arn> \
  --protocol HTTPS --port 443 \
  --certificates CertificateArn=<cert-arn> \
  --default-actions Type=forward,TargetGroupArn=<frontend-tg-arn>

# HTTP → HTTPS redirect
aws elbv2 create-listener \
  --load-balancer-arn <alb-arn> \
  --protocol HTTP --port 80 \
  --default-actions Type=redirect,RedirectConfig='{Protocol=HTTPS,Port=443,StatusCode=HTTP_301}'

# Route /api/* to backend
aws elbv2 create-rule \
  --listener-arn <https-listener-arn> \
  --conditions Field=path-pattern,Values='/api/*' \
  --priority 1 \
  --actions Type=forward,TargetGroupArn=<backend-tg-arn>
```

### Step 6: ECS Cluster + Task Definitions
```bash
# Create cluster
aws ecs create-cluster --cluster-name <app>-cluster

# Create CloudWatch log groups FIRST
aws logs create-log-group --log-group-name /ecs/<app>/frontend
aws logs create-log-group --log-group-name /ecs/<app>/backend

# Create ECS Task Execution Role (if not exists)
aws iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "ecs-tasks.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}'
aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

**Task Definition JSON** (`infra/task-definition.json`):
```json
{
  "family": "<app>",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::<account>:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::<account>:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "frontend",
      "image": "<account>.dkr.ecr.<region>.amazonaws.com/<app>-frontend:latest",
      "portMappings": [{"containerPort": 3000, "protocol": "tcp"}],
      "environment": [
        {"name": "NEXT_PUBLIC_API_URL", "value": "https://<domain>/api"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/<app>/frontend",
          "awslogs-region": "<region>",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "essential": true
    },
    {
      "name": "backend",
      "image": "<account>.dkr.ecr.<region>.amazonaws.com/<app>-backend:latest",
      "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
      "environment": [
        {"name": "MONGODB_URI", "value": "<mongodb-atlas-uri>"},
        {"name": "REDIS_URL", "value": "redis://<elasticache-endpoint>:6379"},
        {"name": "OPENAI_API_KEY", "value": "<key>"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/<app>/backend",
          "awslogs-region": "<region>",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "essential": true
    }
  ]
}
```

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://infra/task-definition.json

# Create ECS service
aws ecs create-service \
  --cluster <app>-cluster \
  --service-name <app>-service \
  --task-definition <app> \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[<private-subnet-1>,<private-subnet-2>],securityGroups=[<ecs-sg-id>],assignPublicIp=DISABLED}" \
  --load-balancers "targetGroupArn=<frontend-tg-arn>,containerName=frontend,containerPort=3000" "targetGroupArn=<backend-tg-arn>,containerName=backend,containerPort=8000"
```

### Step 7: GitHub Actions CI/CD

`.github/workflows/deploy.yml`:
```yaml
name: Deploy to AWS ECS

on:
  push:
    branches: [main]

env:
  AWS_REGION: ap-south-1
  ECR_FRONTEND: <app>-frontend
  ECR_BACKEND: <app>-backend
  ECS_CLUSTER: <app>-cluster
  ECS_SERVICE: <app>-service
  TASK_DEFINITION: <app>

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to ECR
        id: ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build & push frontend
        run: |
          docker build -t ${{ steps.ecr.outputs.registry }}/${{ env.ECR_FRONTEND }}:${{ github.sha }} -f frontend/Dockerfile frontend/
          docker push ${{ steps.ecr.outputs.registry }}/${{ env.ECR_FRONTEND }}:${{ github.sha }}

      - name: Build & push backend
        run: |
          docker build -t ${{ steps.ecr.outputs.registry }}/${{ env.ECR_BACKEND }}:${{ github.sha }} -f backend/Dockerfile backend/
          docker push ${{ steps.ecr.outputs.registry }}/${{ env.ECR_BACKEND }}:${{ github.sha }}

      - name: Download current task definition
        run: |
          aws ecs describe-task-definition --task-definition ${{ env.TASK_DEFINITION }} --query taskDefinition > task-def.json

      - name: Update frontend image in task def
        id: frontend-task
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: task-def.json
          container-name: frontend
          image: ${{ steps.ecr.outputs.registry }}/${{ env.ECR_FRONTEND }}:${{ github.sha }}

      - name: Update backend image in task def
        id: backend-task
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: ${{ steps.frontend-task.outputs.task-definition }}
          container-name: backend
          image: ${{ steps.ecr.outputs.registry }}/${{ env.ECR_BACKEND }}:${{ github.sha }}

      - name: Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ steps.backend-task.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
```

**GitHub Secrets needed:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### Step 8: CloudWatch Monitoring
```bash
# Create metric alarms
aws cloudwatch put-metric-alarm \
  --alarm-name <app>-high-cpu \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=ClusterName,Value=<app>-cluster Name=ServiceName,Value=<app>-service

aws cloudwatch put-metric-alarm \
  --alarm-name <app>-high-memory \
  --metric-name MemoryUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=ClusterName,Value=<app>-cluster Name=ServiceName,Value=<app>-service

# Create dashboard
aws cloudwatch put-dashboard --dashboard-name <app>-dashboard --dashboard-body '{
  "widgets": [
    {"type":"metric","properties":{"metrics":[["AWS/ECS","CPUUtilization","ClusterName","<app>-cluster","ServiceName","<app>-service"]],"period":300,"title":"CPU Utilization"}},
    {"type":"metric","properties":{"metrics":[["AWS/ECS","MemoryUtilization","ClusterName","<app>-cluster","ServiceName","<app>-service"]],"period":300,"title":"Memory Utilization"}},
    {"type":"metric","properties":{"metrics":[["AWS/ApplicationELB","RequestCount","LoadBalancer","<alb-id>"]],"period":60,"title":"Request Count"}},
    {"type":"metric","properties":{"metrics":[["AWS/ApplicationELB","TargetResponseTime","LoadBalancer","<alb-id>"]],"period":60,"title":"Response Time"}},
    {"type":"metric","properties":{"metrics":[["AWS/ApplicationELB","HTTPCode_Target_5XX_Count","LoadBalancer","<alb-id>"]],"period":60,"title":"5xx Errors"}}
  ]
}'
```

### Step 9: Grafana Setup
```bash
# Option A: Self-hosted Grafana on EC2
docker run -d -p 3000:3000 --name grafana grafana/grafana-oss

# Option B: Amazon Managed Grafana (recommended)
aws grafana create-workspace \
  --account-access-type CURRENT_ACCOUNT \
  --authentication-providers AWS_SSO \
  --permission-type SERVICE_MANAGED \
  --workspace-name <app>-grafana
```

**Grafana Dashboard Config:**
- Data Source: CloudWatch
- Panels: CPU, Memory, Request Count, Response Time, Error Rate, Active Tasks
- Alert rules: CPU > 80%, 5xx > 10/min, Response Time > 2s

---

## Dockerfiles

### Frontend Dockerfile
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### docker-compose.yml (Local Dev)
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on: [backend]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - MONGODB_URI=${MONGODB_URI}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on: [redis]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
```

---

## Things People Forget (Critical)

1. **NAT Gateway** — ECS Fargate in private subnet can't pull ECR images without NAT or VPC endpoint. Either add NAT Gateway ($32/month) or create ECR VPC endpoints (free but more setup).

2. **ECS Task Role vs Execution Role** — Execution Role = ECS agent pulls images + writes logs. Task Role = your application's AWS permissions (S3, SES, etc.). These are DIFFERENT.

3. **MongoDB Atlas Network Access** — Whitelist the NAT Gateway's Elastic IP in MongoDB Atlas, not 0.0.0.0/0.

4. **Health Checks** — ALB health check must return 200 on `/` (frontend) and `/health` (backend). If unhealthy, ECS keeps killing and restarting tasks.

5. **Secrets Management** — Never put secrets in task definition JSON. Use AWS Secrets Manager or SSM Parameter Store, reference them in task def with `valueFrom`.

6. **Container Insights** — Enable for ECS to get per-container metrics in CloudWatch:
   ```bash
   aws ecs update-cluster-settings --cluster <app>-cluster --settings name=containerInsights,value=enabled
   ```

7. **Auto-scaling** — Add after initial deploy:
   ```bash
   aws application-autoscaling register-scalable-target \
     --service-namespace ecs \
     --scalable-dimension ecs:service:DesiredCount \
     --resource-id service/<app>-cluster/<app>-service \
     --min-capacity 1 --max-capacity 10
   ```

8. **Cost Control** — Fargate pricing: 0.04048/vCPU/hr + 0.004445/GB/hr. A 0.5 vCPU + 1GB task = ~$30/month. 2 tasks = ~$60/month. NAT Gateway adds $32/month.

9. **Logs Retention** — Set retention on CloudWatch log groups or costs grow forever:
   ```bash
   aws logs put-retention-policy --log-group-name /ecs/<app>/backend --retention-in-days 30
   ```

10. **Rolling Deployments** — ECS default is rolling update. Set `minimumHealthyPercent=50` and `maximumPercent=200` to allow new tasks before killing old ones.

---

## Cost Estimate (ap-south-1)

| Service | Spec | Monthly Cost |
|---------|------|-------------|
| ECS Fargate (2 tasks) | 0.5 vCPU + 1GB each | ~$30-60 |
| NAT Gateway | Data processing | ~$32 + data |
| ALB | Hourly + LCU | ~$20-30 |
| ElastiCache | cache.t3.micro | ~$13 |
| CloudWatch | Logs + metrics | ~$5-15 |
| ECR | Image storage | ~$1-3 |
| ACM (SSL) | Free | $0 |
| **Total** | | **~$100-150/month** |

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `app_name` | string | Yes | Application name (used for all AWS resources) |
| `aws_region` | string | Yes | AWS region (e.g., ap-south-1) |
| `aws_account_id` | string | Yes | AWS account ID |
| `domain` | string | No | Custom domain for SSL |
| `frontend_port` | number | No | Frontend port (default: 3000) |
| `backend_port` | number | No | Backend port (default: 8000) |
| `fargate_cpu` | string | No | Task CPU (default: 512) |
| `fargate_memory` | string | No | Task memory (default: 1024) |
| `desired_count` | number | No | Number of tasks (default: 2) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `alb_dns` | string | ALB DNS name (public URL) |
| `ecr_frontend_uri` | string | Frontend ECR repository URI |
| `ecr_backend_uri` | string | Backend ECR repository URI |
| `cluster_name` | string | ECS cluster name |
| `cloudwatch_dashboard` | string | CloudWatch dashboard URL |

### Credentials
| Name | Source |
|------|--------|
| `AWS_ACCESS_KEY_ID` | IAM User / GitHub Secrets |
| `AWS_SECRET_ACCESS_KEY` | IAM User / GitHub Secrets |
| `MONGODB_URI` | MongoDB Atlas connection string |
| `OPENAI_API_KEY` | OpenAI dashboard |

### Composable With
- `modal-deploy` (alternative: serverless functions)
- `design-website` (frontend design before deployment)
- Any project with frontend + backend containers

### Cost
~$100-150/month for a production setup (ap-south-1 pricing)
