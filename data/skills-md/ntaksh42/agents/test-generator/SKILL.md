---
name: test-generator
description: Generate comprehensive unit, integration, and E2E tests with edge cases, mocks, and assertions. Use when writing tests for functions, classes, APIs, or implementing TDD.
---

# Test Generator Skill

包括的なテストコードを自動生成するスキルです。

## 概要

このスキルは、ソースコードから高品質なユニットテスト、統合テスト、E2Eテストを自動生成します。テスト駆動開発（TDD）をサポートし、エッジケース、モック、アサーションを適切に含んだテストコードを作成します。

## 主な機能

- **ユニットテスト生成**: 関数・メソッド単位の詳細なテスト
- **統合テスト生成**: モジュール間の連携テスト
- **E2Eテスト生成**: エンドツーエンドのシナリオテスト
- **エッジケース網羅**: 境界値、null、例外ケース等を自動検出
- **モック生成**: 外部依存のモックオブジェクト作成
- **アサーション充実**: 期待値と実際の値の包括的な検証
- **テストデータ生成**: リアルなテストデータとフィクスチャ
- **カバレッジ最適化**: 高いコードカバレッジを達成
- **AAA パターン**: Arrange-Act-Assert の明確な構造
- **ドキュメント**: テストの目的と意図を説明するコメント

## サポートフレームワーク

### JavaScript/TypeScript
- **Jest**: React, Node.js の標準
- **Vitest**: Vite ベースの高速テスト
- **Mocha + Chai**: 柔軟な設定
- **Jasmine**: Angular の標準
- **Cypress**: E2E テスト
- **Playwright**: クロスブラウザテスト
- **Testing Library**: React Testing Library, Vue Testing Library

### Python
- **pytest**: モダンで強力
- **unittest**: 標準ライブラリ
- **doctest**: ドキュメント内テスト
- **nose2**: 拡張テストランナー
- **Robot Framework**: キーワード駆動テスト

### Java
- **JUnit 5**: 最新標準
- **TestNG**: 強力な設定
- **Mockito**: モックフレームワーク
- **AssertJ**: 流暢なアサーション
- **Spring Test**: Spring Boot テスト

### Go
- **testing**: 標準ライブラリ
- **testify**: アサーションとモック
- **ginkgo**: BDD スタイル
- **gomock**: モックジェネレーター

### その他
- **Rust**: cargo test
- **C#**: xUnit, NUnit, MSTest
- **Ruby**: RSpec, Minitest
- **PHP**: PHPUnit
- **Swift**: XCTest

## 使用方法

### 基本的なテスト生成

```
この関数のテストを生成してください：

function calculateTotal(items, taxRate) {
  return items.reduce((sum, item) => sum + item.price, 0) * (1 + taxRate);
}

フレームワーク: Jest
```

### クラス全体のテスト

```
このクラスの包括的なテストスイートを作成：
- すべてのメソッドをカバー
- エッジケースを含む
- モックを適切に使用

[クラスコード]
```

### APIエンドポイントのテスト

```
以下のAPIエンドポイントのテストを生成：

POST /api/users
- 成功ケース
- バリデーションエラー
- 認証エラー
- データベースエラー
```

### TDD スタイル

```
以下の要件からテストを先に生成（TDD）：

要件:
- ユーザー登録機能
- メールアドレスの検証
- パスワードのハッシュ化
- 重複登録の防止

フレームワーク: pytest
```

## テスト生成パターン

### 1. ユニットテスト

**入力**:
```typescript
export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency
  }).format(amount);
}
```

