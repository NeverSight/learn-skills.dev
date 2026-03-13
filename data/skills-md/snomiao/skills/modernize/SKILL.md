---
name: modernize
description: Modernize JavaScript/TypeScript toolchain to high-performance native alternatives. Use when upgrading build tools, linters, or compilers.
---

# modernize-ts - Native TypeScript Toolchain Upgrade

You are an expert in modern JavaScript/TypeScript tooling. When this skill is invoked, help users upgrade to high-performance native alternatives.

## IMPORTANT: Use Automation Scripts First

This skill includes scripts to handle mechanical work. **Always try these first** before manual interventions.

```bash
SKILL_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/modernize"
```

**Platform Support:**
- ✓ Linux/macOS - Full support
- ✓ Windows - Requires Git Bash/WSL (usually available with Claude Code)
- If scripts fail: Fall back to manual migration (see bottom of this document)

### 1. Detect Current Environment

```bash
$SKILL_DIR/scripts/detect.sh
```

This outputs JSON with:
- Current linters/formatters (eslint, prettier, biome, oxlint)
- Current bundlers (vite, rollup, webpack, tsdown)
- TypeScript setup
- Existing scripts
- **Upgrade recommendations with priorities**

**Use this output to guide decisions.** Don't manually check package.json.

### 2. Run Migration Scripts

For mechanical work (install packages, update scripts), use these:

**Migrate to oxlint/oxfmt:**
```bash
$SKILL_DIR/scripts/migrate-to-oxlint.sh
```
- Detects package manager automatically
- Installs oxlint
- Updates lint/format scripts
- Creates backup

**Migrate to tsdown:**
```bash
$SKILL_DIR/scripts/migrate-to-tsdown.sh
```
- Detects package manager
- Installs tsdown
- Updates build/dev scripts
- Detects entry point automatically

**Migrate to TypeScript native:**
```bash
$SKILL_DIR/scripts/migrate-to-ts-native.sh
```
- Installs @typescript/native-preview
- No script changes needed (drop-in replacement)

### 3. Your Role After Scripts

After running scripts, focus on:
- Complex configuration migration (e.g., ESLint rules → oxlint)
- Edge cases and compatibility issues
- Testing and verification
- CI/CD updates
- Documentation

**Don't manually install packages or update simple scripts** - the migration scripts handle that.

## Workflow

**Fast path (use scripts):**
1. Run `detect.sh` to analyze environment
2. Review recommendations
3. Run appropriate migration script(s)
4. Handle config migration and edge cases
5. Test and verify

**Manual path (only for edge cases):**
- Complex custom configurations
- Monorepo setups
- Special build requirements
- Compatibility issues found during testing

## Migration Paths

