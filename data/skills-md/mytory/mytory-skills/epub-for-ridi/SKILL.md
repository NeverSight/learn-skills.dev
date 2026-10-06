---
name: epub-for-ridi
description: EPUB을 생성하거나 리디북스(RIDI Books)·국내 뷰어 업로드용으로 검증·보정할 때 사용합니다. Calibre 변환 후 목차가 "없는 작품"으로 뜨거나, NCX 누락·CSS 제약·제목 크기 위계·왼쪽 정렬 문제를 점검·수정할 때, Pandoc·Calibre의 한국어 EPUB에서 따옴표 변형이나 목차 중복을 확인할 때도 사용하세요. 스캔 PDF에서 볼드·소제목·블록인용 서식을 복원하거나, Calibre DOCX 변환에서 볼드가 사라질 때도 사용하세요. 한국어 EPUB·DOCX에서 의미 강조(em)를 밑줄로, 강조(strong)를 볼드로 표시하고 출판물 이름을 《》·〈〉로 다룰 때도 사용하세요.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---

# 리디북스용 EPUB 생성·검증 스킬

Pandoc·Calibre로 한국어 EPUB을 만들 때의 제작 경험과 호환성 점검을 정리한다.
기존 도구와 사용자의 서식 선택을 존중한다. 아래 리디 검증기 규칙은
**2018년에 보관 처리된 CP 업로드용 공개 저장소** 기준이며, 현재 앱이나 개인
파일 가져오기의 필수 조건으로 단정하지 않는다. 로컬 검사 통과와 실제 앱 표시를 구분한다.

## 가장 중요한 사실

- **EPUB3 목차(nav)와 EPUB2 호환 목차(NCX)를 구분한다.** 기존 Calibre 제작 사례에서
  nav만 생성되어 리디 목차 문제가 있었다. 도구·버전별 결과를 열어 확인한다.
  오래된 리디 검증기는 NCX를 요구한다(EPUB-302). 필요한 경우
  `scripts/fix_epub_for_ridi.py`로 추가하며, 이미 있는 NCX는 보존한다.
- **Calibre의 폰트 리스케일링이 제목 위계를 흐트러뜨린다.** `body`에
  12pt를 주고 h2=1.6em, h3=1.3em, h4=1.15em로 지정하면, 리스케일링 후
  실측값이 1.66667 / 1.41667 / 1.125em로 재매핑되어 간격이 좁아지고
  h4는 오히려 작아진다.
  → 필요하면 EPUB 출력에 `--disable-font-rescaling`을 넣는다. 제목 크기는
  `em`을 사용한 예시를 참고한다. `rem`도 사용자 글꼴 설정의 영향을
  받으므로 무조건 금지하지 않으며, 사용자가 지정한 단위를 우선한다.
  (실측표: `references/heading-css.md`)
- **리디 앱에서 헤딩 마진이 표시되지 않으면 패딩을 시도한다.** 이번 제작에서
  사용자가 리디 앱의 마진 문제를 보고했다. 패딩은 호환성 대안이며 실제 표시를 확인한다.
  예시는 `margin: 0; padding-top: 2.5rem; padding-bottom: 1rem`이다.
- **공개 검증기의 HTML-303은 body 인라인 배경색, CSS-301은 html/body 크기를 검사한다.**
  CSS 배경색과 인라인 배경색 검사는 구분한다. 이 검증기의 CSS-301은
  **선택자가 정확히 `html`/`body`일 때만** 검사한다. Calibre는 `body { max-width: ... }`를
  `body class="calibreN"` + `.calibreN { ... }`로 바꿔 내보내므로
  **리디 검증을 그대로 통과한다.** 검증 통과가 안전을 뜻하지는 않는다.
  → `check_ridi.py`는 이 우회 형태를 `CSS-301-L` 경고로 알려 준다.
  → 템플릿 단계에서 `body`의 `max-width`·`background-color`를 빼는 편이 좋다.
- **공개 검증기는 NCX 경로의 `./` 접두를 오류로 처리한다(EPUB-301).**
  경로는 NCX 파일 위치 기준으로 계산한다. nav와 NCX가 다른 폴더이면
  href를 그대로 복사하지 않는다. 파일과 fragment 대상이 존재하는지도 확인한다.

## 워크플로우

### 1. EPUB 생성 (Calibre)

