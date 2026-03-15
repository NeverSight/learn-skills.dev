---
name: rabbit-r1-livekit
description: Build a complete real-time voice AI agent that runs on the Rabbit R1 device, powered by LiveKit. Use when the user wants to create a voice agent for the R1, build a Rabbit R1 creation with LiveKit, or set up an R1 voice AI app.
user_invocable: true
---

# Rabbit R1 LiveKit Voice Agent

Build a complete real-time voice AI agent that runs on the Rabbit R1 device. This skill scaffolds the agent using the official LiveKit CLI, then adds the R1-specific frontend (creation) and web/token server.

## Step 1: Install the LiveKit CLI and Authenticate

### 1a. Install `lk` if needed

Check if `lk` is already installed by running `which lk`. If not found, install it based on platform:

- **macOS**: `brew install livekit-cli`
- **Linux**: `curl -sSL https://get.livekit.io/cli | bash`
- **Windows**: `winget install LiveKit.LiveKitCLI`

Verify with `lk --version`.

### 1b. Check cloud auth status

After the CLI is installed, check if the user is already authenticated by running:

```bash
lk project list
```

If this command succeeds and lists projects, auth is already done — skip to Step 2.

If it returns a message saying you need to auth or pick a project, you **MUST stop all work** and ask the user to authenticate. Use the AskUserQuestion tool with a message like:

> LiveKit Cloud auth is required before I can continue. Please run this in another terminal:
>
> ```
> lk cloud auth
> ```
>
> This will open a browser to sign in (or create an account). Once you're authenticated, come back here and let me know so I can continue.

**CRITICAL**: Do NOT proceed to Step 2 until the user confirms auth is complete. Do NOT attempt to run `lk cloud auth` yourself — it opens a browser and requires interactive login. Do NOT run `lk app create` without auth — it will hang waiting for credentials.

After the user confirms, re-verify with `lk project list` before continuing.

## Step 2: Scaffold the Agent with `lk app create`

Run the following command to scaffold the agent into a directory called `agent/`. The template name is **exactly** `agent-starter-python` — do NOT guess other names:

```bash
lk app create --template agent-starter-python agent
```

**IMPORTANT**: Run this command FIRST, before creating any other project directories (like `creation/`). Do NOT run it in parallel with other setup commands — if it fails, you need to handle the error before proceeding.

If the template name doesn't work (templates change over time), run `lk app create` interactively and select the Python voice agent starter.

This creates a fully configured agent project with:
- `src/agent.py` - the agent entry point
- `pyproject.toml` - dependencies managed by `uv`
- `Dockerfile` - production deployment
- `tests/` - eval framework
- `CLAUDE.md` / `AGENTS.md` - guides for future AI-assisted development

The scaffolded project stays up-to-date with the latest LiveKit Agents SDK and includes its own CLAUDE.md, which is invaluable for building out more advanced features later (handoffs, tasks, tools, etc.).

After scaffolding, customize `src/agent.py`:
- Set a unique `agent_name` in `@server.rtc_session(agent_name="your-r1-agent")`
- Update the `instructions` to mention the R1 context (tiny speaker, voice-only, concise responses, no markdown/emojis)
- Configure STT/LLM/TTS models as needed

## Step 3: Set Up LiveKit Credentials

Write the cloud credentials to the agent directory:

```bash
lk app env -w -d .env.local
```

(Auth was already completed in Step 1b, so this should work immediately.)

## Step 4: Add the R1 Frontend and Web Server

The scaffolded agent project only contains the backend. You need to add two things at the project root level (alongside the agent directory):

### Project Structure

```
project-root/
  web-server.py              # Combined static file server + token API
  creation/                  # The R1 "creation" (the app installed on device)
    index.html               # Main voice agent UI (240x282px)
    install.html             # QR code generator for R1 installation
  agent/                     # <-- The scaffolded LiveKit agent (from lk app create)
    src/agent.py
    pyproject.toml
    ...
```

### web-server.py

Combined static file + token server. Serves the creation files and provides a `/getToken` endpoint that generates LiveKit access tokens with `RoomConfiguration` for agent dispatch.

