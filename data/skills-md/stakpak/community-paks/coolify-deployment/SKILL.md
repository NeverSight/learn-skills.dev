---
name: coolify-deployment
description: |
  Deploy Coolify self-hosted PaaS for application hosting. Covers VM provisioning, installation, GitHub integration, and application deployment with auto-SSL.
license: MIT
tags:
  - coolify
  - paas
  - self-hosted
  - docker
  - deployment
  - heroku-alternative
  - ssl
  - traefik
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.3"
---

# Coolify Self-Hosted PaaS Deployment

## Quick Start

### Install Coolify on VM

```bash
ssh -i <key-file> <user>@<instance-ip>
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | sudo bash
# Access: http://<instance-ip>:8000
```

### Deploy Application

1. Access Coolify UI at `http://<instance-ip>:8000`
2. Create admin account (first visitor gets admin)
3. Add GitHub source → Create project → Deploy from repo
4. Access app at `http://<container-id>.<instance-ip>.sslip.io`

## Server Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 vCPU | 4 vCPU |
| RAM | 2GB | 4GB |
| Storage | 30GB | 50GB |
| OS | Ubuntu 20.04/22.04/24.04 LTS | Ubuntu 24.04 LTS |

**Required Ports:**
- TCP 22 (SSH)
- TCP 80 (HTTP/Let's Encrypt)
- TCP 443 (HTTPS)
- TCP 8000 (Coolify UI)

## Cloud VM Deployment

### 1. Provision Infrastructure

```bash
# Create security group with required ports
# - TCP 22 (SSH)
# - TCP 80 (HTTP)
# - TCP 443 (HTTPS)
# - TCP 8000 (Coolify UI)

# Launch instance with:
# - 2+ vCPU, 2GB+ RAM
# - 30GB+ root volume
# - Ubuntu LTS
# - Public IP
# - SSH key pair
```

### 2. Install Coolify

```bash
# Set key permissions
chmod 400 /path/to/key.pem

# Connect and install
ssh -o StrictHostKeyChecking=no -i /path/to/key.pem <user>@<instance-ip>
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | sudo bash
```

### 3. Initial Setup

1. Open browser: `http://<instance-ip>:8000`
2. **IMPORTANT**: Create admin account immediately
3. Complete setup wizard

### 4. Verify Installation

```bash
ssh -i /path/to/key.pem <user>@<instance-ip> \
  "sudo docker ps --format 'table {{.Names}}\t{{.Status}}' | grep coolify"
```

## Application Deployment

### Supported Build Methods

| Method | Use Case |
|--------|----------|
| Dockerfile | Custom container builds |
| Nixpacks | Auto-detected language builds |
| Docker Compose | Multi-container apps |
| Static | HTML/JS/CSS sites |

### Deploy from GitHub

1. **Add Source**: Sources → Add New → GitHub App
2. **Create Project**: Projects → Add New Project
3. **Add Resource**: Add New Resource → Public/Private Repository
4. **Configure**:
   - Repository URL
   - Branch
   - Build pack (Dockerfile/Nixpacks)
   - Port to expose
5. **Deploy**: Click Deploy button

### Sample Dockerfile Application

```
app/
├── main.py          # Application code
├── requirements.txt # Dependencies
└── Dockerfile       # Container definition
```

**Dockerfile:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Domain Configuration

**Auto-generated (sslip.io):**
- Format: `<container-id>.<public-ip>.sslip.io`
- Works immediately, no DNS required

**Custom Domain:**
1. Add DNS A record → EC2 public IP
2. Update domain in Coolify resource settings
3. Enable SSL (Let's Encrypt auto-configured)

## Verification

### Check Container Status

```bash
ssh -i /path/to/key.pem <user>@<instance-ip> \
  "sudo docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}'"
```

### Test Application

```bash
# Get app URL from Coolify UI
APP_URL="http://<container-id>.<public-ip>.sslip.io"

curl -s $APP_URL/
curl -s $APP_URL/health
```

### Check Logs

```bash
# Application logs
ssh -i /path/to/key.pem <user>@<instance-ip> \
  "sudo docker logs <container-name> --tail 50"

# Coolify logs
ssh -i /path/to/key.pem <user>@<instance-ip> \
  "sudo docker logs coolify --tail 50"
```

## Configuration Reference

### Coolify Containers

| Container | Purpose | Port |
|-----------|---------|------|
| coolify | Main application | 8000 |
| coolify-proxy | Traefik reverse proxy | 80, 443 |
| coolify-db | PostgreSQL database | 5432 |
| coolify-redis | Redis cache | 6379 |
| coolify-realtime | WebSocket server | 6001-6002 |

### Important Paths

| Path | Purpose |
|------|---------|
| `/data/coolify/source/.env` | Coolify configuration |
| `/data/coolify/proxy/dynamic/` | Traefik dynamic config |
| `/data/coolify/applications/` | Application data |
| `/data/coolify/databases/` | Database volumes |

### Environment Variables (Installation)

| Variable | Purpose | Example |
|----------|---------|---------|
| `ROOT_USERNAME` | Admin username | `admin` |
| `ROOT_USER_EMAIL` | Admin email | `admin@example.com` |
| `ROOT_USER_PASSWORD` | Admin password | `SecurePass123` |
| `AUTOUPDATE` | Auto-update toggle | `true`/`false` |

## Production Checklist

- [ ] Create admin account immediately after install
- [ ] Backup `/data/coolify/source/.env` to secure location
- [ ] Configure firewall/security group rules
- [ ] Set up custom domain with SSL
- [ ] Restrict SSH access to specific IPs
- [ ] Configure monitoring/alerts
- [ ] Test deployment rollback procedure
- [ ] Document access credentials securely

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 on public IP | Access via sslip.io domain, not raw IP |
| Cannot access Coolify UI | Check security group allows port 8000 |
| Deployment fails | Check Coolify logs and Dockerfile syntax |
| SSL certificate fails | Ensure port 80 open, DNS configured |
| Container not starting | Check container logs for errors |
| Out of disk space | Prune Docker: `docker system prune -a` |
| Coolify unresponsive | Restart: `docker restart coolify` |

## Update Coolify

```bash
ssh -i /path/to/key.pem <user>@<instance-ip> \
  "cd /data/coolify/source && sudo bash upgrade.sh"
```

## Cleanup

```bash
# Stop all containers
ssh -i /path/to/key.pem <user>@<instance-ip> \
  "cd /data/coolify/source && sudo docker compose down"

# Remove Coolify data (destructive)
ssh -i /path/to/key.pem <user>@<instance-ip> \
  "sudo rm -rf /data/coolify"

# Terminate cloud instance
```

## References

- [Coolify Documentation](https://coolify.io/docs)
- [Coolify Installation Guide](https://coolify.io/docs/get-started/installation)
- [Coolify GitHub](https://github.com/coollabsio/coolify)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [sslip.io](https://sslip.io/)
