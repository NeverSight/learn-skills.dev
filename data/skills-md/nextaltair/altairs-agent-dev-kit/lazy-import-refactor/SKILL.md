---
name: lazy-import-refactor
description: "Refactor module-level imports of heavy native dependencies (torch, tensorflow, jax) to function-internal lazy imports. Use when a library import triggers SIGSEGV or slow startup in environments where the native dep cannot fully initialize (e.g., CUDA driver absent, triton C-extension segfault, missing GPU). Predicts test-side effects from removed module attributes."
metadata:
  short-description: "torch/tensorflow 等 heavy native dep の module-level → function-internal lazy import 化、test 副作用予測まで含む"
allowed-tools:
  - Grep
  - Read
  - Edit
  - Bash
---

# Lazy Import Refactor

Module-level `import torch` / `import tensorflow` 等 heavy native dependency を function-internal lazy import に移行するための手順 + test 副作用予測 + CI-equivalent 検証要件。

## When to Use

- `import <library>` 単体で **SIGSEGV** (CUDA driver 不在 + triton C-ext segfault 等)
- 起動時間短縮のため重い import を遅延させたい
- WebAPI 専用利用者に heavy native dep を不要にしたい
- 上流 lib の lazy import 化を下流プロジェクトから依頼する設計検討

該当した実例: Linux + triton + CUDA driver 不在で `import <ML ライブラリ>` が SIGSEGV → torch / transformers の module-level import 排除で恒久解消したケースがある

## Step 1: Pre-flight grep — 影響範囲完全洗い出し

**Module-level import 全件 (col 0 のみ):**

```bash
find src -name "*.py" | while read f; do
  awk -v fn="$f" '/^(import torch|from torch|import torchvision|from torchvision|import tensorflow|from tensorflow)/{print fn":"NR":"$0}' "$f"
done
```

**テスト側の module attribute patch 全件:**

```bash
find tests -name "*.py" | while read f; do
  awk -v fn="$f" '/@patch.*\.(torch|tensorflow|jax)|patch\.object.*\.(torch|tensorflow|jax)/{print fn":"NR":"$0}' "$f"
done
```

Module-level import を関数内に移すと、その module の `module.torch` 属性が消滅する。**test 側で `@patch("path.to.module.torch")` を使用している箇所は全件 AttributeError で壊れる** ため、事前 grep が必須。

## Step 2: Refactor パターン

```python
# Before (module-level)
import torch

class Foo:
    def bar(self, x: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            ...

# After (TYPE_CHECKING + function-internal)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import torch


class Foo:
    def bar(self, x: torch.Tensor) -> torch.Tensor:
        import torch  # lazy load
        with torch.no_grad():
            ...
```

**必須事項:**
- `from __future__ import annotations` を冒頭に追加 (型ヒントを文字列化、runtime evaluation 回避)
- runtime で使う関数の冒頭で `import torch` を再宣言
- module-level の bare `import torch` は削除

## Step 3: Test 副作用対応

```python
# Before
@patch("your_package.core.heavy_deps.torch")
def test_foo(mock_torch):
    ...

# After
def test_foo(monkeypatch):
    import sys
    from unittest.mock import MagicMock
    mock_torch = MagicMock()
    monkeypatch.setitem(sys.modules, "torch", mock_torch)
    ...
```

詳細パターン (context manager mock, cuda.is_available, getattr-based access 等) は [test-side-effects.md](test-side-effects.md) 参照。

## Step 4: Verification — CI-equivalent filter で必ず検証

プロジェクトの testing ルール（例: [`rules/testing.md`](../../rules/testing.md) の "CI-equivalent filter で local 検証する" セクション）を参照。

**`-m unit` 等の短縮 filter では検証不充分** (本 SKILL の存在理由 — サブモジュール側の marker 差分が短縮 filter では再現できず下流 CI で初検出された実例がある)。CI workflow の filter を完全一致で local 実行する。

モノレポ内の独立パッケージ (submodule 等) の場合:

```bash
cd <package-path>
uv run pytest -m "not downloads_and_runs_model and not calls_real_webapi"
```

## Step 5: Cross-repo PR 順序

submodule で利用される lib の場合:

1. lib 側で fix + CI-equivalent test pass を確認
2. lib 側 PR 起票 → merge 待ち
3. **merge 後**、下流プロジェクトで submodule pin 更新 PR 起票

順序を逆にすると下流 CI で初検出され、hot-fix PR 連鎖が必要になる。

`gh pr create` 実行時、kit の submodule pre-PR check hook (`hook_pre_pr_submodule_check.py`) が導入されていれば、submodule 変更を含む PR で CI-equivalent test 実行確認を要求する (bypass は `CI-EQUIV-TESTED` marker comment)。

## Anti-patterns

- **module-level の上位 lib import**: `from transformers.models.clip import CLIPProcessor` は transformers が torch を eager load するため lazy 化が必要。直接 `import torch` でなくても heavy native dep を引き連れる import は全て対象
- **TYPE_CHECKING 内のみで対応**: `cast(<heavy_lib>.Type, ...)` や `isinstance(x, <heavy_lib>.Type)` のような runtime 評価が必要な箇所では完全には escape できない → `from __future__ import annotations` で型ヒントの string 化と、関数内 `import` の両方を必須とする
- **subprocess regression test の欠落**: lazy import 化が効いているか検証する test を同 PR で追加する。fresh interpreter での `import <lib>; assert 'torch' not in sys.modules` パターンを推奨 (subprocess 経由で session 汚染を回避)
- **`-m unit` での local 検証**: CI が独立 marker (`standard` 等) を使う場合、必ず CI 設定の filter で検証する