```python
"""Combined HTTP static file + token server for R1 creations."""
import json
import os
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from livekit import api
from livekit.protocol.room import RoomConfiguration

os.environ.setdefault("LIVEKIT_URL", "wss://YOUR_LIVEKIT_URL")
os.environ.setdefault("LIVEKIT_API_KEY", "YOUR_API_KEY")
os.environ.setdefault("LIVEKIT_API_SECRET", "YOUR_API_SECRET")

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/getToken":
            self._handle_token()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def _handle_token(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        room_name = body.get("room_name") or f"r1-room-{int(time.time())}"
        identity = body.get("participant_identity") or f"r1-user-{int(time.time())}"

        token = (
            api.AccessToken(os.environ["LIVEKIT_API_KEY"], os.environ["LIVEKIT_API_SECRET"])
            .with_identity(identity)
            .with_name(body.get("participant_name") or "R1 User")
            .with_grants(api.VideoGrants(room_join=True, room=room_name, can_publish=True, can_subscribe=True))
        )

        if body.get("room_config"):
            rc_data = body["room_config"]
            room_config = RoomConfiguration()
            for a in rc_data.get("agents", []):
                dispatch = room_config.agents.add()
                dispatch.agent_name = a.get("agent_name", "")
            token = token.with_room_config(room_config)

        resp = json.dumps({
            "server_url": os.environ["LIVEKIT_URL"],
            "participant_token": token.to_jwt(),
        }).encode()

        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(resp)

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, fmt, *args):
        print(f"[server] {args[0]}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8081), Handler)
    print("Server running on http://0.0.0.0:8081 (static files + token endpoint)")
    server.serve_forever()
```

**Important**: web-server.py needs `livekit-api`: `pip install livekit-api`

Fill in the LiveKit credentials at the top, or set them as environment variables.

### creation/index.html

The main R1 frontend. This is a single-file HTML app optimized for the R1's constraints.

**CRITICAL livekit-client UMD API notes** (these are the #1 source of bugs):

- The UMD global is **`LivekitClient`**, NOT `lk`. Use: `var Room = LivekitClient.Room;`
- Use **`TokenSource.endpoint(url)`** to create a token source, then **`tokenSource.fetch({ roomName, agentName })`**
- The fetch result uses **camelCase**: `tokenResult.serverUrl` and `tokenResult.participantToken`
- Get mic manually via **`navigator.mediaDevices.getUserMedia()`**, then publish with `room.localParticipant.publishTrack(audioTrack, { source: Track.Source.Microphone })`
- Do NOT use `room.localParticipant.setMicrophoneEnabled()` — it may not work reliably in the R1 WebView
- For transcription text streams, use **`reader.readAll()`** (not async iteration)
- For audio visualization, use **`setupAnalyser(track.mediaStreamTrack)`** — pass the raw MediaStreamTrack, create a MediaStream from it, then use `createMediaStreamSource`
- Canvas 2D only — **never use WebGL** (R1 doesn't support it)

The `agentName` in the token fetch MUST match the `agent_name` in the Python agent.

Use the complete working reference below as the basis for index.html. Adapt brand text, colors, and agent name to match the user's project.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=240,height=282,user-scalable=no">
<title>Voice Agent</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 240px; height: 282px; overflow: hidden;
  background: #0e0e10; color: #fff;
  font-family: -apple-system, sans-serif;
  display: flex; flex-direction: column; align-items: center;
  -webkit-user-select: none; user-select: none;
  position: relative;
}
#brand {
  margin-top: 10px; font-size: 10px; font-weight: 600;
  color: rgba(255,255,255,0.3); letter-spacing: 2px; text-transform: uppercase;
}
#status-pill {
  margin-top: 8px; padding: 3px 12px; border-radius: 10px;
  font-size: 10px; font-weight: 600; letter-spacing: 0.5px;
  background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.4);
  transition: all 0.3s;
}
#status-pill.live { background: rgba(254,80,0,0.15); color: #FE5000; }
#status-pill.speaking { background: rgba(254,80,0,0.25); color: #FF8C4C; }
#viz-container {
  flex: 1; display: flex; align-items: center; justify-content: center; width: 100%;
}
canvas { width: 200px; height: 200px; }
#label {
  font-size: 13px; color: rgba(255,255,255,0.7); margin-bottom: 4px; font-weight: 500;
}
#transcript-inline {
  font-size: 9px; color: rgba(255,255,255,0.3); text-align: center;
  padding: 0 12px; max-height: 28px; overflow: hidden; margin-bottom: 4px;
}
#vol-bar {
  width: 120px; height: 3px; background: rgba(255,255,255,0.08);
  border-radius: 2px; margin-bottom: 8px; overflow: hidden;
}
#vol-fill { height: 100%; background: #FE5000; border-radius: 2px; transition: width 0.15s; }
#transcript-panel {
  position: absolute; top: 0; right: -240px; bottom: 0; width: 240px;
  background: rgba(14,14,16,0.97); z-index: 20; transition: right 0.3s ease;
  display: flex; flex-direction: column;
}
#transcript-panel.open { right: 0; }
#transcript-header {
  padding: 10px 12px 6px; font-size: 10px; color: rgba(255,255,255,0.3);
  letter-spacing: 2px; text-transform: uppercase; text-align: center;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
