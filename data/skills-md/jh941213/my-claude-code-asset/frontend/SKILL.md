---
name: frontend
description: |
  빅테크 스타일(Stripe, Vercel, Apple) UI 개발. 플래닝 → 구현까지 한 번에.
  트리거: "프론트엔드", "UI 만들어", "페이지 만들어", "컴포넌트 만들어", "랜딩 페이지", "대시보드 UI"
  안티-트리거: "백엔드 API", "데이터베이스", "CLI 도구"
user-invocable: true
disable-model-invocation: false
context: fork
agent: frontend-developer
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# 프론트엔드 UI 개발

빅테크 스타일(Stripe, Vercel, Apple)의 프론트엔드 UI를 **플래닝 → 구현**까지 한 번에 진행합니다.

## 워크플로우

```
/frontend [요청사항]
    ↓
1. 디자인 규격 작성 (플래닝)
    ↓
2. 사용자 확인
    ↓
3. frontend-developer 에이전트로 구현
    ↓
4. 결과 검증
```

## Phase 1: 플래닝

### 디자인 스타일 선택
| 스타일 | 특징 | 적합한 용도 |
|--------|------|------------|
| **Stripe** | 그라데이션, 밝은 톤, 미묘한 애니메이션 | 결제, SaaS, 랜딩 |
| **Vercel** | 다크모드, 미니멀, 모노톤 | 개발자 도구 |
| **Apple** | 넓은 여백, 타이포 강조 | 제품 소개 |
| **Linear** | 다크, 보라색 악센트 | 생산성 앱 |
| **Notion** | 밝은 톤, 아이콘 활용 | 문서/협업 |

### 규격서 템플릿
```markdown
## [프로젝트명] 디자인 규격

### 스타일: [선택한 스타일]

### 컬러
- Primary: #[hex]
- Background: #[hex]
- Text: #[hex]
- Border: #[hex]
- Accent: #[hex]

### 타이포
- Display: [폰트] / [크기]
- Body: [폰트] / [크기]

### 컴포넌트
1. [컴포넌트1]: [설명]
2. [컴포넌트2]: [설명]

### 레이아웃
- Max width: [px]
- 주요 구조: [설명]
```

## Phase 2: 구현

`frontend-developer` 에이전트를 호출하여 구현합니다.

### 구현 순서
1. CSS 변수 (globals.css)
2. 유틸리티 (lib/utils.ts)
3. UI 컴포넌트 (components/ui/)
4. 레이아웃 (components/layout/)
5. 기능 컴포넌트
6. 페이지 조립
7. 애니메이션

### 필수 의존성
```bash
npm install tailwindcss @tailwindcss/typography
npm install clsx tailwind-merge
npm install framer-motion
npm install lucide-react
npx shadcn@latest init
```

## Phase 3: 검증

구현 완료 후:
- [ ] TypeScript 에러 없음
- [ ] 빌드 성공
- [ ] 반응형 확인
- [ ] 접근성 확인

## 사용 예시

```
/frontend 로그인 페이지 만들어줘. Vercel 스타일로, 이메일/비밀번호 입력 폼과 소셜 로그인 버튼 포함.
```

```
/frontend 대시보드 만들어줘. Stripe 스타일로, 사이드바 + 메인 콘텐츠 영역 + 차트 카드들.
```
