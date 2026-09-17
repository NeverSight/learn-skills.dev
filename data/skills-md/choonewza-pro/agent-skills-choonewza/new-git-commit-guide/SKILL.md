---
name: new-git-commit-guide
description: >
  Use this skill when committing code, writing commit messages, or reviewing
  git history in this Next.js project. Triggers on: "commit this", "write a
  commit message", "what should my commit say", "git commit", or any request
  to stage and commit changes. Provides project-specific conventional commit
  format, Thai-language comment conventions, and scope rules matched to this
  codebase's structure.
metadata:
  author: choonewza@gmail.com
  version: "1.0.0"
---

# Git Commit Guidelines

## Commit Message Format

```
<type>(<scope>): <subject in Thai or English>

[optional body]
```

## Types

| Type       | When to use                                         |
|------------|-----------------------------------------------------|
| `feat`     | New feature or page added                           |
| `fix`      | Bug fix                                             |
| `refactor` | Code restructure without behavior change            |
| `style`    | UI/CSS changes only (no logic change)               |
| `chore`    | Config, deps, tooling (prisma generate, etc.)       |
| `docs`     | Documentation or comment changes                    |
| `perf`     | Performance improvement                             |

## Scopes Matched to This Project

| Scope         | Maps to                                          |
|---------------|--------------------------------------------------|
| `auth`        | `src/lib/auth.ts`, `src/lib/auth-client.ts`, `(auth)/` routes |
| `product`     | `(front)/product/`, `app-product-card.tsx`      |
| `cart`        | `src/lib/cart-store.ts`, cart components         |
| `course`      | `(front)/course/`, `src/services/course-service.ts` |
| `contact`     | `(front)/contact/`, `src/app/api/contact/`       |
| `prisma`      | `prisma/schema.prisma`, `src/lib/prisma.ts`      |
| `ui`          | `src/components/ui/`, `src/components/`          |
| `layout`      | `(front)/layout.tsx`, `(auth)/layout.tsx`        |
| `api`         | `src/app/api/`                                   |
| `config`      | `next.config.ts`, `prisma.config.ts`, `.env`     |

## Subject Rules

- ใช้อังกฤษเท่านั้น
- ประโยคสั้นๆ ไม่เกิน 72 ตัวอักษร
- ไม่ต้องมี period ท้ายประโยค
- ใช้ present tense: "add", "fix", "update" ไม่ใช่ "added", "fixed"

## Examples

```
feat(product): add product detail page
fix(cart): fix totalPrice calculation when qty is 0
chore(prisma): regenerate Prisma client after schema changes
style(ui): update badge color in hero component
refactor(auth): extract signIn logic from page component
feat(api): add GET /api/products endpoint with pagination
fix(contact): prevent XSS in email HTML template
```

## Gotchas

- ห้าม commit ไฟล์ `.env` — มี `BETTER_AUTH_SECRET` และ `DATABASE_URL`
- ไฟล์ `generated/prisma/` ถูก gitignore — ไม่ต้อง stage
- ถ้าแก้ schema แล้วต้อง `npx prisma generate` ก่อน commit ตัว schema
- ไม่ใช้ `--no-verify` เพื่อข้าม hook โดยไม่มีเหตุผล

## Checklist Before Committing

- [ ] ไม่มีไฟล์ `.env` หรือ secret ใน staging area
- [ ] `npm run lint` ผ่านโดยไม่มี error
- [ ] Type ใหม่อยู่ใน `src/types/` ไม่ใช่ inline ใน component
- [ ] ไฟล์ชื่อ kebab-case เช่น `product-service.ts`
