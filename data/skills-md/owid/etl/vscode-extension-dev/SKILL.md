---
name: vscode-extension-dev
description: Develop, build, and test VSCode extensions in this repo. Use when editing extension source code, compiling TypeScript, packaging .vsix files, or installing extensions for testing.
---

# VSCode Extension Development

## Extension locations

Extensions live in `vscode_extensions/<name>/`. Each has:
- `src/extension.ts` — main source code
- `dist/extension.js` — compiled output (esbuild)
- `install/<name>-<version>.vsix` — packaged extension
- `package.json` — manifest with activation events, commands, config

## Build & install workflow

**CRITICAL**: VSCode runs the **installed `.vsix`** from `~/.vscode/extensions/`, NOT the `dist/` in the repo. After every code change you MUST:

1. **Compile**: `cd vscode_extensions/<name> && npm run compile`
2. **Package**: `npx @vscode/vsce package --out install/<name>-<version>.vsix`
3. **Install**: `code --install-extension install/<name>-<version>.vsix --force`
4. **Tell user** to reload: `Cmd+Shift+P` → "Developer: Reload Window"

Just running `npm run compile` is NOT enough — the user will still see old behavior.

## Verifying installed code

To check what code is actually running:
```bash
# Check installed extension has your changes
grep "some_unique_string" ~/.vscode/extensions/<publisher>.<name>-<version>/dist/extension.js
```

## Common pitfalls

- **esbuild watch mode**: `npm run compile` may start a watcher that blocks. This is fine for compilation but you still need to package + install.
- **Version conflicts**: If the installed `.vsix` version matches, VSCode may cache. Use `--force` flag on install.
- **Extension host**: Changes only take effect after "Developer: Reload Window".
