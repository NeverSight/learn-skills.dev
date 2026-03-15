---
name: readme-write
description: Create and update README.md files with proper structure, badges, and sections.
license: MIT
compatibility: opencode
disable-model-invocation: true
---

## Skill: readme-write

**Base directory**: .opencode/skill/readme-write

## What I do

I update and create README.md files that follow best practices:

- Choose the right badge set for the project type
- Structure sections appropriately for the project
- Include essential sections (Features, Getting Started, Usage, etc.)
- Add contribution guidelines when applicable
- Match documentation to the actual project structure

## When to use me

Use this when:

- Starting a new project and need a README scaffold
- Improving an existing README for clarity and completeness
- Preparing a project for open source release
- Updating documentation after major features are added

## How I work

### Step 1: Analyze the project

I examine:

- Project type (library, CLI, web app, TUI, etc.)
- Programming language and framework
- Hosting platform (GitHub, GitLab, Bitbucket, generic)
- Existing files and structure
- Package.json or similar config
- Current documentation state
- Check for existing README.md (preserve if updating)
- **Monorepo structure**: Identify if this is a root README or a package-specific README in a monorepo (Lerna, Nx, Turborepo, Pnpm workspaces)

### Step 2: Select appropriate sections

Choose sections based on project type:

**For all projects:**

- Title with one-line description
- Badges (CI, coverage, license, version)
- Quick start example
- Installation instructions
- Link to full documentation

**For libraries:**

- API documentation
- Configuration options
- Examples with code blocks
- Requirements and dependencies

**For CLI tools:**

- Installation (npm, brew, etc.)
- Usage examples with commands
- Available flags and options
- Keyboard shortcuts

**For web applications:**

- Screenshots or demo links
- Deployment instructions
- Environment variables
- Backend requirements

  **For Monorepos:**

- Workspace overview (list of packages)
- Root-level installation and build commands
- Link to package-specific READMEs
- Shared development requirements

### Step 3: Detect configuration and add badges

First, detect what exists:

- **CI/CD**: Check for `.github/workflows/*.yml`, `.travis.yml`, `.circleci/`, `.gitlab-ci.yml`
- **Package managers**: Look for `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`
- **Quality**: Check for `.codecov.yml`, `codeclimate.yml`, `sonar-project.properties`
- **Hosting**: Detect GitHub (.github directory), GitLab (.gitlab-ci.yml), or generic

**Badge URL patterns by platform:**

- **GitHub**: `https://img.shields.io/github/actions/workflow/status/{org}/{repo}/{workflow}.yml`
- **GitLab**: `https://img.shields.io/gitlab/pipeline/{org}/{repo}`
- **Generics**: Use `shields.io/v2/` format

Select badges based on:

- CI/CD: GitHub Actions, Travis, CircleCI, GitLab CI
- Code quality: Codecov, CodeClimate, Sonar
- Package: npm, PyPI, crates.io, Maven
- Social: Discord, Slack, Matrix

### Step 4: Include supplementary sections

Add based on project maturity:

- Contributing guidelines (CONTRIBUTING.md)
- Code of conduct (CODE_OF_CONDUCT.md)
- Security policy (SECURITY.md)
- Changelog (CHANGELOG.md or HISTORY.md)
- License (LICENSE file)

  ## Output format

I create a README.md file with:

- Markdown syntax throughout
- Proper heading hierarchy (H1 title, H2/H3 sections)
- Code blocks with language annotations
- Relative links to local resources
- Badge images in standard sizes
- **Asset management**: Reference images/logos from `/assets` or `/docs/images` using relative paths

## Example output structure

````markdown
# Project Name

Brief description (one line, under 80 characters)

[![CI](https://img.shields.io/github/actions/workflow/status/{org}/{repo}/test.yml)](https://github.com/{org}/{repo}/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![npm version](https://img.shields.io/npm/v/{project}.svg)](https://www.npmjs.com/package/{project})

## Features

- Feature 1 with brief description
- Feature 2 with brief description
- Feature 3 with brief description

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
npm install project-name
```
````

### Usage

```bash
# Basic usage
npm start --option

# Advanced usage
npm start --option --flag value
```

## Documentation

See [docs/](docs/) for detailed guides.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License - see [LICENSE](LICENSE)

## Handling existing READMEs

When a README.md already exists:

1. **Preserve user content**: Keep custom sections, logos, project-specific content
2. **Update structure**: Add missing sections using the proper hierarchy
3. **Modernize badges**: Update badge URLs to current formats while preserving existing choices
4. **Fix formatting**: Correct markdown syntax, heading levels, and code blocks
5. **Update dates**: Refresh version info, last-updated dates

**Never delete**: User-added sections, custom formatting, project-specific troubleshooting guides, creative content

**Always suggest/fix**: Broken links, outdated badges, incorrect code blocks, missing installation instructions

## Platform-specific badge formats

**GitHub Actions:**

```markdown
[![CI](https://img.shields.io/github/actions/workflow/status/{org}/{repo}/{workflow}.yml)](https://github.com/{org}/{repo}/actions)
```

**GitLab CI:**

```markdown
[![CI](https://img.shields.io/gitlab/pipeline/{org}/{repo}])(https://gitlab.com/{org}/{repo}/pipelines)
```

**npm:**

```markdown
[![npm](https://img.shields.io/npm/v/{package})](https://www.npmjs.com/package/{package})
```

**PyPI:**

```markdown
[![PyPI](https://img.shields.io/pypi/v/{package})](https://pypi.org/project/{package}/)
```

**Crates.io:**

```markdown
[![crates.io](https://img.shields.io/crates/v/{package})](https://crates.io/crates/{package})
```

## Validation checklist

Before finalizing, I ensure:

- [ ] Title is clear and searchable
- [ ] Description fits on one line (under 80 characters)
- [ ] Badges are current and link correctly
- [ ] Installation commands work and match the package manager
- [ ] Code examples are syntactically correct
- [ ] Links are relative or absolute correctly
- [ ] Sections are in logical order
- [ ] No placeholder text like `{org}`, `{repo}`, `{package}` remains
- [ ] Heading hierarchy is correct (one H1 for title, H2/H3 for sections)
- [ ] Code blocks have proper language annotations
- [ ] Badge images display correctly
- [ ] Monorepo: Root README links to packages, package READMEs link back to root
- [ ] Assets: Images use relative paths and are stored in appropriate directories
