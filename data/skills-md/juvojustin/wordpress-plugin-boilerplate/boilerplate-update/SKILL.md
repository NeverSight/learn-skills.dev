---
name: boilerplate-update
description: |
   Guide for updating WordPress plugins to the latest plugin-boilerplate features.
   Use when: (1) Updating build tools or adopting @wordpress/scripts, (2) Adopting
   new features like Abilities API, improved Loader, or i18n workflows, (3) Syncing
   CI/CD pipelines, QA configs, or dependencies, (4) User asks to "update from
   boilerplate", "sync with boilerplate", or "migrate to latest boilerplate".
compatibility: Requires PHP CLI and a WordPress plugin repository with standard plugin headers. This skill is intended for WordPress plugins only.
---

# Boilerplate Update Skill

Update WordPress plugins to the latest plugin-boilerplate features.

## User Confirmation Rules

**ASK for confirmation before:**
- Replacing or significantly restructuring files (Loader.php, main plugin class)
- Changing build tools or asset pipeline
- Modifying CI/CD workflows
- Adding new architectural patterns (Abilities API, Blocks)
- Deleting resources belonging to plugin features

**Proceed without confirmation for:**
- Updating dependency versions
- Adding/renaming scripts with equivalent functionality
- Syncing QA config files
- Copying .opencode commands and .agents/skills

## Identity Replacement Script

Use `scripts/boilerplate-replace.php` (bundled with this skill) for deterministic
placeholder replacement. This avoids manual AI search-and-replace across copied
upstream files.

### Determine the target plugin identity

Before running the script, read these sources from the **target** plugin to determine
the three required parameters:

- **plugin-name** — `Plugin Name:` header in the main plugin PHP file (the root `.php` file containing `@wordpress-plugin` headers)
- **plugin-text-domain** — `Text Domain:` header in the same file
- **plugin-namespace** — the PSR-4 namespace mapped to `src/` in `composer.json` (`autoload.psr-4`), or the `namespace` declaration in `src/*.php` files

### Apply replacements on the cloned boilerplate

Run the script against the **cloned boilerplate directory** so every file in the
reference copy already carries the target plugin's identity before you compare or
copy anything:

```bash
php tmp/boilerplate-ref/.agents/skills/boilerplate-update/scripts/boilerplate-replace.php \
  --path tmp/boilerplate-ref \
  --plugin-name "My Awesome Plugin" \
  --plugin-namespace "My_Awesome_Plugin" \
  --plugin-text-domain "my-awesome-plugin" \
  --cleanup-setup
```

This does three things in one pass:
1. Replaces all boilerplate placeholders (`demo-plugin`, `Demo_Plugin`, etc.)
2. Strips all `BOILERPLATE-DOCS` marker sections
3. Removes setup-only artifacts (`setup.php`, `src/Cli/Setup.php`, composer autoload/hook entries)

After this step every `diff` between `tmp/boilerplate-ref/` and the target plugin
shows only real upstream changes -- no placeholder noise and no setup-only files.

## Workflow

1. Clone fresh boilerplate for comparison:
   ```bash
   git clone --depth 1 https://github.com/JUVOJustin/wordpress-plugin-boilerplate.git ./tmp/boilerplate-ref
   ```
2. Determine target plugin identity (see above).
3. Run the replacement script on `tmp/boilerplate-ref` with `--cleanup-setup` (see above).
4. Use one **subtask/subagent** per key area. Delegate comparison using `diff` against `tmp/boilerplate-ref/`.
5. Present findings to user, categorized by confirmation requirement.
6. Apply changes incrementally.
7. Cleanup: `rm -rf tmp/boilerplate-ref`

## Documentation Reference

The boilerplate includes detailed docs at `tmp/boilerplate-ref/docs/`:

| File | Covers |
|------|--------|
| `abilities.mdx` | Abilities API interfaces, category/ability creation, Loader registration |
| `bundeling.mdx` | wp-scripts bundling, entry points, asset enqueueing, localization |
| `i18n.mdx` | Translation workflow, extract/compile scripts, JSON translations, caveats |
| `create-blocks.mdx` | Block scaffolding, auto-registration via manifest, editor style sharing |
| `wp-env.mdx` | Docker-based dev environment, script structure, CI/CD usage |
| `acf-json-sync.mdx` | ACF field group JSON storage patterns |
| `work-with-ai.mdx` | AI integration: commands, skills, AGENTS.md, WordPress agent skills |
| `documentation.mdx` | Documentation structure, front matter metadata, heading rules |

Read these docs for implementation details. This skill only provides high-level guidance.

## Key Areas to Compare

### 1. PHP (composer.json & QA)

Compare: `diff composer.json tmp/boilerplate-ref/composer.json`

See docs for details: `i18n.mdx`, `bundeling.mdx`

**Key items:**
- `wp-cli/i18n-command` - Translation extraction/compilation
- Scripts: `i18n:extract`, `i18n:compile`, `phpstan`, `phpcs`, `phpcbf`
- Strauss config in `extra.strauss` for namespace prefixing
- QA config files: `phpcs.xml`, `phpstan.neon`


### 2. JS & Bundling (package.json, webpack.config.js)

Compare:
- `diff package.json tmp/boilerplate-ref/package.json`
- `diff webpack.config.js tmp/boilerplate-ref/webpack.config.js`

See docs for details: `bundeling.mdx`, `wp-env.mdx`, `create-blocks.mdx`

**Key items:**
- `@wordpress/scripts` - Bundling, linting, formatting
- `@wordpress/env` - Containerized WordPress for dev/CI
- Scripts: `start`, `build` (with `--blocks-manifest`), `lint:*`, `format`, `create-block`, `env:*`
- QA config: `.eslintrc`

### 3. GitHub Actions (.github/workflows/)

Compare: `diff -r .github/workflows tmp/boilerplate-ref/.github/workflows`

- `setup.yml` - Reusable workflow with dependency caching
- `test-analyse.yml` - PHPStan, PHPCS, JS linting on push
- `deploy.yml` - Release automation, translation compilation via wp-env

### 4. Loader.php

Compare: `diff src/Loader.php tmp/boilerplate-ref/src/Loader.php`

**New methods:**
- `add_shortcode($tag, $component, $callback)`
- `add_cli($name, $instance, $args)`
- `add_ability($ability_class)` - Categories auto-register

### 5. Main Plugin Class

Compare: `diff src/*.php tmp/boilerplate-ref/src/Demo_Plugin.php`

**New patterns:**
- `enqueue_entrypoint($entry)` - See `tmp/boilerplate-ref/docs/bundeling.mdx`
- `register_blocks()` - See `tmp/boilerplate-ref/docs/create-blocks.mdx`

### 6. i18n Workflow

Scripts: `i18n:extract` (creates .pot, updates .po) and `i18n:compile` (generates .mo, .json, .php)

See `tmp/boilerplate-ref/docs/i18n.mdx` for workflow, caveats, and AI command.

### 7. Abilities API (WordPress 6.9+)

See `tmp/boilerplate-ref/docs/abilities.mdx` for interface reference and examples.

**Key pattern:** `$this->loader->add_ability(Abilities\My_Ability::class)`

### 8. Agent Configuration

Compare:
- `diff -r .opencode/command tmp/boilerplate-ref/.opencode/command`
- `diff -r .agents/skills tmp/boilerplate-ref/.agents/skills`

See `tmp/boilerplate-ref/docs/work-with-ai.mdx` for AI integration details.

**Sync strategy:**
- Add new items from upstream
- Update existing (ask user if diff is significant)
- Ask user before removing local-only items
- Adapt text domain and paths after copying
- Remove redundant skills/commands if upstream now includes them or they are possibly renamed

### 9. File Control files
Compare:
- `diff .distignore tmp/boilerplate-ref/.distignore`
- `diff .gitignore tmp/boilerplate-ref/.gitignore`

## Verification

1. Ran `composer install && npm install` after changes
2. Ran `npm run build` after changes
3. Ran `composer phpstan && composer phpcs` after changes
4. Ran `npm run lint:js && npm run lint:style` after changes
5. Test plugin functionality