**生成されるテスト**:
```typescript
import { formatCurrency } from './currency';

describe('formatCurrency', () => {
  describe('正常系', () => {
    it('デフォルトでUSD形式でフォーマットする', () => {
      const result = formatCurrency(1234.56);
      expect(result).toBe('$1,234.56');
    });

    it('指定された通貨でフォーマットする', () => {
      const result = formatCurrency(1234.56, 'EUR');
      expect(result).toBe('€1,234.56');
    });

    it('整数もフォーマットする', () => {
      const result = formatCurrency(1000);
      expect(result).toBe('$1,000.00');
    });

    it('小数点以下を適切に処理する', () => {
      const result = formatCurrency(1234.567);
      expect(result).toBe('$1,234.57'); // 四捨五入
    });
  });

  describe('エッジケース', () => {
    it('0をフォーマットする', () => {
      const result = formatCurrency(0);
      expect(result).toBe('$0.00');
    });

    it('負の数をフォーマットする', () => {
      const result = formatCurrency(-1234.56);
      expect(result).toBe('-$1,234.56');
    });

    it('非常に大きな数をフォーマットする', () => {
      const result = formatCurrency(1234567890.12);
      expect(result).toBe('$1,234,567,890.12');
    });

    it('非常に小さな数をフォーマットする', () => {
      const result = formatCurrency(0.01);
      expect(result).toBe('$0.01');
    });
  });

  describe('異常系', () => {
    it('無効な通貨コードでエラーをスローする', () => {
      expect(() => formatCurrency(100, 'INVALID')).toThrow();
    });

    it('NaNを適切に処理する', () => {
      expect(() => formatCurrency(NaN)).toThrow();
    });

    it('Infinityを適切に処理する', () => {
      expect(() => formatCurrency(Infinity)).toThrow();
    });
  });
});
```

### 2. 統合テスト（API）

**入力**:
```python
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = get_current_user_id()
    order = Order.create(user_id, data['items'])
    return jsonify(order.to_dict()), 201
```

**生成されるテスト**:
```python
import pytest
from app import app, db
from models import User, Order, OrderItem

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def auth_headers(client):
    """認証済みユーザーのヘッダー"""
    user = User.create(email='test@example.com', password='password123')
    token = user.generate_token()
    return {'Authorization': f'Bearer {token}'}

class TestCreateOrder:
    """POST /api/orders のテスト"""

    def test_正常に注文を作成できる(self, client, auth_headers):
        """正常系: 有効なデータで注文を作成"""
        # Arrange
        order_data = {
            'items': [
                {'product_id': 1, 'quantity': 2, 'price': 1000},
                {'product_id': 2, 'quantity': 1, 'price': 2000}
            ]
        }

        # Act
        response = client.post(
            '/api/orders',
            json=order_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 201
        data = response.json
        assert 'id' in data
        assert 'created_at' in data
        assert len(data['items']) == 2
        assert data['total'] == 4000

    def test_認証なしで401エラー(self, client):
        """異常系: 認証ヘッダーなし"""
        response = client.post('/api/orders', json={'items': []})
        assert response.status_code == 401

    def test_空の注文でバリデーションエラー(self, client, auth_headers):
        """異常系: 注文アイテムが空"""
        response = client.post(
            '/api/orders',
            json={'items': []},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert 'items' in response.json['errors']

    def test_無効な商品IDでエラー(self, client, auth_headers):
        """異常系: 存在しない商品ID"""
        order_data = {
            'items': [{'product_id': 99999, 'quantity': 1, 'price': 100}]
        }
        response = client.post(
            '/api/orders',
            json=order_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_負の数量でバリデーションエラー(self, client, auth_headers):
        """エッジケース: 負の数量"""
        order_data = {
            'items': [{'product_id': 1, 'quantity': -1, 'price': 100}]
        }
        response = client.post(
            '/api/orders',
            json=order_data,
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_在庫不足の場合のエラー(self, client, auth_headers):
        """ビジネスロジック: 在庫不足"""
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1000, 'price': 100}]
        }
        response = client.post(
            '/api/orders',
            json=order_data,
            headers=auth_headers
        )
        assert response.status_code == 409
        assert 'stock' in response.json['message'].lower()

    def test_データベースエラーの処理(self, client, auth_headers, monkeypatch):
        """エラーハンドリング: DB接続エラー"""
        def mock_create(*args, **kwargs):
            raise DatabaseError("Connection failed")

        monkeypatch.setattr(Order, 'create', mock_create)

        response = client.post(
            '/api/orders',
            json={'items': [{'product_id': 1, 'quantity': 1, 'price': 100}]},
            headers=auth_headers
        )
        assert response.status_code == 500
```

### 3. E2Eテスト

**入力**:
```
ユーザー登録からログインまでのE2Eテストを生成：
フレームワーク: Playwright
```

