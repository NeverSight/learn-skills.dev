---
name: hwp-parser
description: 한글(HWP/HWPX) 문서를 다양한 포맷(Text, HTML, ODT, PDF)으로 변환하고, Markdown/HTML을 HWPX로 생성하는 작업을 도와줍니다. LLM/RAG 파이프라인을 위한 문서 처리, 청킹, LangChain 연동을 지원합니다.
---

# HWP Parser 개발 도우미

한글(HWP/HWPX) 문서를 읽고 변환하는 모든 작업을 도와줍니다. Python API와 CLI 도구를 제공하며, LLM 활용을 위한 워크플로우를 지원합니다.

## 환경 확인

1. **가상환경 활성화 확인**
   ```bash
   source venv/bin/activate  # 또는 .venv/bin/activate
   ```

2. **패키지 설치 확인**
   ```bash
   pip install -e .  # 개발 모드
   # 또는
   pip install hwpparser[all]  # 전체 기능
   ```

3. **시스템 의존성 확인**
   ```bash
   # PDF 변환 (Chrome headless 사용)
   # macOS - Chrome이 이미 설치되어 있으면 별도 설치 불필요
   brew install --cask google-chrome

   # Ubuntu/Debian
   sudo apt install google-chrome-stable
   # 또는 Chromium
   sudo apt install chromium-browser

   # HWPX 생성 (선택사항)
   brew install pandoc  # macOS
   sudo apt install pandoc  # Ubuntu
   ```

## 요청 분류

사용자 요청을 분석하여 해당하는 기능 파악:

| 키워드 | 기능 | 참조 |
|--------|------|------|
| 텍스트 추출, 읽기, 파싱 | HWP → Text | `hwp_to_text()` |
| HTML 변환, 웹페이지 | HWP → HTML | `hwp_to_html()` |
| ODT, OpenDocument | HWP → ODT | `hwp_to_odt()` |
| PDF 변환 | HWP → PDF | `hwp_to_pdf()` |
| 마크다운, 한글 생성 | Markdown → HWPX | `markdown_to_hwpx()` |
| 청킹, RAG, 벡터 DB | 문서 청킹 | `hwp_to_chunks()` |
| LangChain, 문서 로더 | LangChain 연동 | `HWPLoader` |
| 일괄 변환, 폴더 처리 | 배치 변환 | `batch_convert()` |
| 검색 인덱싱, JSONL | 인덱스 생성 | `export_to_jsonl()` |
| 메타데이터, 정보 추출 | 문서 메타데이터 | `extract_metadata()` |

## 작업 흐름

### 1. 단일 파일 변환
```python
import hwpparser

# HWP 읽기
doc = hwpparser.read_hwp("document.hwp")
print(doc.text)  # 텍스트
print(doc.html)  # HTML

# 파일로 저장
doc.to_odt("output.odt")
doc.to_pdf("output.pdf")

# 빠른 변환
text = hwpparser.hwp_to_text("document.hwp")
```

### 2. CLI 사용
```bash
# 텍스트 추출
hwpparser text document.hwp

# 포맷 변환
hwpparser convert document.hwp output.txt
hwpparser convert document.hwp output.pdf

# 일괄 변환
hwpparser batch ./hwp_files/ -f text -o ./text_files/

# 지원 포맷 확인
hwpparser formats
```

### 3. LLM/RAG 워크플로우
```python
# 청킹 (벡터 DB용)
chunks = hwpparser.hwp_to_chunks("document.hwp", chunk_size=1000)
for chunk in chunks:
    embedding = embed(chunk.text)
    vector_db.insert(embedding, chunk.metadata)

# LangChain 연동
from hwpparser import HWPLoader, DirectoryHWPLoader

loader = HWPLoader("document.hwp")
docs = loader.load()

# 폴더 전체
loader = DirectoryHWPLoader("./documents", recursive=True)
docs = loader.load()

# 검색 인덱싱 (Elasticsearch/Algolia)
hwpparser.export_to_jsonl("./documents", "./index.jsonl", chunk_size=1000)
```

### 4. 배치 처리
```python
# 폴더 내 모든 HWP → TXT
result = hwpparser.batch_convert("./hwp_files", "./text_files", "txt")
print(f"변환 완료: {result.success}/{result.total}")

# 모든 텍스트 합치기
all_text = hwpparser.batch_extract_text("./documents")
```

