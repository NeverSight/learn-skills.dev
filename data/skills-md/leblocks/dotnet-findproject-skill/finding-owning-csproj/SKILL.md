---
name: finding-owning-csproj
description: Finds the .csproj project that owns a given C# (.cs) source file using the findproject dotnet CLI tool. Use when locating, building, or testing the project that contains a specific .cs file, when resolving a file to its nearest project, or when the user mentions findproject, csproj lookup, or a file's owning project. Don't use it for .vbproj or .fsproj projects, for non-.NET languages, or for resolving a project to its solution (.sln).
---

# Finding the owning .csproj for a C# file

`findproject` is a .NET global CLI tool that, given a path to a C# source file,
prints the absolute path of the **nearest** `.csproj` that owns it by walking up
the directory tree.

## When to use

Use `findproject` whenever you need to resolve the `.csproj` that owns a `.cs`
file — to find it, or to build, test, restore, or run that project. Do not guess
the project, walk the directory tree by hand, or grep for `.csproj` files.

## Prerequisite

The `findproject` command must be on `PATH`. If it is missing, install it:

```bash
dotnet tool install --global findproject
```

## Quick start

Pass one existing `.cs` file (relative or absolute; `/` or `\` both work):

```bash
findproject src/Common/Commands.Common/PowerBICmdlet.cs
# -> .../src/Common/Commands.Common/Commands.Common.csproj
```

## Detecting success (important)

The exit code is **always `0`**, even when nothing is found. Do not branch on the
exit code — capture stdout and check whether it is empty.

```bash
proj=$(findproject path/to/File.cs)
if [ -n "$proj" ]; then echo "Owns: $proj"; else echo "No project found"; fi
```

On Windows **cmd.exe**, capture the output with `for /f` and test with
`if defined`:

```bat
@echo off
set "proj="
for /f "delims=" %%i in ('findproject path\to\File.cs') do set "proj=%%i"
if not defined proj echo No project found
if defined proj echo Owns: %proj%
```

## Invocation modes

- **Single file (primary):** `findproject <file.cs>` — the argument must exist
  and end in `.cs` (case-insensitive).
- **No arguments:** `findproject` — finds the `.csproj` at or above the current
  working directory.
- **Stdin:** pipe one path per line (`paths | findproject`). Stdin paths must be
  **absolute** and may be any existing file; output is de-duplicated and sorted.

## Key rules

- Selection walks up and stops at the nearest directory containing **exactly
  one** `.csproj`. A directory with multiple `.csproj` is ambiguous and skipped.
- Only `.csproj` is matched — not `.vbproj` or `.fsproj`.
- No output means "not found" (bad/missing path, no project above, or ambiguity).
