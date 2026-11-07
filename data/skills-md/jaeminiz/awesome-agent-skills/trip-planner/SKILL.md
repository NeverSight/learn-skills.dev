---
name: trip-planner
description: >-
  Interactive expert global travel planner and itinerary architect. Use this skill whenever
  the user wants to plan, organize, or refine any domestic or international travel itinerary
  worldwide (Asia, Europe, Americas, Oceania, etc.). It conducts interactive questionnaires first,
  searches real-time lowest flight and hotel prices via browser/web tools (Naver Travel, Google
  Travel, Skyscanner, etc.), applies live daily exchange rates for any local currency, curates
  food/café options from travel YouTubers, bloggers, and Instagram, adapts local transport
  (Uber/Grab/Trains/Rentals), provides native situational phrases, and strictly confirms with
  the user before generating final Day-by-Day CSVs, all-in-one Google My Maps KML files, and
  choice of 2 mobile web apps: Style 1 (Default: Feature-rich Mobile Pocket Guide with 4 tabs,
  live search, checkmarks, Apple/Google Maps, TTS voice, and exchange calculator) or Style 2
  (Apple iOS Card News App with swipe gestures and 4 utility modals).
---

# 🧭 Global Trip Planner

**Language:** **English (Default)** | [한국어 버전 (Korean)](#korean-version)

> **Universal AI Travel Planner & Itinerary Architect for Agentic Frameworks.**  
> Covers domestic and worldwide international destinations (Asia, Europe, Americas, Oceania, etc.).  
> **Strictly interactive**: Conducts structured questionnaires first, retrieves real-time live flight/hotel pricing and daily foreign exchange rates, curates social media-trending gourmet spots and cafes, and generates **Google My Maps Day-by-Day CSVs, All-in-One KMLs, and 2 Styles of Mobile Web Applications (`[city]_pocket_guide.html` or `[city]_trip_cards.html`)**.

---

## 🌐 Multilingual & Language-Agnostic Execution Policy

This skill automatically detects and adapts to the user's preferred language:
* **English Conversation (Default)**: Conducts all questionnaires, research reports, timeline tables, budgets, and deliverable files completely in **English** (with native local phrases for destination countries).
* **Korean Conversation (한국어 대응)**: 사용자가 한국어로 질문하거나 요청할 경우, 모든 문답과 마스터 일정표, 예산안, 산출물을 **한국어**로 정밀하게 작성합니다.
* **Any Other Language**: Adapts effortlessly to Spanish, Japanese, Chinese, French, German, etc.

---

## ⛔ 6 Strict Planner Rules

1. **Interactive Confirmation First (No Arbitrary Guessing)**:
   - Clarify essential conditions (destination, duration, travel party composition, travel style, and budget) through structured dialogue before drafting any itinerary.
2. **Real-Time Global Search (Live Pricing & Daily Exchange Rates)**:
   - Use browser search tools to inspect real-time bookable flight/hotel options on platforms like Google Flights, Skyscanner, Agoda, Booking.com, and Naver Travel.
   - Apply live daily exchange rates (USD, EUR, JPY, GBP, VND, THB, TWD, etc.) for accurate multi-currency budget calculations.
3. **Media-Driven Deep Trend Research (YouTube, Blogs, Instagram, Google Reviews)**:
   - Conduct cross-platform trend analysis to curate verified local hotspots, food scenes, waiting time estimates, and safety tips.
4. **Route-Optimized Gourmet & Cafe Curation**:
   - Provide selective options tailored to daily travel paths (authentic local eateries, Michelin/bistros, traveler favorites, and scenic healing cafes) and let the user pick their favorites.
5. **Mandatory 5-Column Detailed Timeline Table & Precision Budget (No Abbreviations)**:
   - When presenting the Master Itinerary (Phase 4), **never provide a summarized or shortened overview**.
   - Output full minute-by-minute timeline tables (`No. | Time | Activity Details | Spots & Transit Tips | Situational Local Phrases`) along with multi-stop Google Maps route links and complete budget breakdowns.
6. **Explicit User Confirmation & 2 Web App Style Options**:
   - Before writing any final files, ask the user to confirm the itinerary and **select their preferred Web App Style**:
     - **Style 1: Mobile Pocket Guide Web App (Default & Recommended ⭐)**: 4 native bottom tabs (Timeline, Places, Phrases, Ready), sticky date switcher, real-time search & filters, interactive checkmarks (saved in localStorage), dual Apple/Google Maps links, oversized dialog for drivers/staff & native Web Speech TTS, dynamic exchange rate calculator. (Template: `resources/pocket_guide_app_template.html`).
     - **Style 2: Apple iOS Card News Web App (Option)**: Minimal white glassmorphism card news slide deck with swipe gestures and 4 top utility modals (Budget, Shopping, Emergency, Schedule). (Template: `resources/ios_card_app_template.html`).
   - Only generate the files after the user gives explicit approval. If the user does not specify, default to **Style 1**.

---

## 📋 6-Phase Global Workflow

```
[Phase 1] Initial Interview & Mandatory Questionnaire (Customized by destination)
       ↓
[Phase 2] Real-Time Flight & Hotel Live Pricing & Daily Exchange Rate Report ➔ [User Selection]
       ↓
[Phase 3] Route-Optimized Gourmet & Scenic Spot Curated List ➔ [User Selection]
       ↓
[Phase 4] ⭐ Comprehensive Master Output (Never abbreviated):
          1. Detailed minute-by-minute timeline table (5 columns per day)
          2. Multi-stop Google Maps transit route links
          3. Daily exchange rate applied precision budget breakdown
       ↓
[Phase 5] Explicit User Confirmation & Style Choice:
          "All itinerary details are confirmed. Which web app style would you prefer?
           1) Pocket Guide Web App (Default: 4 tabs, search, checkmarks, Apple/Google Maps, TTS, live rate calculator)
           2) Apple iOS Card News App (Swipe cards, glassmorphism, 4 modals)" ➔ [User Approval]
       ↓
[Phase 6] Final File Generation: Day-by-Day CSVs, [City]_mymaps.kml, and selected Web App ([City]_pocket_guide.html or [City]_trip_cards.html)
```

---

## 📦 Multi-Modal Deliverables

### 1. Google My Maps Day-by-Day CSVs (`day1_itinerary.csv`, `day2_itinerary.csv`...)
* Standard 8-column format: `Date,Time,Place,Latitude,Longitude,GoogleMaps,Description,Transit_Notes`.
* Explicit Latitude and Longitude columns ensure 1-second instant pinpointing without parsing ambiguity in Google My Maps.
* When imported into Google My Maps and styled with [Sequence of numbers], pins are automatically marked `1, 2, 3...` in chronological order.

### 2. All-in-One & Day-by-Day KML Files (`[City]_mymaps.kml`, `[City]_DayN.kml`)
* 100% compliant with Google My Maps parser requirements:
  - **XML Entity Escaped**: All `&` characters in names and descriptions are strictly encoded as `&amp;` to prevent XML syntax parse errors.
  - **Clean Flat Placemarks**: Structured for seamless single-layer import, with optional day-specific KMLs for multi-layer mapping.
  - Chronological numbered pins (`#1`, `#2`...) with clean HTML balloon popups.

#### 💡 User Guide: How to Import into Google My Maps
1. Open **[Google My Maps](https://www.google.com/maps/d/)** ➔ Click **[+ Create a new map]**.
2. Click **[Import]** on the layer ➔ Upload `day1_itinerary.csv` (or full `danang_itinerary.csv`) or drag and drop `[City]_mymaps.kml`.
3. For CSV: Choose `Latitude` and `Longitude` for placemark positions, select `Place` for marker titles. Click **[Uniform style]** ➔ Change to **[Sequence of numbers]** for auto number badges `1, 2, 3...`.

---

### 3. Dual-Style Mobile Web Applications

#### 📱 Style 1: Mobile Pocket Guide Web App (Default & Recommended ⭐)
* **File Target**: `[City]_pocket_guide.html` (or `[City]_trip_cards.html`)
* **Base Template**: [`resources/pocket_guide_app_template.html`](./resources/pocket_guide_app_template.html) (Example: [`examples/danang_pocket_guide.html`](./examples/danang_pocket_guide.html))
* **Key Features**:
  1. **Sticky Date Bar**: Instant switching between days with keyboard arrow key support.
  2. **4 Native Bottom Tabs**:
     - **Timeline (`timeline`)**: Full minute-by-minute schedule, completion progress bar with "Jump to Next Event" anchor, interactive checkmarks (`data-done`) preserved in `localStorage`, dual **Apple Maps** & **Google Maps** one-click links, and collapsible native phrase accordion with **Web Speech API TTS Pronunciation**, **Oversized Fullscreen Dialog (`#phrase-modal`) for drivers and staff**, and **1-click Clipboard Copy**.
     - **Places (`places`)**: Basecamp hotel card, live instant search box, category filter chips (`All`, `Food`, `Shopping`, `Sights`, `Tours`, `Transit`, `Cafe`, `Spa`).
     - **Phrases (`phrases`)**: Complete situational phrase handbook with instant search, audio playback, fullscreen card, and copy buttons.
     - **Ready (`ready`)**: Interactive packing checklist with live count (`X/Total`), shopping wishlist checkmarks, total budget breakdown with **dynamic exchange rate calculator** (auto-converts local currency into KRW/home currency in real-time), food budget list, and critical travel tips.
* **Schema**: Populate `window.TRIP = { meta: {...}, hotel: {...}, days: [...], shopping: [...], packing: [...], budget: [...], food: [...], notes: [...] };`.

#### 🗂️ Style 2: Apple iOS Card News Web App (Option)
* **File Target**: `[City]_trip_cards.html`
* **Base Template**: [`resources/ios_card_app_template.html`](./resources/ios_card_app_template.html) (Example: [`examples/danang_trip_cards.html`](./examples/danang_trip_cards.html))
* **Key Features**:
  - Clean white glassmorphic card deck (`bg-[#F2F2F7]`, `rounded-[28px]`, `shadow-ios`).
  - 1-Card-at-a-time view with swipe gestures and sequence badges.
  - 4 Top Utility Modals: Budget highlight (`#modalBudget`), Shopping wishlist (`#modalShopping`), Emergency taxi cards & contacts (`#modalEmergency`), and Full schedule modal.
* **Schema**: Populate `const itineraryData = [ ... ];` array using exact object structure.

---

<div id="korean-version"></div>

<details>
<summary><b>🇰🇷 한국어 버전 (Click to view Korean Version)</b></summary>

### 🧭 글로벌 전문가 여행 플래너 스킬

전 세계 모든 국내외 여행지(아시아, 유럽, 미주, 대양주 등)를 아우르는 전문 여행 플래너이자 일정 아키텍트입니다.  
**일방적으로 일정을 임의 작성하지 않고** 사용자와 단계별 인터랙티브 문답을 통해 여행 취향을 파악합니다.  
"브라우저" 기반 실시간 최저가(항공·숙소)와 목적지 국가의 당일 실시간 환율을 검색·반영하고, 여행 유튜버·블로거·인스타그램 트렌드를 심층 조사하여 최적의 동선, 맛집, 카페, 교통(우버/그랩/기차 등)을 큐레이션하며, **최종 구글 내 지도 산출물(Day별 CSV & 올인원 KML) 및 2가지 스타일의 모바일 최적화 웹앱(`[도시]_pocket_guide.html` 또는 `[도시]_trip_cards.html`) 생성 전 반드시 사용자의 확인과 스타일 선택을 거칩니다.**

#### ⛔ 플래너 6대 절대 원칙
1. **사전 확인 없는 임의 작성 금지**: 시작 시 목적지, 일정, 인원, 여행 스타일, 예산을 먼저 질문하고 사용자의 선택을 받습니다.
2. **실시간 최저가 및 당일 환율 반영**: 항공/숙소 실시간 검색 및 당일 매매기준율 적용.
3. **트렌드 미디어 심층 리서치**: 유튜브, 블로그, 인스타를 종합 조사하여 최근 검증된 핫플과 미식 반영.
4. **동선 최적화 맛집 & 카페 큐레이션**: 권역별 맛집 및 카페 후보군 제시 후 사용자 선택 유도.
5. **일자별 상세 타임라인 종합 정리표 & 최종 예산표 전체 출력 필수**: 축약 없이 5개 컬럼 테이블 온전히 출력.
6. **최종 산출물 승인 및 2가지 웹앱 스타일 선택 확인**:
   - 파일 생성 전 사용자에게 일정 승인을 구하고 **웹앱 스타일 2가지 중 원하는 레이아웃을 질문**합니다:
     - **스타일 1: 모바일 포켓 가이드 웹앱 (기본 추천 ⭐)**: 4개 탭(일정/장소/회화/준비), 실시간 검색, 완료 체크박스(localStorage), Apple/Google 지도 듀얼 연동, 대형 텍스트 모달 & 원어민 TTS, 실시간 환율 연동 예산 계산기 (`resources/pocket_guide_app_template.html`).
     - **스타일 2: 애플 아이폰 카드뉴스 웹앱 (선택)**: 스와이프 제스처 카드뉴스, 글래스모피즘 디자인, 4대 유틸리티 모달 (`resources/ios_card_app_template.html`).
   - 사용자가 별도 지정하지 않으면 **스타일 1**을 기본 적용합니다.

#### 📋 6단계 워크플로우
1. **[1단계] 사전 인터뷰 및 필수 문답**: 여행지, 일정, 동행자, 선호 스타일, 예산 파악.
2. **[2단계] 실시간 항공·숙소 최저가 & 당일 환율 보고 ➔ [사용자 선택]**
3. **[3단계] 동선 맞춤형 맛집·카페 큐레이션 리스트 ➔ [사용자 선택]**
4. **[4단계] ⭐ 마스터 일정표 & 정밀 예산안 전체 출력 (축약 금지)**
5. **[5단계] 최종 확인 및 웹앱 스타일 선택 질문 ➔ [사용자 승인]**
6. **[6단계] 최종 파일 일괄 빌드**: Day별 CSV, [도시]_mymaps.kml, 선택된 스타일 웹앱

</details>
