---
name: pty-oauth-login
description: Complete an interactive CLI login/OAuth flow (MCP server auth like `claude mcp login <name>`, `claude auth login`, `gh auth login`, etc.) from a headless or non-interactive session, with no SSH and no local terminal on the target machine. Use this whenever a login command fails with "stdin isn't a terminal", hangs waiting for a browser redirect, or the session simply has no TTY — and whenever the user asks to "connect" or "authenticate" a new MCP server, integration, or CLI tool on a specific machine without SSHing in, especially when the approving human is on a different device (phone, laptop) than the one running the CLI. Also reach for this any time OAuth needs to finish inside a headless agent run (e.g. a chat-relayed or cron-triggered session).
---

# PTY OAuth login (no SSH, no local terminal)

Interactive CLI logins (`claude mcp login <name>`, `claude auth login`, `gh
auth login`, and similar) are usually raw-mode TUIs that refuse to run
without a real terminal — they exit immediately with something like `stdin
isn't a terminal` when driven from a plain subprocess/pipe. Naively, that
means SSHing in with a real TTY. It usually doesn't.

Most of these tools have **two** completion paths once they have a real pty:
1. Auto-detect: they open a browser locally and poll the OAuth server until
   the user approves (no callback needed on your end at all — this is the
   easy case, just show the printed URL and wait).
2. Manual fallback: if there's no way to open a browser, they print an
   authorize URL and then wait for the user to **paste the redirect URL**
   back in. The redirect target is typically `localhost:<port>` on the
   machine running the CLI — the browser doing the approving can be on any
   device, since all that matters is that the *code* embedded in that dead
   redirect URL makes it back to the CLI's stdin somehow.

This skill drives that manual fallback from a session that has no terminal
of its own, by giving the CLI a *real* pty (so it doesn't bail out) whose
stdin you can feed asynchronously — even across separate turns, if the human
needs a few minutes to go approve on their phone.

## Procedure

1. **Get a real pty.** Run the target command through `scripts/pty-bridge.py`
   (bundled with this skill — a ~70-line Python wrapper around `pty.fork()`;
   copy it next to where you're running it, or reference it directly). This
   makes the child think it has a controlling terminal regardless of your
   own stdin, which unlocks the manual-paste fallback.

2. **Give it a stdin you can write to later.** A plain pipe closes the
   moment your command finishes. Use a named pipe (FIFO) instead, opened in
   read-write mode so the *open* call never blocks waiting for a peer:

   ```bash
   mkfifo /tmp/login.fifo
   setsid nohup python3 scripts/pty-bridge.py <login-command...> \
     0<>/tmp/login.fifo >/tmp/login.log 2>&1 &
   disown
   ```

   `setsid nohup … & disown` detaches the process from this shell so it
   survives your turn ending — you'll likely need a separate message/turn
   for the human to go approve and paste back the code.

3. **Extract the authorize URL** from `/tmp/login.log` (poll with a short
   sleep loop; give it ~20-30s). The raw output has ANSI/OSC-8 hyperlink
   escapes around it — strip those and pull out the bare
   `https://…/authorize?...` URL.

4. **Hand the URL to the user as a bare, tappable link** — not inside a code
   block/fence, since many chat surfaces (Telegram included) don't
   auto-linkify URLs written that way. Tell them plainly:
   - open it on *any* device (their phone is fine, it does not need to be
     this machine),
   - log in and approve,
   - it will then try to redirect to `localhost:<port>` and **fail to
     load** — that's expected, not an error to worry about,
   - copy the full URL from the address bar at that failed-redirect point
     (it still contains `?code=...&state=...` even though the page didn't
     load) and send it back.

5. **When they send it back, write it into the FIFO** — the raw pasted URL
   is normally fine as-is (most CLIs parse `code`/`state` out of a full
   URL themselves). Send the Enter/carriage-return as a **separate write**,
   not concatenated with the text:

   ```bash
   printf '%s' "$PASTED_URL" > /tmp/login.fifo
   sleep 0.3
   printf '\r' > /tmp/login.fifo
   ```

   This matters: these prompts are almost always raw-mode text inputs
   (Ink or similar). If the code and `\r` arrive in the same write, the
   input widget treats the whole chunk as pasted text and never submits it.
   Use `\r`, not `\n`.

6. **Check the log for success/failure** — look for something like
   `Login successful` / `Authenticated with "<name>"` vs. `OAuth error` /
   `Invalid code` / `expired`. Report the outcome plainly; on failure the
   authorize URL is single-use, so re-run from step 1 rather than retrying
   the same pasted code.

7. **Clean up** — remove the fifo and log file once done
   (`rm -f /tmp/login.fifo /tmp/login.log`), and confirm the credential
   actually stuck (e.g. `claude mcp list` shows `✔ Connected`, `gh auth
   status`, etc.) rather than trusting the log alone.

## Limitations

- Only works for CLIs that actually offer a manual "paste the code/URL"
  fallback. If a tool's login *only* supports automatic local-server
  redirect with zero manual entry option, there's no code to relay and this
  trick can't help — that genuinely needs a browser and terminal on the same
  machine (real SSH, or a port-forward).
- The redirect URL is one-shot and short-lived (the `state`/PKCE challenge
  expires) — don't let a lot of time pass between generating it and the
  user approving it.
- Treat the pasted-back code like a credential while it's in flight — it's
  short-lived and single-use, but avoid logging it anywhere persistent.
