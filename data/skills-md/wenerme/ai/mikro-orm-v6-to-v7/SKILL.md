---
name: mikro-orm-v6-to-v7
description: Use when upgrading @mikro-orm packages from v6 to v7, fixing v7 runtime/type errors (decorator SyntaxError, persistAndFlush removed, nativeInsert not found), adapting knex to kysely or better-sqlite to new SQLite drivers, running MikroORM in Edge/Bun/node:sqlite environments, or choosing between defineEntity vs decorator entity definitions. Triggers on "mikro-orm v7", "persistAndFlush", "@mikro-orm/decorators", "@mikro-orm/sql", "defineEntity", "bun:sqlite mikro-orm".
---

# MikroORM v6 → v7 迁移指南

## 概述

MikroORM v7 是一次重大版本升级。核心变化：原生 ESM、knex→kysely、装饰器拆包、Node.js 22.17+/TypeScript 5.8+ 最低要求。本技能覆盖迁移的所有关键路径，避免常见陷阱。

## 环境要求

| 项目       | v6        | v7            |
|------------|-----------|---------------|
| Node.js    | 18+       | **22.17+**    |
| TypeScript | 5.0+      | **5.8+**      |
| 模块系统   | CJS/ESM   | **原生 ESM**  |

## 迁移步骤总览

### Step 1: 包替换

```bash
# 1. 替换核心包
pnpm remove @mikro-orm/knex
pnpm add @mikro-orm/sql

# 2. 安装装饰器包（如使用装饰器）
pnpm add @mikro-orm/decorators

# 3. SQLite 驱动选择（见 Edge-Ready 参考）
# better-sqlite3: pnpm add @mikro-orm/sqlite
# node:sqlite / bun:sqlite / D1: pnpm add @mikro-orm/sql kysely
```

### Step 2: Import 路径更新

```diff
- import { Entity, PrimaryKey, Property } from '@mikro-orm/core';
+ import { Entity, PrimaryKey, Property } from '@mikro-orm/decorators/legacy';
+ // 或 ES spec 装饰器:
+ // import { Entity, PrimaryKey, Property } from '@mikro-orm/decorators/es';

- import { ... } from '@mikro-orm/knex';
+ import { ... } from '@mikro-orm/sql';
```

关于 ES vs Legacy 装饰器的选择和配置，**必须阅读** [references/decorators.md](references/decorators.md)。

### Step 3: API 替换

```diff
- em.persistAndFlush(entity)
+ em.persist(entity).flush()

- em.removeAndFlush(entity)
+ em.remove(entity).flush()

- em.nativeInsert(Entity, data)
+ em.insert(Entity, data)

- em.getKnex()
+ em.getKysely()

- orm.getSchemaGenerator().createSchema()
+ orm.schema.create()

- em.find('User')
+ em.find(User)

- const orm = MikroORM.initSync({ ... })
+ const orm = new MikroORM({ ... })
```

完整 API 变更对照表见 [references/api-changes.md](references/api-changes.md)。

### Step 4: Entity 定义适配

v7 提供两种实体定义方式：

#### 方式 A: `defineEntity`（推荐，新项目）

```typescript
import { defineEntity, PrimaryKey, Property } from '@mikro-orm/core';

const UserEntity = defineEntity({
  class: class User {},
  tableName: 'user',
  properties: {
    id: p.uuid().primary(),
    name: p.string(),
    email: p.string().nullable(),
    createdAt: p.datetime().onCreate(() => new Date()),
  },
});
```

#### 方式 B: Legacy 装饰器（现有项目迁移）

```typescript
import { BaseEntity, type Opt } from '@mikro-orm/core';
import { Entity, PrimaryKey, Property } from '@mikro-orm/decorators/legacy';

@Entity({ tableName: 'user' })
export class User extends BaseEntity {
  @PrimaryKey({ type: 'uuid', onCreate: () => crypto.randomUUID() })
  id!: string & Opt;

  @Property({ type: 'text' })
  name!: string;

  @Property({ type: 'text', nullable: true })
  email?: string;
}
```

