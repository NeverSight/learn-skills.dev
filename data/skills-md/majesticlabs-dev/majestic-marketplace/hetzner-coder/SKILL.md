---
name: hetzner-coder
description: This skill guides provisioning Hetzner Cloud infrastructure with OpenTofu/Terraform. Use when creating servers, networks, firewalls, load balancers, or volumes on Hetzner Cloud.
allowed-tools: Read Write Edit Grep Glob Bash
---

## Provider Setup

```hcl
terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.50"
    }
  }
}

provider "hcloud" {
  # Uses HCLOUD_TOKEN env var
}
```

### Authentication

```bash
export HCLOUD_TOKEN="your-api-token"
# Or with 1Password
HCLOUD_TOKEN=op://Infrastructure/Hetzner/api_token
```

## Locations

| Code | Region | Network Zone |
|------|--------|--------------|
| `fsn1` | Germany | `eu-central` |
| `nbg1` | Germany | `eu-central` |
| `hel1` | Finland | `eu-central` |
| `ash` | US East | `us-east` |
| `hil` | US West | `us-west` |

See [references/hetzner-server-types.md](references/hetzner-server-types.md) for all server types (CX, CPX, CAX, CCX).

## Servers (Compute)

### Basic Server

```hcl
resource "hcloud_server" "app" {
  name        = "${var.project}-${var.environment}-app"
  server_type = "cx22"
  image       = "ubuntu-24.04"
  location    = "fsn1"

  ssh_keys = [hcloud_ssh_key.deploy.id]

  labels = {
    environment = var.environment
    project     = var.project
    role        = "app"
  }

  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
}
```

### Server with Cloud-Init

```hcl
resource "hcloud_server" "app" {
  name        = "${var.project}-app"
  server_type = "cx22"
  image       = "ubuntu-24.04"
  location    = "fsn1"

  ssh_keys = [hcloud_ssh_key.deploy.id]

  user_data = <<-EOT
    #cloud-config
    package_update: true
    packages:
      - docker.io
      - docker-compose-plugin

    users:
      - name: deploy
        groups: docker, sudo
        sudo: ALL=(ALL) NOPASSWD:ALL
        shell: /bin/bash
        ssh_authorized_keys:
          - ${var.deploy_ssh_key}

    runcmd:
      - systemctl enable --now docker
      - sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
      - sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
      - systemctl restart sshd
  EOT

  labels = {
    environment = var.environment
    role        = "app"
  }
}
```

## Private Networks

### Network with Subnet

```hcl
resource "hcloud_network" "private" {
  name     = "${var.project}-network"
  ip_range = "10.0.0.0/16"

  labels = {
    project = var.project
  }
}

resource "hcloud_network_subnet" "private" {
  network_id   = hcloud_network.private.id
  type         = "cloud"
  network_zone = "eu-central"
  ip_range     = "10.0.1.0/24"
}
```

### Server in Private Network

```hcl
resource "hcloud_server" "db" {
  name        = "${var.project}-db"
  server_type = "cpx31"
  image       = "ubuntu-24.04"
  location    = "fsn1"

  ssh_keys = [hcloud_ssh_key.deploy.id]

  network {
    network_id = hcloud_network.private.id
    ip         = "10.0.1.10"
  }

  public_net {
    ipv4_enabled = false
    ipv6_enabled = false
  }

  labels = {
    role = "database"
  }

  depends_on = [hcloud_network_subnet.private]
}
```

## Firewalls

Never default SSH to `0.0.0.0/0`. Force explicit IP: `tofu apply -var="admin_ip=$(curl -s ifconfig.me)/32"`

### Web Server Firewall

```hcl
resource "hcloud_firewall" "web" {
  name = "${var.project}-web-firewall"

  rule {
    description = "SSH"
    direction   = "in"
    protocol    = "tcp"
    port        = "22"
    source_ips  = [var.admin_ip]
  }

  rule {
    description = "HTTP"
    direction   = "in"
    protocol    = "tcp"
    port        = "80"
    source_ips  = ["0.0.0.0/0", "::/0"]
  }

  rule {
    description = "HTTPS"
    direction   = "in"
    protocol    = "tcp"
    port        = "443"
    source_ips  = ["0.0.0.0/0", "::/0"]
  }

  apply_to {
    label_selector = "role=web"
  }
}

variable "admin_ip" {
  description = "Admin IP for SSH access (CIDR)"
  type        = string
}
```

