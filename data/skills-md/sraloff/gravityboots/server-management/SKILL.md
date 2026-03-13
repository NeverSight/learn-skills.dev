---
name: server-management
description: DigitalOcean Droplets, Linux server security, Nginx, and UFW.
---

# Server Management (DigitalOcean)

## When to use this skill
- Provisioning a new DigitalOcean Droplet.
- Configuring Nginx or UFW.
- Troubleshooting Linux server issues.

## 1. Initial Setup
- **User**: Create a non-root user with sudo privileges immediately.
- **SSH**: Disable password login (`PermitRootLogin no`, `PasswordAuthentication no`). Use SSH keys.

## 2. Security
- **Firewall (UFW)**:
  ```bash
  ufw allow OpenSSH
  ufw allow 'Nginx Full'
  ufw enable
  ```
- **Fail2Ban**: Install to prevent brute force attacks.

## 3. Nginx Config
- **Reverse Proxy**: Standard pattern for Node/Python apps:
  ```nginx
  location / {
      proxy_pass http://localhost:3000;
      proxy_set_header Host $host;
  }
  ```
- **SSL**: Use Certbot (`python3-certbot-nginx`) for auto-renewing Let's Encrypt certificates.
