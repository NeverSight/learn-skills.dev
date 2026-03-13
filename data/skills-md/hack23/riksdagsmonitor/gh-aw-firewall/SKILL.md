---
name: gh-aw-firewall
description: Network egress control for AI agents with domain whitelisting, Squid proxy, iptables enforcement, and secure credential management
license: Apache-2.0
version: 1.0.0
last_updated: 2026-02-17
tags: [github-agentic-workflows, network-security, firewall, squid, domain-whitelisting, egress-control]
---

# 🔥 GitHub Agentic Workflows - Firewall Skill

## 📋 Purpose

Master the **Agentic Workflow Firewall (AWF)** - a network firewall for agentic workflows providing L7 (HTTP/HTTPS) egress control using Squid proxy and Docker containers. This skill provides comprehensive expertise in restricting network access to a whitelist of approved domains for AI agents and their MCP servers.

## 🎯 Core Concepts

### What is AWF?

**AWF (Agentic Workflow Firewall)** is a network security layer that restricts AI agent network access to explicitly approved domains, preventing data exfiltration and unauthorized external communication.

**Key Features:**
- 🌐 **L7 Domain Whitelisting**: HTTP/HTTPS traffic control at application layer
- 🔒 **Host-Level Enforcement**: iptables DOCKER-USER chain for all containers
- 📦 **Chroot Mode**: Host binaries with network isolation
- 🔑 **API Proxy Sidecar**: Secure LLM credential management
- ✅ **Transparent**: Works with existing containers

### Security Model

```
┌────────────────────────────────────────────────┐
│          AI Agent Container                     │
│  ┌──────────────────────────────────────┐     │
│  │   Application Code                    │     │
│  │   (Read-only filesystem)              │     │
│  └───────────────┬──────────────────────┘     │
│                  │ Network Request             │
│                  ▼                              │
│  ┌──────────────────────────────────────┐     │
│  │   iptables DOCKER-USER Chain         │     │
│  │   (Force all traffic through Squid)  │     │
│  └───────────────┬──────────────────────┘     │
└──────────────────┼──────────────────────────────┘
                   │
                   ▼
   ┌───────────────────────────────┐
   │      Squid Proxy               │
   │  ┌─────────────────────────┐  │
   │  │  Domain Whitelist       │  │
   │  │  - github.com ✅        │  │
   │  │  - api.github.com ✅    │  │
   │  │  - evil.com ❌          │  │
   │  └─────────────────────────┘  │
   │                                │
   │  ┌─────────────────────────┐  │
   │  │  SSL Bump (HTTPS)       │  │
   │  │  (Content Inspection)   │  │
   │  └─────────────────────────┘  │
   └────────────┬──────────────────┘
                │
                ▼
         External Network
       (Allowed domains only)
```

## 🏗️ Architecture

### Three Operating Modes

#### 1. Standard Mode (Default)
```bash
awf --allow-domains github.com,api.github.com -- docker run myapp
```

**How it works:**
- Launches Squid proxy with domain whitelist
- Creates iptables rules in DOCKER-USER chain
- Runs command in Docker container
- All HTTP/HTTPS traffic forced through Squid
- Unauthorized domains blocked

#### 2. Chroot Mode
```bash
awf --chroot --allow-domains github.com -- python3 script.py
```

**How it works:**
- Uses host binaries (Python, Node.js, Go)
- Transparent network isolation
- No Docker container overhead
- Squid proxy still enforces whitelist

**Use Cases:**
- Faster startup (no container pull)
- Access to host tools
- Still network-isolated

#### 3. API Proxy Sidecar
```bash
awf --api-proxy --allow-domains api.openai.com,api.anthropic.com -- node agent.js
```

**How it works:**
- Node.js proxy for LLM API calls
- Credentials injected securely
- Tokens never exposed to AI agent
- All calls routed through Squid

## 🔧 Configuration

### CLI Usage

