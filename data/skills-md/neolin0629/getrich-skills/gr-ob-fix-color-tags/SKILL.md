---
name: gr-ob-fix-color-tags
description: |
  批量把 Obsidian 笔记（如大模型生成的生图 prompt）里的十六进制颜色代码用全角括号包起来（#FFFFFF → （#FFFFFF）），避免 # 被识别为标签。在用户指定的目录下扫描 .md 文件，自动跳过代码块、链接、Frontmatter 及已包裹项。适用于 macOS / Linux。
  触发方式：/gr-ob-fix-color-tags、/gr-fix-color-tags、/转义颜色代码、「fix color tags」
---

# gr-ob-fix-color-tags：Obsidian 颜色代码括号包裹工具

把指定目录下 markdown 文件（如 AI 生图 prompt 库）中的十六进制颜色代码用全角括号包裹，避免 `#` 被 Obsidian 误识别为普通标签。

**执行前先问用户要处理哪个目录**，不要默认全库扫描。

## 处理规则

- **匹配目标**：Prompt 中出现的 6 位或 8 位十六进制颜色代码（如 `#FFFFFF`、`#FFFFFF80`、`#FF5500`）
- **安全过滤（不修改）**：
  - Markdown 代码块（```` ``` ````）与行内代码（`` ` ``）
  - 文档头部 YAML frontmatter 区域（`--- ... ---`）
  - 网址 URL（`https://...`）
  - 普通英文字符标签（如 `#photographer`、`#illustration`）或长哈希
  - 前面已经是全角括号 `（` 的已包裹项（保证重复执行幂等）
- **替换**：`#FFFFFF` → `（#FFFFFF）`
- **范围**：用户指定目录下的 `.md` 文件（仅在内容发生改变时写回文件，保护文件的修改时间 mtime）

---

## 执行脚本（macOS / Linux）

把 `TARGET` 改成用户指定的目录：

```bash
TARGET="./prompts"
find "$TARGET" -type f -name "*.md" -print0 | while IFS= read -r -d '' f; do
    perl -0777 -CASD -Mutf8 -e '
        my $file = $ARGV[0];
        open my $fh, "<:encoding(UTF-8)", $file or exit;
        my $text = do { local $/; <$fh> };
        close $fh;

        my $changed = ($text =~ s{
            \A---.*?---\r?\n (*SKIP)(*FAIL)
            | ```.*?``` (*SKIP)(*FAIL)
            | `[^`\r\n]+` (*SKIP)(*FAIL)
            | https?://\S+ (*SKIP)(*FAIL)
            | (?<![（a-zA-Z0-9_#]) \# ([A-Fa-f0-9]{6}(?:[A-Fa-f0-9]{2})?) (?![a-zA-Z0-9)）])
        }{（#$1）}gsx);

        if ($changed) {
            open my $out, ">:encoding(UTF-8)", $file or exit;
            print $out $text;
            close $out;
            print "✅ $file\n";
        }
    ' "$f"
done
```

---

## 验证

找出还没被包裹的颜色代码，无输出表示处理完成。

```bash
TARGET="./prompts"
find "$TARGET" -type f -name "*.md" -print0 | while IFS= read -r -d '' f; do
    perl -0777 -CASD -Mutf8 -ne '
        while (
            m{
                \A---.*?---\r?\n (*SKIP)(*FAIL)
                | ```.*?``` (*SKIP)(*FAIL)
                | `[^`\r\n]+` (*SKIP)(*FAIL)
                | https?://\S+ (*SKIP)(*FAIL)
                | (?<![（a-zA-Z0-9_#]) \# ([A-Fa-f0-9]{6}(?:[A-Fa-f0-9]{2})?) (?![a-zA-Z0-9)）])
            }gsx
        ) {
            print "$ARGV: 未包裹颜色代码 #$1\n";
        }
    ' "$f"
done
```

---

**已知边界**：
- 只处理 6 到 8 位十六进制，CSS 的 3 位简写（`#FFF`）不在范围内——它和 Obsidian 普通标签无法从形式上区分。