### Database Firewall (Private Only)

```hcl
resource "hcloud_firewall" "db" {
  name = "${var.project}-db-firewall"

  rule {
    description = "PostgreSQL"
    direction   = "in"
    protocol    = "tcp"
    port        = "5432"
    source_ips  = ["10.0.0.0/16"]
  }

  rule {
    description = "SSH from bastion"
    direction   = "in"
    protocol    = "tcp"
    port        = "22"
    source_ips  = ["10.0.1.1/32"]
  }

  apply_to {
    label_selector = "role=database"
  }
}
```

## Floating IPs (High Availability)

```hcl
resource "hcloud_floating_ip" "app" {
  type          = "ipv4"
  name          = "${var.project}-vip"
  home_location = "fsn1"
}

resource "hcloud_floating_ip_assignment" "app" {
  floating_ip_id = hcloud_floating_ip.app.id
  server_id      = hcloud_server.app.id
}

output "floating_ip" {
  value = hcloud_floating_ip.app.ip_address
}
```

## Load Balancers

### HTTP Load Balancer

```hcl
resource "hcloud_load_balancer" "web" {
  name               = "${var.project}-lb"
  load_balancer_type = "lb11"
  location           = "fsn1"

  labels = {
    project = var.project
  }
}

resource "hcloud_load_balancer_network" "web" {
  load_balancer_id = hcloud_load_balancer.web.id
  network_id       = hcloud_network.private.id
  ip               = "10.0.1.100"
}

resource "hcloud_load_balancer_service" "http" {
  load_balancer_id = hcloud_load_balancer.web.id
  protocol         = "http"
  listen_port      = 80
  destination_port = 8080

  health_check {
    protocol = "http"
    port     = 8080
    interval = 10
    timeout  = 5
    retries  = 3

    http {
      path         = "/health"
      status_codes = ["200"]
    }
  }
}

resource "hcloud_load_balancer_target" "web" {
  load_balancer_id = hcloud_load_balancer.web.id
  type             = "server"
  server_id        = hcloud_server.app.id
  use_private_ip   = true

  depends_on = [hcloud_load_balancer_network.web]
}
```

### HTTPS Load Balancer with Certificate

```hcl
resource "hcloud_managed_certificate" "web" {
  name         = "${var.project}-cert"
  domain_names = [var.domain, "www.${var.domain}"]

  labels = {
    project = var.project
  }
}

resource "hcloud_load_balancer_service" "https" {
  load_balancer_id = hcloud_load_balancer.web.id
  protocol         = "https"
  listen_port      = 443
  destination_port = 8080

  http {
    certificates = [hcloud_managed_certificate.web.id]
    redirect_http = true
  }

  health_check {
    protocol = "http"
    port     = 8080
    interval = 10
    timeout  = 5
  }
}
```

## Volumes (Persistent Storage)

```hcl
resource "hcloud_volume" "data" {
  name      = "${var.project}-data"
  size      = 100  # GB
  location  = "fsn1"
  format    = "ext4"

  labels = {
    project = var.project
    purpose = "database"
  }
}

resource "hcloud_volume_attachment" "data" {
  volume_id = hcloud_volume.data.id
  server_id = hcloud_server.db.id
  automount = true
}
```

## SSH Keys

```hcl
resource "hcloud_ssh_key" "deploy" {
  name       = "${var.project}-deploy"
  public_key = file(var.ssh_public_key_path)
}
```

## References

- [references/hetzner-server-types.md](references/hetzner-server-types.md) - All server types with specs
- [references/ansible-integration.md](references/ansible-integration.md) - Hetzner+Ansible patterns, Kamal-ready playbooks
- [references/best-practices.md](references/best-practices.md) - Labels, cost optimization, placement groups, snapshots
- [references/object-storage.md](references/object-storage.md) - S3-compatible Object Storage with AWS provider
- [references/production-stack.md](references/production-stack.md) - Complete production setup
