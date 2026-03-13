---
name: figma-to-code
description: Figma 디자인을 고성능 Next.js와 Tailwind CSS 코드로 변환하는 스킬. 픽셀 퍼펙트한 반응형 컴포넌트 구현을 지원합니다.
version: 1.1.0
author: BSD Vibe Coding Center
tags: [figma, nextjs, tailwind-css, frontend, responsive]
---

# 🎨 Next.js Figma 디자인 구현 스킬

이 스킬은 BSD 바이브코딩 수강생들이 **Figma 디자인을 실제 작동하는 Next.js 웹사이트로 변환**할 수 있도록 돕습니다.

## 📋 이 스킬이 하는 일

1. **디자인 분석**: Figma 파일의 레이아웃, 컴포넌트, 색상 시스템 분석
2. **Next.js 컴포넌트화**: Figma 레이어를 재사용 가능한 React 컴포넌트로 변환
3. **Tailwind CSS 적용**: 유틸리티 우선 CSS를 사용한 빠르고 정확한 스타일링
4. **반응형 최적화**: Tailwind의 브레이크포인트를 활용한 모바일/데스크톱 대응
5. **인터랙션 구현**: Framer Motion을 활용한 부드러운 애니메이션 추가

## 🎯 언제 이 스킬을 사용하나요?

- "Figma 디자인을 Next.js 프로젝트로 빠르게 옮기고 싶어요"
- "Tailwind CSS를 써서 디자인과 똑같은 웹사이트를 코딩하고 싶어요"
- "Vercel에 배포할 품질 높은 프론트엔드 코드가 필요해요"

## 🛠️ 기술 스택 (Professional Stack)

### 1. Framework

- **Next.js 14+ (App Router)**
- **TypeScript** (안정성 확보)

### 2. Styling

- **Tailwind CSS**: 디자인 시스템 반영
- **Lucide React / Heroicons**: 아이콘 시스템

### 3. Animation

- **Framer Motion**: 정교한 웹 애니메이션

## 💻 구현 예시 (Figma Design to Next.js)

### 1. Component Analysis

Figma의 'Navbar' 프레임 → `components/Navbar.tsx`

### 2. Implementation Code

```tsx
import React from "react";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between py-6 px-8 bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-gray-100">
      <div className="text-2xl font-bold text-blue-600">Logo</div>
      <ul className="hidden md:flex gap-8 text-gray-600 font-medium">
        <li>
          <Link href="#features" className="hover:text-blue-500 transition">
            기능
          </Link>
        </li>
        <li>
          <Link href="#pricing" className="hover:text-blue-500 transition">
            가격
          </Link>
        </li>
        <li>
          <Link href="#faq" className="hover:text-blue-500 transition">
            FAQ
          </Link>
        </li>
      </ul>
      <button className="bg-blue-600 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-blue-700 transition">
        시작하기
      </button>
    </nav>
  );
}
```

## 📐 Figma 디자인 분석 체크리스트

### 1. 그리드 및 간격

- Tailwind의 Spacing Scale (4, 8, 12, 16px...)에 맞춰 디자인 분석
- `max-w-7xl` 등 표준 컨테이너 너비 설정

### 2. 컬러 시스템

- Figma의 HEX 코드를 `tailwind.config.ts`의 커스텀 컬러로 등록
- 다크 모드(`dark:`) 고려 여부 확인

## 💬 예제 대화

**사용자**: "이 Figma 스크린샷 보고 Next.js + Tailwind로 히어로 섹션 짜줘"

**Claude**:
"Figma 디자인을 분석하여 Next.js 컴포넌트와 Tailwind CSS로 변환해드리겠습니다. 이미지 최적화(`next/image`)와 텍스트 레이아웃을 정교하게 구현한 코드를 생성해 드릴게요..."

---

## 🎯 핵심 정리

이 스킬을 사용하면:
✅ **픽셀 퍼펙트**: Figma 디자인과 99% 일치하는 코드 생성
✅ **생산성 향상**: 수동 마크업 시간을 획기적으로 단축
✅ **클린 코드**: 유지보수가 쉬운 모듈화된 React 컴포넌트 제공
✅ **공연 최적화**: Next.js의 내장 기능을 활용한 최고 수준의 웹 성능

**BSD 학생이라면**: 이제 디자인을 코드로 옮기는 노가다에서 벗어나, 더 중요한 비즈니스 로직 개발에 집중할 수 있습니다! 🎨