#transcript-body { flex: 1; overflow: hidden; padding: 8px 12px; }
#transcript-content { font-size: 11px; line-height: 1.5; color: rgba(255,255,255,0.7); }
#transcript-content .msg {
  margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.04);
}
#transcript-content .msg .role {
  font-size: 9px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px;
}
#transcript-content .msg .role.agent { color: #FE5000; }
#transcript-content .msg .role.user { color: rgba(255,255,255,0.4); }
#transcript-content .msg .text { font-size: 11px; color: rgba(255,255,255,0.65); }
#tap-overlay {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(14,14,16,0.95); display: flex; flex-direction: column;
  align-items: center; justify-content: center; z-index: 30;
}
#tap-overlay.hidden { display: none; }
#tap-circle {
  width: 80px; height: 80px; border-radius: 50%; background: #FE5000;
  display: flex; align-items: center; justify-content: center;
  animation: breathe 2s ease-in-out infinite;
}
#tap-circle svg { width: 32px; height: 32px; fill: white; }
@keyframes breathe {
  0%,100% { transform: scale(1); opacity: 0.9; }
  50% { transform: scale(1.08); opacity: 1; }
}
#tap-text { margin-top: 12px; font-size: 12px; color: rgba(255,255,255,0.5); }
#log {
  position: fixed; bottom: 0; left: 0; right: 0;
  font-size: 7px; color: #ff0; background: rgba(0,0,0,0.9);
  padding: 2px; max-height: 24px; overflow: hidden; z-index: 99;
  display: none;
}
</style>
</head>
<body>
<div id="brand">AGENT NAME</div>
<div id="status-pill">READY</div>
<div id="viz-container"><canvas id="visualizer" width="200" height="200"></canvas></div>
<div id="label"></div>
<div id="transcript-inline"></div>
<div id="vol-bar"><div id="vol-fill" style="width:50%"></div></div>

<div id="transcript-panel">
  <div id="transcript-header">Transcript</div>
  <div id="transcript-body"><div id="transcript-content"></div></div>
</div>

<div id="tap-overlay">
  <div id="tap-circle">
    <svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
  </div>
  <div id="tap-text">Tap to connect</div>
</div>

<div id="log"></div>

