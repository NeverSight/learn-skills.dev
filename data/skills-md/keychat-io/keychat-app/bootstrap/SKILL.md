---
name: bootstrap
description: Initialize or reset the Keychat development environment
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(melos *), Bash(dart pub *)
---

Set up the Keychat development environment from scratch.

## Steps

1. **Update git submodules**
   ```bash
   git submodule update --init --recursive
   ```

2. **Ensure melos is installed**
   ```bash
   dart pub global activate melos 7.3.0
   ```

3. **Bootstrap all packages**
   ```bash
   melos bootstrap
   ```

4. **Check for .env file**
   If `packages/app/.env` doesn't exist, remind the user:
   - Copy `.env.example` to `.env`
   - Configure FCM keys for push notifications

## Success criteria
- All submodules are cloned
- Melos bootstrap completes without errors
- Dependencies are resolved for all packages
