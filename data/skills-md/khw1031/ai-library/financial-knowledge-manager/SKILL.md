---
name: financial-knowledge-manager
description: >
  재무 지식 스킬에 데이터를 추가/수정/관리합니다.
  재무 정보 추가, 데이터 추가, 지식 업데이트, 내용 추가,
  자료 추가, 정보 갱신, 참고자료 추가 요청 시 활성화.
---

# Financial Knowledge Manager

사용자가 제공한 재무 관련 데이터를 분석하여 적절한 지식 스킬의 references 파일에 라우팅하고 추가합니다.

## 스킬 라우팅 맵

| 주제 | 대상 스킬 | 추가 위치 |
|------|----------|----------|
| 투자/금융상품 | financial-investment-guide | references/products.md 또는 strategies.md |
| 세금/절세 | financial-tax-guide | references/income-tax.md, property-tax.md, gift-inheritance-tax.md |
| 보험/보장 | financial-insurance-guide | references/products.md 또는 coverage-analysis.md |
| 부채/대출 | financial-debt-management | references/loan-products.md 또는 repayment-strategies.md |
| 생애설계/은퇴/교육 | financial-life-planning | references/retirement.md 또는 major-expenses.md |
| 예산/지출/저축 | financial-budget-management | references/budget-worksheet.md 또는 expense-analysis.md |

모든 스킬 경로의 기준: `skills/` (프로젝트 루트 기준)

## 워크플로우

### 1단계: 데이터 분석

사용자가 제공한 데이터의 주제를 파악합니다.

- 복수 주제가 혼합된 경우 주제별로 분리
- 주제가 불명확하면 사용자에게 확인 요청

### 2단계: 대상 스킬 결정

위 라우팅 맵을 기반으로 대상 스킬과 파일을 결정합니다.

- 데이터 성격에 따라 적절한 파일 선택 (예: 상품 정보 → products.md, 전략 정보 → strategies.md)
- 해당 스킬 디렉토리가 존재하는지 확인

### 3단계: 대상 파일 읽기

```
Read skills/{대상 스킬}/references/{대상 파일}
```

- 파일이 없으면 새로 생성
- 기존 파일이 있으면 구조와 형식을 파악

### 4단계: 데이터 추가

기존 형식을 유지하며 적절한 섹션에 데이터를 추가합니다.

### 5단계: 검증

파일의 라인 수를 확인합니다.

- **500줄 초과** 시 파일 분할을 제안

## 데이터 추가 규칙

1. **기존 형식 유지**: 대상 파일의 마크다운 헤딩 구조, 리스트 스타일, 테이블 형식을 그대로 따름
2. **적절한 섹션에 추가**: 관련 섹션 하단에 추가, 새로운 카테고리면 섹션 신설
3. **테이블 구조 보존**: 기존 테이블에 행을 추가할 때 컬럼 정렬과 구분선 유지
4. **출처 명시**: 데이터 출처가 있으면 각주 또는 인라인으로 기록
5. **날짜 태그**: 추가 시점을 `<!-- updated: YYYY-MM-DD -->` 형식으로 섹션 상단에 기록
