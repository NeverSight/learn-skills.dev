---
name: localtunnel-auto-expose
description: Automatically exposes local services using LocalTunnel via npx and provides the public URL along with the access password. Use when starting a new service or when external web access is requested.
license: MIT
compatibility: opencode
---

# LocalTunnel Auto Expose

## Purpose
Use this skill when you have started a new local web service (or a development server running on a specific port), or when the user explicitly requests an external/public access address for demonstrations, Webhook testing, or mobile testing.

## Execution Steps

1. **Determine the Port**: First, confirm the port number the local service is running on (e.g., 3000, 5173, 8080, etc.). If it cannot be inferred from the context, ask the user.
2. **Start LocalTunnel**:
   Use the following command to start LocalTunnel. Be sure to run it in **background** or **non-blocking mode** (for example, by using `run_command` and sending to background):
   ```bash
   npx localtunnel --port <PORT>
   ```
3. **Extract Public URL**:
   Check the output of LocalTunnel; it will print something like `your url is: https://<random-string>.loca.lt`. This is the user's **public access address**.
4. **Get Access Password**:
   LocalTunnel requires a password by default (usually the public IP of the machine running it) to bypass the anti-phishing warning page. Execute the following command to get this password, selecting the appropriate command based on the current OS:
   - **Windows (PowerShell)**:
     ```powershell
     (Invoke-RestMethod https://loca.lt/mytunnelpassword).ToString().Trim()
     ```
   - **Windows (CMD)**:
     ```cmd
     curl -s https://loca.lt/mytunnelpassword
     ```
   - **Linux / macOS (Bash / Zsh)**:
     ```bash
     curl -s https://loca.lt/mytunnelpassword
     ```
5. **Inform the User**:
   Once you have the URL and the password, present them to the user using a clear Markdown format.

## Feedback Template Example

```markdown
**LocalTunnel Tunnel Started** 🚀

- **Local Service**: `http://localhost:<PORT>`
- **Public URL**: `https://<random-name>.loca.lt`
- **Access Password**: `<Retrieved Password>`

> **Tip**: When accessing the public URL in a browser for the first time, you will be prompted to enter the Endpoint Password. Please use the Access Password provided above. You can stop external access by closing the corresponding background command or terminal.
```

## Notes
- If Node.js/npm is not installed in the environment, remind or assist the user in installing it first.
- The request to get the password (`https://loca.lt/mytunnelpassword`) must be initiated on the **same machine** that is running the LocalTunnel tunnel to obtain the correct password (which is based on the public IP).
