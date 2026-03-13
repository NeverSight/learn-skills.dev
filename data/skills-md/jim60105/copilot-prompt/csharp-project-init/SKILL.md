---
name: csharp-project-init
description: Initialize a C# ASP.NET Core Web API project with Entity Framework Core, EditorConfig, gitignore, and gitattributes. Use when the user wants to create a new C# project, scaffold a .NET Web API, or set up a C# development environment with EF Core tools.
metadata:
  original-prompt: csharp-project-init.prmpt.md
---

# C# Project Init

Set up a C# ASP.NET Core Web API project with proper tooling and configuration.

Git commit after each step that modifies or creates files. Skip commit if nothing to commit.

## Steps

1. Ensure the Git working tree is clean:
   ```bash
   git status
   ```
   If the working directory is not clean, stop execution.

2. Check .NET SDK version (must be >= `10.0.103`):
   ```bash
   dotnet --version
   ```

3. Create the project using the `webapi` template without `-n` argument:
   ```bash
   dotnet new webapi -controllers
   ```

4. Add Entity Framework Core 10 and related SQL Server NuGet packages. Don't use prerelease versions.

5. Check for EF Core Power Tools CLI:
   ```bash
   efcpt --version
   ```
   If not installed or version is lower than `10`, reinstall:
   ```bash
   dotnet tool install ErikEJ.EFCorePowerTools.Cli -g --version 10.*
   ```

6. Set up C# Global Usings in `GlobalUsings.cs` with common namespaces.

7. Add `.gitignore` file — refer to the gitignore-generator skill.

8. Add `.gitattributes` file:
   ```gitattributes
   # Set default behavior to automatically normalize line endings.
   * text=auto

   # Force batch scripts to always use CRLF line endings.
   *.{cmd,[cC][mM][dD]} text eol=crlf
   *.{bat,[bB][aA][tT]} text eol=crlf

   # Force bash scripts to always use LF line endings.
   *.sh text eol=lf

   .env text eol=lf
   Dockerfile text eol=lf

   # Denote all files that are truly binary and should not be modified.
   *.mp3 binary
   *.wav binary
   *.bmp binary
   *.png binary
   *.jpg binary
   *.gif binary
   ```

9. Download the `.editorconfig`:
   ```bash
   curl -sL https://gist.github.com/jim60105/ae6ba63978a2dc3ffb3ebb77344cc7f7/raw/47f342c4b793a32697af6d62022692c26f849c07/.editorconfig > .editorconfig
   ```

Let's do this step by step.
