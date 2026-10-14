---
name: docsify
description: Helps users quickly generate and manage Docsify documentation projects with version management to prevent breaking changes
version: 1.0.0
commands:
  - name: docsify init
    description: Initialize a new Docsify project structure
  - name: docsify serve
    description: Start a local Docsify development server
  - name: docsify generate
    description: Generate documentation from source code or Markdown files
---

# Docsify Documentation Generator Skill

## Description
Helps users quickly generate and manage Docsify documentation projects. This skill provides functionality for initializing projects, generating documentation structure, configuration, and deployment.

## 📁 Skill Project Structure

This skill is located in a certain organized project with the following structure or in the global skill folder:

```

├── .claude/
│   └── skills/
      └──docsify-skill/
│          └── SKILL.md          ← This file (skill definition) 
└── (other project files)
```

**Key Files:**
- **`.claude/skills/docsify-skill/SKILL.md`** - Main skill definition with all commands and documentation

## Prerequisites & Installation

Before using this skill, ensure you have the following dependencies installed:

### Required Dependencies

**1. Node.js (v12 or higher)**
- Download from: https://nodejs.org/
- Check installation: `node --version`

**2. npm (comes with Node.js)**
- Check installation: `npm --version`

**3. docsify-cli**
Install globally using npm:
```bash
npm install -g docsify-cli
```

### Optional Dependencies (for advanced features)

- **Git** - For version control integration
- **Python 3** - For documentation generation from code
- **Docsify plugins** - Install specific plugins as needed

### Quick Setup Guide

```bash
# 1. Install Node.js from https://nodejs.org/

# 2. Verify Node.js and npm installation
node --version
npm --version

# 3. Install docsify-cli globally (latest stable version)
npm install -g docsify-cli

# 4. Verify docsify installation
docsify --version

# 5. You're ready to use this skill!
/docsify init --name my-project
```

### Version Management - Installing Specific Major Versions

To avoid breaking changes and ensure compatibility, you can install specific major versions:

**Install with a specific major version:**
```bash
# Install docsify-cli v4.x.x (stable)
npm install -g docsify-cli@4

# Install docsify-cli v5.x.x (latest major version)
npm install -g docsify-cli@5

# Install an exact version
npm install -g docsify-cli@4.13.1
```

**Install packages in your project with version pinning:**
```bash
# Install docsify v4 in your project
npm install docsify@4

# Install docsify v5 in your project
npm install docsify@5

# Install with package.json for version management
npm install docsify@^4.13.0  # Allow minor/patch updates in v4
npm install docsify@~4.13.0  # Allow patch updates only in v4.13.x
```

**Check available versions:**
```bash
# View all available versions
npm view docsify versions

# View version ranges
npm info docsify
```

**Why version pinning matters:**
- ✅ Prevents unexpected breaking changes
- ✅ Ensures team consistency
- ✅ Makes deployment predictable
- ✅ Easier debugging and maintenance

### Troubleshooting Installation

**Issue: docsify command not found**
- Solution: Make sure docsify-cli is installed globally: `npm install -g docsify-cli`

**Issue: npm: command not found**
- Solution: Install Node.js from https://nodejs.org/ and restart your terminal

**Issue: Permission denied when installing globally**
- Solution: Use sudo or configure npm permissions: https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally

## Usage

### /docsify init
Initialize a new Docsify project structure

**Options:**
- `--name [project-name]` - Project name (required, alphanumeric and hyphens only)
- `--path [directory]` - Project path (supports relative or absolute paths; defaults to current directory)
- `--theme [theme]` - Theme selection
  - `vue` - Default Vue theme
  - `dark` - Dark theme variant
  - `buble` - Bubble theme (lightweight)
  - `dolphin` - Dolphin theme
- `--version [version]` - Major version to use
  - `@4` - Stable version (recommended for most projects)
  - `@5` - Latest version with new features
  - Exact version: `@4.13.1`

**Output:**
After successful execution, you should see:
```
✓ Project created successfully
✓ Dependencies installed at [project-path]
✓ Use 'docsify serve' to preview
```

**Files Created:**
- `index.html` - Main entry point
- `package.json` - With docsify dependency pinned
- `docs/README.md` - Home page
- `_sidebar.md` - Navigation (if selected)
- `_config.js` - Configuration file

**Examples:**
```
/docsify init --name my-docs
/docsify init --path ./docs --theme dark
/docsify init --name my-docs --version @4
/docsify init --name my-docs --version @5
```

**💡 Helper Prompts:**
- Should include a README with project overview?
- Do you want to add a sidebar navigation (_sidebar.md)?
- Should we configure a search index?
- Do you need a custom cover page?
- Would you like sample documentation pages?
- Which major version of docsify would you prefer? (@4 for stability, @5 for latest features)

### /docsify generate
Generate documentation from source code or Markdown files

