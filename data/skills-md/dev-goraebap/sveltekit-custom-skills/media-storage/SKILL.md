---
name: media-storage
description: "파일 업로드·저장소·첨부 관리 패턴. Actions: 파일 업로드, 이미지 업로드, 파일 처리, 저장소 연동, 썸네일 첨부, 색상 추출, file upload, image upload, storage, attachment, thumbnail. Patterns: Active Storage, blobs 테이블, attachments 테이블, 다형적 첨부, 중복 파일 감지. Storage: Cloudflare R2, AWS S3, @aws-sdk/client-s3, UUID key, 2-level 디렉토리, CDN URL, presigned URL. DB: Drizzle ORM, blob, checksum, MD5, metadata JSON, MIME, byte_size. Color: 지배적 색상 추출, dominant color, Gemini API, hex, blobs.metadata. Query: 썸네일 조회, 서브쿼리, leftJoin, view-model, CDN URL 변환."
allowed-tools: Bash Read Write Edit
metadata:
  author: dev-goraebap
---

# Media Storage

파일 업로드·저장소 연동·첨부 관리를 위한 패턴 모음. 특정 방식을 강제하지 않으며, 프로젝트 상황에 맞게 참고한다.

## 언제 적용하나

- 파일 또는 이미지 업로드 기능을 구현할 때
- 파일과 엔티티를 연결(첨부)하는 구조를 설계할 때
- Cloudflare R2 등 오브젝트 스토리지를 연동할 때
- 썸네일·색상 등 파일 메타데이터를 관리할 때
- 조회 시 파일 URL이나 색상 값을 함께 반환할 때

## 카테고리

| 카테고리 | 적용 상황 | 참조 파일 |
|----------|-----------|-----------|
| **DB 스키마** | blobs/attachments 테이블 설계, Drizzle ORM 스키마 작성 | [schema.md](references/schema.md) |
| **저장소** | R2/S3 클라이언트 초기화, 파일 업로드·삭제, 경로 분산 | [storage.md](references/storage.md) |
| **업로드** | 업로드 서비스 함수, 중복 감지, 지배적 색상 추출, 썸네일 첨부 | [upload.md](references/upload.md) |
| **조회** | 썸네일 서브쿼리, 뷰모델 변환, CDN URL·색상 값 포함 | [query.md](references/query.md) |

## 핵심 규칙 요약

### DB 스키마

- **blobs**: 파일 원본 메타데이터 (key, checksum, metadata JSON 등)
- **attachments**: 파일과 엔티티의 다형적 연결 (record_type, record_id, name)
- **checksum(MD5)** 으로 동일 파일 재사용 — blob은 하나만 저장

### 저장소

- R2는 AWS S3 SDK 호환 — `@aws-sdk/client-s3` 그대로 사용
- UUID key를 2-level 디렉토리(`ab/cd/key`)로 분산 저장
- 환경 변수: `R2_BUCKET_NAME`, `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_PUBLIC_URL`

### 업로드

- 비즈니스 로직은 프레임워크 무관 함수(`uploadMedia`)로 분리
- 이미지 업로드 시 Gemini API로 지배적 색상 추출 → `blobs.metadata` JSON에 저장
- 썸네일 교체 시 기존 첨부 삭제 후 재연결

### 조회

- 서브쿼리로 blob 정보를 함께 가져와 뷰모델로 변환
- `blobs.key` → CDN URL, `blobs.metadata` JSON → 색상 값 파싱

## 실행 방법

### Step 1: 작업 분류

| 요청 예시 | 카테고리 |
|-----------|----------|
| DB 테이블 설계, ORM 스키마 작성 | DB 스키마 |
| R2/S3 연동, 파일 업로드·삭제 구현 | 저장소 |
| 업로드 API, 중복 감지, 색상 추출, 첨부 연결 | 업로드 |
| 썸네일 URL·색상 포함 조회, 뷰모델 반환 | 조회 |
| 파일 업로드 전체 흐름 구현 | 모두 |

### Step 2: 참조 파일 로드

카테고리 테이블에서 해당 참조 파일을 읽는다. 스키마 정의와 코드 예시가 포함되어 있다.

### Step 3: 패턴 적용

참조 파일의 패턴을 프로젝트 스택에 맞게 적용한다. SQL 스키마, ORM 코드, 서비스 함수는 그대로 활용할 수 있다.
