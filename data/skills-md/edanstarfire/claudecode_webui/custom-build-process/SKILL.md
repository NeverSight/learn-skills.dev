---
name: custom-build-process
description: Project-specific build process for the Builder workflow. Builds frontend assets for claudecode_webui.
---

# Custom Build Process

## Purpose

This is a **project-specific custom skill** called by the Builder workflow after implementation is complete.
It handles building project artifacts specific to this project (claudecode_webui).

Generic workflow skills invoke this skill if it exists; if absent, the build step is skipped.

## When Called

The Builder invokes this skill from its working directory (the worktree) after code changes are complete but before testing.

## Build Steps

### Frontend Build (if frontend code changed)

Check if frontend code was modified:
```bash
git diff --name-only HEAD~1 | grep -q "^frontend/" && echo "Frontend changed"
```

If frontend code changed, build it:
```bash
cd frontend && npm run build
```

### Verification

After build:
- Verify `frontend/dist/` directory was created/updated
- Check build output for errors
- Report any build failures

## Usage by Generic Skills

The Builder workflow calls this skill like:

```
Invoke custom-build-process skill (no arguments - uses cwd)
```

The skill runs project-specific build commands in the Builder's working directory.
If this skill does not exist, the generic workflow skips the build step.
