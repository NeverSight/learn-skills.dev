---
name: meegle-mcp
description: Interact with Meegle project management system via MCP protocol
homepage: https://www.meegle.com/
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw": {"requires": {"env": ["MEEGLE_USER_KEY"]}, "primaryEnv": "MEEGLE_USER_KEY", "emoji": "📊", "os": ["darwin", "linux", "win32"]}}
---

# Meegle MCP Skill

Integrate Meegle (visual workflow and project management tool) with OpenClaw using the Model Context Protocol (MCP).

## What is Meegle?

Meegle is a leading visual project management tool powered by Larksuite, designed for agile teams. It provides:
- Customizable Kanban boards and Gantt charts
- Real-time collaboration with integrated chat
- Workflow automation and custom pipelines
- Time tracking and analytics dashboard
- Client portal access for external stakeholders

## Setup

### Prerequisites

You need:
1. A Meegle account with API access
2. Your `MEEGLE_USER_KEY` from your Meegle workspace

### Configuration

#### Option 1: Environment Variable (Recommended)

Set your user key as an environment variable:

```bash
export MEEGLE_USER_KEY="your_user_key_here"
export MEEGLE_MCP_KEY="your_mcp_key_here"
```

Add this to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) to persist across sessions.

#### Option 2: OpenClaw Config

Add the MCP server configuration to your OpenClaw settings:

1. Edit or create your OpenClaw MCP servers config file
2. Add the Meegle MCP server configuration:

```json
{
  "mcpServers": {
    "meegle": {
      "command": "node",
      "args": ["{baseDir}/scripts/mcp-proxy.js"],
      "env": {
        "MEEGLE_USER_KEY": "your_user_key_here",
        "MEEGLE_MCP_URL": "https://project.larksuite.com/mcp_server/v1",
        "MEEGLE_MCP_KEY": "your_mcp_key_here"
      },
      "status": "active"
    }
  }
}
```

#### Option 3: Using mcporter (Alternative)

If you have `mcporter` installed:

```bash
mcporter add meegle \
  --url "https://project.larksuite.com/mcp_server/v1?mcpKey=your_mcp_key_here&userKey={user_key}" \
  --env MEEGLE_USER_KEY=your_user_key_here
```

### Installation

**Via ClawHub (Recommended):**
```bash
clawhub install meegle-mcp
```

**From GitHub:**
```bash
git clone <this-repo-url> meegle-mcp
cd meegle-mcp
./scripts/setup.sh
```

Then restart OpenClaw and verify installation:
   ```bash
   openclaw skills list | grep meegle
   ```

## Available Tools

Once configured, the Meegle MCP server provides various tools for project management. Common operations include:

### Project Management
- **List Projects**: View all projects in your workspace
- **Create Project**: Set up new projects with custom workflows
- **Update Project**: Modify project details, status, or members

### Task Operations
- **Create Task**: Add new tasks with assignees, due dates, and priorities
- **List Tasks**: Filter and search tasks by project, assignee, or status
- **Update Task**: Change task properties, move between workflow stages
- **Get Task Details**: View comprehensive task information

### Workflow Management
- **Get Workflows**: List available workflow templates
- **Apply Workflow**: Assign workflows to projects
- **Update Workflow Stage**: Move items through workflow stages

### Team Collaboration
- **Add Members**: Invite team members to projects
- **List Members**: View project participants and roles
- **Update Permissions**: Manage access levels

### Analytics & Reporting
- **Get Project Stats**: View progress, completion rates, and metrics
- **Time Tracking**: Log and query time entries
- **Generate Reports**: Create custom reports on project data

## Usage Examples

### Creating a New Project
```
Create a new Meegle project called "Q1 Website Redesign" with a Kanban workflow
```

### Managing Tasks
```
Show me all high-priority tasks assigned to me in Meegle
```

```
Create a task in Meegle: "Update landing page copy" assigned to @designer, due next Friday
```

### Workflow Operations
```
Move the task "Homepage mockups" to the "In Review" stage in Meegle
```

### Team Coordination
```
Add john@company.com as a contributor to the "Mobile App" project in Meegle
```

### Reporting
```
Generate a summary of completed tasks in Meegle for the past week
```

## Limitations

- **Authentication**: Requires a valid `MEEGLE_USER_KEY` with appropriate permissions
- **Rate Limits**: Subject to Meegle API rate limits (check your plan)
- **Read-Only Operations**: Some operations may be restricted based on your role
- **Workspace Scope**: Only accesses projects in your authorized workspace

## Security Notes

- **Never commit your `MEEGLE_USER_KEY`** to version control
- Store credentials in environment variables or secure config files
- Review permissions before granting OpenClaw access to Meegle
- Consider using a dedicated service account for automation

## Troubleshooting

### "Authentication failed" error
- Verify your `MEEGLE_USER_KEY` is correct
- Ensure the key has not expired or been revoked
- Check that your Meegle account has API access enabled

### "MCP server not responding"
- Verify network connectivity to `project.larksuite.com`
- Check that the MCP server URL and key are correct
- Review OpenClaw logs: `openclaw logs --filter=meegle`

### Tools not appearing
- Restart OpenClaw after installation
- Check skill is loaded: `openclaw skills list`
- Verify environment variables are set correctly

## Resources

- [Meegle Official Website](https://www.meegle.com/)
- [Meegle Documentation](https://www.larksuite.com/hc/en-US/articles/040270863407-meegle-overview)
- [Larksuite Platform](https://www.larksuite.com/)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)

## Feedback

Issues or suggestions? Open an issue on the skill repository or contact via ClawHub.

---

**Note**: This skill uses the Model Context Protocol to communicate with Meegle's MCP server. Tool availability and capabilities depend on your Meegle plan and permissions.
