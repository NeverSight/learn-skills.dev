---
name: inquirerer-cli-building
description: Build interactive CLI tools with inquirerer. Use when asked to "create a CLI", "build a command-line tool", "add prompts", "create interactive prompts", or when building any CLI application in a Constructive project.
compatibility: inquirerer, Node.js 18+, TypeScript
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Building CLI Tools with inquirerer

A comprehensive guide to building interactive command-line interfaces using inquirerer, the TypeScript-first CLI library used across Constructive projects.

## When to Apply

Use this skill when:
- Creating a new CLI application
- Adding interactive prompts to an existing tool
- Building project scaffolding or setup wizards
- Creating configuration builders
- Implementing any command-line interface in a Constructive project

## Installation

```bash
pnpm add inquirerer
```

## Quick Start

```typescript
import { Inquirerer } from 'inquirerer';

const prompter = new Inquirerer();

const answers = await prompter.prompt({}, [
  {
    type: 'text',
    name: 'projectName',
    message: 'What is your project name?',
    required: true
  },
  {
    type: 'confirm',
    name: 'useTypeScript',
    message: 'Use TypeScript?',
    default: true
  }
]);

console.log(answers);
prompter.close();
```

## Question Types

inquirerer supports six question types:

### Text Question

Collect string input:

```typescript
{
  type: 'text',
  name: 'username',
  message: 'Enter your username',
  required: true,
  pattern: '^[a-z0-9_]+$',  // Regex validation
  default: 'user'
}
```

### Number Question

Collect numeric input:

```typescript
{
  type: 'number',
  name: 'port',
  message: 'Server port?',
  default: 3000,
  validate: (port) => port > 0 && port < 65536
}
```

### Confirm Question

Yes/no questions:

```typescript
{
  type: 'confirm',
  name: 'proceed',
  message: 'Continue with installation?',
  default: true
}
```

### List Question

Select one option (no search):

```typescript
{
  type: 'list',
  name: 'license',
  message: 'Choose a license',
  options: ['MIT', 'Apache-2.0', 'GPL-3.0'],
  default: 'MIT',
  maxDisplayLines: 5
}
```

### Autocomplete Question

Select with fuzzy search:

```typescript
{
  type: 'autocomplete',
  name: 'framework',
  message: 'Choose a framework',
  options: [
    { name: 'React', value: 'react' },
    { name: 'Vue.js', value: 'vue' },
    { name: 'Angular', value: 'angular' }
  ],
  allowCustomOptions: true,
  maxDisplayLines: 8
}
```

### Checkbox Question

Multi-select with search:

```typescript
{
  type: 'checkbox',
  name: 'features',
  message: 'Select features',
  options: ['Auth', 'Database', 'API', 'Testing'],
  default: ['Auth', 'API'],
  returnFullResults: false,  // Only return selected items
  required: true
}
```

## Question Properties

All questions support these base properties:

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Property name in result object |
| `type` | string | Question type |
| `message` | string | Prompt message to display |
| `default` | any | Default value |
| `required` | boolean | Whether input is required |
| `validate` | function | Custom validation function |
| `sanitize` | function | Transform input before storing |
| `pattern` | string | Regex pattern for validation |
| `when` | function | Conditional display |
| `dependsOn` | string[] | Question dependencies |
| `_` | boolean | Mark as positional argument |
| `alias` | string/string[] | Short flag aliases |
| `defaultFrom` | string | Dynamic default from resolver |
| `setFrom` | string | Auto-set value from resolver |

## Validation

### Pattern Validation

```typescript
{
  type: 'text',
  name: 'email',
  message: 'Enter email',
  pattern: '^[^@]+@[^@]+\\.[^@]+$'
}
```

### Custom Validation

```typescript
{
  type: 'text',
  name: 'password',
  message: 'Enter password',
  validate: (input) => {
    if (input.length < 8) {
      return { success: false, reason: 'Must be at least 8 characters' };
    }
    return { success: true };
  }
}
```

### Sanitization

```typescript
{
  type: 'text',
  name: 'tags',
  message: 'Enter tags (comma-separated)',
  sanitize: (input) => input.split(',').map(t => t.trim())
}
```

## Conditional Questions

Show questions based on previous answers:

```typescript
const questions = [
  {
    type: 'confirm',
    name: 'useDatabase',
    message: 'Need a database?',
    default: false
  },
  {
    type: 'list',
    name: 'database',
    message: 'Which database?',
    options: ['PostgreSQL', 'MySQL', 'SQLite'],
    when: (answers) => answers.useDatabase === true
  }
];
```

## Question Dependencies

Ensure questions appear in correct order:

```typescript
[
  {
    type: 'checkbox',
    name: 'services',
    message: 'Select services',
    options: ['Auth', 'Storage', 'Functions']
  },
  {
    type: 'text',
    name: 'authProvider',
    message: 'Auth provider?',
    dependsOn: ['services'],
    when: (answers) => answers.services?.includes('Auth')
  }
]
```

## Positional Arguments

Allow values without flags using `_: true`:

```typescript
const questions = [
  { _: true, name: 'source', type: 'text', message: 'Source file' },
  { _: true, name: 'dest', type: 'text', message: 'Destination' }
];

// Users can run: mycli input.txt output.txt
// Instead of: mycli --source input.txt --dest output.txt
```

## Aliases

Define short flags:

```typescript
{
  name: 'workspace',
  type: 'confirm',
  alias: 'w',  // or ['w', 'ws'] for multiple
  message: 'Create workspace?'
}

// Users can run: mycli -w
// Instead of: mycli --workspace
```

## Dynamic Defaults with Resolvers