### Build Tools
**From:** Rollup, Vite build, esbuild, webpack
**To:** [tsdown](https://github.com/egoist/tsdown) - Fast TypeScript/JavaScript bundler built with Rust

**Benefits:**
- 10-100x faster than traditional bundlers
- Zero config for most projects
- Built-in TypeScript support
- Tree-shaking and minification

### Linting & Formatting
**From:** ESLint, Prettier, Biome
**To:** [oxlint](https://oxc.rs/) + [oxfmt](https://oxc.rs/) - Rust-based linter and formatter

**Benefits:**
- 50-100x faster than ESLint
- Compatible with ESLint rules
- Unified toolchain
- Near-instant feedback

### TypeScript Compiler
**From:** tsc (TypeScript Compiler)
**To:** [@typescript/native-preview](https://github.com/microsoft/TypeScript/tree/main/packages/native-preview) - Native TypeScript compiler

**Benefits:**
- Significantly faster compilation
- Drop-in replacement for tsc
- Official Microsoft implementation
- Better performance for large codebases

## Upgrade Process

When helping with upgrades, follow this systematic approach:

### 1. Analyze Current Setup

First, examine the project:

```bash
# Check package.json for current tools
# Review build scripts
# Identify configuration files (tsconfig.json, .eslintrc, etc.)
```

### 2. Plan Migration

Determine which tools to upgrade based on:
- Current bottlenecks (slow builds, slow linting)
- Project size and complexity
- Team preferences
- CI/CD integration needs

### 3. Implement Incrementally

**Order matters:**
1. Start with linting/formatting (lowest risk)
2. Then upgrade build tools
3. Finally, TypeScript compiler (if needed)

### 4. Update Configuration

**For tsdown:**
```json
{
  "scripts": {
    "build": "tsdown src/index.ts",
    "dev": "tsdown src/index.ts --watch"
  },
  "devDependencies": {
    "tsdown": "latest"
  }
}
```

**For oxlint + oxfmt:**
```json
{
  "scripts": {
    "lint": "oxlint src",
    "format": "oxfmt src",
    "format:check": "oxfmt --check src"
  },
  "devDependencies": {
    "oxlint": "latest"
  }
}
```

**For @typescript/native-preview:**
```json
{
  "scripts": {
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "@typescript/native-preview": "latest"
  }
}
```

### 5. Test Migration

Before finalizing:
- Run the build and verify output
- Check that linting rules still work
- Ensure type checking catches errors
- Test in CI environment
- Verify IDE integration

### 6. Update CI/CD

Update GitHub Actions, GitLab CI, or other pipelines:

```yaml
# Example GitHub Actions
- name: Install dependencies
  run: npm install

- name: Lint
  run: npm run lint

- name: Format check
  run: npm run format:check

- name: Build
  run: npm run build

- name: Type check
  run: npm run typecheck
```

### 7. Document Changes

Update project documentation:
- README.md with new commands
- CONTRIBUTING.md with development setup
- Migration notes for the team

## Common Scenarios

### Scenario 1: Slow ESLint

User complains: "ESLint takes 30 seconds to run"

**Solution:**
1. Install oxlint: `npm install -D oxlint`
2. Migrate ESLint config to oxlint compatible rules
3. Update package.json scripts
4. Keep ESLint config as fallback initially
5. Test thoroughly, then remove ESLint

### Scenario 2: Slow Vite Build

User complains: "Production builds take 5 minutes"

**Solution:**
1. Install tsdown: `npm install -D tsdown`
2. Create minimal tsdown config
3. Update build scripts
4. Compare output with Vite build
5. Adjust config for any differences
6. Switch once validated

### Scenario 3: Large Monorepo Type Checking

User complains: "tsc --noEmit takes forever in our monorepo"

**Solution:**
1. Install @typescript/native-preview
2. Test with subset of packages first
3. Measure performance improvement
4. Roll out to full monorepo
5. Update documentation

## Important Notes

- **Preserve Existing Configs Initially**: Keep old configs commented out during migration
- **Test Incrementally**: Don't upgrade everything at once
- **Measure Performance**: Benchmark before/after to show improvements
- **Check Compatibility**: Ensure editor plugins and tools work with new toolchain
- **Team Communication**: Explain changes and new workflows to the team

## Tool-Specific Tips

### tsdown
- Minimal configuration needed
- Use `tsdown.config.ts` for complex setups
- Supports multiple entry points
- Tree-shaking enabled by default

### oxlint
- Most ESLint rules are supported
- Use `--fix` for auto-fixing
- Much faster than ESLint
- May need custom rules for edge cases

### oxfmt
- Drop-in Prettier replacement
- Use same style options
- Significantly faster
- Consistent with oxlint

### @typescript/native-preview
- Experimental but stable
- Use for type checking only (not emit)
- Faster incremental builds
- Watch mode is very efficient

## Migration Checklist

Use this checklist when upgrading:

- [ ] Analyze current toolchain and pain points
- [ ] Install new tools
- [ ] Update package.json scripts
- [ ] Migrate configuration files
- [ ] Test build output matches original
- [ ] Test linting catches same issues
- [ ] Test type checking works correctly
- [ ] Update CI/CD pipelines
- [ ] Update documentation
- [ ] Test in clean environment
- [ ] Get team approval
- [ ] Remove old dependencies
- [ ] Create migration documentation

## Fallback Strategy

If issues arise:
1. Keep old tools installed temporarily
2. Document any compatibility issues
3. Create hybrid approach if needed
4. Gradual rollout (one tool at a time)

## Resources

- tsdown: https://github.com/egoist/tsdown
- Oxc (oxlint/oxfmt): https://oxc.rs/
- @typescript/native-preview: https://github.com/microsoft/TypeScript/tree/main/packages/native-preview

## Philosophy

These modern tools are designed to be faster and simpler. Trust them to work well with minimal configuration. Start simple, add complexity only when needed.
