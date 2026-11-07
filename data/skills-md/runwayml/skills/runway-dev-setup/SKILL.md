---
name: runway-dev-setup
description: "Use when the user installs or starts using Runway Dev, needs to sign in or create a Developer Portal account, connect Dev MCP, verify account/project access, or finish setup after a developer_not_found error. Guide the user through the browser steps and continue with the task once setup succeeds."
user-invocable: true
---

# Set up Runway Dev

Guide the user from plugin installation to a connected Developer Portal account. This skill is included with the plugin; use it directly and do not install or fetch a duplicate copy.

First check whether the bundled Runway Dev MCP is already connected. If `whoami` succeeds, skip sign-in and continue with project selection. If the server is configured but needs authentication, use the host's connection flow rather than adding another server entry.

## 1. Sign in or create an account

Ask whether the user already has a Runway Dev account only if that is not clear from the conversation. Send them to the [Runway Dev Developer Portal](https://dev.runway.com/): they can sign in with an existing account or create one there. Let the user complete any sign-up, verification, and consent steps themselves in their browser. Do not automate the browser authentication or create an account on the user's behalf.

If they are building an application integration, explain that Developer Portal access alone does not configure the application. They may need to select or create a project and create a project API key in the portal. Follow [API setup](https://docs.dev.runwayml.com/guides/setup/) for current project and key steps. Do not request that the user paste the key into chat.

## 2. Connect Dev MCP

Connect the host to `https://dev.runwayml.com/mcp` using the host's documented MCP setup at [Connect Runway Dev](https://docs.dev.runwayml.com/guides/mcp/). MCP uses browser OAuth. The application SDK uses a separate project API key; never put that key in MCP configuration.

If the MCP server is not configured, help add it using the exact configuration format documented for the user's host. Do not assume every host supports the same plugin-install flow or command. If the host is unknown, link the connection guide and ask which host they are using before editing host-specific config.

When prompted, have the user complete Runway OAuth in their normal browser, return to the same agent session, and retry the MCP check. Never ask for their Runway password, OAuth code, or API key.

For the Codex CLI, run `codex mcp login runway-dev` after installing the plugin to authenticate its bundled connection. Credentials are associated with the configured MCP connection, so signing in through a separately named test entry does not authenticate the bundled server.

## 3. Confirm the account and project

After OAuth completes, call `whoami` and report the connected Developer Portal email or identity shown by the tool. If the user has an app to connect, call `list_projects` and let them choose among accessible projects. Do not guess or silently select a project when there are multiple candidates.

If the user has no project, direct them to create or select one in the Developer Portal, then call `list_projects` again. Do not invent a project-creation MCP tool or call a REST endpoint as a substitute.

## 4. Recover account setup errors

If MCP returns HTTP 403 with the explicit `developer_not_found` error, the OAuth identity is valid but its Developer Portal setup is incomplete. Use `signup_url` from the error response for a new account and `login_url` for an existing account. Older server versions may return only `login_url`; use that link and the current account-setup guide. Show the applicable link and let the user complete setup in their browser. Then have them retry or reconnect Runway Dev in the same coding client, call `whoami` again, and call `list_projects` if the task needs a project.

Do not replace the error's supplied signup/login URL with a guessed account path, infer missing account state from another tool's output, create credentials, change OAuth scopes, or try alternate identity endpoints. If the same error remains after the user reconnects, stop the MCP-dependent action and report the exact blocker. Continue any work that can proceed from public docs and existing application configuration.

## 5. Configure the application key only when needed

For SDK integration work, check whether `RUNWAYML_API_SECRET` is configured without printing its value. If not, direct the user to create a project key in Developer Portal and store it in the app server's environment or secret manager. Keep the key server-side and out of browser bundles, chat, source control, and MCP config. A key is not required merely to connect MCP.

## Links

- [Runway Dev account and MCP setup](https://docs.dev.runwayml.com/guides/mcp/)
- [Project and API key setup](https://docs.dev.runwayml.com/guides/setup/)
- [Runway Dev API security guidance](https://docs.dev.runwayml.com/guides/go-live/)
