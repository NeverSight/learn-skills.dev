---
name: git-commit-push
description: Automates git commit and push workflow with descriptive commit messages. Analyzes changes, generates conventional commit messages, stages files, commits, and pushes to remote. Use when the user asks to commit changes, push code, or save work to git.
---

# Git Commit and Push

## Quick Start

When committing and pushing changes:

1. Check git status to see what changed
2. Stage all changes with `git add .`
3. Generate descriptive commit message following conventional commits
4. Commit with the message
5. Push to remote repository

**Tras el push (deploy en Vercel):** Si se cambiaron assets o se quiere que la actualización se vea pronto en todos los dispositivos, recordar purgar caché: `npm run cache:purge` (o Vercel → Settings → Caches). Ver skill **build-start** y `docs/CACHE_PURGE_ANTES_DEPLOY.md`.

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependencies, build config
- `ci`: CI/CD changes

### Scope (Optional)

Component, module, or area affected (e.g., `auth`, `products`, `admin`)

### Subject

- Use imperative mood: "add" not "added" or "adds"
- First letter lowercase
- No period at the end
- Max 72 characters

### Body (Optional)

- Explain WHAT and WHY, not HOW
- Wrap at 72 characters
- Use bullet points for multiple changes
- Reference issues: "Closes #123"

### Footer (Optional)

- Breaking changes: `BREAKING CHANGE: <description>`
- Issue references: `Closes #123`, `Fixes #456`

## Examples

### Simple Feature

```bash
git commit -m "feat(products): add lazy loading to product images

- Implement lazy loading for offscreen images
- Add sizes attribute for responsive images
- Optimize image decoding with async

Impact: ~250ms improvement in image loading performance"
```

### Multiple Changes

```bash
git commit -m "feat: optimizaciones de performance post-deploy

- Optimización de JavaScript: lazy loading de framer-motion en 5 componentes
- Optimización de imágenes: agregado lazy loading, sizes y decoding async
- Optimización de base de datos: aplicados 7 índices para queries críticas
- Documentación: agregado resumen completo de optimizaciones

Impacto estimado: ~1.6s de mejora en métricas de performance
- JavaScript no utilizado: ~1.3s
- Imágenes offscreen: ~100ms
- Sizing de imágenes: ~150ms
- Tiempo de respuesta del servidor: ~44ms"
```

### Bug Fix

```bash
git commit -m "fix(auth): resolve session expiration issue

- Fix session token refresh logic
- Add proper error handling for expired tokens
- Update session timeout configuration

Fixes #123"
```

### Performance Improvement

```bash
git commit -m "perf(database): optimize product queries with indexes

- Add composite index on products(brand, is_active, created_at)
- Add index on product_categories(category_id, product_id)
- Reduce query time by ~44ms

Closes #456"
```

## Workflow Steps

### 1. Check Status

```bash
git status
```

Review what files changed. Identify the type of changes (feature, fix, refactor, etc.)

### 2. Stage Changes

```bash
git add .
```

Or stage specific files:
```bash
git add path/to/file1.ts path/to/file2.tsx
```

### 3. Generate Commit Message

Analyze the changes and create a commit message:

- **If multiple related changes**: Group them under one commit with bullet points
- **If unrelated changes**: Suggest separate commits
- **If breaking changes**: Include `BREAKING CHANGE:` in footer
- **If fixes issues**: Reference issue numbers in footer

### 4. Commit

```bash
git commit -m "type(scope): subject

body

footer"
```

For multi-line messages, use:
```bash
git commit -m "type(scope): subject" -m "body line 1" -m "body line 2"
```

### 5. Push

```bash
git push
```

Or specify branch:
```bash
git push origin main
```

## Best Practices

1. **One logical change per commit**: Don't mix unrelated changes
2. **Write clear, descriptive messages**: Future you (and teammates) will thank you
3. **Use present tense, imperative mood**: "add feature" not "added feature"
4. **Reference issues**: Link commits to issues/tickets when applicable
5. **Keep commits focused**: If you made many changes, consider multiple commits
6. **Test before committing**: Ensure code works before committing
7. **Review staged changes**: Use `git diff --staged` before committing

## Common Scenarios

### Performance Optimizations

```bash
git commit -m "perf: optimize component rendering

- Implement React.memo for expensive components
- Add lazy loading for below-fold content
- Reduce bundle size by 40KB

Impact: ~1.3s improvement in initial load time"
```

### Database Migrations

```bash
git commit -m "feat(database): add indexes for product queries

- Create composite index on categories(display_order, name)
- Add index on products(slug, is_active)
- Optimize JOIN queries with product_categories indexes

Migration: 20260123_optimize_data_server_queries"
```

### Documentation Updates

```bash
git commit -m "docs: add performance optimization guide

- Document optimization strategies
- Add examples and best practices
- Include metrics and impact analysis"
```

### Bug Fixes

```bash
git commit -m "fix(images): resolve lazy loading issue

- Fix images not loading with lazy attribute
- Add proper error handling for failed loads
- Update sizes attribute for responsive images

Fixes #789"
```

## Error Handling

If push fails:

1. Check if remote branch is ahead: `git fetch`
2. Pull and merge: `git pull origin main`
3. Resolve conflicts if any
4. Push again: `git push`

If commit fails:

1. Check git config: `git config user.name` and `git config user.email`
2. Verify you're on the correct branch: `git branch`
3. Check for uncommitted changes: `git status`

## Notes

- Always verify changes with `git status` before committing
- Use `git diff --staged` to review what will be committed
- Consider using `git commit --amend` for small fixes to last commit (before pushing)
- Use `git commit --no-verify` only when absolutely necessary (bypasses hooks)
