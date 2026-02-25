---
name: angular
description: Modern Angular (v20+) expert with deep knowledge of Signals, Standalone Components, Zoneless applications, SSR/Hydration, and reactive patterns. Use PROACTIVELY for Angular development, component arch
category: Document Processing
source: antigravity
tags: [typescript, react, api, ai, template, document, image, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/angular
---


# Angular Expert

Master modern Angular development with Signals, Standalone Components, Zoneless applications, SSR/Hydration, and the latest reactive patterns.

## When to Use This Skill

- Building new Angular applications (v20+)
- Implementing Signals-based reactive patterns
- Creating Standalone Components and migrating from NgModules
- Configuring Zoneless Angular applications
- Implementing SSR, prerendering, and hydration
- Optimizing Angular performance
- Adopting modern Angular patterns and best practices

## Do Not Use This Skill When

- Migrating from AngularJS (1.x) → use `angular-migration` skill
- Working with legacy Angular apps that cannot upgrade
- General TypeScript issues → use `typescript-expert` skill

## Instructions

1. Assess the Angular version and project structure
2. Apply modern patterns (Signals, Standalone, Zoneless)
3. Implement with proper typing and reactivity
4. Validate with build and tests

## Safety

- Always test changes in development before production
- Gradual migration for existing apps (don't big-bang refactor)
- Keep backward compatibility during transitions

---

## Angular Version Timeline

| Version        | Release | Key Features                                           |
| -------------- | ------- | ------------------------------------------------------ |
| **Angular 20** | Q2 2025 | Signals stable, Zoneless stable, Incremental hydration |
| **Angular 21** | Q4 2025 | Signals-first default, Enhanced SSR                    |
| **Angular 22** | Q2 2026 | Signal Forms, Selectorless components                  |

---

## 1. Signals: The New Reactive Primitive

Signals are Angular's fine-grained reactivity system, replacing zone.js-based change detection.

### Core Concepts

```typescript
import { signal, computed, effect } from "@angular/core";

// Writable signal
const count = signal(0);

// Read value
console.log(count()); // 0

// Update value
count.set(5); // Direct set
count.update((v) => v + 1); // Functional update

// Computed (derived) signal
const doubled = computed(() => count() * 2);

// Effect (side effects)
effect(() => {
  console.log(`Count changed to: ${count()}`);
});
```

### Signal-Based Inputs and Outputs

```typescript
import { Component, input, output, model } from "@angular/core";

@Component({
  selector: "app-user-card",
  standalone: true,
  template: `
    <div class="card">
      <h3>{{ name() }}</h3>
      <span>{{ role() }}</span>
      <button (click)="select.emit(id())">Select</button>
    </div>
  `,
})
export class UserCardComponent {
  // Signal inputs (read-only)
  id = input.required<string>();
  name = input.required<string>();
  role = input<string>("User"); // With default

  // Output
  select = output<string>();

  // Two-way binding (model)
  isSelected = model(false);
}

// Usage:
// <app-user-card [id]="'123'" [name]="'John'" [(isSelected)]="selected" />
```

### Signal Queries (ViewChild/ContentChild)

```typescript
import {
  Component,
  viewChild,
  viewChildren,
  contentChild,
} from "@angular/core";

@Component({
  selector: "app-container",
  standalone: true,
  template: `
    <input #searchInput />
    <app-item *ngFor="let item of items()" />
  `,
})
export class ContainerComponent {
  // Signal-based queries
  searchInput = viewChild<ElementRef>("searchInput");
  items = viewChildren(ItemComponent);
  projectedContent = contentChild(HeaderDirective);

  focusSearch() {
    this.searchInput()?.nativeElement.focus();
  }
}
```

### When to Use Signals vs RxJS

| Use Case                | Signals         | RxJS                             |
| ----------------------- | --------------- | -------------------------------- |
| Local component state   | ✅ Preferred    | Overkill                         |
| Derived/computed values | ✅ `computed()` | `combineLatest` works            |
| Side effects            | ✅ `effect()`   | `tap` operator                   |
| HTTP requests           | ❌              | ✅ HttpClient returns Observable |
| Event streams           | ❌              | ✅ `fromEvent`, operators        |
| Complex async flows     | ❌              | ✅ `switchMap`, `mergeMap`       |

---

## 2. Standalone Components

Standalone components are self-contained and don't require NgModule declarations.

### Creating Standalone Components

```typescript
import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RouterLink } from "@angular/router";

@Component({
  selector: "app-header",
  standalone: true,
  imports: [CommonModule, RouterLink], // Direct imports
  template: `
    <header>
      <a routerLink="/">Home</a>
      <a routerLink="/about">About</a>
    </header>
  `,
})
export class HeaderComponent {}
```

### Bootstrapping Without NgModule

```typescript
// main.ts
import { bootstrapApplication } from "@angular/platform-browser";
import { provideRouter } from "@angular/router";
import { provideHttpClient } from "@angular/common/http";
import { AppComponent
