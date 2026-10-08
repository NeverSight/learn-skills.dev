---
name: abapgit
description: Help with abapGit workflows including repository setup, cloning, serialization, branching strategies, transport-vs-git workflows, CI/CD integration, and .abapgit.xml configuration. Use when users ask about abapGit, git for ABAP, ABAP version control, abapGit clone, abapGit pull, abapGit push, branching strategy for ABAP, abapGit configuration, serialization, deserialization, transport vs git, gCTS, abapGit CI/CD, or managing ABAP code in git repositories. Triggers include "set up abapGit", "clone a repo", "push ABAP to git", "abapGit branching", "abapGit configuration", ".abapgit.xml", "transport vs git", or "CI/CD for ABAP".
---

# abapGit Workflows

Guide for managing ABAP development objects in Git repositories using abapGit.

## Workflow

1. **Determine the user's goal**:
   - Setting up abapGit for the first time
   - Cloning an existing repository
   - Pushing ABAP code to a Git repository
   - Configuring branching or transport strategies
   - Setting up CI/CD pipelines for ABAP
   - Troubleshooting abapGit issues

2. **Identify the environment**:
   - On-premise SAP system with abapGit standalone
   - SAP BTP ABAP Environment (abapGit integration in ADT)
   - gCTS (Git-enabled Change and Transport System)

3. **Guide implementation** with best practices for ABAP-specific Git workflows

## abapGit Overview

| Aspect                | Description                                                       |
| --------------------- | ----------------------------------------------------------------- |
| **What**              | Open-source Git client for ABAP, runs inside the SAP system       |
| **Serialization**     | Converts ABAP objects to file-based format for Git storage        |
| **Deserialization**   | Imports file-based format back into ABAP objects in the system    |
| **Supported Objects** | Classes, interfaces, CDS, function groups, programs, tables, etc. |
| **Installation**      | Via abapGit standalone report or Eclipse plugin                   |

## Setup

### Installing abapGit Standalone (On-Premise)

1. Create report `ZABAPGIT_STANDALONE` or `ZABAPGIT_FULL`
2. Download latest version from https://raw.githubusercontent.com/abapGit/build/main/zabapgit_standalone.prog.abap
3. Copy content into the report and activate
4. Run the report via `SE38` or transaction `ZABAPGIT`

### abapGit in ADT (BTP ABAP Environment)

1. In ADT: **Window → Show View → Other → abapGit Repositories**
2. Link repository using HTTPS URL
3. Requires communication arrangement for Git service

### SSL Certificates

- Download GitHub/GitLab root certificates
- Import via `STRUST` (transaction) → SSL Client (Anonymous) or (Standard)
- Required for HTTPS connections to Git providers

## Core Operations

### Clone a Repository

```
1. Open abapGit (standalone or ADT)
2. Click "+ Clone" / "Link abapGit Repository"
3. Enter repository URL (HTTPS)
4. Select target package (create if needed)
5. Select branch (default: main)
6. Pull objects into the system
```

### Push Changes to Git

```
1. Stage changed objects (select what to include)
2. Write a meaningful commit message
3. Push to remote branch
4. Resolve conflicts if any
```

### Pull Updates from Git

```
1. Open the repository in abapGit
2. Click "Pull"
3. Review incoming changes
4. Activate pulled objects
```

## .abapgit.xml Configuration

The `.abapgit.xml` file in the repository root controls serialization settings:

```xml
<?xml version="1.0" encoding="utf-8"?>
<asx:abap xmlns:asx="http://www.sap.com/abapxml" version="1.0">
 <asx:values>
  <DATA>
   <MASTER_LANGUAGE>E</MASTER_LANGUAGE>
   <STARTING_FOLDER>/src/</STARTING_FOLDER>
   <FOLDER_LOGIC>PREFIX</FOLDER_LOGIC>
   <IGNORE>
    <item>/.gitignore</item>
    <item>/LICENSE</item>
    <item>/README.md</item>
    <item>/package.json</item>
    <item>/.travis.yml</item>
   </IGNORE>
   <REQUIREMENTS/>
  </DATA>
 </asx:values>
</asx:abap>
```

