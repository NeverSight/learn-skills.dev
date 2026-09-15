---
name: acad-arx-wizard
description: "Agentic ObjectARX project scaffolding for AutoCAD 2027 / Visual Studio 2026. Replaces the broken .vsz VsWizardEngine wizard with a PowerShell script that generates identical C++ project files. Works for new ARX/DBX/CRX projects and add-on class wizards (Jig, Reactors, Custom Object, MFC, .NET Wrapper, COM Wrapper, Dynamic Property)."
argument-hint: "Wizard type and project/class name (e.g. 'create an ARX app called MyPlugin with MFC shared', or 'add a Jig class CMyJig to my project')"
---

# ObjectARX Wizard Skill — AutoCAD 2027 / VS 2026

Scaffold ObjectARX C++ projects and classes using an AI conversation + PowerShell generator.

## Skill Location

The scripts live in the same folder as this SKILL.md:

```
<skill-root>/
├── SKILL.md
├── docs/
│   ├── arx-dev-guide.md              ← ObjectARX 2027 build configuration reference
│   └── learnings.md                  ← live wiki: gotchas, workarounds, verified API behaviors
├── scripts/
│   ├── Invoke-TemplateExpansion.ps1   ← shared token engine (do not call directly)
│   ├── New-ArxApp.ps1                 ← full ARX/DBX/CRX project
│   ├── New-ArxCustomObject.ps1        ← custom ObjectDBX entity class
│   ├── New-ArxReactors.ps1            ← transient reactor class
│   ├── New-ArxJig.ps1                 ← AcEdJig subclass
│   ├── New-ArxMFCSupport.ps1          ← MFC dialog / palette / control
│   ├── New-ArxNETWrapper.ps1          ← managed .NET wrapper
│   ├── New-ArxComWrapper.ps1          ← ATL COM wrapper object
│   └── New-ArxDynProp.ps1             ← ATL dynamic property class
├── templates/                         ← source template files (do not edit)
└── props/                             ← Autodesk.arx-2027.props, crx.props
```

## When to Use

