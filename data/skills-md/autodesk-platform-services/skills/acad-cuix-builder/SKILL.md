---
name: acad-cuix-builder
description: "Generate a complete AutoCAD .bundle (CUIX ribbon + extended tooltip GIFs + LISP + PackageContents) from a plain-English prompt. No XML editing required."
argument-hint: "Describe the plugin: panels, buttons, commands, tooltip GIFs, and optional LISP file (e.g. 'drafting tools with zoom selection and layer isolate commands, GIF tooltips, lispPath at D:/demo/DraftingTools.lsp')"
compatibility: "Windows only. Requires CuixBuilder.exe (install via install.ps1) OR .NET SDK 10.0."
---

# AutoCAD CUIX Builder

Conversational skill that generates a complete AutoCAD `.bundle` folder:
- Ribbon tab + panels + buttons (CUIX)
- Extended tooltips with GIF animations (XAML)
- LISP command file (copied from `lispPath`)
- `PackageContents.xml` — AutoCAD plugin manifest

Drop the bundle in `%APPDATA%\Autodesk\ApplicationPlugins\` and AutoCAD auto-loads on next startup.

Architecture reference: see `references/cuix-architecture.md`.

---

## Step 0 — Verify generator is available

```powershell
$exe = "$env:USERPROFILE\.cuixbuilder\CuixBuilder.exe"
if (Test-Path $exe) {
    & $exe --help          # shows all config fields
} elseif (Get-Command dotnet -ErrorAction SilentlyContinue) {
    dotnet --version
} else {
    Write-Host "Neither found — run install.ps1 first"
}
```

- **exe found** → use `& $exe <config.json>` in Step 5
- **dotnet SDK** → use `dotnet run --project <src-path> -c Release -- <config.json>` in Step 5
- **neither** → tell user to run `install.ps1` first (downloads exe, no SDK needed)

---

## Step 1 — Collect plugin identity

Ask:
- **Plugin display name** — shown as ribbon tab and group label (e.g. `Drafting Tools`)
- **Internal name** — derive from display name, no spaces (e.g. `DraftingTools`)

---

## Step 2 — Collect panels

Ask:
- How many ribbon panels?
- Name of each panel (e.g. `Annotation`, `View`)

---

## Step 3 — Collect buttons (per panel)

### Auto-scan icons folder (when user provides a folder path)

If the user says "use icons from `<folder>`", list that folder and auto-match files by button name:

```powershell
Get-ChildItem "D:\SkillDemo\demo\icons\" | Select-Object Name
```

Matching convention (case-insensitive, spaces→empty):
- `{buttonname}.bmp` → `imagePath`  (16×16 ribbon icon)
- `{buttonname}.gif` → `tooltipImage` (expanded tooltip animation)
- `{buttonname}.png` → `tooltipImage` (fallback if no GIF)

Example: button label `Zoom Selection`, internal name `zoomsel`:
- `zoomsel.bmp` → imagePath
- `zoomsel.gif` → tooltipImage

Derive internal name from label: lowercase, strip spaces/special chars (e.g. `Zoom Selection` → `zoomsel`, `Isolate Layer` → `layiso`). If no match found, use colored placeholder.

### Per-button fields

For each panel, for each button ask:
- **Label** — text on the button (e.g. `Quick Leader`)
- **Command** — one of:
  - Bare AutoCAD command: `QLEADER` → generator adds `^C^C` automatically
  - LISP expression: `(c:ZOOMSEL)` → generator adds `^C^C` automatically
  - Pre-formatted: `^C^CMYCOMMAND` → used as-is
- **Image** — auto-matched from icons folder, or path to `.bmp` file, or skip → colored placeholder
- **Tooltip** — short hover text (defaults to label)
- **Tooltip description** — optional extended body text shown in expanded tooltip
- **Tooltip GIF** — auto-matched from icons folder, or path to `.gif`/`.png` (recommended: 300×187px, <30KB)
- **Help topic** — anchor name for F1 help (e.g. `zoomsel`); derive from internal name if not given

### CHM / F1 help

If user does not mention a CHM file, **always ask**:
> "Do you have a CHM help file for F1 support? If yes, provide the path."

If provided, set `chmPath` in config. If skipped, omit `chmPath` (F1 will open AutoCAD's own help).  
Help topic per button = anchor name derived from button internal name (e.g. `zoomsel`).

---

## Step 4 — Output path

Ask where to save the `.cuix` file.  
Default: current directory + `<PluginName>.cuix`

---

## Step 5 — Confirm, build JSON, generate

Show a summary table:
```
Plugin : <DisplayName>   Tab : <Tab>   Output : <path>

