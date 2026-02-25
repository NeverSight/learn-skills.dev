---
name: hytale-server-admin
description: Hytale server setup, configuration, and administration. Covers config.json, permissions.json, authentication, port forwarding, hosting options, and going public. Use when setting up a server, configuring permissions, troubleshooting connection issues, or planning server infrastructure.
---

# Hytale Server Administration

Set up, configure, and manage Hytale servers.

## Server Planning Questions

Before setting up, work through these questions with the server owner:

### Phase 1: Private Server

| Question | Options | Notes |
|----------|---------|-------|
| Where will you host? | Local PC, VPS, Game Host | Local = free, VPS = flexible, Host = easy |
| Who will have access? | Friends list (whitelist) | Start restricted |
| Starting vanilla or modded? | Vanilla first is great! | Can add mods anytime |
| World seed? | Random, specific | Can make new worlds later |
| Backups? | Manual, automated | Set schedule before playing |

> **Tip**: Starting vanilla is perfectly fine! You can add mods later - just make a new world if needed. Many groups prefer to learn vanilla first anyway!

### Phase 2: Going Public

| Question | Options | Notes |
|----------|---------|-------|
| Expected player count? | 10, 50, 100+ | Affects RAM/hosting needs |
| Moderation team? | Solo, trusted friends, hired | Plan roles |
| Rules? | PvP, griefing, chat | Document before opening |
| Server listing? | Private, public discovery | Authentication level |
| Anti-cheat? | Plugins, vanilla | Consider early |
| DDoS protection? | Host-provided, Cloudflare | Required for public |

---

## Requirements

### Hardware (Self-Hosting)

| Players | RAM | CPU | Notes |
|---------|-----|-----|-------|
| 1-5 | 4GB | 2 cores | Minimum |
| 5-20 | 8GB | 4 cores | Recommended |
| 20-50 | 16GB | 6 cores | With mods |
| 50+ | 32GB+ | 8+ cores | Heavy mods |

### Software

- **Java 25** (required)
- **HytaleServer.jar** (from Hytale)
- **Assets.zip** (game assets)

---

## Initial Setup

### Step 1: Download Server Files

1. Download `HytaleServer.jar` from official source
2. Download `Assets.zip` (game assets)
3. Place in a dedicated folder

### Step 2: First Launch

```bash
# Windows
java -Xmx4G -jar HytaleServer.jar --assets ./Assets.zip

# Linux
java -Xmx4G -jar HytaleServer.jar --assets ./Assets.zip
```

This creates the folder structure:
```
server/
├── HytaleServer.jar
├── Assets.zip
├── config.json            # Server settings
├── permissions.json       # Player permissions
├── whitelist.json         # Allowed players
├── bans.json              # Banned players
└── universe/
    └── worlds/
        └── default/
            └── config.json  # World settings
```

### Step 3: Authenticate

```bash
# In server console
/auth login device
```

1. Copy the URL and code shown
2. Visit URL in browser
3. Enter code to authenticate
4. Server can now accept connections

---

## Configuration Files

### config.json (Main Server)

```json
{
  "ServerName": "My Hytale Server",
  "MOTD": "Welcome to our server!",
  "Password": "",
  "MaxPlayers": 20,
  "MaxViewRadius": 12,
  "LocalCompressionEnabled": true
}
```

| Setting | Description |
|---------|-------------|
| `ServerName` | Displayed to players |
| `MOTD` | Message of the day |
| `Password` | Empty = no password |
| `MaxPlayers` | Concurrent player limit |
| `MaxViewRadius` | Render distance |

### World config.json

Located in `universe/worlds/[name]/config.json`:

```json
{
  "seed": "my-custom-seed",
  "pvp": true,
  "fallDamage": true,
  "keepInventory": false,
  "difficulty": "normal"
}
```

---

## Permissions System

### permissions.json Structure

```json
{
  "groups": {
    "default": {
      "permissions": [
        "hytale.command.help",
        "hytale.command.spawn"
      ]
    },
    "moderator": {
      "inherits": ["default"],
      "permissions": [
        "hytale.command.kick",
        "hytale.command.mute",
        "hytale.command.tp"
      ]
    },
    "admin": {
      "inherits": ["moderator"],
      "permissions": [
        "hytale.command.*",
        "hytale.admin.*"
      ]
    }
  },
  "users": {
    "player-uuid-here": {
      "groups": ["admin"]
    }
  }
}
```

### Permission Commands

```bash
# Grant operator status
/op add <username>

# Remove operator status
/op remove <username>

# View player permissions
/permissions user <username> info
```

---

## Networking

### Port Configuration