**Basic Command Structure:**
```bash
awf [firewall-options] -- [command-to-run]
```

The `--` separator divides firewall configuration from the command to execute.

### Domain Allowlisting

**Single Domain:**
```bash
awf --allow-domains github.com -- curl https://api.github.com
```

**Multiple Domains:**
```bash
awf --allow-domains github.com,api.openai.com,anthropic.com -- python agent.py
```

**Wildcard Subdomains:**
```bash
awf --allow-domains '*.github.com' -- npm install
```

**Domain File:**
```bash
# domains.txt
github.com
api.github.com
*.githubusercontent.com

awf --allow-domains-file domains.txt -- git clone https://github.com/repo
```

### Environment Variables

**Passing Variables to Container:**
```bash
awf --env API_KEY --env DEBUG -- node app.js
```

**With Values:**
```bash
awf --env API_KEY=secret123 -- python script.py
```

**From File:**
```bash
# .env file
API_KEY=secret123
DEBUG=true

awf --env-file .env -- npm start
```

### Installation

**Quick Install:**
```bash
curl -sSL https://raw.githubusercontent.com/github/gh-aw-firewall/main/install.sh | sudo bash
```

**Manual Install:**
```bash
npm install -g gh-aw-firewall
```

**Verify:**
```bash
awf --version
awf --help
```

## 🔐 API Proxy Sidecar

### Secure Credential Management

The API proxy sidecar provides secure credential management for LLM APIs (OpenAI, Anthropic) without exposing tokens to AI agents.

**Architecture:**

```
┌──────────────────────────────────────┐
│      AI Agent Container               │
│  ┌────────────────────────────┐      │
│  │  Code makes API call       │      │
│  │  http://localhost:8080/v1  │      │
│  │  (No API key in code)      │      │
│  └──────────────┬─────────────┘      │
└─────────────────┼────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │   API Proxy Sidecar         │
    │  ┌──────────────────────┐   │
    │  │ Inject Credentials   │   │
    │  │ Authorization: sk-xx │   │
    │  └──────────────────────┘   │
    │           │                  │
    │           ▼                  │
    │  ┌──────────────────────┐   │
    │  │  Route via Squid     │   │
    │  └──────────────────────┘   │
    └───────────┬─────────────────┘
                │
                ▼
         ┌─────────────┐
         │ Squid Proxy │
         │ (Whitelist) │
         └──────┬──────┘
                │
                ▼
        External API
     (api.openai.com)
```

**Configuration:**
```bash
# Export credentials (not visible to agent)
export OPENAI_API_KEY=sk-xxx
export ANTHROPIC_API_KEY=sk-ant-xxx

# Start with API proxy
awf --api-proxy \
    --allow-domains api.openai.com,api.anthropic.com \
    -- node agent.js
```

**Agent Code:**
```javascript
// Agent makes calls without credentials
fetch('http://localhost:8080/v1/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [...]
  })
});

// API proxy automatically injects:
// Authorization: Bearer sk-xxx
```

**Benefits:**
- ✅ Credentials never in agent code
- ✅ Tokens isolated in proxy
- ✅ All traffic still goes through Squid
- ✅ Domain whitelist enforced
- ✅ Logging and monitoring

### Implementation Example

**Go Proxy Server:**
```go
package main

import (
    "net/http"
    "net/http/httputil"
    "net/url"
    "os"
)

func main() {
    // Read credentials from environment
    openaiKey := os.Getenv("OPENAI_API_KEY")
    anthropicKey := os.Getenv("ANTHROPIC_API_KEY")
    
    // Squid proxy URL
    squidURL, _ := url.Parse("http://squid:3128")
    
    // Create reverse proxy
    proxy := httputil.NewSingleHostReverseProxy(squidURL)
    
    // Modify request to inject credentials
    director := proxy.Director
    proxy.Director = func(req *http.Request) {
        director(req)
        
        // Inject appropriate credential
        if req.Host == "api.openai.com" {
            req.Header.Set("Authorization", "Bearer "+openaiKey)
        } else if req.Host == "api.anthropic.com" {
            req.Header.Set("x-api-key", anthropicKey)
        }
        
        // Route through Squid
        req.URL.Host = req.Host
        req.URL.Scheme = "https"
    }
    
    http.ListenAndServe(":8080", proxy)
}
```

