---
name: drawover
description: Explain anything by drawing it live on the user's screen with the drawover app (Windows and macOS) - 3D models built part by part with labels and motion, or hand-drawn whiteboard diagrams. Use when the user invokes drawover, or asks you to draw, show, sketch or visualise how something works on their screen.
---

# drawover

drawover is a see-through layer over the user's screen. You send it drawing lines (JSONL, one JSON object per line) and it draws them one by one, with a pen, while you keep sending more. You are the artist: work out the picture yourself, then send it in small batches so the user watches it grow.

## 1. Check the app (once per chat)

Send `GET http://127.0.0.1:47823/status`. A JSON reply with `"app":"drawover"` means it is ready; go to step 2.

No reply:
- Not Windows or macOS: tell the user drawover runs on Windows and macOS only for now, and stop.
- Windows or macOS: install and start the app. First tell the user in one line: "Installing drawover, a small (2-6 MB) app from github.com/mesomya/drawover-skill that shows the drawings on your screen." Then run the script for their system. It installs only if the app is missing, downloads one pinned release, installs it only if its SHA-256 checksum matches, starts the app outside your shell (so it keeps running after the command ends), and prints the status reply once the app is up. Run it as written; do not add delete commands.
- If your tool's safety check blocks the script, tell the user what it does (the line above, plus the checksum check) and ask them to approve it once.

Windows, in PowerShell (from bash, save it as a .ps1 file in the temp folder, not the project, and run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <file>`):

```powershell
$ProgressPreference = "SilentlyContinue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$exe = "$env:LOCALAPPDATA\drawover\drawover-light.exe"
if (-not (Test-Path $exe)) {
  $setup = Join-Path $env:TEMP "drawover-setup-0.3.0.exe"
  Invoke-WebRequest -UseBasicParsing "https://github.com/mesomya/drawover-skill/releases/download/v0.3.0/drawover-setup-x64.exe" -OutFile $setup
  if ((Get-FileHash $setup -Algorithm SHA256).Hash -eq "dc3bea021b48ad6b5bd3b7faf7d04578f5c39970eaca7f502aa6e06ffef3d26f") {
    Start-Process $setup -ArgumentList "/S" -Wait
  } else { "drawover: checksum mismatch, not installed" }
}
explorer.exe $exe
for ($i = 0; $i -lt 20; $i++) { try { Invoke-RestMethod http://127.0.0.1:47823/status; break } catch { Start-Sleep 1 } }
```

macOS, in bash or zsh:

```bash
app="$HOME/Applications/drawover.app"
if [ ! -d "$app" ]; then
  zip="${TMPDIR:-/tmp}/drawover-macos-0.3.0.zip"
  curl -fsSL -o "$zip" https://github.com/mesomya/drawover-skill/releases/download/v0.3.0/drawover-macos.zip
  if [ "$(shasum -a 256 "$zip" | cut -d' ' -f1)" = "4786f9d738c5c24310a79d2af31cae98dffa4fc0d15b2476db74c0543cafe1b7" ]; then
    mkdir -p "$HOME/Applications" && ditto -x -k "$zip" "$HOME/Applications"
  else
    echo "drawover: download failed or checksum mismatch, not installed"
  fi
fi
open "$app" && for i in $(seq 20); do curl -s http://127.0.0.1:47823/status && break; sleep 1; done
```

No status reply after 20 seconds: tell the user drawover did not start, and stop. On macOS, if the system says the app cannot be opened, tell the user to allow it once in System Settings > Privacy & Security > Open Anyway, then run `open "$HOME/Applications/drawover.app"` again.
## 2. Learn the drawing language (once per chat)

Read [reference.md](reference.md) before your first drawing. It lists every line you can send and how to make drawings look good.

## 3. Think once, then draw in one go

The user should see one continuous drawing, not stop-and-start pieces. So:
- **Plan everything first**, before sending anything: every part with its size, position and colour, every label, motion, note and `say` line. Decide it all now; do not re-plan later.
- **Then send it in small pieces, back to back**, each one shell command. Between pieces do not think, check, re-read or explain; just write the next one. The app keeps drawing while you write, so small pieces keep the pen moving.
  1. Tiny, so the first stroke appears within seconds: `{"op":"clear"}` (only for a new topic), the `scene` line, one `say` line and the 2-3 biggest parts or boxes. At most 6 lines.
  2. Then pieces of about 10 lines each, in build order (body, mechanism, details, then labels, motion, notes), with `say` lines spread through them.
  3. In the last piece, the final `say`, then `POST /done` in the same command.
- Each reply is `{"ok":true,"ops":n}`. If it has `badLines` (line numbers in that batch), those lines were broken JSON: fix and resend only them at the end.
Every POST needs the header `X-Drawover: 1`. Use only plain ASCII characters inside the lines (write "x" not a times sign, "-" not a long dash, "deg" not a degree sign).

Windows PowerShell:

```powershell
$lines = @'
{"op":"scene","title":"how a ceiling fan works","kind":"3d"}
{"op":"say","text":"Let's start with the motor housing."}
'@
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:47823/draw -Headers @{"X-Drawover"="1"} -ContentType "text/plain; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($lines))
```

bash or zsh:

```bash
curl -s http://127.0.0.1:47823/draw -H 'X-Drawover: 1' --data-binary @- <<'EOF'
{"op":"scene","title":"how a ceiling fan works","kind":"3d"}
EOF
```

`POST /done` and `POST /clear` take the same header and an empty body.

## 4. After drawing

Reply in chat with 1-3 short sentences on the key idea, then offer 2-3 follow-up questions as plain text (do not send `suggest` lines; the buttons cannot reach you). Keep the chat short; the drawing is the answer.

For a follow-up about the same drawing, keep the existing ids and add to it (more parts, labels, motion, `highlight`, `view`) without `clear`. For a new topic, start with `{"op":"clear"}` and a new `scene`.
