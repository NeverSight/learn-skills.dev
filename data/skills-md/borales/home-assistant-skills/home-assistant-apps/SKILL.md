---
name: home-assistant-apps
description: Develop, configure, test, publish, and secure Home Assistant apps (formerly add-ons) — Docker-based extensions managed by the Supervisor. Use when creating new apps, writing Dockerfiles, configuring config.yaml, setting up Ingress, building repositories, implementing security best practices, or publishing to container registries.
---

# Home Assistant Apps Development

Develop, configure, test, publish, and secure Home Assistant apps (formerly known as add-ons). Apps are Docker container images managed by the Home Assistant Supervisor that extend functionality — from MQTT brokers to file-sharing services and custom web UIs.

## When to Use This Skill

- Creating a new Home Assistant app from scratch
- Writing or reviewing app `config.yaml` configuration
- Creating or modifying app `Dockerfile` and build configuration
- Setting up `build.yaml` for multi-architecture builds
- Configuring app options and option schemas
- Implementing inter-app communication (Supervisor API, Home Assistant API, services)
- Setting up Ingress for embedded web UIs
- Writing AppArmor security profiles
- Creating app repositories with `repository.yaml`
- Publishing apps to container registries (GHCR, Docker Hub)
- Testing apps locally with devcontainers or Docker
- Troubleshooting app installation, runtime, or build issues
- Adding translations, documentation, changelogs, icons, and logos

## Core Concepts

### What Are Home Assistant Apps?

Apps (formerly called "add-ons") allow users to extend Home Assistant by running additional containerized applications alongside it. Under the hood, apps are **Docker container images** published to a container registry (e.g., GitHub Container Registry, Docker Hub). The **Supervisor** manages the full lifecycle: installation, configuration, starting, stopping, updating, and backups.

Developers create GitHub repositories containing one or more apps for easy community sharing.

### Architecture Overview

```
┌──────────────────────────────────────────────┐
│              Home Assistant OS               │
│  ┌────────────────────────────────────────┐  │
│  │            Supervisor                  │  │
│  │  ┌──────────┐ ┌──────────┐ ┌────────┐  │  │
│  │  │  HA Core │ │  App A   │ │ App B  │  │  │
│  │  │(container│ │(container│ │(contai-│  │  │
│  │  │  image)  │ │  image)  │ │ner img)│  │  │
│  │  └──────────┘ └──────────┘ └────────┘  │  │
│  │       Internal Docker Network          │  │
│  └────────────────────────────────────────┘  │
│               Host OS / HW                   │
└──────────────────────────────────────────────┘
```

- **Supervisor** orchestrates all containers, manages the internal network, and exposes management APIs.
- Each app runs as an isolated Docker container on a shared internal network.
- Apps communicate with HA Core and each other via the internal network using hostnames.
- Apps can expose ports, mount host directories, and access hardware devices.

### App File Structure

Every app lives in its own directory with a standard layout:

```
addon_name/
  translations/
    en.yaml
  apparmor.txt        # Optional: custom AppArmor profile
  build.yaml          # Optional: extended build configuration
  CHANGELOG.md        # Changelog for users
  config.yaml         # Required: app configuration
  DOCS.md             # User-facing documentation
  Dockerfile          # Required: container image definition
  icon.png            # App icon (128x128, square, PNG)
  logo.png            # App logo (~250x100, PNG)
  README.md           # Intro shown in app store
  run.sh              # Entry point script
```

> **Note:** Translation files, `config` and `build` all support `.json`, `.yml`, and `.yaml` as file types.

> **Important:** Avoid using `config.yaml` as a filename for anything other than the app configuration. The Supervisor searches recursively for `config.yaml` in the repository.

## App Configuration (`config.yaml`)

The `config.yaml` is the heart of your app. It tells the Supervisor what the app does, what it needs, and how to present it.

### Required Options

| Key           | Type   | Description                                                           |
| ------------- | ------ | --------------------------------------------------------------------- |
| `name`        | string | Display name of the app                                               |
| `version`     | string | Version of the app (must match Docker image tag if using `image`)     |
| `slug`        | string | Unique, URI-friendly identifier within the repository scope           |
| `description` | string | Short description of the app                                          |
| `arch`        | list   | Supported architectures: `armhf`, `armv7`, `aarch64`, `amd64`, `i386` |

### Key Optional Options

