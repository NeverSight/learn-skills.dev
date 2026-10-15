---
name: windows-ai
description: >
  Windows アプリ開発 (Windows AI Foundry) の AI/ML 統合リファレンス。
  Windows AI APIs、LanguageModel, TextRecognizer, ImageScaler, ImageObjectExtractor,
  ImageObjectRemover, ImageDescriptionGenerator, SemanticSearch, ContentModeration,
  Phi Silica LoRA、Windows ML、ONNX Runtime、execution providers、LearningModel、
  Foundry Local、CLI、REST API、SDK、model catalog、MCP サーバー、App Actions、
  IActionProvider、Agent Launchers、DirectML、IDMLDevice、operators、tensors。
user-invocable: false
---

# Windows AI リファレンス

Windows AI Foundry を中心とした Windows 上の AI/ML 開発機能の公式ドキュメントを蒸留したリファレンス。
組み込み AI API、ローカル ONNX 推論 (Windows ML)、ローカルモデルホスティング (Foundry Local)、
エージェント連携 (MCP / App Actions)、低レベル GPU 推論 (DirectML)、NPU ハードウェア・プロファイリング (Copilot+ PC / WPR / WPA) を扱う。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/windows-ai/
  SKILL.md
  references/
    ai-apis/
      README.md
      ai-dev-gallery.md
      platform-card-click-to-do.md
      platform-card-paint.md
      platform-card-recall.md
      platform-card-windows-studio-effects.md
      faq-cloud-vs-local.md
      choose-your-windows-ai-solution.md
      content-moderation.md
      copilot-plus-developer-guide.md
      device-requirements.md
      faq-using-ai.md
      foundry-toolkit-vscode.md
      phi-silica-structured-output.md
      image-description-generator.md
      image-foreground-extractor.md
      image-generator.md
      image-object-extractor.md
      image-object-remover.md
      image-scaler.md
      language-model-best-practices.md
      language-model.md
      language-model-context.md
      language-model-options.md
      phi-silica-lora.md
      platform-card-image-ai-apis.md
      platform-card-phi-silica.md
      platform-card-ocr.md
      local-llms.md
      recognized-text.md
      responsible-ai.md
      semantic-search.md
      speech-recognition-model.md
      text-intelligence-skills.md
      text-recognizer.md
      video-scaler.md
      troubleshooting.md
    windows-ml/
      README.md
      api-reference.md
      bring-your-own-eps.md
      check-ep-versions.md
      deployment-bootstrap.md
      eps-vs-bring-your-own.md
      execution-provider-catalog.md
      execution-provider-errors.md
      execution-providers-overview.md
      get-started.md
      install-execution-providers.md
      learning-model-binding.md
      learning-model-evaluation-result.md
      learning-model-session.md
      learning-model.md
      legacy-windows-machine-learning.md
      logs.md
      migrate-to-windows-ml.md
      model-catalog-source-schema.md
      model-catalog.md
      model-compilation.md
      model-conversion.md
      models.md
      onnx-runtime-inference.md
      onnx-versions.md
      overview.md
      register-execution-providers.md
      run-genai-onnx-models.md
      samples.md
      select-execution-providers.md
      supported-execution-providers.md
      tutorial.md
      update-eps.md
      webgpu-ep-experimental.md
      winml-cli.md
    foundry-local/
      README.md
      architecture.md
      cache-management.md
      installation-and-cli.md
      model-catalog.md
      overview.md
      rest-api.md
      sdk.md
      winml-package.md
    mcp-app-actions/
      README.md
      mcp-overview.md
      mcp-server-overview.md
      mcp-windows-identity.md
      mcp-mcpb.md
      mcp-manual.md
      mcp-containment.md
      test-mcp-server.md
      quickstart-mcp-host.md
      file-connector.md
      odr-tool.md
      app-actions-overview.md
      actions-get-started.md
      actions-uri-launch.md
      actions-iactionprovider-manual.md
      actions-filter-caller.md
      actions-streaming-text.md
      actions-remote-files.md
      actions-availability.md
      actions-display-ui.md
      actions-json.md
      actions-provider-manifest.md
      actions-test-tool.md
      actions-consume.md
      actions-rai-safety.md
      agent-launchers-overview.md
      agents-get-started.md
      agents-json.md
      agent-workspace.md
      security-consent-model.md
    directml/
      README.md
      api-reference-constants.md
      api-reference-enumerations.md
      api-reference-functions.md
      api-reference-interfaces.md
      api-reference-structures.md
      cuda-on-wsl2.md
      debug-layer.md
      dmlcreatedevice.md
      directml-overview.md
      directml-tools.md
      directmlx.md
      errors-and-device-removal.md
      feature-level-history.md
      fused-operators.md
      gpu-accelerated-training.md
      graphs.md
      helper-functions.md
      idmlbindingtable.md
      idmlcommandrecorder.md
      idmlcompiledoperator.md
      idmloperator.md
      idmloperatorinitializer.md
      onnxruntime-directml.md
      operators.md
      programming-guide.md
      pytorch-directml.md
      resource-lifetime-sync.md
      sample-applications.md
      strides-padding-layout.md
      tensors.md
      tensorflow-directml.md
      tensorflow-directml-faq.md
      uav-barriers.md
      version-history.md
      webnn-overview.md
      webnn-tutorial.md
    npu-devices/
      README.md
      byom-model-sources.md
      gpuview-npu.md
      npu-hardware-overview.md
      onnxruntime-etw-tracing.md
      task-manager-npu.md
      wpr-wpa-npu-profiling.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| LanguageModel でオンデバイス生成 AI (Phi Silica) を呼び出したい | ai-apis | [references/ai-apis/README.md](references/ai-apis/README.md) |
