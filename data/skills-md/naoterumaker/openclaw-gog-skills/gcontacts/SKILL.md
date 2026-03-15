---
name: gcontacts
description: >
  Google 連絡先操作（検索・作成・更新・削除）を gog CLI (v0.10.0) で行う。
  「連絡先検索」「〇〇さんの電話番号」「連絡先追加」「連絡先一覧」
  「アドレス帳から探して」「連絡先を更新」などで発火。
---

# Google Contacts 操作スキル (gog v0.10.0)

gog CLI でGoogle連絡先を操作する。

**実行パス:** `gog`

**認証アカウント:** (gogで認証したアカウント)

## Execution Notes

- `exec` ツールで実行時、`timeout: 60` を指定

---

## 連絡先検索

### 名前・メール・電話で検索

```bash
gog contacts search "田中"
gog contacts search "tanaka@example.com"
gog contacts search "090-1234"
```

### 検索結果を絞り込み

```bash
gog contacts search "山田" --max 10
```

---

## 連絡先一覧

```bash
gog contacts list
gog contacts list --max 50
gog contacts list --json
```

---

## 連絡先詳細

```bash
gog contacts get <resourceName>

# resourceNameは "people/c12345678" のような形式
```

---

## 連絡先作成

### 基本

```bash
gog contacts create --name "山田太郎"
```

### フル情報

```bash
gog contacts create \
  --name "山田太郎" \
  --email "yamada@example.com" \
  --phone "090-1234-5678"
```

### 複数メール・電話

```bash
gog contacts create \
  --name "佐藤花子" \
  --email "sato@company.com" \
  --email "sato.personal@example.com" \
  --phone "090-1111-2222" \
  --phone "03-1234-5678"
```

---

## 連絡先更新

```bash
gog contacts update <resourceName> --name "新しい名前"
gog contacts update <resourceName> --email "new@example.com"
gog contacts update <resourceName> --phone "080-9999-8888"
```

---

## 連絡先削除

```bash
gog contacts delete <resourceName>
gog contacts delete <resourceName> --force  # 確認スキップ
```

---

## ディレクトリ連絡先（組織の連絡先）

```bash
# 組織ディレクトリの一覧
gog contacts directory list

# ディレクトリ検索
gog contacts directory search "部署名"
```

---

## その他の連絡先

```bash
# その他の連絡先一覧
gog contacts other list
```

---

## 作成オプション一覧

| オプション | 説明 |
|-----------|------|
| `--name` | 名前 |
| `--email` | メールアドレス（複数可） |
| `--phone` | 電話番号（複数可） |
| `--organization` | 会社名 |
| `--title` | 役職 |
| `--note` | メモ |

---

## 出力オプション

| オプション | 説明 |
|-----------|------|
| `--json` | JSON出力 |
| `--plain` | TSV出力 |
| `--max N` | 最大N件 |

---

## resourceName について

連絡先のIDは `resourceName` 形式:
- `people/c12345678901234567890`

`list` や `search` の結果から取得できる。

---

## 典型ワークフロー

### 連絡先検索→情報取得

```bash
# 1. 検索
gog contacts search "田中" --json

# 2. 詳細取得
gog contacts get "people/c1234567890"
```

### 新規連絡先作成

```bash
gog contacts create \
  --name "新規顧客 株式会社ABC" \
  --email "contact@abc-corp.com" \
  --phone "03-1234-5678" \
  --organization "株式会社ABC" \
  --title "営業部長" \
  --note "2026年2月商談開始"
```

### 連絡先更新

```bash
# 電話番号変更
gog contacts update "people/c1234567890" --phone "080-新番号"
```

---

## 注意事項

- **resourceName**: 操作には正確なresourceNameが必要
- **重複**: 同名の連絡先は複数作成可能
- **同期**: 変更は即時反映
- **削除**: 完全削除（ゴミ箱なし）
