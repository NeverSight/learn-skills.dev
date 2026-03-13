---
name: mikro-orm-entity
description: Use when creating or modifying MikroORM entity files in the `entities/` folder.
---

# MikroORM Entity Guide

Use this skill when creating or modifying MikroORM entity files (`*.entity.ts`).

## Basic Entity Structure

```typescript
import { Entity, PrimaryKey, Property, Unique } from '@mikro-orm/core';
import { uuidv7 } from 'uuidv7';

import { EntityEnum } from '../entity.enums';

@Entity()
export class EntityName {
  @PrimaryKey({ type: 'uuid' })
  id: string = uuidv7();

  @Property()
  @Unique()
  uniqueField!: string;

  @Property({ length: 30, nullable: true })
  optionalField?: string;

  @Property({ type: 'date', nullable: true })
  dateField?: Date;

  @Property({ type: 'string', nullable: true })
  enumField?: EntityEnum;

  @Property({ onCreate: () => new Date() })
  createdAt?: Date;

  @Property({ onCreate: () => new Date(), onUpdate: () => new Date() })
  updatedAt?: Date;
}
```

## Core Rules

### 1. Primary Key
- **Use UUID v7**: Use `uuidv7` package for time-ordered UUIDs
- Assign default value directly in class field (`= uuidv7()`)

### 2. Property Decorators
- Required fields: Use `!` (definite assignment assertion)
- Optional fields: Use `?` (optional) with `nullable: true` option
- String length limits: Use `length` option
- Date type: Explicitly specify `{ type: 'date' }`

### 3. Enum Fields
- Use `@Property({ type: 'string' })`
- Define enums in separate `.enums.ts` file

### 4. Timestamps
- `onCreate`: Auto-set on creation
- `onUpdate`: Auto-update on modification
- Both fields declared as optional (`?`)

### 5. Unique Constraints
- Place `@Unique()` decorator below `@Property()`

## Enum File Structure (*.enums.ts)

```typescript
export enum EntityStatus {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  DELETED = 'DELETED',
}

export enum EntityType {
  TYPE_A = 'TYPE_A',
  TYPE_B = 'TYPE_B',
}
```

- Values in uppercase SNAKE_CASE
- Keep key and value identical

## File Naming Conventions

- Entity file: `{entity-name}.entity.ts`
- Enum file: `{module-name}.enums.ts`
- Folder structure: `src/{module}/entities/`

