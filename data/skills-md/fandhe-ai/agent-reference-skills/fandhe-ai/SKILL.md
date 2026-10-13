---
name: fandhe-ai
description: >
  Rust 製 AI/ML ライブラリ fandhe-ai のリファレンス。Burn / candle / tch 非依存の from-scratch 実装。
  compat::Sequential, compat::array, tape(), tape_for(), Tape, Var, Tensor,
  Gradients, LinearVars, Device (Cpu / Cuda / Metal)。
  tensor-core の kernel fusion, FusionPlan, BackendOps。dynamic-tape autodiff。
  cfg ベースのバックエンド構成・数値一致契約。ONNX / safetensors 相互運用。
  guardrail / self-repair CLI。
user-invocable: false
---

# fandhe-ai

fandhe-ai は Rust 製 AI/ML ライブラリ。Burn / candle / tch などの既存フレームワークに依存せず、テンソル・autodiff・kernel fusion・計算カーネル・バックエンド抽象層を完全自作コアとして実装している。内部は 10 クレートに分かれるが、利用者が直接触れるのは `fandhe-ai` クレート（リポジトリ内パスは `crates/facade`）のみで、公式ドキュメントは「`fandhe-ai` crate のみが supported public API surface、内部クレートの直接利用は非サポート」と明言している。

**注意** — `guardrail` は AI 生成 changeset を判定する CI 用 CLI（check / eval）であり、`openai-agents` / `anthropic-prompt-eval` / `openai-evals-tuning` が扱う LLM 出力の guardrail / eval とは別物。

**他スキルとの使い分け** — `Device::Cuda` / `Device::Metal` を含むバックエンド抽象は fandhe-ai 独自の Rust API であり、CUDA C++ / PTX / CUTLASS を調べる場合は `nvidia-cuda`、MSL / MPSGraph / MLX を調べる場合は `apple-silicon`、HIP / ROCm を調べる場合は `amd-rocm` を参照すること。`Tensor` / autodiff / tape も同様に fandhe-ai 独自の Rust API であり、`apple-ml` の `MLMultiArray`、`apple-silicon`（MLX）の `mx.array` とは別物。fandhe-ai は `fandhe-frontend`（Rust 製フロントエンドフレームワーク）・`fandhe-backend`（Rust 製バックエンド HTTP サーバーフレームワーク）とは同じ Fandhe-AI org の別ライブラリで、API・対象領域とも無関係。

公式ドキュメント: https://fandhe-ai.github.io/fandhe-ai/ / リポジトリ: https://github.com/Fandhe-AI/fandhe-ai

## ディレクトリ構成

```text
skills/fandhe-ai/
  SKILL.md
  references/
    getting-started/
      README.md
      overview.md
      installation.md
      quick-start.md
      crate-layout.md
    guides/
      README.md
      backends.md
      numerical-parity.md
      performance.md
      interop.md
    api/
      README.md
      tape.md
      var.md
      tensor.md
      gradients.md
      linear-vars.md
      device.md
      errors.md
      compat-sequential.md
      compat-array.md
    internals/
      README.md
      tensor-core.md
      tensor-core-fusion.md
      autodiff.md
      backend-cpu.md
      backend-cuda.md
      backend-metal.md
      onnx-interop.md
      bench-harness.md
    tooling/
      README.md
      guardrail.md
      self-repair.md
      config.md
  samples/
    README.md
    getting-started.md
    array-shapes.md
    backend-switching.md
    training-loop.md
    inference.md
    gemm-bench.md
  scripts/
    README.md
    install.md
    dev.md
    cli.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す（`internals/*` は公式が非サポートと明言する内部クレートのアーキテクチャ解説であり、通常の利用手順は `api/` を参照する）
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
| --- | --- | --- |
| fandhe-ai とは何か、10 クレート構成・設計思想、インストール手順、`compat::array` + `compat::Sequential` の最小例、公開/未公開クレート一覧と facade → fandhe-ai の対応を知りたい | getting-started | [references/getting-started/README.md](references/getting-started/README.md) |
| cfg ベースのバックエンド切替と fail-fast 設計、バックエンド間の数値一致契約、kernel fusion を含む性能の考え方、ONNX / safetensors 相互運用のサポート境界を知りたい | guides | [references/guides/README.md](references/guides/README.md) |
| `tape()` / `tape_for(Device)` / `Tape`、`Var`、`Tensor`、`Gradients`、`LinearVars`、`Device`（Cpu / Cuda / Metal）、`AutodiffError` / `BackendError`、`compat::Sequential` / `compat::array` の型・API を知りたい | api | [references/api/README.md](references/api/README.md) |
| `tensor-core`（buffer/device/dispatch/memory_stats/pool/typed, `BackendOps`）や `FusionPlan` / `FusedOpKind` などの kernel fusion 表現、dynamic-tape autodiff の内部実装、CPU/CUDA/Metal 各バックエンドクレートの実装構造、未公開の `onnx-interop` / `bench-harness` クレートを知りたい（いずれも公式非サポートの内部 API） | internals | [references/internals/README.md](references/internals/README.md) |
| CI changeset 判定 CLI `guardrail`（check / eval）、`self-repair`（run / verify-log）、`guardrail.toml` / `policy-exclusion.toml` と判定/評価レポート JSON の形式を知りたい | tooling | [references/tooling/README.md](references/tooling/README.md) |
| `compat::array` + `compat::Sequential` の最小推論、shape 確認、`tape_for(Device)` でのバックエンド明示指定とフォールバック、手動 SGD 学習ループ、`predict()` と `Tape` + `forward()` の推論経路比較、`Var::matmul`（GEMM）の簡易ベンチなど典型的な使い方を知りたい | samples | [samples/README.md](samples/README.md) |
| crate 導入コマンド（crates.io / Git / Path 依存）、サンプル実行・ビルド・テスト・静的検査、`guardrail` / `self-repair` バイナリのコマンドを知りたい | scripts | [scripts/README.md](scripts/README.md) |
