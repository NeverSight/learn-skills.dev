---
name: pgsql-parser-testing
description: Test the pgsql-parser repository (SQL parser/deparser). Use when working in the pgsql-parser repo, fixing deparser issues, running parser tests, or validating SQL round-trips. Scoped specifically to the constructive-io/pgsql-parser repository.
compatibility: Node.js 18+, pnpm, pgsql-parser repository
metadata:
  author: constructive-io
  version: "1.0.0"
  scope: constructive-io/pgsql-parser
---

# PGSQL Parser Testing

Testing workflow for the pgsql-parser repository. This skill is scoped specifically to the `constructive-io/pgsql-parser` monorepo.

## When to Apply

Use this skill when:
- Working in the pgsql-parser repository
- Fixing deparser or parser issues
- Running parser/deparser tests
- Validating SQL round-trip correctness
- Adding new SQL syntax support

## Repository Structure

```
pgsql-parser/
  packages/
    parser/           # SQL parser (libpg_query bindings)
    deparser/         # SQL deparser (AST to SQL)
    plpgsql-parser/   # PL/pgSQL parser
    plpgsql-deparser/ # PL/pgSQL deparser
    types/            # TypeScript type definitions
    utils/            # Utility functions
    traverse/         # AST traversal utilities
    transform/        # AST transformation utilities
```

## Testing Strategy

The pgsql-parser uses AST-level equality for correctness, not string equality:

```
parse(sql1) → ast1 → deparse(ast1) → sql2 → parse(sql2) → ast2
```

While `sql2 !== sql1` textually, a correct round-trip means `ast1 === ast2`.

### Key Principle

Exact SQL string equality is not required. The focus is on comparing resulting ASTs. Use `expectAstMatch` (deparser) or `expectPGParse` (ast package) to validate correctness.

## Development Workflow

### Initial Setup

```bash
pnpm install
pnpm build
```

### Running Tests

Run all tests:
```bash
pnpm test
```

Run tests for a specific package:
```bash
cd packages/deparser
pnpm test
```

Watch mode for rapid iteration:
```bash
cd packages/deparser
pnpm test:watch
```

Run a specific test:
```bash
pnpm test --testNamePattern="specific-test-name"
```

## Fixing Deparser Issues

### Systematic Approach

1. **One test at a time**: Focus on individual failing tests
   ```bash
   pnpm test --testNamePattern="specific-test"
   ```

2. **Always check for regressions**: After each fix, run full test suite
   ```bash
   pnpm test
   ```

3. **Build before testing**: Always rebuild after code changes
   ```bash
   pnpm build && pnpm test
   ```

4. **Clean commits**: Stage files explicitly
   ```bash
   git add packages/deparser/src/specific-file.ts
   ```

### Workflow Loop

```
Make changes → pnpm build → pnpm test --testNamePattern="target" → pnpm test (full) → commit
```

## Test Utilities

### Deparser Tests

Location: `packages/deparser/test-utils/index.ts`

```typescript
import { expectAstMatch } from '../test-utils';

it('deparses SELECT correctly', () => {
  expectAstMatch('SELECT * FROM users');
});
```

### AST Package Tests

Location: `packages/ast/test/utils/index.ts`

Uses database deparser for validation:
```typescript
import { expectPGParse } from '../test/utils';

it('round-trips through database deparser', async () => {
  await expectPGParse('SELECT * FROM users WHERE id = 1');
});
```

Note: AST tests require the database to have `deparser.expressions_array` function available.

## Common Commands

| Command | Description |
|---------|-------------|
| `pnpm build` | Build all packages |
| `pnpm test` | Run all tests |
| `pnpm test:watch` | Run tests in watch mode |
| `pnpm lint` | Run linter |
| `pnpm clean` | Clean build artifacts |

## Package-Specific Testing

### Parser Package

Tests libpg_query bindings and SQL parsing:
```bash
cd packages/parser
pnpm test
```

### Deparser Package

Tests AST-to-SQL conversion:
```bash
cd packages/deparser
pnpm test
```

### PL/pgSQL Packages

Tests PL/pgSQL parsing and deparsing:
```bash
cd packages/plpgsql-parser
pnpm test

cd packages/plpgsql-deparser
pnpm test
```

## Debugging Tips

1. **Use isolated debug scripts** for complex issues (don't commit them)

2. **Check the AST structure** when tests fail:
   ```typescript
   import { parse } from 'pgsql-parser';
   console.log(JSON.stringify(parse('SELECT 1'), null, 2));
   ```

3. **Compare ASTs visually** to understand differences:
   ```typescript
   const ast1 = parse(sql1);
   const ast2 = parse(deparse(ast1));
   console.log('Original:', JSON.stringify(ast1, null, 2));
   console.log('Round-trip:', JSON.stringify(ast2, null, 2));
   ```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests fail after changes | Run `pnpm build` before `pnpm test` |
| Type errors | Check `packages/types` for type definitions |
| Shared code changes | Rebuild dependent packages |
| Snapshot mismatches | Review changes, update with `pnpm test -u` if correct |

## Important Notes

- Changes to `types` or `utils` packages may require rebuilding dependent packages
- Each package can be developed and tested independently
- The project uses Lerna for monorepo management
- Always verify no regressions before committing

## References

- Deparser testing docs: `packages/deparser/TESTING.md`
- Quoting rules: `packages/deparser/QUOTING-RULES.md`
- Deparser usage: `packages/deparser/DEPARSER_USAGE.md`
- PL/pgSQL deparser: `packages/plpgsql-deparser/AGENTS.md`
