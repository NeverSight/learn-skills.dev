---
name: exome
description: This skill provides expertise in using Exome.js, a lightweight state management library for JavaScript applications. It covers creating and managing deeply nested stores, defining actions, integrating with UI frameworks like React, Vue, Svelte, and others, handling middleware, subscriptions, devtools, and best practices. Use this skill when assisting with state management in JS/TS projects, building reactive applications, or troubleshooting Exome-related code.
license: MIT
metadata:
  author: Mārcis Bergmanis
  version: "1.0"
  source: Exome.js official documentation and GitHub
---

# Exome.js State Management

Exome is a 1KB state manager for deeply nested states. State lives in classes extending `Exome`; methods are actions that mutate state and trigger reactive updates.

## Installation

```bash
npm install exome
```

Framework integrations are included — no extra packages needed.

## Core Concepts

### Store Definition

```ts
import { Exome } from 'exome';

export class CounterStore extends Exome {
  public count = 0;

  public increment() {
    this.count += 1;
  }

  public decrement() {
    this.count -= 1;
  }
}

export const counter = new CounterStore();
```

**Important:** Only regular methods are actions (trigger subscribers). Arrow function properties are **not** actions — they won't trigger updates even if they mutate state:

```ts
class MyStore extends Exome {
  public value = 0;

  // Action — triggers subscribers
  public update() {
    this.value += 1;
  }

  // NOT an action — does NOT trigger subscribers
  public silentUpdate = () => {
    this.value += 1;
  };
}
```

### Nested Stores

Child stores are separate `Exome` classes referenced as properties or array items. Circular references and shared instances are handled automatically.

```ts
import { Exome } from 'exome';

class TodoStore extends Exome {
  public completed = false;
  constructor(public content: string) { super(); }

  public toggle() {
    this.completed = !this.completed;
  }
}

class TodoListStore extends Exome {
  public todos: TodoStore[] = [];
  public filter: 'all' | 'active' | 'completed' = 'all';

  public addTodo(content: string) {
    this.todos.push(new TodoStore(content));
  }

  public setFilter(filter: TodoListStore['filter']) {
    this.filter = filter;
  }

  // Getters for computed values (don't trigger re-renders)
  public get filteredTodos() {
    if (this.filter === 'active') return this.todos.filter(t => !t.completed);
    if (this.filter === 'completed') return this.todos.filter(t => t.completed);
    return this.todos;
  }
}
```

### Framework Integration

General pattern: import the framework-specific hook (e.g. `useStore` from `exome/react`), pass a store instance, and get reactive state + bound actions.

See framework-specific guides:
[React/Preact](references/react.md) | [Vue](references/vue.md) | [Svelte](references/svelte.md) | [Solid](references/solid.md) | [Lit](references/lit.md) | [Angular](references/angular.md) | [RxJS](references/rxjs.md) | [Vanilla JS](references/vanilla.md)

## Middleware & DevTools

```ts
import { addMiddleware } from 'exome';
import { exomeReduxDevtools } from 'exome/devtools';

// Enable Redux DevTools in development
if (process.env.NODE_ENV === 'development') {
  addMiddleware(exomeReduxDevtools({ name: 'My App' }));
}
```

Hook into specific actions:

```ts
import { onAction } from 'exome';

onAction(CounterStore, 'increment', (instance) => {
  console.log('incremented to', instance.count);
}, 'after');
```

## Subscriptions

```ts
import { subscribe } from 'exome';

const unsubscribe = subscribe(counter, () => {
  console.log('counter changed:', counter.count);
});
```

## State Snapshots

```ts
import { saveState, loadState, registerLoadable } from 'exome';

// Register store classes for deserialization
registerLoadable({ CounterStore });

const snapshot = saveState(counter);    // JSON string
loadState(newCounter, snapshot);        // Restore state
```

## Best Practices

- One store per file, named `*.store.ts`, class suffixed with `Store`
- Keep business logic in actions; components only render and call actions
- Use getters for computed/derived values (they don't trigger re-renders)
- Keep stores small and nested for performance
- Async actions return promises; Exome handles them natively
- Changes to shared store instances propagate to all references automatically
- Hooks/subscriptions handle cleanup automatically

## Testing

- Use `exome/jest` (or `exome/vitest`) for store snapshot testing
- Use `GhostExome` to create mock store instances
- Test actions by calling methods and asserting state changes