**Options:**
- `--source [path]` - Source file path
- `--output [path]` - Output path
- `--format [format]` - Output format (markdown, html)

**Examples:**
```
/docsify generate --source ./src --output ./docs
```

**💡 Helper Prompts:**
- What programming language are your source files in?
- Do you want to include API documentation?
- Should we extract comments as documentation?
- Do you need to generate table of contents automatically?
- Would you like code examples included?

### /docsify serve
Start a local Docsify development server for preview

**Options:**
- `--port [port]` - Server port (numeric, default 3000; range: 1000-65535)

**Output:**
```
Serving now ~ listening at http://localhost:3000
✓ Listening on http://localhost:3000
```

**Access:**
- Open browser to `http://localhost:3000`
- Changes to markdown files auto-reload
- Stop server: Press `Ctrl+C` in terminal

**Common Issues:**
- Port already in use: Use `--port 3001` to try different port
- Changes not showing: Refresh browser (Ctrl+R or Cmd+R)
- Server won't start: Check if Node.js/docsify is properly installed

**Examples:**
```
/docsify serve --port 3000
/docsify serve --port 3001
```

**💡 Helper Prompts:**
- Which port would you like to use?
- Do you want hot reload enabled?
- Would you like to open the browser automatically?

## Features

- ✅ Quick project initialization
- ✅ Version-specific dependency installation (@4, @5, or exact versions)
- ✅ Automatic documentation structure generation
- ✅ Custom configuration support
- ✅ Local preview functionality
- ✅ Automatic code documentation
- ✅ Multiple theme support
- ✅ SEO configuration
- ✅ Search functionality integration
- ✅ Breaking change prevention with version pinning

## 📁 Generated Docsify Project Structure

When you use `/docsify init`, the following structure is created:

```
my-project/
├── index.html              # Main Docsify entry point
├── README.md               # Project homepage/landing page
├── _sidebar.md             # Left navigation sidebar (optional)
├── _navbar.md              # Top navigation menu (optional)
├── _coverpage.md           # Custom cover/landing page (optional)
├── _config.js              # Docsify configuration file
├── package.json            # Node.js dependencies and scripts
├── package-lock.json       # Locked dependency versions
├── docs/                   # Main documentation folder
│   ├── getting-started.md
│   ├── installation.md
│   ├── usage.md
│   ├── api/
│   │   ├── README.md
│   │   ├── endpoints.md
│   │   └── authentication.md
│   ├── guides/
│   │   ├── README.md
│   │   ├── tutorial.md
│   │   └── best-practices.md
│   ├── examples/
│   │   ├── basic-example.md
│   │   └── advanced-example.md
│   └── troubleshooting.md
└── .nojekyll               # For GitHub Pages deployment
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `index.html` | Main entry point for Docsify - defines UI and CDN dependencies |
| `package.json` | Manages Node.js dependencies (docsify, docsify-cli) and versions |
| `package-lock.json` | Locks exact versions of all dependencies (commit this to git) |
| `README.md` | Homepage/cover page - first thing users see |
| `_sidebar.md` | Defines left sidebar navigation structure |
| `_navbar.md` | Defines top navigation menu (optional) |
| `_coverpage.md` | Custom cover page design (optional) |
| `_config.js` | Docsify configuration (theme, plugins, metadata) |
| `docs/` | Main documentation folder containing all your markdown files |
| `.nojekyll` | Required for GitHub Pages (tells it not to process with Jekyll) |

### Documentation Folder Organization

The `docs/` folder should be organized logically:

```
docs/
├── README.md               # Start page (don't rename!)
├── getting-started.md      # Getting started guide
├── api/
│   ├── README.md           # API overview
│   ├── endpoints.md
│   ├── authentication.md
│   └── error-handling.md
├── guides/
│   ├── README.md           # Guides overview
│   ├── installation.md
│   ├── configuration.md
│   ├── deployment.md
│   └── troubleshooting.md
├── examples/
│   ├── README.md           # Examples overview
│   ├── basic-usage.md
│   ├── advanced-patterns.md
│   └── integration.md
└── contributing.md         # Contribution guidelines
```

### Version Control (.gitignore)

Typical files to ignore:

```
node_modules/
package-lock.json          # Optional: some teams prefer to commit this
*.log
.DS_Store
dist/
.env
```

### Package.json Example

```json
{
  "name": "my-project-docs",
  "version": "1.0.0",
  "description": "Documentation for My Project",
  "scripts": {
    "serve": "docsify serve"
  },
  "devDependencies": {
    "docsify-cli": "^4.13.1"
  }
}
```

### Important Naming Conventions

⚠️ **Do NOT rename these files** - they have special meanings in Docsify:
- `README.md` - Always the home page (must be lowercase)
- `_sidebar.md` - Sidebar navigation (underscore prefix is required)
- `_navbar.md` - Top navigation (underscore prefix is required)
- `_coverpage.md` - Cover page (underscore prefix is required)
- `index.html` - Main entry point (case-sensitive)
- `.nojekyll` - GitHub Pages config (hidden file)

## Workflow Examples

### Basic Workflow
```
1. /docsify init --name my-project --version @4
2. /docsify serve
3. Edit markdown files in docs/ folder
4. Commit and deploy to static hosting
```

### Recommended Workflow
```
1. /docsify init --name my-project --version @4  # Initialize with v4
2. /docsify serve                                 # Start dev server locally
3. /docsify generate --source ./src               # Generate docs from code (optional)
4. Add/edit markdown files in docs/ folder
5. Deploy docs/ folder to GitHub Pages, Netlify, or Vercel
```

## Tips & Best Practices

### Documentation Organization
- **Use clear hierarchies**: Organize content in logical sections
- **Consistent naming**: Use descriptive file names (e.g., `getting-started.md`, `api-reference.md`)
- **README first**: Start with a clear README that explains what the project does
- **Navigation clarity**: Keep sidebar navigation simple and intuitive

### Content Writing
- **Keep it simple**: Write documentation for different experience levels
- **Use examples**: Include code examples and real-world use cases
- **Add visuals**: Use diagrams and screenshots where appropriate
- **Update regularly**: Keep documentation in sync with your codebase

### Performance & Deployment
- **Local testing**: Always test locally before deploying
- **Enable search**: Help users find information quickly
- **Mobile responsive**: Test on different screen sizes
- **Version management**: Consider versioning for different releases

### Dependency Version Management
- **Lock major versions**: Use `@4` or `@5` to prevent unexpected breaking changes
- **Document versions**: Record which docsify version your project uses
- **Test before upgrading**: Always test major version upgrades in a dev environment
- **Use package.json**: Save exact versions in package.json for consistency across teams
- **Communicate changes**: Notify your team when upgrading major versions
- **Check breaking changes**: Review release notes before upgrading
- **Maintain backward compatibility**: Keep old documentation available during transitions

### Common Workflows
```
# Quick start for new project
/docsify init --name my-docs --version @4
cd my-docs
/docsify serve