两种方式的详细对比和场景建议见 [references/decorators.md](references/decorators.md)。

### Step 5: 默认值变更检查

| 配置项 | v6 默认 | v7 默认 | 影响 |
|--------|---------|---------|------|
| 加载策略 | `joined` | **`balanced`** | to-many 关系改为独立查询 |
| `forceUtcTimezone` | `false` | **`true`** | 现有非 UTC 数据会被错误解读 |
| 嵌入属性前缀 | `absolute` | **`relative`** | 嵌套嵌入列名可能变化 |
| `@Transactional` 传播 | `REQUIRES_NEW` | **`REQUIRED`** | 默认加入已有事务 |
| `processOnCreateHooksEarly` | `false` | **`true`** | `onCreate` 在 `em.create` 中立即执行 |

**关键**: 如果现有数据以本地时区存储，升级前必须决定是否迁移数据或显式设 `forceUtcTimezone: false`。

### Step 6: Edge/Bun/node:sqlite 适配

如需在 Edge Runtime、Bun 或使用 `node:sqlite` 运行 MikroORM，**必须阅读** [references/edge-ready-sqlite.md](references/edge-ready-sqlite.md)。

## 实体定义方式选择

```
需要实体定义？
  ├─ 新项目 / 无历史 decorator 代码 → defineEntity（类型推断更好）
  ├─ 现有项目迁移 / 大量 decorator 实体 → Legacy decorator
  └─ TC39 decorator 环境（Node 22.6+原生支持）→ ES spec decorator
```

## 常见错误快速定位

| 症状 | 原因 | 修复 |
|------|------|------|
| `Cannot find module '@mikro-orm/knex'` | 包重命名 | 替换为 `@mikro-orm/sql` |
| `persistAndFlush is not a function` | API 移除 | `em.persist(entity).flush()` |
| `nativeInsert is not a function` | 方法重命名 | `em.insert(Entity, data)` |
| `Decorator SyntaxError` (SWC/Vite) | 装饰器编译未配置 | 见 [decorators.md](references/decorators.md) |
| `Value for X.id is required` | `onCreate` 未配置 | PrimaryKey 加 `onCreate` |
| `TypedArray.prototype.join incompatible` | Blob clone 问题 | 见 [known-issues.md](references/known-issues.md) |
| `string reference not supported` | 字符串引用移除 | 改为类引用 `() => Entity` |
| Schema diff 出现意外变更 | 默认值变更 | 检查 Step 5 默认值表 |

更多已知问题和解决方案见 [references/known-issues.md](references/known-issues.md)。

## 迁移检查清单

- [ ] Node.js ≥ 22.17，TypeScript ≥ 5.8
- [ ] `@mikro-orm/knex` → `@mikro-orm/sql`
- [ ] 安装 `@mikro-orm/decorators`，更新 import
- [ ] 替换 `persistAndFlush` / `removeAndFlush`
- [ ] 替换字符串引用为类引用
- [ ] 更新 `SchemaGenerator` / `Migrator` / `Seeder` 方法名
- [ ] QueryBuilder `.execute()` / `.getResult()` 替代直接 await
- [ ] 更新 `driverOptions` 去掉 `connection` 嵌套
- [ ] 检查 `forceUtcTimezone` 对现有数据的影响
- [ ] 更新 Formula/Index/Check 回调签名（`quote` 辅助函数）
- [ ] 运行 `orm.schema.update({ diff: true })` 检查 schema 变更
- [ ] 运行 typecheck 和测试验证

## 参考文档

- [装饰器迁移: ES vs Legacy vs defineEntity](references/decorators.md)
- [Edge-Ready SQLite 配置](references/edge-ready-sqlite.md)
- [完整 API 变更对照表](references/api-changes.md)
- [已知问题与解决方案](references/known-issues.md)
