---
name: stitch-react
description: "Stitch 스크린을 React 컴포넌트 시스템으로 변환합니다 — 디자인 토큰 추출, 컴포넌트 분해, TypeScript 타입 생성, 자동 검증 포함. Triggers on: Stitch React, 컴포넌트 변환, React 변환, HTML to React. NOT for: 새 React 앱 생성, API 구현."
user-invocable: true
allowed-tools:
  - "stitch*:*"
  - "mcp__stitch*"
  - "Read"
  - "Write"
  - "Edit"
  - "Bash"
---

# Stitch to React Components

Stitch에서 생성된 HTML 스크린을 재사용 가능한 React 컴포넌트 시스템으로 변환합니다. 디자인 토큰 추출, 컴포넌트 분해, 자동 검증을 포함합니다.

## 개요

이 스킬은 Stitch의 정적 HTML 출력을 프로덕션 레디 React 컴포넌트로 변환합니다:

1. **디자인 토큰 추출**: 색상, 타이포그래피, 간격을 토큰으로 추출
2. **컴포넌트 분해**: HTML을 재사용 가능한 컴포넌트로 분리
3. **TypeScript 지원**: Props 타입 정의 자동 생성
4. **검증**: 생성된 컴포넌트의 문법 및 타입 검증

## 사전 요구사항

- Stitch MCP 서버 접근 권한
- Stitch 프로젝트와 생성된 스크린
- Node.js 환경 (React 프로젝트)
- `DESIGN.md` 파일 (선택, 토큰 일관성 향상)

## 변환 워크플로우

### Step 1: Stitch 스크린 가져오기

```bash
# Stitch MCP로 스크린 HTML 다운로드
[prefix]:get_screen 호출
→ htmlCode.downloadUrl에서 HTML 다운로드
→ source.html로 저장
```

### Step 2: 디자인 토큰 추출

Stitch HTML에서 Tailwind 클래스와 인라인 스타일을 분석하여 디자인 토큰을 추출합니다.

#### 색상 토큰

```typescript
// tokens/colors.ts
export const colors = {
  // Primary
  primary: {
    DEFAULT: '#0066FF',
    hover: '#0052CC',
    light: '#E6F0FF',
  },
  // Neutral
  neutral: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    // ...
    900: '#111827',
  },
  // Semantic
  success: '#10B981',
  error: '#EF4444',
  warning: '#F59E0B',
} as const;
```

#### 타이포그래피 토큰

```typescript
// tokens/typography.ts
export const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },
  fontSize: {
    xs: ['0.75rem', { lineHeight: '1rem' }],
    sm: ['0.875rem', { lineHeight: '1.25rem' }],
    base: ['1rem', { lineHeight: '1.5rem' }],
    lg: ['1.125rem', { lineHeight: '1.75rem' }],
    xl: ['1.25rem', { lineHeight: '1.75rem' }],
    '2xl': ['1.5rem', { lineHeight: '2rem' }],
    '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
  },
  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
} as const;
```

#### 간격 토큰

```typescript
// tokens/spacing.ts
export const spacing = {
  px: '1px',
  0: '0',
  0.5: '0.125rem',
  1: '0.25rem',
  2: '0.5rem',
  3: '0.75rem',
  4: '1rem',
  5: '1.25rem',
  6: '1.5rem',
  8: '2rem',
  10: '2.5rem',
  12: '3rem',
  16: '4rem',
  20: '5rem',
  24: '6rem',
} as const;
```

### Step 3: 컴포넌트 분해

HTML 구조를 분석하여 재사용 가능한 컴포넌트로 분해합니다.

#### 분해 원칙

| 원칙 | 설명 |
|------|------|
| 단일 책임 | 각 컴포넌트는 하나의 역할만 |
| 재사용성 | 여러 곳에서 사용될 패턴 식별 |
| 구성 가능성 | 작은 컴포넌트로 큰 컴포넌트 구성 |
| Props 기반 | 하드코딩 대신 Props로 커스터마이징 |

#### 컴포넌트 계층 구조

```
components/
├── primitives/          # 기본 요소
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Text.tsx
│   └── Icon.tsx
├── patterns/            # 재사용 패턴
│   ├── Card.tsx
│   ├── Badge.tsx
│   ├── Avatar.tsx
│   └── Tooltip.tsx
├── blocks/              # 섹션 블록
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── Hero.tsx
│   └── Features.tsx
└── layouts/             # 레이아웃
    ├── PageLayout.tsx
    └── GridLayout.tsx
```

### Step 4: 컴포넌트 생성

#### Button 컴포넌트 예시

