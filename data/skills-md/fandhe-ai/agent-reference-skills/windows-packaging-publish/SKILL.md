---
name: windows-packaging-publish
description: >
  Windows アプリ開発 (MSIX / Microsoft Store) のパッケージング・配置・公開リファレンス。
  MSIX, AppxManifest, MakeAppx, MSIX Packaging Tool, Package Bundles, App Attach,
  Package Support Framework, Package Identity, PackageFamilyName, PackageManager,
  スパースパッケージ, App Installer, サイドローディング, Windows App SDK Bootstrapper,
  自己完結型デプロイ, SignTool, Azure Trusted Signing (Azure Artifact Signing), 証明書, CI/CD 署名,
  Partner Center, アプリ送信, 年齢レーティング, ストアリスティング, 段階的ロールアウト,
  StoreContext, msstore CLI, 認定プロセス, 分析レポート。
user-invocable: false
---

# Windows パッケージング・公開 リファレンス

Windows アプリを MSIX 化して配布・デプロイし、Microsoft Store に公開するための公式ドキュメントを蒸留したリファレンス。
パッケージ作成、パッケージ ID、配置アーキテクチャ、コード署名、ストア送信・審査・分析までを網羅する。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/windows-packaging-publish/
  SKILL.md
  references/
    msix-packaging/
      README.md
      app-streaming-install.md
      appv-vs-msix-comparison.md
      asset-packages.md
      create-psf-fixup.md
      differential-package-updates.md
      framework-packages.md
      makeappx-cli.md
      modification-packages.md
      msix-app-attach.md
      msix-containerization-overview.md
      msix-overview.md
      msix-packaging-tool.md
      msix-sdk.md
      msix-toolkit.md
      optional-packages.md
      package-asset-requirements.md
      package-bundles-architecture.md
      package-extensions-guide.md
      package-manifest-schema.md
      package-structure.md
      package-support-framework.md
      resource-packages.md
      single-project-msix.md
      unsigned-package.md
      vs-packaging-project.md
    package-identity/
      README.md
      apis-requiring-package-identity.md
      detect-package-identity.md
      get-activation-info-for-packaged-apps.md
      integrate-packaged-app-with-file-explorer.md
      package-class.md
      package-id-class.md
      package-identity-overview.md
      package-manager.md
      package-uninstall-update.md
      packaged-vs-unpackaged-behavior.md
      persistent-identity.md
      sparse-packages-external-location.md
    deployment/
      README.md
      app-installer-file-overview.md
      app-installer-troubleshooting.md
      app-installer-update-settings.md
      choose-distribution-path.md
      dotnet-deployment-models.md
      enterprise-deployment-intune.md
      enterprise-deployment-tools.md
      gradual-package-rollout.md
      package-folding.md
      shared-package-container.md
      sideloading-prerequisites.md
      store-package-code-driven-update.md
      tamper-protection.md
      windows-app-sdk-bootstrapper-api.md
      windows-app-sdk-deploy-packaged-apps.md
      windows-app-sdk-deploy-unpackaged-apps.md
      windows-app-sdk-deployment-architecture.md
      windows-app-sdk-runtime-version-management.md
      windows-app-sdk-self-contained-deploy.md
    code-signing/
      README.md
      azure-key-vault-signing.md
      azure-trusted-signing.md
      certificate-types.md
      cicd-signing.md
      device-guard-signing.md
      msix-signing-requirements.md
      self-signed-certificate.md
      signing-troubleshooting.md
      signtool-sign.md
      signtool-timestamp.md
      signtool-verify.md
      smartscreen-reputation.md
    store-publish/
      README.md
      acquisitions-report.md
      add-on-submission.md
      additional-information.md
      age-ratings.md
      analytics-overview.md
      app-certification-process.md
      app-package-requirements.md
      app-performance-insights.md
      app-properties.md
      attract-and-promote.md
      create-app-submission.md
      developer-account.md
      distribute-win32-app.md
      gradual-package-rollout.md
      health-report.md
      manage-submission-options.md
      market-selection.md
      msi-exe-publishing.md
      msi-manual-package-validation.md
      msstore-cli.md
      package-flights.md
      pricing-and-availability.md
      product-page-experiments.md
      publish-app-update.md
      pwa-submission.md
      ratings-reviews-report.md
      remove-app-and-addon.md
      reserve-app-name.md
      resolve-submission-errors.md
      responsible-ai-faq-ai-generated-keywords.md
      screenshots-and-images.md
      store-context.md
      store-listings.md
      store-policies.md
      store-product.md
      submission-api-msi.md
      submission-api-msix.md
      upload-app-packages.md
      usage-report.md
      visibility-options.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| MSIX パッケージの構造・AppxManifest スキーマを理解したい | msix-packaging | [references/msix-packaging/README.md](references/msix-packaging/README.md) |