<script src="https://unpkg.com/livekit-client/dist/livekit-client.umd.js"></script>
<script>
    var logEl = document.getElementById('log');
    var statusPill = document.getElementById('status-pill');
    var labelEl = document.getElementById('label');
    var transcriptInline = document.getElementById('transcript-inline');
    var tapOverlay = document.getElementById('tap-overlay');
    var tapText = document.getElementById('tap-text');
    var volFill = document.getElementById('vol-fill');
    var canvas = document.getElementById('visualizer');
    var ctx2d = canvas.getContext('2d');
    var transcriptPanel = document.getElementById('transcript-panel');
    var transcriptContent = document.getElementById('transcript-content');
    var transcriptBody = document.getElementById('transcript-body');

    var TOKEN_URL = window.location.origin + '/getToken';
    var Room = LivekitClient.Room;
    var RoomEvent = LivekitClient.RoomEvent;
    var Track = LivekitClient.Track;
    var TokenSource = LivekitClient.TokenSource;

    var room = null;
    var audioStream = null;
    var started = false;
    var appState = 'idle';
    var volume = 0.5;
    var audioElements = [];
    var analyser = null;
    var dataArray = null;
    var currentIntensity = 0.0;
    var startTime = Date.now();
    var scrollMode = 'volume';
    var transcriptOpen = false;
    var messages = [];

    function log(msg) { logEl.textContent = msg; console.log(msg); }

    function setState(s, text) {
        appState = s;
        statusPill.textContent = s === 'live' ? 'LISTENING' : s === 'speaking' ? 'SPEAKING' : s.toUpperCase();
        statusPill.className = s;
        if (text) labelEl.textContent = text;
    }

    function setVolume(v) {
        volume = v;
        audioElements.forEach(function(el) { el.volume = v; });
        volFill.style.width = Math.round(v * 100) + '%';
        labelEl.textContent = 'Vol: ' + Math.round(v * 100) + '%';
        clearTimeout(window._volTimeout);
        window._volTimeout = setTimeout(function() { labelEl.textContent = ''; }, 1500);
    }

    function escapeHtml(str) {
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function addMessage(role, text) {
        messages.push({ role: role, text: text });
        renderTranscript();
        transcriptInline.textContent = text;
    }

    function renderTranscript() {
        var html = '';
        for (var i = 0; i < messages.length; i++) {
            var m = messages[i];
            html += '<div class="msg"><div class="role ' + m.role + '">' + m.role + '</div>';
            html += '<div class="text">' + escapeHtml(m.text) + '</div></div>';
        }
        transcriptContent.innerHTML = html;
        transcriptBody.scrollTop = transcriptBody.scrollHeight;
    }

    // Side button toggles transcript
    window.addEventListener('sideClick', function() {
        if (!started) return;
        transcriptOpen = !transcriptOpen;
        if (transcriptOpen) {
            scrollMode = 'transcript';
            transcriptPanel.classList.add('open');
        } else {
            scrollMode = 'volume';
            transcriptPanel.classList.remove('open');
        }
    });

    // Keyboard fallback for testing (Escape = side button)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') window.dispatchEvent(new Event('sideClick'));
    });

    window.addEventListener('scrollUp', function() {
        if (scrollMode === 'volume') setVolume(Math.min(1.0, volume + 0.1));
        else transcriptBody.scrollTop -= 30;
    });
    window.addEventListener('scrollDown', function() {
        if (scrollMode === 'volume') setVolume(Math.max(0.0, volume - 0.1));
        else transcriptBody.scrollTop += 30;
    });

    // 2D Canvas visualizer (R1 has no WebGL)
    function drawViz() {
        requestAnimationFrame(drawViz);
        var energy = 0;
        if (analyser && dataArray) {
            analyser.getByteFrequencyData(dataArray);
            var total = 0, count = Math.min(dataArray.length, 40);
            for (var i = 0; i < count; i++) total += dataArray[i];
            energy = (total / count) / 255;
        } else {
            energy = appState === 'idle' ? 0.0 : appState === 'connecting' ? 0.15 : appState === 'live' ? 0.1 : 0.0;
        }
        currentIntensity += (energy - currentIntensity) * 0.15;

        var w = 200, h = 200;
        ctx2d.clearRect(0, 0, w, h);
        var cx = w / 2, cy = h / 2;
        var t = (Date.now() - startTime) / 1000;
        var intensity = currentIntensity;

        for (var i = 3; i >= 0; i--) {
            var speed = 1.0 + i * 0.3;
            var wave = Math.sin(t * speed + i * 1.57) * 0.5 + 0.5;
            var radius = 20 + intensity * 30 + i * 12 + wave * 8 * intensity;
            var alpha = (0.15 + 0.25 * intensity) * (1.0 - i * 0.2);
            ctx2d.beginPath();
            ctx2d.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx2d.strokeStyle = 'rgba(254, 80, 0, ' + alpha + ')';
            ctx2d.lineWidth = 2 + intensity * 3;
            ctx2d.stroke();
        }

        if (appState === 'speaking') {
            for (var i = 0; i < 12; i++) {
                var angle = (i / 12) * Math.PI * 2 + t * (0.3 + (i % 3) * 0.15);
                var r = 35 + intensity * 25 + Math.sin(t * 2 + i) * 5;
                var px = cx + Math.cos(angle) * r;
                var py = cy + Math.sin(angle) * r;
                ctx2d.beginPath();
                ctx2d.arc(px, py, 2 + intensity * 1.5, 0, Math.PI * 2);
                ctx2d.fillStyle = 'rgba(254, 80, 0, ' + (0.3 + 0.7 * intensity) + ')';
                ctx2d.fill();
            }
        }

        var innerRadius = 15 + intensity * 20;
        var grad = ctx2d.createRadialGradient(cx, cy, 0, cx, cy, innerRadius);
        grad.addColorStop(0, 'rgba(254, 80, 0, ' + (0.5 + intensity * 0.5) + ')');
        grad.addColorStop(0.6, 'rgba(254, 80, 0, ' + (0.15 + intensity * 0.2) + ')');
        grad.addColorStop(1, 'rgba(254, 80, 0, 0)');
        ctx2d.beginPath();
        ctx2d.arc(cx, cy, innerRadius, 0, Math.PI * 2);
        ctx2d.fillStyle = grad;
        ctx2d.fill();

        if (appState !== 'speaking' && appState !== 'live') {
            var pulse = Math.sin(t * 1.5) * 0.5 + 0.5;
            var breathRadius = 25 + pulse * 10;
            var breathGrad = ctx2d.createRadialGradient(cx, cy, 0, cx, cy, breathRadius);
            breathGrad.addColorStop(0, 'rgba(254, 80, 0, ' + (pulse * 0.2) + ')');
            breathGrad.addColorStop(1, 'rgba(254, 80, 0, 0)');
            ctx2d.beginPath();
            ctx2d.arc(cx, cy, breathRadius, 0, Math.PI * 2);
            ctx2d.fillStyle = breathGrad;
            ctx2d.fill();
        }
    }
    drawViz();

    function setupAnalyser(mediaStreamTrack) {
        try {
            var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            var stream = new MediaStream([mediaStreamTrack]);
            var source = audioCtx.createMediaStreamSource(stream);
            analyser = audioCtx.createAnalyser();
            analyser.fftSize = 256;
            analyser.smoothingTimeConstant = 0.7;
            dataArray = new Uint8Array(analyser.frequencyBinCount);
            source.connect(analyser);
            log('analyser connected');
        } catch (e) {
            log('analyser err: ' + e.message);
        }
    }

    // Tap to start — use document.body for reliable touch handling on R1
    document.body.addEventListener('touchstart', function(e) {
        e.preventDefault();
        if (!started) { started = true; startAll(); }
    });
    document.body.addEventListener('click', function() {
        if (!started) { started = true; startAll(); }
    });

    async function startAll() {
        try {
            tapText.textContent = 'Connecting...';
            setState('connecting', '');

            // Get mic FIRST (requires user gesture in R1 WebView)
            log('getting mic');
            audioStream = await navigator.mediaDevices.getUserMedia({
                audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true, sampleRate: 44100, channelCount: 1 }
            });

            // Warm up AudioContext (some WebViews need this)
            var micCtx = new (window.AudioContext || window.webkitAudioContext)({ latencyHint: 'interactive', sampleRate: 44100 });
            if (micCtx.state === 'suspended') await micCtx.resume();
            micCtx.createMediaStreamSource(audioStream);
            log('mic ok');

            // Get token via TokenSource.endpoint (handles room_config/agent dispatch automatically)
            tapText.textContent = 'Getting token...';
            var tokenSource = TokenSource.endpoint(TOKEN_URL);
            var tokenResult = await tokenSource.fetch({ roomName: 'r1-room-' + Date.now(), agentName: 'your-r1-agent' });
            log('token ok');

            tapText.textContent = 'Joining...';
            room = new Room({ adaptiveStream: true, dynacast: true });

            room.on(RoomEvent.TrackSubscribed, function(track, pub, participant) {
                if (track.kind === Track.Kind.Audio) {
                    var el = track.attach();
                    el.volume = volume;
                    audioElements.push(el);
                    document.body.appendChild(el);
                    setupAnalyser(track.mediaStreamTrack);
                    log('agent audio attached');
                }
            });

            room.on(RoomEvent.TrackUnsubscribed, function(track) {
                track.detach().forEach(function(el) { el.remove(); });
            });

            room.on(RoomEvent.ActiveSpeakersChanged, function(speakers) {
                var agentSpeaking = speakers.some(function(s) { return s !== room.localParticipant; });
                if (agentSpeaking && appState !== 'connecting') {
                    setState('speaking', '');
                } else if (!agentSpeaking && appState === 'speaking') {
                    setState('live', '');
                }
            });

            // Transcription via text streams — use reader.readAll(), NOT async iteration
            room.registerTextStreamHandler('lk.transcription', async function(reader, info) {
                var message = await reader.readAll();
                var role = info.identity !== room.localParticipant.identity ? 'agent' : 'user';
                if (messages.length > 0 && messages[messages.length - 1].role === role) {
                    messages[messages.length - 1].text = message;
                    renderTranscript();
                    transcriptInline.textContent = message;
                } else {
                    addMessage(role, message);
                }
            });

            room.on(RoomEvent.ParticipantConnected, function(p) {
                log('joined: ' + p.identity);
                labelEl.textContent = '';
            });
            room.on(RoomEvent.Disconnected, function() {
                setState('idle', 'Disconnected');
                started = false;
                tapOverlay.className = '';
                tapText.textContent = 'Tap to reconnect';
            });

            // Connect using camelCase response fields
            await room.connect(tokenResult.serverUrl, tokenResult.participantToken);
            log('room: ' + room.name);

            // Publish mic manually (more reliable than setMicrophoneEnabled on R1)
            var audioTrack = audioStream.getAudioTracks()[0];
            await room.localParticipant.publishTrack(audioTrack, { source: Track.Source.Microphone });
            log('mic published');

            tapOverlay.className = 'hidden';
            setState('live', '');

            // Attach any already-present remote audio
            room.remoteParticipants.forEach(function(p) {
                p.audioTrackPublications.forEach(function(pub) {
                    if (pub.track) {
                        var el = pub.track.attach();
                        el.volume = volume;
                        audioElements.push(el);
                        document.body.appendChild(el);
                        setupAnalyser(pub.track.mediaStreamTrack);
                    }
                });
            });

            if (room.remoteParticipants.size === 0) {
                labelEl.textContent = 'Waiting for agent...';
            }

        } catch (error) {
            log('ERROR: ' + error.name + ': ' + error.message);
            tapText.textContent = 'Error: ' + error.message;
            started = false;
        }
    }
