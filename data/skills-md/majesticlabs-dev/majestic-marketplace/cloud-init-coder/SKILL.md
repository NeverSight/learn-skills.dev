---
name: cloud-init-coder
description: This skill guides writing cloud-init configurations for VM provisioning. Use when creating user_data blocks in Terraform/OpenTofu, or cloud-init YAML for AWS, DigitalOcean, GCP, or Azure instances.
allowed-tools: Read Write Edit Grep Glob
---

# Cloud-Init Coder

## Overview

Cloud-init is the industry standard for cross-platform cloud instance initialization. It runs on first boot to configure users, packages, files, and services before the instance becomes available.

## Core Format

Cloud-init configs start with `#cloud-config`:

```yaml
#cloud-config
package_update: true
packages:
  - nginx
  - docker.io
```

## User Management

### Create Deploy User

```yaml
#cloud-config
users:
  - name: deploy
    groups: docker, sudo
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... deploy@example.com
```

### Multiple Users

```yaml
#cloud-config
users:
  - default  # Keep cloud provider's default user
  - name: deploy
    groups: docker
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... key1
  - name: monitoring
    groups: adm
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... monitoring-key
```

## Package Installation

### Basic Packages

```yaml
#cloud-config
package_update: true
package_upgrade: true
packages:
  - docker.io
  - docker-compose-plugin
  - nginx
  - certbot
  - python3-certbot-nginx
  - fail2ban
  - ufw
```

### From Custom Repositories

```yaml
#cloud-config
apt:
  sources:
    docker:
      source: "deb [arch=amd64] https://download.docker.com/linux/ubuntu $RELEASE stable"
      keyid: 9DC858229FC7DD38854AE2D88D81803C0EBFCD88

packages:
  - docker-ce
  - docker-ce-cli
  - containerd.io
```

## SSH Hardening

### Declarative SSH Lockdown

Prefer declarative `ssh_pwauth: false` over runcmd sed commands:

```yaml
#cloud-config
ssh_pwauth: false  # Disable password auth at cloud-init level

runcmd:
  # Additional hardening via sshd_config
  - sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
  - systemctl restart sshd
```

### Full SSH Hardening

```yaml
#cloud-config
ssh_pwauth: false  # Declarative - cleaner than sed

runcmd:
  # Disable root login (or use prohibit-password for key-only root)
  - sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
  - sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

  # Disable password authentication (backup for ssh_pwauth)
  - sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

  # Increase keepalive for stable connections
  - sed -i 's/^#\?ClientAliveInterval.*/ClientAliveInterval 60/' /etc/ssh/sshd_config
  - sed -i 's/^#\?ClientAliveCountMax.*/ClientAliveCountMax 10/' /etc/ssh/sshd_config

  # Restart SSH
  - systemctl restart sshd
```

## Docker Setup

### Docker with Compose

```yaml
#cloud-config
package_update: true
packages:
  - docker.io
  - docker-compose-plugin

groups:
  - docker

users:
  - name: deploy
    groups: docker
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA...

runcmd:
  - systemctl enable --now docker
  - usermod -aG docker deploy
```

### Docker with Custom Daemon Config

```yaml
#cloud-config
write_files:
  - path: /etc/docker/daemon.json
    content: |
      {
        "log-driver": "json-file",
        "log-opts": {
          "max-size": "10m",
          "max-file": "3"
        },
        "storage-driver": "overlay2"
      }

runcmd:
  - systemctl enable --now docker
```

## File Creation

### Write Configuration Files

```yaml
#cloud-config
write_files:
  - path: /etc/nginx/sites-available/app
    content: |
      server {
          listen 80;
          server_name example.com;
          location / {
              proxy_pass http://127.0.0.1:3000;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
          }
      }
    owner: root:root
    permissions: '0644'

  - path: /opt/app/.env
    content: |
      RAILS_ENV=production
      PORT=3000
    owner: deploy:deploy
    permissions: '0600'
```

### Download Files

```yaml
#cloud-config
runcmd:
  - curl -fsSL https://example.com/setup.sh -o /opt/setup.sh
  - chmod +x /opt/setup.sh
  - /opt/setup.sh
```

## Service Configuration

### Enable and Start Services

```yaml
#cloud-config
runcmd:
  - systemctl enable --now docker
  - systemctl enable --now nginx
  - systemctl enable --now fail2ban
```

### Systemd Service Creation

