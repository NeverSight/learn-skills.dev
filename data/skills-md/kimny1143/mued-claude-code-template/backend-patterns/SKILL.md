---
name: backend-patterns
description: >
  バックエンドコード規約とパターン集。APIルート、Repository、バリデーション等の実装パターン。
  使用タイミング: (1) 新しいAPIルート作成時 (2) Repository実装時 (3) バリデーション設計時
  (4) エラーハンドリング実装時 (5) バックエンドのベストプラクティス確認時。
  トリガー例: 「APIルートを作って」「Repositoryパターンで」「バックエンドのパターン」
  「Zodでバリデーション」「エラーハンドリングのパターン」
---

# backend-patterns - バックエンドパターン集

バックエンドコード規約とパターン。

## 使い方

```
新しいAPIルートを作る時、このスキルを参照
```

---

## 1. APIルート構造

### 認証パターン（Next.js例）

```typescript
// 認証ミドルウェアを使用
import { withAuth } from '@/lib/middleware/with-auth';
import { apiSuccess, apiError } from '@/lib/api-response';

export const GET = withAuth(async ({ userId, request }) => {
  const data = await repository.findByUserId(userId);
  return apiSuccess({ data });
});

export const POST = withAuth(async ({ userId, request }) => {
  const body = await request.json();
  // バリデーション & 処理
  return apiSuccess({ created: result });
});
```

### Express.js例

```typescript
import { Router } from 'express';
import { authenticate } from '@/middleware/auth';
import { validate } from '@/middleware/validate';

const router = Router();

router.get('/', authenticate, async (req, res) => {
  const data = await repository.findByUserId(req.user.id);
  res.json({ success: true, data });
});

router.post('/', authenticate, validate(createSchema), async (req, res) => {
  const result = await repository.create(req.body);
  res.status(201).json({ success: true, data: result });
});
```

---

## 2. レスポンス形式

### 統一レスポンス

```typescript
// lib/api-response.ts
export function apiSuccess<T>(data: T, options?: { status?: number }) {
  return Response.json(
    { success: true, data, timestamp: new Date().toISOString() },
    { status: options?.status ?? 200 }
  );
}

export function apiError(message: string, options?: { status?: number; code?: string }) {
  return Response.json(
    { success: false, error: message, code: options?.code, timestamp: new Date().toISOString() },
    { status: options?.status ?? 400 }
  );
}
```

### レスポンス形式

```json
// 成功
{
  "success": true,
  "data": { ... },
  "timestamp": "2026-01-19T12:00:00.000Z"
}

// エラー
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2026-01-19T12:00:00.000Z"
}
```

---

## 3. バリデーション

### Zodスキーマ

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email('Invalid email'),
  name: z.string().min(1, 'Name is required').max(100),
  role: z.enum(['user', 'admin']).optional(),
});

// APIルートで使用
const validation = createUserSchema.safeParse(body);
if (!validation.success) {
  return apiError('Invalid input', { status: 400 });
}
const { email, name, role } = validation.data;
```

### 共通スキーマ

```typescript
// UUID
const idSchema = z.string().uuid('Invalid ID format');

// ページネーション
const paginationSchema = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(20),
});
```

---

## 4. Repository パターン

### 基本構造

```typescript
// lib/repositories/user.repository.ts
import { db } from '@/db';
import { users } from '@/db/schema';
import { eq } from 'drizzle-orm';

export interface CreateUserInput {
  email: string;
  name: string;
}

export const userRepository = {
  async create(input: CreateUserInput) {
    const [result] = await db.insert(users).values(input).returning();
    return result;
  },

  async findById(id: string) {
    const [result] = await db
      .select()
      .from(users)
      .where(eq(users.id, id))
      .limit(1);
    return result ?? null;
  },

  async findByEmail(email: string) {
    const [result] = await db
      .select()
      .from(users)
      .where(eq(users.email, email))
      .limit(1);
    return result ?? null;
  },

  async update(id: string, input: Partial<CreateUserInput>) {
    const [result] = await db
      .update(users)
      .set({ ...input, updatedAt: new Date() })
      .where(eq(users.id, id))
      .returning();
    return result;
  },

  async delete(id: string) {
    await db.delete(users).where(eq(users.id, id));
  },
};
```

---

## 5. エラーハンドリング

```typescript
export const POST = withAuth(async ({ userId, request }) => {
  try {
    const body = await request.json();
    const result = await repository.create(body);
    return apiSuccess({ result });
  } catch (error) {
    console.error('[API] Error:', error);

    if (error instanceof z.ZodError) {
      return apiError('Validation failed', { status: 400 });
    }

    if (error instanceof Error && error.message.includes('unique')) {
      return apiError('Already exists', { status: 409 });
    }

    return apiError('Internal server error', { status: 500 });
  }
});
```

---

## 6. チェックリスト

新しいAPIルート作成時:

- [ ] 認証ミドルウェア適用
- [ ] リクエストバリデーション（Zod）
- [ ] 統一レスポンス形式使用
- [ ] エラーハンドリング（try-catch）
- [ ] 認可チェック（リソース所有者確認）
- [ ] ログ出力

---

## 7. アンチパターン

```typescript
// ❌ 認証なし
export async function GET(request: Request) {
  const data = await db.select().from(users);
  return Response.json(data);
}

// ❌ バリデーションなし
const { email } = await request.json();
await db.insert(users).values({ email });

// ❌ エラー握りつぶし
try {
  await riskyOperation();
} catch (e) {
  // 何もしない
}
```
