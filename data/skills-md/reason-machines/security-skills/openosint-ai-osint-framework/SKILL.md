---
name: openosint-ai-osint-framework
description: AI-powered OSINT agent with interactive REPL, MCP server, and CLI for email/username/domain/IP/phone investigation using 11 integrated tools
triggers:
  - investigate an email address for social accounts
  - search for username across social platforms
  - check if email has been in data breaches
  - enumerate subdomains for a domain
  - lookup IP geolocation and ASN information
  - run OSINT investigation on a target
  - search shodan for exposed services
  - generate google dorks for OSINT research
---

# OpenOSINT AI OSINT Framework

> Skill by [ara.so](https://ara.so) — Security Skills collection.

OpenOSINT is an AI-powered Open Source Intelligence framework that combines 11 OSINT tools into a unified interface. It operates as an interactive REPL with natural language investigation, a direct CLI for scripting, and an MCP server for AI client integration. The AI agent intelligently chains tools based on findings and compiles structured reports. All tools run as async subprocess wrappers with hard timeout enforcement.

## Installation

```bash
# Clone and install
git clone https://github.com/OpenOSINT/OpenOSINT.git
cd OpenOSINT
pip install -e .

# Set Anthropic API key (or use --provider ollama for local models)
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Install external OSINT tools
pip install holehe sherlock-project sublist3r

# Download phoneinfoga binary from https://github.com/sundowndev/phoneinfoga/releases
# Place in PATH
```

## Optional Dependencies

```bash
# For local LLM (no API key required)
pip install ollama
ollama pull llama3.2

# For Shodan API
pip install shodan
export SHODAN_API_KEY=your-shodan-key

# For PDF reports
pip install reportlab

# API keys for enhanced functionality
export HIBP_API_KEY=your-hibp-key           # HaveIBeenPwned
export IPINFO_TOKEN=your-ipinfo-token       # ipinfo.io
export VIRUSTOTAL_API_KEY=your-vt-key       # VirusTotal
```

## Usage Modes

### Interactive REPL (AI-Powered)

```bash
# Launch interactive AI agent
openosint

# Or explicitly
openosint shell

# Use local Ollama instead of Anthropic
openosint --provider ollama
```

In REPL, type natural language queries:
```
openosint ❯ investigate user@example.com
openosint ❯ find accounts for johndoe99
openosint ❯ check breaches for admin@company.com
openosint ❯ enumerate subdomains of example.com
```

REPL commands:
- `<target>` - Investigate email/username/domain/IP/phone
- `clear` - Reset conversation memory
- `save` - Save last report to reports/
- `tools` - List available tools and status
- `config` - Show current configuration
- `help` - Show all commands
- `exit` / Ctrl-D - Exit

### Direct CLI (No AI)

```bash
# Email investigation
openosint email target@example.com
openosint email target@example.com -t 60  # 60 second timeout

# Username search
openosint username johndoe99
openosint username johndoe99 -t 120

# Shodan lookup
openosint shodan 8.8.8.8
openosint shodan "apache port:80 country:DE"

# VirusTotal lookup
openosint virustotal example.com
openosint virustotal 192.168.1.1

# Multi-target investigation
openosint multi "user@example.com johndoe99 example.com"

# Parallel execution (run multiple tools simultaneously)
openosint --parallel email user@example.com
openosint --parallel username johndoe99

# JSON output for scripting
openosint --json email user@example.com
```

## Python API Usage

### Direct Tool Usage

```python
import asyncio
from openosint.tools.email import search_email
from openosint.tools.username import search_username
from openosint.tools.breach import search_breach
from openosint.tools.whois import search_whois
from openosint.tools.ip import search_ip
from openosint.tools.domain import search_domain
from openosint.tools.dorks import generate_dorks
from openosint.tools.paste import search_paste
from openosint.tools.phone import search_phone
from openosint.tools.shodan import search_shodan
from openosint.tools.virustotal import search_virustotal

async def investigate_email(email: str):
    """Investigate an email address."""
    # Search social accounts
    accounts = await search_email(email, timeout=60)
    print(f"Social accounts: {accounts}")
    
    # Check data breaches
    breaches = await search_breach(email)
    print(f"Breaches: {breaches}")
    
    # Search paste dumps
    pastes = await search_paste(email)
    print(f"Paste dumps: {pastes}")
    
    # Generate search dorks
    dorks = await generate_dorks(email)
    print(f"Google dorks: {dorks}")

async def investigate_username(username: str):
    """Find username across platforms."""
    platforms = await search_username(username, timeout=120)
    print(f"Found on platforms: {platforms}")

async def investigate_domain(domain: str):
    """Investigate a domain."""
    # WHOIS lookup
    whois = await search_whois(domain)
    print(f"WHOIS: {whois}")
    
    # Subdomain enumeration
    subdomains = await search_domain(domain)
    print(f"Subdomains: {subdomains}")
    
    # VirusTotal check
    vt_result = await search_virustotal(domain)
    print(f"VirusTotal: {vt_result}")

async def investigate_ip(ip: str):
    """Investigate an IP address."""
    # IP geolocation
    ip_info = await search_ip(ip)
    print(f"IP info: {ip_info}")
    
    # Shodan lookup
    shodan_data = await search_shodan(ip)
    print(f"Shodan: {shodan_data}")

async def investigate_phone(phone: str):
    """Investigate a phone number (E.164 format)."""
    phone_info = await search_phone(phone)
    print(f"Phone info: {phone_info}")

# Run investigations
asyncio.run(investigate_email("target@example.com"))
asyncio.run(investigate_username("johndoe99"))
asyncio.run(investigate_domain("example.com"))
asyncio.run(investigate_ip("8.8.8.8"))
asyncio.run(investigate_phone("+14155552671"))
```

### AI Agent Usage

```python
import asyncio
from openosint.agent import OpenOSINTAgent

async def ai_investigation():
    """Run AI-powered investigation."""
    agent = OpenOSINTAgent(
        api_key=None,  # Uses ANTHROPIC_API_KEY from env
        provider="anthropic",  # or "ollama"
        model="claude-3-5-sonnet-20241022"
    )
    
    # Natural language investigation
    response = await agent.investigate("investigate user@example.com")
    print(response)
    
    # Agent automatically chains tools based on findings
    response = await agent.investigate(
        "find all accounts for johndoe99 and check for breaches"
    )
    print(response)
    
    # Get conversation history
    history = agent.get_history()
    
    # Clear conversation
    agent.clear_history()

asyncio.run(ai_investigation())
```

### Parallel Execution

```python
import asyncio
from openosint.tools.email import search_email
from openosint.tools.breach import search_breach
from openosint.tools.paste import search_paste

async def parallel_email_investigation(email: str):
    """Run multiple tools in parallel."""
    results = await asyncio.gather(
        search_email(email, timeout=60),
        search_breach(email),
        search_paste(email),
        return_exceptions=True  # Don't fail if one tool errors
    )
    
    accounts, breaches, pastes = results
    
    report = {
        "email": email,
        "accounts": accounts if not isinstance(accounts, Exception) else str(accounts),
        "breaches": breaches if not isinstance(breaches, Exception) else str(breaches),
        "pastes": pastes if not isinstance(pastes, Exception) else str(pastes)
    }
    
    return report

# Run parallel investigation
result = asyncio.run(parallel_email_investigation("target@example.com"))
print(result)
```

## Tool-Specific Examples

### Email Investigation

```python
async def comprehensive_email_scan(email: str):
    """Complete email OSINT scan."""
    from openosint.tools.email import search_email
    from openosint.tools.breach import search_breach
    from openosint.tools.paste import search_paste
    from openosint.tools.dorks import generate_dorks
    
    print(f"[*] Investigating {email}")
    
    # Find social accounts
    print("[*] Searching social accounts...")
    accounts = await search_email(email)
    
    # Check breaches (requires HIBP_API_KEY)
    print("[*] Checking data breaches...")
    breaches = await search_breach(email)
    
    # Search paste dumps
    print("[*] Searching paste sites...")
    pastes = await search_paste(email)
    
    # Generate Google dorks
    print("[*] Generating Google dorks...")
    dorks = await generate_dorks(email)
    
    return {
        "accounts": accounts,
        "breaches": breaches,
        "pastes": pastes,
        "dorks": dorks
    }
```

### Username Investigation

```python
async def comprehensive_username_scan(username: str):
    """Complete username OSINT scan."""
    from openosint.tools.username import search_username
    from openosint.tools.paste import search_paste
    from openosint.tools.dorks import generate_dorks
    
    print(f"[*] Investigating {username}")
    
    # Search across 300+ platforms
    print("[*] Searching platforms (this may take 2+ minutes)...")
    platforms = await search_username(username, timeout=180)
    
    # Search paste dumps
    print("[*] Searching paste sites...")
    pastes = await search_paste(username)
    
    # Generate Google dorks
    print("[*] Generating Google dorks...")
    dorks = await generate_dorks(username)
    
    return {
        "platforms": platforms,
        "pastes": pastes,
        "dorks": dorks
    }
```

### Domain Investigation

```python
async def comprehensive_domain_scan(domain: str):
    """Complete domain OSINT scan."""
    from openosint.tools.whois import search_whois
    from openosint.tools.domain import search_domain
    from openosint.tools.virustotal import search_virustotal
    from openosint.tools.dorks import generate_dorks
    
    print(f"[*] Investigating {domain}")
    
    # WHOIS lookup
    print("[*] Running WHOIS...")
    whois = await search_whois(domain)
    
    # Subdomain enumeration
    print("[*] Enumerating subdomains...")
    subdomains = await search_domain(domain)
    
    # VirusTotal scan (requires VIRUSTOTAL_API_KEY)
    print("[*] Checking VirusTotal...")
    vt_result = await search_virustotal(domain)
    
    # Generate Google dorks
    print("[*] Generating Google dorks...")
    dorks = await generate_dorks(domain)
    
    return {
        "whois": whois,
        "subdomains": subdomains,
        "virustotal": vt_result,
        "dorks": dorks
    }
```

### IP Investigation

```python
async def comprehensive_ip_scan(ip: str):
    """Complete IP OSINT scan."""
    from openosint.tools.ip import search_ip
    from openosint.tools.shodan import search_shodan
    from openosint.tools.virustotal import search_virustotal
    
    print(f"[*] Investigating {ip}")
    
    # IP geolocation
    print("[*] Geolocating IP...")
    ip_info = await search_ip(ip)
    
    # Shodan lookup (requires SHODAN_API_KEY)
    print("[*] Querying Shodan...")
    shodan_data = await search_shodan(ip)
    
    # VirusTotal scan (requires VIRUSTOTAL_API_KEY)
    print("[*] Checking VirusTotal...")
    vt_result = await search_virustotal(ip)
    
    return {
        "ip_info": ip_info,
        "shodan": shodan_data,
        "virustotal": vt_result
    }
```

### Shodan Advanced Queries

```python
async def shodan_queries():
    """Advanced Shodan search examples."""
    from openosint.tools.shodan import search_shodan
    
    # Host lookup (specific IP)
    host = await search_shodan("8.8.8.8")
    
    # Banner search
    apache = await search_shodan("apache port:80")
    
    # Country-specific search
    german_servers = await search_shodan("apache port:80 country:DE")
    
    # Vulnerable systems
    heartbleed = await search_shodan("vuln:CVE-2014-0160")
    
    # ICS/SCADA
    scada = await search_shodan("port:502")  # Modbus
    
    # Webcams
    cameras = await search_shodan("Server: SQ-WEBCAM")
    
    return {
        "host": host,
        "apache": apache,
        "german_servers": german_servers,
        "heartbleed": heartbleed,
        "scada": scada,
        "cameras": cameras
    }
```

## MCP Server Integration

OpenOSINT can run as an MCP server for Claude Desktop or other MCP clients:

```json
{
  "mcpServers": {
    "openosint": {
      "command": "python",
      "args": ["-m", "openosint.mcp_server"],
      "env": {
        "ANTHROPIC_API_KEY": "your-key",
        "HIBP_API_KEY": "your-key",
        "SHODAN_API_KEY": "your-key",
        "VIRUSTOTAL_API_KEY": "your-key",
        "IPINFO_TOKEN": "your-token"
      }
    }
  }
}
```

Then in Claude Desktop, you can use natural language:
```
"Investigate user@example.com for social accounts and data breaches"
"Find all platforms where johndoe99 has accounts"
"Enumerate subdomains for example.com"
```

## Configuration

### Environment Variables

```bash
# Required for AI agent (unless using --provider ollama)
export ANTHROPIC_API_KEY=sk-ant-your-key

# Optional API keys
export HIBP_API_KEY=your-hibp-key           # For search_breach
export SHODAN_API_KEY=your-shodan-key       # For search_shodan
export VIRUSTOTAL_API_KEY=your-vt-key       # For search_virustotal
export IPINFO_TOKEN=your-ipinfo-token       # For enhanced search_ip

# For local LLM
export OLLAMA_HOST=http://localhost:11434   # Default Ollama endpoint
```

### Timeouts

All tools accept a `timeout` parameter (seconds):

```python
# Default timeouts
await search_email(email, timeout=60)      # 60 seconds
await search_username(username, timeout=120)  # 120 seconds (sherlock is slow)
await search_domain(domain, timeout=90)    # 90 seconds
await search_phone(phone, timeout=30)      # 30 seconds
await search_shodan(query, timeout=30)     # 30 seconds

# Custom timeout
await search_email(email, timeout=180)     # 3 minutes
```

## Common Patterns

### Batch Email Investigation

```python
async def batch_email_investigation(emails: list[str]):
    """Investigate multiple emails in parallel."""
    from openosint.tools.email import search_email
    from openosint.tools.breach import search_breach
    
    async def investigate_one(email: str):
        accounts = await search_email(email)
        breaches = await search_breach(email)
        return {
            "email": email,
            "accounts": accounts,
            "breaches": breaches
        }
    
    results = await asyncio.gather(
        *[investigate_one(email) for email in emails],
        return_exceptions=True
    )
    
    return [r for r in results if not isinstance(r, Exception)]

emails = ["user1@example.com", "user2@example.com", "user3@example.com"]
results = asyncio.run(batch_email_investigation(emails))
```

### Export Report

```python
async def investigate_and_export(target: str, output_path: str):
    """Run investigation and save report."""
    from openosint.agent import OpenOSINTAgent
    import json
    
    agent = OpenOSINTAgent()
    response = await agent.investigate(f"investigate {target}")
    
    # Save as JSON
    with open(output_path, "w") as f:
        json.dump({
            "target": target,
            "findings": response,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    return response

asyncio.run(investigate_and_export(
    "user@example.com",
    "reports/investigation.json"
))
```

### Error Handling

```python
async def safe_investigation(email: str):
    """Investigate with proper error handling."""
    from openosint.tools.email import search_email
    from openosint.tools.breach import search_breach
    
    results = {}
    
    # Each tool runs independently
    try:
        results["accounts"] = await search_email(email, timeout=60)
    except asyncio.TimeoutError:
        results["accounts"] = "ERROR: Timeout after 60 seconds"
    except Exception as e:
        results["accounts"] = f"ERROR: {str(e)}"
    
    try:
        results["breaches"] = await search_breach(email)
    except Exception as e:
        results["breaches"] = f"ERROR: {str(e)}"
    
    return results
```

## Troubleshooting

### holehe Not Found

```bash
# Install holehe
pip install holehe

# Verify installation
which holehe
holehe --help
```

### sherlock Not Found

```bash
# Install sherlock-project
pip install sherlock-project

# Verify installation
which sherlock
sherlock --help
```

### phoneinfoga Not Found

```bash
# Download binary from GitHub releases
wget https://github.com/sundowndev/phoneinfoga/releases/download/v2.11.0/phoneinfoga_Linux_x86_64.tar.gz
tar -xzf phoneinfoga_Linux_x86_64.tar.gz
sudo mv phoneinfoga /usr/local/bin/
chmod +x /usr/local/bin/phoneinfoga

# Verify
phoneinfoga version
```

### HIBP API Returns 401

```bash
# Get API key from https://haveibeenpwned.com/API/Key
export HIBP_API_KEY=your-actual-key
```

### Shodan API Returns 401

```bash
# Get API key from https://account.shodan.io
export SHODAN_API_KEY=your-actual-key

# Verify
python -c "import shodan; api=shodan.Shodan('$SHODAN_API_KEY'); print(api.info())"
```

### VirusTotal API Returns 403

```bash
# Get API key from https://www.virustotal.com/gui/my-apikey
export VIRUSTOTAL_API_KEY=your-actual-key
```

### Ollama Connection Error

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.2

# Verify running
curl http://localhost:11434/api/tags

# Use with OpenOSINT
openosint --provider ollama
```

### Subprocess Timeout

```python
# Increase timeout for slow tools
await search_username(username, timeout=300)  # 5 minutes for sherlock
```

### Rate Limiting

```python
# Add delays between requests
import asyncio

async def rate_limited_batch(emails: list[str], delay: float = 2.0):
    """Investigate emails with rate limiting."""
    results = []
    for email in emails:
        result = await search_email(email)
        results.append(result)
        await asyncio.sleep(delay)  # 2 second delay
    return results
```

### Memory Issues with Large Results

```python
# Stream results instead of loading all at once
async def stream_investigation(emails: list[str]):
    """Process results one at a time."""
    for email in emails:
        result = await search_email(email)
        # Process immediately
        print(f"Results for {email}: {result}")
        # Don't accumulate in memory
        del result
```

## Tool Status Check

```python
async def check_tool_status():
    """Verify which tools are available."""
    from openosint.tools.email import search_email
    from openosint.tools.username import search_username
    from openosint.tools.phone import search_phone
    import shutil
    import os
    
    status = {
        "holehe": shutil.which("holehe") is not None,
        "sherlock": shutil.which("sherlock") is not None,
        "sublist3r": shutil.which("sublist3r") is not None,
        "phoneinfoga": shutil.which("phoneinfoga") is not None,
        "hibp_api_key": os.getenv("HIBP_API_KEY") is not None,
        "shodan_api_key": os.getenv("SHODAN_API_KEY") is not None,
        "virustotal_api_key": os.getenv("VIRUSTOTAL_API_KEY") is not None,
        "ipinfo_token": os.getenv("IPINFO_TOKEN") is not None,
    }
    
    for tool, available in status.items():
        symbol = "✓" if available else "✗"
        print(f"{symbol} {tool}")
    
    return status

asyncio.run(check_tool_status())
```