```bash
ebook-convert book_doc.html book.epub \
  --epub-version 3 \
  --disable-font-rescaling \
  --level1-toc '//h:h2' --level2-toc '//h:h3' --level3-toc '//h:h4' \
  --change-justification left \
  --cover cover.jpg
```

- `--level1-toc '//h:h2'` 등: h1이 장 표제가 아니라 책 제목일 때 필요하다.
  문서의 실제 제목 단계에 맞게 선택한다. h1이 장 제목인 문서에 이 예시를 그대로 적용하지 않는다.
- `--change-justification left`: 왼쪽 정렬을 원하는 경우의 옵션이다.
  양끝정렬이 요청되었다면 유지하고, 출력 형식별 지원 옵션을 확인한다.

### 2. 리디 규격 보정

```bash
python3 scripts/fix_epub_for_ridi.py book.epub
```

NCX 생성·OPF 연결, `./` 정리, html/body 크기·배경 속성 제거를 수행한다.
제자리 수정이므로 사본에서 먼저 실행하고, 수정 내역이 요청한 서식과 맞는지 확인한다.
명령의 `scripts/` 경로는 이 스킬 폴더 기준이다.

### 3. 검증

```bash
python3 scripts/check_ridi.py book.epub          # 공개 규칙 일부의 보조 검사
```

EPUB 표준 규격까지 확인하려면 epubcheck도 함께 돌린다. 스킬에 포함되어
있지는 않으니 아래 중 하나로 준비한다.

```bash
# Homebrew
brew install epubcheck
# 또는 W3C 릴리스 ZIP
# https://github.com/w3c/epubcheck/releases 에서 릴리스와 Java 요구사항 확인
java -jar /path/to/epubcheck.jar book.epub
```

`check_ridi.py`는 공개 규칙 일부를 구현한 보조 검사이며 공식 검증기 전체를
대체하지 않는다. EPUB3에서는 NCX가 선택 사항이므로 epubcheck의 NCX 누락
비검출은 표준 검사 실패가 아니다. 구조 검사 이후 실제 리디 앱에서 목차 이동·제목 여백·
글꼴 크기 변경·인용 표시를 확인한다. 앱을 확인하지 못했다면 그 한계를 알린다.

## 스캔본 서식 복원 (볼드·소제목·블록인용)

스캔본을 OCR/추출한 텍스트 레이어는 문자만 주고 원본의 굵게·소제목·블록인용은
사라진다. 상세한 실측값과 함정은 `references/scan-format-recovery.md`에 있다.
핵심만 옮기면 다음과 같다.

- **볼드**: 텍스트 레이어에 굵기 정보가 없으면 페이지를 400 dpi로 렌더한 뒤
  단어별 **수평 잉크 런 중앙값**으로 판정한다(실측 본문 ~5px, 볼드 ~9px).
  임계값은 그 책에서 다시 측정한다. 문자 오프셋을 계산할 때 단어 사이
  공백 1칸을 반드시 문자로 포함한다(빠뜨리면 볼드 위치가 밀린다).
- **소제목**: `?`·`!`로 끝나는 질문형 제목을 종결부호로 오인하면 전부 탈락한다.
  `looks_heading()`의 종결부호 목록에서 `?`·`!`를 제외한다.
- **블록인용**: 이 책은 **일반 문단도 첫 줄을 들여쓰므로 "들여쓰기=인용"이
  아니다.** 문단 내 **모든 줄**의 시작 x가 본문 기준선보다 오른쪽일 때만
  블록인용으로 본다. 첫 줄만 들여쓴 것(일반 문단·리스트 hanging indent)은 제외한다.
  초기 검출기 362개 → 최종 61개로 정정한 사례가 있다.
- **번역 적용**: 검출 JSON을 토큰 정렬로 청크에 대응시켜
  청크별 서식 가이드(`#### HEADINGS`/`BLOCKQUOTES`/`BOLD`)를 만들고,
  병렬 서브에이전트가 원문 대조로 `###`·`**`·`>` 마커를 삽입하게 한다.
- **검증**: 마커를 제거한 텍스트가 백업 본문과 문자 단위로 동일한지 확인한다.
  최종 EPUB의 `<strong>`·`<blockquote>`·헤딩 개수를 검출 결과와 대조한다.
- 출발점 스크립트: `scripts/detect_print_format.py` (페이지 범위·오프셋·
  머리글 높이는 책마다 조정).

