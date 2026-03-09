---
name: mapbox-mcp-devkit-patterns
description: Integration patterns for Mapbox MCP DevKit Server in AI coding assistants. Covers setup, style management, token management, validation workflows, and documentation access through MCP. Use when building Mapbox applications with AI coding assistance.
---

# Mapbox MCP DevKit Patterns

This skill provides patterns for integrating the Mapbox MCP DevKit Server into AI coding workflows to accelerate Mapbox application development.

## What is Mapbox MCP DevKit?

The [Mapbox MCP DevKit Server](https://github.com/mapbox/mcp-devkit-server) is a Model Context Protocol (MCP) server that gives AI assistants direct access to Mapbox developer APIs:

- **Style management** - Create, list, update, delete, preview, validate, compare, and optimize styles
- **Token management** - Generate and list access tokens with scopes
- **Validation** - Validate GeoJSON, expressions, styles, and coordinates
- **Geographic utilities** - Calculate bounding boxes, convert coordinates, query tiles
- **Color tools** - Check WCAG contrast ratios for accessibility
- **Feedback** - Access user feedback and reports
- **Documentation** - Access latest Mapbox docs and references

**Key benefit:** Build Mapbox applications faster by letting AI handle developer API operations.

## Setup & Installation

### Prerequisites

- Mapbox account with access token
- AI coding assistant that supports MCP (Claude Code, Cursor, Windsurf, Cline, etc.)

### Option 1: Hosted Server (Recommended)

**Easiest setup** - Use Mapbox's hosted DevKit MCP server at:

```
https://mcp-devkit.mapbox.com/mcp
```

No installation required, just configure your AI assistant.

**Authentication:** The hosted server supports OAuth, so no token configuration needed! Simply add the server URL:

#### For Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "mapbox-devkit-mcp": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp-devkit.mapbox.com/mcp"]
    }
  }
}
```

You'll be prompted to authenticate via OAuth on first use.

#### For Claude Code

Claude Code supports both user-level and project-level MCP configuration:

**User-level** (applies to all projects) - `~/.claude.json`:

```json
{
  "mcpServers": {
    "mapbox-devkit": {
      "url": "https://mcp-devkit.mapbox.com/mcp"
    }
  }
}
```

**Project-level** (specific project, can commit to git) - `.mcp.json` in repository root:

```json
{
  "mcpServers": {
    "mapbox-devkit": {
      "url": "https://mcp-devkit.mapbox.com/mcp"
    }
  }
}
```

See [Claude Code settings documentation](https://code.claude.com/docs/en/settings) for more details on configuration scopes.

#### For Cursor

Create or edit `.cursor/mcp.json` (project-local) or `~/.cursor/mcp.json` (global):

```json
{
  "mcpServers": {
    "mapbox-devkit": {
      "url": "https://mcp-devkit.mapbox.com/mcp"
    }
  }
}
```

After saving, restart Cursor. Click "Needs authentication" when prompted and follow the OAuth flow.

#### For VS Code with Copilot

Create or edit `mcp.json`:

```json
{
  "servers": {
    "mapbox-devkit": {
      "type": "http",
      "url": "https://mcp-devkit.mapbox.com/mcp"
    }
  }
}
```

After saving, refresh the MCP service in VS Code. Requires GitHub Copilot with MCP support enabled.

#### For Windsurf/Cline

Similar configuration using the hosted URL with OAuth support.

### Option 2: Self-Hosted (Advanced)

For development, debugging, or customization:

```bash
# Clone the DevKit server
git clone https://github.com/mapbox/mcp-devkit-server.git
cd mcp-devkit-server

# Install dependencies
npm install

