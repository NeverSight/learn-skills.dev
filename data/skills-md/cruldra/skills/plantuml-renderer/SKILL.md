---
name: plantuml-renderer
description: Use when the user wants to render PlantUML diagrams from pasted text or files that contain valid PlantUML blocks (such as .puml, .md, or .docx text content), and expects image/text output like svg, png, txt, or utxt via local Java + plantuml.jar.
---

# PlantUML Renderer

将包含 PlantUML 代码的输入渲染为图表文件，支持文本输入与文件输入。

## 使用场景

- 用户明确要求“渲染 PlantUML / 生成 UML 图 / 导出 svg/png/txt/utxt”。
- 用户提供了任意包含有效 PlantUML 代码块（`@startuml ... @enduml`）的内容。
- 输入不一定是 `.puml`，也可以是 Markdown、Word 文档提取文本等。

## 前提条件（必须先检查）

1. 必须验证 Java 可用：
   ```bash
   java -version
   ```
2. 必须确认 JAR 存在：`./assets/plantuml.jar`
3. 如果缺少 Java 或 JAR，停止渲染并明确告知缺失项。

## 标准工作流

1. **接收输入**
   - 支持两类输入：
     - 用户直接粘贴的文本。
     - 用户提供的文件路径。

2. **提取 PlantUML 代码**
   - 从输入中提取完整 `@startuml ... @enduml` 代码块。
   - 若没有任何有效代码块，返回明确错误并提示用户补充有效 PlantUML 代码。

3. **确认输出格式**
   - 询问用户输出格式（如 `svg`、`png`、`txt`、`utxt`）。
   - 用户未指定时，默认使用 `svg`。

4. **构造渲染命令**
   - 命令参数需参考 `./references/cli_man.txt`。
   - 推荐使用 `--format <name>`，也可使用 `--svg` / `--png` / `--txt` / `--utxt`。

5. **执行渲染并生成文件**
   - 默认输出命名规则：
     - 如果输入是文件：`<input_filename>.<format>`
     - 如果输入是粘贴文本：`output.<format>`
   - 若一个输入中有多个 `@startuml` 块，PlantUML 可能按 `_001`、`_002` 追加后缀输出，属于正常行为。

6. **清理中间文件**
   - 渲染完成后，删除过程中产生的所有中间文件，仅保留最终目标输出文件。
   - 需清理的中间文件包括：
     - 为粘贴文本输入临时创建的 `.puml` 文件。
     - PlantUML 渲染过程中产生的临时文件或辅助文件（如 `.cmapx` 等）。
   - **不得删除**的文件：
     - 用户原始输入文件（无论是 `.puml`、`.md` 还是其他格式）。
     - 最终目标输出文件（如 `.svg`、`.png`、`.atxt`、`.utxt`）。
   - 清理前应先确认目标输出文件已成功生成。

7. **ASCII 文本格式特例**
   - 当输出格式是 `txt` 或 `utxt`（纯文本图）时，必须参考：
     - `./references/ascii_guide.md`
   - 输出扩展名通常为 `.atxt` 或 `.utxt`，应在结果说明中明确实际生成文件名。

## 命令模板

以下命令均以技能目录为当前工作目录为前提。

### 文件输入

```bash
java -jar "./assets/plantuml.jar" --format svg "<input_file>"
java -jar "./assets/plantuml.jar" --format png "<input_file>"
java -jar "./assets/plantuml.jar" --format txt "<input_file>"
java -jar "./assets/plantuml.jar" --format utxt "<input_file>"
```

### 文本输入（通过 stdin）

```bash
java -jar "./assets/plantuml.jar" --svg -pipe > "output.svg"
```

如需 ASCII：

```bash
java -jar "./assets/plantuml.jar" --txt -pipe > "output.atxt"
java -jar "./assets/plantuml.jar" --utxt -pipe > "output.utxt"
```

## 关键规则

- 优先保证“提取代码块 + 正确格式 + 成功落盘”三件事。
- 不要假设输入是完整 `.puml` 文件；只要代码块有效就应处理。
- 若命令执行失败，返回原始错误并给出可操作修复建议（Java、JAR 路径、语法错误、Graphviz 依赖等）。
- 对语法检查可使用：
  ```bash
  java -jar "./assets/plantuml.jar" --check-syntax "<input_file_or_dir>"
  ```

## 快速检查清单

- [ ] `java -version` 成功
- [ ] `./assets/plantuml.jar` 存在
- [ ] 已提取至少一个有效 `@startuml ... @enduml`
- [ ] 已确认输出格式（默认 `svg`）
- [ ] 已执行渲染命令并确认输出文件存在
- [ ] 若为 `txt/utxt`，已参考 `./references/ascii_guide.md`
- [ ] 已清理所有中间文件，仅保留目标输出文件