## 🌐 SSL Bump (HTTPS Inspection)

### Content Inspection

SSL Bump allows Squid to inspect HTTPS traffic for URL path filtering and content validation.

**Configuration:**
```squid
# Enable SSL Bump
http_port 3128 ssl-bump \
    cert=/etc/squid/certs/squid-ca-cert.pem \
    key=/etc/squid/certs/squid-ca-key.pem

# SSL Bump rules
acl step1 at_step SslBump1
ssl_bump peek step1
ssl_bump bump all

# URL path filtering
acl allowed_paths url_regex ^https://api\.github\.com/repos/
http_access allow allowed_paths
http_access deny all
```

**Use Cases:**
- ✅ Block specific URL paths
- ✅ Content validation
- ✅ Deep packet inspection
- ✅ Logging HTTPS requests

**Security Considerations:**
- ⚠️ Requires CA certificate in agent
- ⚠️ Man-in-the-middle by design
- ✅ Transparent to agent code
- ✅ Logs include HTTPS details

## 🔄 GitHub Actions Integration

### Basic Workflow

```yaml
name: Agentic Workflow with Firewall

on: pull_request

jobs:
  agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install AWF
        run: |
          curl -sSL https://raw.githubusercontent.com/github/gh-aw-firewall/main/install.sh | sudo bash
      
      - name: Run Agent with Firewall
        run: |
          awf --allow-domains github.com,api.github.com \
              -- node agent.js
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### MCP Server Configuration

```yaml
- name: Run MCP Server with Firewall
  run: |
    awf --allow-domains github.com,api.githubcopilot.com \
        --env GITHUB_TOKEN \
        -- docker run -i \
        -e GITHUB_TOKEN \
        ghcr.io/github/github-mcp-server:latest
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Multi-Stage Pipeline

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build with NPM Registry
        run: |
          awf --allow-domains registry.npmjs.org \
              -- npm install
      
      - name: Test with External APIs
        run: |
          awf --allow-domains api.github.com,api.openai.com \
              --api-proxy \
              -- npm test
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Deploy (No Network)
        run: |
          awf --allow-domains '' \
              -- npm run build
```

## 📊 Logging & Monitoring

### Log Files

**Squid Access Log:**
```bash
# Location
/var/log/squid/access.log

# Format
timestamp ip method url status bytes

# View recent
tail -f /var/log/squid/access.log

# Filter blocked requests
grep "TCP_DENIED" /var/log/squid/access.log
```

**Squid Cache Log:**
```bash
# Location
/var/log/squid/cache.log

# Contains
- Squid startup/shutdown
- Configuration errors
- Domain whitelist violations

# Monitor
tail -f /var/log/squid/cache.log
```

### Quick Reference

**View All Traffic:**
```bash
awf --log-level debug --allow-domains github.com -- curl https://api.github.com
```

**Filter by Domain:**
```bash
grep "github.com" /var/log/squid/access.log
```

**Count Requests:**
```bash
awk '{print $7}' /var/log/squid/access.log | sort | uniq -c | sort -rn
```

**Blocked Requests:**
```bash
grep "TCP_DENIED" /var/log/squid/access.log | awk '{print $7}' | sort | uniq
```

### Monitoring Metrics

**Prometheus Exporter:**
```yaml
# docker-compose.yml
services:
  squid-exporter:
    image: boynux/squid-exporter
    ports:
      - "9301:9301"
    environment:
      - SQUID_HOSTNAME=squid
      - SQUID_PORT=3128
