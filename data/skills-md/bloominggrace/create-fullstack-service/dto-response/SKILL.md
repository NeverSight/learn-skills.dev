---
name: dto-response
description: Use when creating or modifying DTO files in the `dto/` folder.
---

# DTO and Response Class Guide

Use this skill when creating or modifying DTO files in the `dto/` folder.

## Input DTO (Request)

```typescript
import { IsDateString, IsEnum, IsNotEmpty, IsOptional, IsString, Length } from 'class-validator';
import { IsE164 } from 'src/app.utils';

import { EntityEnum } from '../entity.enums';

export class CreateEntityDto {
  @IsNotEmpty()
  @IsString()
  requiredField!: string;

  @IsOptional()
  @IsString()
  @Length(1, 30)
  optionalField?: string;

  @IsOptional()
  @IsDateString()
  dateField?: string;

  @IsOptional()
  @IsEnum(EntityEnum)
  enumField?: EntityEnum;
}
```

### Input DTO Rules

1. **Use class-validator decorators**
   - `@IsNotEmpty()`: Required fields
   - `@IsOptional()`: Optional fields
   - `@IsString()`, `@IsNumber()`, `@IsBoolean()`: Type validation
   - `@IsEnum()`: Enum value validation
   - `@Length()`: String length limits
   - `@IsDateString()`: ISO 8601 date strings

2. **Field Declaration**
   - Required fields: `!` (definite assignment assertion)
   - Optional fields: `?` (optional)

3. **Custom Decorators**
   - Phone numbers: `@IsE164()` (E.164 format validation)
   - Define additional decorators in `app.utils.ts` as needed

4. **Naming Conventions**
   - Find: `Find{Entity}Dto`
   - Create: `Create{Entity}Dto`
   - Update: `Update{Entity}Dto`
   - Other: `{Action}{Entity}Dto`

## Output Response Class

```typescript
import { Expose } from 'class-transformer';

import { EntityEnum } from '../entity.enums';

export class FindEntityRes {
  @Expose()
  id!: string;

  @Expose()
  name!: string;

  @Expose()
  enumField!: EntityEnum;

  @Expose()
  createdAt!: Date;
}
```

### Output Response Rules

1. **@Expose() decorator is required**
   - Use `@Expose()` on all fields to expose
   - Works with `excludeExtraneousValues: true` option

2. **Naming Conventions**
   - Find: `Find{Entity}Res`
   - Create: `Create{Entity}Res`
   - Update: `Update{Entity}Res`
   - Other: `{Action}{Entity}Res`

3. **Entity → Response Transformation**

```typescript
import { mapTo } from '../app.utils';

// Usage in controller
return mapTo(FindEntityRes, entity);
```

## DTO/Response Same File Pattern

Define in same file when DTO and Response are closely related (e.g., update API):

```typescript
// update-entity.dto.ts
import { Expose } from 'class-transformer';
import { IsOptional, IsString, Length } from 'class-validator';

export class UpdateEntityDto {
  @IsOptional()
  @IsString()
  @Length(0, 30)
  name?: string;
}

export class UpdateEntityRes {
  @Expose()
  id!: string;

  @Expose()
  name!: string;
}
```

## mapTo Utility

Transformation function defined in `app.utils.ts`:

```typescript
import { type ClassConstructor, plainToInstance } from 'class-transformer';

export function mapTo<T, I>(type: ClassConstructor<T>, instance: I): T {
  return plainToInstance(type, instance, {
    excludeExtraneousValues: true,
  });
}
```

## Custom Validator Pattern

```typescript
import { applyDecorators } from '@nestjs/common';
import { Matches } from 'class-validator';

export function IsE164(): PropertyDecorator {
  return applyDecorators(
    Matches(/^\+[1-9]\d{1,14}$/, {
      message: '전화번호는 E.164을 준수해야 합니다.',
    }),
  );
}
```

## File Structure

```
src/{module}/dto/
├── create-{entity}.dto.ts
├── update-{entity}.dto.ts
├── find-{entity}.dto.ts
└── index.ts  # barrel export
```

### index.ts (Barrel Export)

```typescript
export * from './create-entity.dto';
export * from './update-entity.dto';
export * from './find-entity.dto';
```

## ValidationPipe Configuration

Global pipe setup in `main.ts`:

```typescript
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,           // Remove undefined fields
    forbidNonWhitelisted: true, // Error on undefined fields
    transform: true,           // Auto type transformation
  }),
);
```