Auto-populate defaults from git, npm, or custom sources:

```typescript
const questions = [
  {
    type: 'text',
    name: 'author',
    message: 'Author name?',
    defaultFrom: 'git.user.name'  // Auto-fills from git config
  },
  {
    type: 'text',
    name: 'email',
    message: 'Email?',
    defaultFrom: 'git.user.email'
  },
  {
    type: 'text',
    name: 'year',
    message: 'Copyright year?',
    defaultFrom: 'date.year'
  }
];
```

### Built-in Resolvers

| Resolver | Description |
|----------|-------------|
| `git.user.name` | Git global user name |
| `git.user.email` | Git global user email |
| `npm.whoami` | Logged in npm user |
| `date.year` | Current year |
| `date.month` | Current month |
| `date.day` | Current day |
| `date.iso` | ISO date (YYYY-MM-DD) |
| `workspace.name` | Package name from nearest package.json |
| `workspace.license` | License from package.json |
| `workspace.author` | Author from package.json |

### Custom Resolvers

```typescript
import { registerDefaultResolver } from 'inquirerer';

registerDefaultResolver('cwd.name', () => {
  return process.cwd().split('/').pop();
});

// Use in questions
{
  type: 'text',
  name: 'projectName',
  defaultFrom: 'cwd.name'
}
```

### setFrom vs defaultFrom

- `defaultFrom`: Sets as default, user can override
- `setFrom`: Auto-sets value, skips prompt entirely

```typescript
{
  type: 'text',
  name: 'createdAt',
  setFrom: 'date.iso'  // Auto-set, no prompt shown
}
```

## CLI Class

For complete CLI applications with argument parsing:

```typescript
import { CLI, CommandHandler, CLIOptions } from 'inquirerer';

const handler: CommandHandler = async (argv, prompter, options) => {
  const answers = await prompter.prompt(argv, [
    { type: 'text', name: 'name', message: 'Name?', required: true }
  ]);
  console.log('Hello,', answers.name);
};

const options: Partial<CLIOptions> = {
  version: 'myapp@1.0.0',
  minimistOpts: {
    alias: { v: 'version', h: 'help' }
  }
};

const cli = new CLI(handler, options);
await cli.run();
```

## CLI Utilities

inquirerer provides utilities for building CLIs:

```typescript
import { 
  parseArgv,           // Parse command-line arguments
  extractFirst,        // Extract subcommand
  getPackageVersion,   // Get version from package.json
  cliExitWithError     // Exit with error message
} from 'inquirerer';

const argv = parseArgv(process.argv);
const { first: command, newArgv } = extractFirst(argv);

switch (command) {
  case 'init':
    await handleInit(newArgv);
    break;
  case 'build':
    await handleBuild(newArgv);
    break;
  default:
    console.log('Unknown command');
}
```

## UI Components

### Spinner

```typescript
import { createSpinner } from 'inquirerer';

const spinner = createSpinner('Loading...');
spinner.start();
await doWork();
spinner.succeed('Done!');
// Or: spinner.fail('Failed'), spinner.warn('Warning')
```

### Progress Bar

```typescript
import { createProgress } from 'inquirerer';

const progress = createProgress('Installing');
progress.start();
for (let i = 0; i < items.length; i++) {
  await processItem(items[i]);
  progress.update((i + 1) / items.length);
}
progress.complete('Installed');
```

### Streaming Text

```typescript
import { createStream } from 'inquirerer';

const stream = createStream({ showCursor: true });
stream.start();
for await (const token of llmResponse) {
  stream.append(token);
}
stream.done();
```

## Non-Interactive Mode

For CI/CD environments:

```typescript
const prompter = new Inquirerer({
  noTty: true,      // Disable interactive mode
  useDefaults: true // Use defaults without prompting
});
```

## Complete Example

```typescript
import { Inquirerer, Question, parseArgv } from 'inquirerer';

interface ProjectConfig {
  name: string;
  description: string;
  typescript: boolean;
  features: string[];
}

const argv = parseArgv(process.argv);
const prompter = new Inquirerer();

const questions: Question[] = [
  {
    _: true,
    type: 'text',
    name: 'name',
    message: 'Project name',
    required: true,
    pattern: '^[a-z0-9-]+$',
    defaultFrom: 'cwd.name'
  },
  {
    type: 'text',
    name: 'description',
    message: 'Description',
    default: 'My awesome project'
  },
  {
    type: 'confirm',
    name: 'typescript',
    alias: 'ts',
    message: 'Use TypeScript?',
    default: true
  },
  {
    type: 'checkbox',
    name: 'features',
    message: 'Select features',
    options: ['ESLint', 'Prettier', 'Jest', 'Husky'],
    default: ['ESLint', 'Prettier']
  }
];

const config = await prompter.prompt<ProjectConfig>(argv, questions);
console.log('Creating project:', config);
prompter.close();
```

Run interactively or with CLI args:

```bash
# Interactive
node setup.js

# With args
node setup.js my-project --ts --features ESLint,Jest
```

## Best Practices

1. **Always close the prompter** when done: `prompter.close()`
2. **Use TypeScript interfaces** for type-safe answers
3. **Provide defaults** for better UX
4. **Use `defaultFrom`** for dynamic defaults from git/npm
5. **Support non-interactive mode** for CI/CD
6. **Use positional arguments** for common inputs
7. **Add aliases** for frequently used flags
8. **Validate early** with patterns and custom validators

## References

- npm package: https://www.npmjs.com/package/inquirerer
- Related skill: `inquirerer-anti-patterns` for what NOT to do
- Related skill: `pnpm-workspace` for monorepo setup