**生成されるテスト**:
```typescript
import { test, expect } from '@playwright/test';

test.describe('ユーザー認証フロー', () => {
  test('新規ユーザー登録からログインまで', async ({ page }) => {
    // 1. 登録ページに移動
    await page.goto('/signup');
    await expect(page).toHaveTitle(/Sign Up/);

    // 2. 登録フォームに入力
    const timestamp = Date.now();
    const email = `test${timestamp}@example.com`;
    const password = 'SecurePassword123!';

    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);
    await page.fill('input[name="confirmPassword"]', password);
    await page.fill('input[name="name"]', 'Test User');

    // 3. 登録を実行
    await page.click('button[type="submit"]');

    // 4. 成功メッセージを確認
    await expect(page.locator('.success-message')).toBeVisible();
    await expect(page.locator('.success-message')).toContainText(
      'Registration successful'
    );

    // 5. 確認メールの検証（モック）
    // 実際の実装ではメールサービスのAPIをチェック

    // 6. ログインページに移動
    await page.goto('/login');

    // 7. ログイン情報を入力
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');

    // 8. ダッシュボードにリダイレクトされることを確認
    await expect(page).toHaveURL(/\/dashboard/);
    await expect(page.locator('.user-name')).toContainText('Test User');

    // 9. ユーザーメニューが表示されることを確認
    await page.click('.user-menu-toggle');
    await expect(page.locator('.user-menu')).toBeVisible();
    await expect(page.locator('.user-email')).toContainText(email);
  });

  test('無効なメールアドレスでエラー表示', async ({ page }) => {
    await page.goto('/signup');

    await page.fill('input[name="email"]', 'invalid-email');
    await page.fill('input[name="password"]', 'Password123!');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).toContainText(
      'Invalid email address'
    );
  });

  test('既存メールアドレスで登録エラー', async ({ page }) => {
    await page.goto('/signup');

    // 既に存在するメールアドレスを使用
    await page.fill('input[name="email"]', 'existing@example.com');
    await page.fill('input[name="password"]', 'Password123!');
    await page.fill('input[name="confirmPassword"]', 'Password123!');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message')).toContainText(
      'Email already registered'
    );
  });
});
```

### 4. モックの生成

**入力**:
```java
public class UserService {
    private UserRepository repository;
    private EmailService emailService;

    public User createUser(UserDto dto) {
        User user = repository.save(new User(dto));
        emailService.sendWelcomeEmail(user.getEmail());
        return user;
    }
}
```

**生成されるテスト**:
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository repository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private UserService userService;

    @Test
    void createUser_正常系_ユーザーを作成しウェルカムメールを送信() {
        // Arrange
        UserDto dto = new UserDto("test@example.com", "John Doe");
        User savedUser = new User(1L, "test@example.com", "John Doe");

        when(repository.save(any(User.class))).thenReturn(savedUser);
        doNothing().when(emailService).sendWelcomeEmail(anyString());

        // Act
        User result = userService.createUser(dto);

        // Assert
        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals("test@example.com", result.getEmail());
        assertEquals("John Doe", result.getName());

        // Verify interactions
        verify(repository, times(1)).save(any(User.class));
        verify(emailService, times(1)).sendWelcomeEmail("test@example.com");
    }

    @Test
    void createUser_異常系_リポジトリエラーでメール送信しない() {
        // Arrange
        UserDto dto = new UserDto("test@example.com", "John Doe");
        when(repository.save(any(User.class)))
            .thenThrow(new DatabaseException("Connection failed"));

        // Act & Assert
        assertThrows(DatabaseException.class, () -> {
            userService.createUser(dto);
        });

        // メールサービスが呼ばれないことを確認
        verify(emailService, never()).sendWelcomeEmail(anyString());
    }

    @Test
    void createUser_異常系_メール送信失敗時の処理() {
        // Arrange
        UserDto dto = new UserDto("test@example.com", "John Doe");
        User savedUser = new User(1L, "test@example.com", "John Doe");

        when(repository.save(any(User.class))).thenReturn(savedUser);
        doThrow(new EmailException("SMTP error"))
            .when(emailService).sendWelcomeEmail(anyString());

        // Act & Assert
        // メール送信失敗でもユーザーは作成される想定
        User result = userService.createUser(dto);
        assertNotNull(result);

        // または、メール送信失敗時に例外をスローする実装の場合
        // assertThrows(EmailException.class, () -> userService.createUser(dto));
    }
}
```

## テスト戦略

### テストピラミッド

```
        /\
       /E2E\       少数: 重要なユーザーフロー
      /------\
     /統合テスト\     中程度: モジュール間連携
    /----------\
   /ユニットテスト\   多数: 個別関数・メソッド
  /--------------\
