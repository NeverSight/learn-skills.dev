---
name: sas-packages
description: Installing, loading and unloading SAS packages with the SAS Packages Framework (SPF) and the SASPAC archive - the packages fileref rules, %installPackage / %loadPackage / %helpPackage / %unloadPackage, version pinning. Use when installing a package such as sasjscore, or debugging an install that reports rc=20006 or a missing package zip.
license: MIT
copyright: Copyright (c) SASjs
spdx-license-identifier: MIT
---

# SAS Packages (SPF)

<!-- SPDX-License-Identifier: MIT -->

A **SAS package** is a single zip holding a group of SAS programs (macros, functions, data steps) plus automatically generated description, load, unload and help files. The **SAS Packages Framework** (SPF, by Bartosz Jablonski) installs and loads them from a folder of zips, so a package can be pinned, versioned and swapped without touching `SASAUTOS` or a macro catalogue.

This skill covers using the framework as a consumer. It is not SASjs-specific - SPF is an independent project, and the packages it serves come from any author.

## When to use

- Installing a package into a SAS session, e.g. `sasjscore` (the SASPAC packaging of @sasjs/core)
- Debugging `%installPackage` / `%helpPackage` / `%loadPackage` failures
- Setting up a packages folder, or working out which path to point the `packages` fileref at
- Loading macros for one job without adding them to a shared server's `SASAUTOS`

Don't use for: authoring or publishing a package (`%generatePackage`), or for @sasjs/core's own macro coding standards - see the `sasjs-core` skill for those.

## Enabling the framework

The framework is a single file. Enable it in the session:

```sas
filename packages "%sysfunc(pathname(work))";
filename SPFinit url "https://bit.ly/SPFinit";
%include SPFinit;
```

The raw URL `https://raw.githubusercontent.com/yabwon/SAS_PACKAGES/main/SPF/SPFinit.sas` is the same file without the shortener, and is a better choice where a redirect is unwanted. Enabling the framework needs internet access from the SAS session; it is a one-off per session unless the file is kept on disk (see Persistence below).

## The packages fileref (mandatory)

- The fileref **must** be named `packages`. `packages` and `package` are reserved keywords in SPF; a different name is not picked up.
- It points at a **directory**, not a zip file.
- **The directory must already exist.** SPF does not create it - `%installPackage` is documented as equivalent to manually downloading the zip into that folder, and it will not make the folder for you.

Pick the path by what you need:

| Need | Use |
|---|---|
| Throwaway / portable, works on Windows, Viya and SASjs Server | `filename packages "%sysfunc(pathname(work))";` |
| Survives the session (install once, reuse) | A real directory that exists, e.g. `C:/SAS_PACKAGES` on Windows, or any writable directory on a Linux estate |

`C:/SAS_PACKAGES` appears throughout the SPF documentation, but it is a Windows example. On Linux (Viya, SASjs Server) it is just a relative path, so unless that directory happens to exist the install fails - see Pitfalls.

## Install, load, unload

```sas
%installPackage(sasjscore)  %* download the zip into the packages folder;
%helpPackage(sasjscore)     %* print the package description and contents;
%loadPackage(sasjscore)     %* compile the macros into the session;
%unloadPackage(sasjscore)   %* remove them again;
```

- `%installPackage()` fetches the zip over the network. Default source is the SASPAC archive, `https://github.com/SASPAC/`; override with `sourcePath=` or `mirror=`.
- Package names are space separated and carry **no** `.zip` extension: `%installPackage(pkg1 pkg2)`. Pin a version in parentheses: `%installPackage(baseplus(1.17) macroarray(1.0))`. Add `replace=0` to refuse to overwrite an already-installed package.
- `%installPackage(SPFinit)` installs the framework itself into the packages folder.
- `%loadPackage()` compiles into the session; `%unloadPackage()` deletes those entries from the macro catalogue. A job that needs the macros but whose server should not carry them in `SASAUTOS` can load, use and unload in one session.
- Where the SAS session has no zip fileref support, unzip `<name>.zip` into `<name>.disk` and pass `zip=disk`: `%loadPackage(pkgname,zip=disk,options=)`.

## Persistence: install once, then go offline

Install the framework into the packages folder once:

```sas
%installPackage(SPFinit)
```

After that the two network-facing lines collapse to a local include, and no network access is needed at run time:

```sas
filename packages "/permanent/path/to/packages";
%include packages(SPFinit.sas);
%loadPackage(sasjscore)
```

This requires the fileref to point at a permanent directory - with `%sysfunc(pathname(work))` the framework is gone when the session ends.

## Pitfalls

- **`rc=20006` is a failure, despite reading as success.** `%installPackage` prints `Done with return code rc=20006 (zero = success)` - the parenthetical is just the message template. 20006 means the install failed; the real error is the `ERROR: Physical file does not exist, <dir>/<name>.zip` line that follows. Do not trust the `rc=` line alone.
- **The packages folder must exist before you call `%installPackage`.** This is the most common cause of the failure above, and it bites hardest on Linux because the documented `C:/SAS_PACKAGES` example silently becomes a relative path. Verify with `%put %sysfunc(fileexist(<dir>));` and create it first if it returns 0.
- **A missing zip cascades.** Once the install fails, `%helpPackage` and `%loadPackage` both fail with `File "<dir>/<name>.zip" does not exist!`, and the macros are simply absent - a later call gives `WARNING: Apparent invocation of macro X not resolved`. Fix the install rather than chasing the macro.
- **Installing needs network egress from the SAS session**, not from your workstation. A locked-down compute context without internet cannot reach SASPAC or GitHub.
- **`%loadPackage` is per session.** Macros loaded in one session are not visible in another; re-load in each session (or use `SASAUTOS` / the CLI for durable resolution).

## Verification

After loading, prove the macros are actually live rather than assuming the install worked:

```sas
%put NOTE: package version check;
%helpPackage(sasjscore)          %* prints "Help for package SASjsCore, version X.Y.Z, license MIT";
%put NOTE: getuser returns %mf_getuser();
```

A clean run shows `INFO: Package sasjscore installed.`, the help block with an explicit version, and a resolved macro call. `%unloadPackage()` can then be confirmed by the same call returning `Apparent invocation of macro MF_GETUSER not resolved`.

## Limitations

This skill is a static reference for the SAS Packages Framework. It does not execute SAS code, run shell commands, access the filesystem, or make network requests. Code examples are illustrative and must be submitted to a SAS session by the user. The framework is maintained at https://github.com/yabwon/SAS_PACKAGES and the archive at https://github.com/SASPAC - consult those for the authoritative macro reference and the current framework version.
