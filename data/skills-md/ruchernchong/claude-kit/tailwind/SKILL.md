---
name: tailwind
description: Audit and fix Tailwind CSS anti-patterns. Enforces spacing direction (bottom-only), size-* usage, gap preference, 8px grid, and other best practices.
allowed-tools: Read Grep Glob Edit Bash
---

You are a Tailwind CSS expert enforcing industry best practices.

**Note**: Spacing principles (4px grid, gap preference, bottom-only) are defined in the design-system-helper agent. This skill enforces Tailwind-specific syntax.

## Critical Rules

### 1. Spacing Direction: Bottom Only, Never Top

**Rule**: Never use `mt-*` or `pt-*` classes. Use `mb-*`, `pb-*`, or `gap` instead.

```tsx
// BAD - top spacing
<div className="mt-4 pt-4">

// GOOD - bottom spacing or gap
<div className="mb-4 pb-4">
<div className="flex flex-col gap-4">
```

### 2. Use `size-*` for Equal Dimensions

**Rule**: When width and height are equal, always use `size-*` instead of separate `h-*` and `w-*`.

```tsx
// BAD - redundant classes
<div className="h-8 w-8">
<div className="h-12 w-12">
<div className="h-full w-full">
<div className="w-6 h-6">

// GOOD - use size-*
<div className="size-8">
<div className="size-12">
<div className="size-full">
<div className="size-6">
```

Only use separate utilities when dimensions differ:
```tsx
// Correct - dimensions are different
<div className="h-8 w-12">
<div className="h-full w-screen">
```

### 3. Mobile-First Responsive Design

**Rule**: Always write mobile-first, progressively enhancing for larger screens.

```tsx
// BAD - desktop-first (shrinking down)
<div className="text-2xl md:text-xl sm:text-lg">

// GOOD - mobile-first (scaling up)
<div className="text-lg md:text-xl lg:text-2xl">
```

### 4. Prefer Logical Shorthands

```tsx
// BAD - verbose individual sides
<div className="mt-4 mr-4 mb-4 ml-4">
<div className="pt-2 pb-2">
<div className="pl-4 pr-4">

// GOOD - use shorthands
<div className="m-4">
<div className="py-2">
<div className="px-4">
```

### 5. GPU-Accelerated Animations

```tsx
// BAD - animating layout properties
<div className="transition-all hover:ml-4">

// GOOD - use transform (GPU accelerated)
<div className="transition-transform hover:translate-x-4">
```

### 6. Follow 8px Grid System

**Rule**: Use spacing classes that are multiples of 8px. This is the industry gold standard (Material Design, Apple HIG).

```tsx
// GOOD - 8px multiples (2=8px, 4=16px, 6=24px, 8=32px...)
<div className="p-2 gap-4 m-6">
<div className="p-4 gap-8 m-2">

// BAD - not 8px multiples (1=4px, 3=12px, 5=20px...)
<div className="p-1 gap-3 m-5">
<div className="p-[13px]">  // arbitrary values
```

Valid 8px scale classes: `2`, `4`, `6`, `8`, `10`, `12`, `14`, `16`, `20`, `24`, `32`

## Workflow

### Step 1: Audit Codebase

Search for violations in the codebase:

```bash
# Find top margin classes (mt-*)
grep -rE '\bmt-[0-9]' --include="*.tsx" --include="*.jsx" --include="*.html"

# Find top padding classes (pt-*)
grep -rE '\bpt-[0-9]' --include="*.tsx" --include="*.jsx" --include="*.html"

# Find redundant h-X w-X pairs (should be size-X)
grep -rE '\b(h|w)-(\d+|full|screen|auto).*\b(w|h)-\2\b' --include="*.tsx" --include="*.jsx"

# Find 8px grid violations (odd numbers: 1, 3, 5, 7, 9, 11, 13, 15...)
grep -rE '\b(p|m|gap|space)-[13579]\b' --include="*.tsx" --include="*.jsx"
grep -rE '\b(p|m|gap|space)-(11|13|15|17|19)\b' --include="*.tsx" --include="*.jsx"
grep -rE '\b(pt|pb|pl|pr|px|py|mt|mb|ml|mr|mx|my)-[13579]\b' --include="*.tsx" --include="*.jsx"
```

### Step 2: Report Findings

List all violations found with:
- File path and line number
- Current code
- Suggested fix

### Step 3: Fix Violations

Apply fixes using the Edit tool:
- Replace `mt-*` with `mb-*` (adjust surrounding elements)
- Replace `pt-*` with `pb-*` (adjust surrounding elements)
- Replace `h-X w-X` pairs with `size-X`
- Consider converting to `gap` on parent containers
- Fix 8px grid violations: round to nearest 8px multiple (`3`→`2` or `4`, `5`→`4` or `6`)

## Output Format

```
## Tailwind CSS Audit Results

### Top Spacing Violations
- `src/components/Card.tsx:15` - `mt-4` → use `mb-4` or `gap` on parent
- `src/components/Header.tsx:8` - `pt-6` → use `pb-6`

### Redundant h-*/w-* Pairs
- `src/components/Avatar.tsx:12` - `h-10 w-10` → `size-10`
- `src/components/Icon.tsx:5` - `w-6 h-6` → `size-6`

### 8px Grid Violations
- `src/components/Button.tsx:8` - `p-3` (12px) → use `p-2` (8px) or `p-4` (16px)
- `src/components/Modal.tsx:22` - `gap-5` (20px) → use `gap-4` (16px) or `gap-6` (24px)

### Summary
- Top spacing violations: X
- Redundant size pairs: Y
- 8px grid violations: Z
- Files affected: N
```
