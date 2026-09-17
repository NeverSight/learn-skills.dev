---
name: lanhu-mcp-collaboration
description: AI-powered design collaboration server connecting Lanhu design platform with AI coding assistants for requirements analysis, UI design extraction, and team knowledge sharing
triggers:
  - analyze requirements from Lanhu prototype
  - extract design specs from Lanhu
  - download design assets and slices from Lanhu
  - share team knowledge via Lanhu MCP message board
  - get UI design parameters and CSS code from Lanhu
  - check team collaboration notes in Lanhu
  - analyze Axure prototype requirements
  - export design slices with semantic naming
---

# Lanhu MCP Collaboration

> Skill by [ara.so](https://ara.so) — MCP Skills collection.

## Overview

Lanhu MCP Server is a Model Context Protocol server that connects AI coding assistants to the Lanhu (蓝湖) design collaboration platform. It enables automated requirements analysis, UI design extraction, team knowledge sharing, and design-to-code conversion with vision-capable AI models.

**Core capabilities:**
- **Requirements Analysis**: Automatic Axure prototype extraction with 3 analysis modes (Development/Testing/Exploration)
- **UI Design Support**: Design spec extraction with precise parameters (spacing, colors, fonts) + HTML/CSS code generation
- **Team Message Board**: Shared knowledge base across all AI assistants, breaking IDE silos
- **Smart Asset Export**: Automatic design slice extraction with semantic naming
- **Performance**: Version-based caching, incremental updates, concurrent processing

**Supported AI Clients**: Cursor, Windsurf, Claude Code, OpenClaw, ClawBot, Trae, Cline, and any MCP-compatible tool

## Installation

### Prerequisites

- **Python 3.10+**
- **Vision-capable AI model** (Claude, GPT-4V, Gemini, Kimi, Qwen, DeepSeek)
- **Lanhu account** with valid cookie authentication

### Quick Install (Recommended)

Simply ask your AI assistant:
```
"Help me clone and install https://github.com/dsphper/lanhu-mcp"
```

The AI will guide you through cloning, dependency installation, cookie configuration, and server startup.

### Manual Installation

**Option 1: Docker (Recommended)**

```bash
# Clone repository
git clone https://github.com/dsphper/lanhu-mcp.git
cd lanhu-mcp

# Configure environment (interactive cookie setup)
bash setup-env.sh  # Linux/Mac
# or
setup-env.bat      # Windows

# Start service
docker-compose up -d
```

**Option 2: Source Code**

```bash
# Clone repository
git clone https://github.com/dsphper/lanhu-mcp.git
cd lanhu-mcp

# One-click installation (includes cookie setup)
bash easy-install.sh  # Linux/Mac
# or
easy-install.bat      # Windows
```

**Manual dependency installation:**
```bash
pip install -r requirements.txt
playwright install chromium
```

## Configuration

### Required: Lanhu Cookie

Export your Lanhu cookie (obtained from browser DevTools after logging into lanhuapp.com):

```bash
export LANHU_COOKIE="your_lanhu_cookie_here"
```

### Optional: Feishu Webhook

For team notifications and @mentions:

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-url"
```

Or edit `lanhu_mcp_server.py`:
```python
DEFAULT_FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-url"
```

### Optional: Server Configuration

```bash
export SERVER_HOST="0.0.0.0"
export SERVER_PORT=8000
export DATA_DIR="./data"
export HTTP_TIMEOUT=30
export VIEWPORT_WIDTH=1920
export VIEWPORT_HEIGHT=1080
export DEBUG="false"
```

### Start Server

**Source code:**
```bash
python lanhu_mcp_server.py
```

**Docker:**
```bash
docker-compose up -d
docker-compose logs -f  # View logs
docker-compose down     # Stop
```

Server runs at `http://localhost:8000/mcp`

## AI Client Configuration

### Claude Code

In `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "lanhu": {
      "type": "http",
      "url": "http://localhost:8000/mcp?role=Developer&name=YourName"
    }
  }
}
```

### Cursor / Windsurf / Others

In MCP settings:
```json
{
  "mcpServers": {
    "lanhu": {
      "url": "http://localhost:8000/mcp?role=Developer&name=YourName"
    }
  }
}
```

**URL Parameters:**
- `role`: User role (Developer/Frontend/Backend/Tester/Product)
- `name`: Username for collaboration tracking and @mentions (use English to avoid encoding issues)

## Key Tools & Commands

### 1. Requirements Analysis

**Tool:** `analyze_requirements_document`

Analyze Axure prototypes with AI-powered extraction:

```python
# User prompt example:
"Please analyze this requirements document using MCP:
https://lanhuapp.com/web/#/item/project/product?tid=xxx&pid=xxx&docId=xxx"

# The AI will call:
analyze_requirements_document(
    url="https://lanhuapp.com/web/#/item/project/product?tid=xxx&pid=xxx&docId=xxx",
    mode="development"  # Options: development | testing | exploration
)
```

**Analysis Modes:**

- **`development`**: Detailed field rules, business logic, global flowcharts
- **`testing`**: Test scenarios, test cases, boundary values, validation rules
- **`exploration`**: Core feature overview, module dependencies, review points

**Four-Stage Workflow:**
1. Global text scanning (establish overall understanding)
2. Grouped detailed analysis (based on selected mode)
3. Reverse validation (ensure zero omissions)
4. Generate deliverables (requirements doc/test plan/review slides)

### 2. UI Design Analysis

**Tool:** `view_design_document`

Extract design specs with precise parameters and generated code:

```python
# User prompt:
"Please view this design document using MCP:
https://lanhuapp.com/web/#/item/project/stage?tid=xxx&pid=xxx"

# Returns:
# - Design image previews
# - Precise parameters (dimensions, spacing, colors, fonts)
# - HTML + CSS code conversion
```

**Output includes:**
- Component dimensions and spacing
- Color values (HEX/RGB)
- Font sizes and weights
- Auto-generated HTML/CSS code matching Lanhu's native export

### 3. Design Asset Export

**Tool:** `export_design_slices`

Download design slices with semantic naming:

```python
# User prompt:
"Export all design slices from this Lanhu page"

export_design_slices(
    design_url="https://lanhuapp.com/web/#/item/project/stage?tid=xxx&pid=xxx",
    output_dir="./assets"
)
```

**Features:**
- Automatic slice detection
- Semantic file naming based on layer paths
- Organized folder structure
- Supports PNG, SVG, and other formats

### 4. Team Message Board

**Tools:** `create_message`, `list_messages`, `search_messages`

Share knowledge and context across all team AI assistants:

```python
# Create knowledge entry
create_message(
    project_url="https://lanhuapp.com/web/#/item/project/...",
    content="User authentication requires OAuth2 flow with refresh token rotation",
    message_type="knowledge",  # Options: knowledge | task | question | experience
    tags=["auth", "security", "backend"]
)

# Search team knowledge
search_messages(
    project_url="https://lanhuapp.com/web/#/item/project/...",
    keyword="authentication",
    message_type="knowledge"
)

# @mention team member (triggers Feishu notification)
create_message(
    project_url="https://lanhuapp.com/web/#/item/project/...",
    content="@zhangsan Please review the API error handling logic",
    message_type="task",
    mentioned_users=["zhangsan"]
)
```

**Message Types:**
- **`knowledge`**: Permanent knowledge base entries (pitfalls, best practices)
- **`task`**: Task assignments with @mention support
- **`question`**: Questions for team discussion
- **`experience`**: Lessons learned and implementation notes

## Common Patterns

### Pattern 1: Full Requirements Analysis Workflow

```python
# Step 1: User provides Lanhu URL
user: "Analyze requirements: https://lanhuapp.com/web/#/item/project/product?tid=123&pid=456&docId=789"

# Step 2: AI calls analyze_requirements_document
result = analyze_requirements_document(
    url="https://lanhuapp.com/web/#/item/project/product?tid=123&pid=456&docId=789",
    mode="development"
)

# Step 3: AI processes four-stage analysis
# - Stage 1: Scans all pages and extracts text
# - Stage 2: Groups pages and analyzes by business modules
# - Stage 3: Reverse validates for missing items
# - Stage 4: Generates structured requirements document

# Step 4: Save insights to team knowledge base
create_message(
    project_url="https://lanhuapp.com/web/#/item/project/product?tid=123&pid=456",
    content="Key finding: User role permissions require cascading delete logic",
    message_type="knowledge",
    tags=["permissions", "database"]
)
```

### Pattern 2: Design-to-Code Implementation

```python
# Step 1: View design and get parameters
user: "Implement this design: https://lanhuapp.com/web/#/item/project/stage?tid=123&pid=456"

design_data = view_design_document(
    url="https://lanhuapp.com/web/#/item/project/stage?tid=123&pid=456"
)

# Step 2: Extract design parameters
# Returns:
# {
#   "preview_image": "base64_image_data",
#   "parameters": {
#     "width": "375px",
#     "height": "812px",
#     "spacing": {"top": "20px", "left": "16px"},
#     "colors": {"primary": "#1677FF", "text": "#333333"},
#     "fonts": {"title": "16px/bold", "body": "14px/regular"}
#   },
#   "html_css": "<div class='container'>...</div>\n<style>...</style>"
# }

# Step 3: Export required assets
export_design_slices(
    design_url="https://lanhuapp.com/web/#/item/project/stage?tid=123&pid=456",
    output_dir="./src/assets/images"
)

# Step 4: AI generates implementation code using parameters + HTML/CSS reference
```

### Pattern 3: Team Collaboration Tracking

```python
# Developer A's AI analyzes requirements
analyze_requirements_document(
    url="https://lanhuapp.com/web/#/item/project/product?tid=123&pid=456&docId=789",
    mode="development"
)

# Save analysis results
create_message(
    project_url="https://lanhuapp.com/web/#/item/project/product?tid=123&pid=456",
    content="Requirements analysis complete. 5 core modules identified: User, Product, Order, Payment, Notification",
    message_type="knowledge",
    tags=["requirements", "architecture"]
)

# Tester B's AI searches team knowledge
messages = search_messages(
    project_url="https://lanhuapp.com/web/#/item/project/product?tid=123&pid=456",
    keyword="requirements analysis",
    message_type="knowledge"
)
# Returns Developer A's analysis — no duplicate work!

# Tester B's AI now performs test-focused analysis
analyze_requirements_document(
    url="https://lanhuapp.com/web/#/item/project/product?tid=123&pid=456&docId=789",
    mode="testing"
)
```

### Pattern 4: Environment Variable Best Practices

```python
# Never hardcode secrets
# ❌ BAD:
LANHU_COOKIE = "abc123..."
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# ✅ GOOD: Use environment variables
import os

LANHU_COOKIE = os.getenv("LANHU_COOKIE")
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK_URL")

# Validate required config
if not LANHU_COOKIE:
    raise ValueError("LANHU_COOKIE environment variable is required")
```

## Troubleshooting

### Issue: "No vision-capable model detected"

**Cause:** Using text-only AI model (e.g., GPT-3.5, Claude Instant)

**Solution:** Switch to vision-capable model:
- Claude 3+ (Sonnet, Opus)
- GPT-4V, GPT-4o
- Gemini Pro Vision
- Kimi, Qwen-VL, DeepSeek-VL

### Issue: "Cookie authentication failed"

**Cause:** Invalid or expired Lanhu cookie

**Solution:**
1. Login to https://lanhuapp.com in browser
2. Open DevTools → Network tab
3. Find any API request to lanhuapp.com
4. Copy full `Cookie` header value
5. Update `LANHU_COOKIE` environment variable
6. Restart server

### Issue: "Design-to-code conversion unavailable"

**Cause:** Design file uploaded with outdated Lanhu plugin

**Solution:**
1. Ask UI designer to update Lanhu plugin (Figma/Sketch/Adobe XD)
2. Re-upload design file
3. Retry design analysis

### Issue: "Message board not syncing across AI assistants"

**Cause:** Different MCP server instances or cache issues

**Solution:**
1. Ensure all AI clients connect to same MCP server URL
2. Verify `project_url` is identical across calls
3. Clear cache: `rm -rf ./data/cache/*`
4. Restart MCP server

### Issue: Docker container fails to start

**Cause:** Port conflict or missing environment variables

**Solution:**
```bash
# Check port availability
lsof -i :8000

# Verify environment variables
docker-compose config

# Check logs
docker-compose logs lanhu-mcp

# Restart with clean state
docker-compose down -v
docker-compose up -d
```

### Issue: Slow requirements analysis

**Cause:** Large prototype with many pages, no caching

**Solution:**
1. Enable version-based caching (automatic)
2. Use `exploration` mode for quick overview
3. Increase concurrent processing:
   ```bash
   export HTTP_TIMEOUT=60
   export VIEWPORT_WIDTH=1920
   export VIEWPORT_HEIGHT=1080
   ```
4. Subsequent analyses will use cached data (much faster)

## Advanced Usage

### Custom Analysis Modes

Modify `lanhu_mcp_server.py` to add custom analysis perspectives:

```python
ANALYSIS_MODES = {
    "development": "Developer perspective with detailed field rules",
    "testing": "QA perspective with test cases and validation",
    "exploration": "Quick overview for stakeholder review",
    "security": "Security-focused analysis for audit"  # Custom mode
}
```

### Feishu User ID Mapping

Enable @mention notifications by updating `FEISHU_USER_ID_MAP`:

```python
FEISHU_USER_ID_MAP = {
    "zhangsan": "ou_1234567890abcdef",
    "lisi": "ou_abcdef1234567890",
    # Add your team members
}
```

### Performance Tuning

```bash
# Increase concurrent downloads
export HTTP_TIMEOUT=60

# Larger viewport for high-res screenshots
export VIEWPORT_WIDTH=2560
export VIEWPORT_HEIGHT=1440

# Enable debug logging
export DEBUG="true"
```

## Integration Examples

### Cursor AI Integration

```typescript
// In Cursor, add to .cursor/mcp.json
{
  "mcpServers": {
    "lanhu": {
      "url": "http://localhost:8000/mcp?role=Frontend&name=Alice"
    }
  }
}

// Then prompt:
// "Using Lanhu MCP, analyze the design at https://lanhuapp.com/... 
//  and generate React components with Tailwind CSS"
```

### Windsurf Cascade Integration

```json
// In Windsurf settings
{
  "mcp": {
    "servers": {
      "lanhu": {
        "url": "http://localhost:8000/mcp?role=Fullstack&name=Bob"
      }
    }
  }
}
```

### Claude Code Integration

```json
// In claude_desktop_config.json
{
  "mcpServers": {
    "lanhu": {
      "type": "http",
      "url": "http://localhost:8000/mcp?role=Backend&name=Charlie"
    }
  }
}
```

## Additional Resources

- **Cookie Setup Guide**: `GET-COOKIE-TUTORIAL.md`
- **AI Installation Guide**: `ai-install-guide.md`
- **Docker Deployment**: `DEPLOY.md`
- **Contributing**: `CONTRIBUTING.md`
- **GitHub**: https://github.com/dsphper/lanhu-mcp
- **MCP Protocol**: https://modelcontextprotocol.io/

## License

MIT License - See `LICENSE` file for details.