| Key                 | Type        | Default       | Description                                                                                                                                 |
| ------------------- | ----------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`               | url         | —             | Homepage/docs URL for the app                                                                                                               |
| `startup`           | string      | `application` | Start order: `initialize` → `system` → `services` → `application` → `once`                                                                  |
| `boot`              | string      | `auto`        | `auto`, `manual`, or `manual_only`                                                                                                          |
| `ports`             | dict        | —             | Network ports: `"container-port/type": host-port`. Use `null` to disable                                                                    |
| `ports_description` | dict        | —             | Human-readable port descriptions                                                                                                            |
| `host_network`      | bool        | `false`       | Run on the host network                                                                                                                     |
| `map`               | list        | —             | Bind-mount HA directories: `homeassistant_config`, `addon_config`, `ssl`, `addons`, `backup`, `share`, `media`, `all_addon_configs`, `data` |
| `options`           | dict        | —             | Default option values                                                                                                                       |
| `schema`            | dict        | —             | Validation schema for user options. Set to `false` to disable validation                                                                    |
| `image`             | string      | —             | Pre-built container image name (e.g., `ghcr.io/user/{arch}-addon-name`)                                                                     |
| `ingress`           | bool        | `false`       | Enable Ingress (embedded web UI via HA)                                                                                                     |
| `ingress_port`      | int         | `8099`        | Internal port for Ingress                                                                                                                   |
| `ingress_entry`     | string      | `/`           | URL entry point for Ingress                                                                                                                 |
| `ingress_stream`    | bool        | `false`       | Enable request streaming for Ingress                                                                                                        |
| `homeassistant_api` | bool        | `false`       | Enable access to HA Core REST API via proxy                                                                                                 |
| `hassio_api`        | bool        | `false`       | Enable access to Supervisor REST API                                                                                                        |
| `hassio_role`       | string      | `default`     | API role: `default`, `homeassistant`, `backup`, `manager`, `admin`                                                                          |
| `auth_api`          | bool        | `false`       | Allow access to HA user authentication backend                                                                                              |
| `privileged`        | list        | —             | Kernel capabilities: `NET_ADMIN`, `SYS_ADMIN`, `SYS_RAWIO`, etc.                                                                            |
| `full_access`       | bool        | `false`       | Full hardware access (use sparingly!)                                                                                                       |
| `apparmor`          | bool/string | `true`        | Enable or specify custom AppArmor profile                                                                                                   |
| `devices`           | list        | —             | Host device paths to map (e.g., `/dev/ttyAMA0`)                                                                                             |
| `uart`              | bool        | `false`       | Auto-map all UART/serial devices                                                                                                            |
| `usb`               | bool        | `false`       | Map raw USB access with plug & play                                                                                                         |
| `gpio`              | bool        | `false`       | Map GPIO interface                                                                                                                          |
| `audio`             | bool        | `false`       | Use internal PulseAudio system                                                                                                              |
| `video`             | bool        | `false`       | Map all video devices                                                                                                                       |
| `homeassistant`     | string      | —             | Minimum required HA Core version (e.g., `2024.10.5`)                                                                                        |
| `init`              | bool        | `true`        | Use Docker default init. Set `false` for S6 Overlay v3+                                                                                     |
| `stdin`             | bool        | `false`       | Enable STDIN via HA API                                                                                                                     |
| `backup`            | string      | `hot`         | `hot` or `cold` (cold stops the app first)                                                                                                  |
| `backup_pre`        | string      | —             | Command to run before backup                                                                                                                |
| `backup_post`       | string      | —             | Command to run after backup                                                                                                                 |
| `backup_exclude`    | list        | —             | Glob patterns to exclude from backups                                                                                                       |
| `watchdog`          | string      | —             | Health monitoring URL                                                                                                                       |
| `advanced`          | bool        | `false`       | Only show to users with "Advanced" mode enabled                                                                                             |
| `stage`             | string      | `stable`      | `stable`, `experimental`, or `deprecated`                                                                                                   |
| `timeout`           | int         | `10`          | Seconds before Docker daemon kill                                                                                                           |
| `tmpfs`             | bool        | `false`       | Use tmpfs for `/tmp`                                                                                                                        |
| `discovery`         | list        | —             | Services this app provides for HA discovery                                                                                                 |
| `services`          | list        | —             | Service dependencies: `service:provide`, `service:want`, `service:need`                                                                     |
| `breaking_versions` | list        | —             | Versions requiring manual update                                                                                                            |
| `panel_icon`        | string      | `mdi:puzzle`  | MDI icon for sidebar panel                                                                                                                  |
| `panel_title`       | string      | —             | Custom sidebar panel title                                                                                                                  |
| `panel_admin`       | bool        | `true`        | Restrict panel to admin users                                                                                                               |
| `webui`             | string      | —             | External web UI URL template                                                                                                                |
| `environment`       | dict        | —             | Environment variables for the container                                                                                                     |
| `host_dbus`         | bool        | `false`       | Map host D-Bus into the app                                                                                                                 |
| `host_pid`          | bool        | `false`       | Share host PID namespace (not protected only)                                                                                               |
| `host_ipc`          | bool        | `false`       | Share IPC namespace                                                                                                                         |
| `host_uts`          | bool        | `false`       | Use host UTS namespace                                                                                                                      |
| `kernel_modules`    | bool        | `false`       | Map host kernel modules (read-only)                                                                                                         |
| `realtime`          | bool        | `false`       | Host schedule access with `SYS_NICE`                                                                                                        |
| `journald`          | bool        | `false`       | Map host system journal (read-only)                                                                                                         |
| `udev`              | bool        | `false`       | Mount host udev database (read-only)                                                                                                        |
| `devicetree`        | bool        | `false`       | Map `/device-tree`                                                                                                                          |
| `legacy`            | bool        | `false`       | Enable legacy mode for images without `hass.io` labels                                                                                      |
| `ulimits`           | dict        | —             | Resource limits (e.g., `nofile`) as int or `{soft, hard}`                                                                                   |

### Full Configuration Example

```yaml
name: "My Smart App"
version: "2.1.0"
slug: "my_smart_app"
description: "A feature-rich app for Home Assistant"
url: "https://github.com/user/ha-my-smart-app"
arch:
  - aarch64
  - amd64
  - armv7