```yaml
#cloud-config
write_files:
  - path: /etc/systemd/system/myapp.service
    content: |
      [Unit]
      Description=My Application
      After=network.target docker.service
      Requires=docker.service

      [Service]
      Type=simple
      User=deploy
      WorkingDirectory=/opt/app
      ExecStart=/usr/bin/docker compose up
      ExecStop=/usr/bin/docker compose down
      Restart=always
      RestartSec=10

      [Install]
      WantedBy=multi-user.target

runcmd:
  - systemctl daemon-reload
  - systemctl enable --now myapp
```

## Firewall Configuration

### UFW Setup

```yaml
#cloud-config
packages:
  - ufw

runcmd:
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow ssh
  - ufw allow http
  - ufw allow https
  - ufw --force enable
```

## Terraform/OpenTofu Integration

### Inline User Data

```hcl
resource "digitalocean_droplet" "app" {
  name   = "app-server"
  image  = "ubuntu-22-04-x64"
  size   = "s-1vcpu-1gb"
  region = "nyc1"

  user_data = <<-EOT
    #cloud-config
    package_update: true
    packages:
      - docker.io
      - docker-compose-plugin
    users:
      - name: deploy
        groups: docker
        sudo: ALL=(ALL) NOPASSWD:ALL
        shell: /bin/bash
        ssh_authorized_keys:
          - ${var.deploy_ssh_key}
    runcmd:
      - systemctl enable --now docker
  EOT
}
```

### Template File

```hcl
# templates/cloud-init.yaml
#cloud-config
package_update: true
packages:
  - docker.io
users:
  - name: ${username}
    groups: docker
    ssh_authorized_keys:
      - ${ssh_key}

# main.tf
resource "digitalocean_droplet" "app" {
  user_data = templatefile("${path.module}/templates/cloud-init.yaml", {
    username = var.deploy_user
    ssh_key  = var.deploy_ssh_key
  })
}
```

## Complete Production Example

```yaml
#cloud-config
package_update: true
package_upgrade: true

packages:
  - docker.io
  - docker-compose-plugin
  - fail2ban
  - ufw
  - unattended-upgrades

groups:
  - docker

users:
  - name: deploy
    groups: docker, sudo
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... deploy-key

write_files:
  - path: /etc/docker/daemon.json
    content: |
      {
        "log-driver": "json-file",
        "log-opts": { "max-size": "10m", "max-file": "3" }
      }

  - path: /etc/fail2ban/jail.local
    content: |
      [sshd]
      enabled = true
      port = ssh
      filter = sshd
      maxretry = 3
      bantime = 3600

runcmd:
  # Docker
  - systemctl enable --now docker

  # SSH hardening
  - sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
  - sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
  - sed -i 's/^#\?ClientAliveInterval.*/ClientAliveInterval 60/' /etc/ssh/sshd_config
  - sed -i 's/^#\?ClientAliveCountMax.*/ClientAliveCountMax 10/' /etc/ssh/sshd_config
  - systemctl restart sshd

  # Firewall
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow ssh
  - ufw allow http
  - ufw allow https
  - ufw --force enable

  # Fail2ban
  - systemctl enable --now fail2ban

  # Auto-updates
  - systemctl enable --now unattended-upgrades

final_message: "Cloud-init completed after $UPTIME seconds"
```

## Server Tuning

### Performance and Cleanup

```yaml
#cloud-config
runcmd:
  # Reduce swap usage (better for databases/apps with their own memory management)
  - |
    if ! grep -q "vm.swappiness=10" /etc/sysctl.conf; then
      echo "vm.swappiness=10" >> /etc/sysctl.conf
      sysctl -p
    fi

  # Set timezone
  - timedatectl set-timezone UTC  # Or: Europe/Berlin, America/New_York

  # Cleanup
  - apt-get autoremove -y
  - apt-get clean
```

### Swappiness Values

| Value | Behavior |
|-------|----------|
| `0` | Only swap to avoid OOM |
| `10` | Minimal swapping (recommended for apps) |
| `60` | Default Ubuntu |
| `100` | Aggressive swapping |

## Debugging

### Check Cloud-Init Status

```bash
# View cloud-init status
cloud-init status

# View cloud-init logs
cat /var/log/cloud-init.log
cat /var/log/cloud-init-output.log

# Re-run cloud-init (for testing)
sudo cloud-init clean
sudo cloud-init init
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| YAML parse error | Indentation wrong | Use 2-space indent, validate YAML |
| User not created | Missing `users:` key | Ensure `users:` is at root level |
| Packages not installed | `package_update: false` | Set `package_update: true` |
| SSH key rejected | Wrong key format | Use full public key string |
| Service not starting | Order dependency | Use `After=` in systemd unit |