</script>
</body>
</html>
```

### creation/install.html

QR code page for installing the creation on the R1. Uses `qr-code-styling` from unpkg:

```javascript
const qrData = JSON.stringify({
    title: "Your Agent Name",
    url: creationUrl,  // https://xxxx-xx-xx.tunnelmole.net/creation/
    description: "Description of your agent",
    iconUrl: "",
    themeColor: "#FE5000"
});
```

## Architecture

```
R1 WebView --> web-server.py (port 8081, HTTPS via tunnelmole) --> LiveKit Cloud (WebRTC SFU + Agent Dispatch) --> LiveKit Agent (Python: STT -> LLM -> TTS)
```

### Flow
1. User taps R1 screen (user gesture required for mic access)
2. Frontend fetches LiveKit token from `/getToken` (same origin)
3. Token includes `RoomConfiguration` with agent dispatch (names which agent to use)
4. Frontend connects to LiveKit room via WebRTC, publishes mic audio
5. LiveKit Cloud dispatches the named agent to the room
6. Agent receives audio, runs STT -> LLM -> TTS pipeline
7. Agent publishes audio response back over WebRTC
8. R1 plays audio through speaker

## Critical R1 WebView Constraints

These are hard-won discoveries. Violating any of these will cause silent failures on the device.

### HTTPS is MANDATORY for mic access
The R1 WebView does NOT treat custom domains as secure contexts. `navigator.mediaDevices` is `undefined` over HTTP. You MUST use tunnelmole or similar HTTPS tunnel. The R1's own `*.rabbitos.app` domain is whitelisted regardless.

### No WebGL
The Flutter-based WebView does not support WebGL. Always use Canvas 2D for visualizations. Do NOT attempt WebGL — just use 2D from the start.

### Touch/Click Event Quirks
- `onclick` in dynamic `innerHTML` does NOT fire - use `addEventListener`
- `touchstart` on specific elements may not fire - use `document.body` touchstart with `e.target` checking
- Touch events need `e.preventDefault()` to avoid double-firing with click events

### Available APIs
- AudioContext, WebRTC (RTCPeerConnection), MediaRecorder, WebSocket, Canvas 2D, getUserMedia (HTTPS only)
- NOT available: WebGL, getUserMedia over HTTP

### Screen Size
- 240x282 pixels. Design all UI for this exact size.

### R1 Native Bridges (JavaScript globals in WebView)
- `PluginMessageHandler.postMessage()` - send messages to R1 system/LLM
- `FlutterButtonHandler.postMessage()` - button events
- `AccelerometerHandler.postMessage()` - accelerometer data
- `CreationStorageHandler.postMessage()` - persistent storage
- `TouchEventHandler.postMessage()` - touch events
- `closeWebView` - close the creation

### R1 Custom Events (dispatched on `window`)
- `sideClick` - side button press
- `longPressStart` / `longPressEnd` - long press on side button
- `scrollUp` / `scrollDown` - scroll wheel rotation

## Step 5: Auto-Start All Services and Show QR Code

After all files are created and dependencies installed, automatically start everything and display the install QR code in the terminal.

### 5a: Kill any existing process on port 8081

```bash
lsof -ti:8081 | xargs kill 2>/dev/null || true
```

### 5b: Start all three services in background

Start these in parallel using background bash tasks:

1. **Web server**: `cd PROJECT_ROOT && python web-server.py`
2. **HTTPS tunnel**: `tmole 8081` (install with `npm install -g tunnelmole` if not found)
3. **Agent**: `cd PROJECT_ROOT/agent && uv run python src/agent.py dev`

### 5c: Wait for tunnel URL and verify services

Read the tunnelmole background task output (non-blocking) until you see the HTTPS URL. Also verify the agent registered successfully by checking its output for "registered worker".

Extract the HTTPS URL from the tmole output (the `https://` line).