startup: services
boot: auto
ports:
  8080/tcp: 8080
  1883/tcp: null
ports_description:
  8080/tcp: "Web interface"
  1883/tcp: "MQTT (disabled by default)"
map:
  - type: homeassistant_config
    read_only: true
  - type: ssl
  - type: share
    read_only: false
homeassistant: "2024.1.0"
homeassistant_api: true
hassio_api: true
hassio_role: default
ingress: true
ingress_port: 8080
auth_api: true
init: false
panel_icon: mdi:robot
panel_title: "Smart App"
watchdog: "http://[HOST]:[PORT:8080]/health"
options:
  mqtt_host: ""
  mqtt_port: 1883
  log_level: "info"
schema:
  mqtt_host: str
  mqtt_port: port
  log_level: "list(debug|info|warning|error)"
image: "ghcr.io/user/{arch}-my-smart-app"
```

### Options & Schema Validation

The `options` key defines defaults; `schema` defines validation rules. Set a default to `null` to make an option **mandatory** (user must provide a value before the app starts).

**Supported schema types:**

| Type                    | Variants                                       | Description                             |
| ----------------------- | ---------------------------------------------- | --------------------------------------- |
| `str`                   | `str(min,)`, `str(,max)`, `str(min,max)`       | String with optional length constraints |
| `bool`                  | —                                              | Boolean true/false                      |
| `int`                   | `int(min,)`, `int(,max)`, `int(min,max)`       | Integer with optional range             |
| `float`                 | `float(min,)`, `float(,max)`, `float(min,max)` | Floating point with optional range      |
| `email`                 | —                                              | Valid email address                     |
| `url`                   | —                                              | Valid URL                               |
| `password`              | —                                              | Password field (masked in UI)           |
| `port`                  | —                                              | Valid network port number               |
| `match(REGEX)`          | —                                              | Match against a regular expression      |
| `list(val1\|val2\|...)` | —                                              | Enumerated list of allowed values       |
| `device`                | `device(subsystem=tty)`                        | Device path with optional filter        |

**Making an option truly optional** (no default, not required): use `?` suffix in the schema and omit from `options`:

```yaml
options:
  required_name: "World"
  required_port: 8080
schema:
  required_name: str
  required_port: port
  optional_debug: "bool?" # Truly optional — no default, not required
  optional_label: "str?" # Truly optional
```

**Nested structures (max depth 2):**

```yaml
options:
  logins:
    - username: admin
      password: "secret"
schema:
  logins:
    - username: str
      password: password
```

**Removing deprecated options programmatically (Bashio):**

```bash
options=$(bashio::addon.options)
old_key='deprecated_option'
if bashio::jq.exists "${options}" ".${old_key}"; then
    bashio::log.info "Removing ${old_key}"
    bashio::addon.option "${old_key}"
fi
```

## App Dockerfile

All apps are based on Alpine Linux base images. Home Assistant automatically substitutes the correct base image per architecture.

### Standard Dockerfile Template

```dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for app
RUN \
  apk add --no-cache \
    python3 \
    py3-pip

