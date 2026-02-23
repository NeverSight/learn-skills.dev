---
name: changelog-generator
description: Generate comprehensive changelogs from git history following Keep a Changelog format. Use when creating release notes or maintaining version history.
---

# Changelog Generator Skill

Gitコミット履歴から美しいChangelogを自動生成するスキルです。

## 概要

Git コミットメッセージを解析し、Conventional Commits形式やKeep a Changelog形式の整理されたChangelogを生成します。

## 主な機能

- **自動カテゴリ分類**: feat, fix, docs, refactor等
- **セマンティックバージョニング**: 変更内容からバージョン推定
- **Markdown/HTML出力**: 複数形式対応
- **リンク自動生成**: Issue, PR, コミットへのリンク
- **Breaking Changes検出**: 互換性のない変更を強調
- **Contributors リスト**: 貢献者の自動抽出
- **リリースノート**: プレスリリース形式の生成

## 使用方法

### 基本的なChangelog生成

```
Gitコミット履歴からChangelogを生成：
期間: v1.0.0..HEAD
形式: Keep a Changelog
```

### 詳細設定

```
Changelogを生成：
- 期間: 2024-01-01..2024-06-30
- 形式: Conventional Commits
- グループ化: タイプ別
- リンク: GitHub Issue, PR
- 貢献者リスト: 含める
```

## 出力例

### Keep a Changelog 形式

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.0] - 2024-06-15

### Added
- User authentication with JWT tokens (#123)
- Real-time notifications via WebSocket (#145)
- Dark mode support (#156)
- Export data to CSV feature (#167)

### Changed
- Improved search algorithm performance by 60% (#134)
- Updated UI design for better accessibility (#142)
- Migrated from REST to GraphQL for user API (#151)

### Fixed
- Fixed memory leak in file upload (#128)
- Resolved CORS issues on production (#139)
- Fixed pagination bug in user list (#147)

### Security
- Updated dependencies with known vulnerabilities (#155)
- Implemented rate limiting on API endpoints (#161)

### Deprecated
- `/api/v1/users` endpoint (use `/api/v2/users` instead) (#149)

## [2.0.0] - 2024-03-20

### Added
- Complete redesign of the admin dashboard
- Multi-language support (EN, JP, ES, FR)
- Two-factor authentication

### Changed
- **BREAKING**: Changed API response format from XML to JSON
- **BREAKING**: Renamed `getUserData()` to `fetchUser()`
- Minimum Node.js version is now 18.x

### Removed
- **BREAKING**: Removed deprecated `/api/legacy` endpoints
- Dropped support for IE11

## [1.5.2] - 2024-01-10

### Fixed
- Critical bug in payment processing
- Session timeout issues

## Contributors

Thank you to all contributors who made this release possible:
- @john-doe (15 commits)
- @jane-smith (12 commits)
- @developer123 (8 commits)

[Unreleased]: https://github.com/user/repo/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/user/repo/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/user/repo/compare/v1.5.2...v2.0.0
[1.5.2]: https://github.com/user/repo/releases/tag/v1.5.2
```

### Conventional Commits 形式

```markdown
# Release Notes - v2.1.0

**Release Date**: 2024-06-15

## 🚀 Features

- **auth**: Add JWT authentication system ([#123](https://github.com/user/repo/pull/123))
  - Implement token generation and validation
  - Add refresh token mechanism
  - Session management improvements

- **notifications**: Real-time WebSocket notifications ([#145](https://github.com/user/repo/pull/145))
  - Push notifications for important events
  - Configurable notification preferences

- **ui**: Dark mode support ([#156](https://github.com/user/repo/pull/156))
  - Theme toggle in user settings
  - Persists user preference

## 🐛 Bug Fixes

- **upload**: Fix memory leak in file upload handler ([#128](https://github.com/user/repo/pull/128))
- **api**: Resolve CORS configuration issues ([#139](https://github.com/user/repo/pull/139))
- **pagination**: Fix off-by-one error in user list ([#147](https://github.com/user/repo/pull/147))

## ⚡ Performance

- **search**: Improve search algorithm (60% faster) ([#134](https://github.com/user/repo/pull/134))
- **database**: Add indexes to frequently queried columns

## 📝 Documentation

- **api**: Update API documentation with new endpoints
- **readme**: Add contribution guidelines
- **examples**: Add code examples for authentication

## 🔒 Security

- **deps**: Update vulnerable dependencies ([#155](https://github.com/user/repo/pull/155))
- **api**: Implement rate limiting ([#161](https://github.com/user/repo/pull/161))

## 🎨 Refactoring

- **components**: Reorganize React components structure
- **types**: Improve TypeScript type definitions

## ⚠️ Breaking Changes

None in this release

## 📊 Statistics

- **Commits**: 47
- **Contributors**: 8
- **Files Changed**: 156
- **Lines Added**: 3,421
- **Lines Removed**: 1,892

## 🙏 Contributors

- @john-doe - 15 commits
- @jane-smith - 12 commits
- @developer123 - 8 commits
- @contributor456 - 6 commits
- @newbie789 - 3 commits
- @bugfixer - 2 commits
- @docs-writer - 1 commit
```

## Conventional Commits タイプ

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `style`: コードスタイル（フォーマット等）
- `refactor`: リファクタリング
- `perf`: パフォーマンス改善
- `test`: テスト追加・修正
- `chore`: ビルド、ツール等
- `ci`: CI設定
- `build`: ビルドシステム
- `revert`: 変更の取り消し

## カスタマイズ

```
Changelogを生成：

設定:
- スコープ: v2.0.0..v2.5.0
- 除外: "chore", "style"
- グループ化: モジュール別
- フォーマット: HTML
- テンプレート: カスタム
- Breaking Changes: 別セクションで強調
- リンク先: GitHub
```

## 統合

### GitHub Release

```
GitHub Releaseノートを生成：
タグ: v2.1.0
含める:
- What's Changed
- New Contributors
- Full Changelog link
```

### NPM/PyPI

```
npm/PyPI用のリリースノート生成：
バージョン: 2.1.0
ハイライト: 主要な機能と修正
インストール手順含む
```

## ベストプラクティス

1. **Conventional Commits使用**: 自動化しやすい
2. **セマンティックバージョニング**: バージョン番号に意味を持たせる
3. **定期的な更新**: リリース毎に更新
4. **ユーザー視点**: 技術的詳細より影響を記載
5. **Breaking Changes明記**: アップグレードガイド提供

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
最新リリースのChangelogを生成：
- 形式: Keep a Changelog
- 前回タグ: v2.0.0
- 現在: HEAD
- GitHub リンク含む
- 貢献者リスト含む
```

完全なChangelogが生成されます！