# Edit docs/ folder with your markdown files
# Then deploy the entire project to GitHub Pages, Netlify, or Vercel
```

### Useful Resources
- Docsify Official: https://docsify.js.org
- Markdown Guide: https://www.markdownguide.org
- Docsify Plugins: https://docsify.js.org/#/plugins
- Docsify Themes: https://docsify.js.org/#/themes

## Frequently Asked Questions

### ❓ General

**Q: What's the difference between v4 and v5?**
A: v4 is stable and battle-tested; v5 has new features but may have breaking changes. Use @4 unless you need v5 features.

**Q: How do I upgrade from v4 to v5 later?**
A: Edit `package.json` and change `docsify@4` to `docsify@5`, then run `npm install`. Test thoroughly before deploying.

**Q: Do I need to install docsify globally or locally?**
A: Local install (in the project) is recommended. Each project gets its own version in `package.json`.

**Q: How do I configure the project (title, theme, etc)?**
A: Edit `_config.js` in your project root to customize title, theme, plugins, and other settings.

### 🛠️ Troubleshooting

**Q: I get "project already exists" error**
A: Use a different project name or specify a different `--path`

**Q: Commands aren't showing in auto-complete**
A: Restart Claude Code or reload the skills

**Q: Port 3000 is already in use**
A: Use `/docsify serve --port 3001` or find what's using 3000 and close it

**Q: My changes don't appear when I reload the page**
A: Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R), or restart the server

**Q: docsify command not found**
A: Make sure docsify-cli is installed globally: `npm install -g docsify-cli`

### 📋 Quick Reference

| Task | Command |
|------|---------|
| Create new project | `/docsify init --name my-docs --version @4` |
| Start dev server | `/docsify serve` |
| Generate docs from code | `/docsify generate --source ./src --output ./docs` |
| Stop server | Press `Ctrl+C` in terminal |
| Deploy | Push entire project (or just docs/ folder) to static hosting |

### ✅ Pre-flight Checklist

Before starting, verify:
- [ ] Node.js installed: `node --version` (should be v12+)
- [ ] npm installed: `npm --version`
- [ ] docsify-cli installed: `docsify --version`
- [ ] Have a directory ready for your project
- [ ] Choose a version (@4 recommended for beginners)

## Notes

- Ensure Node.js and docsify-cli are installed before using
- Project structure will be created automatically with `/docsify init`
- Configuration file is `_config.js` (edit directly to customize)
- Documentation files go in the `docs/` directory (all markdown files)
- Each project has its own `package.json` for version management
- Version must start with `@` (e.g., `@4`, not `4`) when specifying versions
- Deploy by pushing your entire project folder (or just docs/ folder) to static hosting
- Success indicators: ✓ marks in output, created files visible in directory