### 5d: Print the install link and run instructions

Once you have the tunnel URL, output a message to the user in this format (replace TUNNEL_URL and PROJECT_DIR with actual values). The install link MUST be the very first thing the user sees — put it above everything else:

```
Install on R1: TUNNEL_URL/creation/install.html

All 3 services are running. To run again next time, open 3 terminals in PROJECT_DIR:

  1. python web-server.py
  2. tmole 8081
  3. cd agent && uv run python src/agent.py dev

Voice agent UI (browser test): TUNNEL_URL/creation/
```

The install.html page already generates the QR code for the user to scan with their R1 — no need to generate one in the terminal.

## Running Manually (Without This Skill)

1. **Install web-server dependency**: `pip install livekit-api`
2. **Install agent dependencies**: `cd agent && uv sync`
3. **Download models**: `cd agent && uv run python src/agent.py download-files`
4. **Start the web server**: `python web-server.py` (from project root)
5. **Start tunnelmole**: `tmole 8081` (copy the HTTPS URL). Install with `npm install -g tunnelmole` if needed.
6. **Start the agent**: `cd agent && uv run python src/agent.py dev`
7. **Install on R1**: Open `https://YOUR_TMOLE_URL/creation/install.html` in a browser, scan QR with R1

## Customization Points

When the user describes what they want their agent to do, customize:

