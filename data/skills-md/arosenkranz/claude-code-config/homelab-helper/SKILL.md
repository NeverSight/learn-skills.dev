---
name: homelab-helper
description: Expert guidance for homelab infrastructure, self-hosting, and Raspberry Pi optimization. Use when recommending self-hosted services, configuring Docker services, setting up reverse proxies, integrating Home Assistant, or troubleshooting homelab networking.
---

# Homelab Helper

Guidance for self-hosting, home infrastructure, and Raspberry Pi optimization.

## Alex's Current Setup

- **Synology NAS**: Running Plex
- **Raspberry Pi 5** (Raspberry Pi OS):
  - Home Assistant
  - Music Assistant
  - Datadog Agent
  - Docker-based services via Portainer

## Self-Hosted Service Recommendations

### Media & Entertainment
| Service | Purpose | Resource Usage |
|---------|---------|----------------|
| Jellyfin | Media server (Plex alternative) | Medium |
| Navidrome | Music streaming | Low |
| Audiobookshelf | Audiobooks/podcasts | Low |
| Calibre-web | E-book library | Low |

### Productivity
| Service | Purpose | Resource Usage |
|---------|---------|----------------|
| Paperless-ngx | Document management | Medium |
| Mealie | Recipe manager | Low |
| Linkwarden | Bookmark manager | Low |
| Vikunja | Task management | Low |

### Home Automation
| Service | Purpose | Resource Usage |
|---------|---------|----------------|
| Home Assistant | Automation hub | Medium |
| Node-RED | Flow automation | Low |
| Mosquitto | MQTT broker | Very Low |
| Zigbee2MQTT | Zigbee devices | Low |

### Monitoring & Management
| Service | Purpose | Resource Usage |
|---------|---------|----------------|
| Uptime Kuma | Service monitoring | Very Low |
| Dozzle | Docker log viewer | Very Low |
| Homepage | Dashboard | Very Low |
| Netdata | System metrics | Low |

## Docker Compose Best Practices

### Service Template

```yaml
version: "3.8"

services:
  myservice:
    image: organization/image:tag  # Always pin versions
    container_name: myservice
    restart: unless-stopped

    # Resource limits for Pi
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 128M

    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

    environment:
      - TZ=America/New_York
      - PUID=1000
      - PGID=1000

    volumes:
      - ./config:/config           # Config persistence
      - /etc/localtime:/etc/localtime:ro  # Timezone

    networks:
      - proxy  # For reverse proxy

    labels:
      # Traefik labels for reverse proxy
      - "traefik.enable=true"
      - "traefik.http.routers.myservice.rule=Host(`service.local`)"

networks:
  proxy:
    external: true
```

### Organizing Multiple Compose Files

```
~/docker/
├── core/
│   └── docker-compose.yml    # Traefik, Portainer, Watchtower
├── media/
│   └── docker-compose.yml    # Plex, Jellyfin, *arr stack
├── home/
│   └── docker-compose.yml    # Home Assistant, MQTT
├── monitoring/
│   └── docker-compose.yml    # Uptime Kuma, Dozzle
└── .env                      # Shared environment variables
```

## Reverse Proxy Setup (Traefik)

```yaml
# core/docker-compose.yml
version: "3.8"

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    restart: unless-stopped
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=${ACME_EMAIL}"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`traefik.${DOMAIN}`)"
      - "traefik.http.routers.dashboard.service=api@internal"
      - "traefik.http.routers.dashboard.middlewares=auth"
      - "traefik.http.middlewares.auth.basicauth.users=${TRAEFIK_AUTH}"

networks:
  proxy:
    name: proxy
```

## Raspberry Pi Optimization

### Memory Management

```bash
# Check memory usage
free -h

# Reduce GPU memory (headless server)
# In /boot/config.txt
gpu_mem=16

# Enable zram for better memory utilization
sudo apt install zram-tools
# Edit /etc/default/zramswap
ALLOCATION=100  # Percentage of RAM
```

### Storage Optimization

```bash
# Use SSD/NVMe instead of SD card for Docker
# Mount external drive
sudo mkdir /mnt/ssd
sudo mount /dev/sda1 /mnt/ssd

# Add to /etc/fstab
/dev/sda1 /mnt/ssd ext4 defaults,noatime 0 2

# Move Docker data directory
sudo systemctl stop docker
sudo mv /var/lib/docker /mnt/ssd/docker
sudo ln -s /mnt/ssd/docker /var/lib/docker
sudo systemctl start docker
```

### Temperature Monitoring

```bash
# Check CPU temperature
vcgencmd measure_temp

# Monitor continuously
watch -n 1 vcgencmd measure_temp

# In Docker compose for monitoring
environment:
  - HOST_PROC=/host/proc
volumes:
  - /proc:/host/proc:ro
```

## Home Assistant Integration

### Docker Compose for HA

```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable
    container_name: homeassistant
    restart: unless-stopped
    network_mode: host  # Required for device discovery
    privileged: true     # Required for Bluetooth/USB
    volumes:
      - ./config:/config
      - /etc/localtime:/etc/localtime:ro
      - /run/dbus:/run/dbus:ro  # For Bluetooth
    environment:
      - TZ=America/New_York
```

### Useful Automations

```yaml
# Turn off lights when no one home
automation:
  - alias: "Lights off when away"
    trigger:
      - platform: state
        entity_id: group.family
        to: "not_home"
        for: "00:10:00"
    action:
      - service: light.turn_off
        target:
          entity_id: all
```

## Network Configuration

### Static IP for Services

```bash
# /etc/dhcpcd.conf on Raspberry Pi
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 1.1.1.1
```

### Local DNS with Pi-hole

```yaml
services:
  pihole:
    image: pihole/pihole:latest
    container_name: pihole
    restart: unless-stopped
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "8080:80/tcp"
    environment:
      TZ: America/New_York
      WEBPASSWORD: ${PIHOLE_PASSWORD}
    volumes:
      - ./etc-pihole:/etc/pihole
      - ./etc-dnsmasq.d:/etc/dnsmasq.d
    cap_add:
      - NET_ADMIN
```

## Backup Strategy

### Automated Backups

```bash
#!/bin/bash
# backup-docker.sh
BACKUP_DIR="/mnt/nas/backups/docker"
DATE=$(date +%Y%m%d)

# Stop services
docker-compose -f ~/docker/core/docker-compose.yml down

# Backup volumes
tar -czf "$BACKUP_DIR/docker-volumes-$DATE.tar.gz" ~/docker/

# Restart services
docker-compose -f ~/docker/core/docker-compose.yml up -d

# Keep only last 7 days
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
```

### Cron Schedule

```bash
# Run daily at 3 AM
0 3 * * * /home/pi/scripts/backup-docker.sh >> /var/log/backup.log 2>&1
```

## Security Checklist

- [ ] Change default SSH port
- [ ] Disable password auth, use SSH keys
- [ ] Set up fail2ban
- [ ] Use reverse proxy with SSL
- [ ] Keep containers updated (Watchtower)
- [ ] Isolate containers with networks
- [ ] Don't expose unnecessary ports
- [ ] Use secrets management for credentials