# Build the server
npm run build
```

**Configuration for self-hosted (Claude Desktop):**

```json
{
  "mcpServers": {
    "MapboxDevKitServer": {
      "command": "node",
      "args": ["/Users/username/github-projects/mcp-devkit-server/dist/esm/index.js"],
      "env": {
        "MAPBOX_ACCESS_TOKEN": "some token"
      }
    }
  }
}
```

Replace `/Users/username/github-projects/` with your actual path.

### Verify Installation

Ask your AI assistant:

```
"List the available Mapbox DevKit tools"
```

You should see 30+ tools including:

- **Style tools**: `create_style_tool`, `list_styles_tool`, `update_style_tool`, `delete_style_tool`, `preview_style_tool`, etc.
- **Token tools**: `create_token_tool`, `list_tokens_tool`
- **Validation tools**: `validate_geojson_tool`, `validate_style_tool`, `validate_expression_tool`
- **Geographic tools**: `bounding_box_tool`, `coordinate_conversion_tool`, `tilequery_tool`
- **Documentation**: `get_latest_mapbox_docs_tool`

## Core Workflows

### 1. Style Management

**Create a style conversationally:**

```
"Create a dark mode Mapbox style with 3D buildings, emphasize parks in green,
and use blue for water. Name it 'app-dark-mode'."
```

The AI will use `create_style_tool` tool to:

- Generate style JSON following Mapbox Style Spec
- Upload to your Mapbox account
- Return style ID and preview URL

**Update existing style:**

```
"Update style mapbox://styles/username/style-id to make roads more prominent
and reduce building opacity to 0.6"
```

**Validate style:**

```
"Validate this style JSON: [paste style]"
```

### 2. Token Management

**Create scoped token:**

```
"Create a Mapbox token with these scopes:
- styles:read
- fonts:read
- datasets:read
Restrict it to domains: localhost, example.com"
```

**List existing tokens:**

```
"Show me all my Mapbox tokens and their scopes"
```

**Use case:** Generate tokens for different environments (development, staging, production) with appropriate restrictions.

### 3. Data Validation

**Validate GeoJSON:**

```
"Validate this GeoJSON and show any errors:
{
  \"type\": \"FeatureCollection\",
  \"features\": [...]
}"
```

**Validate expressions:**

```
"Is this a valid Mapbox expression?
['case', ['<', ['get', 'population'], 1000], 'small', 'large']"
```

**Coordinate conversion:**

```
"Convert longitude -122.4194, latitude 37.7749 from WGS84 to Web Mercator"
```

### 4. Documentation Access

**Get style spec info:**

```
"What properties are available for fill layers in Mapbox GL JS?"
```

**Check token scopes:**

```
"What token scopes do I need to use the Directions API?"
```

**Streets v8 fields:**

```
"What fields are available in the 'road' layer of Streets v8?"
```

## Design Patterns

### Pattern 1: Iterative Style Development

**Workflow:**

1. Describe desired style in natural language
2. AI creates initial style via MCP
3. View preview URL
4. Request adjustments
5. AI updates style via MCP
6. Repeat until satisfied

**Example conversation:**

```
You: "Create a style for a real estate app - emphasize property boundaries,
     show parks prominently, muted roads"

AI: [Creates style, returns ID and preview URL]

You: "Make the property boundaries purple and thicker"

AI: [Updates style]

You: "Perfect! Now add POI icons for schools and transit"

AI: [Updates style with symbols]
```

**Benefits:**

- No manual JSON editing
- Visual feedback via preview URLs
- Rapid iteration

### Pattern 2: Environment-Specific Tokens

**Workflow:**

1. Define requirements per environment
2. AI creates tokens with appropriate scopes/restrictions
3. Store securely in environment variables

**Example:**

```
You: "Create three tokens:
1. Development - all scopes, localhost only
2. Staging - read-only scopes, staging.example.com
3. Production - minimal scopes, example.com only"

AI: [Creates three tokens with specified configurations]
```

**Benefits:**

- Least-privilege access
- Domain restrictions prevent token misuse
- Clear separation of concerns

### Pattern 3: Validation-First Development

**Workflow:**

1. Design data structure
2. Validate GeoJSON before using
3. Validate expressions before adding to style
4. Catch errors early

**Example:**

```
You: "I have GeoJSON with restaurant locations. Validate it and check for
     any missing required properties"

AI: [Validates, reports any issues]

You: "Now create a style that displays these restaurants with icons sized
     by rating. Validate the expression first."

AI: [Validates expression, then creates style]
```

**Benefits:**

- Catch errors before deployment
- Ensure data integrity
- Faster debugging

### Pattern 4: Documentation-Driven Development

**Workflow:**

1. Ask about Mapbox capabilities
2. Get authoritative documentation
3. Implement with correct patterns
4. Validate implementation

**Example:**

```
You: "How do I create a choropleth map in Mapbox GL JS?"

AI: [Retrieves docs, provides pattern]

You: "Create a style with that pattern for population density data"

