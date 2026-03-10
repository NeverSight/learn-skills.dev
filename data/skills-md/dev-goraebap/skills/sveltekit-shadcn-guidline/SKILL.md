---
name: sveltekit-shadcn-guidline
description: "SvelteKit 프로젝트에서 shadcn-svelte 컴포넌트를 활용하는 가이드. 사용자가 UI 화면을 구성하거나 어떤 컴포넌트를 써야 할지 고민할 때, 또는 shadcn-svelte 컴포넌트를 설치하거나 초기 설정이 필요할 때 반드시 이 스킬을 사용한다. 버튼, 모달, 카드, 사이드바, 폼, 테이블 등 UI 요소를 언급하면 이 스킬을 적극 참고한다."
---

# shadcn-svelte 가이드

> shadcn-svelte는 TypeScript, Tailwind CSS, Bits UI 기반의 접근성 높은 Svelte/SvelteKit 컴포넌트 모음이다. CLI로 컴포넌트를 설치하고 소스를 직접 수정할 수 있다.

---

## 사용 원칙

이 스킬의 주 목적은 **화면 구성 시 알맞은 컴포넌트를 선택하고 올바르게 사용하도록 돕는 것**이다. 아래 컴포넌트 목록을 참고해 작업에 적합한 컴포넌트를 추천하고 코드를 작성한다.

컴포넌트를 실제로 추가해야 할 때는 아래 "컴포넌트 설치" 절차를 따른다.

---

## 컴포넌트 설치

### 1. shadcn-svelte 설정 확인

컴포넌트를 추가하기 전에 작업공간에 shadcn-svelte가 초기화되어 있는지 확인한다:

```bash
ls components.json
```

- **파일이 있으면** → 이미 설정 완료. 바로 컴포넌트 추가로 이동.
- **파일이 없으면** → 사용자에게 직접 초기화를 요청한다:

> **shadcn-svelte가 초기화되어 있지 않습니다.**
> 터미널에서 아래 명령어를 원하는 설정으로 먼저 실행해 주세요:
>
> ```bash
> npx shadcn-svelte@latest init
> ```
>
> 권장 설정:
> - Base color: `Slate`
> - Global CSS: `src/routes/+layout.svelte`
> - Import aliases: `$lib`, `$lib/components`, `$lib/utils`, `$lib/hooks`, `$lib/components/ui`
>
> 완료되면 다시 알려주세요.

초기화 완료 확인 후 컴포넌트 추가로 진행한다.

### 2. 컴포넌트 추가 방식 선택

사용자에게 설치 방식을 확인한다:

**A. 필요한 컴포넌트만 설치 (권장)**
```bash
npx shadcn-svelte@latest add button
npx shadcn-svelte@latest add dialog card
```

**B. 전체 컴포넌트 일괄 설치**
```bash
npx shadcn-svelte@latest add --all

# 확인 프롬프트 없이
npx shadcn-svelte@latest add --all --yes

# 기존 파일 덮어쓰기
npx shadcn-svelte@latest add --all --overwrite
```

### 주요 CLI 옵션

| 옵션 | 설명 |
|------|------|
| `-a, --all` | 모든 컴포넌트 설치 |
| `-y, --yes` | 확인 프롬프트 건너뜀 |
| `-o, --overwrite` | 기존 파일 덮어쓰기 |
| `--no-deps` | 패키지 의존성 설치 제외 |

### 컴포넌트 임포트

```ts
import { Button } from "$lib/components/ui/button/index.js";
import { Dialog } from "$lib/components/ui/dialog/index.js";
```

---

## 컴포넌트 목록

### Form & Input (폼 & 입력)