| TextRecognizer / ImageScaler / ImageObjectExtractor / ImageDescriptionGenerator で画像・OCR 処理を実装したい | ai-apis | [references/ai-apis/README.md](references/ai-apis/README.md) |
| SemanticSearch / ContentModeration / responsible AI ガイドラインを適用したい | ai-apis | [references/ai-apis/README.md](references/ai-apis/README.md) |
| Copilot+ PC 向け開発ガイド・AI Dev Gallery・Foundry Toolkit で AI 機能を選定・試作したい | ai-apis | [references/ai-apis/README.md](references/ai-apis/README.md) |
| Windows ML で ONNX モデルをローカル推論したい | windows-ml | [references/windows-ml/README.md](references/windows-ml/README.md) |
| execution providers の選択・登録・インストール・トラブルシューティングをしたい | windows-ml | [references/windows-ml/README.md](references/windows-ml/README.md) |
| LearningModel / LearningModelSession でモデルをバインド・評価したい | windows-ml | [references/windows-ml/README.md](references/windows-ml/README.md) |
| Windows ML の CLI・診断ログ・WebGPU EP を扱いたい | windows-ml | [references/windows-ml/README.md](references/windows-ml/README.md) |
| Foundry Local で LLM をローカルホストしたい | foundry-local | [references/foundry-local/README.md](references/foundry-local/README.md) |
| Foundry Local の CLI / REST API / SDK / model catalog / キャッシュ管理を使いたい | foundry-local | [references/foundry-local/README.md](references/foundry-local/README.md) |
| MCP サーバーを実装・登録・テストしたい | mcp-app-actions | [references/mcp-app-actions/README.md](references/mcp-app-actions/README.md) |
| App Actions / IActionProvider でアプリの機能を外部公開したい | mcp-app-actions | [references/mcp-app-actions/README.md](references/mcp-app-actions/README.md) |
| Agent Launchers / Agent Workspace / セキュリティ同意モデルを実装したい | mcp-app-actions | [references/mcp-app-actions/README.md](references/mcp-app-actions/README.md) |
| DirectML で GPU 推論デバイス・オペレーター・テンソルを直接制御したい | directml | [references/directml/README.md](references/directml/README.md) |
| ONNX Runtime / PyTorch / TensorFlow から DirectML バックエンドを利用したい | directml | [references/directml/README.md](references/directml/README.md) |
| WebNN で GPU/NPU 推論をブラウザ・アプリから呼び出したい | directml | [references/directml/README.md](references/directml/README.md) |
| Copilot+ PC / NPU ハードウェア要件を確認したい | npu-devices | [references/npu-devices/README.md](references/npu-devices/README.md) |
| Task Manager / WPR / WPA / GPUView / ETW で NPU 使用率・推論を計測したい | npu-devices | [references/npu-devices/README.md](references/npu-devices/README.md) |
| 自前 ONNX モデルを NPU 向けに調達・量子化したい (BYOM) | npu-devices | [references/npu-devices/README.md](references/npu-devices/README.md) |

このスキルは Windows AI Foundry 配下の AI/ML 機能（組み込み AI API、ローカル推論、エージェント連携、DirectML、NPU ハードウェア・プロファイリング）のみを扱う。
WinUI コントロールやレイアウト・データバインディングなど UI 実装は windows-winui-controls, windows-winui-ui, windows-app-sdk が担当し、パッケージング・配布は windows-packaging-publish、グラフィックス・メディア描画は windows-graphics-media が担当する。