| Protocol | Port | Purpose |
|----------|------|---------|
| UDP | 5520 | Game traffic (default) |

**Important**: Hytale uses **UDP**, not TCP!

### Firewall Rules

**Windows PowerShell (Admin):**
```powershell
New-NetFirewallRule -DisplayName "Hytale Server" -Direction Inbound -Protocol UDP -LocalPort 5520 -Action Allow
```

**Linux (ufw):**
```bash
sudo ufw allow 5520/udp
```

**Linux (iptables):**
```bash
sudo iptables -A INPUT -p udp --dport 5520 -j ACCEPT
```

### Port Forwarding (Home Router)

1. Access router admin (usually 192.168.1.1)
2. Find Port Forwarding section
3. Add rule:
   - Protocol: **UDP**
   - External Port: **5520**
   - Internal IP: Your server PC's IP
   - Internal Port: **5520**

### Custom Port

```bash
java -jar HytaleServer.jar --assets ./Assets.zip --bind 0.0.0.0:25565
```

---

## Private Server Setup

### Whitelist-Only Access

Edit `whitelist.json`:
```json
{
  "enabled": true,
  "players": [
    "friend1-uuid",
    "friend2-uuid"
  ]
}
```

Or use commands:
```bash
/whitelist add <username>
/whitelist remove <username>
/whitelist on
/whitelist off
```

### Password Protection

In `config.json`:
```json
{
  "Password": "secretpassword123"
}
```

---

## Going Public Checklist

### Before Launch

- [ ] **Rules documented** - Create /rules command
- [ ] **Moderation team ready** - Assign roles
- [ ] **Backup system working** - Test restore
- [ ] **Anti-grief plugins** - Protect builds
- [ ] **Reporting system** - How players report issues
- [ ] **DDoS protection** - If self-hosting

### Server Hardening

```json
{
  "MaxPlayers": 50,
  "RateLimit": {
    "ConnectionsPerIP": 2,
    "CommandsPerMinute": 30
  }
}
```

### Recommended Plugins

| Purpose | Examples |
|---------|----------|
| Permissions | HyperPerms |
| Economy | HyVault |
| Protection | WorldGuard-equivalent |
| Moderation | Essentials-equivalent |

---

## Hosting Options

### Self-Hosting

| Pros | Cons |
|------|------|
| Free | Your hardware/bandwidth |
| Full control | You handle maintenance |
| No monthly cost | Uptime depends on you |

### VPS Hosting

| Pros | Cons |
|------|------|
| Always online | Monthly cost ($10-50+) |
| Better bandwidth | Some technical knowledge |
| Scalable | You manage software |

**Recommended VPS**: 
- Hetzner, OVH, Linode, DigitalOcean

### Game Server Hosts

| Pros | Cons |
|------|------|
| Easy setup | Higher cost |
| Control panel | Less flexibility |
| Support included | Limited customization |

**Popular Hosts**:
- BisectHosting, Apex, Shockbyte, PebbleHost

---

## Common Commands

| Command | Description |
|---------|-------------|
| `/help` | List all commands |
| `/op add <user>` | Grant admin |
| `/kick <user>` | Kick player |
| `/ban <user>` | Ban player |
| `/whitelist add <user>` | Allow player |
| `/tp <user>` | Teleport to player |
| `/gamemode <mode>` | Change gamemode |
| `/plugin list` | List plugins |
| `/plugin reload` | Reload plugins |
| `/save-all` | Force world save |
| `/stop` | Gracefully stop server |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Players can't connect | Check firewall + port forward (UDP!) |
| Authentication failed | Re-run `/auth login device` |
| Server crashes | Check RAM allocation, reduce view distance |
| Lag | Lower MaxPlayers, optimize plugins |
| World corruption | Restore from backup |

---

## Backup Strategy

### Manual Backup

```bash
# Stop server first!
cp -r universe/ backup/universe_$(date +%Y%m%d)/
```

### Automated (Linux cron)

```bash
# Daily backup at 4 AM
0 4 * * * /path/to/backup-script.sh
```

---

## Quick Reference

| Task | Command/File |
|------|--------------|
| Start server | `java -Xmx4G -jar HytaleServer.jar --assets ./Assets.zip` |
| Authenticate | `/auth login device` |
| Main config | `config.json` |
| Permissions | `permissions.json` |
| Whitelist | `whitelist.json` / `/whitelist` |
| Default port | UDP 5520 |

---

## Resources

- **Official Manual**: [Hytale Server Manual](https://support.hytale.com/hc/en-us/articles/45326769420827)
- **Plugin Development**: See `hytale-plugin-dev` skill
- **Team Workflow**: See `git-workflow` skill
