---
name: vsdevshell
description: Enter the Visual Studio Developer environment in the current PowerShell session via the VsDevShell module (MSBuild/CL toolchain env vars).
---

# VsDevShell (Visual Studio Developer Shell)

Use this skill when you need to run Windows build tools that typically only work after a Visual Studio Developer Prompt / `VsDevCmd.bat` has been applied.

## When to use

Use this skill when you see errors like:

- `msbuild : The term 'msbuild' is not recognized...`
- `cl.exe`/`link.exe`/`rc.exe` not found
- CMake/Ninja can’t find the MSVC toolchain

Start with `msbuild`, but the same approach applies to many VS toolchain commands.

## Common tools that often need VS dev env

If you need to run any of the following, **enter the VS dev shell first** so PATH/Windows SDK/VC tools variables are set correctly:

- Build / project tooling: `msbuild.exe`, `devenv.com`, `nmake.exe`
- Build systems (sometimes VS-bundled): `cmake.exe`, `ninja.exe`
- Packaging & signing (Windows SDK): `signtool.exe`, `makeappx.exe`, `makepri.exe`, `appcert.exe`
- Resources & manifests (Windows SDK): `rc.exe`, `mt.exe`, `mc.exe`
- IDL / interop: `midl.exe`, `tlibimp.exe`, `tlbexp.exe`
- Binary inspection & PDB/symbol utilities (varies by installed components): `dumpbin.exe`, `pdbcopy.exe`, `pdbstr.exe`, `symstore.exe`, `symchk.exe`
- Driver/INF tooling (specialized; requires WDK components): `inf2cat.exe`

If the user’s command references one of these tools (or a build script calls them indirectly), run the “enter dev env” step before running the command.

## Key idea

`Enter-VsDevShell` updates **process environment variables** (PATH, INCLUDE, LIB, VSINSTALLDIR, etc.) for the **current PowerShell process**.

- Run it in the **same** terminal/session where you will run `msbuild`.
- In VS Code tool runners, avoid starting a brand-new shell between “enter dev env” and “build”.

To restore the original environment (the values captured when you entered), use:

- `Exit-VsDevShell`

### Important: one-time per PowerShell process

Treat `Enter-VsDevShell` as a **one-time initialization step per PowerShell process**:

- If you start a **fresh** `pwsh`/`powershell.exe` process (new terminal tab, new task invocation, new CI step, etc.) and you need VS build tools, you must call `Enter-VsDevShell` in that process.
- If you **reuse an existing** PowerShell process where you already called `Enter-VsDevShell`, don’t call it again.
- If you really need to re-enter without leaving, use `Enter-VsDevShell -Force`.
- If you need a *different* dev environment (for example a different `-Arch`/`-HostArch`/`-WinSdk`), use a **new PowerShell process** and call `Enter-VsDevShell` there with the new parameters.

## Prerequisite

This skill assumes the `VsDevShell` module is installed and available on `PSModulePath`.

- Verify availability: `Get-Module -ListAvailable VsDevShell`

If it isn't present, install it from PowerShell Gallery for the current user:

- `Install-Module -Name VsDevShell -Repository PSGallery -Scope CurrentUser`

Then import it:

- `Import-Module VsDevShell`

Notes:

- On first install, PowerShell may prompt to install the NuGet provider and/or to trust `PSGallery`.

## Parameter mapping (intent → Enter-VsDevShell)

- `-Arch`: **target** architecture you want to build for
  - Build `Win32` → `-Arch x86`
  - Build `x64` → `-Arch x64`
  - Build `ARM64` → `-Arch arm64`
- `-HostArch`: architecture of the machine running the tools
  - Typical x64 Windows host → `-HostArch x64`
  - Typical x86 Windows host → `-HostArch x86`
  - Note: currently only `x86`/`x64` are accepted for `-HostArch`.
