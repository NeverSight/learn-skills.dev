---
name: chrome-devtools
description: Chrome debugging and inspection via local CDP Docker container
category: debugging
triggers: [debug, inspect, devtools, performance, network, chrome, CDP]
docker_required: true
ruby_required: true
---

# Chrome DevTools Protocol Skill

## Purpose
Provides Chrome DevTools Protocol (CDP) access through a local Docker container, enabling browser debugging, network inspection, performance profiling, and DOM manipulation without remote MCP dependencies.

## Capabilities
- **Page Control**: Navigate, reload, screenshot
- **JavaScript Execution**: Evaluate scripts in browser context
- **Network Monitoring**: Capture requests, responses, timing
- **DOM Inspection**: Query and manipulate DOM elements
- **Performance**: Profiling, metrics, Core Web Vitals
- **Console**: Capture console logs and errors

## Requirements

### Docker
- Docker Desktop installed and running
- `agent-network` Docker network created
- Chrome DevTools container running

### Ruby
- Ruby ≥2.7
- Gems: `websocket-client-simple`, `json`, `net-http`

### Setup
```bash
# Start Chrome DevTools container
cd ~/.claude/skills/chrome-devtools/docker
docker-compose up -d

# Verify container is running
docker ps | grep chrome-devtools-server

# Check CDP endpoint
curl http://localhost:9222/json/version
```

## Usage

### Page Navigation
```bash
# Navigate to URL
~/.claude/skills/chrome-devtools/scripts/navigate.rb "https://example.com"
```

### JavaScript Evaluation
```bash
# Execute JavaScript
~/.claude/skills/chrome-devtools/scripts/evaluate.rb "document.title"

# Get complex data
~/.claude/skills/chrome-devtools/scripts/evaluate.rb "Array.from(document.querySelectorAll('a')).map(a => a.href)"
```

### Network Monitoring
```bash
# Capture network traffic
~/.claude/skills/chrome-devtools/scripts/network_capture.rb "https://example.com" 5

# Arguments: URL, duration (seconds)
```

### Screenshots
```bash
# Capture screenshot
~/.claude/skills/chrome-devtools/scripts/screenshot.rb /tmp/screenshot.png

# JPEG with quality
~/.claude/skills/chrome-devtools/scripts/screenshot.rb /tmp/screenshot.jpg --format jpeg --quality 80
```

### Console Logs
```bash
# Monitor console output
~/.claude/skills/chrome-devtools/scripts/console_log.rb "https://example.com" 10

# Arguments: URL, duration (seconds)
```

## Docker Management

### Start Container
```bash
~/.claude/skills/chrome-devtools/scripts/start.sh
```

### Stop Container
```bash
~/.claude/skills/chrome-devtools/scripts/stop.sh
```

### Restart Container
```bash
~/.claude/skills/chrome-devtools/scripts/restart.sh
```

### Check Status
```bash
~/.claude/skills/chrome-devtools/scripts/status.sh
```

### VNC Access (Visual Debugging)
```bash
# Get VNC connection details
~/.claude/skills/chrome-devtools/scripts/vnc_url.sh

# Connect with VNC viewer to: vnc://localhost:5900
# Password: secret
```

## Troubleshooting

### Container won't start
**Symptom**: `docker-compose up -d` fails

**Solutions**:
1. Check Docker Desktop is running
2. Verify SHM size setting (Chrome needs shared memory)
3. Check logs: `docker-compose logs`
4. Try with increased shm_size in docker-compose.yml

### CDP connection failed
**Symptom**: Can't connect to WebSocket

**Solutions**:
1. Verify container is running: `docker ps | grep chrome`
2. Check CDP endpoint: `curl http://localhost:9222/json`
3. Verify port not in use: `lsof -i :9222`
4. Check container logs: `docker logs chrome-devtools-server`

### Browser crashed
**Symptom**: CDP commands fail with "Target closed"

**Solutions**:
1. Restart container: `docker-compose restart`
2. Check memory limits (Chrome needs ≥1GB)
3. Review crash logs: `docker logs chrome-devtools-server`

### VNC not working
**Symptom**: Can't connect to VNC

**Solutions**:
1. Verify VNC port exposed: `docker port chrome-devtools-server`
2. Check DEFAULT_HEADLESS=false in environment
3. Try different VNC client
4. Restart container: `docker-compose restart`

## Performance Notes
- Container startup: ~15-20 seconds
- CDP response time: <200ms typical
- Memory usage: ~800MB-1.5GB
- Supports up to 5 concurrent sessions (configurable)

## Advanced Configuration

### Headless vs Headed Mode
Edit `docker-compose.yml` environment:
```yaml
environment:
  - DEFAULT_HEADLESS=false  # Enable headed mode for VNC
```

### Session Limits
```yaml
environment:
  - MAX_CONCURRENT_SESSIONS=10
```

### Preboot Optimization
```yaml
environment:
  - PREBOOT_CHROME=true  # Faster first connection
```

## CDP Domains Reference

### Commonly Used Domains
- **Page**: Navigation, lifecycle, resources
- **Runtime**: JavaScript evaluation, console
- **Network**: Request/response monitoring
- **DOM**: Document structure, queries
- **Performance**: Metrics, profiling
- **Debugger**: Breakpoints, stepping
- **Profiler**: CPU/Memory profiling

### Event Subscription Example
```ruby
require_relative 'cdp_client'

client = CDPClient.new
client.network_enable

client.on_event('Network.requestWillBeSent') do |params|
  puts "Request: #{params['request']['url']}"
end

client.page_navigate('https://example.com')
sleep 5 # Capture traffic
```

## See Also
- Playwright skill for browser automation
- CDP Protocol documentation: https://chromedevtools.github.io/devtools-protocol/
- Original research: `~/.claude/claudedocs/research_mcp_to_agent_skill_conversion_20251116.md`
