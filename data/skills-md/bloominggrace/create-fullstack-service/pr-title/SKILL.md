---
name: pr-title
description: Use when writing Pull Request titles or commit messages to follow the Korean action word convention.
---

# Pull Request Title Guide

Use this skill when creating PR titles or commit messages.

## Basic Format

```
{Subject} {Action}
```

- **Subject**: The target being modified (file, module, feature, library, etc.)
- **Action**: The type of change being made

## Subject Naming Rules

Choose the subject based on what is being modified:

| Target Type | Subject Example | Description |
|-------------|-----------------|-------------|
| Config file | TSConfig, ESLint, MikroORM | Use the official/common name of the tool |
| Module | JwtModule, CacheModule, UsersController | Use the class/module name |
| Feature | CI, E2E 테스트, Git Hooks | Use the feature name |
| Library | Lodash, Vitest, Turborepo | Use the library name |
| Domain | 사용자, 인증, OTP | Use Korean domain terms |

### Examples
- `tsconfig.ts` → **TSConfig**
- `eslint.config.mjs` → **ESLint**
- `mikro-orm.config.ts` → **MikroORM**
- `users.service.ts` → **사용자** or **UsersService**

## Action Types

| Action | Usage | Example |
|--------|-------|---------|
| 설정 | Initial setup or configuration | `JwtModule 설정` |
| 변경 | Modify existing configuration | `TSConfig 변경` |
| 수정 | Fix issues or errors | `ESLint 에러 수정` |
| 추가 | Add new features | `UsersController 테스트 추가` |
| 적용 | Apply new tools or patterns | `Turborepo 적용` |
| 구축 | Build infrastructure | `CI 구축` |
| 교체 | Replace with alternatives | `Lodash를 es-toolkit으로 교체` |
| 마이그레이션 | Migrate to new tools | `Jest에서 Vitest로 마이그레이션` |
| 표준화 | Standardize patterns | `응답 변환 방식 표준화` |
| 보강 | Strengthen/enhance | `사용자 수정 테스트 보강` |
| 향상 | Improve quality | `pre-push 로그 가독성 향상` |
| 제외 | Exclude from rules | `fixup 커밋 제목 길이 제한 제외` |
| 정의 | Define rules/specs | `Cursor 규칙 정의` |

## Good Examples

```
✅ TSConfig 경로 별칭 설정
✅ mise 환경 변수 설정
✅ ESLint 설정 수정
✅ JWT 환경 변수 이름 오타 수정
✅ Jest에서 Vitest로 마이그레이션
✅ Lodash를 es-toolkit으로 교체
✅ 사용자 수정 테스트 보강
✅ pre-push 로그 가독성 향상
```

## Bad Examples

```
❌ 설정 파일 수정 (too vague - what config?)
❌ 버그 수정 (too vague - what bug?)
❌ 테스트 추가 (too vague - what test?)
❌ Web 앱 TSConfig 설정 (unnecessary context - Vite implies Web)
```

## Tips

1. **Be specific**: The subject should clearly identify what was changed
2. **Use official names**: TSConfig (not tsconfig), ESLint (not eslint)
3. **Avoid redundancy**: Don't repeat context that can be inferred
4. **Keep it concise**: Title should be scannable at a glance
5. **Use Korean for actions**: 설정, 수정, 추가, etc.

## Related: Commit Message vs PR Title

- **Commit messages**: Can be more granular, multiple per PR
- **PR title**: Should summarize the overall change in one line