- [Button](https://shadcn-svelte.com/docs/components/button.md): 버튼
- [Button Group](https://shadcn-svelte.com/docs/components/button-group.md): 관련 버튼을 묶는 그룹
- [Calendar](https://shadcn-svelte.com/docs/components/calendar.md): 날짜 선택 캘린더
- [Checkbox](https://shadcn-svelte.com/docs/components/checkbox.md): 체크박스
- [Combobox](https://shadcn-svelte.com/docs/components/combobox.md): 자동완성 입력 + 커맨드 팔레트
- [Date Picker](https://shadcn-svelte.com/docs/components/date-picker.md): 범위/프리셋 포함 날짜 선택기
- [Field](https://shadcn-svelte.com/docs/components/field.md): 레이블 + 컨트롤 + 도움말 조합 폼 필드
- [Formsnap](https://shadcn-svelte.com/docs/components/form.md): Formsnap + Superforms + Zod 폼 구성
- [Input](https://shadcn-svelte.com/docs/components/input.md): 텍스트 입력 필드
- [Input Group](https://shadcn-svelte.com/docs/components/input-group.md): 입력 필드에 추가 정보/액션 붙이기
- [Input OTP](https://shadcn-svelte.com/docs/components/input-otp.md): OTP 입력 (복사/붙여넣기 지원)
- [Label](https://shadcn-svelte.com/docs/components/label.md): 접근성 레이블
- [Native Select](https://shadcn-svelte.com/docs/components/native-select.md): 스타일드 네이티브 select
- [Radio Group](https://shadcn-svelte.com/docs/components/radio-group.md): 라디오 버튼 그룹 (단일 선택)
- [Select](https://shadcn-svelte.com/docs/components/select.md): 드롭다운 선택 (버튼 트리거)
- [Slider](https://shadcn-svelte.com/docs/components/slider.md): 범위 값 슬라이더
- [Switch](https://shadcn-svelte.com/docs/components/switch.md): 토글 스위치
- [Textarea](https://shadcn-svelte.com/docs/components/textarea.md): 멀티라인 텍스트 입력

### Layout & Navigation (레이아웃 & 내비게이션)

- [Accordion](https://shadcn-svelte.com/docs/components/accordion.md): 펼치고 접는 아코디언
- [Breadcrumb](https://shadcn-svelte.com/docs/components/breadcrumb.md): 현재 위치 경로 표시
- [Navigation Menu](https://shadcn-svelte.com/docs/components/navigation-menu.md): 사이트 내비게이션 메뉴
- [Resizable](https://shadcn-svelte.com/docs/components/resizable.md): 키보드 지원 리사이저블 패널
- [Scroll Area](https://shadcn-svelte.com/docs/components/scroll-area.md): 커스텀 스크롤 영역
- [Separator](https://shadcn-svelte.com/docs/components/separator.md): 콘텐츠 구분선
- [Sidebar](https://shadcn-svelte.com/docs/components/sidebar.md): 조합 가능한 사이드바
- [Tabs](https://shadcn-svelte.com/docs/components/tabs.md): 탭 패널

### Overlays & Dialogs (오버레이 & 다이얼로그)

- [Alert Dialog](https://shadcn-svelte.com/docs/components/alert-dialog.md): 확인을 요구하는 모달 다이얼로그
- [Command](https://shadcn-svelte.com/docs/components/command.md): 커맨드 메뉴 (⌘K 스타일)
- [Context Menu](https://shadcn-svelte.com/docs/components/context-menu.md): 우클릭 컨텍스트 메뉴
- [Dialog](https://shadcn-svelte.com/docs/components/dialog.md): 모달 다이얼로그
- [Drawer](https://shadcn-svelte.com/docs/components/drawer.md): 드로어 (모바일 친화적)
- [Dropdown Menu](https://shadcn-svelte.com/docs/components/dropdown-menu.md): 버튼 트리거 드롭다운 메뉴
- [Hover Card](https://shadcn-svelte.com/docs/components/hover-card.md): 호버 시 링크 미리보기
- [Menubar](https://shadcn-svelte.com/docs/components/menubar.md): 데스크탑 앱 스타일 메뉴바
- [Popover](https://shadcn-svelte.com/docs/components/popover.md): 팝오버
- [Sheet](https://shadcn-svelte.com/docs/components/sheet.md): 화면 가장자리 슬라이드 패널
- [Tooltip](https://shadcn-svelte.com/docs/components/tooltip.md): 호버/포커스 툴팁

### Feedback & Status (피드백 & 상태)

- [Alert](https://shadcn-svelte.com/docs/components/alert.md): 알림 박스
- [Badge](https://shadcn-svelte.com/docs/components/badge.md): 배지
- [Empty](https://shadcn-svelte.com/docs/components/empty.md): 빈 상태 표시
- [Progress](https://shadcn-svelte.com/docs/components/progress.md): 진행률 표시바
- [Skeleton](https://shadcn-svelte.com/docs/components/skeleton.md): 로딩 중 플레이스홀더
- [Sonner](https://shadcn-svelte.com/docs/components/sonner.md): 토스트 알림
- [Spinner](https://shadcn-svelte.com/docs/components/spinner.md): 로딩 스피너

### Display & Media (표시 & 미디어)

- [Aspect Ratio](https://shadcn-svelte.com/docs/components/aspect-ratio.md): 비율 고정 컨테이너
- [Avatar](https://shadcn-svelte.com/docs/components/avatar.md): 사용자 아바타 (폴백 포함)
- [Card](https://shadcn-svelte.com/docs/components/card.md): 헤더/콘텐츠/푸터 카드
- [Carousel](https://shadcn-svelte.com/docs/components/carousel.md): 스와이프 캐러셀 (Embla 기반)
- [Chart](https://shadcn-svelte.com/docs/components/chart.md): 차트 (LayerChart 기반)
- [Data Table](https://shadcn-svelte.com/docs/components/data-table.md): 데이터 그리드 (TanStack Table 기반)
- [Item](https://shadcn-svelte.com/docs/components/item.md): 다목적 콘텐츠 표시
- [Kbd](https://shadcn-svelte.com/docs/components/kbd.md): 키보드 입력 표시
- [Table](https://shadcn-svelte.com/docs/components/table.md): 반응형 테이블
- [Typography](https://shadcn-svelte.com/docs/components/typography.md): 제목/단락/목록 타이포그래피

### Misc (기타)

- [Collapsible](https://shadcn-svelte.com/docs/components/collapsible.md): 접기/펼치기 패널
- [Pagination](https://shadcn-svelte.com/docs/components/pagination.md): 페이지네이션
- [Range Calendar](https://shadcn-svelte.com/docs/components/range-calendar.md): 날짜 범위 선택 캘린더
- [Toggle](https://shadcn-svelte.com/docs/components/toggle.md): 켜기/끄기 토글 버튼
- [Toggle Group](https://shadcn-svelte.com/docs/components/toggle-group.md): 토글 버튼 그룹

---

## 참고 문서

- [CLI 전체 문서](https://shadcn-svelte.com/docs/cli.md)
- [Theming (테마 커스터마이징)](https://shadcn-svelte.com/docs/theming.md)
- [다크 모드 설정](https://shadcn-svelte.com/docs/dark-mode/svelte.md)
- [Tailwind v4 마이그레이션](https://shadcn-svelte.com/docs/migration/tailwind-v4.md)
- [Svelte 5 마이그레이션](https://shadcn-svelte.com/docs/migration/svelte-5.md)
- [components.json 설정](https://shadcn-svelte.com/docs/components-json.md)