```

### カバレッジ目標

- **ユニットテスト**: 80-90% のコードカバレッジ
- **統合テスト**: 主要なエンドポイント、モジュール連携
- **E2Eテスト**: クリティカルなユーザージャーニー

## テストデータ生成

### ファクトリーパターン

```python
# pytest fixture
@pytest.fixture
def user_factory():
    """ユーザーテストデータのファクトリー"""
    def _create_user(**kwargs):
        defaults = {
            'email': f'user{random.randint(1000, 9999)}@example.com',
            'name': 'Test User',
            'age': 25,
            'active': True
        }
        defaults.update(kwargs)
        return User(**defaults)
    return _create_user

def test_user_creation(user_factory):
    user1 = user_factory()
    user2 = user_factory(email='specific@example.com', age=30)
    assert user1.email != user2.email
    assert user2.age == 30
```

### フィクスチャ

```typescript
// Jest fixture
export const testUsers = {
  admin: {
    id: 1,
    email: 'admin@example.com',
    role: 'admin',
    permissions: ['read', 'write', 'delete']
  },
  regularUser: {
    id: 2,
    email: 'user@example.com',
    role: 'user',
    permissions: ['read']
  },
  inactiveUser: {
    id: 3,
    email: 'inactive@example.com',
    role: 'user',
    active: false
  }
};
```

## ベストプラクティス

### 1. テストの独立性

```typescript
// ❌ 悪い例: テスト間で状態を共有
let sharedUser;

test('create user', () => {
  sharedUser = createUser();
});

test('update user', () => {
  updateUser(sharedUser); // 前のテストに依存
});

// ✅ 良い例: 各テストが独立
test('create user', () => {
  const user = createUser();
  expect(user).toBeDefined();
});

test('update user', () => {
  const user = createUser(); // 独自にセットアップ
  updateUser(user);
  expect(user.updatedAt).toBeDefined();
});
```

### 2. 明確なテスト名

```python
# ❌ 悪い例
def test_user():
    pass

# ✅ 良い例
def test_create_user_with_valid_email_succeeds():
    pass

def test_create_user_with_invalid_email_raises_validation_error():
    pass
```

### 3. AAA パターン

```javascript
test('calculateDiscount applies 10% discount for premium users', () => {
  // Arrange (準備)
  const user = { type: 'premium' };
  const price = 1000;

  // Act (実行)
  const result = calculateDiscount(user, price);

  // Assert (検証)
  expect(result).toBe(900);
});
```

### 4. 適切なアサーション

```typescript
// ❌ 悪い例: 曖昧なアサーション
expect(result).toBeTruthy();

// ✅ 良い例: 具体的なアサーション
expect(result).toBe(true);
expect(result.status).toBe('success');
expect(result.data).toHaveLength(5);
expect(result.error).toBeUndefined();
```

## カスタマイズオプション

### テスト生成の詳細設定

```
以下の設定でテストを生成：

- フレームワーク: Jest
- カバレッジ目標: 90%
- エッジケース: 徹底的に
- モック: 外部API、データベース
- アサーションスタイル: expect
- ファイル命名: *.test.ts
- テストデータ: ファクトリーパターン使用
```

## 統合とCI/CD

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm test
      - run: npm run test:coverage
      - uses: codecov/codecov-action@v3
```

## 制限事項

- **ビジネスロジックの理解**: 要件の深い理解が必要なテストは人間の補完が必要
- **外部依存**: 実際の外部サービスとの統合テストは設定が必要
- **UI/UXテスト**: ビジュアル回帰テストは専用ツールが必要
- **パフォーマンステスト**: 負荷テストは別のツールが推奨

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
この関数の包括的なテストスイートを生成してください：

function validatePassword(password) {
  if (password.length < 8) return false;
  if (!/[A-Z]/.test(password)) return false;
  if (!/[a-z]/.test(password)) return false;
  if (!/[0-9]/.test(password)) return false;
  if (!/[!@#$%^&*]/.test(password)) return false;
  return true;
}

要件:
- フレームワーク: Jest
- エッジケースを網羅
- 各条件の境界値テスト
- わかりやすいテスト名
```

このプロンプトで、完全なテストスイートが生成されます！