### 기존 번역서의 전체 서식을 재검수할 때

- 구조 검사 통과와 원본 서식 일치는 별도로 확인한다. 요청 범위의 원본 페이지
  이미지를 대조하고, 의미상 강조된 이탤릭도 확인한다. 번역에서는 강조된 단어에
  대응하는 범위만 표시한다. 한 단어의 강조를 절 전체로 넓히지 않는다.
- 사각형 불릿이 `m`·`w`·`o`·`e@`·`=` 등으로 OCR되거나 통째로 누락될 수 있다.
  원본 이미지로 확인한 뒤 Markdown 목록으로 복원한다. 문자 모양만 보고
  전역 치환하지 않는다.
- 원본에서 이어지는 인용은 여러 문단과 출처를 함께 묶는다. 페이지 구분 주석
  때문에 인용이 갈라지지 않았는지 생성된 XHTML과 DOCX 인용 스타일을 확인한다.
- 본문 보존 검사는 적용이 확정된 변경 기록만 사용하고 초안은 제외한다.
  행·문단 문맥에서 치환 대상을 확인하고, 같은 행의 변경은 순서대로 검증한다.
  서식 변경은 마커 제거 전후의 본문이 같아야 한다. OCR 오류·머리글 제거 등
  의도한 본문 수정은 따로 기록해 백업과 비교한다.
- EPUB3 목차와 NCX를 각각 검사한다. NCX에만 제목 페이지 항목과 실제 책 제목
  항목이 중복되면 동일 제목임을 확인하고 제목 페이지의 `navPoint`만 제거한다.
  제목 페이지 XHTML·spine·나머지 항목은 보존하고 모든 목차 경로와 조각 식별자를
  검증한다.

## Calibre DOCX 변환에서 볼드 유실

Calibre가 HTML의 `<strong>`을 굵기 없는 캐릭터 스타일(`Text0`/`Text1`, 색상만
보유)로 매핑해 **DOCX에서 볼드가 사라지는 사례**가 있었다. `<em>`은 유사하게
`Text2`/`Text3`로 매핑되지만 이탤릭은 유지됐다.

해결: 생성된 DOCX의 `word/styles.xml`에서 `<w:b>`가 없는 색상 전용 캐릭터
스타일에 `<w:b/>`·`<w:bCs/>`를 주입한다. `scripts/fix_docx_bold.py`가 이
작업을 한다(인자로 docx 경로들). 빌드 파이프라인에서는 DOCX 생성 직후 호출한다.

- 별칭·사본으로 만든 DOCX(`사본.docx`)는 별도 파일이므로 그것도 fix하거나,
  재빌드 파이프라인이 항상 후처리하도록 한다.
- "TextN" id 휴리스틱은 도구 버전에 따라 다를 수 있으므로 전후로
  `styles.xml`과 실제 렌더를 확인한다. 이탤릭이 굵어지는 오탐이 보이면
  해당 styleId를 제외 목록에 넣는다.

## 서브에이전트로 번역·검수할 때

긴 책을 병렬로 번역할 때 서브에이전트를 쓰면 일관성·속도를 챙길 수 있다.
모델은 **상속 기본값**을 쓰고 spawn 시 모델을 하드코딩하지 않는다. 이 세션
설정에서 서브에이전트 기본 모델이 다른 모델로 잡혀 있어 의도치 않은 과금이
발생한 사례가 있으므로, spawn 전에 상속 모델을 확인한다. 검수(대조) 단계는
추론 수준을 높인 서브에이전트로 돌리는 편이 오역·누락 검출에 유리하다.

## Pandoc 따옴표와 목차 — 실제 제작에서 확인한 문제

한국어 서명·강조 표기의 번역 원칙은 `translate-long-text` 스킬을 따른다.
출력 단계에서는 서명 부호로 표시한 출판물 이름이 em으로 남지 않았는지,
EPUB의 em은 `font-style: normal; text-decoration: underline`, strong은 볼드인지
확인한다. DOCX도 em에 대응하는 텍스트가 밑줄이고 기울임꼴이 남지 않았는지
검사한다. 원문의 의미상 강조를 삭제하지 않고 표시 방식만 바꾼다.