# Copy data for app
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
```

### Build Arguments

| Arg             | Description                                    |
| --------------- | ---------------------------------------------- |
| `BUILD_FROM`    | Dynamic base image for the target architecture |
| `BUILD_VERSION` | App version read from `config.yaml`            |
| `BUILD_ARCH`    | Current build architecture                     |

### Architecture-Specific Dockerfiles

You can suffix the Dockerfile for architecture-specific builds:

```
Dockerfile          # Default
Dockerfile.amd64    # AMD64-specific
Dockerfile.aarch64  # ARM64-specific
```

### Required Labels (for non-local builds)

```dockerfile
LABEL \
  io.hass.version="VERSION" \
  io.hass.type="addon" \
  io.hass.arch="armhf|aarch64|i386|amd64"
```

## App Script (`run.sh`)

The entry point script runs when the container starts. All HA app base images come with [Bashio](https://github.com/hassio-addons/bashio) pre-installed for common operations.

### Reading Options

```bash
#!/usr/bin/with-contenv bashio

# Read options from /data/options.json via Bashio
TARGET=$(bashio::config 'target')
LOG_LEVEL=$(bashio::config 'log_level')

bashio::log.info "Starting with target=${TARGET}, log_level=${LOG_LEVEL}"
```

### Key Runtime Paths

| Path                 | Description                                     |
| -------------------- | ----------------------------------------------- |
| `/data`              | Persistent storage volume                       |
| `/data/options.json` | User configuration (JSON)                       |
| `/config`            | Mapped `addon_config` directory (if configured) |
| `/share`             | Shared HA files (if mapped)                     |
| `/ssl`               | SSL certificates (if mapped)                    |
| `/homeassistant`     | HA config directory (if mapped)                 |

## Extended Build Configuration (`build.yaml`)

Use `build.yaml` for custom base images, extra build args, labels, and code signing:

```yaml
build_from:
  aarch64: mycustom/base-image:latest
  amd64: mycustom/amd64-image:latest
args:
  MY_BUILD_ARG: xy
labels:
  org.opencontainers.image.title: "My App"
codenotary:
  signer: dev@example.com
  base_image: notary@home-assistant.io
```

| Key                     | Required | Description                                                                     |
| ----------------------- | -------- | ------------------------------------------------------------------------------- |
| `build_from`            | no       | Architecture → base image mapping                                               |
| `args`                  | no       | Additional Docker build arguments                                               |
| `labels`                | no       | Additional Docker labels                                                        |
| `codenotary`            | no       | Codenotary CAS signing configuration                                            |
| `codenotary.signer`     | no       | Signer email for image verification                                             |
| `codenotary.base_image` | no       | Email to verify base image (use `notary@home-assistant.io` for official images) |

## App Communication

### Internal Network

All apps share an internal Docker network and can communicate using hostnames:

- **Name format:** `{REPO}_{SLUG}` (e.g., `local_my_addon`, `a1b2c3_my_addon`)
- **DNS hostname:** Replace `_` with `-` (e.g., `local-my-addon`)
- Apps on host network can reach internal apps by name, but not vice versa — use **aliases** for bidirectional access.
- Use `supervisor` as the hostname for the Supervisor API.

### Communicating with Home Assistant Core

Enable `homeassistant_api: true` in `config.yaml`, then use the internal proxy:

```bash
#!/usr/bin/with-contenv bashio

# REST API via internal proxy (auto-authenticated)
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  -H "Content-Type: application/json" \
  http://supervisor/core/api/config

# WebSocket API
# Connect to: ws://supervisor/core/websocket
# Use SUPERVISOR_TOKEN as password
```

- The `SUPERVISOR_TOKEN` environment variable is automatically injected.
- REST endpoint: `http://supervisor/core/api/`
- WebSocket endpoint: `ws://supervisor/core/websocket`

### Communicating with the Supervisor API

Enable `hassio_api: true` and optionally set `hassio_role`:

```bash
#!/usr/bin/with-contenv bashio

# Get Supervisor info
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/info
```

**API calls available without `hassio_api: true`:**

- `/core/api`, `/core/api/stream`, `/core/websocket`
- `/addons/self/*`
- `/services*`, `/discovery*`
- `/info`

### Services API (Inter-App Service Discovery)

Apps can discover shared services (MQTT, MySQL) without user configuration:

```bash
#!/usr/bin/with-contenv bashio

# Discover MQTT service
MQTT_HOST=$(bashio::services mqtt "host")
MQTT_USER=$(bashio::services mqtt "username")
MQTT_PASSWORD=$(bashio::services mqtt "password")

# Use in your app
mosquitto_sub -h "${MQTT_HOST}" -u "${MQTT_USER}" -P "${MQTT_PASSWORD}" -t "#"
```

Declare service usage in `config.yaml`:

```yaml
services:
  - mqtt:want # Can use MQTT if available
  - mysql:need # Requires MySQL to function
```

Service relationship types:

- `provide` — this app provides the service
- `want` — this app can optionally use the service
- `need` — this app requires the service to work

## Ingress (Embedded Web UI)

Ingress allows users to access your app's web interface directly through the Home Assistant UI, with authentication handled automatically by HA.

### Ingress Configuration

```yaml
# config.yaml
ingress: true
ingress_port: 8099 # Default; change if your server uses a different port
ingress_entry: / # URL entry point
```

### Ingress Requirements

1. Set `ingress: true` in `config.yaml`
2. Your web server must listen on the configured `ingress_port` (default `8099`)
3. **Only allow connections from `172.30.32.2`** — deny all other IPs
4. Users are pre-authenticated by HA — no additional auth needed

### Ingress Supports

- HTTP/1.x
- Streaming content
- WebSockets

### Nginx Ingress Example

**ingress.conf:**

```nginx
server {
    listen 8099;
    allow  172.30.32.2;
    deny   all;
}
```

**Dockerfile:**

```dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk --no-cache add \
    nginx \
  && mkdir -p /run/nginx

COPY ingress.conf /etc/nginx/http.d/

CMD [ "nginx", "-g", "daemon off;error_log /dev/stdout debug;" ]
```

**config.yaml:**

```yaml
name: "Ingress Example"
version: "1.0.0"
slug: "nginx-ingress-example"
description: "Ingress testing"
arch:
  - amd64
  - armhf
  - armv7
  - i386
ingress: true
```

### User Identification via Ingress Headers

When accessed via Ingress, the Supervisor injects user identity headers:

| Header                       | Description              |
| ---------------------------- | ------------------------ |
| `X-Remote-User-Id`           | Authenticated HA user ID |
| `X-Remote-User-Name`         | Username                 |
| `X-Remote-User-Display-Name` | Display name             |

## App Translations

Provide localized configuration labels in `translations/{language_code}.yaml`:

```yaml
# translations/en.yaml
configuration:
  ssl:
    name: Enable SSL
    description: Enable usage of SSL on the webserver inside the app
  ssh:
    name: SSH Options
    description: Configure SSH authentication options
    fields:
      public_key:
        name: Public Key
        description: Client Public Key
      private_key:
        name: Private Key
        description: Client Private Key

network:
  80/TCP: The webserver port (Not used for Ingress)
```

