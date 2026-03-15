---
name: find-credential-usage
description: "Search your entire system to find all instances where a specific API key, token, or credential has been used or stored. Use this skill when the user asks to locate, audit, or track where a credential appears across files, environment variables, configuration files, logs, or shell history. Helps identify security risks and credential exposure."
---

# Find Credential Usage

## Input Parameters

| Parameter              | Required | Description                                                                                                              | Example                  |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| `credential_to_search` | Yes      | The API key, token, password, or credential string to search for                                                         | sk-svcacct-2HXNWxbX0cap |
| `search_scope`         | No       | `full` (entire home directory), `projects` (Code/Herd only), or `critical` (.env and config files only)                  | full                     |

## Procedure

1. Ask for the credential to search if not provided
2. Search each location and collect results:

   ```bash
   # Environment variables
   env | grep -i "{{SEARCH_TERM}}"

   # Shell profiles
   grep -r "{{SEARCH_TERM}}" ~/.zshrc ~/.bashrc ~/.bash_profile ~/.profile ~/.zprofile 2>/dev/null

   # Shell history
   history | grep -i "{{SEARCH_TERM}}"

   # .env files (home directory, 3 levels deep)
   cd ~ && find . -maxdepth 3 -type f -name "*.env*" -exec grep -l "{{SEARCH_TERM}}" {} \; 2>/dev/null

   # Project directories
   grep -r "{{SEARCH_TERM}}" ~/Code ~/Herd 2>/dev/null | head -50

   # macOS Keychain
   security find-generic-password -w -s "{{SEARCH_TERM}}" 2>/dev/null || echo "Not found in Keychain"
   ```

3. Compile results into a markdown report organized by location type (env vars, shell profiles, .env files, keychain, project files)
4. Display a summary with total instance count and file paths

## Notes

- Search runs locally — credentials are not transmitted externally
- Results may include sensitive information; handle the generated report carefully
- Large searches may take several minutes
- Shell history is unsearchable if history logging is disabled

## Example

```
find all instances where I have used this API key across my system
where is this token stored on my machine
audit where this API key appears in my files
check if this credential is exposed anywhere on my system
scan my projects and config files for this secret
```
