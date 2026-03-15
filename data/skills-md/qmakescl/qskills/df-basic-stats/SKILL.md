---
name: df-basic-stats
description: >
  데이터프레임(DataFrame)의 기초 통계를 자동 산출하는 스킬.
  사용자가 CSV, Excel, Parquet 등 테이블 형식 데이터를 업로드하거나
  "기초 통계", "기술통계", "describe", "EDA", "데이터 요약", "분포 확인",
  "결측값 확인", "프로파일링" 등을 언급할 때 반드시 이 스킬을 사용한다.
  데이터 탐색, 변수 타입 파악, 결측 현황 확인, 연속형·정수형·범주형·날짜형
  별 맞춤 통계 산출, ydata-profiling 리포트 생성을 모두 포함한다.
  사용자가 "데이터 좀 봐줘", "이 파일 분석해줘" 같은 모호한 요청을 할 때도
  첫 단계로 이 스킬을 트리거하는 것이 좋다.
author: yoonani(from CultureLab, aka Q)
version: 2026-02-12
source: https://github.com/qmakescl/QSkills
---
 
# DataFrame 기초 통계 분석 스킬

## 개요

이 스킬은 사용자가 제공한 데이터프레임에 대해 **자동 타입 추론 → 타입별 맞춤 통계 산출 → 분포 프로파일링 리포트 생성**을 일관된 파이프라인으로 수행한다.

## 워크플로우

```
1. 데이터 로드       → 사용자 파일을 pd.DataFrame으로 읽기
2. 타입 추론         → 각 열을 4가지 타입으로 분류
3. 통계 산출         → 타입별 맞춤 통계 계산
4. 프로파일 리포트   → ydata-profiling HTML 생성
5. 결과 전달         → JSON 요약 + HTML 리포트를 사용자에게 제공
```

## 실행 방법

### Step 1: 의존성 확인

```bash
pip install pandas numpy matplotlib ydata-profiling --break-system-packages -q
```

ydata-profiling이 설치 실패하면 Step 4(프로파일 리포트)만 건너뛴다. matplotlib이 설치 실패하면 범주형 분포 차트만 건너뛴다. 나머지 통계 산출은 pandas/numpy만으로 동작한다.

### Step 2: 데이터 로드

사용자가 제공한 파일 경로에서 데이터를 로드한다.
파일 위치는 플랫폼마다 다르므로 환경에 맞게 결정한다:

| 환경 변수 / 관례 | 설명 |
|-----------------|------|
| `$UPLOAD_DIR` 또는 플랫폼 제공 경로 | 사용자 업로드 파일 위치 |
| `$OUTPUT_DIR` 또는 플랫폼 제공 경로 | 결과물 전달 위치 |
| 별도 경로 규칙이 없으면 | 현재 작업 디렉토리(CWD) 기준 |

```python
import pandas as pd

# 확장자에 따라 자동 선택
df = pd.read_csv(path)        # .csv
df = pd.read_excel(path)      # .xlsx, .xls
df = pd.read_parquet(path)    # .parquet
df = pd.read_json(path)       # .json
```

### Step 3: 통계 산출 스크립트 실행

메인 분석 스크립트를 실행한다. `$SKILL_DIR`은 이 스킬이 설치된 디렉토리 경로이다:

```bash
# 기본 실행 (JSON + MD + HTML + 차트 모두 자동 생성)
python $SKILL_DIR/scripts/compute_stats.py <input_file>

# HTML 리포트 없이
python $SKILL_DIR/scripts/compute_stats.py <input_file> --no-html

# MD 리포트 없이
python $SKILL_DIR/scripts/compute_stats.py <input_file> --no-md
```

출력 파일명은 입력 파일명에서 자동 결정된다:
- `{dataset_name}-stats.json` — 열별 통계 (구조화 데이터)
- `report/{dataset_name}-stats.md` — 기초통계 + 차트 + 인사이트 통합 리포트
- `{dataset_name}-ydata-profiling.html` — 상세 프로파일 리포트
- `charts/*.png` — 범주형 분포 차트 이미지

또는 Python에서 직접 import (sys.path에 스킬 디렉토리 추가 필요):

```python
import sys, os
sys.path.insert(0, os.path.join(os.environ.get("SKILL_DIR", "."), "scripts"))
from compute_stats import compute_basic_stats

result = compute_basic_stats(
    df,
    dataset_name="titanic",
    profile_report_path="titanic-ydata-profiling.html",
    chart_output_dir="./",
    md_output_path="titanic-stats.md",
)
```

### Step 4: 결과 전달

