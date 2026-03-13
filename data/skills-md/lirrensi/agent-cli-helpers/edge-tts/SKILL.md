---
name: edge-tts
description: >
  Generate complete, production-ready TTS (Text-to-Speech) scripts and CLI tools using
  edge-tts — Microsoft's neural voice engine with 400+ natural-sounding voices.
  Use this skill whenever the user wants to speak text aloud from the terminal/PowerShell,
  list or search voices, select voices by name/language/gender, control rate/volume/pitch,
  save speech to MP3/audio files, or pipe text into a speak command.
  Trigger for ANY request involving TTS, speech synthesis, say command, speak function,
  voice output, edge-tts, or audio from scripts — even small snippets. Always check
  installation first and prefer uv tool install for setup.
---

# PowerShell / Terminal TTS Skill (edge-tts)

Use **edge-tts** — free, neural-quality voices (400+), works from any terminal.
No Windows API nonsense. Sounds like a real human. 🎉

---

## Step 1 — Check & Install

**Always check if installed first:**
```powershell
Get-Command edge-tts -ErrorAction SilentlyContinue
```

**Install with uv (preferred):**
```powershell
uv tool install edge-tts
```

**Fallback with pip:**
```powershell
pip install edge-tts
```

This installs two executables: `edge-tts` (generate audio) and `edge-playback` (speak aloud).

---

## Step 2 — Basic Usage

**Speak aloud (use `edge-playback`, NOT `edge-tts --play`):**
```powershell
edge-playback --text "Hello world"
```

**Save to MP3:**
```powershell
edge-tts --text "Hello world" --write-media output.mp3
```

> ⚠️ `--play` flag does NOT exist on Windows. Always use `edge-playback` to speak aloud.

---

## Step 3 — Voices

**List ALL voices (400+):**
```powershell
edge-tts --list-voices
```

**Filter voices by language in PowerShell:**
```powershell
edge-tts --list-voices | Select-String "en-US"
edge-tts --list-voices | Select-String "Female"
```

**Recommended English neural voices:**
| Voice | Gender | Style |
|---|---|---|
| `en-US-AriaNeural` | Female | Natural, warm |
| `en-US-JennyNeural` | Female | Friendly |
| `en-US-GuyNeural` | Male | Natural |
| `en-US-EricNeural` | Male | Calm |
| `en-GB-SoniaNeural` | Female | British |
| `en-GB-RyanNeural` | Male | British |
| `en-AU-NatashaNeural` | Female | Australian |

**Use a specific voice:**
```powershell
edge-playback --voice "en-US-AriaNeural" --text "Hi, I'm Aria!"
edge-tts --voice "en-US-AriaNeural" --text "Hi" --write-media aria.mp3
```

---

## Step 4 — Rate, Volume, Pitch

All adjustments use `+X%` or `-X%` string format:

```powershell
# Rate: default is +0%, range roughly -50% to +100%
edge-playback --voice "en-US-AriaNeural" --rate "+20%" --text "Faster speech"
edge-playback --voice "en-US-AriaNeural" --rate "-30%" --text "Slower speech"

# Volume: default +0%
edge-playback --voice "en-US-AriaNeural" --volume "+50%" --text "Louder"

# Pitch: default +0Hz
edge-playback --voice "en-US-AriaNeural" --pitch "+10Hz" --text "Higher pitch"
```

---

## The Complete Say.ps1 Script

When the user wants a full CLI wrapper script, generate this:

```powershell
<#
.SYNOPSIS
    TTS CLI wrapper around edge-tts / edge-playback.

.DESCRIPTION
    Speaks text aloud or saves to MP3. Supports pipeline input,
    voice selection, rate/volume/pitch control, and voice listing/search.

.EXAMPLE
    .\Say.ps1 "Hello world"
    .\Say.ps1 -Text "Hello" -Voice "en-US-AriaNeural" -Rate "+20%"
    .\Say.ps1 -Text "Hello" -OutFile speech.mp3
    .\Say.ps1 -List
    .\Say.ps1 -Search "en-GB"
    "Hello from pipeline" | .\Say.ps1
#>

[CmdletBinding(DefaultParameterSetName = 'Speak')]
param(
    [Parameter(ParameterSetName='Speak', Position=0, ValueFromPipeline=$true)]
    [string]$Text,

    [Parameter(ParameterSetName='Speak')]
    [string]$Voice = 'en-US-AriaNeural',

    # Rate adjustment e.g. "+20%", "-10%"
    [Parameter(ParameterSetName='Speak')]
    [string]$Rate = '+0%',

    # Volume adjustment e.g. "+50%", "-20%"
    [Parameter(ParameterSetName='Speak')]
    [string]$Volume = '+0%',

    # Pitch adjustment e.g. "+5Hz", "-10Hz"
    [Parameter(ParameterSetName='Speak')]
    [string]$Pitch = '+0Hz',

    # Save to MP3 file (speaks aloud if omitted)
    [Parameter(ParameterSetName='Speak')]
    [string]$OutFile,

    # Also speak aloud when saving to file
    [Parameter(ParameterSetName='Speak')]
    [switch]$Also,

    [Parameter(ParameterSetName='List', Mandatory)]
    [switch]$List,

    [Parameter(ParameterSetName='Search', Mandatory)]
    [string]$Search
)

begin {
    # Check edge-tts is installed
    if (-not (Get-Command edge-tts -ErrorAction SilentlyContinue)) {
        Write-Error "edge-tts not found. Install with: uv tool install edge-tts"
        exit 1
    }

    # LIST mode
    if ($PSCmdlet.ParameterSetName -eq 'List') {
        edge-tts --list-voices
        return
    }

    # SEARCH mode
    if ($PSCmdlet.ParameterSetName -eq 'Search') {
        Write-Host "Voices matching '$Search':" -ForegroundColor Cyan
        edge-tts --list-voices | Select-String $Search
        return
    }
}

process {
    if ($PSCmdlet.ParameterSetName -ne 'Speak') { return }
    if (-not $Text) { return }

    $baseArgs = @(
        '--voice',  $Voice,
        '--rate',   $Rate,
        '--volume', $Volume,
        '--pitch',  $Pitch,
        '--text',   $Text
    )

    if ($OutFile) {
        & edge-tts @baseArgs --write-media $OutFile
        Write-Host "Saved to: $OutFile" -ForegroundColor Green
        if ($Also) {
            & edge-playback @baseArgs
        }
    } else {
        & edge-playback @baseArgs
    }
}
```

---

## Pipeline Examples

```powershell
# Simple string
"Good morning!" | .\Say.ps1

# From file
Get-Content notes.txt | .\Say.ps1 -Voice "en-GB-SoniaNeural"

# Command output
(Get-Date -Format "dddd, MMMM d") | .\Say.ps1

# Save to file
"Hello" | .\Say.ps1 -OutFile hello.mp3

# Speak AND save
.\Say.ps1 -Text "Hello" -OutFile hello.mp3 -Also
```

---

## Common Gotchas

- **`--play` doesn't exist on Windows** — always use `edge-playback` executable instead
- **Rate/Volume/Pitch need `+X%` / `+XHz` format** — not plain numbers
- **Requires internet** — edge-tts calls Microsoft's servers for synthesis
- **Output is MP3** not WAV — use ffmpeg if WAV needed: `ffmpeg -i out.mp3 out.wav`
- **Voice names are case-sensitive** — `en-US-AriaNeural` not `en-us-arianeural`
- **`uv tool install`** puts executables in uv's tool bin — make sure it's on PATH
