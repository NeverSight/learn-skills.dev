---
name: backend-architecture-guidelines
description: 7-layer architecture design guidelines for Laravel applications. Covers layer responsibilities, dependency rules, and Laravel-native patterns. Reference this skill when planning backend architecture decisions during Phase 1 (Planning & Review).
---

# Backend Architecture Guidelines - 7-Layer Laravel-Native

This skill provides architectural guidelines for Laravel applications following a 7-layer Laravel-native architecture.

## Table of Contents
- [How to Use This Skill](#how-to-use-this-skill)
- [Architecture Overview](#architecture-overview)
- [Dependency Rules](#dependency-rules)
- [Layer Responsibilities](#layer-responsibilities)
- [Static Analysis with Deptrac](#static-analysis-with-deptrac)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Decision Framework](#decision-framework)
- [Architecture Decision Checklist](#architecture-decision-checklist)
- [Reference Documentation](#reference-documentation)

---

## How to Use This Skill

### Quick Reference - Phase 1: Architecture Planning

**Architecture Decision Checklist:**
- [ ] 要件から適切なレイヤーを決定 ([Layer Responsibilities](#layer-responsibilities))
- [ ] 依存関係ルールを検証 ([Dependency Rules](#dependency-rules))
- [ ] DTO設計（Laravel Data）を検討
- [ ] Repository の必要性を判断 ([Decision Framework](#decision-framework))
- [ ] Anti-patternsチェック ([Anti-Patterns](#anti-patterns-to-avoid))
- [ ] Deptrac設定を計画

**詳細な規約:**
- `.claude/rules/backend/` - レイヤー構造、DTO、テスト、コーディング規約の詳細

---

## Architecture Overview

```
7層レイヤードアーキテクチャ（Laravel-native）

┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
│               (Controller, Middleware, Inertia)             │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Request Layer                            │
│                (FormRequest, Validation)                    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     UseCase Layer                            │
│                  (Business Logic, DTO)                      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                            │
│                 (Shared/Reusable Logic)                     │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Repository Layer                          │
│              (Data Access Abstraction)                      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Model Layer                             │
│                  (Eloquent Models)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Resource Layer                            │
│               (JSON Response Transformation)                │
└─────────────────────────────────────────────────────────────┘
```

### ディレクトリ構造 (`app/` 配下にフラット配置)

```
app/
├── Http/
│   ├── Controllers/
│   │   ├── Api/              # API Controllers（REST API）
│   │   └── Web/              # Web Controllers（Inertia.js用）
│   ├── Requests/             # FormRequests（バリデーション）
│   └── Resources/            # API Resources（JSONレスポンス）
├── UseCases/                 # UseCases（ビジネスロジック）
│   └── {Resource}/
│       ├── Create{Resource}UseCase.php
│       └── Update{Resource}UseCase.php
├── Services/                 # Services（共通ロジック）
├── Repositories/             # Repositories（データアクセス）
│   └── {Resource}/
│       ├── {Resource}RepositoryInterface.php
│       └── {Resource}Repository.php
├── Data/                     # DTOs（Laravel Data）
│   └── {Resource}/
│       ├── Create{Resource}Data.php
│       └── Update{Resource}Data.php
├── Models/                   # Eloquent Models
├── Policies/                 # Policies（認可）
└── Enums/                    # Enums（列挙型）
```

---

## Dependency Rules

### 基本ルール
**依存は上位層から下位層への一方向のみ**

```
Presentation → Request → UseCase → Service/Repository → Model → Resource
```

### 各レイヤーの依存関係

| レイヤー | 依存可能 | 依存禁止 |
|---------|----------|----------|
| **Presentation (Controllers)** | Request, UseCase, Resource | Model直接, Service直接 |
| **Request (FormRequests)** | DTO (Laravel Data) | Model, UseCase |
| **UseCase** | Repository Interface, Service, Policy | Controller, Request |
| **Service** | Repository, Model | Controller, UseCase |
| **Repository** | Model | Controller, UseCase |
| **Model** | なし（最下層） | 全ての上位層 |
| **Resource** | Model | Controller, UseCase |

---

## Layer Responsibilities

### 各層の責務一覧

| レイヤー | 責務 | 配置 |
|---------|------|------|
| **Presentation** | HTTP Request/Response, 認可チェック | `app/Http/Controllers/` |
| **Request** | バリデーション、DTO変換 | `app/Http/Requests/` |
| **UseCase** | ビジネスロジック、トランザクション制御 | `app/UseCases/` |
| **Service** | 汎用的なビジネスロジック（複数UseCaseで共有） | `app/Services/` |
| **Repository** | データアクセス抽象化、複雑なクエリ | `app/Repositories/` |
| **Model** | ドメインモデル、リレーション定義 | `app/Models/` |
| **Resource** | JSONレスポンス整形 | `app/Http/Resources/` |

### Web Controllers vs API Controllers

| 種別 | 責務 | 命名 |
|------|------|------|
| **Web Controller** | 初期ページ描画、静的マスターデータ提供 | `{Resource}PageController` |
| **API Controller** | CRUD操作、動的データ処理 | `{Resource}Controller` |

📖 **詳細**: `.claude/rules/backend/02-layers.md`

---

## Static Analysis with Deptrac

Deptrac を使用してアーキテクチャ境界を静的解析で検証する。

```yaml
# deptrac/layer.yaml
deptrac:
  paths:
    - ./app
  layers:
    - name: Presentation
      collectors:
        - type: directory
          value: app/Http/Controllers
    - name: Request
      collectors:
        - type: directory
          value: app/Http/Requests
    - name: UseCase
      collectors:
        - type: directory
          value: app/UseCases
    - name: Service
      collectors:
        - type: directory
          value: app/Services
    - name: Repository
      collectors:
        - type: directory
          value: app/Repositories
    - name: Model
      collectors:
        - type: directory
          value: app/Models
    - name: Resource
      collectors:
        - type: directory
          value: app/Http/Resources

  ruleset:
    Presentation:
      - Request
      - UseCase
      - Resource
    Request:
      - Data
    UseCase:
      - Repository
      - Service
      - Policy
    Service:
      - Repository
      - Model
    Repository:
      - Model
    Resource:
      - Model
    Model: []
```

```bash
# 検証コマンド
./vendor/bin/deptrac analyse --config-file=deptrac/layer.yaml
```

---

## Anti-Patterns to Avoid

### 1. Controller でのビジネスロジック
```php
// ❌ WRONG
class PostController extends Controller
{
    public function store(Request $request)
    {
        // ビジネスロジックがControllerに
        if (Post::where('user_id', auth()->id())->count() > 10) {
            throw new \Exception('Limit exceeded');
        }
        $post = Post::create($request->all());
        return response()->json($post);
    }
}

// ✅ CORRECT
class PostController extends Controller
{
    public function store(StorePostRequest $request, CreatePostUseCase $useCase)
    {
        $data = $request->getCreatePostData();
        $post = $useCase->execute($data);
        return response()->json(new PostResource($post), 201);
    }
}
```

### 2. UseCase での HTTP 依存
```php
// ❌ WRONG
class CreatePostUseCase
{
    public function execute(Request $request): Post  // HTTP依存
    {
        return Post::create($request->all());
    }
}

// ✅ CORRECT
class CreatePostUseCase
{
    public function execute(CreatePostData $data): Post  // DTOを使用
    {
        return $this->repository->create(...);
    }
}
```

### 3. Web Controller での動的データ提供
```php
// ❌ WRONG
class PostPageController extends Controller
{
    public function index()
    {
        return Inertia::render('Post/Index', [
            'posts' => Post::all(),  // 動的データをWeb Controllerで
        ]);
    }
}

// ✅ CORRECT
class PostPageController extends Controller
{
    public function index()
    {
        return Inertia::render('Post/Index', [
            'statusOptions' => PostStatus::toSelectArray(),  // 静的データのみ
        ]);
        // 動的データはReact側からAPI経由で取得
    }
}
```

---

## Decision Framework

### Repository を作成すべきケース

| ケース | 理由 |
|--------|------|
| 複雑なクエリ | 複数テーブル結合、サブクエリ、集計処理 |
| トランザクション制御 | 複数のDB操作を1つのトランザクションで管理 |
| テスト容易性 | モック可能なインターフェース提供 |

### Repository を作成しなくても良いケース

| ケース | 理由 |
|--------|------|
| シンプルな CRUD | Eloquent の標準機能で十分 |
| 単一モデル操作 | 複雑なクエリロジックがない |

📖 **詳細**: `.claude/rules/backend/02-layers.md`

### Service を作成すべきケース

| ケース | 例 |
|--------|-----|
| 複数UseCase間で共有されるロジック | ファイルエクスポート、通知送信 |
| 外部サービス連携 | API呼び出し、メール送信 |
| 複雑な計算処理 | レポート集計、統計計算 |

---

## Architecture Decision Checklist

### レイヤー配置
- [ ] コードは正しいレイヤーに配置されているか？
- [ ] 依存方向は上位→下位の一方向か？
- [ ] ビジネスロジックは UseCase に集約されているか？

### Controller 設計
- [ ] Controller は HTTP handling のみか？
- [ ] UseCase を呼び出しているか？
- [ ] Web Controller は静的データのみ提供しているか？

### UseCase 設計
- [ ] Input DTO (Laravel Data) を使用しているか？
- [ ] Repository Interface 経由でアクセスしているか？
- [ ] HTTP 依存がないか？

### Repository 設計
- [ ] Interface と Implementation が分離されているか？
- [ ] トランザクション制御が適切か？
- [ ] Eloquent Model を返しているか？

### DTO 設計
- [ ] `#[TypeScript()]` attribute が付与されているか？
- [ ] `readonly` property を使用しているか？
- [ ] FormRequest に DTO 変換メソッドがあるか？

---

## Reference Documentation

詳細な実装ガイドと例:

- **`.claude/rules/backend/01-overview.md`** - アーキテクチャ全体像
- **`.claude/rules/backend/02-layers.md`** - 各レイヤーの詳細責務とコード例
- **`.claude/rules/backend/03-dto-data.md`** - Laravel Data による DTO 実装
- **`.claude/rules/backend/04-typescript-generation.md`** - TypeScript 型生成
- **`.claude/rules/backend/05-inertia-backend.md`** - Inertia.js バックエンド実装
- **`.claude/rules/backend/06-testing.md`** - テスト戦略
- **`.claude/rules/backend/07-best-practices.md`** - ベストプラクティス
- **`.claude/rules/backend/08-coding-standards.md`** - コーディング規約