### Key Settings

| Setting           | Values              | Description                                     |
| ----------------- | ------------------- | ----------------------------------------------- |
| `MASTER_LANGUAGE` | `E`, `D`, etc.      | Master language for texts                       |
| `STARTING_FOLDER` | `/src/`             | Root folder for serialized objects              |
| `FOLDER_LOGIC`    | `PREFIX` / `FULL`   | How package hierarchy maps to folders           |
| `IGNORE`          | File patterns       | Files to exclude from deserialization           |
| `REQUIREMENTS`    | Software components | Dependencies that must be present before import |

### Folder Logic

- **PREFIX**: Package name prefix is removed. `Z_PKG_SUB` under `Z_PKG` → `sub/` folder
- **FULL**: Full package name becomes folder. `Z_PKG_SUB` → `z_pkg_sub/`

## Branching Strategy

### Recommended: Trunk-Based for ABAP

```
main (production-ready)
  └── feature/add-validation
  └── feature/new-report
  └── bugfix/fix-calculation
```

- Keep `main` branch stable and deployable
- Create short-lived feature branches
- Merge via pull requests with code review
- One SAP system per branch for development

### Transport-Based Strategy

```
DEV system ←→ feature branches
QAS system ←→ release branch
PRD system ←  main branch (tags for releases)
```

## Transport vs. Git Workflows

| Aspect                  | Transport-Based     | Git-Based (abapGit)                      |
| ----------------------- | ------------------- | ---------------------------------------- |
| **Versioning**          | Transport requests  | Git commits with full history            |
| **Collaboration**       | Transport of copies | Branches, pull requests, code review     |
| **Rollback**            | Difficult           | `git revert` or checkout previous commit |
| **CI/CD**               | Limited             | Full integration with pipelines          |
| **Multi-system**        | Transport routes    | Clone/pull to each system                |
| **Conflict resolution** | Manual              | Git merge tools                          |

### Hybrid Approach

Many teams use abapGit for version control while retaining transports for deployment:

1. Develop in DEV system
2. Commit changes to Git (abapGit push)
3. Use transport requests to move to QAS/PRD
4. Git serves as source of truth and backup

## CI/CD Integration

### abaplint in CI Pipeline

```yaml
# .github/workflows/abaplint.yml
name: abaplint
on: [push, pull_request]
jobs:
  abaplint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: niclas-timm/abaplint-action@main
```

### abaplint.json Configuration

```json
{
  "global": {
    "files": "/src/**/*.*"
  },
  "syntax": {
    "version": "Cloud",
    "errorNamespace": "^(Z|Y|LCL_|LIF_)"
  },
  "rules": {
    "description": "ABAP lint configuration"
  }
}
```

## Troubleshooting

| Issue                      | Solution                                     |
| -------------------------- | -------------------------------------------- |
| SSL handshake error        | Import SSL certificates via `STRUST`         |
| Authorization error        | Check `S_DEVELOP` authorization object       |
| Object locked by transport | Release or remove transport lock             |
| Serialization error        | Check object type support in abapGit         |
| Namespace conflicts        | Ensure unique naming conventions             |
| Large repository slow      | Use shallow clone or split into sub-packages |

## Output Format

When helping with abapGit topics, structure responses as:

```markdown
## abapGit Guidance

### Context

- Environment: [On-premise / BTP / gCTS]
- Operation: [Clone / Push / Pull / Setup]

### Steps

[Step-by-step instructions]

### Configuration

[Relevant .abapgit.xml or abaplint settings]
```

## References

- abapGit Documentation: https://docs.abapgit.org/
- abapGit GitHub: https://github.com/abapGit/abapGit
- abaplint: https://abaplint.org/

## Related Skills

- **abap**: Use for abaplint integration with abapGit repositories
- **btp-abap-environment**: Use for abapGit setup in BTP ABAP Environment
- **abap-cloud**: Use for ensuring abapGit repositories are ABAP Cloud compliant