1. `{dataset_name}-stats.json` → 열별 통계 (구조화 데이터)
2. `{dataset_name}-stats.md` → 기초통계 + 차트 + 인사이트 통합 리포트 (**주 결과물**)
3. `{dataset_name}-ydata-profiling.html` → 상세 프로파일 리포트
4. `charts/*.png` → 범주형 분포 차트 이미지

에이전트는 **report/{dataset_name}-stats.md**를 읽어 사용자에게 텍스트로 설명하는 것을 기본으로 한다.

## 타입 추론 규칙

| 판정 순서 | 조건 | 분류 |
|-----------|------|------|
| 1 | `datetime64` dtype | `datetime` |
| 2 | 정수 dtype (numpy int, pandas Int) | `integer` |
| 3 | 실수 dtype (float) | `continuous` |
| 4 | object인데 80%+ 숫자 변환 가능 & 모두 정수 | `integer` |
| 5 | object인데 80%+ 숫자 변환 가능 & 소수점 포함 | `continuous` |
| 6 | object인데 80%+ 날짜 파싱 가능 | `datetime` |
| 7 | 그 외 전부 | `categorical` |

> 상세 추론 로직은 `references/type-inference.md` 참조.

## 타입별 산출 통계

| 통계 항목 | continuous | integer | categorical | datetime |
|-----------|:----------:|:-------:|:-----------:|:--------:|
| 응답수 (valid_count) | ✓ | ✓ | ✓ | ✓ |
| 결측수 (missing_count) | ✓ | ✓ | ✓ | ✓ |
| 결측률 (missing_rate) | ✓ | ✓ | ✓ | ✓ |
| 평균 (mean) | ✓ | ✓ | | |
| 표준편차 (std) | ✓ | ✓ | | |
| 중앙값 (median) | ✓ | ✓ | | |
| 최솟값 (min) | ✓ | ✓ | | ✓ |
| 최댓값 (max) | ✓ | ✓ | | ✓ |
| 최빈값 (mode) | | ✓ | ✓ | ✓ |
| 고유값 수 (unique_count) | | | ✓ | |
| 상위 빈도값 (top5_values) | | | ✓ (>8 범주) | |
| 분포 (distribution) | | | ✓ (≤8 범주) | |
| 분포 설명 (distribution_description) | | | ✓ (≤8 범주) | |
| 분포 차트 (distribution_chart) | | | ✓ (≤8 범주) | |

## 출력 형식

결과는 다음 JSON 구조로 반환된다:

```json
{
  "dataframe_shape": {"rows": 1000, "cols": 8},
  "columns": [
    {
      "column_name": "age",
      "inferred_type": "integer",
      "total_count": 1000,
      "valid_count": 985,
      "missing_count": 15,
      "missing_rate": 0.015,
      "mean": 42.3,
      "std": 14.2,
      "median": 41.0,
      "min": 18.0,
      "max": 75.0,
      "mode": 35
    }
  ],
  "profile_report": "report.html"
}
```

## 엣지 케이스 처리

- **빈 데이터프레임**: 행이 0개면 shape 정보만 반환하고 경고 메시지 출력
- **전체 결측 열**: 통계값을 모두 null로 반환
- **혼합 타입 열**: object로 처리 후 숫자/날짜 변환 시도 (80% 임계값 적용)
- **ydata-profiling 미설치**: 경고만 출력하고 프로파일 리포트 없이 나머지 통계 정상 반환
- **대용량 데이터 (>100만 행)**: profiling은 `minimal=True` 모드 강제 적용

## 플랫폼 경로 설정

이 스킬은 특정 플랫폼의 절대 경로에 의존하지 않는다.
각 에이전트 환경에서 아래 3가지 경로를 자신의 환경에 맞게 결정하면 된다:

| 변수 | 의미 | 예시 |
|------|------|------|
| `SKILL_DIR` | 이 스킬이 설치된 디렉토리 | `/mnt/skills/user/df-basic-stats` |
| `UPLOAD_DIR` | 사용자 파일 업로드 위치 | 플랫폼 제공 경로 또는 CWD |
| `OUTPUT_DIR` | 결과 파일 전달 위치 | 플랫폼 제공 경로 또는 CWD |

**플랫폼별 참고:**
- Anthropic Claude 컴퓨터: `UPLOAD_DIR=/mnt/user-data/uploads`, `OUTPUT_DIR=/mnt/user-data/outputs`
- OpenAI Code Interpreter: 둘 다 `/mnt/data/`
- 로컬 에이전트 (LangChain, Claude Code 등): 현재 작업 디렉토리(CWD) 기준

## 참고 문서

- `references/type-inference.md` — 타입 추론 알고리즘 상세 설명
- `references/output-schema.md` — 전체 출력 JSON 스키마 정의
- `scripts/compute_stats.py` — 메인 실행 스크립트 (CLI + 모듈)
