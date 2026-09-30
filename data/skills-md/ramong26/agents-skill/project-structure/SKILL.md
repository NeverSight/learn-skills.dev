---
name: project-structure
description: >-
  This skill should be used when the user asks how to organize or lay out code.
  It mandates a structure where one task maps to one folder: colocated domain
  folders, downward-only imports, cross-domain access through a public interface,
  and shared/ only for code used by two or more domains. Do not use for
  implementing the feature logic itself.
---

# Project Structure

**한 작업은 한 폴더 안에서 끝난다.** 이 구조의 목적은 에이전트가 요청을 받았을 때 폴더 하나만 열어도 필요한 코드가 전부 거기 있고, 나머지는 열어볼 필요가 없게 만드는 것이다. 아래 규칙은 예외 없이 적용한다.

## 1. 도메인 폴더 하나에 전부 모은다

한 기능에 필요한 코드는 기술 타입별로 흩지 않고 도메인 폴더 안에 함께 둔다.

아래는 `payment` 도메인을 예시로 든 것이다. 도메인 이름과 계층 이름은 프로젝트 용어에 맞추되, 계층 구성과 경계는 그대로 지킨다.

백엔드 예시:

```text
payment/
├── handler        # route / controller
├── service        # use case
├── repository     # 데이터 접근
├── model          # entity / schema
└── public         # 다른 도메인에 공개하는 것만
```

프론트엔드 예시:

```text
payment/
├── components
├── hooks
├── api
├── model          # type / schema
└── utils
```

`controllers/`, `services/`, `hooks/`, `types/`처럼 타입별로 전체를 묶는 최상위 폴더는 만들지 않는다. 그런 구조에서는 결제 하나를 고치려고 폴더 다섯 개를 열어야 한다.

폴더 이름은 요청에 쓰이는 말과 같게 짓는다. (예시: 결제 → `payment`, 로그인 → `auth`, 장바구니 → `cart`, 상품 → `product`, 문의 → `inquiry`, Header → `header` 또는 `layout`)

## 2. import는 위에서 아래로만 흐른다

```text
Route / Page          (상위)
   ↓
Service / Feature
   ↓
Repository / API Client
   ↓
Model / Type          (하위)
```

- 하위 계층은 상위 계층을 import하지 않는다. (repository가 service를, model이 handler를 부르지 않는다)
- 같은 계층끼리 서로 import하지 않는다.
- 순환 참조를 만들지 않는다.

한 방향이라서 아래로 따라가면 끝이 나오고, 위로 거슬러 올라갈 일이 없다.

## 3. 도메인 밖은 public 아니면 shared뿐

한 도메인 폴더가 밖에서 참조할 수 있는 것은 두 가지뿐이다.

```text
# 예시
payment/  →  other-domain/public/     (해당 도메인이 공개한 것만)
payment/  →  shared/                  (두 개 이상 도메인이 쓰는 것만)
```

- 다른 도메인의 `handler`, `service`, `repository`, `model`을 직접 import하지 않는다. 필요하면 그 도메인의 `public`에 추가한다.
- `shared/`는 실제로 두 개 이상 도메인이 쓰는 코드만 둔다. 한 도메인만 쓰면 그 도메인 안에 둔다.

## 4. 여러 도메인을 조율하는 로직은 별도 계층에 둔다

하나의 작업이 여러 도메인에 걸쳐 있으면 특정 도메인 하나에 책임을 몰아넣지 않는다. 조율 전용 위치를 만들고 거기서 각 도메인의 `public`만 호출한다.

조율 계층은 그 자체를 하나의 도메인처럼 두거나:

```text
# 예시
checkout/
```

또는 프로젝트에 맞는 이름의 계층으로 둔다.

```text
# 예시
application/
saga/
usecase/
orchestrator/
```

조율은 위에서 내려오는 방향으로만 한다.

```text
# 예시
CheckoutService
 ├── Order
 ├── Payment
 └── Inventory
```

- `OrderService`가 Payment와 Inventory까지 관리하게 만들지 않는다.
- 조율 계층은 각 도메인의 `public`만 호출하고, 도메인은 조율 계층을 import하지 않는다.
- 도메인끼리 직접 호출해 순서를 맞추지 않는다. 순서가 필요하면 조율 계층이 갖는다.

## 5. 새 코드를 배치할 때

1. 어느 도메인인지 정한다. 정해지지 않으면 도메인부터 나눈다.
2. 그 도메인 안에서 어느 계층인지 정한다.
3. 다른 도메인이 필요하면 그 도메인의 `public`만 쓴다. 없으면 추가한다.
4. 여러 도메인에 걸치면 어느 한 도메인이 아니라 조율 계층에 둔다.
5. 두 개 이상 도메인이 쓰게 되면 그때 `shared/`로 옮긴다. 미리 옮기지 않는다.
6. 이미 있는 abstraction과 중복되지 않는지 확인한다.

## 6. 기존 레포에 적용할 때

- 이미 확립된 구조와 naming convention이 있으면 그것을 우선하고, 그 안에서 위 규칙을 지킨다.
- 요청과 무관한 구조 개편을 함께 하지 않고, 변경 범위를 작게 유지한다.
- 기존 public interface를 불필요하게 바꾸지 않는다.
- 옮기는 이유를 위 규칙 중 하나로 설명할 수 있어야 한다. 취향으로 옮기지 않는다.
- 근거 없이 새로운 architecture pattern을 도입하지 않는다.

## 7. 검증

프로젝트에 있는 수단만, 변경 범위에 맞게 실행한다.

```text
architecture test
    ↓
type check
    ↓
lint
    ↓
관련 테스트
    ↓
build
```

의존 방향과 레이어를 검사하는 architecture test가 있으면 반드시 존중하고, 실패하면 실패가 가리키는 경계부터 고친다.

경계를 검사하는 수단이 없으면 문서만으로는 구조가 유지되지 않으므로 도입을 제안한다. 스택별 설정 예시는 `references/boundary-enforcement.md`에 있다.

## 8. 금지

- 타입별 최상위 폴더로 한 기능을 여러 폴더에 흩뜨리기
- 하위 계층이 상위 계층을 import (역방향 참조)
- 다른 도메인의 내부 구현 직접 import
- 도메인 간 순환 참조
- 한 도메인이 다른 도메인들을 조율하게 만들기 (조율은 별도 계층)
- 도메인이 조율 계층을 import하기
- 한 도메인만 쓰는 코드를 `shared/`에 두기
- `shared/`가 도메인 코드를 import하기
- 이미 있는 abstraction 중복 구현
- 요청과 무관한 구조 개편