Panel: <name>
  [1] <label>  →  <command>   image: <file or "placeholder blue">
  [2] ...
```

Confirm with user, then build the JSON config:

```json
{
  "pluginName": "DraftingTools",
  "displayName": "Drafting Tools",
  "tab": "Drafting Tools",
  "outputPath": "C:\\full\\path\\DraftingTools.cuix",
  "acadDir": "C:\\Program Files\\Autodesk\\AutoCAD 2027",
  "lispPath": "C:\\full\\path\\DraftingTools.lsp",
  "panels": [
    {
      "name": "Panel Name",
      "buttons": [
        {
          "label": "Zoom Selection",
          "command": "(c:ZOOMSEL)",
          "imagePath": "C:\\icons\\zoomsel.bmp",
          "tooltip": "Zoom to selected objects",
          "tooltipDescription": "Zooms viewport to fit current selection set.",
          "tooltipImage": "C:\\icons\\zoomsel.gif"
        }
      ]
    }
  ]
}
```

- `acadDir` — AutoCAD install dir, used to detect R-series (R26.0 = 2027, R25.1 = 2026, R25.0 = 2025)
- `lispPath` — copied into bundle; `.Help.html` and `.chm` next to it are also auto-copied
- `tooltipImage` — GIF/PNG shown in expanded tooltip; recommended 300×187px, <30KB
- `imagePath` — 16×16 BMP for ribbon button icon; omit for auto-generated colored placeholder

Write config with an explicit timestamp to `$env:TEMP`, then run:

```powershell
$configPath = "$env:TEMP\cuix_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
# ... write config to $configPath ...

# With exe (preferred)
& "$env:USERPROFILE\.cuixbuilder\CuixBuilder.exe" $configPath

# With SDK fallback — clone source from GitHub
$src = "$env:TEMP\acad-cuix-builder-src"
if (-not (Test-Path $src)) {
    git clone https://github.com/ADN-DevTech/acad-cuix-builder $src
}
dotnet run --project $src -c Release -- $configPath
```

---

## Step 6 — Report result

On success:
```
Done: <outputPath>
In AutoCAD: CUILOAD → browse to <outputPath>
```

On failure: show stderr and diagnose (common: missing exe, wrong path, invalid JSON).

---

## Command normalization

| User types | Becomes |
|---|---|
| `QLEADER` | `^C^CQLEADER` |
| `zoom e` | `^C^CZOOM E` |
| `(alert "Hi")` | `^C^C(alert "Hi")` |
| `^C^CMYCOMMAND` | `^C^CMYCOMMAND` (unchanged) |

---

## Placeholder icon colors (auto-generated when no image provided)

Index cycles 0→7 across all buttons in the CUIX.

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Blue | Green | Orange | Purple | Teal | Red | Amber | Cyan |

---

## F1 Help — CHM via PackageContents

F1 help works via **CHM + PackageContents.xml**. Tested and confirmed working in AutoCAD 2027.

### How it works
- `HelpFile="./Contents/Win64/Plugin.chm"` on `<ApplicationPackage>`
- `<Command Local="ZOOMSEL" HelpTopic="zoomsel" />` — anchor name only (no `.htm`)
- CUIX `<ToolTip HelpTopic="zoomsel" HelpSource="C:\absolute\path\Plugin.chm" />`

### Config
Set `chmPath` + `helpTopic` (anchor name, not filename) per button:

```json
{
  "chmPath": "C:\\path\\to\\DraftingTools.chm",
  "panels": [{
    "buttons": [{
      "helpTopic": "zoomsel"
    }]
  }]
}
```

CuixBuilder strips `.htm`/`.html` extensions automatically if user provides a filename — always outputs anchor name only.

---

## Requirements

- **CuixBuilder.exe** — install via `install.ps1` (downloads from GitHub Releases, ~200KB)
- **.NET 10 runtime** — ships with AutoCAD 2027; or install from https://dot.net
- **Windows only** — AutoCAD bundle format is Windows-specific