```typescript
// components/primitives/Button.tsx
import { forwardRef, type ButtonHTMLAttributes } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: 'bg-primary text-white hover:bg-primary-hover',
        secondary: 'bg-neutral-100 text-neutral-900 hover:bg-neutral-200',
        outline: 'border border-neutral-200 bg-white hover:bg-neutral-50',
        ghost: 'hover:bg-neutral-100',
        destructive: 'bg-error text-white hover:bg-error/90',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-sm',
        lg: 'h-12 px-6 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size }), className)}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <span className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
        ) : null}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

#### Card 컴포넌트 예시

```typescript
// components/patterns/Card.tsx
import { forwardRef, type HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'outlined' | 'elevated';
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    const variants = {
      default: 'bg-white rounded-xl',
      outlined: 'bg-white rounded-xl border border-neutral-200',
      elevated: 'bg-white rounded-xl shadow-lg',
    };

    return (
      <div
        ref={ref}
        className={cn(variants[variant], className)}
        {...props}
      />
    );
  }
);

Card.displayName = 'Card';

// Sub-components
export const CardHeader = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6 pb-0', className)} {...props} />
  )
);

export const CardContent = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6', className)} {...props} />
  )
);

export const CardFooter = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6 pt-0 flex items-center gap-4', className)} {...props} />
  )
);
```

### Step 5: 검증

생성된 컴포넌트를 검증합니다.

#### TypeScript 검증

```bash
# 타입 체크
npx tsc --noEmit

# 린트 검사
npx eslint components/
```

#### 스토리북 검증 (선택)

```typescript
// components/primitives/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Primitives/Button',
  component: Button,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'Button',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    children: 'Button',
    variant: 'secondary',
  },
};

export const Loading: Story = {
  args: {
    children: 'Loading',
    isLoading: true,
  },
};
```

## 출력 파일 구조

```
src/
├── tokens/
│   ├── index.ts
│   ├── colors.ts
│   ├── typography.ts
│   ├── spacing.ts
│   └── shadows.ts
├── components/
│   ├── primitives/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── ...
│   ├── patterns/
│   │   ├── Card.tsx
│   │   └── ...
│   ├── blocks/
│   │   ├── Header.tsx
│   │   └── ...
│   └── index.ts
├── lib/
│   └── utils.ts
└── pages/
    └── [StitchPage].tsx   # 변환된 전체 페이지
```

## DESIGN.md 연동

`DESIGN.md`가 있으면 토큰 추출 시 참조하여 일관성을 보장합니다:

```typescript
// DESIGN.md의 색상 섹션과 매핑
const designMdColors = {
  'Deep Ocean Blue': '#0066FF',    // → colors.primary.DEFAULT
  'Whisper Gray': '#F5F5F5',       // → colors.neutral.100
  'Midnight Text': '#1A1A1A',      // → colors.neutral.900
};
```

## 자동화 스크립트

### 변환 스크립트

```typescript
// scripts/convert-stitch.ts
import { parseHTML } from './parsers/html';
import { extractTokens } from './extractors/tokens';
import { generateComponents } from './generators/components';
import { validateOutput } from './validators';

async function convertStitchScreen(htmlPath: string, outputDir: string) {
  // 1. HTML 파싱
  const dom = await parseHTML(htmlPath);

  // 2. 토큰 추출
  const tokens = extractTokens(dom);

  // 3. 컴포넌트 생성
  const components = generateComponents(dom, tokens);

  // 4. 파일 출력
  await writeTokens(outputDir, tokens);
  await writeComponents(outputDir, components);

  // 5. 검증
  const valid = await validateOutput(outputDir);
  if (!valid) {
    throw new Error('Validation failed');
  }

  console.log('Conversion complete!');
}
```

## 일반적인 변환 패턴

### Tailwind → CSS-in-JS

```typescript
// Stitch HTML
<button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg">

// React 컴포넌트
<Button variant="primary" size="md">
```

### 정적 콘텐츠 → Props

```typescript
// Stitch HTML
<h1 class="text-3xl font-bold">Welcome to Our App</h1>

// React 컴포넌트
interface HeadingProps {
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

<Heading size="xl">{title}</Heading>
```

### 반복 요소 → 매핑

```typescript
// Stitch HTML (반복된 카드)
<div class="card">...</div>
<div class="card">...</div>
<div class="card">...</div>

// React 컴포넌트
{items.map((item) => (
  <Card key={item.id} {...item} />
))}
```

## 피해야 할 함정

| 문제 | 해결책 |
|------|--------|
| ❌ 모든 스타일을 인라인으로 | 토큰과 variants 사용 |
| ❌ 하드코딩된 텍스트 | Props로 전달 |
| ❌ 단일 거대 컴포넌트 | 작은 컴포넌트로 분해 |
| ❌ 타입 정의 누락 | 모든 Props에 TypeScript 타입 |
| ❌ 접근성 무시 | ARIA 속성 및 시맨틱 HTML |

## 리소스

- **Stitch 문서**: https://stitch.withgoogle.com/docs/
- **class-variance-authority**: https://cva.style/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Radix UI**: https://www.radix-ui.com/ (접근성 있는 primitives)
