---
name: shaper-setup
description: Ensure Shaper CLI is installed, configure shaper.json, authenticate, and safely pull remote dashboards/tasks.
---

# Shaper Environment Setup Skill

Use this skill to prepare the local workspace for Shaper dashboard development. It ensures the environment meets all requirements, the Shaper CLI is installed, authentication is configured, and remote resources are safely pulled.

## Workflow

Follow these steps sequentially to setup the environment:

### 1. Operating System Validation
- **Requirement**: Shaper is supported **only** on macOS and Linux. Windows is not supported.
- **Action**: Check the current OS. If the user is running Windows, inform them that Shaper is not supported and halt.

### 2. Verify Shaper CLI Installation
- **Action**: Run `shaper --version`.
- **Handling**:
  - If the command succeeds, proceed to Step 3.
  - If the command fails or `shaper` is not found, stop and instruct the user to install the Shaper CLI by following the official documentation:
    👉 https://taleshape.com/shaper/docs/installing-shaper/

### 3. Manage Configuration File (`shaper.json`)
- **Config Override**: Commands take an optional `--config-file` flag to override the default file path. Check if a custom config file path is passed/configured. The default path is `./shaper.json`.
- **URL Override & Instance Selection**: Commands take an optional `--url <URL>` flag to overwrite the instance URL defined in `shaper.json` with another URL. If the user specifies or indicates that they want to overwrite or target a different Shaper instance (e.g., staging vs. production), adapt all Shaper commands by passing `--url <URL>`.
- **Action**: Check if the configuration file exists at `./shaper.json` (or the path specified by `--config-file`).
- **If the config file does NOT exist**:
  1. Ask the user for the **URL of their Shaper instance** and the **directory to use** (default directory is `.`).
  2. Create the configuration file with the following JSON structure:
     ```json
     {
       "url": "<USER_PROVIDED_URL>",
       "directory": "<USER_PROVIDED_DIRECTORY_OR_DOT>",
       "schemaIgnore": []
     }
     ```
  3. Ensure the JSON is properly formatted and saved.

### 4. Authentication (`shaper login`) & Git Hygiene
- **Explicit Login Requirement**: Shaper CLI commands do not automatically log in the user. You must run `shaper login` before executing other CLI commands.
- **Action**: Execute the login command:
  ```bash
  shaper login
  # Or, if overwriting the instance URL:
  shaper login --url <URL>
  # Or, if using a custom config:
  shaper login --config-file <PATH_TO_CONFIG>
  ```
- **User Action Required**: Executing `shaper login` prompts the user to open a URL and confirm authentication in their browser. Inform the user that they need to open the URL and approve the authentication request.
- **Token Storage**: Successful authentication saves an auth token in a local `.shaper-auth` file (located in the same directory as the configuration or command invocation).
- **Git Hygiene**:
  - Check if `.shaper-auth` is added to your `.gitignore`.
  - If `.gitignore` does not exist, create it.
  - Append `.shaper-auth` to `.gitignore` if it is not already present, ensuring the token is never committed to version control.

### 5. Git Status Check & Data Pulling
- **Safety Rule**: To avoid overwriting work, never pull remote changes if there are uncommitted local edits.
- **Action**: Check the repository's git status by running `git status --porcelain`.
- **Handling**:
  - If there are uncommitted changes, **abort** the pull and warn the user. Ask them to commit or stash their changes first.
  - If git status is clean, run the pull command:
    ```bash
    shaper pull --yes
    # Or, if overwriting the instance URL:
    shaper pull --yes --url <URL>
    # Or, if using a custom config:
    shaper pull --yes --config-file <PATH_TO_CONFIG>
    ```
- **Authentication Failure Handling**: If `shaper pull` (or any subsequent Shaper CLI command) fails due to authentication errors, call `shaper login` to prompt the user to authenticate before retrying.
