---
name: cloudflare-tunnel-ec2-deployment
description: |
  Deploy containerized applications to AWS EC2 and expose them publicly via Cloudflare Tunnel with automatic HTTPS. Eliminates need for load balancers, SSL certificates, or public inbound ports.
license: MIT
metadata:
  author: Stakpak <team@stakpak.dev>
  version: 1.0.17
---

# Deploying Applications on EC2 with Cloudflare Tunnel

## Quick Start

### Provision and Deploy

```bash
# Get VPC and subnet
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text)
SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=map-public-ip-on-launch,Values=true" --query 'Subnets[0].SubnetId' --output text)

# Create security group
SG_ID=$(aws ec2 create-security-group --group-name app-sg --description "Security group for app deployment" --vpc-id $VPC_ID --query 'GroupId' --output text)
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0

# Launch instance
AMI_ID=$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=al2023-ami-2023*-x86_64" "Name=state,Values=available" --query 'sort_by(Images, &CreationDate)[-1].ImageId' --output text)
INSTANCE_ID=$(aws ec2 run-instances --image-id $AMI_ID --instance-type t3.small --key-name app-deploy-key --security-group-ids $SG_ID --subnet-id $SUBNET_ID --associate-public-ip-address --query 'Instances[0].InstanceId' --output text)
```

## Prerequisites

* AWS CLI configured with appropriate permissions (EC2, VPC)
* Cloudflare account with a domain configured
* Docker-compatible application with Dockerfile
* Cloudflare Tunnel token from Zero Trust dashboard

## Infrastructure Setup

### 1. VPC Resources

```bash
# Get default VPC
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" \
  --query 'Vpcs[0].VpcId' --output text)

# Get public subnet
SUBNET_ID=$(aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" "Name=map-public-ip-on-launch,Values=true" \
  --query 'Subnets[0].SubnetId' --output text)
```

### 2. Security Group

```bash
# Create security group - only SSH needed for management
# Cloudflare Tunnel handles all inbound traffic
SG_ID=$(aws ec2 create-security-group \
  --group-name app-sg \
  --description "Security group for app deployment" \
  --vpc-id $VPC_ID \
  --query 'GroupId' --output text)

# Allow SSH access (restrict to your IP in production)
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp --port 22 --cidr 0.0.0.0/0
```

**Key insight:** With Cloudflare Tunnel, you don't need to open ports 80/443. The tunnel creates outbound connections to Cloudflare, eliminating inbound attack surface.

### 3. SSH Key Pair

```bash
# Generate local key
ssh-keygen -t ed25519 -f ~/.ssh/app-deploy-key -N "" -C "app-deploy"

# Import to AWS
aws ec2 import-key-pair \
  --key-name app-deploy-key \
  --public-key-material fileb://~/.ssh/app-deploy-key.pub
```

**Important:** Never delete SSH keys after creation - you'll be locked out of the instance.

### 4. Launch EC2 Instance

```bash
# Get latest Amazon Linux 2023 AMI
AMI_ID=$(aws ec2 describe-images --owners amazon \
  --filters "Name=name,Values=al2023-ami-2023*-x86_64" "Name=state,Values=available" \
  --query 'sort_by(Images, &CreationDate)[-1].ImageId' --output text)

# Launch instance
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type t3.small \
  --key-name app-deploy-key \
  --security-group-ids $SG_ID \
  --subnet-id $SUBNET_ID \
  --associate-public-ip-address \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-app}]' \
  --query 'Instances[0].InstanceId' --output text)

# Wait for instance and get IP
aws ec2 wait instance-running --instance-ids $INSTANCE_ID
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
```

### Instance Sizing

| Instance Type | Use Case |
|---------------|----------|
| `t3.micro` | Simple static sites, minimal APIs |
| `t3.small` | Standard web apps, Node.js/Python services |
| `t3.medium` | Apps with build steps, multiple containers |

## Application Deployment

### Install Docker

```bash
# Wait for SSH to be ready (30-60 seconds after instance running)
sleep 45

# Install Docker
ssh -i ~/.ssh/app-deploy-key ec2-user@$PUBLIC_IP \
  "sudo dnf install -y docker git && \
   sudo systemctl enable --now docker && \
   sudo usermod -aG docker ec2-user"
```

### Deploy Application