AI: [Creates style following documented pattern]
```

**Benefits:**

- Always use latest best practices
- No outdated Stack Overflow answers
- Official Mapbox guidance

## When to Use MCP DevKit

### ✅ Use DevKit when:

- Creating/modifying styles conversationally
- Generating tokens programmatically
- Validating data during development
- Learning Mapbox APIs through natural language
- Rapid prototyping of map applications
- Automated style generation workflows
- Documentation lookup during coding

### ❌ Don't use DevKit for:

- Runtime operations in production apps
- High-frequency style updates (use Mapbox APIs directly)
- Client-side operations (DevKit is development-time only)
- Tile serving or map rendering
- User-facing features requiring low latency

## Integration with Existing Tools

### With Mapbox Studio

DevKit complements, doesn't replace Studio:

- **DevKit:** Quick iterations, automated workflows, AI assistance
- **Studio:** Visual editing, fine-tuning, team collaboration

**Pattern:** Use DevKit for initial creation, Studio for refinement.

### With Mapbox APIs

DevKit wraps Mapbox APIs but doesn't replace them:

- **DevKit:** Development-time operations via AI
- **APIs:** Production runtime operations

**Pattern:** Use DevKit during development, APIs in production code.

### With Version Control

**Pattern:** Save generated styles to git for review and rollback.

```
You: "Create a new style for the home page map and save the JSON to
     styles/home-map.json"

AI: [Creates style, writes JSON to file]

You: [Review, commit to git]
```

## Best Practices

### Security

- **Never commit access tokens** - Use environment variables
- **Use scoped tokens** - Minimal necessary permissions
- **Add URL restrictions** - Limit to your domains
- **Rotate tokens regularly** - Generate new tokens periodically

### Style Management

- **Version your styles** - Save JSON to source control
- **Use meaningful names** - `prod-light-mode` not `style-123`
- **Document decisions** - Add comments explaining style choices
- **Preview before deploying** - Always check preview URL

### Validation

- **Validate early** - Check data before creating styles
- **Use strict validation** - Don't skip validation steps
- **Test expressions** - Validate before adding to styles
- **Verify coordinates** - Ensure correct format and bounds

### Documentation

- **Ask specific questions** - "What are fill-extrusion properties?"
- **Reference versions** - Specify GL JS version if relevant
- **Cross-reference** - Validate AI responses against official docs

## Troubleshooting

### DevKit not appearing in AI assistant

**Check:**

1. MCP server running? Check logs
2. Config file in correct location?
3. Token environment variable set?
4. Path to `index.js` correct?

**Solution:** Restart AI assistant after config changes.

### Style creation fails

**Check:**

1. Access token has `styles:write` scope
2. Style name is unique
3. JSON is valid Mapbox Style Spec

**Solution:** Use `validate_style_tool` tool first.

### Token creation fails

**Check:**

1. Access token has `tokens:write` scope
2. Requested scopes are valid
3. URL restrictions are well-formed

**Solution:** Check token scope documentation via DevKit.

### Validation errors

**Check:**

1. GeoJSON follows spec (RFC 7946)
2. Coordinates are [longitude, latitude] order
3. Properties match expected schema

**Solution:** Ask AI to explain validation errors.

## Example Workflows

### Build a Restaurant Finder

```
You: "I'm building a restaurant finder app. Create:
1. A light, neutral style emphasizing restaurants
2. A token for localhost with minimal scopes
3. Validate this GeoJSON with restaurant locations: [paste]"

AI: [Creates style, token, validates data]

You: "Add filters to show only 4+ star restaurants"

AI: [Updates style with expression]

You: "Generate a preview URL"

AI: [Returns preview]
```

### Create Multi-Environment Setup

```
You: "Set up styles and tokens for dev, staging, prod:
- Dev: Full access, localhost
- Staging: Read-only, staging.example.com
- Prod: Minimal scopes, example.com

Each environment needs its own style variant."

AI: [Creates 3 styles and 3 tokens with specifications]
```

### Validate Third-Party Data

```
You: "I received GeoJSON from a vendor. Validate it, check for:
- Correct coordinate order
- Valid geometry types
- Required properties: name, address, category"

AI: [Validates, reports issues]

You: "Fix the issues and save cleaned data to data/locations.json"

AI: [Fixes, saves file]
```

## Resources

- [Mapbox MCP DevKit Server](https://github.com/mapbox/mcp-devkit-server)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Mapbox Style Specification](https://docs.mapbox.com/style-spec/)
- [Mapbox API Documentation](https://docs.mapbox.com/api/)
- [Token Scopes Reference](https://docs.mapbox.com/api/accounts/tokens/)

## When to Use This Skill

Invoke this skill when:

- Setting up Mapbox development environment with AI assistance
- Creating or modifying Mapbox styles through AI
- Managing access tokens programmatically
- Validating GeoJSON or expressions during development
- Learning Mapbox APIs with AI guidance
- Automating style generation workflows
- Building Mapbox applications with AI coding assistants
