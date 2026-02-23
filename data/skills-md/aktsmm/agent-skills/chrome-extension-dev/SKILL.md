---
name: chrome-extension-dev
description: "Chrome/ブラウザ拡張機能開発の包括的ガイド。WXTフレームワーク、Manifest V3、Chrome API、テスト手法をカバー。Use when: ブラウザ拡張機能を作成・修正する時。Triggers on 'ブラウザ拡張機能', 'Chrome拡張', 'browser extension', 'WXT', 'content script', 'service worker'."
---

# Chrome Extension Dev

ブラウザ拡張機能開発の包括的ガイド。

## When to Use

- **ブラウザ拡張機能を作りたい**、**Chrome拡張**、**browser extension**
- WXT フレームワークでの開発
- Content Script / Service Worker の実装
- Chrome API（tabs, storage, cookies等）の使用
- Manifest V3 への対応・移行

## 推奨技術スタック（2025/2026）

| カテゴリ         | 推奨                                 |
| ---------------- | ------------------------------------ |
| フレームワーク   | **WXT** (Vite ベース)                |
| フロントエンド   | React 18+ / Vue 3 / Svelte           |
| 言語             | TypeScript                           |
| スタイリング     | Tailwind CSS                         |
| UIコンポーネント | shadcn/ui / Mantine                  |
| 状態管理         | Zustand / Jotai                      |
| テスト           | Vitest (ユニット) + Playwright (E2E) |

## WXT クイックスタート

```bash
# 新規プロジェクト作成
npm create wxt@latest

# テンプレート指定
npm create wxt@latest -- --template react-ts
npm create wxt@latest -- --template vue-ts

# 開発コマンド
npm run dev    # HMR付き開発サーバー
npm run build  # プロダクションビルド
npm run zip    # ストア提出用パッケージ
```

## プロジェクト構成

```
project/
├── entrypoints/           # 自動検出エントリポイント
│   ├── background.ts      # Service Worker
│   ├── content.ts         # Content Script
│   ├── popup/             # Popup UI
│   │   ├── index.html
│   │   └── main.tsx
│   └── options/           # Options Page
├── components/            # 自動インポートUIコンポーネント
├── utils/                 # 自動インポートユーティリティ
├── public/                # 静的アセット（icon等）
├── wxt.config.ts          # WXT設定
└── package.json
```

## 主要 Chrome API

| API                  | 用途               | 権限                     |
| -------------------- | ------------------ | ------------------------ |
| `chrome.tabs`        | タブ操作           | `tabs` / `activeTab`     |
| `chrome.storage`     | データ永続化       | `storage`                |
| `chrome.runtime`     | メッセージング     | なし                     |
| `chrome.scripting`   | スクリプト/CSS注入 | `scripting` + host権限   |
| `chrome.cookies`     | Cookie操作         | `cookies` + host権限     |
| `chrome.offscreen`   | DOM操作（SW内）    | `offscreen`              |

→ 詳細: [references/chrome-api.md](references/chrome-api.md)

## Manifest V3 制限事項

| 制限               | 対処法                             |
| ------------------ | ---------------------------------- |
| 30秒タイムアウト   | `chrome.alarms` でウェイクアップ   |
| DOMアクセス不可    | `chrome.offscreen` を使用          |
| 永続化なし         | `chrome.storage.session` を使用    |
| eval()禁止         | 事前にバンドル                     |
| リモートコード禁止 | 全コードをバンドル                 |

→ 詳細: [references/manifest-v3.md](references/manifest-v3.md)

## 権限変更時の注意

> **⚠️ 重要**: `permissions`/`host_permissions`変更後は**拡張機能の再読み込みでは不十分**。
> 削除→再インストールが必要。

## Key References

| トピック         | リファレンス                                         |
| ---------------- | ---------------------------------------------------- |
| Chrome API 詳細  | [references/chrome-api.md](references/chrome-api.md) |
| Manifest V3      | [references/manifest-v3.md](references/manifest-v3.md) |
| テスト           | [references/testing.md](references/testing.md)       |
| 公開             | [references/publishing.md](references/publishing.md) |
| よくあるパターン | [references/patterns.md](references/patterns.md)     |

## Done Criteria

- [ ] WXT プロジェクト構成が正しい
- [ ] 必要な権限が `wxt.config.ts` に設定されている
- [ ] Manifest V3 制限を考慮した実装
- [ ] 開発モードで動作確認済み
- [ ] ビルドエラーがない

## External Resources

- [WXT 公式](https://wxt.dev)
- [Chrome Extension Docs](https://developer.chrome.com/docs/extensions)
- [Chrome API Reference](https://developer.chrome.com/docs/extensions/reference)