- Developer wants to start a new AutoCAD 2027 ARX/DBX/CRX C++ project in VS 2026
- Developer wants to add a Jig, Reactor, Custom Object, or other class to an existing project
- The classic VS wizard (File → New → Project → ObjectARX) is broken (VS 2026 regression — see MS Developer Community #11071541)

## Wizard Types

| User says... | Script to run |
|---|---|
| "ARX app", "new plugin", "create project" | `New-ArxApp.ps1` |
| "custom object", "custom entity", "AcDbEntity subclass" | `New-ArxCustomObject.ps1` |
| "reactor", "database reactor", "entity reactor" | `New-ArxReactors.ps1` |
| "jig", "AcEdJig", "interactive input" | `New-ArxJig.ps1` |
| "MFC dialog", "palette", "dockbar", "MFC class" | `New-ArxMFCSupport.ps1` |
| ".NET wrapper", "managed wrapper", "C++/CLI" | `New-ArxNETWrapper.ps1` |
| "COM wrapper", "ATL object", "IDispatch" | `New-ArxComWrapper.ps1` |
| "dynamic property", "AcDbDynBlockReference", "dynprop" | `New-ArxDynProp.ps1` |

---

## Procedure

### Step 1 — Identify skill root

Resolve the absolute path to this SKILL.md's containing directory.
All scripts are at: `<skill-root>\scripts\`

---

### Step 2 — Identify wizard type

Map user intent to one of the 8 wizard types above. If unclear, ask:
> "Which wizard do you need? New ARX/DBX/CRX project, or an add-on class (Jig, Reactor, Custom Object, MFC, .NET Wrapper, COM Wrapper, Dynamic Property)?"

---

### Step 3 — Collect parameters

Ask only for **mandatory** parameters that are missing. Do not ask for optional ones unless the user mentions them.

#### New-ArxApp — full project

| Parameter | Mandatory | Values | Ask if missing |
|---|---|---|---|
| `-ProjectName` | Yes | valid C++ identifier | "What is the project name?" |
| `-OutputPath`  | Yes | folder path | "Where should the project be created?" |
| `-AppType`     | No  | `arx` / `dbx` / `crx` | Default: `arx` (ask if user is unsure) |
| `-MfcMode`     | No  | `none` / `shared` / `ext` | Default: `none` |
| `-UseAtl`      | No  | switch | Only ask if user mentions COM |
| `-UseDotNet`   | No  | switch | Only ask if user mentions .NET or CLR |
| `-RdsPrefix`   | No  | 3-letter symbol | Default: `Adk` |

#### New-ArxCustomObject — custom entity

| Parameter | Mandatory | Default |
|---|---|---|
| `-ClassName`   | Yes | — |
| `-OutputPath`  | Yes | — |
| `-BaseClass`   | No  | `AcDbEntity` |
| `-Protocols`   | No  | `2` (Object + Entity) |
| `-ProjectName` | No  | `MyProject` |

#### New-ArxReactors — reactor

| Parameter | Mandatory | Notes |
|---|---|---|
| `-ClassName`    | Yes | — |
| `-ReactorType`  | Yes | See reactor type list below |
| `-OutputPath`   | Yes | — |
| `-ProjectName`  | No  | `MyProject` |

Common reactor types: `AcDbDatabaseReactor`, `AcDbObjectReactor`, `AcDbEntityReactor`,
`AcEdInputContextReactor`, `AcApDocManagerReactor`, `AcDbLayoutManagerReactor`,
`AcDbAnnotationScaleReactor`, `AcDMMReactor`

#### New-ArxJig — jig class

| Parameter | Mandatory | Default |
|---|---|---|
| `-ClassName`       | Yes | — |
| `-OutputPath`      | Yes | — |
| `-ObjectName`      | No  | `AcDbEntity` |
| `-NumberOfInputs`  | No  | `1` |
| `-ProjectName`     | No  | `MyProject` |

#### New-ArxMFCSupport — MFC class

| Parameter | Mandatory | Default |
|---|---|---|
| `-ClassName`   | Yes | — |
| `-OutputPath`  | Yes | — |
| `-MfcType`     | No  | `Dialog` |
| `-IddDialog`   | No  | `IDD_DIALOG1` |
| `-ProjectName` | No  | `MyProject` |

MFC types: `Dialog`, `ChildDialog`, `TabDialog`, `Palette`, `PaletteSet`,
`DockControlBar`, `Control`, `FileDialog`, `FileNavDialog`,
`FieldDialog`, `FieldFormatDialog`, `FieldOptionDialog`

#### New-ArxNETWrapper — managed wrapper

| Parameter | Mandatory | Default |
|---|---|---|
| `-WrapperName`       | Yes | — |
| `-OutputPath`        | Yes | — |
| `-CustomObjectName`  | No  | `AcDbEntity` |
| `-CompanyNamespace`  | No  | `Autodesk` |
| `-ObjectNamespace`   | No  | `AutoCAD` |
| `-ManagedDerivation` | No  | `Entity` |
| `-ProjectName`       | No  | `MyProject` |

#### New-ArxComWrapper — ATL COM wrapper

| Parameter | Mandatory | Default |
|---|---|---|
| `-ShortName`       | Yes | — |
| `-OutputPath`      | Yes | — |
| `-ConnectionPoints`| No  | switch |
| `-InterfaceDual`   | No  | switch |
| `-ProjectName`     | No  | `MyProject` |

#### New-ArxDynProp — dynamic property

| Parameter | Mandatory | Default |
|---|---|---|
| `-ClassName`       | Yes | — |
| `-OutputPath`      | Yes | — |
| `-InterfaceName`   | No  | derived from ClassName |
| `-ConnectionPoints`| No  | switch |
| `-ProjectName`     | No  | `MyProject` |

---

### Step 4 — Run the script

Run the appropriate script from `<skill-root>\scripts\` in a PowerShell terminal.

Example for a full ARX project:

```powershell
& powershell.exe -ExecutionPolicy Bypass -NoProfile -File "<skill-root>\scripts\New-ArxApp.ps1" `
    -ProjectName MyPlugin `
    -OutputPath  "C:\Dev" `
    -AppType     arx `
    -MfcMode     shared
```

Example for a Jig add-on:

```powershell
& powershell.exe -ExecutionPolicy Bypass -NoProfile -File "<skill-root>\scripts\New-ArxJig.ps1" `
    -ClassName      CMyJig `
    -ObjectName     AcDbLine `
    -NumberOfInputs 2 `
    -ProjectName    MyPlugin `
    -OutputPath     "C:\Dev\MyPlugin"
```

---

### Step 5 — Confirm output

After the script runs, confirm what was generated by listing the output folder:

```powershell
Get-ChildItem "C:\Dev\MyPlugin" | Select-Object Name, Length
```

Report the file list to the user and include next steps:

**For New-ArxApp:**
> "Project created at `C:\Dev\MyPlugin\MyPlugin.vcxproj`. Open it in Visual Studio 2026. Verify the ObjectARX SDK path in `Autodesk.arx-2027.props`, then Build → x64 Debug."

**For add-on wizards:**
> "Generated `ClassName.h` and `ClassName.cpp` in `OutputPath`. In Visual Studio: right-click your project → Add → Existing Item → select the files."

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Destination already exists` | Choose a different `-OutputPath`, or delete the existing folder first |
| `ReactorType not found` | Run `Get-ChildItem <skill-root>\templates\reactors\*_tmpl.h \| ForEach-Object { $_.Name -replace '_tmpl\.h$','' }` for the full list |
| Build error: `Cannot open include file 'acdb.h'` | Set `ARXSDK` env var or edit `Autodesk.arx-2027.props` to point at your ObjectARX 2027 SDK |
| `CLRSupport` errors in .NET wrapper | Ensure the project's `.vcxproj` has `<CLRSupport>NetCore</CLRSupport>` |
| VS 2026 wizard still broken | This skill replaces it — ignore the broken File→New wizard. Use this skill instead. |

---

## Post-Scaffolding: Build Configuration Reference

After a project is scaffolded, the developer (or you, the AI agent) will continue writing plug-in code. When helping with build settings, library selection, preprocessor defines, or diagnosing linker/runtime errors, **read `<skill-root>/docs/arx-dev-guide.md`**. It covers:

- Required compiler flags (`/MD`, `/EHsc`, `/GR`, etc.) and **why** each matters
- The property-sheet inheritance chain (`rxsdk_common` → debug/release → dbx/arx/crx)
- Which `.lib` files to link for each project type (DBX, ARX, CRX) and optional APIs (B-Rep, AEC Modeler)
- Debug vs Release configuration differences
- Common pitfalls — especially **the `/MD` vs `/MDd` rule** (AutoCAD is always a Release binary; plug-ins must use `/MD` even in Debug)

> **Critical rule:** AutoCAD ships as a Release build. Plug-in DLLs must always link with `/MD` (MultiThreadedDLL), never `/MDd`. Using `/MDd` causes CRT mismatch, heap corruption, and crashes. `/MDd` is only valid with an internal Autodesk Debug build of AutoCAD.

---

## Field Learnings

`<skill-root>/docs/learnings.md` is a living wiki of gotchas hit in real sessions: VS 2026 + MFC + ARX SDK 2027 build traps, DllMain conflicts, MFC module-state rules, scaffold quirks. Read it when:

- Diagnosing build / link errors that look like CRT / STL / RTC mismatches
- A scaffolded project fails on first build with MFC shared mode
- Adding new templates — promote any newly verified fix from `learnings.md` back into the template files in this skill so future scaffolds inherit the fix.
