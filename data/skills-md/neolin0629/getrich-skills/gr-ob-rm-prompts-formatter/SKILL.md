---
name: gr-ob-rm-prompts-formatter
description: |
  批量删除 Obsidian 笔记开头的 YAML frontmatter（Obsidian 属性区，`---` 包起来的那段），只保留正文。默认处理 prompts/ 目录下的 .md 文件，可指定其他目录。适用于 macOS / Linux。
  触发方式：/gr-ob-rm-prompts-formatter、/删除 frontmatter、/清理属性、「remove frontmatter」
---

# gr-ob-rm-prompts-formatter：批量删除 frontmatter

删除指定目录下 Markdown 文件开头的 YAML frontmatter，只保留正文。

**这是破坏性操作，执行前必须做两件事：**

1. 确认要处理的目标目录（默认 `prompts/`），避免误选全局目录。
2. 确认目录在 Git 托管中且工作区干净，或预先完成备份。执行后用 `git diff` 复查。

## 处理规则

- **严格行首匹配**：仅删除文件**最开头**（兼容可选 UTF-8 BOM）由单独成行 `---` 包裹的 YAML 区，连同其后紧随的空白行一并清除。
- **行内破折号安全**：frontmatter 内容中出现 `---`（如提示词标题、分隔符文本）绝不会误判提前截断。
- **零副作用跳过**：没有 frontmatter 的文件完全不作修改，严格保留文件修改时间（mtime）与 inode，不污染 Obsidian 同步。
- **正文保护**：正文内部的 `---` 分割线完全保留。

---

## 第一步：预览（只读安全检查）

把 `TARGET` 改成目标目录。此步骤仅在终端预览将被删除的 frontmatter 内容，不修改任何文件。

```bash
TARGET="./prompts"
find "$TARGET" -type f -name "*.md" -exec perl -0777 -ne '
    print "── $ARGV\n$1\n\n" if /\A(?:\xEF\xBB\xBF)?---[ \t]*\r?\n(.*?)^---[ \t]*(?:\r?\n|$)/ms;
' {} +
```

> **说明**：无任何输出说明目录下没有包含 frontmatter 的文件，无需后续操作。

---

## 第二步：执行删除

仅当文件首部存在 frontmatter 时才会写入修改；未包含属性区的文件原封不动跳过，并精准报告处理结果。

```bash
TARGET="./prompts"
find "$TARGET" -type f -name "*.md" -exec perl -0777 -e '
for my $f (@ARGV) {
    open my $fh, "<:raw", $f or next;
    my $c = do { local $/; <$fh> };
    close $fh;
    if ($c =~ s/\A(?:\xEF\xBB\xBF)?---[ \t]*\r?\n.*?^---[ \t]*(?:\r?\n|$)(?:[ \t]*\r?\n)*//ms) {
        open my $out, ">:raw", $f or next;
        print $out $c;
        close $out;
        print "✅ $f\n";
    }
}
' {} +
```

---

## 第三步：验证

1. **复查预览**：重新运行第一步的预览命令，若终端无任何输出，说明已全部清理干净。
2. **Git 复查**：运行 `git diff` 抽样核验，确认仅清除了头部的属性块，正文无误删。

---

## 已知风险与边界

1. **正文首行即为分割线**：若笔记本身**没有** frontmatter，但正文第 1 行碰巧也是 `---` 分割线，且正文后续还有单独成行的 `---`，会被视作属性块被删除。执行前请务必通过「第一步：预览」进行排查。
2. **不支持 `...` 结束符**：仅识别 YAML 规范及 Obsidian 默认的 `---` 闭合线，不支持非标准的 `...`（Obsidian 亦不支持）。
