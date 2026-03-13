---
name: figma-ddocdoc-app
description: ddocdoc-app(React Native) 디자인 시스템 피그마-코드 매핑 가이드. 피그마 컴포넌트를 React Native(NativeWind) 코드로 변환할 때, 컬러 토큰 사용법과 컴포넌트 매핑 규칙을 참조.
metadata:
  author: ddocdoc
  version: "1.0.0"
---

# Figma ddocdoc Design System

ddocdoc-app React Native 프로젝트의 디자인 시스템 레퍼런스. 2개 규칙 파일로 구성. 피그마 컴포넌트 변환 시 반드시 이 가이드를 따른다.

## When to Apply

Reference these guidelines when:
- 피그마 디자인을 React Native 코드로 구현할 때
- NativeWind 컬러 클래스 매핑이 필요할 때
- 피그마 컴포넌트명에 해당하는 코드 컴포넌트를 찾을 때
- 버튼, 팝업, 입력, 바텀시트, 헤더, 선택 컨트롤 컴포넌트를 구현할 때

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Color & Styling | CRITICAL | `code-` |
| 2 | Component Mapping | HIGH | `component-` |

## Quick Reference

### 1. Color & Styling (CRITICAL)

- `code` - 컬러 토큰(Yellow/CoolGray/NeutralGray 등), NativeWind className 패턴, lineHeight 오버라이드, inline style 예외

### 2. Component Mapping (HIGH)

- `component` - SolidButton, FilterButton, SimplePopup, BaseSnackbar, BaseTextInput, SSNBackNumberPadBottomSheet, BaseBottomSheet, NavButtonTitleHeader, Checkbox 전체 매핑

## How to Use

Read individual rule files for detailed Figma mapping and code examples:

```
rules/code.md
rules/component.md
```

Each rule file contains:
- YAML frontmatter with title, impact, and tags
- Figma component name → code component mapping
- Props reference
- Usage code examples

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
