---
name: fastapi-implementation
description: This skill should be used when the user asks to implement, add, or scaffold a new feature, router, or endpoint in a FastAPI backend — e.g. "FastAPI에 게시글 API 추가해줘", "이 엔드포인트 구현해줘", "add a new FastAPI router/endpoint", "implement this backend feature in FastAPI". It generates router/schema/model/service files following standard FastAPI project layout. Do not use for non-FastAPI backends, frontend work, or simple bug fixes.
---

# FastAPI Feature Implementation

> 이 스킬은 실제 프로젝트 코드에서 추출한 게 아니라 FastAPI 공식 문서와 커뮤니티에서
> 널리 쓰이는 표준 관례로 작성됐다. 실제로 이 스택을 쓰는 레포가 생기면 그 코드를
> 기준으로 다시 다듬는다. 그 전까지는 아래 구조를 기본값으로만 쓰고, 대상 레포에
> 이미 다른 컨벤션이 있으면 그것을 우선한다.

## 적용 전 확인

- 대상 레포에 이미 다른 폴더 구조가 있으면 이 스킬의 템플릿보다 그것을 우선한다.
- ORM(SQLAlchemy 등), 비동기 여부, 의존성 주입 방식을 기존 코드에서 먼저 확인한다.

## 폴더 구조 (도메인 기준)

```text
app/<feature>/
├── router.py        # APIRouter, 엔드포인트 정의
├── schemas.py         # Pydantic 요청/응답 모델
├── models.py           # ORM 모델 (SQLAlchemy 등)
└── service.py          # 비즈니스 로직
```

## 라우터

- 각 도메인은 자체 `APIRouter()`를 갖고, `app/main.py`에서 `app.include_router(<feature>_router, prefix="/<feature>", tags=["<feature>"])`로 등록한다.
- 엔드포인트 함수는 `response_model`을 명시해 응답 스키마를 고정한다.

## 스키마 (Pydantic)

- 요청/응답 모델을 `BaseModel` 서브클래스로 분리한다 (`<Feature>Create`, `<Feature>Response` 등). ORM 모델을 그대로 응답에 쓰지 않는다.
- ORM 모델에서 변환이 필요하면 `model_config = ConfigDict(from_attributes=True)`를 응답 스키마에 설정한다.

## 서비스와 의존성 주입

- 비즈니스 로직은 `service.py`에 함수 또는 클래스로 두고, 라우터에서 `Depends()`로 주입한다.
- DB 세션은 `Depends(get_db)` 같은 공용 의존성을 재사용한다. 이미 있는 세션 관리 방식을 새로 만들지 않는다.

### `Annotated` 매개변수 선언

`Annotated` 안에는 `Query(...)`, `Depends(...)` 같은 FastAPI 메타데이터를 넣고 기본값은 밖에 둔다.

```python
db: Annotated[Session, Depends(get_db)]
page: Annotated[int, Query(ge=1)] = 1
sort_by: Annotated[SortBy, Query(alias="sortBy")] = "dateTime"
```

- `Query(None)`과 `= Depends(get_db)`는 쓰지 않는다.
- alias는 기존 API 이름을 유지하고, 이미 있는 변환 함수를 재사용한다.

인증 의존성도 동일하다.

```python
credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]
db: Annotated[Session, Depends(get_db)]
```

상세 조회는 `None` 검사 후 기존 변환 함수를 호출한다.

```python
if meeting is None:
    raise NOT_FOUND_MEETING
return to_meeting_response(meeting)
```

Pylance가 표시하는 `(class) MeetingsResponse`나 `__pydantic_*` 목록은 Pydantic 클래스 정보이며 오류가 아니다.

## 에러 처리

- 실패 케이스는 `HTTPException(status_code=..., detail=...)`으로 명시적인 상태 코드와 함께 던진다.
- 레포에 이미 전역 예외 핸들러(`@app.exception_handler`)가 있으면 그 패턴을 따른다.

## DB 스키마 관리 (알려진 리스크)

- SQLAlchemy `Base.metadata.create_all()`을 프로덕션에서 그대로 쓰면 스키마 변경이 반영되지 않거나 예기치 않게 동작할 수 있다. 표준 관례는 Alembic으로 마이그레이션을 관리하는 것이다. 이 설정은 사용자가 명시적으로 요청하기 전에는 변경하지 않고, 스키마가 바뀌는 기능을 구현할 때만 위험을 알린다.

## 결과

새로 만든 파일 목록, `main.py`의 라우터 등록 여부, 실행한 검증(타입 체크·테스트)을 정리해 보여준다.