### 5. HWPX 생성
```python
# Markdown → HWPX
hwpparser.markdown_to_hwpx("# 제목\n내용", "output.hwpx")

# HTML → HWPX
hwpparser.html_to_hwpx("<h1>제목</h1><p>내용</p>", "output.hwpx")

# 통합 변환 인터페이스
hwpparser.convert("input.md", "output.hwpx")
hwpparser.convert("input.docx", "output.hwpx")
```

## 지원 변환

| 입력 → 출력 | 함수/CLI |
|------------|---------|
| HWP → Text | `hwp_to_text()`, `convert ... -f text` |
| HWP → HTML | `hwp_to_html()`, `convert ... -f html` |
| HWP → ODT | `hwp_to_odt()`, `convert ... -f odt` |
| HWP → PDF | `hwp_to_pdf()`, `convert ... -f pdf` |
| Markdown → HWPX | `markdown_to_hwpx()`, `convert file.md file.hwpx` |
| HTML → HWPX | `html_to_hwpx()` |
| DOCX → HWPX | `convert file.docx file.hwpx` |

## 주요 작업 예시

### 단일 파일 텍스트 추출
**요청**: "이 HWP 파일 내용 읽어줘"
```python
text = hwpparser.hwp_to_text("document.hwp")
print(text)
```

### 폴더 전체 일괄 변환
**요청**: "documents 폴더의 모든 HWP를 PDF로 변환해줘"
```python
result = hwpparser.batch_convert("./documents", "./pdf_output", "pdf")
print(f"성공: {result.success}, 실패: {result.failed}")
```

### RAG 파이프라인 구축
**요청**: "HWP 문서들을 청킹해서 벡터 DB에 넣을 수 있게 해줘"
```python
# 청킹
chunks = hwpparser.hwp_to_chunks("document.hwp", chunk_size=1000)

# 벡터화 및 저장
for chunk in chunks:
    embedding = your_embed_function(chunk.text)
    vector_db.insert({
        'embedding': embedding,
        'text': chunk.text,
        'metadata': chunk.metadata  # file, page, offset 등
    })
```

### LangChain 문서 로더
**요청**: "LangChain에서 HWP 문서들 사용하고 싶어"
```python
from hwpparser import DirectoryHWPLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 문서 로드
loader = DirectoryHWPLoader("./documents", recursive=True)
docs = loader.load()

# 청킹
splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
chunks = splitter.split_documents(docs)
```

### 검색 인덱스 생성
**요청**: "Elasticsearch에 넣을 JSONL 파일 만들어줘"
```python
hwpparser.export_to_jsonl(
    "./documents",
    "./search_index.jsonl",
    chunk_size=1000  # 청킹 포함
)
```

### 마크다운을 한글 문서로 변환
**요청**: "README를 HWPX로 만들어줘"
```python
hwpparser.convert("README.md", "README.hwpx")
```

### 메타데이터 추출
**요청**: "이 HWP 파일 정보 알려줘"
```python
meta = hwpparser.extract_metadata("document.hwp")
print(f"글자 수: {meta['char_count']}")
print(f"단어 수: {meta['word_count']}")
```

## 예외 처리

```python
from hwpparser.exceptions import (
    HWPFileNotFoundError,
    ConversionError,
    DependencyError,
    UnsupportedFormatError
)

try:
    result = hwpparser.convert("document.hwp", "output.pdf")
except HWPFileNotFoundError:
    print("파일을 찾을 수 없습니다")
except DependencyError as e:
    print(f"의존성 누락: {e}")
except ConversionError as e:
    print(f"변환 실패: {e}")
```

## 테스트

```bash
# 전체 테스트
pytest tests/ -v

# 특정 모듈 테스트
pytest tests/test_reader.py -v

# 커버리지
pytest tests/ --cov=hwpparser
```

## 참고 문서

- [API Reference](references/api.md)
- [CLI Guide](references/cli.md)
- [Workflows](references/workflows.md)
- [Troubleshooting](references/troubleshooting.md)

## 의존성 라이선스

**중요**: 이 프로젝트는 AGPL v3 라이선스의 `pyhwp` 라이브러리에 의존합니다.
- pyhwp: Copyright © 2010-2023 mete0r
- 라이선스: GNU Affero General Public License v3
- 저장소: https://github.com/mete0r/pyhwp