- 한국어 곡선 따옴표가 이미 있는 원고에 `--from=markdown+smart`를 적용하면
  Pandoc 2.19.2에서 `‘싸게 사서 비싸게 팔라’가 그들의 기본 격언이다.`의
  여는 부호가 `’`로 바뀌었다. 인용 뒤 한국어 조사까지 포함해 재현했다.
  조사 없는 인용문 단독으로는 같은 문제가 나타나지 않았으므로 실제 문맥으로 확인한다. 이 경우 `--from=markdown-smart`로 자동 변환을 끄고,
  원고에 `‘…’`·`“…”`를 명시한다. 직선 따옴표는 문맥을 보고 변환하며
  `Workers’`, `O’Connor`, `’79` 같은 아포스트로피·연도 표기를 인용부호로 세지 않는다.
- 작은따옴표·큰따옴표의 개수만 같다고 통과시키지 않는다. 방향·짝·중첩을
  확인하고, 본문 XHTML/XML에서 추출한 부호 순서가 원고와 같은지 대조한다.
  OCR이 만든 가짜 여는 부호와 영문 연속 인용의 반복 여는 부호는 스캔을 확인한다.
- 자동 목차용 제목과 표지의 책 제목·부제를 구분한다. 표지용 제목을 일반 문단이나
  명시적인 비목차 대상으로 두어 책 제목이 두 번 등록되는 일을 막는다.
  생성된 nav와 NCX에서 실제 항목과 링크를 확인한다.
- 인용문이 여러 문단이나 원문 페이지 표지 주석을 통과하면 인용 구조를 확인한다.
  EPUB의 blockquote 범위와 DOCX의 인용 스타일에 출처까지 포함되는지 확인한다.

Pandoc 예시(기존 표지·메타데이터 옵션은 프로젝트에 맞게 추가):

```bash
pandoc book.md --from=markdown-smart --to=epub3 --toc \
  --toc-depth=3 --metadata=lang:ko --css=epub.css --output=book.epub
```

## 한국어 강조·서명 표기 (em→밑줄, strong→볼드)

한국어 본문은 의미 강조에 **이탤릭을 쓰지 않는다.** 다음을 지킨다.

- `em`(원문 `*...*`) → **밑줄**, `strong`(원문 `**...**`) → **볼드**.
- 책·소책자·잡지·신문 등 출판물 이름 → 《…》, 조문·법률·개별 글 제목 → 〈…〉.
  **한 문서에서 한 세트만** 쓴다(국립국어원). `『…』`(홑화살괄호)는 쓰지 않는다.
  서명을 나타내던 원문 이탤릭은 서명 부호로 바꾸면서 제거한다.
- CSS: `em, i { font-style: normal; text-decoration: underline; }`
- 블록인용도 한국어에서는 이탤릭으로 두지 않는다(`blockquote { font-style: normal }`).

### Calibre가 밑줄을 지우는 함정 (실측)

- 변환 준비 스크립트의 `* { text-decoration: none !important; }` 전역 규칙이
  **em 밑줄까지 제거한다.** 링크만 없애려면 `a { text-decoration: none !important }`로 한정한다.
- `<u>...</u>`는 Calibre가 밑줄 없는 `<span>`으로 바꾼다. 밑줄 강조는
  **`*em*`으로 마크다운에 남기고** CSS로 밑줄을 입히는 편이 안전하다.
- **DOCX**: Calibre가 `<em>`을 캐릭터 스타일(rStyle) 없이 평문 run으로 떨어뜨리는
  경우가 있다. 변환 후 `word/document.xml`에서 강조 run을 찾아
  `<w:u w:val="single"/>`를 주입한다(`scripts/fix_docx_bold.py --em-underline`).
  Calibre가 이탤릭을 `<w:i>` 캐릭터 스타일로 매핑한 경우에는 그 스타일을
  밑줄로 바꾼다(같은 스크립트의 `underline_italics`).
- 변환 후 **산출물에서** `text-decoration: underline` 규칙과 밑줄 run이 살아
  있는지 검사한다. HTML 단계에서 통과해도 변환기가 지울 수 있다.

### 표지 페이지 빈 장 함정

Calibre 기본 `titlepage.xhtml`은 `<img style="height: 100%">`를 쓴다. 부모 높이가
0으로 잡히는 뷰어에서 표지가 **빈 페이지**로 보인다. 이미지 스타일을
`max-width:100%;max-height:100%;width:auto;height:auto`로 바꾸고 body에
`height:100%`를 준다(`merge_and_build.py`의 titlepage 후처리 참조).

### 역자·기여자 메타데이터