1. **Agent instructions** in `agent/src/agent.py` - the `instructions` parameter
2. **Agent name** - must match in both `agent.py` (`agent_name=`) and `index.html` (`agentName:`)
3. **LLM model** - change `inference.LLM(model=...)` (e.g., `openai/gpt-4o`, `anthropic/claude-sonnet-4-20250514`)
4. **TTS voice** - change the voice ID in `inference.TTS(voice=...)`
5. **Brand text and colors** in `index.html` - the `#brand` div and `#FE5000` color
6. **Tools** - add tools to the Agent class for function calling
7. **Handoffs/Tasks** - for complex multi-step workflows, use LiveKit's handoff and task system

For advanced agent features (tools, handoffs, tasks, workflows), refer to the CLAUDE.md/AGENTS.md that ships with the scaffolded agent project - it has detailed guidance and links to LiveKit docs.

## Important Notes

- The `uv.lock` file should be committed for reproducible builds
- Always use `uv` (not pip) for the agent directory
- The web-server.py uses `livekit-api` (installed via pip, separate from the agent's venv)
- ALWAYS verify that `agent_name` matches between frontend and backend - this is the #1 cause of "agent never joins"
- The R1 WebView is Chrome-based but runs in Flutter, so test carefully
- For complex agents, use LiveKit's handoff/task workflow system instead of one long instruction prompt