```bash
# Clone and build application
ssh -i ~/.ssh/app-deploy-key ec2-user@$PUBLIC_IP \
  "git clone <REPO_URL> app && \
   cd app && \
   echo 'ENV_VAR=value' > .env"

# Build and run container
ssh -i ~/.ssh/app-deploy-key ec2-user@$PUBLIC_IP \
  "cd app && \
   sudo docker build -t myapp:latest . && \
   sudo docker run -d --name myapp --restart unless-stopped -p 80:80 myapp:latest"
```

### Production Dockerfile Pattern

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG VITE_API_KEY
ENV VITE_API_KEY=$VITE_API_KEY
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Reasoning:** Multi-stage builds reduce image size and don't include build tools in production.

## Cloudflare Tunnel Configuration

### Install cloudflared

```bash
ssh -i ~/.ssh/app-deploy-key ec2-user@$PUBLIC_IP \
  "curl -fsSL https://pkg.cloudflare.com/cloudflared.repo | \
   sudo tee /etc/yum.repos.d/cloudflared.repo && \
   sudo yum install -y cloudflared"
```

### Install Tunnel as Service

```bash
# Use the token from Cloudflare Zero Trust dashboard
ssh -i ~/.ssh/app-deploy-key ec2-user@$PUBLIC_IP \
  "sudo cloudflared service install <TUNNEL_TOKEN>"
```

**Reasoning:** Installing as a systemd service ensures the tunnel auto-starts on reboot and restarts on failure.

### Verify Tunnel Connection

```bash
ssh -i ~/.ssh/app-deploy-key ec2-user@$PUBLIC_IP \
  "sudo systemctl status cloudflared"
```

Look for: `Registered tunnel connection` messages (should see 4 connections for a healthy tunnel).

## DNS Configuration

### Cloudflare Dashboard Method

In Cloudflare Zero Trust dashboard:
1. Navigate to **Networks → Tunnels**
2. Select your tunnel → **Public Hostname** tab
3. Add hostname:
   - Subdomain: `app`
   - Domain: `example.com`
   - Type: `HTTP`
   - URL: `localhost:80`

This automatically creates a CNAME record pointing to `<tunnel-id>.cfargotunnel.com`.

### API Method

```bash
# Create DNS record via API
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "app",
    "content": "<tunnel-id>.cfargotunnel.com",
    "proxied": true
  }'
```

## Validation

### Test Deployment

```bash
# Test via tunnel (may take 1-2 minutes for DNS propagation)
curl -sI https://app.example.com/

# Check container logs
ssh -i ~/.ssh/app-deploy-key ec2-user@$PUBLIC_IP \
  "sudo docker logs myapp"

# Verify tunnel health
ssh -i ~/.ssh/app-deploy-key ec2-user@$PUBLIC_IP \
  "sudo journalctl -u cloudflared -n 20"
```

### Success Criteria

* HTTP 200 response from public URL
* No errors in container logs
* 4 registered tunnel connections

## Outputs Documentation

Create an outputs file for future reference:

```json
{
  "app_url": "https://app.example.com",
  "ec2_instance_id": "<instance-id>",
  "ec2_public_ip": "<public-ip>",
  "aws_region": "us-east-1",
  "ssh_command": "ssh -i ~/.ssh/app-deploy-key ec2-user@<public-ip>",
  "cloudflare_tunnel_id": "<tunnel-id>",
  "container_name": "myapp"
}
```

## Security Considerations

* **Restrict SSH access** - Use specific IP ranges instead of 0.0.0.0/0
* **No public ports needed** - Cloudflare Tunnel eliminates need for ports 80/443
* **Rotate tunnel tokens** - If compromised, regenerate in Cloudflare dashboard
* **Use secrets management** - Don't hardcode API keys in Dockerfiles; use build args or runtime env vars
* **Enable Cloudflare Access** - Add authentication layer for sensitive applications

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| DNS not resolving | `dig @1.1.1.1 app.example.com` | Wait for propagation or check CNAME record |
| Tunnel not connecting | Check `systemctl status cloudflared` | Verify token, check outbound connectivity on port 7844 |
| Container not starting | `docker logs myapp` | Check Dockerfile, environment variables |
| 502 Bad Gateway | Tunnel running but app not responding | Verify container is listening on correct port |

## References

* [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)
* [AWS EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/)
* [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)