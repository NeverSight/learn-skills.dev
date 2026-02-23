---
name: digitalocean-coder
description: This skill guides writing DigitalOcean infrastructure with OpenTofu/Terraform. Use when provisioning Droplets, VPCs, Managed Databases, Firewalls, or other DO resources.
allowed-tools: Read Write Edit Grep Glob Bash
---

## Provider Setup

```hcl
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  # Uses DIGITALOCEAN_TOKEN env var
}
```

## VPC (Virtual Private Cloud)

```hcl
resource "digitalocean_vpc" "main" {
  name     = "${var.project}-${var.environment}-vpc"
  region   = var.region
  ip_range = "10.10.0.0/16"

  description = "VPC for ${var.project} ${var.environment}"
}
```

## Droplets (Compute)

### Basic Droplet

```hcl
resource "digitalocean_droplet" "app" {
  name     = "${var.project}-${var.environment}-app"
  region   = var.region
  size     = var.droplet_size  # s-1vcpu-1gb, s-2vcpu-4gb, etc.
  image    = "ubuntu-22-04-x64"
  vpc_uuid = digitalocean_vpc.main.id

  ssh_keys   = var.ssh_key_ids
  monitoring = true
  ipv6       = false

  tags = [var.project, var.environment]
}
```

### Droplet with Cloud-Init

```hcl
resource "digitalocean_droplet" "app" {
  name     = "${var.project}-app"
  region   = var.region
  size     = "s-1vcpu-2gb"
  image    = "ubuntu-22-04-x64"
  vpc_uuid = digitalocean_vpc.main.id

  ssh_keys   = var.ssh_key_ids
  monitoring = true

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
      - sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
      - systemctl restart sshd
  EOT

  tags = [var.project]
}
```

See [references/digitalocean-sizes.md](references/digitalocean-sizes.md) for droplet and database sizes.

## Reserved IP (Static IP)

```hcl
resource "digitalocean_reserved_ip" "app" {
  region = var.region
}

resource "digitalocean_reserved_ip_assignment" "app" {
  ip_address = digitalocean_reserved_ip.app.ip_address
  droplet_id = digitalocean_droplet.app.id
}

output "app_ip" {
  value = digitalocean_reserved_ip.app.ip_address
}
```

## Firewall

### Basic Web Server Firewall

```hcl
resource "digitalocean_firewall" "web" {
  name = "${var.project}-web-firewall"

  droplet_ids = [digitalocean_droplet.app.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = var.ssh_allowed_ips
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
```

### Dynamic IP Whitelist

```hcl
variable "db_allowed_ips" {
  type        = list(string)
  default     = []
  description = "IPs allowed to access database directly"
}

resource "digitalocean_database_firewall" "postgres" {
  cluster_id = digitalocean_database_cluster.postgres.id

  rule {
    type  = "droplet"
    value = digitalocean_droplet.app.id
  }

  dynamic "rule" {
    for_each = var.db_allowed_ips
    content {
      type  = "ip_addr"
      value = rule.value
    }
  }
}
```

## Managed Database

### PostgreSQL Cluster

```hcl
resource "digitalocean_database_cluster" "postgres" {
  name       = "${var.project}-${var.environment}-pg"
  engine     = "pg"
  version    = "16"
  size       = var.db_size  # db-s-1vcpu-1gb, db-s-2vcpu-4gb
  region     = var.region
  node_count = 1  # Increase for HA

  private_network_uuid = digitalocean_vpc.main.id

  tags = [var.project, var.environment]
}

resource "digitalocean_database_firewall" "postgres" {
  cluster_id = digitalocean_database_cluster.postgres.id

  rule {
    type  = "droplet"
    value = digitalocean_droplet.app.id
  }
}

output "database_uri" {
  value     = digitalocean_database_cluster.postgres.uri
  sensitive = true
}

output "database_private_uri" {
  value     = digitalocean_database_cluster.postgres.private_uri
  sensitive = true
}
```

### Redis Cluster

```hcl
resource "digitalocean_database_cluster" "redis" {
  name       = "${var.project}-${var.environment}-redis"
  engine     = "redis"
  version    = "7"
  size       = "db-s-1vcpu-1gb"
  region     = var.region
  node_count = 1

  private_network_uuid = digitalocean_vpc.main.id
  tags                 = [var.project]
}
```

## Spaces (Object Storage)

```hcl
resource "digitalocean_spaces_bucket" "assets" {
  name   = "${var.project}-assets"
  region = var.spaces_region  # nyc3, sfo3, ams3, sgp1, fra1

  acl = "private"
}

resource "digitalocean_spaces_bucket_cors_configuration" "assets" {
  bucket = digitalocean_spaces_bucket.assets.id
  region = var.spaces_region

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST"]
    allowed_origins = ["https://${var.domain}"]
    max_age_seconds = 3600
  }
}

output "spaces_endpoint" {
  value = digitalocean_spaces_bucket.assets.bucket_domain_name
}
```

## DNS Records

```hcl
resource "digitalocean_domain" "main" {
  name = var.domain
}

resource "digitalocean_record" "app" {
  domain = digitalocean_domain.main.id
  type   = "A"
  name   = "@"
  value  = digitalocean_reserved_ip.app.ip_address
  ttl    = 300
}

resource "digitalocean_record" "www" {
  domain = digitalocean_domain.main.id
  type   = "CNAME"
  name   = "www"
  value  = "@"
  ttl    = 300
}
```

## SSH Keys

```hcl
data "digitalocean_ssh_key" "deploy" {
  name = "deploy-key"
}

resource "digitalocean_ssh_key" "deploy" {
  name       = "${var.project}-deploy"
  public_key = file("~/.ssh/deploy.pub")
}
```

See [references/digitalocean-production-stack.md](references/digitalocean-production-stack.md) for a complete production setup with VPC, droplet, firewall, database, and outputs.

## References

- [references/digitalocean-sizes.md](references/digitalocean-sizes.md) - Droplet and database sizes
- [references/digitalocean-production-stack.md](references/digitalocean-production-stack.md) - Complete production setup
