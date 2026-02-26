---
name: mcp-jetbrains-ide
description: Control JetBrains IDE (IntelliJ, WebStorm, PyCharm) via MCP. Use when manipulating IDE files, running configurations, searching code, or performing refactoring. Triggers on "open in IDE", "run configuration", "refactor code", "IDE search", "JetBrains".
---

# JetBrains IDE MCP

MCP service at `http://localhost:64342/sse` (sse) with 21 tools.

## Requirements

- `mh` CLI must be installed. If not available, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/vaayne/mcphub/main/scripts/install.sh | sh
  ```

## Usage

List tools: `mh list -u http://localhost:64342/sse -t sse`
Get tool details: `mh inspect -u http://localhost:64342/sse -t sse <tool-name>`
Invoke tool: `mh invoke -u http://localhost:64342/sse -t sse <tool-name> '{"param": "value"}'`

## Notes

- Run `inspect` before invoking unfamiliar tools to get full parameter schema
- Timeout: 30s default, use `--timeout <seconds>` to adjust
- The IDE must be running with the MCP plugin active for this to work

## Tools

| Tool                      | Description                                                                                  |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| `buildProject`            | Triggers building of the project, returns build errors. Use after edits to validate changes. |
| `createNewFile`           | Creates a new file at the specified path, optionally with initial content.                   |
| `executeRunConfiguration` | Run a specific run configuration and wait for completion.                                    |
| `findFilesByGlob`         | Search for files matching a glob pattern (e.g. `**/*.txt`).                                  |
| `findFilesByNameKeyword`  | Search for files by name keyword (case-insensitive).                                         |
| `getAllOpenFilePaths`     | Get paths of all currently open files in the editor.                                         |
| `getFileProblems`         | Analyze a file for errors and warnings using IDE inspections.                                |
| `getFileTextByPath`       | Read file contents by project-relative path.                                                 |
| `getProjectDependencies`  | Get list of all project dependencies.                                                        |
| `getProjectModules`       | Get list of all modules with their types.                                                    |
| `getRepositories`         | Get list of VCS roots in the project.                                                        |
| `getRunConfigurations`    | Get available run configurations with details.                                               |
| `getSymbolInfo`           | Get Quick Documentation info for a symbol at position.                                       |
| `listDirectoryTree`       | Get tree representation of a directory structure.                                            |
| `openFileInEditor`        | Open a file in the IDE editor.                                                               |
| `permissionPrompt`        | Handle permission prompts.                                                                   |
| `reformatFile`            | Apply code formatting rules to a file.                                                       |
| `renameRefactoring`       | Rename a symbol with full project-wide refactoring.                                          |
| `replaceTextInFile`       | Replace text in a file with find/replace options.                                            |
| `searchInFilesByRegex`    | Search project files using regex pattern.                                                    |
| `searchInFilesByText`     | Search project files for text substring.                                                     |
