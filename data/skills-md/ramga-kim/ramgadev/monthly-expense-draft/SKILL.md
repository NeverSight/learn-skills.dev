---
name: monthly-expense-draft
description: 월간 경비청구 기안. Goworks 경비청구서 작성, 전자결재 경비 기안 요청 시 사용.
allowed-tools: mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_fill_form, mcp__plugin_playwright_playwright__browser_wait_for, mcp__plugin_playwright_playwright__browser_select_option, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_run_code, mcp__plugin_playwright_playwright__browser_file_upload, mcp__plugin_playwright_playwright__browser_network_requests, mcp__plugin_playwright_playwright__browser_tabs
compatibility: claude-code, gemini-cli, opencode, gpt-codex
metadata:
  category: finance-ops
  requires_browser_automation: "true"
  requires_receipt_images: "true"
---

# Goworks 경비청구서 기안

영수증 이미지에서 데이터를 추출하고 Goworks 경비청구서 기안 폼을 자동으로 채운다.

## Preconditions

- 브라우저 자동화 도구가 필요하다.
- 도구가 없으면 현재 환경에 맞는 provider 문서를 먼저 읽는다.
- 브라우저 자동화가 준비되지 않으면 폼 자동 입력 단계로 진행하지 않는다.

## First read

1. `workflow.md`
2. `skill-config.yaml` 또는 `skill-config.example.yaml`
3. 현재 실행 환경의 provider 문서

## Inputs

- 영수증 루트 경로는 최초 1회만 확인한다.
- 개인 설정값은 로컬에서만 채운다.
  - 이메일: `{YOUR_EMAIL}`
  - 패스워드: `{YOUR_PASSWORD}`
  - 영수증 루트 경로: `{YOUR_RECEIPT_ROOT_PATH}`

## 접속 정보

- 경비청구서 기안 URL: `https://www.goworks.co.kr/Approval/NewForm?templateid=2679`

### 로그인 처리

- 폼 제목이 보이면 로그인된 상태다.
- Microsoft 로그인으로 넘어가면 저장된 계정 정보로 로그인하거나 사용자에게 수동 로그인 안내를 한다.

## Workflow

### Phase 1: 입력과 폴더 준비

1. `receipt_root`가 없으면 한 번만 질문하고, 가능하면 `skill-config.yaml`에 저장한다.
2. 브라우저 워커는 답변을 기다리지 말고 먼저 Goworks 폼 접속과 로그인 상태 확인을 진행한다.
3. 전월 기준 대상 폴더를 정하고, 없으면 생성한다.
4. 영수증 처리는 이미지 파일(`jpg`, `jpeg`, `png`)만 대상으로 한다. `zip`, `7z`, `rar`, `pdf`, `xlsx`는 무시한다.
5. OCR은 별도 워커로 돌리고, 결과는 `{ date, amount, vendor, category }` 형식의 날짜 오름차순 JSON 배열로 받는다.

### Phase 2: 폼 입력과 첨부

1. 제목은 `[경비청구서] {전월}월 개인경비` 기본값을 사용한다.
2. 행 추가와 값 입력은 가능한 한 `browser_run_code` 한 번으로 일괄 처리한다.
3. 계정과목은 기본 `야근주말식대`, 지출구분은 기본 `개인`을 사용한다.
4. 영수증 이미지만 zip으로 압축해 첨부한다.
5. 업로드 확인과 DOM 세부 구조는 `reference/goworks-upload.md`를 따른다.

## Validation

- 폼 제목이 전월 기준으로 입력되어 있어야 한다.
- 내역 행 수가 영수증 건수와 일치해야 한다.
- 첨부 목록에 zip 파일명과 용량이 보여야 한다.
- 클라이언트 측 업로드 목록에 `File` 인스턴스가 존재해야 한다.

## 기본값

- 계정과목: `야근주말식대`
- 지출구분: `개인`
- 결재선, 참조, 보안구분, 보존연한은 서버 기본값을 따른다.

## Constraints

- 사용자에게 묻는 것은 루트 경로처럼 처음 한 번 필요한 값만 허용한다.
- 업무내용과 사업부는 사용자가 직접 보충하거나 미리 알려준 경우만 자동 입력한다.
- 상신 버튼은 절대 클릭하지 않는다.
- 상신 후 확인 단계 전에는 임시 zip 복사본을 삭제하지 않는다.

## References

- `workflow.md`
- `reference/goworks-upload.md`