- `-AppPlatform`: accepted for compatibility, but currently not used to build `VsDevCmd.bat` arguments.
- `-WinSdk`: optional Windows SDK version string (only set when the user specifies a required SDK)
- `-NoExt`, `-NoLogo`: optional switches to reduce startup work/noise
- `-VsInstallPath`: only set when targeting a specific Visual Studio installation

## Recommended workflow (msbuild)

1. Import and enter the environment (x64 host building x64):

  - Run in the *current* PowerShell session:
    - `Import-Module VsDevShell`
    - `Enter-VsDevShell -Arch x64 -HostArch x64 -NoLogo`

2. Verify:

  - Run: `msbuild -version`

3. Build:

   - Run your `msbuild` command (solution/project + configuration/platform as requested).

## VS Code / tool-runner tip

If your tool runner uses a fresh PowerShell process per command, run the “enter dev env” step and the build command in the **same** invocation, for example:

- `pwsh -NoProfile -Command "Import-Module VsDevShell; Enter-VsDevShell -Arch x64 -HostArch x64 -NoLogo; msbuild -version"`

If your tool runner reuses a single long-lived terminal session, run `Enter-VsDevShell` once at the start of that session, then run as many build commands as you need in the same session.

## Cross-compile examples

- Build Win32 from an x64 machine:
  - `Enter-VsDevShell -Arch x86 -HostArch x64`

- Build ARM64 from an x64 machine:
  - `Enter-VsDevShell -Arch arm64 -HostArch x64`

## Inspect without applying

If you want to see what would change without modifying your current process environment:

- `Get-VsDevEnv -Arch x64 -HostArch x64 | Format-Table -AutoSize`

## Cmdlets and common workflows

### Enter / Leave

- Compute + apply VS dev environment:
  - `Enter-VsDevShell -Arch x64 -HostArch x64`
- Restore original values captured at enter time:
  - `Exit-VsDevShell`

### Export / Import `.env`

Export the computed delta to a standard `.env` file (UTF-8 no BOM):

- `Export-VsDevEnv -Arch x64 -HostArch x64 -Path .\vsdev.env -Mode Update`

Apply a `.env` file in the current session:

- Pipeline form:
  - `Import-VsDevEnv .\vsdev.env | Enter-VsDevShell`
- Shortcut:
  - `Enter-VsDevShell -EnvFilePath .\vsdev.env`

Restore only the keys listed in the file (using the saved pre-enter snapshot):

- `Exit-VsDevShell -EnvFilePath .\vsdev.env`

Fully piped chain (compute → export → import → apply):

```powershell
Get-VsDevEnv -Arch x64 -HostArch x64 |
  Export-VsDevEnv -Path .\vsdev.env -Mode Update -PassThru |
  Import-VsDevEnv |
  Enter-VsDevShell
```

Notes:

- This writes the **computed values** (including `PATH`) and will typically **override** whatever values your target process already has.
- Loading a dotenv file varies by tool/shell. For example, in `bash` you often need `set -a; source ./vsdev.env; set +a` to export the variables to child processes.

### GitHub Actions (`GITHUB_ENV`)

In GitHub Actions, `$env:GITHUB_ENV` is a standard env file shared across steps.
Update it so later steps inherit the VS dev environment:

- `Export-VsDevEnv -Arch x64 -HostArch x64 -Path $env:GITHUB_ENV -Mode Update`

If `$env:GITHUB_PATH` is available and you want PATH handled there, use:

- `Export-VsDevEnv -Arch x64 -HostArch x64 -Path $env:GITHUB_ENV -Mode Update -PathMode GitHubPath`

Apply it in the current step/session (optional):

- `Enter-VsDevShell -EnvFilePath $env:GITHUB_ENV`

## Notes

- Windows only (relies on `%COMSPEC%` and Visual Studio's `VsDevCmd.bat`).
- If `msbuild` still isn’t available after enabling the environment, the installed Visual Studio workload may be missing MSBuild/VC tools.
- `AppPlatform` is currently accepted but not used to build `VsDevCmd.bat` arguments.