| MakeAppx / MSIX Packaging Tool / Visual Studio でパッケージを作成したい | msix-packaging | [references/msix-packaging/README.md](references/msix-packaging/README.md) |
| パッケージバンドル・App Attach・Package Support Framework を扱いたい | msix-packaging | [references/msix-packaging/README.md](references/msix-packaging/README.md) |
| MSIX コンテナ化の仕組み・App-V との比較・MSIX Toolkit/SDK を調べたい | msix-packaging | [references/msix-packaging/README.md](references/msix-packaging/README.md) |
| パッケージ ID の5要素・PackageFamilyName・PackageFullName を理解したい | package-identity | [references/package-identity/README.md](references/package-identity/README.md) |
| Package / PackageId / PackageManager クラスで実行時にパッケージ情報を取得・操作したい | package-identity | [references/package-identity/README.md](references/package-identity/README.md) |
| スパースパッケージで非パッケージアプリにパッケージ ID を付与したい | package-identity | [references/package-identity/README.md](references/package-identity/README.md) |
| パッケージ化デスクトップアプリに File Explorer コンテキストメニューを統合したい | package-identity | [references/package-identity/README.md](references/package-identity/README.md) |
| パッケージ化アプリのアクティベーション情報取得・永続 ID（証明書更新時の ID 維持）を扱いたい | package-identity | [references/package-identity/README.md](references/package-identity/README.md) |
| Microsoft Store / サイドロード / 非パッケージ配布のどれを選ぶか判断したい | deployment | [references/deployment/README.md](references/deployment/README.md) |
| App Installer ファイルで自動更新付きサイドローディングを構成したい | deployment | [references/deployment/README.md](references/deployment/README.md) |
| Windows App SDK の Bootstrapper API・自己完結型デプロイ・Intune 配布を構成したい | deployment | [references/deployment/README.md](references/deployment/README.md) |
| Windows App SDK ランタイムのインストール済みバージョン確認・削除を行いたい | deployment | [references/deployment/README.md](references/deployment/README.md) |
| パッケージの改ざん検知（Tamper Protection）・パッケージフォールディング・共有パッケージコンテナを理解したい | deployment | [references/deployment/README.md](references/deployment/README.md) |
| SignTool でパッケージに署名・タイムスタンプ・検証したい | code-signing | [references/code-signing/README.md](references/code-signing/README.md) |
| 証明書の種類（自己署名 / OV / EV / Azure Trusted Signing）を選定したい | code-signing | [references/code-signing/README.md](references/code-signing/README.md) |
| CI/CD パイプラインで自動署名を組み込みたい | code-signing | [references/code-signing/README.md](references/code-signing/README.md) |
| SmartScreen の評判メカニズムを理解したい | code-signing | [references/code-signing/README.md](references/code-signing/README.md) |
| Partner Center でアプリを送信・審査に出したい | store-publish | [references/store-publish/README.md](references/store-publish/README.md) |
| 価格・市場・年齢レーティング・ストアリスティングを設定したい | store-publish | [references/store-publish/README.md](references/store-publish/README.md) |
| StoreContext / 送信 API / msstore CLI で購入・公開を自動化し、段階的ロールアウト・分析レポート（利用状況・クラッシュ率）を確認したい | store-publish | [references/store-publish/README.md](references/store-publish/README.md) |
| アドオン送信・製品ページ実験・アトラクト施策・分析レポート群（利用状況・評価・パフォーマンス）を扱いたい | store-publish | [references/store-publish/README.md](references/store-publish/README.md) |
| MSI/EXE アプリや PWA を Store に配布・検証したい | store-publish | [references/store-publish/README.md](references/store-publish/README.md) |

このスキルは MSIX パッケージング・パッケージ ID・配置アーキテクチャ（Windows App SDK の Bootstrapper API・自己完結型デプロイを含む）・コード署名・Microsoft Store 公開フローを扱う。UI コントロール (windows-winui-controls)、レイアウト・スタイル (windows-winui-ui / windows-design)、Windows App SDK のライフサイクル・ウィンドウ・通知等のランタイム API (windows-app-sdk)、データ保存・相互運用・テストなど他の関心事は他の windows-* スキルが担当する。