Calibre `--book-producer`는 OPF `dc:contributor`에 `role=bkp`(book producer)로
들어간다. 번역서라면 이 값을 **역자(모델명 등)로 바꾸고 role을 `trl`(translator)로**
바꾼다. EPUB 후처리에서 `dc:contributor` 텍스트와 role refinement를 함께 고친다.
`--translator` 옵션을 파이프라인에 연결해 두면 빌드 때 자동 반영된다.

## 헤딩 CSS 템플릿

`references/heading-css.md`에 위계·패딩·`keep-all`이 적용된 완성 CSS가 있다.
핵심은 다음과 같다.

```css
h1, h2, h3, h4, h5, h6 {
    margin: 0;
    padding-top: 2.5rem;      /* 마진 표시 문제가 있으면 패딩으로 대체 */
    padding-bottom: 1rem;
    word-break: keep-all;     /* 한국어 단어 중간 줄바꿈 방지 */
    line-height: 1.35;
    page-break-after: avoid;
}
h1 { font-size: 2em;    }
h2 { font-size: 1.6em;  }
h3 { font-size: 1.3em;  }
h4 { font-size: 1.15em; }
h5 { font-size: 1em;    }
h6 { font-size: 0.9em;  }
```

공통 헤딩 패딩만 지정하고 크기를 생략하면 뷰어에서 h1과 h2가 같은 크기로
보일 수 있다. 단계별 크기를 명시하고 생성된 CSS의 실제 규칙과 헤딩 태그를
함께 검사한다. DOCX도 스타일 이름만 존재하는지 보지 말고 각 제목 문단의
스타일 연결·스타일 정의·단계별 크기를 확인한다. 납품 파일이 여러 폴더에
있으면 사용자가 여는 경로에도 최신 검수본이 반영되어 있는지 확인한다.

## 빌드 파이프라인에 통합할 때

여러 형식(docx/epub/pdf)을 한 HTML에서 만들면, EPUB 전용 옵션이 다른
형식에 영향을 주지 않도록 **포맷별 분기**에 넣는다. 그리고 생성된 EPUB에
대해 필요한 NCX 후처리와 검증을 EPUB 분기에 연결한다.

한 가지 함정: HTML 재생성 여부를 `output.md`의 mtime만으로 판단하면
**템플릿(CSS)만 고쳤을 때 재빌드가 건너뛰어진다.** 템플릿 mtime도 비교해야
한다.

## 표지 이미지

공개 검증기 설정의 표지 기준은 최소 560×800, 권장 1120×1600이다.
기본 비교 모드는 픽셀 면적이므로 축별 비교와 구분한다(`references/ridi-rules.md`).

기존 Calibre `--cover` 사례에서는 1120×1600 입력이 830×1186 정도로 축소됐다.
버전·옵션에 따라 달라지므로 출력 파일 안의 실제 크기를 확인한다. 로컬 검사
경고만으로 업로드 성공을 단정하지 않는다. 권장 크기를 지키고 싶으면
설치된 Calibre 버전의 표지 크기 옵션을 확인하거나 표지 이미지와 XHTML을
교체한다. 직접 교체할 때는 OPF의 cover-image 등록과 링크도 함께 확인한다.

## 참고 문서

- `references/ridi-rules.md` — 리디 검증기 오류 코드와 세부 기준값
- `references/heading-css.md` — 헤딩 CSS 전문과 근거
- `references/scan-format-recovery.md` — 스캔본 볼드·소제목·블록인용 복원 실측·함정

## 스크립트

- `scripts/check_ridi.py` — 공개 리디 규칙 보조 검사
- `scripts/fix_epub_for_ridi.py` — NCX 생성·OPF 연결·`./` 정리 등 보정
- `scripts/fix_docx_bold.py` — Calibre DOCX 변환 후 볼드 유실 복원
- `scripts/detect_print_format.py` — 스캔 PDF 서식(볼드·소제목·인용) 검출 출발점

## 주의

- 이 스킬은 EPUB 자체를 다룬다. 번역·OCR 등 원문 처리 파이프라인은
  `translate-long-text` 스킬을 함께 사용한다.
- 리디 규칙은 검증기 저장소(`ridi/ePub-Validator`) 기준이다. 현재 앱 동작은 따로 확인한다.
  출처·도구 버전·검증 범위를 기록하고 새 근거가 있을 때 기준을 갱신한다.
