---
name: m3-web-angular
description: Implement Material Design 3 in Angular using Angular Material (@angular/material) with first-class M3 support. Covers M3 theming via design tokens, SCSS mixins, CLI schematics, and component usage. Use this when building M3-styled Angular applications.
license: Apache-2.0
---

# Material Design 3 — Angular Material

## Overview

Angular Material (`@angular/material`) has first-class M3 support since v17.2+. The Angular team works closely with Google's Material team. Full M3 theming via design tokens, SCSS mixins, and CLI schematics.

**Keywords**: Material Design 3, M3, Angular, Angular Material, @angular/material, SCSS, design tokens, schematics

## When to Use

- Angular projects — this is the most official, well-integrated M3 implementation for any web framework
- Enterprise applications requiring official Google M3 support
- Projects using Angular CLI and schematics

## Install

```bash
ng add @angular/material
```

## Generate M3 Theme

```bash
ng generate @angular/material:m3-theme
```

## Theme Setup (SCSS)

```scss
@use '@angular/material' as mat;
@include mat.core();

$my-theme: mat.define-theme((
  color: (
    theme-type: light,
    primary: #6750A4,
    secondary: #625B71,
    tertiary: #7D5260,
  ),
));

$dark-theme: mat.define-theme((
  color: (
    theme-type: dark,
    primary: #6750A4,
    secondary: #625B71,
    tertiary: #7D5260,
  ),
));

:root {
  @include mat.all-component-themes($my-theme);
  color-scheme: light;
}

html.dark-theme {
  @include mat.all-component-colors($dark-theme);
  color-scheme: dark;
}
```

## Component Examples

### Buttons

```html
<button mat-raised-button color="primary">Filled</button>
<button mat-stroked-button>Outlined</button>
<button mat-button>Text</button>
<button mat-fab><mat-icon>add</mat-icon></button>
```

### Cards

```html
<mat-card appearance="raised">
  <mat-card-header>
    <mat-card-title>Title</mat-card-title>
  </mat-card-header>
  <mat-card-content>Content</mat-card-content>
  <mat-card-actions>
    <button mat-button>Action</button>
  </mat-card-actions>
</mat-card>
```

### Text Fields

```html
<mat-form-field appearance="outline">
  <mat-label>Email</mat-label>
  <input matInput type="email" />
</mat-form-field>

<mat-form-field appearance="fill">
  <mat-label>Name</mat-label>
  <input matInput />
</mat-form-field>
```

### Navigation

```html
<mat-toolbar color="primary">
  <span>My App</span>
</mat-toolbar>

<mat-tab-group>
  <mat-tab label="Home">Home content</mat-tab>
  <mat-tab label="Search">Search content</mat-tab>
</mat-tab-group>

<mat-sidenav-container>
  <mat-sidenav mode="side" opened>Navigation</mat-sidenav>
  <mat-sidenav-content>Main content</mat-sidenav-content>
</mat-sidenav-container>
```

### Dialogs

```html
<button mat-raised-button (click)="openDialog()">Open Dialog</button>
```

```typescript
import { MatDialog } from '@angular/material/dialog';

constructor(private dialog: MatDialog) {}

openDialog() {
  this.dialog.open(MyDialogComponent);
}
```

## Checklist

- [ ] M3 theme generated via `ng generate @angular/material:m3-theme`
- [ ] Primary, secondary, and tertiary colors defined
- [ ] Both light and dark theme variants configured
- [ ] SCSS mixins applied at root level
- [ ] Components use `color="primary"` binding for theming
- [ ] Typography uses M3 type scale via Angular Material's typography system

## Resources

- `m3-theme.scss` — Ready-to-use Angular Material M3 theme SCSS (orange palette, light + dark) included in this skill's directory. Copy into your project and customize.
- `material-theme-builder` skill — Generate a custom palette from any source color.
- Available palettes: `$red-palette`, `$green-palette`, `$blue-palette`, `$yellow-palette`, `$cyan-palette`, `$magenta-palette`, `$orange-palette`, `$chartreuse-palette`, `$spring-green-palette`, `$azure-palette`, `$violet-palette`, `$rose-palette`
- GitHub: https://github.com/angular/components
- Theming guide: https://material.angular.dev/guide/theming
- M3 migration: https://v17.material.angular.dev/guide/material-3
- Design tokens: https://konstantin-denerz.com/angular-material-3-theming-design-tokens-and-system-variables/
- Component catalog: https://material.angular.dev/components/categories
- SCSS API reference: https://github.com/angular/components/blob/main/src/material/_index.scss