- `configuration` keys must match keys in your `schema`
- `network` keys must match keys in your `ports`
- Use valid language codes from the [HA frontend translations metadata](https://github.com/home-assistant/frontend/blob/dev/src/translations/translationMetadata.json)

## App Repositories

### Repository Structure

A repository is a Git repo containing one or more app directories plus a `repository.yaml` at the root:

```
my-ha-apps/
  repository.yaml
  addon_a/
    config.yaml
    Dockerfile
    ...
  addon_b/
    config.yaml
    Dockerfile
    ...
```

### Repository Configuration (`repository.yaml`)

```yaml
name: My Home Assistant Apps
url: https://github.com/user/my-ha-apps
maintainer: Your Name <email@example.com>
```

| Key          | Required | Description             |
| ------------ | -------- | ----------------------- |
| `name`       | yes      | Repository display name |
| `url`        | no       | Repository homepage     |
| `maintainer` | no       | Contact info            |

### Installing a Repository

Users add repositories via: **Settings → Apps → App Store → ⋮ → Repositories**

You can provide a [my.home-assistant.io](https://my.home-assistant.io/create-link/) link for one-click installation.

### Stable and Canary Branches

Offer multiple release channels using Git branches:

```
https://github.com/user/my-ha-apps          # stable
https://github.com/user/my-ha-apps#beta     # beta channel
https://github.com/user/my-ha-apps#next     # canary/next channel
```

Use different repository names per branch (e.g., "My App (stable)" vs. "My App (beta)").

## Testing

### Recommended: VS Code Devcontainer

The fastest development workflow uses the official devcontainer:

1. Install the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) VS Code extension
2. Copy [devcontainer.json](https://github.com/home-assistant/devcontainer/raw/main/addons/devcontainer.json) to `.devcontainer/devcontainer.json`
3. Copy [tasks.json](https://github.com/home-assistant/devcontainer/raw/main/addons/tasks.json) to `.vscode/tasks.json`
4. Open in VS Code → "Reopen in Container"
5. Run task: **Terminal → Run Task → "Start Home Assistant"**
6. Access HA at `http://localhost:7123/`
7. Your apps appear automatically under **Local Apps**

### Remote Development

For hardware-dependent apps, copy files to a real device's `/addons` directory via Samba or SSH. **Comment out the `image` key** in `config.yaml` to force local builds:

```yaml
# image: ghcr.io/user/{arch}-my-addon   # Comment out for local build
```

### Local Docker Build

Using the official builder:

```bash
docker run \
  --rm -it --name builder --privileged \
  -v /path/to/addon:/data \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  ghcr.io/home-assistant/amd64-builder \
  -t /data --all --test \
  -i my-test-addon-{arch} -d local
```

Using standalone Docker:

```bash
docker build \
  --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base:latest" \
  -t local/my-test-addon \
  .
```

### Local Docker Run

```bash
docker run \
  --rm \
  -v /tmp/my_test_data:/data \
  -p 8080:8080 \
  local/my-test-addon
```

### Base Images

| Architecture | Base Image                                   |
| ------------ | -------------------------------------------- |
| `amd64`      | `ghcr.io/home-assistant/amd64-base:latest`   |
| `aarch64`    | `ghcr.io/home-assistant/aarch64-base:latest` |
| `armhf`      | `ghcr.io/home-assistant/armhf-base:latest`   |
| `armv7`      | `ghcr.io/home-assistant/armv7-base:latest`   |
| `i386`       | `ghcr.io/home-assistant/i386-base:latest`    |

### Logs

All `stdout` and `stderr` output goes to Docker logs, viewable from the app page in the Supervisor panel.

## Publishing

### Pre-Built Containers (Recommended)

Build images for each architecture and push to a container registry. This provides fast, reliable installs for users.

**Using the official builder (from a Git repo):**

```bash
docker run \
  --rm --privileged \
  -v ~/.docker/config.json:/root/.docker/config.json:ro \
  ghcr.io/home-assistant/amd64-builder \
  --all \
  -t addon-folder \
  -r https://github.com/user/addons \
  -b main
```

**Using the official builder (local directory):**

```bash
docker run \
  --rm --privileged \
  -v ~/.docker/config.json:/root/.docker/config.json:ro \
  -v /my_addon:/data \
  ghcr.io/home-assistant/amd64-builder \
  --all \
  -t /data
```

**Image naming with `{arch}` substitution in `config.yaml`:**

```yaml
image: "ghcr.io/user/{arch}-addon-name"
```

The `{arch}` placeholder is replaced with the user's architecture at install time.

**Workflow tip:** Use a separate `build` branch or PR for building. After pushing images, merge to `main`. The default branch should always match the latest container registry tag.

### Locally Built Containers

Apps without the `image` key will be built on the user's device. This is simpler for development but creates slower installs and more SD card wear. **Migrate to pre-built containers** once your app is established.

## Presentation Best Practices

### Documentation Files

| File           | Purpose                                                                   |
| -------------- | ------------------------------------------------------------------------- |
| `README.md`    | Short intro shown in the app store                                        |
| `DOCS.md`      | Detailed user documentation (configuration, troubleshooting, license)     |
| `CHANGELOG.md` | Version history following [Keep a Changelog](https://keepachangelog.com/) |

### Icons and Logos

| Asset | File       | Format | Size                   |
| ----- | ---------- | ------ | ---------------------- |
| Icon  | `icon.png` | PNG    | 128×128px (1:1 square) |
| Logo  | `logo.png` | PNG    | ~250×100px             |

## Security

### Security Rating System

Every app starts with a base score of **5** (out of 6). Actions during development adjust the score:

| Action                                                                                                                         | Score Impact | Notes                           |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------ | ------------------------------- |
| `ingress: true`                                                                                                                | **+2**       | Overrides `auth_api` rating     |
| `auth_api: true`                                                                                                               | **+1**       | Overridden by Ingress           |
| Codenotary CAS signed                                                                                                          | **+1**       | —                               |
| Custom `apparmor.txt`                                                                                                          | **+1**       | Applied after installation      |
| `apparmor: false`                                                                                                              | **-1**       | —                               |
| `privileged` with `NET_ADMIN`, `SYS_ADMIN`, `SYS_RAWIO`, `SYS_PTRACE`, `SYS_MODULE`, or `DAC_READ_SEARCH`; or `kernel_modules` | **-1**       | Applied once even if multiple   |
| `hassio_role: manager`                                                                                                         | **-1**       | —                               |
| `host_network: true`                                                                                                           | **-1**       | —                               |
| `hassio_role: admin`                                                                                                           | **-2**       | —                               |
| `host_pid: true`                                                                                                               | **-2**       | —                               |
| `host_uts: true` + `privileged: SYS_ADMIN`                                                                                     | **-1**       | —                               |
| `full_access: true`                                                                                                            | **Set to 1** | Overrides all other adjustments |
| `docker_api: true`                                                                                                             | **Set to 1** | Overrides all other adjustments |

### API Roles

| Role            | Access Level                                |
| --------------- | ------------------------------------------- |
| `default`       | Info-level API calls only                   |
| `homeassistant` | All Home Assistant API endpoints            |
| `backup`        | All backup API endpoints                    |
| `manager`       | Extended rights for CLI-type apps           |
| `admin`         | Full API access; can toggle protection mode |

### Best Practices for Secure Apps

1. **Don't run on host network** unless absolutely necessary
2. **Create a custom AppArmor profile** (`apparmor.txt`) for a +1 security boost
3. **Map folders read-only** unless write access is genuinely needed
4. **Minimize API permissions** — use the lowest `hassio_role` that works
5. **Sign images with Codenotary CAS** for a +1 security boost
6. **Use Ingress** instead of exposing ports directly (+2 security boost)
7. **Use HA auth backend** instead of custom credentials (`auth_api: true`)

### AppArmor Profile Template

```
#include <tunables/global>

profile ADDON_SLUG flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Capabilities
  file,
  signal (send) set=(kill,term,int,hup,cont),

  # S6-Overlay
  /init ix,
  /bin/** ix,
  /usr/bin/** ix,
  /run/{s6,s6-rc*,service}/** ix,
  /package/** ix,
  /command/** ix,
  /etc/services.d/** rwix,
  /etc/cont-init.d/** rwix,
  /etc/cont-finish.d/** rwix,
  /run/{,**} rwk,
  /dev/tty rw,

  # Bashio
  /usr/lib/bashio/** ix,
  /tmp/** rwk,

  # App data
  /data/** rw,

  # Service profile
  /usr/bin/myprogram cx -> myprogram,

  profile myprogram flags=(attach_disconnected,mediate_deleted) {
    #include <abstractions/base>

    signal (receive) peer=*_ADDON_SLUG,

    /data/** rw,
    /share/** rw,

    /usr/bin/myprogram r,
    /bin/bash rix,
    /bin/echo ix,
    /etc/passwd r,
    /dev/tty rw,
  }
}
```

**Steps to create a custom AppArmor profile:**

1. Start with minimum required access
2. Add `complain` flag to the profile for testing
3. Run the app and review audit log: `journalctl _TRANSPORT="audit" -g 'apparmor="ALLOWED"'`
4. Add access rules for every allowed action
5. Remove `complain` flag so violations are **denied** not just logged
6. Repeat when updating the service

### Protection Mode

All apps run in protection-enabled mode by default, restricting system access. Options like `full_access`, `docker_api`, and `host_pid` are only available when protection is disabled. **Use with extreme caution.**

### Authenticating via HA User Backend

Instead of storing credentials in plain text config:

```yaml
# config.yaml
auth_api: true
```

Then validate credentials against HA's auth backend via the Supervisor Auth API endpoint.

## App Advanced Options (`addon_config`)

For apps that need user-provided files (custom configs, binary files, etc.):

1. Add `addon_config` to `map` in `config.yaml` (use `addon_config:rw` if write access is needed)
2. Users place files in `/addon_configs/{REPO}_{SLUG}/`
3. Files are mounted at `/config` inside the container
4. Provide an option in your schema for the file path, or document a fixed filename

**Use cases:**

- Complex configuration files that an internal service reads directly
- Binary files or certificates
- Live-reloading config for internal services
- Output files for user access (logs, databases, generated files)

## Common Patterns

### Pattern 1: Minimal "Hello World" App

**config.yaml:**

```yaml
name: "Hello World"
description: "My first real app!"
version: "1.0.0"
slug: "hello_world"
init: false
arch:
  - aarch64
  - amd64
  - armhf
  - armv7
  - i386
```

**Dockerfile:**

```dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
```

**run.sh:**

```bash
#!/usr/bin/with-contenv bashio

echo "Hello world!"
```

### Pattern 2: Python HTTP Server with Port Exposure

**config.yaml:**

```yaml
name: "Hello World"
description: "My first real app!"
version: "1.1.0"
slug: "hello_world"
init: false
arch:
  - aarch64
  - amd64
  - armhf
  - armv7
  - i386
startup: services
ports:
  8000/tcp: 8000
options: {}
schema: {}
```

**Dockerfile:**

```dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3

WORKDIR /data

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
```

**run.sh:**

```bash
#!/usr/bin/with-contenv bashio

echo "Hello world!"
python3 -m http.server 8000
```

### Pattern 3: App with Options and HA API Access

**config.yaml:**

```yaml
name: "Smart Monitor"
version: "1.0.0"
slug: "smart_monitor"
description: "Monitors entities and sends notifications"
arch:
  - aarch64
  - amd64
startup: application
homeassistant_api: true
ingress: true
ingress_port: 8099
init: false
options:
  entities: []
  refresh_interval: 30
schema:
  entities:
    - str
  refresh_interval: "int(5,3600)"
```

**run.sh:**

```bash
#!/usr/bin/with-contenv bashio

REFRESH=$(bashio::config 'refresh_interval')

bashio::log.info "Starting Smart Monitor (refresh every ${REFRESH}s)"

while true; do
  # Call HA API to get entity states
  STATES=$(curl -s \
    -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
    -H "Content-Type: application/json" \
    http://supervisor/core/api/states)

  bashio::log.info "Fetched states successfully"
  sleep "${REFRESH}"
done
```

### Pattern 4: Service Provider App (MQTT)

```yaml
# config.yaml
name: "Custom MQTT Broker"
version: "2.0.0"
slug: "custom_mqtt"
description: "Custom MQTT broker with advanced features"
arch:
  - aarch64
  - amd64
startup: services
ports:
  1883/tcp: 1883
  9001/tcp: null
services:
  - mqtt:provide
discovery:
  - mqtt
options:
  persistence: true
  max_connections: 100
schema:
  persistence: bool
  max_connections: "int(1,10000)"
```

### Pattern 5: GitHub Actions CI/CD for App Publishing

```yaml
# .github/workflows/publish.yml
name: Publish App
on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          platforms: linux/amd64,linux/arm64,linux/arm/v7
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.event.release.tag_name }}
            ghcr.io/${{ github.repository }}:latest
```

## Troubleshooting

### App Not Appearing in Store

1. Press **Ctrl+F5** (Windows/Linux) or **Cmd+Shift+R** (macOS) to clear browser cache
2. Check **Settings → System → Logs → Supervisor** for validation errors
3. Verify `config.yaml` is valid YAML (use [yamllint.com](http://www.yamllint.com/))
4. Ensure `slug` is unique and URI-friendly
5. Click "Check for updates" in the App Store

### App Won't Start

1. Check Docker logs via the app's "Log" tab in the Supervisor panel
2. Verify `run.sh` uses **LF line endings** (not CRLF)
3. Ensure `run.sh` is executable (`chmod a+x run.sh`)
4. If using S6 Overlay v3+, set `init: false` in `config.yaml`

### Config Changes Not Taking Effect

1. Bump the `version` in `config.yaml`
2. Click "Check for updates" → Reinstall
3. Or: uninstall and reinstall the app

## References

- [Home Assistant App Developer Documentation](https://developers.home-assistant.io/docs/apps/)
- [Tutorial: Making Your First App](https://developers.home-assistant.io/docs/apps/tutorial)
- [App Configuration Reference](https://developers.home-assistant.io/docs/apps/configuration)
- [App Communication](https://developers.home-assistant.io/docs/apps/communication)
- [Local App Testing](https://developers.home-assistant.io/docs/apps/testing)
- [Publishing Your App](https://developers.home-assistant.io/docs/apps/publishing)
- [Presenting Your App](https://developers.home-assistant.io/docs/apps/presentation)
- [App Repositories](https://developers.home-assistant.io/docs/apps/repository)
- [App Security](https://developers.home-assistant.io/docs/apps/security)
- [Supervisor API](https://developers.home-assistant.io/docs/api/supervisor/endpoints)
- [Bashio Library](https://github.com/hassio-addons/bashio)
- [Example App Repository](https://github.com/home-assistant/addons-example)
- [Home Assistant Core Apps](https://github.com/home-assistant/addons)
- [Home Assistant Docker Base Images](https://github.com/home-assistant/docker-base)
- [Home Assistant Builder](https://github.com/home-assistant/builder)
- [Community Apps](https://github.com/hassio-addons)
- [Home Assistant Devcontainer](https://github.com/home-assistant/devcontainer)