```

**Grafana Dashboard:**
- Total requests
- Allowed vs denied
- Top domains
- Response times
- Cache hit rate

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Refused

**Symptom:**
```
Error: connect ECONNREFUSED 127.0.0.1:3128
```

**Diagnosis:**
```bash
# Check Squid is running
ps aux | grep squid

# Check Squid port
netstat -tlnp | grep 3128

# Check Squid logs
tail /var/log/squid/cache.log
```

**Solutions:**
- Ensure Squid container is running
- Verify iptables rules are applied
- Check Squid configuration syntax

#### 2. Domain Not Whitelisted

**Symptom:**
```
HTTP 403 Forbidden
TCP_DENIED/403
```

**Diagnosis:**
```bash
# Check domain in whitelist
grep "example.com" /etc/squid/allowed-domains.txt

# View denied requests
grep "TCP_DENIED" /var/log/squid/access.log | tail -20
```

**Solutions:**
- Add domain to whitelist
- Use wildcard: `*.example.com`
- Check for typos in domain name

#### 3. SSL Certificate Issues

**Symptom:**
```
Error: certificate verify failed
```

**Diagnosis:**
```bash
# Check CA certificate
ls -la /etc/squid/certs/

# Test SSL connection
openssl s_client -connect api.github.com:443 -proxy localhost:3128
```

**Solutions:**
- Install Squid CA certificate in container
- Disable SSL Bump if not needed
- Use `--insecure` flag for testing (not production)

#### 4. Performance Issues

**Symptom:**
- Slow response times
- High latency

**Diagnosis:**
```bash
# Check Squid CPU/memory
docker stats squid

# Monitor request timing
tail -f /var/log/squid/access.log | grep -o "TCP_[A-Z_]*"
```

**Solutions:**
- Increase Squid cache size
- Add more Squid workers
- Use connection pooling
- Enable HTTP/2

#### 5. Docker Networking

**Symptom:**
```
Error: network unreachable
```

**Diagnosis:**
```bash
# Check Docker network
docker network ls
docker network inspect awf-network

# Check iptables
sudo iptables -L DOCKER-USER -n -v
```

**Solutions:**
- Verify Docker network exists
- Check iptables rules are applied
- Restart Docker daemon

## ⚙️ Advanced Configuration

### Custom Squid Configuration

**squid.conf:**
```squid
# Basic ACLs
acl localnet src 172.16.0.0/12
acl SSL_ports port 443
acl Safe_ports port 80
acl CONNECT method CONNECT

# Allowed domains from file
acl allowed_domains dstdomain "/etc/squid/allowed-domains.txt"

# Deny CONNECT to other than SSL ports
http_access deny CONNECT !SSL_ports

# Allow only safe ports
http_access deny !Safe_ports

# Allow localhost
http_access allow localnet

# Allow only whitelisted domains
http_access allow allowed_domains

# Deny everything else
http_access deny all

# Logging
access_log /var/log/squid/access.log squid
cache_log /var/log/squid/cache.log

# Performance
cache_mem 256 MB
maximum_object_size 50 MB
cache_dir ufs /var/spool/squid 1000 16 256

# DNS
dns_nameservers 8.8.8.8 8.8.4.4
```

### Docker Compose Setup

```yaml
version: '3.8'

services:
  squid:
    image: ubuntu/squid:latest
    container_name: awf-squid
    ports:
      - "3128:3128"
    volumes:
      - ./squid.conf:/etc/squid/squid.conf:ro
      - ./allowed-domains.txt:/etc/squid/allowed-domains.txt:ro
      - squid-cache:/var/spool/squid
      - squid-logs:/var/log/squid
    networks:
      - awf-network
    restart: unless-stopped

  agent:
    image: myagent:latest
    depends_on:
      - squid
    environment:
      - HTTP_PROXY=http://squid:3128
      - HTTPS_PROXY=http://squid:3128
    networks:
      - awf-network

networks:
  awf-network:
    driver: bridge

volumes:
  squid-cache:
  squid-logs:
```

### iptables Rules

**Automatic (via AWF):**
```bash
awf --allow-domains github.com -- docker run myapp
# iptables rules applied automatically
```

**Manual:**
```bash
# Force all container traffic to Squid
sudo iptables -I DOCKER-USER -p tcp --dport 80 -j REDIRECT --to-port 3128
sudo iptables -I DOCKER-USER -p tcp --dport 443 -j REDIRECT --to-port 3128

# Verify rules
sudo iptables -L DOCKER-USER -n -v
```

## 🎯 Best Practices

### 1. Principle of Least Privilege

**❌ DON'T: Allow all subdomains**
```bash
awf --allow-domains '*' -- node agent.js
```

**✅ DO: Specific domains only**
```bash
awf --allow-domains api.github.com,api.openai.com -- node agent.js
```

### 2. Use API Proxy for Credentials

**❌ DON'T: Expose tokens to agent**
```javascript
const token = process.env.OPENAI_API_KEY;  // Visible to agent
```

**✅ DO: Use API proxy**
```bash
awf --api-proxy -- node agent.js  # Tokens in proxy only
```

### 3. Monitor and Audit

**Enable comprehensive logging:**
```bash
awf --log-level debug \
    --audit-log /var/log/awf/audit.log \
    --allow-domains github.com \
    -- python agent.py
```

**Review logs regularly:**
```bash
# Daily review
grep "TCP_DENIED" /var/log/squid/access.log | wc -l

# Alert on suspicious patterns
grep "evil.com" /var/log/squid/access.log && notify-admin
```

### 4. Test Firewall Rules

**Verify blocking:**
```bash
# Should succeed
awf --allow-domains github.com -- curl https://api.github.com

# Should fail
awf --allow-domains github.com -- curl https://evil.com
```

### 5. Performance Optimization

**Enable caching:**
```squid
cache_mem 512 MB
maximum_object_size 100 MB
cache_dir ufs /var/spool/squid 10000 16 256
```

**Use connection pooling:**
```squid
persistent_connection_timeout 60 seconds
client_persistent_connections on
server_persistent_connections on
```

### 6. Security Hardening

**Disable unnecessary features:**
```squid
# No FTP
acl FTP proto FTP
http_access deny FTP

# No HTTPS without SSL Bump
acl SSL_ports port 443
http_access deny CONNECT !SSL_ports
```

**Regular updates:**
```bash
# Update Squid
docker pull ubuntu/squid:latest

# Update AWF
npm update -g gh-aw-firewall
```

## 🔗 Related Skills

- **gh-aw-safe-outputs** - Controlled write operations
- **gh-aw-mcp-gateway** - MCP server routing
- **gh-aw-security-architecture** - Overall security model
- **gh-aw-containerization** - Docker patterns
- **gh-aw-authentication-credentials** - Credential management

## 📚 References

- [AWF Repository](https://github.com/github/gh-aw-firewall)
- [Quickstart Guide](https://github.com/github/gh-aw-firewall/docs/quickstart.md)
- [Chroot Mode](https://github.com/github/gh-aw-firewall/docs/chroot-mode.md)
- [API Proxy Sidecar](https://github.com/github/gh-aw-firewall/docs/api-proxy-sidecar.md)
- [GitHub Actions Integration](https://github.com/github/gh-aw-firewall/docs/github_actions.md)
- [Squid Documentation](http://www.squid-cache.org/Doc/)

## ✅ Remember

- ✅ AWF provides L7 domain whitelisting
- ✅ iptables enforces rules at host level
- ✅ Three modes: Standard, Chroot, API Proxy
- ✅ Use API proxy for credential isolation
- ✅ SSL Bump enables HTTPS inspection
- ✅ Monitor logs for security events
- ✅ Test firewall rules before production
- ✅ Principle of least privilege (minimal domains)
- ✅ Regular security updates
- ✅ Works transparently with containers

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-17  
**Maintained by**: Hack23 AB
