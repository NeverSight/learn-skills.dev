---
name: anti-slop-design
description: Create distinctive, production-grade frontend interfaces that avoid generic AI aesthetics. Use when building web components, game UIs, landing pages, dashboards, or any visual web interface. Prevents purple-gradient-rounded-corner-Inter-font syndrome.
metadata:
  author: misskim
  version: "1.0"
  origin: Concept inspired by Anthropic frontend-design skill, rewritten for our environment
---

# Anti-Slop Design

모든 프론트엔드 작업에서 "AI가 만든 것 같은" 뻔한 디자인을 절대 방지한다.

## AI Slop의 징후 (절대 금지)

- Inter/Roboto/Arial/시스템 폰트 기본 사용
- 보라색 그라디언트 on 흰 배경
- 모든 요소에 균일한 rounded corners
- 가운데 정렬만 하는 레이아웃
- 뻔한 hero section + 3-column features
- 모든 카드에 동일한 그림자
- 감정 없는 일러스트레이션

## 디자인 프로세스

### 1. 맥락 파악
- **목적:** 이 인터페이스가 해결하는 문제는?
- **사용자:** 누가 쓰나? (게이머? 개발자? 일반인?)
- **톤:** 극단적으로 선택 — 아래 중 하나:
  - 브루탈리즘 / 미니멀 / 레트로퓨처리즘 / 유기적자연
  - 럭셔리 / 장난감같은 / 에디토리얼 / 아트데코
  - 인더스트리얼 / 소프트파스텔 / 80s네온 / 일본미니멀
- **차별점:** 사용자가 기억할 단 하나의 요소는?

### 2. 핵심 원칙

**타이포그래피:**
- 독특하고 아름다운 폰트 선택 (Google Fonts에서 발굴)
- 디스플레이 폰트 + 본문 폰트 페어링
- 매번 다른 폰트 조합 (같은 폰트 반복 금지)

**컬러:**
- CSS 변수로 일관성 확보
- 지배적 색상 + 강렬한 액센트 (고르게 분배하지 말 것)
- 매번 다른 색상 팔레트

**모션:**
- CSS-only 우선 (HTML 단일 파일의 경우)
- 페이지 로드 시 staggered reveal이 핵심 인상
- hover/scroll 기반 의외의 상호작용

**공간 구성:**
- 비대칭 레이아웃, 겹침, 대각선 흐름
- 그리드를 깨는 요소들
- 넉넉한 여백 또는 의도적 밀도

**배경/디테일:**
- 단색 배경 기본값 금지
- 그라디언트 메쉬, 노이즈 텍스처, 기하학 패턴
- 깊이감을 주는 레이어, 그림자, 투명도

### 3. 게임 UI 특화 원칙

게임 인터페이스 제작 시 추가 적용:
- **몰입감 우선:** UI가 게임 세계관의 일부여야 함
- **에셋 활용:** NAS 게임마당(161GB), Gemini AI 생성, 무료 에셋 사이트
- **애니메이션:** CSS transitions + requestAnimationFrame
- **사운드 피드백:** 클릭/호버 시 효과음 (가능한 경우)
- **반응형:** 텔레그램 Mini App 환경 고려 (WebView safe-area)

## 품질 체크리스트

- [ ] Inter/Roboto/Arial 사용하지 않았는가?
- [ ] 보라색 그라디언트 없는가?
- [ ] 모든 요소가 동일한 border-radius가 아닌가?
- [ ] 레이아웃에 비대칭 요소가 있는가?
- [ ] 이전에 만든 것과 다른 폰트/색상인가?
- [ ] "이게 AI가 만든 거야?"라는 말이 안 나올 정도인가?
