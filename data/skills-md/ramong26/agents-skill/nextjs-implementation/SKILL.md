---
name: nextjs-implementation
description: This skill should be used when the user asks to implement, add, or scaffold a new page, feature, or UI slice in a Next.js (App Router) frontend — e.g. "새 페이지 만들어줘", "게시글 목록 화면 구현해줘", "이 API 연결하는 화면 만들어줘", "add a new page/feature to the Next.js app". It generates app/page/widgets/entities/shared files following Feature-Sliced Design layering with TanStack Query. Do not use for non-Next.js frontends, backend work, or simple styling tweaks.
---

# Next.js (App Router) Feature Implementation

Next.js App Router 프론트엔드에 Feature-Sliced Design(FSD) 레이어를 따라 새 화면/기능을 구현한다.

## 적용 전 확인

- 대상 레포에 이미 다른 레이어 구조가 있으면 이 스킬의 템플릿보다 그것을 우선한다.
- 기존 슬라이스(예: 같은 레포의 다른 기능)가 있으면 그 파일을 먼저 읽고 그대로 따라간다. 이 문서는 참고용 기본값이지 절대 규칙이 아니다.

## 레이어 구조

```text
app/<route>/page.tsx        # 라우팅만 담당, 로직 없이 page 레이어를 렌더링만 함
page/<slice>/
├── index.ts                # 공개 API만 re-export
├── ui/<Slice>Page.tsx       # 실제 화면 컴포넌트
└── model/                   # 이 화면 전용 상태·목업·유틸
widgets/<widget>/
├── index.ts
├── ui/<Widget>.tsx
└── model/
entities/<entity>/
├── index.ts                 # api 등 공개할 것만 re-export
├── api/<entity>-api.ts       # ky로 raw fetch 함수
├── api/use<Action><Entity>Query.ts  # TanStack Query queryOptions 팩토리
└── model/<entity>-type.ts    # 응답 타입
shared/
├── ui/        # shadcn 스타일 프리미티브, index.ts로 barrel export
├── lib/       # cn() 등 순수 유틸
└── constants/ # queryKey.ts, route.ts 등 전역 상수
```

## 임포트 경계 (FSD)

- 각 슬라이스는 `index.ts`로 노출한 것만 다른 슬라이스에서 가져다 쓴다. `@/entities/post/api/posts-api`처럼 내부 경로로 직접 들어가지 않고 `@/entities/post`로 가져온다.
- `app/<route>/page.tsx`는 `page/<slice>`의 컴포넌트를 렌더링만 하고 데이터 로직을 직접 두지 않는다.
- 경로 별칭은 `@/*` → 레포 루트.

## entities (API + 타입)

```ts
// entities/<entity>/api/<entity>-api.ts
import ky from 'ky';
import type { <Entity>ListRes } from '../model/<entity>-type';

export const get<Entity>List = async (): Promise<<Entity>ListRes[]> => {
  return ky.get('/api/<entity>/list', { searchParams: { page: 1, limit: 10 } }).json<<Entity>ListRes[]>();
};
```

```ts
// entities/<entity>/api/useGet<Entity>ListQuery.ts
import { queryKeys } from '@/shared/constants/queryKey';
import { get<Entity>List } from './<entity>-api';

export const get<Entity>ListQuery = () => ({
  queryKey: queryKeys.<entity>s.lists(),
  queryFn: get<Entity>List,
});
```

- 새 엔티티를 추가하면 `shared/constants/queryKey.ts`의 `queryKeys`에 `all`/`lists()` 키 팩토리를 같은 패턴으로 추가한다.
- 응답 타입은 `entities/<entity>/model/<entity>-type.ts`에 인터페이스로 선언한다.
- `entities/<entity>/index.ts`는 다른 레이어가 실제로 쓰는 것만 re-export한다 (예: `export { get<Entity>List } from './api/<entity>-api';`).

## page / widgets (화면)

- 데이터는 컴포넌트에서 `useQuery(get<Entity>ListQuery())`로 가져온다.
- `page/<slice>/ui/<Slice>Page.tsx`가 실제 화면이고, `page/<slice>/index.ts`가 그것만 re-export한다.
- 재사용 가능한 화면 조각은 `widgets/`로 분리한다 (예: 카드 아이템, 헤더).
- 스타일은 Tailwind 유틸리티 클래스 + `shared/lib/cn()`으로 조합한다. 새 variant가 필요한 프리미티브는 `class-variance-authority`(`cva`)를 쓴다.

## app 라우트

```tsx
// app/(main)/<route>/page.tsx
import { <Slice>Page } from '@/page/<slice>';

export default function <Route>() {
  return <<Slice>Page />;
}
```

- 동적 라우트(`[id]`)는 Next.js 16 기준 `params`가 `Promise`이므로 `await`로 풀어서 사용한다.

## 데이터 페칭 클라이언트

- `app/provider/MainProvider.tsx`의 `QueryClientProvider` 설정을 그대로 재사용한다. 새 Provider를 추가로 만들지 않는다.
- 서버 컴포넌트에서 직접 fetch가 필요한 게 아니라면, 클라이언트 컴포넌트에서 TanStack Query로 처리하는 기존 패턴을 따른다.

## 결과

새로 만든 파일 목록(레이어별로 구분), `queryKey.ts`·`route.ts` 변경 여부, 실행한 검증(lint·build)을 정리해 보여준다.
